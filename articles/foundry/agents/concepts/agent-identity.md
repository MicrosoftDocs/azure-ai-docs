---
title: "Agent identity concepts in Microsoft Foundry"
description: "Learn how agent identities and agent identity blueprints work in Microsoft Foundry, including RBAC, authentication for tools, and governance."
#customer intent: As a security administrator, I want to know how an agent identity eliminates the need for passwords and certificates so that I can reduce security risks in my environment.
author: sdgilley
ms.author: sgilley
ms.reviewer: fosteramanda
ms.date: 04/13/2026
ms.topic: concept-article
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ai-usage: ai-assisted
ms.custom: pilot-ai-workflow-jan-2026, doc-kit-assisted
---

# Agent identity concepts in Microsoft Foundry
An *agent identity* is a specialized identity type in [Microsoft Entra ID](/entra/fundamentals/what-is-entra) that's designed specifically for AI agents. It provides a standardized framework for governing, authenticating, and authorizing AI agents across Microsoft services. This framework enables agents to securely access resources, interact with users, and communicate with other systems.

Microsoft Foundry automatically provisions and manages agent identities throughout the agent lifecycle. This integration simplifies permission management while maintaining security and auditability as agents move from development to production.

This article explains how agent identities relate to Microsoft Entra ID objects, how Foundry uses them when an agent calls tools, and how to apply least-privilege access with Azure role-based access control (RBAC).

## Prerequisites

* Understanding of [Microsoft Entra ID and OAuth](/entra/architecture/auth-sync-overview) authentication
* Familiarity with [Azure role-based access control (RBAC)](/azure/role-based-access-control/overview)
* Basic knowledge of AI agents and their runtime requirements

For Foundry-specific RBAC roles and scopes, see [Azure role-based access control in Foundry](../../concepts/rbac-foundry.md).

## How agent identities work in Foundry

Foundry uses Microsoft Entra ID agent identities to support two related needs:

- **Management and governance**: Give administrators a consistent way to inventory agents, apply policies, and audit activity.
- **Tool authentication**: Let an agent authenticate to downstream systems (for example, Azure Storage) without embedding secrets in prompts, code, or connection strings.

At a high level, Foundry does the following:

1. Provisions an **agent identity blueprint** and one or more **agent identities** in Microsoft Entra ID.
2. Assigns RBAC roles (or other permission models, depending on the target system) to the agent identity.
3. When the agent invokes a tool, Foundry requests an access token for the downstream service and uses that token to authenticate the tool call.

### Runtime token exchange

When an agent invokes a tool, a multi-step OAuth 2.0 token exchange occurs automatically between Agent Service, Microsoft Entra ID, and the downstream resource. Developers don't manage tokens directly — Agent Service handles the entire exchange.

The exchange progresses through four stages:

- **Blueprint authentication**: Agent Service presents the blueprint's OAuth credentials to Microsoft Entra ID. This proves that Agent Service is authorized to act on behalf of the blueprint and its agent identities.

- **Agent identity token issuance**: Microsoft Entra ID validates the blueprint credentials and issues a token for the specific agent identity. This token is distinct from human user or managed identity tokens — it identifies the agent as an independent actor in the directory.

- **Scoped token request**: Agent Service presents the agent identity token back to Microsoft Entra ID and requests a new access token scoped to the **audience** of the downstream service. The audience is the OAuth resource identifier for the target service (for example, `https://storage.azure.com` for Azure Storage).

- **Authenticated tool call**: Agent Service passes the scoped access token to the MCP server or A2A endpoint. The downstream resource validates the token and checks the agent identity's RBAC role assignments before granting or denying access.

The following table lists common audience values for global Azure services:

| Downstream service | Audience value |
| --- | --- |
| Azure Storage | `https://storage.azure.com` |
| Azure Logic Apps | `https://logic.azure.com` |
| Azure Cosmos DB | `https://cosmos.azure.com` |
| Microsoft Graph | `https://graph.microsoft.com` |
| Azure Key Vault | `https://vault.azure.net` |

> [!IMPORTANT]
> An incorrect audience value causes authentication failures even when RBAC roles are correctly assigned. The audience must match the resource identifier of the downstream service, not the URL of the MCP server itself.

### Terms used in this article

| Term | What it means in Foundry |
| --- | --- |
| Agent identity | A Microsoft Entra ID service principal that represents the agent at runtime. |
| Agent identity blueprint | A Microsoft Entra ID object that governs a class of agent identities and is used for lifecycle operations. |
| `agentIdentityId` | The identifier you use when assigning permissions to the agent identity. |
| Audience | The resource identifier for the downstream service the token is meant for (for example, `https://storage.azure.com`). |

## Key concepts

The Agent ID platform framework introduces formal *agent identities* and *agent identity blueprints* in Microsoft Entra ID to represent AI agents. You can use this framework to securely communicate with AI agents. This framework also enables those AI agents to securely communicate with web services, other AI agents, and various systems.

> [!NOTE]
> The Microsoft Entra Agent ID framework is currently in preview. Features and APIs might change before general availability.

### Agent identity

An agent identity is a special service principal in Microsoft Entra ID. It represents an identity that the agent identity blueprint created and is authorized to impersonate.

#### Security benefits

Agent identities help address specific security challenges that AI agents pose:

* Distinguish operations that AI agents perform from operations that workforce, customer, or workload identities perform.
* Enable AI agents to gain right-sized access across systems.
* Prevent AI agents from gaining access to critical security roles and systems.
* Scale identity management to large numbers of AI agents that can be quickly created and destroyed.

#### Authentication capabilities

Agent identities support two key authentication scenarios:

* **Attended (delegated access or on-behalf-of flow)**: The agent operates on behalf of a human user, using the OAuth 2.0 on-behalf-of (OBO) flow. The user first authenticates to the application, and the application passes the user's token to Agent Service. Agent Service then exchanges that token for one that carries both the agent identity and the user's delegated permissions. This approach means the agent can only access resources that the user has consented to and is authorized for.
* **Unattended (application-only flow)**: The agent acts under its own authority, using the OAuth 2.0 client credentials flow. Agent Service authenticates the blueprint to Microsoft Entra ID, obtains a token for the agent identity, and requests a scoped access token for the downstream resource. The agent's access is governed entirely by its own RBAC role assignments, Microsoft Graph app-level permissions, or other authorization policies — no human user is involved.

### Agent identity blueprint

An agent identity blueprint serves as the reusable, governing template from which all associated agent identities are created. It corresponds to a *kind*, *type*, or *class* of agents. It acts as the management object for all agent identity instances of that class.

#### Blueprint capabilities

Agent identity blueprints serve three essential purposes:

**Type classification**: The blueprint establishes the category of agent, such as "Contoso Sales Agent." This classification enables administrators to:

* Apply Conditional Access policies to all agents of that type.
* Disable or revoke permissions for all agents of that kind.
* Audit and govern agents at scale through consistent, blueprint-based controls.

**Identity creation authority**: Services that create agent identities use the blueprint to authenticate. Blueprints have OAuth credentials that services use to request tokens from Microsoft Entra ID for creating, updating, or deleting agent identities. These credentials include client secrets, certificates, or federated credentials like managed identities.

**Runtime authentication platform**: The hosting service uses the blueprint during runtime authentication. The service requests an access token by using the blueprint's OAuth credentials. It then presents that token to Microsoft Entra ID to obtain a token for one of its agent identities.

#### Blueprint metadata

For example, an organization might use an AI agent called the "Contoso Sales Agent." The blueprint defines information such as:

* The name of the agent type: "Contoso Sales Agent."
* The publisher or organization responsible for the blueprint: "Contoso."
* The roles that the agent might perform: "sales manager" or "sales rep."
* Microsoft Graph permissions or delegated scopes: "read the signed-in user's calendar."

### Federated identity credentials

The blueprint's OAuth credentials determine how Agent Service authenticates to Microsoft Entra ID during the [runtime token exchange](#runtime-token-exchange). Blueprints support three credential types:

| Credential type | How it works | Trade-offs |
| --- | --- | --- |
| Client secret | A shared secret string stored in the blueprint's Entra ID registration. | Simplest to configure, but requires manual rotation and secure storage. |
| Certificate | An X.509 certificate used for assertion-based authentication. | Stronger than client secrets, but requires certificate lifecycle management. |
| Federated credential (managed identity) | A trust relationship between the blueprint and a managed identity or service principal. No secret is stored in the blueprint. | Recommended for production. Azure manages credential rotation automatically. |

The federated credential option is the most relevant to Foundry. When Foundry provisions an agent identity blueprint for your project, the blueprint establishes a trust relationship with the project's managed identity. The authentication chain works as follows:

- The **agent identity blueprint** has a federated credential trust relationship with the project's **managed identity**.
- At runtime, Agent Service uses the managed identity to authenticate the blueprint to **Microsoft Entra ID**. No client secret or certificate is needed.
- Entra ID validates the federated credential and issues a token for the **agent identity** (the service principal).
- The agent identity token is then exchanged for a **scoped access token** targeting the downstream resource's audience.

This chain is designed to eliminate stored secrets in the blueprint configuration. Azure manages credential rotation through the managed identity's infrastructure, and each layer — managed identity, agent identity, and downstream resource — has independent, least-privilege role assignments. However, some tool configurations still expose the project managed identity as an authentication option.

> [!NOTE]
> The managed identity authenticates the *blueprint* to Entra ID. It doesn't directly access the downstream resource. The agent identity — not the managed identity — is the principal that requires RBAC role assignments on the target resource.

## Foundry integration

Foundry automatically integrates with Microsoft Entra Agent ID by creating and managing identities throughout the agent development lifecycle. When you create your first agent in a Foundry project, the system provisions a default agent identity blueprint and a default agent identity for your project.

### Shared project identity

All unpublished or in-development agents within the same project share a common identity. This design simplifies permission management because unpublished agents typically require the same access patterns and permission configurations. The shared identity approach provides these benefits:

* **Simplified administration**: Administrators can centrally manage permissions for all in-development agents within a project.
* **Reduced identity sprawl**: Using a single identity per project prevents unnecessary identity creation during early experimentation.
* **Developer autonomy**: After the shared identity is configured, developers can independently build and test agents without repeatedly configuring new permissions.

To find your shared agent identity blueprint and agent identity, go to your Foundry project in the [Azure portal](https://portal.azure.com). On the **Overview** pane, select **JSON View**. Choose the latest API version to view and copy the identities.

:::image type="content" source="../media/agent-identity/azure-agent-identity-json-view.png" alt-text="Screenshot of the JSON view in the Azure portal displaying an agent identity blueprint and agent identity details for a Foundry project." lightbox="../media/agent-identity/azure-agent-identity-json-view.png":::

### Distinct agent identity

When an agent's permissions, auditability, or lifecycle requirements diverge from the project defaults, you should upgrade to a distinct identity. Publishing an agent automatically creates a dedicated agent identity blueprint and agent identity. Both are bound to the agent application resource. This distinct identity represents the agent's system authority for accessing its own resources.

Common scenarios that require distinct identities include:

* Agents ready for integration testing.
* Agents prepared for production consumption.
* Agents that require unique permission sets.
* Agents that need independent audit trails.

To find the distinct agent identity blueprint and agent identity, go to your agent application resource in the Azure portal. On the **Overview** pane, select **JSON View**. Choose the latest API version to view and copy the identities.

## Tool authentication

Agents access remote resources and tools by using agent identities for authentication. The authentication mechanism differs based on the agent's publication status:

* **Unpublished agents**: Authenticate by using the shared project's agent identity.
* **Published agents**: Authenticate by using the unique agent identity that's associated with the agent application.

When you [publish an agent](../how-to/publish-agent.md), you must reassign RBAC permissions to the new agent identity for any resources that the agent needs to access. This reassignment ensures that the published agent maintains appropriate access while operating under its distinct identity.

### Assign permissions to the agent identity

The agent identity is a service principal in Microsoft Entra ID. You assign RBAC roles to it the same way you assign roles to any other service principal or managed identity. Use the `agentIdentityId` from your project or agent application's JSON view as the assignee.

For example, to grant an agent identity read/write access to a storage account, assign the **Storage Blob Data Contributor** role at the storage account scope:

```azurecli
az role assignment create \
    --assignee "<agentIdentityId>" \
    --role "Storage Blob Data Contributor" \
    --scope "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.Storage/storageAccounts/<storage-account>"
```

To verify the assignment:

```azurecli
az role assignment list \
    --assignee "<agentIdentityId>" \
    --scope "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.Storage/storageAccounts/<storage-account>" \
    --output table
```

Common role assignments for agent tools:

| Tool scenario | Required role | Target scope |
| --- | --- | --- |
| MCP server that reads/writes blobs | Storage Blob Data Contributor | Storage account |
| MCP server that triggers logic apps | Logic Apps Standard Operator (Preview) | Logic App resource |
| A2A tool that queries Cosmos DB | Cosmos DB Built-in Data Reader | Cosmos DB account |

> [!IMPORTANT]
> When you publish an agent, it receives a new distinct `agentIdentityId`. Repeat these role assignments for the new identity. The shared project identity roles don't carry over to the published agent's identity.

### Supported tools

Currently, the tools that support authentication with an agent identity are:

* **Model Context Protocol (MCP)**: Use your agent's identity to authenticate with MCP servers that support agent identity authentication (preview). For details, see [Model Context Protocol](../how-to/tools/model-context-protocol.md) and [MCP server authentication](../how-to/mcp-authentication.md).
* **Agent-to-Agent (A2A)**: Enable secure communication between agents by using agent identities (preview). For details, see [Agent-to-Agent tool](../how-to/tools/agent-to-agent.md) and [Agent2Agent (A2A) authentication](./agent-to-agent-authentication.md).

Other tools and integrations might use different authentication methods (for example, key-based authentication or OAuth identity passthrough). Use the tool documentation to confirm supported authentication.

### Configure tool connections

To connect an MCP server or A2A endpoint with agent identity authentication, create a project connection that specifies the authentication type and the target audience for the downstream service. The authentication type depends on the tool:

| Tool type | Auth type value | Connection category |
| --- | --- | --- |
| MCP server | `AgenticIdentityToken` | `RemoteTool` |
| A2A endpoint | `AgenticIdentity` | `RemoteA2A` |

When the agent invokes the tool, Agent Service uses the agent identity to obtain an access token scoped to the **audience** value, then passes that token to the tool endpoint for authentication.

For step-by-step configuration instructions, see:

- [Set up MCP server authentication](../how-to/mcp-authentication.md#use-agent-identity-authentication-preview)
- [Agent2Agent (A2A) authentication](./agent-to-agent-authentication.md)

## Security considerations

Agent identities help you reduce risk by removing the need to embed long-lived credentials in agent configurations. Use these practices to keep access least-privilege and auditable:

- Assign only the permissions the agent needs for its tool actions. Prefer narrow scopes (resource or resource group) over subscription-wide access.
- Treat the shared project identity as a broader blast radius. If an agent needs tighter controls or separate auditing, publish it so it gets a distinct identity, and assign roles to that new identity.
- Review and log access to non-Microsoft tools and servers. If a tool call leaves Microsoft services, your data handling and retention depend on the external provider.

## Limitations

- Only some tools currently support agent identity authentication. Check the tool documentation for supported authentication.
- Publishing an agent changes which identity is used for tool calls (shared project identity versus distinct agent identity). Plan for role reassignment when you publish.

## Common issues

These issues commonly cause tool authentication failures when using agent identities:

- **Roles assigned to the wrong identity**: Confirm you granted permissions to the current identity used by the agent (shared project identity for unpublished agents, distinct identity for published agents).
- **Missing role assignments**: Ensure the agent identity has the required RBAC role on the target resource. For Foundry roles and scopes, see [Azure role-based access control in Foundry](../../concepts/rbac-foundry.md).
- **Incorrect audience**: Ensure the audience matches the downstream service you’re calling (for example, `https://storage.azure.com` for Azure Storage).

For tool-specific troubleshooting, see the tool documentation:

- [Model Context Protocol](../how-to/tools/model-context-protocol.md)
- [Agent-to-Agent tool](../how-to/tools/agent-to-agent.md)

## Manage agent identities

Agent identities persist as long as the associated Foundry project or agent application resource exists. When you delete a Foundry project, the associated agent identity blueprint and shared agent identity are removed. Published agents have their own identity lifecycle tied to the agent application resource — deleting the agent application removes its distinct identity.

You can view and manage all agent identities in your tenant through the Microsoft Entra admin center. Sign in to the [Microsoft Entra admin center](https://entra.microsoft.com) and browse to **Entra ID** > **Agent ID** > **All agent identities** to see an inventory of all agents in your tenant, including Foundry agents, Microsoft Copilot Studio agents, and others.

:::image type="content" source="../media/agent-identity/entra-admin-center-agent-identities.png" alt-text="Screenshot of the Microsoft Entra admin center that shows the tab for agent identities with an inventory of all agents in the tenant." lightbox="../media/agent-identity/entra-admin-center-agent-identities.png":::

In this experience, you can enable built-in security controls, including:

* **Conditional Access**: Apply access policies to agent identities.
* **Identity protection**: Monitor and protect agent identities from threats.
* **Network access**: Control network-based access for agents.
* **Governance**: Manage expiration, owners, and sponsors for agent identities.

For more information about Microsoft Entra Agent ID features, see [Microsoft Entra documentation](/entra/fundamentals/what-is-entra).

## Related content

* [Publish and share agents in Microsoft Foundry](../how-to/publish-agent.md)
* [Azure role-based access control in Foundry](../../concepts/rbac-foundry.md)
* [MCP server authentication](../how-to/mcp-authentication.md)
* [Agent2Agent (A2A) authentication](./agent-to-agent-authentication.md)
* [Microsoft Entra Agent ID documentation](/entra/agent-id/)
