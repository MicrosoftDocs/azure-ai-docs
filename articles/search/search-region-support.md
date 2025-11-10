---
title: Supported Regions
titleSuffix: Azure AI Search
description: Learn about the regions that offer Azure AI Search and the features available in each region.
author: haileytap
ms.author: haileytapia
manager: nitinme
ms.date: 10/30/2025
ms.service: azure-ai-search
ms.topic: conceptual
ms.custom:
  - references_regions
  - build-2025
---

# Azure AI Search regions list

This article identifies the cloud regions in which Azure AI Search is available. It also lists which premium features are available in each region.

## Features subject to regional availability

When you create an Azure AI Search service, your region selection might depend on features that are only available in certain regions. The following table lists those region-specific features.

| Feature | Description | Availability |
|---------|-------------|--------------|
| [AI enrichment](cognitive-search-concept-intro.md) | Refers to [built-in skills](cognitive-search-predefined-skills.md) that make internal calls to Azure AI for enrichment and transformation during indexing. Integration requires that Azure AI Search coexists with an [Azure AI services multi-service account](/azure/ai-services/multi-service-resource#azure-ai-services-resource-for-azure-ai-search-skills) in the same physical region. You can bypass region requirements by using [identity-based connections](cognitive-search-attach-cognitive-services.md#bill-through-a-keyless-connection), currently in public preview. | Regional support is noted in this article. |
| [Availability zones](/azure/reliability/reliability-ai-search#availability-zone-support) | Divides a region's data centers into distinct physical location groups, providing high availability within the same geo. | Regional support is noted in this article. |
| [Agentic retrieval](agentic-retrieval-overview.md) | Takes a dependency on semantic ranker, which is another premium feature. | Regional support is noted in this article. |
| [Confidential computing](search-security-overview.md#data-in-use) | Deploys your search service on confidential VMs to process data in a hardware-based trusted execution environment.<p>Confidential computing disables or restricts certain features, including agentic retrieval, semantic ranker, query rewrite, and skillset execution. | Regional support is noted in this article. |
| [Semantic ranker](semantic-search-overview.md) | Takes a dependency on Microsoft-hosted models in specific regions. | Regional support is noted in this article. |
| [Query rewrite](semantic-how-to-query-rewrite.md) | Takes a dependency on Microsoft-hosted models in specific regions. | Regional support is noted in this article. |
| [Extra capacity](search-limits-quotas-capacity.md#service-limits) | Higher-capacity partitions became available in select regions starting in April 2024, with a second wave following in May 2024. Currently, there are just a few regions that *don't* offer higher-capacity partitions.<p>If you have an older search service in a supported region, check if you can [upgrade your service](search-how-to-upgrade.md). Otherwise, create a new search service to benefit from more capacity at the same billing rate. | Regional support is noted in the footnotes of this article. |
| Capacity constraints | In some regions, insufficient capacity prevents you from creating search services on certain tiers. The Azure portal automatically hides regions and tiers that aren't available for new deployments. | Regional support is noted in the footnotes of this article. |
| [Azure AI Vision 4.0 multimodal APIs](search-get-started-portal-image-search.md) | Refers to the Azure AI Vision multimodal embeddings skill and vectorizer that call the multimodal embedding API. | Check the [Azure AI Vision region list](/azure/ai-services/computer-vision/overview-image-analysis#region-availability) first, and then verify Azure AI Search is available in the same region.|

## Azure Public regions

You can create an Azure AI Search service in any of the following Azure public regions. Almost all of these regions support [higher-capacity tiers](search-limits-quotas-capacity.md#service-limits). Exceptions are noted where they apply.

### Americas

| Region | AI enrichment | Availability zones | Agentic retrieval | Confidential computing | Semantic ranker | Query rewrite |
|--|--|--|--|--|--|--|
| Brazil South​​ ​| ✅ |  | ✅ | ✅ | ✅ | ✅ |
| Canada Central​​ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Canada East​​ ​|  |  | ✅ |  | ✅ |  |
| ​Central US​​ | ✅ | ✅ | ✅ |  | ✅ | ✅ |
| East US​ | ✅ | ✅ | ✅ |  | ✅ |  |
| East US 2 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Mexico Central |  | ✅ |  |  |  |  |
| North Central US​ ​| ✅ |  | ✅ |  | ✅ | ✅ |
| South Central US​ | ✅ | ✅ | ✅ |  | ✅ | ✅ |
| West US​​ | ✅ |  | ✅ |  | ✅ | ✅ |
| West US 2​ ​| ✅ | ✅ | ✅ |  | ✅ | ✅ |
| West US 3​ | ✅ | ✅ | ✅ |  | ✅ | ✅ |
| West Central US​ ​ | ✅ |  | ✅ |  | ✅ |  |

### Europe

| Region | AI enrichment | Availability zones | Agentic retrieval | Confidential computing | Semantic ranker | Query rewrite |
|--|--|--|--|--|--|--|
| France Central​​ | ✅ | ✅ | ✅ |  | ✅ | ✅ |
| Germany West Central​ ​| ✅ | ✅ | ✅ |  | ✅ |  |
| Italy North​​ |  | ✅ | ✅ | ✅ | ✅ |  |
| Norway East​​ | ✅ | ✅ |  | ✅ |  |  |
| North Europe​​ | ✅ | ✅ | ✅ |  | ✅ | ✅ |
| Poland Central​​ |  |  | ✅ |  | ✅ |  |
| Spain Central <sup>1</sup> |  | ✅ |  | ✅ | ✅ | ✅ |
| Sweden Central​​ | ✅ | ✅ | ✅ |  | ✅ | ✅ |
| Switzerland North​ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Switzerland West​ | ✅ | ✅ | ✅ |  | ✅ |  |
| UK South​ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| UK West​ ​|  |  | ✅ |  | ✅ |  |
| West Europe​​ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

<sup>1</sup> [Higher storage limits](search-limits-quotas-capacity.md#service-limits) aren't available in this region. If you want higher limits, choose a different region.

### Middle East

| Region | AI enrichment | Availability zones | Agentic retrieval | Confidential computing | Semantic ranker | Query rewrite |
|--|--|--|--|--|--|--|
| Israel Central​ <sup>1</sup> |  | ✅ |  |  |  |  |
| Qatar Central​ <sup>1</sup> |  | ✅ | ✅ |  | ✅ |  |
| UAE North​​ | ✅ | ✅ | ✅ | ✅ | ✅ |  |

<sup>1</sup> [Higher storage limits](search-limits-quotas-capacity.md#service-limits) aren't available in this region. If you want higher limits, choose a different region.

### Africa

| Region | AI enrichment | Availability zones | Agentic retrieval | Confidential computing | Semantic ranker | Query rewrite |
|--|--|--|--|--|--|--|
| South Africa North​ | ✅ | ✅ | ✅ | ✅ | ✅ |  |

### Asia Pacific

| Region | AI enrichment | Availability zones | Agentic retrieval | Confidential computing | Semantic ranker | Query rewrite |
|--|--|--|--|--|--|--|
| Australia East​ ​| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Australia Southeast​​​ |  |  | ✅ |  | ✅ |  |
| Central India | ✅ | ✅ | ✅ |  | ✅ | ✅ |
| East Asia​ | ✅ | ✅ | ✅ |  | ✅ | ✅ |
| Indonesia Central |  | ✅ |  |  |  |  |
| Jio India West​​ | ✅ |  | ✅ |  | ✅ | ✅ |
| Jio India Central​​ |  |  |  |  |  |  |
| Japan East | ✅ | ✅ | ✅ |  | ✅ | ✅ |
| Japan West​ | ✅ |  | ✅ |  | ✅ |  |
| Korea Central | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Korea South​​ |  |  | ✅ |  | ✅ |  |
| Malaysia West |  | ✅ |  |  |  |  |
| New Zealand North |  | ✅ |  |  |  |  |
| South India |  | ✅ |  |  |  |  |
| Southeast Asia​​ | ✅ | ✅ | ✅ |  | ✅ | ✅ |

## Azure Government regions

| Region | AI enrichment | Availability zones | Agentic retrieval | Confidential computing | Semantic ranker | Query rewrite |
|--|--|--|--|--|--|--|
| Arizona | ✅ |  | ✅ |  | ✅ | ✅ |
| Texas |  |  |  |  |  |  |
| Virginia | ✅ | ✅ | ✅ |  | ✅ | ✅ |

## Azure operated by 21Vianet

| Region | AI enrichment <sup>1</sup> | Availability zones | Agentic retrieval | Confidential computing | Semantic ranker | Query rewrite |
|--|--|--|--|--|--|--|
| China East |  |  |  |  |  |  |
| China East 2 <sup>2</sup> | ✅ |  |  |  |  |  |
| China East 3 |  |  |  |  |  |  |
| China North |  |  |  |  |  |  |
| China North 2 <sup>2</sup> |  |  |  |  |  |  |
| China North 3 |  | ✅ | ✅ |  | ✅ | ✅ |

<sup>1</sup> Only China East 2 fully supports AI enrichment. In other 21Vianet regions, you can use skillsets with the [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md) for integrated vectorization, which depends on the availability of Azure OpenAI and Azure AI Search in your region. Otherwise, AI enrichment isn't supported.

<sup>2</sup> [Higher storage limits](search-limits-quotas-capacity.md#service-limits) aren't available in this region. If you want higher limits, choose a different region.

## Related content

- [Azure AI Vision region list](/azure/ai-services/computer-vision/overview-image-analysis#region-availability)
- [Availability zone region availability](/azure/reliability/availability-zones-region-support)
- [Azure product by region page](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/?products=search)
