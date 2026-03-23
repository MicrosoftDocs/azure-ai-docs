---
title: Enable priority processing for Microsoft Foundry Models
description: "Learn how to enable priority processing for Microsoft Foundry models to achieve low latency and high availability for time-sensitive workloads."
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 03/23/2026
ms.author: mopeakande
author: msakande
ms.reviewer: seramasu
reviewer: rsethur
ai-usage: ai-assisted
ms.custom:
  - ignite-2025, pilot-ai-workflow-jan-2026
  - classic-and-new
  - doc-kit-assisted
#customerIntent: As a developer or data scientist working with latency-sensitive AI applications, I want to understand and implement priority processing for Microsoft Foundry models so that I can achieve predictable low latency and high availability for time-critical workloads without requiring long-term commitments or provisioned capacity.
---

# Enable priority processing for Microsoft Foundry models

[!INCLUDE [priority-processing 1](../includes/concepts-priority-processing-1.md)]

## Priority processing support

# [Global standard](#tab/global-standard)

### Global standard model availability

| **Region**             | **gpt-5.4, 2026-03-05** | **gpt-5.2, 2025-12-11** | **gpt-5.1, 2025-11-13** | **gpt-4.1, 2025-04-14** |
|:-----------------------|:-----------------------:|:-----------------------:|:-----------------------:|:-----------------------:|
| australiaeast          | -                       | ✅                      | ✅                      | ✅                      |
| brazilsouth            | -                       | ✅                      | ✅                      | ✅                      |
| canadacentral          | -                       | ✅                      | ✅                      | ✅                      |
| canadaeast             | -                       | ✅                      | ✅                      | ✅                      |
| centralus              | -                       | ✅                      | ✅                      | ✅                      |
| eastus                 | -                       | ✅                      | ✅                      | ✅                      |
| eastus2                | ✅                      | ✅                      | ✅                      | ✅                      |
| francecentral          | -                       | ✅                      | ✅                      | ✅                      |
| germanywestcentral     | -                       | ✅                      | ✅                      | ✅                      |
| italynorth             | -                       | ✅                      | ✅                      | ✅                      |
| japaneast              | -                       | ✅                      | ✅                      | ✅                      |
| koreacentral           | -                       | ✅                      | ✅                      | ✅                      |
| northcentralus         | -                       | ✅                      | ✅                      | ✅                      |
| norwayeast             | -                       | ✅                      | ✅                      | ✅                      |
| polandcentral          | ✅                      | ✅                      | ✅                      | ✅                      |
| southafricanorth       | -                       | ✅                      | ✅                      | ✅                      |
| southcentralus         | ✅                      | ✅                      | ✅                      | ✅                      |
| southeastasia          | -                       | ✅                      | ✅                      | ✅                      |
| southindia             | -                       | ✅                      | ✅                      | ✅                      |
| spaincentral           | -                       | ✅                      | ✅                      | ✅                      |
| swedencentral          | ✅                      | ✅                      | ✅                      | ✅                      |
| switzerlandnorth       | -                       | ✅                      | ✅                      | ✅                      |
| switzerlandwest        | -                       | ✅                      | ✅                      | ✅                      |
| uaenorth               | -                       | ✅                      | ✅                      | ✅                      |
| uksouth                | -                       | ✅                      | ✅                      | ✅                      |
| westeurope             | -                       | ✅                      | -                       | ✅                      |
| westus                 | -                       | ✅                      | ✅                      | ✅                      |
| westus3                | -                       | ✅                      | -                       | ✅                      |


# [Data Zone standard](#tab/datazone-standard)

### Data zone standard model availability

| **Region**             | **gpt-5.4, 2026-03-05** | **gpt-5.2, 2025-12-11** | **gpt-5.1, 2025-11-13** | **gpt-4.1, 2025-04-14** |
|:-----------------------|:-----------------------:|:-----------------------:|:-----------------------:|:-----------------------:|
| centralus              | ✅                      | ✅                      | ✅                      | ✅                      |
| eastus                 | ✅                      | ✅                      | ✅                      | ✅                      |
| eastus2                | ✅                      | ✅                      | ✅                      | ✅                      |
| francecentral          | -                       | -                       | ✅                      | ✅                      |
| germanywestcentral     | -                       | -                       | -                       | ✅                      |
| italynorth             | -                       | -                       | -                       | ✅                      |
| northcentralus         | ✅                      | ✅                      | ✅                      | ✅                      |
| polandcentral          | -                       | -                       | -                       | ✅                      |
| southcentralus         | ✅                      | ✅                      | ✅                      | ✅                      |
| spaincentral           | -                       | -                       | -                       | ✅                      |
| swedencentral          | -                       | -                       | ✅                      | ✅                      |
| westeurope             | -                       | -                       | -                       | ✅                      |
| westus                 | ✅                      | ✅                      | ✅                      | ✅                      |
| westus3                | ✅                      | ✅                      | ✅                      | ✅                      |


---

> [!NOTE]
> Model and region availability is expected to expand in the days ahead. Check this page for updates. For pricing information, see [this page](https://azure.microsoft.com/pricing/details/azure-openai/).

## Enable priority processing at the deployment level

You can enable priority processing at the deployment level and [(optionally) at the request level](#enable-priority-processing-at-the-request-level).

> [!NOTE]
> Priority processing can be enabled in Global standard or Data Zone standard (US) deployments. Priority processing uses the same quota as standard processing.

In the [!INCLUDE [foundry-link](../../includes/foundry-link.md)] portal, turn on the **Priority processing** toggle on the deployment details page when creating the deployment or update the setting of a deployed model by editing the deployment details.

:::image type="content" source="../media/priority-processing/enable-priority-processing-foundry.png" alt-text="Screenshot showing how to enable priority processing during model deployment in the Foundry portal." lightbox="../media/priority-processing/enable-priority-processing-foundry.png":::
> [!NOTE]
> If you prefer to use code to enable priority processing at the deployment level, you can do so via the REST API for deployment by setting the `service_tier` attribute as follows: `"properties" : {"service_tier" : "priority"}`. Allowed values for the `service_tier` attribute are `default` and `priority`. `default` implies standard processing, while `priority` enables priority processing.

Once a model deployment is configured to use priority processing, you can start sending requests to the model.

[!INCLUDE [priority-processing 2](../includes/concepts-priority-processing-2.md)]
