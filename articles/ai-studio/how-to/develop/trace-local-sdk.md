---
title: How to trace your application with Azure AI Inference SDK
titleSuffix: Azure AI Studio
description: This article provides instructions on how to trace your application with  Azure AI Inference SDK.
manager: scottpolly
ms.service: azure-ai-studio
ms.custom:
  - build-2024
ms.topic: how-to
ms.date: 11/19/2024
ms.reviewer: truptiparkar
ms.author: lagayhar  
author: lgayhardt
---

# How to trace your application with Azure AI Inference SDK

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Tracing is a powerful tool that offers developers an in-depth understanding of the execution process of their generative AI applications. It provides a detailed view of the execution flow, including the inputs and outputs of each node within the application. This essential information proves critical while debugging complex applications or optimizing performance.

Tracing with the Azure AI SDK offers enhanced visibility and simplified troubleshooting for LLM-based applications, effectively supporting development, iteration, and production monitoring. Tracing follows the OpenTelemetry specification, capturing and visualizing the internal execution details of any AI application, enhancing the overall development experience. The Azure AI Inference client library provides experimental support for tracing with OpenTelemetry.

## Enable trace in your application

### Prerequisites

- An [Azure Subscription](https://azure.microsoft.com/).
- An Azure AI project, see [Create a project in Azure AI Studio](../create-projects.md).
- An AI model supporting the [Azure AI model inference API](https://aka.ms/azureai/modelinference) deployed through AI Studio.

# [Python](#tab/python)

- Python 3.8 or later installed, including pip.

# [JavaScript](#tab/javascript)

- Supported Environments: LTS versions of Node.js

# [C#](#tab/python)

- To construct the client library, you need to pass in the endpoint URL. The endpoint URL has the form `https://your-host-name.your-azure-region.inference.ai.azure.com`, where your-host-name is your unique model deployment host name and your-azure-region is the Azure region where the model is deployed (for example, eastus2).
- Depending on your model deployment and authentication preference, you either need a key to authenticate against the service, or Microsoft Entra ID credentials. The key is a 32-character string.

---

### Installation

# [Python](#tab/python)

Install the package `azure-ai-inference` using your package manager, like pip:

```bash
  pip install azure-ai-inference
```

Install the Azure Core OpenTelemetry Tracing plugin, OpenTelemetry, and the OTLP exporter for sending telemetry to your observability backend. To install the necessary packages for Python, use the following pip commands:

```bash
pip install azure-core-tracing-opentelemetry 

pip install opentelemetry 

pip install azure-core-tracing-opentelemetry 

pip install opentelemetry-exporter-otlp 
```

# [JavaScript](#tab/javascript)

Install the package `@azure-rest/ai-inference` and Azure ModelClient REST client library for JavaScript using npm:

```bash
    npm install @azure-rest/ai-inference
```

# [C#](#tab/python)

Install the Azure AI inference client library for .NET with [NuGet](https://aka.ms/azsdk/azure-ai-inference/csharp/package): 

```dotnetcli
    dotnet add package Azure.AI.Inference --prerelease
```

---

To learn more, see the [Inference SDK reference](../../reference/reference-model-inference-api.md).

### Configuration

# [Python](#tab/python)

You need to add following configuration settings as per your use case:

- To capture prompt and completion contents, set the `AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED` environment variable to true (case insensitive). By default, prompts, completions, function names, parameters, or outputs aren't recorded.
- To enable Azure SDK tracing, set the AZURE_SDK_TRACING_IMPLEMENTATION environment variable to opentelemetry. Alternatively, you can configure it in the code with the following snippet:

    ```python
    from azure.core.settings import settings 
    
    settings.tracing_implementation = "opentelemetry" 
    ```

    To learn more, see [Azure Core Tracing OpenTelemetry client library for Python](/python/api/overview/azure/core-tracing-opentelemetry-readme).

If you want to install Azure AI Inferencing package with support for OpenTelemetry based tracing, use the following command:

```bash
pip install azure-ai-inference[opentelemetry] 
```

# [JavaScript](#tab/javascript)

Instrumentation is only supported for Chat Completion without streaming. To enable instrumentation, you need to register exporter(s). Following is an example of how to add a console exporter.

Console Exporter:

```javascript
import { ConsoleSpanExporter, NodeTracerProvider, SimpleSpanProcessor } from "@opentelemetry/sdk-trace-node"; 

const provider = new NodeTracerProvider(); 

provider.addSpanProcessor(new SimpleSpanProcessor(new ConsoleSpanExporter())); 

provider.register(); 
```


# [C#](#tab/python)

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

# [C#](#tab/python)

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

### Tracing Your Own Functions:

# [Python](#tab/python)

The `@tracer.start_as_current_span` decorator can be used to trace your own functions. This traces the function parameters and their values. You can also add further attributes to the span in the function implementation as demonstrated in the following example.

> [!NOTE]
> You will have to set up the tracer in your code before using the decorator. To learn more. see [OpenTelemetry Python Documentation](https://opentelemetry.io/docs/languages/python/).

```python
from opentelemetry.trace import get_tracer 

tracer = get_tracer(__name__) 

@tracer.start_as_current_span("get_temperature") # type: ignore 

def get_temperature(city: str) -> str: 

 

    # Adding attributes to the current span 

    span = trace.get_current_span() 

    span.set_attribute("requested_city", city) 

 

    if city == "Seattle": 

        return "75" 

    elif city == "New York City": 

        return "80" 

    else: 

        return "Unavailable" 

```


# [JavaScript](#tab/javascript)

OpenTelemetry provides `startActiveSpan` to instrument your own code. Here's an example of how to use it: 

```javascript

import { trace } from "@opentelemetry/api"; 

const tracer = trace.getTracer("sample", "0.1.0"); 

const getWeatherFunc = (location: string, unit: string): string => { 

  return tracer.startActiveSpan("getWeatherFunc", span => { 

    if (unit !== "celsius") { 

      unit = "fahrenheit"; 

    } 

    const result = `The temperature in ${location} is 72 degrees ${unit}`; 

    span.setAttribute("result", result); 

    span.end(); 

    return result; 

  }); 

} 
```

# [C#](#tab/python)

To trace your own functions, use the OpenTelemetry API to start and end spans around the code you want to trace. Here's an example:

```csharp
using OpenTelemetry.Trace; 

var tracer = Sdk.CreateTracerProviderBuilder() 

    .AddSource("sample") 

    .Build() 

    .GetTracer("sample"); 

using (var span = tracer.StartActiveSpan("getWeatherFunc")) 

{ 
    var location = "Seattle"; 

    var unit = "celsius"; 

    if (unit != "celsius") 

    { 
        unit = "fahrenheit"; 
    } 

    var result = $"The temperature in {location} is 72 degrees {unit}"; 

    span.SetAttribute("result", result); 

    Console.WriteLine(result); 

} 
```

To learn more, see [OpenTelemetry .NET](https://opentelemetry.io/docs/languages/net/).

---

## Attach User feedback to traces

To attach user feedback to traces and visualize them in AI Studio using OpenTelemetry's semantic conventions, you can instrument your application enabling tracing and logging user feedback. By correlating feedback traces with their respective chat request traces using the response ID, you can use view and manage these traces in AI studio. OpenTelemetry's specification allows for standardized and enriched trace data, which can be analyzed in AI Studio for performance optimization and user experience insights. This approach helps you use the full power of OpenTelemetry for enhanced observability in your applications.  



## Related content

# [Python](#tab/python)

- [Python samples]() containing fully runnable Python code for tracing using synchronous and asynchronous clients.
- [Python samples to use Azure AI Project with tracing](https://github.com/Azure/azure-sdk-for-python/tree/feature/azure-ai-projects/sdk/ai/azure-ai-projects/samples/inference)

# [JavaScript](#tab/javascript)

- [JavaScript samples](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-inference-rest/samples/v1-beta/typescript/src/telemetry.ts) containing fully runnable JavaScript code for tracing using synchronous and asynchronous clients.
- [JavaScript samples to use Azure AI Project with tracing](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-inference-rest/samples/v1-beta/typescript/src/telemetryWithToolCall.ts)

# [C#](#tab/python)

[C# Samples](https://github.com/Azure/azure-sdk-for-net/blob/Azure.AI.Inference_1.0.0-beta.2/sdk/ai/Azure.AI.Inference/samples/Sample8_ChatCompletionsWithOpenTelemetry.md) containing fully runnable C# code for doing inference using synchronous and asynchronous methods.

---

- [Get started building a chat app using the prompt flow SDK](../../quickstarts/get-started-code.md)
- [Work with projects in VS Code](vscode.md)

