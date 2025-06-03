---
title: Understanding Azure OpenAI in Azure AI Foundry Models deployment types
description: Learn how to use Azure OpenAI deployment types | Global-Standard | Standard | Provisioned.
author: mrbullwinkle
ms.author: mbullwin
manager: nitinme
ms.date: 04/30/2025
ms.service: azure-ai-openai
ms.topic: how-to
ms.custom:
  - build-2025
---

# Azure OpenAI deployment types

Azure OpenAI provides customers with choices on the hosting structure that fits their business and usage patterns. The service offers two main types of deployments: **standard** and **provisioned**. For a given deployment type, customers can align their workloads with their data processing requirements by choosing an Azure geography (`Standard` or `Provisioned-Managed`), Microsoft specified data zone (`DataZone-Standard` or `DataZone Provisioned-Managed`), or Global (`Global-Standard` or `Global Provisioned-Managed`) processing options.

For fine-tuned models, an additional `Developer` deployment type provides a cost-efficient means of custom model evaluation, but without data residency.

All deployments can perform the exact same inference operations, however the billing, scale, and performance are substantially different. As part of your solution design, you will need to make two key decisions:

- **Data processing location**  
- **Call volume**

## Azure OpenAI Deployment Data Processing Locations

For standard deployments, there are three deployment type options to choose from - global, data zone, and Azure geography. For provisioned deployments, there are two deployment type options to choose from - global and Azure geography. Global standard is the recommended starting point. 

Global deployments leverage Azure's global infrastructure to dynamically route customer traffic to the data center with the best availability for the customer’s inference requests. This means you will get the highest initial throughput limits and best model availability with Global while still providing our uptime SLA and low latency. For high volume workloads above the specified usage tiers on standard and global standard, you may experience increased latency variation. For customers that require the lower latency variance at large workload usage, we recommend leveraging our provisioned deployment types.

Our global deployments will be the first location for all new models and features. Depending on call volume, customers with large volume and low latency variance requirements should consider our provisioned deployment types.

Data zone deployments leverage Azure's global infrastructure to dynamically route customer traffic to the data center with the best availability for the customer's inference requests within the data zone defined by Microsoft. Positioned between our Azure geography and Global deployment offerings, data zone deployments provide elevated quota limits while keeping data processing within the Microsoft specified data zone. Data stored at rest will continue to remain in the geography of the Azure OpenAI resource (e.g., for an Azure OpenAI resource created in the Sweden Central Azure region, the Azure geography is Sweden).

If the Azure OpenAI resource used in your Data Zone deployment is located in the United States, the data will be processed within the United States. If the Azure OpenAI resource used in your Data Zone deployment is located in a European Union Member Nation, the data will be processed within the European Union Member Nation geographies. For all Azure OpenAI deployment types, any data stored at rest will continue to remain in the geography of the Azure OpenAI resource. Azure data processing and compliance commitments remain applicable.

For any [deployment type](/azure/ai-services/openai/how-to/deployment-types) labeled 'Global,' prompts and responses may be processed in any geography where the relevant Azure OpenAI model is deployed (learn more about [region availability of models](/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability)). For any deployment type labeled as 'DataZone,' prompts and responses may be processed in any geography within the specified data zone, as defined by Microsoft. If you create a DataZone deployment in an Azure OpenAI resource located in the United States, prompts and responses may be processed anywhere within the United States. If you create a DataZone deployment in an Azure OpenAI resource located in a European Union Member Nation, prompts and responses may be processed in that or any other European Union Member Nation. For both Global and DataZone deployment types, any data stored at rest, such as uploaded data, is stored in the customer-designated geography. Only the location of processing is affected when a customer uses a Global deployment type or DataZone deployment type in Azure OpenAI in Azure AI Foundry Models; Azure data processing and compliance commitments remain applicable.

> [!NOTE]
> With Global standard and Data zone standard deployment types if the primary region experiences an interruption in service all traffic that is initially routed to this region will be impacted. To learn more, consult the [business continuity and disaster recovery guide](../how-to/business-continuity-disaster-recovery.md).

## Global standard

> [!IMPORTANT]
> Data stored at rest remains in the designated Azure geography, while data may be processed for inferencing in any Azure OpenAI location. [Learn more about data residency](https://azure.microsoft.com/explore/global-infrastructure/data-residency/).

**SKU name in code:** `GlobalStandard`

Global deployments are available in the same Azure OpenAI resources as non-global deployment types but allow you to leverage Azure's global infrastructure to dynamically route traffic to the data center with best availability for each request.  Global standard provides the highest default quota and eliminates the need to load balance across multiple resources.  

Customers with high consistent volume may experience greater latency variability. The threshold is set per model. See the [quotas page to learn more](./quota.md).  For applications that require the lower latency variance at large workload usage, we recommend purchasing provisioned throughput.

## Global provisioned

> [!IMPORTANT]
> Data stored at rest remains in the designated Azure geography, while data may be processed for inferencing in any Azure OpenAI location. [Learn more about data residency](https://azure.microsoft.com/explore/global-infrastructure/data-residency/).

**SKU name in code:** `GlobalProvisionedManaged`

Global deployments are available in the same Azure OpenAI resources as non-global deployment types but allow you to leverage Azure's global infrastructure to dynamically route traffic to the data center with best availability for each request. Global provisioned deployments provide reserved model processing capacity for high and predictable throughput using Azure global infrastructure.  

## Global batch

> [!IMPORTANT]
> Data stored at rest remains in the designated Azure geography, while data may be processed for inferencing in any Azure OpenAI location. [Learn more about data residency](https://azure.microsoft.com/explore/global-infrastructure/data-residency/).

[Global batch](./batch.md) is designed to handle large-scale and high-volume processing tasks efficiently. Process asynchronous groups of requests with separate quota, with 24-hour target turnaround, at [50% less cost than global standard](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/). With batch processing, rather than send one request at a time you send a large number of requests in a single file. Global batch requests have a separate enqueued token quota avoiding any disruption of your online workloads.  

**SKU name in code:** `GlobalBatch`

Key use cases include:

* **Large-Scale Data Processing:** Quickly analyze extensive datasets in parallel.

* **Content Generation:** Create large volumes of text, such as product descriptions or articles.

* **Document Review and Summarization:** Automate the review and summarization of lengthy documents.

* **Customer Support Automation:** Handle numerous queries simultaneously for faster responses.

* **Data Extraction and Analysis:** Extract and analyze information from vast amounts of unstructured data.

* **Natural Language Processing (NLP) Tasks:** Perform tasks like sentiment analysis or translation on large datasets.

* **Marketing and Personalization:** Generate personalized content and recommendations at scale.

## Data zone standard

> [!IMPORTANT]
> Data stored at rest remains in the designated Azure geography, while data may be processed for inferencing in any Azure OpenAI location within the Microsoft specified data zone. [Learn more about data residency](https://azure.microsoft.com/explore/global-infrastructure/data-residency/).

**SKU name in code:** `DataZoneStandard`

Data zone standard deployments are available in the same Azure OpenAI resource as all other Azure OpenAI deployment types but allow you to leverage Azure global infrastructure to dynamically route traffic to the data center within the Microsoft defined data zone with the best availability for each request. Data zone standard provides higher default quotas than our Azure geography-based deployment types. 

Customers with high consistent volume may experience greater latency variability. The threshold is set per model. See the [Quotas and limits](/azure/ai-services/openai/quotas-limits#usage-tiers) page to learn more. For workloads that require low latency variance at large volume, we recommend leveraging the provisioned deployment offerings. 

## Data zone provisioned

> [!IMPORTANT]
> Data stored at rest remains in the designated Azure geography, while data may be processed for inferencing in any Azure OpenAI location within the Microsoft specified data zone.[Learn more about data residency](https://azure.microsoft.com/explore/global-infrastructure/data-residency/).

**SKU name in code:** `DataZoneProvisionedManaged`

Data zone provisioned deployments are available in the same Azure OpenAI resource as all other Azure OpenAI deployment types but allow you to leverage Azure global infrastructure to dynamically route traffic to the data center within the Microsoft specified data zone with the best availability for each request. Data zone provisioned deployments provide reserved model processing capacity for high and predictable throughput using Azure infrastructure within the Microsoft specified data zone.  

## Data zone batch

> [!IMPORTANT]
> Data stored at rest remains in the designated Azure geography, while data may be processed for inferencing in any Azure OpenAI location within the Microsoft specified data zone. [Learn more about data residency](https://azure.microsoft.com/explore/global-infrastructure/data-residency/).
 
**SKU name in code:** `DataZoneBatch`

Data zone batch deployments provide all the same functionality as [global batch deployments](./batch.md) while allowing you to leverage Azure global infrastructure to dynamically route traffic to only data centers within the Microsoft defined data zone with the best availability for each request. 

## Standard

**SKU name in code:** `Standard`

Standard deployments provide a pay-per-call billing model on the chosen model. Provides the fastest way to get started as you only pay for what you consume. Models available in each region as well as throughput may be limited.  

Standard deployments are optimized for low to medium volume workloads with high burstiness. Customers with high consistent volume may experience greater latency variability.

## Provisioned

**SKU name in code:** `ProvisionedManaged`

Provisioned deployments allow you to specify the amount of throughput you require in a deployment. The service then allocates the necessary model processing capacity and ensures it's ready for you. Throughput is defined in terms of provisioned throughput units (PTU) which is a normalized way of representing the throughput for your deployment. Each model-version pair requires different amounts of PTU to deploy and provide different amounts of throughput per PTU. Learn more from our [Provisioned throughput concepts article](../concepts/provisioned-throughput.md).

### How to disable access to global deployments in your subscription

Azure Policy helps to enforce organizational standards and to assess compliance at-scale. Through its compliance dashboard, it provides an aggregated view to evaluate the overall state of the environment, with the ability to drill down to the per-resource, per-policy granularity. It also helps to bring your resources to compliance through bulk remediation for existing resources and automatic remediation for new resources. [Learn more about Azure Policy and specific built-in controls for AI services](/azure/ai-services/security-controls-policy).

You can use the following policy to disable access to any Azure OpenAI deployment type. To disable access to a specific deployment type, replace `GlobalStandard` with the sku name for the deployment type that you would like to disable access to. 

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
> Data stored at rest remains in the designated Azure geography, while data may be processed for inferencing in any Azure OpenAI location. [Learn more about data residency](https://azure.microsoft.com/explore/global-infrastructure/data-residency/).

**SKU name in code:** `Developer`

Fine-tuned models support a Developer deployment specifically designed to support custom model evaluation. It offers no data residency guarantees nor does it offer an SLA. To learn more about using the Developer deployment type, see the [fine-tuning guide](./fine-tune-test.md).

## Deploy models

:::image type="content" source="../media/deployment-types/deploy-models-new.png" alt-text="Screenshot that shows the model deployment dialog in Azure AI Foundry portal with three deployment types highlighted.":::

To learn about creating resources and deploying models refer to the [resource creation guide](./create-resource.md).


## See also

- [Quotas & limits](./quota.md)
- [Provisioned throughput units (PTU) onboarding](./provisioned-throughput-onboarding.md)
- [Provisioned throughput units (PTU) getting started](./provisioned-get-started.md)
