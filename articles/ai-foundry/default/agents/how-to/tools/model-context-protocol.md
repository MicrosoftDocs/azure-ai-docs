---
title: Connect to MCP Server Endpoints for agents (Preview)
titleSuffix: Microsoft Foundry
description: Connect your Foundry agents to Model Context Protocol (MCP) servers using the MCP tool. Extend capabilities with external tools and data.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 02/09/2026
author: alvinashcraft
ms.author: aashcraft
ai-usage: ai-assisted
zone_pivot_groups: selection-mcp-code-new
ms.custom: dev-focus, pilot-ai-workflow-jan-2026
#CustomerIntent: As a developer, I want to connect my Foundry agent to external MCP servers so that I can extend agent capabilities with third-party tools.
---

# Connect agents to Model Context Protocol servers (preview)

[!INCLUDE [feature-preview](../../../../includes/feature-preview.md)]

> [!NOTE]
> When you use a [Network Secured Microsoft Foundry](../../../../agents/how-to/virtual-networks.md), you can't use private MCP servers deployed in the same virtual network. You can only use publicly accessible MCP servers.

Connect your Foundry agents to [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) servers by using the MCP tool. This extends agent capabilities with external tools and data sources. By connecting to remote MCP server endpoints, your agents can access tools hosted by developers and organizations that MCP-compatible clients like Foundry Agent Service can use.

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
| ✔️ | ✔️ | ✔️ | ✔️ | - | ✔️ | ✔️ | ✔️ |

## Prerequisites

Before you begin, ensure you have:

- An Azure subscription with an active Microsoft Foundry project.
- Azure role-based access control (RBAC): Contributor or Owner role on the Foundry project.
- The latest prerelease SDK package for your language. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true) for installation details.
- Azure credentials configured for authentication (such as `DefaultAzureCredential`).
- Environment variables configured:
  - `AZURE_AI_PROJECT_ENDPOINT` or `FOUNDRY_PROJECT_ENDPOINT`: Your project endpoint URL.
  - `AZURE_AI_MODEL_DEPLOYMENT_NAME` or `MODEL_DEPLOYMENT_NAME`: Your model deployment name.
  - `MCP_PROJECT_CONNECTION_NAME`: Your MCP project connection name.
- Access to a remote MCP server endpoint (such as GitHub's MCP server at `https://api.githubcopilot.com/mcp`).

## Authentication

Many MCP servers require authentication.

In Foundry Agent Service, use a project connection to store authentication details (for example, API keys or bearer tokens) instead of hard-coding credentials in your app.

To learn about supported authentication options (key-based, Microsoft Entra identities, and OAuth identity passthrough), see [MCP server authentication](../mcp-authentication.md).

> [!NOTE]
> Set `project_connection_id` to the ID of your project connection.

<!-- The verbiage in the following section is required. Do not remove or modify. -->
## Considerations for using non-Microsoft services and servers

You're subject to the terms between you and the service provider when you use connected non-Microsoft services. When you connect to a non-Microsoft service, you pass some of your data (such as prompt content) to the non-Microsoft service, or your application might receive data from the non-Microsoft service. You're responsible for your use of non-Microsoft services and data, along with any charges associated with that use.

Third parties, not Microsoft, create the remote MCP servers that you decide to use with the MCP tool described in this article. Microsoft doesn't test or verify these servers. Microsoft has no responsibility to you or others in relation to your use of any remote MCP servers.

Carefully review and track what MCP servers you add to Foundry Agent Service. Rely on servers hosted by trusted service providers themselves rather than proxies.

The MCP tool allows you to pass custom headers, such as authentication keys or schemas, that a remote MCP server might need. Review all data that you share with remote MCP servers and log the data for auditing purposes. Be aware of non-Microsoft practices for retention and location of data.

## Best practices

For general guidance on tool usage, see [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md).

When you use MCP servers, follow these practices:

- Prefer an allow-list of tools by using `allowed_tools`.
- Require approval for high-risk operations (especially tools that write data or change resources).
- Review the requested tool name and arguments before you approve.
- Log approvals and tool calls for auditing and troubleshooting.

## Create an agent in Python with the MCP tool

Use the following code sample to create an agent and call the function. You need the latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true) for details.

:::zone pivot="python"

### Quick verification

Before running the full sample, verify your project connection (optional, for authenticated MCP servers):

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
    
    # Verify MCP connection exists (optional - only needed for authenticated servers)
    connection_name = os.environ.get("MCP_PROJECT_CONNECTION_NAME")
    if connection_name:
        try:
            conn = project_client.connections.get(connection_name)
            print(f"MCP connection verified: {conn.name}")
        except Exception as e:
            print(f"MCP connection '{connection_name}' not found: {e}")
    else:
        print("MCP_PROJECT_CONNECTION_NAME not set (optional for unauthenticated servers).")
        print("Available connections:")
        for conn in project_client.connections.list():
            print(f"  - {conn.name}")
```

If this code runs without errors, your credentials are configured correctly. For authenticated MCP servers, ensure your connection exists.

### Full sample

The following example shows how to use the GitHub MCP server as a tool for an agent.

```python
import os
import json
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, MCPTool, Tool
from openai.types.responses.response_input_param import McpApprovalResponse, ResponseInputParam

load_dotenv()

endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
    project_client.get_openai_client() as openai_client,
):

    # [START tool_declaration]
    tool = MCPTool(
        server_label="api-specs",
        server_url="https://api.githubcopilot.com/mcp",
        require_approval="always",
        project_connection_id=os.getenv("MCP_PROJECT_CONNECTION_NAME"),
    )
    # [END tool_declaration]

    # Create a prompt agent with MCP tool capabilities
    agent = project_client.agents.create_version(
        agent_name="MyAgent7",
        definition=PromptAgentDefinition(
            model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
            instructions="Use MCP tools as needed",
            tools=[tool],
        ),
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    # Create a conversation to maintain context across multiple interactions
    conversation = openai_client.conversations.create()
    print(f"Created conversation (id: {conversation.id})")

    # Send initial request that will trigger the MCP tool
    response = openai_client.responses.create(
        conversation=conversation.id,
        input="What is my username in my GitHub profile?",
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
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

    print("Final input:")
    print(input_list)

    # Send the approval response back to continue the agent's work
    # This allows the MCP tool to access the GitHub repository and complete the original request
    response = openai_client.responses.create(
        input=input_list,
        previous_response_id=response.id,
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )

    print(f"Response: {response.output_text}")

    # Clean up resources by deleting the agent version
    # This prevents accumulation of unused agent versions in your project
    project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
    print("Agent deleted")
```

### Expected output

The following example shows the expected output when you run the sample:

```console
Agent created (id: <agent-id>, name: MyAgent7, version: 1)
Created conversation (id: <conversation-id>)
Final input:
[McpApprovalResponse(type='mcp_approval_response', approve=True, approval_request_id='<approval-request-id>')]
Response: Your GitHub username is "example-username".
Agent deleted
```

:::zone-end

:::zone pivot="csharp"
## Create an agent with MCP tool

The following example shows how to use the GitHub MCP server as a tool for an agent. The example uses synchronous methods to create an agent. For asynchronous methods, see the [sample code](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample19_MCP.md) in the Azure SDK for .NET repository on GitHub.

```csharp
// Create project client and read the environment variables that are used in the next steps.
var projectEndpoint = System.Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("MODEL_DEPLOYMENT_NAME");
AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

// Create Agent with the `MCPTool`. Note that in this scenario 
// GlobalMcpToolCallApprovalPolicy.AlwaysRequireApproval is used,
// which means that any calls to the MCP server must be approved.
PromptAgentDefinition agentDefinition = new(model: modelDeploymentName)
{
    Instructions = "You are a helpful agent that can use MCP tools to assist users. Use the available MCP tools to answer questions and perform tasks.",
    Tools = { ResponseTool.CreateMcpTool(
        serverLabel: "api-specs",
        serverUri: new Uri("https://gitmcp.io/Azure/azure-rest-api-specs"),
        toolCallApprovalPolicy: new McpToolCallApprovalPolicy(GlobalMcpToolCallApprovalPolicy.AlwaysRequireApproval
    )) }
};
AgentVersion agentVersion = projectClient.Agents.CreateAgentVersion(
    agentName: "myAgent",
    options: new(agentDefinition));

// If the tool approval is required, the response item is
// of `McpToolCallApprovalRequestItem` type and contains all
// the information about tool call. This example checks that
// the server label is "api-specs" and approves the tool call.
// All other calls are denied because they should not occur for
// the current configuration.
ProjectResponsesClient responseClient = projectClient.OpenAI.GetProjectResponsesClientForAgent(agentVersion.Name);

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
projectClient.Agents.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

### Expected output

The following example shows the expected output when you run the sample:

```console
Approval requested for api-specs...
Response: The Azure REST API specifications repository contains the OpenAPI specifications for Azure services. It is
organized by service and includes guidelines for contributing new specifications. The repository is intended for use by developers building tools and services that interact with Azure APIs.
```

## Create an agent with the MCP tool using project connection authentication

### Quick verification

Before running the full sample, verify your project connection (optional, for authenticated MCP servers):

```csharp
using Azure.AI.Projects;
using Azure.Identity;

var projectEndpoint = System.Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT");
var mcpConnectionName = System.Environment.GetEnvironmentVariable("MCP_PROJECT_CONNECTION_NAME");

AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

Console.WriteLine("Connected to project.");

// Verify MCP connection exists (optional - only needed for authenticated servers)
if (!string.IsNullOrEmpty(mcpConnectionName))
{
    try
    {
        AIProjectConnection conn = projectClient.Connections.GetConnection(connectionName: mcpConnectionName);
        Console.WriteLine($"MCP connection verified: {conn.Name}");
    }
    catch (Exception ex)
    {
        Console.WriteLine($"MCP connection '{mcpConnectionName}' not found: {ex.Message}");
    }
}
else
{
    Console.WriteLine("MCP_PROJECT_CONNECTION_NAME not set (optional for unauthenticated servers).");
    Console.WriteLine("Available connections:");
    foreach (var conn in projectClient.Connections.GetConnections())
    {
        Console.WriteLine($"  - {conn.Name}");
    }
}
```

If this code runs without errors, your credentials are configured correctly. For authenticated MCP servers, ensure your connection exists.

### Full sample

In this example, you learn how to authenticate to the GitHub MCP server and use it as a tool for an agent. The example uses synchronous methods to create an agent. For asynchronous methods, see the [sample code](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample20_MCP_Connection.md) in the Azure SDK for .NET repository on GitHub.

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
// Create project client and read the environment variables to be used in the next steps.
var projectEndpoint = System.Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("MODEL_DEPLOYMENT_NAME");
var mcpConnectionName = System.Environment.GetEnvironmentVariable("MCP_PROJECT_CONNECTION_NAME");
AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

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
PromptAgentDefinition agentDefinition = new(model: modelDeploymentName)
{
    Instructions = "You are a helpful agent that can use MCP tools to assist users. Use the available MCP tools to answer questions and perform tasks.",
    Tools = { tool }
};
AgentVersion agentVersion = projectClient.Agents.CreateAgentVersion(
    agentName: "myAgent",
    options: new(agentDefinition));

// If the tool approval is required, the response item is
// of McpToolCallApprovalRequestItem type and contains all
// the information about tool call. This example checks that
// the server label is "api-specs" and approves the tool call,
// All other calls are denied because they shouldn't happen given
// the current configuration.
ProjectResponsesClient responseClient = projectClient.OpenAI.GetProjectResponsesClientForAgent(agentVersion.Name);

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
projectClient.Agents.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
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
import "dotenv/config";

import * as readline from "readline";

import * as readline from "readline";

const projectEndpoint = process.env["FOUNDRY_PROJECT_ENDPOINT"] || "<project endpoint>";
const deploymentName = process.env["MODEL_DEPLOYMENT_NAME"] || "<model deployment name>";

export async function main(): Promise<void> {
  // Create AI Project client
  const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());
  const openAIClient = await project.getOpenAIClient();

  console.log("Creating agent with MCP tool...");

  // Define MCP tool that connects to Azure REST API specifications GitHub repository
  // The tool requires approval for each operation to ensure user control over external requests
  const agent = await project.agents.createVersion("agent-mcp", {
    kind: "prompt",
    model: deploymentName,
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
  const conversation = await openAIClient.conversations.create();
  console.log(`Created conversation (id: ${conversation.id})`);

  // Send initial request that will trigger the MCP tool to access Azure REST API specs
  // This will generate an approval request since requireApproval="always"
  console.log("\nSending request that will trigger MCP approval...");
  const response = await openAIClient.responses.create(
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
  const finalResponse = await openAIClient.responses.create(
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
  await openAIClient.conversations.delete(conversation.id);
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

## Create an agent with the MCP tool using project connection authentication

### Quick verification

Before running the full sample, verify your project connection (optional, for authenticated MCP servers):

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import "dotenv/config";

const projectEndpoint = process.env["FOUNDRY_PROJECT_ENDPOINT"] || "<project endpoint>";
const mcpConnectionName = process.env["MCP_PROJECT_CONNECTION_NAME"] || "";

async function verifyConnection(): Promise<void> {
  const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());
  console.log("Connected to project.");

  // Verify MCP connection exists (optional - only needed for authenticated servers)
  if (mcpConnectionName) {
    try {
      const conn = await project.connections.get(mcpConnectionName);
      console.log(`MCP connection verified: ${conn.name}`);
    } catch (error) {
      console.log(`MCP connection '${mcpConnectionName}' not found: ${error}`);
    }
  } else {
    console.log("MCP_PROJECT_CONNECTION_NAME not set (optional for unauthenticated servers).");
    console.log("Available connections:");
    for await (const conn of project.connections.list()) {
      console.log(`  - ${conn.name}`);
    }
  }
}

verifyConnection().catch(console.error);
```

If this code runs without errors, your credentials are configured correctly. For authenticated MCP servers, ensure your connection exists.

### Full sample

The following TypeScript sample demonstrates how to create an agent with MCP tool capabilities using project connection authentication, send requests that trigger MCP approval workflows, handle approval requests, and clean up resources. For a JavaScript version, see the [sample code](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2-beta/javascript/agents/tools/agentMcpConnectionAuth.js) on the Azure SDK for JavaScript repository on GitHub.

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import OpenAI from "openai";
import "dotenv/config";

const projectEndpoint = process.env["FOUNDRY_PROJECT_ENDPOINT"] || "<project endpoint>";
const deploymentName = process.env["MODEL_DEPLOYMENT_NAME"] || "<model deployment name>";
const mcpConnectionName = process.env["MCP_PROJECT_CONNECTION_NAME"] || "";

export async function main(): Promise<void> {
  // Create AI Project client
  const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());
  const openAIClient = await project.getOpenAIClient();

  console.log("Creating agent with MCP tool using project connection...");

  // Define MCP tool that connects to GitHub Copilot API with project connection authentication
  // The project connection should have Authorization header configured with "Bearer <GitHub PAT token>"
  // Token can be created at https://github.com/settings/personal-access-tokens/new
  const agent = await project.agents.createVersion("agent-mcp-connection-auth", {
    kind: "prompt",
    model: deploymentName,
    instructions: "Use MCP tools as needed",
    tools: [
      {
        type: "mcp",
        server_label: "api-specs",
        server_url: "https://api.githubcopilot.com/mcp",
        require_approval: "always",
        project_connection_id: mcpConnectionName,
      },
    ],
  });
  console.log(`Agent created (id: ${agent.id}, name: ${agent.name}, version: ${agent.version})`);

  // Create a conversation thread to maintain context across multiple interactions
  console.log("\nCreating conversation...");
  const conversation = await openAIClient.conversations.create();
  console.log(`Created conversation (id: ${conversation.id})`);

  // Send initial request that will trigger the MCP tool
  console.log("\nSending request that will trigger MCP approval...");
  const response = await openAIClient.responses.create(
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
  const finalResponse = await openAIClient.responses.create(
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
  await openAIClient.conversations.delete(conversation.id);
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

:::zone pivot="rest"
## Create a response that uses the MCP tool (REST API)

The following example shows how to call an MCP tool by using the Responses API. If the response includes an output item with `type` set to `mcp_approval_request`, send a follow-up request that includes a `mcp_approval_response` item.

### Prerequisites

Set these environment variables:

- `PROJECT_ENDPOINT`: Your project endpoint URL.
- `API_VERSION`: The API version (for example, `2025-11-15-preview`).
- `AGENT_TOKEN`: A bearer token for Foundry.
- `MODEL_DEPLOYMENT_NAME`: Your model deployment name.
- `MCP_PROJECT_CONNECTION_NAME` (optional): Your MCP project connection name.

If your MCP server doesn't require authentication, omit `project_connection_id` from the request body.

> [!NOTE]
> For REST API, you need to first retrieve the connection ID from the connection name using the Connections API, then pass the ID to the MCP tool configuration.

> [!TIP]
> For details on the MCP tool schema and approval items, see [OpenAI.MCPTool](../../../../reference/foundry-project-rest-preview.md#openaimcptool) and the MCP approval item types in the REST reference.


```bash
curl --request POST \
  --url "$PROJECT_ENDPOINT/openai/responses?api-version=$API_VERSION" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "model": "'$MODEL_DEPLOYMENT_NAME'",
  "input": "What is my username in my GitHub profile?",
  "tools": [
    {
      "type": "mcp",
      "server_label": "github",
      "server_url": "https://api.githubcopilot.com/mcp",
      "project_connection_id": "'$MCP_PROJECT_CONNECTION_NAME'"
    }
  ]
}'
```

If the response includes an output item with `type` set to `mcp_approval_request`, copy the approval request item `id` as `APPROVAL_REQUEST_ID`. Also copy the top-level response `id` as `PREVIOUS_RESPONSE_ID`.

### 2. Send an approval response

```bash
curl --request POST \
  --url "$PROJECT_ENDPOINT/openai/responses?api-version=$API_VERSION" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
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

:::zone-end

## How it works

You need to bring a remote MCP server (an existing MCP server endpoint) to Foundry Agent Service. You can bring multiple remote MCP servers by adding them as tools. For each tool, you need to provide a unique `server_label` value within the same agent and a `server_url` value that points to the remote MCP server. Be sure to carefully review which MCP servers you add to Foundry Agent Service.

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
1. Submit your approval to the agent by using `response_id` and setting `approve` to `true`.

## Known limitations

- **Non-streaming MCP tool call timeout**: Non-streaming MCP tool calls have a timeout of 100 seconds. If your MCP server takes longer than 100 seconds to respond, the call fails. To avoid timeouts, ensure that your MCP server responds within this limit. If your use case requires longer processing times, consider optimizing the server-side logic or breaking the operation into smaller steps.

## Common questions and errors

The following are common issues that you might encounter when using MCP tools with Foundry Agent Service:

- "Invalid tool schema":

    An invalid tool schema usually happens if you have `anyOf` or `allOf` in your MCP server definition, or if a parameter can take multiple types of values. Update your MCP server definition and try again.

- "Unauthorized" or "Forbidden" from the MCP server:

    Confirm the MCP server supports your authentication method, and verify the credentials stored in your project connection. For GitHub, use least-privilege tokens and rotate them regularly.

- The model never calls your MCP tool:

    Confirm your agent instructions encourage tool usage, and verify `server_label`, `server_url`, and `allowed_tools` values. If you set `allowed_tools`, make sure the tool name matches what the MCP server exposes.

- The agent never continues after approval:

    Confirm you send a follow-up request with `previous_response_id` set to the original response ID, and that you use the approval request item ID as `approval_request_id`.

## Host a local MCP server

The Agent Service runtime only accepts a remote MCP server endpoint. If you want to add tools from a local MCP server, you need to self-host it on [Azure Container Apps](https://github.com/Azure-Samples/mcp-container-ts) or [Azure Functions](https://github.com/Azure-Samples/mcp-sdk-functions-hosting-python/tree/main) to get a remote MCP server endpoint. Consider the following factors when hosting local MCP servers in the cloud:

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

- [Get started with agents using code](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true)
- [MCP server authentication](../mcp-authentication.md)
- [Build and register a Model Context Protocol (MCP) server](../../../mcp/build-your-own-mcp-server.md)
- [MCP tool REST reference](../../../../reference/foundry-project-rest-preview.md#openaimcptool)
- [Security Best Practices for MCP](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices)
- [Understanding and mitigating security risks in MCP implementations](https://techcommunity.microsoft.com/blog/microsoft-security-blog/understanding-and-mitigating-security-risks-in-mcp-implementations/4404667)
