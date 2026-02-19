---
title: C-Sharp file for model inference SDK to OpenAI SDK migration
description: Include file
author: msakande
ms.author: mopeakande
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
ms.date: 11/05/2025
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

# [OpenAI SDK](#tab/openai)

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

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```csharp
using Azure;
using Azure.AI.Inference;

ChatCompletionsClient client = new ChatCompletionsClient(
    new Uri("https://<resource>.services.ai.azure.com/models"),
    new AzureKeyCredential(Environment.GetEnvironmentVariable("AZURE_INFERENCE_CREDENTIAL"))
);
```

---

With Microsoft Entra ID authentication:

# [OpenAI SDK](#tab/openai)

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

---

## Chat completions

# [OpenAI SDK](#tab/openai)

```csharp
using OpenAI.Chat;

ChatCompletion completion = client.CompleteChat(
    new SystemChatMessage("You are a helpful assistant."),
    new UserChatMessage("What is Azure AI?")
);

Console.WriteLine(completion.Content[0].Text);
```

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```csharp
using Azure.AI.Inference;

ChatCompletionsOptions requestOptions = new ChatCompletionsOptions()
{
    Messages = {
        new ChatRequestSystemMessage("You are a helpful assistant."),
        new ChatRequestUserMessage("What is Azure AI?")
    },
    Model = "DeepSeek-V3.1", // Optional for single-model endpoints
};

Response<ChatCompletions> response = client.Complete(requestOptions);
Console.WriteLine(response.Value.Choices[0].Message.Content);
```

---

### Streaming

# [OpenAI SDK](#tab/openai)

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

---

## Embeddings

# [OpenAI SDK](#tab/openai)

```csharp
using OpenAI;
using OpenAI.Embeddings;
using System.ClientModel;

EmbeddingClient client = new(
    "text-embedding-3-small",
    credential: new ApiKeyCredential("API-KEY"),
    options: new OpenAIClientOptions()
    {

        Endpoint = new Uri("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1")
    }
);

string input = "This is a test";

OpenAIEmbedding embedding = client.GenerateEmbedding(input);
ReadOnlyMemory<float> vector = embedding.ToFloats();
Console.WriteLine($"Embeddings: [{string.Join(", ", vector.ToArray())}]");
```

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

---