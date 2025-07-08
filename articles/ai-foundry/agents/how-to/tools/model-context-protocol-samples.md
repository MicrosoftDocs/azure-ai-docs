---
title: 'MCP tool code samples'
titleSuffix: Azure AI Foundry
description: Find code samples to connect Foundry Agent service with MCP.
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

# How to use the Model Context Protocol (MCP) tool

Use this article to find step-by-step instructions and code samples for connecting Foundry Agent service with MCP.

Follow the [REST API Quickstart](../../quickstart.md?pivots=rest-api#api-call-information) to set the right values for the environment variables `AGENT_TOKEN`, `AZURE_AI_FOUNDRY_PROJECT_ENDPOINT`, and `API_VERSION`.


## Create an Agent with the MCP tool enabled

To make the MCP tool available to your agent, initialize a tool with the server endpoint, server label and more
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
              "server_url": "<your MCP server url>",
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

Create a run to pass headers for the tool and observe that the model uses the Grounding with Bing Search tool to provide a response to the user's question. 
`require_approval` parameter is optional. If not provided, `always` is the default value, meaning each time developer needs to approve before calling. Supported values:

- `always` by default
- `never` meaning no approval is required
- `{"never":[<tool_name_1>, <tool_name_2>]}` you can also provide a list of tools without required approval
- `{"always":[<tool_name_1>, <tool_name_2>]}` you can provide a list of tools with required approval

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

If the model is trying to invoke a tool in your MCP server with approval required, you get a run with `require_action` status.
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
Make sure you carefully reviewed the tool and argument(s) to be passed and make an informed decision for approval.

## Submit your approval
If you decide to approve, you need to set the `approve` parameter to be `true` with the `id` for the preceding tool calls.
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
