---
title: "Explore Foundry MCP Server best practices and security guidance"
description: "Security guidance for Foundry MCP Server, including identity, RBAC, Conditional Access policies, network isolation, and data residency."
keywords: mcp, foundry mcp server, security, entra id, rbac
author: sdgilley
ms.author: sgilley
ms.reviewer: sehan
ms.date: 04/02/2026
ms.topic: concept-article
ms.service: azure-ai-foundry
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# Foundry MCP Server best practices and security guidance
Foundry MCP Server (preview) tools automate read and write operations across Foundry resources, including deployments, datasets, evaluations, monitoring, and analytics. This guidance helps you verify intent, reduce risk, and apply security and governance practices before you run MCP tools.

In this article, you learn about:

- How to interpret MCP Server responses and verify accuracy
- The impact of write operations on Foundry resources
- Best practices for safe tool execution, resource management, and change tracking
- Security and governance controls, including identity, RBAC, Conditional Access, network isolation, and data residency
- Troubleshooting common issues

[!INCLUDE [preview-feature](../openai/includes/preview-feature.md)]

## Prerequisites

- An Azure account with an active subscription.
- A [Foundry project](../quickstarts/get-started-code.md) with Contributor or higher role.
- To configure Conditional Access policies, you need the [Conditional Access Administrator](/entra/identity/role-based-access-control/permissions-reference#conditional-access-administrator) role in Microsoft Entra ID.
- [Azure CLI](/cli/azure/install-azure-cli) (required only for the `az ad sp create` command).

## Interpreting the response

MCP Server provides output that is passed to the language model selected for your agent (for example, Visual Studio Code with GitHub Copilot). The language model combines this output with the conversation context to generate a final response based on its capabilities. Always verify the accuracy of the language model’s response. It may include details that are inferred or generated beyond the MCP Server’s original output.

## Impact of write operations

Write operations have a critical impact on Foundry resources. Proceed with caution and proper planning when you interact with Foundry MCP Server, just as you would when using the portal, SDKs, or REST APIs. For example:

- Deployments: Immediately affect live apps and billing.
- Deletions: Permanently remove resources and can break dependent services.
- Evaluations: Consume compute quota and incur costs.
- Datasets: Can overwrite existing versions.

Examples of resource impact:

- Deleting a deployment breaks all applications using that endpoint.
- Large evaluations can consume significant quota allocation.
- New deployments start billing immediately.
- Overwriting a dataset affects evaluation reproducibility.

## Best practices for safe execution

Follow these practices to make sure write operations run as you intend:

### Tool execution verification

- **Verify tool selection**: Confirm the correct MCP tool and parameters match your intention before execution.
- **Check parameters**: Review all tool parameters (resource IDs, deployment names, dataset paths) for accuracy. Common parameter formats include:

  | Parameter type | Format | Where to find it |
  | -------------- | ------ | ---------------- |
  | Foundry resource ID | `/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.CognitiveServices/accounts/{account_name}` | Azure portal **Properties** page for the account |
  | Project endpoint | `https://{account_name}.services.ai.azure.com/api/projects/{project_name}` | Foundry project details page |
  | Project resource ID | `/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.CognitiveServices/accounts/{account_name}/projects/{project_name}` | Azure portal **Properties** page or Foundry project details page |

  If you provide a project resource ID, the language model in your MCP host extracts the needed values and formulates the parameters to pass to MCP tools. Confirm before approval that the intended parameter values are passed to the MCP tools.
- **Check environment targeting**: Make sure resource endpoints and project URLs point to the intended environment.

### Resource management via MCP server

- **Check dependencies**: Use monitoring tools to make sure no app depends on a resource before you delete it.
- **Check quota**: Query quota status before you create new deployments or run large evaluations.
- **Resource discovery**: List existing deployments and datasets before making changes.
- **Plan capacity**: Check available quota and usage metrics before resource-intensive operations.

### Safe MCP operation practices

- **Test in nonproduction**: Use development project endpoints first.
- **Make incremental changes**: Change one resource at a time instead of making bulk updates.
- **Validate changes**: Use read-only tools to confirm changes take effect.
- **Handle errors**: Monitor responses for errors or unexpected results.

### Documentation and tracking

- **Log operations**: Use Azure resource Activity Logs to track affected resources.
- **Back up configuration**: Export current deployment and dataset configurations before you modify them.
- **Track changes**: Record MCP operation details for troubleshooting and rollback.

## Security and governance

This section summarizes identity, access control, policy, network isolation, and data residency considerations to help you apply governance before MCP operations.

### Identity and access management

Authenticate to Foundry MCP Server using a Microsoft Entra token scoped to `https://mcp.ai.azure.com`.

Azure role-based access control (RBAC) applies to all operations on Foundry resources supported by Foundry MCP Server. Operations run according to the authenticated user's permissions. The following table summarizes how RBAC roles map to MCP operation types:

| Operation type | Minimum required role | Examples |
| -------------- | --------------------- | -------- |
| Read (list, get, query) | Reader | List deployments, get model details, query evaluation results |
| Write (create, update) | Contributor | Create deployments, update datasets, start evaluations |
| Delete | Contributor | Delete deployments, remove datasets |
| Manage access | Owner or User Access Administrator | Assign roles, manage permissions |

For more information on role assignments, see [Role-based access control for Microsoft Foundry](../concepts/rbac-foundry.md).

### Control access with Conditional Access policies

Tenant admins can use Conditional Access policies to grant or block access to Foundry MCP Server for selected users or workload identities.

1. Materialize the service principal for the Foundry MCP Server application ID by running the following command:

    ```azurecli
    az ad sp create --id fcdfa2de-b65b-4b54-9a1c-81c8a18282d9
    ```

    The application ID in this command represents Foundry MCP Server. You can verify this application ID by searching for "Foundry MCP Server" in the Entra ID enterprise applications list.

1. Find the enterprise application for Foundry MCP Server using the application ID. Open the [Azure portal Entra ID page](https://portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/Overview) and search for the application ID `fcdfa2de-b65b-4b54-9a1c-81c8a18282d9`.

    :::image type="content" source="../media/mcp/foundry-find-mcp-app.png" alt-text="Screenshot of MCP app in Entra ID.":::

1. Select **Conditional Access** under **Security** on the left pane of the selected app, then select **New Policy** to configure access control.

    1. Under **Users**, select **Specific users included** and add the users or groups you want to restrict.
    1. Under **Target resources**, confirm the Foundry MCP Server application is selected.

    :::image type="content" source="../media/mcp/foundry-conditional-access.png" alt-text="Screenshot of conditional access options for the app configuration.":::

    :::image type="content" source="../media/mcp/foundry-new-access-policy.png" alt-text="Screenshot of creating a new conditional access policy for the app.":::

1. Select **Grant**, then choose **Block access**.

    :::image type="content" source="../media/mcp/foundry-block-access.png" alt-text="A screenshot showing how to block app access.":::

After the policy is in place, designated users and groups can't obtain the Entra token needed to connect.

### Network isolation

Foundry MCP Server currently doesn't support network isolation. It exposes the public endpoint `https://mcp.ai.azure.com` that any MCP client can use. It connects to your Foundry resource through its public endpoint. If your Foundry resources use Azure Private Links, the server can't reach them and operations fail with a connectivity error.

> [!NOTE]
> This limitation applies to the hosted Foundry MCP Server (`mcp.ai.azure.com`). If you build your own MCP server and connect it to Foundry Agent Service, Agent Service supports [private MCP server endpoints](../agents/how-to/tools/model-context-protocol.md#public-and-private-mcp-server-endpoints) through Standard Agent Setup with private networking.

### Data residency

Foundry MCP Server uses a global stateless proxy architecture. Data created by backend services that interact with MCP Server stays encrypted at rest in the region you select. MCP Server itself doesn't store data. For performance and availability, requests and responses can be processed in data centers in the European Union (EU) or the United States (US), with all data encrypted in transit.  

> [!IMPORTANT]
> By using this preview feature, you acknowledge and consent to any cross-region processing that might occur. For example, an EU resource accessed by a US user could be routed through US infrastructure. If your organization requires strict in-region processing, don't use Foundry MCP Server or restrict its use to scenarios that remain within your selected region.

## Troubleshooting

Use this section to quickly diagnose common MCP Server issues.

### Authentication failures

If you receive a `401 Unauthorized` error or the sign-in prompt doesn't appear:

1. Sign out of your Azure account in Visual Studio Code, or the tool that you're using.
1. Sign back in with a Microsoft account that has access to your Azure subscription.
1. Verify your access token is valid by running `az account get-access-token --resource https://mcp.ai.azure.com` in the terminal.

If the token request fails, confirm your account has the required Entra ID permissions. For more information, see [Manage users and authentication in Entra ID](/entra/fundamentals/how-to-manage-user-profile-info).

### Permission errors

If you see `403 Forbidden` or "Access denied" errors when running MCP tools:

1. Open the Azure portal and navigate to your Foundry project.
1. Select **Access control (IAM)** and verify your account has Contributor or higher role.
1. If you recently received a role assignment, wait a few minutes for propagation and try again.

For more information, see [Role-based access control for Microsoft Foundry](../concepts/rbac-foundry.md).

### Server connectivity issues

If the MCP server fails to start or times out:

1. Verify your network allows outbound HTTPS connections to `https://mcp.ai.azure.com`.
1. Check for proxy or firewall rules that might block the endpoint.
1. Try opening `https://mcp.ai.azure.com` in a browser to confirm reachability.

If your Foundry resources use Azure Private Links, the hosted Foundry MCP Server can't reach them through the public endpoint. Disable Private Link, use SDKs/REST APIs, or use a [custom MCP server with private networking](../agents/how-to/tools/model-context-protocol.md#public-and-private-mcp-server-endpoints) through Foundry Agent Service.

### Tool discovery problems

If Foundry tools don't appear in the agent mode tools list:

1. Open the **Output** view in Visual Studio Code and select the MCP server log channel.
1. Verify the server shows a successful connection and tool registration.
1. Restart Visual Studio Code or reload your workspace.
1. If tools still don't appear, remove and re-add the server configuration.

## Related content

- Review [available tools and example prompts](available-tools.md) for Foundry MCP Server
- Get started with [Foundry MCP Server](get-started.md)
- Learn how to [build your own MCP server](build-your-own-mcp-server.md) 
