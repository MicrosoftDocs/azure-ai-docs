---
title: Supported regions
titleSuffix: Azure AI Search
description: Shows supported regions and feature availability across regions for Azure AI Search.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: conceptual
ms.custom: references_regions
ms.date: 11/19/2024

---

# Azure AI Search regions list

This article identifies the cloud regions in which Azure AI Search is available. It also lists which premium features are available in each region. 

## Features subject to regional availability

| Feature | Availability |
|---------|--------------|
| [Extra capacity](search-limits-quotas-capacity.md#service-limits) | Higher capacity partitions became available in selected regions starting in April 2024 with a second wave following in May 2024. If you're using an older search service, create a new search service to benefit from more capacity at the same billing rate. To check existing capacity, [find your search service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices) and select the **Properties** tab in the middle of the Overview page. To check search service age, follow [these instructions](vector-search-index-size.md#how-to-check-service-creation-date).  Currently, there are just a few regions that *don't* offer higher capacity partitions. Regional support for extra capacity is noted in the footnotes of this article.|
| [Availability zones](search-reliability.md#availability-zone-support) | Divides a region's data centers into distinct physical location groups, providing high-availability within the same geo. Regional support is noted in this article. |
| [AI service integration](cognitive-search-concept-intro.md) | Refers to skills that make internal calls to Azure AI for enrichment and transformation during indexing. Integration requires that Azure AI Search coexists with an [Azure AI multi-service account](/azure/ai-services/multi-service-resource) in the same physical region. Regional support is noted in this article. |
| [Azure OpenAI integration](vector-search-integrated-vectorization.md)  | Refers to skills and vectorizers that make internal calls to deployed embedding and chat models on Azure OpenAI. Check [Azure OpenAI model region availability](/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability) for the most current list of regions for each embedding and chat model. Specific Azure OpenAI models are in fewer regions, so be sure to check for joint regional availability before installing.|
| [Azure AI Foundry integration](vector-search-integrated-vectorization-ai-studio.md) | Refers to skills and vectorizers that make internal calls to the models hosted in the model catalog. Check [Azure AI Foundry region availability](/azure/ai-studio/reference/region-support) for the most current list of regions. |
| [Azure AI Vision 4.0 multimodal APIs for image vectorization](search-get-started-portal-image-search.md) | Refers to skills and vectorizers that call the multimodal embedding API. Check the [Azure AI Vision region list](/azure/ai-services/computer-vision/overview-image-analysis#region-availability) for joint regional availability. |
| [Semantic ranker](semantic-search-overview.md) | Takes a dependency on Microsoft-hosted models in specific regions. Regional support is noted in this article. |

## Azure Public regions

You can create an Azure AI Search resource in any of the following Azure public regions. Almost all of these regions support [higher capacity tiers](search-limits-quotas-capacity.md#service-limits). Exceptions are noted where they apply.

AI service integration refers to internal connections to an Azure AI multi-service account and doesn't include Azure OpenAI integration.

### Americas

| Region | AI service integration | Semantic ranker | Availability zones | Capacity constrained |
|--|--|--|--|--|
| Brazil South​​ ​ | ✅ | ✅ | |  |
| Canada Central​​ | ✅ | ✅ | ✅ |  |
| Canada East​​ ​ |  | ✅ | |  |
| East US​ | ✅ | ✅ | ✅ |  |
| East US 2 ​ | ✅ | ✅ | ✅ | Basic, S1 |
| ​Central US​​ | ✅ | ✅ | ✅ |  |
| North Central US​ ​ | ✅ | ✅ | |  | 
| South Central US​  | ✅ | ✅ | ✅ | All Tiers |
| West US​ ​ | ✅ | ✅ | |  |
| West US 2​ ​ | ✅ | ✅ | ✅ | |
| West US 3​ | ✅ | ✅ |✅ | Basic, S1 |
| West Central US​ ​ | ✅ | ✅ | | |

### Europe

| Region | AI service integration | Semantic ranker | Availability zones | Capacity constrained |
|--|--|--|--|--|
| North Europe​​ | ✅ | ✅ | ✅ | S2, S3, S3, S3 HD, L1, L2 |
| West Europe​​ <sup>1</sup>| ✅ | ✅ | ✅ | All Tiers |
| France Central​​ | ✅ | ✅ | ✅ | |
| Germany West Central​ <sup>1</sup>​| ✅ |  | ✅ | |
| Italy North​​ |  |  | ✅ | |
| Norway East​​ | ✅ |  | ✅ |  |
| Poland Central​​ |  |  |  |  |
| Spain Central <sup>1</sup> |  |  | ✅  |  |
| Sweden Central​​ | ✅ |  | ✅ |  |
| Switzerland North​ | ✅ | ✅ | ✅ |  |
| Switzerland West​ <sup>1</sup>| ✅ | ✅ | ✅ |  |
| UK South​ | ✅ | ✅ | ✅ |  |
| UK West​ ​|  | ✅ | |  |

<sup>1</sup> This region runs on older infrastructure that has lower storage limits per partition at every tier. Choose a different region if you want [higher limits](search-limits-quotas-capacity.md#service-limits).

### Middle East

| Region | AI service integration | Semantic ranker | Availability zones | Capacity constrained |
|--|--|--|--|--|
| Israel Central​ <sup>1</sup> |  |  | ✅  |  |
| Qatar Central​ <sup>1</sup> |  |  | ✅ | |
| UAE North​​ | ✅ |  | ✅ |  |

<sup>1</sup> This region runs on older infrastructure that has lower storage limits per partition at every tier. Choose a different region if you want [higher limits](search-limits-quotas-capacity.md#service-limits).

### Africa

| Region | AI service integration | Semantic ranker | Availability zones | Capacity constrained |
|--|--|--|--|--|
| South Africa North​ | ✅ |  | ✅ |   |

### Asia Pacific

| Region | AI service integration | Semantic ranker | Availability zones | Capacity constrained |
|--|--|--|--|--|
| Australia East​ ​ | ✅ | ✅ | ✅ |   |
| Australia Southeast​​​ |  | ✅ |  | |
| East Asia​ | ✅ | ✅ | ✅ |  |
| Southeast Asia​ ​ ​ | ✅ | ✅ | ✅ |  |
| Central India | ✅ | ✅ | ✅ |  |
| Jio India West​ ​ | ✅ | ✅ |  |
| South India <sup>1</sup> |  | | ✅ |
| Japan East  | ✅ | ✅ | ✅ |
| Japan West​ | ✅ | ✅ |  |
| Korea Central | ✅ | ✅ | ✅ |
| Korea South​ ​ |  | ✅ |  |

<sup>1</sup> This region runs on older infrastructure that has lower storage limits per partition at every tier. Choose a different region if you want [higher limits](search-limits-quotas-capacity.md#service-limits).

## Azure Government regions

| Region | AI service integration | Semantic ranker | Availability zones | Capacity constrained |
|--|--|--|--|--|
| Arizona | ✅ | ✅  | | |
| Texas |  | ✅ |  | |
| Virginia | ✅ | ✅  | ✅ | All Tiers |

## Azure operated by 21Vianet

| Region | AI service integration | Semantic ranker | Availability zones | Capacity constrained |
|--|--|--|--|--|
| China East |  |  |  |
| China East 2 <sup>1</sup> | ✅  | | | |
| China East 3 |  |  |  | |
| China North |  |  | | |
| China North 2 <sup>1</sup> |  |  | | |
| China North 3 | | ✅ | ✅ | |

<sup>1</sup> This region runs on older infrastructure that has lower storage limits per partition at every tier. Choose a different region if you want [higher limits](search-limits-quotas-capacity.md#service-limits).

## See also

- [Azure AI Foundry region availability](/azure/ai-studio/reference/region-support)
- [Azure OpenAI model region availability](/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability)
- [Azure AI Vision region list](/azure/ai-services/computer-vision/overview-image-analysis#region-availability)
- [Availability zone region availability](/azure/reliability/availability-zones-region-support)
- [Azure product by region page](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/?products=search)
