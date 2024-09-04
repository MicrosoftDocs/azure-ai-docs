---
title: Feature availability across clouds regions
titleSuffix: Azure AI Search
description: Shows supported regions and feature availability across regions for Azure AI Search.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: cognitive-search
ms.topic: conceptual
ms.custom: references_regions
ms.date: 09/03/2024

---

# Azure AI Search feature availability across cloud regions

This article identifies the cloud regions in which Azure AI Search is available. It also lists which premium features are available in each region.

## Features subject to regional availability

| Feature | Availability |
|---------|--------------|
| [Extra capacity](search-limits-quotas-capacity.md#service-limits) | Higher capacity partitions became available in selected regions starting in April 2024 with a second wave following in May 2024. Currently, there are just a few regions that *don't* offer higher capacity partitions. If you're using an older search service, create a new search service to benefit from more capacity at the same billing rate. To check existing capacity, [find your search service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices) and select the **Properties** tab in the middle of the Overview page. To check search service age, follow [these instructions](vector-search-index-size.md#how-to-check-service-creation-date). Regional support for extra capacity is noted in the footnotes of this article.|
| [Availability zones](search-reliability.md#availability-zone-support) | Divides a region's data centers into distinct physical location groups, providing high-availability within the same geo. Regional support is noted in this article. |
| [Azure AI integration](vector-search-integrated-vectorization.md) | Refers to skills and vectorizers that make internal calls to Azure AI and Azure OpenAI. Integration requires that Azure AI Search coexists with an [Azure AI multi-service account](/azure/ai-services/multi-service-resource) in the same physical region. <p>AI Search also integrates with Azure OpenAI. Check [Azure OpenAI model region availability](/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability) for the most current list of regions for each embedding and chat model. Regional support for Azure AI integration is noted in this article. Specific Azure OpenAI models are in fewer regions, so be sure to check before installing.|
| [Azure AI Studio integration](vector-search-integrated-vectorization-ai-studio.md) | Check [Azure AI Studio region availability](/azure/ai-studio/reference/region-support) for the most current list of regions. |
| [Azure AI Vision 4.0 multimodal APIs for image vectorization](search-get-started-portal-image-search.md) | Check the [Azure AI Vision region list for multimodal embeddings](/azure/ai-services/computer-vision/overview-image-analysis#region-availability) support. Be sure to create both your Azure AI multi-service account and Azure AI Search service in one of those supported regions. |
| [Semantic ranking](semantic-search-overview.md) | Takes a dependency on Microsoft-hosted models in specific regions. Regional support is noted in this article. |

<!-- Each cloud region noted in this article includes a column indicating support for the following features.

- [Semantic ranking](semantic-search-overview.md) depends on models hosted in specific regions.
- [AI enrichment](cognitive-search-concept-intro.md) refers to skills and vectorizers that make internal calls to Azure AI and Azure OpenAI. Integration requires that Azure AI Search coexist with an [Azure AI multi-service account](/azure/ai-services/multi-service-resource) in the same physical region.
- [Availability zones](search-reliability.md#availability-zone-support) are an Azure platform capability that divides a region's data centers into distinct physical location groups to provide high-availability, within the same region.

We recommend that you check [Azure AI Studio region availability](/azure/ai-studio/reference/region-support) and [Azure OpenAI model region availability](/azure/reliability/availability-zones-service-support#azure-regions-with-availability-zone-support) for the most current list of regions for those features. 

Also, if you plan to use Azure AI Vision 4.0 multimodal APIs for image vectorization, it's available in a reduced list of regions. [Check the Azure AI Vision region list for multimodal embeddings](/azure/ai-services/computer-vision/overview-image-analysis#region-availability) and be sure to create both your Azure AI multi-service account and Azure AI Search service in one of those supported regions.

> [!NOTE]
> Higher capacity partitions became available in selected regions starting in April 2024. A second wave of higher capacity partitions released in May 2024. Currently, there are just a few regions that *don't* offer higher capacity patitions, and those are indicated in footnotes.
>
> If you're using an older search service, consider creating a new search service in a supported region to benefit from more capacity at the same billing rate as before. For more information, see [Service limits](search-limits-quotas-capacity.md#service-limits) and [How to check service creation date](vector-search-index-size.md#how-to-check-service-creation-date). -->

## Azure Public regions

You can create an Azure AI Search resource in any of the following Azure public regions. Almost all of these regions support [higher capacity tiers](search-limits-quotas-capacity.md#service-limits). Exceptions are noted where they apply.

### Americas

| Region | AI integration | Semantic ranking | Availability zones |
|--|--|--|--|
| Brazil South​​ ​ | ✅ | ✅ | |
| Canada Central​​ | ✅ | ✅ | ✅ |
| Canada East​​ ​ |  | ✅ | |
| East US​ | ✅ | ✅ | ✅ |
| East US 2 ​ | ✅ | ✅ | ✅ |
| ​Central US​ <sup>1</sup>​ | ✅ | ✅ | ✅ |
| North Central US​ ​ | ✅ | ✅ | |
| South Central US​ <sup>1</sup>​ | ✅ | ✅ | ✅ |
| West US​ ​ | ✅ | ✅ | |
| West US 2​ <sup>1</sup>​ | ✅ | ✅ | ✅ |
| West US 3​ <sup>1</sup>​ | ✅ | ✅ |✅ |
| West Central US​ ​ | ✅ | ✅ | |

<sup>1</sup> Currently, this region is at capacity for Basic and Standard (S1) tiers. Choose a higher tier or a different region.

### Europe

| Region | AI integration | Semantic ranking | Availability zones |
|--|--|--|--|
| North Europe​​ <sup>1</sup>| ✅ | ✅ | ✅ |
| West Europe​​ <sup>2</sup>| ✅ | ✅ | ✅ |
| France Central​​ | ✅ | ✅ | ✅ |
| Germany West Central​ ​| ✅ |  | ✅ |
| Italy North​​ |  |  | ✅ |
| Norway East​​ | ✅ |  | ✅ |
| Poland Central​​ |  |  |  |
| Spain Central |  |  | ✅  |
| Sweden Central​​ | ✅ |  | ✅ |
| Switzerland North​ | ✅ | ✅ | ✅ |
| Switzerland West​ | ✅ | ✅ | ✅ |
| UK South​ | ✅ | ✅ | ✅ |
| UK West​ ​|  | ✅ | |

<sup>1</sup> Currently, this region is at capacity for Basic and Standard (S1) tiers. Choose a higher tier or a different region.

<sup>2</sup> West Europe is at capacity for all tiers and isn't accepting any new search services. Additionally, the clusters used to run Azure AI Search don't have the [higher capacity partitions](search-limits-quotas-capacity.md#service-limits) that were brought online in April 2024. This means that search services deployed in this region have lower storage and computing capability.

### Middle East

| Region | AI integration | Semantic ranking | Availability zones |
|--|--|--|--|
| Israel Central​ <sup>2</sup> |  |  | ✅  |
| Qatar Central​ <sup>1, 2</sup> |  |  | ✅ |
| UAE North​​ | ✅ |  | ✅ |

<sup>1</sup> Currently, this region is at capacity for Basic and Standard (S1) tiers. Choose a higher tier or a different region.

<sup>2</sup> These regions run on older infrastructure that has lower capacity per partition at every tier. Choose a different region if you want [higher capacity](search-limits-quotas-capacity.md#service-limits).

### Africa

| Region | AI integration | Semantic ranking | Availability zones |
|--|--|--|--|
| South Africa North​ | ✅ |  | ✅ |

### Asia Pacific

| Region | AI integration | Semantic ranking | Availability zones |
|--|--|--|--|
| Australia East​ ​ | ✅ | ✅ | ✅ |
| Australia Southeast​​​ |  | ✅ |  |
| East Asia​ | ✅ | ✅ | ✅ |
| Southeast Asia​ ​ ​ | ✅ | ✅ | ✅ |
| Central India| ✅ | ✅ | ✅ |
| Jio India West​ ​ | ✅ | ✅ |  |
| South India <sup>2</sup> |  | | ✅ |
| Japan East <sup>1</sup> | ✅ | ✅ | ✅ |
| Japan West​ | ✅ | ✅ |  |
| Korea Central | ✅ | ✅ | ✅ |
| Korea South​ ​ |  | ✅ |  |

<sup>1</sup> Currently, this region is at capacity for Basic and Standard (S1) tiers. Choose a higher tier or a different region.

<sup>2</sup> These regions run on older infrastructure that has lower capacity per partition at every tier. Choose a different region if you want [higher capacity](search-limits-quotas-capacity.md#service-limits).

## Azure Government regions

All of these regions support [higher capacity tiers](search-limits-quotas-capacity.md#service-limits). 

None of these regions support Azure [role-based access for data plane operations](search-security-rbac.md). You must use key-based authentication for indexing and query workloads.

| Region | AI integration | Semantic ranking | Availability zones |
|--|--|--|--|
| Arizona | ✅ | ✅  | |
| Texas |  |  |  |
| Virginia | ✅ | ✅  | ✅ |

## Azure operated by 21Vianet

You can install Azure AI Search in any of the following regions. If you need semantic ranking or AI enrichment, choose a region that provides the feature.

| Region | AI integration | Semantic ranking | Availability zones |
|--|--|--|--|
| China East <sup>1</sup> |  |  |  |
| China East 2 <sup>1</sup> | ✅  | | |
| China East 3 |  |  |  |
| China North <sup>1</sup> |  |  | |
| China North 2 <sup>1</sup> |  |  | |
| China North 3 | | ✅ | ✅ |

<sup>1</sup> These regions run on older infrastructure that has lower capacity per partition at every tier. Choose a different region if you want [higher capacity](search-limits-quotas-capacity.md#service-limits).

<!-- ## Early Update Access Program (EUAP)

These regions

| Region | AI enrichment | Semantic ranking | Availability zones |
|--|--|--|--|
| Central US EUAP​ <sup>1</sup> | | ✅ | |
| East US 2 EUAP ​ | | ✅ | |

<sup>1</sup> This region runs on older infrastructure that has lower capacity per partition at every tier. You can't create a search service with [higher capacity](search-limits-quotas-capacity.md#service-limits) in this region. -->

## See also

- [Azure AI Studio region availability](/azure/ai-studio/reference/region-support)
- [Azure OpenAI model region availability](/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability)
- [Availability zone region availability](/azure/reliability/availability-zones-service-support#azure-regions-with-availability-zone-support)
- [Azure product by region page](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/?products=search)