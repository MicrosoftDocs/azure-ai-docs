---
title: 'How to use Azure AI Foundry Agent Service with function calling'
titleSuffix: Azure AI Foundry
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

# Sample using agents with functions in Azure.AI.Agents

In this example we are demonstrating how to use the local functions with the agents. The functions can be used to provide agent specific information in response to user question.

1. First, set up the configuration and create a `PersistentAgentsClient`. This client will be used for all interactions with the Azure AI Agents Service. This step also includes all necessary `using` directives.

```C# Snippet:AgentsFunctions_Step1_SetupClient
using Azure;
using Azure.AI.Agents.Persistent;
using Azure.Identity;
using Microsoft.Extensions.Configuration;
using System.Text.Json;

IConfigurationRoot configuration = new ConfigurationBuilder()
    .SetBasePath(AppContext.BaseDirectory)
    .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
    .Build();

var projectEndpoint = configuration["ProjectEndpoint"];
var modelDeploymentName = configuration["ModelDeploymentName"];
PersistentAgentsClient client = new(projectEndpoint, new DefaultAzureCredential());
```

2. Next, define the local functions that the agent can call. For each function, create a `FunctionToolDefinition` that describes its name, purpose, and parameters to the agent. These functions and definitions are used by both synchronous and asynchronous agent operations.

```C# Snippet:AgentsFunctions_Step2_DefineFunctionTools
string GetUserFavoriteCity() => "Seattle, WA";
FunctionToolDefinition getUserFavoriteCityTool = new("getUserFavoriteCity", "Gets the user's favorite city.");

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

string GetWeatherAtLocation(string location, string temperatureUnit = "f") => location switch
{
    "Seattle, WA" => temperatureUnit == "f" ? "70f" : "21c",
    _ => throw new NotImplementedException()
};
FunctionToolDefinition getCurrentWeatherAtLocationTool = new(
    name: "getCurrentWeatherAtLocation",
    description: "Gets the current weather at a provided location.",
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
                Unit = new
                {
                    Type = "string",
                    Enum = new[] { "c", "f" },
                },
            },
            Required = new[] { "location" },
        },
        new JsonSerializerOptions() { PropertyNamingPolicy = JsonNamingPolicy.CamelCase }));
```

3. Create a helper function, `GetResolvedToolOutput`. This function takes a `RequiredToolCall` (when the agent determines a local function should be executed) and invokes the appropriate C# function defined in the previous step. It then wraps the result in a `ToolOutput` object for the agent.

```C# Snippet:AgentsFunctions_Step3_GetResolvedToolOutput
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
        if (functionToolCall.Name == getCurrentWeatherAtLocationTool.Name)
        {
            string locationArgument = argumentsJson.RootElement.GetProperty("location").GetString();
            if (argumentsJson.RootElement.TryGetProperty("unit", out JsonElement unitElement))
            {
                string unitArgument = unitElement.GetString();
                return new ToolOutput(toolCall, GetWeatherAtLocation(locationArgument, unitArgument));
            }
            return new ToolOutput(toolCall, GetWeatherAtLocation(locationArgument));
        }
    }
    return null;
}
```

4. Now, create the agent. Provide the model deployment name (retrieved in step 1), a descriptive name for the agent, instructions for its behavior, and the list of `FunctionToolDefinition`s (defined in step 2) it can use.

Synchronous sample:

```C# Snippet:AgentsFunctions_Step4_CreateAgent_Sync
PersistentAgent agent = client.Administration.CreateAgent(
    model: modelDeploymentName,
    name: "SDK Test Agent - Functions",
    instructions: "You are a weather bot. Use the provided functions to help answer questions. "
        + "Customize your responses to the user's preferences as much as possible and use friendly "
        + "nicknames for cities whenever possible.",
    tools: [getUserFavoriteCityTool, getCityNicknameTool, getCurrentWeatherAtLocationTool]);
```

Asynchronous sample:

```C# Snippet:AgentsFunctions_Step4_CreateAgent_Async
PersistentAgent agent = await client.Administration.CreateAgentAsync(
    model: modelDeploymentName,
    name: "SDK Test Agent - Functions",
    instructions: "You are a weather bot. Use the provided functions to help answer questions. "
        + "Customize your responses to the user's preferences as much as possible and use friendly "
        + "nicknames for cities whenever possible.",
    tools: [getUserFavoriteCityTool, getCityNicknameTool, getCurrentWeatherAtLocationTool]);
```

5. Create a new conversation thread and add an initial user message to it. The agent will respond to this message.

Synchronous sample:

```C# Snippet:AgentsFunctions_Step5_CreateThreadAndMessage_Sync
PersistentAgentThread thread = client.Threads.CreateThread();

client.Messages.CreateMessage(
    thread.Id,
    MessageRole.User,
    "What's the weather like in my favorite city?");
```

Asynchronous sample:

```C# Snippet:AgentsFunctions_Step5_CreateThreadAndMessage_Async
PersistentAgentThread thread = await client.Threads.CreateThreadAsync();

await client.Messages.CreateMessageAsync(
    thread.Id,
    MessageRole.User,
    "What's the weather like in my favorite city?");
```

6. Create a run for the agent on the thread and poll for its completion. If the run requires action (e.g., a function call), submit the tool outputs.

Synchronous sample:

```C# Snippet:AgentsFunctions_Step6_CreateAndPollRun_Sync
ThreadRun run = client.Runs.CreateRun(thread.Id, agent.Id);

do
{
    Thread.Sleep(TimeSpan.FromMilliseconds(500));
    run = client.Runs.GetRun(thread.Id, run.Id);

    if (run.Status == RunStatus.RequiresAction
        && run.RequiredAction is SubmitToolOutputsAction submitToolOutputsAction)
    {
        List<ToolOutput> toolOutputs = [];
        foreach (RequiredToolCall toolCall in submitToolOutputsAction.ToolCalls)
        {
            toolOutputs.Add(GetResolvedToolOutput(toolCall));
        }
        run = client.Runs.SubmitToolOutputsToRun(run, toolOutputs);
    }
}
while (run.Status == RunStatus.Queued
    || run.Status == RunStatus.InProgress
    || run.Status == RunStatus.RequiresAction);
```

Asynchronous sample:

```C# Snippet:AgentsFunctions_Step6_CreateAndPollRun_Async
ThreadRun run = await client.Runs.CreateRunAsync(thread.Id, agent.Id);

do
{
    await Task.Delay(TimeSpan.FromMilliseconds(500));
    run = await client.Runs.GetRunAsync(thread.Id, run.Id);

    if (run.Status == RunStatus.RequiresAction
        && run.RequiredAction is SubmitToolOutputsAction submitToolOutputsAction)
    {
        List<ToolOutput> toolOutputs = [];
        foreach (RequiredToolCall toolCall in submitToolOutputsAction.ToolCalls)
        {
            ToolOutput? toolOutput = GetResolvedToolOutput(toolCall);
            if (toolOutput != null)
            {
                toolOutputs.Add(toolOutput);
            }
        }
        run = await client.Runs.SubmitToolOutputsToRunAsync(run, toolOutputs);
    }
}
while (run.Status == RunStatus.Queued
    || run.Status == RunStatus.InProgress
    || run.Status == RunStatus.RequiresAction);
```

7. After the run completes, retrieve and display the messages from the thread to see the conversation, including the agent's responses.

Synchronous sample:

```C# Snippet:AgentsFunctions_Step7_ProcessResults_Sync
Pageable<ThreadMessage> messages = client.Messages.GetMessages(
    threadId: thread.Id,
    order: ListSortOrder.Ascending
);

foreach (ThreadMessage threadMessage in messages)
{
    foreach (MessageContent content in threadMessage.ContentItems)
    {
        switch (content)
        {
            case MessageTextContent textItem:
                Console.WriteLine($"[{threadMessage.Role}]: {textItem.Text}");
                break;
        }
    }
}
```

Asynchronous sample:

```C# Snippet:AgentsFunctions_Step7_ProcessResults_Async
AsyncPageable<ThreadMessage> messages = client.Messages.GetMessagesAsync(
    threadId: thread.Id,
    order: ListSortOrder.Ascending
);

await foreach (ThreadMessage threadMessage in messages)
{
    foreach (MessageContent content in threadMessage.ContentItems)
    {
        switch (content)
        {
            case MessageTextContent textItem:
                Console.WriteLine($"[{threadMessage.Role}]: {textItem.Text}");
                break;
        }
    }
}
```

8. Finally, clean up the created resources by deleting the thread and the agent.

Synchronous sample:

```C# Snippet:AgentsFunctions_Step8_Cleanup_Sync
client.Threads.DeleteThread(threadId: thread.Id);
client.Administration.DeleteAgent(agentId: agent.Id);
```

Asynchronous sample:

```C# Snippet:AgentsFunctions_Step8_Cleanup_Async
await client.Threads.DeleteThreadAsync(threadId: thread.Id);
await client.Administration.DeleteAgentAsync(agentId: agent.Id);
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
Start by defining a function for your agent to call. When you create a function for an agent to call, you describe its structure with any required parameters in a docstring.
```python
import json
import datetime
from typing import Any, Callable, Set, Dict, List, Optional

def fetch_weather(location: str) -> str:
    """
    Fetches the weather information for the specified location.

    :param location: The location to fetch weather for.
    :return: Weather information as a JSON string.
    """
    # Mock weather data for demonstration purposes
    mock_weather_data = {"New York": "Sunny, 25°C", "London": "Cloudy, 18°C", "Tokyo": "Rainy, 22°C"}
    weather = mock_weather_data.get(location, "Weather data not available for this location.")
    return json.dumps({"weather": weather})

# Define user functions
user_functions = {fetch_weather}
```

## Create a client and agent

In the sample below we create a client and define a `toolset` which will be used to process the functions defined in `user_functions`.

`toolset`: When using the toolset parameter, you provide not only the function definitions and descriptions but also their implementations. The SDK will execute these functions within `create_and_run_process` or streaming. These functions will be invoked based on their definitions.

```python
import os, time
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import FunctionTool

# Retrieve the project endpoint from environment variables
project_endpoint = os.environ["PROJECT_ENDPOINT"]

# Initialize the AIProjectClient
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),
    api_version="latest",
)

# Initialize the FunctionTool with user-defined functions
functions = FunctionTool(functions=user_functions)

with project_client:
    # Create an agent with custom functions
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="my-agent",
        instructions="You are a helpful agent",
        tools=functions.definitions,
    )
    print(f"Created agent, ID: {agent.id}")
```
## Create a thread
```python
# Create a thread for communication
thread = project_client.agents.threads.create()
print(f"Created thread, ID: {thread.id}")

# Send a message to the thread
message = project_client.agents.messages.create(
    thread_id=thread.id,
    role="user",
    content="Hello, send an email with the datetime and weather information in New York?",
)
print(f"Created message, ID: {message['id']}")
```
## Create a run and check the output
```python
# Create and process a run for the agent to handle the message
run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
print(f"Created run, ID: {run.id}")

# Poll the run status until it is completed or requires action
while run.status in ["queued", "in_progress", "requires_action"]:
    time.sleep(1)
    run = project_client.agents.runs.get(thread_id=thread.id, run_id=run.id)

    if run.status == "requires_action":
        tool_calls = run.required_action.submit_tool_outputs.tool_calls
        tool_outputs = []
        for tool_call in tool_calls:
            if tool_call.name == "fetch_weather":
                output = fetch_weather("New York")
                tool_outputs.append({"tool_call_id": tool_call.id, "output": output})
        project_client.agents.runs.submit_tool_outputs(thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs)

print(f"Run completed with status: {run.status}")

# Fetch and log all messages from the thread
messages = project_client.agents.messages.list(thread_id=thread.id)
for message in messages:
    print(f"Role: {message['role']}, Content: {message['content']}")

# Delete the agent after use
project_client.agents.delete_agent(agent.id)
print("Deleted agent")
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
