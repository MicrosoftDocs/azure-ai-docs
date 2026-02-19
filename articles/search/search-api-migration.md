---
title: Upgrade REST API versions
titleSuffix: Azure AI Search
description: Review differences in API versions and learn about the REST API lifecycle and the steps for migrating code to the newer versions.
manager: nitinme
author: bevloh
ms.author: beloh
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: upgrade-and-migration-article
ms.date: 12/17/2025
---

# Upgrade to the latest REST API in Azure AI Search

Use this article to migrate to newer versions of the [**Search Service REST APIs**](/rest/api/searchservice/) and the [**Search Management REST APIs**](/rest/api/searchmanagement/) for [data plane and control plane](/azure/azure-resource-manager/management/control-plane-and-data-plane) operations.

Here are the most recent versions of the REST APIs:

| Targeted operations | REST API | Status |
|---------------------|----------|--------|
| Data plane | [`2025-09-01`](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-09-01&preserve-view=true) | Stable |
| Data plane | [`2025-11-01-preview`](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) | Preview |
| Control plane | [`2025-05-01`](/rest/api/searchmanagement/operation-groups?view=rest-searchmanagement-2025-05-01&preserve-view=true) | Stable |
| Control plane | [`2025-02-01-preview`](/rest/api/searchmanagement/operation-groups?view=rest-searchmanagement-2025-02-01-preview&preserve-view=true) | Preview |

Upgrade instructions focus on code changes that get you through breaking changes from previous versions so that existing code runs the same as before, but on the newer API version. Once your code is in working order, you can decide whether to adopt newer features. To learn more about new features, see [What's New](whats-new.md).

We recommend upgrading API versions in succession, working through each version until you get to the newest one.

`2023-07-01-preview` was the first REST API for vector support. **Do not use this API version**. It's now deprecated and you should migrate to either stable or newer preview REST APIs immediately.

> [!NOTE]
> REST API reference docs are now versioned. For version-specific content, open a reference page and then use the selector located above the table of contents, to pick your version.

## When to upgrade

Azure AI Search breaks backward compatibility as a last resort. Upgrade is necessary when:

+ Your code references a retired or unsupported API version and is subject to one or more breaking changes. You must address breaking changes if your code targets [`2025-11-01-preview`](#breaking-changes-for-agentic-retrieval) for agentic retrieval, [`2025-05-01-preview`](#breaking-changes-for-knowledge-agents) for knowledge agents, [`2023-07-10-preview`](#code-upgrade-for-vector-indexes-and-queries) for vectors, [`2020-06-01-preview`](#breaking-changes-for-semantic-ranker) for semantic ranker, and [`2019-05-06`](#upgrade-to-2019-05-06) for obsolete skills and workarounds.

+ Your code fails when unrecognized properties are returned in an API response. As a best practice, your application should ignore properties that it doesn't understand.

+ Your code persists API requests and tries to resend them to the new API version. For example, this might happen if your application persists continuation tokens returned from the Search API (for more information, look for `@search.nextPageParameters` in the [Search API Reference](/rest/api/searchservice/documents/search-post)).

## How to upgrade

1. If you're upgrading a data plane version, review [what's been released](whats-new.md) in the new API version.

1. Update the `api-version` parameter, specified in the request header, to a newer version.

   In your application code that makes direct calls to the REST APIs, search for all instances of the existing version and then replace it with the new version. For more information about structuring a REST call, see [Quickstart: Full-text search using REST](search-get-started-text.md).

   If you're using an Azure SDK, each package targets a specific version of the REST API. To determine which REST API version your package supports, review its change log. Update to the latest package version to access the latest features and API improvements.

1. If you're upgrading a data plane version, review the breaking changes documented in this article and implement the workarounds. Start with the version used by your code and resolve any breaking change for each newer API version until you get to the newest stable or preview release.

## Breaking changes

The following breaking changes apply to data operations.

### Breaking changes for agentic retrieval

The latest `2025-11-01-preview` refactors the APIs for knowledge agents (bases), knowledge sources, and the retrieve action. The latest `2025-11-01-preview` renames knowledge agents to knowledge bases and relocates several properties. Several properties are replaced or relocated to other objects. 

For help with breaking changes, see [Migrate your agentic retrieval code](agentic-retrieval-how-to-migrate.md).

### Breaking changes for knowledge agents

[Knowledge agents](agentic-retrieval-how-to-create-knowledge-base.md) were introduced in `2025-05-01-preview`. In `2025-08-01-preview`, `targetIndexes` was replaced with a new knowledge source object and `defaultMaxDocsForReranker` was replaced with other APIs. More breaking changes are introduced in `2025-11-01-preview`.

For help with breaking changes, see [Migrate your agentic retrieval code](agentic-retrieval-how-to-migrate.md).

### Breaking changes for client code that reads connection information

Effective March 29, 2024 and applicable to all [supported REST APIs](/rest/api/searchservice/search-service-api-versions):

+ [GET Skillset](/rest/api/searchservice/skillsets/get), [GET Index](/rest/api/searchservice/indexes/get), and [GET Indexer](/rest/api/searchservice/indexers/get) no longer return keys or connection properties in a response. This is a breaking change if you have downstream code that reads keys or connections (sensitive data) from a GET response.

+ If you need to retrieve admin or query API keys for your search service, use the [Search Management REST APIs](search-security-api-keys.md?tabs=rest-find#find-existing-keys).

+ If you need to retrieve connection strings of another Azure resource such as Azure Storage or Azure Cosmos DB, use the APIs of that resource and published guidance to obtain the information.

### Breaking changes for semantic ranker

[Semantic ranker](semantic-search-overview.md) became generally available in `2023-11-01`. These are the breaking changes from earlier releases:

+ In all versions after `2020-06-01-preview`: `semanticConfiguration` replaces `searchFields` as the mechanism for specifying which fields to use for L2 ranking.

+ For all API versions, updates on July 14, 2023 to the Microsoft-hosted semantic models made semantic ranker language-agnostic, effectively decommissioning the `queryLanguage` property. There's no "breaking change" in code, but the property is ignored.

See [Migrate from preview version](semantic-code-migration.md) to transition your code to use `semanticConfiguration`.

## Data plane upgrades

Upgrade guidance assumes upgrade from the most recent previous version. If your code is based on an old API version, we recommend upgrading through each successive version to get to the newest version.

### Upgrade to 2025-11-01-preview

[`2025-11-01-preview`](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) introduces the following breaking changes to agentic retrieval as implemented in the `2025-08-01-preview`:

+ Replaces `agents` with `knowledgebases`. Several properties related to knowledge sources moved out of the knowledge base definition and to the retrieve action.
+ Knowledge source properties are refactored, implementing a new `ingestionParameters` object for knowledge sources that generate an indexer pipeline.

For more information on changes and code migration, see [breaking changes in 2025-11-01-preview](agentic-retrieval-how-to-migrate.md#version-specific-changes) and [How to migrate](agentic-retrieval-how-to-migrate.md#how-to-migrate).

For all other existing APIs, there are no behavior changes. You can swap in the new API version and your code runs the same as before.

### Upgrade to 2025-09-01

[`2025-09-01`](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-09-01&preserve-view=true) is the latest stable REST API version and it adds general availability for the OneLake indexer, Document Layout skill, and other APIs.

There are no breaking changes if you're upgrading from `2024-07-01` and not using any preview features. To use the new stable release, change the API version and test your code.

### Upgrade to 2025-08-01-preview

[`2025-08-01-preview`](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-08-01-preview&preserve-view=true) introduces the following breaking changes to knowledge agents created using `2025-05-01-preview`:

+ Replaces `targetIndexes` with `knowledgeSources`.
+ Removes `defaultMaxDocsForReranker` without replacement.

Otherwise, there are no behavior changes on existing APIs. You can swap in the new API version and your code runs the same as before.

### Upgrade to 2025-05-01-preview

[`2025-05-01-preview`](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-05-01-preview&preserve-view=true) provides new features, but there are no behavior changes on existing APIs. You can swap in the new API version and your code runs the same as before.

### Upgrade to 2025-03-01-preview

[`2025-03-01-preview`](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-03-01-preview&preserve-view=true) provides new features, but there are no behavior changes on existing APIs. You can swap in the new API version and your code runs the same as before.

### Upgrade to 2024-11-01-preview

[`2024-11-01-preview`](/rest/api/searchservice/operation-groups?view=rest-searchservice-2024-11-01-preview&preserve-view=true) query rewrite, Document Layout skill, keyless billing for skills processing, Markdown parsing mode, and rescoring options for compressed vectors.

If you're upgrading from `2024-09-01-preview`, you can swap in the new API version and your code runs the same as before.

However, the new version introduces syntax changes to `vectorSearch.compressions`:

+ Replaces `rerankWithOriginalVectors` with `enableRescoring`
+ Moves `defaultOversampling` to a new `rescoringOptions` property object

Backwards compatibility is preserved due to an internal API mapping, but we recommend changing the syntax if you adopt the new preview version. For a comparison of the syntax, see [Compress vectors using scalar or binary quantization](vector-search-how-to-quantization.md#add-compressions-to-a-search-index).

### Upgrade to 2024-09-01-preview

[`2024-09-01-preview`](/rest/api/searchservice/operation-groups?view=rest-searchservice-2024-09-01-preview&preserve-view=true) adds Matryoshka Representation Learning (MRL) compression for text-embedding-3 models, targeted vector filtering for hybrid queries, vector subscore details for debugging, and token chunking for [Text Split skill](cognitive-search-skill-textsplit.md).

If you're upgrading from `2024-05-01-preview`, you can swap in the new API version and your code runs the same as before.

### Upgrade to 2024-07-01

[`2024-07-01`](/rest/api/searchservice/operation-groups?view=rest-searchservice-2024-07-01&preserve-view=true) is a general release. The former preview features are now generally available: integrated chunking and vectorization (Text Split skill, AzureOpenAIEmbedding skill), query vectorizer based on AzureOpenAIEmbedding, vector compression (scalar quantization, binary quantization, stored property, narrow data types).

There are no breaking changes if you upgrade from `2024-05-01-preview` to stable. To use the new stable release, change the API version and test your code.

There are breaking changes if you upgrade directly from `2023-11-01`. Follow the steps outlined for each newer preview to migrate from `2023-11-01` to `2024-07-01`.

### Upgrade to 2024-05-01-preview

[`2024-05-01-preview`](/rest/api/searchservice/operation-groups?view=rest-searchservice-2024-05-01-preview&preserve-view=true) adds an indexer for Microsoft OneLake, binary vectors, and more embedding models.

If you're upgrading from `2024-03-01-preview`, the AzureOpenAIEmbedding skill now requires a model name and dimensions property.

1. Search your codebase for [AzureOpenAIEmbedding](cognitive-search-skill-azure-openai-embedding.md) references.

1. Set `modelName` to "text-embedding-ada-002" and set `dimensions` to "1536".

### Upgrade to 2024-03-01-preview

[`2024-03-01-preview`](/rest/api/searchservice/operation-groups?view=rest-searchservice-2024-03-01-preview&preserve-view=true) adds narrow data types, scalar quantization, and vector storage options.

If you're upgrading from `2023-10-01-preview`, there are no breaking changes. However, there's one behavior difference: for `2023-11-01` and newer previews, the `vectorFilterMode` default changed from postfilter to prefilter for [filter expressions](vector-search-filters.md).

1. Search your codebase for `vectorFilterMode` references.

1. If the property is explicitly set, no action is required. If you relied on the default value, the new default behavior is to filter *before* query execution. If you want post-query filtering, explicitly set `vectorFilterMode` to postfilter to retain the old behavior.

### Upgrade to 2023-11-01

[`2023-11-01`](/rest/api/searchservice/operation-groups?view=rest-searchservice-2023-11-01&preserve-view=true) is a general release. The former preview features are now generally available: semantic ranker and vector support.

There are no breaking changes from `2023-10-01-preview`, but there are multiple breaking changes from `2023-07-01-preview` to `2023-11-01`. For more information, see [Upgrade from 2023-07-01-preview](#upgrade-from-2023-07-01-preview).

To use the new stable release, change the API version and test your code.

### Upgrade to 2023-10-01-preview

[`2023-10-01-preview`](/rest/api/searchservice/operation-groups?view=rest-searchservice-2023-10-01-preview&preserve-view=true) was the first preview version to add [built-in data chunking and vectorization during indexing](vector-search-integrated-vectorization.md) and [built-in query vectorization](vector-search-how-to-configure-vectorizer.md). It also supports vector indexing and queries from the previous version.

If you're upgrading from the previous version, the next section has the steps.

### Upgrade from 2023-07-01-preview

Don't use this API version. It implements a vector query syntax that's incompatible with any newer API version.

`2023-07-01-preview` is now deprecated, so you shouldn't base new code on this version, nor should you upgrade *to* this version under any circumstances. This section explains the migration path from `2023-07-01-preview` to any newer API version.

#### Portal upgrade for vector indexes

Azure portal supports a one-click upgrade path for `2023-07-01-preview` indexes. It detects vector fields and provides a **Migrate** button.

+ Migration path is from `2023-07-01-preview` to `2024-05-01-preview`.
+ Updates are limited to vector field definitions and vector search algorithm configurations.
+ Updates are one-way. You can't reverse the upgrade. Once the index is upgraded, you must use `2024-05-01-preview` or later to query the index.

There's no portal migration for upgrading vector query syntax. See [code upgrades](#code-upgrade-for-vector-indexes-and-queries) for query syntax changes.

Before selecting **Migrate**, select **Edit JSON** to review the updated schema first. You should find a schema that conforms to the changes described in the [code upgrade](#code-upgrade-for-vector-indexes-and-queries) section. Portal migration only handles indexes with one vector search algorithm configuration. It creates a default profile that maps to the `2023-07-01-preview` vector search algorithm. Indexes with multiple vector search configurations require manual migration.

#### Code upgrade for vector indexes and queries

[Vector search](vector-search-overview.md) support was introduced in [Create or Update Index (2023-07-01-preview)](/rest/api/searchservice/preview-api/create-or-update-index).

Upgrading from `2023-07-01-preview` to any newer stable or preview version requires:

+ Renaming and restructuring the vector configuration in the index
+ Rewriting your vector queries

Use the instructions in this section to migrate vector fields, configuration, and queries from `2023-07-01-preview`.

1. Call [Get Index](/rest/api/searchservice/indexes/get?view=rest-searchservice-2023-11-01&tabs=HTTP&preserve-view=true) to retrieve the existing definition.

1. Modify the vector search configuration. `2023-11-01` and later versions introduce the concept of *vector profiles* that bundle vector-related configurations under one name. Newer versions also rename `algorithmConfigurations` to `algorithms`.

   + Rename `algorithmConfigurations` to `algorithms`. This is only a renaming of the array. The contents are backwards compatible. This means your existing HNSW configuration parameters can be used.

   + Add `profiles`, giving a name and an algorithm configuration for each one.

    **Before migration (2023-07-01-preview)**:

    ```http
      "vectorSearch": {
        "algorithmConfigurations": [
            {
                "name": "myHnswConfig",
                "kind": "hnsw",
                "hnswParameters": {
                    "m": 4,
                    "efConstruction": 400,
                    "efSearch": 500,
                    "metric": "cosine"
                }
            }
        ]}
    ```

    **After migration (2023-11-01)**:

    ```http
      "vectorSearch": {
        "algorithms": [
          {
            "name": "myHnswConfig",
            "kind": "hnsw",
            "hnswParameters": {
              "m": 4,
              "efConstruction": 400,
              "efSearch": 500,
              "metric": "cosine"
            }
          }
        ],
        "profiles": [
          {
            "name": "myHnswProfile",
            "algorithm": "myHnswConfig"
          }
        ]
      }
    ```

1. Modify vector field definitions, replacing `vectorSearchConfiguration` with `vectorSearchProfile`. Make sure the profile name resolves to a new vector profile definition, and not the algorithm configuration name. Other vector field properties remain unchanged. For example, they can't be filterable, sortable, or facetable, nor use analyzers or normalizers or synonym maps.

    **Before (2023-07-01-preview)**:

    ```http
      {
          "name": "contentVector",
          "type": "Collection(Edm.Single)",
          "key": false,
          "searchable": true,
          "retrievable": true,
          "filterable": false,  
          "sortable": false,  
          "facetable": false,
          "analyzer": "",
          "searchAnalyzer": "",
          "indexAnalyzer": "",
          "normalizer": "",
          "synonymMaps": "", 
          "dimensions": 1536,
          "vectorSearchConfiguration": "myHnswConfig"
      }
    ```

    **After (2023-11-01)**:

    ```http
      {
        "name": "contentVector",
        "type": "Collection(Edm.Single)",
        "searchable": true,
        "retrievable": true,
        "filterable": false,  
        "sortable": false,  
        "facetable": false,
        "analyzer": "",
        "searchAnalyzer": "",
        "indexAnalyzer": "",
        "normalizer": "",
        "synonymMaps": "", 
        "dimensions": 1536,
        "vectorSearchProfile": "myHnswProfile"
      }
    ```

1. Call [Create or Update Index](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2023-11-01&tabs=HTTP&preserve-view=true) to post the changes.

1. Modify [Search POST](/rest/api/searchservice/documents/search-post?view=rest-searchservice-2023-11-01&tabs=HTTP&preserve-view=true) to change the query syntax. This API change enables support for polymorphic vector query types.

   + Rename `vectors` to `vectorQueries`.
   + For each vector query, add `kind`, setting it to `vector`.
   + For each vector query, rename `value` to `vector`.
   + Optionally, add `vectorFilterMode` if you're using [filter expressions](vector-search-filters.md). The default is  prefilter for indexes created after `2023-10-01`. Indexes created before that date only support postfilter, regardless of how you set the filter mode.

    **Before (2023-07-01-preview)**:

    ```http
    {
        "search": (this parameter is ignored in vector search),
        "vectors": [
          {
            "value": [
                0.103,
                0.0712,
                0.0852,
                0.1547,
                0.1183
            ],
            "fields": "contentVector",
            "k": 5
          }
        ],
        "select": "title, content, category"
    }
    ```

    **After (2023-11-01)**:

    ```http
    {
      "search": "(this parameter is ignored in vector search)",
      "vectorQueries": [
        {
          "kind": "vector",
          "vector": [
            0.103,
            0.0712,
            0.0852,
            0.1547,
            0.1183
          ],
          "fields": "contentVector",
          "k": 5
        }
      ],
      "vectorFilterMode": "preFilter",
      "select": "title, content, category"
    }
    ```

These steps complete the migration to `2023-11-01` stable API version or newer preview API versions.

### Upgrade to 2020-06-30

In this version, there's one breaking change and several behavioral differences. Generally available features include:

+ [Knowledge store](knowledge-store-concept-intro.md), persistent storage of enriched content created through skillsets, created for downstream analysis and processing through other applications. A knowledge store is created through Azure AI Search REST APIs but it resides in Azure Storage.

#### Breaking change

Code written against earlier API versions breaks on `2020-06-30` and later if code contains the following functionality:

+ Any `Edm.Date` literals (a date composed of year-month-day, such as `2020-12-12`) in filter expressions must follow the `Edm.DateTimeOffset` format: `2020-12-12T00:00:00Z`. This change was necessary to handle erroneous or unexpected query results due to timezone differences.

#### Behavior changes

+ [BM25 ranking algorithm](index-ranking-similarity.md) replaces the previous ranking algorithm with newer technology. Services created after 2019 use this algorithm automatically. For older services, you must set parameters to use the new algorithm.

+ Ordered results for null values have changed in this version, with null values appearing first if the sort is `asc` and last if the sort is `desc`. If you wrote code to handle how null values are sorted, be aware of this change.

### Upgrade to 2019-05-06

Features that became generally available in this API version include:

+ [Autocomplete](index-add-suggesters.md) is a typeahead feature that completes a partially specified term input.
+ [Complex types](search-howto-complex-data-types.md) provides native support for structured object data in search index.
+ [JsonLines parsing modes](search-how-to-index-azure-blob-json.md), part of Azure Blob indexing, creates one search document per JSON entity that is separated by a newline.
+ [AI enrichment](cognitive-search-concept-intro.md) provides indexing that uses the AI enrichment engines of Foundry Tools.

#### Breaking changes

Code written against an earlier API version breaks on `2019-05-06` and later if it contains the following functionality:

1. Type property for Azure Cosmos DB. For indexers targeting an [Azure Cosmos DB for NoSQL API](search-how-to-index-cosmosdb-sql.md) data source, change `"type": "documentdb"` to `"type": "cosmosdb"`.

1. If your indexer error handling includes references to the `status` property, you should remove it. We removed status from the error response because it wasn't providing useful information.

1. Data source connection strings are no longer returned in the response. From API versions `2019-05-06` and `2019-05-06-Preview` onwards, the data source API no longer returns connection strings in the response of any REST operation. In previous API versions, for data sources created using POST, Azure AI Search returned **201** followed by the OData response, which contained the connection string in plain text.

1. Named Entity Recognition cognitive skill is retired. If you called the [Name Entity Recognition](cognitive-search-skill-named-entity-recognition.md) skill in your code, the call fails. Replacement functionality is [Entity Recognition Skill (V3)](cognitive-search-skill-entity-recognition-v3.md). Follow the recommendations in [Deprecated skills](cognitive-search-skill-deprecated.md) to migrate to a supported skill.

#### Upgrading complex types

API version `2019-05-06` added formal support for complex types. If your code implemented previous recommendations for complex type equivalency in 2017-11-11-Preview or 2016-09-01-Preview, there are some new and changed limits starting in version `2019-05-06` of which you need to be aware:

+ The limits on the depth of subfields and the number of complex collections per index have been lowered. If you created indexes that exceed these limits using the preview api-versions, any attempt to update or recreate them using API version `2019-05-06` fails. If you find yourself in this situation, you need to redesign your schema to fit within the new limits and then rebuild your index.

+ There's a new limit starting in api-version `2019-05-06` on the number of elements of complex collections per document. If you created indexes with documents that exceed these limits using the preview api-versions, any attempt to reindex that data using api-version `2019-05-06` fails. If you find yourself in this situation, you need to reduce the number of complex collection elements per document before reindexing your data.

For more information, see [Service limits for Azure AI Search](search-limits-quotas-capacity.md).

##### How to upgrade an old complex type structure

If your code is using complex types with one of the older preview API versions, you might be using an index definition format that looks like this:

```json
{
  "name": "hotels",  
  "fields": [
    { "name": "HotelId", "type": "Edm.String", "key": true, "filterable": true },
    { "name": "HotelName", "type": "Edm.String", "searchable": true, "filterable": false, "sortable": true, "facetable": false },
    { "name": "Description", "type": "Edm.String", "searchable": true, "filterable": false, "sortable": false, "facetable": false, "analyzer": "en.microsoft" },
    { "name": "Description_fr", "type": "Edm.String", "searchable": true, "filterable": false, "sortable": false, "facetable": false, "analyzer": "fr.microsoft" },
    { "name": "Category", "type": "Edm.String", "searchable": true, "filterable": true, "sortable": true, "facetable": true },
    { "name": "Tags", "type": "Collection(Edm.String)", "searchable": true, "filterable": true, "sortable": false, "facetable": true, "analyzer": "tagsAnalyzer" },
    { "name": "ParkingIncluded", "type": "Edm.Boolean", "filterable": true, "sortable": true, "facetable": true },
    { "name": "LastRenovationDate", "type": "Edm.DateTimeOffset", "filterable": true, "sortable": true, "facetable": true },
    { "name": "Rating", "type": "Edm.Double", "filterable": true, "sortable": true, "facetable": true },
    { "name": "Address", "type": "Edm.ComplexType" },
    { "name": "Address/StreetAddress", "type": "Edm.String", "filterable": false, "sortable": false, "facetable": false, "searchable": true },
    { "name": "Address/City", "type": "Edm.String", "searchable": true, "filterable": true, "sortable": true, "facetable": true },
    { "name": "Address/StateProvince", "type": "Edm.String", "searchable": true, "filterable": true, "sortable": true, "facetable": true },
    { "name": "Address/PostalCode", "type": "Edm.String", "searchable": true, "filterable": true, "sortable": true, "facetable": true },
    { "name": "Address/Country", "type": "Edm.String", "searchable": true, "filterable": true, "sortable": true, "facetable": true },
    { "name": "Location", "type": "Edm.GeographyPoint", "filterable": true, "sortable": true },
    { "name": "Rooms", "type": "Collection(Edm.ComplexType)" }, 
    { "name": "Rooms/Description", "type": "Edm.String", "searchable": true, "filterable": false, "sortable": false, "facetable": false, "analyzer": "en.lucene" },
    { "name": "Rooms/Description_fr", "type": "Edm.String", "searchable": true, "filterable": false, "sortable": false, "facetable": false, "analyzer": "fr.lucene" },
    { "name": "Rooms/Type", "type": "Edm.String", "searchable": true },
    { "name": "Rooms/BaseRate", "type": "Edm.Double", "filterable": true, "facetable": true },
    { "name": "Rooms/BedOptions", "type": "Edm.String", "searchable": true },
    { "name": "Rooms/SleepsCount", "type": "Edm.Int32", "filterable": true, "facetable": true },
    { "name": "Rooms/SmokingAllowed", "type": "Edm.Boolean", "filterable": true, "facetable": true },
    { "name": "Rooms/Tags", "type": "Collection(Edm.String)", "searchable": true, "filterable": true, "facetable": true, "analyzer": "tagsAnalyzer" }
  ]
}  
```

A newer tree-like format for defining index fields was introduced in API version `2017-11-11-Preview`. In the new format, each complex field has a fields collection where its subfields are defined. In API version 2019-05-06, this new format is used exclusively and attempting to create or update an index using the old format will fail. If you have indexes created using the old format, you'll need to use API version `2017-11-11-Preview` to update them to the new format before they can be managed using API version 2019-05-06.

You can update flat indexes to the new format with the following steps using API version `2017-11-11-Preview`:

1. Perform a GET request to retrieve your index. If it’s already in the new format, you’re done.

1. Translate the index from the flat format to the new format. You have to write code for this task since there's no sample code available at the time of this writing.

1. Perform a PUT request to update the index to the new format. Avoid changing any other details of the index, such as the searchability/filterability of fields, because changes that affect the physical expression of existing index isn't allowed by the Update Index API.

> [!NOTE]
> It isn't possible to manage indexes created with the old "flat" format from the Azure portal. Upgrade your indexes from the “flat” representation to the “tree” representation at your earliest convenience.

## Control plane upgrades

**Applies to:** `2014-07-31-Preview`, `2015-02-28`, and `2015-08-19`

The `listQueryKeys` GET request on older Search Management API versions is now deprecated. We recommend migrating to the most recent stable control plane API version to use the [`listQueryKeys` POST request](/rest/api/searchmanagement/query-keys/list-by-search-service).

1. In existing code, change the `api-version` parameter to the most recent version (`2025-05-01`).

1. Reframe the request from `GET` to `POST`:

   ```http
   POST https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Search/searchServices/{searchServiceName}/listQueryKeys?api-version=2025-05-01
   Authorization: Bearer {{token}}
   ```

1. If you're using an Azure SDK, it's recommended that you upgrade to the latest version.

### Next steps

Review the Search REST API reference documentation. If you encounter problems, ask us for help on [Stack Overflow](https://stackoverflow.com/) or [contact support](https://azure.microsoft.com/support/community/?product=search).

> [!div class="nextstepaction"]
> [Search service REST API Reference](/rest/api/searchservice/)
