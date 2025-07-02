---
title: Azure OpenAI C# support
titleSuffix: Azure OpenAI in Azure AI Foundry Models
description: Azure OpenAI C# support
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.date: 03/27/2025
---


The Azure OpenAI client library for .NET is a companion to the [official OpenAI client library for .NET](https://github.com/openai/openai-dotnet). The Azure OpenAI library configures a client for use with Azure OpenAI and provides extra strongly typed extension support for request and response models specific to Azure OpenAI scenarios.

### Stable release: 

[Source code](https://github.com/Azure/azure-sdk-for-net/blob/Azure.AI.OpenAI_2.0.0/sdk/openai/Azure.AI.OpenAI/src) | [Package (NuGet)](https://www.nuget.org/packages/Azure.AI.OpenAI) | [Package reference documentation](/dotnet/api/overview/azure/ai.openai-readme?view=azure-dotnet&preserve-view=true) [API reference documentation](../../reference.md) |  [Samples](https://github.com/Azure/azure-sdk-for-net/blob/Azure.AI.OpenAI_2.0.0/sdk/openai/Azure.AI.OpenAI/tests/Samples)
 
### Preview release: 

The preview release has access to the latest features.

[Source code](https://github.com/Azure/azure-sdk-for-net/tree/Azure.AI.OpenAI_2.1.0-beta.2/sdk/openai/Azure.AI.OpenAI/src) | [Package (NuGet)](https://www.nuget.org/packages/Azure.AI.OpenAI/2.2.0-beta.4) | [API reference documentation](../../reference.md) | [Package reference documentation](/dotnet/api/overview/azure/ai.openai-readme?view=azure-dotnet-preview&preserve-view=true)   [Samples](https://github.com/Azure/azure-sdk-for-net/tree/Azure.AI.OpenAI_2.2.0-beta.4/sdk/openai/Azure.AI.OpenAI/tests/Samples)


## Azure OpenAI API version support

Unlike the Azure OpenAI client libraries for Python and JavaScript, the Azure OpenAI .NET package is limited to targeting a specific subset of the Azure OpenAI API versions. Generally each Azure OpenAI .NET package unlocks access to newer Azure OpenAI API release features. Having access to the latest API versions impacts feature availability.

Version selection is controlled by the [`AzureOpenAIClientOptions.ServiceVersion`](/dotnet/api/azure.ai.openai.azureopenaiclientoptions.serviceversion?view=azure-dotnet&preserve-view=true) enum.

The [stable release](/dotnet/api/azure.ai.openai.azureopenaiclientoptions.serviceversion?view=azure-dotnet&preserve-view=true) currently targets:

`2024-06-01`

The [preview release](/dotnet/api/azure.ai.openai.azureopenaiclientoptions.serviceversion?view=azure-dotnet-preview&preserve-view=true) can currently target:

- `2024-08-01-preview`
- `2024-09-01-preview`
- `2024-10-01-preview`
- `2024-12-01-preview`
- `2025-01-01-preview`
- `2025-03-01-preview`

## Installation

```dotnetcli
dotnet add package Azure.AI.OpenAI --prerelease
```

The `Azure.AI.OpenAI` package builds on the [official OpenAI package](https://www.nuget.org/packages/OpenAI), which is included as a dependency.

## Authentication

To interact with Azure OpenAI or OpenAI, create an instance of [`AzureOpenAIClient`](/dotnet/api/azure.ai.openai.azureopenaiclient?view=azure-dotnet-preview&preserve-view=true) with one of the following approaches:

# [Microsoft Entra ID](#tab/dotnet-secure)

A secure, keyless authentication approach is to use Microsoft Entra ID (formerly Azure Active Directory) via the [Azure Identity library](/dotnet/api/overview/azure/identity-readme?view=azure-dotnet&preserve-view=true ). To use the library:

```dotnetcli
dotnet add package Azure.Identity
```

Use the desired credential type from the library. For example, [`DefaultAzureCredential`](/dotnet/api/azure.identity.defaultazurecredential?view=azure-dotnet&preserve-view=true):

```csharp
AzureOpenAIClient openAIClient = new(
    new Uri("https://your-azure-openai-resource.com"),
    new DefaultAzureCredential());
ChatClient chatClient = openAIClient.GetChatClient("my-gpt-4o-mini-deployment");
```

For more information about Azure OpenAI keyless authentication, see the "[Get started with the Azure OpenAI security building block](/azure/developer/ai/get-started-securing-your-ai-app?tabs=github-codespaces&pivots=dotnet)" QuickStart article. 

# [API Key](#tab/dotnet-key)

```csharp
string keyFromEnvironment = Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY");

AzureOpenAIClient openAIClient = new(
    new Uri("https://your-azure-openai-resource.com"),
    new ApiKeyCredential(keyFromEnvironment));
ChatClient chatClient = openAIClient.GetChatClient("my-gpt-35-turbo-deployment");
```

---

## Audio

[`AzureOpenAIClient.GetAudioClient`](/dotnet/api/azure.ai.openai.azureopenaiclient.getaudioclient?view=azure-dotnet-preview&preserve-view=true )

### Transcription

```csharp
AzureOpenAIClient openAIClient = new(
    new Uri("https://your-azure-openai-resource.com"),
    new DefaultAzureCredential());

AudioClient client = openAIClient.GetAudioClient("whisper");

string audioFilePath = Path.Combine("Assets", "speech.mp3");

AudioTranscriptionOptions options = new()
{
    ResponseFormat = AudioTranscriptionFormat.Verbose,
    TimestampGranularities = AudioTimestampGranularities.Word | AudioTimestampGranularities.Segment,
};

AudioTranscription transcription = client.TranscribeAudio(audioFilePath, options);

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

### Text to Speech (TTS)

```csharp
using Azure.AI.OpenAI;
using Azure.Identity;
using OpenAI.Audio;

AzureOpenAIClient openAIClient = new(
    new Uri("https://your-azure-openai-resource.com"),
    new DefaultAzureCredential());

AudioClient client = openAIClient.GetAudioClient("tts-hd"); //Replace with your Azure OpenAI model deployment

string input = "Testing, testing, 1, 2, 3";

BinaryData speech = client.GenerateSpeech(input, GeneratedSpeechVoice.Alloy);

using FileStream stream = File.OpenWrite($"{Guid.NewGuid()}.mp3");
speech.ToStream().CopyTo(stream);
```

## Chat

[`AzureOpenAIClient.GetChatClient`](/dotnet/api/azure.ai.openai.azureopenaiclient.getchatclient?view=azure-dotnet-preview&preserve-view=true)

```csharp
AzureOpenAIClient openAIClient = new(
    new Uri("https://your-azure-openai-resource.com"),
    new DefaultAzureCredential());
ChatClient chatClient = openAIClient.GetChatClient("my-gpt-4o-deployment");

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

Console.WriteLine($"{completion.Role}: {completion.Content[0].Text}");
```

### Stream chat messages

Streaming chat completions use the `CompleteChatStreaming` and `CompleteChatStreamingAsync` method, which return a `ResultCollection<StreamingChatCompletionUpdate>` or `AsyncCollectionResult<StreamingChatCompletionUpdate>` instead of a `ClientResult<ChatCompletion>`. 

These result collections can be iterated over using foreach or await foreach, with each update arriving as new data is available from the streamed response.

```csharp
AzureOpenAIClient openAIClient = new(
    new Uri("https://your-azure-openai-resource.com"),
    new DefaultAzureCredential());
ChatClient chatClient = openAIClient.GetChatClient("my-gpt-4o-deployment");

CollectionResult<StreamingChatCompletionUpdate> completionUpdates = chatClient.CompleteChatStreaming(
    [
        new SystemChatMessage("You are a helpful assistant that talks like a pirate."),
        new UserChatMessage("Hi, can you help me?"),
        new AssistantChatMessage("Arrr! Of course, me hearty! What can I do for ye?"),
        new UserChatMessage("What's the best way to train a parrot?"),
    ]);

foreach (StreamingChatCompletionUpdate completionUpdate in completionUpdates)
{
    foreach (ChatMessageContentPart contentPart in completionUpdate.ContentUpdate)
    {
        Console.Write(contentPart.Text);
    }
}
```

## Embeddings

[`AzureOpenAIClient.GetEmbeddingClient`](/dotnet/api/azure.ai.openai.azureopenaiclient.getembeddingclient?view=azure-dotnet-preview&preserve-view=true)

```csharp
using Azure.AI.OpenAI;
using Azure.Identity;
using OpenAI.Embeddings;

AzureOpenAIClient openAIClient = new(
    new Uri("https://your-azure-openai-resource.com"),
    new DefaultAzureCredential());

EmbeddingClient client = openAIClient.GetEmbeddingClient("text-embedding-3-large"); //Replace with your model deployment name

string description = "This is a test embedding";

OpenAIEmbedding embedding = client.GenerateEmbedding(description);
ReadOnlyMemory<float> vector = embedding.ToFloats();

Console.WriteLine(string.Join(", ", vector.ToArray()));
```

## Fine-tuning

Currently not supported with the Azure OpenAI .NET packages.

## Batch

Currently not supported with the Azure OpenAI .NET packages.

## Images

[`AzureOpenAIClient.GetImageClient`](/dotnet/api/azure.ai.openai.azureopenaiclient.getimageclient?view=azure-dotnet-preview&preserve-view=true)

```csharp
using Azure.AI.OpenAI;
using Azure.Identity;
using OpenAI.Images;

AzureOpenAIClient openAIClient = new(
    new Uri("https://your-azure-openai-resource.com"),
    new DefaultAzureCredential());

ImageClient client = openAIClient.GetImageClient("dall-e-3"); // replace with your model deployment name.

string prompt = "A rabbit eating pancakes.";

ImageGenerationOptions options = new()
{
     Quality = GeneratedImageQuality.High,
     Size = GeneratedImageSize.W1792xH1024,
     Style = GeneratedImageStyle.Vivid,
     ResponseFormat = GeneratedImageFormat.Bytes
};

GeneratedImage image = client.GenerateImage(prompt, options);
BinaryData bytes = image.ImageBytes;

using FileStream stream = File.OpenWrite($"{Guid.NewGuid()}.png");
bytes.ToStream().CopyTo(stream);

```

- [C# Image generation quickstart guide](/azure/ai-services/openai/dall-e-quickstart?tabs=dalle3%2Ccommand-line%2Ckeyless%2Ctypescript-keyless&pivots=programming-language-csharp)

## Reasoning models

```csharp
using Azure.AI.OpenAI;
using Azure.AI.OpenAI.Chat;
using Azure.Identity;
using OpenAI.Chat;


AzureOpenAIClient openAIClient = new(
    new Uri("https://YOUR-RESOURCE-NAME.openai.azure.com/"),
    new DefaultAzureCredential());
ChatClient chatClient = openAIClient.GetChatClient("o3-mini");

// Create ChatCompletionOptions and set the reasoning effort level
ChatCompletionOptions options = new ChatCompletionOptions
{
    ReasoningEffortLevel = ChatReasoningEffortLevel.Low,
    MaxOutputTokenCount = 100000
};

#pragma warning disable AOAI001 //currently required to use MaxOutputTokenCount

options.SetNewMaxCompletionTokensPropertyEnabled(true);

ChatCompletion completion = chatClient.CompleteChat(
    [

        new UserChatMessage("Testing 1,2,3")
    ],
    options); // Pass the options to the CompleteChat method

Console.WriteLine($"{completion.Role}: {completion.Content[0].Text}");
```


## Completions (legacy)

Not supported with the Azure OpenAI .NET packages.


## Error handling

### Error codes

| Status Code | Error Type |
|----|---|
| 400         | `Bad Request Error`          |
| 401         | `Authentication Error`      |
| 403         | `Permission Denied Error`    |
| 404         | `Not Found Error`            |
| 422         | `Unprocessable Entity Error` |
| 429         | `Rate Limit Error`           |
| 500         | `Internal Server Error`      |
| 503         | `Service Unavailable`       |
| 504         | `Gateway Timeout` |

### Retries

The client classes will automatically retry the following errors up to three more times using exponential backoff:

- 408 Request Timeout
- 429 Too Many Requests
- 500 Internal Server Error
- 502 Bad Gateway
- 503 Service Unavailable
- 504 Gateway Timeout


