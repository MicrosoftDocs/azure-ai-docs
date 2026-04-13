---
title: "What Is Provisioned Throughput for Foundry Models? (classic)"
description: "Learn how provisioned throughput enables efficient deployment of Azure OpenAI and Foundry Models with stable latency and allocated capacity. Get started today. (classic)"
#customer intent: As a developer, I want to understand provisioned throughput so I can deploy and manage AI models efficiently.
ai-usage: ai-assisted
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: concept-article
ms.date: 02/10/2026
ms.custom:
  - dev-focus, pilot-ai-workflow-jan-2026
  - classic-and-new
manager: nitinme
author: msakande 
ms.author: mopeakande
ms.reviewer: seramasu
reviewer: rsethur
recommendations: false
#CustomerIntent As a developer, I want to understand provisioned throughput so I can deploy and manage AI models efficiently.
ROBOTS: NOINDEX, NOFOLLOW
---

# What is provisioned throughput for Foundry Models? (classic)

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../../foundry/openai/concepts/provisioned-throughput.md)

> [!TIP]
> For more information on recent changes to the provisioned throughput offering, see the [update article](./provisioned-migration.md).

The Microsoft Foundry provisioned throughput offering is a model deployment type that allows you to specify the amount of throughput you require in a model deployment. Foundry then allocates the necessary model processing capacity and ensures it's ready for you. Use the provisioned throughput you requested across a diverse portfolio of [models that are sold directly by Azure](../../../ai-foundry/concepts/foundry-models-overview.md#models-sold-directly-by-azure). These models include Azure OpenAI models and newly introduced flagship model families like Azure DeepSeek within Foundry Models, with more model families onboarding over time.

Provisioned throughput provides:

| Benefit                          | Description                                                                   |
| -------------------------------- | ----------------------------------------------------------------------------- |
| **Broader model choice**         | Access to the latest flagship models                                          |
| **Flexibility**                  | Switch models and deployments with given provisioned throughput quota         |
| **Significant discounts**        | Boost your reservation utilization with a more flexible reservation choice    |
| **Predictable performance**      | Stable max latency and throughput for uniform workloads                       |
| **Allocated processing capacity**| Throughput is available whether used or not once deployed                     |
| **Cost savings**                 | High throughput workloads might provide cost savings versus token-based consumption |

> [!TIP]
> * Take advantage of more cost savings when you buy [Microsoft Foundry Provisioned Throughput reservations](/azure/cost-management-billing/reservations/azure-openai#buy-a-microsoft-azure-openai-service-reservation).
> * Provisioned throughput is available as the following deployment types: [global provisioned](../../foundry-models/concepts/deployment-types.md#global-provisioned), [data zone provisioned](../../foundry-models/concepts/deployment-types.md#data-zone-provisioned) and [regional provisioned](../../foundry-models/concepts/deployment-types.md#regional-provisioned).

[!INCLUDE [provisioned-throughput 1](../../../foundry/openai/includes/concepts-provisioned-throughput-1.md)]
