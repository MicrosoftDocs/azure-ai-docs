---
title: "Connect to MCP Server Endpoints for agents"
description: "Connect your Foundry agents to Model Context Protocol (MCP) servers using the MCP tool. Extend capabilities with external tools and data."
services: cognitive-services
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 04/23/2026
author: jonburchel
reviewer: lindazqli
ms.author: jburchel
ms.reviewer: zhuoqunli
ai-usage: ai-assisted
zone_pivot_groups: selection-mcp-code-new
ms.custom: dev-focus, pilot-ai-workflow-jan-2026, doc-kit-assisted
#CustomerIntent: As a developer, I want to connect my Foundry agent to external MCP servers so that I can extend agent capabilities with third-party tools.
---

# Connect agents to Model Context Protocol servers

Connect your Foundry agents to [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) servers by using the MCP tool. This connection extends agent capabilities with external tools and data sources. By connecting to remote MCP server endpoints, your agent's Foundry model can access tools hosted by developers and organizations that MCP-compatible clients like Foundry Agent Service can use.

MCP is an open standard that defines how applications provide tools and contextual data to large language models (LLMs). It enables consistent, scalable integration of external tools into model workflows.

In this article, you learn how to:

- Add a remote MCP server as a tool.
- Authenticate to an MCP server by using a project connection.
- Review and approve MCP tool calls.
- Troubleshoot common MCP integration issues.

For conceptual details about how MCP integration works, see [How it works](#how-it-works).

### Usage support

The following table shows SDK and setup support for MCP connections.

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

Before you begin, make sure you have:

- An Azure subscription with an active Microsoft Foundry project.
- Azure role-based access control (RBAC): Contributor or Owner role on the Foundry project.
- The latest SDK package for your language. The .NET SDK is currently in preview. For installation details, see the [quickstart](../../../quickstarts/get-started-code.md).
- Azure credentials configured for authentication (such as `DefaultAzureCredential`).
- Access to a remote MCP server endpoint (such as GitHub's MCP server at `https://api.githubcopilot.com/mcp`).

## Public and private MCP server endpoints

Agent Service supports both public and private MCP server endpoints:

- **Public endpoints**: Connect to any publicly accessible remote MCP server. This option works with both Basic and Standard agent setups.
- **Private endpoints**: Connect to MCP servers that aren't exposed to the public internet. Private MCP requires [Standard Agent Setup with private networking](../virtual-networks.md) and a dedicated MCP subnet within your virtual network.

For private MCP servers, deploy your MCP server on Azure Container Apps with internal-only ingress on a dedicated MCP subnet delegated to `Microsoft.App/environments`. To get started, use the [19-private-network-agents-tools-setup](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/19-private-network-agents-tools-setup) template, which provisions the required network infrastructure including the MCP subnet.

For details about tool support in network-isolated environments, see [Agent tools with network isolation](../../../how-to/configure-private-link.md#agent-tools-with-network-isolation).

## Use Foundry Toolboxes as MCP endpoints

Foundry Toolboxes (preview) let you bundle multiple tools - such as Web Search, Code Interpreter, File Search, Azure AI Search, MCP servers, OpenAPI tools, and Agent-to-Agent connections - into a single MCP-compatible endpoint. Instead of configuring each tool separately on every agent, create a Toolbox in Foundry and point your agent to the Toolbox endpoint by using the standard `mcp` tool configuration (`server_url` and `server_label`).

Because the Toolbox endpoint is MCP-compatible, any runtime that can consume an MCP server can also consume a Toolbox. This compatibility includes Foundry Agent Service, Microsoft Agent Framework, LangGraph, GitHub Copilot SDK, and other MCP-enabled clients. You can add, remove, or reconfigure tools in the Toolbox without changing your agent code.

For setup steps, see [Create and use a Foundry Toolbox](toolbox.md).

## Authentication

Many MCP servers require authentication.

In Foundry Agent Service, use a project connection to store authentication details, such as API keys or bearer tokens, instead of hard-coding credentials in your app.

To learn about supported authentication options, including key-based, Microsoft Entra identities, and OAuth identity passthrough, see [MCP server authentication](../mcp-authentication.md).

> [!NOTE]
> Set `project_connection_id` to the ID of your project connection.

> [!TIP]
> When you add the Azure DevOps MCP Server (preview) through the **Add Tools** catalog, you authenticate to Azure DevOps during the organization connection step and store the authentication as a project connection. Use least-privilege access and review scopes when connecting the organization.

When you use a Foundry Toolbox MCP endpoint, the Toolbox centrally manages authentication. The Toolbox handles credential injection, token refresh, and policy enforcement at runtime for all tools in the bundle. Agents authenticate to the Toolbox endpoint itself by using Microsoft Entra credentials, such as `DefaultAzureCredential`, and individual tool credentials don't need to be passed by each agent. For Toolbox auth configuration, see [Toolbox prerequisites](toolbox.md#prerequisites).

<!-- The verbiage in the following section is required. Do not remove or modify. -->
## Considerations for using non-Microsoft services and servers

You're subject to the terms between you and the service provider when you use connected non-Microsoft services. When you connect to a non-Microsoft service, you pass some of your data, such as prompt content, to the non-Microsoft service, or your application might receive data from the non-Microsoft service. You're responsible for your use of non-Microsoft services and data, along with any charges associated with that use.

Third parties, not Microsoft, create the remote MCP servers that you decide to use with the MCP tool described in this article. Microsoft doesn't test or verify these servers. Microsoft has no responsibility to you or others in relation to your use of any remote MCP servers.

Carefully review and track what MCP servers you add to Foundry Agent Service. Rely on servers hosted by trusted service providers themselves rather than proxies.

The MCP tool allows you to pass custom headers, such as authentication keys or schemas, that a remote MCP server might need. Review all data that you share with remote MCP servers and log the data for auditing purposes. Be aware of non-Microsoft practices for retention and location of data.

> [!NOTE]
> Foundry Toolboxes are different from third-party MCP servers. Toolboxes are organization-governed resources that you create and manage within your Microsoft Foundry project. However, you're still responsible for tool selection, data handling, and compliance when curating Toolbox contents.

## Best practices

For general guidance on tool usage, see [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md).

When you use MCP servers, follow these practices:

- Use an allow list of tools by using `allowed_tools`.
- Require approval for high-risk operations, especially tools that write data or change resources.
- Review the requested tool name and arguments before you approve.
- Log approvals and tool calls for auditing and troubleshooting.

> [!TIP]
> When you add the Azure DevOps MCP Server through the **Add Tools** catalog, the tool selection configuration maps to the `allowed_tools` behavior described in this article. Selecting a subset of tools in the catalog UI is equivalent to specifying an `allowed_tools` list in code.

## Create an agent in Python with the MCP tool

Use the following code sample to create an agent and call the function. The .NET SDK is currently in preview. See the [quickstart](../../../quickstarts/get-started-code.md) for details.

:::zone pivot="python"

The following example shows how to use the GitHub MCP server as a tool for an agent. Select **Prompt Agents** to use the Azure AI Projects SDK to create a server-side prompt agent, or **Hosted Agents** to use the Agent Framework [`FoundryChatClient`](../../quickstarts/responses-api.md) to build an ephemeral, in-process agent.

### [Prompt Agents](#tab/prompt-agents)

```python
import json
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, MCPTool
from openai.types.responses.response_input_param import McpApprovalResponse, ResponseInputParam

# Format: "https://resource_name.ai.azure.com/api/projects/project_name"
PROJECT_ENDPOINT = "your_project_endpoint"
MCP_CONNECTION_NAME = "my-mcp-connection"

# Create clients to call Foundry API
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()

# [START tool_declaration]
tool = MCPTool(
    server_label="api-specs",
    server_url="https://api.githubcopilot.com/mcp",
    require_approval="always",
    project_connection_id=MCP_CONNECTION_NAME,
)
# [END tool_declaration]

# Create a prompt agent with MCP tool capabilities
agent = project.agents.create_version(
    agent_name="MyAgent7",
    definition=PromptAgentDefinition(
        model="gpt-5-mini",
        instructions="Use MCP tools as needed",
        tools=[tool],
    ),
)
print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

# Create a conversation to maintain context across multiple interactions
conversation = openai.conversations.create()
print(f"Created conversation (id: {conversation.id})")

# Send initial request that will trigger the MCP tool
response = openai.responses.create(
    conversation=conversation.id,
    input="What is my username in my GitHub profile?",
    extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
)

# Process any MCP approval requests that were generated
input_list: ResponseInputParam = []
for item in response.output:
    if item.type == "mcp_approval_request" and item.id:
        print("MCP approval requested")
        print(f"  Server: {item.server_label}")
        print(f"  Tool: {getattr(item, 'name', '<unknown>')}")
        print(
            f"  Arguments: {json.dumps(getattr(item, 'arguments', None), indent=2, default=str)}"
        )

        # Approve only after you review the tool call.
        # In production, implement your own approval UX and policy.
        should_approve = (
            input("Approve this MCP tool call? (y/N): ").strip().lower() == "y"
        )
        input_list.append(
            McpApprovalResponse(
                type="mcp_approval_response",
                approve=should_approve,
                approval_request_id=item.id,
            )
        )

# Send the approval response back to continue the agent's work
response = openai.responses.create(
    input=input_list,
    previous_response_id=response.id,
    extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
)

print(f"Response: {response.output_text}")

# Clean up resources by deleting the agent version
project.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
print("Agent deleted")
```

### Expected output

The following example shows the expected output when you run the sample:

```console
Agent created (id: <agent-id>, name: MyAgent7, version: 1)
Created conversation (id: <conversation-id>)
Response: Your GitHub username is "example-username".
Agent deleted
```

### [Hosted Agents](#tab/hosted-agents)

This sample uses [`FoundryChatClient`](../../quickstarts/responses-api.md) from the Microsoft Agent Framework and calls `get_mcp_tool()` to register a hosted MCP server with per-tool approval control. Install the package with `pip install agent-framework-foundry aiohttp`, set the `FOUNDRY_PROJECT_ENDPOINT` and `FOUNDRY_MODEL` environment variables, and sign in with `az login`.

```python
import asyncio
from typing import Any

from agent_framework import Agent, Message
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential

async def main() -> None:
    # Reads FOUNDRY_PROJECT_ENDPOINT and FOUNDRY_MODEL from the environment.
    client = FoundryChatClient(credential=AzureCliCredential())

    # Register a hosted MCP server. Use approval_mode="always_require" in production
    # so the user approves each tool call; "never_require" skips approvals.
    mcp_tool = client.get_mcp_tool(
        name="Microsoft Learn MCP",
        url="https://learn.microsoft.com/api/mcp",
        approval_mode={"never_require_approval": ["microsoft_docs_search"]},
    )

    async with Agent(
        client=client,
        name="DocsAgent",
        instructions="You are a helpful assistant that uses your MCP tool "
        "to help with Microsoft documentation questions.",
        tools=[mcp_tool],
    ) as agent:
        query = "What is Microsoft Agent Framework?"
        result = await agent.run(query)

        # Handle any approval prompts raised by the MCP tool.
        while len(result.user_input_requests) > 0:
            new_inputs: list[Any] = [query]
            for user_input_needed in result.user_input_requests:
                print(
                    f"Approval requested for {user_input_needed.function_call.name} "
                    f"with arguments: {user_input_needed.function_call.arguments}"
                )
                new_inputs.append(Message(role="assistant", contents=[user_input_needed]))
                approve = input("Approve function call? (y/n): ").lower() == "y"
                new_inputs.append(
                    Message(
                        role="user",
                        contents=[user_input_needed.to_function_approval_response(approve)],
                    )
                )
            result = await agent.run(new_inputs)

        print(f"Agent: {result}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Expected output

The agent calls the Microsoft Learn MCP server and returns documentation-grounded text:

```console
Agent: Microsoft Agent Framework is an open-source framework for building, orchestrating, and deploying AI agents ...
```

For the full sample, including session-based approval flows and streaming, see [foundry_chat_client_with_hosted_mcp.py](https://github.com/microsoft/agent-framework/blob/main/python/samples/02-agents/providers/foundry/foundry_chat_client_with_hosted_mcp.py). For local (stdio) MCP servers, see [foundry_chat_client_with_local_mcp.py](https://github.com/microsoft/agent-framework/blob/main/python/samples/02-agents/providers/foundry/foundry_chat_client_with_local_mcp.py).

---

:::zone-end

:::zone pivot="csharp"
## Create an agent with MCP tool

The following example shows how to use a remote MCP server as a tool for an agent. Select **Prompt Agents** to use the Azure AI Projects SDK to create a server-side prompt agent, or **Hosted Agents** to use the Microsoft Agent Framework to build an ephemeral, in-process agent.

### [Prompt Agents](#tab/prompt-agents)

The example uses synchronous methods to create an agent. For asynchronous methods, see the [sample code](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Extensions.OpenAI/samples/Sample19_MCP.md) in the Azure SDK for .NET repository on GitHub.

```csharp
using System;
using Azure.AI.Projects;
using Azure.AI.Extensions.OpenAI;
using Azure.Identity;

// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
var projectEndpoint = "your_project_endpoint";

// Create project client to call Foundry API
AIProjectClient projectClient = new(
    endpoint: new Uri(projectEndpoint),
    tokenProvider: new DefaultAzureCredential());

// Create Agent with the `MCPTool`. Note that in this scenario 
// GlobalMcpToolCallApprovalPolicy.AlwaysRequireApproval is used,
// which means that any calls to the MCP server must be approved.
DeclarativeAgentDefinition agentDefinition = new(model: "gpt-5-mini")
{
    Instructions = "You are a helpful agent that can use MCP tools to assist users. Use the available MCP tools to answer questions and perform tasks.",
    Tools = { ResponseTool.CreateMcpTool(
        serverLabel: "api-specs",
        serverUri: new Uri("https://gitmcp.io/Azure/azure-rest-api-specs"),
        toolCallApprovalPolicy: new McpToolCallApprovalPolicy(GlobalMcpToolCallApprovalPolicy.AlwaysRequireApproval
    )) }
};
AgentVersion agentVersion = projectClient.AgentAdministrationClient.CreateAgentVersion(
    agentName: "myAgent",
    options: new(agentDefinition));

// If the tool approval is required, the response item is
// of `McpToolCallApprovalRequestItem` type and contains all
// the information about tool call. This example checks that
// the server label is "api-specs" and approves the tool call.
// All other calls are denied because they should not occur for
// the current configuration.
ProjectResponsesClient responseClient = projectClient.ProjectOpenAIClient.GetProjectResponsesClientForAgent(agentVersion.Name);

CreateResponseOptions nextResponseOptions = new([ResponseItem.CreateUserMessageItem("Please summarize the Azure REST API specifications README")]);
ResponseResult latestResponse = null;

while (nextResponseOptions is not null)
{
    latestResponse = responseClient.CreateResponse(nextResponseOptions);
    nextResponseOptions = null;

    foreach (ResponseItem responseItem in latestResponse.OutputItems)
    {
        if (responseItem is McpToolCallApprovalRequestItem mcpToolCall)
        {
            nextResponseOptions = new CreateResponseOptions()
            {
                PreviousResponseId = latestResponse.Id,
            };
            if (string.Equals(mcpToolCall.ServerLabel, "api-specs"))
            {
                Console.WriteLine($"Approval requested for {mcpToolCall.ServerLabel} (tool: {mcpToolCall.ToolName})");
                Console.Write("Approve this MCP tool call? (y/N): ");
                bool approved = string.Equals(Console.ReadLine(), "y", StringComparison.OrdinalIgnoreCase);
                nextResponseOptions.InputItems.Add(ResponseItem.CreateMcpApprovalResponseItem(approvalRequestId: mcpToolCall.Id, approved: approved));
            }
            else
            {
                Console.WriteLine($"Rejecting unknown call {mcpToolCall.ServerLabel}...");
                nextResponseOptions.InputItems.Add(ResponseItem.CreateMcpApprovalResponseItem(approvalRequestId: mcpToolCall.Id, approved: false));
            }
        }
    }
}

// Output the final response from the agent.
Console.WriteLine(latestResponse.GetOutputText());

// Clean up resources by deleting the agent version.
projectClient.AgentAdministrationClient.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

### Expected output

The following example shows the expected output when you run the sample:

```console
Approval requested for api-specs...
Response: The Azure REST API specifications repository contains the OpenAPI specifications for Azure services. It is
organized by service and includes guidelines for contributing new specifications. The repository is intended for use by developers building tools and services that interact with Azure APIs.
```

### [Hosted Agents](#tab/hosted-agents)

This sample uses the Microsoft Agent Framework and calls `AsAIAgent(...)` on `AIProjectClient` together with an MCP client to expose remote MCP tools to the agent. Install the `Microsoft.Agents.AI.Foundry`, `Azure.AI.Projects`, and `ModelContextProtocol` packages, set the `AZURE_AI_PROJECT_ENDPOINT` and `AZURE_AI_MODEL_DEPLOYMENT_NAME` environment variables, and sign in with `az login`.

```csharp
using Azure.AI.Projects;
using Azure.Identity;
using Microsoft.Agents.AI;
using Microsoft.Extensions.AI;
using ModelContextProtocol.Client;

string endpoint = Environment.GetEnvironmentVariable("AZURE_AI_PROJECT_ENDPOINT")
    ?? throw new InvalidOperationException("AZURE_AI_PROJECT_ENDPOINT is not set.");
string deploymentName = Environment.GetEnvironmentVariable("AZURE_AI_MODEL_DEPLOYMENT_NAME") ?? "gpt-5-mini";

// Connect to the Microsoft Learn MCP server via Streamable HTTP transport.
Console.WriteLine("Connecting to MCP server at https://learn.microsoft.com/api/mcp ...");

await using McpClient mcpClient = await McpClient.CreateAsync(new HttpClientTransport(new()
{
    Endpoint = new Uri("https://learn.microsoft.com/api/mcp"),
    Name = "Microsoft Learn MCP",
}));

// Retrieve the list of tools available on the MCP server.
IList<McpClientTool> mcpTools = await mcpClient.ListToolsAsync();
Console.WriteLine($"MCP tools available: {string.Join(", ", mcpTools.Select(t => t.Name))}");

List<AITool> agentTools = [.. mcpTools.Cast<AITool>()];

AIProjectClient aiProjectClient = new(new Uri(endpoint), new DefaultAzureCredential());

AIAgent agent = aiProjectClient.AsAIAgent(
    deploymentName,
    instructions: "You are a helpful assistant that can answer Microsoft documentation questions. Use the Microsoft Learn MCP tool to search documentation.",
    name: "DocsAgent",
    tools: agentTools);

const string Prompt = "How does one create an Azure storage account using the az CLI?";
Console.WriteLine($"User: {Prompt}\n");
Console.WriteLine($"Agent: {await agent.RunAsync(Prompt)}");
```

### Expected output

The agent queries the Microsoft Learn MCP server for documentation snippets and answers:

```console
User: How does one create an Azure storage account using the az CLI?

Agent: To create an Azure storage account using the az CLI, run: `az storage account create --name <name> --resource-group <rg> --location <region> --sku Standard_LRS` ...
```

For local MCP transports and additional patterns, see [Agent_Step09_UsingMcpClientAsTools](https://github.com/microsoft/agent-framework/tree/main/dotnet/samples/02-agents/AgentsWithFoundry/Agent_Step09_UsingMcpClientAsTools) and [Agent_Step23_LocalMCP](https://github.com/microsoft/agent-framework/tree/main/dotnet/samples/02-agents/AgentsWithFoundry/Agent_Step23_LocalMCP).

---

## Create an agent by using the MCP tool with project connection authentication

In this example, you learn how to authenticate to the GitHub MCP server and use it as a tool for an agent. The example uses synchronous methods to create an agent. For asynchronous methods, see the [sample code](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Extensions.OpenAI/samples/Sample20_MCP_Connection.md) in the Azure SDK for .NET repository on GitHub.

#### Set up project connection

Before running the sample:

1. Sign in to your GitHub profile.
1. Select the profile picture at the upper right corner.
1. Select **Settings**.
1. In the left panel, select **Developer Settings** and **Personal access tokens > Tokens (classic)**.
1. At the top, select **Generate new token**, enter your password, and create a token that can read public repositories.
   - **Important:** Save the token, or keep the page open as once the page is closed, token can't be shown again.
1. In the Azure portal, open Microsoft Foundry.
1. In the left panel, select **Management center** and then select **Connected resources**.
1. Create new connection of **Custom keys** type.
1. Name it and add a key value pair.
1. Set the key name to `Authorization` and the value should have a form of `Bearer your_github_token`.

### Code sample to create the agent

```csharp
using System;
using Azure.AI.Projects;
using Azure.AI.Extensions.OpenAI;
using Azure.Identity;

// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
var projectEndpoint = "your_project_endpoint";
var mcpConnectionName = "my-mcp-connection";

// Create project client to call Foundry API
AIProjectClient projectClient = new(
    endpoint: new Uri(projectEndpoint),
    tokenProvider: new DefaultAzureCredential());

// Create an agent with the MCPTool. Note that, in this scenario,
// GlobalMcpToolCallApprovalPolicy.AlwaysRequireApproval is used.
// This means that any calls to the MCP server must be approved.
// The ProjectConnectionId property is then set on the McpTool
// so agent can authenticate with GitHub.
McpTool tool = ResponseTool.CreateMcpTool(
        serverLabel: "api-specs",
        serverUri: new Uri("https://api.githubcopilot.com/mcp"),
        toolCallApprovalPolicy: new McpToolCallApprovalPolicy(GlobalMcpToolCallApprovalPolicy.AlwaysRequireApproval
    ));
tool.ProjectConnectionId = mcpConnectionName;
DeclarativeAgentDefinition agentDefinition = new(model: "gpt-5-mini")
{
    Instructions = "You are a helpful agent that can use MCP tools to assist users. Use the available MCP tools to answer questions and perform tasks.",
    Tools = { tool }
};
AgentVersion agentVersion = projectClient.AgentAdministrationClient.CreateAgentVersion(
    agentName: "myAgent",
    options: new(agentDefinition));

// If the tool approval is required, the response item is
// of McpToolCallApprovalRequestItem type and contains all
// the information about tool call. This example checks that
// the server label is "api-specs" and approves the tool call,
// All other calls are denied because they shouldn't happen given
// the current configuration.
ProjectResponsesClient responseClient = projectClient.ProjectOpenAIClient.GetProjectResponsesClientForAgent(agentVersion.Name);

CreateResponseOptions nextResponseOptions = new([ResponseItem.CreateUserMessageItem("What is my username in my GitHub profile?")]);
ResponseResult latestResponse = null;

while (nextResponseOptions is not null)
{
    latestResponse = responseClient.CreateResponse(nextResponseOptions);
    nextResponseOptions = null;

    foreach (ResponseItem responseItem in latestResponse.OutputItems)
    {
        if (responseItem is McpToolCallApprovalRequestItem mcpToolCall)
        {
            nextResponseOptions = new()
            {
                PreviousResponseId = latestResponse.Id,
            };
            if (string.Equals(mcpToolCall.ServerLabel, "api-specs"))
            {
                Console.WriteLine($"Approval requested for {mcpToolCall.ServerLabel} (tool: {mcpToolCall.ToolName})");
                Console.Write("Approve this MCP tool call? (y/N): ");
                bool approved = string.Equals(Console.ReadLine(), "y", StringComparison.OrdinalIgnoreCase);
                nextResponseOptions.InputItems.Add(ResponseItem.CreateMcpApprovalResponseItem(approvalRequestId: mcpToolCall.Id, approved: approved));
            }
            else
            {
                Console.WriteLine($"Rejecting unknown call {mcpToolCall.ServerLabel}...");
                nextResponseOptions.InputItems.Add(ResponseItem.CreateMcpApprovalResponseItem(approvalRequestId: mcpToolCall.Id, approved: false));
            }
        }
    }
}

// Output the final response from the agent.
Console.WriteLine(latestResponse.GetOutputText());

// Clean up resources by deleting the agent version.
projectClient.AgentAdministrationClient.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

### Expected output

The following example shows the expected output when you run the sample:

```console
Approval requested for api-specs...
Response: Your GitHub username is "example-username".
```
:::zone-end

:::zone pivot="typescript"
## Create an agent in TypeScript with the MCP tool

The following TypeScript sample demonstrates how to create an agent with MCP tool capabilities, send requests that trigger MCP approval workflows, handle approval requests, and clean up resources. For a JavaScript version, see the [sample code](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2-beta/javascript/agents/tools/agentMcp.js) on the Azure SDK for JavaScript repository on GitHub.

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import OpenAI from "openai";
import * as readline from "readline";

// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
const PROJECT_ENDPOINT = "your_project_endpoint";

export async function main(): Promise<void> {
  // Create clients to call Foundry API
  const project = new AIProjectClient(PROJECT_ENDPOINT, new DefaultAzureCredential());
  const openai = project.getOpenAIClient();

  console.log("Creating agent with MCP tool...");

  // Define MCP tool that connects to Azure REST API specifications GitHub repository
  // The tool requires approval for each operation to ensure user control over external requests
  const agent = await project.agents.createVersion("agent-mcp", {
    kind: "prompt",
    model: "gpt-5-mini",
    instructions:
      "You are a helpful agent that can use MCP tools to assist users. Use the available MCP tools to answer questions and perform tasks.",
    tools: [
      {
        type: "mcp",
        server_label: "api-specs",
        server_url: "https://gitmcp.io/Azure/azure-rest-api-specs",
        require_approval: "always",
      },
    ],
  });
  console.log(`Agent created (id: ${agent.id}, name: ${agent.name}, version: ${agent.version})`);

  // Create a conversation thread to maintain context across multiple interactions
  console.log("\nCreating conversation...");
  const conversation = await openai.conversations.create();
  console.log(`Created conversation (id: ${conversation.id})`);

  // Send initial request that will trigger the MCP tool to access Azure REST API specs
  // This will generate an approval request since requireApproval="always"
  console.log("\nSending request that will trigger MCP approval...");
  const response = await openai.responses.create(
    {
      conversation: conversation.id,
      input: "Please summarize the Azure REST API specifications Readme",
    },
    {
      body: { agent: { name: agent.name, type: "agent_reference" } },
    },
  );

  // Process any MCP approval requests that were generated
  // When requireApproval="always", the agent will request permission before accessing external resources
  const inputList: OpenAI.Responses.ResponseInputItem.McpApprovalResponse[] = [];

  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  const ask = (q: string) => new Promise<string>((resolve) => rl.question(q, resolve));
  for (const item of response.output) {
    if (item.type === "mcp_approval_request") {
      if (item.server_label === "api-specs" && item.id) {
        console.log(`\nReceived MCP approval request (id: ${item.id})`);
        console.log(`  Server: ${item.server_label}`);
        console.log(`  Tool: ${item.name}`);

        // Approve only after you review the tool call.
        // In production, implement your own approval UX and policy.
        const answer = (await ask("Approve this MCP tool call? (y/N): ")).trim().toLowerCase();
        const approve = answer === "y";
        inputList.push({
          type: "mcp_approval_response",
          approval_request_id: item.id,
          approve,
        });
      }
    }
  }

  rl.close();

  console.log(`\nProcessing ${inputList.length} approval request(s)`);
  console.log("Final input:");
  console.log(JSON.stringify(inputList, null, 2));

  // Send the approval response back to continue the agent's work
  // This allows the MCP tool to access the GitHub repository and complete the original request
  console.log("\nSending approval response...");
  const finalResponse = await openai.responses.create(
    {
      input: inputList,
      previous_response_id: response.id,
    },
    {
      body: { agent: { name: agent.name, type: "agent_reference" } },
    },
  );

  console.log(`\nResponse: ${finalResponse.output_text}`);

  // Clean up resources by deleting the agent version and conversation
  // This prevents accumulation of unused resources in your project
  console.log("\nCleaning up resources...");
  await openai.conversations.delete(conversation.id);
  console.log("Conversation deleted");

  await project.agents.deleteVersion(agent.name, agent.version);
  console.log("Agent deleted");

  console.log("\nMCP sample completed!");
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

### Expected output

The following example shows the expected output when you run the sample:

```console
Creating agent with MCP tool...
Agent created (id: <agent-id>, name: agent-mcp, version: 1)

Creating conversation...
Created conversation (id: <conversation-id>)

Sending request that will trigger MCP approval...

Received MCP approval request (id: <approval-request-id>)
  Server: api-specs
  Tool: get-readme

Processing 1 approval request(s)
Final input:
[
  {
    "type": "mcp_approval_response",
    "approval_request_id": "<approval-request-id>",
    "approve": true
  }
]

Sending approval response...

Response: The Azure REST API specifications repository contains the OpenAPI specifications for Azure services. It is organized by service and includes guidelines for contributing new specifications. The repository is intended for use by developers building tools and services that interact with Azure APIs.

Cleaning up resources...
Conversation deleted
Agent deleted

MCP sample completed!
```

## Create an agent by using the MCP tool with project connection authentication

The following TypeScript sample demonstrates how to create an agent with MCP tool capabilities using project connection authentication, send requests that trigger MCP approval workflows, handle approval requests, and clean up resources. For a JavaScript version, see the [sample code](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2-beta/javascript/agents/tools/agentMcpConnectionAuth.js) on the Azure SDK for JavaScript repository on GitHub.

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import OpenAI from "openai";
import * as readline from "readline";

// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
const PROJECT_ENDPOINT = "your_project_endpoint";
const MCP_CONNECTION_NAME = "my-mcp-connection";

export async function main(): Promise<void> {
  // Create clients to call Foundry API
  const project = new AIProjectClient(PROJECT_ENDPOINT, new DefaultAzureCredential());
  const openai = project.getOpenAIClient();

  console.log("Creating agent with MCP tool using project connection...");

  // Define MCP tool that connects to GitHub Copilot API with project connection authentication
  // The project connection should have Authorization header configured with "Bearer <GitHub PAT token>"
  // Token can be created at https://github.com/settings/personal-access-tokens/new
  const agent = await project.agents.createVersion("agent-mcp-connection-auth", {
    kind: "prompt",
    model: "gpt-5-mini",
    instructions: "Use MCP tools as needed",
    tools: [
      {
        type: "mcp",
        server_label: "api-specs",
        server_url: "https://api.githubcopilot.com/mcp",
        require_approval: "always",
        project_connection_id: MCP_CONNECTION_NAME,
      },
    ],
  });
  console.log(`Agent created (id: ${agent.id}, name: ${agent.name}, version: ${agent.version})`);

  // Create a conversation thread to maintain context across multiple interactions
  console.log("\nCreating conversation...");
  const conversation = await openai.conversations.create();
  console.log(`Created conversation (id: ${conversation.id})`);

  // Send initial request that will trigger the MCP tool
  console.log("\nSending request that will trigger MCP approval...");
  const response = await openai.responses.create(
    {
      conversation: conversation.id,
      input: "What is my username in my GitHub profile?",
    },
    {
      body: { agent: { name: agent.name, type: "agent_reference" } },
    },
  );

  // Process any MCP approval requests that were generated
  const inputList: OpenAI.Responses.ResponseInputItem.McpApprovalResponse[] = [];

  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  const ask = (q: string) => new Promise<string>((resolve) => rl.question(q, resolve));
  for (const item of response.output) {
    if (item.type === "mcp_approval_request") {
      if (item.server_label === "api-specs" && item.id) {
        console.log(`\nReceived MCP approval request (id: ${item.id})`);
        console.log(`  Server: ${item.server_label}`);
        console.log(`  Tool: ${item.name}`);

        // Approve only after you review the tool call.
        // In production, implement your own approval UX and policy.
        const answer = (await ask("Approve this MCP tool call? (y/N): ")).trim().toLowerCase();
        const approve = answer === "y";
        inputList.push({
          type: "mcp_approval_response",
          approval_request_id: item.id,
          approve,
        });
      }
    }
  }

  rl.close();

  console.log(`\nProcessing ${inputList.length} approval request(s)`);
  console.log("Final input:");
  console.log(JSON.stringify(inputList, null, 2));

  // Send the approval response back to continue the agent's work
  // This allows the MCP tool to access the GitHub repository and complete the original request
  console.log("\nSending approval response...");
  const finalResponse = await openai.responses.create(
    {
      input: inputList,
      previous_response_id: response.id,
    },
    {
      body: { agent: { name: agent.name, type: "agent_reference" } },
    },
  );

  console.log(`\nResponse: ${finalResponse.output_text}`);

  // Clean up resources by deleting the agent version and conversation
  // This prevents accumulation of unused resources in your project
  console.log("\nCleaning up resources...");
  await openai.conversations.delete(conversation.id);
  console.log("Conversation deleted");

  await project.agents.deleteVersion(agent.name, agent.version);
  console.log("Agent deleted");

  console.log("\nMCP with project connection sample completed!");
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

### Expected output

The following example shows the expected output when you run the sample:

```console
Creating agent with MCP tool using project connection...
Agent created (id: <agent-id>, name: agent-mcp-connection-auth, version: 1)
Creating conversation...
Created conversation (id: <conversation-id>)
Sending request that will trigger MCP approval...
Received MCP approval request (id: <approval-request-id>)
  Server: api-specs
  Tool: get-github-username
Processing 1 approval request(s)
Final input:
[
  {
    "type": "mcp_approval_response",
    "approval_request_id": "<approval-request-id>",
    "approve": true
  }
]
Sending approval response...
Response: Your GitHub username is "example-username".
Cleaning up resources...
Conversation deleted
Agent deleted
MCP with project connection sample completed!
```
:::zone-end

:::zone pivot="java"

## Use MCP tools in a Java agent

Add the dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-agents</artifactId>
    <version>2.0.0</version>
</dependency>
```

### Create an agent with MCP tool

```java
import com.azure.ai.agents.AgentsClient;
import com.azure.ai.agents.AgentsClientBuilder;
import com.azure.ai.agents.ResponsesClient;
import com.azure.ai.agents.models.AgentReference;
import com.azure.ai.agents.models.AgentVersionDetails;
import com.azure.ai.agents.models.AzureCreateResponseOptions;
import com.azure.ai.agents.models.McpTool;
import com.azure.ai.agents.models.PromptAgentDefinition;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

import java.util.Collections;

public class McpToolExample {
    public static void main(String[] args) {
        // Format: "https://resource_name.ai.azure.com/api/projects/project_name"
        String projectEndpoint = "your_project_endpoint";
        String mcpConnectionName = "my-mcp-connection";

        AgentsClientBuilder builder = new AgentsClientBuilder()
            .credential(new DefaultAzureCredentialBuilder().build())
            .endpoint(projectEndpoint);

        AgentsClient agentsClient = builder.buildAgentsClient();
        ResponsesClient responsesClient = builder.buildResponsesClient();

        // Create MCP tool with server label, URL, connection, and approval mode
        McpTool mcpTool = new McpTool("api-specs")
            .setServerUrl("https://gitmcp.io/Azure/azure-rest-api-specs")
            .setProjectConnectionId(mcpConnectionName)
            .setRequireApproval("always");

        // Create agent with MCP tool
        PromptAgentDefinition agentDefinition = new PromptAgentDefinition("gpt-5-mini")
            .setInstructions("You are a helpful assistant that can use MCP tools.")
            .setTools(Collections.singletonList(mcpTool));

        AgentVersionDetails agent = agentsClient.createAgentVersion("mcp-agent", agentDefinition);
        System.out.printf("Agent created: %s (version %s)%n", agent.getName(), agent.getVersion());

        // Create a response
        AgentReference agentReference = new AgentReference(agent.getName())
            .setVersion(agent.getVersion());

        Response response = responsesClient.createAzureResponse(
            new AzureCreateResponseOptions().setAgentReference(agentReference),
            ResponseCreateParams.builder()
                .input("Summarize the Azure REST API specifications"));

        System.out.println("Response: " + response.output());

        // Clean up
        agentsClient.deleteAgentVersion(agent.getName(), agent.getVersion());
    }
}
```

### Expected output

```output
Agent created: mcp-agent (version 1)
Response: [ResponseOutputItem containing MCP tool results ...]
```

:::zone-end

:::zone pivot="rest"
## Use the MCP tool with the REST API

The following examples show how to create an agent with the MCP tool and call it by using the Responses API. If the response includes an output item with `type` set to `mcp_approval_request`, send a follow-up request that includes a `mcp_approval_response` item.

### Prerequisites

Set these environment variables:

- `FOUNDRY_PROJECT_ENDPOINT`: Your project endpoint URL.
- `FOUNDRY_MODEL_DEPLOYMENT_NAME`: Your model deployment name.
- `AGENT_TOKEN`: A bearer token for Foundry.
- `MCP_PROJECT_CONNECTION_NAME` (optional): Your MCP project connection name.

Get an access token:

```bash
export AGENT_TOKEN=$(az account get-access-token --scope "https://ai.azure.com/.default" --query accessToken -o tsv)
```

If your MCP server doesn't require authentication, omit `project_connection_id` from the request body.

> [!NOTE]
> For REST API, you need to first retrieve the connection ID from the connection name using the Connections API, then pass the ID to the MCP tool configuration.

> [!TIP]
> For details on the MCP tool schema and approval items, see [OpenAI.MCPTool](../../../reference/foundry-project-rest-preview.md#openaimcptool) and the MCP approval item types in the REST reference.

### 1. Create an MCP agent

```bash
curl -X POST "$FOUNDRY_PROJECT_ENDPOINT/agents?api-version=v1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -d '{
    "name": "<AGENT_NAME>-mcp",
    "description": "MCP agent",
    "definition": {
      "kind": "prompt",
      "model": "'$FOUNDRY_MODEL_DEPLOYMENT_NAME'",
      "instructions": "You are a helpful agent that can use MCP tools to assist users. Use the available MCP tools to answer questions and perform tasks.",
      "tools": [
        {
          "type": "mcp",
          "server_label": "api-specs",
          "server_url": "https://gitmcp.io/Azure/azure-rest-api-specs",
          "require_approval": "never"
        }
      ]
    }
  }'
```

To use an authenticated MCP server with a project connection, add `"project_connection_id": "'$MCP_PROJECT_CONNECTION_NAME'"` to the tool definition and change `server_url` to the authenticated server endpoint (for example, `https://api.githubcopilot.com/mcp`).

### 2. Create a response

```bash
curl -X POST "$FOUNDRY_PROJECT_ENDPOINT/openai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -d '{
    "agent": {"type": "agent_reference", "name": "<AGENT_NAME>-mcp"},
    "input": "Please summarize the Azure REST API specifications Readme"
  }'
```

If the response includes an output item with `type` set to `mcp_approval_request`, copy the approval request item `id` as `APPROVAL_REQUEST_ID`. Also copy the top-level response `id` as `PREVIOUS_RESPONSE_ID`.

### 3. Send an approval response

If the MCP tool requires approval, send a follow-up request:

```bash
curl -X POST "$FOUNDRY_PROJECT_ENDPOINT/openai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -d '{
    "previous_response_id": "'$PREVIOUS_RESPONSE_ID'",
    "input": [
      {
        "type": "mcp_approval_response",
        "approval_request_id": "'$APPROVAL_REQUEST_ID'",
        "approve": true
      }
    ]
  }'
```

### 4. Clean up resources

Delete the agent:

```bash
curl -X DELETE "$FOUNDRY_PROJECT_ENDPOINT/agents/<AGENT_NAME>-mcp?api-version=v1" \
  -H "Authorization: Bearer $AGENT_TOKEN"
```

:::zone-end

## How it works

You need to bring a remote MCP server (an existing MCP server endpoint) to Foundry Agent Service. You can bring multiple remote MCP servers by adding them as tools. For each tool, you need to provide a unique `server_label` value within the same agent and a `server_url` value that points to the remote MCP server. Be sure to carefully review which MCP servers you add to Foundry Agent Service.

In addition to connecting arbitrary remote MCP servers by URL, some MCP servers can be added directly from the Foundry **Add Tools** catalog. For example, Azure DevOps MCP Server (preview) is available as a catalog entry. Catalog entries simplify connection setup and align with the same approval and auditing mechanisms documented in this article.

For more information on using MCP, see:

- [Security Best Practices](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices) on the Model Context Protocol website.
- [Understanding and mitigating security risks in MCP implementations](https://techcommunity.microsoft.com/blog/microsoft-security-blog/understanding-and-mitigating-security-risks-in-mcp-implementations/4404667) in the Microsoft Security Community Blog.

## Set up the MCP connection

The following steps outline how to connect to a remote MCP server from Foundry Agent Service:

1. Find the remote MCP server that you want to connect to, such as the GitHub MCP server. Create or update a Foundry agent with an `mcp` tool by using the following information:
   1. `server_url`: The URL of the MCP server, such as `https://api.githubcopilot.com/mcp/`.
   1. `server_label`: A unique identifier of this MCP server to the agent, such as `github`.
   1. `allowed_tools`: An optional list of tools that this agent can access and use. If you don't provide this value, the default value includes all of the tools in the MCP server.
   1. `require_approval`: Optionally determine whether approval is required. The default value is `always`. Supported values are:
      - `always`: A developer needs to provide approval for every call. If you don't provide a value, this one is the default.
      - `never`: No approval is required.
      - `{"never":[<tool_name_1>, <tool_name_2>]}`: You provide a list of tools that don't require approval.
      - `{"always":[<tool_name_1>, <tool_name_2>]}`: You provide a list of tools that require approval.
  1. `project_connection_id`: The project connection ID that stores authentication and other connection details for the MCP server.
1. If the model tries to invoke a tool in your MCP server with approval required, you get a response output item type as `mcp_approval_request`. In the response output item, you can get more details on which tool in the MCP server is called and arguments to be passed. Review the tool and arguments so that you can make an informed decision for approval.
1. Submit your approval to the agent by using `previous_response_id` and setting `approve` to `true`.

### Connect to Azure DevOps MCP Server

Azure DevOps MCP Server (preview) is available as a catalog entry in Foundry. To add it:

1. In [Foundry portal](https://ai.azure.com), go to your project.
1. Select **Add Tools** > **Catalog** and search for "Azure DevOps."
1. Select **Azure DevOps MCP Server (preview)** and select **Create**.
1. Enter your Azure DevOps organization name and select **Connect**.
1. Choose which Azure DevOps tools to expose to your agent. You can select a subset of tools to control exactly what the agent can access.

This catalog-based setup creates the MCP tool for use by agents without requiring code changes. You can validate connectivity and tool behavior in the Foundry chat testing experience before integrating the tool into production code.

> [!TIP]
> **Toolbox versioning**: Foundry Toolboxes support versioning, so you can iterate on a new version without affecting production agents. Use the **consumer endpoint** (`{project_endpoint}/toolboxes/{name}/mcp?api-version=v1`) for production agents - it always serves the promoted default version. Use the **version-specific endpoint** (`{project_endpoint}/toolboxes/{name}/versions/{version}/mcp?api-version=v1`) to test before promoting. Keep `server_label` unique per agent, even when switching Toolbox versions. For details, see [Promote a version to default](toolbox.md#promote-a-version-to-default).

## Long-running operations

Some MCP servers expose tools that take longer than the standard synchronous timeout to return a result. To support these operations, run the agent in [background mode](../../concepts/runtime-components.md#run-an-agent-in-background-mode). Background mode runs the response asynchronously, so the MCP tool call can continue without holding an open connection, and you poll for the response status until it completes. This approach lets MCP tool calls exceed the 100-second non-streaming timeout described in [Known limitations](#known-limitations).

The MCP server must implement the long-running operation on the server side. The agent runtime starts the response, returns immediately with a response `id` and a `status` of `queued`, and processes the MCP tool call in the background. You poll the response `id` until `status` becomes `completed`, then read the final output.

Background mode for long-running MCP operations is supported only with the following models:

- `gpt-5.5`
- `gpt-5.5-pro`
- `gpt-5.4`
- `gpt-5.4-pro`
- `gpt-5.4-mini`
- `gpt-5.4-nano`

If your agent uses a model that isn't in this list, MCP tool calls run synchronously and are subject to the 100-second timeout.

The following examples invoke an agent that's already configured with an MCP tool, set `background` to `true`, and poll until the response completes. Replace the placeholder values with your own.

# [Python](#tab/lro-python)

```python
from time import sleep
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

PROJECT_ENDPOINT = "your_project_endpoint"
AGENT_NAME = "your_mcp_agent_name"

project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()

# Start a background response. It returns immediately with status "queued".
response = openai.responses.create(
    extra_body={
        "agent_reference": {
            "name": AGENT_NAME,
            "type": "agent_reference",
        }
    },
    input="Run the long-running task and summarize the result.",
    background=True,
)

# Poll the response ID until the MCP tool call completes.
while response.status in ("queued", "in_progress"):
    sleep(5)
    response = openai.responses.retrieve(response.id)

print(response.output_text)
```

# [JavaScript](#tab/lro-javascript)

```javascript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";

const PROJECT_ENDPOINT = "your_project_endpoint";
const AGENT_NAME = "your_mcp_agent_name";

const project = new AIProjectClient(PROJECT_ENDPOINT, new DefaultAzureCredential());
const openai = await project.getOpenAIClient();

// Start a background response. It returns immediately with status "queued".
let response = await openai.responses.create({
  input: "Run the long-running task and summarize the result.",
  background: true,
  agent_reference: {
    name: AGENT_NAME,
    type: "agent_reference",
  },
});

// Poll the response ID until the MCP tool call completes.
while (response.status === "queued" || response.status === "in_progress") {
  await new Promise((r) => setTimeout(r, 5000));
  response = await openai.responses.retrieve(response.id);
}
console.log(response.output_text);
```

# [C#](#tab/lro-csharp)

```csharp
using Azure.Identity;
using Azure.AI.Projects;

var projectEndpoint = "your_project_endpoint";
var agentName = "your_mcp_agent_name";

AIProjectClient projectClient = new(
    endpoint: new Uri(projectEndpoint),
    tokenProvider: new DefaultAzureCredential());

ProjectResponsesClient responsesClient
    = projectClient.ProjectOpenAIClient.GetProjectResponsesClientForAgent(agentName);

// Start a background response. It returns immediately with status "queued".
ResponseResult response = await responsesClient.CreateResponseAsync(
    new CreateResponseOptions
    {
        InputItems = { ResponseItem.CreateUserMessageItem(
            "Run the long-running task and summarize the result.") },
        Background = true,
    });

// Poll the response ID until the MCP tool call completes.
while (response.Status is "queued" or "in_progress")
{
    await Task.Delay(5000);
    response = await responsesClient.RetrieveResponseAsync(response.Id);
}
Console.WriteLine(response.GetOutputText());
```

# [REST](#tab/lro-rest)

Create a background response. The request returns immediately with a response `id` and a `status` of `queued`:

```bash
curl -X POST "$FOUNDRY_PROJECT_ENDPOINT/openai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -d '{
    "agent": {"type": "agent_reference", "name": "<AGENT_NAME>-mcp"},
    "input": "Run the long-running task and summarize the result.",
    "background": true
  }'
```

Copy the response `id` from the result, then poll it until `status` is `completed`:

```bash
curl "$FOUNDRY_PROJECT_ENDPOINT/openai/v1/responses/$RESPONSE_ID" \
  -H "Authorization: Bearer $AGENT_TOKEN"
```

When `status` is `completed`, the `output` array contains the MCP tool call result and the final assistant message.

---

## Known limitations

- **Non-streaming MCP tool call timeout**: Non-streaming MCP tool calls have a timeout of 100 seconds. If your MCP server takes longer than 100 seconds to respond, the call fails. To avoid timeouts, ensure that your MCP server responds within this limit. If your use case requires longer processing times, run the agent in [background mode](#long-running-operations) with a supported model, optimize the server-side logic, or break the operation into smaller steps.
- **Private MCP requires Standard Agent Setup**: Private MCP server connectivity is only available with [Standard Agent Setup with private networking](../virtual-networks.md) (BYO VNet). Basic agent setup doesn't support private MCP endpoints.
- **Private MCP hosting**: Azure Container Apps on a dedicated MCP subnet is the tested configuration for private MCP servers. Function Apps or App Services as the private MCP server host might work but aren't internally validated.

## Common questions and errors

The following common issues might occur when you use MCP tools with Foundry Agent Service:

- "Invalid tool schema":

    This error usually happens if your MCP server definition includes `anyOf` or `allOf`, or if a parameter accepts multiple types of values. Update your MCP server definition and try again.

- "Unauthorized" or "Forbidden" from the MCP server:

    Confirm the MCP server supports your authentication method, and verify the credentials stored in your project connection. For GitHub, use least-privilege tokens and rotate them regularly.

- The model never calls your MCP tool:

    Confirm your agent instructions encourage tool usage, and verify `server_label`, `server_url`, and `allowed_tools` values. If you set `allowed_tools`, make sure the tool name matches what the MCP server exposes.

- The agent never continues after approval:

    Confirm you send a follow-up request with `previous_response_id` set to the original response ID, and that you use the approval request item ID as `approval_request_id`.

## Host a local MCP server

The Agent Service runtime only accepts a remote MCP server endpoint. If you want to add tools from a local MCP server, you need to self-host it on [Azure Container Apps](https://github.com/Azure-Samples/mcp-container-ts) or [Azure Functions](https://github.com/Azure-Samples/mcp-sdk-functions-hosting-python/tree/main) to get a remote MCP server endpoint.

The remote endpoint can be either a public endpoint or a private endpoint within your VNet. For private MCP servers, deploy your Container App with internal-only ingress (`--internal-only true`) on a dedicated MCP subnet. See [Public and private MCP server endpoints](#public-and-private-mcp-server-endpoints) for setup details.

Consider the following factors when hosting local MCP servers in the cloud:

| Local MCP server setup | Hosting in Azure Container Apps | Hosting in Azure Functions |
| --- | --- | --- |
| **Transport** | HTTP POST/GET endpoints required. | HTTP streamable required. |
| **Code changes** | Container rebuild required. | Azure Functions-specific configuration files required in the root directory. |
| **Authentication** | Custom authentication implementation required. | Key-based only. OAuth needs API Management. |
| **Language** | Any language that runs in Linux containers (Python, Node.js, .NET, TypeScript, Go). | Python, Node.js, Java, .NET only. |
| **Container requirements** | Linux (linux/amd64) only. No privileged containers. | Containerized servers aren't supported. |
| **Dependencies** | All dependencies must be in container image. | OS-level dependencies (such as Playwright) aren't supported. |
| **State** | Stateless only. | Stateless only. |
| **UVX/NPX** | Supported. | Not supported. `npx` start commands not supported. |

## Related content

- [Get started with agents using code](../../../quickstarts/get-started-code.md)
- [MCP server authentication](../mcp-authentication.md)
- [Build and register a Model Context Protocol (MCP) server](../../../mcp/build-your-own-mcp-server.md)
- [Set up private networking for Foundry Agent Service](../virtual-networks.md)
- [Configure private link for Foundry](../../../how-to/configure-private-link.md)
- [MCP tool REST reference](../../../reference/foundry-project-rest-preview.md#openaimcptool)
- [Security Best Practices for MCP](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices)
- [Understanding and mitigating security risks in MCP implementations](https://techcommunity.microsoft.com/blog/microsoft-security-blog/understanding-and-mitigating-security-risks-in-mcp-implementations/4404667)
