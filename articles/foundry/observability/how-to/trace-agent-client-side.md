---
title: "Add client-side tracing to Foundry agents"
description: "Instrument AI agents with OpenTelemetry client-side tracing using the Microsoft Foundry SDK. Export traces to Azure Monitor or the console in Python and C#."
ai-usage: ai-assisted
author: aahill
ms.author: aahi
ms.reviewer: lagayhar
ms.date: 03/23/2026
ms.service: azure-ai-foundry
ms.topic: how-to
---

# Add client-side tracing to Foundry agents (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Microsoft Foundry automatically captures server-side traces for agents running in the portal. Client-side tracing extends that visibility into your own application code. By instrumenting your agent application with OpenTelemetry, you can capture spans for model calls, tool invocations, and custom logic — then export them to Azure Monitor Application Insights or the console for debugging.

In this article, you learn how to:

- Install the required OpenTelemetry tracing packages.
- Enable GenAI tracing instrumentation for agent applications.
- Export traces to Azure Monitor or the console.
- Enable content recording to capture message contents.
- Enable trace context propagation for distributed tracing (Python).
- Trace custom functions.

## Prerequisites

- A [Foundry project](../../how-to/create-projects.md) with an [Application Insights resource connected](trace-agent-setup.md#connect-application-insights-to-your-foundry-project).
- An AI model deployed to the project. Note the deployment name.
- [Azure CLI](/cli/azure/install-azure-cli) installed. Sign in by running `az login`.
- Contributor or higher role on the Foundry project. To view traces, you also need [Log Analytics Reader](/azure/azure-monitor/logs/manage-access?tabs=portal#log-analytics-reader) on the connected Application Insights resource. For more information, see [Role-based access control in Foundry](../../concepts/rbac-foundry.md).
- The following environment variables set with your own values:

  | Variable | Description |
  | --- | --- |
  | `FOUNDRY_PROJECT_ENDPOINT` | Your Foundry project endpoint URL. Find it on the project **Overview** page in the Foundry portal. |
  | `FOUNDRY_MODEL_NAME` | The deployment name of an AI model in your project. Find it under **Models** in the Foundry portal. |

### Language-specific prerequisites

# [Python](#tab/python)

- Python 3.9 or later.
- The `azure-ai-projects` package version 2.0.0 or later.

# [C#](#tab/csharp)

- .NET 8.0 or later.
- The `Azure.AI.Projects` NuGet package.

---

## Install tracing packages

# [Python](#tab/python)

Install the Microsoft Foundry SDK, OpenTelemetry, and the Azure Monitor exporter:

```bash
pip install azure-ai-projects azure-identity opentelemetry-sdk azure-core-tracing-opentelemetry azure-monitor-opentelemetry
```

For console-only or OTLP export (for example, [Aspire Dashboard](/dotnet/aspire/fundamentals/dashboard/standalone)), install the OTLP exporter:

```bash
pip install opentelemetry-exporter-otlp
```

# [C#](#tab/csharp)

Add the required NuGet packages:

```dotnetcli
dotnet add package Azure.AI.Projects --prerelease
dotnet add package Azure.AI.Projects.Agents --prerelease
dotnet add package Azure.Identity
dotnet add package Azure.Monitor.OpenTelemetry.Exporter
dotnet add package OpenTelemetry.Exporter.Console
```

---

## Enable GenAI tracing

GenAI tracing instrumentation is an experimental preview feature. Spans, attributes, and events might change in future versions. You must explicitly opt in before tracing is active.

# [Python](#tab/python)

Set the `AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING` environment variable to `true` **before** calling `AIProjectInstrumentor().instrument()`:

```python
import os

os.environ["AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING"] = "true"

from azure.ai.projects.telemetry import AIProjectInstrumentor

# Enable instrumentation
AIProjectInstrumentor().instrument()
```

If the variable isn't set or isn't `true` (case-insensitive), tracing instrumentation isn't enabled and a warning is logged.

# [C#](#tab/csharp)

Use an `AppContext` switch or the same environment variable:

```csharp
// Enable GenAI tracing
AppContext.SetSwitch("Azure.Experimental.EnableGenAITracing", true);
```

If both the `AppContext` switch and the environment variable are set, the `AppContext` switch takes priority.

---

## Export traces to Azure Monitor

Send traces to [Azure Application Insights](/azure/azure-monitor/app/app-insights-overview) so they appear in the Foundry portal's **Traces** view and in Azure Monitor.

# [Python](#tab/python)

```python
import os

os.environ["AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING"] = "true"

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from azure.identity import DefaultAzureCredential
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=endpoint, credential=credential) as project,
):
    # Get the Application Insights connection string from the project
    connection_string = project.telemetry.get_application_insights_connection_string()
    configure_azure_monitor(connection_string=connection_string)

    tracer = trace.get_tracer(__name__)

    with tracer.start_as_current_span("agent-tracing-scenario"):
        with project.get_openai_client() as openai:
            # Create an agent
            agent = project.agents.create_version(
                agent_name="MyAgent",
                definition=PromptAgentDefinition(
                    model=os.environ["FOUNDRY_MODEL_NAME"],
                    instructions="You are a helpful assistant.",
                ),
            )
            print(f"Agent created (id: {agent.id}, name: {agent.name})")

            # Create a conversation and get a response
            conversation = openai.conversations.create()
            response = openai.responses.create(
                conversation=conversation.id,
                extra_body={"agent_reference": {"name": agent.name, "id": agent.id, "type": "agent_reference"}},
                input="What is the largest city in France?",
            )
            print(f"Response: {response.output_text}")

            # Clean up
            openai.conversations.delete(conversation_id=conversation.id)
            project.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
```

Reference: [`AIProjectClient`](/python/api/azure-ai-projects/azure.ai.projects.aiprojectclient), [`DefaultAzureCredential`](/python/api/azure-identity/azure.identity.defaultazurecredential), [`configure_azure_monitor`](/python/api/azure-monitor-opentelemetry/azure.monitor.opentelemetry)

# [C#](#tab/csharp)

```csharp
using Azure.AI.Projects;
using Azure.AI.Projects.Agents;
using Azure.Identity;
using Azure.Monitor.OpenTelemetry.Exporter;
using OpenTelemetry;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;

var projectEndpoint = Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT");
var modelName = Environment.GetEnvironmentVariable("FOUNDRY_MODEL_NAME");

// Enable GenAI tracing
AppContext.SetSwitch("Azure.Experimental.EnableGenAITracing", true);

AIProjectClient projectClient = new(
    endpoint: new Uri(projectEndpoint),
    tokenProvider: new DefaultAzureCredential());

// Get the Application Insights connection string from the project
var connectionString = await projectClient.Telemetry
    .GetApplicationInsightsConnectionStringAsync();

// The Azure Monitor exporter reads this environment variable automatically
Environment.SetEnvironmentVariable(
    "APPLICATIONINSIGHTS_CONNECTION_STRING", connectionString);

// Configure OpenTelemetry with Azure Monitor exporter
var tracerProvider = Sdk.CreateTracerProviderBuilder()
    .AddSource("Azure.AI.Projects.*")
    .SetResourceBuilder(
        ResourceBuilder.CreateDefault().AddService("AgentTracingSample"))
    .AddAzureMonitorTraceExporter()
    .Build();

using (tracerProvider)
{
    // Create an agent
    DeclarativeAgentDefinition agentDefinition = new(model: modelName)
    {
        Instructions = "You are a helpful assistant."
    };
    AgentVersion agent = await projectClient.Agents.CreateAgentVersionAsync(
        agentName: "myAgent",
        options: new(agentDefinition));
    Console.WriteLine(
        $"Agent created (id: {agent.Id}, name: {agent.Name})");

    // Clean up
    projectClient.Agents.DeleteAgentVersion(
        agentName: agent.Name, agentVersion: agent.Version);
}
```

Reference: [`AIProjectClient`](/dotnet/api/azure.ai.projects.aiprojectclient), [`DefaultAzureCredential`](/dotnet/api/azure.identity.defaultazurecredential), [`Sdk.CreateTracerProviderBuilder`](https://github.com/open-telemetry/opentelemetry-dotnet/tree/main/src/OpenTelemetry)

---

> [!NOTE]
> To correlate traces with a specific agent in the Foundry portal, include the `agent_reference` with both `name` and `id` in your `responses.create()` call (as shown in the Python sample above). Traces typically appear within 2-5 minutes.

## Export traces to the console

Console export is useful for local debugging. Traces print directly to standard output.

# [Python](#tab/python)

```python
import os

os.environ["AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING"] = "true"

from azure.ai.projects.telemetry import AIProjectInstrumentor
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

# Set up console tracing
tracer_provider = TracerProvider()
tracer_provider.add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(tracer_provider)

# Enable instrumentation
AIProjectInstrumentor().instrument()

tracer = trace.get_tracer(__name__)
```

You can also use [Aspire Dashboard](/dotnet/aspire/fundamentals/dashboard/standalone) as a local OTLP-compatible viewer. Install the OTLP exporter (`pip install opentelemetry-exporter-otlp`) and configure it as the exporter instead of `ConsoleSpanExporter`.

Reference: [`AIProjectInstrumentor`](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects#tracing), [`ConsoleSpanExporter`](https://opentelemetry-python.readthedocs.io/en/latest/sdk/trace.export.html)

# [C#](#tab/csharp)

```csharp
using Azure.AI.Projects;
using Azure.Identity;
using OpenTelemetry;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;

// Enable GenAI tracing
AppContext.SetSwitch("Azure.Experimental.EnableGenAITracing", true);

// Configure OpenTelemetry with console exporter
var tracerProvider = Sdk.CreateTracerProviderBuilder()
    .AddSource("Azure.AI.Projects.*")
    .SetResourceBuilder(
        ResourceBuilder.CreateDefault().AddService("AgentTracingSample"))
    .AddConsoleExporter()
    .Build();

using (tracerProvider)
{
    // Agent operations emit traces to the console
}
```

---

## Enable content recording

Content recording captures message contents and tool call arguments in traces. This data might include sensitive user information.

> [!CAUTION]
> Content recording captures user messages, tool call arguments, and model outputs. Only enable this setting in development environments. Don't enable content recording in production unless your compliance and privacy requirements allow it.

# [Python](#tab/python)

Set the environment variable before instrumenting:

```python
import os

os.environ["OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT"] = "true"
```

> [!IMPORTANT]
> This variable controls recording only for built-in traces. When you use the `@trace_function` decorator on your own functions, all parameters and return values are always traced regardless of this setting.

# [C#](#tab/csharp)

Use an `AppContext` switch or the environment variable:

```csharp
// Enable content recording
AppContext.SetSwitch("Azure.Experimental.TraceGenAIMessageContent", true);
```

Or set the `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` environment variable to `true`. The `AppContext` switch takes priority.

---

## Enable trace context propagation (Python)

Trace context propagation allows client-side spans to correlate with server-side spans from Azure OpenAI and other Azure services. When enabled, the SDK automatically injects [W3C Trace Context](https://www.w3.org/TR/trace-context/) headers (`traceparent` and `tracestate`) into HTTP requests made by OpenAI clients obtained via `get_openai_client()`.

Trace context propagation is **enabled by default** when tracing is enabled. To disable it, set the `AZURE_TRACING_GEN_AI_ENABLE_TRACE_CONTEXT_PROPAGATION` environment variable to `false`, or pass the parameter directly:

```python
from azure.ai.projects.telemetry import AIProjectInstrumentor

# Disable trace context propagation
AIProjectInstrumentor().instrument(enable_trace_context_propagation=False)
```

Changes to this setting only affect OpenAI clients obtained via `get_openai_client()` **after** the change. Previously acquired clients aren't affected.

### Control baggage propagation

By default, only `traceparent` and `tracestate` headers are propagated. To also include the `baggage` header, set `AZURE_TRACING_GEN_AI_TRACE_CONTEXT_PROPAGATION_INCLUDE_BAGGAGE` to `true`.

> [!IMPORTANT]
> The `baggage` header can contain arbitrary key-value pairs, including user identifiers, session information, or other potentially sensitive data. Before enabling baggage propagation:
>
> - Audit what data your application and third-party libraries add to OpenTelemetry baggage.
> - Understand that baggage is sent to Azure OpenAI and might be logged by Azure services.
> - Never add sensitive information to baggage when propagation is enabled.

> [!NOTE]
> The C# SDK relies on standard .NET `System.Diagnostics.Activity` propagation. Explicit per-request trace context injection isn't exposed as a separate SDK feature.

## Trace custom functions

### Python — use the `@trace_function` decorator

The `trace_function` decorator creates an OpenTelemetry span for each call to your function. Parameters are recorded as `code.function.parameter.<name>` and the return value as `code.function.return.value`.

```python
from azure.ai.projects.telemetry import trace_function

@trace_function
def fetch_weather(location: str) -> str:
    """Get the current weather for a location."""
    return f"Weather in {location}: sunny, 72°F"
```

The decorator handles basic data types (`str`, `int`, `float`, `bool`) and collections (`list`, `dict`, `tuple`, `set`). Object types are omitted.

> [!NOTE]
> The `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` environment variable doesn't affect custom function tracing. The `@trace_function` decorator always traces parameters and return values.

### C# — use `ActivitySource` manually

The C# SDK doesn't include a tracing decorator. Use the standard .NET `ActivitySource` to instrument your own functions:

```csharp
using System.Diagnostics;

// Define a custom activity source
private static readonly ActivitySource s_source = new("MyApp.CustomFunctions");

string FetchWeather(string location)
{
    using var activity = s_source.StartActivity("FetchWeather");
    activity?.SetTag("input.location", location);

    var result = $"Weather in {location}: sunny, 72°F";
    activity?.SetTag("output", result);
    return result;
}
```

Register your custom source alongside the SDK source in your tracer provider:

```csharp
var tracerProvider = Sdk.CreateTracerProviderBuilder()
    .AddSource("Azure.AI.Projects.*")
    .AddSource("MyApp.CustomFunctions")
    .SetResourceBuilder(
        ResourceBuilder.CreateDefault().AddService("MyApp"))
    .AddConsoleExporter()
    .Build();
```

## Add custom attributes to spans (Python)

Create a custom `SpanProcessor` to inject metadata like session IDs into every span:

```python
from opentelemetry.sdk.trace import SpanProcessor, ReadableSpan
from opentelemetry.trace import Span

class CustomAttributeSpanProcessor(SpanProcessor):
    def on_start(self, span: Span, parent_context=None):
        span.set_attribute("session.id", "user-session-abc")

    def on_end(self, span: ReadableSpan):
        pass
```

Register the processor with the global tracer provider:

```python
from typing import cast
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

provider = cast(TracerProvider, trace.get_tracer_provider())
provider.add_span_processor(CustomAttributeSpanProcessor())
```

## Control tracing behavior with environment variables

The following table lists all environment variables you can use to configure tracing behavior:

| Variable | Language | Default | Description |
| --- | --- | --- | --- |
| `AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING` | Python, C# | `false` | Enable GenAI tracing instrumentation. |
| `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` | Python, C# | `false` | Capture message contents and tool call parameters. |
| `AZURE_TRACING_GEN_AI_ENABLE_TRACE_CONTEXT_PROPAGATION` | Python | `true`* | Inject W3C Trace Context headers into requests. |
| `AZURE_TRACING_GEN_AI_TRACE_CONTEXT_PROPAGATION_INCLUDE_BAGGAGE` | Python | `false` | Include the `baggage` header in trace context propagation. |
| `AZURE_TRACING_GEN_AI_INSTRUMENT_RESPONSES_API` | Python | `true` | Auto-instrument Responses and Conversations APIs. |
| `AZURE_TRACING_GEN_AI_INCLUDE_BINARY_DATA` | Python | `false` | Include image and file data in spans (not just file IDs). |

\* Default is `true` when tracing is enabled.

For the full list of environment variables and their behavior, see [Tracing in the Azure AI Projects SDK README](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/README.md#tracing).

> [!WARNING]
> Enabling `AZURE_TRACING_GEN_AI_INCLUDE_BINARY_DATA` can significantly increase trace payload size. Some tracing backends have limitations on the maximum size of span data. Verify that your observability backend supports the expected payload sizes before enabling this setting.

## Security and privacy

Client-side tracing can capture sensitive information. Follow these practices to reduce risk:

- **Content recording**: Captures user inputs, model responses, and tool call arguments. Disable in production unless required.
- **Baggage propagation**: Can expose PII and session data. Disabled by default.
- **Trace context propagation**: Sends trace IDs to Azure services. If compliance requirements prohibit sharing trace identifiers, disable it.
- **Secrets**: Don't store secrets, credentials, or tokens in prompts, tool arguments, or span attributes.
- **Access control**: Treat trace data as production telemetry. Apply the same access controls and retention policies you use for logs and metrics.

## Troubleshooting

| Issue | Resolution |
| --- | --- |
| Tracing doesn't produce any spans | Verify `AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING` is set to `true` **before** calling `AIProjectInstrumentor().instrument()` (Python) or before creating the tracer provider (C#). |
| Message content doesn't appear in spans | Set `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` to `true`. |
| Traces don't appear in Azure Monitor | Verify the Application Insights connection string is correct and the resource is accessible. Check that your account has the [Log Analytics Reader role](/azure/azure-monitor/logs/manage-access?tabs=portal#log-analytics-reader). |
| Client-side and server-side spans aren't correlated | (Python) Verify trace context propagation is enabled and that OpenAI clients are obtained via `get_openai_client()` **after** instrumentation. |
| Traces appear with a delay | Traces typically take 2-5 minutes to appear in the Foundry portal and Azure Monitor. Wait and refresh. |

## Related content

- [Agent tracing overview (preview)](../concepts/trace-agent-concept.md)
- [Set up tracing in Microsoft Foundry](trace-agent-setup.md)
- [Configure tracing for agent frameworks](trace-agent-framework.md)
- [Monitor agents with the Agent Monitoring Dashboard](how-to-monitor-agents-dashboard.md)
