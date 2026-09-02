---
title: "Connect agents to MCP server endpoints"
description: "Connect your Foundry agents to Model Context Protocol (MCP) servers using the MCP tool. Extend capabilities with external tools and data."
services: cognitive-services
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 08/26/2026
author: mattwojo
reviewer: lindazqli
ms.author: mattwoj
ms.reviewer: zhuoqunli
ai-usage: ai-assisted
zone_pivot_groups: selection-mcp-code-new
ms.custom: dev-focus, pilot-ai-workflow-jan-2026, doc-kit-assisted
#CustomerIntent: As a developer, I want to connect my Foundry agent to external MCP servers so that I can extend agent capabilities with third-party tools.
---

# Connect agents to Model Context Protocol servers

Connect your Foundry agents to [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) servers by using the MCP tool. This connection extends agent capabilities with external tools and data sources. By connecting to remote MCP server endpoints, your agent's Foundry model can access tools hosted by developers and organizations that MCP-compatible clients like Foundry Agent Service can use.

MCP is an open standard that defines how applications provide tools and contextual data to large language models (LLMs). It enables consistent, scalable integration of external tools into model workflows.

[!INCLUDE [toolbox-recommended](../../includes/toolbox-recommended.md)]

In this article, you learn how to:

- Add a remote MCP server as a tool.
- Authenticate to an MCP server by using a project connection.
- Review and approve MCP tool calls.
- Troubleshoot common MCP integration issues.

If you use a coding agent like GitHub Copilot, the [Microsoft Foundry Skill](../../../how-to/develop/use-microsoft-foundry-skill.md) can help configure MCP tool connections, authentication, approval behavior, and troubleshooting steps.

## Prerequisites

Before you begin, make sure you have:

- An Azure subscription with an active Microsoft Foundry project.
- The **Foundry User** role on the Foundry project to create and test agents. If you create a project connection for MCP authentication, you also need the **Foundry Project Manager** role on that project.

  [!INCLUDE [role-rename-note](../../../includes/role-rename-note.md)]
- The latest SDK package for your language. The .NET SDK is currently in preview. For installation details, see the [quickstart](../../../quickstarts/get-started-code.md).
- Azure credentials configured for authentication (such as `DefaultAzureCredential`).
- Access to a remote MCP server endpoint (such as GitHub's MCP server at `https://api.githubcopilot.com/mcp`).

## Choose a task

| Task | Path |
| --- | --- |
| Connect an agent and confirm the first successful tool call | [Follow the connect, approve, verify, and clean-up route](#first-success-route). |
| Add credentials or identity-based access | **Secondary:** [Configure authentication](#authentication). |
| Connect to a private MCP endpoint | **Secondary:** [Review public and private endpoint requirements](#public-and-private-mcp-server-endpoints). |
| Run a long operation in background mode | **Secondary:** [Configure long-running operations](#long-running-operations-preview). |
| Understand streaming and timeout behavior | **Secondary:** [Review the known limitations](#known-limitations). |
| Configure server options or host a local server | **Secondary:** [Set up the MCP connection](#set-up-the-mcp-connection) or [host a local MCP server](#host-a-local-mcp-server). |

For conceptual details about how MCP integration works, see [How it works](#how-it-works).

## Usage support

The following table shows SDK and setup support for MCP connections.

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Public and private MCP server endpoints

Agent Service supports both public and private MCP server endpoints:

- **Public endpoints**: Connect to any publicly accessible remote MCP server. This option works with both Basic and Standard agent setups.
- **Private endpoints**: Connect to MCP servers that aren't exposed to the public internet. Private MCP requires [private networking setup](../virtual-networks.md) and a dedicated MCP subnet within your virtual network.

For private MCP servers, deploy your MCP server on Azure Container Apps with internal-only ingress on a dedicated MCP subnet delegated to `Microsoft.App/environments`. To get started, use the [19-private-network-agents-tools-setup](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/19-private-network-agent-tools) template, which provisions the required network infrastructure including the MCP subnet or [11-private-network-basic-project](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/11-private-network-basic-vnet) if you dont want to bring your own resources.

For details about tool support in network-isolated environments, see [Agent tools with network isolation](../../../how-to/configure-private-link.md#agent-tools-with-network-isolation).

## Use Foundry Toolboxes as MCP endpoints

Foundry Toolboxes let you bundle multiple tools - such as Web Search, Code Interpreter, File Search, Azure AI Search, MCP servers, OpenAPI tools, and Agent-to-Agent connections - into a single MCP-compatible endpoint. Instead of configuring each tool separately on every agent, create a Toolbox in Foundry and point your agent to the Toolbox endpoint by using the standard `mcp` tool configuration (`server_url` and `server_label`).

Because the Toolbox endpoint is MCP-compatible, any runtime that can consume an MCP server can also consume a Toolbox. This compatibility includes Foundry Agent Service, Microsoft Agent Framework, LangGraph, GitHub Copilot SDK, and other MCP-enabled clients. You can add, remove, or reconfigure tools in the Toolbox without changing your agent code.

For setup steps, see [Create and use a Foundry Toolbox](toolbox.md).

The toolbox MCP endpoint supports long-running operations through [MCP tasks](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/tasks), which is in preview. To use long-running tools, make sure your agent harness supports [MCP tasks](https://modelcontextprotocol.io/extensions/tasks/overview).

### Toolbox MCP authentication and configuration

Create a project connection for your MCP server with the auth type that matches your scenario, then reference it from a minimal toolbox YAML.

**Step 1. Create the connection**

Export your project endpoint and set it as the active project for the `azd ai` commands:

```bash
PROJECT_ENDPOINT="https://<account>.services.ai.azure.com/api/projects/<project>"
azd ai project set $PROJECT_ENDPOINT
```

Pick the auth variant you need:

```bash
# No auth — public MCP server
azd ai connection create my-mcp-conn \
  --kind remote-tool \
  --target https://learn.microsoft.com/api/mcp \
  --auth-type none

# Custom-keys header (for example, GitHub PAT)
azd ai connection create my-mcp-conn \
  --kind remote-tool \
  --target https://api.githubcopilot.com/mcp/ \
  --auth-type custom-keys \
  --custom-key "Authorization=******"

# OAuth — bring your own app registration
azd ai connection create my-mcp-conn \
  --kind remote-tool \
  --target https://your-mcp-server.example.com \
  --auth-type oauth2 \
  --authorization-url https://auth.example.com/authorize \
  --token-url https://auth.example.com/token \
  --client-id <oauth-client-id> \
  --client-secret <oauth-client-secret> \
  --scopes "<scope1> <scope2>"

# User Entra token (managed user identity passthrough; for example, Microsoft Fabric)
azd ai connection create my-mcp-conn \
  --kind remote-tool \
  --target https://api.fabric.microsoft.com/v1/mcp/fabricaihub/integrations/m365 \
  --auth-type user-entra-token \
  --audience https://analysis.windows.net/powerbi/api

# Project managed identity — the project's system-assigned MI
azd ai connection create my-mcp-conn \
  --kind remote-tool \
  --target https://<resource>.cognitiveservices.azure.com/language/mcp \
  --auth-type project-managed-identity \
  --audience https://cognitiveservices.azure.com

# Agentic identity — the agent's per-project identity
azd ai connection create my-mcp-conn \
  --kind remote-tool \
  --target https://<resource>.cognitiveservices.azure.com/language/mcp \
  --auth-type agentic-identity \
  --audience https://cognitiveservices.azure.com
```

| `--auth-type` | Additional flags |
|---------------|------------------|
| `none` | — |
| `custom-keys` | `--custom-key "Header=Value"` (repeatable) |
| `oauth2` | `--authorization-url`, `--token-url`, `--client-id`, `--client-secret`, `--scopes` |
| `user-entra-token` | `--audience <entra-audience>` |
| `project-managed-identity` | `--audience <entra-audience>` (optional) |
| `agentic-identity` | `--audience <entra-audience>` |

For identity-based auth (`user-entra-token`, `project-managed-identity`, `agentic-identity`), assign the corresponding principal the required RBAC role on the target resource before you call the toolbox.

**Step 2. Define the toolbox**

```yaml
# my-toolbox.yaml
description: MCP server tools
connections:
  - name: my-mcp-conn
```

**Step 3. Create the toolbox**

```bash
azd ai toolbox create my-toolbox --from-file my-toolbox.yaml
```

The first time a user calls a toolbox with an OAuth-based MCP in a project, the MCP endpoint returns a `CONSENT_REQUIRED` error (code `-32006`) with a consent URL:

```json
{
  "error": {
    "code": -32006,
    "message": "User consent is required. Please visit: https://..."
  }
}
```

This error is expected. Open the consent URL in a browser, complete the OAuth authorization flow, and then retry the agent call. Subsequent calls succeed without re-prompting.

## Authentication

**Secondary path:** Configure authentication after the first-success route when your MCP server requires credentials or identity-based access.

Many MCP servers require authentication.

In Foundry Agent Service, use a project connection to store authentication details, such as API keys or bearer tokens, instead of hard-coding credentials in your app.

To learn about supported authentication options, including key-based, Microsoft Entra identities, and OAuth identity passthrough, see [MCP server authentication](../mcp-authentication.md).

> [!NOTE]
> Set `project_connection_id` to the ID of your project connection.

> [!TIP]
> When you add the Azure DevOps MCP Server through the **Add Tools** catalog, you authenticate to Azure DevOps during the organization connection step and store the authentication as a project connection. Use least-privilege access and review scopes when connecting the organization.

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
- Treat tool descriptions, annotations, and results from remote MCP servers as untrusted input. They can contain indirect prompt injection instructions.
- Require approval for high-risk operations, especially tools that write data or change resources.
- Review the requested tool name and arguments before you approve.
- Review `allowed_tools`, approval settings, and connection permissions when the server's operator, exposed tools, or behavior changes.
- Log approvals and tool calls for auditing and troubleshooting.

> [!TIP]
> When you add the Azure DevOps MCP Server through the **Add Tools** catalog, the tool selection configuration maps to the `allowed_tools` behavior described in this article. Selecting a subset of tools in the catalog UI is equivalent to specifying an `allowed_tools` list in code.

<a id="first-success-route"></a>

**First-success route: connect, approve, verify, and clean up**

Use the prompt-agent sample for your selected language. When the sample has agent-type tabs, select **Prompt Agents**. This route keeps the first run focused on one task: connect one MCP server, invoke one tool, and inspect the result.

1. **Connect:** Configure the MCP tool with `require_approval` set to `always`, and attach it to the agent.
1. **Approve:** Run the sample, review the requested server, tool, and arguments, and approve only the expected call.
1. **Verify:** Confirm that the final response contains information returned by the MCP tool, as shown in the expected output.
1. **Clean up:** Run the sample's clean-up operation. The prompt-agent samples delete the agent version, and the TypeScript sample also deletes its conversation.

## Create an agent in Python with the MCP tool

Use the following code sample to create an agent and call the function. The .NET SDK is currently in preview. See the [quickstart](../../../quickstarts/get-started-code.md) for details.

:::zone pivot="python"

The following example shows how to add the GitHub MCP server to a toolbox and attach the toolbox to an agent. Select **Prompt Agents** to use the Azure AI Projects SDK to create a server-side prompt agent, or **Hosted Agents** to use the Agent Framework [`FoundryChatClient`](../../quickstarts/responses-api.md) to build an ephemeral, in-process agent.

### Prompt agents

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

### Hosted agents

This sample uses [`FoundryChatClient`](../../quickstarts/responses-api.md) from the Microsoft Agent Framework, creates a toolbox containing the GitHub MCP server, then attaches the toolbox endpoint to your hosted agent with `FoundryToolbox`. Install the packages with `pip install agent-framework-foundry`, set the `FOUNDRY_PROJECT_ENDPOINT` and `FOUNDRY_MODEL` environment variables, and sign in with `az login`.

```python
import asyncio

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient, FoundryToolbox
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MCPToolboxTool
from azure.identity import AzureCliCredential

PROJECT_ENDPOINT = "https://<account>.services.ai.azure.com/api/projects/<project>"
MCP_CONNECTION_NAME = "my-mcp-connection"


async def main() -> None:
    credential = AzureCliCredential()

    # 1. Add the GitHub MCP server to a toolbox.
    project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential)
    server_tool = MCPToolboxTool(
        server_label="api-specs",
        server_url="https://api.githubcopilot.com/mcp",
        require_approval="always",
        project_connection_id=MCP_CONNECTION_NAME,
    )
    toolbox = project.toolboxes.create_version(
        name="mcp-server-toolbox",
        description="Toolbox with the GitHub MCP server",
        tools=[server_tool],
    )

    # 2. The toolbox exposes an MCP-compatible endpoint.
    TOOLBOX_MCP_URL = (
        f"{PROJECT_ENDPOINT}/toolboxes/{toolbox.name}"
        f"/versions/{toolbox.version}/mcp?api-version=v1"
    )

    # 3. Attach the toolbox to the hosted agent as an MCP tool.
,
        timeout=120.0,
    )

    toolbox_tool = FoundryToolbox(credential, url=TOOLBOX_MCP_URL)

agent = Agent(
        client=FoundryChatClient(credential=credential),
        instructions="You are a helpful assistant that uses your MCP tool "
        "to help with Microsoft documentation questions.",
        tools=[toolbox_tool],
    )

    result = await agent.run("What is Microsoft Agent Framework?")
    print(f"Agent: {result.text}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Expected output

The agent calls the Microsoft Learn MCP server through the toolbox endpoint and returns documentation-grounded text:

```console
Agent: Microsoft Agent Framework is an open-source framework for building, orchestrating, and deploying AI agents ...
```

For the full toolbox hosted-agent patterns, see [Use a toolbox with a hosted agent](use-toolbox-hosted-agent.md).

---

:::zone-end

:::zone pivot="csharp"
## Create an agent with MCP tool

The following example shows how to add a remote MCP server to a toolbox and attach the toolbox to an agent. Select **Prompt Agents** to use the Azure AI Projects SDK to create a server-side prompt agent, or **Hosted Agents** to use the Microsoft Agent Framework to build an ephemeral, in-process agent.

### Prompt agents

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

### Hosted agents

This sample creates the MCP server toolbox with the Azure AI Projects SDK, then uses the Microsoft Agent Framework `AddFoundryToolboxes` integration to expose the toolbox tools to your hosted agent. Set the `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_OPENAI_ENDPOINT`, and `AZURE_AI_MODEL_DEPLOYMENT_NAME` environment variables, and sign in with `az login`.

```csharp
using Azure.AI.AgentServer.Responses;
using Azure.AI.AgentServer.Responses.Models;
using Azure.AI.OpenAI;
using Azure.AI.Projects;
using Azure.AI.Extensions.OpenAI;
using Azure.Identity;
using Microsoft.Agents.AI;
using Microsoft.Agents.AI.Foundry.Hosting;
using Microsoft.Extensions.DependencyInjection;
using OpenAI.Chat;

string projectEndpoint = Environment.GetEnvironmentVariable("AZURE_AI_PROJECT_ENDPOINT")
    ?? "https://<account>.services.ai.azure.com/api/projects/<project>";
string openAiEndpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT")
    ?? throw new InvalidOperationException("AZURE_OPENAI_ENDPOINT is not set.");
string deploymentName = Environment.GetEnvironmentVariable("AZURE_AI_MODEL_DEPLOYMENT_NAME") ?? "gpt-5-mini";

DefaultAzureCredential credential = new();

// 1. Create the MCP server tool and add it to a toolbox.
AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: credential);
McpTool mcpTool = ResponseTool.CreateMcpTool(
    serverLabel: "api-specs",
    serverUri: new Uri("https://gitmcp.io/Azure/azure-rest-api-specs"),
    toolCallApprovalPolicy: new McpToolCallApprovalPolicy(
        GlobalMcpToolCallApprovalPolicy.AlwaysRequireApproval));

ToolboxVersion toolboxVersion = projectClient.AgentAdministrationClient
    .GetAgentToolboxes().CreateToolboxVersion(
        toolboxName: "mcp-server-toolbox",
        tools: [ProjectsAgentTool.AsProjectTool(mcpTool)],
        description: "Toolbox with the GitHub MCP server");

// Create the hosted agent and register the toolbox integration.
AIAgent agent = projectClient.AsAIAgent(
    model: deploymentName,
    instructions: "You are a helpful assistant with access to the toolbox tools.",
    name: "hosted-toolbox-agent");

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddFoundryResponses(agent);
builder.Services.AddFoundryToolboxes(credential, toolboxVersion.Name);

var app = builder.Build();
app.MapFoundryResponses();
app.Run();
```

### Expected output

When invoked, the hosted agent queries the Microsoft Learn MCP server through the toolbox endpoint for documentation snippets and answers:

```console
User: How does one create an Azure storage account using the az CLI?

Agent: To create an Azure storage account using the az CLI, run: `az storage account create --name <name> --resource-group <rg> --location <region> --sku Standard_LRS` ...
```

For a maintained .NET Agent Framework integration, see [Use a toolbox with a hosted agent](use-toolbox-hosted-agent.md).

---

## Create an agent by using the MCP tool with project connection authentication

In this example, you learn how to authenticate to the GitHub MCP server inside a toolbox, then attach the toolbox MCP endpoint to an agent. The example uses synchronous methods to create the toolbox and agent. For asynchronous methods, see the [sample code](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Extensions.OpenAI/samples/Sample20_MCP_Connection.md) in the Azure SDK for .NET repository on GitHub.

### Set up project connection

Before running the sample:

1. Sign in to your GitHub profile.
1. Select the profile picture at the upper right corner.
1. Select **Settings**.
1. In the left panel, select **Developer Settings** and **Personal access tokens > Tokens (classic)**.
1. At the top, select **Generate new token**, enter your password, and create a token that can read public repositories.
   - **Important:** Save the token, or keep the page open as once the page is closed, token can't be shown again.
1. In the Azure portal, open Microsoft Foundry.
1. Select **Manage** in the upper-right navigation, select **Project details**, and then select the **Connected resources** tab.
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

// 1. Add the GitHub MCP server to a toolbox. Using a toolbox is the recommended
//    way to give agents tools. See /azure/foundry/agents/concepts/toolbox-overview
AgentToolboxes toolboxClient = projectClient.AgentAdministrationClient.GetAgentToolboxes();

McpTool mcpTool = ResponseTool.CreateMcpTool(
    serverLabel: "api-specs",
    serverUri: new Uri("https://api.githubcopilot.com/mcp"),
    toolCallApprovalPolicy: new McpToolCallApprovalPolicy(
        GlobalMcpToolCallApprovalPolicy.AlwaysRequireApproval));
mcpTool.ProjectConnectionId = mcpConnectionName;

ToolboxVersion toolboxVersion = toolboxClient.CreateToolboxVersion(
    toolboxName: "mcp-server-toolbox",
    tools: [ProjectsAgentTool.AsProjectTool(mcpTool)],
    description: "Toolbox with the GitHub MCP server");

// 2. The toolbox exposes an MCP-compatible endpoint.
var toolboxMcpUrl = new Uri(
    $"{projectEndpoint}/toolboxes/{toolboxVersion.Name}" +
    $"/versions/{toolboxVersion.Version}/mcp?api-version=v1");

// 3. Create a remote-tool project connection that points at the toolbox endpoint.
//    Use a user Entra token so the caller's identity is passed through
//    (audience https://ai.azure.com). Create the connection once, for example
//    with the Azure Developer CLI:
//
//    azd ai connection create mcp-server-toolbox-conn \
//      --kind remote-tool \
//      --target "<toolboxMcpUrl>" \
//      --auth-type user-entra-token \
//      --audience https://ai.azure.com
var toolboxConnectionName = "mcp-server-toolbox-conn";

// 4. Attach the toolbox to a prompt agent as an MCP tool. Note that in this scenario
//    GlobalMcpToolCallApprovalPolicy.AlwaysRequireApproval is used, which means that
//    any calls to the toolbox MCP endpoint must be approved.
McpTool toolboxTool = ResponseTool.CreateMcpTool(
    serverLabel: "toolbox",
    serverUri: toolboxMcpUrl,
    toolCallApprovalPolicy: new McpToolCallApprovalPolicy(
        GlobalMcpToolCallApprovalPolicy.AlwaysRequireApproval));
toolboxTool.ProjectConnectionId = toolboxConnectionName;

DeclarativeAgentDefinition agentDefinition = new(model: "gpt-5-mini")
{
    Instructions = "You are a helpful agent that can use MCP tools to assist users. Use the available MCP tools to answer questions and perform tasks.",
    Tools = { toolboxTool }
};
AgentVersion agentVersion = projectClient.AgentAdministrationClient.CreateAgentVersion(
    agentName: "myAgent",
    options: new(agentDefinition));

// If the tool approval is required, the response item is
// of McpToolCallApprovalRequestItem type and contains all
// the information about tool call. This example checks that
// the server label is "toolbox" and approves the tool call.
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
            if (string.Equals(mcpToolCall.ServerLabel, "toolbox"))
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
Approval requested for toolbox...
Response: Your GitHub username is "example-username".
```
:::zone-end

:::zone pivot="typescript"
## Create an agent in TypeScript with the MCP tool

The following TypeScript sample demonstrates how to add an MCP server to a toolbox, attach the toolbox to an agent, send requests that trigger MCP approval workflows, handle approval requests, and clean up resources. For a JavaScript version, see the [sample code](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2/javascript/agents/tools/agentMcp.js) on the Azure SDK for JavaScript repository on GitHub.

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

  // 1. Add the Azure REST API specifications MCP server to a toolbox. Using a toolbox is
  //    the recommended way to give agents tools. See /azure/foundry/agents/concepts/toolbox-overview
  const toolbox = await project.toolboxes.createVersion(
    "mcp-server-toolbox",
    [
      {
        type: "mcp",
        server_label: "api-specs",
        server_url: "https://gitmcp.io/Azure/azure-rest-api-specs",
        require_approval: "always",
      },
    ],
    { description: "Toolbox with the Azure REST API specifications MCP server" },
  );

  // 2. The toolbox exposes an MCP-compatible endpoint.
  const toolboxMcpUrl =
    `${PROJECT_ENDPOINT}/toolboxes/${toolbox.name}` +
    `/versions/${toolbox.version}/mcp?api-version=v1`;

  // 3. Create a remote-tool project connection that points at the toolbox endpoint.
  //    Use a user Entra token so the caller's identity is passed through
  //    (audience https://ai.azure.com). Create the connection once, for example
  //    with the Azure Developer CLI:
  //
  //    azd ai connection create mcp-server-toolbox-conn \
  //      --kind remote-tool \
  //      --target "<toolboxMcpUrl>" \
  //      --auth-type user-entra-token \
  //      --audience https://ai.azure.com
  const toolboxConnectionName = "mcp-server-toolbox-conn";

  // 4. Attach the toolbox to a prompt agent as an MCP tool.
  // The toolbox tool requires approval for each operation to ensure user control over external requests.
  const agent = await project.agents.createVersion("agent-mcp", {
    kind: "prompt",
    model: "gpt-5-mini",
    instructions:
      "You are a helpful agent that can use MCP tools to assist users. Use the available MCP tools to answer questions and perform tasks.",
    tools: [
      {
        type: "mcp",
        server_label: "toolbox",
        server_url: toolboxMcpUrl,
        require_approval: "always",
        project_connection_id: toolboxConnectionName,
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
      body: { agent_reference: { name: agent.name, type: "agent_reference" } },
    },
  );

  // Process any MCP approval requests that were generated
  // When requireApproval="always", the agent will request permission before accessing external resources
  const inputList: OpenAI.Responses.ResponseInputItem.McpApprovalResponse[] = [];

  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  const ask = (q: string) => new Promise<string>((resolve) => rl.question(q, resolve));
  for (const item of response.output) {
    if (item.type === "mcp_approval_request") {
      if (item.server_label === "toolbox" && item.id) {
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
      body: { agent_reference: { name: agent.name, type: "agent_reference" } },
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

The following TypeScript sample demonstrates how to add an authenticated MCP server to a toolbox, attach the toolbox MCP endpoint to an agent, send requests that trigger MCP approval workflows, handle approval requests, and clean up resources. For a JavaScript version, see the [sample code](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2/javascript/agents/tools/agentMcpConnectionAuth.js) on the Azure SDK for JavaScript repository on GitHub.

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

  // 1. Add the GitHub MCP server to a toolbox with project connection authentication.
  // The project connection should have Authorization header configured with "Bearer <GitHub PAT token>"
  // Token can be created at https://github.com/settings/personal-access-tokens/new
  const toolbox = await project.toolboxes.createVersion(
    "mcp-server-toolbox",
    [
      {
        type: "mcp",
        server_label: "api-specs",
        server_url: "https://api.githubcopilot.com/mcp",
        require_approval: "always",
        project_connection_id: MCP_CONNECTION_NAME,
      },
    ],
    { description: "Toolbox with the GitHub MCP server" },
  );

  // 2. The toolbox exposes an MCP-compatible endpoint.
  const toolboxMcpUrl =
    `${PROJECT_ENDPOINT}/toolboxes/${toolbox.name}` +
    `/versions/${toolbox.version}/mcp?api-version=v1`;

  // 3. Create a remote-tool project connection that points at the toolbox endpoint.
  //    Use a user Entra token so the caller's identity is passed through
  //    (audience https://ai.azure.com). Create the connection once, for example
  //    with the Azure Developer CLI:
  //
  //    azd ai connection create mcp-server-toolbox-conn \
  //      --kind remote-tool \
  //      --target "<toolboxMcpUrl>" \
  //      --auth-type user-entra-token \
  //      --audience https://ai.azure.com
  const toolboxConnectionName = "mcp-server-toolbox-conn";

  // 4. Attach the toolbox to a prompt agent as an MCP tool.
  const agent = await project.agents.createVersion("agent-mcp-connection-auth", {
    kind: "prompt",
    model: "gpt-5-mini",
    instructions: "Use MCP tools as needed",
    tools: [
      {
        type: "mcp",
        server_label: "toolbox",
        server_url: toolboxMcpUrl,
        require_approval: "always",
        project_connection_id: toolboxConnectionName,
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
      body: { agent_reference: { name: agent.name, type: "agent_reference" } },
    },
  );

  // Process any MCP approval requests that were generated
  const inputList: OpenAI.Responses.ResponseInputItem.McpApprovalResponse[] = [];

  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  const ask = (q: string) => new Promise<string>((resolve) => rl.question(q, resolve));
  for (const item of response.output) {
    if (item.type === "mcp_approval_request") {
      if (item.server_label === "toolbox" && item.id) {
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
      body: { agent_reference: { name: agent.name, type: "agent_reference" } },
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
  Server: toolbox
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

> [!TIP]
> Most agents use a [toolbox](../../concepts/toolbox-overview.md) to add the file search tool and attach the toolbox to your agent as an MCP tool. *If you are using the Java SDK, an API for creating toolboxes is not yet available. Create a toolbox by using the Python, REST API, C#,TypeScript, or the [Foundry portal](../../how-to/tools/toolbox.md), then reference it's MCP endpoint from your Java agent as an `McpTool`.

Add the dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-agents</artifactId>
    <version>2.2.0</version>
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
        // Create the toolbox out-of-band by using Python, REST, the Foundry portal, C#, or TypeScript.
        String toolboxMcpUrl = projectEndpoint + "/toolboxes/mcp-server-toolbox/versions/1/mcp?api-version=v1";
        String toolboxConnectionName = "mcp-server-toolbox-conn";

        AgentsClientBuilder builder = new AgentsClientBuilder()
            .credential(new DefaultAzureCredentialBuilder().build())
            .endpoint(projectEndpoint);

        AgentsClient agentsClient = builder.buildAgentsClient();
        ResponsesClient responsesClient = builder.buildResponsesClient();

        // Attach the toolbox MCP endpoint with server label, URL, connection, and approval mode.
        McpTool mcpTool = new McpTool("toolbox")
            .setServerUrl(toolboxMcpUrl)
            .setProjectConnectionId(toolboxConnectionName)
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

If the MCP server inside the toolbox doesn't require authentication, omit `project_connection_id` from the toolbox tool definition. The agent's MCP tool still uses `project_connection_id` for the remote-tool connection to the toolbox endpoint.

> [!NOTE]
> For REST API, use the remote-tool project connection name that you create for the toolbox endpoint as `project_connection_id` on the agent's MCP tool.

> [!TIP]
> For details on the MCP tool schema and approval items, see the [Microsoft Foundry REST API reference](https://ai.azure.com/api-reference).

### 1. Create a toolbox with the MCP server

The recommended way to add an MCP server is through a toolbox, then attach the toolbox to your agent as an MCP tool. See [What is a toolbox?](../../concepts/toolbox-overview.md)

```bash
curl -X POST "$FOUNDRY_PROJECT_ENDPOINT/toolboxes/mcp-server-toolbox/versions?api-version=v1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -d '{
    "description": "Toolbox with the Azure REST API specifications MCP server",
    "tools": [
      {
        "type": "mcp",
        "server_label": "api-specs",
        "server_url": "https://gitmcp.io/Azure/azure-rest-api-specs",
        "require_approval": "never"
      }
    ]
  }'
```

The toolbox exposes an MCP-compatible endpoint at `$FOUNDRY_PROJECT_ENDPOINT/toolboxes/mcp-server-toolbox/versions/<version>/mcp?api-version=v1`, where `<version>` is the version returned by the previous call.

### 2. Create a remote-tool connection to the toolbox

Create a remote-tool project connection that points to the toolbox endpoint. Use a user Entra token so the caller's identity is passed through (audience `https://ai.azure.com`):

```bash
azd ai connection create mcp-server-toolbox-conn \
  --kind remote-tool \
  --target "$FOUNDRY_PROJECT_ENDPOINT/toolboxes/mcp-server-toolbox/versions/<version>/mcp?api-version=v1" \
  --auth-type user-entra-token \
  --audience https://ai.azure.com
```

### 3. Create an MCP agent

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
          "server_label": "toolbox",
          "server_url": "'$FOUNDRY_PROJECT_ENDPOINT'/toolboxes/mcp-server-toolbox/versions/<version>/mcp?api-version=v1",
          "require_approval": "always",
          "project_connection_id": "mcp-server-toolbox-conn"
        }
      ]
    }
  }'
```

To use an authenticated MCP server inside the toolbox, add `"project_connection_id": "'$MCP_PROJECT_CONNECTION_NAME'"` to the toolbox tool definition. Change `server_url` to the authenticated server endpoint (for example, `https://api.githubcopilot.com/mcp`).

### 4. Create a response

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

### 5. Send an approval response

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

### 6. Clean up resources

Delete the agent:

```bash
curl -X DELETE "$FOUNDRY_PROJECT_ENDPOINT/agents/<AGENT_NAME>-mcp?api-version=v1" \
  -H "Authorization: Bearer $AGENT_TOKEN"
```

:::zone-end

## How it works

You need to bring a remote MCP server (an existing MCP server endpoint) to Foundry Agent Service. You can bring multiple remote MCP servers by adding them as tools. For each tool, you need to provide a unique `server_label` value within the same agent and a `server_url` value that points to the remote MCP server. Be sure to carefully review which MCP servers you add to Foundry Agent Service.

In addition to connecting arbitrary remote MCP servers by URL, you can add some MCP servers directly from the Foundry **Add Tools** catalog. For example, Azure DevOps MCP Server is available as a catalog entry. Azure DevOps hosts the remote MCP endpoint and exposes it over streamable HTTP, so you don't install or host the server when you add it from the Foundry catalog. Catalog entries simplify connection setup and align with the same approval and auditing mechanisms documented in this article.

For more information on using MCP, see:

- [Security Best Practices](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices) on the Model Context Protocol website.
- [Understanding and mitigating security risks in MCP implementations](https://techcommunity.microsoft.com/blog/microsoft-security-blog/understanding-and-mitigating-security-risks-in-mcp-implementations/4404667) in the Microsoft Security Community Blog.

## Set up the MCP connection

**Secondary path - advanced operations:** Use this reference after the first-success route to restrict tools, change approval behavior, or add a project connection.

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

Azure DevOps MCP Server is available as a catalog entry in Foundry.

> [!IMPORTANT]
> The remote Azure DevOps MCP Server authenticates with Microsoft Entra ID. Your Azure DevOps organization must be backed by a Microsoft Entra tenant. Standalone Microsoft account (MSA) organizations aren't supported.

To add the server:

1. In [Foundry portal](https://ai.azure.com), go to your project.
1. Select **Add Tools** > **Catalog** and search for "Azure DevOps."
1. Select **Azure DevOps MCP Server** and select **Create**.
1. Enter your Azure DevOps organization name and select **Connect**.
1. Choose which Azure DevOps tools to expose to your agent. You can select a subset of tools to control exactly what the agent can access.

This catalog-based setup creates the MCP tool for use by agents without requiring code changes. You can validate connectivity and tool behavior in the Foundry chat testing experience before integrating the tool into production code.

> [!TIP]
> **Toolbox versioning**: Foundry Toolboxes support versioning, so you can iterate on a new version without affecting production agents. Use the **consumer endpoint** (`{project_endpoint}/toolboxes/{name}/mcp?api-version=v1`) for production agents - it always serves the promoted default version. Use the **version-specific endpoint** (`{project_endpoint}/toolboxes/{name}/versions/{version}/mcp?api-version=v1`) to test before promoting. Keep `server_label` unique per agent, even when switching Toolbox versions. For details, see [Promote a version to default](toolbox.md#promote-a-version-to-default).

## Long-running operations (preview)

**Secondary path - background mode:** Use this mode only when an MCP operation can't complete within the standard synchronous timeout.

Some MCP servers expose tools that take longer than the standard synchronous timeout to return a result. To support these operations, run the agent in [background mode](../../concepts/runtime-components.md#run-an-agent-in-background-mode). Background mode runs the response asynchronously, so the MCP tool call can continue without holding an open connection, and you poll for the response status until it completes. This approach lets MCP tool calls exceed the 100-second non-streaming timeout described in [Known limitations](#known-limitations).

> [!NOTE]
> Long-running MCP operations are in preview. Preview features are provided without a service-level agreement and aren't recommended for production workloads. Behavior and supported models can change.

### Requirements for the MCP server

The agent runtime relies on the MCP server to run the operation asynchronously and report progress. The server must:

- Implement the [Model Context Protocol tasks capability](https://modelcontextprotocol.io/specification) so a tool call can return a task reference instead of blocking until the work finishes.
- Return a related task identifier in the tool result metadata (the `io.modelcontextprotocol/related-task` field with a `taskId`) when it starts a long-running operation.
- Expose a way for the runtime to poll the task status and retrieve the final result after the task completes.
- Be reachable as a remote MCP endpoint, the same as any other MCP tool. Local MCP servers must be self-hosted to provide a remote endpoint. See [Host a local MCP server](#host-a-local-mcp-server).

When the agent runtime calls a tool that starts a long-running operation, the server returns the task reference and the runtime keeps the response in the background. The runtime starts the response, returns immediately with a response `id` and a `status` of `queued`, and collects the result when the task finishes. You poll the response `id` until `status` becomes `completed`, then read the final output.

Background mode for long-running MCP operations works with any model that supports background mode, such as `gpt-5.4` or `gpt-5.5`.

If your agent uses a model that doesn't support background mode, MCP tool calls run synchronously and are subject to the 100-second timeout.

### Enable background mode in the Microsoft Foundry portal

You can turn on background mode for an agent in the [Microsoft Foundry portal](https://ai.azure.com/) playground, without writing code:

1. Open your agent, and select the **Playground** tab.
1. In the **Model** list, select a model that supports background mode, such as `gpt-5.4` or `gpt-5.5`.
1. Select the parameters icon next to the model, and turn on **Background mode**.

1. Under **Tools**, add a tool whose MCP server supports MCP tasks, such as a Fabric data agent added through the Fabric IQ tool. For steps, see [Connect agents to Microsoft Fabric with Fabric IQ](fabric-iq.md#run-a-fabric-data-agent-in-background-mode).
1. Send a message. The agent starts a background run and shows its progress while the long-running tool call completes. When the run finishes, the response appears in the chat.

### Run background mode with code

The following examples invoke an agent that's already configured with an MCP tool, set `background` to `true`, and poll until the response completes. Replace the placeholder values with your own.

:::zone pivot="python"

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

:::zone-end

:::zone pivot="csharp"

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

:::zone-end

:::zone pivot="typescript"

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";

const PROJECT_ENDPOINT = "your_project_endpoint";
const AGENT_NAME = "your_mcp_agent_name";

const project = new AIProjectClient(PROJECT_ENDPOINT, new DefaultAzureCredential());
const openai = project.getOpenAIClient();

// Start a background response. It returns immediately with status "queued".
let response = await openai.responses.create(
  {
    input: "Run the long-running task and summarize the result.",
    background: true,
  },
  { body: { agent_reference: { name: AGENT_NAME, type: "agent_reference" } } },
);

// Poll the response ID until the MCP tool call completes.
while (response.status === "queued" || response.status === "in_progress") {
  await new Promise((r) => setTimeout(r, 5000));
  response = await openai.responses.retrieve(response.id);
}
console.log(response.output_text);
```

:::zone-end

:::zone pivot="java"

```java
import com.azure.ai.agents.*;
import com.azure.ai.agents.models.AgentReference;
import com.azure.ai.agents.models.AzureCreateResponseOptions;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

String projectEndpoint = "your_project_endpoint";
String agentName = "your_mcp_agent_name";

AgentsClientBuilder builder = new AgentsClientBuilder()
    .credential(new DefaultAzureCredentialBuilder().build())
    .endpoint(projectEndpoint);
ResponsesClient responsesClient = builder.buildResponsesClient();

AgentReference agentRef = new AgentReference(agentName);

// Start a background response. It returns immediately with status "queued".
Response response = responsesClient.createAzureResponse(
    new AzureCreateResponseOptions()
        .setAgentReference(agentRef)
        .setBackground(true),
    ResponseCreateParams.builder()
        .input("Run the long-running task and summarize the result."));

// Poll the response ID until the MCP tool call completes.
while (response.status().equals("queued") || response.status().equals("in_progress")) {
    Thread.sleep(5000);
    response = responsesClient.getAzureResponse(response.id());
}
System.out.println(response.output());
```

:::zone-end

:::zone pivot="rest"

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

:::zone-end

## Known limitations

**Secondary path - streaming behavior:** Review these limits after the first-success route if your client streams responses or your MCP call approaches the synchronous timeout.

- **Non-streaming MCP tool call timeout**: Non-streaming MCP tool calls have a timeout of 100 seconds. If your MCP server takes longer than 100 seconds to respond, the call fails. To avoid timeouts, ensure that your MCP server responds within this limit. If your use case requires longer processing times, run the agent in [background mode](#long-running-operations-preview) with a supported model, optimize the server-side logic, or break the operation into smaller steps.
- **Private MCP requires Standard Agent Setup**: Private MCP server connectivity is only available with [Standard Agent Setup with private networking](../virtual-networks.md) (BYO VNet). Basic agent setup doesn't support private MCP endpoints.
- **Private MCP hosting**: Azure Container Apps on a dedicated MCP subnet is the tested configuration for private MCP servers. Function Apps or App Services as the private MCP server host might work but aren't internally validated.

## Common questions and errors

The following common issues might occur when you use MCP tools with Foundry Agent Service:

- "Invalid tool schema":

    This error usually happens if your MCP server definition includes `anyOf` or `allOf`, or if a parameter accepts multiple types of values. Update your MCP server definition and try again.

- "Unauthorized" or "Forbidden" from the MCP server:

  Confirm the MCP server supports your authentication method, and verify the credentials stored in your project connection. For GitHub, use least-privilege tokens and rotate them regularly. For Azure DevOps MCP Server, verify that the organization is backed by a Microsoft Entra tenant and that you can complete the organization connection flow in Foundry. Standalone Microsoft account organizations aren't supported.

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
- [Microsoft Foundry REST API reference](https://ai.azure.com/api-reference)
- [Security Best Practices for MCP](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices)
- [Understanding and mitigating security risks in MCP implementations](https://techcommunity.microsoft.com/blog/microsoft-security-blog/understanding-and-mitigating-security-risks-in-mcp-implementations/4404667)
