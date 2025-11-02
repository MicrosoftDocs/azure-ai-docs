---
title: Include file
description: Include file
author: msakande
ms.reviewer: mopeakande
ms.author: mopeakande
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 10/28/2025
ms.custom: include
---

## Setup

Install the OpenAI SDK:

```dotnetcli
dotnet add package OpenAI
```

For Microsoft Entra ID authentication, also install:

```dotnetcli
dotnet add package Azure.Identity
```

## Client configuration

With API key authentication:

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```csharp
using Azure;
using Azure.AI.Inference;

ChatCompletionsClient client = new ChatCompletionsClient(
    new Uri("https://<resource>.services.ai.azure.com/models"),
    new AzureKeyCredential(Environment.GetEnvironmentVariable("AZURE_INFERENCE_CREDENTIAL"))
);
```

# [OpenAI v1 SDK](#tab/openai)

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

---

With Microsoft Entra ID authentication:

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```csharp
using Azure;
using Azure.Identity;
using Azure.AI.Inference;

ChatCompletionsClient client = new ChatCompletionsClient(
    new Uri("https://<resource>.services.ai.azure.com/models"),
    new DefaultAzureCredential()
);
```

# [OpenAI v1 SDK](#tab/openai)

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

---

## Responses API

Currently, responses API supports Azure OpenAI in Foundry Models but doesn't support other [Foundry Models sold directly by Azure](../../foundry-models/concepts/models-sold-directly-by-azure.md). 

To perform chat completions with Azure OpenAI models, use the Responses API as shown:

# [Azure AI Inference SDK](#tab/azure-ai-inference)

Azure AI Inference SDK doesn't support the Responses API. Use chat completions instead.

# [OpenAI v1 SDK](#tab/openai)

```csharp
using OpenAI;
using OpenAI.Responses;

#pragma warning disable OPENAI001

string deploymentName = "gpt-4o-mini"; // Your deployment name
OpenAIResponseClient client = new(
    model: deploymentName,
    credential: new ApiKeyCredential(Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")),
    options: new OpenAIClientOptions()
    {
        Endpoint = new Uri("https://<resource>.openai.azure.com/openai/v1/")
    }
);

OpenAIResponse response = client.CreateResponse(
    userInputText: "This is a test."
);

Console.WriteLine($"[ASSISTANT]: {response.GetOutputText()}");
```

---

## Chat completions

# [Azure AI Inference SDK](#tab/azure-ai-inference)

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

# [OpenAI v1 SDK](#tab/openai)

```csharp
using OpenAI.Chat;

ChatCompletion completion = client.CompleteChat(
    new SystemChatMessage("You are a helpful assistant."),
    new UserChatMessage("What is Azure AI?")
);

Console.WriteLine(completion.Content[0].Text);
```

---

### Streaming

# [Azure AI Inference SDK](#tab/azure-ai-inference)

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

# [OpenAI v1 SDK](#tab/openai)

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

---

## Embeddings

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```csharp
using Azure;
using Azure.AI.Inference;

EmbeddingsClient client = new EmbeddingsClient(
    new Uri("https://<resource>.services.ai.azure.com/models"),
    new AzureKeyCredential(Environment.GetEnvironmentVariable("AZURE_INFERENCE_CREDENTIAL"))
);

EmbeddingsOptions embeddingsOptions = new EmbeddingsOptions()
{
    Input = { "Your text string goes here" },
    Model = "text-embedding-3-small"
};

Response<EmbeddingsResult> response = client.Embed(embeddingsOptions);
ReadOnlyMemory<float> embedding = response.Value.Data[0].Embedding;
```

# [OpenAI v1 SDK](#tab/openai)

OpenAI v1 SDK doesn't support embeddings models.

---

## Image generation

# [Azure AI Inference SDK](#tab/azure-ai-inference)

Azure AI Inference SDK doesn't support image generation models.

# [OpenAI v1 SDK](#tab/openai)

OpenAI v1 SDK doesn't support image generation models.

---
