---
title: Use tool calling with Foundry Local
titleSuffix: Foundry Local
description: Learn how to write applications with Foundry Local that make use of tool calling
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.topic: how-to
ms.author: nakersha
ms.reviewer: metang
author: natke
reviewer: metang
ms.date: 11/17/2025
---

# How to use tool calling with Foundry Local

[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]

Foundry Local can make use of tool calling, a technique where you prompt the model with definitions of available tools that together with a text prompt, allow the model to work out which tools should be called and with what input data. The application then calls those tools and adds the results to a subsequent model prompt to answer the user's query.

The tools can perform functions that the model doesn't have access to, such as getting the current weather, or reading files on the local file system, or accessing a user's address book (providing the application has permission to do so).

This guide shows you how to use this feature of Foundry Local.

## Models that support tool calling

Using the `foundry model list` command you can see which models support tool calling.

In the `Task` column, you can see that the `tools` task indicates that tool calling is supported.

## Tool calling with C# 

The `Microsoft.Extensions.AI` library provides a sophisticated layer that allows a C# application to easily take advantage of tool calling. The tools can be specified as ordinary methods on a class and decorated so that they are included in the model input in the format that the model needs. Follow the steps in the sections below to utilize `Microsoft.Extensions.AI` for tool calling with Foundry Local. The full code sample is shown after the breakdown.

### Choose the model

Choose a model that supports tool calling. In this case, we choose the `qwen2.5-7b` model. This alias resolves to the best variant for your device to execute on.

### Create the chat client

```csharp
var chatClient = client.GetChatClient(model?.ModelId).AsIChatClient().AsBuilder().UseFunctionInvocation().Build();
```

Note the chat client needs to built with `UseFunctionInvocation()`.

### Define the tools

Define the tools in your code. The tools can be methods inside classes. You can see in the sample that there are three tools defined:

* `GetCurrentWeather()`
* `GetTypicalWeather()`
* `GetDateTime()`

Once the tools are defined, they can be added as input to the model:

```csharp
IList<AITool> tools = [
    AIFunctionFactory.Create(WeatherService.GetCurrentWeather),
    AIFunctionFactory.Create(WeatherService.GetTypicalWeather),
    AIFunctionFactory.Create(DateService.GetDateTime)
];
```

### Create the messages object with the prompt

```csharp
var messages = new ChatMessage[]
{
    new ChatMessage(ChatRole.System, "You are a helpful assistant with some tools. When you are mapping cities to timezones, ensure the timezone string is standard"),
    new ChatMessage(ChatRole.User, userPrompt)
};
```

### Run the model

```csharp
var completion = await chatClient.GetResponseAsync(messages, options);
```

The chat client runs the model, extracts the tool call specifications, calls tools, and feeds the result back in the model to help it respond to the prompt.

```bash
dotnet run                
Enter your question or request:
> What time is it in Sydney?
Starting model: qwen2.5-1.5b...
User prompt: What time is it in Sydney?
Processing with model: qwen2.5-1.5b...

In Sydney at this moment, it's Tuesday, November 18, 2025 at 5:17 PM
```

### Full Sample

```csharp
using OpenAI;
using System.ClientModel;
using System.ComponentModel;
using Microsoft.AI.Foundry.Local;
using Microsoft.Extensions.AI;
using ChatMessage = Microsoft.Extensions.AI.ChatMessage;

// Parse command line arguments for model alias and user prompt
var alias = "qwen2.5-7b";
string userPrompt = "";

// Prompt user for input
Console.WriteLine("Enter your question or request:");
Console.Write("> ");
userPrompt = Console.ReadLine() ?? "Hello, how are you?";

Console.WriteLine($"Starting model: {alias}...");

var manager = await FoundryLocalManager.StartModelAsync(aliasOrModelId: alias);

var model = await manager.GetModelInfoAsync(aliasOrModelId: alias);
ApiKeyCredential key = new ApiKeyCredential(manager.ApiKey);
OpenAIClient client = new OpenAIClient(key, new OpenAIClientOptions
{
    Endpoint = manager.Endpoint
});

var chatClient = client.GetChatClient(model?.ModelId).AsIChatClient().AsBuilder().UseFunctionInvocation().Build();

IList<AITool> tools = [
    AIFunctionFactory.Create(WeatherService.GetCurrentWeather),
    AIFunctionFactory.Create(WeatherService.GetTypicalWeather),
    AIFunctionFactory.Create(DateService.GetDateTime)
];

var messages = new ChatMessage[]
{
    new ChatMessage(ChatRole.System, "You are a helpful assistant with some tools. When you are mapping cities to timezones, ensure the timezone string is standard"),
    new ChatMessage(ChatRole.User, userPrompt)
};

ChatOptions options = new()
{
    Tools = tools,
    ToolMode = ChatToolMode.RequireAny,
    MaxOutputTokens = 2048
};

Console.WriteLine($"User prompt: {userPrompt}");
Console.WriteLine($"Processing with model: {alias}...");
Console.WriteLine();

try {
    var completion = await chatClient.GetResponseAsync(messages, options);
    // Print the last assistant message
    Console.WriteLine(completion.Messages.Last().Contents[0]);
} catch (Exception ex) {
    Console.WriteLine($"Model {alias} produced an error: {ex.Message}");
    return;
}

public class WeatherService
{
    [Description("Get the current weather for a specified city.")]
    public static string GetCurrentWeather(string city)
    {
        // In a real implementation, this method would call a weather API.
        return $"The current weather in {city} is sunny with a temperature of 25°C.";
    }

    [Description("Get the typical weather for a specified city and date / time.")]
    public static string GetTypicalWeather(string city, [Description("The date and time for which to get the typical weather in a format that can be parsed by DateTIme")] string datetime)
    {
        var parsedDateTime = DateTime.Parse(datetime.ToString());
        return $"The typical weather at {datetime} in {city} is mild with occasional rain.";
    }   
}

public class DateService
{
    [Description("Get the current date and time in a timezone.")]
    public static string GetDateTime(string timeZone)
    {
        if (timeZone == "" || timeZone == null)
        {
            return DateTime.Now.ToString("F");
        }
        else
        {
            var timeZoneInfo = TimeZoneInfo.FindSystemTimeZoneById(timeZone);
            var localTime = TimeZoneInfo.ConvertTimeFromUtc(DateTime.UtcNow, timeZoneInfo);
            return $"{localTime:F}";
        }
    }
}   
```

This sample uses the following dependencies:

```xml
<<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net9.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Azure.AI.OpenAI" Version="2.1.0" />
    <PackageReference Include="Microsoft.AI.Foundry.Local" Version="0.1.0" />
    <PackageReference Include="Microsoft.Extensions.AI" Version="9.9.0" />
    <PackageReference Include="Microsoft.Extensions.AI.OpenAI" Version="9.8.0-preview.1.25412.6" />
    <PackageReference Include="OpenAI" Version="2.3.0" />
  </ItemGroup>

</Project>
```

## Tool calling in Python

The following sample shows the equivalent sample using Python. The Python sample has fewer convenience APIs. The messages that are input to the model, and the tool definitions have to be explicitly specified. And the tool responses need to be explicitly run and the results thereof fed back into the model.

```python
from openai import OpenAI
import json

from foundry_local import FoundryLocalManager


class ToolCall:

    @staticmethod
    def run():
        # By using an alias, the most suitable model will be downloaded 
        # to your end-user's device.
        alias = "qwen2.5-7b"

        # Create a FoundryLocalManager instance. This will start the Foundry 
        # Local service if it is not already running and load the specified model.
        manager = FoundryLocalManager(alias)

        client = OpenAI(
            base_url=manager.endpoint,
            api_key=manager.api_key  # API key is not required for local usage
        )

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco"
                            }
                        },
                        "required": ["city"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_typical_weather",
                    "description": "Get the typical weather for a specified city and date / time.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco"
                            },
                            "datetime": {
                                "type": "string",
                                "description": "The date and time for which to get the typical weather in a format that can be parsed by datetime"
                            }
                        },
                        "required": ["city", "datetime"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_date_time",
                    "description": "Get the current date and time in a timezone.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "timeZone": {
                                "type": "string",
                                "description": "The timezone string (e.g., 'America/New_York', 'Europe/London')"
                            }
                        },
                        "required": ["timeZone"]
                    }
                }
            }
        ]

        # Create a running input list we will add to over time
        input_list = [
            {"role": "system", "content": "You are a helpful assistant with some tools. When you are mapping cities to timezones, ensure the timezone string is standard."},
            {"role": "user", "content": "What is the time and weather in Dubai?"},
        ]

        # Prompt the model with tools defined
        response = client.chat.completions.create(
            model=manager.get_model_info(alias).id,
            messages=input_list,
            tools=tools,
            stream=False
        )

        # Add response to input list
        print(response.model_dump_json(indent=2))
        input_list.append(response.choices[0].delta)

        # Save tool call outputs for subsequent requests
        tool_call = response.choices[0].delta["tool_calls"][0]
        tool_name = tool_call["function"]["name"]
        tool_call_arguments = json.loads(tool_call["function"]["arguments"])

        def get_current_weather(city):
            return f"The weather in {city} is sunny with a high of 75°F."

        def get_typical_weather(city, datetime):
            from datetime import datetime as dt
            parsed_datetime = dt.fromisoformat(datetime.replace('Z', '+00:00')) if 'Z' in datetime or '+' in datetime or '-' in datetime else dt.strptime(datetime, '%Y-%m-%d %H:%M:%S')
            return f"The typical weather at {datetime} in {city} is mild with occasional rain."

        def get_date_time(timeZone):
            from datetime import datetime
            import zoneinfo
            if not timeZone or timeZone == "":
                return datetime.now().strftime('%A, %B %d, %Y %I:%M:%S %p')
            else:
                try:
                    tz = zoneinfo.ZoneInfo(timeZone)
                    local_time = datetime.now(tz)
                    return local_time.strftime('%A, %B %d, %Y %I:%M:%S %p')
                except Exception:
                    return f"Invalid timezone: {timeZone}"

        get_tool = {
            'get_current_weather': get_current_weather,
            'get_typical_weather': get_typical_weather,
            'get_date_time': get_date_time,
       }

        # Execute the tool logic
        if tool_name == "get_current_weather":
            result = {f"{tool_name}": get_tool[tool_name](tool_call_arguments["city"])}
        elif tool_name == "get_typical_weather":
            result = {f"{tool_name}": get_tool[tool_name](tool_call_arguments["city"], tool_call_arguments["datetime"])}
        elif tool_name == "get_date_time":
            result = {f"{tool_name}": get_tool[tool_name](tool_call_arguments["timeZone"])}
        else:
            result = {f"{tool_name}": f"Unknown tool: {tool_name}"}

        # Provide tool call results to the model
        input_list.append({
            "role": "tool",
            "content": json.dumps(result),
        })

        print("Final input:")
        for row in input_list:
            print(json.dumps(row, indent=2))

        response = client.chat.completions.create(
            model=manager.get_model_info(alias).id,
            messages=input_list,
            tools=tools,
            stream=False,
        )

        # The model's response
        print("Final output:")
        print(response.model_dump_json(indent=2))
        print("\n" + response.choices[0].delta["content"])



if __name__ == "__main__":
    ToolCall.run()
```

## Related content

- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Microsoft.Extensions.AI](/dotnet/ai/microsoft-extensions-ai)
