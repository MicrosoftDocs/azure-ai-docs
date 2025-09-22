---
title: View Trace Results for AI Agents in Azure AI Foundry
titleSuffix: Azure AI Foundry
description: View trace results for AI agents using Azure AI Foundry SDK and OpenTelemetry. Learn to see execution traces, debug performance, and monitor AI agent behavior step-by-step.
author: lgayhardt
ms.author: lagayhar
ms.reviewer: ychen
ms.date: 09/18/2025
ms.service: azure-ai-foundry
ms.topic: how-to
ai-usage: ai-assisted
ms.custom: references_regions
---

# View trace results for AI agents in Azure AI Foundry (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Learn how to view trace results for AI agents in Azure AI Foundry. See execution traces, analyze behavior, and debug performance issues using the SDK with OpenTelemetry and Azure Monitor.

In this article, you learn how to:

- View agent traces in the Agents playground.
- Interpret spans (steps, tool calls, nested operations).
- Enable metrics for AI quality and safety.
- Retrieve traces for past threads.
- Plan optimization next steps.

Determining the reasoning behind your agent's executions is important for troubleshooting and debugging. However, it can be difficult for complex agents for many reasons:

- There could be a high number of steps involved in generating a response, making it hard to keep track of all of them.
- The sequence of steps might vary based on user input.
- The inputs/outputs at each stage might be long and deserve more detailed inspection.
- Each step of an agent's runtime might also involve nesting. For example, an agent might invoke a tool, which uses another process, which then invokes another tool. If you notice strange or incorrect output from a top-level agent run, it might be difficult to determine exactly where in the execution the issue was introduced.

Trace results solve this by allowing you to view the inputs and outputs of each primitive involved in a particular agent run, displayed in the order they were invoked, making it easy to understand and debug your AI agent's behavior.

## Trace key concepts overview

Here's a brief overview of key concepts before getting started:

| Key concepts             | Description            |
|---------------------|-----------------------------------------------------------------|
| Traces              | Traces capture the journey of a request or workflow through your application by recording events and state changes (function calls, values, system events). See [OpenTelemetry Traces](https://opentelemetry.io/docs/concepts/signals/traces/). |
| Spans               | Spans are the building blocks of traces, representing single operations within a trace. Each span captures start and end times, attributes, and can be nested to show hierarchical relationships, allowing you to see the full call stack and sequence of operations.                                                                                         |
| Attributes          | Attributes are key-value pairs attached to traces and spans, providing contextual metadata such as function parameters, return values, or custom annotations. These enrich trace data making it more informative and useful for analysis.                                                                                                 |
| Semantic conventions| OpenTelemetry defines semantic conventions to standardize names and formats for trace data attributes, making it easier to interpret and analyze across tools and platforms. To learn more, see [OpenTelemetry's Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/).                  |
| Trace exporters     | Trace exporters send trace data to backend systems for storage and analysis. Azure AI supports exporting traces to Azure Monitor and other OpenTelemetry-compatible platforms, enabling integration with various observability tools.   |

### Best practices

- Use consistent span attributes.
- Correlate evaluation run IDs for quality + performance analysis.
- Redact sensitive content; avoid storing secrets in attributes.
                                                                          

## Setup tracing in Azure AI Foundry SDK

For chat completions or building agents with Azure AI Foundry, install:

```bash
pip install azure-ai-projects azure-identity
```

To instrument tracing, you need to install the following instrumentation libraries:

```bash
pip install azure-monitor-opentelemetry opentelemetry-sdk
```

To view traces in Azure AI Foundry, you need to connect an Application Insights resource to your Azure AI Foundry project.

1. Navigate to **Tracing** in the left navigation pane of the Azure AI Foundry portal.
2. Create a new Application Insights resource if you don't already have one.
3. Connect the resource to your AI Foundry project.

## Instrument tracing in your code

To trace the content of chat messages, set the `AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED` environment variable to true (case insensitive). Keep in mind this might contain personal data. To learn more, see [Azure Core Tracing OpenTelemetry client library for Python](/python/api/overview/azure/core-tracing-opentelemetry-readme).

```python
import os
os.environ["AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED"] = "true" # False by default
```
Let's begin instrumenting our agent with OpenTelemetry tracing, by starting off with authenticating and connecting to your Azure AI Project using the `AIProjectClient`.

```python
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
project_client = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint=os.environ["PROJECT_ENDPOINT"],
)
```

Next, retrieve the connection string from the Application Insights resource connected to your project and set up the OTLP exporters to send telemetry into Azure Monitor.

```python
from azure.monitor.opentelemetry import configure_azure_monitor

connection_string = project_client.telemetry.get_application_insights_connection_string()
configure_azure_monitor(connection_string=connection_string) #enable telemetry collection
```

Now, trace your code where you create and execute your agent and user message in your Azure AI Project, so you can see detailed steps for troubleshooting or monitoring.

```python
from opentelemetry import trace
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("example-tracing"):
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="my-assistant",
        instructions="You are a helpful assistant"
    )
    thread = project_client.agents.threads.create()
    message = project_client.agents.messages.create(
        thread_id=thread.id, role="user", content="Tell me a joke"
    )
    run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
```

After running your agent, you can go begin to [view traces in Azure AI Foundry Portal](#view-traces-in-azure-ai-foundry-portal).

### Log traces locally

To connect to [Aspire Dashboard](https://aspiredashboard.com/#start) or another OpenTelemetry compatible backend, install the OpenTelemetry Protocol (OTLP) exporter. This enables you to print traces to the console or use a local viewer such as Aspire Dashboard.

```bash
pip install azure-core-tracing-opentelemetry opentelemetry-exporter-otlp opentelemetry-sdk
```

Next, configure tracing for console output:

```python
from azure.core.settings import settings
settings.tracing_implementation = "opentelemetry"

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

# Setup tracing to console
span_exporter = ConsoleSpanExporter()
tracer_provider = TracerProvider()
tracer_provider.add_span_processor(SimpleSpanProcessor(span_exporter))
trace.set_tracer_provider(tracer_provider)
```

Or modify the above code, based on [Aspire Dashboard](https://aspiredashboard.com/#start), to trace to a local OTLP viewer.

Now enable Agent instrumentation and run your Agent:

```python
from azure.ai.agents.telemetry import AIAgentsInstrumentor
AIAgentsInstrumentor().instrument()

# Start tracing
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("example-tracing"):
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="my-assistant",
        instructions="You are a helpful assistant"
    )
    thread = project_client.agents.threads.create()
    message = project_client.agents.messages.create(
        thread_id=thread.id, role="user", content="Tell me a joke"
    )
    run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
```

## Trace custom functions

To trace your custom functions, use the OpenTelemetry SDK to instrument your code.

1. **Set up a tracer provider**: Initialize a tracer provider to manage and create spans.
2. **Create spans**: Wrap the code you want to trace with spans. Each span represents a unit of work and can be nested to form a trace tree.
3. **Add attributes**: Enrich spans with attributes to provide more context for the trace data.
4. **Configure an exporter**: Send the trace data to a backend for analysis and visualization.

Here’s an example of tracing a custom function:

```python
from opentelemetry import trace
from opentelemetry.trace import SpanKind

# Initialize tracer
tracer = trace.get_tracer(__name__)

def custom_function():
    with tracer.start_as_current_span("custom_function") as span:
        span.set_attribute("custom_attribute", "value")
        # Your function logic here
        print("Executing custom function")

custom_function()
```

For detailed instructions and advanced usage, refer to the [OpenTelemetry documentation](https://opentelemetry.io/docs/).

## Attach user feedback to traces

To attach user feedback to traces and visualize it in the Azure AI Foundry portal, you can instrument your application to enable tracing and log user feedback using OpenTelemetry's semantic conventions.

By correlating feedback traces with their respective chat request traces using the response ID or thread ID, you can view and manage these traces in Azure AI Foundry portal. OpenTelemetry's specification allows for standardized and enriched trace data, which can be analyzed in Azure AI Foundry portal for performance optimization and user experience insights. This approach helps you use the full power of OpenTelemetry for enhanced observability in your applications.

To log user feedback, follow this format:

The user feedback evaluation event can be captured if and only if the user provided a reaction to the GenAI model response. It SHOULD, when possible, be parented to the GenAI span describing such response.


The user feedback event body has the following structure:

| Body Field | Type | Description | Examples | Requirement Level |
|---|---|---|---|---|
| `comment` | string | Additional details about the user feedback | `"I did not like it"` | `Opt-in` |

## Using service name in trace data

To identify your service via a unique ID in Application Insights, you can use the service name OpenTelemetry property in your trace data. This is useful if you're logging data from multiple applications to the same Application Insights resource, and you want to differentiate between them.

For example, let's say you have two applications: **App-1** and **App-2**, with tracing configured to log data to the same Application Insights resource. Perhaps you'd like to set up **App-1** to be evaluated continuously by **Relevance** and **App-2** to be evaluated continuously by **Relevance**. You can use the service name to filter by `Application` when monitoring your application in AI Foundry Portal.

To set up the service name property, you can do so directly in your application code by following the steps, see [Using multiple tracer providers with different Resource](https://opentelemetry.io/docs/languages/python/cookbook/#using-multiple-tracer-providers-with-different-resource). Alternatively, you can set the environment variable `OTEL_SERVICE_NAME` before deploying your app. To learn more about working with the service name, see [OTEL Environment Variables](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configuration) and [Service Resource Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/resource/#service).

To query trace data for a given service name, query for the `cloud_roleName` property.

```sql
| where cloud_RoleName == "service_name"
```

## Enable tracing for Langchain

You can enable tracing for Langchain that follows OpenTelemetry standards as per [opentelemetry-instrumentation-langchain](https://pypi.org/project/opentelemetry-instrumentation-langchain/). To enable tracing for Langchain, install the package `opentelemetry-instrumentation-langchain` using your package manager, like pip:

```bash
pip install opentelemetry-instrumentation-langchain
```

Once necessary packages are installed, you can easily begin to [Instrument tracing in your code](#instrument-tracing-in-your-code).

## View trace results in the Azure AI Foundry Agents playground

The Agents playground in the Azure AI Foundry portal lets you view trace results for threads and runs that your agents produce. To see trace results, select **Thread logs** in an active thread. You can also optionally select **Metrics** to enable automatic evaluations of the model's performance across several dimensions of **AI quality** and **Risk and safety**.

> [!NOTE]
> Evaluation in the playground is billed as outlined under Trust and Azure AI Foundry Observability on [the pricing page](https://azure.microsoft.com/pricing/details/ai-foundry/?msockid=1f44c87dd9fa6d1e257fdd6dd8406c42). Results are available for 24 hours before expiring. To get evaluation results, select your desired metrics and chat with your agent.
> - Evaluations aren't available in the following regions.
>     - `australiaeast`
>     - `japaneast`
>     - `southindia`
>     - `uksouth`

:::image type="content" source="../../media/trace/trace-agent-playground.png" alt-text="A screenshot of the agent playground in the Azure AI Foundry portal." lightbox="../../media/trace/trace-agent-playground.png":::

After selecting **Thread logs**, review:

- Thread details
- Run information
- Ordered run steps and tool calls
- Inputs / outputs between user and agent
- Linked evaluation metrics (if enabled)

:::image type="content" source="../../agents/media/thread-trace.png" alt-text="A screenshot of a trace." lightbox="../../agents/media/thread-trace.png":::

> [!TIP]
> If you want to view trace results from a previous thread, select **My threads** in the **Agents** screen. Choose a thread, and then select **Try in playground**.
> :::image type="content" source="../../agents/media/thread-highlight.png" alt-text="A screenshot of the threads screen." lightbox="../../agents/media/thread-highlight.png":::
> You'll be able to see the **Thread logs** button at the top of the screen to view the trace results.


> [!NOTE]
> Observability features such as Risk and Safety Evaluation are billed based on consumption as listed in the [Azure pricing page](https://azure.microsoft.com/pricing/details/ai-foundry/).

## View traces in Azure AI Foundry portal

In your project, go to `Tracing` to filter your traces as you see fit.

By selecting a trace, you can step through each span and identify issues while observing how your application is responding. This can help you debug and pinpoint issues in your application.

## View traces in Azure Monitor

If you logged traces using the previous code snippet, then you're all set to view your traces in Azure Monitor Application Insights. You can open in Application Insights from **Manage data source** and use the **End-to-end transaction details view** to further investigate.

For more information on how to send Azure AI Inference traces to Azure Monitor and create Azure Monitor resource, see [Azure Monitor OpenTelemetry documentation](/azure/azure-monitor/app/opentelemetry-enable).

## Related content

- [Python samples](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-inference/samples/sample_chat_completions_with_tracing.py) containing fully runnable Python code for tracing using synchronous and asynchronous clients.
- [Python samples for tracing agents with console tracing and Azure Monitor](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-agents/samples/agents_telemetry)
- [JavaScript samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-inference-rest/samples/v1-beta/typescript/src) containing fully runnable JavaScript code for tracing using synchronous and asynchronous clients.
- [C# Samples](https://github.com/Azure/azure-sdk-for-net/blob/Azure.AI.Inference_1.0.0-beta.2/sdk/ai/Azure.AI.Inference/samples/Sample8_ChatCompletionsWithOpenTelemetry.md) containing fully runnable C# code for doing inference using synchronous and asynchronous methods.
