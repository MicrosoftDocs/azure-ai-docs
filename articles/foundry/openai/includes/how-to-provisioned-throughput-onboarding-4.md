---
title: Include file
description: Include file
author: msakande
ms.reviewer: seramasu
ms.author: mopeakande
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Azure Reservations for Foundry Provisioned Throughput

Discounts on top of the hourly usage price can be obtained by purchasing an Azure Reservation for Foundry Regional Provisioned, Data Zone Provisioned, and Global Provisioned. An Azure Reservation is a term-discounting mechanism shared by many Azure products. For example, Compute and Cosmos DB. For Foundry Regional Provisioned, Data Zone Provisioned, and Global Provisioned, the reservation provides a discount in exchange for committing to payment for fixed number of PTUs for a one-month or one-year period.  

* Azure Reservations are purchased via the [Reservations page in the Azure portal](https://portal.azure.com/#view/Microsoft_Azure_Reservations/ReservationsBrowseBlade/productType/Reservations).

* Reservations are purchased regionally and can be flexibly scoped to cover usage from a group of deployments. Reservation scopes include: 

  * Individual resource groups or subscriptions 

  * A group of subscriptions in a Management Group 

  * All subscriptions in a billing account 

* Discount applies when Deployment type (Regional/Data Zone/Global), Region, and Reservation scope (subscription or resource group) match the running deployment. Matching is not by model or deployment ID. Multiple deployments within scope can consume the same reservation up to its PTU quantity.

* New reservations can be purchased to cover the same scope as existing reservations, to allow for discounting of new provisioned deployments. The scope of existing reservations can also be updated at any time without penalty, for example to cover a new subscription. 

* Reservations for Global, Data Zone, and Regional deployments aren't interchangeable. You need to purchase a separate reservation for each deployment type. 

* Reservations can be canceled after purchase, but credits are limited.  

* If the size of provisioned deployments within the scope of a reservation exceeds the amount of the reservation, the excess is charged at the hourly rate. For example, if deployments amounting to 250 PTUs exist within the scope of a 200 PTU reservation, 50 PTUs will be charged on an hourly basis until the deployment sizes are reduced to 200 PTUs, or a new reservation is created to cover the remaining 50. 

* Reservations guarantee a discounted price for the selected term.  They don't reserve capacity on the service or guarantee that it will be available when a deployment is created. It's highly recommended that customers create deployments prior to purchasing a reservation to protect against over-purchasing a reservation. 

> [!IMPORTANT] 
> * Capacity availability for model deployments is dynamic and changes frequently across regions and models. To protect against purchasing a reservation for more PTUs than you can use, create deployments first, and then purchase the Azure Reservation to cover the PTUs you have deployed. This best practice will ensure that you can take full advantage of the reservation discount, and protects you from committing to a reservation that you cannot use. 
>
> * The Azure role and tenant policy requirements to purchase a reservation are different than those required to create a deployment or Foundry resource. Verify authorization to purchase reservations in advance of needing to do so. See [Foundry Provisioned Throughput Reservation](https://aka.ms/oai/docs/ptum-reservations) for more details.
