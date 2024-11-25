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

In early-December, 2024, Microsoft launched several changes to the Provisioned offering. These changes include:
    - A new deployment type, Data zone provisioned
    - Updated hourly pricing for Global and Data zone provisioned deployment types
    - New Azure Reservations for Global and Data zone provisioned deployment types

This article is intended for existing users of the provisioned throughput offering. New customers should refer to the [Azure OpenAI provisioned onboarding guide](../how-to/provisioned-throughput-onboarding.md).

## What's changing?

The changes below apply to the Global Provisioned, Data Zone Provisioned, and Provisioned deployment types.

> [!IMPORTANT]
> The changes in this article do not apply to the older *"Provisioned Classic (PTU-C)"* offering. They only affect the Provisioned (also known as the Provisioned Managed) offering.

### Data Zone provisioned
Data zone provisioned deployments are available in the same Azure OpenAI resource as all other Azure OpenAI deployment types but allow you to leverage Azure's global infrastructure to dynamically route traffic to the data center within the Microsoft defined data zone with the best availability for each request. Data zone provisioned deployments provide reserved model processing capacity for high and predictable throughput using Azure global infrastructure within the Microsoft defined data zone. Data zone deployments are supported for gpt-4o and gpt-4o-mini model families. 

For more information, see the [deployment types guide](https://aka.ms/aoai/docs/deployment-types).

### New hourly pricing for Global and Data Zone provisioned deployments
In August 2024, Microsoft announced that Provisioned deployments would move to a new [hourly payment model](./provisioned-migration.md) with the option to purchase Azure Reservations to support additional discounts. In December's provisioned update, we will be introducing differentiated hourly pricing across Global provisioned, Data zone provisioned, and provisioned deployment types. For more information on the hourly price for each Provisioned deployment type, see the [Pricing details page](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/). 

### New Azure Reservations for Globl and Data zone provisioned deployments
In addition to the updates for the hourly payment model, new Azure Reservations will be introduced specifically for 

## Migrating existing deployments to Global or Data zone provisioned


### Zero downtime migration 

> [!IMPORTANT]
> Both self-service approaches generate some additional charges as the payment mode is switched from Committed to Hourly/Reservation.  These are characteristics of the migration approaches and customers aren't credited for these charges.  Customers may choose to use the managed migration approach described below to avoid them.

### Migration with downtime 


