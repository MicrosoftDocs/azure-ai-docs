---
title: "Get started with Microsoft Foundry SDKs and Endpoints (temp)"
description: "This article provides an overview of the Microsoft Foundry SDKs and endpoints and how to get started using them. (temp)"
ms.service: azure-ai-foundry
ms.custom:
  - classic-and-new
  - build-2024
  - ignite-2024
  - dev-focus
ai-usage: ai-assisted
ms.topic: how-to
ms.date: 02/06/2026
ms.reviewer: dantaylo
ms.author: johalexander
author: ms-johnalex
zone_pivot_groups: foundry-sdk-overview-languages
# customer intent: I want to learn how to use the Microsoft Foundry SDK and endpoints to build AI applications on Azure.
---

# Microsoft Foundry SDKs and Endpoints (temp)

A Foundry resource provides unified access to models, agents, and tools. This article explains which SDK and endpoint to use for your scenario.

| SDK | What it's for | Endpoint |
| --- | --- | --- |
| **Foundry SDK** | Foundry-specific capabilities with OpenAI-compatible interfaces. Includes access to Foundry direct models through the Responses API (not Chat Completions). | `https://<resource-name>.services.ai.azure.com/api/projects/<project-name>` |
| **OpenAI SDK** | Latest OpenAI SDK models and features with the full OpenAI API surface. Foundry direct models available through Chat Completions API (not Responses). | `https://<resource-name>.openai.azure.com/openai/v1` |
| **Foundry Tools SDKs** | Prebuilt solutions (Vision, Speech, Content Safety, and more). | Tool-specific endpoints (varies by service). |
| **Agent Framework** | Multi-agent orchestration in code. Cloud-agnostic. | Uses the project endpoint via the Foundry SDK. |

**Choose your SDK**:
- Use **Foundry SDK** when building apps with agents, evaluations, or Foundry-specific features
- Use **OpenAI SDK** when maximum OpenAI compatibility is required, or using Foundry direct models via Chat Completions
- Use **Foundry Tools SDKs** when working with specific AI services (Vision, Speech, Language, etc.)
- Use **Agent Framework** when building multi-agent systems in code (local orchestration)

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

### Verify prerequisites

Before proceeding, confirm:

- [ ] Azure subscription is active: `az account show`
- [ ] You have the required RBAC role: Check Azure portal → Foundry resource → Access control (IAM)
- [ ] Language runtime installed:
  - Python: `python --version` (≥3.8)
  - Node.js: `node --version` (≥18)
  - .NET: `dotnet --version` (≥6.0)
  - Java: `java --version` (≥11)

## Foundry SDK

The Foundry SDK connects to a single project endpoint that provides access to the most popular Foundry capabilities:

```
https://<resource-name>.services.ai.azure.com/api/projects/<project-name>
```

> [!NOTE]
> If your organization uses a custom subdomain, replace `<resource-name>` with `<your-custom-subdomain>` in the endpoint URL.

This approach simplifies application configuration. Instead of managing multiple endpoints, you configure one.

### Install the SDK

> [!NOTE]
> **SDK versions:** The 2.x preview SDK targets the new Foundry portal and API. The 1.x GA SDK targets Foundry classic. Make sure the samples you follow match your installed package.

::: zone pivot="programming-language-python"

| SDK Version   | Portal Version  | Status  | Python Package                |
|---------------|-----------------|---------|-------------------------------|
| 2.x (preview) | Foundry (new)   | Preview | `azure-ai-projects>=2.0.0b1 --pre`  |
| 1.x (GA)      | Foundry classic | Stable  | `azure-ai-projects==1.0.0`    |

The [Azure AI Projects client library for Python](/python/api/overview/azure/ai-projects-readme?view=azure-python-preview) is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.

Run these commands to install the preview packages for Foundry projects.
```bash
pip install --pre azure-ai-projects
pip install azure-identity openai
```
::: zone-end

::: zone pivot="programming-language-java"

| SDK Version   | Portal Version  | Status  | Java Package                    |
|---------------|-----------------|---------|---------------------------------|
| 1.0.0-beta.3<br>1.0.0-beta.1 | Foundry (new)   | Preview | `azure-ai-projects`<br>`azure-ai-agents` |

::: zone-end

::: zone pivot="programming-language-javascript"

| SDK Version   | Portal Version  | Status  | JavaScript Package                    |
|---------------|-----------------|---------|---------------------------------|
| 2.0.0-beta.4 (preview) | Foundry (new)   | Preview | `@azure/ai-projects 'prerelease'` |
| 1.0.1 | Foundry classic | Stable | `@azure/ai-projects`             |

::: zone-end

::: zone pivot="programming-language-csharp"

| SDK Version   | Portal Version  | Status  | .NET Package                    |
|---------------|-----------------|---------|---------------------------------|
| 1.2.0-beta.5 (preview) | Foundry (new)   | Preview | `Azure.AI.Projects`<br>`Azure.AI.Projects.Openai` |
| 1.x (GA)      | Foundry classic | Stable  | `Azure.AI.Projects`             |

::: zone-end

::: zone pivot="programming-language-java"

The [Azure AI Projects client library for Java (preview)](/java/api/overview/azure/ai-projects-readme) is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Add these packages to your installation for Foundry projects.

```java
package com.azure.ai.agents;

import com.azure.core.util.Configuration;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;
```
::: zone-end

::: zone pivot="programming-language-javascript"

The [Azure AI Projects client library for JavaScript](/javascript/api/overview/azure/ai-projects-readme) is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.

Run this command to install the preview JavaScript packages for Foundry projects.
```bash
npm install @azure/ai-projects@beta @azure/identity dotenv
```
::: zone-end

::: zone pivot="programming-language-csharp"

The [Azure AI Projects client library for .NET](/dotnet/api/overview/azure/ai.projects-readme) is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.

Run this command to add the Azure.AI.Projects package to your .NET project.

```bash
dotnet add package Azure.AI.Projects --prerelease
dotnet add package Azure.AI.Projects.OpenAI --prerelease
dotnet add package Azure.Identity
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

project_client = AIProjectClient(
  endpoint="https://<resource-name>.services.ai.azure.com/api/projects/<project-name>",
  credential=DefaultAzureCredential())
```**Create an OpenAI-compatible client from your project:**

```python
with project_client.get_openai_client() as openai_client:
    response = openai_client.responses.create(
        model="gpt-5.2",
        input="What is the size of France in square miles?",
    )
    print(f"Response output: {response.output_text}")
```

**Expected output**:
```
Response output: France has an area of approximately 213,011 square miles (551,695 square kilometers).
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
```**Create and use an OpenAI-compatible client from your project:**
```java
OpenAIClient openAIClient = projectClient.getOpenAIClient();
```
::: zone-end

::: zone pivot="programming-language-javascript"

**Create a project client:**

```javascript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import "dotenv/config";

const projectEndpoint = "https://<resource-name>.services.ai.azure.com/api/projects/<project-name>";
const deploymentName = "gpt-5.2";
const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());
```
**Create an OpenAI-compatible client from your project:**
```javascript
const openAIClient = await project.getOpenAIClient();
const response = await openAIClient.responses.create({
    model: deploymentName,
    input: "What is the size of France in square miles?",
});
console.log(`Response output: ${response.output_text}`);
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
- [Enable app tracing](/azure/foundry-classic/how-to/develop/trace-application)
- [Fine-tune a model](/azure/ai-foundry/openai/how-to/fine-tuning?tabs=azure-openai&pivots=programming-language-python)
- Get endpoints and keys for Foundry Tools, local orchestration, and more

## Troubleshooting

### Authentication errors

If you see `DefaultAzureCredential failed to retrieve a token`:

1. **Verify Azure CLI is authenticated**:
   ```bash
   az account show
   az login  # if not logged in
   ```

2. **Check RBAC role assignment**:
   - Confirm you have at least the Azure AI User role on the Foundry project
   - See [Assign Azure roles](/azure/role-based-access-control/role-assignments-portal)

3. **For managed identity in production**:
   - Ensure the managed identity has the appropriate role assigned
   - See [Configure managed identities](../../concepts/authentication-authorization-foundry.md#identity-types)

### Endpoint configuration errors

If you see `Connection refused` or `404 Not Found`:

- **Verify resource and project names** match your actual deployment
- **Check endpoint URL format**: Should be `https://<resource-name>.services.ai.azure.com/api/projects/<project-name>`
- **For custom subdomains**: Replace `<resource-name>` with your custom subdomain

### SDK version mismatches

If code samples fail with `AttributeError` or `ModuleNotFoundError`:

- **Check SDK version**:
  ```bash
  pip show azure-ai-projects  # Python
  npm list @azure/ai-projects  # JavaScript
  dotnet list package  # .NET
  ```
- **Verify moniker alignment**: 2.x SDK requires Foundry portal, 1.x SDK requires Foundry classic
- **Reinstall with correct version flags**: See installation commands in each language section above

## OpenAI SDK

Use the OpenAI SDK when you want the full OpenAI API surface and maximum client compatibility. This endpoint provides access to Azure OpenAI models and Foundry direct models (via Responses API). It doesn't provide access to Foundry-specific features like agents and evaluations.

The following snippet shows how to use the Azure OpenAI `/openai/v1` endpoint directly.

::: zone pivot="programming-language-python"

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

**Expected output**:
```json
{
  "id": "resp_abc123",
  "object": "response",
  "created": 1234567890,
  "model": "gpt-5.2",
  "output_text": "France has an area of approximately 213,011 square miles (551,695 square kilometers)."
}
```

For more information, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-python)

::: zone-end

::: zone pivot="programming-language-java"

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]
The following snippet shows how to use the Azure OpenAI `/openai/v1` endpoint directly.

```java
import com.azure.identity.AuthenticationUtil;
import com.azure.identity.DefaultAzureCredential;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.credential.BearerTokenCredential;

import java.util.function.Supplier;

DefaultAzureCredential tokenCredential = new DefaultAzureCredentialBuilder().build();
String endpoint = "https://<resource-name>.openai.azure.com/openai/v1";
String deploymentName = "gpt-5.2";
Supplier<String> bearerTokenSupplier = AuthenticationUtil.getBearerTokenSupplier(
        tokenCredential, "https://cognitiveservices.azure.com/.default");
OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
        .baseUrl(endpoint)
        .credential(BearerTokenCredential.create(bearerTokenSupplier))
        .build();

ResponseCreateParams responseCreateParams = ResponseCreateParams.builder()
        .input("What is the speed of light?")
        .model(deploymentName) 
        .build();

Response response = openAIClient.responses().create(responseCreateParams);

System.out.println("Response output: " + response.getOutputText());
```
For more information on using the OpenAI SDK, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-java)
::: zone-end

::: zone pivot="programming-language-javascript"

```javascript
const endpoint = "https://<resource-name>.openai.azure.com/openai/v1";
const scope = "https://cognitiveservices.azure.com/.default";
const azureADTokenProvider = getBearerTokenProvider(new DefaultAzureCredential(), scope);
const client = new OpenAI({ baseURL: endpoint, apiKey: azureADTokenProvider });
const response = await client.responses.create({
        model: deploymentName,
        input: "What is the size of France in square miles?",
    });
console.log(`Response output: ${response.output_text}`);
```

For more information on using the OpenAI SDK, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-javascript)
::: zone-end

::: zone pivot="programming-language-csharp"

1. Install the OpenAI package:
   Run this command to add the OpenAI client library to your .NET project.
   ```bash
   dotnet add package OpenAI
   ```When it succeeds, the .NET CLI confirms that it installed the `OpenAI` package.

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
        authenticationPolicy: tokenPolicy, // To use Entra 
     // credential: new ApiKeyCredential("<YOUR-AZURE-OPENAI-API-KEY>") // To use APIKEY 
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
For more information on using the OpenAI SDK, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-programming-language-dotnet)
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
