---
title: Use Foundry Agent Service with function calling
titleSuffix: Microsoft Foundry
description: Learn how to implement function calling with Microsoft Foundry Agents. Define functions, handle requests, and execute custom code for AI-powered workflows.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 12/19/2025
author: alvinashcraft
ms.author: aashcraft
zone_pivot_groups: selection-function-calling
ms.custom: azure-ai-agents
ai-usage: ai-assisted
---

# Azure AI Agents function calling

> [!NOTE]
> This article refers to the classic version of the agents API. 
>
> 🔍 [View the new function calling documentation](../../../default/agents/how-to/tools/function-calling.md?view=foundry&preserve-view=true).

By using Azure AI Agents function calling, you can extend agent capabilities by defining custom functions. When an agent determines that a function needs to be called, it returns metadata with the function name and arguments. Your application code executes the function and returns results. This guide shows you how to implement function calling in Python, C#, JavaScript, Java, and REST API to create powerful AI workflows.

> [!NOTE]
> - The agent requests function calls from your code, and your application executes the functions. Run executions expire 10 minutes after creation, so ensure your functions complete and return responses within this time limit.
> - Both the Microsoft Foundry portal and the Microsoft Foundry SDK support function calling. When you create agents with function calling capabilities, they appear in both portals. However, executing function calling requires your custom code. The portals facilitate agent configuration and monitoring but can't directly execute your custom functions.

### Usage support

| Azure AI foundry support | Python SDK | C# SDK | JavaScript SDK | REST API | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|
|      | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Best practices

### Multi-turn function calling

The agent may require multiple function calls to complete a single user request. For example, if a user asks "What's the weather like in my favorite city?", the agent might:

1. First call `getUserFavoriteCity()` to determine the city
2. Then call `getWeather(location)` with the result

Your polling loop must handle multiple `requires_action` states in sequence. Don't assume the run completes after submitting one function result—continue polling until the run status is `completed` or a terminal state (`failed`, `cancelled`, `expired`).

### Error handling in functions

When your function execution fails, you have two options:

1. **Return an error message** - Submit a descriptive error as the tool output. The agent can use this to provide a helpful response to the user.
2. **Cancel the run** - If the error is unrecoverable, cancel the run and handle it in your application.

```python
# Example: Returning an error message
if error_occurred:
    tool_outputs.append({
        "tool_call_id": tool_call.id,
        "output": json.dumps({"error": "Location not found. Please provide a valid city name."})
    })
```

### Timeout considerations

Runs expire **10 minutes** after creation. Plan your function implementations accordingly:

- If your function makes external API calls, set appropriate timeouts
- For long-running operations, consider returning a partial result or status update
- Monitor run status and handle `expired` status gracefully

### Polling with backoff

Instead of polling with a fixed delay, consider exponential backoff to reduce API calls:

```python
# Example: Exponential backoff polling
import time

delay = 0.5  # Start with 500ms
max_delay = 5  # Cap at 5 seconds

while run.status in ["queued", "in_progress", "requires_action"]:
    time.sleep(delay)
    run = project_client.agents.runs.get(thread_id=thread.id, run_id=run.id)

    if run.status == "requires_action":
        # Handle function call, reset delay after action
        delay = 0.5
    else:
        # Increase delay for next poll
        delay = min(delay * 1.5, max_delay)
```

### Function definition best practices

- **Use clear descriptions** - The agent uses your function descriptions to decide when to call them. Be specific about what each function does and when it should be used.
- **Validate required parameters** - Mark parameters as `required` in your schema if they're necessary for the function to work correctly.
- **Keep parameter names intuitive** - Use names like `location`, `temperature_unit` rather than abbreviations.
- **Return structured JSON** - Return JSON objects rather than plain strings to give the agent more context about the result.

::: zone pivot="python"
## Function calling code example

> [!NOTE]
> You can find a streaming example on [GitHub](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-agents/samples/agents_streaming/sample_agents_stream_eventhandler_with_functions.py).

The following Python code demonstrates how to implement an agent with function calling capabilities. This example shows:

1. **Define function tools** - Create Python functions (like `fetch_weather`) that the agent can request to call.
1. **Register functions with the agent** - Provide function definitions to the agent so it knows what capabilities are available.
1. **Create and run the agent** - Set up the agent, thread, and message to start a conversation.
1. **Handle function call requests** - When the agent determines it needs a function, poll the run status and detect when `status == "requires_action"`.
1. **Execute functions** - **Your code is responsible for calling the actual function** - the agent doesn't execute it automatically.
1. **Return results** - Submit the function output back to the agent to continue the conversation.

> [!IMPORTANT]
> The language model (LLM) doesn't execute your functions directly. When the agent determines a function is needed, it returns a request with the function name and arguments. Your application code must detect this request, execute the appropriate function, and submit the results back to the agent.

Use the following code sample to create an agent and call the function.

```python
import os, time
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import FunctionTool
import json
import datetime
from typing import Any, Callable, Set, Dict, List, Optional


# Start by defining a function for your agent to call. 
# When you create a function for an agent to call, you describe its structure 
# with any required parameters in a docstring.


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

# Retrieve the project endpoint from environment variables
project_endpoint = os.environ["PROJECT_ENDPOINT"]
model_name = os.environ["MODEL_DEPLOYMENT_NAME"]
# Initialize the AIProjectClient
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential()
)

# Initialize the FunctionTool with user-defined functions
functions = FunctionTool(functions=user_functions)

with project_client:
    # Create an agent with custom functions
    agent = project_client.agents.create_agent(
        model=model_name,
        name="my-agent",
        instructions="You are a helpful agent",
        tools=functions.definitions,
    )
    print(f"Created agent, ID: {agent.id}")

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

# Create and process a run for the agent to handle the message
run = project_client.agents.runs.create(thread_id=thread.id, agent_id=agent.id)
print(f"Created run, ID: {run.id}")

# Poll the run status until it is completed or requires action
while run.status in ["queued", "in_progress", "requires_action"]:
    time.sleep(1)
    run = project_client.agents.runs.get(thread_id=thread.id, run_id=run.id)

    if run.status == "requires_action":
        tool_calls = run.required_action.submit_tool_outputs.tool_calls
        tool_outputs = []
        for tool_call in tool_calls:
            if tool_call.function.name == "fetch_weather":
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
## Function calling code example

> [!NOTE]
> You can find a streaming example on [GitHub](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Agents.Persistent/samples/Sample8_PersistentAgents_FunctionsWithStreaming.md).

The following C# code demonstrates how to implement an agent with function calling capabilities. This example shows:

1. **Define function tools** - Create C# methods (like `GetWeatherAtLocation`) that the agent can request to call.
1. **Create function definitions** - Use `FunctionToolDefinition` to describe each function's purpose and parameters to the agent.
1. **Implement function execution logic** - Build a helper method to route function call requests to your actual C# methods.
1. **Create and run the agent** - Set up the agent, thread, and message to start a conversation.
1. **Handle function call requests** - Poll the run status and detect when `Status == RunStatus.RequiresAction`.
1. **Execute functions** - **Your code is responsible for calling the actual function** - the agent doesn't execute it automatically.
1. **Return results** - Submit the function output back to the agent using `SubmitToolOutputsToRun`.

> [!IMPORTANT]
> The language model (LLM) doesn't execute your functions directly. When the agent determines a function is needed, it returns a request with the function name and arguments. Your application code must detect this request, execute the appropriate function, and submit the results back to the agent.

### Configure the client and define functions

```csharp
using Azure;
using Azure.AI.Agents.Persistent;
using Azure.Identity;
using Microsoft.Extensions.Configuration;
using System.Text.Json;

//First, set up the configuration using `appsettings.json`, load it, and create a `PersistentAgentsClient`. 

IConfigurationRoot configuration = new ConfigurationBuilder()
    .SetBasePath(AppContext.BaseDirectory)
    .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
    .Build();

// Read necessary configuration values (Project Endpoint and Model Deployment Name)
var projectEndpoint = configuration["PROJECT_ENDPOINT"];
var modelDeploymentName = configuration["MODEL_DEPLOYMENT_NAME"];
// Initialize the client to interact with the Azure AI Agents Persistent Client using default credentials
PersistentAgentsClient client = new(projectEndpoint, new DefaultAzureCredential());

//Define the local C# functions that your agent can call, 
//along with their `FunctionToolDefinition` to describe their purpose and parameters to the agent.

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

//Implement function execution logic

/*
Create a helper function, `GetResolvedToolOutput`, to process `RequiredToolCall` objects from the agent. 
This function will invoke the appropriate C# local function and return its output to the agent.
*/

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

//Create agent and conversation thread

/*
Create the `PersistentAgent`, providing the model deployment name, a descriptive name, 
instructions for its behavior, and the list of `FunctionToolDefinitions` it can use. 
Then, create a `PersistentAgentThread` and add an initial user message to start the conversation.
*/

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

//Process run and handle function calls

/*
Create a `ThreadRun` for the agent on the thread. Poll for the run's completion status. 
If the run status is `RequiresAction`, it means the agent needs to call one of your local functions. 
Use the `GetResolvedToolOutput` helper to get the function's result and submit it back to the run.

Start a run for the agent to process the messages in the thread
*/

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
        run = client.Runs.SubmitToolOutputsToRun(run, toolOutputs, null);
    }
}
// Continue looping while the run is in progress or requires action
while (run.Status == RunStatus.Queued
    || run.Status == RunStatus.InProgress
    || run.Status == RunStatus.RequiresAction);

// Retrieve and display results

/*
After the run completes, retrieve all messages from the thread to see the full conversation, 
including the agent's final response.
*/

// Retrieve all messages from the completed thread, oldest first
Pageable<PersistentThreadMessage> messages = client.Messages.GetMessages(
    threadId: thread.Id,
    order: ListSortOrder.Ascending
);

// Iterate through each message in the thread
foreach (PersistentThreadMessage threadMessage in messages)
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

// Clean up resources

/*
Finally, clean up the created resources by deleting the thread and the agent.
*/

// Delete the conversation thread
client.Threads.DeleteThread(threadId: thread.Id);
// Delete the agent definition
client.Administration.DeleteAgent(agentId: agent.Id);
```

::: zone-end

::: zone pivot="javascript"
## Function calling code example

The following JavaScript code demonstrates how to implement an agent with function calling capabilities. This example shows how to:

1. **Define function tools** - Create JavaScript functions (like `getWeather`) that the agent can request to call.
1. **Create a function executor class** - Use `FunctionToolExecutor` to organize functions and their definitions.
1. **Register functions with the agent** - Provide function definitions by using `ToolUtility.createFunctionTool`.
1. **Create and run the agent** - Set up the agent, thread, and message to start a conversation.
1. **Handle function call requests** - Poll the run status and detect when `status === "requires_action"`.
1. **Execute functions** - **Your code is responsible for calling the actual function** - the agent doesn't execute it automatically.
1. **Return results** - Submit the function output back to the agent by using `submitToolOutputs`.

> [!IMPORTANT]
> The language model (LLM) doesn't execute your functions directly. When the agent determines a function is needed, it returns a request with the function name and arguments. Your application code must detect this request, execute the appropriate function, and submit the results back to the agent.

```javascript

// Define a function for your agent to call

/*
Start by defining a function for your agent to call. When you create a function for an agent to call, 
you describe its structure of it with any required parameters in a docstring. 
*/

const { AgentsClient, ToolUtility, isOutputOfType } = require("@azure/ai-agents");
const { delay } = require("@azure/core-util");
const { DefaultAzureCredential } = require("@azure/identity");

require("dotenv/config");

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

// Create a client and agent

const projectEndpoint = process.env["PROJECT_ENDPOINT"];
const modelName = process.env["MODEL_DEPLOYMENT_NAME"];

const client = new AgentsClient(projectEndpoint, new DefaultAzureCredential());
const functionToolExecutor = new FunctionToolExecutor();
  const functionTools = functionToolExecutor.getFunctionDefinitions();
  const agent = await client.createAgent(modelName, {
    name: "my-agent",
    instructions:
      "You are a weather bot. Use the provided functions to help answer questions. Customize your responses to the user's preferences as much as possible and use friendly nicknames for cities whenever possible.",
    tools: functionTools,
  });
  console.log(`Created agent, agent ID: ${agent.id}`);

// Create a thread
const thread = await client.threads.create();
console.log(`Created Thread, thread ID:  ${thread.id}`);

// Create message
const message = await client.messages.create(
  thread.id,
  "user",
  "What's the weather like in my favorite city?",
);
console.log(`Created message, message ID ${message.id}`);

// Create a run and check the output

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
// Delete agent - comment this out if you want to keep your agent
await client.deleteAgent(agent.id);
console.log(`Deleted agent, agent ID: ${agent.id}`);

```

::: zone-end

::: zone pivot="rest"
## Function calling code example

The following REST API examples demonstrate how to implement an agent with function calling capabilities. This example shows:

1. **Define function tools** - Describe your function structure with parameters in the agent creation request.
1. **Create the agent** - Register the agent with function definitions so it knows what capabilities are available.
1. **Create a thread and add messages** - Set up the conversation thread and add the user's question.
1. **Run the thread** - Start the agent execution to process the message.
1. **Poll run status** - Check the run status to detect when the agent requests a function call.
1. **Execute functions** - **Your code is responsible for calling the actual function** - the agent doesn't execute it automatically.
1. **Submit function results** - Return the function output to the agent so that the run can continue and complete.

> [!IMPORTANT]
> The language model (LLM) doesn't execute your functions directly. When the agent determines a function is needed, the run status indicates `requires_action` with function call details. Your application code must detect this, execute the appropriate function, and submit the results back to the agent via the API.

### Define a function for your agent to call

Start by defining a function for your agent to call. When you create a function for an agent to call, describe its structure with any required parameters in a docstring. See the other SDK languages for example functions.


### Create an agent

Follow the [REST API Quickstart](../../quickstart.md?pivots=rest-api) to set the right values for the environment variables `AGENT_TOKEN`, `AZURE_AI_FOUNDRY_PROJECT_ENDPOINT`, and `API_VERSION`.

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/assistants?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "instructions": "You are a weather bot. Use the provided functions to answer questions.",
    "model": "gpt-4o-mini",
    "tools": [
      {
        "type": "function",
        "function": {
          "name": "get_weather",
          "description": "Get the weather in location",
          "parameters": {
            "type": "object",
            "properties": {
              "location": {
                "type": "string",
                "description": "The city name, for example San Francisco"
              }
            },
            "required": ["location"]
          }
        }
      }
    ]
  }'
```

### Create a thread

Capture the `id` from the response (for example, `thread_abc123`) so you can reuse it in later requests.

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

#### Add a user question to the thread

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

### Run the thread

Store the returned `run` identifier (for example, `run_abc123`) for subsequent polling requests.

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/runs?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "asst_abc123"
  }'
```

### Retrieve the status of the run

```bash
curl --request GET \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/runs/run_abc123?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN"
```

When the agent needs one of your functions, the run enters the `requires_action` state. The response includes the `required_action.submit_tool_outputs.tool_calls` array, which lists the name of the function to call and its arguments.

```json
{
  "id": "run_abc123",
  "status": "requires_action",
  "required_action": {
    "type": "submit_tool_outputs",
    "submit_tool_outputs": {
      "tool_calls": [
        {
          "id": "call_123",
          "type": "function",
          "function": {
            "name": "get_weather",
            "arguments": "{\"location\":\"Seattle\"}"
          }
        }
      ]
    }
  }
}
```

When you detect the `requires_action` status:

1. Extract the `tool_calls` array from `required_action.submit_tool_outputs.tool_calls`.
1. For each tool call, use the `function.name` and `function.arguments` values to execute your own function implementation.
1. Capture the output from your function.
1. Submit the results by using the following endpoint, matching each output to its `tool_call_id`.

### Submit function results to the run

After your code executes the function, send the output back to the run by calling `submit-tool-outputs`. Use the `tool_call_id` from the polling response so the service can match your output to the original request.

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/runs/run_abc123/submit-tool-outputs?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tool_outputs": [
      {
        "tool_call_id": "call_123",
        "output": "{\"forecast\":\"Rainy and 55 F\"}"
      }
    ]
  }'
```

Submitting the output moves the run back to the `in_progress` state. Continue polling until the status changes to `completed`.

### Retrieve the agent response

```bash
curl --request GET \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/messages?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN"
```
::: zone-end

::: zone pivot="java"
## Function calling code example

The following Java code demonstrates how to implement an agent with function calling capabilities. This example shows:

1. **Define function tools** - Create Java functions (like `getUserFavoriteCity` and `getCityNickname`) that the agent can request to call.
1. **Create function definitions** - Use `FunctionToolDefinition` to describe each function's purpose and parameters to the agent.
1. **Implement function execution logic** - Build a resolver function to route function call requests to your actual Java methods.
1. **Create and run the agent** - Set up the agent, thread, and message to start a conversation.
1. **Handle function call requests** - Poll the run status and detect when `status == RunStatus.REQUIRES_ACTION`.
1. **Execute functions** - **Your code is responsible for calling the actual function** - the agent doesn't execute it automatically.
1. **Return results** - Submit the function output back to the agent using `submitToolOutputsToRun`.

> [!IMPORTANT]
> The language model (LLM) doesn't execute your functions directly. When the agent determines a function is needed, it returns a request with the function name and arguments. Your application code must detect this request, execute the appropriate function, and submit the results back to the agent.

```java
package com.example.agents;

import com.azure.ai.agents.persistent.MessagesClient;
import com.azure.ai.agents.persistent.PersistentAgentsAdministrationClient;
import com.azure.ai.agents.persistent.PersistentAgentsClient;
import com.azure.ai.agents.persistent.PersistentAgentsClientBuilder;
import com.azure.ai.agents.persistent.RunsClient;
import com.azure.ai.agents.persistent.ThreadsClient;
import com.azure.ai.agents.persistent.models.CreateAgentOptions;
import com.azure.ai.agents.persistent.models.CreateRunOptions;
import com.azure.ai.agents.persistent.models.FunctionDefinition;
import com.azure.ai.agents.persistent.models.FunctionToolDefinition;
import com.azure.ai.agents.persistent.models.MessageImageFileContent;
import com.azure.ai.agents.persistent.models.MessageRole;
import com.azure.ai.agents.persistent.models.MessageTextContent;
import com.azure.ai.agents.persistent.models.PersistentAgent;
import com.azure.ai.agents.persistent.models.PersistentAgentThread;
import com.azure.ai.agents.persistent.models.RequiredFunctionToolCall;
import com.azure.ai.agents.persistent.models.RequiredToolCall;
import com.azure.ai.agents.persistent.models.RunStatus;
import com.azure.ai.agents.persistent.models.SubmitToolOutputsAction;
import com.azure.ai.agents.persistent.models.ThreadMessage;
import com.azure.ai.agents.persistent.models.ThreadRun;
import com.azure.ai.agents.persistent.models.ToolOutput;
import com.azure.ai.agents.persistent.models.MessageContent;
import com.azure.core.http.rest.PagedIterable;
import com.azure.core.util.BinaryData;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.json.JsonMapper;

import java.net.URL;
import java.io.File;
import java.io.FileNotFoundException;
import java.net.URISyntaxException;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.function.Function;

public class AgentExample {

    public static void main(String[] args) throws FileNotFoundException, URISyntaxException {

        // variables for authenticating requests to the agent service 
        String projectEndpoint = System.getenv("PROJECT_ENDPOINT");
        String modelName = System.getenv("MODEL_DEPLOYMENT_NAME");
        
        PersistentAgentsClientBuilder clientBuilder = new PersistentAgentsClientBuilder().endpoint(projectEndpoint)
            .credential(new DefaultAzureCredentialBuilder().build());
        PersistentAgentsClient agentsClient = clientBuilder.buildClient();
        PersistentAgentsAdministrationClient administrationClient = agentsClient.getPersistentAgentsAdministrationClient();
        ThreadsClient threadsClient = agentsClient.getThreadsClient();
        MessagesClient messagesClient = agentsClient.getMessagesClient();
        RunsClient runsClient = agentsClient.getRunsClient();

        Supplier<String> getUserFavoriteCity = () -> "Seattle, WA";
        FunctionToolDefinition getUserFavoriteCityTool = new FunctionToolDefinition(
            new FunctionDefinition(
                "getUserFavoriteCity",
                BinaryData.fromObject(
                    new Object()
                ))
        );

        Function<String, String> getCityNickname = location -> {
            return "The Emerald City";
        };

        FunctionToolDefinition getCityNicknameTool = new FunctionToolDefinition(
            new FunctionDefinition(
                "getCityNickname",
                BinaryData.fromObject(
                    mapOf(
                        "type", "object",
                        "properties", mapOf(
                            "location",
                            mapOf(
                                "type", "string",
                                "description", "The city and state, e.g. San Francisco, CA")
                        ),
                        "required", new String[]{"location"}))
            ).setDescription("Get the nickname of a city")
        );

        Function<RequiredToolCall, ToolOutput> getResolvedToolOutput = toolCall -> {
            if (toolCall instanceof RequiredFunctionToolCall) {
                RequiredFunctionToolCall functionToolCall = (RequiredFunctionToolCall) toolCall;
                String functionName = functionToolCall.getFunction().getName();
                if (functionName.equals("getUserFavoriteCity")) {
                    return new ToolOutput().setToolCallId(functionToolCall.getId())
                        .setOutput(getUserFavoriteCity.get());
                } else if (functionName.equals("getCityNickname")) {
                    String arguments = functionToolCall.getFunction().getArguments();
                    try {
                        JsonNode root = new JsonMapper().readTree(arguments);
                        String location = String.valueOf(root.get("location").asText());
                        return new ToolOutput().setToolCallId(functionToolCall.getId())
                            .setOutput(getCityNickname.apply(location));
                    } catch (JsonProcessingException e) {
                        throw new RuntimeException(e);
                    }
                }
            }
            return null;
        };

        String agentName = "functions_example";
        CreateAgentOptions createAgentOptions = new CreateAgentOptions(modelName)
            .setName(agentName)
            .setInstructions("You are a weather bot. Use the provided functions to help answer questions. "
                + "Customize your responses to the user's preferences as much as possible and use friendly "
                + "nicknames for cities whenever possible.")
            .setTools(Arrays.asList(getUserFavoriteCityTool, getCityNicknameTool));
        PersistentAgent agent = administrationClient.createAgent(createAgentOptions);

        PersistentAgentThread thread = threadsClient.createThread();
        ThreadMessage createdMessage = messagesClient.createMessage(
            thread.getId(),
            MessageRole.USER,
            "What's the nickname of my favorite city?");

        try {
            //run agent
            CreateRunOptions createRunOptions = new CreateRunOptions(thread.getId(), agent.getId())
                .setAdditionalInstructions("");
            ThreadRun threadRun = runsClient.createRun(createRunOptions);

            do {
                Thread.sleep(500);
                threadRun = runsClient.getRun(thread.getId(), threadRun.getId());
                if (threadRun.getStatus() == RunStatus.REQUIRES_ACTION
                    && threadRun.getRequiredAction() instanceof SubmitToolOutputsAction) {
                    SubmitToolOutputsAction submitToolsOutputAction = (SubmitToolOutputsAction) (threadRun.getRequiredAction());
                    ArrayList<ToolOutput> toolOutputs = new ArrayList<ToolOutput>();
                    for (RequiredToolCall toolCall : submitToolsOutputAction.getSubmitToolOutputs().getToolCalls()) {
                        toolOutputs.add(getResolvedToolOutput.apply(toolCall));
                    }
                    threadRun = runsClient.submitToolOutputsToRun(thread.getId(), threadRun.getId(), toolOutputs);
                }
            }
            while (
                threadRun.getStatus() == RunStatus.QUEUED
                    || threadRun.getStatus() == RunStatus.IN_PROGRESS
                    || threadRun.getStatus() == RunStatus.REQUIRES_ACTION);

            if (threadRun.getStatus() == RunStatus.FAILED) {
                System.out.println(threadRun.getLastError().getMessage());
            }

            printRunMessages(messagesClient, thread.getId());
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        } finally {
            //cleanup
            threadsClient.deleteThread(thread.getId());
            administrationClient.deleteAgent(agent.getId());
        }
    }

    // Use "Map.of" if available
    @SuppressWarnings("unchecked")
    private static <T> Map<String, T> mapOf(Object... inputs) {
        Map<String, T> map = new HashMap<>();
        for (int i = 0; i < inputs.length; i += 2) {
            String key = (String) inputs[i];
            T value = (T) inputs[i + 1];
            map.put(key, value);
        }
        return map;
    }
    // A helper function to print messages from the agent
    public static void printRunMessages(MessagesClient messagesClient, String threadId) {

        PagedIterable<ThreadMessage> runMessages = messagesClient.listMessages(threadId);
        for (ThreadMessage message : runMessages) {
            System.out.print(String.format("%1$s - %2$s : ", message.getCreatedAt(), message.getRole()));
            for (MessageContent contentItem : message.getContent()) {
                if (contentItem instanceof MessageTextContent) {
                    System.out.print((((MessageTextContent) contentItem).getText().getValue()));
                } else if (contentItem instanceof MessageImageFileContent) {
                    String imageFileId = (((MessageImageFileContent) contentItem).getImageFile().getFileId());
                    System.out.print("Image from ID: " + imageFileId);
                }
                System.out.println();
            }
        }
    }

    // a helper function to wait until a run has completed running
    public static void waitForRunCompletion(String threadId, ThreadRun threadRun, RunsClient runsClient)
        throws InterruptedException {

        do {
            Thread.sleep(500);
            threadRun = runsClient.getRun(threadId, threadRun.getId());
        }
        while (
            threadRun.getStatus() == RunStatus.QUEUED
                || threadRun.getStatus() == RunStatus.IN_PROGRESS
                || threadRun.getStatus() == RunStatus.REQUIRES_ACTION);

        if (threadRun.getStatus() == RunStatus.FAILED) {
            System.out.println(threadRun.getLastError().getMessage());
        }
    }
    private static Path getFile(String fileName) throws FileNotFoundException, URISyntaxException {
        URL resource = AgentExample.class.getClassLoader().getResource(fileName);
        if (resource == null) {
            throw new FileNotFoundException("File not found");
        }
        File file = new File(resource.toURI());
        return file.toPath();
    }
    @FunctionalInterface
    public interface Supplier<T> extends java.util.function.Supplier<T> {
    /**
     * Retrieves an instance of the appropriate type. The returned object may or may not be a new
     * instance, depending on the implementation.
     *
     * @return an instance of the appropriate type
     */
    @Override
    T get();
    }
}
```
::: zone-end
