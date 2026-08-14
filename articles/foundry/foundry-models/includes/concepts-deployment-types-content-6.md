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
