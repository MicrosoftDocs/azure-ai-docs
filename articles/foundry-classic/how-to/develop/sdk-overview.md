---
title: "Get started with Microsoft Foundry SDKs and Endpoints (classic)"
description: "This article provides an overview of the Microsoft Foundry SDKs and endpoints and how to get started using them. (classic)"
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
ROBOTS: NOINDEX, NOFOLLOW
---

# Microsoft Foundry SDKs and Endpoints (classic)

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../../foundry/how-to/develop/sdk-overview.md)

[!INCLUDE [sdk-overview 1](../../../foundry/includes/how-to-develop-sdk-overview-1.md)]

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
> This article applies to a **[!INCLUDE [fdp](../../../foundry/includes/fdp-project-name.md)]**. The code shown here doesn't work for a **[!INCLUDE [hub](../../includes/hub-project-name.md)]**. For more information, see [Types of projects](../../what-is-foundry.md#types-of-projects).

> [!NOTE]
> **SDK versions:** The 2.x GA SDK targets the new Foundry portal and API. The 1.x GA SDK targets Foundry classic. Make sure the samples you follow match your installed package.

::: zone pivot="programming-language-python"

[!INCLUDE [sdk-overview-python](../../../foundry/includes/sdk/sdk-overview-python.md)]

Run this command to install the stable packages for Foundry classic projects.
```bash
pip install openai azure-identity azure-ai-projects==1.0.0
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

[!INCLUDE [feature-preview](../../../foundry/includes/feature-preview.md)]

Add these packages to your installation for Foundry classic projects.

```java
package com.azure.ai.foundry.samples;
import com.azure.ai.projects;
import com.azure.ai.inference.ChatCompletionsClient;
import com.azure.ai.inference.ChatCompletionsClientBuilder;
import com.azure.ai.inference.models.ChatCompletions;
import com.azure.core.credential.AzureKeyCredential;
import com.azure.core.credential.TokenCredential;
import com.azure.core.exception.HttpResponseException;
import com.azure.core.util.logging.ClientLogger;
import com.azure.identity.DefaultAzureCredentialBuilder;
```
::: zone-end

::: zone pivot="programming-language-javascript"

The [Azure AI Projects client library for JavaScript](/javascript/api/overview/azure/ai-projects-readme) is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.

Run this command to install the current JavaScript packages for Foundry classic projects.
```bash
npm install @azure/ai-projects @azure/identity
```
::: zone-end

::: zone pivot="programming-language-csharp"

The [Azure AI Projects client library for .NET](/dotnet/api/overview/azure/ai.projects-readme) is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.

Run these commands to add the Azure AI SDK packages for Foundry classic projects.

```bash
# Add Azure AI SDK packages
dotnet add package Azure.Identity
dotnet add package Azure.AI.Projects 
dotnet add package Azure.AI.Agents.Persistent
dotnet add package Azure.AI.Inference
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
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

project = AIProjectClient(
    endpoint="https://<resource-name>.services.ai.azure.com/api/projects/<project-name>",
    credential=DefaultAzureCredential(),
)
```**Create an OpenAI-compatible client from your project:**

```python
models = project_client.get_openai_client(api_version="2024-10-21")
chat_responses = models.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "What is the size of France in square miles?"},
    ],
)

print(chat_responses.choices[0].message.content)
```
::: zone-end

::: zone pivot="programming-language-java"

**Create a project client:**
```java
package com.azure.ai.foundry.samples;

import com.azure.ai.inference.ChatCompletionsClient;
import com.azure.ai.inference.ChatCompletionsClientBuilder;
import com.azure.ai.inference.models.ChatCompletions;
import com.azure.core.credential.AzureKeyCredential;
import com.azure.core.credential.TokenCredential;
import com.azure.core.exception.HttpResponseException;
import com.azure.core.util.logging.ClientLogger;
import com.azure.identity.DefaultAzureCredentialBuilder;

String  prompt = "What best practices should I follow when asking an AI model to review Java code?";
String endpoint = "https://<resource-name>.services.ai.azure.com/api/projects/<project-name>";
TokenCredential credential = new DefaultAzureCredentialBuilder().build();
ChatCompletionsClient client = new ChatCompletionsClientBuilder()
    .credential(credential)
    .endpoint(endpoint)
    .buildClient();
```**Create and use an OpenAI-compatible client from your project:**
```java
ChatCompletions completions = client.complete(prompt);
String content = completions.getChoice().getMessage().getContent();
System.out.println("\nResponse from AI assistant:\n" + content);
```
::: zone-end

::: zone pivot="programming-language-javascript"

**Create a project client:**

```javascript
const endpoint = "https://<resource-name>.services.ai.azure.com/api/projects/<project-name>";
const deployment = "gpt-4o";

const project = new AIProjectClient(endpoint, new DefaultAzureCredential());
```
**Create an OpenAI-compatible client from your project:**
```javascript
const client = await project.getAzureOpenAIClient({
    // The API version should match the version of the Azure OpenAI resource
    apiVersion: "2024-12-01-preview"
});
const chatCompletion = await client.chat.completions.create({
    model: deployment,
    messages: [
        { role: "system", content: "You are a helpful assistant" },
        { role: "user", content: "What is the speed of light?" },
    ],
});

console.log(chatCompletion.choices[0].message.content);
```
::: zone-end

::: zone pivot="programming-language-csharp"

**Create a project client:**

```csharp
string endpoint = "https://<resource-name>.services.ai.azure.com/api/projects/<project-name>";
AIProjectClient projectClient = new AIProjectClient(new Uri(endpoint), new DefaultAzureCredential());
```
**Create an OpenAI-compatible client from your project:**

```csharp
ClientConnection connection = projectClient.GetConnection(typeof(AzureOpenAIClient).FullName!);
if (!connection.TryGetLocatorAsUri(out Uri uri) || uri is null)
{
    throw new InvalidOperationException("Invalid URI.");
}
uri = new Uri($"https://{uri.Host}");
const string modelDeploymentName = "gpt-4o";  
AzureOpenAIClient azureOpenAIClient = new AzureOpenAIClient(uri, new DefaultAzureCredential());
ChatClient chatClient = azureOpenAIClient.GetChatClient(deploymentName: modelDeploymentName);

Console.WriteLine("Complete a chat");
ChatCompletion result = chatClient.CompleteChat("List all the rainbow colors");
Console.WriteLine(result.Content[0].Text);
```
::: zone-end

### What you can do with the Foundry SDK

- [Access Foundry Models](../../quickstarts/get-started-code.md), including Azure OpenAI
- [Use the Foundry Agent Service](../../../ai-services/agents/quickstart.md?context=/azure/ai-foundry/context/context)
- [Run cloud evaluations](cloud-evaluation.md)
- [Enable app tracing](./trace-application.md)
- [Fine-tune a model](/azure/ai-foundry/openai/how-to/fine-tuning?tabs=azure-openai&pivots=programming-language-python)
- Get endpoints and keys for Foundry Tools, local orchestration, and more

[!INCLUDE [sdk-overview 2](../../../foundry/includes/how-to-develop-sdk-overview-2.md)]

## OpenAI SDK

Use the OpenAI SDK when you want the full OpenAI API surface and maximum client compatibility. This endpoint provides access to Azure OpenAI models and Foundry direct models (via Chat Completions API). It doesn't provide access to Foundry-specific features like agents and evaluations.

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

For more information, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-python).
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

[!INCLUDE [feature-preview](../../../foundry/includes/feature-preview.md)]
The following snippet shows how to use the Azure OpenAI `/openai/v1` endpoint directly.

```java
import com.azure.ai.openai.OpenAIClient;
import com.azure.ai.openai.OpenAIClientBuilder;
import com.azure.ai.openai.models.ChatChoice;
import com.azure.ai.openai.models.ChatCompletions;
import com.azure.ai.openai.models.ChatCompletionsOptions;
import com.azure.ai.openai.models.ChatRequestAssistantMessage;
import com.azure.ai.openai.models.ChatRequestMessage;
import com.azure.ai.openai.models.ChatRequestSystemMessage;
import com.azure.ai.openai.models.ChatRequestUserMessage;
import com.azure.ai.openai.models.ChatResponseMessage;
import com.azure.core.credential.AzureKeyCredential;
import com.azure.core.util.Configuration;

import java.util.ArrayList;
import java.util.List;

String endpoint = "https://<resource-name>.openai.azure.com/openai/v1";
String deploymentName = "gpt-5.2";
TokenCredential defaultCredential = new DefaultAzureCredentialBuilder().build();
OpenAIClient client = new OpenAIClientBuilder()
    .credential(defaultCredential)
    .endpoint("{endpoint}")
    .buildClient();

List<ChatRequestMessage> chatMessages = new ArrayList<>();
chatMessages.add(new ChatRequestSystemMessage("You are a helpful assistant."));
chatMessages.add(new ChatRequestUserMessage("What is the speed of light?"));

ChatCompletions chatCompletions = client.getChatCompletions(deploymentName, new ChatCompletionsOptions(chatMessages));

System.out.printf("Model ID=%s is created at %s.%n", chatCompletions.getId(), chatCompletions.getCreatedAt());
for (ChatChoice choice : chatCompletions.getChoices()) {
    ChatResponseMessage message = choice.getMessage();
    System.out.printf("Index: %d, Chat Role: %s.%n", choice.getIndex(), message.getRole());
    System.out.println("Message:");
    System.out.println(message.getContent());
```

For more information on using the OpenAI SDK, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-java).
::: zone-end

::: zone pivot="programming-language-javascript"

```javascript
import { AzureOpenAI } from "openai";
import { DefaultAzureCredential } from "@azure/identity";

const deployment = "gpt-4o"
const endpoint = "https://<resource-name>.openai.azure.com/openai/v1";
const scope = "https://ai.azure.com/.default";
const apiVersion = "2024-04-01-preview";

const azureADTokenProvider = getBearerTokenProvider(new DefaultAzureCredential(), scope);

const options = { azureADTokenProvider, deployment, apiVersion }

const client = new AzureOpenAI(options);

const result = await client.chat.completions.create({
    model: deployment,
    messages: [
        { role: "system", content: "You are a helpful assistant" },
        { role: "user", content: "What is the speed of light?" },
    ],
});
console.log(result.choices[0].message.content);
```

For more information on using the OpenAI SDK, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-javascript).
::: zone-end

::: zone pivot="programming-language-csharp"

1. Install the OpenAI package:
   Run this command to add the OpenAI client library to your .NET project.
   ```bash
   dotnet add package OpenAI
   ```When it succeeds, the .NET CLI confirms that it installed the `OpenAI` package.

   This snippet configures `DefaultAzureCredential`, builds `OpenAIClientOptions`, and creates a `ChatClient` for the Azure OpenAI v1 endpoint.
   ```csharp
   using System.ClientModel.Primitives;
   using Azure.Identity;
   using OpenAI;
   using OpenAI.Chat;
    
   #pragma warning disable OPENAI001

   const string directModelEndpoint  = "https://<resource-name>.openai.azure.com/openai/v1/";
   const string modelDeploymentName = "gpt-5.2";    
    
   BearerTokenPolicy tokenPolicy = new(
        new DefaultAzureCredential(),
        "https://ai.azure.com/.default");
   OpenAIClient openAIClient = new(
        authenticationPolicy: tokenPolicy,
        options: new OpenAIClientOptions()
        {
            Endpoint = new($"{directModelEndpoint}"),
        });
   ChatClient chatClient = openAIClient.GetChatClient(modelDeploymentName);
    
   ChatCompletion completion = await chatClient.CompleteChatAsync(
        [
            new SystemChatMessage("You are a helpful assistant."),
                        new UserChatMessage("How many feet are in a mile?")
        ]);
    
   Console.WriteLine(completion.Content[0].Text);
   #pragma warning restore OPENAI001
   ```

For more information on using the OpenAI SDK, see [Azure OpenAI supported programming languages](/azure/ai-foundry/openai/supported-languages?tabs=dotnet-secure%2Csecure%2Cpython-entra&pivots=programming-language-programming-language-dotnet).
::: zone-end

[!INCLUDE [sdk-overview 3](../../../foundry/includes/how-to-develop-sdk-overview-3.md)]
