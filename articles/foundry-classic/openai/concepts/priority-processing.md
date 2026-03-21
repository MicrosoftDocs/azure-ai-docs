---
title: "Enable priority processing for Microsoft Foundry Models (classic)"
description: "Learn how to enable priority processing for Microsoft Foundry models to achieve low latency and high availability for time-sensitive workloads. (classic)"
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 03/20/2026
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
ROBOTS: NOINDEX, NOFOLLOW
---

# Enable priority processing for Microsoft Foundry models (classic)

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../../foundry/openai/concepts/priority-processing.md)

[!INCLUDE [priority-processing 1](../../../foundry/openai/includes/concepts-priority-processing-1.md)]

## Priority processing support

# [Global standard](#tab/global-standard)

### Global standard model availability

| **Region**     | **gpt-5.4, 2026-03-05** | **gpt-5.2, 2025-12-11** | **gpt-5.1, 2025-11-13** | **gpt-4.1, 2025-04-14** |
|:---------------|:-----------------------:|:-----------------------:|:-----------------------:|:-----------------------:|
| canadaeast     | ❌                      | ✅                      | ✅                      | ✅                      |
| centralus      | ❌                      | ✅                      | ✅                      | ✅                      |
| eastus         | ❌                      | ✅                      | ✅                      | ✅                      |
| francecentral  | ❌                      | ✅                      | ✅                      | ✅                      |
| koreacentral   | ❌                      | ✅                      | ✅                      | ✅                      |
| polandcentral  | ✅                      | ✅                      | ✅                      | ✅                      |
| southcentralus | ✅                      | ✅                      | ✅                      | ✅                      |
| southindia     | ❌                      | ✅                      | ✅                      | ✅                      |
| swedencentral  | ✅                      | ✅                      | ✅                      | ✅                      |
| uksouth        | ❌                      | ✅                      | ✅                      | ✅                      |
| westeurope     | ❌                      | ✅                      | ❌                      | ✅                      |
| westus3        | ❌                      | ✅                      | ❌                      | ✅                      |


# [Data Zone standard](#tab/datazone-standard)

### Data zone standard model availability

| **Region**     | **gpt-5.4, 2026-03-05** | **gpt-5.2, 2025-12-11** | **gpt-5.1, 2025-11-13** | **gpt-4.1, 2025-04-14** |
|:---------------|:-----------------------:|:-----------------------:|:-----------------------:|:-----------------------:|
| canadaeast     | ❌                      | ❌                      | ❌                      | ❌                      |
| centralus      | ✅                      | ✅                      | ✅                      | ✅                      |
| eastus         | ✅                      | ✅                      | ✅                      | ✅                      |
| francecentral  | ❌                      | ❌                      | ✅                      | ✅                      |
| koreacentral   | ❌                      | ❌                      | ❌                      | ❌                      |
| polandcentral  | ❌                      | ❌                      | ❌                      | ✅                      |
| southcentralus | ✅                      | ✅                      | ✅                      | ✅                      |
| southindia     | ❌                      | ❌                      | ❌                      | ❌                      |
| swedencentral  | ❌                      | ❌                      | ✅                      | ✅                      |
| uksouth        | ❌                      | ❌                      | ❌                      | ❌                      |
| westeurope     | ❌                      | ❌                      | ❌                      | ✅                      |
| westus3        | ✅                      | ✅                      | ✅                      | ✅                      |

---

> [!NOTE]
> Model and region availability is expected to expand in the days ahead. Check this page for updates. For pricing information, see [this page](https://azure.microsoft.com/pricing/details/azure-openai/).

## Enable priority processing at the deployment level

You can enable priority processing at the deployment level and [(optionally) at the request level](#enable-priority-processing-at-the-request-level).

> [!NOTE]
> Priority processing can be enabled in Global standard or Data Zone standard (US) deployments. Priority processing uses the same quota as standard processing.

In the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs), turn on the **Priority processing** toggle on the deployment details page when creating the deployment or update the setting of a deployed model by editing the deployment details.

:::image type="content" source="../media/priority-processing/enable-priority-processing.png" alt-text="Screenshot showing how to enable priority processing by updating the settings of a deployed model in the Foundry portal." lightbox="../media/priority-processing/enable-priority-processing.png":::

> [!NOTE]
> If you prefer to use code to enable priority processing at the deployment level, you can do so via the REST API for deployment by setting the `service_tier` attribute as follows: `"properties" : {"service_tier" : "priority"}`. Allowed values for the `service_tier` attribute are `default` and `priority`. `default` implies standard processing, while `priority` enables priority processing.

Once a model deployment is configured to use priority processing, you can start sending requests to the model.

[!INCLUDE [priority-processing 2](../../../foundry/openai/includes/concepts-priority-processing-2.md)]
