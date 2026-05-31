---
title: "Get started with Microsoft Foundry SDKs and Endpoints"
description: "This article provides an overview of the Microsoft Foundry SDKs and endpoints and how to get started using them."
ms.service: microsoft-foundry
ms.subservice: foundry-sdk
ms.custom:
  - classic-and-new
  - build-2024
  - ignite-2024
  - dev-focus
  - doc-kit-assisted
ai-usage: ai-assisted
ms.topic: how-to
ms.date: 04/10/2026
ms.reviewer: dantaylo
ms.author: sgilley
author: sdgilley
zone_pivot_groups: foundry-sdk-overview-languages
# customer intent: I want to learn how to use the Microsoft Foundry SDK and endpoints to build AI applications on Azure.
---

# Microsoft Foundry SDKs and Endpoints

[!INCLUDE [sdk-overview 1](../../includes/how-to-develop-sdk-overview-1.md)]

## Foundry SDK

The Foundry SDK is a thin-client SDK that gives you access to all of the Foundry project APIs through a single project endpoint:

```
https://<resource-name>.services.ai.azure.com/api/projects/<project-name>
```

It's the foundation other Foundry-aware SDKs build on. For example, the Agent Framework `foundry` package takes a dependency on the Foundry SDK and uses it to access Foundry functionality — you don't need to wire up the project endpoint or OpenAI-compatible client yourself when you use `FoundryChatClient`.

> [!NOTE]
> If your organization uses a custom subdomain, replace `<resource-name>` with `<your-custom-subdomain>` in the endpoint URL.

This approach simplifies application configuration. Instead of managing multiple endpoints, you configure one.

### Install the SDK

::: zone pivot="programming-language-python"

[!INCLUDE [sdk-overview-python](../../includes/sdk/sdk-overview-python.md)]

Run this command to install the packages for Foundry projects.
```bash
pip install "azure-ai-projects>=2.0.0"
```
::: zone-end

::: zone pivot="programming-language-java"

| SDK Version   | Portal Version  | Status  | Java Package                    |
|---------------|-----------------|---------|---------------------------------|
| 2.0.0 | Foundry (new)   | Stable | `azure-ai-projects`<br>`azure-ai-agents` |

::: zone-end

::: zone pivot="programming-language-javascript"

| SDK Version   | Portal Version  | Status  | JavaScript Package                    |
|---------------|-----------------|---------|---------------------------------|
| 2.0.1 | Foundry (new)   | Stable | `@azure/ai-projects` |
| 1.0.1 | Foundry classic | Stable | `@azure/ai-projects`             |

::: zone-end

::: zone pivot="programming-language-csharp"

| SDK Version   | Portal Version  | Status  | .NET Package                    |
|---------------|-----------------|---------|---------------------------------|
| 2.0.0 (GA) | Foundry (new)   | Stable | `Azure.AI.Projects`<br>`Azure.AI.Projects.Agents`<br>`Azure.AI.Extensions.OpenAI` |
| 1.1.0 (GA)      | Foundry classic | Stable  | `Azure.AI.Projects`             |

> [!IMPORTANT]
> Don't install `Azure.AI.Projects.OpenAI` (preview) alongside `Azure.AI.Extensions.OpenAI` (GA). Both packages define the same types in different namespaces, which causes ambiguous reference errors. Use only `Azure.AI.Extensions.OpenAI` for agent scenarios.

::: zone-end

::: zone pivot="programming-language-java"

The [Azure AI Projects client library for Java](/java/api/overview/azure/ai-projects-readme) is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.

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

Run this command to install the JavaScript packages for Foundry projects.
```bash
npm install @azure/ai-projects @azure/identity dotenv
```
::: zone-end

::: zone pivot="programming-language-csharp"

The [Azure AI Projects client library for .NET](/dotnet/api/overview/azure/ai.projects-readme) is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.

Run these commands to add the required packages to your .NET project.

```bash
dotnet add package Azure.AI.Projects
dotnet add package Azure.AI.Projects.Agents
dotnet add package Azure.AI.Extensions.OpenAI
dotnet add package Azure.Identity
```
::: zone-end

### Using the Foundry SDK

The SDK exposes two client types because Foundry and OpenAI have different API shapes:

- **Project client** – Use for Foundry-native operations where OpenAI has no equivalent. Examples: listing connections, retrieving project properties, enabling tracing.
- **OpenAI-compatible client** – Use for Foundry functionality that builds on OpenAI concepts. The Responses API, agents, evaluations, and fine-tuning all use OpenAI-style request/response patterns. This client targets the Responses API on your Foundry project endpoint, which gives you access to Foundry Models from the catalog (including non-Azure-OpenAI direct models) plus platform tools — standard OpenAI tools like file search, code interpreter, and web search, alongside Foundry-exclusive tools like memory, SharePoint, WorkIQ, Fabric IQ, and MCP servers. The project endpoint serves this traffic on the `/openai` route.

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
using Azure.AI.Projects;
using Azure.AI.Extensions.OpenAI;
using Azure.Identity;

string endpoint = "https://<resource-name>.services.ai.azure.com/api/projects/<project-name>";

AIProjectClient projectClient = new(
    endpoint: new Uri(endpoint), 
    tokenProvider: new DefaultAzureCredential());
```
**Create an OpenAI-compatible client from your project:**

```csharp
var responseClient = projectClient.ProjectOpenAIClient.GetProjectResponsesClientForModel("gpt-5.2");
var response = responseClient.CreateResponse("What is the speed of light?");
Console.WriteLine(response.GetOutputText());
```
::: zone-end

### What you can do with the Foundry SDK

- [Access Foundry Models](../../quickstarts/get-started-code.md), including Azure OpenAI
- [Use the Foundry Agent Service](../../agents/quickstarts/prompt-agent.md)
- [Run batch evaluations](cloud-evaluation.md)
- [Enable app tracing](../../observability/how-to/trace-agent-setup.md)
- [Fine-tune a model](/azure/ai-foundry/openai/how-to/fine-tuning?tabs=azure-openai&pivots=programming-language-python)
- Get endpoints and keys for Foundry Tools, local orchestration, and more

[!INCLUDE [sdk-overview 2](../../includes/how-to-develop-sdk-overview-2.md)]

## OpenAI SDK

Use the OpenAI SDK when you want the full OpenAI API surface, the best latency, and maximum compatibility with existing OpenAI clients. This endpoint exposes the Responses API on Azure OpenAI directly and provides access to Azure OpenAI models and Foundry direct models, including embeddings, chat completions, and image generation. It doesn't provide access to Foundry-specific features like agents, evaluations, or Foundry-exclusive platform tools — for those, use the Responses API on the Foundry project endpoint through the [Foundry SDK](#foundry-sdk).

> [!TIP]
> Use the OpenAI SDK endpoint for [generating embeddings](../../openai/how-to/embeddings.md). The project endpoint used by the Foundry SDK doesn't currently route embedding requests.

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

   This snippet configures `DefaultAzureCredential`, builds `OpenAIClientOptions`, and creates a `ResponsesClient` for the Azure OpenAI v1 endpoint.
   ```csharp
   using Azure.Identity;
   using OpenAI;
   using OpenAI.Responses;
   using System.ClientModel.Primitives;
   
   #pragma warning disable OPENAI001
 
   const string directModelEndpoint  = "https://<resource-name>.openai.azure.com/openai/v1/";
   const string deploymentName = "gpt-5.2";    

   BearerTokenPolicy tokenPolicy = new(
        new DefaultAzureCredential(),
        "https://ai.azure.com/.default");
    
   OpenAIClient openAIClient = new(
        authenticationPolicy: tokenPolicy,
        options: new OpenAIClientOptions()
        {
            Endpoint = new($"{directModelEndpoint}"),
        });
   ResponsesClient client = openAIClient.GetResponsesClient();

   CreateResponseOptions options = new()
    {
        Model = deploymentName,
        InputItems = { ResponseItem.CreateUserMessageItem("What is the size of France in square miles?") },
        Temperature = (float)0.7,
    };
    
   var modelDirectResponse = client.CreateResponse(options);
    
   Console.WriteLine($"[ASSISTANT]: {modelDirectResponse.Value.GetOutputText()}");
   #pragma warning restore OPENAI001
   ```
For more information on using the OpenAI SDK, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-programming-language-dotnet)
::: zone-end

## Anthropic SDK

Use the Anthropic SDK to work with Anthropic Claude models deployed in Foundry. Claude models use a separate `/anthropic` endpoint and the Anthropic Messages API, not the OpenAI-compatible endpoint.

The Anthropic endpoint appends `/anthropic` to your resource URL:

```
https://<resource-name>.services.ai.azure.com/anthropic
```

The Messages API is available at:

```
https://<resource-name>.services.ai.azure.com/anthropic/v1/messages
```

::: zone pivot="programming-language-python"

```python
from anthropic import AnthropicFoundry
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)

client = AnthropicFoundry(
    azure_ad_token_provider=token_provider,
    base_url="https://<resource-name>.services.ai.azure.com/anthropic",
)

message = client.messages.create(
    model="claude-sonnet-4-6",  # Replace with your deployment name
    messages=[
        {"role": "user", "content": "What are 3 things to visit in Seattle?"}
    ],
    max_tokens=1048,
)

print(message.content)
```

::: zone-end

::: zone pivot="programming-language-csharp"

The Anthropic SDK doesn't provide a native C# client. Use the REST API with `HttpClient` to call Claude models.

```csharp
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using Azure.Identity;

string endpoint = "https://<resource-name>.services.ai.azure.com/anthropic/v1/messages";
string deploymentName = "claude-sonnet-4-6"; // Replace with your deployment name

var credential = new DefaultAzureCredential();
var token = await credential.GetTokenAsync(
    new Azure.Core.TokenRequestContext(["https://ai.azure.com/.default"]));

using var httpClient = new HttpClient();
httpClient.DefaultRequestHeaders.Authorization =
    new AuthenticationHeaderValue("Bearer", token.Token);
httpClient.DefaultRequestHeaders.Add("anthropic-version", "2023-06-01");

var requestBody = new
{
    model = deploymentName,
    messages = new[] { new { role = "user", content = "What are 3 things to visit in Seattle?" } },
    max_tokens = 1048
};

var response = await httpClient.PostAsync(
    endpoint,
    new StringContent(JsonSerializer.Serialize(requestBody), Encoding.UTF8, "application/json"));

string result = await response.Content.ReadAsStringAsync();
Console.WriteLine(result);
```

::: zone-end

::: zone pivot="programming-language-javascript"

```javascript
import AnthropicFoundry from '@anthropic-ai/foundry-sdk';
import { getBearerTokenProvider, DefaultAzureCredential } from "@azure/identity";

const tokenProvider = getBearerTokenProvider(
    new DefaultAzureCredential(),
    'https://ai.azure.com/.default');

const client = new AnthropicFoundry({
    azureADTokenProvider: tokenProvider,
    baseURL: "https://<resource-name>.services.ai.azure.com/anthropic",
    apiVersion: "2023-06-01"
});

const message = await client.messages.create({
    model: "claude-sonnet-4-6", // Replace with your deployment name
    messages: [{ role: "user", content: "What are 3 things to visit in Seattle?" }],
    max_tokens: 1048,
});

console.log(message);
```

::: zone-end

::: zone pivot="programming-language-java"

The Anthropic SDK doesn't provide a native Java client. Use the REST API with `HttpClient` to call Claude models.

```java
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.core.credential.TokenRequestContext;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

String endpoint = "https://<resource-name>.services.ai.azure.com/anthropic/v1/messages";
String deploymentName = "claude-sonnet-4-6"; // Replace with your deployment name

var credential = new DefaultAzureCredentialBuilder().build();
var token = credential.getToken(
    new TokenRequestContext().addScopes("https://ai.azure.com/.default")).block();

String requestBody = """
    {
        "model": "%s",
        "messages": [{"role": "user", "content": "What are 3 things to visit in Seattle?"}],
        "max_tokens": 1048
    }
    """.formatted(deploymentName);

HttpClient httpClient = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create(endpoint))
    .header("Authorization", "Bearer " + token.getToken())
    .header("Content-Type", "application/json")
    .header("anthropic-version", "2023-06-01")
    .POST(HttpRequest.BodyPublishers.ofString(requestBody))
    .build();

HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
System.out.println(response.body());
```

::: zone-end

For more information, see [Use Anthropic Claude models in Microsoft Foundry](../../foundry-models/how-to/use-foundry-models-claude.md).

[!INCLUDE [sdk-overview 3](../../includes/how-to-develop-sdk-overview-3.md)]
