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

::: zone pivot="csharp"

## Configure client and define functions

First, set up the configuration using `appsettings.json` and create a `PersistentAgentsClient`. 

```csharp
using Azure;
using Azure.AI.Agents.Persistent;
using Azure.Identity;
using Microsoft.Extensions.Configuration;
using System.Text.Json;

// Load configuration from appsettings.json file
IConfigurationRoot configuration = new ConfigurationBuilder()
    .SetBasePath(AppContext.BaseDirectory)
    .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
    .Build();

// Read necessary configuration values (Project Endpoint and Model Deployment Name)
var projectEndpoint = configuration["ProjectEndpoint"];
var modelDeploymentName = configuration["ModelDeploymentName"];
// Initialize the client to interact with the Azure AI Agents Persistent Client using default credentials
PersistentAgentsClient client = new(projectEndpoint, new DefaultAzureCredential());
```

## Define functions
Define the local C# functions that your agent can call, along with their `FunctionToolDefinition` to describe their purpose and parameters to the agent.

```csharp
// Function to get the user's favorite city (hardcoded for example)
string GetUserFavoriteCity() => "Seattle, WA";
// Definition for the GetUserFavoriteCity function, describing its purpose to the agent
FunctionToolDefinition getUserFavoriteCityTool = new("getUserFavoriteCity", "Gets the user's favorite city.");

// Function to get a city's nickname based on its location
string GetCityNickname(string location) => location switch
{
    "Seattle, WA" => "The Emerald City",
    // Handle cases where the nickname is not known
    _ => throw new NotImplementedException(), 
};
// Definition for the GetCityNickname function, including parameter description
FunctionToolDefinition getCityNicknameTool = new(
    name: "getCityNickname",
    description: "Gets the nickname of a city, e.g. 'LA' for 'Los Angeles, CA'.",
    // Define the expected parameters (location string)
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

// Function to get weather at a specific location, with an optional temperature unit
string GetWeatherAtLocation(string location, string temperatureUnit = "f") => location switch
{
    "Seattle, WA" => temperatureUnit == "f" ? "70f" : "21c",
    // Handle cases where weather data is not available
    _ => throw new NotImplementedException()
};
// Definition for the GetWeatherAtLocation function, specifying parameters and enum for unit
FunctionToolDefinition getCurrentWeatherAtLocationTool = new(
    name: "getCurrentWeatherAtLocation",
    description: "Gets the current weather at a provided location.",
    // Define expected parameters (location string, optional unit enum)
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

## Implement function execution logic

Create a helper function, `GetResolvedToolOutput`, to process `RequiredToolCall` objects from the agent. This function will invoke the appropriate C# local function and return its output to the agent.

```csharp
// Helper function to execute the correct local C# function based on the tool call request from the agent
ToolOutput GetResolvedToolOutput(RequiredToolCall toolCall)
{
    // Check if the required call is a function call
    if (toolCall is RequiredFunctionToolCall functionToolCall)
    {
        // Execute GetUserFavoriteCity if its name matches
        if (functionToolCall.Name == getUserFavoriteCityTool.Name)
        {
            return new ToolOutput(toolCall, GetUserFavoriteCity());
        }
        // Parse the arguments provided by the agent for other functions
        using JsonDocument argumentsJson = JsonDocument.Parse(functionToolCall.Arguments);
        // Execute GetCityNickname if its name matches
        if (functionToolCall.Name == getCityNicknameTool.Name)
        {
            // Extract the 'location' argument
            string locationArgument = argumentsJson.RootElement.GetProperty("location").GetString();
            return new ToolOutput(toolCall, GetCityNickname(locationArgument));
        }
        // Execute GetWeatherAtLocation if its name matches
        if (functionToolCall.Name == getCurrentWeatherAtLocationTool.Name)
        {
            // Extract the 'location' argument
            string locationArgument = argumentsJson.RootElement.GetProperty("location").GetString();
            // Check if the optional 'unit' argument was provided
            if (argumentsJson.RootElement.TryGetProperty("unit", out JsonElement unitElement))
            {
                string unitArgument = unitElement.GetString();
                return new ToolOutput(toolCall, GetWeatherAtLocation(locationArgument, unitArgument));
            }
            // Call without the unit if it wasn't provided
            return new ToolOutput(toolCall, GetWeatherAtLocation(locationArgument));
        }
    }
    // Return null if the tool call type isn't handled
    return null;
}
```

## Create agent and conversation thread

Now, create the `PersistentAgent`, providing the model deployment name, a descriptive name, instructions for its behavior, and the list of `FunctionToolDefinitions` it can use. Then, create a `PersistentAgentThread` and add an initial user message to start the conversation.

```csharp
// Create the agent instance
PersistentAgent agent = client.Administration.CreateAgent(
    model: modelDeploymentName, 
    name: "SDK Test Agent - Functions",
    instructions: "You are a weather bot. Use the provided functions to help answer questions. "
        + "Customize your responses to the user's preferences as much as possible and use friendly "
        + "nicknames for cities whenever possible.",
    tools: [getUserFavoriteCityTool, getCityNicknameTool, getCurrentWeatherAtLocationTool]);

// Create a new conversation thread for the agent
PersistentAgentThread thread = client.Threads.CreateThread();

// Add the initial user message to the thread
client.Messages.CreateMessage(
    thread.Id,
    MessageRole.User,
    "What's the weather like in my favorite city?");
```

## Process run and handle function calls

Create a `ThreadRun` for the agent on the thread. Poll for the run's completion status. If the run status is `RequiresAction`, it means the agent needs to call one of your local functions. Use the `GetResolvedToolOutput` helper to get the function's result and submit it back to the run.

```csharp
// Start a run for the agent to process the messages in the thread
ThreadRun run = client.Runs.CreateRun(thread.Id, agent.Id);

// Loop to check the run status and handle required actions
do
{
    // Wait briefly before checking the status again
    Thread.Sleep(TimeSpan.FromMilliseconds(500));
    // Get the latest status of the run
    run = client.Runs.GetRun(thread.Id, run.Id);

    // Check if the agent requires a function call to proceed
    if (run.Status == RunStatus.RequiresAction
        && run.RequiredAction is SubmitToolOutputsAction submitToolOutputsAction)
    {
        // Prepare a list to hold the outputs of the tool calls
        List<ToolOutput> toolOutputs = [];
        // Iterate through each required tool call
        foreach (RequiredToolCall toolCall in submitToolOutputsAction.ToolCalls)
        {
            // Execute the function and get the output using the helper method
            toolOutputs.Add(GetResolvedToolOutput(toolCall));
        }
        // Submit the collected tool outputs back to the run
        run = client.Runs.SubmitToolOutputsToRun(run, toolOutputs);
    }
}
// Continue looping while the run is in progress or requires action
while (run.Status == RunStatus.Queued
    || run.Status == RunStatus.InProgress
    || run.Status == RunStatus.RequiresAction);
```

## Retrieve and display results

After the run completes, retrieve all messages from the thread to see the full conversation, including the agent's final response.

```csharp
// Retrieve all messages from the completed thread, oldest first
Pageable<ThreadMessage> messages = client.Messages.GetMessages(
    threadId: thread.Id,
    order: ListSortOrder.Ascending
);

// Iterate through each message in the thread
foreach (ThreadMessage threadMessage in messages)
{
    // Iterate through content items in the message (usually just one text item)
    foreach (MessageContent content in threadMessage.ContentItems)
    {
        // Process based on content type
        switch (content)
        {
            // If it's a text message
            case MessageTextContent textItem:
                // Print the role (user/agent) and the text content
                Console.WriteLine($"[{threadMessage.Role}]: {textItem.Text}");
                break;
            // Add handling for other content types if necessary (e.g., images)
        }
    }
}
```

## Clean up resources

Finally, clean up the created resources by deleting the thread and the agent.

```csharp
// Delete the conversation thread
client.Threads.DeleteThread(threadId: thread.Id);
// Delete the agent definition
client.Administration.DeleteAgent(agentId: agent.Id);
```

::: zone-end

::: zone pivot="javascript"

## Define a function for your agent to call

Start by defining a function for your agent to call. When you create a function for an agent to call, you describe its structure of it with any required parameters in a docstring. 

```javascript
class FunctionToolExecutor {
    functionTools;

    constructor() {
      this.functionTools = [
        {
          func: this.getUserFavoriteCity,
          ...ToolUtility.createFunctionTool({
            name: "getUserFavoriteCity",
            description: "Gets the user's favorite city.",
            parameters: {},
          }),
        },
        {
          func: this.getCityNickname,
          ...ToolUtility.createFunctionTool({
            name: "getCityNickname",
            description: "Gets the nickname of a city, e.g. 'LA' for 'Los Angeles, CA'.",
            parameters: {
              type: "object",
              properties: {
                location: { type: "string", description: "The city and state, e.g. Seattle, Wa" },
              },
            },
          }),
        },
        {
          func: this.getWeather,
          ...ToolUtility.createFunctionTool({
            name: "getWeather",
            description: "Gets the weather for a location.",
            parameters: {
              type: "object",
              properties: {
                location: { type: "string", description: "The city and state, e.g. Seattle, Wa" },
                unit: { type: "string", enum: ["c", "f"] },
              },
            },
          }),
        },
      ];
    }

    getUserFavoriteCity() {
      return { location: "Seattle, WA" };
    }

    getCityNickname(_location) {
      return { nickname: "The Emerald City" };
    }

    getWeather(_location, unit) {
      return { weather: unit === "f" ? "72f" : "22c" };
    }

    invokeTool(toolCall) {
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
      const result = this.functionTools
        .find((tool) => tool.definition.function.name === toolCall.function.name)
        ?.func(...args);
      return result
        ? {
            toolCallId: toolCall.id,
            output: JSON.stringify(result),
          }
        : undefined;
    }

    getFunctionDefinitions() {
      return this.functionTools.map((tool) => {
        return tool.definition;
      });
    }
  }
```

## Create a client and agent


```javascript
const { AgentsClient, ToolUtility, isOutputOfType } = require("@azure/ai-agents");
const { delay } = require("@azure/core-util");
const { DefaultAzureCredential } = require("@azure/identity");

require("dotenv/config");

const projectEndpoint = process.env["PROJECT_ENDPOINT"] || "<project connection string>";

const client = new AgentsClient(projectEndpoint, new DefaultAzureCredential());
const functionToolExecutor = new FunctionToolExecutor();
  const functionTools = functionToolExecutor.getFunctionDefinitions();
  const agent = await client.createAgent("gpt-4o", {
    name: "my-agent",
    instructions:
      "You are a weather bot. Use the provided functions to help answer questions. Customize your responses to the user's preferences as much as possible and use friendly nicknames for cities whenever possible.",
    tools: functionTools,
  });
  console.log(`Created agent, agent ID: ${agent.id}`);
```

## Create a thread

```javascript
// Create thread
const thread = await client.threads.create();
console.log(`Created Thread, thread ID:  ${thread.id}`);

// Create message
const message = await client.messages.create(
  thread.id,
  "user",
  "What's the weather like in my favorite city?",
);
console.log(`Created message, message ID ${message.id}`);
```

## Create a run and check the output

```javascript
// Create run
let run = await client.runs.create(thread.id, agent.id);
console.log(`Created Run, Run ID:  ${run.id}`);

while (["queued", "in_progress", "requires_action"].includes(run.status)) {
  await delay(1000);
  run = await client.runs.get(thread.id, run.id);
  console.log(`Current Run status - ${run.status}, run ID: ${run.id}`);
  if (run.status === "requires_action" && run.requiredAction) {
    console.log(`Run requires action - ${run.requiredAction}`);
    if (isOutputOfType(run.requiredAction, "submit_tool_outputs")) {
      const submitToolOutputsActionOutput = run.requiredAction;
      const toolCalls = submitToolOutputsActionOutput.submitToolOutputs.toolCalls;
      const toolResponses = [];
      for (const toolCall of toolCalls) {
        if (isOutputOfType(toolCall, "function")) {
          const toolResponse = functionToolExecutor.invokeTool(toolCall);
          if (toolResponse) {
            toolResponses.push(toolResponse);
          }
        }
      }
      if (toolResponses.length > 0) {
        run = await client.runs.submitToolOutputs(thread.id, run.id, toolResponses);
        console.log(`Submitted tool response - ${run.status}`);
      }
    }
  }
}

console.log(`Run status - ${run.status}, run ID: ${run.id}`);
const messages = client.messages.list(thread.id);
for await (const threadMessage of messages) {
  console.log(
    `Thread Message Created at  - ${threadMessage.createdAt} - Role - ${threadMessage.role}`,
  );
  threadMessage.content.forEach((content) => {
    if (isOutputOfType(content, "text")) {
      const textContent = content;
      console.log(`Text Message Content - ${textContent.text.value}`);
    } else if (isOutputOfType(content, "image_file")) {
      const imageContent = content;
      console.log(`Image Message Content - ${imageContent.imageFile.fileId}`);
    }
  });
}
// Delete agent
await client.deleteAgent(agent.id);
console.log(`Deleted agent, agent ID: ${agent.id}`);

```

::: zone-end

::: zone pivot="rest"

## Define a function for your agent to call

Start by defining a function for your agent to call. When you create a function for an agent to call, you describe its structure of it with any required parameters in a docstring. See the other SDK languages for example functions.


## Create an agent

Follow the [REST API Quickstart](../../quickstart.md?pivots=rest-api#api-call-information) to set the right values for the environment variables `AGENT_TOKEN`, `AZURE_AI_FOUNDRY_PROJECT_ENDPOINT` and `API_VERSION`.

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/assistants?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
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

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d ''
```

### Add a user question to the thread

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/messages?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
      "role": "user",
      "content": "What is the weather in Seattle?"
    }'
```

## Run the thread

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/runs?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "asst_abc123",
  }'
```

## Retrieve the status of the run

```bash
curl --request GET \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/runs/run_abc123?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN"
```

## Retrieve the agent response

```bash
curl --request GET \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/messages?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN"
```

::: zone-end
