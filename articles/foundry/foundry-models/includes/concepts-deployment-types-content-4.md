---
title: include file
description: include file
ai-usage: ai-assisted
author: alvinashcraft
ms.author: aashcraft
ms.service: microsoft-foundry
ms.topic: include
ms.date: 08/06/2026
ms.custom: include, classic-and-new
---

| Deployment type | SKU code | Data processing | Billing | Best for |
| --------------- | -------- | --------------- | ------- | -------- |
| [Global Standard](#global-standard) | `GlobalStandard` | Any Azure region | Pay-per-token | General workloads, highest quota |
| [Global Provisioned](#global-provisioned) | `GlobalProvisionedManaged` | Any Azure region | Reserved PTU | Predictable high-throughput |
| [Global Batch](#global-batch) | `GlobalBatch` | Any Azure region | 50% discount, 24-hr | Large async jobs |
| [Data Zone Standard](#data-zone-standard) | `DataZoneStandard` | Within data zone | Pay-per-token | EU/US/APAC data zone compliance |
| [Data Zone Provisioned](#data-zone-provisioned) | `DataZoneProvisionedManaged` | Within data zone | Reserved PTU | Data zone + predictable throughput |
| [Data Zone Batch](#data-zone-batch) | `DataZoneBatch` | Within data zone | 50% discount | Large async jobs with data zone |
| [Standard](#standard) | `Standard` | Single region | Pay-per-token | Regional compliance, low volume |
| [Regional Provisioned](#regional-provisioned) | `ProvisionedManaged` | Single region | Reserved PTU | Regional compliance + throughput |
| [Developer](#developer-for-fine-tuned-models) | `DeveloperTier` | Any Azure region | Pay-per-token | Fine-tuned model evaluation only (24-hour lifetime, no SLA or data-residency guarantee) |

> [!NOTE]
> Not all models support all deployment types. Check [Foundry Models sold by Azure](../concepts/models-sold-directly-by-azure.md) for model availability by deployment type and region.

SLA guarantees vary by deployment type. Provisioned types provide guaranteed throughput and lower latency variance. Standard types offer best-effort service. Developer deployments don't include an SLA. For details, see the [Azure SLA for Azure OpenAI Service](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services).

> [!TIP]
> For detailed pricing, see [Azure OpenAI Service pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/).

## Choose the right deployment type

Use the following table for a quick recommendation, then refine it with the criteria that follow.

| Requirement | Recommended tier |
| --- | --- |
| Default: newest models, lowest price, broadest regions | Global Standard |
| Reserved, predictable throughput | Global Provisioned |
| Keep processing within a data zone | Data Zone Standard or Data Zone Provisioned |
| Data residency plus reserved throughput | Data Zone Provisioned |
| Pin processing to a single region | Standard or Regional Provisioned (where supported) |
| Large asynchronous jobs at lower cost | Global Batch or Data Zone Batch (where supported) |
| Evaluate a fine-tuned model (temporary, no SLA) | Developer |

### By data residency requirement

- **No restrictions**: Use Global Standard or Global Provisioned
- **EU, US, or APAC data zone**: Use Data Zone Standard or Data Zone Provisioned in a region within that data zone
- **Single region only**: Use Standard or Regional Provisioned

For the exact regions in each data zone, see [Data Zone deployments](#data-zone-deployments).

### By workload pattern
