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
ms.date: 03/31/2025
ms.reviewer: truptiparkar
ms.author: lagayhar
author: lgayhardt
---

# How to trace your application with Azure AI Foundry project library (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

In this article, you'll learn how to trace your application with Azure AI Foundry SDK with your choice between using Python, JavaScript, or C#. This provides support for tracing with OpenTelemetry.

## Prerequisites

- An [Azure Subscription](https://azure.microsoft.com/).
- An Azure AI project, see [Create a project in Azure AI Foundry portal](../create-projects.md).
- An AI model supporting the [Azure AI Foundry Models API](https://aka.ms/azureai/modelinference) deployed through Azure AI Foundry.
- If using Python, you need Python 3.8 or later installed, including pip.
- If using JavaScript, the supported environments are LTS versions of Node.js.

## Tracing using Azure AI Foundry project library

# [Python](#tab/python)

The best way to get started using the Azure AI Foundry SDK is by using a project. AI projects connect together different data, assets, and services you need to build AI applications. The AI project client allows you to easily access these project components from your code by using a single connection string. First follow steps to [create an AI Project](../create-projects.md) if you don't have one already.
To enable tracing, first ensure your project has an attached Application Insights resource. Go to the **Tracing** page of your project in Azure AI Foundry portal and follow instructions to create or attach Application Insights. If one was enabled, you can get the Application Insights connection string, and observe the full execution path through Azure Monitor.

Make sure to install following packages via

```bash
pip install opentelemetry-sdk
pip install azure-core-tracing-opentelemetry
pip install azure-monitor-opentelemetry
```

Refer the following samples to get started with tracing using Azure AI Project SDK:

- [Python Sample with console tracing for Azure AI Inference Client](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/inference/sample_chat_completions_with_azure_ai_inference_client_and_console_tracing.py) containing fully runnable Python code for tracing using synchronous and asynchronous clients.
- [Python Sample with Azure Monitor for Azure AI Inference Client](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-inference/samples/sample_chat_completions_with_tracing.py) containing fully runnable Python code for tracing using synchronous and asynchronous clients.
- [Python Sample with console tracing for Azure OpenAI](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/inference/sample_chat_completions_with_azure_openai_client_and_console_tracing.py) containing fully runnable Python code for tracing using synchronous and asynchronous clients.
- [Python Sample with Azure Monitor for Azure OpenAI](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/inference/sample_chat_completions_with_azure_openai_client_and_azure_monitor_tracing.py) containing fully runnable Python code for tracing using synchronous and asynchronous clients.

# [JavaScript](#tab/javascript)

Tracing isn't yet integrated into the Azure AI Projects SDK for JS. For instructions on how to instrument and log traces from the Azure AI Inference package, see [JavaScript samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-inference-rest/samples/v1-beta/typescript/src).

# [C#](#tab/csharp)

Tracing isn't yet integrated into the Azure AI Projects SDK for C#. For instructions on how to instrument and log traces from the Azure AI Inference package, see [azure-sdk-for-dotnet](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Inference/samples/Sample8_ChatCompletionsWithOpenTelemetry.md).

---

## Enable Tracing using Azure AI Inference Library

### Installation

# [Python](#tab/python)

Install the package `azure-ai-inference` using your package manager, like pip:

```bash
  pip install azure-ai-inference[opentelemetry] 
```

Install the Azure Core OpenTelemetry Tracing plugin, OpenTelemetry, and the OTLP exporter for sending telemetry to your observability backend. To install the necessary packages for Python, use the following pip commands:

```bash
pip install opentelemetry-sdk

pip install opentelemetry-exporter-otlp 
```

To learn more about Azure AI Inference SDK for Python and observability, see [Tracing via Inference SDK for Python](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-inference/README.md#observability-with-opentelemetry).

# [JavaScript](#tab/javascript)

Install the package `@azure-rest/ai-inference` for JavaScript using npm:

```bash
    npm install @azure-rest/ai-inference
```

To learn more about Azure AI Inference SDK for JavaScript and observability, see [Tracing via Inference SDK for JavaScript](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-inference-rest/README.md#instrumentation).

# [C#](#tab/csharp)

Install the Azure AI Inference client library for .NET with [NuGet](https://aka.ms/azsdk/azure-ai-inference/csharp/package): 

```dotnetcli
    dotnet add package Azure.AI.Inference --prerelease
```

To learn more Azure AI Inference SDK for C# and observability, see the [Tracing via Inference SDK for C#](https://github.com/Azure/azure-sdk-for-net/tree/Azure.AI.Inference_1.0.0-beta.2/sdk/ai/Azure.AI.Inference#observability-with-opentelemetry).

---

To learn more, see the [Inference SDK reference](../../../ai-foundry/model-inference/reference/reference-model-inference-api.md).

### Configuration

# [Python](#tab/python)

You need to add following configuration settings as per your use case:

- To capture prompt and completion contents, set the `AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED` environment variable to true (case insensitive). By default, prompts, completions, function names, parameters, or outputs aren't recorded.
    To learn more, see [Azure Core Tracing OpenTelemetry client library for Python](/python/api/overview/azure/core-tracing-opentelemetry-readme).

# [JavaScript](#tab/javascript)

Instrumentation is only supported for Chat Completion without streaming. To enable instrumentation, you need to register exporter(s). Following is an example of how to add a console exporter.

Console Exporter:

```javascript
import { ConsoleSpanExporter, NodeTracerProvider, SimpleSpanProcessor } from "@opentelemetry/sdk-trace-node"; 

const provider = new NodeTracerProvider(); 

provider.addSpanProcessor(new SimpleSpanProcessor(new ConsoleSpanExporter())); 

provider.register(); 
```

# [C#](#tab/csharp)

Distributed tracing and metrics with OpenTelemetry are supported in Azure AI Inference in experimental mode and could be enabled through either of these steps: 

- Set the `AZURE_EXPERIMENTAL_ENABLE_ACTIVITY_SOURCE` environment variable to true.
- Set the `Azure.Experimental.EnableActivitySource` context switch to true in your application code.

---

### Enable Instrumentation

# [Python](#tab/python)

The final step is to enable Azure AI Inference instrumentation with the following code snippet:

```python
from azure.ai.inference.tracing import AIInferenceInstrumentor 

# Instrument AI Inference API 

AIInferenceInstrumentor().instrument() 

```

It's also possible to uninstrument the Azure AI Inference API by using the uninstrument call. After this call, the traces will no longer be emitted by the Azure AI Inference API until instrument is called again:

```python
AIInferenceInstrumentor().uninstrument() 
```

# [JavaScript](#tab/javascript)

To use instrumentation for Azure SDK, you need to register it before importing any dependencies from `@azure/core-tracing`, such as `@azure-rest/ai-inference`.

```Javascript
import { registerInstrumentations } from "@opentelemetry/instrumentation"; 

import { createAzureSdkInstrumentation } from "@azure/opentelemetry-instrumentation-azure-sdk"; 


registerInstrumentations({ 

  instrumentations: [createAzureSdkInstrumentation()], 

}); 

import ModelClient from "@azure-rest/ai-inference"; 

```

When making a call for chat completion, you need to include the tracingOptions with the active tracing context: 

```javascript

import { context } from "@opentelemetry/api"; 

client.path("/chat/completions").post({ 

      body: {...}, 

      tracingOptions: { tracingContext: context.active() } 

}); 

```

# [C#](#tab/csharp)

To configure OpenTelemetry and enable Azure AI Inference tracing, follow these steps:

1. **Install OpenTelemetry Packages**: Install the following dependencies for HTTP tracing and metrics instrumentation as well as console and [OTLP](https://opentelemetry.io/docs/specs/otel/protocol/) exporters:

    ```csharp
       dotnet add package OpenTelemetry.Instrumentation.Http 
    
       dotnet add package OpenTelemetry.Exporter.Console 
    
       dotnet add package OpenTelemetry.Exporter.OpenTelemetryProtocol 
    ```

1. **Enable Experimental Azure SDK Observability**: Set the context switch to enable experimental Azure SDK observability:

    ```csharp
       AppContext.SetSwitch("Azure.Experimental.EnableActivitySource", true); 
    ```

1. **Enable Content Recording**: By default, instrumentation captures chat messages without content. To enable content recording, set the following context switch: 

    ```csharp
     AppContext.SetSwitch("Azure.Experimental.TraceGenAIMessageContent", true);
    ```

1. **Configure Tracer Provider**: Configure the tracer provider to export traces and metrics to console and to the local OTLP destination as needed.

---

### Tracing your own functions

To trace your own custom functions, you can leverage OpenTelemetry, you'll need to instrument your code with the OpenTelemetry SDK. This involves setting up a tracer provider and creating spans around the code you want to trace. Each span represents a unit of work and can be nested to form a trace tree. You can add attributes to spans to enrich the trace data with additional context. Once instrumented, configure an exporter to send the trace data to a backend for analysis and visualization. For detailed instructions and advanced usage, refer to the [OpenTelemetry documentation](https://opentelemetry.io/docs/). This will help you monitor the performance of your custom functions and gain insights into their execution.

### Using service name in trace data

To identify your service via a unique ID in Application Insights, you can use the service name OpenTelemetry property in your trace data. This is particularly useful if you're logging data from multiple applications to the same Application Insights resource, and you want to differentiate between them. For example, lets say you have two applications: **App-1** and **App-2**, with tracing configured to log data to the same Application Insights resource. Perhaps you'd like to set up **App-1** to be evaluated continuously by **Relevance** and **App-2** to be evaluated continuously by **Groundedness**. You can use the service name to differentiate between the applications in your Online Evaluation configurations.

To set up the service name property, you can do so directly in your application code by following the steps, see  [Using multiple tracer providers with different Resource](https://opentelemetry.io/docs/languages/python/cookbook/#using-multiple-tracer-providers-with-different-resource). Alternatively, you can set the environment variable `OTEL_SERVICE_NAME` prior to deploying your app. To learn more about working with the service name, see [OTEL Environment Variables](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configuration) and [Service Resource Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/resource/#service).

To query trace data for a given service name, query for the `cloud_roleName` property. In case you're leveraging Online Evaluation, add the following line to the KQL query you use within your Online Evaluation set-up:

```sql
| where cloud_RoleName == "service_name"
```

## Enable Tracing for Langchain

# [Python](#tab/python)

You can enable tracing for Langchain that follows OpenTelemetry standards as per [opentelemetry-instrumentation-langchain](https://pypi.org/project/opentelemetry-instrumentation-langchain/) To enable tracing for Langchain, follow following steps:

Install the package `opentelemetry-instrumentation-langchain` using your package manager, like pip:

```bash
  pip install opentelemetry-instrumentation-langchain
```

Once necessary packages are installed, you can easily enable tracing via [Tracing using Azure AI Foundry project library](#tracing-using-azure-ai-foundry-project-library)

# [JavaScript](#tab/javascript)
Currently this is supported in Python only.

# [C#](#tab/csharp)
Currently this is supported in Python only.

---

## Attach User feedback to traces

To attach user feedback to traces and visualize them in Azure AI Foundry portal using OpenTelemetry's semantic conventions, you can instrument your application enabling tracing and logging user feedback. By correlating feedback traces with their respective chat request traces using the response ID, you can use view and manage these traces in Azure AI Foundry portal. OpenTelemetry's specification allows for standardized and enriched trace data, which can be analyzed in Azure AI Foundry portal for performance optimization and user experience insights. This approach helps you use the full power of OpenTelemetry for enhanced observability in your applications.  

To log user feedback, follow this format:
The user feedback evaluation event can be captured if and only if user provided a reaction to GenAI model response.
It SHOULD, when possible, be parented to the GenAI span describing such response.

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
<!-- END AUTOGENERATED TEXT -->
The user feedback event body has the following structure:

| Body Field | Type | Description | Examples | Requirement Level |
|---|---|---|---|---|
| `comment` | string | Additional details about the user feedback | `"I did not like it"` | `Opt-in` |

## Related content

- [Python samples](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-inference/samples/sample_chat_completions_with_tracing.py) containing fully runnable Python code for tracing using synchronous and asynchronous clients.
- [Sample Agents with Console tracing](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/sample_agents_functions_with_console_tracing.py)
- [Sample Agents with Azure Monitor](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/sample_agents_basics_with_azure_monitor_tracing.py)
- [JavaScript samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-inference-rest/samples/v1-beta/typescript/src) containing fully runnable JavaScript code for tracing using synchronous and asynchronous clients.
- [C# Samples](https://github.com/Azure/azure-sdk-for-net/blob/Azure.AI.Inference_1.0.0-beta.2/sdk/ai/Azure.AI.Inference/samples/Sample8_ChatCompletionsWithOpenTelemetry.md) containing fully runnable C# code for doing inference using synchronous and asynchronous methods.
