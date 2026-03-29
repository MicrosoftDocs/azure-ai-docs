---
author: jonburchel
ms.author: jburchel
ms.reviewer: samkemp
ms.topic: include
ms.date: 03/29/2026
---

[!INCLUDE [C# project setup](../csharp-project-setup.md)]

## Browse the catalog and select a model

The Foundry Local SDK provides a model catalog that lists all available models. In this step, you initialize the SDK and select a model for your chat assistant.

1. Open `Program.cs` and replace its contents with the following code to initialize the SDK and select a model:

    ```csharp
    using Microsoft.AI.Foundry.Local;
    using Microsoft.Extensions.Logging;

    CancellationToken ct = CancellationToken.None;

    var config = new Configuration
    {
        AppName = "chat-assistant",
        LogLevel = Microsoft.AI.Foundry.Local.LogLevel.Information
    };

    using var loggerFactory = LoggerFactory.Create(builder =>
    {
        builder.SetMinimumLevel(Microsoft.Extensions.Logging.LogLevel.Information);
    });
    var logger = loggerFactory.CreateLogger<Program>();

    // Initialize the singleton instance
    await FoundryLocalManager.CreateAsync(config, logger);
    var mgr = FoundryLocalManager.Instance;

    // Select a model from the catalog
    var catalog = await mgr.GetCatalogAsync();
    var model = await catalog.GetModelAsync("phi-3.5-mini")
        ?? throw new Exception("Model not found");

    // Download the model (skips if already cached)
    await model.DownloadAsync(progress =>
    {
        Console.Write($"\rDownloading model: {progress:F2}%");
        if (progress >= 100f) Console.WriteLine();
    });

    // Load the model into memory
    await model.LoadAsync();
    Console.WriteLine("Model loaded and ready.");
    ```

    The `GetModelAsync` method accepts a model alias, which is a short friendly name that maps to a specific model in the catalog. The `DownloadAsync` method fetches the model weights to your local cache, and `LoadAsync` makes the model ready for inference.

## Define a system prompt

A system prompt sets the assistant's personality and behavior. It's the first message in the conversation history and the model references it throughout the conversation.

Add a system prompt to shape how the assistant responds:

```csharp
using Betalgo.Ranul.OpenAI.ObjectModels.RequestModels;

// Start the conversation with a system prompt
var messages = new List<ChatMessage>
{
    new ChatMessage
    {
        Role = "system",
        Content = "You are a helpful, friendly assistant. Keep your responses " +
                  "concise and conversational. If you don't know something, say so."
    }
};
```

> [!TIP]
> Experiment with different system prompts to change the assistant's behavior. For example, you can instruct it to respond as a pirate, a teacher, or a domain expert.

## Implement multi-turn conversation

A chat assistant needs to maintain context across multiple exchanges. You achieve this by keeping a list of all messages (system, user, and assistant) and sending the full list with each request. The model uses this history to generate contextually relevant responses.

Add a conversation loop that:

- Reads user input from the console.
- Appends the user message to the history.
- Sends the complete history to the model.
- Appends the assistant's response to the history for the next turn.

```csharp
// Get a chat client
var chatClient = await model.GetChatClientAsync();

Console.WriteLine("\nChat assistant ready! Type 'quit' to exit.\n");

while (true)
{
    Console.Write("You: ");
    var userInput = Console.ReadLine();
    if (string.IsNullOrWhiteSpace(userInput) ||
        userInput.Equals("quit", StringComparison.OrdinalIgnoreCase) ||
        userInput.Equals("exit", StringComparison.OrdinalIgnoreCase))
    {
        break;
    }

    // Add the user's message to conversation history
    messages.Add(new ChatMessage { Role = "user", Content = userInput });

    // Send the full conversation history and get a response
    var response = await chatClient.CompleteChatAsync(messages, ct);
    var assistantMessage = response.Choices[0].Message.Content;

    // Add the assistant's response to conversation history
    messages.Add(new ChatMessage { Role = "assistant", Content = assistantMessage });

    Console.WriteLine($"Assistant: {assistantMessage}\n");
}
```

Each call to `CompleteChatAsync` receives the full message history. This is how the model "remembers" previous turns — it doesn't store state between calls.

## Add streaming responses

Streaming prints each token as it's generated, which makes the assistant feel more responsive. Replace the `CompleteChatAsync` call with `CompleteChatStreamingAsync` to stream the response token by token.

Update the conversation loop to use streaming:

```csharp
while (true)
{
    Console.Write("You: ");
    var userInput = Console.ReadLine();
    if (string.IsNullOrWhiteSpace(userInput) ||
        userInput.Equals("quit", StringComparison.OrdinalIgnoreCase) ||
        userInput.Equals("exit", StringComparison.OrdinalIgnoreCase))
    {
        break;
    }

    // Add the user's message to conversation history
    messages.Add(new ChatMessage { Role = "user", Content = userInput });

    // Stream the response token by token
    Console.Write("Assistant: ");
    var fullResponse = string.Empty;
    var streamingResponse = chatClient.CompleteChatStreamingAsync(messages, ct);
    await foreach (var chunk in streamingResponse)
    {
        var content = chunk.Choices[0].Message.Content;
        if (!string.IsNullOrEmpty(content))
        {
            Console.Write(content);
            Console.Out.Flush();
            fullResponse += content;
        }
    }
    Console.WriteLine("\n");

    // Add the complete response to conversation history
    messages.Add(new ChatMessage { Role = "assistant", Content = fullResponse });
}
```

The streaming version accumulates the full response so it can be added to the conversation history after the stream completes.

## Complete code

Replace the contents of `Program.cs` with the following complete code:

```csharp
using Microsoft.AI.Foundry.Local;
using Betalgo.Ranul.OpenAI.ObjectModels.RequestModels;
using Microsoft.Extensions.Logging;

CancellationToken ct = CancellationToken.None;

var config = new Configuration
{
    AppName = "chat-assistant",
    LogLevel = Microsoft.AI.Foundry.Local.LogLevel.Information
};

using var loggerFactory = LoggerFactory.Create(builder =>
{
    builder.SetMinimumLevel(Microsoft.Extensions.Logging.LogLevel.Information);
});
var logger = loggerFactory.CreateLogger<Program>();

// Initialize the singleton instance
await FoundryLocalManager.CreateAsync(config, logger);
var mgr = FoundryLocalManager.Instance;

// Select and load a model from the catalog
var catalog = await mgr.GetCatalogAsync();
var model = await catalog.GetModelAsync("phi-3.5-mini")
    ?? throw new Exception("Model not found");

await model.DownloadAsync(progress =>
{
    Console.Write($"\rDownloading model: {progress:F2}%");
    if (progress >= 100f) Console.WriteLine();
});

await model.LoadAsync();
Console.WriteLine("Model loaded and ready.");

// Get a chat client
var chatClient = await model.GetChatClientAsync();

// Start the conversation with a system prompt
var messages = new List<ChatMessage>
{
    new ChatMessage
    {
        Role = "system",
        Content = "You are a helpful, friendly assistant. Keep your responses " +
                  "concise and conversational. If you don't know something, say so."
    }
};

Console.WriteLine("\nChat assistant ready! Type 'quit' to exit.\n");

while (true)
{
    Console.Write("You: ");
    var userInput = Console.ReadLine();
    if (string.IsNullOrWhiteSpace(userInput) ||
        userInput.Equals("quit", StringComparison.OrdinalIgnoreCase) ||
        userInput.Equals("exit", StringComparison.OrdinalIgnoreCase))
    {
        break;
    }

    // Add the user's message to conversation history
    messages.Add(new ChatMessage { Role = "user", Content = userInput });

    // Stream the response token by token
    Console.Write("Assistant: ");
    var fullResponse = string.Empty;
    var streamingResponse = chatClient.CompleteChatStreamingAsync(messages, ct);
    await foreach (var chunk in streamingResponse)
    {
        var content = chunk.Choices[0].Message.Content;
        if (!string.IsNullOrEmpty(content))
        {
            Console.Write(content);
            Console.Out.Flush();
            fullResponse += content;
        }
    }
    Console.WriteLine("\n");

    // Add the complete response to conversation history
    messages.Add(new ChatMessage { Role = "assistant", Content = fullResponse });
}

// Clean up - unload the model
await model.UnloadAsync();
Console.WriteLine("Model unloaded. Goodbye!");
```

## Run the application

Run the chat assistant:

```bash
dotnet run
```

You see output similar to:

```
Downloading model: 100.00%
Model loaded and ready.

Chat assistant ready! Type 'quit' to exit.

You: What is photosynthesis?
Assistant: Photosynthesis is the process plants use to convert sunlight, water, and carbon
dioxide into glucose and oxygen. It mainly happens in the leaves, inside structures
called chloroplasts.

You: Why is it important for other living things?
Assistant: It's essential because photosynthesis produces the oxygen that most living things
breathe. It also forms the base of the food chain — animals eat plants or eat other
animals that depend on plants for energy.

You: quit
Model unloaded. Goodbye!
```

Notice how the assistant remembers context from previous turns — when you ask "Why is it important for other living things?", it knows you're still talking about photosynthesis.
