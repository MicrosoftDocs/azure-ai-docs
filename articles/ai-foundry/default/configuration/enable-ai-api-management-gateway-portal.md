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
ms.date: 10/29/2025
ai-usage: ai-assisted
---

# Configure AI Gateway in your Foundry resources

Microsoft Foundry integrates with AI Gateway to enable advanced management and governance capabilities. This integration uses Azure API Management behind the scenes.

AI Gateway enables:

> [!div class="checklist"]
> * Multi-team token containment (prevent one project from monopolizing capacity).
> * Cost control by capping aggregate usage.
> * Compliance boundaries for regulated workloads (enforce predictable usage ceilings).
> * Registration of [custom agents for governance](../control-plane/register-custom-agent.md).

## Prerequisites

- Azure subscription ([create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)).

- Permissions to create or reuse an Azure API Management (APIM) instance:
  - To create an APIM instance: **Contributor** or **Owner** on the target resource group (or subscription).
  - To manage an existing APIM instance: **API Management Service Contributor** (or **Owner**) on the APIM instance. For more information, see [How to use role-based access control in Azure API Management](/azure/api-management/api-management-role-based-access-control).

- Access to the Foundry portal (**Admin console**) for the target Foundry resource.
  - For example: **Azure AI Account Owner** or **Azure AI Owner** on the Foundry resource. For more information, see [Role-based access control for Microsoft Foundry](../../concepts/rbac-foundry.md).

- Decision on whether to create a dedicated APIM instance or reuse an existing one.

## Understand AI Gateway scope

An AI Gateway sits between clients and Microsoft Foundry building blocks, including models or tools. All requests flow through the APIM instance once associated. Limits apply at the project level (each project can have its own TPM and quota settings).

:::image type="content" source="..\media\enable-ai-api-management-gateway-portal\gateway-architecture-diagram.png" alt-text="Logical flow showing client requests passing through AI Gateway (APIM) before reaching model deployments within a project.":::

## Choose API Management usage model

When you create a new AI Gateway, decide whether to:

- Create a new APIM instance.
- Use an existing APIM instance.

If you use an existing APIM instance, choose one that meets your organization's governance and networking requirements.

When you create a new instance from the Foundry portal flow, the SKU defaults to Basic v2. 

> [!TIP]
> AI Gateway in Azure API Management service is free for the first 100,000 API requests. For more information about costs and pricing for the API Management service, see [API Management Pricing](https://azure.microsoft.com/pricing/details/api-management/).

## Create an AI Gateway

Follow these steps in the Foundry portal to enable AI Gateway for a resource.

1. [!INCLUDE [foundry-sign-in](../../default/includes/foundry-sign-in.md)]

1. Select **Operate** > **Admin console**.

1. Open the **AI Gateway** tab.

1. Select **Add AI Gateway**.

    :::image type="content" source="..\media\enable-ai-api-management-gateway-portal\foundry-add-ai-gateway.png" alt-text="An screenshot showing how to add an AI Gateway to a given Foundry resource." lightbox="..\media\enable-ai-api-management-gateway-portal\foundry-add-ai-gateway.png":::

1. Select the Foundry resource you want to connect with the gateway.

1. Select **Create new** or **Use existing** APIM.

    :::image type="content" source="..\media\enable-ai-api-management-gateway-portal\create-ai-gateway-portal.png" alt-text="AI Gateway tab in the Admin console showing options to create or select an API Management instance." lightbox="..\media\enable-ai-api-management-gateway-portal\create-ai-gateway-portal.png":::

1. Name the gateway, and select **Add** to create or associate the APIM instance.

1. Validate that the AI Gateway is listed now.

1. Once AI Gateway is configured for the Foundry resource, each project have its own configuration, including if they want to use AI Gateway or not. New projects created in the Foundry resource have AI Gateway enabled by default. However, existing projects must be enabled for AI Gateway. 

1. To add existing projects to the AI Gateway, select the name of the AI Gateway you just created. You see a list of all the projects in the Foundry resource with a column **Gateway status** showing if the project has AI Gateway enabled or not. Locate your project and then select **Add project to gateway**. The column **Gateway status** shows **Enabled**.

    :::image type="content" source="..\control-plane\media\register-custom-agent\verify-ai-gateway-project.png" alt-text="An screenshot showing how to enable a given project by adding it to the gateway." lightbox="..\control-plane\media\register-custom-agent\verify-ai-gateway-project.png":::

## Governance scenarios

Once you configured AI Gateway for your resource and project, you can:

* [Configure token limits for models](../control-plane/how-to-enforce-limits-models.md).
* [Add custom agents to Control Plane](../control-plane/register-custom-agent.md).
* Govern MCP and A2A agent tools.

## Clean up resources

If you created a dedicated APIM instance for this purpose:

1. Confirm that no other workloads depend on it.
1. Disable the AI Gateway for all projects in the Foundry resource it's associated with.
1. Remove linked resources in Azure portal.
1. Delete the APIM instance with the same name as the AI gateway in Azure portal (if it's not used for any other purpose).

## Related content

- [AI Gateway capabilities in Azure API Management](/azure/api-management/genai-gateway-capabilities)
- [Azure API Management overview](/azure/api-management/api-management-key-concepts)
- [Limit large language model API token usage](/azure/api-management/llm-token-limit-policy)
- [How to use role-based access control in Azure API Management](/azure/api-management/api-management-role-based-access-control)
- [Role-based access control for Microsoft Foundry](../../concepts/rbac-foundry.md)
