---
title: Migrate semantic ranking code 
titleSuffix: Azure AI Search
description: Migrate semantic ranking code from preview to stable versions, and now to newer preview versions.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: how-to
ms.date: 12/17/2025
ms.update-cycle: 365-days
---

# Migrate semantic ranking code from previous versions

If your semantic ranking code was written against early preview APIs, this article identifies the code changes necessary for migrating to newer API versions. Breaking changes for semantic ranker are limited to query logic in recent APIs, but if your code was written against the initial preview version, you might need to change your semantic configuration as well.

## Breaking changes

There are two breaking changes for semantic ranker across REST API versions:

+ `searchFields` was replaced by `semanticConfiguration` in 2021-04-30-preview
+ `queryLanguage` was ignored starting in 2023-07-01-preview, but reinstated for query rewrite in 2024-11-01-preview

Other version-specific updates pertain to new capabilities, but don't break existing code and are therefore not breaking changes.

If you're using Azure SDKs, multiple APIs have been renamed over time. The SDK change logs provide the details.

## API versions providing semantic ranking

Check your code for the REST API version or SDK package version to confirm which one provides semantic ranking. The following API versions have some level of support for semantic ranking.

| Release&nbsp;type | REST&nbsp;API&nbsp;version | Semantic ranker updates |
|--|--|--|
| initial | [2020-06-30-preview](/rest/api/searchservice/preview-api/search-documents) | Adds `queryType=semantic` to Search Documents |
| preview | [2021-04-30-preview](/rest/api/searchservice/preview-api/search-documents)  | Adds `semanticConfiguration` to Create or Update Index |
| preview | [2023-07-01-preview](/rest/api/searchservice/preview-api/search-documents) | Updates `semanticConfiguration`. Starting on July 14, 2023 updates to the Microsoft-hosted semantic models made semantic ranker language-agnostic, effectively decommissioning the `queryLanguage` property for semantic ranking. There's no breaking change in code, but the property is ignored. Customers were advised to remove this property from code.|
| preview | [2023-10-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2023-10-01-preview&preserve-view=true) | Adds `semanticQuery` to send a query used only for reranking purposes. |
| stable | [2023-11-01](/rest/api/searchservice/operation-groups?view=rest-searchservice-2023-11-01&preserve-view=true) | Generally available. Introduced changes to `semanticConfiguration` that progressed to the stable version. If your code targets this version or later, it's compatible with newer API versions unless you adopt new preview features.|
| preview | [2024-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2024-05-01-preview&preserve-view=true) | No change |
| stable | [2024-07-01](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2024-07-01&preserve-view=true) | No change |
| preview | [2024-09-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2024-09-01-preview&preserve-view=true) | No change |
| preview | [2024-11-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2024-11-01-preview&preserve-view=true) | Adds query rewrite. The `queryLanguage` property is now required if you use [query rewrite (preview)](semantic-how-to-query-rewrite.md).  |
| preview | [2025-03-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-03-01-preview&preserve-view=true) | Adds opt-in to prerelease versions of semantic models. |
| preview | [2025-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-05-01-preview&preserve-view=true) | No API updates in this preview, but semantic ranking now has [better integration with scoring profiles](semantic-how-to-enable-scoring-profiles.md). |
| preview | [2025-08-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-08-01-preview&preserve-view=true) | No change |
| preview | [2025-11-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) | Available on free tiers. |

## Change logs for Azure SDKs

To determine which semantic features are available in a specific Azure SDK package and whether any APIs have been renamed, see the SDK's change log:

+ [Azure SDK for .NET change log](https://github.com/Azure/azure-sdk-for-net/blob/Azure.Search.Documents_11.5.1/sdk/search/Azure.Search.Documents/CHANGELOG.md#1150-2023-11-10&preserve-view=true)
+ [Azure SDK for Python change log](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md#1140-2023-10-13&preserve-view=true)
+ [Azure SDK for Java change log](https://github.com/Azure/azure-sdk-for-java/blob/azure-search-documents_11.6.1/sdk/search/azure-search-documents/CHANGELOG.md#1160-2023-11-13&preserve-view=true)
+ [Azure SDK for JavaScript change log](https://github.com/Azure/azure-sdk-for-js/blob/%40azure/search-documents_12.0.0/sdk/search/search-documents/CHANGELOG.md#1200-2023-11-13&preserve-view=true)

## 2024-11-01-preview

+ Adds [query rewrite](semantic-how-to-query-rewrite.md) to Search Documents.
+ Requires `queryLanguage` for query rewrite workloads. For a list of valid values, see the [REST API](/rest/api/searchservice/documents/search-post?view=rest-searchservice-2024-11-01-preview#querylanguage&preserve-view=true).

## 2024-09-01-preview

No changes to semantic ranking syntax from the 2024-07-01 stable version.

## 2024-07-01

No changes to semantic ranking syntax from the 2024-05-01-preview version.

Don't use this API version. It implements a vector query syntax that's incompatible with any newer API version.

## 2024-05-01-preview

No changes to semantic ranking syntax from the 2024-03-01-preview version.

## 2024-03-01-preview

No changes to semantic ranking syntax from the 2023-10-01-preview version, but vector queries are introduced. Semantic ranking now applies to responses from hybrid and vector queries. You can apply reranking on any human-readable text fields in the response, assuming the fields are listed in `prioritizedFields`.

## 2023-11-01

+ Excludes `SemanticDebug` and `semanticQuery`, otherwise the same as the 2023-10-01-preview version.

## 2023-10-01-preview

+ Adds `semanticQuery`

## 2023-07-01-preview

+ Adds `semanticErrorHandling`, `semanticMaxWaitInMilliseconds`.
+ Adds numerous semantic-related fields to the response, such as `SemanticDebug` and `SemanticErrorMode`.
+ Ignores `queryLanguage`, it's no longer used in semantic ranking.

Starting on July 14, 2023, semantic ranker is language agnostic. In preview versions, semantic ranking would deprioritize results differing from the `querylanguage` specified by the field analyzer. However, the `queryLanguage` property is still applicable to [spell correction](speller-how-to-add.md) and the short list of languages supported by that feature.

## 2021-04-30-preview

+ Semantic support is through [Search Documents](/rest/api/searchservice/preview-api/search-documents) and [Create or Update Index](/rest/api/searchservice/preview-api/create-or-update-index) preview API calls.
+ Adds `semanticConfiguration` to a search index. A semantic configuration has a name and a prioritized field list.
+ Adds ``prioritizedFields`.

The `searchFields` property is no longer used to prioritize fields. In all versions moving forward, `semanticConfiguration.prioritizedFields` replaces `searchFields` as the mechanism for specifying which fields to use for L2 ranking.

## 2020-06-30-preview

+ Semantic support is through a [Search Documents](/rest/api/searchservice/preview-api/search-documents) preview API call.
+ Adds `queryType=semantic` to the query request.
+ Adapts `searchFields` so that if the query type is semantic, the `searchFields` property determines the priority order of field inputs to the semantic ranker.
+ Adds `captions`, `answers`, and `highlights` to the query response.

## Next steps

Test your semantic configuration migration by running a semantic query.

> [!div class="nextstepaction"]
> [Create a semantic query](semantic-how-to-query-request.md)
