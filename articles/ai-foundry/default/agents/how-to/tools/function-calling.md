---
title: 'How to use function calling with the agent API'
titleSuffix: Microsoft Foundry
description: Learn how to use function calling with the agent API.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 12/05/2025
author: alvinashcraft
ms.author: aashcraft
ms.custom: azure-ai-agents
zone_pivot_groups: selection-function-calling-new
---

# Function calling for agents

Microsoft Foundry agents support function calling. With function calling, you can describe the structure of functions to an agent and then return the functions that need to be called along with their arguments.

> [!NOTE]
> - Runs expire 10 minutes after creation. Be sure to submit your tool outputs before the expiration.
> - Although function calling isn't supported in the Microsoft Foundry portal, agents appear in the portal after creation. Agents that run in the portal don't perform function calling.

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
:::zone-end

:::zone pivot="csharp"

For C# usage, see the [Sample using Agents with functions in Azure.AI.Projects.OpenAI](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample9_Function.md) example in the Azure SDK for .NET repository on GitHub.

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
::: zone-end
