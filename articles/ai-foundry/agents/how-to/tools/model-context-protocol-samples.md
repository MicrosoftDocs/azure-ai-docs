---
title: Code Samples for the Model Context Protocol Tool (Preview)
titleSuffix: Azure AI Foundry
description: Find code samples to connect Azure AI Foundry Agent Service with MCP servers.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 07/14/2025
author: aahill
ms.author: aahi
zone_pivot_groups: selection-mcp-code
ms.custom: azure-ai-agents-code
---

# Code samples for the Model Context Protocol tool (preview)

Use this article to find code samples for connecting Azure AI Foundry Agent Service with Model Context Protocol (MCP) servers.

:::zone pivot="python"

## Initialize the client

The code begins by setting up the necessary imports, getting the relevant MCP server configuration, and initializing the AI Project client:

```python
# Import necessary libraries
import os, time
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import McpTool, RequiredMcpToolCall, SubmitToolApprovalAction, ToolApproval

# Get the MCP server configuration from environment variables
mcp_server_url = os.environ.get("MCP_SERVER_URL", "https://gitmcp.io/Azure/azure-rest-api-specs")
mcp_server_label = os.environ.get("MCP_SERVER_LABEL", "github")

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
```

## Set up the tool

To add the MCP server to the agent, use the following example, which takes the MCP server label and URL from the last step. You can also add or remove allowed tools dynamically through the `allow_tool` parameter.

```python
mcp_tool = McpTool(
    server_label=mcp_server_label,
    server_url=mcp_server_url,
    allowed_tools=[],  # Optional: specify allowed tools
)

# You can also add or remove allowed tools dynamically
search_api_code = "search_azure_rest_api_code"
mcp_tool.allow_tool(search_api_code)
print(f"Allowed tools: {mcp_tool.allowed_tools}")
```

## Create an agent

You create an agent by using the `project_client.agents.create_agent` method:

```python
# Create a new agent.
# NOTE: To reuse an existing agent, fetch it with get_agent(agent_id)
with project_client:
    agents_client = project_client.agents

    # Create a new agent.
    # NOTE: To reuse an existing agent, fetch it with get_agent(agent_id)
    agent = agents_client.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="my-mcp-agent",
        instructions="You are a helpful agent that can use MCP tools to assist users. Use the available MCP tools to answer questions and perform tasks.",
        tools=mcp_tool.definitions,
    )
```

## Create a thread

Create the thread and add the initial user message:

```python
# Create a thread for communication
thread = agents_client.threads.create()
print(f"Created thread, ID: {thread.id}")

# Create a message for the thread
message = agents_client.messages.create(
    thread_id=thread.id,
    role="user",
    content="Please summarize the Azure REST API specifications Readme",
)
print(f"Created message, ID: {message.id}")
```

## Handle tool approvals

Set the MCP server update headers and optionally disable tool approval requirements:

```python
mcp_tool.update_headers("SuperSecret", "123456")
# mcp_tool.set_approval_mode("never")  # Uncomment to disable approval requirements
run = agents_client.runs.create(thread_id=thread.id, agent_id=agent.id, tool_resources=mcp_tool.resources)
print(f"Created run, ID: {run.id}")
```

## Create a run and check the output

Create the run, check the output, and examine what tools were called during the run:

```python
    # Create and automatically process the run, handling tool calls internally
    run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Retrieve the steps taken during the run for analysis
    run_steps = project_client.agents.run_steps.list(thread_id=thread.id, run_id=run.id)

    # Loop through each step to display information
    for step in run_steps:
        print(f"Step {step['id']} status: {step['status']}")

        tool_calls = step.get("step_details", {}).get("tool_calls", [])
        for call in tool_calls:
            print(f"  Tool Call ID: {call.get('id')}")
            print(f"  Type: {call.get('type')}")
            function_details = call.get("function", {})
            if function_details:
                print(f"  Function name: {function_details.get('name')}")
                print(f" function output: {function_details.get('output')}")

        print()
```

## Perform cleanup

After the interaction is complete, the script performs cleanup by deleting the created agent resource via `agents_client.delete_agent()` to avoid leaving unused resources. It also fetches and prints the entire message history from the thread by using `agents_client.list_messages()` for review or logging.

```python
        # Delete the agent resource to clean up
        project_client.agents.delete_agent(agent.id)
        print("Deleted agent")

        # Fetch and log all messages exchanged during the conversation thread
        messages = project_client.agents.messages.list(thread_id=thread.id)
        for msg in messages:
            print(f"Message ID: {msg.id}, Role: {msg.role}, Content: {msg.content}")
```

:::zone-end

:::zone pivot="rest"

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

:::zone-end
