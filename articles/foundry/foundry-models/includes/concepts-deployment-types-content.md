---
title: include file
description: include file
author: alvinashcraft
ms.author: aashcraft
ms.service: microsoft-foundry
ms.topic: include
ms.date: 08/06/2026
ms.custom: include, classic-and-new
---

When you deploy a model in Microsoft Foundry, you choose a deployment type that determines:

- **Where your data is processed** (global, data zone, or single region)
- **How you pay** (pay-per-token or reserved capacity)
- **Performance characteristics** (latency variance, throughput limits)

These deployment types apply to the **Serverless API** deployment option. Open-source and custom models that use **managed compute** don't use these types. For how the options differ, see [Deployment overview for Microsoft Foundry Models](../../concepts/deployments-overview.md).

The service offers three main categories: *standard* (pay-per-token), *provisioned* (reserved capacity), and *batch* (discounted asynchronous processing). A *Developer* type is also available for fine-tuned model evaluation. Within the standard and provisioned categories, you can choose global, data zone, or regional processing based on your compliance requirements.

[!INCLUDE [try-instant-models](../../includes/try-instant-models.md)]

:::image type="content" source="../media/add-model-deployments/models-deploy-deployment-type.png" alt-text="Screenshot of the Foundry portal deployment dialog showing the deployment type selection box with Global Standard selected." lightbox="../media/add-model-deployments/models-deploy-deployment-type.png":::

> [!IMPORTANT]
> **Data residency for all deployment types**: Data stored at rest remains in the designated Azure geography. However, inferencing data is processed as follows:
> - **Global** types: May be processed in any Azure region
> - **Data Zone** types: The service processes data only within the Microsoft-specified data zone (US, EU, or Asia Pacific (APAC)).
> - **Standard (single region)** types: The service processes data in the deployment region.
>
> [Learn more about data residency](https://azure.microsoft.com/explore/global-infrastructure/data-residency/).

## Start with Global Standard

For most workloads, start with **Global Standard**. It launches first when a new model releases, has the lowest price, and offers the broadest region coverage. Move to another deployment type only when you have a specific reason, such as data residency, reserved throughput, or asynchronous batch processing.

New deployment types become available in a set order: Global, then Data Zone, then single region. Single-region deployment types arrive last, have no guaranteed availability date, and depend on capacity that frees up as older models retire. For the authoritative launch order, see [Model launch and availability](../../openai/concepts/model-retirements.md#model-launch-and-availability).

## Deployment type comparison

Instant models let you run inference without creating a deployment, so they aren't deployment types. To try a model instantly, see [Instant access to models](../../concepts/instant-models.md).

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

- **Quick start, prototyping, or trying a new model**: Use [instant access (preview)](../../concepts/instant-models.md) (no deployment needed)
- **Variable, bursty traffic**: Use Standard or Global Standard (pay-per-token)
- **Consistent high volume**: Use Provisioned types (reserved capacity)
- **Large batch jobs (not time-sensitive)**: Use Global Batch or Data Zone Batch (50% cost savings)
- **Fine-tuned model evaluation**: Use Developer (no SLA, lowest cost)

### By latency requirement

- **Low latency variance required**: Use Provisioned types
- **Latency variance acceptable**: Use Standard types
- **Evaluating a fine-tuned model**: Use developer (no SLA; not intended for latency-sensitive workloads).

## Data processing locations

Standard and provisioned deployments both offer three data-processing options: global, data zone, and single region (Azure geography). Global standard is a common starting point for most workloads.

### Global deployments

Global deployments use Azure's global infrastructure to dynamically route traffic to available datacenters. Global deployments offer the highest initial throughput limits and broadest model availability.

For high-volume workloads, you might experience increased latency variation. If you require lower latency variance at scale, use provisioned deployment types.

Global deployments receive new models and features first.

### Data Zone deployments

For **Global** deployment types, the service can process prompts and responses in any geography where the model is deployed. For **Data Zone** deployment types, the service processes prompts and responses only within the specified data zone:

- **United States**: The service processes data anywhere within the US.
- **European Union**: The service processes data within the [Azure EU Data Boundary](/privacy/eudb/eu-data-boundary-learn).
- **Asia Pacific**: The service processes data within the APAC data zone.

The EU Data Zone follows the [Azure EU Data Boundary](/privacy/eudb/eu-data-boundary-learn), which can include European Free Trade Association (EFTA) countries and regions such as Norway and Switzerland in addition to EU member states. The APAC Data Zone covers multiple Asia Pacific regions. Microsoft can add regions to either data zone without prior notice to improve capacity and availability. For the current per-region breakdown, see the "Model region availability by deployment type" section of [Foundry Models sold by Azure](../concepts/models-sold-directly-by-azure.md).

> [!NOTE]
> With Global Standard and Data Zone Standard deployment types, if the primary region experiences an interruption in service, all traffic initially routed to this region is affected. To learn more, see the [high availability and disaster recovery guide](../../how-to/high-availability-resiliency.md).

## Global Standard

- SKU name in code: `GlobalStandard`

Global Standard deployments use Azure's global infrastructure to dynamically route traffic to available datacenters. This deployment type provides the highest default quota and eliminates the need to load balance across multiple resources.  

Customers with high consistent volume might experience greater latency variability. The threshold is set per model. To learn more, see the [Quotas page](../quotas-limits.md). For applications that require lower latency variance at large workload usage, consider provisioned throughput.

Global Standard supports priority processing for faster response times on a pay-as-you-go basis. To learn more, see [Priority processing for Foundry models](../../openai/concepts/priority-processing.md).

## Global Provisioned

- SKU name in code: `GlobalProvisionedManaged`

Global Provisioned deployments use Azure's global infrastructure to dynamically route traffic to available datacenters. This deployment type provides reserved model processing capacity for predictable throughput, combining global routing with guaranteed capacity.

With provisioned throughput, you purchase a fixed number of provisioned throughput units (PTUs) that guarantee a specific level of processing capacity. This deployment type provides lower and more consistent latency than Global Standard. To learn more, see [Provisioned throughput concepts](../../openai/concepts/provisioned-throughput.md).

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

> [!NOTE]
> Batch deployments trade real-time responsiveness for cost savings. Batch requests don't have a real-time SLA — they target completion within 24 hours but might take longer.

## Data Zone Standard

- SKU name in code: `DataZoneStandard`

Data Zone Standard deployments dynamically route traffic to datacenters within the Microsoft-defined data zone (US, EU, or APAC). This deployment type provides higher default quotas than single-region deployment types while keeping data within the specified zone.

Customers with high consistent volume might experience greater latency variability. The threshold is set per model. To learn more, see the [quotas and limits page](../quotas-limits.md). For workloads that require low latency variance at large volume, consider provisioned deployment types.

Data Zone Standard supports priority processing for faster response times on a pay-as-you-go basis. To learn more, see [Priority processing for Foundry models](../../openai/concepts/priority-processing.md).

## Data Zone Provisioned

- SKU name in code: `DataZoneProvisionedManaged`

Data Zone Provisioned deployments dynamically route traffic within the Microsoft-specified data zone (US, EU, or APAC) while providing reserved model processing capacity. This deployment type combines data zone compliance with high and predictable throughput.  

## Data Zone Batch

- SKU name in code: `DataZoneBatch`

Data Zone Batch deployments provide the same functionality as [Global Batch](../../openai/how-to/batch.md), including 50% cost savings and 24-hour turnaround. Traffic is routed only to datacenters within the Microsoft-defined data zone (US, EU, or APAC).

## Standard

- SKU name in code: `Standard`

Standard deployments use pay-per-token billing. You pay only for what you consume. Models available in each region and throughput might be limited.

Standard deployments are suited for low-to-medium volume workloads with high burstiness. Customers with high consistent volume might experience greater latency variability.

## Regional Provisioned

- SKU name in code: `ProvisionedManaged`

Regional Provisioned deployments allow you to specify the amount of throughput you require in a deployment. The service then allocates the necessary model processing capacity and ensures it's ready for you. Throughput is defined in terms of provisioned throughput units (PTUs), which is a normalized way of representing the throughput for your deployment. Each model-version pair requires different amounts of PTUs to deploy, and provides different amounts of throughput per PTU. Minimum PTU requirements vary by model. For current minimums and available capacity, see [Provisioned throughput concepts](../../openai/concepts/provisioned-throughput.md).

## Developer (for fine-tuned models)

- SKU name in code: `DeveloperTier`

The Developer deployment type is designed for fine-tuned model evaluation only. It provides cost-efficient testing of custom models but doesn't include data residency guarantees or an SLA. Developer deployments have a fixed 24-hour lifetime and are automatically deleted after expiration. To learn more about using the Developer deployment type, see the [fine-tuning guide](../../../foundry-classic/openai/how-to/fine-tune-test.md).

## Troubleshooting deployment issues

Common issues when creating or using deployments:

| Issue | Cause | Resolution |
|-------|-------|------------|
| Deployment type unavailable | Model doesn't support the selected type | Check [model availability by deployment type](../concepts/models-sold-directly-by-azure.md) |
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

## Related content

- [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md)
- [Create and deploy an Azure OpenAI in Microsoft Foundry Models resource](../../../foundry-classic/openai/how-to/create-resource.md)
- [Foundry Models sold by Azure](../concepts/models-sold-directly-by-azure.md)
- [Model region availability by deployment type](../concepts/models-sold-directly-by-azure.md)
- [Microsoft Foundry Models quotas and limits](../quotas-limits.md)
- [Provisioned throughput concepts](../../openai/concepts/provisioned-throughput.md)
- [Global Batch processing](../../openai/how-to/batch.md)
- [Azure OpenAI Service pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/)
- [Data privacy and security for Foundry Models](../../../foundry-classic/how-to/concept-data-privacy.md)
- [High availability and disaster recovery](../../how-to/high-availability-resiliency.md)
