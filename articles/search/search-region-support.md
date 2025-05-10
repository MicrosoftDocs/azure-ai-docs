---
title: Supported Regions
titleSuffix: Azure AI Search
description: Shows supported regions and feature availability across regions for Azure AI Search.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: conceptual
ms.custom: references_regions
ms.date: 04/14/2025

---

# Azure AI Search regions list

This article identifies the cloud regions in which Azure AI Search is available. It also lists which premium features are available in each region.

## Features subject to regional availability

Some features take a dependency on other Azure services or infrastructure that are subject to regional availability. If you need a specific feature, make sure it's available in the desired region.

| Feature | Description | Availability |
|---------|-------------|--------------|
| [Extra capacity](search-limits-quotas-capacity.md#service-limits) | Higher capacity partitions became available in select regions starting in April 2024, with a second wave following in May 2024. Currently, there are just a few regions that *don't* offer higher capacity partitions. If you have an older search service in a supported region, check if you can [upgrade your service](search-how-to-upgrade.md). Otherwise, create a new search service to benefit from more capacity at the same billing rate. |  Regional support for extra capacity is noted in the footnotes of this article. <p>Check your [service age](search-how-to-upgrade.md#check-your-service-creation-or-upgrade-date) to see if your search service was created after high capacity partitions became available. <p>To check the capacity of an existing service, [find your search service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices) and select the **Properties** tab in the middle of the **Overview** page.|
| [Availability zones](search-reliability.md#availability-zone-support) | Divides a region's data centers into distinct physical location groups, providing high availability within the same geo. | Regional support is noted in this article. |
| [Semantic ranker](semantic-search-overview.md) | Takes a dependency on Microsoft-hosted models in specific regions. | Regional support is noted in this article. |
| [Query rewrite](semantic-how-to-query-rewrite.md) | Takes a dependency on Microsoft-hosted models in specific regions. | Regional support is noted in this article. |
| [AI enrichment](cognitive-search-concept-intro.md) | Refers to [built-in skills](cognitive-search-predefined-skills.md) that make internal calls to Azure AI for enrichment and transformation during indexing. Integration requires that Azure AI Search coexists with an [Azure AI services multi-service account](/azure/ai-services/multi-service-resource#azure-ai-services-resource-for-azure-ai-search-skills) in the same physical region. You can bypass region requirements if you use [identity-based connections](cognitive-search-attach-cognitive-services.md#bill-through-a-keyless-connection), currently in public preview. | Regional support is noted in this article. |
| [Azure OpenAI integration](vector-search-integrated-vectorization.md)  | Refers to the AzureOpenAIEmbedding skill and vectorizer that make internal calls to deployed embedding models on Azure OpenAI. | Check [Azure OpenAI model region availability](/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability) for the most current list of regions for each embedding and chat model. Specific Azure OpenAI models are in fewer regions, so check for model availability first, and then verify Azure AI Search is available in the same region.|
| [Azure AI Foundry integration](vector-search-integrated-vectorization-ai-studio.md) | Refers to skills and vectorizers that make internal calls to the models hosted in the model catalog. | Check [Azure AI Foundry region availability](/azure/ai-foundry/reference/region-support) for the most current list of regions. |
| [Azure AI Vision 4.0 multimodal APIs](search-get-started-portal-image-search.md) | Refers to the Azure AI Vision multimodal embeddings skill and vectorizer that call the multimodal embedding API. | Check the [Azure AI Vision region list](/azure/ai-services/computer-vision/overview-image-analysis#region-availability) first, and then verify Azure AI Search is available in the same region.|

## Azure Public regions

You can create an Azure AI Search resource in any of the following Azure public regions. Almost all of these regions support [higher capacity tiers](search-limits-quotas-capacity.md#service-limits). Exceptions are noted where they apply.

AI enrichment refers to internal connections to an Azure AI services multi-service account and doesn't include Azure OpenAI integration.

### Americas

| Region | AI enrichment | Availability zones | Semantic ranker | Query rewrite |
|--|--|--|--|--|
| Brazil South​​ ​| ✅ |  | ✅ |  |
| Canada Central​​ | ✅ | ✅ | ✅ |  |
| Canada East​​ ​|  |  | ✅ |  |
| ​Central US​​ | ✅ | ✅ | ✅ |  |
| East US​ | ✅ | ✅ | ✅ |  |
| East US 2 ​ | ✅ | ✅ | ✅ |  |
| Mexico Central |  | ✅ |  |  |
| North Central US​ ​| ✅ |  | ✅ |  |
| South Central US​ | ✅ | ✅ | ✅ |  |
| West US​​ | ✅ |  | ✅ |  |
| West US 2​ <sup>1</sup>​| ✅ | ✅ | ✅ |  |
| West US 3​ | ✅ | ✅ | ✅ |  |
| West Central US​ ​ | ✅ |  | ✅ |  |

### Europe

| Region | AI enrichment | Availability zones | Semantic ranker | Query rewrite |
|--|--|--|--|--|
| North Europe​​ | ✅ | ✅ | ✅ | ✅ |
| West Europe​​ | ✅ | ✅ | ✅ |  |
| France Central​​ | ✅ | ✅ | ✅ |  |
| Germany West Central​ ​| ✅ | ✅ |  |  |
| Italy North​​ |  | ✅ |  |  |
| Norway East​​ | ✅ | ✅ |  |  |
| Poland Central​​ |  |  |  |  |
| Spain Central <sup>2</sup> |  | ✅ |  |  |
| Sweden Central​​ | ✅ | ✅ | ✅ | ✅ |
| Switzerland North​ | ✅ | ✅ | ✅ |  |
| Switzerland West​ | ✅ | ✅ | ✅ |  |
| UK South​ | ✅ | ✅ | ✅ |  |
| UK West​ ​|  |  | ✅ |  |

<sup>1</sup> This region has capacity constraints on the following tiers: S2, S3, L1, and L2.

<sup>2</sup> [Higher storage limits](search-limits-quotas-capacity.md#service-limits) aren't available in this region. If you want higher limits, choose a different region.

### Middle East

| Region | AI enrichment | Availability zones | Semantic ranker | Query rewrite |
|--|--|--|--|--|
| Israel Central​ <sup>1</sup> |  | ✅ |  |  |
| Qatar Central​ <sup>1</sup> |  | ✅ |  |  |
| UAE North​​ | ✅ | ✅ |  |  |

<sup>1</sup> [Higher storage limits](search-limits-quotas-capacity.md#service-limits) aren't available in this region. If you want higher limits, choose a different region.

### Africa

| Region | AI enrichment | Availability zones | Semantic ranker | Query rewrite |
|--|--|--|--|--|
| South Africa North​ | ✅ | ✅ |  |  |

### Asia Pacific

| Region | AI enrichment | Availability zones | Semantic ranker | Query rewrite |
|--|--|--|--|--|
| Australia East​ ​| ✅ | ✅ | ✅ |  |
| Australia Southeast​​​ |  |  | ✅ |  |
| East Asia​ | ✅ | ✅ | ✅ |  |
| Southeast Asia​​ | ✅ | ✅ | ✅ | ✅ |
| Central India | ✅ | ✅ | ✅ |  |
| Jio India West​​ | ✅ |  | ✅ |  |
| South India <sup>1</sup> |  | ✅ |  |  |
| Japan East | ✅ | ✅ | ✅ |  |
| Japan West​ | ✅ |  | ✅ |  |
| Korea Central | ✅ | ✅ | ✅ |  |
| Korea South​​ |  |  | ✅ |  |
| Indonesia Central |  | ✅ |  |  |

<sup>1</sup> [Higher storage limits](search-limits-quotas-capacity.md#service-limits) aren't available in this region. If you want higher limits, choose a different region.

## Azure Government regions

| Region | AI enrichment | Availability zones | Semantic ranker | Query rewrite |
|--|--|--|--|--|
| Arizona | ✅ |  | ✅ |  |
| Texas |  |  |  |  |
| Virginia | ✅ | ✅ | ✅ |  |

## Azure operated by 21Vianet

| Region | AI enrichment | Availability zones | Semantic ranker | Query rewrite |
|--|--|--|--|--|
| China East |  |  |  |  |
| China East 2 <sup>1</sup> | ✅ |  |  |  |
| China East 3 |  |  |  |  |
| China North |  |  |  |  |
| China North 2 <sup>1</sup> |  |  |  |  |
| China North 3 |  | ✅ | ✅ |  |

<sup>1</sup> [Higher storage limits](search-limits-quotas-capacity.md#service-limits) aren't available in this region. If you want higher limits, choose a different region.

## See also

- [Azure AI Foundry region availability](/azure/ai-foundry/reference/region-support)
- [Azure OpenAI model region availability](/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability)
- [Azure AI Vision region list](/azure/ai-services/computer-vision/overview-image-analysis#region-availability)
- [Availability zone region availability](/azure/reliability/availability-zones-region-support)
- [Azure product by region page](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/?products=search)
