---
title: How to trace your application with Azure AI Inference SDK
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to trace your application with Azure AI Inference SDK.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - build-2024
  - ignite-2024
ms.topic: how-to
ms.date: 05/19/2025
ms.reviewer: amibp
ms.author: lagayhar
author: lgayhardt
---

# Tracing your AI application (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Tracing provides deep visibility into execution of your application by capturing detailed telemetry at each execution step. This helps diagnose issues and enhance performance by identifying problems such as inaccurate tool calls, misleading prompts, high latency, low-quality evaluation scores, and more.  

This article walks you through how to instrument tracing in your AI applications using OpenTelemetry and Azure Monitor for enhanced observability and debugging.

Here's a brief overview of key concepts before getting started:

| Key concepts             | Description            |
|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Traces              | Traces capture the journey of a request or workflow through your application by recording events and state changes during execution, such as function calls, variable values, and system events. To learn more, see [OpenTelemetry Traces](https://opentelemetry.io/docs/concepts/signals/traces/).                                                      |
| Spans               | Spans are the building blocks of traces, representing single operations within a trace. Each span captures start and end times, attributes, and can be nested to show hierarchical relationships, allowing you to see the full call stack and sequence of operations.                                                                                         |
| Attributes          | Attributes are key-value pairs attached to traces and spans, providing contextual metadata such as function parameters, return values, or custom annotations. These enrich trace data making it more informative and useful for analysis.                                                                                                 |
| Semantic conventions| OpenTelemetry defines semantic conventions to standardize names and formats for trace data attributes, making it easier to interpret and analyze across tools and platforms. To learn more, see [OpenTelemetry's Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/).                  |
| Trace exporters     | Trace exporters send trace data to backend systems for storage and analysis. Azure AI supports exporting traces to Azure Monitor and other OpenTelemetry-compatible platforms, enabling integration with various observability tools.                                                                               |

## Setup

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
from opentelemetry import trace
from azure.monitor.opentelemetry import configure_azure_monitor
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
import os

os.environ["AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED"] = "true" # False by default

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"],
)
```

### Log to Azure Monitor Application Insights

Retrieve the connection string from the Application Insights resource connected to your project and set up the OTLP exporters to send telemetry into Azure Monitor.

```python
connection_string = project_client.telemetry.get_connection_string()

if not connection_string:
    print("Application Insights is not enabled. Enable by going to Observability > Traces in your AI Foundry project.")
    exit()

configure_azure_monitor(connection_string=connection_string)
```

Start collecting telemetry and send to your project's connected Application Insights resource.

```python
# Start tracing
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("example-tracing"):
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="my-assistant",
        instructions="You are a helpful assistant"
    )
    thread = project_client.agents.create_thread()
    message = project_client.agents.create_message(
        thread_id=thread.id, role="user", content="Tell me a joke"
    )
    run = project_client.agents.create_run(thread_id=thread.id, agent_id=agent.id)
```

### Log to a local OTLP endpoint

To connect to Aspire Dashboard or another OpenTelemetry compatible backend, install the OpenTelemetry Protocol (OTLP) exporter. This enables you to print traces to the console or use a local viewer such as Aspire Dashboard.

```bash
pip install opentelemetry-exporter-otlp
```

```python
# Enable console tracing
project_client.telemetry.enable(destination=sys.stdout)

# for local OTLP endpoint, change the destination to
# project_client.telemetry.enable(destination="http://localhost:4317")
```

### Trace custom functions

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

### Attach user feedback to traces

To attach user feedback to traces and visualize it in the Azure AI Foundry portal, you can instrument your application to enable tracing and log user feedback using OpenTelemetry's semantic conventions. By correlating feedback traces with their respective chat request traces using the response ID, you can view and manage these traces in Azure AI Foundry portal. OpenTelemetry's specification allows for standardized and enriched trace data, which can be analyzed in Azure AI Foundry portal for performance optimization and user experience insights. This approach helps you use the full power of OpenTelemetry for enhanced observability in your applications.

To log user feedback, follow this format:

The user feedback evaluation event can be captured if and only if the user provided a reaction to the GenAI model response. It SHOULD, when possible, be parented to the GenAI span describing such response.

<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->
The event name MUST be `gen_ai.evaluation.user_feedback`.

| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
|`gen_ai.response.id`| string | The unique identifier for the completion. | `chatcmpl-123` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `gen_ai.evaluation.score`| double | Quantified score calculated based on the user reaction in [-1.0, 1.0] range with 0 representing a neutral reaction. | `0.42` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

The user feedback event body has the following structure:

| Body Field | Type | Description | Examples | Requirement Level |
|---|---|---|---|---|
| `comment` | string | Additional details about the user feedback | `"I did not like it"` | `Opt-in` |

### Using service name in trace data

To identify your service via a unique ID in Application Insights, you can use the service name OpenTelemetry property in your trace data. This is useful if you're logging data from multiple applications to the same Application Insights resource, and you want to differentiate between them.

For example, let's say you have two applications: **App-1** and **App-2**, with tracing configured to log data to the same Application Insights resource. Perhaps you'd like to set up **App-1** to be evaluated continuously by **Relevance** and **App-2** to be evaluated continuously by **Relevance**. You can use the service name to filter by `Application` when monitoring your application in AI Foundry Portal.

To set up the service name property, you can do so directly in your application code by following the steps, see [Using multiple tracer providers with different Resource](https://opentelemetry.io/docs/languages/python/cookbook/#using-multiple-tracer-providers-with-different-resource). Alternatively, you can set the environment variable `OTEL_SERVICE_NAME` before deploying your app. To learn more about working with the service name, see [OTEL Environment Variables](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configuration) and [Service Resource Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/resource/#service).

To query trace data for a given service name, query for the `cloud_roleName` property.

```sql
| where cloud_RoleName == "service_name"
```

## Enable Tracing for Langchain

You can enable tracing for Langchain that follows OpenTelemetry standards as per [opentelemetry-instrumentation-langchain](https://pypi.org/project/opentelemetry-instrumentation-langchain/). To enable tracing for Langchain, install the package `opentelemetry-instrumentation-langchain` using your package manager, like pip:

```bash
pip install opentelemetry-instrumentation-langchain
```

Once necessary packages are installed, you can easily begin to [Instrument tracing in your code](#instrument-tracing-in-your-code).

## Visualize your traces

### View your traces for local debugging

#### Prompty

Using Prompty, you can trace your application with **Open Telemetry**, which offers enhanced visibility and simplified troubleshooting for LLM-based applications. This method adheres to the OpenTelemetry specification, enabling the capture and visualization of an AI application's internal execution details, which improves debugging and enhances the development process. To learn more, see [Debugging Prompty](https://prompty.ai/docs/getting-started/debugging-prompty).

#### Aspire Dashboard

Aspire Dashboard is a free & open-source OpenTelemetry dashboard for deep insights into your apps on your local development machine. To learn more, see [Aspire Dashboard](https://aspiredashboard.com/#start).

### Debugging with traces in Azure AI Foundry portal

In your project, go to `Tracing` to filter your traces as you see fit.

By selecting a trace, I can step through each span and identify issues while observing how my application is responding.

### View traces in Azure Monitor

If you logged traces using the previous code snippet, then you're all set to view your traces in Azure Monitor Application Insights. You can open in Application Insights from **Manage data source** and use the **End-to-end transaction details view** to further investigate.

For more information on how to send Azure AI Inference traces to Azure Monitor and create Azure Monitor resource, see [Azure Monitor OpenTelemetry documentation](/azure/azure-monitor/app/opentelemetry-enable).

## Related content

- [Python samples](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-inference/samples/sample_chat_completions_with_tracing.py) containing fully runnable Python code for tracing using synchronous and asynchronous clients.
- [Sample Agents with Console tracing](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/sample_agents_functions_with_console_tracing.py)
- [Sample Agents with Azure Monitor](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/sample_agents_basics_with_azure_monitor_tracing.py)
- [JavaScript samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-inference-rest/samples/v1-beta/typescript/src) containing fully runnable JavaScript code for tracing using synchronous and asynchronous clients.
- [C# Samples](https://github.com/Azure/azure-sdk-for-net/blob/Azure.AI.Inference_1.0.0-beta.2/sdk/ai/Azure.AI.Inference/samples/Sample8_ChatCompletionsWithOpenTelemetry.md) containing fully runnable C# code for doing inference using synchronous and asynchronous methods.
