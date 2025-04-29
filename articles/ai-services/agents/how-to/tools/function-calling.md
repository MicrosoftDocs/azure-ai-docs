---
title: 'How to use Azure AI Foundry Agent Service with function calling'
titleSuffix: Azure OpenAI
description: Learn how to use Azure AI Agents with function calling.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 01/30/2025
author: aahill
ms.author: aahi
zone_pivot_groups: selection-function-calling
ms.custom: azure-ai-agents
---

# Azure AI Agents function calling

Azure AI Agents supports function calling, which allows you to describe the structure of functions to an agent and then return the functions that need to be called along with their arguments.

> [!NOTE]
> Runs expire ten minutes after creation. Be sure to submit your tool outputs before the expiration.

### Usage support

|Azure AI foundry support  | Python SDK |	C# SDK | JavaScript SDK | REST API | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|
|      | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

::: zone pivot="csharp"

## Define a function for your agent to call

Start by defining a function for your agent to call. When you create a function for an agent to call, you describe its structure of it with any required parameters in a docstring. 

```csharp
// Example of a function that defines no parameters
string GetUserFavoriteCity() => "Seattle, WA";
FunctionToolDefinition getUserFavoriteCityTool = new("getUserFavoriteCity", "Gets the user's favorite city.");
// Example of a function with a single required parameter
string GetCityNickname(string location) => location switch
{
    "Seattle, WA" => "The Emerald City",
    _ => throw new NotImplementedException(),
};
FunctionToolDefinition getCityNicknameTool = new(
    name: "getCityNickname",
    description: "Gets the nickname of a city, e.g. 'LA' for 'Los Angeles, CA'.",
    parameters: BinaryData.FromObjectAsJson(
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
            },
            Required = new[] { "location" },
        },
        new JsonSerializerOptions() { PropertyNamingPolicy = JsonNamingPolicy.CamelCase }));
```

<!--See the [C# file on GitHub](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/user_functions.py) for an additional function definition examples. -->

In the following sample, we create a helper function to get and parse the resolved tools' outputs, and return it. 

```csharp
ToolOutput GetResolvedToolOutput(RequiredToolCall toolCall)
{
    if (toolCall is RequiredFunctionToolCall functionToolCall)
    {
        if (functionToolCall.Name == getUserFavoriteCityTool.Name)
                {
                    return new ToolOutput(toolCall, GetUserFavoriteCity());
                }
                using JsonDocument argumentsJson = JsonDocument.Parse(functionToolCall.Arguments);
        if (functionToolCall.Name == getCityNicknameTool.Name)
        {
            string locationArgument = argumentsJson.RootElement.GetProperty("location").GetString();
            return new ToolOutput(toolCall, GetCityNickname(locationArgument));
        }
    }
    return null;
}
```

## Create a client and agent

```csharp
// note: parallel function calling is only supported with newer models like gpt-4-1106-preview
Response<Agent> agentResponse = await client.CreateAgentAsync(
    model: "gpt-4-1106-preview",
    name: "SDK Test Agent - Functions",
        instructions: "You are a weather bot. Use the provided functions to help answer questions. "
            + "Customize your responses to the user's preferences as much as possible and use friendly "
            + "nicknames for cities whenever possible.",
    tools: new List<ToolDefinition> { getUserFavoriteCityTool, getCityNicknameTool, getCurrentWeatherAtLocationTool }
    );
Agent agent = agentResponse.Value;
```

## Create a thread

```csharp
Response<AgentThread> threadResponse = await client.CreateThreadAsync();
AgentThread thread = threadResponse.Value;

Response<ThreadMessage> messageResponse = await client.CreateMessageAsync(
    thread.Id,
    MessageRole.User,
    "What's the weather like in my favorite city?");
ThreadMessage message = messageResponse.Value;
```

## Create a run and check the output

```csharp
Response<ThreadRun> runResponse = await client.CreateRunAsync(thread, agent);

#region Snippet:FunctionsHandlePollingWithRequiredAction
do
{
    await Task.Delay(TimeSpan.FromMilliseconds(500));
    runResponse = await client.GetRunAsync(thread.Id, runResponse.Value.Id);

    if (runResponse.Value.Status == RunStatus.RequiresAction
        && runResponse.Value.RequiredAction is SubmitToolOutputsAction submitToolOutputsAction)
    {
        List<ToolOutput> toolOutputs = new();
        foreach (RequiredToolCall toolCall in submitToolOutputsAction.ToolCalls)
        {
            toolOutputs.Add(GetResolvedToolOutput(toolCall));
        }
        runResponse = await client.SubmitToolOutputsToRunAsync(runResponse.Value, toolOutputs);
    }
}
while (runResponse.Value.Status == RunStatus.Queued
    || runResponse.Value.Status == RunStatus.InProgress);
#endregion

Response<PageableList<ThreadMessage>> afterRunMessagesResponse
    = await client.GetMessagesAsync(thread.Id);
IReadOnlyList<ThreadMessage> messages = afterRunMessagesResponse.Value.Data;

// Note: messages iterate from newest to oldest, with the messages[0] being the most recent
foreach (ThreadMessage threadMessage in messages)
{
    Console.Write($"{threadMessage.CreatedAt:yyyy-MM-dd HH:mm:ss} - {threadMessage.Role,10}: ");
    foreach (MessageContent contentItem in threadMessage.ContentItems)
    {
        if (contentItem is MessageTextContent textItem)
        {
            Console.Write(textItem.Text);
        }
        else if (contentItem is MessageImageFileContent imageFileItem)
        {
            Console.Write($"<image from ID: {imageFileItem.FileId}");
        }
        Console.WriteLine();
    }
}
```

::: zone-end

::: zone pivot="javascript"

## Define a function for your agent to call

Start by defining a function for your agent to call. When you create a function for an agent to call, you describe its structure of it with any required parameters in a docstring. 

```javascript
class FunctionToolExecutor {
  private functionTools: { func: Function, definition: FunctionToolDefinition }[];

  constructor() {
    this.functionTools = [{
      func: this.getUserFavoriteCity,
      ...ToolUtility.createFunctionTool({
        name: "getUserFavoriteCity",
        description: "Gets the user's favorite city.",
        parameters: {}
      })
    }, {
      func: this.getCityNickname,
      ...ToolUtility.createFunctionTool({
        name: "getCityNickname",
        description: "Gets the nickname of a city, e.g. 'LA' for 'Los Angeles, CA'.",
        parameters: { type: "object", properties: { location: { type: "string", description: "The city and state, e.g. Seattle, Wa" } } }
      })
    }, {
      func: this.getWeather,
      ...ToolUtility.createFunctionTool({
        name: "getWeather",
        description: "Gets the weather for a location.",
        parameters: { type: "object", properties: { location: { type: "string", description: "The city and state, e.g. Seattle, Wa" }, unit: { type: "string", enum: ['c', 'f'] } } }
      })
    }];
  }

  private getUserFavoriteCity(): {} {
    return { "location": "Seattle, WA" };
  }

  private getCityNickname(location: string): {} {
    return { "nickname": "The Emerald City" };
  }

  private getWeather(location: string, unit: string): {} {
    return { "weather": unit === "f" ? "72f" : "22c" };
  }

  public invokeTool(toolCall: RequiredToolCallOutput & FunctionToolDefinitionOutput): ToolOutput | undefined {
    console.log(`Function tool call - ${toolCall.function.name}`);
    const args = [];
    if (toolCall.function.parameters) {
      try {
        const params = JSON.parse(toolCall.function.parameters);
        for (const key in params) {
          if (Object.prototype.hasOwnProperty.call(params, key)) {
            args.push(params[key]);
          }
        }
      } catch (error) {
        console.error(`Failed to parse parameters: ${toolCall.function.parameters}`, error);
        return undefined;
      }
    }
    const result = this.functionTools.find((tool) => tool.definition.function.name === toolCall.function.name)?.func(...args);
    return result ? {
      toolCallId: toolCall.id,
      output: JSON.stringify(result)
    } : undefined;
  }

  public getFunctionDefinitions(): FunctionToolDefinition[] {
    return this.functionTools.map(tool => {return tool.definition});
  }
}
```

## Create a client and agent


```javascript
const functionToolExecutor = new FunctionToolExecutor();
const functionTools = functionToolExecutor.getFunctionDefinitions();
const agent = await client.agents.createAgent("gpt-4o",
  {
    name: "my-agent",
    instructions: "You are a weather bot. Use the provided functions to help answer questions. Customize your responses to the user's preferences as much as possible and use friendly nicknames for cities whenever possible.",
    tools: functionTools
  });
console.log(`Created agent, agent ID: ${agent.id}`);
```

## Create a thread

```javascript
// create a thread
const thread = await client.agents.createThread();

// add a message to thread
await client.agents.createMessage(
    thread.id, {
    role: "user",
    content: "What is the weather in Seattle?",
});
```

## Create a run and check the output

```javascript

  // create a run
  const streamEventMessages = await client.agents.createRun(thread.id, agent.id).stream();

  for await (const eventMessage of streamEventMessages) {
    switch (eventMessage.event) {
      case RunStreamEvent.ThreadRunCreated:
        break;
      case MessageStreamEvent.ThreadMessageDelta:
        {
          const messageDelta = eventMessage.data;
          messageDelta.delta.content.forEach((contentPart) => {
            if (contentPart.type === "text") {
              const textContent = contentPart;
              const textValue = textContent.text?.value || "No text";
            }
          });
        }
        break;

      case RunStreamEvent.ThreadRunCompleted:
        break;
      case ErrorEvent.Error:
        console.log(`An error occurred. Data ${eventMessage.data}`);
        break;
      case DoneEvent.Done:
        break;
    }
  }

  // Print the messages from the agent
  const messages = await client.agents.listMessages(thread.id);

  // Messages iterate from oldest to newest
  // messages[0] is the most recent
  for (let i = messages.data.length - 1; i >= 0; i--) {
    const m = messages.data[i];
    if (isOutputOfType<MessageTextContentOutput>(m.content[0], "text")) {
      const textContent = m.content[0];
      console.log(`${textContent.text.value}`);
      console.log(`---------------------------------`);
    }
  }
```

::: zone-end

::: zone pivot="python"


## Define a function for your agent to call

Start by defining a function for your agent to call. When you create a function for an agent to call, you describe its structure of it with any required parameters in a docstring. 

```python
import json
import datetime
from typing import Any, Callable, Set, Dict, List, Optional

def fetch_weather(location: str) -> str:
    """
    Fetches the weather information for the specified location.

    :param location (str): The location to fetch weather for.
    :return: Weather information as a JSON string.
    :rtype: str
    """
    # In a real-world scenario, you'd integrate with a weather API.
    # Here, we'll mock the response.
    mock_weather_data = {"New York": "Sunny, 25°C", "London": "Cloudy, 18°C", "Tokyo": "Rainy, 22°C"}
    weather = mock_weather_data.get(location, "Weather data not available for this location.")
    weather_json = json.dumps({"weather": weather})
    return weather_json

# Statically defined user functions for fast reference
user_functions: Set[Callable[..., Any]] = {
    fetch_weather,
}
```


## Create a client and agent

In the sample below we create a client and define a `toolset` which will be used to process the functions defined in `user_functions`.

`toolset`: When using the toolset parameter, you provide not only the function definitions and descriptions but also their implementations. The SDK will execute these functions within create_and_run_process or streaming. These functions will be invoked based on their definitions.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import FunctionTool, ToolSet
from user_functions import user_functions # user functions which can be found in a user_functions.py file.

# Create an Azure AI Client from a connection string, copied from your Azure AI Foundry project.
# It should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<HubName>"
# Customers need to login to Azure subscription via Azure CLI and set the environment variables

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"],
)

# Initialize agent toolset with user functions
functions = FunctionTool(user_functions)
toolset = ToolSet()
toolset.add(functions)

agent = project_client.agents.create_agent(
    model="gpt-4o-mini", name="my-agent", instructions="You are a weather bot. Use the provided functions to help answer questions.", toolset=toolset
)
print(f"Created agent, ID: {agent.id}")
```

## Create a thread

```python
# Create thread for communication
thread = project_client.agents.create_thread()
print(f"Created thread, ID: {thread.id}")

# Create message to thread
message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="Hello, send an email with the datetime and weather information in New York?",
)
print(f"Created message, ID: {message.id}")
```

## Create a run and check the output

```python
# Create and process agent run in thread with tools
run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
print(f"Run finished with status: {run.status}")

if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Delete the agent when done
project_client.agents.delete_agent(agent.id)
print("Deleted agent")

# Fetch and log all messages
messages = project_client.agents.list_messages(thread_id=thread.id)
print(f"Messages: {messages}")
```

::: zone-end

::: zone pivot="rest"

## Define a function for your agent to call

Start by defining a function for your agent to call. When you create a function for an agent to call, you describe its structure of it with any required parameters in a docstring. See the other SDK languages for example functions.


## Create a client and agent

Follow the [REST API Quickstart](../../quickstart.md?pivots=rest-api) to set the right values for the environment variables `AZURE_AI_AGENTS_TOKEN` and `AZURE_AI_AGENTS_ENDPOINT`.
```console
curl $AZURE_AI_AGENTS_ENDPOINT/assistants?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "instructions": "You are a weather bot. Use the provided functions to answer questions.",
    "model": "gpt-4o-mini",
    tools=[{
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get the weather in location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {"type": "string", "description": "The city name, for example San Francisco"}
          },
          "required": ["location"]
        }
      }
    }]
  }'
```


## Create a thread

```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d ''
```

### Add a user question to the thread

```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/messages?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
      "role": "user",
      "content": "What is the weather in Seattle?"
    }'
```

## Run the thread

```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/runs?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "asst_abc123",
  }'
```

## Retrieve the status of the run

```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/runs/run_abc123?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN"
```

## Retrieve the agent response

```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/messages?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN"
```

::: zone-end