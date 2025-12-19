---
title: Code Samples for the Model Context Protocol Tool (Preview)
titleSuffix: Microsoft Foundry
description: Find code samples to connect Foundry Agent Service with MCP servers.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 12/19/2025
author: alvinashcraft
ms.author: aashcraft
zone_pivot_groups: selection-mcp-code
ms.custom: azure-ai-agents-code
---

# How to use the Model Context Protocol (MCP) tool (preview)

> [!NOTE]
> This article refers to the classic version of the agents API. 
>
> 🔍 [View the new MCP tool documentation](../../../default/agents/how-to/tools/model-context-protocol.md?view=foundry&preserve-view=true).

This article provides code samples for connecting Foundry Agent Service with Model Context Protocol (MCP) servers.

## Prerequisites

- A [configured MCP server](./model-context-protocol.md#setup), such as the GitHub MCP server.

:::zone pivot="csharp"
- Install the `Azure.AI.Agents.Persistent` and `Azure.Identity` NuGet packages to your project:

  ```console
  dotnet add package Azure.AI.Agents.Persistent
  dotnet add package Azure.Identity
  ```
:::zone-end

> [!NOTE]
> **MCP server authentication**: Many MCP servers require authentication through custom headers, such as API keys, Bearer tokens, or OAuth credentials. Use the `UpdateHeader` method (C#) or `update_headers` method (Python) to pass authentication headers to your MCP server. For more information about authentication and security considerations, see the [How it works](./model-context-protocol.md?view=foundry&preserve-view=true#how-it-works) section in the **Connect to Model Context Protocol servers** documentation.

## Code samples

:::zone pivot="csharp"

## Create a project client

Make sure your code includes the required `using` statements for this example.

```csharp
using Azure;
using Azure.AI.Agents.Persistent;
using Azure.Identity;
using System;
using System.Collections.Generic;
using System.Threading;
```

Create a client object that contains the endpoint for connecting to your AI project and other resources.

> [!NOTE]
> You can find an asynchronous example on [GitHub](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.Agents.Persistent/samples).

```csharp
var projectEndpoint = System.Environment.GetEnvironmentVariable("PROJECT_ENDPOINT");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("MODEL_DEPLOYMENT_NAME");
var mcpServerUrl = System.Environment.GetEnvironmentVariable("MCP_SERVER_URL");
var mcpServerLabel = System.Environment.GetEnvironmentVariable("MCP_SERVER_LABEL");

PersistentAgentsClient agentClient = new(projectEndpoint, new DefaultAzureCredential());
```

## Create the MCP tool definition

Create the MCP tool definition and configure the allowed tools.

```csharp
// Create MCP tool definition
MCPToolDefinition mcpTool = new(mcpServerLabel, mcpServerUrl);

// Configure allowed tools (optional)
string searchApiCode = "search_azure_rest_api_code";
mcpTool.AllowedTools.Add(searchApiCode);
```

Use the `MCPToolDefinition` during the agent initialization.

```csharp
PersistentAgent agent = agentClient.Administration.CreateAgent(
   model: modelDeploymentName,
   name: "my-mcp-agent",
   instructions: "You are a helpful agent that can use MCP tools to assist users. Use the available MCP tools to answer questions and perform tasks.",
   tools: [mcpTool]);
```

## Create a thread and add a message

Create the thread, add the message containing a question for the agent, and start the run with MCP tool resources.

```csharp
PersistentAgentThread thread = agentClient.Threads.CreateThread();

// Create message to thread
PersistentThreadMessage message = agentClient.Messages.CreateMessage(
    thread.Id,
    MessageRole.User,
    "Please summarize the Azure REST API specifications Readme");

MCPToolResource mcpToolResource = new(mcpServerLabel);
mcpToolResource.UpdateHeader("SuperSecret", "123456");
ToolResources toolResources = mcpToolResource.ToToolResources();

// Run the agent with MCP tool resources
ThreadRun run = agentClient.Runs.CreateRun(thread, agent, toolResources);

// Handle run execution and tool approvals
while (run.Status == RunStatus.Queued || run.Status == RunStatus.InProgress || run.Status == RunStatus.RequiresAction)
{
    Thread.Sleep(TimeSpan.FromMilliseconds(1000));
    run = agentClient.Runs.GetRun(thread.Id, run.Id);

    if (run.Status == RunStatus.RequiresAction && run.RequiredAction is SubmitToolApprovalAction toolApprovalAction)
    {
        var toolApprovals = new List<ToolApproval>();
        foreach (var toolCall in toolApprovalAction.SubmitToolApproval.ToolCalls)
        {
            if (toolCall is RequiredMcpToolCall mcpToolCall)
            {
                Console.WriteLine($"Approving MCP tool call: {mcpToolCall.Name}, Arguments: {mcpToolCall.Arguments}");
                toolApprovals.Add(new ToolApproval(mcpToolCall.Id, approve: true)
                {
                    Headers = { ["SuperSecret"] = "123456" }
                });
            }
        }

        if (toolApprovals.Count > 0)
        {
            run = agentClient.Runs.SubmitToolOutputsToRun(thread.Id, run.Id, toolApprovals: toolApprovals);
        }
    }
}
```

## Print the messages

```csharp
Pageable<PersistentThreadMessage> messages = agentClient.Messages.GetMessages(
    threadId: thread.Id,
    order: ListSortOrder.Ascending
);

foreach (PersistentThreadMessage threadMessage in messages)
{
    Console.Write($"{threadMessage.CreatedAt:yyyy-MM-dd HH:mm:ss} - {threadMessage.Role,10}: ");
    foreach (MessageContent contentItem in threadMessage.ContentItems)
    {
        if (contentItem is MessageTextContent textItem)
        {
            Console.Write(textItem.Text);
        }
        else if (contentItem is MessageImageFileContent imageFileItem)
        {
            Console.Write($"<image from ID: {imageFileItem.FileId}>");
        }
        Console.WriteLine();
    }
}
```

## Optional: Delete the agent

When you finish using your agent, delete it by using the following code:

```csharp
agentClient.Threads.DeleteThread(threadId: thread.Id);
agentClient.Administration.DeleteAgent(agentId: agent.Id);
```
:::zone-end

:::zone pivot="python"

## Create an Agent with the MCP Tool

The following code sample begins by setting up the necessary imports, getting the relevant MCP server configuration, and initializing the AI Project client. It then creates an agent, adds a message to a thread, and runs the agent.


```python
# Import necessary libraries

import os, time
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import (
    ListSortOrder,
    McpTool,
    RequiredMcpToolCall,
    RunStepActivityDetails,
    SubmitToolApprovalAction,
    ToolApproval,
)

# Get MCP server configuration from environment variables
mcp_server_url = os.environ.get("MCP_SERVER_URL", "https://gitmcp.io/Azure/azure-rest-api-specs")
mcp_server_label = os.environ.get("MCP_SERVER_LABEL", "github")

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
# Initialize agent MCP tool
mcp_tool = McpTool(
    server_label=mcp_server_label,
    server_url=mcp_server_url,
    allowed_tools=[],  # Optional: specify allowed tools
)

# You can also add or remove allowed tools dynamically
search_api_code = "search_azure_rest_api_code"
mcp_tool.allow_tool(search_api_code)
print(f"Allowed tools: {mcp_tool.allowed_tools}")

# Create agent with MCP tool and process agent run
with project_client:
    agents_client = project_client.agents

    # Create a new agent.
    # NOTE: To reuse existing agent, fetch it with get_agent(agent_id)
    agent = agents_client.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="my-mcp-agent",
        instructions="You are a helpful agent that can use MCP tools to assist users. Use the available MCP tools to answer questions and perform tasks.",
        tools=mcp_tool.definitions,
    )

    print(f"Created agent, ID: {agent.id}")
    print(f"MCP Server: {mcp_tool.server_label} at {mcp_tool.server_url}")

    # Create thread for communication
    thread = agents_client.threads.create()
    print(f"Created thread, ID: {thread.id}")

    # Create message to thread
    message = agents_client.messages.create(
        thread_id=thread.id,
        role="user",
        content="Please summarize the Azure REST API specifications Readme",
    )
    print(f"Created message, ID: {message.id}")
    # Create and process agent run in thread with MCP tools
    mcp_tool.update_headers("SuperSecret", "123456")
    # mcp_tool.set_approval_mode("never")  # Uncomment to disable approval requirement
    run = agents_client.runs.create(thread_id=thread.id, agent_id=agent.id, tool_resources=mcp_tool.resources)
    print(f"Created run, ID: {run.id}")

    while run.status in ["queued", "in_progress", "requires_action"]:
        time.sleep(1)
        run = agents_client.runs.get(thread_id=thread.id, run_id=run.id)

        if run.status == "requires_action" and isinstance(run.required_action, SubmitToolApprovalAction):
            tool_calls = run.required_action.submit_tool_approval.tool_calls
            if not tool_calls:
                print("No tool calls provided - cancelling run")
                agents_client.runs.cancel(thread_id=thread.id, run_id=run.id)
                break

            tool_approvals = []
            for tool_call in tool_calls:
                if isinstance(tool_call, RequiredMcpToolCall):
                    try:
                        print(f"Approving tool call: {tool_call}")
                        tool_approvals.append(
                            ToolApproval(
                                tool_call_id=tool_call.id,
                                approve=True,
                                headers=mcp_tool.headers,
                            )
                        )
                    except Exception as e:
                        print(f"Error approving tool_call {tool_call.id}: {e}")

            print(f"tool_approvals: {tool_approvals}")
            if tool_approvals:
                agents_client.runs.submit_tool_outputs(
                    thread_id=thread.id, run_id=run.id, tool_approvals=tool_approvals
                )

        print(f"Current run status: {run.status}")

    print(f"Run completed with status: {run.status}")
    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Display run steps and tool calls
    run_steps = agents_client.run_steps.list(thread_id=thread.id, run_id=run.id)

    # Loop through each step
    for step in run_steps:
        print(f"Step {step['id']} status: {step['status']}")

        # Check if there are tool calls in the step details
        step_details = step.get("step_details", {})
        tool_calls = step_details.get("tool_calls", [])

        if tool_calls:
            print("  MCP Tool calls:")
            for call in tool_calls:
                print(f"    Tool Call ID: {call.get('id')}")
                print(f"    Type: {call.get('type')}")

        if isinstance(step_details, RunStepActivityDetails):
            for activity in step_details.activities:
                for function_name, function_definition in activity.tools.items():
                    print(
                        f'  The function {function_name} with description "{function_definition.description}" will be called.:'
                    )
                    if len(function_definition.parameters) > 0:
                        print("  Function parameters:")
                        for argument, func_argument in function_definition.parameters.properties.items():
                            print(f"      {argument}")
                            print(f"      Type: {func_argument.type}")
                            print(f"      Description: {func_argument.description}")
                    else:
                        print("This function has no parameters")

        print()  # add an extra newline between steps

    # Fetch and log all messages
    messages = agents_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
    print("\nConversation:")
    print("-" * 50)
    for msg in messages:
        if msg.text_messages:
            last_text = msg.text_messages[-1]
            print(f"{msg.role.upper()}: {last_text.text.value}")
            print("-" * 50)

    # Example of dynamic tool management
    print(f"\nDemonstrating dynamic tool management:")
    print(f"Current allowed tools: {mcp_tool.allowed_tools}")

    # Remove a tool
    try:
        mcp_tool.disallow_tool(search_api_code)
        print(f"After removing {search_api_code}: {mcp_tool.allowed_tools}")
    except ValueError as e:
        print(f"Error removing tool: {e}")

    # Clean-up and delete the agent once the run is finished.
    # NOTE: Comment out this line if you plan to reuse the agent later.
    agents_client.delete_agent(agent.id)
    print("Deleted agent")
```

## Next steps

* [Tools overview](./overview.md)
* [Python SDK samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-agents/samples)

:::zone-end

:::zone pivot="rest"

Follow the [REST API quickstart](../../quickstart.md?pivots=rest-api) to set the right values for the environment variables `AGENT_TOKEN`, `AZURE_AI_FOUNDRY_PROJECT_ENDPOINT`, and `API_VERSION`.

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

Create a run to pass headers for the tool. You can see that the model uses the Grounding with Bing Search tool to provide a response to the user's question.

The `require_approval` parameter is optional. Supported values are:

- `always`: A developer needs to provide approval for every call. If you don't provide a value, this value is the default.
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
