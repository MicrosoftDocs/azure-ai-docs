---
title: Use function calling with agent API
titleSuffix: Microsoft Foundry
description: Learn how to use function calling with Microsoft Foundry agent API. Includes code examples in Python, C#, and REST API to define and execute functions.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 12/16/2025
author: alvinashcraft
ms.author: aashcraft
ms.custom: azure-ai-agents, dev-focus
ai-usage: ai-assisted
zone_pivot_groups: selection-function-calling-new
---

# Function calling for agents

Microsoft Foundry agents support function calling. By using function calling, you can describe the structure of functions to an agent. The agent can then return the functions that need to be called along with their arguments.

> [!NOTE]
> - Runs expire 10 minutes after creation. Be sure to submit your tool outputs before the expiration.
> - Although the Microsoft Foundry portal doesn't support function calling, agents appear in the portal after creation. Agents that run in the portal don't perform function calling.

### Usage support

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|---------|
| ✔️ | ✔️ | ✔️ | - | - | ✔️ | ✔️ | ✔️ |

## Example agent code

> [!NOTE]
> You need the latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#install-and-authenticate) for details.

:::zone pivot="python"

Use the following code sample to create an agent and call the function. You need the latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#install-and-authenticate) for details.

```python
import os
import json
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, Tool, FunctionTool
from azure.identity import DefaultAzureCredential
from openai.types.responses.response_input_param import FunctionCallOutput, ResponseInputParam

load_dotenv()

# Define a function tool for the model to use
func_tool = FunctionTool(
    name="get_horoscope",
    parameters={
        "type": "object",
        "properties": {
            "sign": {
                "type": "string",
                "description": "An astrological sign like Taurus or Aquarius",
            },
        },
        "required": ["sign"],
        "additionalProperties": False,
    },
    description="Get today's horoscope for an astrological sign.",
    strict=True,
)

tools: list[Tool] = [func_tool]


def get_horoscope(sign: str) -> str:
    """Generate a horoscope for the given astrological sign."""
    return f"{sign}: Next Tuesday you will befriend a baby otter."


project_client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)


with project_client:

    agent = project_client.agents.create_version(
        agent_name="MyAgent",
        definition=PromptAgentDefinition(
            model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
            instructions="You are a helpful assistant that can use function tools.",
            tools=tools,
        ),
    )

    openai_client = project_client.get_openai_client()

    # Prompt the model with tools defined
    response = openai_client.responses.create(
        input="What is my horoscope? I am an Aquarius.",
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )
    print(f"Response output: {response.output_text}")

    input_list: ResponseInputParam = []
    # Process function calls
    for item in response.output:
        if item.type == "function_call":
            if item.name == "get_horoscope":
                # Execute the function logic for get_horoscope
                horoscope = get_horoscope(**json.loads(item.arguments))

                # Provide function call results to the model
                input_list.append(
                    FunctionCallOutput(
                        type="function_call_output",
                        call_id=item.call_id,
                        output=json.dumps({"horoscope": horoscope}),
                    )
                )

    print("Final input:")
    print(input_list)

    response = openai_client.responses.create(
        input=input_list,
        previous_response_id=response.id,
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )
```

### Expected output

The following example shows the expected output:

```console
Response output: 
Final input:
[FunctionCallOutput(type='function_call_output', call_id='call_abc123', output='{"horoscope": "Aquarius: Next Tuesday you will befriend a baby otter."}')]
```

:::zone-end

:::zone pivot="csharp"
## Use agents with functions example

In this example, you use local functions with agents. Use the functions to give the Agent specific information in response to a user question. The code in this example is synchronous. For an asynchronous example, see the [sample code](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample9_Function.md) example in the Azure SDK for .NET repository on GitHub.

```csharp
// Create project client and read the environment variables that will be used in the next steps.
var projectEndpoint = System.Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("MODEL_DEPLOYMENT_NAME");
AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

// Define three functions:
//   1. GetUserFavoriteCity always returns "Seattle, WA".
//   2. GetCityNickname handles only "Seattle, WA"
//      and throws an exception for other city names.
//   3. GetWeatherAtLocation returns the weather in Seattle, WA.

/// Example of a function that defines no parameters but
/// returns the user's favorite city.
private static string GetUserFavoriteCity() => "Seattle, WA";

/// <summary>
/// Example of a function with a single required parameter
/// </summary>
/// <param name="location">The location to get nickname for.</param>
/// <returns>The city nickname.</returns>
/// <exception cref="NotImplementedException"></exception>
private static string GetCityNickname(string location) => location switch
{
    "Seattle, WA" => "The Emerald City",
    _ => throw new NotImplementedException(),
};

/// <summary>
/// Example of a function with one required and one optional, enum parameter
/// </summary>
/// <param name="location">Get weather for location.</param>
/// <param name="temperatureUnit">"c" or "f"</param>
/// <returns>The weather in selected location.</returns>
/// <exception cref="NotImplementedException"></exception>
public static string GetWeatherAtLocation(string location, string temperatureUnit = "f") => location switch
{
    "Seattle, WA" => temperatureUnit == "f" ? "70f" : "21c",
    _ => throw new NotImplementedException()
};

// For each function, create FunctionTool, which defines the function name, description, and parameters.
public static readonly FunctionTool getUserFavoriteCityTool = ResponseTool.CreateFunctionTool(
    functionName: "getUserFavoriteCity",
    functionDescription: "Gets the user's favorite city.",
    functionParameters: BinaryData.FromString("{}"),
    strictModeEnabled: false
);

public static readonly FunctionTool getCityNicknameTool = ResponseTool.CreateFunctionTool(
    functionName: "getCityNickname",
    functionDescription: "Gets the nickname of a city, e.g. 'LA' for 'Los Angeles, CA'.",
    functionParameters: BinaryData.FromObjectAsJson(
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
        new JsonSerializerOptions() { PropertyNamingPolicy = JsonNamingPolicy.CamelCase }
    ),
    strictModeEnabled: false
);

private static readonly FunctionTool getCurrentWeatherAtLocationTool = ResponseTool.CreateFunctionTool(
    functionName: "getCurrentWeatherAtLocation",
    functionDescription: "Gets the current weather at a provided location.",
    functionParameters: BinaryData.FromObjectAsJson(
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
        new JsonSerializerOptions() { PropertyNamingPolicy = JsonNamingPolicy.CamelCase }
    ),
    strictModeEnabled: false
);

// Create the method GetResolvedToolOutput.
// It runs the preceding functions and wraps the output in a ResponseItem object.
private static FunctionCallOutputResponseItem GetResolvedToolOutput(FunctionCallResponseItem item)
{
    if (item.FunctionName == getUserFavoriteCityTool.FunctionName)
    {
        return ResponseItem.CreateFunctionCallOutputItem(item.CallId, GetUserFavoriteCity());
    }
    using JsonDocument argumentsJson = JsonDocument.Parse(item.FunctionArguments);
    if (item.FunctionName == getCityNicknameTool.FunctionName)
    {
        string locationArgument = argumentsJson.RootElement.GetProperty("location").GetString();
        return ResponseItem.CreateFunctionCallOutputItem(item.CallId, GetCityNickname(locationArgument));
    }
    if (item.FunctionName == getCurrentWeatherAtLocationTool.FunctionName)
    {
        string locationArgument = argumentsJson.RootElement.GetProperty("location").GetString();
        if (argumentsJson.RootElement.TryGetProperty("unit", out JsonElement unitElement))
        {
            string unitArgument = unitElement.GetString();
            return ResponseItem.CreateFunctionCallOutputItem(item.CallId, GetWeatherAtLocation(locationArgument, unitArgument));
        }
        return ResponseItem.CreateFunctionCallOutputItem(item.CallId, GetWeatherAtLocation(locationArgument));
    }
    return null;
}

// Create an agent version with the defined functions as tools.
PromptAgentDefinition agentDefinition = new(model: modelDeploymentName)
{
    Instructions = "You are a weather bot. Use the provided functions to help answer questions. "
            + "Customize your responses to the user's preferences as much as possible and use friendly "
            + "nicknames for cities whenever possible.",
    Tools = { getUserFavoriteCityTool, getCityNicknameTool, getCurrentWeatherAtLocationTool }
};
AgentVersion agentVersion = projectClient.Agents.CreateAgentVersion(
    agentName: "myAgent",
    options: new(agentDefinition));

// Responses must be obtained multiple times to supply function outputs.
// Method CreateAndCheckResponse is defined for brevity.
public static ResponseResult CreateAndCheckResponse(ResponsesClient responseClient, IEnumerable<ResponseItem> items)
{
    ResponseResult response = responseClient.CreateResponse(
        inputItems: items);
    Assert.That(response.Status, Is.EqualTo(ResponseStatus.Completed));
    return response;
}

// If the local function call is required, the response item is of type FunctionCallResponseItem.
// It contains the function name needed by the Agent. In this case, use the helper method
// GetResolvedToolOutput to get the FunctionCallOutputResponseItem with the function call result.
// To provide the right answer, supply all the response items to the CreateResponse call.
// At the end, output the function's response.
ResponsesClient responseClient = projectClient.OpenAI.GetProjectResponsesClientForAgent(agentVersion.Name);

ResponseItem request = ResponseItem.CreateUserMessageItem("What's the weather like in my favorite city?");
List<ResponseItem> inputItems = [request];
bool funcionCalled = false;
ResponseResult response;
do
{
    response = CreateAndCheckResponse(
        responseClient,
        inputItems);
    funcionCalled = false;
    foreach (ResponseItem responseItem in response.OutputItems)
    {
        inputItems.Add(responseItem);
        if (responseItem is FunctionCallResponseItem functionToolCall)
        {
            Console.WriteLine($"Calling {functionToolCall.FunctionName}...");
            inputItems.Add(GetResolvedToolOutput(functionToolCall));
            funcionCalled = true;
        }
    }
} while (funcionCalled);
Console.WriteLine(response.GetOutputText());

// Remove all the resources created in this sample.
projectClient.Agents.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

### Expected output

The following example shows the expected output:

```console
Calling getUserFavoriteCity...
Calling getCityNickname...
Calling getCurrentWeatherAtLocation...
Your favorite city, Seattle, WA, is also known as The Emerald City. The current weather there is 70f.
```
:::zone-end

:::zone pivot="rest"
There are two ways to use function calling in Foundry Agent Service.

1. You can create just `response` and when you need the agent to call this function again, you can create another `response`.
1. You can create on `conversation` and within this conversation, you can create multiple `conversation items`. Each conversation item corresponds to one `response`. You can organize your responses and function calling more consistently.

## Define a function for your agent to call

Start by defining a function for your agent to call. When you create a function for an agent to call, describe its structure and any required parameters in a docstring. For example functions, see the other SDK languages.

## Create an agent version

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/agents/$AGENTVERSION_NAME/versions?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Test agent version with code interpreter tool",
    "metadata": { "env": "test", "owner": "user" },
    "definition": {
      "kind": "prompt",
      "model": {{model}},
      "instructions": "You are a helpful agent.",
      "tools": [
        {
          "type": "function",
          "name": "getCurrentWeather",
          "description": "Get the current weather in a location",
          "parameters": {
            "type": "object",
            "properties": {
              "location": {"type": "string", "description": "The city and state e.g. San Francisco, CA"},
              "unit": {"type": "string", "enum": ["c", "f"]}
            },
            "required": ["location"]
          }
        }
      ]
    }
  }'
```

## Create a conversation

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/openai/conversations?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d ''
```

## Create a response

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/openai/responses?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": {{model}},
    "conversation": {{conversation.id}},
    "input": [{
        "type": "message",
        "role": "user",
        "content": [
            {
                "type": "input_text",
                "text": "What's the weather in Dar es Salaam, Tanzania?"
            }
        ]
    }],
    "tools": [
      {
        "type": "function",
        "name": "getCurrentWeather",
        "description": "Get the current weather in a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {"type": "string", "description": "The city and state e.g. San Francisco, CA"},
            "unit": {"type": "string", "enum": ["c", "f"]}
          },
          "required": ["location"]
        }
      }
    ],
    "stream": true
  }
'
```

### Expected output

The response contains a function call item that you need to process:

```json
{
  "output": [
    {
      "type": "function_call",
      "call_id": "call_xyz789",
      "name": "getCurrentWeather",
      "arguments": "{\"location\": \"Dar es Salaam, Tanzania\", \"unit\": \"c\"}"
    }
  ]
}
```

After you process the function call and provide the output back to the agent, the final response includes the weather information in natural language.

::: zone-end
