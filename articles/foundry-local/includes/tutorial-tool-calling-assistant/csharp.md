---
author: jonburchel
ms.author: jburchel
ms.reviewer: samkemp
ms.topic: include
ms.date: 03/29/2026
---

[!INCLUDE [C# project setup](../csharp-project-setup.md)]

## Define tools

Tool calling lets the model request that your code runs a function and returns the result. You define the available tools as a list of JSON schemas that describe each function's name, purpose, and parameters.

1. Open `Program.cs` and add the following tool definitions:

    ```csharp
    using System.Text.Json;

    // Define tools the model can call
    var tools = new[]
    {
        new
        {
            type = "function",
            function = new
            {
                name = "get_weather",
                description = "Get the current weather for a location",
                parameters = new
                {
                    type = "object",
                    properties = new
                    {
                        location = new
                        {
                            type = "string",
                            description = "The city or location"
                        },
                        unit = new
                        {
                            type = "string",
                            @enum = new[] { "celsius", "fahrenheit" },
                            description = "Temperature unit"
                        }
                    },
                    required = new[] { "location" }
                }
            }
        },
        new
        {
            type = "function",
            function = new
            {
                name = "calculate",
                description = "Perform a math calculation",
                parameters = new
                {
                    type = "object",
                    properties = new
                    {
                        expression = new
                        {
                            type = "string",
                            description = "The math expression to evaluate"
                        }
                    },
                    required = new[] { "expression" }
                }
            }
        }
    };
    ```

    Each tool definition includes a `name`, a `description` that helps the model decide when to use it, and a `parameters` schema that describes the expected input.

1. Add the C# methods that implement each tool:

    ```csharp
    using System.Data;

    string ExecuteTool(string functionName, JsonElement arguments)
    {
        switch (functionName)
        {
            case "get_weather":
                var location = arguments.GetProperty("location").GetString()
                    ?? "unknown";
                var unit = arguments.TryGetProperty("unit", out var u)
                    ? u.GetString() ?? "celsius"
                    : "celsius";
                var temp = unit == "celsius" ? 22 : 72;
                return JsonSerializer.Serialize(new
                {
                    location,
                    temperature = temp,
                    unit,
                    condition = "Sunny"
                });

            case "calculate":
                var expression = arguments.GetProperty("expression")
                    .GetString() ?? "";
                try
                {
                    var result = new DataTable().Compute(expression, null);
                    return JsonSerializer.Serialize(new
                    {
                        expression,
                        result = result?.ToString()
                    });
                }
                catch (Exception ex)
                {
                    return JsonSerializer.Serialize(new
                    {
                        error = ex.Message
                    });
                }

            default:
                return JsonSerializer.Serialize(new
                {
                    error = $"Unknown function: {functionName}"
                });
        }
    }
    ```

    The model doesn't run these functions directly. It returns a tool call request with the function name and arguments, and your code executes the function.

## Send a message that triggers tool use

Initialize the Foundry Local SDK, load a model, and send a message that the model can answer by calling a tool.

```csharp
using Microsoft.AI.Foundry.Local;
using Betalgo.Ranul.OpenAI.ObjectModels.RequestModels;
using Microsoft.Extensions.Logging;

CancellationToken ct = CancellationToken.None;

var config = new Configuration
{
    AppName = "tool-calling-app",
    LogLevel = Microsoft.AI.Foundry.Local.LogLevel.Information
};

using var loggerFactory = LoggerFactory.Create(builder =>
{
    builder.SetMinimumLevel(
        Microsoft.Extensions.Logging.LogLevel.Information
    );
});
var logger = loggerFactory.CreateLogger<Program>();

// Initialize the singleton instance
await FoundryLocalManager.CreateAsync(config, logger);
var mgr = FoundryLocalManager.Instance;

// Select and load a model
var catalog = await mgr.GetCatalogAsync();
var model = await catalog.GetModelAsync("phi-3.5-mini")
    ?? throw new Exception("Model not found");

await model.DownloadAsync(progress =>
{
    Console.Write($"\rDownloading model: {progress:F2}%");
    if (progress >= 100f) Console.WriteLine();
});

await model.LoadAsync();
Console.WriteLine("Model loaded and ready.\n");

// Get a chat client
var chatClient = await model.GetChatClientAsync();

// Start with a system prompt and a user message
var messages = new List<ChatMessage>
{
    new ChatMessage
    {
        Role = "system",
        Content = "You are a helpful assistant with access to tools. " +
                  "Use them when needed to answer questions accurately."
    },
    new ChatMessage
    {
        Role = "user",
        Content = "What's the weather like today?"
    }
};

// Send the request with tools
var response = await chatClient.CompleteChatAsync(messages, ct, tools);
Console.WriteLine("Response received.");
```

When the model determines that a tool is needed, the response contains `ToolCalls` instead of a regular text message. The next step shows how to detect and handle these calls.

## Execute the tool and return results

After the model responds with a tool call, you extract the function name and arguments, run the function, and send the result back.

```csharp
var choice = response.Choices[0].Message;

// Check if the model wants to call a tool
if (choice.ToolCalls is { Count: > 0 })
{
    // Add the assistant's response (with tool calls) to the history
    messages.Add(choice);

    foreach (var toolCall in choice.ToolCalls)
    {
        var args = JsonDocument.Parse(
            toolCall.FunctionCall.Arguments
        ).RootElement;
        Console.WriteLine(
            $"Tool call: {toolCall.FunctionCall.Name}({args})"
        );

        // Execute the function
        var result = ExecuteTool(toolCall.FunctionCall.Name, args);

        // Add the tool result to the conversation
        messages.Add(new ChatMessage
        {
            Role = "tool",
            ToolCallId = toolCall.Id,
            Content = result
        });
    }

    // Send the updated conversation back to the model
    var finalResponse = await chatClient.CompleteChatAsync(
        messages, ct, tools
    );
    Console.WriteLine(
        $"Assistant: {finalResponse.Choices[0].Message.Content}"
    );
}
else
{
    // No tool call — the model responded directly
    Console.WriteLine($"Assistant: {choice.Content}");
}
```

The key steps in the tool calling loop are:

1. **Detect tool calls** — check `response.Choices[0].Message.ToolCalls`.
1. **Execute the function** — parse the arguments and call your local function.
1. **Return the result** — add a message with role `tool` and the matching `ToolCallId`.
1. **Get the final answer** — the model uses the tool result to generate a natural response.

## Handle the complete tool calling loop

Here's the complete application that combines tool definitions, SDK initialization, and the tool calling loop into a single runnable file.

Replace the contents of `Program.cs` with the following complete code:

```csharp
using System.Data;
using System.Text.Json;
using Microsoft.AI.Foundry.Local;
using Betalgo.Ranul.OpenAI.ObjectModels.RequestModels;
using Microsoft.Extensions.Logging;

CancellationToken ct = CancellationToken.None;

// --- Tool definitions ---
var tools = new[]
{
    new
    {
        type = "function",
        function = new
        {
            name = "get_weather",
            description = "Get the current weather for a location",
            parameters = new
            {
                type = "object",
                properties = new
                {
                    location = new
                    {
                        type = "string",
                        description = "The city or location"
                    },
                    unit = new
                    {
                        type = "string",
                        @enum = new[] { "celsius", "fahrenheit" },
                        description = "Temperature unit"
                    }
                },
                required = new[] { "location" }
            }
        }
    },
    new
    {
        type = "function",
        function = new
        {
            name = "calculate",
            description = "Perform a math calculation",
            parameters = new
            {
                type = "object",
                properties = new
                {
                    expression = new
                    {
                        type = "string",
                        description =
                            "The math expression to evaluate"
                    }
                },
                required = new[] { "expression" }
            }
        }
    }
};

// --- Tool implementations ---
string ExecuteTool(string functionName, JsonElement arguments)
{
    switch (functionName)
    {
        case "get_weather":
            var location = arguments.GetProperty("location")
                .GetString() ?? "unknown";
            var unit = arguments.TryGetProperty("unit", out var u)
                ? u.GetString() ?? "celsius"
                : "celsius";
            var temp = unit == "celsius" ? 22 : 72;
            return JsonSerializer.Serialize(new
            {
                location,
                temperature = temp,
                unit,
                condition = "Sunny"
            });

        case "calculate":
            var expression = arguments.GetProperty("expression")
                .GetString() ?? "";
            try
            {
                var result = new DataTable()
                    .Compute(expression, null);
                return JsonSerializer.Serialize(new
                {
                    expression,
                    result = result?.ToString()
                });
            }
            catch (Exception ex)
            {
                return JsonSerializer.Serialize(new
                {
                    error = ex.Message
                });
            }

        default:
            return JsonSerializer.Serialize(new
            {
                error = $"Unknown function: {functionName}"
            });
    }
}

string ProcessToolCalls(
    List<ChatMessage> msgs,
    Betalgo.Ranul.OpenAI.ObjectModels.ResponseModels.ChatCompletionResponse resp,
    dynamic client)
{
    var choice = resp.Choices[0].Message;

    while (choice.ToolCalls is { Count: > 0 })
    {
        msgs.Add(choice);

        foreach (var toolCall in choice.ToolCalls)
        {
            var args = JsonDocument.Parse(
                toolCall.FunctionCall.Arguments
            ).RootElement;
            Console.WriteLine(
                $"  Tool call: {toolCall.FunctionCall.Name}({args})"
            );

            var result = ExecuteTool(
                toolCall.FunctionCall.Name, args
            );
            msgs.Add(new ChatMessage
            {
                Role = "tool",
                ToolCallId = toolCall.Id,
                Content = result
            });
        }

        resp = ((Task<Betalgo.Ranul.OpenAI.ObjectModels.ResponseModels
            .ChatCompletionResponse>)client
            .CompleteChatAsync(msgs, ct, tools)).Result;
        choice = resp.Choices[0].Message;
    }

    return choice.Content ?? "";
}

// --- Main application ---
var config = new Configuration
{
    AppName = "tool-calling-app",
    LogLevel = Microsoft.AI.Foundry.Local.LogLevel.Information
};

using var loggerFactory = LoggerFactory.Create(builder =>
{
    builder.SetMinimumLevel(
        Microsoft.Extensions.Logging.LogLevel.Information
    );
});
var logger = loggerFactory.CreateLogger<Program>();

await FoundryLocalManager.CreateAsync(config, logger);
var mgr = FoundryLocalManager.Instance;

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

var chatClient = await model.GetChatClientAsync();

var messages = new List<ChatMessage>
{
    new ChatMessage
    {
        Role = "system",
        Content = "You are a helpful assistant with access to tools. " +
                  "Use them when needed to answer questions accurately."
    }
};

Console.WriteLine("\nTool-calling assistant ready! Type 'quit' to exit.\n");

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

    messages.Add(new ChatMessage
    {
        Role = "user",
        Content = userInput
    });

    var response = await chatClient.CompleteChatAsync(
        messages, ct, tools
    );

    var choice = response.Choices[0].Message;

    if (choice.ToolCalls is { Count: > 0 })
    {
        messages.Add(choice);

        foreach (var toolCall in choice.ToolCalls)
        {
            var args = JsonDocument.Parse(
                toolCall.FunctionCall.Arguments
            ).RootElement;
            Console.WriteLine(
                $"  Tool call: {toolCall.FunctionCall.Name}({args})"
            );

            var result = ExecuteTool(
                toolCall.FunctionCall.Name, args
            );
            messages.Add(new ChatMessage
            {
                Role = "tool",
                ToolCallId = toolCall.Id,
                Content = result
            });
        }

        var finalResponse = await chatClient.CompleteChatAsync(
            messages, ct, tools
        );
        var answer = finalResponse.Choices[0].Message.Content ?? "";
        messages.Add(new ChatMessage
        {
            Role = "assistant",
            Content = answer
        });
        Console.WriteLine($"Assistant: {answer}\n");
    }
    else
    {
        var answer = choice.Content ?? "";
        messages.Add(new ChatMessage
        {
            Role = "assistant",
            Content = answer
        });
        Console.WriteLine($"Assistant: {answer}\n");
    }
}

await model.UnloadAsync();
Console.WriteLine("Model unloaded. Goodbye!");
```

## Run the application

Run the tool-calling assistant:

```bash
dotnet run
```

You see output similar to:

```
Downloading model: 100.00%
Model loaded and ready.

Tool-calling assistant ready! Type 'quit' to exit.

You: What's the weather like today?
  Tool call: get_weather({"location":"current location"})
Assistant: The weather today is sunny with a temperature of 22°C.

You: What is 245 * 38?
  Tool call: calculate({"expression":"245 * 38"})
Assistant: 245 multiplied by 38 equals 9,310.

You: quit
Model unloaded. Goodbye!
```

The model decides when to call a tool based on the user's message. For a weather question it calls `get_weather`, for math it calls `calculate`, and for general questions it responds directly without any tool calls.
