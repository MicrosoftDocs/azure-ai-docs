---
title: "Create a private tool catalog in Foundry Agent Service"
description: "Create an organization-scoped private tool catalog for MCP servers using Azure API Center, then discover and configure it in Foundry Tools."
author: aahill
ms.author: aahi
ms.date: 01/20/2026
ms.manager: nitinme
ms.topic: how-to
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.custom: pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
---

# Create a private tool catalog (preview)

[!INCLUDE [preview-feature](../../../openai/includes/preview-feature.md)]

Use this article to create a private tool catalog for your organization by using [Azure API Center](/azure/api-center/register-discover-mcp-server). In Foundry Agent Service, developers can discover tools from your private catalog in Foundry Tools.

## Prerequisites

* A Foundry project. For setup guidance, see [Create projects in Microsoft Foundry](../../../how-to/create-projects.md).
* Permissions to discover and configure tools in your Foundry project. For more information, see [Role-based access control in Microsoft Foundry](../../../concepts/rbac-foundry.md).
* An [Azure API Center](/azure/api-center/set-up-api-center).

    > [!NOTE]
    > The API Center name is the name that developers use to find the catalog in Foundry Tools. Use a descriptive name.

* One or more remote MCP servers that you want to share with your organization. Register them with API Center by following [Configure environments and deployments in Azure API Center](/azure/api-center/tutorials/configure-environments-deployments).

## Plan access for admins and developers

Decide who manages the catalog and who consumes it.

| Goal | Who | Where | What to do |
|---|---|---|---|
| Create and manage the tool catalog | Catalog admins | Azure API Center | Create the API Center resource, register MCP servers, and (optionally) configure authorization settings. |
| Discover tools from the private catalog | Developers | Azure API Center (RBAC) | Assign access so developers can view the registered MCP servers. |
| Configure and use tools | Developers | Foundry project | Confirm developers can access the Foundry project and can configure tools in Foundry Tools. |

## Configure authentication (optional)

If your remote MCP server requires authentication, configure it in Azure API Center.

1. In the [Azure portal](https://portal.azure.com), go to your API Center resource.
1. Select **Governance** > **Authorization**.

    :::image type="content" source="../media/tool-catalog/api-center-resource.png" alt-text="Screenshot of the Azure API Center resource page in the Azure portal." lightbox="../media/tool-catalog/api-center-resource.png":::

1. Select **Add configuration**.
1. Under **Security scheme**, choose the scheme required by your MCP server (for example, **API Key**, **OAuth**, or **HTTP** bearer token), then provide the required values.

    > [!IMPORTANT]
    > Treat any credentials as secrets. Don't paste secrets into prompts or source control. For guidance on authentication approaches in Agent Service (including shared and per-user authentication), see [MCP server authentication](mcp-authentication.md).

1. Select the MCP server, then select **Details** > **Versions** > **Manage access (preview)**.

    :::image type="content" source="../media/tool-catalog/api-center-versions.png" alt-text="Screenshot of the Versions page for an API Center entry in the Azure portal." lightbox="../media/tool-catalog/api-center-versions.png":::

1. Select the authorization configuration you created.

## Give access to your organization

To let developers discover MCP servers from your private tool catalog in Foundry Tools, assign them access to the API Center resource.

1. Decide whether to grant access to a security group or to individual users.
1. Assign at least the [Azure API Center Data Reader](/azure/role-based-access-control/built-in-roles/integration#azure-api-center-data-reader) role (or an equivalent custom role) to those users.

## Verify the private tool catalog in Foundry Tools

After you grant access, confirm that developers can find the catalog in Foundry.

1. In the Foundry portal, open the project that your developers use.
1. Go to **Build** > **Tools**.
1. Use search and filters to find your private tool catalog by the API Center name.
1. Select a tool from the catalog and review its setup requirements.

To add an MCP server tool to an agent, see [Connect to Model Context Protocol servers](tools/model-context-protocol.md).

## Troubleshooting

| Issue | Cause | Resolution |
|---|---|---|
| You can't find the private tool catalog in Foundry Tools. | You don't have access to the API Center resource, or you're in the wrong Foundry project. | Confirm you have the required API Center role assignment, then confirm you're in the expected Foundry project and go to **Build** > **Tools**. |
| You can see the catalog, but you can't configure a tool. | The tool requires authentication or configuration values you don't have. | Review the tool's setup requirements, then ask a catalog admin for the required access. For MCP authentication options, see [MCP server authentication](mcp-authentication.md). |
| Tool calls fail after configuration. | Authentication is incorrect, expired, or not supported by the MCP server. | Re-check the authentication method required by the MCP server, and validate the credential format. For guidance, see [MCP server authentication](mcp-authentication.md). |

## Next steps

> [!div class="nextstepaction"]
> [Discover and manage tools in the Foundry tool catalog](../concepts/tool-catalog.md)

> [!div class="nextstepaction"]
> [Connect to Model Context Protocol servers](tools/model-context-protocol.md)
