---
title: "Connect to an A2A agent endpoint from Foundry Agent Service"
description: "Connect your Foundry agent to a remote Agent2Agent (A2A) endpoint. Configure connections, authentication, and use SDK integration to call external A2A agents."
services: azure-ai-agent-service
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 08/05/2026
author: mattwojo
reviewer: zhuoqunli
ms.author: mattwoj
ms.reviewer: lindazqli
ms.custom: azure-ai-agents, dev-focus, pilot-ai-workflow-jan-2026, doc-kit-assisted
ai-usage: ai-assisted
zone_pivot_groups: selection-agent-to-agent
---

# Connect to an A2A agent endpoint from Foundry Agent Service (preview)

[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

You can extend the capabilities of your Microsoft Foundry agent by connecting to a remote Agent2Agent (A2A) endpoint that supports the [A2A protocol](https://a2a-protocol.org/latest/). The A2A tool enables agent-to-agent communication through a standardized protocol, allowing your Foundry agent to exchange context and collaborate with external agents.

This article shows you how to configure an A2A connection and call a remote A2A endpoint from your Foundry Agent Service agent.

If you want to **expose** your own agent as an A2A endpoint that other agents can call, see [Host an A2A-compatible agent endpoint](#host-an-a2a-compatible-agent-endpoint).

When your Foundry agent calls a remote agent through the A2A tool, the remote agent processes the request and returns a response. Your Foundry agent uses that response to generate an answer for the user and continues to manage the conversation.

To learn more on optimizing tool usage, see [best practices](../../concepts/tool-best-practice.md).

[!INCLUDE [toolbox-recommended](../../includes/toolbox-recommended.md)]

> [!NOTE]
> **Migrating from `agent.as_tool` or Connected Agents?** 
>
> The Connected Agents tool from the classic Agents API isn't available in the new Foundry Agent Service. To connect one agent to another, use one of the following approaches:
>
> - **A2A tool** (this article): Connect to any A2A-compatible endpoint, including another Foundry agent exposed as an A2A endpoint. See [Host an A2A-compatible agent endpoint](#host-an-a2a-compatible-agent-endpoint) to set up the Foundry agent as an endpoint.
> - **Workflows**: Orchestrate multiple Foundry agents declaratively using sequential, group chat, or human-in-the-loop patterns. See [Build a workflow in Microsoft Foundry](../../concepts/workflow.md).
>
> For a complete mapping of classic agent tools to their replacements in the new API, see [Agent tool availability](../../how-to/migrate.md#agent-tool-availability).

## Usage support

The following table shows SDK and setup support.

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

- An Azure subscription with an active Foundry project.
- A model deployment (for example, `gpt-4.1-mini`) in your Foundry project.
- Required Azure role: On the Foundry resource, **Contributor** or **Owner** for management and **Foundry User** for building an agent.

  [!INCLUDE [role-rename-note](../../../includes/role-rename-note.md)]
- SDK installation:
  - Python (GA): `pip install "azure-ai-projects>=2.0.0"`
  - C#: `Azure.AI.Projects` NuGet package
  - TypeScript (GA): `@azure/ai-projects` npm package
  - Java: `com.azure:azure-ai-agents:2.0.0` Maven dependency
- Values to update in code:
  - Project endpoint URL (for example, `https://<resource>.ai.azure.com/api/projects/<project>`).
  - Model deployment name (for example, `gpt-4.1-mini`).
  - A2A connection name (created in the Foundry portal).
  - A2A base URI (optional, only needed for non-`RemoteA2A` connections).
- An A2A connection configured in your Foundry project. For connection setup and REST examples, see [Create an A2A connection](#create-an-a2a-connection).

## Create an A2A connection

Create a project connection for your A2A endpoint so you can store authentication securely and reuse it across agent versions.

For details about supported authentication approaches, see [Agent2Agent (A2A) authentication](../../concepts/agent-to-agent-authentication.md).

If you are connecting to a Foundry agent as the target, set the connection **target** to the target agent's A2A base path, `https://{account}.services.ai.azure.com/api/projects/{project}/agents/{agent}/endpoint/protocols/a2a`, and use the audience `https://ai.azure.com`. Don't set an agent card path. Foundry resolves the default agent card path automatically and negotiates the A2A protocol version for you. You also don't need to set the optional `send_credentials_for_agent_card` field, because Foundry doesn't require the agent card fetch to carry separate credentials. However, the target agent must have incoming A2A enabled; see [Enable incoming A2A on a Foundry agent](../enable-agent-to-agent-endpoint.md).

For other endpoints, if the endpoint requires authentication to read its agent card, set `send_credentials_for_agent_card` to `true` in the A2A tool definition. Otherwise, Agent Service fetches the agent card anonymously by default. For more information, see [Credentials for the agent card request](../../concepts/agent-to-agent-authentication.md#credentials-for-the-agent-card-request).

### Create the connection in the Foundry portal

1. [!INCLUDE [foundry-sign-in](../../../includes/foundry-sign-in.md)]
1. Select **Tools**.
1. Select **Connect tool**.
1. Select the **Custom** tab.
1. Select **Agent2Agent (A2A)**, and then select **Create**.
1. Enter a **Name** and an **A2A Agent Endpoint**.
1. Under **Authentication**, select an authentication method. For key-based authentication, set the credential name (for example, `x-api-key`) and the corresponding secret value.

### Get the connection identifier for code

Use your connection name in code. Your code uses this name to retrieve the full connection ID at runtime:

- **Python/C#/TypeScript**: Call `project.connections.get(connection_name)` to get the connection object, then access `connection.id`.
- **REST API**: Include the connection ID in the `project_connection_id` field of the A2A tool definition.

:::zone pivot="python"
## Create an agent with the A2A tool

Select **Prompt Agents** to use the Azure AI Projects SDK to create a server-side prompt agent, or **Hosted Agents** to use the Agent Framework [`FoundryChatClient`](../../quickstarts/responses-api.md) to build an ephemeral, in-process agent.

### [Prompt Agents](#tab/prompt-agents)

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    A2APreviewTool,
)

# Format: "https://resource_name.ai.azure.com/api/projects/project_name"
PROJECT_ENDPOINT = "your_project_endpoint"
A2A_CONNECTION_NAME = "my-a2a-connection"
AGENT_NAME = "my-agent"

# Create clients to call Foundry API
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()

# Create the A2A tool from the project connection
a2a_connection = project.connections.get(A2A_CONNECTION_NAME)
tool = A2APreviewTool(
    project_connection_id=a2a_connection.id,
)

# Create the agent with the A2A tool
agent = project.agents.create_version(
    agent_name=AGENT_NAME,
    definition=PromptAgentDefinition(
        model="gpt-5-mini",
        instructions="You are a helpful assistant.",
        tools=[tool],
    ),
)
print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")
```

Next, send a request to the agent and print the response:

```python
# Send a request to the agent
response = openai.responses.create(
    tool_choice="required",
    input="What can the secondary agent do?",
    extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
)
print(response.output_text)

# Clean up the created agent version
project.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
```

### Expected output

The agent responds with information about the secondary agent's capabilities, demonstrating successful A2A communication.

### [Hosted Agents](#tab/hosted-agents)

This sample uses [`FoundryChatClient`](../../quickstarts/responses-api.md) from the Microsoft Agent Framework to create the `a2a-toolbox` and connect to its MCP endpoint with `MCPStreamableHTTPTool`. Install the packages with `pip install agent-framework-foundry httpx azure-ai-projects`, replace `PROJECT_ENDPOINT` with your project endpoint, and sign in with `az login`. For the complete hosted-agent toolbox pattern, see the [full sample](https://aka.ms/foundry-toolbox-maf).

```python
import asyncio

import httpx
from agent_framework import Agent, MCPStreamableHTTPTool
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential, get_bearer_token_provider
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import A2APreviewTool

PROJECT_ENDPOINT = "https://<account>.services.ai.azure.com/api/projects/<project>"
A2A_CONNECTION_NAME = "my-a2a-connection"

# Create the A2A tool and add it to a toolbox
credential = AzureCliCredential()
project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential)
a2a_connection = project.connections.get(A2A_CONNECTION_NAME)
toolbox = project.toolboxes.create_toolbox_version(
    name="a2a-toolbox",
    description="Toolbox with the A2A tool",
    tools=[A2APreviewTool(project_connection_id=a2a_connection.id)],
)
```

Next, attach the toolbox to the hosted agent as an MCP tool and run it:

```python
class _ToolboxAuth(httpx.Auth):
    def __init__(self, token_provider):
        self._token_provider = token_provider

    def auth_flow(self, request):
        request.headers["Authorization"] = f"******"
        yield request


async def main() -> None:
    # The toolbox exposes an MCP-compatible endpoint
    TOOLBOX_MCP_URL = (
        f"{PROJECT_ENDPOINT}/toolboxes/{toolbox.name}"
        f"/versions/{toolbox.version}/mcp?api-version=v1"
    )

    # Attach the toolbox to the hosted agent as an MCP tool
    token_provider = get_bearer_token_provider(credential, "https://ai.azure.com/.default")
    http_client = httpx.AsyncClient(auth=_ToolboxAuth(token_provider), timeout=120.0)
    mcp_tool = MCPStreamableHTTPTool(
        name="toolbox",
        url=TOOLBOX_MCP_URL,
        http_client=http_client,
        load_prompts=False,
    )

    agent = Agent(
        client=FoundryChatClient(credential=credential),
        instructions="You are a helpful assistant.",
        tools=[mcp_tool],
    )

    result = await agent.run("What can the secondary agent do?")
    print(f"Agent: {result.text}")


if __name__ == "__main__":
    asyncio.run(main())
```

### Expected output

The agent calls the secondary agent through the `a2a-toolbox` MCP endpoint and prints the consolidated reply:

```console
Agent: The secondary agent can help with ...
```

For the complete hosted-agent toolbox pattern, see the [full sample](https://aka.ms/foundry-toolbox-maf).

---

:::zone-end

:::zone pivot="csharp"

## Create an agent with the A2A tool

This example creates an agent that can call a remote A2A endpoint. For the connection setup steps, see [Create an A2A connection](#create-an-a2a-connection). Select **Prompt Agents** to use the Azure AI Projects SDK to create a server-side prompt agent, or **Hosted Agents** to use the Microsoft Agent Framework to compose two agents in-process by exposing one agent as a function tool of another.

### [Prompt Agents](#tab/prompt-agents)

```csharp
using System;
using Azure.AI.Projects;
using Azure.AI.Extensions.OpenAI;
using Azure.Identity;

var projectEndpoint = "https://<resource>.ai.azure.com/api/projects/<project>";
var a2aConnectionName = "my-a2a-connection";
var a2aBaseUri = "https://<a2a-endpoint>"; // Optional for non-RemoteA2A connections.

// Create project client to call Foundry API
AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

// Create the A2ATool and provide it with the A2A connection ID
AIProjectConnection a2aConnection = projectClient.Connections.GetConnection(connectionName: a2aConnectionName);
A2APreviewTool a2aTool = new()
{
    ProjectConnectionId = a2aConnection.Id
};
if (!string.Equals(a2aConnection.Type.ToString(), "RemoteA2A"))
{
  if (string.IsNullOrWhiteSpace(a2aBaseUri))
    {
    throw new InvalidOperationException($"The connection {a2aConnection.Name} is of {a2aConnection.Type.ToString()} type and does not carry the A2A service base URI. Set a2aBaseUri before running this sample.");
    }
    a2aTool.BaseUri = new Uri(a2aBaseUri);
}

// Create the agent with the A2A tool
DeclarativeAgentDefinition agentDefinition = new(model: "gpt-5-mini")
{
    Instructions = "You are a helpful assistant.",
    Tools = { a2aTool }
};
AgentVersion agentVersion = projectClient.AgentAdministrationClient.CreateAgentVersion(
    agentName: "myAgent",
    options: new(agentDefinition));
```

Next, send a request to the agent and print the response:

```csharp
// Send the request and print the response
ProjectResponsesClient responseClient = projectClient.ProjectOpenAIClient.GetProjectResponsesClientForAgent(agentVersion.Name);
CreateResponseOptions responseOptions = new()
{
    ToolChoice = ResponseToolChoice.CreateRequiredChoice(),
    InputItems = { ResponseItem.CreateUserMessageItem("What can the secondary agent do?") },
};
ResponseResult response = responseClient.CreateResponse(responseOptions);
Console.WriteLine(response.GetOutputText());

// Clean up the created agent version
projectClient.AgentAdministrationClient.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

### Expected output

The console displays the agent's response text from the A2A endpoint. After completion, the agent version is deleted to clean up resources.

### [Hosted Agents](#tab/hosted-agents)

This sample creates the `a2a-toolbox` with the Azure AI Projects SDK, then uses `ResponsesServer` from the Microsoft Agent Framework with a custom `ToolboxMcpClient` to discover and invoke the A2A tool through the toolbox MCP endpoint. Set the `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_OPENAI_ENDPOINT`, and `AZURE_AI_MODEL_DEPLOYMENT_NAME` environment variables, and sign in with `az login`. For the complete hosted-agent toolbox pattern, see the [full sample](https://aka.ms/foundry-toolbox-maf).

```csharp
using Azure.AI.AgentServer.Responses;
using Azure.AI.AgentServer.Responses.Models;
using Azure.AI.OpenAI;
using Azure.AI.Projects;
using Azure.AI.Extensions.OpenAI;
using Azure.Identity;
using Microsoft.Extensions.AI;
using Microsoft.Extensions.DependencyInjection;
using OpenAI.Chat;

const string AgentInstructions = "You are a helpful assistant.";
const string AgentName = "A2AAgent";

string projectEndpoint = Environment.GetEnvironmentVariable("AZURE_AI_PROJECT_ENDPOINT")
    ?? "https://<account>.services.ai.azure.com/api/projects/<project>";
string a2aConnectionName = "my-a2a-connection";
string openAiEndpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT")
    ?? throw new InvalidOperationException("AZURE_OPENAI_ENDPOINT is not set.");
string deploymentName = Environment.GetEnvironmentVariable("AZURE_AI_MODEL_DEPLOYMENT_NAME") ?? "gpt-5-mini";

DefaultAzureCredential credential = new();

// Create the A2A tool and add it to a toolbox
AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: credential);
AIProjectConnection a2aConnection = projectClient.Connections.GetConnection(connectionName: a2aConnectionName);
A2APreviewTool a2aTool = new() { ProjectConnectionId = a2aConnection.Id };
ProjectsAgentTool a2aProjectTool = a2aTool;
ToolboxVersion toolboxVersion = projectClient.AgentAdministrationClient
    .GetAgentToolboxes().CreateToolboxVersion(
        toolboxName: "a2a-toolbox",
        tools: [a2aProjectTool],
        description: "Toolbox with the A2A tool");
```

Next, attach the toolbox to the hosted agent:

```csharp
// The toolbox exposes an MCP-compatible endpoint
string toolboxMcpEndpoint =
    $"{projectEndpoint}/toolboxes/{toolboxVersion.Name}/versions/{toolboxVersion.Version}/mcp?api-version=v1";

// Attach the toolbox to the hosted agent
AzureOpenAIClient openAIClient = new(new Uri(openAiEndpoint), credential);
ChatClient chatClient = openAIClient.GetChatClient(deploymentName);

// ToolboxMcpClient discovers toolbox tools via MCP tools/list and calls them via tools/call
ToolboxMcpClient toolboxClient = new(toolboxMcpEndpoint, credential);

ResponsesServer.Run<ToolboxHandler>(configure: builder =>
{
    builder.Services.AddSingleton(new AgentConfig(
        name: AgentName,
        instructions: AgentInstructions,
        chatClient: chatClient,
        toolboxClient: toolboxClient));
});
```

### Expected output

When invoked, the hosted agent calls the secondary agent through the `a2a-toolbox` MCP endpoint and prints the consolidated reply:

```console
Agent: The secondary agent can help with ...
```

For a maintained .NET Agent Framework integration, see [Use a toolbox with a hosted agent](use-toolbox-hosted-agent.md).

---

:::zone-end

:::zone pivot="rest-api"
## Create an A2A connection by using the REST API

Use these examples to create a project connection that stores your authentication information.

To get an access token for the Azure Resource Manager endpoint:

```azurecli
az account get-access-token --scope https://management.azure.com/.default --query accessToken -o tsv
```

### Key-based

```bash
curl --request PUT \
  --url 'https://management.azure.com/subscriptions/{{subscription_id}}/resourceGroups/{{resource_group_name}}/providers/Microsoft.CognitiveServices/accounts/{{foundry_account_name}}/projects/{{project_name}}/connections/{{connection_name}}?api-version=2025-04-01-preview' \
  --header 'Authorization: Bearer {{token}}' \
  --header 'Content-Type: application/json' \
  --data '{
    "tags": null,
    "location": null,
    "name": "{{connection_name}}",
    "type": "Microsoft.MachineLearningServices/workspaces/connections",
    "properties": {
      "authType": "CustomKeys",
      "group": "ServicesAndApps",
      "category": "RemoteA2A",
      "expiryTime": null,
      "target": "{{a2a_endpoint}}",
      "isSharedToAll": true,
      "sharedUserList": [],
      "Credentials": {
        "Keys": {
          "{{key_name}}": "{{key_value}}"
        }
      },
      "metadata": {
        "ApiType": "Azure"
      }
    }
  }'
```

### Managed OAuth Identity Passthrough

This option is supported when you select **Managed OAuth** in the Foundry tool catalog.

```bash
curl --request PUT \
  --url 'https://management.azure.com/subscriptions/{{subscription_id}}/resourceGroups/{{resource_group_name}}/providers/Microsoft.CognitiveServices/accounts/{{foundry_account_name}}/projects/{{project_name}}/connections/{{connection_name}}?api-version=2025-04-01-preview' \
  --header 'Authorization: Bearer {{token}}' \
  --header 'Content-Type: application/json' \
  --data '{
    "tags": null,
    "location": null,
    "name": "{{connection_name}}",
    "type": "Microsoft.MachineLearningServices/workspaces/connections",
    "properties": {
      "authType": "OAuth2",
      "group": "ServicesAndApps",
      "category": "RemoteA2A",
      "expiryTime": null,
      "target": "{{a2a_endpoint}}",
      "isSharedToAll": true,
      "sharedUserList": [],
      "useCustomConnector": false,
      "connectorName": "{{connector_name}}",
      "Credentials": {},
      "metadata": {
        "ApiType": "Azure"
      }
    }
  }'
```

### Custom OAuth Identity Passthrough

Custom OAuth doesn't support the update operation. Create a new connection if you want to update certain values.

If your OAuth app doesn't require a client secret, omit `ClientSecret`.

> [!NOTE]
> Provide each scope as a separate string in the `Scopes` array. If your tooling or UI expects scopes as a single string, separate them with a **single space**, not a comma — this follows the [OAuth 2.0 spec](https://datatracker.ietf.org/doc/html/rfc6749#section-3.3).

```bash
curl --request PUT \
  --url 'https://management.azure.com/subscriptions/{{subscription_id}}/resourceGroups/{{resource_group_name}}/providers/Microsoft.CognitiveServices/accounts/{{foundry_account_name}}/projects/{{project_name}}/connections/{{connection_name}}?api-version=2025-04-01-preview' \
  --header 'Authorization: Bearer {{token}}' \
  --header 'Content-Type: application/json' \
  --data '{
    "tags": null,
    "location": null,
    "name": "{{connection_name}}",
    "type": "Microsoft.MachineLearningServices/workspaces/connections",
    "properties": {
      "authType": "OAuth2",
      "group": "ServicesAndApps",
      "category": "RemoteA2A",
      "expiryTime": null,
      "target": "{{a2a_endpoint}}",
      "isSharedToAll": true,
      "sharedUserList": [],
      "TokenUrl": "{{token_url}}",
      "AuthorizationUrl": "{{authorization_url}}",
      "RefreshUrl": "{{refresh_url}}",
      "Scopes": [
        "{{scope}}"
      ],
      "Credentials": {
        "ClientId": "{{client_id}}",
        "ClientSecret": "{{client_secret}}"
      },
      "metadata": {
        "ApiType": "Azure"
      }
    }
  }'
```

### Foundry Project Managed Identity

```bash
curl --request PUT \
  --url 'https://management.azure.com/subscriptions/{{subscription_id}}/resourceGroups/{{resource_group_name}}/providers/Microsoft.CognitiveServices/accounts/{{foundry_account_name}}/projects/{{project_name}}/connections/{{connection_name}}?api-version=2025-04-01-preview' \
  --header 'Authorization: Bearer {{token}}' \
  --header 'Content-Type: application/json' \
  --data '{
    "tags": null,
    "location": null,
    "name": "{{connection_name}}",
    "type": "Microsoft.MachineLearningServices/workspaces/connections",
    "properties": {
      "authType": "ProjectManagedIdentity",
      "group": "ServicesAndApps",
      "category": "RemoteA2A",
      "expiryTime": null,
      "target": "{{a2a_endpoint}}",
      "isSharedToAll": true,
      "sharedUserList": [],
      "audience": "{{audience}}",
      "Credentials": {},
      "metadata": {
        "ApiType": "Azure"
      }
    }
  }'
```

### Agent identity

```bash
curl --request PUT \
  --url 'https://management.azure.com/subscriptions/{{subscription_id}}/resourceGroups/{{resource_group_name}}/providers/Microsoft.CognitiveServices/accounts/{{foundry_account_name}}/projects/{{project_name}}/connections/{{connection_name}}?api-version=2025-04-01-preview' \
  --header 'Authorization: Bearer {{token}}' \
  --header 'Content-Type: application/json' \
  --data '{
    "tags": null,
    "location": null,
    "name": "{{connection_name}}",
    "type": "Microsoft.MachineLearningServices/workspaces/connections",
    "properties": {
      "authType": "AgenticIdentityToken",
      "group": "ServicesAndApps",
      "category": "RemoteA2A",
      "expiryTime": null,
      "target": "{{a2a_endpoint}}",
      "isSharedToAll": true,
      "sharedUserList": [],
      "audience": "{{audience}}",
      "Credentials": {},
      "metadata": {
        "ApiType": "Azure"
      }
    }
  }'
```

## Add A2A tool to Foundry Agent Service

Get an access token:

```azurecli
az account get-access-token --scope https://ai.azure.com/.default --query accessToken -o tsv
```

Use that token as `{{agent_token}}` in the request.

The recommended way to add an A2A tool is through a toolbox, then attach the toolbox to your agent as an MCP tool. See [What is a toolbox?](../../concepts/toolbox-overview.md)

1. Create a toolbox that contains the A2A tool:

```bash
curl --request POST \
  --url '{{project_endpoint}}/toolboxes/a2a-toolbox/versions?api-version=v1' \
  -H 'Content-Type: application/json' \
  -d '{
    "description": "Toolbox with the A2A tool",
    "tools": [
      {
        "type": "a2a_preview",
        "base_url": "{{a2a_endpoint}}",
        "project_connection_id": "{{project_connection_id}}"
      }
    ]
  }'
```

   The toolbox exposes an MCP-compatible endpoint at `{{project_endpoint}}/toolboxes/a2a-toolbox/versions/<version>/mcp?api-version=v1`, where `<version>` is the version returned by the previous call.

1. Create a remote-tool project connection that points at the toolbox endpoint, using a user Entra token so the caller's identity is passed through (audience `https://ai.azure.com`).

    ```bash
    azd ai connection create a2a-toolbox-conn \
      --kind remote-tool \
      --target "{{project_endpoint}}/toolboxes/a2a-toolbox/versions/<version>/mcp?api-version=v1" \
      --auth-type user-entra-token \
      --audience https://ai.azure.com
    ```

1. Create an agent version that uses the toolbox by attaching it as an MCP tool:

    ```bash
    curl --request POST \
      --url '{{project_endpoint}}/agents/{{agent_name}}/versions?api-version=v1' \
      -H 'Authorization: Bearer {{agent_token}}' \
      -H 'Content-Type: application/json' \
      -d '{
      "description": "Test agent version description",
      "definition": {
        "kind": "prompt",
        "model": "{{model}}",
        "tools": [
          {
            "type": "mcp",
            "server_label": "toolbox",
            "server_url": "{{project_endpoint}}/toolboxes/a2a-toolbox/versions/<version>/mcp?api-version=v1",
            "require_approval": "never",
            "project_connection_id": "a2a-toolbox-conn"
          }
        ],
        "instructions": "You are a helpful agent."
      }
    }'
    ```

To delete an agent version, send a `DELETE` request to the same endpoint with the agent name and version.
:::zone-end

### Add an A2A tool to a toolbox with the Azure Developer CLI

Create a `remote-a2a` connection for the remote agent, then reference it from a minimal toolbox YAML.

**Step 1. Create the connection**

Pick the auth variant you need:

```bash
# No auth
azd ai connection create my-a2a-conn \
  --kind remote-a2a \
  --target https://your-remote-agent.azurecontainerapps.io \
  --auth-type none

# Custom-keys header
azd ai connection create my-a2a-conn \
  --kind remote-a2a \
  --target https://your-remote-agent.azurecontainerapps.io \
  --auth-type custom-keys \
  --custom-key "Authorization=******"

# OAuth — bring your own app registration
azd ai connection create my-a2a-conn \
  --kind remote-a2a \
  --target https://your-remote-agent.azurecontainerapps.io \
  --auth-type oauth2 \
  --authorization-url https://auth.example.com/authorize \
  --token-url https://auth.example.com/token \
  --client-id <oauth-client-id> \
  --client-secret <oauth-client-secret> \
  --scopes "<scope1> <scope2>"

# User Entra token (managed user identity passthrough)
azd ai connection create my-a2a-conn \
  --kind remote-a2a \
  --target https://your-remote-agent.azurecontainerapps.io \
  --auth-type user-entra-token \
  --audience "<entra-audience>"

# Project managed identity
azd ai connection create my-a2a-conn \
  --kind remote-a2a \
  --target https://your-remote-agent.azurecontainerapps.io \
  --auth-type project-managed-identity \
  --audience "<entra-audience>"

# Agentic identity
azd ai connection create my-a2a-conn \
  --kind remote-a2a \
  --target https://your-remote-agent.azurecontainerapps.io \
  --auth-type agentic-identity \
  --audience "<entra-audience>"
```

| `--auth-type` | Additional flags |
|---------------|------------------|
| `none` | — |
| `custom-keys` | `--custom-key "Header=Value"` (repeatable) |
| `oauth2` | `--authorization-url`, `--token-url`, `--client-id`, `--client-secret`, `--scopes` |
| `user-entra-token` | `--audience <entra-audience>` |
| `project-managed-identity` | `--audience <entra-audience>` (optional) |
| `agentic-identity` | `--audience <entra-audience>` |

**Step 2. Define the toolbox**

```yaml
# my-toolbox.yaml
description: Agent-to-Agent toolbox
connections:
  - name: my-a2a-conn
```

**Step 3. Create the toolbox**

```bash
azd ai toolbox create my-toolbox --from-file my-toolbox.yaml
```

:::zone pivot="typescript"

This sample demonstrates how to create an AI agent with A2A capabilities by using the `a2a_preview` tool type and the Azure AI Projects client. The agent communicates with other agents and provides responses based on inter-agent interactions by using the A2A protocol.

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";

const PROJECT_ENDPOINT = "https://<resource>.ai.azure.com/api/projects/<project>";
const A2A_CONNECTION_NAME = "my-a2a-connection";

// Create clients to call Foundry API
const project = new AIProjectClient(PROJECT_ENDPOINT, new DefaultAzureCredential());
const openai = project.getOpenAIClient();

// Get the A2A connection by name to retrieve its ID
const a2aConnection = await project.connections.get(A2A_CONNECTION_NAME);

// Add the A2A tool to a toolbox
const toolbox = await project.toolboxes.createVersion(
  "a2a-toolbox",
  [
    {
      type: "a2a_preview",
      project_connection_id: a2aConnection.id,
    },
  ],
  { description: "Toolbox with the A2A tool" },
);

// The toolbox exposes an MCP-compatible endpoint
const toolboxMcpUrl =
  `${PROJECT_ENDPOINT}/toolboxes/${toolbox.name}` +
  `/versions/${toolbox.version}/mcp?api-version=v1`;
```

Create a remote-tool project connection that points at the toolbox endpoint. Use a user Entra token so the caller's identity is passed through (audience `https://ai.azure.com`). Create the connection once, for example with the Azure Developer CLI:

```bash
azd ai connection create a2a-toolbox-conn \
  --kind remote-tool \
  --target "<toolboxMcpUrl>" \
  --auth-type user-entra-token \
  --audience https://ai.azure.com
```

Next, attach the toolbox to a prompt agent as an MCP tool and run it:

```typescript
const toolboxConnectionName = "a2a-toolbox-conn";

// Attach the toolbox to a prompt agent as an MCP tool
const agent = await project.agents.createVersion("MyA2AAgent", {
  kind: "prompt",
  model: "gpt-5-mini",
  instructions: "You are a helpful assistant.",
  tools: [
    {
      type: "mcp",
      server_label: "toolbox",
      server_url: toolboxMcpUrl,
      require_approval: "never",
      project_connection_id: toolboxConnectionName,
    },
  ],
});
console.log(`Agent created (id: ${agent.id}, name: ${agent.name}, version: ${agent.version})`);

// Send a request to the agent
const response = await openai.responses.create(
  {
    input: "What can the secondary agent do?",
  },
  {
    body: {
      agent: { name: agent.name, type: "agent_reference" },
      tool_choice: "required",
    },
  },
);
console.log(response.output_text);

// Clean up the created agent version
await project.agents.deleteVersion(agent.name, agent.version);
```

### Expected output

The console displays the agent's response text from the A2A endpoint. After completion, the agent version is deleted to clean up resources.
:::zone-end

:::zone pivot="java"

## Use agent-to-agent communication in Java

Update these values in your Java agent after you create the toolbox:

- `projectEndpoint` — Your project endpoint.
- `toolboxMcpUrl` — The MCP endpoint for the toolbox version that contains the A2A tool.
- `toolboxConnectionName` — The remote-tool project connection name for the toolbox endpoint.

Add the dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-agents</artifactId>
    <version>2.2.0</version>
</dependency>
```

> [!TIP]
> **Recommended:** For most agents, add the A2A tool through a [toolbox](../../concepts/toolbox-overview.md) and attach the toolbox to your agent as an MCP tool. The Java SDK doesn't yet expose a toolbox creation API, so create the toolbox by using the [Python](?pivots=python), [REST API](?pivots=rest-api), [C#](?pivots=csharp), or [TypeScript](?pivots=typescript) example, or the [Foundry portal](../../how-to/tools/toolbox.md), and then reference its MCP endpoint from your Java agent as an `McpTool`.

:::zone-end

## Troubleshooting

| Issue | Cause | Resolution |
| --- | --- | --- |
| Agent doesn't invoke the A2A tool | Agent definition doesn't include A2A tool configuration | Confirm your agent definition includes the A2A tool and that you configured the connection. If you're using responses, confirm you're not forcing a different tool. |
| Agent doesn't invoke the A2A tool | Prompt doesn't require remote agent | Update your prompt to require calling the remote agent, or remove conflicting tool choice settings. |
| Authentication failures (401 or 403) | Connection authentication type mismatch | Confirm the connection's authentication type matches your endpoint requirements. For key-based auth, confirm the credential name matches what the endpoint expects (`x-api-key` or `Authorization`). |
| SDK sample can't find the connection | Connection name mismatch | Confirm the connection name in code matches the connection name in Foundry. |
| Network or TLS errors | Endpoint unreachable or invalid certificate | Confirm the endpoint is publicly reachable and uses a valid TLS certificate. Check firewall rules and proxy settings. |
| Remote agent returns unexpected response | Response format incompatibility | Confirm the remote agent follows A2A protocol specifications. Check that response content types match expected formats. |
| Connection timeout | Remote agent slow to respond | Increase timeout settings or verify the remote agent's performance. Consider implementing retry logic with exponential backoff. |
| Missing A2A tool in response | Tool not enabled for the agent | Recreate the agent with the A2A tool explicitly enabled, and verify the connection is active and properly configured. |

## Host an A2A-compatible agent endpoint

You can expose your Foundry agent as an A2A endpoint directly by enabling the A2A protocol on the agent. For step-by-step instructions, see [Enable incoming A2A on a Foundry agent](../enable-agent-to-agent-endpoint.md).

If your agent is deployed outside of Agent Service, or if you need a custom hosting approach, use one of the following alternatives.

### Option 1: Register a custom A2A agent in Foundry Control Plane

If you already have an agent deployed outside of Agent Service that supports the A2A protocol, register it in Foundry Control Plane for centralized management, observability, and governance.

1. Deploy your A2A-compatible agent to any reachable endpoint.
1. [Register the agent in Foundry Control Plane](../../../control-plane/register-custom-agent.md), and select **A2A** as the protocol.
1. Foundry generates a proxy URL and discovers your agent card at `/.well-known/agent-card.json`.

After registration, other agents can connect to your agent through the proxy URL. Foundry provides access control and monitoring through the AI gateway.

For authentication setup, see [Agent2Agent (A2A) authentication](../../concepts/agent-to-agent-authentication.md).

### Option 2: Build a custom A2A server that wraps a Foundry agent

Build a lightweight A2A server that delegates to your Foundry agent through the Responses API:

1. Create an A2A server by using the official A2A SDK for your language ([Python](https://github.com/a2aproject/a2a-python), [.NET](https://github.com/a2aproject/a2a-dotnet), or [JavaScript](https://github.com/a2aproject/a2a-js)).
1. Implement the server to call your Foundry agent through the Responses API.
1. Serve an agent card at `/.well-known/agent-card.json` that describes your agent's capabilities.
1. Deploy the server and [register it in Foundry Control Plane](../../../control-plane/register-custom-agent.md).

For more information about the A2A protocol requirements for servers, see the [A2A specification](https://a2a-protocol.org/latest/).

<!-- The verbiage in the following section is required. Do not remove or modify. -->
## Considerations for using non-Microsoft services

You're subject to the terms between you and the service provider when you use connected non-Microsoft services and servers ("non-Microsoft services"). Under your agreement governing use of Microsoft Online services, non-Microsoft services are non-Microsoft Products. When you connect to a non-Microsoft service, you pass some of your data (such as prompt content) to the non-Microsoft services, or your application might receive data from the non-Microsoft services. You're responsible for your use of non-Microsoft services and data, along with any charges associated with that use. 

Third parties, not Microsoft, create the non-Microsoft services, including A2A agent endpoints, that you decide to use with the A2A tool described in this article. Microsoft didn't test or verify these A2A agent endpoints. Microsoft has no responsibility to you or others in relation to your use of any non-Microsoft services.  

Carefully review and track the A2A agent endpoints you add to Foundry Agent Service. Rely on endpoints hosted by trusted service providers themselves rather than proxies. 

The A2A tool allows you to pass custom headers, such as authentication keys or schemas, that an A2A agent endpoint might need. Review all data that you share with non-Microsoft services, including A2A agent endpoints, and log the data for auditing purposes. Be aware of non-Microsoft practices for retention and location of data. 

## Related content

- [Agent2Agent (A2A) authentication](../../concepts/agent-to-agent-authentication.md)
- [Register and manage custom agents](../../../control-plane/register-custom-agent.md)
- [Best practices for tools](../../concepts/tool-best-practice.md)
- [Foundry project REST API (preview)](../../../reference/foundry-project-rest-preview.md)
