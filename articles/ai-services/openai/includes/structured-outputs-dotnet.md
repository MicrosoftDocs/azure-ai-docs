---
ms.service: azure-ai-openai
ms.topic: how-to
ms.date: 02/10/2025
author: mrbullwinkle
ms.author: mbullwin
zone_pivot_groups: structured-outputs
---

## Getting started

Add the following packages to your project to work with Azure OpenAI:

- **[Azure.AI.OpenAI](https://www.nuget.org/packages/Azure.AI.OpenAI/)**: Provides an Azure OpenAI client with Azure specific functionality that builds on top of the standard [OpenAI](https://www.nuget.org/packages/OpenAI/) library dependency.
- **[Azure.Identity](https://www.nuget.org/packages/Azure.Identity)**: Provides Microsoft Entra ID token authentication support across the Azure SDK libraries. 
- **[Newtonsoft.Json.Schema](https://www.nuget.org/packages/Newtonsoft.Json.Schema)**: Provides helpful utilities for working with JSON schemas.

```dotnetcli
dotnet add package Azure.AI.OpenAI --prerelease
dotnet add package Azure.Identity
dotnet add package Newtonsoft.Json.Schema
```

# [Microsoft Entra ID](#tab/dotnet-entra-id)

If you are new to using Microsoft Entra ID for authentication see [How to configure Azure OpenAI in Azure AI Foundry Models with Microsoft Entra ID authentication](../how-to/managed-identity.md).

```csharp
using Azure.AI.OpenAI;
using Azure.Identity;
using Newtonsoft.Json.Schema.Generation;
using OpenAI.Chat;
using System.ClientModel;

// Create the clients
string endpoint = GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT");

AzureOpenAIClient openAIClient = new(
    new Uri(endpoint),
    new DefaultAzureCredential());

var client = openAIClient.GetChatClient("gpt-4o");

// Create a chat with initial prompts
var chat = new List<ChatMessage>()
    {
         new SystemChatMessage("Extract the event information and projected weather."),
         new UserChatMessage("Alice and Bob are going to a science fair in Seattle on June 1st, 2025.")
    };

// Get the schema of the class for the structured response
JSchemaGenerator generator = new JSchemaGenerator();
var jsonSchema = generator.Generate(typeof(CalendarEvent)).ToString();

// Get a completion with structured output
var chatUpdates = client.CompleteChatStreamingAsync(
        chat,
        new ChatCompletionOptions()
        {
            ResponseFormat = ChatResponseFormat.CreateJsonSchemaFormat(
                        "calenderEvent",
                        BinaryData.FromString(jsonSchema))
        });

// Write the structured response
await foreach (var chatUpdate in chatUpdates)
{
    foreach (var contentPart in chatUpdate.ContentUpdate)
    {
        Console.Write(contentPart.Text);
    }
}

// The class for the structured response
public class CalendarEvent()
{
    public string Name { get; set; }
    public string Date { get; set; }
    public List<string> Participants { get; set; }
}

```

# [Key-based auth](#tab/dotnet-keys)

```csharp
using Azure.AI.OpenAI;
using Newtonsoft.Json.Schema.Generation;
using OpenAI.Chat;
using System.ClientModel;

// Create the clients
string endpoint = GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT");
string key = GetEnvironmentVariable("AZURE_OPENAI_API_KEY");

AzureOpenAIClient openAIClient = new(
    new Uri(endpoint),
    new ApiKeyCredential(key));

var client = openAIClient.GetChatClient("gpt-4o");

// Create a chat with initial prompts
var chat = new List<ChatMessage>()
    {
         new SystemChatMessage("Extract the event information and projected weather."),
         new UserChatMessage("Alice and Bob are going to a science fair in Seattle on June 1st, 2025.")
    };

// Get the schema of the class for the structured response
JSchemaGenerator generator = new JSchemaGenerator();
var jsonSchema = generator.Generate(typeof(CalendarEvent)).ToString();

// Get a completion with structured output
var chatUpdates = client.CompleteChatStreamingAsync(
        chat,
        new ChatCompletionOptions()
        {
            ResponseFormat = ChatResponseFormat.CreateJsonSchemaFormat(
                        "calenderEvent",
                        BinaryData.FromString(jsonSchema))
        });

// Write the structured response
await foreach (var chatUpdate in chatUpdates)
{
    foreach (var contentPart in chatUpdate.ContentUpdate)
    {
        Console.Write(contentPart.Text);
    }
}

// The class for the structured response
public class CalendarEvent()
{
    public string Name { get; set; }
    public string Date { get; set; }
    public List<string> Participants { get; set; }
}

```

---

## Function calling with structured outputs

Structured Outputs for function calling can be enabled with a single parameter, by supplying `strict: true`. 

# [Microsoft Entra ID](#tab/dotnet-entra-id)

```csharp
using Azure.AI.OpenAI;
using Newtonsoft.Json.Schema.Generation;
using OpenAI.Chat;
using System.ClientModel;

// Create the clients
string endpoint = GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT");

AzureOpenAIClient openAIClient = new(
    new Uri(endpoint),
    new DefaultAzureCredential());

var chatClient = openAIClient.GetChatClient("gpt-4o");

// Local function to be used by the assistant tooling
string GetTemperature(string location, string date)
{
    // Placeholder for Weather API
    if(location == "Seattle" && date == "2025-06-01")
    {
        return "75";
    }

    return "50";
}

// Create a tool to get the temperature
ChatTool GetTemperatureTool = ChatTool.CreateFunctionTool(
    functionName: nameof(GetTemperature),
    functionSchemaIsStrict: true,
    functionDescription: "Get the projected temperature by date and location.",
    functionParameters: BinaryData.FromBytes("""
        {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The location of the weather."
                },
                "date": {
                    "type": "string",
                    "description": "The date of the projected weather."
                }
            },
            "required": ["location", "date"],
            "additionalProperties": false  
        }
        """u8.ToArray())
);

// Create a chat with prompts
var chat = new List<ChatMessage>()
    {
         new SystemChatMessage("Extract the event information and projected weather."),
         new UserChatMessage("Alice and Bob are going to a science fair in Seattle on June 1st, 2025.")
    };

// Create a JSON schema for the CalendarEvent structured response
JSchemaGenerator generator = new JSchemaGenerator();
var jsonSchema = generator.Generate(typeof(CalendarEvent)).ToString();

// Get a chat completion from the AI model
var completion = chatClient.CompleteChat(
        chat,
        new ChatCompletionOptions()
        {
            ResponseFormat = ChatResponseFormat.CreateJsonSchemaFormat(
                "calenderEvent",
                BinaryData.FromString(jsonSchema)),
            Tools = { GetTemperatureTool }
        });

Console.WriteLine(completion.Value.ToolCalls[0].FunctionName);

// Structured response class
public class CalendarEvent()
{
    public string Name { get; set; }
    public string Date { get; set; }
    public string Temperature { get; set; }
    public List<string> Participants { get; set; }
}
```

# [Key-based auth](#tab/dotnet-keys)

```csharp
using Azure.AI.OpenAI;
using Newtonsoft.Json.Schema.Generation;
using OpenAI.Chat;
using System.ClientModel;

// Create the clients
string endpoint = GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT");
string key = GetEnvironmentVariable("AZURE_OPENAI_API_KEY");

AzureOpenAIClient openAIClient = new(
    new Uri(endpoint),
    new ApiKeyCredential(key));

var chatClient = openAIClient.GetChatClient("gpt-4o");

// Local function to be used by the assistant tooling
string GetTemperature(string location, string date)
{
    // Placeholder for Weather API
    if(location == "Seattle" && date == "2025-06-01")
    {
        return "75";
    }

    return "50";
}

// Create a tool to get the temperature
ChatTool GetTemperatureTool = ChatTool.CreateFunctionTool(
    functionName: nameof(GetTemperature),
    functionSchemaIsStrict: true,
    functionDescription: "Get the projected temperature by date and location.",
    functionParameters: BinaryData.FromBytes("""
        {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The location of the weather."
                },
                "date": {
                    "type": "string",
                    "description": "The date of the projected weather."
                }
            },
            "required": ["location", "date"],
            "additionalProperties": false  
        }
        """u8.ToArray())
);

// Create a chat with prompts
var chat = new List<ChatMessage>()
    {
         new SystemChatMessage("Extract the event information and projected weather."),
         new UserChatMessage("Alice and Bob are going to a science fair in Seattle on June 1st, 2025.")
    };

// Create a JSON schema for the CalendarEvent structured response
JSchemaGenerator generator = new JSchemaGenerator();
var jsonSchema = generator.Generate(typeof(CalendarEvent)).ToString();

// Get a chat completion from the AI model
var completion = chatClient.CompleteChat(
        chat,
        new ChatCompletionOptions()
        {
            ResponseFormat = ChatResponseFormat.CreateJsonSchemaFormat(
                "calenderEvent",
                BinaryData.FromString(jsonSchema)),
            Tools = { GetTemperatureTool }
        });

Console.WriteLine(completion.Value.ToolCalls[0].FunctionName);

// Structured response class
public class CalendarEvent()
{
    public string Name { get; set; }
    public string Date { get; set; }
    public string Temperature { get; set; }
    public List<string> Participants { get; set; }
}
```
