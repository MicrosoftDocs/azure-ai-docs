---
title: Explore Foundry MCP Server best practices and security guidance
description: Learn about Foundry MCP Server best practices and security guidance
keywords: azure developer cli, azd
author: sdgilley
ms.author: sgilley
ms.reviewer: sehan
ms.date: 11/04/2025
ms.topic: get-started
ms.service: azure-ai-foundry
ai-usage: ai-assisted
---

# Foundry MCP Server best practices and security guidance

Use Foundry MCP Server (preview) tools to automate read and write operations across Foundry resources (deployments, datasets, evaluations, monitoring, analytics). This guidance helps you verify intent, reduce risk, and apply security and governance practices before you run MCP tools.

[!INCLUDE [preview-feature](../../openai/includes/preview-feature.md)]

## Interpreting the response

MCP Server provides output that is passed to the language model selected for your agent (for example, Visual Studio Code with GitHub Copilot). The language model combines this output with the conversation context to generate a final response based on its capabilities. Always verify the accuracy of the language model’s response. It may include details that are inferred or generated beyond the MCP Server’s original output.

## Impact of write operations

Write operations have a critical impact on Foundry resources. Proceed with caution and proper planning when you interact with Foundry MCP Server (preview), just as you would when using the portal, SDKs, or REST APIs. For example:

- Deployments: Immediately affect live apps and billing.
- Deletions: Permanently remove resources and can break dependent services.
- Evaluations: Consume compute quota and incur costs.
- Datasets: Can overwrite existing versions.

Examples of resource impact:

- Deleting a deployment breaks all applications using that endpoint.
- Large evaluations can consume significant quota allocation.
- New deployments start billing immediately.
- Overwriting a dataset affects evaluation reproducibility.

## Best practices for safe executions 

Follow these practices to make sure write operations run as you intend:

### Tool execution verification

- **Verify tool selection**: Confirm the correct MCP tool and parameters match your intention before execution.
- **Check parameters**: Review all tool parameters (resource IDs, deployment names, dataset paths) for accuracy.
  - For example, many model and deployment related tools would take Foundry resource ID in the format of `/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.CognitiveServices/accounts/{account_name}` - this Foundry resource ID has the information about the subscription, resource group name, and the Foundry account name.
  - Similarly, many agent and evaluation related tools would take Foundry project endpoint in the format of `https://{account_name}.services.ai.azure.com/api/projects/{project_name}`, which has the information about the Foundry account name and the project name.
  - If you provide project resource ID in the format of `/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.CognitiveServices/accounts/{account_name}/projects/{project_name}` that you can find from either Properties page of the account on Azure portal or Microsoft Foundry project details page, the language model used in your MCP Host will extract needed info and formulate the parameters to pass to the MCP tools. Confirm before approval that intended parameter values are passed to the MCP tools.
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

Authenticate to Foundry MCP Server (preview) using a Microsoft Entra token scoped to `https://mcp.ai.azure.com`.

Azure role-based access control (RBAC) applies to all operations on Foundry resources supported by Foundry MCP Server (preview). Operations run according to the authenticated user's permissions.

### Allow tenant admin control via Azure Policy

Tenant admins can use Azure Policy to grant or block access to Foundry MCP Server (preview) for selected users or workload identities.

1. Materialize the service principal for Foundry MCP Server (preview) application ID by running `az ad sp create --id fcdfa2de-b65b-4b54-9a1c-81c8a18282d9`. The application ID used in this command represents Foundry MCP Server (preview).

1. Find the enterprise application for Foundry MCP Server (preview) using the application ID. Open the [Azure portal Entra ID page](https://portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/Overview) and search for the application ID `fcdfa2de-b65b-4b54-9a1c-81c8a18282d9`.

    :::image type="content" source="../media/mcp/foundry-find-mcp-app.png" alt-text="Screenshot of MCP app in Entra ID.":::

1. Click Conditional Access under Security on the left pane of the selected app for Foundry MCP Server (preview) and click New Policy to specify the users or workload identities.

    :::image type="content" source="../media/mcp/foundry-conditional-access.png" alt-text="Screenshot of conditional access options for the app configuration.":::

    :::image type="content" source="../media/mcp/foundry-new-access-policy.png" alt-text="Screenshot of creating a new conditional access policy for the app.":::

1. Select **Grant**, then choose **Block access**.

    :::image type="content" source="../media/mcp/foundry-block-access.png" alt-text="A screenshot showing how to block app access.":::

After the policy is in place, designated users and groups can't obtain the Entra token needed to connect.

### Network isolation

Foundry MCP Server (preview) currently doesn't support network isolation. It exposes the public endpoint `https://mcp.ai.azure.com` that any MCP client can use. It connects to your Foundry resource through its public endpoint. If your Foundry resources use Azure Private Links, the server can't reach them and operations fail.

### Data Residency

Foundry MCP Server (preview) ("MCP Server") uses a global stateless proxy architecture. Data created by backend services that interact with MCP Server stays encrypted at rest in the region you select. MCP Server itself doesn't store data. For performance and availability, requests and responses can be processed in data centers in the European Union (EU) or the United States (US), with all data encrypted in transit.  

> [!IMPORTANT]
> By using this preview feature, you are acknowledging and consenting to any cross-region processing that may occur. As an example, an EU resource accessed by a US user could be routed through US infrastructure. If your organization requires strict in-region processing, do not use the Foundry MCP Server (preview) or restrict its use to scenarios that remain within your selected region.

## Troubleshooting and FAQs

Use this section to quickly diagnose common MCP Server issues.

### Authentication failures

Check your permissions in Entra ID and confirm your access token is valid. Sign out, then sign back in to your Azure account in Visual Studio Code. For more information, see Manage users and authentication in Entra ID. 

### Permission errors

Check your resource role assignments in the Azure portal to make sure you have the permissions for the operations you need. For more information, see [Role-based access control for Microsoft Foundry](../../concepts/rbac-foundry.md).

### Server connectivity issues

Make sure your network allows outbound HTTPS connections to Azure services and no firewall rules block the MCP Server endpoint. See Azure connectivity troubleshooting for more help.

### Tool discovery problems

Make sure the MCP server is running and tools are loaded by checking the Output view in Visual Studio Code. Restart VS Code or reload your workspace to fix discovery issues.

## Related content

- Review [available tools and example prompts](available-tools.md) for Foundry MCP Server
- Get started with [Foundry MCP Server](get-started.md)
- Learn how to [build your own MCP server](build-your-own-mcp-server.md) 
