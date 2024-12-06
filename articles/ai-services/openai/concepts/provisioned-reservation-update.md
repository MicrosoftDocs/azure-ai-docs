---
title: 'Azure OpenAI Provisioned December 2024 Update'
titleSuffix: Azure OpenAI
description: Learn about new Provisioned skus and commercial changes for Provisioned offers
manager: chrhoder
ms.service: azure-ai-openai
ms.custom:
ms.topic: how-to
ms.date: 11/25/2024
author: sydneemayers
ms.author: sydneemayers
recommendations: false
---
# Azure OpenAI provisioned December 2024 update 

In early December, 2024, Microsoft launched several changes to the provisioned offering. These changes include:
- A new deployment type, **data zone provisioned**.
- Updated hourly pricing for global and data zone provisioned deployment types
- New Azure Reservations for global and data zone provisioned deployment types

This article is intended for existing users of the provisioned throughput offering. New customers should refer to the [Azure OpenAI provisioned onboarding guide](../how-to/provisioned-throughput-onboarding.md).

## What's changing?

The changes below apply to the global provisioned, data zone provisioned, and provisioned deployment types.

> [!IMPORTANT]
> The changes in this article do not apply to the older *"Provisioned Classic (PTU-C)"* offering. They only affect the Provisioned (also known as the Provisioned Managed) offering.

### Data zone provisioned
Data zone provisioned deployments are available in the same Azure OpenAI resource as all other Azure OpenAI deployment types but allow you to leverage Azure's global infrastructure to dynamically route traffic to the data center within the Microsoft defined data zone with the best availability for each request. Data zone provisioned deployments provide reserved model processing capacity for high and predictable throughput using Azure global infrastructure within the Microsoft defined data zone. Data zone deployments are supported for gpt-4o and gpt-4o-mini model families. 

For more information, see the [deployment types guide](https://aka.ms/aoai/docs/deployment-types).

### New hourly pricing for global and data zone provisioned deployments
In August 2024, Microsoft announced that Provisioned deployments would move to a new [hourly payment model](./provisioned-migration.md) with the option to purchase Azure Reservations to support additional discounts. In December's provisioned update, we will be introducing differentiated hourly pricing across global provisioned, data zone provisioned, and provisioned deployment types. For more information on the hourly price for each provisioned deployment type, see the [Pricing details page](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/). 

### New Azure Reservations for global and data zone provisioned deployments
In addition to the updates for the hourly payment model, new Azure Reservations will be introduced specifically for global and data zone provisioned deployment types. With these new Azure Reservations, every provisioned deployment type will have a separate Azure Reservation that can be purchased to support additional discounts. The mapping between each provisioned deployment type and the associated Azure Reservation are as follows:

| Provisioned deployment type | Sku name in code  | Azure Reservation product name |
|---|---|---|
| Global provisioned | `GlobalProvisionedManaged`  | Provisioned Managed Global  |
| Data zone provisioned | `DataZoneProvisionedManaged`  | Provisioned Managed Data Zone  |
| Provisioned | `ProvisionedManaged`  | Provisioned Managed Regional |

> [!IMPORTANT]
> Azure Reservations for Azure OpenAI provisioned offers are not interchangeable across deployment types. The Azure Reservation purchased must match the provisioned deployment type. If the Azure Reservation purchased does not match the provisioned deployment type, the provisioned deployment will default to the hourly payment model until a matching Azure Reservation product is purchased. For more information, see the [Azure Reservations for Azure OpenAI Service provisioned guidance](https://aka.ms/oai/docs/ptum-reservations).

## Migrating existing deployments to global or data zone provisioned
Existing customers of provisioned deployments can choose to migrate to global or data zone provisioned deployments to benefit from the lower deployment minimums, granular scale increments, or differentiated pricing available for these deployment types. To learn more about how global and data zone provisioned deployments handle data processing across Azure geographies, see the Azure OpenAI deployment [data processing documentation](https://aka.ms/aoai/docs/data-processing-locations).

Two approaches are available for customers to migrate from provisioned deployments to global or data zone provisioned deployments. 

### Zero downtime migration 
The zero downtime migration approach allows customers to migrate their existing provisioned deployments to global or data zone provisioned deployments without interrupting the existing inference traffic on their deployment. This migration approach minimizes workload interruptions, but does require a customer to have multiple coexisting deployments while shifting traffic over. The process to migrate a provisioned deployment using the zero downtime migration approach is as follows:
- Create a new deployment using the global or data zone provisioned deployment types in the target Azure OpenAI resource.
- Transition traffic from the existing regional provisioned deployment type to the newly created global or data zone provisioned deployment until all traffic is offloaded from the existing regional provisioned deployment.
- Once traffic is migrated over to the new deployment, validate that there are no inference requests being processed on the previous provisioned deployment by ensuring the Azure OpenAI Requests metric does not show any API calls made within 5-10 minutes of the inference traffic being migrated over to the new deployment. For more information on this metric, [see the Monitor Azure OpenAI documentation](https://aka.ms/aoai/docs/monitor-azure-openai).
- Once you confirm that no inference calls have been made, delete the regional provisioned deployment.

### Migration with downtime 
The migration with downtime approach involves migrating existing provisioned deployments to global or data zone provisioned deployments while stopping any existing inference traffic on the original provisioned deployment. This migration approach does not require coexistence of multiple deployments to support but does require workload interruption to complete. The process to migrate a provisioned deployment using the migration with downtime approach is as follows:
- Validate that there are no inference requests being processed on the previous provisioned deployment by ensuring the Azure OpenAI Requests metric does not show any API calls made within the last 5-10 minutes. For more information on this metric, [see the Monitor Azure OpenAI documentation](https://aka.ms/aoai/docs/monitor-azure-openai).
- Once you confirm that no inference calls have been made, delete the regional provisioned deployment.
- Create a new deployment using the global or data zone deployment types in the target Azure OpenAI resource.
- Once your new deployment has succeeded, you may resume inference traffic on the new global or data zone deployment.

## How do I migrate my existing Azure Reservation to the new Azure Reservation products?
Azure Reservations for Azure OpenAI Service provisioned offers are specific to the provisioned deployment type. If the Azure Reservation purchased does not match the provisioned deployment type, the deployment will default to the hourly payment model. If you choose to migrate to global or data zone provisioned deployments, you may need to purchase a new Azure Reservation for these deployments to support additional discounts. For more information on how to purchase a new Azure Reservation or make changes to an existing Azure Reservation, see the [Azure Reservations for Azure OpenAI Service Provisioned guidance](https://aka.ms/aoai/reservation-transition).

