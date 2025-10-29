---
title: How to get started with Azure AI Foundry SDK
titleSuffix: Azure AI Foundry
description: This article provides an overview of the Azure AI Foundry SDK and how to get started using it.
ms.service: azure-ai-foundry
ms.custom:
  - build-2024
  - ignite-2024
ai-usage: ai-assisted
ms.topic: how-to
ms.date: 09/15/2025
ms.reviewer: dantaylo
ms.author: johalexander
author: ms-johnalex
zone_pivot_groups: foundry-sdk-overview-languages
# customer intent: I want to learn how to use the Azure AI Foundry SDK to build AI applications on Azure.
---

# Azure AI Foundry SDK client libraries

The Azure AI Foundry SDK is a comprehensive toolchain designed to simplify the development of AI applications on Azure. It enables developers to:

- Access popular models from various model providers through a single interface
- Easily combine together models, data, and AI services to build AI-powered applications
- Evaluate, debug, and improve application quality & safety across development, testing, and production environments

The Azure AI Foundry SDK is a set of client libraries and services designed to work together. 

> [!NOTE]
> This article applies to a **[!INCLUDE [fdp](../../includes/fdp-project-name.md)]**. The code shown here doesn't work for a **[!INCLUDE [hub](../../includes/hub-project-name.md)]**. For more information, see [Types of projects](../../what-is-azure-ai-foundry.md#project-types).

## Prerequisites

* [!INCLUDE [azure-subscription](../../includes/azure-subscription.md)]
* [Create a [!INCLUDE [fdp-project-name](../../includes/fdp-project-name.md)]](../create-projects.md) if you don't have one already.
* [!INCLUDE [find-endpoint](../../includes/find-endpoint.md)]
* Sign in with the Azure CLI using the same account that you use to access your project:

    ```bash
    az login
    ```

## Unified Projects client library

The following examples show how to connect to your Azure AI Foundry project using different programming languages. This connection is the first step to accessing models, data, and AI services through the SDK. Each code block demonstrates how to authenticate and create a client for your project endpoint.

> [!TIP]
> The code samples below are starting points. You’ll use these clients to interact with models, run evaluations, and more, as described in the client libraries section below.


::: zone pivot="programming-language-python"

The [Azure AI Foundry Projects client library for Python](/python/api/overview/azure/ai-projects-readme) is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.

* Install the project client library 

    ```bash
    pip install azure-ai-projects azure-identity
    ```

* Create a project client in code. **Copy** the Azure AI Foundry project endpoint from the Overview page of the project and update the connections string value.

    ```python
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    
    project = AIProjectClient(
      endpoint="your_project_endpoint",  # Replace with your endpoint
      credential=DefaultAzureCredential())
    # The AIProjectClient lets you access models, data, and services in your project.
    ```
::: zone-end

::: zone pivot="programming-language-java"

The [Azure AI Foundry Projects client library for Java (preview)](/java/api/overview/azure/ai-projects-readme) is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

* Add these packages to your installation:
    * `com.azure.ai.projects`
    * `com.azure.core`

* Create a project client in code. **Copy** the Azure AI Foundry project endpoint from the Overview page of the project and update the connections string value.

    ```java
    import com.azure.ai.projects.ProjectsClient;
    import com.azure.ai.projects.ProjectsClientBuilder;
    import com.azure.core.credential.AzureKeyCredential;
    
    String endpoint ="your_project_endpoint"; // Replace with your endpoint
    
    ProjectsClient projectClient = new ProjectsClientBuilder()
        .credential(new DefaultAzureCredential())
        .endpoint(endpoint)
        .buildClient();
    // The ProjectsClient enables unified access to your project's resources.
    ```



::: zone-end

::: zone pivot="programming-language-javascript"

The [Azure AI Foundry Projects client library for JavaScript](/javascript/api/overview/azure/ai-projects-readme) is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.

* Install dependencies (preview):

    ```bash
    npm install @azure/ai-projects @azure/identity
    ```

* Create a project client in code. **Copy** the Azure AI Foundry project endpoint from the Overview page of the project and update the connections string value.


    ```javascript
    import { AIProjectClient } from '@azure/ai-projects';
    import { DefaultAzureCredential } from '@azure/identity';
    
    const endpoint = "your_project_endpoint"; // Replace with your actual endpoint
    const project = new AIProjectClient(endpoint, new DefaultAzureCredential());
    const projectClient = await project.getAzureOpenAIClient({
        // The API version should match the version of the Azure OpenAI resource
        apiVersion: "2024-12-01-preview"
    });
    // The AIProjectClient lets you access models, data, and services in your project.
    ```


::: zone-end

::: zone pivot="programming-language-csharp"

The [Azure AI Foundry Projects client library for .NET](/dotnet/api/overview/azure/ai.projects-readme) is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.

* Install packages:

    ```bash
    dotnet add package Azure.Identity
    dotnet add package Azure.Core
    dotnet add package Azure.AI.Inference
    ```

* Create a project client in code. **Copy** the Azure AI Foundry project endpoint from the Overview page of the project and update the connections string value.

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
    // The PerRetry position ensures the authentication policy is applied to every retry attempt.
    // This is important for robust authentication in distributed/cloud environments.
    clientOptions.AddPolicy(tokenPolicy, HttpPipelinePosition.PerRetry);
    
    var projectClient = new ChatCompletionsClient(
        endpointUrl, 
        credential,
        clientOptions
    );
    // The ChatCompletionsClient lets you interact with models and services in your project.
    ```

::: zone-end

After you create a client, you can use it to access models, run evaluations, and connect to other AI services. The next section lists the available client libraries and shows how to use them for specific Azure AI services.

<a name="azure-ai-foundry-agent-service"></a>
* Using the project endpoint, you can:
    - [Use Foundry Model](../../quickstarts/get-started-code.md), including Azure OpenAI
    - [Use Foundry Agent Service](../../../ai-services/agents/quickstart.md?context=/azure/ai-foundry/context/context)
    - [Run evaluations in the cloud](cloud-evaluation.md))
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

<!-- ::: zone pivot="programming-language-go"
[!INCLUDE [Go include](../../includes/sdk/go.md)]
::: zone-end -->

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
