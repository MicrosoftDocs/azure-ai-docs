---
title: Get started with Microsoft Foundry SDKs and Endpoints
titleSuffix: Microsoft Foundry
description: This article provides an overview of the Microsoft Foundry SDKs and endpoints and how to get started using them.
ms.service: azure-ai-foundry
ms.custom:
  - build-2024
  - ignite-2024
ai-usage: ai-assisted
ms.topic: how-to
ms.date: 11/24/2025
ms.reviewer: dantaylo
ms.author: johalexander
author: ms-johnalex
zone_pivot_groups: foundry-sdk-overview-languages
monikerRange: foundry-classic || foundry
# customer intent: I want to learn how to use the Microsoft Foundry SDK to build AI applications on Azure.
---

# Microsoft Foundry SDKs and Endpoints

[!INCLUDE [version-banner](../../includes/version-banner.md)]

This article describes the SDKs and endpoints you can use with your Foundry resource. It shows you how to connect to your project, access models from different providers, and use Foundry Tools. The SDK offers a unified way to work with AI resources through client libraries in multiple programming languages.

The Microsoft Foundry SDK simplifies AI application development on Azure. It lets developers:

- Access models from various providers through one interface
- Combine models, data, and AI services to build AI-powered applications
- Evaluate, debug, and improve application quality and safety in development, testing, and production

The Microsoft Foundry SDK integrates with other client libraries and services that work together. 

## Foundry SDK

Developers working with Microsoft Foundry need flexibility to integrate multiple AI capabilities into unified workflows. These SDKs provide the building blocks for provisioning resources, orchestrating agents, and connecting to specialized AI services. By choosing the right library, you can streamline development, reduce complexity, and ensure your solutions scale across Foundry projects and external endpoints.

::: moniker range="foundry-classic"

> [!NOTE]
> This article applies to a **[!INCLUDE [fdp](../../includes/fdp-project-name.md)]**. The code shown here doesn't work for a **[!INCLUDE [hub](../../includes/hub-project-name.md)]**. For more information, see [Types of projects](../../what-is-azure-ai-foundry.md#types-of-projects).

::: moniker-end

## Prerequisites

* [!INCLUDE [azure-subscription](../../includes/azure-subscription.md)]

::: moniker range="foundry-classic"
* [Create a [!INCLUDE [fdp-project-name](../../includes/fdp-project-name.md)]](../create-projects.md) if you don't have one already.
* [!INCLUDE [find-endpoint](../../includes/find-endpoint.md)]
::: moniker-end

::: moniker range="foundry"
* [!INCLUDE [find-endpoint](../../default/includes/find-endpoint.md)]
::: moniker-end

* Sign in with the Azure CLI using the same account that you use to access your project:

    ```bash
    az login
    ```

The following examples show how to authenticate and create a client for your project endpoint.

> [!TIP]
> These code samples are starting points. Use these clients to interact with models, run evaluations, and more, as explained in the client libraries section.

::: zone pivot="programming-language-python"

The [Azure AI Projects client library for Python](/python/api/overview/azure/ai-projects-readme?view=azure-python-preview&preserve-view=true) is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.

* Install the project client library 

    ::: moniker range="foundry-classic"
    ```bash
    pip install azure-ai-projects azure-identity openai
    ```
    ::: moniker-end
    ::: moniker range="foundry"
    ```bash
    pip install --pre azure-ai-projects
    pip install azure-identity openai
    ```
    ::: moniker-end

* Create a project client in code. **Copy** the Foundry project endpoint from the Overview page of the project and update the endpoint string value.

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

The [Azure AI Projects client library for Java (preview)](/java/api/overview/azure/ai-projects-readme) is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

* Add these packages to your installation:
    * `com.azure.ai.projects`
    * `com.azure.core`

* Create a project client in code. **Copy** the Foundry project endpoint from the Overview page of the project and update the connections string value.

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

The [Azure AI Projects client library for JavaScript](/javascript/api/overview/azure/ai-projects-readme) is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.

* Install dependencies (preview):

    ```bash
    npm install @azure/ai-projects @azure/identity
    ```

* Create a project client in code. **Copy** the Foundry project endpoint from the Overview page of the project and update the endpoint string value.


    ```javascript
    import { AIProjectClient } from '@azure/ai-projects';
    import { DefaultAzureCredential } from '@azure/identity';
    
    const endpoint = "your_project_endpoint"; // Replace with your actual endpoint

    const project = new AIProjectClient(endpoint, new DefaultAzureCredential());
    // The AIProjectClient lets you access models, data, and services in your project.
    ```

::: zone-end

::: zone pivot="programming-language-csharp"

The [Azure AI Projects client library for .NET](/dotnet/api/overview/azure/ai.projects-readme) is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.

* Install packages:

    ```bash
    dotnet add package Azure.Identity
    dotnet add package Azure.Core
    dotnet add package OpenAI
    ```

* Create a project client in code. **Copy** the Foundry project endpoint from the Overview page of the project and update the endpointUrl string value.

    ```csharp
    using Azure.Identity;
    using Azure.Core;
    using Azure.Core.Pipeline;
    using Azure.AI.Projects;
    using System;

    string endpointUrl = "your_project_endpoint"; // Replace with your endpoint

    DefaultAzureCredential credential = new();
    BearerTokenPolicy tokenPolicy = new(credential, "https://cognitiveservices.azure.com/.default");

    AIProjectClientOptions clientOptions = new AIProjectClientOptions();
    // The PerRetry position ensures the authentication policy is applied to every retry attempt.
    // This is important for robust authentication in distributed/cloud environments.
    clientOptions.AddPolicy(tokenPolicy, HttpPipelinePosition.PerRetry);

    AIProjectClient projectClient = new(new Uri(endpointUrl), new DefaultAzureCredential(), clientOptions);
    // The AIProjectClient lets you access models, data, and services in your project.
    ```

::: zone-end

## OpenAI SDK

The OpenAI SDK lets you interact with the Azure OpenAI service. It offers a simple interface for making API calls and managing authentication. The OpenAI SDK directly calls the Azure OpenAI endpoint. The following code snippet shows how to create the OpenAI client from the Project client for proper scoping and context management.

### Which endpoint should you use?
- **Managing a Project or calling Agents v2?** Use the Foundry Project endpoint with the Foundry SDK. Get your OpenAI client from the Project using Microsoft Entra ID for authentication.
- **Calling a model directly?** Use the Azure OpenAI endpoint with the OpenAI SDK with Microsoft Entra ID as the preferred authentication method. If using API keys, choose the v1 endpoint: `https://<YOUR-RESOURCE-NAME>.openai.azure.com/openai/v1/`.

### Create an OpenAI client from your project

::: zone pivot="programming-language-python"

::: moniker range="foundry-classic"
```python
# Use the AIProjectClient to create an OpenAI client for your project
openai_client = project.get_openai_client(api_version="api_version")
response = openai_client.responses.create(
    model="gpt-4.1-mini",
    input="What is the size of France in square miles?",
)
print(f"Response output: {response.output_text}")
```

The following code snippet demonstrates how to use the Azure OpenAI v1 endpoint with the OpenAI client for responses.

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://<YOUR-RESOURCE-NAME>.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

response = client.responses.create(
    model="model_deployment_name",
    input= "What is the size of France in square miles?" 
)

print(response.model_dump_json(indent=2)) 
```

For more information on using the OpenAI SDK, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?view=foundry-classic&tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-python&preserve-view=true).
::: moniker-end
::: moniker range="foundry"

```python
# Use the AIProjectClient to create an OpenAI client for your project
openai_client = project.get_openai_client()
response = openai_client.responses.create(
    model="gpt-4.1-mini",
    input="What is the size of France in square miles?",
)
print(f"Response output: {response.output_text}")
```

The following code snippet demonstrates how to use the Azure OpenAI v1 endpoint with the OpenAI client for responses.

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://<YOUR-RESOURCE-NAME>.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

response = client.responses.create(
    model="model_deployment_name",
    input= "What is the size of France in square miles?" 
)

print(response.model_dump_json(indent=2)) 
```
For more information on using the OpenAI SDK, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?view=foundry&tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-python&preserve-view=true)
::: moniker-end

::: zone-end

::: zone pivot="programming-language-java"

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

```java
// 
OpenAIClient openAIClient = projectClient.getOpenAIClient();
```
::: moniker range="foundry-classic"
For more information on using the OpenAI SDK, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?view=foundry-classic&tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-java&preserve-view=true).
::: moniker-end
::: moniker range="foundry"
For more information on using the OpenAI SDK, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?view=foundry&tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-java&preserve-view=true)
::: moniker-end
::: zone-end

::: zone pivot="programming-language-javascript"

```javascript
// Use the AIProjectClient to create an OpenAI client for your project
const openAIClient = await project.getOpenAIClient();
```

::: moniker range="foundry-classic"
For more information on using the OpenAI SDK, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?view=foundry-classic&tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-javascript&preserve-view=true).
::: moniker-end
::: moniker range="foundry"
For more information on using the OpenAI SDK, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?view=foundry&tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-javascript&preserve-view=true)
::: moniker-end

::: zone-end

::: zone pivot="programming-language-csharp"

1. Install the OpenAI package:

    ```bash
    dotnet add package OpenAI
    ```
1. The following code snippet demonstrates how to create the OpenAI client directly using the Azure OpenAI v1 endpoint.

    ```csharp
    using Azure.Identity;
    using Azure.Core;
    using Azure.Core.Pipeline;   
    using OpenAI;
    using System;
    using System.ClientModel.Primitives;
    
    endpointUrl = "https://<YOUR-RESOURCE-NAME>.openai.azure.com/openai/v1/"
    
    DefaultAzureCredential credential = new();
    BearerTokenPolicy tokenPolicy = new(credential, "https://cognitiveservices.azure.com/.default");
    
    OpenAIClientOptions clientOptions = new()
    {
        Endpoint = new Uri(endpointUrl)
    };
    
    // The PerRetry position ensures the authentication policy is applied to every retry attempt.
    // This is important for robust authentication in distributed/cloud environments.
    clientOptions.AddPolicy(tokenPolicy, HttpPipelinePosition.PerRetry);
    
    var projectClient = new ResponseClient(
        endpointUrl, 
        credential,
        clientOptions
    );
    // The ResponseClient lets you interact with models and services in your project.
    ```

::: moniker range="foundry-classic"
For more information on using the OpenAI SDK, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?view=foundry-classic&tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-programming-language-dotnet&preserve-view=true).
::: moniker-end
::: moniker range="foundry"
For more information on using the OpenAI SDK, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?view=foundry&tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-programming-language-dotnet&preserve-view=true)
::: moniker-end

::: zone-end

After you create a client, use it to access models, run evaluations, and connect to other AI services.

* Using the project endpoint, you can:
    - [Use Foundry Models](../../quickstarts/get-started-code.md), including Azure OpenAI
    - [Use Foundry Agent Service](../../../ai-services/agents/quickstart.md?context=/azure/ai-foundry/context/context)
    - [Run evaluations in the cloud](cloud-evaluation.md)
    - [Enable tracing for your app](../../concepts/trace.md) 
    - [Fine tune a model](/azure/ai-foundry/openai/how-to/fine-tuning?view=foundry&tabs=azure-openai&pivots=programming-language-python&preserve-view=true)
    - Retrieve endpoints and keys for external resource connections, such as Foundry Tools, local orchestration, and more.
    
 The next section lists the Foundry Tools client libraries and shows how to use them.

## Foundry Tools SDKs

To use Foundry Tools, you can use the following SDKs with the endpoints listed.

### Which endpoint should you use?

Choose an endpoint based on your needs:

Use the Azure AI Services endpoint to access Computer Vision, Content Safety, Document Intelligence, Language, Translation, and Token Foundry Tools.

Azure AI Services endpoint: `https://<YOUR-RESOURCE-NAME>.services.ai.azure.com/`

For Speech and Translation Foundry Tools, use the endpoints in the following tables. Replace placeholders with your resource information.

#### Speech Endpoints

| Foundry Tool | Endpoint |
| --- | --- |
|Speech to Text (Standard)|`https://<YOUR-RESOURCE-REGION>.stt.speech.microsoft.com`|
|Text to Speech (Neural)|`https://<YOUR-RESOURCE-REGION>.tts.speech.microsoft.com`|
|Custom Voice|`https://<YOUR-RESOURCE-NAME>.cognitiveservices.azure.com/`|

#### Translation Endpoints

| Foundry Tool | Endpoint |
| --- | --- |
|Text Translation|`https://api.cognitive.microsofttranslator.com/`|
|Document Translation|`https://<YOUR-RESOURCE-NAME>.cognitiveservices.azure.com/`|

The following sections include quickstart links for the Foundry Tools SDKs and reference information.

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

## Using the Agent Framework for local orchestration

Microsoft Agent Framework is an open-source development kit for building AI agents and multi-agent workflows for .NET and Python. It provides a way to build and manage AI agents that can interact with users and other services. It can orchestrate agents in Foundry, or have local agents that use Foundry models. 

For more information, see the [Microsoft Agent Framework overview](/agent-framework/overview/agent-framework-overview)