---
title: "Connect agents to Microsoft Fabric with Fabric IQ (preview)"
description: "Learn how to connect your Microsoft Foundry agent to Fabric IQ, a Microsoft Fabric workload that unifies business data through an enterprise ontology and AI agents so your agents can reason over your data in shared semantic context."
services: cognitive-services
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 06/26/2026
author: zhuoqunli
ms.author: zhuoqunli
ms.custom:
 - dev-focus
ai-usage: ai-assisted
zone_pivot_groups: selection-fabric-iq
---

# Connect agents to Microsoft Fabric with Fabric IQ (preview)

[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

> [!WARNING]
> When you connect to Fabric IQ, you may incur costs and data may be sent outside the Azure compliance boundary and processed according to the applicable service terms and data handling policies. It is your responsibility to manage whether your data will flow outside of your organization's compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
>
> You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. See the [Foundry Agent Service transparency note](/azure/foundry/responsible-ai/agents/transparency-note).

> [!NOTE]
> For information on optimizing tool usage, see [best practices](../../concepts/tool-best-practice.md).

[Fabric IQ (preview)](/fabric/iq/overview) is a Microsoft Fabric workload that unifies data across OneLake and organizes it according to the language of your business. It exposes that data to analytics, AI agents, and applications with consistent semantic meaning through its core items: the [ontology (preview)](/fabric/iq/ontology/overview), which defines your enterprise vocabulary as entity types (such as Customer, Order, and Product), their properties, relationships, and data bindings to OneLake sources (lakehouses, eventhouses, and Power BI semantic models); the [Fabric data agent](/fabric/data-science/concept-data-agent), which enables conversational Q&A over ontology-grounded data; [Power BI semantic models](/fabric/data-warehouse/semantic-models), which provide curated analytics with measures and hierarchies. The ontology includes a Natural Language to Ontology (NL2Ontology) layer that converts natural-language questions into structured queries, so agents can ask questions using business terms instead of table names or query syntax.

When you connect your Foundry agent to Fabric IQ by registering it as a server-side tool, your agent can delegate natural-language tasks to the Fabric IQ workload—for example, "Which customers placed orders above $10,000 last quarter?" Fabric IQ handles data retrieval, ontology-grounded reasoning, and response synthesis, then returns the result to your agent. All requests run in the context of the signed-in user, honor Fabric permissions and governance policies, and remain within the Microsoft Fabric trust boundary.

## Usage support

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Fabric IQ | ✔️ | ✔️ | ✔️ | — | ✔️ | ✔️ | ✔️ |

## Prerequisites

> [!NOTE]
> Virtual network (VNet) support depends on the Fabric item type. For details, see [Virtual network support](#virtual-network-support).

> [!IMPORTANT]
> Fabric IQ isn't available in regions where Power BI is the only Fabric workload. Confirm your Fabric workspace is in a region that supports the full Fabric stack — see [Microsoft Fabric region availability](/fabric/admin/region-availability#power-bi).

Before you begin, make sure you have:

- A [Microsoft Fabric license](https://www.microsoft.com/microsoft-fabric) that grants access to the Fabric items your agent queries. Users who invoke Fabric IQ through your agent must also have this license.
- An active [Microsoft Foundry project](../../../how-to/create-projects.md) with a deployed model.
- **Azure RBAC roles**:
  - **Foundry User** role on the Foundry project for the developer identity, the agent's runtime identity, and any user identity involved in OAuth flows.
  - **Foundry Project Manager** role on the Foundry project for creating a Foundry connection to the Fabric IQ endpoint.
- **Foundry Toolkit**: Install [Visual Studio Code](https://code.visualstudio.com/) and [Foundry Toolkit for Visual Studio Code](https://code.visualstudio.com/docs/intelligentapps/overview#_install-and-setup).

## How it works

1. **Your agent dispatches a tool call** — When the agent model identifies a task that requires Fabric data, it emits a tool call to the `fabric_iq_preview` tool.
1. **Fabric IQ processes the request** — Fabric IQ receives the natural-language query and routes it based on the target item type:
   - **Ontology** — The Natural Language to Ontology (NL2Ontology) layer converts the query into a structured ontology query against your enterprise entities, relationships, and data bindings.
   - **Fabric data agent** — The query goes directly to the data agent for conversational Q&A over ontology-grounded data.
   - **Power BI semantic models** — Fabric IQ queries the semantic model's measures and hierarchies to return analytics results.
1. **The result is returned to your agent** — Fabric IQ returns the synthesized response. Your agent incorporates it into its reply to the user. All requests run in the context of the signed-in user and honor Fabric permissions and governance policies.

## Connect to Fabric IQ

### Find your Fabric IQ server details

Fabric IQ exposes different MCP endpoint URLs depending on the type of Fabric item you're connecting to. The value you supply as `server_url` follows one of these patterns:

| Fabric item type | `server_url` pattern | Supported authentication |
|---|---|---|
| **Power BI semantic model** | `https://{host}/v1/mcp/fabricaihub/integrations/m365` | BYO Entra app, managed OAuth |
| **Ontology** | `https://{host}/v1/mcp/dataPlane/workspaces/{workspaceId}/items/{itemId}/ontologyEndpoint` | BYO Entra app, managed OAuth |
| **Data agent** | `https://{host}/v1/mcp/workspaces/{workspaceId}/dataagents/{dataAgentId}/agent` | BYO Entra app, managed OAuth |

Replace the placeholders as follows:

- `{host}` — The Fabric API host, typically `api.fabric.microsoft.com`
- `{workspaceId}` — The GUID of your Microsoft Fabric workspace
- `{itemId}` / `{dataAgentId}` — The GUID of the specific Fabric item

You can find the workspace and item GUIDs in the Microsoft Fabric portal: open your workspace, select the item, and copy the IDs from the browser URL.

> [!NOTE]
> If the data agent's workspace uses a [workspace-level private link](#virtual-network-support), replace `api.fabric.microsoft.com` with the workspace-specific host. See [Connect to a data agent over a workspace-level private link](#connect-to-a-data-agent-over-a-workspace-level-private-link).

> [!NOTE]
> Among the Fabric IQ item types, only the **data agent** MCP endpoint supports long-running operations through [background mode](../../concepts/runtime-components.md#run-an-agent-in-background-mode). Ontology and Power BI semantic model endpoints run synchronously and are subject to the standard tool-call timeout. Because the data agent endpoint is an MCP server, you run it in background mode the same way as any other MCP tool — set `background` to `true` and poll the response until it completes. For code samples, see [Long-running operations](model-context-protocol.md#long-running-operations-preview).

> [!TIP]
> For **Power BI semantic models**, we highly recommend using the latest models such as `gpt-5.4` or `opus 4.7`. Semantic model queries involve complex measure and hierarchy reasoning that benefits significantly from the improved reasoning capability of newer models.

> [!IMPORTANT]
> For **Power BI semantic models**, we recommend restricting the tool surface with `allowed_tools` so the agent reasons over the schema and runs queries directly instead of pre-generating DAX. Set `allowed_tools` to:
>
> - `GetInstructions`
> - `DiscoverArtifacts`
> - `GetReportMetadata`
> - `GetSemanticModelSchema`
> - `ExecuteQuery`
> - `ValueSearch`
>
> Omit `GenerateQuery`. This list lets the agent discover artifacts, inspect the semantic model schema, execute queries, and search for values, without an intermediate query-generation step.

For **`server_label`**, use any short lowercase identifier with hyphens, for example `fabriciq-ontology`. This label appears in approval prompts when the model calls the tool.

### Add the Fabric IQ tool to your agent

:::zone pivot="vscode"

Use Foundry Toolkit for Visual Studio Code to add an existing Fabric IQ connection to a toolbox, then connect your agent to the published toolbox endpoint.

> [!NOTE]
> Adding a Fabric IQ (OneLake Catalog) connection from Foundry Toolkit isn't directly supported yet. Open this toolbox in the Foundry portal to create the connection, then return to Foundry Toolkit. The connection appears in the **Configured** list.

1. Select **Foundry Toolkit** in the Activity Bar.
1. Under **My Resources**, expand **Your project name** > **Tools**.
1. Create a toolbox, or open an existing toolbox.
1. Select **Add tools**.
1. On the **Configured** tab, select **Fabric IQ (OneLake Catalog)**.
1. Select **Add Tools**.
1. Select **Publish** for a new toolbox, or **Save Changes** for an existing toolbox.

:::image type="content" source="../../media/tools/fabric-iq/toolbox-vscode-fabric-iq.png" alt-text="Screenshot of Foundry Toolkit in Visual Studio Code showing the Select a tool dialog with Fabric IQ OneLake Catalog in the Configured list." lightbox="../../media/tools/fabric-iq/toolbox-vscode-fabric-iq.png":::

For the full toolbox creation workflow, see [Curate intent-based toolbox in Foundry](toolbox.md#step-1-create-a-toolbox-version).

To add the Fabric IQ tool directly to an agent by using code or the REST API, select the Python, .NET, JavaScript, or REST API tab in this section.

:::zone-end

:::zone pivot="python"

Install the package:

```bash
pip install "azure-ai-projects>=2.2.0" python-dotenv
```

Set the following environment variables:

- `FOUNDRY_PROJECT_ENDPOINT` — your project endpoint, found in the Overview page of your Foundry project.
- `FOUNDRY_MODEL_NAME` — the deployment name of the model the agent uses.
- `FABRIC_IQ_PROJECT_CONNECTION_ID` — the fully qualified resource ID of the Fabric IQ project connection.

```python
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, FabricIQPreviewTool

load_dotenv()

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
    project_client.get_openai_client() as openai_client,
):
    tool_payload = FabricIQPreviewTool(
        project_connection_id=os.environ["FABRIC_IQ_PROJECT_CONNECTION_ID"],
        require_approval="never",
    )

    agent = project_client.agents.create_version(
        agent_name="MyAgent",
        definition=PromptAgentDefinition(
            model=os.environ["FOUNDRY_MODEL_NAME"],
            instructions="Use the available Fabric IQ tools to answer questions and perform tasks.",
            tools=[tool_payload],
        ),
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    user_input = "Which customers placed orders above $10,000 last quarter?"
    response = openai_client.responses.create(
        input=user_input,
        extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
    )

    print(f"Agent response: {response.output_text}")

    # Clean up the agent version so unused versions don't accumulate in the project.
    project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
    print("Agent deleted")
```

**Expected output**: The agent calls Fabric IQ with the user's query. Fabric IQ queries the ontology-grounded data using your business terms, synthesizes results from bound OneLake sources, and returns the answer.

:::zone-end



:::zone pivot="rest-api"

**Step 1:** Create the agent with the Fabric IQ tool:

```http
POST {project_endpoint}/agents/{agent_name}/versions?api-version=v1
Authorization: Bearer {token}
Content-Type: application/json

{
  "definition": {
    "kind": "prompt",
    "model": "gpt-4o-mini",
    "instructions": "You are a helpful assistant with access to your organization's Microsoft Fabric data through Fabric IQ. Use Fabric IQ to answer questions about business entities, relationships, and data in the ontology—such as customers, orders, products, and pipelines.",
    "tools": [
      {
        "type": "fabric_iq_preview",
        "project_connection_id": "{connection-name}",
        "server_label": "{fabric-iq-server-label}",
        "server_url": "{fabric-iq-server-url}"
      }
    ]
  }
}
```

**Step 2:** Create a conversation session:

```http
POST {project_endpoint}/openai/v1/conversations
Authorization: Bearer {token}
Content-Type: application/json

{}
```

The response includes an `id` field. Use it in the next step.

**Step 3:** Send a request to the agent:

```http
POST {project_endpoint}/openai/v1/responses
Authorization: Bearer {token}
Content-Type: application/json

{
  "conversation": "{conversation_id}",
  "input": "Which customers placed orders above $10,000 last quarter?",
  "agent_reference": {
    "type": "agent_reference",
    "name": "{agent_name}"
  }
}
```

The response includes metadata about the agent execution and a `text` field in `content` with the synthesized answer.

> [!NOTE]
> Use token scope `https://ai.azure.com/.default` when getting the bearer token.

:::zone-end

:::zone pivot="dotnet"

```csharp
using Azure.AI.Projects;
using Azure.Identity;

var projectEndpoint = Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT");
var modelDeploymentName = Environment.GetEnvironmentVariable("FOUNDRY_MODEL_NAME");
var fabricIQConnectionName = Environment.GetEnvironmentVariable("FABRIC_IQ_PROJECT_CONNECTION_NAME");

AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

string fabricIQConnectionId =
    (await projectClient.Connections.GetConnectionAsync(fabricIQConnectionName)).Value.Id;

FabricIQPreviewTool fabricIQTool = new(projectConnectionId: fabricIQConnectionId)
{
    RequireApproval = BinaryData.FromObjectAsJson("never"),
};
DeclarativeAgentDefinition agentDefinition = new(model: modelDeploymentName)
{
    Instructions = "Use the available Fabric IQ tools to answer questions and perform tasks.",
    Tools = { fabricIQTool },
};

ProjectsAgentVersion agentVersion = await projectClient.AgentAdministrationClient.CreateAgentVersionAsync(
    agentName: "myFabricIQAgent",
    options: new(agentDefinition));
Console.WriteLine($"Agent created (name: {agentVersion.Name}, version: {agentVersion.Version})");

ProjectResponsesClient responseClient =
    projectClient.ProjectOpenAIClient.GetProjectResponsesClientForAgent(agentVersion.Name);
CreateResponseOptions responseOptions = new()
{
    ToolChoice = ResponseToolChoice.CreateRequiredChoice(),
    InputItems = { ResponseItem.CreateUserMessageItem("Which customers placed orders above $10,000 last quarter?") },
};
ResponseResult response = await responseClient.CreateResponseAsync(responseOptions);
Console.WriteLine(response.GetOutputText());

// Clean up
await projectClient.AgentAdministrationClient.DeleteAgentVersionAsync(
    agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

:::zone-end

:::zone pivot="javascript"

```javascript
const { DefaultAzureCredential } = require("@azure/identity");
const { AIProjectClient } = require("@azure/ai-projects");
require("dotenv/config");

const projectEndpoint = process.env["FOUNDRY_PROJECT_ENDPOINT"];
const deploymentName = process.env["FOUNDRY_MODEL_NAME"];
const fabricIqProjectConnectionId = process.env["FABRIC_IQ_PROJECT_CONNECTION_ID"];

async function main() {
  const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());
  const openAIClient = project.getOpenAIClient();

  const tool = {
    type: "fabric_iq_preview",
    project_connection_id: fabricIqProjectConnectionId,
    require_approval: "never",
  };

  const agent = await project.agents.createVersion("MyAgent", {
    kind: "prompt",
    model: deploymentName,
    instructions: "Use the available Fabric IQ tools to answer questions and perform tasks.",
    tools: [tool],
  });
  console.log(`Agent created (id: ${agent.id}, name: ${agent.name}, version: ${agent.version})`);

  const userInput = process.env["FABRIC_IQ_USER_INPUT"] || "Summarize the available datasets";
  const response = await openAIClient.responses.create(
    { input: userInput },
    { body: { agent_reference: { name: agent.name, type: "agent_reference" } } },
  );
  console.log(`Agent response: ${response.output_text}`);

  // Clean up the agent version so unused versions don't accumulate in the project.
  await project.agents.deleteVersion(agent.name, agent.version);
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

:::zone-end

## Authentication and security

Fabric IQ uses Microsoft Entra ID delegated authentication (On-Behalf-Of, OBO). All requests run in the context of the signed-in user. Application-only (app-only) authentication isn't supported. Microsoft Fabric permissions and data governance policies are enforced automatically — Fabric IQ can never surface data that the signed-in user isn't already permitted to see.

The authentication method available depends on the Fabric item type:

- **Ontology** - BYO Entra app or managed OAuth. To use BYO Entra app, register a dedicated Entra application with Power BI delegated permissions.
- **Data agent** — BYO Entra app (with data agent scopes) or managed OAuth.
- **Power BI semantic model** — BYO Entra app or managed OAuth.

### Set up your Entra app for ontology (one-time, per organization)

An Entra admin must complete the following steps before you can create a Fabric IQ connection for an ontology item in Foundry.

#### Create the app registration

1. Go to the [Microsoft Entra admin center](https://entra.microsoft.com/). In the left navigation, select **Entra ID** > **App registrations**.
1. Select **New registration**. Give the app a descriptive name and set **Supported account types** to **Accounts in this organizational directory only**. Select **Register**.
1. Copy the **Application (client) ID**. You need this value when creating the Foundry connection.
1. Select **API permissions** > **Add a permission** > **Microsoft APIs**. Find and select **Power BI Service**, select **Delegated permissions**, and add the following permissions:
   - `Item.Execute.All`
   - `Item.Read.All`

   :::image type="content" source="../../media/tools/fabric-iq/entra-api-permissions-search.png" alt-text="Screenshot of the Request API permissions panel for Power BI Service in the Microsoft Entra admin center, showing Item.Execute.All and Item.Read.All selected as delegated permissions, both with admin consent not required." lightbox="../../media/tools/fabric-iq/entra-api-permissions-search.png":::

   Select **Add permissions**.
1. Select **Grant admin consent for {your-organization}** in the **Configured permissions** panel. A Global Administrator must approve. This step allows users in your organization to authenticate through the Fabric IQ connection.
1. Select **Certificates & secrets** > **New client secret**. Add a description and expiration. Select **Add**, then immediately copy the secret **Value** — it's only shown once.
1. Copy your **Directory (tenant) ID** from the **Microsoft Entra ID** overview page.

#### Fill in the Foundry connection values

In [Microsoft Foundry](https://ai.azure.com/nextgen), open your project and go to **Settings** > **Connections** > **New connection** > **Fabric IQ**. Fill in the following fields:

| Field | Value |
| --- | --- |
| **Client ID** | Application (client) ID from step 3 |
| **Client secret** | Client secret value from step 6 |
| **Authorization URL** | `https://login.microsoftonline.com/{tenant-id}/oauth2/v2.0/authorize` |
| **Token URL** | `https://login.microsoftonline.com/{tenant-id}/oauth2/v2.0/token` |
| **Refresh URL** | `https://login.microsoftonline.com/{tenant-id}/oauth2/v2.0/token` |
| **Scopes** | `https://analysis.windows.net/powerbi/api/Item.Execute.All,https://analysis.windows.net/powerbi/api/Item.Read.All,offline_access` |

Replace `{tenant-id}` with your Directory (tenant) ID from step 7. Select **Save** to create the connection.

> [!NOTE]
> For data agent connections using BYO Entra, use the `DataAgent.Execute.All` delegated permission instead of the Power BI scopes listed above. Add `https://analysis.windows.net/powerbi/api/DataAgent.Execute.All` as the scope in the Foundry connection, and grant admin consent for that permission in your app registration.

#### Add the redirect URI to your app registration

After Foundry creates the connection, it displays an OAuth redirect URL. Add this URL to your app registration:

1. In the [Microsoft Entra admin center](https://entra.microsoft.com/), go to **Entra ID** > **App registrations** and select your app.
1. Select **Authentication** > **Add a platform** > **Web**.
1. Under **Redirect URIs**, paste the OAuth redirect URL from Foundry.
1. Select **Configure**.

## Virtual network support

Virtual network (VNet) support through Azure Private Link depends on the Fabric item type you connect to.

| Fabric item type | Virtual network support |
| --- | --- |
| Ontology | Tenant-level private link |
| Data agent | Tenant-level and workspace-level private link |
| Power BI semantic model | Public access only |

[Tenant-level private links](/fabric/security/security-private-links-overview) apply network restrictions across your whole tenant and don't change the `server_url` you configure. Data agent items also support [workspace-level private links](/fabric/security/security-workspace-level-private-links-overview), which isolate a single workspace and require a workspace-specific endpoint and a dedicated Foundry connection, as described in the next section. Power BI semantic models support public access only.

### Connect to a data agent over a workspace-level private link

When a workspace blocks public access through a [workspace-level private link](/fabric/security/security-workspace-level-private-links-set-up), its data agent is no longer reachable at the shared `api.fabric.microsoft.com` host. Use the workspace-specific private endpoint instead, and create a Foundry connection that forwards the signed-in user's Entra token to that endpoint.

#### Build the workspace private endpoint URL

Replace the `api.fabric.microsoft.com` host in the data agent `server_url` with the workspace fully qualified domain name (FQDN):

`https://{workspaceId}.z{xy}.w.api.fabric.microsoft.com/v1/mcp/workspaces/{workspaceId}/dataagents/{dataAgentId}/agent`

Where:

- `{workspaceId}` is the workspace ID with the dashes removed.
- `z` is a literal part of the host name.
- `{xy}` is the first two characters of the workspace ID.

For example, for workspace ID `1234567890abcdef1234567890abcdef`, the host is `1234567890abcdef1234567890abcdef.z12.w.api.fabric.microsoft.com`. For more information, see [Connecting to workspaces](/fabric/security/security-workspace-level-private-links-overview#connecting-to-workspaces).

#### Create the Foundry connection

Create a remote tool connection that uses Microsoft Entra ID On-Behalf-Of (OBO) authentication with the user's token and connects through the workspace private endpoint. Configure the audience as the Power BI API resource `https://analysis.windows.net/powerbi/api`, which authorizes data agent execution using the `DataAgent.Execute.All` permission scope.

# [azd](#tab/azd)

Add the connection to the `resources` section of your `azure.yaml` file, then run `azd provision`:

```yaml
resources:
  - kind: connection
    name: fabriciq-dataagent-vnet
    category: RemoteTool
    authType: UserEntraToken
    audience: https://analysis.windows.net/powerbi/api
    target: https://{workspaceId}.z{xy}.w.api.fabric.microsoft.com/v1/mcp/workspaces/{workspaceId}/dataagents/{dataAgentId}/agent
```

# [REST API](#tab/rest-api)

Send a PUT request to the connections API. Replace the placeholders with your subscription, resource group, Foundry account, and project names, and supply a Microsoft Entra access token for Azure Resource Manager.

```http
PUT https://management.azure.com/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.CognitiveServices/accounts/{account-name}/projects/{project-name}/connections/fabriciq-dataagent-vnet?api-version=2025-10-01-preview
Authorization: Bearer {arm-access-token}
Content-Type: application/json

{
  "properties": {
    "category": "RemoteTool",
    "authType": "UserEntraToken",
    "target": "https://{workspaceId}.z{xy}.w.api.fabric.microsoft.com/v1/mcp/workspaces/{workspaceId}/dataagents/{dataAgentId}/agent",
    "audience": "https://analysis.windows.net/powerbi/api",
    "isSharedToAll": true
  }
}
```

---

After you create the connection, reference it from your agent tool definition through its `project_connection_id`. The connection's `target` already points to the workspace private endpoint, so requests route over the workspace-level private link.

## Data governance and compliance

Fabric IQ processes requests within the Microsoft Fabric compliance boundary for your workspace's region. The following commitments apply when you route agent queries through Fabric IQ.

### Data residency

Fabric IQ retrieves and processes data within the region where your Microsoft Fabric workspace resides. Data doesn't cross regional boundaries during query execution. The applicable region and its compliance scope are determined by your workspace location — see [Microsoft Fabric region availability](/fabric/admin/region-availability) for the list of supported regions and the compliance frameworks each region satisfies.

> [!NOTE]
> If your Foundry project is in a different Azure region than your Fabric workspace, query results are returned cross-region. Review [Microsoft Fabric region availability](/fabric/admin/region-availability) and your organization's data residency requirements before connecting a Fabric workspace in a different region.

### Compliance certifications

Fabric IQ inherits Microsoft Fabric's compliance certifications for the workspace region. For compliance documentation, audit reports, and the frameworks applicable to each region, see [Microsoft Fabric region availability](/fabric/admin/region-availability).

## Admin management

### Grant admin consent

A Global Administrator must grant tenant-wide admin consent for the Entra app registration before users can authenticate with the Fabric IQ connection:

1. In the [Microsoft Entra admin center](https://entra.microsoft.com/), go to **Entra ID** > **App registrations** and select your app.
1. Select **API permissions**.
1. Select **Grant admin consent for {your-organization}** and approve. Each listed permission shows a green checkmark when consent is granted.

> [!NOTE]
> DataAgent.Execute.All also requires admin consent. If you use this permission for data agent connections, follow the same process.

### Restrict network access

To restrict agent traffic to your private network, configure Foundry Agent Service with a virtual network. See [Private networking for agents](../virtual-networks.md) for setup instructions. For the Fabric-side network options that each item type supports, see [Virtual network support](#virtual-network-support).

### Publish Fabric items before use

A Fabric admin must publish each Fabric item — ontology, data agent, or Power BI semantic model — before it can be consumed through Fabric IQ. Unpublished items aren't reachable at the MCP endpoint, and requests against them fail. Confirm that the item is published in the Microsoft Fabric portal before configuring the Foundry connection.

## Troubleshoot

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| 404 or `Not Found` error when connecting | The `server_url` is incorrect or the Fabric item isn't published. | Verify the workspace and item GUIDs in the Fabric portal URL. Confirm the item is published. |
| 401 Unauthorized | Admin consent hasn't been granted or the Entra app is misconfigured. | Verify admin consent was granted for all required API permissions. Check that the client ID, secret, and scopes match what you configured in Foundry. |
| `CONSENT_REQUIRED` error at runtime | The signed-in user hasn't completed the OAuth flow for the connection. | Open the consent URL returned in the error, complete the OAuth flow in a browser, then retry. |
| Empty or incorrect results from ontology queries | Ontology entities, properties, or data bindings are incomplete. | Verify the ontology item is published and that entity types, properties, and data bindings are fully configured in Fabric IQ. |
| Poor-quality answers from Power BI semantic models | The model doesn't have strong enough reasoning for complex measure queries. | Use a latest-generation model such as `gpt-5.4` or `opus 4.7`. These models handle semantic model complexity significantly better than older models. |
| Agent never calls the Fabric IQ tool | The model doesn't recognize when to delegate to Fabric IQ. | Add guidance in the system prompt, for example: *"Use the Fabric IQ tool for any question about business data, entities, metrics, or organizational knowledge."* |

## Related content

- [What is Fabric IQ (preview)?](/fabric/iq/overview)
- [What is ontology (preview)?](/fabric/iq/ontology/overview)
- [Fabric data agent concepts](/fabric/data-science/concept-data-agent)
- [Overview of the Power BI MCP servers (preview)](/power-bi/developer/mcp/mcp-servers-overview)
- [Tool best practices](../../concepts/tool-best-practice.md)
