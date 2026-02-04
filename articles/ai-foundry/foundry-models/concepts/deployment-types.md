---
title: Understanding deployment types in Microsoft Foundry Models
titleSuffix: Microsoft Foundry
description: Compare Microsoft Foundry deployment types including Global Standard, Provisioned, DataZone, and Batch. Learn about data residency, pricing, and when to use each type.
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
author: msakande
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: concept-article
ms.date: 02/04/2026
ms.author: mopeakande
ms.custom: ignite-2024, github-universe-2024, pilot-ai-workflow-jan-2026

---

# Deployment types for Microsoft Foundry Models

When you deploy a model in Microsoft Foundry, you choose a deployment type that determines:

- **Where your data is processed** (global, data zone, or single region)
- **How you pay** (pay-per-token or reserved capacity)
- **Performance characteristics** (latency variance, throughput limits)

The service offers two main categories: *standard* (pay-per-token) and *provisioned* (reserved capacity). Within each category, you can choose global, data zone, or regional processing based on your compliance requirements.

:::image type="content" source="../media/add-model-deployments/models-deploy-deployment-type.png" alt-text="Screenshot of the Foundry portal deployment dialog showing the deployment type selection box with Global Standard selected." lightbox="../media/add-model-deployments/models-deploy-deployment-type.png":::

> [!IMPORTANT]
> **Data residency for all deployment types**: Data stored at rest remains in the designated Azure geography. However, inferencing data is processed as follows:
> - **Global** types: May be processed in any Azure region
> - **DataZone** types: Processed only within the Microsoft-specified data zone (US or EU)
> - **Standard/Regional** types: Processed in the deployment region
>
> [Learn more about data residency](https://azure.microsoft.com/explore/global-infrastructure/data-residency/).

## Deployment type comparison

| Deployment type | SKU code | Data processing | Billing | Best for |
| --------------- | -------- | --------------- | ------- | -------- |
| [Global Standard](#global-standard) | `GlobalStandard` | Any Azure region | Pay-per-token | General workloads, highest quota |
| [Global Provisioned](#global-provisioned) | `GlobalProvisionedManaged` | Any Azure region | Reserved PTU | Predictable high-throughput |
| [Global Batch](#global-batch) | `GlobalBatch` | Any Azure region | 50% discount, 24-hr | Large async jobs |
| [Data Zone Standard](#data-zone-standard) | `DataZoneStandard` | Within data zone | Pay-per-token | EU/US data zone compliance |
| [Data Zone Provisioned](#data-zone-provisioned) | `DataZoneProvisionedManaged` | Within data zone | Reserved PTU | Data zone + predictable throughput |
| [Data Zone Batch](#data-zone-batch) | `DataZoneBatch` | Within data zone | 50% discount | Large async jobs with data zone |
| [Standard](#standard) | `Standard` | Single region | Pay-per-token | Regional compliance, low volume |
| [Regional Provisioned](#regional-provisioned) | `ProvisionedManaged` | Single region | Reserved PTU | Regional compliance + throughput |
| [Developer](#developer-for-fine-tuned-models) | `DeveloperTier` | Any Azure region | Pay-per-token | Fine-tuned model evaluation only |

> [!NOTE]
> Not all models support all deployment types. Check [Foundry Models sold directly by Azure](models-sold-directly-by-azure.md) for model availability by deployment type and region.

> [!TIP]
> For detailed pricing, see [Azure OpenAI Service pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/).

## Choose the right deployment type

Use the following criteria to select a deployment type:

### By data residency requirement

- **No restrictions**: Use Global Standard or Global Provisioned
- **EU data zone**: Use DataZone Standard or DataZone Provisioned in an EU region
- **US data zone**: Use DataZone Standard or DataZone Provisioned in a US region
- **Single region only**: Use Standard or Regional Provisioned

### By workload pattern

- **Variable, bursty traffic**: Use Standard or Global Standard (pay-per-token)
- **Consistent high volume**: Use Provisioned types (reserved capacity)
- **Large batch jobs (not time-sensitive)**: Use Global Batch or DataZone Batch (50% cost savings)
- **Fine-tuned model evaluation**: Use Developer (no SLA, lowest cost)

### By latency requirement

- **Low latency variance required**: Use Provisioned types
- **Latency variance acceptable**: Use Standard types

## Data processing locations

For standard deployments, there are three options: global, data zone, and Azure geography. For provisioned deployments, there are two options: global and Azure geography. Global Standard is a common starting point for most workloads.

### Global deployments

Global deployments use Azure's global infrastructure to dynamically route traffic to available datacenters. Global deployments offer the highest initial throughput limits and broadest model availability.

For high-volume workloads, you might experience increased latency variation. If you require lower latency variance at scale, use provisioned deployment types.

Global deployments receive new models and features first.

### Data Zone deployments

For **Global** deployment types, prompts and responses might be processed in any geography where the model is deployed. For **DataZone** deployment types, prompts and responses are processed only within the specified data zone:

- **United States**: Data processed anywhere within the US
- **European Union**: Data processed within any EU member nation

Learn more in the "Model region availability by deployment type" section of [Foundry Models sold directly by Azure](models-sold-directly-by-azure.md#foundry-models-sold-directly-by-azure).

> [!NOTE]
> With Global Standard and Data Zone Standard deployment types, if the primary region experiences an interruption in service, all traffic initially routed to this region is affected. To learn more, see the [business continuity and disaster recovery guide](../../openai/how-to/business-continuity-disaster-recovery.md).

## Global Standard

- SKU name in code: `GlobalStandard`

Global Standard deployments use Azure's global infrastructure to dynamically route traffic to available datacenters. This deployment type provides the highest default quota and eliminates the need to load balance across multiple resources.  

Customers with high consistent volume might experience greater latency variability. The threshold is set per model. To learn more, see the [Quotas page](../quotas-limits.md). For applications that require lower latency variance at large workload usage, consider provisioned throughput.

Global Standard supports priority processing for faster response times on a pay-as-you-go basis. To learn more, see [Priority processing for Foundry models (preview)](../../openai/concepts/priority-processing.md).

## Global Provisioned

- SKU name in code: `GlobalProvisionedManaged`

Global Provisioned deployments use Azure's global infrastructure to dynamically route traffic to available datacenters. This deployment type provides reserved model processing capacity for predictable throughput, combining global routing with guaranteed capacity.  

## Global Batch

- SKU name in code: `GlobalBatch`

[Global Batch](../../openai/how-to/batch.md) handles large-scale and high-volume processing tasks. You can process asynchronous groups of requests with separate quota and a 24-hour target turnaround, at [50% less cost than Global Standard](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/). With batch processing, rather than sending one request at a time, you send a large number of requests in a single file. Global Batch requests have a separate enqueued token quota, which avoids any disruption of your online workloads.  

Common use cases:

- **Large-scale data processing**: Analyze datasets in parallel.
- **Content generation**: Create large volumes of text, such as product descriptions or articles.
- **Document review and summarization**: Process and summarize lengthy documents.
- **Customer support automation**: Handle numerous queries simultaneously.
- **Data extraction and analysis**: Extract and analyze information from large amounts of unstructured data.
- **Natural language processing (NLP) tasks**: Perform sentiment analysis or translation on large datasets.

## Data Zone Standard

- SKU name in code: `DataZoneStandard`

Data Zone Standard deployments dynamically route traffic to datacenters within the Microsoft-defined data zone (US or EU). This deployment type provides higher default quotas than geography-based deployment types while keeping data within the specified zone.

Customers with high consistent volume might experience greater latency variability. The threshold is set per model. To learn more, see the [quotas and limits page](../quotas-limits.md). For workloads that require low latency variance at large volume, consider provisioned deployment types.

Data Zone Standard supports priority processing for faster response times on a pay-as-you-go basis. To learn more, see [Priority processing for Foundry models (preview)](../../openai/concepts/priority-processing.md).

## Data Zone Provisioned

- SKU name in code: `DataZoneProvisionedManaged`

Data Zone Provisioned deployments dynamically route traffic within the Microsoft-specified data zone (US or EU) while providing reserved model processing capacity. This deployment type combines data zone compliance with high and predictable throughput.  

## Data Zone Batch

- SKU name in code: `DataZoneBatch`

Data Zone Batch deployments provide the same functionality as [Global Batch](../../openai/how-to/batch.md), including 50% cost savings and 24-hour turnaround. Traffic is routed only to datacenters within the Microsoft-defined data zone (US or EU).

## Standard

- SKU name in code: `Standard`

Standard deployments use pay-per-call billing. You pay only for what you consume. Models available in each region and throughput might be limited.

Standard deployments are suited for low-to-medium volume workloads with high burstiness. Customers with high consistent volume might experience greater latency variability.

## Regional Provisioned

- SKU name in code: `ProvisionedManaged`

Regional Provisioned deployments allow you to specify the amount of throughput you require in a deployment. The service then allocates the necessary model processing capacity and ensures it's ready for you. Throughput is defined in terms of provisioned throughput units, which is a normalized way of representing the throughput for your deployment. Each model-version pair requires different amounts of provisioned throughput units to deploy, and provides different amounts of throughput per provisioned throughput unit. Learn more in the [article about provisioned throughput concepts](../../openai/concepts/provisioned-throughput.md).

## Developer (for fine-tuned models)

- SKU name in code: `DeveloperTier`

The Developer deployment type is designed for fine-tuned model evaluation only. It provides cost-efficient testing of custom models but doesn't include data residency guarantees or an SLA. To learn more about using the Developer deployment type, see the [fine-tuning guide](../../openai/how-to/fine-tune-test.md).

## Troubleshooting deployment issues

Common issues when creating or using deployments:

| Issue | Cause | Resolution |
|-------|-------|------------|
| Deployment type unavailable | Model doesn't support the selected type | Check [model availability by deployment type](models-sold-directly-by-azure.md) |
| Quota exceeded | Subscription limit reached for tokens per minute | Request quota increase in Azure portal or use a different region |
| Region unavailable | Model not deployed in selected region | Select a region from the model's availability list |
| Provisioned capacity unavailable | No PTU capacity in region | Try a different region or use Global Provisioned for broader availability |

For quota limits by deployment type, see [Foundry Models quotas and limits](../quotas-limits.md).

## Restrict deployment types with Azure Policy

Azure Policy helps enforce organizational standards and assess compliance at scale. Through its compliance dashboard, you can evaluate the overall state of the environment and drill down to per-resource, per-policy granularity. Azure Policy also supports bulk remediation for existing resources and automatic remediation for new resources. [Learn more about Azure Policy and specific built-in controls for Foundry Tools](../../../ai-services/security-controls-policy.md).

Use the following policy to disable access to a specific Foundry deployment type. Replace `GlobalStandard` with the SKU name for the deployment type you want to restrict.

```json
{
    "mode": "All",
    "policyRule": {
        "if": {
            "allOf": [
                {
                    "field": "type",
                    "equals": "Microsoft.CognitiveServices/accounts/deployments"
                },
                {
                    "field": "Microsoft.CognitiveServices/accounts/deployments/sku.name",
                    "equals": "GlobalStandard"
                }
            ]
        }
    }
}
```

## Deploy models

:::image type="content" source="../../openai/media/deployment-types/deploy-models-new.png" alt-text="Screenshot of the Foundry portal deployment dialog showing the model name field and deployment options.":::

To learn about creating resources and deploying models, see [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md) and [Create and deploy an Azure OpenAI in Microsoft Foundry Models resource](../../openai/how-to/create-resource.md).

## Related content

- [Foundry Models sold directly by Azure](models-sold-directly-by-azure.md)
- [Microsoft Foundry Models quotas and limits](../quotas-limits.md)
- [Provisioned throughput concepts](../../openai/concepts/provisioned-throughput.md)
- [Global Batch processing](../../openai/how-to/batch.md)
- [Azure OpenAI Service pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/)
- [Data privacy and security for Foundry Models](../../how-to/concept-data-privacy.md)
- [Business continuity and disaster recovery](../../openai/how-to/business-continuity-disaster-recovery.md)