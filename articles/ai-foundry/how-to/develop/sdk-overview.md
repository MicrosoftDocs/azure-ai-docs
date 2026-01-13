---
title: Get started with Microsoft Foundry SDKs and Endpoints
titleSuffix: Microsoft Foundry
description: This article provides an overview of the Microsoft Foundry SDKs and endpoints and how to get started using them.
ms.service: azure-ai-foundry
ms.custom:
  - build-2024
  - ignite-2024
  - dev-focus
ai-usage: ai-assisted
ms.topic: how-to
ms.date: 01/13/2026
ms.reviewer: dantaylo
ms.author: johalexander
author: ms-johnalex
zone_pivot_groups: foundry-sdk-overview-languages
monikerRange: foundry-classic || foundry
# customer intent: I want to learn how to use the Microsoft Foundry SDK and endpoints to build AI applications on Azure.
---

# Microsoft Foundry SDKs and Endpoints

[!INCLUDE [version-banner](../../includes/version-banner.md)]

Use this how-to to connect to your Microsoft Foundry project fast. You'll install the language package you need, authenticate with Microsoft Entra ID, and run a quick call to confirm the SDK can reach your Foundry or Azure OpenAI endpoint.

With the SDK ready, you can:

- Access models from multiple providers through a single project endpoint
- Combine models, data, and Foundry Tools to power agents and applications
- Evaluate, debug, and monitor app quality across development, testing, and production

If you need a conceptual overview before diving in, see [What is Azure AI Foundry](../../what-is-azure-ai-foundry.md).


## Prerequisites

- [!INCLUDE [azure-subscription](../../includes/azure-subscription.md)]

- Have one of the following Azure RBAC roles to create and manage Foundry resources:
  - **Azure AI User** (least-privilege role for development)
  - **Azure AI Project Manager** (for managing Foundry projects)
  - **Contributor** or **Owner** (for subscription-level permissions)
  
  For details on each role's permissions, see [Role-based access control for Microsoft Foundry](/azure/ai-foundry/concepts/rbac-azure-ai-foundry).

- Install the required language runtimes, global tools, and VS Code extensions as described in [Prepare your development environment](install-cli-sdk.md).

> [!IMPORTANT]
> Before starting, make sure your development environment is ready.  
> This article focuses on **scenario-specific steps** like SDK installation, authentication, and running sample code.
>

## Foundry SDK

Developers using Microsoft Foundry need flexibility to combine AI features in one workflow. These SDKs give you building blocks to provision resources, orchestrate agents, and connect to Foundry Tools. Pick the right library to streamline development, cut complexity, and help your solutions scale across Foundry projects and external endpoints.

The Foundry API Endpoint grants users access to Agents, Evaluations, and deployed models for inference and more.

> [!IMPORTANT]
> Endpoints use your resource name or a custom subdomain. If your organization set up a custom subdomain, replace `your-resource-name` with `your-custom-subdomain` in all examples.
> For example:
> - `https://<your-resource-name>.services.ai.azure.com`
> - `https://<your-custom-subdomain>.services.ai.azure.com`

Foundry simplifies endpoint management by combining endpoints. Fewer endpoints make them easier to manage. Your current endpoints still work. To find every endpoint, open the Azure portal resource details page. Select **JSON view** to list all Foundry capabilities and endpoints.

For some operations, the Foundry SDK and API reuse the OpenAI SDK and API. This makes it easy to switch from OpenAI to Foundry while gaining more features. Use a Project client to access the OpenAI SDK for tasks like using the Responses API, fine-tuning, or running an agent.

* With the Foundry endpoint, you can:
    - [Access Foundry Models](../../quickstarts/get-started-code.md), including Azure OpenAI
    - [Use the Foundry Agent Service](../../../ai-services/agents/quickstart.md?context=/azure/ai-foundry/context/context)
    - [Run cloud evaluations](cloud-evaluation.md)
    - [Enable app tracing](../../concepts/trace.md)
    - [Fine-tune a model](/azure/ai-foundry/openai/how-to/fine-tuning?view=foundry&tabs=azure-openai&pivots=programming-language-python&preserve-view=true)
    - Get endpoints and keys for Foundry Tools, local orchestration, and more.

This section provides code examples to get started using the Foundry SDK in your preferred programming language.

::: moniker range="foundry-classic"

> [!NOTE]
> This article applies to a **[!INCLUDE [fdp](../../includes/fdp-project-name.md)]**. The code shown here doesn't work for a **[!INCLUDE [hub](../../includes/hub-project-name.md)]**. For more information, see [Types of projects](../../what-is-azure-ai-foundry.md#types-of-projects).

::: moniker-end

> [!TIP]
> These code samples are starting points. Use these clients to interact with models, run evaluations, and more, as explained in the client libraries section.

::: zone pivot="programming-language-python"

The [Azure AI Projects client library for Python](/python/api/overview/azure/ai-projects-readme?view=azure-python-preview&preserve-view=true) is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.

* Install the project client library 

    ::: moniker range="foundry-classic"
    Run this command to install the stable packages for Foundry classic projects.
    ```bash
    pip install azure-ai-projects azure-identity openai
    ```
    When the installation succeeds, pip prints each package version so you can confirm the setup.
    ::: moniker-end
    ::: moniker range="foundry"
    Run these commands to install the preview packages for Foundry projects.
    ```bash
    pip install --pre azure-ai-projects
    pip install azure-identity openai
    ```
    When the commands finish, pip displays installation summaries for each package.
    ::: moniker-end

* Create a project client in code. **Copy** the Foundry project endpoint from the Overview page of the project and update the endpoint string value.

    This snippet authenticates with `DefaultAzureCredential` and constructs an `AIProjectClient` for your Foundry project endpoint.
    ```python
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    
    project = AIProjectClient(
      endpoint="https://<your-resource-name>.services.ai.azure.com",  # Replace with your endpoint
      credential=DefaultAzureCredential())
    # The AIProjectClient lets you access models, data, and services in your project.
    ```

When the client initializes, you can use it to access models, data, and services in your project.

::: zone-end

::: zone pivot="programming-language-java"

The [Azure AI Projects client library for Java (preview)](/java/api/overview/azure/ai-projects-readme) is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

* Add these packages to your installation:
    * `com.azure.ai.projects`
    * `com.azure.core`

* Create a project client in code. **Copy** the Foundry project endpoint from the Overview page of the project and update the connections string value.

    This snippet builds a `ProjectsClient` with `DefaultAzureCredential` so you can access your Foundry project endpoint.
    ```java
    import com.azure.ai.projects.ProjectsClient;
    import com.azure.ai.projects.ProjectsClientBuilder;
    import com.azure.core.credential.AzureKeyCredential;
    import com.azure.identity.DefaultAzureCredentialBuilder;
    
    String endpoint ="https://<your-resource-name>.services.ai.azure.com"; // Replace with your endpoint
    
    ProjectsClient projectClient = new ProjectsClientBuilder()
        .credential(new DefaultAzureCredentialBuilder().build())
        .endpoint(endpoint)
        .buildClient();
    // The ProjectsClient enables unified access to your project's resources.
    ```

When the client builds successfully, you can call it to access project resources.

::: zone-end

::: zone pivot="programming-language-javascript"

The [Azure AI Projects client library for JavaScript](/javascript/api/overview/azure/ai-projects-readme) is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.

* Install dependencies (preview):

    ::: moniker range="foundry-classic"
    Run this command to install the current JavaScript packages for Foundry classic projects.
    ```bash
    npm install @azure/ai-projects @azure/identity
    ```
    When the installation completes, npm lists the packages it added to your project.
    ::: moniker-end
    ::: moniker range="foundry"
    Run this command to install the preview JavaScript packages for Foundry projects.
    ```bash
    npm install @azure/ai-projects@beta @azure/identity
    ```
    When the installation completes, npm prints the package tree so you can verify the dependency versions.
    ::: moniker-end

* Create a project client in code. **Copy** the Foundry project endpoint from the Overview page of the project and update the endpoint string value.

    This snippet authenticates with `DefaultAzureCredential` and constructs an `AIProjectClient` instance for JavaScript.
    ```javascript
    import { AIProjectClient } from '@azure/ai-projects';
    import { DefaultAzureCredential } from '@azure/identity';
    
    const endpoint = "https://<your-resource-name>.services.ai.azure.com"; // Replace with your actual endpoint

    const project = new AIProjectClient(endpoint, new DefaultAzureCredential());
    // The AIProjectClient lets you access models, data, and services in your project.
    ```

When the client initializes, you can call it to work with models, data, and services in your project.

::: zone-end

::: zone pivot="programming-language-csharp"

The [Azure AI Projects client library for .NET](/dotnet/api/overview/azure/ai.projects-readme) is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.

* Install packages:

    Run this command to add the Azure.AI.Projects package to your .NET project.
    ```bash
    dotnet add package Azure.AI.Projects --version 1.2
    ```
When the install succeeds, the .NET CLI reports that it added the package and its dependencies.

* Create a project client in code. **Copy** the Foundry project endpoint from the Overview page of the project and update the endpointUrl string value.

    This snippet authenticates with `DefaultAzureCredential`, configures an `AIProjectClient`, and prepares it for retries with a token policy.
    ```csharp
    using Azure.AI.Projects;
    using Azure.AI.Projects.OpenAI;
    using Azure.Identity;
    using OpenAI;
    using OpenAI.Responses;
    using System.ClientModel.Primitives;
    using System;

    string projectEndpointUrl = "https://<your-resource-name>.services.ai.azure.com"; // Replace with your endpoint

    DefaultAzureCredential credential = new();
    BearerTokenPolicy tokenPolicy = new(credential, "https://cognitiveservices.azure.com/.default");

    AIProjectClient projectClient = new(endpoint: new Uri(projectEndpointUrl), tokenProvider: new DefaultAzureCredential());        
    // The AIProjectClient lets you access models, data, and services in your project.

    const string deploymentName = "gpt-4.1";
    
    OpenAIResponseClient modelResponseClient = projectClient.OpenAI.GetProjectResponsesClientForModel(deploymentName);
    OpenAIResponse modelResponse = modelResponseClient.CreateResponse("Tell me a C# joke in the style of a deadpan standup comic.");
    
    Console.WriteLine("Model response: " + modelResponse.GetOutputText());
    ```

When the client builds successfully, you can call it to manage models, evaluations, and other project resources.

::: zone-end

### Which endpoint should you use when working with OpenAI?

- **Starting with Foundry Agents Service?** Use the Foundry Project endpoint with the Foundry SDK. Authenticate with Microsoft Entra ID to get your OpenAI client from the Project. 
    - Use this endpoint for tasks like working with models and agents, running agent evaluations, fine-tuning models, and related operations.
    - For non-OpenAI models using the responses API, use the OpenAI client from the Foundry SDK.
- **Using other OpenAI code?** Use the Azure OpenAI endpoint with the OpenAI SDK. Authenticate with Microsoft Entra ID.
    - Access all Azure OpenAI features, including audio transcription and image generation.
    - Some extended features from Foundry Agents Service might need extra configuration.
- If you use API keys, choose the v1 endpoint: `https://<YOUR-RESOURCE-NAME>.openai.azure.com/openai/v1/`.
  
## OpenAI SDK

The OpenAI SDK lets you interact with the Azure OpenAI service. It offers a simple interface for making API calls and managing authentication. The OpenAI SDK directly calls the Azure OpenAI endpoint. To use OpenAI models with full OpenAI support, then use the v1 endpoint: `https://<YOUR-RESOURCE-NAME>.openai.azure.com/openai/v1/` and OpenAI SDK directly.

### Create an OpenAI client from your project

::: zone pivot="programming-language-python"

::: moniker range="foundry-classic"
This snippet uses the `AIProjectClient` to request an OpenAI client scoped to your project.
```python
# Use the AIProjectClient to create an OpenAI client for your project
openai_client = project.get_openai_client(api_version="api_version")
response = openai_client.responses.create(
    model="gpt-4.1-mini",
    input="What is the size of France in square miles?",
)
print(f"Response output: {response.output_text}")
```

When the call succeeds, the client returns response content that you can log or process in your app.

The following code snippet demonstrates how to use the Azure OpenAI v1 endpoint with the OpenAI client for responses.

This snippet authenticates with `DefaultAzureCredential`, retrieves a bearer token, and sends a request to the Azure OpenAI v1 endpoint.

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

When the request succeeds, the client prints the JSON payload so you can inspect the generated content.

For more information on using the OpenAI SDK, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?view=foundry-classic&tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-python&preserve-view=true).
::: moniker-end
::: moniker range="foundry"

This snippet uses the `AIProjectClient` to request an OpenAI client from your Foundry project.

```python
# Use the AIProjectClient to create an OpenAI client for your project
openai_client = project.get_openai_client()
response = openai_client.responses.create(
    model="gpt-4.1-mini",
    input="What is the size of France in square miles?",
)
print(f"Response output: {response.output_text}")
```

When the call succeeds, the client returns response text that you can display or log.

The following code snippet demonstrates how to use the Azure OpenAI v1 endpoint with the OpenAI client for responses.

This snippet authenticates with `DefaultAzureCredential`, obtains a token provider, and submits a responses request to the Azure OpenAI v1 endpoint.

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

When the request succeeds, the client prints the JSON payload so you can verify the generated output.
For more information on using the OpenAI SDK, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?view=foundry&tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-python&preserve-view=true)
::: moniker-end

::: zone-end

::: zone pivot="programming-language-java"

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

This snippet retrieves an `OpenAIClient` from the `ProjectsClient` so you can send OpenAI requests through Foundry.

```java
// 
OpenAIClient openAIClient = projectClient.getOpenAIClient();
```

When the call succeeds, you can invoke OpenAI operations by using the returned client.
::: moniker range="foundry-classic"
For more information on using the OpenAI SDK, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?view=foundry-classic&tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-java&preserve-view=true).
::: moniker-end
::: moniker range="foundry"
For more information on using the OpenAI SDK, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?view=foundry&tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-java&preserve-view=true)
::: moniker-end
::: zone-end

::: zone pivot="programming-language-javascript"

This snippet uses the project client to create an OpenAI client you can reuse across requests.

```javascript
// Use the AIProjectClient to create an OpenAI client for your project
const openAIClient = await project.getOpenAIClient();
```

When the call resolves, you receive an `openAIClient` instance that you can use for responses and other OpenAI operations.

::: moniker range="foundry-classic"
For more information on using the OpenAI SDK, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?view=foundry-classic&tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-javascript&preserve-view=true).
::: moniker-end
::: moniker range="foundry"
For more information on using the OpenAI SDK, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?view=foundry&tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-javascript&preserve-view=true)
::: moniker-end

::: zone-end

::: zone pivot="programming-language-csharp"

1. Install the OpenAI package:

    Run this command to add the OpenAI client library to your .NET project.
    ```bash
    
    dotnet add package OpenAI
    ```
When it succeeds, the .NET CLI confirms that it installed the `OpenAI` package.
1. The following code snippet demonstrates how to create the OpenAI client directly using the Azure OpenAI v1 endpoint.

    This snippet configures `DefaultAzureCredential`, builds `OpenAIClientOptions`, and creates a `ResponseClient` for the Azure OpenAI v1 endpoint.
    ```csharp
    using Azure.Identity;
    using Azure.Core;
    using OpenAI;
    using System;
    using System.ClientModel.Primitives;
    
    #pragma warning disable OPENAI001 

    const string directModelEndpoint  = "https://<YOUR-RESOURCE-NAME>.openai.azure.com/openai/v1/"; // Replace with your endpoint
    const string deploymentName = "gpt-4.1";    

    BearerTokenPolicy tokenPolicy = new(
        new DefaultAzureCredential(),
        "https://cognitiveservices.azure.com/.default");
    
    OpenAIResponseClient client = new(
        model: deploymentName,
        authenticationPolicy: tokenPolicy,
        options: new OpenAIClientOptions()
        {
            Endpoint = new($"{directModelEndpoint}"),
        });
    ResponseCreationOptions options = new ResponseCreationOptions
    {
        Temperature = (float)0.7,
    };
    
    OpenAIResponse modelDirectResponse = client.CreateResponse(
         [
            ResponseItem.CreateUserMessageItem("What is the size of France in square miles?"),
         ], options);
    
    Console.WriteLine($"[ASSISTANT]: {modelDirectResponse.GetOutputText()}");
    // The ResponseClient lets you interact with models and services in your project.
    ```

When the client instantiates successfully, you can call it to send responses requests to your Azure OpenAI deployment.

::: moniker range="foundry-classic"
For more information on using the OpenAI SDK, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?view=foundry-classic&tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-programming-language-dotnet&preserve-view=true).
::: moniker-end
::: moniker range="foundry"
For more information on using the OpenAI SDK, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?view=foundry&tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-programming-language-dotnet&preserve-view=true)
::: moniker-end

::: zone-end

## Using the Agent Framework for local orchestration

Microsoft Agent Framework is an open-source development kit for building AI agents and multi-agent workflows for .NET and Python. It provides a way to build and manage AI agents that can interact with users and other services. It can orchestrate agents in Foundry, or have local agents that use Foundry models. 

For more information, see the [Microsoft Agent Framework overview](/agent-framework/overview/agent-framework-overview)

 The next section lists the Foundry Tools client libraries and shows how to use them.

## Foundry Tools SDKs

To use Foundry Tools, you can use the following SDKs with the endpoints listed.

### Which Azure AI Services endpoint should you use?

Choose an endpoint based on your needs:

Use the Azure AI Services endpoint to access Computer Vision, Content Safety, Document Intelligence, Language, Translation, and Token Foundry Tools.

Azure AI Services endpoint: `https://<YOUR-RESOURCE-NAME>.cognitiveservices.azure.com/`

> [!NOTE]
> Endpoints use either your resource name or a custom subdomain. If your organization set up a custom subdomain, replace `your-resource-name` with `your-custom-subdomain` in all endpoint examples.

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
