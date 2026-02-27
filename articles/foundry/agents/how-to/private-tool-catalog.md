---
title: "Create a private tool catalog in Foundry Agent Service"
description: "Create a private tool catalog in Foundry Agent Service using Azure API Center. Let developers discover and configure organization-scoped MCP server tools."
author: aahill
ms.author: aahi
ms.date: 02/03/2026
ms.manager: nitinme
ms.topic: how-to
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.custom: pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
#CustomerIntent: As a platform admin, I want to create a private tool catalog so that developers in my organization can discover and use approved MCP server tools.
---

# Create a private tool catalog (preview)

[!INCLUDE [preview-feature](../../../openai/includes/preview-feature.md)]

Create a private tool catalog so developers in your organization can discover, configure, and use MCP server tools through Foundry Tools. A private tool catalog uses [Azure API Center](/azure/api-center/register-discover-mcp-server) to register organization-scoped tools that only your developers can access.

## Prerequisites

* A Foundry project. For setup guidance, see [Create projects in Microsoft Foundry](../../../how-to/create-projects.md).
* Permissions to discover and configure tools in your Foundry project. For more information, see [Role-based access control in Microsoft Foundry](../../../concepts/rbac-foundry.md).
* An [Azure API Center](/azure/api-center/set-up-api-center).

    > [!NOTE]
    > The API Center name is the name that developers use to find the catalog in Foundry Tools. Use a descriptive name.

* One or more remote MCP servers that you want to share with your organization. Register them with API Center by following [Configure environments and deployments in Azure API Center](/azure/api-center/tutorials/configure-environments-deployments).

## Plan administrator and developer access

Before you create the catalog, decide who manages it and who consumes it.

| Goal | Who | Where | What to do |
|---|---|---|---|
| Create and manage the tool catalog | Catalog admins | Azure API Center | Create the API Center resource, register MCP servers, and (optionally) configure authorization settings. |
| Discover tools from the private catalog | Developers | Azure API Center (RBAC) | Assign access so developers can view the registered MCP servers. |
| Configure and use tools | Developers | Foundry project | Confirm developers can access the Foundry project and can configure tools in Foundry Tools. |

## Configure MCP server authentication

If your remote MCP server requires authentication, configure the authentication settings in Azure API Center. This step is optional if your MCP server doesn't require authentication.

1. In the [Azure portal](https://portal.azure.com), go to your API Center resource.
1. Select **Governance** > **Authorization**.

    :::image type="content" source="../media/tool-catalog/api-center-resource.png" alt-text="Screenshot that shows the Governance menu expanded with the Authorization option selected in Azure API Center." lightbox="../media/tool-catalog/api-center-resource.png":::

1. Select **Add configuration**.
1. Under **Security scheme**, choose the scheme required by your MCP server (for example, **API Key**, **OAuth**, or **HTTP** bearer token), then provide the required values.

    > [!IMPORTANT]
    > Treat any credentials as secrets. Don't paste secrets into prompts or source control. For guidance on authentication approaches in Agent Service (including shared and per-user authentication), see [MCP server authentication](mcp-authentication.md).

1. Select the MCP server, then select **Details** > **Versions** > **Manage access (preview)**.

    :::image type="content" source="../media/tool-catalog/api-center-versions.png" alt-text="Screenshot that shows the Versions page with the Manage access option for configuring authorization in Azure API Center." lightbox="../media/tool-catalog/api-center-versions.png":::

1. Select the authorization configuration you created.

After you complete these steps, the MCP server is configured to use the selected authentication scheme when developers invoke it from Foundry Tools.

## Grant developer access to the catalog

Assign Azure RBAC permissions so developers can discover MCP servers from your private tool catalog in Foundry Tools.

1. Decide whether to grant access to a security group or to individual users.
1. Assign at least the [Azure API Center Data Reader](/azure/role-based-access-control/built-in-roles/integration#azure-api-center-data-reader) role (or an equivalent custom role) to those users.

> [!NOTE]
> Role assignments can take up to 24 hours to propagate. If developers don't see the catalog immediately, wait and try again.

## Verify catalog discovery in Foundry Tools

After you grant access, confirm that developers can find and use the catalog in the Foundry portal.

1. In the Foundry portal, open the project that your developers use.
1. Go to **Build** > **Tools**.
1. Use search and filters to find your private tool catalog by the API Center name.
1. Select a tool from the catalog and review its setup requirements.

If the catalog appears and displays your registered MCP servers, the configuration is complete. To add an MCP server tool to an agent, see [Connect to Model Context Protocol servers](tools/model-context-protocol.md).

## Troubleshoot private tool catalog issues

If you encounter problems setting up or using your private tool catalog, use the following table to identify and resolve common issues.

| Issue | Cause | Resolution |
|---|---|---|
| The private tool catalog doesn't appear in Foundry Tools. | You don't have access to the API Center resource, or you're in the wrong Foundry project. | Confirm you have the Azure API Center Data Reader role assignment. Then confirm you're in the expected Foundry project and go to **Build** > **Tools**. |
| The catalog appears, but you can't configure a tool. | The tool requires authentication or configuration values you don't have. | Review the tool's setup requirements, then ask a catalog admin for the required access. For MCP authentication options, see [MCP server authentication](mcp-authentication.md). |
| Tool calls fail after configuration. | Authentication is incorrect, expired, or not supported by the MCP server. | Re-check the authentication method required by the MCP server, and validate the credential format. For guidance, see [MCP server authentication](mcp-authentication.md). |
| The catalog doesn't appear after role assignment. | Azure RBAC role assignments can take up to 24 hours to propagate. | Wait up to 24 hours and try again. If the issue persists, verify the role assignment in the Azure portal under **Access control (IAM)**. |
| MCP server shows as unavailable. | The MCP server URL changed, or the server is offline. | Verify the MCP server endpoint is accessible. Update the server registration in API Center if the URL changed. |
| OAuth authentication prompts repeatedly. | Token expiration or consent not granted. | Ensure users grant consent when prompted. For long-running sessions, tokens might expire. Re-authenticate through the tool configuration. |

## Related content

[Discover and manage tools in the Foundry tool catalog](../concepts/tool-catalog.md)

[Connect to Model Context Protocol servers](tools/model-context-protocol.md)
