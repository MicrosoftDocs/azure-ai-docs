---
title: Use Native Chat Completions
titleSuffix: Foundry Local
description: This article provides instructions on how to leverage native chat completions API in Foundry Local.
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.custom: build-2025
ms.topic: how-to
ms.author: jburchel
ms.reviewer: samkemp
ms.date: 10/01/2025
author: jonburchel
reviewer: samuel100
ai-usage: ai-assisted
---
    
# Use Foundry Local native chat completions API

[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]

Foundry Local has a native chat completions API that allows you to use the inference capabilities without needing to rely on the optional Web Server or separate SDKs (such as the OpenAI chat completions API). This article shows you how to use the native chat completions API in Foundry Local.

## Prerequisites

- [.NET 8.0 SDK](https://dotnet.microsoft.com/en-us/download/dotnet/8.0) or later installed.

## Create project

Create a new C# project and navigate into it:

```bash
dotnet new console -n hello-foundry-local
cd hello-foundry-local
```

### Install NuGet Packages

Install the following NuGet packages into your project folder:

```bash
dotnet add package Microsoft.AI.Foundry.Local
```

## Use native chat completions API    

The following example demonstrates how to use the native chat completions API in Foundry Local. The code includes the following steps:

1. Initializes a `FoundryLocalManager` instance with a `Configuration`.
1. Gets a `Model` object from the model catalog using an alias. Note: Foundry Local will select the best variant for the model automatically based on the available hardware of the host machine.
1. Downloads and loads the model variant.
1. Uses the native chat completions API to generate a response.
1. Unloads the model.

Copy-and-paste the following code into a C# file named `Program.cs`:

```csharp
using Microsoft.AI.Foundry.Local;
using Microsoft.AI.Foundry.Local.OpenAI;
using Betalgo.Ranul.OpenAI.ObjectModels.RequestModels;
using Microsoft.Extensions.Logging;

var config = new Configuration
{
    AppName = "hello-foundry-local",
    LogLevel = Microsoft.AI.Foundry.Local.LogLevel.Information,
};

using var loggerFactory = LoggerFactory.Create(builder =>
{
    builder.SetMinimumLevel(Microsoft.Extensions.Logging.LogLevel.Information);
});
var logger = loggerFactory.CreateLogger<Program>();

// Initialize the singleton instance.
await FoundryLocalManager.CreateAsync(config, logger);
var mgr = FoundryLocalManager.Instance;

// Get the model catalog
var catalog = mgr.GetCatalog();

// Get a model using an alias
var model = await catalog.GetModelAsync("qwen2.5-0.5b") ?? throw new Exception("Model not found");

await model.DownloadAsync();
await model.LoadAsync();

// Get a chat client
ChatClient chatClient = await model.GetChatClientAsync();

// Create a chat message
List<ChatMessage> messages = new()
{
    new ChatMessage { Role = "user", Content = "Why is the sky blue?" }
};

var streamingResponse = chatClient.CompleteChatStreamingAsync(messages);
await foreach (var chunk in streamingResponse)
{
    Console.Write(chunk.Choices[0].Message.Content);
    Console.Out.Flush();
}
Console.WriteLine();

// Tidy up - unload the model
await model.UnloadAsync();
```

Run the code using the following command:

```bash
dotnet run
```

## Related content

- [Integrate Foundry Local with 3rd party SDKs](how-to-integrate-with-inference-sdks.md)
- [Use Foundry Local with LangChain](how-to-use-langchain-with-foundry-local.md)
- [Compile Hugging Face models to run on Foundry Local](how-to-compile-hugging-face-models.md)
- [Explore the Foundry Local CLI reference](../reference/reference-cli.md)