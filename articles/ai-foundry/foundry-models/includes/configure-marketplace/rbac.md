---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.date: 09/29/2025
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