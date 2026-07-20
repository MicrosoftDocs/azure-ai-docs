---
title: C-Sharp file for model inference SDK to OpenAI SDK migration
description: Include file
author: msakande
ms.author: mopeakande
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: include
ms.date: 06/04/2026
ms.custom: include
ai-usage: ai-assisted
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
    "https://ai.azure.com/.default"
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
        new ChatRequestUserMessage("How many languages are in the world?")
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

## Responses

The Responses API is OpenAI's stateful interface that returns a structured `output` array containing message, tool call, and reasoning items.

# [OpenAI SDK](#tab/openai)

```csharp
using OpenAI.Responses;

var responseClient = client.GetResponsesClient("DeepSeek-V3.1");
var result = await responseClient.CreateResponseAsync(new CreateResponseOptions(
    [ResponseItem.CreateUserMessageItem("How many languages are in the world?")])
    { MaxOutputTokenCount = 2000 }
);

Console.WriteLine(result.Value.GetOutputText());
```

# [Azure AI Inference SDK](#tab/azure-ai-inference)

The Azure AI Inference SDK doesn't expose the Responses API. To call it, use the OpenAI SDK.

---

### Reasoning

> [!NOTE]
> This information on reasoning content doesn't apply to Azure OpenAI models. Azure OpenAI reasoning models use the [reasoning summaries feature](../../openai/how-to/reasoning.md#reasoning-summary).

Some reasoning models, like DeepSeek-R1, generate completions and include the reasoning behind them. The Responses API surfaces this as a structured `reasoning` output item whose `summary[].text` contains the model's thinking, alongside the final answer.

# [OpenAI SDK](#tab/openai)

```csharp
using System.Text;
using OpenAI.Responses;

var responseClient = client.GetResponsesClient("DeepSeek-R1-0528");
var result = await responseClient.CreateResponseAsync(new CreateResponseOptions(
    [ResponseItem.CreateUserMessageItem("How many languages are in the world?")])
    { MaxOutputTokenCount = 2000 }
);

// Walk OutputItems for ReasoningResponseItem entries and join SummaryParts text.
var sb = new StringBuilder();
foreach (var item in result.Value.OutputItems)
{
    if (item is not ReasoningResponseItem reasoning) continue;
    foreach (var part in reasoning.SummaryParts)
    {
        if (part is ReasoningSummaryTextPart textPart && !string.IsNullOrEmpty(textPart.Text))
        {
            if (sb.Length > 0) sb.Append('\n');
            sb.Append(textPart.Text);
        }
    }
}

Console.WriteLine($"Thinking: {sb.ToString().Trim()}");
Console.WriteLine($"Answer:   {result.Value.GetOutputText()}");
```

**Output is as follows:**

```console
Thinking: Okay, the user is asking how many languages exist in the world. I need to provide a clear and accurate answer...
Answer:   There are approximately 7,000 languages spoken around the world today.
```

[!INCLUDE [reasoning-tokens-known-issue](reasoning-tokens-known-issue.md)]


# [Azure AI Inference SDK](#tab/azure-ai-inference)

The Azure AI Inference SDK doesn't expose the Responses API. To get reasoning content, call the chat completions API instead. The reasoning is included in the message content wrapped in `<think>` and `</think>` tags, which you can extract with a regex match.

```csharp
using Azure.AI.Inference;
using System.Text.RegularExpressions;

ChatCompletionsOptions requestOptions = new ChatCompletionsOptions()
{
    Messages = {
        new ChatRequestSystemMessage("You are a helpful assistant."),
        new ChatRequestUserMessage("How many languages are in the world?")
    },
    Model = "DeepSeek-R1-0528", // Optional for single-model endpoints
};

Response<ChatCompletions> response = client.Complete(requestOptions);
string content = response.Value.Choices[0].Message.Content;

Regex regex = new Regex(@"<think>(.*?)</think>(.*)", RegexOptions.Singleline);
Match match = regex.Match(content);

if (match.Success)
{
    Console.WriteLine($"Thinking: {match.Groups[1].Value.Trim()}");
    Console.WriteLine($"Answer:   {match.Groups[2].Value.Trim()}");
}
else
{
    Console.WriteLine($"Response: {content}");
}
```

**Output is as follows:**

```console
Thinking: Okay, the user is asking how many languages exist in the world. I need to provide a clear and accurate answer...
Answer:   There are approximately 7,000 languages spoken around the world today.
```

---

When you make multi-turn conversations, avoid sending the reasoning content in the chat history because reasoning tends to generate long explanations.

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