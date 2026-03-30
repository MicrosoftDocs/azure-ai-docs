---
title: "Get started with Microsoft Foundry SDKs and Endpoints"
description: "This article provides an overview of the Microsoft Foundry SDKs and endpoints and how to get started using them."
ms.service: azure-ai-foundry
ms.custom:
  - classic-and-new
  - build-2024
  - ignite-2024
  - dev-focus
  - doc-kit-assisted
ai-usage: ai-assisted
ms.topic: how-to
ms.date: 03/06/2026
ms.reviewer: dantaylo
ms.author: johalexander
author: ms-johnalex
zone_pivot_groups: foundry-sdk-overview-languages
# customer intent: I want to learn how to use the Microsoft Foundry SDK and endpoints to build AI applications on Azure.
---

# Microsoft Foundry SDKs and Endpoints

[!INCLUDE [sdk-overview 1](../../includes/how-to-develop-sdk-overview-1.md)]

## Foundry SDK

The Foundry SDK connects to a single project endpoint that provides access to the most popular Foundry capabilities:

```
https://<resource-name>.services.ai.azure.com/api/projects/<project-name>
```

> [!NOTE]
> If your organization uses a custom subdomain, replace `<resource-name>` with `<your-custom-subdomain>` in the endpoint URL.

This approach simplifies application configuration. Instead of managing multiple endpoints, you configure one.

### Install the SDK

[!INCLUDE [sdk-overview-python](../../includes/sdk/sdk-overview-python.md)]

Run this command to install the packages for Foundry projects.
```bash
pip install azure-ai-projects >=2.0.0
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
```

**Create an OpenAI-compatible client from your project:**

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
- [Run batch evaluations](cloud-evaluation.md)
- [Enable app tracing](../../observability/how-to/trace-agent-setup.md)
- [Fine-tune a model](/azure/ai-foundry/openai/how-to/fine-tuning?tabs=azure-openai&pivots=programming-language-python)
- Get endpoints and keys for Foundry Tools, local orchestration, and more

[!INCLUDE [sdk-overview 2](../../includes/how-to-develop-sdk-overview-2.md)]

## OpenAI SDK

Use the OpenAI SDK when you want the full OpenAI API surface and maximum client compatibility. This endpoint provides access to Azure OpenAI models and Foundry direct models (via Responses API). It doesn't provide access to Foundry-specific features like agents and evaluations.

The following snippet shows how to use the Azure OpenAI `/openai/v1` endpoint directly.

::: zone pivot="programming-language-python"

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
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
        tokenCredential, "https://ai.azure.com/.default");
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
const scope = "https://ai.azure.com/.default";
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
        "https://ai.azure.com/.default");
    
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

[!INCLUDE [sdk-overview 3](../../includes/how-to-develop-sdk-overview-3.md)]
