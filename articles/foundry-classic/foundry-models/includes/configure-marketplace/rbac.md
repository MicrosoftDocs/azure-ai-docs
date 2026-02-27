---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.date: 02/11/2026
ms.topic: include
---

## Permissions required to subscribe to Models from Partners and Community

[Foundry Models from partners and community](../../concepts/models-from-partners.md) available for deployment (for example, Cohere models) require Azure Marketplace. Model providers define the license terms and set the price for use of their models using Azure Marketplace.

When deploying third-party models, ensure you have the following permissions in your account:

> [!div class="checklist"]
> * On the Azure subscription:
>   * `Microsoft.MarketplaceOrdering/agreements/offers/plans/read`
>   * `Microsoft.MarketplaceOrdering/agreements/offers/plans/sign/action`
>   * `Microsoft.MarketplaceOrdering/offerTypes/publishers/offers/plans/agreements/read`
>   * `Microsoft.Marketplace/offerTypes/publishers/offers/plans/agreements/read`
>   * `Microsoft.SaaS/register/action`
> * On the resource group—to create and use the SaaS resource:
>   * `Microsoft.SaaS/resources/read`
>   * `Microsoft.SaaS/resources/write`

The **Owner** and **Contributor** built-in roles on the Azure subscription include these permissions. If you don't have the required permissions, ask your subscription administrator to assign you the **Contributor** role, or [create a custom role](/azure/role-based-access-control/custom-roles) that includes the listed actions.

To verify your permissions, go to the [Azure portal](https://portal.azure.com), open your subscription, select **Access control (IAM)** > **Check access**, and review your assigned roles.

> [!TIP]
> `Microsoft.SaaS/register/action` is a one-time registration of the SaaS resource provider on the subscription. After registration, it doesn't need to be repeated for each deployment.