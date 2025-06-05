---
title: Preview feature list
titleSuffix: Azure AI Search
description: Preview features are released so that customers can provide feedback on their design and utility. This article is a comprehensive list of all features currently in preview.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.custom:
  - build-2024
  - ignite-2024
ms.topic: conceptual
ms.date: 05/15/2025
---

# Preview features in Azure AI Search

This article identifies all data plane and control plane features in public preview. This list is helpful for checking feature status. It also explains how to call a preview REST API.

Preview API versions are cumulative and roll up to the next preview. We recommend always using the latest preview APIs for full access to all preview features.

Preview features are removed from this list if they're retired or transition to general availability. For announcements regarding general availability and retirement, see [Service Updates](https://azure.microsoft.com/updates/?product=search) or [What's New](whats-new.md).

## Data plane preview features

|Feature&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  | Category | Description | Availability  |
|---------|------------------|-------------|---------------|
| [**Agentic retrieval**](search-agentic-retrieval-concept.md) | Query | Create a conversational search experience powered by large language models (LLMs) and your proprietary data. Agentic retrieval breaks down complex user queries into subqueries, runs the subqueries in parallel, and extracts grounding data from documents indexed in Azure AI Search. The output is intended for agents and custom chat solutions. A new [knowledge agent](search-agentic-retrieval-how-to-create.md) object is introduced in this preview. Its [response payload](search-agentic-retrieval-how-to-retrieve.md) is designed for downstream agent and chat model consumption, with full transparency of the query plan and reference data. To get started, see [Quickstart: Agentic retrieval](search-get-started-agentic-retrieval.md). | [Knowledge Agents (preview)](/rest/api/searchservice/knowledge-agents?view=rest-searchservice-2025-05-01-preview&preserve-view=true) and [Knowledge Retrieval (preview)](/rest/api/searchservice/knowledge-retrieval?view=rest-searchservice-2025-05-01-preview&preserve-view=true)|
| [**Multivector support**](vector-search-multi-vector-fields.md) | Indexing | Index multiple child vectors within a single document field. You can now use vector types in nested fields of complex collections, effectively allowing multiple vectors to be associated with a single document.| [Create or Update Index (preview)](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2025-05-01-preview&preserve-view=true). |
| [**Scoring profiles with semantic ranking**](semantic-how-to-enable-scoring-profiles.md) | Relevance | Semantic ranker adds a new field, `@search.rerankerBoostedScore`, to help you maintain consistent relevance and greater control over final ranking outcomes in your search pipeline. | [Create or Update Index (preview)](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2025-05-01-preview&preserve-view=true). |
| [**Logic Apps integration in the portal wizard**](search-how-to-index-logic-apps-indexers.md) | Indexing | Create an automated indexing pipeline that retrieves content using a logic app workflow. Use the [Import and vectorize data wizard](search-get-started-portal-import-vectors.md) in the Azure portal to build an indexing pipeline based on Logic Apps. | Image and vectorize data wizard in the Azure portal. |
| [**Document-level access control**](search-document-level-access-overview.md) | Security | Flow document-level permissions from blobs in Azure Data Lake Storage (ADLS) Gen2 to searchable documents in an index. Queries can now filter results based on user identity for selected data sources. | [Create or Update Index (preview)](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2025-05-01-preview&preserve-view=true). |
| [**GenAI Prompt skill**](cognitive-search-skill-genai-prompt.md) | Skills | A new skill that connects to a large language model (LLM) for information, using a prompt you provide. With this skill, you can populate a searchable field using content from an LLM. A primary use case for this skill is *image verbalization*, using an LLM to describe images and send the description to a searchable field in your index. | [Create or Update Skillset (preview)](/rest/api/searchservice/skillsets/create-or-update?view=rest-searchservice-2025-05-01-preview&preserve-view=true). |
| [**Document Layout skill**](cognitive-search-skill-document-intelligence-layout.md)| Skills | New parameters are available for this skill if you use the 2025-05-01-preview API version or later. The new parameters support image offset metadata that improves the image search experience. | [Create or Update Skillset (preview)](/rest/api/searchservice/skillsets/create-or-update?view=rest-searchservice-2025-05-01-preview&preserve-view=true). |
| [**Index "description" support**](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2025-05-01-preview&preserve-view=true#request-body) | REST | The 2025-05-01-preview API version adds a description to an index. A description is useful in agentic solutions, where the agent reads the description to decide whether to run a query or move on to another index. | [Create or Update Index (preview)](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2025-05-01-preview&preserve-view=true). |
| [**flightingOptIn parameter in a semantic configuration**](semantic-how-to-configure.md#opt-in-for-prerelease-semantic-ranking-models) | Queries| You can opt in to use prerelease semantic ranking models if one is available in a search service region. | [Create or Update Index (preview)](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2025-03-01-preview&preserve-view=true). |
| [**Rescore vector queries over binary embeddings using full precision vectors**](vector-search-how-to-quantization.md#recommended-rescoring-techniques) | Relevance (scoring) | For vector indexes that contain quantized binary embeddings, you can rescore query results using a full precision query vector. The query engine uses the dot product for rescoring, which improves the quality of search results. Set `enableRescoring` and `discardOriginals` to use this feature.| [Create or Update Index (preview)](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2025-03-01-preview&preserve-view=true). |
| [**Facet hierarchies, aggregations, and facet filters**](search-faceted-navigation-examples.md) | Queries| New facet query parameters support nested facets. For numeric facetable fields, you can sum the values of each field. You can also specify filters on a facet to add inclusion or exclusion criteria. | [Search Documents (preview)](/rest/api/searchservice/documents/search-post?view=rest-searchservice-2025-03-01-preview&preserve-view=true). |
| [**Query rewrite in the semantic reranker**](semantic-how-to-query-rewrite.md) | Relevance (scoring) | You can set options on a semantic query to rewrite the query input into a revised or expanded query that generates more relevant results from the L2 ranker. | [Search Documents (preview)](/rest/api/searchservice/documents/search-post?view=rest-searchservice-2024-11-01-preview&preserve-view=true).|
| [**Document Layout skill**](cognitive-search-skill-document-intelligence-layout.md) | Applied AI (skills) | A new skill used to analyze a document for structure and provide [structure-aware chunking](search-how-to-semantic-chunking.md). | [Create or Update Skillset (preview)](/rest/api/searchservice/skillsets/create-or-update?view=rest-searchservice-2024-11-01-preview&preserve-view=true). |
| [**Keyless billing for Azure AI skills processing**](cognitive-search-attach-cognitive-services.md). | Applied AI (skills) | You can now use a managed identity and roles for a keyless connection to Azure AI services for built-in skills processing. This capability removes restrictions for having both search and AI services in the same region.  | [Create or Update Skillset  (preview)](/rest/api/searchservice/skillsets/create-or-update?view=rest-searchservice-2024-11-01-preview&preserve-view=true).|
| [**Markdown parsing mode**](search-how-to-index-markdown-blobs.md) | Indexer data source | With this parsing mode, indexers can generate one-to-one or one-to-many search documents from Markdown files in Azure Storage. | [Create or Update Indexer (preview)](/rest/api/searchservice/indexers/create-or-update?view=rest-searchservice-2024-11-01-preview&preserve-view=true). |
| [**Rescoring options for compressed vectors**](vector-search-how-to-quantization.md) | Relevance (scoring) | You can set options to rescore with original vectors instead of compressed vectors. Applies to HNSW and exhaustive KNN vector algorithms, using binary and scalar compression. | [Create or Update Index (preview)](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2024-09-01-preview&preserve-view=true).|
| [**Lower the dimension requirements for MRL-trained text embedding models on Azure OpenAI**](vector-search-how-to-truncate-dimensions.md) | Index | Text-embedding-3-small and Text-embedding-3-large are trained using Matryoshka Representation Learning (MRL). This allows you to truncate the embedding vectors to fewer dimensions, and adjust the balance between vector index size usage and retrieval quality. A new `truncationDimension` provides the MRL behaviors as an extra parameter in a vector compression configuration. This can only be configured for new vector fields. | [Create or Update Index (preview)](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2024-09-01-preview&preserve-view=true). |
| [**Unpack `@search.score` to view subscores in hybrid search results**](hybrid-search-ranking.md#unpack-a-search-score-into-subscores-preview) | Relevance (scoring) | You can investigate Reciprocal Rank Fusion (RRF) ranked results by viewing the individual query subscores of the final merged and scored result. A new `debug` property unpacks the search score. `QueryResultDocumentSubscores`, `QueryResultDocumentRerankerInput`, and `QueryResultDocumentSemanticField` provide the extra detail. | [Search Documents (preview)](/rest/api/searchservice/documents/search-post?view=rest-searchservice-2024-09-01-preview&preserve-view=true). |
| [**Target filters in a hybrid search to just the vector queries**](hybrid-search-how-to-query.md#hybrid-search-with-filters-targeting-vector-subqueries-preview) | Query | A filter on a hybrid query involves all subqueries on the request, regardless of type. You can override the global filter to scope the filter to a specific subquery. A new `filterOverride` parameter provides the behaviors. | [Search Documents (preview)](/rest/api/searchservice/documents/search-post?view=rest-searchservice-2024-09-01-preview&preserve-view=true). |
| [**Text Split skill (token chunking)**](cognitive-search-skill-textsplit.md) | Applied AI (skills) | This skill has new parameters that improve data chunking for embedding models. A new `unit` parameter lets you specify token chunking. You can now chunk by token length, setting the length to a value that makes sense for your embedding model. You can also specify the tokenizer and any tokens that shouldn't be split during data chunking. | [Create or Update Skillset (preview)](/rest/api/searchservice/skillsets/create-or-update?view=rest-searchservice-2024-09-01-preview&preserve-view=true). |
| [**Azure AI Vision multimodal embedding skill**](cognitive-search-skill-vision-vectorize.md) | Applied AI (skills) | A new skill type that calls Azure AI Vision multimodal API to generate embeddings for text or images during indexing. | [Create or Update Skillset (preview)](/rest/api/searchservice/skillsets/create-or-update?view=rest-searchservice-2024-05-01-preview&preserve-view=true). |
| [**Azure Machine Learning (AML) skill**](cognitive-search-aml-skill.md) | Applied AI (skills) | AML skill integrates an inferencing endpoint from Azure Machine Learning. In previous preview APIs, it supports connections to deployed custom models in an AML workspace. Starting in the 2024-05-01-preview, you can use this skill in workflows that connect to embedding models in the Azure AI Foundry model catalog. It's also available in the Azure portal, in skillset design, assuming Azure AI Search and Azure Machine Learning services are deployed in the same subscription. | [Create or Update Skillset (preview)](/rest/api/searchservice/skillsets/create-or-update?view=rest-searchservice-2024-05-01-preview&preserve-view=true). |
| [**Incremental enrichment cache**](cognitive-search-incremental-indexing-conceptual.md) | Applied AI (skills) | Adds caching to an enrichment pipeline, allowing you to reuse existing output if a targeted modification, such as an update to a skillset or another object, doesn't change the content. Caching applies only to enriched documents produced by a skillset.| [Create or Update Indexer (preview)](/rest/api/searchservice/indexers/create-or-update?view=rest-searchservice-2024-05-01-preview&preserve-view=true). |
|  [**OneLake files indexer**](search-how-to-index-onelake-files.md) | Indexer data source | New data source for extracting searchable data and metadata data from a [lakehouse](/fabric/onelake/create-lakehouse-onelake) on top of [OneLake](/fabric/onelake/onelake-overview) | [Create or Update Data Source (preview)](/rest/api/searchservice/data-sources/create-or-update?view=rest-searchservice-2024-05-01-preview&preserve-view=true). |
|  [**Azure Files indexer**](search-file-storage-integration.md) | Indexer data source | New data source for indexer-based indexing from [Azure Files](https://azure.microsoft.com/services/storage/files/) | [Create or Update Data Source (preview)](/rest/api/searchservice/data-sources/create-or-update?view=rest-searchservice-2024-05-01-preview&preserve-view=true). |
| [**SharePoint Online indexer**](search-howto-index-sharepoint-online.md) | Indexer data source | New data source for indexer-based indexing of SharePoint content. | [Sign up](https://aka.ms/azure-cognitive-search/indexer-preview) to enable the feature. [Create or Update Data Source (preview)](/rest/api/searchservice/data-sources/create-or-update?view=rest-searchservice-2024-05-01-preview&preserve-view=true) or the Azure portal. |
|  [**MySQL indexer**](search-howto-index-mysql.md) | Indexer data source | New data source for indexer-based indexing of Azure MySQL data sources.| [Sign up](https://aka.ms/azure-cognitive-search/indexer-preview) to enable the feature. [Create or Update Data Source (preview)](/rest/api/searchservice/data-sources/create-or-update?view=rest-searchservice-2024-05-01-preview&preserve-view=true), [.NET SDK 11.2.1](/dotnet/api/azure.search.documents.indexes.models.searchindexerdatasourcetype.mysql), and Azure portal. |
| [**Azure Cosmos DB for MongoDB indexer**](search-howto-index-cosmosdb.md) | Indexer data source | New data source for indexer-based indexing through the MongoDB APIs in Azure Cosmos DB. | [Sign up](https://aka.ms/azure-cognitive-search/indexer-preview) to enable the feature. [Create or Update Data Source (preview)](/rest/api/searchservice/data-sources/create-or-update?view=rest-searchservice-2024-05-01-preview&preserve-view=true) or the Azure portal. |
| [**Azure Cosmos DB for Apache Gremlin indexer**](search-howto-index-cosmosdb.md) | Indexer data source | New data source for indexer-based indexing through the Apache Gremlin APIs in Azure Cosmos DB. | [Sign up](https://aka.ms/azure-cognitive-search/indexer-preview) to enable the feature. [Create or Update Data Source (preview)](/rest/api/searchservice/data-sources/create-or-update?view=rest-searchservice-2024-05-01-preview&preserve-view=true). |
| [**Native blob soft delete**](search-howto-index-changed-deleted-blobs.md) | Indexer data source | Applies to the Azure Blob Storage indexer. Recognizes blobs that are in a soft-deleted state, and removes the corresponding search document during indexing. | [Create or Update Data Source (preview)](/rest/api/searchservice/data-sources/create-or-update?view=rest-searchservice-2024-05-01-preview&preserve-view=true). |
| [**Reset Documents**](search-howto-run-reset-indexers.md) | Indexer | Reprocesses individually selected search documents in indexer workloads. | [Reset Documents (preview)](/rest/api/searchservice/indexers/reset-docs?view=rest-searchservice-2024-05-01-preview&preserve-view=true). |
| [**speller**](speller-how-to-add.md) | Query | Optional spelling correction on query term inputs for simple, full, and semantic queries. | [Search Documents (preview)](/rest/api/searchservice/documents/search-post?view=rest-searchservice-2024-05-01-preview&preserve-view=true). |
| [**Normalizers**](search-normalizers.md) | Query |  Normalizers provide simple text preprocessing: consistent casing, accent removal, and ASCII folding, without invoking the full text analysis chain.| [Search Documents (preview)](/rest/api/searchservice/documents/search-post?view=rest-searchservice-2024-05-01-preview&preserve-view=true). |
| [**featuresMode parameter**](/rest/api/searchservice/documents/search-post?view=rest-searchservice-2024-05-01-preview&preserve-view=true) | Relevance (scoring) | BM25 relevance score expansion to include details: per field similarity score, per field term frequency, and per field number of unique tokens matched. You can consume these data points in [custom scoring solutions](https://github.com/Azure-Samples/search-ranking-tutorial). | [Search Documents (preview)](/rest/api/searchservice/documents/search-post?view=rest-searchservice-2024-05-01-preview&preserve-view=true).|
| [**vectorQueries.threshold parameter**](vector-search-how-to-query.md#vector-weighting) | Relevance (scoring)  | Exclude low-scoring search result based on a minimum score. | [Search Documents (preview)](/rest/api/searchservice/documents/search-post?view=rest-searchservice-2024-05-01-preview&preserve-view=true). |
| [**hybridSearch.maxTextRecallSize and countAndFacetMode parameters**](hybrid-search-how-to-query.md#set-maxtextrecallsize-and-countandfacetmode) | Relevance (scoring)  |  adjust the inputs to a hybrid query by controlling the amount BM25-ranked results that flow to the hybrid ranking model.  | [Search Documents (preview)](/rest/api/searchservice/documents/search-post?view=rest-searchservice-2024-05-01-preview&preserve-view=true). |
| [**moreLikeThis**](search-more-like-this.md) | Query | Finds documents that are relevant to a specific document. This feature has been in earlier previews. | [Search Documents (preview)](/rest/api/searchservice/documents/search-post?view=rest-searchservice-2024-05-01-preview&preserve-view=true). |

## Control plane preview features

|Feature&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  | Category | Description | Availability  |
|---------|------------------|-------------|---------------|
| [**Service upgrade**](search-how-to-upgrade.md) | Feature | Upgrade your search service to higher storage limits in your region. With a one-time upgrade, you no longer need to recreate your service. | The Azure portal and [Upgrade Service (2025-02-01-preview)](/rest/api/searchmanagement/services/upgrade?view=rest-searchmanagement-2025-02-01-preview&preserve-view=true). |
| [**Pricing tier change**](search-capacity-planning.md#change-your-pricing-tier) | Feature | Change the [pricing tier](search-sku-tier.md) of your search service. This provides flexibility to scale storage, increase request throughput, and decrease latency based on your needs. In this preview, you can only change between Basic and Standard (S1, S2, and S3) tiers. | The Azure portal and [Update Service (2025-02-01-preview)](/rest/api/searchmanagement/services/update?view=rest-searchmanagement-2025-02-01-preview&preserve-view=true#searchupdateservicewithsku). |
| [**Network security perimeter**](search-security-network-security-perimeter.md) | Service | Join a search service to a [network security perimeter](/azure/private-link/network-security-perimeter-concepts) to control network access to your search service. | The Azure portal and the [Network Security Perimeter APIs 2024-06-01-preview](/rest/api/searchmanagement/network-security-perimeter-configurations?view=rest-searchmanagement-2024-06-01-preview&preserve-view=true) or the latest preview version. |
| [**Search service under a user-assigned managed identity**](search-howto-managed-identities-data-sources.md) | Service | Configures a search service to use a previously created user-assigned managed identity. | [Services - Update](/rest/api/searchmanagement/services/update?view=rest-searchmanagement-2024-06-01-preview&preserve-view=true#identity), 2021-04-01-preview, or the latest preview version. We recommend using the latest preview version. |

## Preview features in Azure SDKs

Each Azure SDK team releases beta packages on their own timeline. Check the change log for mentions of new features in beta packages:

+ [Change log for Azure SDK for .NET](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md)
+ [Change log for Azure SDK for Java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md)
+ [Change log for Azure SDK for JavaScript](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md)
+ [Change log for Azure SDK for Python](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md).

## Using preview features

Experimental features are available through the preview REST API first, followed by Azure portal, and then the Azure SDKs. 

The following statements apply to preview features:

+ Preview features are available under [Supplemental Terms of Use](https://azure.microsoft.com/support/legal/preview-supplemental-terms/), without a service level agreement.
+ Preview features might undergo breaking changes if a redesign is required. 
+ Sometimes preview features don't make it into a GA release.

If you write code against a preview API, you should prepare to upgrade that code to newer API versions when they roll out. We maintain an [Upgrade REST APIs](search-api-migration.md) document to make that step easier.

## How to call a preview REST API

Preview REST APIs are accessed through the api-version parameter on the URI. Older previews are still operational but become stale over time and aren't updated with new features or bug fixes.

For data plane operation on content, [**`2024-05-01-preview`**](/rest/api/searchservice/search-service-api-versions#2024-05-01-Preview) is the most recent preview version. The following example shows the syntax for [Indexes GET (preview)](/rest/api/searchservice/indexes/get?view=rest-searchservice-2024-05-01-preview&preserve-view=true):

```rest
GET {endpoint}/indexes('{indexName}')?api-version=2024-05-01-Preview
```

For management operations on the search service, [**`2025-05-01-preview`**](/rest/api/searchmanagement/services/update?view=rest-searchmanagement-2025-05-01-preview&preserve-view=true) is the most recent preview version. The following example shows the syntax for Update Service 2025-05-01-preview version.

```rest
PATCH https://management.azure.com/subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Search/searchServices/mysearchservice?api-version=2025-05-01-preview

{
  "tags": {
    "app-name": "My e-commerce app",
    "new-tag": "Adding a new tag"
  },
  "properties": {
    "replicaCount": 2
  }
}
```

## See also

+ [Quickstart: REST APIs](search-get-started-rest.md)
+ [Search REST API overview](/rest/api/searchservice/)
+ [Search REST API versions](/rest/api/searchservice/search-service-api-versions)
+ [Manage using the REST APIs](search-manage-rest.md)
+ [Management REST API overview](/rest/api/searchmanagement/)
+ [Management REST API versions](/rest/api/searchmanagement/management-api-versions)
