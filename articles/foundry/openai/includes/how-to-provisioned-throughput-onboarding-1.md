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

Use this article to learn about costs associated with provisioned throughput units (PTUs). For an overview of the provisioned throughput offering, see [What is provisioned throughput?](../concepts/provisioned-throughput.md). When you're ready to sign up for the provisioned throughput offering, see the [getting started guide](../how-to/provisioned-get-started.md).

> [!NOTE]
> In function calling and agent use cases, token usage can be variable. You should understand your expected Tokens Per Minute (TPM) usage in detail before migrating workloads to PTU.

## Provisioned throughput units

Provisioned throughput units (PTUs) are generic units of model processing capacity that you can use to size provisioned deployments to achieve the required throughput for processing prompts and generating completions.  Provisioned throughput units are granted to a subscription as quota. Each quota is specific to a region and defines  the maximum number of PTUs that can be assigned to deployments in that subscription and region.

## Provisioned throughput billing

Microsoft Foundry [Regional Provisioned Throughput](../../foundry-models/concepts/deployment-types.md#regional-provisioned), [Data Zone Provisioned Throughput](../../foundry-models/concepts/deployment-types.md#data-zone-provisioned), and [Global Provisioned Throughput](../../foundry-models/concepts/deployment-types.md#global-provisioned) are billed hourly based on the number of deployed PTUs, with substantial term discount available via the purchase of Azure reservations.  

The hourly billing model is useful for short-term deployment needs, such as validating new models or acquiring capacity for a hackathon.  However, the discounts provided by the Azure reservation for Foundry Regional Provisioned, Data Zone Provisioned, and Global Provisioned are considerable and most customers with consistent long-term usage will find a reserved model to be a better value proposition. 

[Azure reservations](#azure-reservations-for-foundry-provisioned-throughput) are a financial discount construct applied to billing meters, not to service interactions (like deployment). Reservations and deployments are loosely coupled to provide flexibility. You create or delete deployments and reservations independently. This approach lets you change resources, subscriptions, or deployments without changing the billing construct.

Recommended order of operations to avoid unwanted charges:
1. Use Foundry to deploy your model in a region with available quota. This step confirms capacity exists, since quota does not equal capacity.
1. After deployment, share deployment details, including deployment type (Global Provisioned, Data Zone Provisioned, or Regional Provisioned), region, and subscription, with your admin.
1. The admin uses these details to either purchase a new reservation matching the deployment details, or verify that an existing reservation matches, to receive the discounted rate.

> [!NOTE]
> Foundry provisioned customers onboarded prior to the August self-service update use a purchase model called the Commitment model. These customers can continue to use this older purchase model alongside the Hourly/reservation purchase model. The Commitment model is not available for new customers or [certain new models](../../../foundry-classic/openai/concepts/provisioned-migration.md#supported-models-on-commitment-payment-model) introduced after August 2024. For details on the Commitment purchase model and options for coexistence and migration, see the [Foundry Provisioned August Update](../../../foundry-classic/openai/concepts/provisioned-migration.md).
