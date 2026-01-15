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
ms.date: 01/15/2026
ms.reviewer: dantaylo
ms.author: johalexander
author: ms-johnalex
zone_pivot_groups: foundry-sdk-overview-languages
monikerRange: foundry-classic || foundry
# customer intent: I want to learn how to use the Microsoft Foundry SDK and endpoints to build AI applications on Azure.
---

# Microsoft Foundry SDKs and Endpoints

[!INCLUDE [version-banner](../../includes/version-banner.md)]

Creating a Foundry resource unlocks access to models, agents, and tools through a unified set of SDKs and endpoints. This article covers what each SDK is for and which endpoint to use.

| SDK | What it's for | Endpoint |
| --- | --- | --- |
| **Foundry SDK** | Foundry-specific capabilities with OpenAI-compatible interfaces. Includes access to Foundry direct models through the Responses API (not Chat Completions). | `https://<resource-name>.services.ai.azure.com/api/projects/<project-name>` |
| **OpenAI SDK** | Latest OpenAI SDK models and features with the full OpenAI API surface. Foundry direct models available through Chat Completions API (not Responses). | `https://<resource-name>.openai.azure.com/openai/v1` |
| **Foundry Tools SDKs** | Prebuilt solutions (Vision, Speech, Content Safety, and more). | Tool-specific endpoints (varies by service). |
| **Agent Framework** | Multi-agent orchestration in code. Cloud-agnostic. | Uses the project endpoint via the Foundry SDK. |

> [!NOTE]
> **Resource types:** A Foundry resource provides all endpoints previously listed. An Azure OpenAI resource provides only the `/openai/v1` endpoint.
>
> **Authentication:** Samples here use Microsoft Entra ID (`DefaultAzureCredential`). API keys work on `/openai/v1`. Pass the key as `api_key` instead of a token provider.


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

The Foundry SDK connects to a single project endpoint that provides access to the most popular Foundry capabilities:

```
https://<resource-name>.services.ai.azure.com/api/projects/<project-name>
```

> [!NOTE]
> If your organization uses a custom subdomain, replace `<resource-name>` with `<your-custom-subdomain>` in the endpoint URL.

This simplifies application configuration. Instead of managing multiple endpoints, you configure one.

### Install the SDK

::: moniker range="foundry-classic"

> [!NOTE]
> This article applies to a **[!INCLUDE [fdp](../../includes/fdp-project-name.md)]**. The code shown here doesn't work for a **[!INCLUDE [hub](../../includes/hub-project-name.md)]**. For more information, see [Types of projects](../../what-is-azure-ai-foundry.md#types-of-projects).

::: moniker-end

> [!NOTE]
> **SDK versions:** The 2.x preview SDK targets the new Foundry portal and API. The 1.x GA SDK targets Foundry classic. Make sure the samples you follow match your installed package.

::: zone pivot="programming-language-python"

The [Azure AI Projects client library for Python](/python/api/overview/azure/ai-projects-readme?view=azure-python-preview&preserve-view=true) is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.

::: moniker range="foundry-classic"
Run this command to install the stable packages for Foundry classic projects.
```bash
pip install azure-ai-projects azure-identity openai
```
::: moniker-end
::: moniker range="foundry"
Run these commands to install the preview packages for Foundry projects.
```bash
pip install --pre azure-ai-projects
pip install azure-identity openai
```
::: moniker-end

::: zone-end

::: zone pivot="programming-language-java"

The [Azure AI Projects client library for Java (preview)](/java/api/overview/azure/ai-projects-readme) is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Add these packages to your installation:
* `com.azure.ai.projects`
* `com.azure.core`

::: zone-end

::: zone pivot="programming-language-javascript"

The [Azure AI Projects client library for JavaScript](/javascript/api/overview/azure/ai-projects-readme) is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.

::: moniker range="foundry-classic"
Run this command to install the current JavaScript packages for Foundry classic projects.
```bash
npm install @azure/ai-projects @azure/identity
```
::: moniker-end
::: moniker range="foundry"
Run this command to install the preview JavaScript packages for Foundry projects.
```bash
npm install @azure/ai-projects@beta @azure/identity
```
::: moniker-end

::: zone-end

::: zone pivot="programming-language-csharp"

The [Azure AI Projects client library for .NET](/dotnet/api/overview/azure/ai.projects-readme) is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.

Run this command to add the Azure.AI.Projects package to your .NET project.
```bash
dotnet add package Azure.AI.Projects --version 1.2
```

::: zone-end

### Using the Foundry SDK

The SDK exposes two client types because Foundry and OpenAI have different API shapes:

- **Project client** – Use for Foundry-native operations where OpenAI has no equivalent. Examples: listing connections, retrieving project properties, enabling tracing.
- **OpenAI-compatible client** – Use for Foundry functionality that builds on OpenAI concepts. The Responses API, agents, evaluations, and fine-tuning all use OpenAI-style request/response patterns. This client also gives you access to Foundry direct models (non-Azure-OpenAI models hosted in Foundry). The project endpoint serves this traffic on the `/openai` route.

Most apps use both clients. Use the project client for setup and configuration, then use the OpenAI-compatible client for running agents, evaluations, and calling models (including Foundry direct models).

::: zone pivot="programming-language-python"

**Create a project client:**

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

project = AIProjectClient(
  endpoint="https://<resource-name>.services.ai.azure.com/api/projects/<project-name>",
  credential=DefaultAzureCredential())
```

**Create an OpenAI-compatible client from your project:**

```python
openai_client = project.inference.get_azure_openai_client(api_version="2024-10-21")
response = openai_client.responses.create(
    model="gpt-5.2",
    input="What is the speed of light?",
)
print(response.output_text)
```

::: zone-end

::: zone pivot="programming-language-java"

**Create a project client:**

```java
import com.azure.ai.projects.ProjectsClient;
import com.azure.ai.projects.ProjectsClientBuilder;
import com.azure.identity.DefaultAzureCredentialBuilder;

String endpoint = "https://<resource-name>.services.ai.azure.com/api/projects/<project-name>";

ProjectsClient projectClient = new ProjectsClientBuilder()
    .credential(new DefaultAzureCredentialBuilder().build())
    .endpoint(endpoint)
    .buildClient();
```

**Create an OpenAI-compatible client from your project:**

```java
OpenAIClient openAIClient = projectClient.getOpenAIClient();
```

::: zone-end

::: zone pivot="programming-language-javascript"

**Create a project client:**

```javascript
import { AIProjectClient } from '@azure/ai-projects';
import { DefaultAzureCredential } from '@azure/identity';

const endpoint = "https://<resource-name>.services.ai.azure.com/api/projects/<project-name>";
const project = new AIProjectClient(endpoint, new DefaultAzureCredential());
```

**Create an OpenAI-compatible client from your project:**

```javascript
const openAIClient = await project.getOpenAIClient();
```

::: zone-end

::: zone pivot="programming-language-csharp"

**Create a project client:**

```csharp
using Azure.AI.Projects.OpenAI; 
using Azure.Identity;
using OpenAI.Responses;

string endpoint = "https://<resource-name>.services.ai.azure.com/api/projects/<project-name>";

AIProjectClient projectClient = new(
    endpoint: new Uri(endpoint), 
    tokenProvider: new DefaultAzureCredential());
```

**Create an OpenAI-compatible client from your project:**

```csharp
#pragma warning disable OPENAI001
OpenAIResponseClient responseClient = projectClient.OpenAI.GetProjectResponsesClientForModel("gpt-5.2");
OpenAIResponse response = responseClient.CreateResponse("What is the speed of light?");
Console.WriteLine(response.GetOutputText());
#pragma warning restore OPENAI001
```

::: zone-end

### What you can do with the Foundry SDK

- [Access Foundry Models](../../quickstarts/get-started-code.md), including Azure OpenAI
- [Use the Foundry Agent Service](../../../ai-services/agents/quickstart.md?context=/azure/ai-foundry/context/context)
- [Run cloud evaluations](cloud-evaluation.md)
- [Enable app tracing](../../concepts/trace.md)
- [Fine-tune a model](/azure/ai-foundry/openai/how-to/fine-tuning?view=foundry&tabs=azure-openai&pivots=programming-language-python&preserve-view=true)
- Get endpoints and keys for Foundry Tools, local orchestration, and more

## OpenAI SDK

Use the OpenAI SDK when you want the full OpenAI API surface and maximum client compatibility. This endpoint provides access to Azure OpenAI models and Foundry direct models (via Chat Completions API). It does not provide access to Foundry-specific features like agents and evaluations.

### Create an OpenAI client from your project

::: zone pivot="programming-language-python"

::: moniker range="foundry-classic"
This snippet uses the `AIProjectClient` to request an OpenAI client scoped to your project.
```python
# Use the AIProjectClient to create an OpenAI client for your project
openai_client = project.get_openai_client(api_version="2024-10-21")
response = openai_client.responses.create(
    model="gpt-5.2",
    input="What is the size of France in square miles?",
)
print(f"Response output: {response.output_text}")
```

The following snippet shows how to use the Azure OpenAI `/openai/v1` endpoint directly.

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://<resource-name>.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

response = client.responses.create(
    model="model_deployment_name",
    input= "What is the size of France in square miles?" 
)

print(response.model_dump_json(indent=2)) 
```

For more information, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?view=foundry-classic&tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-python&preserve-view=true).
::: moniker-end
::: moniker range="foundry"

This snippet uses the `AIProjectClient` to request an OpenAI client from your Foundry project.

```python
# Use the AIProjectClient to create an OpenAI client for your project
openai_client = project.get_openai_client()
response = openai_client.responses.create(
    model="gpt-5.2",
    input="What is the size of France in square miles?",
)
print(f"Response output: {response.output_text}")
```

The following snippet shows how to use the Azure OpenAI `/openai/v1` endpoint directly.

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://<resource-name>.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

response = client.responses.create(
    model="model_deployment_name",
    input= "What is the size of France in square miles?" 
)

print(response.model_dump_json(indent=2)) 
```

For more information, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?view=foundry&tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-python&preserve-view=true)
::: moniker-end

::: zone-end

::: zone pivot="programming-language-java"

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

This snippet retrieves an `OpenAIClient` from the `ProjectsClient` so you can send OpenAI requests through Foundry.

```java
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

This snippet uses the project client to create an OpenAI client you can reuse across requests.

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
 
    const string directModelEndpoint  = "https://<resource-name>.openai.azure.com/openai/v1/";
    const string deploymentName = "gpt-5.2";    

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
    #pragma warning restore OPENAI001
    // The ResponseClient lets you interact with models and services in your project.
    ```


::: moniker range="foundry-classic"
For more information on using the OpenAI SDK, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?view=foundry-classic&tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-programming-language-dotnet&preserve-view=true).
::: moniker-end
::: moniker range="foundry"
For more information on using the OpenAI SDK, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?view=foundry&tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-programming-language-dotnet&preserve-view=true)
::: moniker-end

::: zone-end

## Using the Agent Framework for local orchestration

Microsoft Agent Framework is an open-source SDK for building multi-agent systems in code (for example, .NET and Python) with a cloud-provider-agnostic interface.

Use Agent Framework when you want to define and orchestrate agents locally. Pair it with the Foundry SDK when you want those agents to run against Foundry models or when you want Agent Framework to orchestrate agents hosted in Foundry.

For more information, see the [Microsoft Agent Framework overview](/agent-framework/overview/agent-framework-overview).

## Foundry Tools SDKs

Foundry Tools (formerly Azure AI Services) are prebuilt point solutions with dedicated SDKs. Use the following endpoints to work with Foundry Tools.

### Which endpoint should you use?

Choose an endpoint based on your needs:

Use the Azure AI Services endpoint to access Computer Vision, Content Safety, Document Intelligence, Language, Translation, and Token Foundry Tools.

Foundry Tools endpoint: `https://<your-resource-name>.cognitiveservices.azure.com/`

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
