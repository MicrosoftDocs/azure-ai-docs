---
title: How to migrate from Azure.AI.OpenAI 1.0 Beta to 2.0
titleSuffix: Azure OpenAI in Microsoft Foundry Models
description: Learn about migrating to the latest release of the Azure OpenAI package for .NET.
author: mrbullwinkle 
ms.author: mbullwin 
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.custom: devx-track-dotnet
ms.topic: how-to
ms.date: 11/6/2025
manager: nitinme
---

# Migrate from 1.0 beta to 2.0 (`Azure.AI.OpenAI`)

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

> [!NOTE]
> This guidance is no longer recommended. To take advantage of the latest v1 API refer to the [.NET programming language guide](../supported-languages.md).

## Setup

Stable releases of `Azure.AI.OpenAI` are associated with a corresponding stable Azure OpenAI in Microsoft Foundry Models API version label, for example, `2024-10-21`.

```dotnetcli
dotnet add package Azure.AI.OpenAI
```

Beta releases of `Azure.AI.OpenAI` are associated with a corresponding preview Azure OpenAI API version label, for example, `2024-03-01-preview`.

```dotnetcli
dotnet add package Azure.AI.OpenAI --prerelease
```

## Client configuration

Although client instantiation is similar to 1.0, 2.0 introduces a distinct, Azure-specific top-level client that individual scenario clients are retrieved from.

# [Azure.AI.OpenAI 1.0 Beta](#tab/beta)

```csharp
// 1.0 - BEFORE: Getting a general-purpose client ready for use in 1.0
OpenAIClient client = new(
    new Uri("https://your-resource.openai.azure.com/"),
    new AzureKeyCredential(Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY"));
```

# [Azure.AI.OpenAI 2.0](#tab/stable)

```csharp
// 2.0 - NEW: Get a chat completions client from a top-level Azure client
AzureOpenAIClient openAIClient = new(
    new Uri("https://your-resource.openai.azure.com/"),
    new AzureKeyCredential(Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY"));
ChatClient chatClient = openAIClient.GetChatClient("my-gpt-4o-mini-deployment");
```

Just like in 1.0, the new `AzureOpenAIClient` supports the use of Microsoft Entra ID credentials when the [Azure.Identity](/dotnet/api/overview/azure/identity-readme?view=azure-dotnet&preserve-view=true) package is installed.

```csharp
// 2.0: Microsoft Entra ID via Azure.Identity's DefaultAzureCredential
string endpoint = "https://myaccount.openai.azure.com/";
AzureOpenAIClient client = new(new Uri(endpoint), new DefaultAzureCredential());
```

---

## Chat completion

# [Azure.AI.OpenAI 1.0 Beta](#tab/beta)

```csharp
// 1.0 - BEFORE
OpenAIClient client = new(azureOpenAIResourceUri, azureOpenAIApiKey);

var chatCompletionsOptions = new ChatCompletionsOptions()
{
    DeploymentName = "gpt-3.5-turbo", // Use DeploymentName for "model" with non-Azure clients
    Messages =
    {
        // The system message represents instructions or other guidance about how the assistant should behave
        new ChatRequestSystemMessage("You are a helpful assistant. You will talk like a pirate."),
        // User messages represent current or historical input from the end user
        new ChatRequestUserMessage("Can you help me?"),
        // Assistant messages represent historical responses from the assistant
        new ChatRequestAssistantMessage("Arrrr! Of course, me hearty! What can I do for ye?"),
        new ChatRequestUserMessage("What's the best way to train a parrot?"),
    }
};
```

# [Azure.AI.OpenAI 2.0](#tab/stable)

```csharp
// 2.0 - NEW
ChatClient chatClient = aoaiClient.GetChatClient("my-gpt-4o-mini-deployment");

ChatCompletion completion = chatClient.CompleteChat(
    [
        // System messages represent instructions or other guidance about how the assistant should behave
        new SystemChatMessage("You are a helpful assistant that talks like a pirate."),
        // User messages represent user input, whether historical or the most recent input
        new UserChatMessage("Hi, can you help me?"),
        // Assistant messages in a request represent conversation history for responses
        new AssistantChatMessage("Arrr! Of course, me hearty! What can I do for ye?"),
        new UserChatMessage("What's the best way to train a parrot?"),
    ]);
```

---

Consuming chat completions response is simplified in 2.0.

# [Azure.AI.OpenAI 1.0 Beta](#tab/beta)

```csharp
// 1.0 - BEFORE:
Response<ChatCompletions> response = await client.GetChatCompletionsAsync(chatCompletionsOptions);
ChatResponseMessage responseMessage = response.Value.Choices[0].Message;
Console.WriteLine($"[{responseMessage.Role.ToString().ToUpperInvariant()}]: {responseMessage.Content}");
```

# [Azure.AI.OpenAI 2.0](#tab/stable)

```csharp
// 2.0 - NEW:
ChatCompletion completion = await chatClient.CompleteChatAsync(messages);
Console.WriteLine($"{completion.Role}: {completion.Content[0].Text}");
```

---

### Streaming

# [Azure.AI.OpenAI 1.0 Beta](#tab/beta)

```csharp
// 1.0 - BEFORE
await foreach (StreamingChatCompletionsUpdate chatUpdate in client.GetChatCompletionsStreaming(chatCompletionsOptions))
{
    if (chatUpdate.Role.HasValue)
    {
        Console.Write($"{chatUpdate.Role.Value.ToString().ToUpperInvariant()}: ");
    }
    if (!string.IsNullOrEmpty(chatUpdate.ContentUpdate))
    {
        Console.Write(chatUpdate.ContentUpdate);
    }
}
```

# [Azure.AI.OpenAI 2.0](#tab/stable)

```csharp
// 2.0 - NEW
AsyncCollectionResult<StreamingChatCompletionUpdate> completionUpdates
  = await chatClient.CompleteChatStreamingAsync(messages);

foreach (StreamingChatCompletionUpdate completionUpdate in completionUpdates)
{
    foreach (ChatMessageContentPart contentPart in completionUpdate.ContentUpdate)
    {
        Console.Write(contentPart.Text);
    }
}
```

---

### Tool definitions

# [Azure.AI.OpenAI 1.0 Beta](#tab/beta)

```csharp
// 1.0 - BEFORE
var getWeatherTool = new ChatCompletionsFunctionToolDefinition()
{
    Name = "get_current_weather",
    Description = "Get the current weather in a given location",
    Parameters = BinaryData.FromObjectAsJson(
    new
    {
        Type = "object",
        Properties = new
        {
            Location = new
            {
                Type = "string",
                Description = "The city and state, e.g. San Francisco, CA",
            },
            Unit = new
            {
                Type = "string",
                Enum = new[] { "celsius", "fahrenheit" },
            }
        },
        Required = new[] { "location" },
    },
    new JsonSerializerOptions() {  PropertyNamingPolicy = JsonNamingPolicy.CamelCase }),
};

var chatCompletionsOptions = new ChatCompletionsOptions()
{
    DeploymentName = "gpt-35-turbo-1106",
    Messages = { new ChatRequestUserMessage("What's the weather like in Boston?") },
    Tools = { getWeatherTool },
};

Response<ChatCompletions> response = await client.GetChatCompletionsAsync(chatCompletionsOptions);
```

# [Azure.AI.OpenAI 2.0](#tab/stable)

```csharp
// 2.0 - NEW
ChatTool getCurrentWeatherTool = ChatTool.CreateFunctionTool(
    functionName: nameof(GetCurrentWeather),
    functionDescription: "Get the current weather in a given location",
    functionParameters: BinaryData.FromString("""
    {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g. Boston, MA"
            },
            "unit": {
                "type": "string",
                "enum": [ "celsius", "fahrenheit" ],
                "description": "The temperature unit to use. Infer this from the specified location."
            }
        },
        "required": [ "location" ]
    }
    """)
);

ChatCompletionOptions options = new()
{
    Tools = { getCurrentWeatherTool },
};

ChatCompletion completion = await chatClient.CompleteChatAsync(
    ["What's the weather like Boston?"],
    options);
```

---

### Handling tool call responses

# [Azure.AI.OpenAI 1.0 Beta](#tab/beta)

```csharp
// 1.0 - BEFORE
var chatCompletionsOptions = new ChatCompletionsOptions()
{
    DeploymentName = "gpt-35-turbo-1106",
    Messages = { new ChatRequestUserMessage("What's the weather like in Boston?") },
    Tools = { getWeatherTool },
};

Response<ChatCompletions> response = await client.GetChatCompletionsAsync(chatCompletionsOptions);
```

# [Azure.AI.OpenAI 2.0](#tab/stable)

```csharp
// 2.0 - NEW
if (completion.FinishReason == ChatFinishReason.ToolCalls)
{
    // Add a new assistant message to the conversation history that includes the tool calls
    conversationMessages.Add(new AssistantChatMessage(completion));

    foreach (ChatToolCall toolCall in completion.ToolCalls)
    {
        conversationMessages.Add(new ToolChatMessage(toolCall.Id, GetToolCallContent(toolCall)));
    }

    // Now make a new request with all the messages thus far, including the original
}
```

---

## Chat with On Your Data

# [Azure.AI.OpenAI 1.0 Beta](#tab/beta)

```csharp
// 1.0 - BEFORE
AzureSearchChatExtensionConfiguration contosoExtensionConfig = new()
{
    SearchEndpoint = new Uri("https://your-contoso-search-resource.search.windows.net"),
    Authentication = new OnYourDataApiKeyAuthenticationOptions("<your Cognitive Search resource API key>"),
};

ChatCompletionsOptions chatCompletionsOptions = new()
{
    DeploymentName = "gpt-35-turbo-0613",
    Messages =
    {
        new ChatRequestSystemMessage(
            "You are a helpful assistant that answers questions about the Contoso product database."),
        new ChatRequestUserMessage("What are the best-selling Contoso products this month?")
    },

    // The addition of AzureChatExtensionsOptions enables the use of Azure OpenAI capabilities that add to
    // the behavior of Chat Completions, here the "using your own data" feature to supplement the context
    // with information from an Azure Cognitive Search resource with documents that have been indexed.
    AzureExtensionsOptions = new AzureChatExtensionsOptions()
    {
        Extensions = { contosoExtensionConfig }
    }
};

Response<ChatCompletions> response = await client.GetChatCompletionsAsync(chatCompletionsOptions);
```

# [Azure.AI.OpenAI 2.0](#tab/stable)

```csharp
// 2.0 - NEW
// Extension methods to use data sources with options are subject to SDK surface changes. Suppress the
// warning to acknowledge and this and use the subject-to-change AddDataSource method.
#pragma warning disable AOAI001

ChatCompletionOptions options = new();
options.AddDataSource(new AzureSearchChatDataSource()
{
    Endpoint = new Uri("https://your-search-resource.search.windows.net"),
    IndexName = "contoso-products-index",
    Authentication = DataSourceAuthentication.FromApiKey(
        Environment.GetEnvironmentVariable("OYD_SEARCH_KEY")),
});

ChatCompletion completion = chatClient.CompleteChat(
    [
        new UserChatMessage("What are the best-selling Contoso products this month?"),
    ],
    options);

ChatMessageContext onYourDataContext = completion.GetMessageContext();

if (onYourDataContext?.Intent is not null)
{
    Console.WriteLine($"Intent: {onYourDataContext.Intent}");
}
foreach (ChatCitation citation in onYourDataContext?.Citations ?? [])
{
    Console.WriteLine($"Citation: {citation.Content}");
}
```

---

## Embeddings

# [Azure.AI.OpenAI 1.0 Beta](#tab/beta)

```csharp
// 1.0 - BEFORE
EmbeddingsOptions embeddingsOptions = new()
{
    DeploymentName = "text-embedding-ada-002",
    Input = { "Your text string goes here" },
};
Response<Embeddings> response = await client.GetEmbeddingsAsync(embeddingsOptions);

// The response includes the generated embedding.
EmbeddingItem item = response.Value.Data[0];
ReadOnlyMemory<float> embedding = item.Embedding;
```

# [Azure.AI.OpenAI 2.0](#tab/stable)


```csharp
// 2.0 - NEW
EmbeddingClient client = aoaiClient.GetEmbeddingClient("text-embedding-3-small");

string description = "Best hotel in town if you like luxury hotels. They have an amazing infinity pool, a spa,"
    + " and a really helpful concierge. The location is perfect -- right downtown, close to all the tourist"
    + " attractions. We highly recommend this hotel.";

OpenAIEmbedding embedding = client.GenerateEmbedding(description);
ReadOnlyMemory<float> vector = embedding.ToFloats();
```

---

## Image generation

# [Azure.AI.OpenAI 1.0 Beta](#tab/beta)

```csharp
// 1.0 - BEFORE
Response<ImageGenerations> response = await client.GetImageGenerationsAsync(
    new ImageGenerationOptions()
    {
        DeploymentName = usingAzure ? "my-azure-openai-dall-e-3-deployment" : "dall-e-3",
        Prompt = "a happy monkey eating a banana, in watercolor",
        Size = ImageSize.Size1024x1024,
        Quality = ImageGenerationQuality.Standard
    });

ImageGenerationData generatedImage = response.Value.Data[0];
if (!string.IsNullOrEmpty(generatedImage.RevisedPrompt))
{
    Console.WriteLine($"Input prompt automatically revised to: {generatedImage.RevisedPrompt}");
}
Console.WriteLine($"Generated image available at: {generatedImage.Url.AbsoluteUri}");
```

# [Azure.AI.OpenAI 2.0](#tab/stable)

```csharp
// 2.0 - NEW
ImageClient imageClient = aoaiClient.GetImageClient("my-dall-e-3-deployment");

string prompt = "The concept for a living room that blends Scandinavian simplicity with Japanese minimalism for"
    + " a serene and cozy atmosphere. It's a space that invites relaxation and mindfulness, with natural light"
    + " and fresh air. Using neutral tones, including colors like white, beige, gray, and black, that create a"
    + " sense of harmony. Featuring sleek wood furniture with clean lines and subtle curves to add warmth and"
    + " elegance. Plants and flowers in ceramic pots adding color and life to a space. They can serve as focal"
    + " points, creating a connection with nature. Soft textiles and cushions in organic fabrics adding comfort"
    + " and softness to a space. They can serve as accents, adding contrast and texture.";

ImageGenerationOptions options = new()
{
    Quality = GeneratedImageQuality.High,
    Size = GeneratedImageSize.W1792xH1024,
    Style = GeneratedImageStyle.Vivid,
    ResponseFormat = GeneratedImageFormat.Bytes
};

GeneratedImage image = imageClient.GenerateImage(prompt, options);
BinaryData bytes = image.ImageBytes;
```

---

## Audio transcription

# [Azure.AI.OpenAI 1.0 Beta](#tab/beta)

```csharp
// 1.0 - BEFORE
using Stream audioStreamFromFile = File.OpenRead("myAudioFile.mp3");

var transcriptionOptions = new AudioTranscriptionOptions()
{
    DeploymentName = "my-whisper-deployment", // whisper-1 as model name for non-Azure OpenAI
    AudioData = BinaryData.FromStream(audioStreamFromFile),
    Filename = "test.mp3",
    ResponseFormat = AudioTranscriptionFormat.Verbose,
};

Response<AudioTranscription> transcriptionResponse
    = await client.GetAudioTranscriptionAsync(transcriptionOptions);
AudioTranscription transcription = transcriptionResponse.Value;

// When using Simple, SRT, or VTT formats, only transcription.Text will be populated
Console.WriteLine($"Transcription ({transcription.Duration.Value.TotalSeconds}s):");
Console.WriteLine(transcription.Text);
```

# [Azure.AI.OpenAI 2.0](#tab/stable)

```csharp
// 2.0 - NEW
AudioClient client = aoaiClient.GetAudioClient("my-whisper-1-deployment");

AudioTranscriptionOptions options = new()
{
    ResponseFormat = AudioTranscriptionFormat.Verbose,
    TimestampGranularities = AudioTimestampGranularities.Word | AudioTimestampGranularities.Segment,
};

AudioTranscription transcription = client.TranscribeAudio("my_audio_file.mp3", options);

Console.WriteLine("Transcription:");
Console.WriteLine($"{transcription.Text}");

Console.WriteLine();
Console.WriteLine($"Words:");
foreach (TranscribedWord word in transcription.Words)
{
    Console.WriteLine($"  {word.Word,15} : {word.StartTime.TotalMilliseconds,5:0} - {word.EndTime.TotalMilliseconds,5:0}");
}

Console.WriteLine();
Console.WriteLine($"Segments:");
foreach (TranscribedSegment segment in transcription.Segments)
{
    Console.WriteLine($"  {segment.Text,90} : {segment.StartTime.TotalMilliseconds,5:0} - {segment.EndTime.TotalMilliseconds,5:0}");
}
```

---