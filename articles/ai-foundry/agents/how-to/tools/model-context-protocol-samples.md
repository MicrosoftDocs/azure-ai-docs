---
title: Code Samples for the Model Context Protocol Tool (Preview)
titleSuffix: Azure AI Foundry
description: Find code samples to connect Azure AI Foundry Agent Service with MCP servers.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 06/26/2025
author: aahill
ms.author: aahi
zone_pivot_groups: selection-mcp-code
ms.custom: azure-ai-agents-code
---

# Code samples for the Model Context Protocol tool (preview)

Use this article to find code samples for connecting Azure AI Foundry Agent Service with Model Context Protocol (MCP) servers.

Follow the [REST API quickstart](../../quickstart.md?pivots=rest-api#api-call-information) to set the right values for the environment variables `AGENT_TOKEN`, `AZURE_AI_FOUNDRY_PROJECT_ENDPOINT`, and `API_VERSION`.

## Create an agent with the MCP tool enabled

To make the MCP tool available to your agent, initialize a tool with the server endpoint, server label, and more:

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/assistants?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    "instructions": "You are a customer support chatbot. Use the tools provided and your knowledge base to best respond to customer queries.",
    "tools": [
          {
              "type": "mcp",
              "server_label": "<unique name for your MCP server>",
              "server_url": "<your MCP server URL>",
              "allowed_tools": ["<tool_name>"], # optional
          }
      ],
  "name": "my-assistant",
  "model": "gpt-4o",
}"
```

## Create a thread

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d ''
```

## Add a user question to the thread

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/messages?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
      "role": "user",
      "content": "<user input related to the MCP server you connect>"
    }'
```

## Create a run and check the output

Create a run to pass headers for the tool. Observe that the model uses the Grounding with Bing Search tool to provide a response to the user's question.

The `require_approval` parameter is optional. Supported values are:

- `always`: A developer needs to provide approval for every call. If you don't provide a value, this one is the default.
- `never`: No approval is required.
- `{"never":[<tool_name_1>, <tool_name_2>]}`: You provide a list of tools that don't require approval.
- `{"always":[<tool_name_1>, <tool_name_2>]}`: You provide a list of tools that require approval.

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/runs?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
      "assistant_id": "<agent_id>",
      "tool_resources": {
          "mcp": [
            {
                "server_label": "<the same unique name you provided during agent creation>",
    "require_approval": "always" #always by default
                "headers": {
                    "Authorization": "Bearer <token>",
                }

            }
          ]
      },
    }'
```

## Retrieve the status of the run

```bash
curl --request GET \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/runs/run_abc123?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN"
```

If the model tries to invoke a tool in your MCP server with approval required, you get a run with `requires_action` status:

```bash
{
  "id": "run_123",
  "object": "thread.run",
  ...
  "status": "requires_action",
  ...
  "required_action": {
    "type": "submit_tool_approval",
    "submit_tool_approval": {
      "tool_calls": [
        {
          "id": "call_123",
          "type": "mcp",
          "arguments": "{...}",
          "name": "<tool_name>",
          "server_label": "<server_label_you_provided>"
        }
      ]
    }
  },
  ...
  "tools": [
    {
      "type": "mcp",
      "server_label": "<server_label_you_provided>",
      "server_url": "<server_url_you_provided>",
      "allowed_tools": null
    }
  ],
 ...
}
```

Carefully review the tool and arguments to be passed so that you can make an informed decision for approval.

## Submit your approval

If you decide to approve, set the `approve` parameter to `true` with the `id` value for the preceding tool calls:

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/runs/run_abc123/submit_tool_outputs?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "tool_approvals": [
        {
            "tool_call_id": "call_abc123",
            "approve": true,
            "headers": {
            }
        }
    ]
}
```

## Retrieve the agent response

```bash
curl --request GET \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/messages?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN"
```
