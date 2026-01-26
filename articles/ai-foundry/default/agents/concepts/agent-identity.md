---
title: Manage agent identities with Microsoft Entra ID
titleSuffix: Microsoft Foundry
description: Learn how agent identities and agent identity blueprints work in Microsoft Foundry, including RBAC, authentication for tools, and governance.
#customer intent: As a security administrator, I want to know how an agent identity eliminates the need for passwords and certificates so that I can reduce security risks in my environment.
author: sdgilley
ms.author: sgilley
ms.reviewer: fosteramanda
ms.date: 01/20/2026
ms.topic: concept-article
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ai-usage: ai-assisted
ms.custom: pilot-ai-workflow-jan-2026
---

# Agent identity concepts in Microsoft Foundry

An *agent identity* is a specialized identity type in [Microsoft Entra ID](/entra/fundamentals/what-is-entra) that's designed specifically for AI agents. It provides a standardized framework for governing, authenticating, and authorizing AI agents across Microsoft services. This framework enables agents to securely access resources, interact with users, and communicate with other systems.

Microsoft Foundry automatically provisions and manages agent identities throughout the agent lifecycle. This integration simplifies permission management while maintaining security and auditability as agents move from development to production.

This article explains how agent identities relate to Microsoft Entra ID objects, how Foundry uses them when an agent calls tools, and how to apply least-privilege access with Azure role-based access control (RBAC).

## Prerequisites

* Understanding of [Microsoft Entra ID and OAuth](/entra/architecture/auth-sync-overview) authentication
* Familiarity with [Azure role-based access control (RBAC)](/azure/role-based-access-control/overview)
* Basic knowledge of AI agents and their runtime requirements

For Foundry-specific RBAC roles and scopes, see [Azure role-based access control in Foundry](../../../concepts/rbac-foundry.md).

## How agent identities work in Foundry

Foundry uses Microsoft Entra ID agent identities to support two related needs:

- **Management and governance**: Give administrators a consistent way to inventory agents, apply policies, and audit activity.
- **Tool authentication**: Let an agent authenticate to downstream systems (for example, Azure Storage) without embedding secrets in prompts, code, or connection strings.

At a high level, Foundry does the following:

1. Provisions an **agent identity blueprint** and one or more **agent identities** in Microsoft Entra ID.
2. Assigns RBAC roles (or other permission models, depending on the target system) to the agent identity.
3. When the agent invokes a tool, Foundry requests an access token for the downstream service and uses that token to authenticate the tool call.

### Terms used in this article

| Term | What it means in Foundry |
| --- | --- |
| Agent identity | A Microsoft Entra ID service principal that represents the agent at runtime. |
| Agent identity blueprint | A Microsoft Entra ID object that governs a class of agent identities and is used for lifecycle operations. |
| `agentIdentityId` | The identifier you use when assigning permissions to the agent identity. |
| Audience | The resource identifier for the downstream service the token is meant for (for example, `https://storage.azure.com`). |

## Key concepts

The Agent ID platform framework introduces formal *agent identities* and *agent identity blueprints* in Microsoft Entra ID to represent AI agents. You can use this framework to securely communicate with AI agents. This framework also enables those AI agents to securely communicate with web services, other AI agents, and various systems.

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

* **Attended (delegated access or on-behalf-of flow)**: The agent operates on behalf of a human user. It uses delegated permissions that the user grants. The agent can then act under the user's authority to access resources or APIs as that user.
* **Unattended**: The agent acts under its own authority. It acts as a service or an application identity by using its app-assigned roles, RBAC, or Microsoft Graph permissions. Or it acts as an autonomous identity with user-like claims that allow the agent to authenticate and operate independently.

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

### Supported tools

Currently, the tools that support authentication with an agent identity are:

* **Model Context Protocol (MCP)**: Use your agent's identity to authenticate with MCP servers that support agent identity authentication. For details, see [Model Context Protocol (preview)](../how-to/tools/model-context-protocol.md) and [MCP server authentication](../how-to/mcp-authentication.md).
* **Agent-to-Agent (A2A)**: Enable secure communication between agents by using agent identities. For details, see [Agent-to-Agent tool (preview)](../how-to/tools/agent-to-agent.md) and [Agent2Agent (A2A) authentication](./agent-to-agent-authentication.md).

Other tools and integrations might use different authentication methods (for example, key-based authentication or OAuth identity passthrough). Use the tool documentation to confirm supported authentication.

### Configure MCP tool authentication

To configure an MCP tool to authenticate by using an agent identity:

1. Ensure that you have an MCP server that you want to configure as a tool for your agent.

1. Get the ID for the agent identity. In the Azure portal, go to your Foundry project. On the **Overview** pane, select **JSON View** and choose the latest API version. Copy the `agentIdentityId` value.

1. Create a connection to your remote MCP server that uses `AgenticIdentityToken` as the authentication type. The **Audience** box specifies which service or API the token is intended to access. For example:

   * For an MCP server that lists blobs in your storage account, set the audience as `https://storage.azure.com`.
   * For an Azure Logic Apps MCP server, set the audience as `https://logic.azure.com`.

    You can create the connection by using either the REST API or the Foundry portal:

    #### [REST API](#tab/rest-api)

    To get an access token, run the commands `az login` and then `az account get-access-token`.

    ```http
    PUT https://management.azure.com/subscriptions/{{subscription_id}}/resourceGroups/{{resource_group}}/providers/Microsoft.CognitiveServices/accounts/{{account_name}}/projects/{{project_name}}/connections/{{mcp_connection_name}}?api-version={{api_version}}
    Authorization: Bearer {{token}}
    Content-Type: application/json
    
    {
        "tags": null,
        "location": null,
        "name": "{YOUR_CONNECTION_NAME}",
        "type": "CognitiveServices/accounts/projects/connections",
        "properties": {
        "authType": "AgenticIdentityToken",
        "group": "ServicesAndApps",
        "category": "RemoteTool",
        "expiryTime": null,
        "target": "{YOUR_MCP_REMOTE_URL}",
        "isSharedToAll": true,
        "sharedUserList": [],
        "audience": "{YOUR_AUDIENCE}",
        "Credentials": {},
        "metadata": {
            "ApiType": "Azure"
        }
        }
    }
    ```
    
    #### [Foundry portal](#tab/foundry-portal)
    1. [!INCLUDE [foundry-sign-in](../../includes/foundry-sign-in.md)]

    1. Select **Build**.

    1. Select **Agents**.

    1. Select the agent that you want to use.

    1. Under **Tools**, select **+ Add**.

    1. On the **Custom** tab, select **Model Context Protocol (MCP)**.

    1. Under **Authentication**, select **Microsoft Entra**. Under  **Type**, select **Agent identity**.

    1. Fill in the endpoint and audience information, and then select **Connect**.

    ---

1. Assign to the agent identity the required permissions for its actions by using the `agentIdentityId` value that you copied. For example:

   * For an MCP server that lists blob containers, assign the **Storage Blob Data Contributor** role at the **Azure Storage Account** scope.
   * For an Azure Logic Apps MCP server, assign the **Logic Apps Standard Reader** role on the **Logic App** resource.

1. Connect the tool. If you're using code, create an agent with the MCP tool. (For details, see the MCP documentation.) If you're using the Foundry portal, the MCP tool is automatically added to the agent.

When the agent invokes the MCP server, it uses the available agent identity to obtain an authorization token for the **audience** value. It then passes the token to the MCP server for authentication.

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
- **Missing role assignments**: Ensure the agent identity has the required RBAC role on the target resource. For Foundry roles and scopes, see [Azure role-based access control in Foundry](../../../concepts/rbac-foundry.md).
- **Incorrect audience**: Ensure the audience matches the downstream service you’re calling (for example, `https://storage.azure.com` for Azure Storage).

For tool-specific troubleshooting, see the tool documentation:

- [Model Context Protocol (preview)](../how-to/tools/model-context-protocol.md)
- [Agent-to-Agent tool (preview)](../how-to/tools/agent-to-agent.md)

## Manage agent identities

You can view and manage all agent identities in your tenant through the Microsoft Entra admin center. Go to the [tab for agent identities](https://entra.microsoft.com/?Microsoft_AAD_RegisteredApps=stage1&exp.EnableAgentIDUX=true#view/Microsoft_AAD_RegisteredApps/AllAgents.MenuView/~/allAgentIds) to see an inventory of all agents in your tenant, including Foundry agents, Microsoft Copilot Studio agents, and others.

:::image type="content" source="../media/agent-identity/entra-admin-center-agent-identities.png" alt-text="Screenshot of the Microsoft Entra admin center that shows the tab for agent identities with an inventory of all agents in the tenant." lightbox="../media/agent-identity/entra-admin-center-agent-identities.png":::

In this experience, you can enable built-in security controls, including:

* **Conditional Access**: Apply access policies to agent identities.
* **Identity protection**: Monitor and protect agent identities from threats.
* **Network access**: Control network-based access for agents.
* **Governance**: Manage expiration, owners, and sponsors for agent identities.

For more information about Microsoft Entra Agent ID features, see [Microsoft Entra documentation](/entra/fundamentals/what-is-entra).

## Related content

* [Publish and share agents in Microsoft Foundry](../how-to/publish-agent.md)
* [Azure role-based access control in Foundry](../../../concepts/rbac-foundry.md)
* [MCP server authentication](../how-to/mcp-authentication.md)
