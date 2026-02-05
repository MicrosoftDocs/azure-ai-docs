---
title: Use function calling with Microsoft Foundry agents
titleSuffix: Microsoft Foundry
description: Use function calling to extend Microsoft Foundry agents with custom functions. Define tools with Python, C#, or REST and return outputs to the agent.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 02/05/2026
author: alvinashcraft
ms.author: aashcraft
ms.custom: azure-ai-agents, dev-focus, pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
zone_pivot_groups: selection-function-calling-new
---

# Use function calling with Microsoft Foundry agents

Microsoft Foundry agents support function calling, which lets you extend agents with custom capabilities. Define a function with its name, parameters, and description, and the agent can request your app to call it. Your app executes the function and returns the output. The agent then uses the result to continue the conversation with accurate, real-time data from your systems.

> [!IMPORTANT]
> Runs expire 10 minutes after creation. Submit your tool outputs before they expire.

You can run agents with function tools in the Microsoft Foundry portal. However, the portal doesn't support adding, removing, or updating function definitions on an agent. Use the SDK or REST API to configure function tools.

## Usage support

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ✔️ | ✔️ | ✔️ | - | - | ✔️ | ✔️ | ✔️ |

## Prerequisites

Before you start, make sure you have:

- A [basic or standard agent environment](../../../../agents/environment-setup.md).
- A Foundry project and a deployed model.
- The latest prerelease SDK package for your language (`azure-ai-projects>=2.0.0b1` for Python, `Azure.AI.Projects.OpenAI` prerelease for .NET). For installation and authentication steps, see the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true).

### Environment variables

Each language uses different environment variable names. Use one set consistently.

| Language | Project endpoint | Model deployment name |
| --- | --- | --- |
| Python | `AZURE_AI_PROJECT_ENDPOINT` | `AZURE_AI_MODEL_DEPLOYMENT_NAME` |
| C# | `FOUNDRY_PROJECT_ENDPOINT` | `MODEL_DEPLOYMENT_NAME` |
| REST API | `AZURE_AI_FOUNDRY_PROJECT_ENDPOINT` | (use the request body field) |

> [!TIP]
> If you use `DefaultAzureCredential`, sign in by using `az login` before running the samples.

### Quick verification

If you're not sure your authentication and endpoint are set up correctly, run the following snippet first.

```python
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"], credential=credential) as project_client,
):
    print("Connected to project.")
```

## Create an agent with function tools

Function calling follows this pattern:

1. **Define function tools** — Describe each function's name, parameters, and purpose.
1. **Create an agent** — Register the agent with your function definitions.
1. **Send a prompt** — The agent analyzes the prompt and requests function calls if needed.
1. **Execute and return** — Your app runs the function and submits the output back to the agent.
1. **Get the final response** — The agent uses your function output to complete its response.

> [!NOTE]
> You need the latest prerelease package. For more information, see the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#get-ready-to-code).

:::zone pivot="python"

Use the following code sample to create an agent, handle a function call, and return tool output back to the agent.

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
var inputItems = new List<ResponseItem> { request };
bool functionCalled = false;
ResponseResult response;
do
{
    response = CreateAndCheckResponse(
        responseClient,
        inputItems);
    functionCalled = false;
    foreach (ResponseItem responseItem in response.OutputItems)
    {
        inputItems.Add(responseItem);
        if (responseItem is FunctionCallResponseItem functionToolCall)
        {
            Console.WriteLine($"Calling {functionToolCall.FunctionName}...");
            inputItems.Add(GetResolvedToolOutput(functionToolCall));
            functionCalled = true;
        }
    }
} while (functionCalled);
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

1. Create a `response`. When you need the agent to call functions again, create another `response`.
1. Create a `conversation`, then create multiple conversation items. Each conversation item corresponds to one `response`.

Set the following environment variables before running the examples:

```bash
export AGENT_TOKEN=$(az account get-access-token --resource https://cognitiveservices.azure.com --query accessToken -o tsv)
export API_VERSION="2025-11-15-preview"
```

## Define a function for your agent to call

Start by defining a function for your agent to call. When you create a function for an agent to call, describe its structure and any required parameters in a docstring. For example functions, see the other SDK languages.

## Create an agent version

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/agents/$AGENTVERSION_NAME/versions?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
        "description": "Test agent version with function calling",
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

## Verify function calling works

Use these checks to confirm function calling is working:

1. Your first response contains an output item with `type` set to `function_call`.
1. Your app executes the requested function by using the returned arguments.
1. Your app submits a follow-up response that includes a `function_call_output` item and references the previous response, and the agent returns a natural-language answer.

If you use tracing in Microsoft Foundry, confirm the tool invocation occurred. For guidance on validating tool invocation and controlling tool usage, see [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md).

## Security and data considerations

- Treat tool arguments and tool outputs as untrusted input. Validate and sanitize values before using them.
- Don't pass secrets (API keys, tokens, connection strings) in tool output. Return only the data the model needs.
- Apply least privilege to the identity used by `DefaultAzureCredential`.
- Avoid side effects unless you explicitly intend them. For example, restrict function tools to safe operations, or require explicit user confirmation for actions that change data.
- For long-running operations, return a status immediately and implement polling. The 10-minute run expiration applies to total elapsed time, not individual function execution.

## Troubleshooting

| Issue | Likely cause | Resolution |
| --- | --- | --- |
| Agent returns function call but no final answer. | Tool output not returned to model. | Execute the function, then call `responses.create` with the tool output and `previous_response_id` to continue. |
| No function call occurs. | Function not in agent definition or poor naming. | Confirm the function tool is added to the agent. Use clear, descriptive names and parameter descriptions. |
| Arguments aren't valid JSON. | Schema mismatch or model hallucination. | Verify JSON schema uses correct types and required properties. Handle parsing errors gracefully in your app. |
| Required fields are missing. | Schema doesn't enforce required properties. | Add `"required": [...]` array to your parameter schema. Set `strict: true` for stricter validation. |
| Tool outputs fail due to expiration. | Run expired (10-minute limit). | Return tool outputs promptly. For slow operations, return a status and poll separately. |
| Function called with wrong parameters. | Ambiguous function description. | Improve the function `description` field. Add detailed parameter descriptions with examples. |
| Multiple function calls in one response. | Model determined multiple functions needed. | Handle each function call in the output array. Return all results in a single `responses.create` call. |
| Function not visible in Foundry portal. | Portal doesn't execute function calls. | Test function calling via SDK or REST API. The portal shows agents but doesn't invoke functions. |

## Clean up resources

When you finish testing, delete the resources you created to avoid ongoing costs:

- Delete the agent version.
- Delete conversations created for testing.

## Related content

- [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md)
- [Connect OpenAPI tools to Microsoft Foundry agents](openapi.md)
- [Microsoft Foundry Quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true)
