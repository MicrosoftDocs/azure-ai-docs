---
title: Understanding deployment types in Azure AI Foundry Models
titleSuffix: Azure AI Foundry
description: Learn how to use deployment types in Azure AI model deployments
author: santiagxf
manager: nitinme
ms.service: azure-ai-model-inference
ms.topic: how-to
ms.date: 05/19/2025
ms.author: fasantia
ms.custom: ignite-2024, github-universe-2024
---

# Deployment types in Azure AI Foundry Models

Azure AI Foundry Models makes models available using the *model deployment* concept in Azure AI Foundry Services (formerly known Azure AI Services). *Model deployments* are also Azure resources and, when created, they give access to a given model under certain configurations. Such configuration includes the infrastructure require to process the requests. 

Azure AI Foundry Models provides customers with choices on the hosting structure that fits their business and usage patterns. Those options are translated to different deployments types (or SKUs) that are available at model deployment time in the Azure AI Foundry resource.

:::image type="content" source="../media/add-model-deployments/models-deploy-deployment-type.png" alt-text="Screenshot showing how to customize the deployment type for a given model deployment." lightbox="../media/add-model-deployments/models-deploy-deployment-type.png":::

**Different model providers offer different deployments types** that you can select from. When selecting a deployment type, consider your **data residency needs** and **call volume/capacity** requirements.


## Global standard

> [!IMPORTANT]
> Data stored at rest remains in the designated Azure geography, while data may be processed for inferencing in any Azure AI Foundry location. [Learn more about data residency](https://azure.microsoft.com/explore/global-infrastructure/data-residency/).

**SKU name in code:** `GlobalStandard`

Global deployments are available in the same Azure AI Foundry Services as non-global deployment types but allow you to leverage Azure's global infrastructure to dynamically route traffic to the data center with best availability for each request.  Global standard provides the highest default quota and eliminates the need to load balance across multiple resources.  

Customers with high consistent volume may experience greater latency variability. The threshold is set per model. See the [quotas page to learn more](../quotas-limits.md).  For applications that require the lower latency variance at large workload usage, we recommend purchasing provisioned throughput.

## Global provisioned

> [!IMPORTANT]
> Data stored at rest remains in the designated Azure geography, while data may be processed for inferencing in any Azure AI Foundry location. [Learn more about data residency](https://azure.microsoft.com/explore/global-infrastructure/data-residency/).

**SKU name in code:** `GlobalProvisionedManaged`

Global deployments are available in the same Azure AI Foundry Services as non-global deployment types but allow you to leverage Azure's global infrastructure to dynamically route traffic to the data center with best availability for each request. Global provisioned deployments provide reserved model processing capacity for high and predictable throughput using Azure global infrastructure.  

## Global batch

> [!IMPORTANT]
> Data stored at rest remains in the designated Azure geography, while data may be processed for inferencing in any Azure AI Foundry location. [Learn more about data residency](https://azure.microsoft.com/explore/global-infrastructure/data-residency/).

Global batch is designed to handle large-scale and high-volume processing tasks efficiently. Process asynchronous groups of requests with separate quota, with 24-hour target turnaround, at [50% less cost than global standard](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/). With batch processing, rather than send one request at a time you send a large number of requests in a single file. Global batch requests have a separate enqueued token quota avoiding any disruption of your online workloads.  

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
> Data stored at rest remains in the designated Azure geography, while data may be processed for inferencing in any Azure AI Foundry location within the Microsoft specified data zone. [Learn more about data residency](https://azure.microsoft.com/explore/global-infrastructure/data-residency/).

**SKU name in code:** `DataZoneStandard`

Data zone standard deployments are available in the same Azure AI Foundry resource as all other AI Foundry Models deployment types but allow you to leverage Azure global infrastructure to dynamically route traffic to the data center within the Microsoft defined data zone with the best availability for each request. Data zone standard provides higher default quotas than our Azure geography-based deployment types. 

Customers with high consistent volume may experience greater latency variability. The threshold is set per model. See the [Quotas and limits](/azure/ai-services/openai/quotas-limits#usage-tiers) page to learn more. For workloads that require low latency variance at large volume, we recommend leveraging the provisioned deployment offerings. 

## Data zone provisioned

> [!IMPORTANT]
> Data stored at rest remains in the designated Azure geography, while data may be processed for inferencing in any Azure AI Foundry location within the Microsoft specified data zone.[Learn more about data residency](https://azure.microsoft.com/explore/global-infrastructure/data-residency/).

**SKU name in code:** `DataZoneProvisionedManaged`

Data zone provisioned deployments are available in the same Azure AI Foundry resource as all other AI Foundry Models deployment types but allow you to leverage Azure global infrastructure to dynamically route traffic to the data center within the Microsoft specified data zone with the best availability for each request. Data zone provisioned deployments provide reserved model processing capacity for high and predictable throughput using Azure infrastructure within the Microsoft specified data zone.  

## Data zone batch

> [!IMPORTANT]
> Data stored at rest remains in the designated Azure geography, while data may be processed for inferencing in any Azure AI Foundry location within the Microsoft specified data zone. [Learn more about data residency](https://azure.microsoft.com/explore/global-infrastructure/data-residency/).
 
**SKU name in code:** `DataZoneBatch`

Data zone batch deployments provide all the same functionality as global batch deployments while allowing you to leverage Azure global infrastructure to dynamically route traffic to only data centers within the Microsoft defined data zone with the best availability for each request. 

## Standard

**SKU name in code:** `Standard`

Standard deployments provide a pay-per-call billing model on the chosen model. Provides the fastest way to get started as you only pay for what you consume. Models available in each region as well as throughput may be limited.  

Standard deployments are optimized for low to medium volume workloads with high burstiness. Customers with high consistent volume may experience greater latency variability.

## Provisioned

**SKU name in code:** `ProvisionedManaged`

Provisioned deployments allow you to specify the amount of throughput you require in a deployment. The service then allocates the necessary model processing capacity and ensures it's ready for you. Throughput is defined in terms of provisioned throughput units (PTU) which is a normalized way of representing the throughput for your deployment. Each model-version pair requires different amounts of PTU to deploy and provide different amounts of throughput per PTU. Learn more from our [Provisioned throughput concepts article](/azure/ai-services/openai/concepts/provisioned-throughput).


## Control deployment options

Administrators can control which model deployment types are available to their users by using Azure Policies. Learn more about [How to control AI model deployment with custom policies](../../../ai-studio/how-to/custom-policy-model-deployment.md).

## Related content

- [Quotas & limits](../quotas-limits.md)
- [Data privacy, and security for Azure AI Foundry Models](../../how-to/concept-data-privacy.md)
