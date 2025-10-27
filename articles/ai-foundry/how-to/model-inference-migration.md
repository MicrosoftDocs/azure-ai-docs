---
title: Migrate from Azure AI Inference SDK to OpenAI v1 SDK (take2)
titleSuffix: Azure AI Foundry
description: Learn how to migrate your applications from Azure AI Inference SDK to OpenAI v1 SDK for Azure AI Foundry Models
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 10/27/2025
ms.author: mopeakande
author: msakande
ms.reviewer: achand
reviewer: achandmsft
ms.custom: migration
ai-usage: ai-assisted
---

# Migrate from Azure AI Inference SDK to OpenAI v1 SDK (take2)

This article provides guidance on migrating your applications from the Azure AI Inference SDK to the OpenAI v1 SDK. The OpenAI v1 SDK offers broader compatibility with OpenAI's latest features and allows you to seamlessly switch between OpenAI and Azure endpoints with minimal code changes.

## Benefits of migrating

Migrating to the OpenAI v1 SDK provides several advantages:

- **Unified API**: Use the same SDK for both OpenAI and Azure OpenAI endpoints
- **Latest features**: Access to the newest OpenAI features without waiting for Azure-specific updates
- **Simplified authentication**: Built-in support for both API key and Microsoft Entra ID authentication
- **No API versioning**: The v1 API eliminates the need to frequently update `api-version` parameters
- **Broader model support**: Works with Azure OpenAI in Foundry Models and other Foundry Models from providers like DeepSeek and Grok

## Prerequisites

Before migrating, ensure you have:

- An Azure AI Foundry resource with model deployments
- Basic familiarity with the Azure AI Inference SDK
- The OpenAI SDK installed for your programming language

## Key differences

The following table shows the main differences between the two SDKs:

| Aspect | Azure AI Inference SDK | OpenAI v1 SDK |
|--------|------------------------|---------------|
| Client class | `ChatCompletionsClient` | `OpenAI` |
| Endpoint format | `https://<resource>.services.ai.azure.com/models` | `https://<resource>.openai.azure.com/openai/v1/` |
| API version | Required in URL or parameter | Not required |
| Model parameter | Optional (for multi-model endpoints) | Required (deployment name) |
| Authentication | Azure credentials only | API key or Azure credentials |

## Migration guide

The following sections show how to migrate common tasks from the Azure AI Inference SDK to the OpenAI v1 SDK.

### Installing the SDK

First, install the appropriate OpenAI SDK for your programming language.

# [Python](#tab/python)

**Azure AI Inference SDK**:

```bash
pip install azure-ai-inference
```

**OpenAI v1 SDK**:

```bash
pip install openai
```

For Microsoft Entra ID authentication, also install:

```bash
pip install azure-identity
```

# [C#](#tab/csharp)

**Azure AI Inference SDK**:

```dotnetcli
dotnet add package Azure.AI.Inference --prerelease
```

**OpenAI v1 SDK**:

The OpenAI SDK for .NET is included in the official OpenAI package. No separate Azure package is needed.

```dotnetcli
dotnet add package OpenAI
```

For Microsoft Entra ID authentication, also install:

```dotnetcli
dotnet add package Azure.Identity
```

# [JavaScript](#tab/javascript)

**Azure AI Inference SDK**:

```bash
npm install @azure-rest/ai-inference
```

**OpenAI v1 SDK**:

```bash
npm install openai
```

For Microsoft Entra ID authentication, also install:

```bash
npm install @azure/identity
```

# [Java](#tab/java)

**Azure AI Inference SDK**:

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-inference</artifactId>
    <version>1.0.0-beta.1</version>
</dependency>
```

**OpenAI v1 SDK**:

The official OpenAI Java SDK can be added to your project. Check the [OpenAI Java GitHub repository](https://github.com/openai/openai-java) for the latest version.

For Microsoft Entra ID authentication, also add:

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-identity</artifactId>
    <version>1.18.0</version>
</dependency>
```

# [Go](#tab/go)

**Azure AI Inference SDK**:

The Azure AI Inference SDK for Go is available as part of the Azure SDK.

**OpenAI v1 SDK**:

```bash
go get github.com/openai/openai-go/v2
```

For Microsoft Entra ID authentication, also install:

```bash
go get -u github.com/Azure/azure-sdk-for-go/sdk/azidentity
```

# [REST](#tab/rest)

No installation needed for REST API calls. You can use tools like `curl`, `Invoke-RestMethod`, or any HTTP client library.

---

### Creating a client

The client creation process changes significantly when migrating to the OpenAI v1 SDK.

# [Python](#tab/python)

**Azure AI Inference SDK** (API key):

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

client = ChatCompletionsClient(
    endpoint="https://<resource>.services.ai.azure.com/models",
    credential=AzureKeyCredential(os.environ["AZURE_INFERENCE_CREDENTIAL"]),
)
```

**OpenAI v1 SDK** (API key):

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://<resource>.openai.azure.com/openai/v1/",
)
```

**Azure AI Inference SDK** (Microsoft Entra ID):

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.identity import DefaultAzureCredential

client = ChatCompletionsClient(
    endpoint="https://<resource>.services.ai.azure.com/models",
    credential=DefaultAzureCredential(),
    credential_scopes=["https://cognitiveservices.azure.com/.default"],
)
```

**OpenAI v1 SDK** (Microsoft Entra ID):

```python
import os
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), 
    "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(
    base_url="https://<resource>.openai.azure.com/openai/v1/",
    api_key=token_provider,
)
```

# [C#](#tab/csharp)

**Azure AI Inference SDK** (API key):

```csharp
using Azure;
using Azure.AI.Inference;

ChatCompletionsClient client = new ChatCompletionsClient(
    new Uri("https://<resource>.services.ai.azure.com/models"),
    new AzureKeyCredential(Environment.GetEnvironmentVariable("AZURE_INFERENCE_CREDENTIAL"))
);
```

**OpenAI v1 SDK** (API key):

```csharp
using OpenAI;
using OpenAI.Chat;
using System.ClientModel;

ChatClient client = new(
    model: "gpt-4o-mini", // Your deployment name
    credential: new ApiKeyCredential(Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")),
    options: new OpenAIClientOptions() { 
        Endpoint = new Uri("https://<resource>.openai.azure.com/openai/v1/")
    }
);
```

**Azure AI Inference SDK** (Microsoft Entra ID):

```csharp
using Azure;
using Azure.Identity;
using Azure.AI.Inference;

ChatCompletionsClient client = new ChatCompletionsClient(
    new Uri("https://<resource>.services.ai.azure.com/models"),
    new DefaultAzureCredential()
);
```

**OpenAI v1 SDK** (Microsoft Entra ID):

```csharp
using Azure.Identity;
using OpenAI;
using OpenAI.Chat;
using System.ClientModel.Primitives;

#pragma warning disable OPENAI001

BearerTokenPolicy tokenPolicy = new(
    new DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"
);

ChatClient client = new(
    model: "gpt-4o-mini", // Your deployment name
    authenticationPolicy: tokenPolicy,
    options: new OpenAIClientOptions() {
        Endpoint = new Uri("https://<resource>.openai.azure.com/openai/v1/")
    }
);
```

# [JavaScript](#tab/javascript)

**Azure AI Inference SDK** (API key):

```javascript
import ModelClient from "@azure-rest/ai-inference";
import { AzureKeyCredential } from "@azure/core-auth";

const client = ModelClient(
    "https://<resource>.services.ai.azure.com/models", 
    new AzureKeyCredential(process.env.AZURE_INFERENCE_CREDENTIAL)
);
```

**OpenAI v1 SDK** (API key):

```javascript
import { OpenAI } from "openai";

const client = new OpenAI({
    baseURL: "https://<resource>.openai.azure.com/openai/v1/",
    apiKey: process.env.AZURE_OPENAI_API_KEY
});
```

**Azure AI Inference SDK** (Microsoft Entra ID):

```javascript
import ModelClient from "@azure-rest/ai-inference";
import { DefaultAzureCredential } from "@azure/identity";

const clientOptions = { 
    credentials: { 
        scopes: ["https://cognitiveservices.azure.com/.default"] 
    } 
};

const client = ModelClient(
    "https://<resource>.services.ai.azure.com/models", 
    new DefaultAzureCredential(),
    clientOptions
);
```

**OpenAI v1 SDK** (Microsoft Entra ID):

```javascript
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";
import { OpenAI } from "openai";

const tokenProvider = getBearerTokenProvider(
    new DefaultAzureCredential(),
    'https://cognitiveservices.azure.com/.default'
);

const client = new OpenAI({
    baseURL: "https://<resource>.openai.azure.com/openai/v1/",
    apiKey: tokenProvider
});
```

# [Java](#tab/java)

**Azure AI Inference SDK** (API key):

```java
import com.azure.ai.inference.ChatCompletionsClient;
import com.azure.ai.inference.ChatCompletionsClientBuilder;
import com.azure.core.credential.AzureKeyCredential;

ChatCompletionsClient client = new ChatCompletionsClientBuilder()
    .credential(new AzureKeyCredential(System.getenv("AZURE_INFERENCE_CREDENTIAL")))
    .endpoint("https://<resource>.services.ai.azure.com/models")
    .buildClient();
```

**OpenAI v1 SDK** (API key):

```java
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;

OpenAIClient client = OpenAIOkHttpClient.builder()
    .baseUrl("https://<resource>.openai.azure.com/openai/v1/")
    .apiKey(System.getenv("AZURE_OPENAI_API_KEY"))
    .build();
```

**Azure AI Inference SDK** (Microsoft Entra ID):

```java
import com.azure.ai.inference.ChatCompletionsClient;
import com.azure.ai.inference.ChatCompletionsClientBuilder;
import com.azure.identity.DefaultAzureCredential;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.core.credential.TokenCredential;

TokenCredential credential = new DefaultAzureCredentialBuilder().build();
ChatCompletionsClient client = new ChatCompletionsClientBuilder()
    .credential(credential)
    .endpoint("https://<resource>.services.ai.azure.com/models")
    .buildClient();
```

**OpenAI v1 SDK** (Microsoft Entra ID):

```java
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.azure.identity.DefaultAzureCredential;
import com.azure.identity.DefaultAzureCredentialBuilder;

DefaultAzureCredential tokenCredential = new DefaultAzureCredentialBuilder().build();

OpenAIClient client = OpenAIOkHttpClient.builder()
    .baseUrl("https://<resource>.openai.azure.com/openai/v1/")
    .credential(BearerTokenCredential.create(
        AuthenticationUtil.getBearerTokenSupplier(
            tokenCredential, 
            "https://cognitiveservices.azure.com/.default"
        )
    ))
    .build();
```

# [Go](#tab/go)

**Azure AI Inference SDK** (API key):

Azure AI Inference SDK for Go uses Azure SDK patterns.

**OpenAI v1 SDK** (API key):

```go
import (
    "github.com/openai/openai-go/v2"
    "github.com/openai/openai-go/v2/option"
)

client := openai.NewClient(
    option.WithBaseURL("https://<resource>.openai.azure.com/openai/v1/"),
    option.WithAPIKey(os.Getenv("AZURE_OPENAI_API_KEY")),
)
```

**Azure AI Inference SDK** (Microsoft Entra ID):

Azure AI Inference SDK for Go supports Microsoft Entra ID through Azure SDK.

**OpenAI v1 SDK** (Microsoft Entra ID):

```go
import (
    "github.com/Azure/azure-sdk-for-go/sdk/azidentity"
    "github.com/openai/openai-go/v2"
    "github.com/openai/openai-go/v2/azure"
    "github.com/openai/openai-go/v2/option"
)

tokenCredential, err := azidentity.NewDefaultAzureCredential(nil)
if err != nil {
    panic(err)
}

client := openai.NewClient(
    option.WithBaseURL("https://<resource>.openai.azure.com/openai/v1/"),
    azure.WithTokenCredential(tokenCredential),
)
```

# [REST](#tab/rest)

**Azure AI Inference SDK** (API key):

```bash
curl -X POST https://<resource>.services.ai.azure.com/models/chat/completions \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_INFERENCE_CREDENTIAL" \
  -d '{...}'
```

**OpenAI v1 SDK** (API key):

```bash
curl -X POST https://<resource>.openai.azure.com/openai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{...}'
```

**Azure AI Inference SDK** (Microsoft Entra ID):

```bash
curl -X POST https://<resource>.services.ai.azure.com/models/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_TOKEN" \
  -d '{...}'
```

**OpenAI v1 SDK** (Microsoft Entra ID):

```bash
curl -X POST https://<resource>.openai.azure.com/openai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_TOKEN" \
  -d '{...}'
```

---

### Sending chat completion requests

The method for sending chat completion requests changes when migrating.

# [Python](#tab/python)

**Azure AI Inference SDK**:

```python
from azure.ai.inference.models import SystemMessage, UserMessage

response = client.complete(
    messages=[
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="What is Azure AI?"),
    ],
    model="gpt-4o-mini"  # Optional for single-model endpoints
)

print(response.choices[0].message.content)
```

**OpenAI v1 SDK**:

```python
completion = client.chat.completions.create(
    model="gpt-4o-mini",  # Required: your deployment name
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is Azure AI?"}
    ]
)

print(completion.choices[0].message.content)
```

# [C#](#tab/csharp)

**Azure AI Inference SDK**:

```csharp
using Azure.AI.Inference;

ChatCompletionsOptions requestOptions = new ChatCompletionsOptions()
{
    Messages = {
        new ChatRequestSystemMessage("You are a helpful assistant."),
        new ChatRequestUserMessage("What is Azure AI?")
    },
    Model = "gpt-4o-mini", // Optional for single-model endpoints
};

Response<ChatCompletions> response = client.Complete(requestOptions);
Console.WriteLine(response.Value.Choices[0].Message.Content);
```

**OpenAI v1 SDK**:

```csharp
using OpenAI.Chat;

ChatCompletion completion = client.CompleteChat(
    new SystemChatMessage("You are a helpful assistant."),
    new UserChatMessage("What is Azure AI?")
);

Console.WriteLine(completion.Content[0].Text);
```

# [JavaScript](#tab/javascript)

**Azure AI Inference SDK**:

```javascript
const response = await client.path("/chat/completions").post({
    body: {
        messages: [
            { role: "system", content: "You are a helpful assistant." },
            { role: "user", content: "What is Azure AI?" }
        ],
        model: "gpt-4o-mini" // Optional for single-model endpoints
    }
});

console.log(response.body.choices[0].message.content);
```

**OpenAI v1 SDK**:

```javascript
const completion = await client.chat.completions.create({
    model: "gpt-4o-mini", // Required: your deployment name
    messages: [
        { role: "system", content: "You are a helpful assistant." },
        { role: "user", content: "What is Azure AI?" }
    ]
});

console.log(completion.choices[0].message.content);
```

# [Java](#tab/java)

**Azure AI Inference SDK**:

```java
import com.azure.ai.inference.models.*;
import java.util.List;

List<ChatRequestMessage> messages = List.of(
    new ChatRequestSystemMessage("You are a helpful assistant."),
    new ChatRequestUserMessage("What is Azure AI?")
);

ChatCompletionsOptions options = new ChatCompletionsOptions(messages);
options.setModel("gpt-4o-mini"); // Optional for single-model endpoints

ChatCompletions response = client.complete(options);
System.out.println(response.getChoices().get(0).getMessage().getContent());
```

**OpenAI v1 SDK**:

```java
import com.openai.models.chat.completions.*;

ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
    .addSystemMessage("You are a helpful assistant.")
    .addUserMessage("What is Azure AI?")
    .model("gpt-4o-mini") // Required: your deployment name
    .build();

ChatCompletion completion = client.chat().completions().create(params);
System.out.println(completion.choices().get(0).message().content());
```

# [Go](#tab/go)

**Azure AI Inference SDK**:

Azure AI Inference SDK for Go uses Azure SDK patterns for chat completions.

**OpenAI v1 SDK**:

```go
import (
    "context"
    "fmt"
    "github.com/openai/openai-go/v2"
)

chatCompletion, err := client.Chat.Completions.New(context.TODO(), openai.ChatCompletionNewParams{
    Messages: []openai.ChatCompletionMessageParamUnion{
        openai.SystemMessage("You are a helpful assistant."),
        openai.UserMessage("What is Azure AI?"),
    },
    Model: "gpt-4o-mini", // Required: your deployment name
})

if err != nil {
    panic(err.Error())
}

fmt.Println(chatCompletion.Choices[0].Message.Content)
```

# [REST](#tab/rest)

**Azure AI Inference SDK**:

```bash
curl -X POST https://<resource>.services.ai.azure.com/models/chat/completions \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_INFERENCE_CREDENTIAL" \
  -d '{
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "What is Azure AI?"}
    ],
    "model": "gpt-4o-mini"
  }'
```

**OpenAI v1 SDK**:

```bash
curl -X POST https://<resource>.openai.azure.com/openai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "What is Azure AI?"}
    ]
  }'
```

---

### Handling streaming responses

Streaming allows you to receive responses as they're generated.

# [Python](#tab/python)

**Azure AI Inference SDK**:

```python
from azure.ai.inference.models import SystemMessage, UserMessage

response = client.complete(
    stream=True,
    messages=[
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="Write a poem about Azure."),
    ],
    model="gpt-4o-mini"
)

for update in response:
    if update.choices:
        print(update.choices[0].delta.content or "", end="")
```

**OpenAI v1 SDK**:

```python
stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a poem about Azure."}
    ],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

# [C#](#tab/csharp)

**Azure AI Inference SDK**:

```csharp
using Azure.AI.Inference;

ChatCompletionsOptions requestOptions = new ChatCompletionsOptions()
{
    Messages = {
        new ChatRequestSystemMessage("You are a helpful assistant."),
        new ChatRequestUserMessage("Write a poem about Azure.")
    },
    Model = "gpt-4o-mini",
};

StreamingResponse<StreamingChatCompletionsUpdate> response = client.CompleteStreaming(requestOptions);

await foreach (StreamingChatCompletionsUpdate update in response)
{
    if (update.ContentUpdate != null)
    {
        Console.Write(update.ContentUpdate);
    }
}
```

**OpenAI v1 SDK**:

```csharp
using OpenAI.Chat;

CollectionResult<StreamingChatCompletionUpdate> updates = client.CompleteChatStreaming(
    new SystemChatMessage("You are a helpful assistant."),
    new UserChatMessage("Write a poem about Azure.")
);

foreach (StreamingChatCompletionUpdate update in updates)
{
    foreach (ChatMessageContentPart part in update.ContentUpdate)
    {
        Console.Write(part.Text);
    }
}
```

# [JavaScript](#tab/javascript)

**Azure AI Inference SDK**:

```javascript
const response = await client.path("/chat/completions").post({
    body: {
        messages: [
            { role: "system", content: "You are a helpful assistant." },
            { role: "user", content: "Write a poem about Azure." }
        ],
        model: "gpt-4o-mini",
        stream: true
    }
}).asNodeStream();

for await (const chunk of response) {
    if (chunk.choices && chunk.choices[0]?.delta?.content) {
        process.stdout.write(chunk.choices[0].delta.content);
    }
}
```

**OpenAI v1 SDK**:

```javascript
const stream = await client.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
        { role: "system", content: "You are a helpful assistant." },
        { role: "user", content: "Write a poem about Azure." }
    ],
    stream: true
});

for await (const chunk of stream) {
    if (chunk.choices[0]?.delta?.content) {
        process.stdout.write(chunk.choices[0].delta.content);
    }
}
```

# [Java](#tab/java)

**Azure AI Inference SDK**:

```java
import com.azure.ai.inference.models.*;

List<ChatRequestMessage> messages = List.of(
    new ChatRequestSystemMessage("You are a helpful assistant."),
    new ChatRequestUserMessage("Write a poem about Azure.")
);

ChatCompletionsOptions options = new ChatCompletionsOptions(messages);
options.setModel("gpt-4o-mini");

IterableStream<ChatCompletions> response = client.completeStream(options);

response.forEach(update -> {
    if (update.getChoices() != null && !update.getChoices().isEmpty()) {
        String content = update.getChoices().get(0).getDelta().getContent();
        if (content != null) {
            System.out.print(content);
        }
    }
});
```

**OpenAI v1 SDK**:

```java
import com.openai.models.chat.completions.*;
import java.util.stream.Stream;

ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
    .addSystemMessage("You are a helpful assistant.")
    .addUserMessage("Write a poem about Azure.")
    .model("gpt-4o-mini")
    .build();

Stream<ChatCompletionChunk> stream = client.chat().completions().createStreaming(params);

stream.forEach(chunk -> {
    if (chunk.choices() != null && !chunk.choices().isEmpty()) {
        String content = chunk.choices().get(0).delta().content();
        if (content != null) {
            System.out.print(content);
        }
    }
});
```

# [Go](#tab/go)

**Azure AI Inference SDK**:

Azure AI Inference SDK for Go supports streaming through Azure SDK patterns.

**OpenAI v1 SDK**:

```go
import (
    "context"
    "fmt"
    "github.com/openai/openai-go/v2"
)

stream := client.Chat.Completions.NewStreaming(context.TODO(), openai.ChatCompletionNewParams{
    Messages: []openai.ChatCompletionMessageParamUnion{
        openai.SystemMessage("You are a helpful assistant."),
        openai.UserMessage("Write a poem about Azure."),
    },
    Model: "gpt-4o-mini",
})

for stream.Next() {
    chunk := stream.Current()
    if len(chunk.Choices) > 0 && chunk.Choices[0].Delta.Content != "" {
        fmt.Print(chunk.Choices[0].Delta.Content)
    }
}

if err := stream.Err(); err != nil {
    panic(err.Error())
}
```

# [REST](#tab/rest)

**Azure AI Inference SDK**:

```bash
curl -X POST https://<resource>.services.ai.azure.com/models/chat/completions \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_INFERENCE_CREDENTIAL" \
  -d '{
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Write a poem about Azure."}
    ],
    "model": "gpt-4o-mini",
    "stream": true
  }'
```

**OpenAI v1 SDK**:

```bash
curl -X POST https://<resource>.openai.azure.com/openai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Write a poem about Azure."}
    ],
    "stream": true
  }'
```

---

### Error handling

Error handling differs slightly between the two SDKs.

# [Python](#tab/python)

**Azure AI Inference SDK**:

```python
from azure.core.exceptions import HttpResponseError

try:
    response = client.complete(
        messages=[{"role": "user", "content": "Hello"}],
        model="gpt-4o-mini"
    )
except HttpResponseError as error:
    print(f"Request failed: {error.status_code}")
    print(f"Error message: {error.message}")
```

**OpenAI v1 SDK**:

```python
from openai import OpenAIError, RateLimitError, APIError

try:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello"}]
    )
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
except APIError as e:
    print(f"API error: {e}")
except OpenAIError as e:
    print(f"OpenAI error: {e}")
```

# [C#](#tab/csharp)

**Azure AI Inference SDK**:

```csharp
using Azure;
using Azure.AI.Inference;

try
{
    Response<ChatCompletions> response = client.Complete(requestOptions);
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"Request failed: {ex.Status}");
    Console.WriteLine($"Error message: {ex.Message}");
}
```

**OpenAI v1 SDK**:

```csharp
using OpenAI;
using System.ClientModel;

try
{
    ChatCompletion completion = client.CompleteChat(messages);
}
catch (ClientResultException ex)
{
    Console.WriteLine($"Request failed with status: {ex.Status}");
    Console.WriteLine($"Error message: {ex.Message}");
}
```

# [JavaScript](#tab/javascript)

**Azure AI Inference SDK**:

```javascript
try {
    const response = await client.path("/chat/completions").post({
        body: {
            messages: [{ role: "user", content: "Hello" }],
            model: "gpt-4o-mini"
        }
    });
} catch (error) {
    console.error(`Request failed: ${error.statusCode}`);
    console.error(`Error message: ${error.message}`);
}
```

**OpenAI v1 SDK**:

```javascript
import { OpenAI } from "openai";

try {
    const completion = await client.chat.completions.create({
        model: "gpt-4o-mini",
        messages: [{ role: "user", content: "Hello" }]
    });
} catch (error) {
    if (error instanceof OpenAI.APIError) {
        console.error(`API error: ${error.status} - ${error.message}`);
    } else {
        console.error(`Unexpected error: ${error}`);
    }
}
```

# [Java](#tab/java)

**Azure AI Inference SDK**:

```java
import com.azure.core.exception.HttpResponseException;

try {
    ChatCompletions response = client.complete(options);
} catch (HttpResponseException ex) {
    System.err.println("Request failed: " + ex.getResponse().getStatusCode());
    System.err.println("Error message: " + ex.getMessage());
}
```

**OpenAI v1 SDK**:

```java
import com.openai.core.http.HttpClient;
import com.openai.errors.*;

try {
    ChatCompletion completion = client.chat().completions().create(params);
} catch (RateLimitException e) {
    System.err.println("Rate limit exceeded: " + e.getMessage());
} catch (ApiException e) {
    System.err.println("API error: " + e.statusCode() + " - " + e.getMessage());
} catch (OpenAIException e) {
    System.err.println("OpenAI error: " + e.getMessage());
}
```

# [Go](#tab/go)

**Azure AI Inference SDK**:

Azure AI Inference SDK for Go uses standard Go error handling with Azure SDK patterns.

**OpenAI v1 SDK**:

```go
import (
    "context"
    "errors"
    "fmt"
    "github.com/openai/openai-go/v2"
)

chatCompletion, err := client.Chat.Completions.New(context.TODO(), params)
if err != nil {
    var apiErr *openai.Error
    if errors.As(err, &apiErr) {
        fmt.Printf("API error: %s (code: %s)\n", apiErr.Message, apiErr.Code)
    } else {
        fmt.Printf("Error: %v\n", err)
    }
    return
}
```

# [REST](#tab/rest)

**Azure AI Inference SDK**:

Check HTTP status codes and parse the error response:

```bash
response=$(curl -s -w "\n%{http_code}" -X POST \
  https://<resource>.services.ai.azure.com/models/chat/completions \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_INFERENCE_CREDENTIAL" \
  -d '{"messages":[{"role":"user","content":"Hello"}],"model":"gpt-4o-mini"}')

http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" -ne 200 ]; then
    echo "Error: HTTP $http_code"
    echo "$body"
fi
```

**OpenAI v1 SDK**:

Error handling is similar, checking HTTP status codes:

```bash
response=$(curl -s -w "\n%{http_code}" -X POST \
  https://<resource>.openai.azure.com/openai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{"model":"gpt-4o-mini","messages":[{"role":"user","content":"Hello"}]}')

http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" -ne 200 ]; then
    echo "Error: HTTP $http_code"
    echo "$body"
fi
```

---

## Common migration patterns

### Model parameter handling

- **Azure AI Inference SDK**: The `model` parameter is optional for single-model endpoints but required for multi-model endpoints
- **OpenAI v1 SDK**: The `model` parameter is always required and should be set to your deployment name

### Endpoint URL format

- **Azure AI Inference SDK**: Uses `https://<resource>.services.ai.azure.com/models`
- **OpenAI v1 SDK**: Uses `https://<resource>.openai.azure.com/openai/v1/`

### Response structure

The response structure is similar but has some differences:

- **Azure AI Inference SDK**: Returns `ChatCompletions` object with `choices[].message.content`
- **OpenAI v1 SDK**: Returns `ChatCompletion` object with `choices[].message.content`

Both SDKs provide similar access patterns to response data, including:
- Message content
- Token usage
- Model information
- Finish reason

## Migration checklist

Use this checklist to ensure a smooth migration:

- [ ] Install the OpenAI v1 SDK for your programming language
- [ ] Update authentication code (API key or Microsoft Entra ID)
- [ ] Change endpoint URLs from `.services.ai.azure.com/models` to `.openai.azure.com/openai/v1/`
- [ ] Update client initialization code
- [ ] Always specify the `model` parameter with your deployment name
- [ ] Update request method calls (`complete` → `chat.completions.create`)
- [ ] Update streaming code if applicable
- [ ] Update error handling to use OpenAI SDK exceptions
- [ ] Test all functionality thoroughly
- [ ] Update documentation and code comments

## Troubleshooting

### Authentication failures

If you experience authentication failures:

- Verify your API key is correct and hasn't expired
- For Microsoft Entra ID, ensure your application has the correct permissions
- Check that the credential scope is set to `https://cognitiveservices.azure.com/.default`

### Endpoint errors

If you receive endpoint errors:

- Verify the endpoint URL format includes `/openai/v1/` at the end
- Ensure your resource name is correct
- Check that the model deployment exists and is active

### Model not found errors

If you receive "model not found" errors:

- Verify you're using your deployment name, not the model name
- Check that the deployment is active in your Azure AI Foundry resource
- Ensure the deployment name matches exactly (case-sensitive)

## Related content

- [How to generate chat completions with Azure AI Foundry Models](../foundry-models/how-to/use-chat-completions.md)
- [Azure OpenAI supported programming languages](../openai/supported-languages.md)
- [Switch between OpenAI and Azure OpenAI endpoints](/azure/developer/ai/how-to/switching-endpoints)
- [Azure OpenAI in Azure AI Foundry Models API lifecycle](../openai/api-version-lifecycle.md)
