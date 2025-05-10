---
title: How to get started with Azure AI Foundry SDK
titleSuffix: Azure AI Foundry
description: This article provides an overview of the Azure AI Foundry SDK and how to get started using it.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - build-2024
  - ignite-2024
ms.topic: how-to
ms.date: 05/07/2025
ms.reviewer: dantaylo
ms.author: sgilley
author: sdgilley
zone_pivot_groups: foundry-sdk-languages
# customer intent: I want to learn how to use the Azure AI Foundry SDK to build AI applications on Azure.
---

# Azure AI Foundry SDK client libraries

The Azure AI Foundry SDK is a comprehensive toolchain designed to simplify the development of AI applications on Azure. It enables developers to:

- Access popular models from various model providers through a single interface
- Easily combine together models, data, and AI services to build AI-powered applications
- Evaluate, debug, and improve application quality & safety across development, testing, and production environments

The Azure AI Foundry SDK is a set of client libraries and services designed to work together. 

## Prerequisites

* An Azure subscription. If you don't have one, create a [free account](https://azure.microsoft.com/free/).
* [Create a project](../create-projects.md) if you don't have one already.
* Sign in with the Azure CLI using the same account that you use to access your AI Project:

    ```bash
    az login
    ```

## Unified Projects client library

The Azure AI Foundry Projects client library is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.

::: zone pivot="programming-language-python"

* Install the project client library 

    ```bash
    pip install azure-ai-projects azure-ai-identity
    ```

* Create a project client in code.  **Copy** the Azure AI Foundry project endpoint from the Overview page of the project and update the connections string value.

    ```python
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    
    project = AIProjectClient.from_connection_string(
      endpoint="your_project_endpoint",  # Replace with your endpoint
      credential=DefaultAzureCredential())
    ```

::: zone-end

::: zone pivot="programming-language-java"


* Add these packages to your installation:
    * `com.azure.ai.projects`
    * `com.azure.core`

* Create a project client in code.  **Copy** the Azure AI Foundry project endpoint from the Overview page of the project and update the connections string value.

    ```java
    import com.azure.ai.projects.ProjectsClient;
    import com.azure.ai.projects.ProjectsClientBuilder;
    import com.azure.core.credential.AzureKeyCredential;
    
    String endpoint ="your_project_endpoint"; // Replace with your endpoint
    
    ProjectsClient client = new ProjectsClientBuilder()
        .credential(new AzureKeyCredential(apiKey))
        .endpoint(endpoint)
        .buildClient();
    ```



::: zone-end

::: zone pivot="programming-language-javascript"

* Install dependencies:

    ```bash
    npm install @azure/ai-projects @azure/identity
    ```

* Create a project client in code.  **Copy** the Azure AI Foundry project endpoint from the Overview page of the project and update the connections string value.


    ```javascript
    import { AIProjectClient } from '@azure/ai-projects';
    import { DefaultAzureCredential } from '@azure/identity';
    
    const endpoint = "your_project_endpoint"; // Replace with your actual endpoint
    const project = new AIProjectClient(endpoint, new DefaultAzureCredential());
    
    const client = project.inference.azureOpenAI();
    ```

::: zone-end

::: zone pivot="programming-language-csharp"

* Install packages:

    ```bash
    dotnet add package Azure.Identity
    dotnet add package Azure.Core
    dotnet add package Azure.AI.Inference
    ```

* Create a project client in code.  **Copy** the Azure AI Foundry project endpoint from the Overview page of the project and update the connections string value.

    ```csharp
    using Azure;
    using Azure.Identity;
    using Azure.AI.Inference;
    using Azure.Core;
    using Azure.Core.Pipeline;
    
    var endpointUrl = "your_project_endpoint"; // Replace with your actual endpoint
    var credential = new DefaultAzureCredential();
    
    AzureAIInferenceClientOptions clientOptions = new AzureAIInferenceClientOptions();
    BearerTokenAuthenticationPolicy tokenPolicy = new BearerTokenAuthenticationPolicy(
        credential, 
        new string[] { "https://cognitiveservices.azure.com/.default" }
    );
    clientOptions.AddPolicy(tokenPolicy, HttpPipelinePosition.PerRetry);
    
    var client = new ChatCompletionsClient(
        endpointUrl, 
        credential,
        clientOptions
    );
    ```

::: zone-end

<a name="azure-ai-foundry-agent-service"></a>
* Using the project endpoint, you can:
    - [Use Foundry Model](../../quickstarts/get-started-code.md), including Azure OpenAI
    - [Use Foundry Agent Service](../../../ai-services/agents/quickstart.md?context=/azure/ai-foundry/context/context)
    - [Run evaluations in the cloud](../../../ai-services/openai/how-to/evaluations.md?context=/azure/ai-foundry/context/context)
    - [Enable tracing for your app](../../concepts/trace.md) 
    - Retrieve endpoints and keys for external resource connections

## Azure AI Services client libraries

To use Azure AI services, you can use the following client libraries with the endpoints listed on the project homepage.

<!-- ::: zone pivot="programming-language-cpp"
[!INCLUDE [C++ include](../../includes/sdk/cpp.md)]
::: zone-end -->

::: zone pivot="programming-language-csharp"
[!INCLUDE [C# include](../../includes/sdk/csharp.md)]
::: zone-end

::: zone pivot="programming-language-go"
[!INCLUDE [Go include](../../includes/sdk/go.md)]
::: zone-end

::: zone pivot="programming-language-java"
[!INCLUDE [Java include](../../includes/sdk/java.md)]
::: zone-end

::: zone pivot="programming-language-javascript"
[!INCLUDE [JavaScript include](../../includes/sdk/javascript.md)]
::: zone-end

<!-- ::: zone pivot="programming-language-objectivec"
[!INCLUDE [ObjectiveC include](../../includes/sdk/objective-c.md)]
::: zone-end -->

::: zone pivot="programming-language-python"
[!INCLUDE [Python include](./../../includes/sdk/python.md)]
::: zone-end

<!-- ::: zone pivot="programming-language-swift"
[!INCLUDE [Swift include](../../includes/sdk/swift.md)]
::: zone-end -->
