---
title: "Use function calling with Microsoft Foundry agents"
description: "Use function calling to extend Microsoft Foundry agents with custom functions. Define tools with Python, C#, TypeScript, or REST and return outputs to the agent."
services: cognitive-services
manager: nitinme
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 03/30/2026
author: alvinashcraft
ms.author: aashcraft
ms.custom: azure-ai-agents, dev-focus, pilot-ai-workflow-jan-2026, doc-kit-assisted
ai-usage: ai-assisted
zone_pivot_groups: selection-function-calling-new
---

# Use function calling with Microsoft Foundry agents
Microsoft Foundry agents support function calling, which lets you extend agents with custom capabilities. Define a function with its name, parameters, and description, and the agent can request your app to call it. Your app executes the function and returns the output. The agent then uses the result to continue the conversation with accurate, real-time data from your systems.

> [!IMPORTANT]
> Runs expire 10 minutes after creation. Submit your tool outputs before they expire.

You can run agents with function tools in the Microsoft Foundry portal. However, the portal doesn't support adding, removing, or updating function definitions on an agent. Use the SDK or REST API to configure function tools.

## Usage support

The following table shows SDK and setup support.

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

Before you start, make sure you have:

- A [basic or standard agent environment](../../../agents/environment-setup.md).
- A Foundry project and a deployed model.
- The SDK package for your language:
  - Python: `azure-ai-projects` (latest)
  - .NET: `Azure.AI.Extensions.OpenAI`
  - TypeScript: `@azure/ai-projects` (latest)
  - Java: `azure-ai-agents`
  
  For installation and authentication steps, see the [quickstart](../../../quickstarts/get-started-code.md).

> [!TIP]
> If you use `DefaultAzureCredential`, sign in by using `az login` before running the samples.

## Create an agent with function tools

Function calling follows this pattern:

1. **Define function tools** — Describe each function's name, parameters, and purpose.
1. **Create an agent** — Register the agent with your function definitions.
1. **Send a prompt** — The agent analyzes the prompt and requests function calls if needed.
1. **Execute and return** — Your app runs the function and submits the output back to the agent.
1. **Get the final response** — The agent uses your function output to complete its response.

:::zone pivot="python"

Use the following code sample to create an agent, handle a function call, and return tool output back to the agent.

```python
import json
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, Tool, FunctionTool
from azure.identity import DefaultAzureCredential
from openai.types.responses.response_input_param import FunctionCallOutput, ResponseInputParam

def get_horoscope(sign: str) -> str:
    """Generate a horoscope for the given astrological sign."""
    return f"{sign}: Next Tuesday you will befriend a baby otter."

# Format: "https://resource_name.ai.azure.com/api/projects/project_name"
PROJECT_ENDPOINT = "your_project_endpoint"

project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()

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

agent = project.agents.create_version(
    agent_name="MyAgent",
    definition=PromptAgentDefinition(
        model="gpt-4.1-mini",
        instructions="You are a helpful assistant that can use function tools.",
        tools=tools,
    ),
)

# Prompt the model with tools defined
response = openai.responses.create(
    input="What is my horoscope? I am an Aquarius.",
    extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
)

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

# Submit function results and get the final response
response = openai.responses.create(
    input=input_list,
    previous_response_id=response.id,
    extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
)

print(f"Agent response: {response.output_text}")

# Clean up resources
project.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
```

### Expected output

The following example shows the expected output:

```console
Agent response: Your horoscope for Aquarius: Next Tuesday you will befriend a baby otter.
```

:::zone-end

:::zone pivot="csharp"
## Use agents with functions example

In this example, you use local functions with agents. Use the functions to give the Agent specific information in response to a user question. The code in this example is synchronous. For an asynchronous example, see the [sample code](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Extensions.OpenAI/samples/Sample9_Function.md) example in the Azure SDK for .NET repository on GitHub.

```csharp
using System;
using Azure.AI.Projects;
using Azure.AI.Extensions.OpenAI;
using Azure.Identity;

class FunctionCallingDemo
{
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

    // Format: "https://resource_name.ai.azure.com/api/projects/project_name"
    private const string ProjectEndpoint = "your_project_endpoint";

    public static void Main() 
    {
        AIProjectClient projectClient = new(endpoint: new Uri(ProjectEndpoint), tokenProvider: new DefaultAzureCredential());
        // Create an agent version with the defined functions as tools.
        DeclarativeAgentDefinition agentDefinition = new(model: "gpt-4.1-mini")
        {
            Instructions = "You are a weather bot. Use the provided functions to help answer questions. "
                    + "Customize your responses to the user's preferences as much as possible and use friendly "
                    + "nicknames for cities whenever possible.",
            Tools = { getUserFavoriteCityTool, getCityNicknameTool, getCurrentWeatherAtLocationTool }
        };
        AgentVersion agentVersion = projectClient.AgentAdministrationClient.CreateAgentVersion(
            agentName: "myAgent",
            options: new(agentDefinition));

        // If the local function call is required, the response item is of type FunctionCallResponseItem.
        // It contains the function name needed by the Agent. In this case, use the helper method
        // GetResolvedToolOutput to get the FunctionCallOutputResponseItem with the function call result.
        // To provide the right answer, supply all the response items to the CreateResponse call.
        // At the end, output the function's response.
        ResponsesClient responseClient = projectClient.ProjectOpenAIClient.GetProjectResponsesClientForAgent(agentVersion.Name);

        ResponseItem request = ResponseItem.CreateUserMessageItem("What's the weather like in my favorite city?");
        var inputItems = new List<ResponseItem> { request };
        string previousResponseId = null;
        bool functionCalled = false;
        ResponseResult response;
        do
        {
            response = responseClient.CreateResponse(
                previousResponseId: previousResponseId,
                inputItems: inputItems);
            previousResponseId = response.Id;
            inputItems.Clear();
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
        projectClient.AgentAdministrationClient.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
    }
}
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
export AGENT_TOKEN=$(az account get-access-token --scope "https://ai.azure.com/.default" --query accessToken -o tsv)
```

## Define a function for your agent to call

Start by defining a function for your agent to call. When you create a function for an agent to call, describe its structure and any required parameters in a docstring. For example functions, see the other SDK languages.

## Create an agent

```bash
curl -X POST "$FOUNDRY_PROJECT_ENDPOINT/agents?api-version=v1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -d '{
    "name": "<AGENT_NAME>-function-calling",
    "description": "Agent with function calling",
    "definition": {
      "kind": "prompt",
      "model": "<MODEL_DEPLOYMENT>",
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
curl -X POST "$FOUNDRY_PROJECT_ENDPOINT/openai/v1/conversations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -d '{
    "items": [
      {
        "type": "message",
        "role": "user",
        "content": [
          {
            "type": "input_text",
            "text": "What'\''s the weather in Dar es Salaam, Tanzania?"
          }
        ]
      }
    ]
  }'
```

Save the returned conversation ID (`conv_xyz...`) for the next step.

## Create a response

Replace `<CONVERSATION_ID>` with the ID from the previous step.

```bash
curl -X POST "$FOUNDRY_PROJECT_ENDPOINT/openai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -d '{
    "agent": {"type": "agent_reference", "name": "<AGENT_NAME>-function-calling"},
    "conversation": "<CONVERSATION_ID>",
    "input": []
  }'
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

### Submit function call output

After processing the function call locally, submit the result back to the agent:

```bash
curl -X POST "$FOUNDRY_PROJECT_ENDPOINT/openai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -d '{
    "agent": {"type": "agent_reference", "name": "<AGENT_NAME>-function-calling"},
    "conversation": "<CONVERSATION_ID>",
    "input": [
      {
        "type": "function_call_output",
        "call_id": "<CALL_ID>",
        "output": "{\"temperature\": \"30\", \"unit\": \"c\", \"description\": \"Sunny\"}"
      }
    ]
  }'
```

Replace `<CALL_ID>` with the `call_id` value from the function call in the previous response. The agent uses the function output to generate a natural language answer.

:::zone-end

:::zone pivot="typescript"

Use the following code sample to create an agent with function tools, handle function calls from the model, and provide function results to get the final response.

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";

// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
const projectEndpoint = "your_project_endpoint";

/**
 * Define a function tool for the model to use
 */
const funcTool = {
  type: "function" as const,
  name: "get_horoscope",
  description: "Get today's horoscope for an astrological sign.",
  strict: true,
  parameters: {
    type: "object",
    properties: {
      sign: {
        type: "string",
        description: "An astrological sign like Taurus or Aquarius",
      },
    },
    required: ["sign"],
    additionalProperties: false,
  },
};

/**
 * Generate a horoscope for the given astrological sign.
 */
function getHoroscope(sign: string): string {
  return `${sign}: Next Tuesday you will befriend a baby otter.`;
}

export async function main(): Promise<void> {
  // Create AI Project client
  const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());
  const openai = project.getOpenAIClient();

  // Create agent with function tools
  const agent = await project.agents.createVersion("function-tool-agent", {
    kind: "prompt",
    model: "gpt-4.1-mini",
    instructions: "You are a helpful assistant that can use function tools.",
    tools: [funcTool],
  });

  // Prompt the model with tools defined
  const response = await openai.responses.create(
    {
      input: [
        {
          type: "message",
          role: "user",
          content: "What is my horoscope? I am an Aquarius.",
        },
      ],
    },
    {
      body: { agent: { name: agent.name, type: "agent_reference" } },
    },
  );
  console.log(`Response output: ${response.output_text}`);

  // Process function calls
  const inputList: Array<{
    type: "function_call_output";
    call_id: string;
    output: string;
  }> = [];

  for (const item of response.output) {
    if (item.type === "function_call") {
      if (item.name === "get_horoscope") {
        // Parse the function arguments
        const args = JSON.parse(item.arguments);

        // Execute the function logic for get_horoscope
        const horoscope = getHoroscope(args.sign);

        // Provide function call results to the model
        inputList.push({
          type: "function_call_output",
          call_id: item.call_id,
          output: JSON.stringify({ horoscope }),
        });
      }
    }
  }

  // Submit function results to get final response
  const finalResponse = await openai.responses.create(
    {
      input: inputList,
      previous_response_id: response.id,
    },
    {
      body: { agent: { name: agent.name, type: "agent_reference" } },
    },
  );

  // Print the final response
  console.log(finalResponse.output_text);

  // Clean up
  await project.agents.deleteVersion(agent.name, agent.version);
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

### Expected output

The following example shows the expected output:

```console
Response output: 
Your horoscope for Aquarius: Next Tuesday you will befriend a baby otter.
```

:::zone-end

:::zone pivot="java"

## Use function calling in a Java agent

### Set up

Add the dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-agents</artifactId>
    <version>2.0.0</version>
</dependency>
```

### Create an agent with function tools

```java
import com.azure.ai.agents.AgentsClient;
import com.azure.ai.agents.AgentsClientBuilder;
import com.azure.ai.agents.ResponsesClient;
import com.azure.ai.agents.models.AgentReference;
import com.azure.ai.agents.models.AgentVersionDetails;
import com.azure.ai.agents.models.AzureCreateResponseOptions;
import com.azure.ai.agents.models.FunctionTool;
import com.azure.ai.agents.models.PromptAgentDefinition;
import com.azure.core.util.BinaryData;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class FunctionCallingExample {
    // Format: "https://resource_name.ai.azure.com/api/projects/project_name"
    private static final String PROJECT_ENDPOINT = "your_project_endpoint";

    public static void main(String[] args) {
        AgentsClientBuilder builder = new AgentsClientBuilder()
            .credential(new DefaultAzureCredentialBuilder().build())
            .endpoint(PROJECT_ENDPOINT);

        AgentsClient agentsClient = builder.buildAgentsClient();
        ResponsesClient responsesClient = builder.buildResponsesClient();

        // Define function parameters
        Map<String, BinaryData> parameters = new HashMap<>();
        parameters.put("type", BinaryData.fromString("\"object\""));
        parameters.put("properties", BinaryData.fromString(
            "{\"location\":{\"type\":\"string\",\"description\":\"The city and state, e.g. Seattle, WA\"},"
            + "\"unit\":{\"type\":\"string\",\"enum\":[\"celsius\",\"fahrenheit\"]}}"));
        parameters.put("required", BinaryData.fromString("[\"location\"]"));

        FunctionTool weatherFunction = new FunctionTool("get_weather", parameters, true);

        // Create agent with function tool
        PromptAgentDefinition agentDefinition = new PromptAgentDefinition("gpt-4.1-mini")
            .setInstructions("You are a weather assistant. Use the get_weather function to retrieve weather information.")
            .setTools(Arrays.asList(weatherFunction));

        AgentVersionDetails agent = agentsClient.createAgentVersion("function-calling-agent", agentDefinition);
        System.out.printf("Agent created: %s (version %s)%n", agent.getName(), agent.getVersion());

        // Create a response - the agent will call the function
        AgentReference agentReference = new AgentReference(agent.getName())
            .setVersion(agent.getVersion());

        Response response = responsesClient.createAzureResponse(
            new AzureCreateResponseOptions().setAgentReference(agentReference),
            ResponseCreateParams.builder()
                .input("What is the weather in Seattle?"));

        System.out.println("Response: " + response.output());

        // Clean up
        agentsClient.deleteAgentVersion(agent.getName(), agent.getVersion());
    }
}
```

For the complete function calling loop that handles the tool call and submits results back to the agent, see the [Azure AI Agents Java SDK samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/ai/azure-ai-agents/src/samples/).

:::zone-end

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
| Arguments aren't valid JSON. | Schema mismatch or model generated incorrect information. | Verify JSON schema uses correct types and required properties. Handle parsing errors gracefully in your app. |
| Required fields are missing. | Schema doesn't enforce required properties. | Add `"required": [...]` array to your parameter schema. Set `strict: true` for stricter validation. |
| Tool outputs fail due to expiration. | Run expired (10-minute limit). | Return tool outputs promptly. For slow operations, return a status and poll separately. |
| Function called with wrong parameters. | Ambiguous function description. | Improve the function `description` field. Add detailed parameter descriptions with examples. |
| Multiple function calls in one response. | Model determined multiple functions needed. | Handle each function call in the output array. Return all results in a single `responses.create` call. |
| Function not visible in Foundry portal. | Portal doesn't execute function calls. | Test function calling via SDK or REST API. The portal shows agents but doesn't invoke functions. |

## Clean up resources

When you finish testing, delete the resources you created to avoid ongoing costs.

Delete the agent:

```bash
curl -X DELETE "$FOUNDRY_PROJECT_ENDPOINT/agents/<AGENT_NAME>-function-calling?api-version=v1" \
  -H "Authorization: Bearer $AGENT_TOKEN"
```

Delete the conversation:

```bash
curl -X DELETE "$FOUNDRY_PROJECT_ENDPOINT/openai/v1/conversations/<CONVERSATION_ID>" \
  -H "Authorization: Bearer $AGENT_TOKEN"
```

## Related content

- [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md)
- [Connect OpenAPI tools to Microsoft Foundry agents](openapi.md)
- [Microsoft Foundry Quickstart](../../../quickstarts/get-started-code.md)
