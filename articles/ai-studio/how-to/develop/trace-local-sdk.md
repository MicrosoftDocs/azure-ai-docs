---
title: How to trace your application with Azure AI Inference SDK
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to trace your application with  Azure AI Inference SDK.
manager: scottpolly
ms.service: azure-ai-studio
ms.custom:
  - build-2024
  - ignite-2024
ms.topic: how-to
ms.date: 11/19/2024
ms.reviewer: truptiparkar
ms.author: lagayhar
author: lgayhardt
---

# How to trace your application with Azure AI Inference SDK

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

In this article you'll learn how to trace your application with Azure AI Inference SDK with your choice between using Python, JavaScript, or C#. The Azure AI Inference client library provides support for tracing with OpenTelemetry.

## Enable trace in your application

### Prerequisites

- An [Azure Subscription](https://azure.microsoft.com/).
- An Azure AI project, see [Create a project in Azure AI Foundry portal](../create-projects.md).
- An AI model supporting the [Azure AI model inference API](https://aka.ms/azureai/modelinference) deployed through Azure AI Foundry.
- If using Python, you need Python 3.8 or later installed, including pip.
- If using JavaScript, the supported environments are LTS versions of Node.js.

### Installation

# [Python](#tab/python)

Install the package `azure-ai-inference` using your package manager, like pip:

```bash
  pip install azure-ai-inference[opentelemetry] 
```

Install the Azure Core OpenTelemetry Tracing plugin, OpenTelemetry, and the OTLP exporter for sending telemetry to your observability backend. To install the necessary packages for Python, use the following pip commands:

```bash
pip install opentelemetry 

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

To learn more , see the [Inference SDK reference](../../reference/reference-model-inference-api.md).

### Configuration

# [Python](#tab/python)

You need to add following configuration settings as per your use case:

- To capture prompt and completion contents, set the `AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED` environment variable to true (case insensitive). By default, prompts, completions, function names, parameters, or outputs aren't recorded.
- To enable Azure SDK tracing, set the `AZURE_SDK_TRACING_IMPLEMENTATION` environment variable to opentelemetry. Alternatively, you can configure it in the code with the following snippet:

    ```python
    from azure.core.settings import settings 
    
    settings.tracing_implementation = "opentelemetry" 
    ```

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

It's also possible to uninstrument the Azure AI Inferencing API by using the uninstrument call. After this call, the traces will no longer be emitted by the Azure AI Inferencing API until instrument is called again:

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

To configure OpenTelemetry and enable Azure AI Inference tracing follow these steps:

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

## Attach User feedback to traces

To attach user feedback to traces and visualize them in Azure AI Foundry portal using OpenTelemetry's semantic conventions, you can instrument your application enabling tracing and logging user feedback. By correlating feedback traces with their respective chat request traces using the response ID, you can use view and manage these traces in Azure AI Foundry portal. OpenTelemetry's specification allows for standardized and enriched trace data, which can be analyzed in Azure AI Foundry portal for performance optimization and user experience insights. This approach helps you use the full power of OpenTelemetry for enhanced observability in your applications.  

## Related content

- [Python samples](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-inference/samples/sample_chat_completions_with_tracing.py) containing fully runnable Python code for tracing using synchronous and asynchronous clients.
- [JavaScript samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-inference-rest/samples/v1-beta/typescript/src) containing fully runnable JavaScript code for tracing using synchronous and asynchronous clients.
- [C# Samples](https://github.com/Azure/azure-sdk-for-net/blob/Azure.AI.Inference_1.0.0-beta.2/sdk/ai/Azure.AI.Inference/samples/Sample8_ChatCompletionsWithOpenTelemetry.md) containing fully runnable C# code for doing inference using synchronous and asynchronous methods.
