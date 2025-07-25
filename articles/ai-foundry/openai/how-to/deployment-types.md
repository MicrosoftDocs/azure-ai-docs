---
title: Understanding Azure AI Foundry Models Deployment Types
description: Learn how to use Azure AI Foundry deployment types including Global Standard, Standard, and Provisioned. 
author: mrbullwinkle
ms.author: mbullwin
manager: nitinme
ms.date: 04/30/2025
ms.service: azure-ai-openai
ms.topic: how-to
ms.custom:
  - build-2025
---

# Deployment types for Azure AI Foundry models

Azure AI Foundry makes models available by using the model deployment concept in Azure AI Foundry Services (formerly known as Azure AI Services). Model deployments are also Azure resources and, when created, give access to a given model under certain configurations. Such a configuration includes the infrastructure required to process the requests.

Azure AI Foundry models provide customers with hosting structure choices that fit their business and usage patterns. Those options are translated to different deployments types (or SKUs) that are available at model deployment time in the Azure AI Foundry resource. 

The service offers two main types of deployments: *standard* and *provisioned*. For a given deployment type, customers can align their workloads with their data processing requirements. They can choose an Azure geography (`Standard` or `Provisioned-Managed`), a Microsoft-specified data zone (`DataZone-Standard` or `DataZone Provisioned-Managed`), or a global (`Global-Standard` or `Global Provisioned-Managed`) processing option.

For fine-tuned models, an additional `Developer` deployment type provides a cost-efficient means of custom model evaluation, but without data residency.

All deployments can perform the exact same inference operations, but the billing, scale, and performance are substantially different. As part of your solution design, you need to make key decisions in two categories:

- Data-processing location  
- Call volume

## Azure AI Foundry deployment data processing locations

For standard deployments, there are three deployment-type options to choose from: global, data zone, and Azure geography. For provisioned deployments, there are two deployment-type options to choose from: global and Azure geography. We recommend Global Standard as a starting point.

### Global deployments

Global deployments use the global infrastructure of Azure to dynamically route customer traffic to the data center with the best availability for the customer’s inference requests. This means that global offers the highest initial throughput limits and best model availability, but still provides our uptime SLA and low latency. For high-volume workloads above the specified usage tiers on Standard and Global Standard, you might experience increased latency variation. For customers that require the lower latency variance at large workload usage, we recommend using our provisioned deployment types.

Our global deployments are the first location for all new models and features. Depending on call volume, customers with large volume and low latency variance requirements should consider our provisioned deployment types.

### Data Zone deployments

Data Zone deployments use the global infrastructure of Azure. They dynamically route customer traffic to the data center with the best availability for the customer's inference requests within the data zone defined by Microsoft. Positioned between our Azure geography and global deployment offerings, data zone deployments provide elevated quota limits, but keep data processing within the Microsoft-specified data zone. Data stored at rest continues to remain in the geography of the Azure AI Foundry resource. For example, for an AI Foundry resource created in the Sweden Central Azure region, the Azure geography is Sweden.

If the Azure AI Foundry resource used in your data zone deployment is located in the United States, the data is processed within the United States. If the Azure AI Foundry resource used in your data zone deployment is located in a European Union member nation, the data is processed within the European Union member nation geographies. For all Azure AI Foundry deployment types, any data stored at rest continues to remain in the geography of the Azure AI Foundry resource. Azure data processing and compliance commitments are still applicable.

For any [deployment type](/azure/ai-services/openai/how-to/deployment-types) labeled `Global`, prompts and responses might be processed in any geography where the relevant Azure AI Foundry model is deployed (learn more about [region availability of models](/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability)). For any deployment type labeled as `DataZone`, prompts and responses might be processed in any geography within the specified data zone, as defined by Microsoft. 

If you create a `DataZone` deployment in an Azure AI Foundry resource located in the United States, prompts and responses might be processed anywhere within the United States. If you create a DataZone deployment in an Azure AI Foundry resource located in a European Union member nation, prompts and responses might be processed in that or any other European Union member nation. 

For both `Global` and `DataZone` deployment types, any data stored at rest, such as uploaded data, is stored in the customer-designated geography. The location of processing only is affected when a customer uses a `Global` deployment type or `DataZone` deployment type in Azure AI Foundry resource. Azure data processing and compliance commitments are still applicable.

> [!NOTE]
> With Global Standard and Data Zone Standard deployment types, if the primary region experiences an interruption in service, all traffic that is initially routed to this region is impacted. To learn more, consult the [business continuity and disaster recovery guide](../how-to/business-continuity-disaster-recovery.md).

## Global Standard

> [!IMPORTANT]
> Data stored at rest remains in the designated Azure geography. However, data might be processed for inferencing in any Azure AI Foundry location. [Learn more about data residency](https://azure.microsoft.com/explore/global-infrastructure/data-residency/).

- SKU name in code: `GlobalStandard`

Global deployments are available in the same Azure AI Foundry resources as non-global deployment types. However, they allow you to use the global infrastructure of Azure to dynamically route traffic to the data center with the best availability for each request. Global Standard provides the highest default quota and eliminates the need to load balance across multiple resources.  

Customers with high consistent volume might experience greater latency variability. The threshold is set per model. To learn more, see the [Quotas page](./quota.md). For applications that require lower latency variance at large workload usage, we recommend purchasing provisioned throughput.

## Global Provisioned

> [!IMPORTANT]
> Data stored at rest remains in the designated Azure geography. However, data might be processed for inferencing in any Azure AI Foundry location. [Learn more about data residency](https://azure.microsoft.com/explore/global-infrastructure/data-residency/).

- SKU name in code: `GlobalProvisionedManaged`

Global deployments are available in the same Azure AI Foundry resources as non-global deployment types. However, they allow you to use the global infrastructure of Azure to dynamically route traffic to the data center with the best availability for each request. Global-Provisioned deployments provide reserved model processing capacity for high and predictable throughput by using Azure global infrastructure.  

## Global Batch

> [!IMPORTANT]
> Data stored at rest remains in the designated Azure geography. However, data might be processed for inferencing in any Azure AI Foundry location. [Learn more about data residency](https://azure.microsoft.com/explore/global-infrastructure/data-residency/).

[Global Batch](./batch.md) is designed to handle large-scale and high-volume processing tasks efficiently. You can process asynchronous groups of requests with separate quota and a 24-hour target turnaround, at [50% less cost than Global Standard](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/). With batch processing, rather than sending one request at a time, you send a large number of requests in a single file. Global Batch requests have a separate enqueued token quota, which avoids any disruption of your online workloads.  

- SKU name in code: `GlobalBatch`

Key use cases include:

- **Large-scale data processing**: Quickly analyze extensive datasets in parallel.
- **Content generation**: Create large volumes of text, such as product descriptions or articles.
- **Document review and summarization**: Automate the review and summarization of lengthy documents.
- **Customer support automation**: Handle numerous queries simultaneously for faster responses.
- **Data extraction and analysis**: Extract and analyze information from vast amounts of unstructured data.
- **Natural language processing (NLP) tasks**: Perform tasks like sentiment analysis or translation on large datasets.
- **Marketing and personalization**: Generate personalized content and recommendations at scale.

## Data Zone Standard

> [!IMPORTANT]
> Data stored at rest remains in the designated Azure geography. However, data might be processed for inferencing in any Azure AI Foundry location within the Microsoft-specified data zone. [Learn more about data residency](https://azure.microsoft.com/explore/global-infrastructure/data-residency/).

- SKU name in code: `DataZoneStandard`

Data Zone Standard deployments are available in the same Azure AI Foundry resource as all other Azure AI Foundry deployment types. However, they allow you to use the global infrastructure of Azure to dynamically route traffic to the data center within the Microsoft-defined data zone with the best availability for each request. Data Zone Standard provides higher default quotas than our Azure geography-based deployment types.

Customers with high consistent volume might experience greater latency variability. The threshold is set per model. To learn more, see the [quotas and limits page](/azure/ai-services/openai/quotas-limits#usage-tiers). For workloads that require low latency variance at large volume, we recommend using the provisioned deployment offerings.

## Data Zone Provisioned

> [!IMPORTANT]
> Data stored at rest remains in the designated Azure geography. However, data might be processed for inferencing in any Azure AI Foundry location within the Microsoft-specified data zone. [Learn more about data residency](https://azure.microsoft.com/explore/global-infrastructure/data-residency/).

SKU name in code: `DataZoneProvisionedManaged`

Data Zone Provisioned deployments are available in the same Azure AI Foundry resource as all other Azure AI Foundry deployment types. However, they allow you to use the global infrastructure of Azure to dynamically route traffic to the data center within the Microsoft-specified data zone with the best availability for each request. Data Zone Provisioned deployments provide reserved model processing capacity for high and predictable throughput by using Azure infrastructure within the Microsoft-specified data zone.  

## Data Zone Batch

> [!IMPORTANT]
> Data stored at rest remains in the designated Azure geography. However, data might be processed for inferencing in any Azure AI Foundry location within the Microsoft-specified data zone. [Learn more about data residency](https://azure.microsoft.com/explore/global-infrastructure/data-residency/).

- SKU name in code: `DataZoneBatch`

Data Zone Batch deployments provide all the same functionality as [Global Batch deployments](./batch.md). However, they allow you to use the global infrastructure of Azure to dynamically route traffic to only data centers within the Microsoft-defined data zone with the best availability for each request.

## Standard

- SKU name in code: `Standard`

Standard deployments provide a pay-per-call billing model on the chosen model. This model can be a fast way to get started, because you pay only for what you consume. Models available in each region and throughput might be limited.  

Standard deployments are optimized for low-to-medium volume workloads with high burstiness. Customers with high consistent volume might experience greater latency variability.

## Regional Provisioned

- SKU name in code: `ProvisionedManaged`

Regional Provisioned deployments allow you to specify the amount of throughput you require in a deployment. The service then allocates the necessary model processing capacity and ensures it's ready for you. Throughput is defined in terms of provisioned throughput units, which is a normalized way of representing the throughput for your deployment. Each model-version pair requires different amounts of provisioned throughput units to deploy, and provides different amounts of throughput per provisioned throughput unit. Learn more from this article about [provisioned throughput concepts](../concepts/provisioned-throughput.md).

### Disable access to global deployments in your subscription

Azure Policy helps to enforce organizational standards and to assess compliance at scale. Through its compliance dashboard, it provides an aggregated view to evaluate the overall state of the environment, with the ability to drill down to per-resource, per-policy granularity. It also helps to bring your resources to compliance through bulk remediation for existing resources and automatic remediation for new resources. [Learn more about Azure Policy and specific built-in controls for AI services](/azure/ai-services/security-controls-policy).

You can use the following policy to disable access to any Azure AI Foundry deployment type. To disable access to a specific deployment type, replace `GlobalStandard` with the SKU name for the deployment type that you would like to disable access to.

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

## Developer (for fine-tuned models)

> [!IMPORTANT]
> Data stored at rest remains in the designated Azure geography. However, data might be processed for inferencing in any Azure AI Foundry location. [Learn more about data residency](https://azure.microsoft.com/explore/global-infrastructure/data-residency/).

- SKU name in code: `Developer`

Fine-tuned models support a `Developer` deployment designed to support custom model evaluation. It doesn't offer data residency guarantees or an SLA. To learn more about using the `Developer` deployment type, see the [fine-tuning guide](./fine-tune-test.md).

## Deploy models

:::image type="content" source="../media/deployment-types/deploy-models-new.png" alt-text="Screenshot that shows the model deployment dialog in Azure AI Foundry portal with a deployment type highlighted.":::

To learn about creating resources and deploying models, refer to the [Resource creation guide](./create-resource.md).

## Related content

- [Quotas and limits](./quota.md)
- [Onboarding for provisioned throughput units](./provisioned-throughput-onboarding.md)
- [Get started with provisioned throughput units](./provisioned-get-started.md)
