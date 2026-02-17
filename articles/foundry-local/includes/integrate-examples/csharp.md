---
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 01/06/2026
ms.author: samkemp
author: samuel100
ai-usage: ai-assisted
---

## Prerequisites

- Install Foundry Local. For setup steps, see [Get started with Foundry Local](../../get-started.md).
- [.NET 9.0 SDK](https://dotnet.microsoft.com/download/dotnet/9.0) or later installed.

## Samples repository

The sample in this article can be found in the [Foundry Local C# SDK Samples GitHub repository](https://aka.ms/foundrylocalSDK).

## Set up project

[!INCLUDE [project-setup](./../csharp-project-setup.md)]

## Use OpenAI SDK with Foundry Local

The following example demonstrates how to use the OpenAI SDK with Foundry Local. The code includes the following steps:

1. Initializes a `FoundryLocalManager` instance with a `Configuration` that includes the web service configuration. The web service is an OpenAI compliant endpoint.
1. Gets a `Model` object from the model catalog using an alias.

   > [!NOTE]
   > Foundry Local will select the best variant for the model automatically based on the available hardware of the host machine.

1. Downloads and loads the model variant.
1. Starts the web service.
1. Uses the OpenAI SDK to call the local Foundry web service.
1. Tidies up by stopping the web service and unloading the model.

Copy-and-paste the following code into a C# file named `Program.cs`:

```csharp
using Microsoft.AI.Foundry.Local;
using Microsoft.Extensions.Logging;
using OpenAI;
using System.ClientModel;

var config = new Configuration
{
    AppName = "app-name",
    LogLevel = Microsoft.AI.Foundry.Local.LogLevel.Information,
    Web = new Configuration.WebService
    {
        Urls = "http://127.0.0.1:55588"
    }
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
var catalog = await mgr.GetCatalogAsync();

// Get a model using an alias
var model = await catalog.GetModelAsync("qwen2.5-0.5b") ?? throw new Exception("Model not found");

// Download the model (the method skips download if already cached)
await model.DownloadAsync(progress =>
{
    Console.Write($"\rDownloading model: {progress:F2}%");
    if (progress >= 100f)
    {
        Console.WriteLine();
    }
});

// Load the model
await model.LoadAsync();

// Start the web service
await mgr.StartWebServiceAsync();

// <<<<<< OPEN AI SDK USAGE >>>>>>
// Use the OpenAI SDK to call the local Foundry web service

ApiKeyCredential key = new ApiKeyCredential("notneeded");
OpenAIClient client = new OpenAIClient(key, new OpenAIClientOptions
{
    Endpoint = new Uri(config.Web.Urls + "/v1"),
});

var chatClient = client.GetChatClient(model.Id);

var completionUpdates = chatClient.CompleteChatStreaming("Why is the sky blue?");

Console.Write($"[ASSISTANT]: ");
foreach (var completionUpdate in completionUpdates)
{
    if (completionUpdate.ContentUpdate.Count > 0)
    {
        Console.Write(completionUpdate.ContentUpdate[0].Text);
    }
}
Console.WriteLine();
// <<<<<< END OPEN AI SDK USAGE >>>>>>

// Tidy up
// Stop the web service and unload model
await mgr.StopWebServiceAsync();
await model.UnloadAsync();
```

Reference: [Foundry Local SDK reference](../../reference/reference-sdk.md)
Reference: [Foundry Local REST API reference](../../reference/reference-rest.md)

Run the code using the following command:

### [Windows](#tab/windows)

For x64 Windows, use the following command:

```bash
dotnet run -r win-x64
```

For arm64 Windows, use the following command:

```bash
dotnet run -r win-arm64
```


### [Cross-Platform](#tab/xplatform)

For macOS, use the following command:

```bash
dotnet run -r osx-arm64
```

For Linux, use the following command:

```bash
dotnet run -r linux-x64
```

For Windows, use the following command:

```bash
dotnet run -r win-x64
```

> [!NOTE]
> If you are targeting Windows, we recommend using the Windows-specific instructions under the Windows tab for optimal performance and experience.

You should see a streaming response printed to your console.

---