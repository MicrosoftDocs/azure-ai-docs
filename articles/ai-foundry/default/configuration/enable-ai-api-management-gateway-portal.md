---
title: Configure AI Gateway in your Foundry resources
titleSuffix: Microsoft Foundry
description: Enable AI Gateway with Azure API Management to apply tokens-per-minute limits and token quotas to model deployments in Microsoft Foundry.
#customer intent: As an IT admin, I want to enforce token limits on AI model deployments so that I can prevent excessive usage and align with organizational policies.
author: jonburchel
ms.author: jburchel
ms.reviewer: ankamene
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 02/19/2026
ms.custom: dev-focus
ai-usage: ai-assisted
---

# Configure AI Gateway in your Foundry resources

This article shows you how to enable AI Gateway for a Microsoft Foundry resource using the Foundry portal. AI Gateway uses Azure API Management behind the scenes to provide token limits, quotas, and governance for model deployments.

## Prerequisites

- Azure subscription ([create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)).

- Permissions to create or reuse an Azure API Management (APIM) instance:
  - To create an APIM instance: **Contributor** or **Owner** on the target resource group (or subscription).
  - To manage an existing APIM instance: **API Management Service Contributor** (or **Owner**) on the APIM instance. For more information, see [How to use role-based access control in Azure API Management](/azure/api-management/api-management-role-based-access-control).
- Access to the Foundry portal (**Admin console**) for the target Foundry resource.
  - For example: **Azure AI Account Owner** or **Azure AI Owner** on the Foundry resource. For more information, see [Role-based access control for Microsoft Foundry](../../concepts/rbac-foundry.md).
- Decision on whether to create a dedicated APIM instance or reuse an existing one.

## Requirements for using an existing API Management instance

When you select **Use existing APIM**, only API Management instances that meet all of the following requirements are listed:

- The API Management instance must be in the **same Microsoft Entra tenant** and the same **subscription** as the Foundry resource.
- You must have at least the **API Management Service Contributor** role (or Owner) on the API Management instance.
- The API Management instance must use a **supported service tier** for AI Gateway. Currently, instances in the [v2 tiers](/azure/api-management/v2-service-tiers-overview) are supported. 
- The API Management instance must not already be associated with another AI Gateway.

If none of your API Management instances appear in the list, verify that the instance meets the requirements above and that you have the required permissions.

## Create an AI Gateway

Follow these steps in the Foundry portal to enable AI Gateway for a resource.

1. [!INCLUDE [foundry-sign-in](../../default/includes/foundry-sign-in.md)]

1. Select **Operate** > **Admin console**.

1. Open the **AI Gateway** tab.

1. Select **Add AI Gateway**.

    :::image type="content" source="..\media\enable-ai-api-management-gateway-portal\foundry-add-ai-gateway.png" alt-text="A screenshot showing how to add an AI Gateway to a given Foundry resource." lightbox="..\media\enable-ai-api-management-gateway-portal\foundry-add-ai-gateway.png":::

1. Select the Foundry resource you want to connect with the gateway.

1. Select **Create new** or **Use existing** APIM.

    - **Create new**: Creates a Basic v2 SKU instance. Basic v2 is designed for development and testing with SLA support.
    - **Use existing**: Select an instance that meets your organization's governance and networking requirements.

    > [!TIP]
    > AI Gateway in Azure API Management service is free for the first 100,000 API requests. For more information about costs and pricing, see [API Management Pricing](https://azure.microsoft.com/pricing/details/api-management/).

    :::image type="content" source="..\media\enable-ai-api-management-gateway-portal\create-ai-gateway-portal.png" alt-text="Screenshot of AI Gateway tab in the Admin console showing options to create or select an API Management instance." lightbox="..\media\enable-ai-api-management-gateway-portal\create-ai-gateway-portal.png":::

1. Name the gateway, and select **Add** to create or associate the APIM instance.

1. Verify the AI Gateway appears in the list with a status of **Enabled**. If the status shows **Provisioning**, wait a few minutes and refresh the page.

1. New projects created in the Foundry resource have AI Gateway enabled by default. Existing projects must be enabled manually.

1. To enable an existing project, select the AI Gateway name to view associated projects.

1. In the project list, locate the project you want to enable. The **Gateway status** column shows current status.

1. Select **Add project to gateway**. The **Gateway status** column updates to **Enabled**.

    :::image type="content" source="..\control-plane\media\register-custom-agent\verify-ai-gateway-project.png" alt-text="A screenshot showing how to enable a given project by adding it to the gateway." lightbox="..\control-plane\media\register-custom-agent\verify-ai-gateway-project.png":::

## Verify the gateway is working

Confirm that traffic routes through AI Gateway:

1. In the Azure portal, open the API Management instance connected to your Foundry resource.
1. Select **Metrics** or **Logs** to confirm requests appear when you call a model deployment.
1. If you configured token limits, verify they apply by testing a request that exceeds the limit.

## Understand AI Gateway architecture

AI Gateway sits between clients and Foundry building blocks, including models and tools. All requests flow through the APIM instance once associated. Limits apply at the project level, so each project can have its own TPM and quota settings.

:::image type="content" source="..\media\enable-ai-api-management-gateway-portal\gateway-architecture-diagram.png" alt-text="Logical flow showing client requests passing through AI Gateway (APIM) before reaching model deployments within a project.":::

AI Gateway enables:

- Multi-team token containment (prevent one project from monopolizing capacity).
- Cost control by capping aggregate usage.
- Compliance boundaries for regulated workloads (enforce predictable usage ceilings).
- Registration of [custom agents for governance](../control-plane/register-custom-agent.md).

## Governance scenarios

Once you configured AI Gateway for your resource and project, you can:

* [Configure token limits for models](../control-plane/how-to-enforce-limits-models.md).
* [Add custom agents to Control Plane](../control-plane/register-custom-agent.md).
* Govern MCP and A2A agent tools.

## Troubleshooting

| Issue | Cause | Resolution |
| ----- | ----- | ---------- |
| AI Gateway doesn't appear after creation. | Provisioning is still in progress. | Wait a few minutes and refresh the page. Basic v2 instances typically provision within 5-10 minutes. |
| Project shows **Gateway status** as **Disabled**. | Existing projects aren't automatically enabled for AI Gateway. | Select the AI Gateway, locate the project, and select **Add project to gateway**. |
| Requests bypass the gateway. | The project wasn't enabled before requests were made, or the gateway isn't fully provisioned. | Verify the gateway status shows **Enabled** for both the resource and project. |
| Permission error when creating gateway. | Missing required RBAC role. | Verify you have **Contributor** or **Owner** on the resource group (to create) or **API Management Service Contributor** on an existing instance. |
| Existing API Management instance does not appear in the list when selecting **Use existing APIM** | The API Management instance does not meet the eligibility requirements or the user does not have sufficient permissions. | Verify that the API Management instance is in the same tenant, uses a supported SKU, is not already associated with another AI Gateway, and that you have the API Management Service Contributor role (or Owner) on the instance. |
| Token limits don't apply to requests. | Limits aren't configured, or the project isn't using the gateway. | Verify the project is enabled for AI Gateway, then configure token limits in the Admin console. |

For tools-specific troubleshooting, see [Tools governance with AI Gateway](/azure/ai-foundry/agents/how-to/tools/governance#troubleshooting).

## Clean up resources

If you created a dedicated APIM instance for this purpose:

1. Confirm that no other workloads depend on it.
1. Disable the AI Gateway for all projects in the Foundry resource it's associated with.
1. Remove linked resources in Azure portal.
1. Delete the APIM instance with the same name as the AI gateway in Azure portal (if it isn't used for any other purpose).

## Related content

- [AI Gateway capabilities in Azure API Management](/azure/api-management/genai-gateway-capabilities)
- [Azure API Management overview](/azure/api-management/api-management-key-concepts)
- [Limit large language model API token usage](/azure/api-management/llm-token-limit-policy)
- [How to use role-based access control in Azure API Management](/azure/api-management/api-management-role-based-access-control)
- [Role-based access control for Microsoft Foundry](../../concepts/rbac-foundry.md)
