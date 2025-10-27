## Benefits of migrating

Migrating to the OpenAI v1 SDK provides several advantages:

- **Unified API**: Use the same SDK for both OpenAI and Azure OpenAI endpoints
- **Latest features**: Access to the newest OpenAI features without waiting for Azure-specific updates
- **Simplified authentication**: Built-in support for both API key and Microsoft Entra ID authentication
- **No API versioning**: The v1 API eliminates the need to frequently update `api-version` parameters
- **Broader model support**: Works with Azure OpenAI in Foundry Models and other Foundry Models from providers like DeepSeek and Grok

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

With Microsoft Entra ID:

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

For Azure OpenAI models, use the Responses API for chat completions:

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

```csharp
using OpenAI;
using OpenAI.Embeddings;

EmbeddingClient client = new(
    "text-embedding-3-small", // Your deployment name
    credential: new ApiKeyCredential(Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")),
    options: new OpenAIClientOptions()
    {
        Endpoint = new Uri("https://<resource>.openai.azure.com/openai/v1/")
    }
);

string input = "Your text string goes here";

OpenAIEmbedding embedding = client.GenerateEmbedding(input);
ReadOnlyMemory<float> vector = embedding.ToFloats();
```

---

## Image generation

# [Azure AI Inference SDK](#tab/azure-ai-inference)

Azure AI Inference SDK doesn't support image generation. Use OpenAI SDK instead.

# [OpenAI v1 SDK](#tab/openai)

```csharp
using OpenAI;
using OpenAI.Images;

AzureOpenAIClient openAIClient = new(
    new Uri("https://<resource>.openai.azure.com/"),
    new AzureKeyCredential(Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY"))
);

ImageClient imageClient = openAIClient.GetImageClient("dall-e-3"); // Your deployment name

string prompt = "a happy monkey eating a banana, in watercolor";

ImageGenerationOptions options = new()
{
    Quality = GeneratedImageQuality.Standard,
    Size = GeneratedImageSize.W1024xH1024,
    ResponseFormat = GeneratedImageFormat.Uri
};

GeneratedImage image = imageClient.GenerateImage(prompt, options);
Console.WriteLine($"Generated image available at: {image.ImageUri}");
```

---

## Error handling

# [Azure AI Inference SDK](#tab/azure-ai-inference)

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

# [OpenAI v1 SDK](#tab/openai)

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

---
