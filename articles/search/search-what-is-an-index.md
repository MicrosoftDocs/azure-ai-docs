---
title: Search index overview
titleSuffix: Azure AI Search
description: Explains index content, construction, physical expression, and schema.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: concept-article
ms.date: 01/27/2026
ms.update-cycle: 365-days
---

# Search indexes in Azure AI Search

In Azure AI Search, a *search index* is your searchable content on a search service, available to the local search engine for indexing, agentic retrieval, full-text search, vector search, hybrid search, and filtered queries. An index is defined by a schema that's saved to your search service, with data ingestion following as a second step. Indexed content exists on your search service, apart from your primary external data stores, which is necessary for the millisecond response times expected in modern search applications. Except for remote agentic retrieval and indexer-driven indexing scenarios, the search service never connects to or queries your external source data.

This article covers the key concepts for creating and managing a search index, including:

+ Content (documents and schema)
+ Physical data structure
+ Basic operations

> [!TIP]
> **Quick summary:**
> - An index stores your searchable content
> - Schema defines fields and their behaviors
> - Documents are individual searchable items (similar to rows in a database)
> - [Jump to creating an index →](search-how-to-create-search-index.md)

## Schema of a search index

In Azure AI Search, indexes contain *search documents*. Conceptually, a document is a single unit of searchable data in your index. For example, a retailer might have a document for each product, a university might have a document for each class, a travel site might have a document for each hotel and destination, and so forth. Mapping these concepts to more familiar database equivalents: a *search index* equates to a *table*, and *documents* are roughly equivalent to *rows* in a table.

Here's an example of what an index schema looks like.

```json
{
  "name": "name_of_index, unique across the service",
  "description" : "Health plan coverage for standard and premium plans for Northwind and Contoso employees.",
  "fields": [
    {
      "name": "name_of_field",
      "type": "Edm.String | Collection(Edm.String) | Collection(Edm.Single) | Edm.Int32 | Edm.Int64 | Edm.Double | Edm.Boolean | Edm.DateTimeOffset | Edm.GeographyPoint",
      "searchable": true (default where applicable) | false (only Edm.String and Collection(Edm.String) fields can be searchable),
      "filterable": true (default) | false,
      "sortable": true (default where applicable) | false (Collection(Edm.String) fields cannot be sortable),
      "facetable": true (default where applicable) | false (Edm.GeographyPoint fields cannot be facetable),
      "key": true (only Edm.String fields can be keys) | false (default where applicable),
      "retrievable": true (default) | false,
      "analyzer": "name_of_analyzer_for_search_and_indexing" (only if 'searchAnalyzer' and 'indexAnalyzer' are not set),
      "searchAnalyzer": "name_of_search_analyzer" (only if 'indexAnalyzer' is set and 'analyzer' is not set),
      "indexAnalyzer": "name_of_indexing_analyzer" (only if 'searchAnalyzer' is set and 'analyzer' is not set),
      "normalizer":  "name_of_normalizer" (applies to fields that are filterable),
      "synonymMaps": "name_of_synonym_map" (optional, only one synonym map per field is currently supported),
      "dimensions": "number of dimensions used by an embedding models" (applies to vector fields of type Collection(Edm.Single)),
      "vectorSearchProfile": "name_of_vector_profile" (indexes can have many configurations but a field can use just one)
    }
  ],
  "suggesters": [ ],
  "scoringProfiles": [ ],
  "analyzers":(optional)[ ... ],
  "charFilters":(optional)[ ... ],
  "tokenizers":(optional)[ ... ],
  "tokenFilters":(optional)[ ... ],
  "defaultScoringProfile": (optional) "...",
  "corsOptions": (optional) { },
  "encryptionKey":(optional){ },
  "semantic":(optional){ },
  "vectorSearch":(optional){ }
}
```

The `fields` collection is typically the largest part. Each field has a name, [data type](/rest/api/searchservice/Supported-data-types), and attributes that determine usage at query time.

Other elements are collapsed for brevity, but the following links provide details: 

+ [suggesters](index-add-suggesters.md) support type-ahead queries like autocomplete.
+ [scoringProfiles](index-add-scoring-profiles.md) are used for relevance tuning.
+ [analyzers](search-analyzers.md) are used to process strings into tokens according to linguistic rules or other characteristics supported by the analyzer.
+ [corsOptions](search-how-to-create-search-index.md#corsoptions), or Cross-origin remote scripting (CORS), is used for apps that issues requests from different domains.
+ [encryptionKey](search-security-manage-encryption-keys.md) configures double-encryption of sensitive content in the index.
+ [semantic](semantic-how-to-query-request.md) configures semantic reranking in full text and hybrid search.
+ [vectorSearch](vector-search-how-to-create-index.md) configures vector fields and queries.

### Field definitions

A search document is defined by the `fields` collection in the body of [Create Index request](/rest/api/searchservice/indexes/create). You need fields for document identification (keys), storing searchable text, and fields for supporting filters, facets, and sorting. You might also need fields for data that a user never sees. For example, you might want fields for profit margins or marketing promotions that you can use in a [scoring profile](index-add-scoring-profiles.md) to boost a search score.

If incoming data is hierarchical in nature, you can represent it within an index as a [complex type](search-howto-complex-data-types.md), used for nested structures. The sample data set, [Hotels](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/hotels), illustrates complex types using an Address (contains multiple subfields) that has a one-to-one relationship with each hotel, and a Rooms complex collection, where multiple rooms are associated with each hotel. 

<a name="index-attributes"></a>

### Field attributes

Field attributes determine how a field is used, such as whether it's used in full text search, faceted navigation, sort operations, and so forth. 

+ String fields are often marked as `searchable` and `retrievable`. 
+ Fields used to narrow or order search results are marked as `sortable`, `filterable`, and `facetable`.

|Attribute|Description|  
|---------------|-----------------|  
|searchable |Full-text or vector searchable. Text fields are subject to lexical analysis such as word-breaking during indexing. For details, see [How full text search works](search-lucene-query-architecture.md).|  
|filterable |Referenced in $filter queries. Filterable fields of type `Edm.String` or `Collection(Edm.String)` don't undergo word-breaking, so comparisons are for exact matches only. Given the string "sunny day", `$filter=f eq 'sunny'` finds no matches, but `$filter=f eq 'sunny day'` succeeds. |  
|sortable |By default the system sorts by a search score, but you can configure an explicit sort based on fields in the documents. Fields of type `Collection(Edm.String)` can't be sortable. |  
|facetable |Typically used in a presentation of search results that includes a hit count by category (for example, hotels in a specific city). This option can't be used with fields of type `Edm.GeographyPoint`. Fields of type `Edm.String` that are filterable, sortable, or facetable can be at most 32 kilobytes in length. For details, see [Create Index (REST API)](/rest/api/searchservice/indexes/create).|  
|key |Unique identifier for documents within the index. Exactly one field must be chosen as the key field and it must be of type `Edm.String`.|  
|retrievable |Determines whether the field can be returned in a search result. This is useful when you want to use a field (such as *profit margin*) as a filter, sorting, or scoring mechanism, but don't want the field to be visible to the end user. This attribute must be `true` for `key` fields.|  

Although you can add new fields at any time, existing field definitions are locked in for the lifetime of the index. For this reason, developers typically use the Azure portal for creating simple indexes, testing ideas, or using the Azure portal pages to look up a setting. Frequent iteration over an index design is more efficient if you follow a code-based approach so that you can rebuild the index easily.

> [!NOTE]
> The APIs you use to build an index have varying default behaviors. For the [REST APIs](/rest/api/searchservice/indexes/create), most attributes are enabled by default (for example, searchable and retrievable are true for string fields) and you often only need to set them if you want to turn them off. For the .NET SDK, the opposite is true. On any property you don't explicitly set, the default is to disable the corresponding search behavior unless you specifically enable it.

<a name="index-size"></a>

## Physical structure and size

In Azure AI Search, the physical structure of an index is largely an internal implementation. You can access its schema, load and query its content, monitor its size, and manage its capacity. However, Microsoft manages the infrastructure and physical data structures stored with your search service.

You can monitor index size on the **Search management > Indexes** page in the Azure portal. Alternatively, you can issue a [GET INDEX request](/rest/api/searchservice/indexes/get) against your search service or a [Service Statistics request](/rest/api/searchservice/get-service-statistics/get-service-statistics) to check the value of storage size.

> [!NOTE]
> If you're actively [deleting content](search-how-to-delete-documents.md), index storage and size are updated every few minutes. Deletion runs as a background process. Expect a small delay on metric updates.

The size of an index is determined by the:

+ Quantity and composition of your documents.
+ Attributes on individual fields: retrievable doesn't bloat your index, but filterable, sortable, and facetable consume more storage for storing non-tokenized text.
+ Index configuration. Specifically, whether you include suggesters or specialized [analyzers](search-analyzers.md). If you use the edgeNgram tokenizer to store verbatim sequences of characters (`a, ab, abc, abcd`), the index is larger than if you use the standard analyzer.

Document composition and quantity are determined by what you choose to import. Remember that a search index should only contain content that's useful for your search application. If source data includes binary fields, omit those fields unless you're using AI enrichment to crack and analyze the content to create text-searchable information.

Field attributes determine behaviors. To support those behaviors, the indexing process creates the necessary data structures. For example, for a field of type `Edm.String`, "searchable" invokes [full-text search](search-lucene-query-architecture.md), which scans inverted indexes for the tokenized term. In contrast, a "filterable" or "sortable" attribute supports iteration over unmodified strings. 

[**Suggesters**](index-add-suggesters.md) are constructs that support type-ahead or autocomplete queries. When you include a suggester, the indexing process creates the data structures necessary for verbatim character matches. Suggesters are implemented at the field level, so choose only those fields that are reasonable for type-ahead.

## Basic operations and interaction

Now that you have a better idea of what an index is, this section introduces index runtime operations, including connecting to and securing a single index.

> [!NOTE]
> There's no portal or API support for moving or copying an index. Typically, you either point your application deployment to a different search service (using the same index name) or revise the name to create a copy on your current search service and then build it.

### Index isolation
  
In Azure AI Search, you work with one index at a time. All index-related operations target a single index. There's no concept of related indexes or the joining of independent indexes for either indexing or querying.

### Continuously available

An index is immediately available for queries as soon as the first document is indexed, but it's not fully operational until all documents are indexed. Internally, an index is [distributed across partitions and executes on replicas](search-capacity-planning.md#concepts-search-units-replicas-partitions). The physical index is managed internally. You manage the logical index.

An index is continuously available and can't be paused or taken offline. Because it's designed for continuous operation, updates to its content and additions to the index itself happen in real time. If a request coincides with a document update, queries might temporarily return incomplete results.

Query continuity exists for document operations, such as refreshing or deleting, and for modifications that don't affect the existing structure or integrity of an index, such as adding new fields. Structural updates, such as changing existing fields, are typically managed using a drop-and-rebuild workflow in a development environment or by creating a new version of the index on the production service.

To avoid an [index rebuild](search-howto-reindex.md), some customers who are making small changes "version" a field by creating a new one that coexists with a previous version. Over time, this leads to orphaned content by way of obsolete fields and obsolete custom analyzer definitions, especially in a production index that's expensive to replicate. You can address these issues during planned updates to the index as part of index lifecycle management.

### Endpoint connection and security

All indexing and query requests target an index. Endpoints are usually one of the following:

| Endpoint | Connection and access control |
|----------|-------------------------------|
| `<your-service>.search.windows.net/indexes` | Targets the indexes collection. Used when creating, listing, or deleting an index. Admin rights are required for these operations and available through admin [API keys](search-security-api-keys.md) or a [Search Contributor role](search-security-rbac.md#built-in-roles-used-in-search). |
| `<your-service>.search.windows.net/indexes/<your-index>/docs` | Targets the documents collection of a single index. Used when querying an index or data refresh. For queries, read rights are sufficient and available through query API keys or a data reader role. For data refresh, admin rights are required. |

#### How to connect to an index

1. [Start with the Azure portal](https://portal.azure.com) and your search service dashboard.

1. Try other clients for programmatic access. We recommend the quickstarts for first steps:

   + [Quickstart: Connect to a search service](search-get-started-rbac.md)
   + [Quickstart: REST](search-get-started-text.md)
   + [Quickstart: Full-text search](search-get-started-text.md)
   + [Quickstart: Agentic retrieval](search-get-started-agentic-retrieval.md)

## Next steps

You can get hands-on experience creating an index using almost any sample or walkthrough for Azure AI Search. For starters, you could choose any of the quickstarts from the table of contents.

But you'll also want to become familiar with methodologies for loading an index with data. Index definition and data import strategies are defined in tandem. The following articles provide more information about creating and loading an index.

+ [Create a search index](search-how-to-create-search-index.md)
+ [Update an index](search-howto-reindex.md)
+ [Create a vector store](vector-search-how-to-create-index.md)
+ [Create an index alias](search-how-to-alias.md)
+ [Data import overview](search-what-is-data-import.md)
+ [Load an index](search-how-to-load-search-index.md)
