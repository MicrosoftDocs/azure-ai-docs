---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-model-inference
ms.date: 5/11/2025
ms.topic: include
---

## Permissions required to subscribe to Azure Ecosystem Models

Azure Ecosystem Models available for deployment (for example, Cohere models) require Azure Marketplace. Model providers define the license terms and set the price for use of their models using Azure Marketplace.

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