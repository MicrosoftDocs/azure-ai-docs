---
title: Define index projections
titleSuffix: Azure AI Search
description: Index projections specify how parent-child content is mapped to fields in a search index when you use integrated vectorization for data chunking.
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: how-to
ms.date: 01/30/2026
ms.update-cycle: 180-days
---

# Define an index projection for parent-child indexing

If you're chunking content for either a RAG pattern or vectorization, you can specify an **index projection** to control *one-to-many indexing*, where source content (one) is projected to one or more indexes (many). The intent of an index projection is to control whether elements of the parent document, such as a file name or creation date:

- Repeat for each child (chunk) in a single index
- Are indexed as standalone search documents in the same index
- Or, are ingested into separate indexes

We recommend repeating parent fields in a single index because having different document shapes or splitting content into two indexes can be difficult to query, especially in classic search where index joins aren't supported.

In Azure AI Search, chunking is performed by skills and thus depends on indexers. To define an index projection, specify it in a [skillset](cognitive-search-working-with-skillsets.md).

## Prerequisites

- Azure AI Search, any tier or region.

- An [indexer-based indexing pipeline](search-indexer-overview.md).

- A [supported data source](search-indexer-overview.md#supported-data-sources) having content that you want to chunk.

- An index (one or many) that accepts the output of the indexer pipeline.

- A skill that [chunks content](vector-search-how-to-chunk-documents.md), such as the [Text Split skill](cognitive-search-skill-textsplit.md). 

The skillset contains the indexer projection that shapes the data for one-to-many indexing. A skillset could also have other skills, such as an embedding skill like [AzureOpenAIEmbedding](cognitive-search-skill-azure-openai-embedding.md) if your scenario includes integrated vectorization.

## Choose an approach

Index projections generate "child" documents (chunks) for each "parent" document. Choose how to handle parent content:

| Approach | Description | Configuration |
|----------|-------------|---------------|
| **Single index, repeating parent fields** (recommended) | Parent fields repeat for each chunk. All documents have a uniform shape. | Set both indexer `targetIndexName` and index projection `targetIndexName` to the same index. Set `projectionMode` to `skipIndexingParentDocuments`. |
| **Single index, mixed document shapes** | Parent documents and chunk documents coexist. Parent documents have null chunk fields. | Set both `targetIndexName` values to the same index. Set `projectionMode` to `includeIndexingParentDocuments` (or omit, as it's the default). |
| **Two or more separate indexes** | Parent index for metadata lookups, child index for search. No query-time joins. | Set indexer `targetIndexName` to parent index. Set index projection `targetIndexName` to child index. The `selectors` array determines the quantity and composition of the child index. |

For most RAG scenarios, use the first approach. See the [classic RAG example](https://github.com/Azure-Samples/azure-search-classic-rag/blob/main/README.md).

### Implementation steps for the recommended approach

1. [Create an index](#create-an-index-for-one-to-many-indexing) designed for chunks, with parent fields included.
1. [Create a skillset](#add-index-projections-to-a-skillset) with a chunking skill and `indexProjections`.
1. [Create an indexer](search-how-to-create-indexers.md) pointing to your [supported data source](search-indexer-overview.md#supported-data-sources).

If your data source supports change tracking, the indexer synchronizes changes automatically.

## Create an index for one-to-many indexing

Whether you create one index for chunks that repeat parent values, or separate indexes for parent-child field placement, the primary index used for searching is designed around data chunks. The index schema must have the following fields:

- A document key field uniquely identifying each document. It must be defined as type `Edm.String` with the `keyword` analyzer.

- A field associating each chunk with its parent. It must be of type `Edm.String`. It can't be the document key field, and must have `filterable` set to true. It's referred to as parent_id in the examples and as a [projected key value](#projected-key-value) in this article.

- Other fields for content, such as text or vectorized chunk fields.

An index must exist on the search service before you create the skillset or run the indexer. The `selectors` you define in the skillset should include these fields.

### Single index schema inclusive of parent and child fields

A single index designed around chunks with parent content repeating for each chunk is the predominant pattern for RAG and vector search scenarios. The ability to associate the correct parent content with each chunk is enabled through index projections.

The following schema is an example that meets the requirements for index projections. In this example:

- Parent fields are the parent_id and the title, and they repeat for each chunk
- Child fields are the vector and nonvector vector chunks. The chunk_id is the document ID of this index.

You can use the Azure portal, REST APIs, or an Azure SDK to [create an index](search-how-to-load-search-index.md).

#### [**REST**](#tab/rest-create-index)

Use a REST client or the Azure portal **Add index** action and JSON option to create the index.

```json
{
    "name": "my_consolidated_index",
    "fields": [
        {"name": "chunk_id", "type": "Edm.String", "key": true, "filterable": true, "analyzer": "keyword"},
        {"name": "parent_id", "type": "Edm.String", "filterable": true},
        {"name": "title", "type": "Edm.String", "searchable": true, "filterable": true, "sortable": true, "retrievable": true},
        {"name": "chunk", "type": "Edm.String","searchable": true,"retrievable": true},
        {"name": "chunk_vector", "type": "Collection(Edm.Single)", "searchable": true, "retrievable": false, "stored": false, "dimensions": 1536, "vectorSearchProfile": "hnsw"}
    ],
    "vectorSearch": {
        "algorithms": [{"name": "hnsw", "kind": "hnsw", "hnswParameters": {}}],
        "profiles": [{"name": "hnsw", "algorithm": "hnsw"}]
    }
}
```

#### [**Python**](#tab/python-create-index)

This example is similar to the [classic RAG example](https://github.com/Azure-Samples/azure-search-classic-rag/blob/main/README.md). It's an index schema designed for chunked content extracted from a parent document and combines all parent-child fields in the same index.

```python
 # Create a search index  
 index_name = "my_consolidated_index"
 index_client = SearchIndexClient(endpoint=AZURE_SEARCH_SERVICE, credential=credential)  
 fields = [
     SearchField(name="document_id", type=SearchFieldDataType.String, key=True, sortable=True, filterable=True, facetable=True, analyzer_name="keyword"),  
     SearchField(name="parent_id", type=SearchFieldDataType.String, filterable=True),  
     SearchField(name="title", type=SearchFieldDataType.String, searchable=True, sortable=False, filterable=True, facetable=False, retrievable=True), 
     SearchField(name="chunk", type=SearchFieldDataType.String, sortable=False, filterable=False, facetable=False, retrievable=True),  
     SearchField(name="chunk_vector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single, searchable=True, retrievable=False), vector_search_dimensions=1024, vector_search_profile_name="myHnswProfile")
     ]  

 # Configure the vector search configuration  
 vector_search = VectorSearch(  
     algorithms=[  
         HnswAlgorithmConfiguration(name="myHnsw"),
     ],  
     profiles=[  
         VectorSearchProfile(  
             name="myHnswProfile",  
             algorithm_configuration_name="myHnsw",  
             vectorizer_name="myOpenAI",  
         )
     ],  
     vectorizers=[  
         AzureOpenAIVectorizer(  
             vectorizer_name="myOpenAI",  
             kind="azureOpenAI",  
             parameters=AzureOpenAIVectorizerParameters(  
                 resource_url=AZURE_OPENAI_ACCOUNT,  
                 deployment_name="text-embedding-3-large",
                 model_name="text-embedding-3-large"
             ),
         ),  
     ], 
 )  

 # Create the search index
 index = SearchIndex(name=index_name, fields=fields, vector_search=vector_search)  
 result = index_client.create_or_update_index(index)  
 print(f"{result.name} created")  
```

---

## Add index projections to a skillset

Index projections are defined inside a skillset definition and are primarily defined as an array of `selectors`, where each selector corresponds to a different target index on the search service. This section starts with syntax and examples for context, followed by [parameter reference](#parameter-reference). 

#### [**REST**](#tab/rest-create-index-projection)

Index projections are generally available. We recommend the most recent stable API:

- [Create Skillset (api-version=2025-09-01)](/rest/api/searchservice/skillsets/create)

Here's an example payload for an index projections definition that you might use to project individual pages output by the [Text Split skill](cognitive-search-skill-textsplit.md) as their own documents in the search index.

```json
"indexProjections": {
    "selectors": [
        {
            "targetIndexName": "my_consolidated_index",
            "parentKeyFieldName": "parent_id",
            "sourceContext": "/document/pages/*",
            "mappings": [
                {
                    "name": "chunk",
                    "source": "/document/pages/*",
                    "sourceContext": null,
                    "inputs": []
                },
                {
                    "name": "chunk_vector",
                    "source": "/document/pages/*/chunk_vector",
                    "sourceContext": null,
                    "inputs": []
                },
                {
                    "name": "title",
                    "source": "/document/title",
                    "sourceContext": null,
                    "inputs": []
                }
            ]
        }
    ],
    "parameters": {
        "projectionMode": "skipIndexingParentDocuments"
    }
}
```

#### [**Python**](#tab/python-create-index-projection)

We recommend the [latest stable package](https://pypi.org/project/azure-search-documents/) for index projections.

```python
index_projections = SearchIndexerIndexProjection(  
    selectors=[  
        SearchIndexerIndexProjectionSelector(  
            target_index_name=index_name,  
            parent_key_field_name="parent_id",  
            source_context="/document/pages/*",  
            mappings=[  
                InputFieldMappingEntry(name="chunk", source="/document/pages/*"),  
                InputFieldMappingEntry(name="chunk_vector", source="/document/pages/*/chunk_vector"),
                InputFieldMappingEntry(name="title", source="/document/title")
            ],  
        ),  
    ],  
    parameters=SearchIndexerIndexProjectionsParameters(  
        projection_mode=IndexProjectionMode.SKIP_INDEXING_PARENT_DOCUMENTS  
    ),  
) 
```

#### [**.NET**](#tab/dotnet-create-index)

For .NET developers, use the [IndexProjections Class](/dotnet/api/azure.search.documents.indexes.models.searchindexerskillset.indexprojection?view=azure-dotnet&preserve-view=true) in the Azure.Search.Documents client library.

---

### Parameter reference

| Index projection parameters | Definition |
|----------------------------|------------|
| `selectors` | An array with parameters for the main search corpus, usually the index designed around chunks. You can send content to multiple child indexes by specifying multiple selectors. The index schemas must exist on the search service before you run the indexer. |
| `parameters` | A parameter dictionary of index projection-specific configuration properties. |

Parameters have the following elements as part of their definition.

| Parameters | Definition |
|----------------------------|------------|
| `parameters.projectionMode` | An optional parameter providing instructions to the indexer. Valid values include `includeIndexingParentDocuments` and `skipIndexingParentDocuments`. <br><br>The best value for this parameter is `skipIndexingParentDocuments`. You should use it when chunked documents are the primary search target. <br><br>If you don't set `skipIndexingParentDocuments` for `projectionMode`, you get `includeIndexingParentDocuments` automatically because it's the default. It adds extra search documents in your index that are null for chunks, but populated with parent-specific content. For example, if five PDFs contribute 100 chunks to the index, then the number of documents in the index is 105. The five documents created for parent fields have nulls for chunk (child) fields, making them substantially different from the bulk of the documents in the index. For this reason, we recommend `projectionMode` set to `skipIndexingParentDocuments`. |

Selectors have the following elements as part of their definition.

| Selectors | Definition |
|-----------|------------|
| `selectors.targetIndexName` | The name of the index into which index data is projected. It's either the single chunked index with repeating parent fields, or it's the child index if you're using [separate indexes](#example-of-separate-parent-child-indexes) for parent-child content. |
| `selectors.parentKeyFieldName` | The name of the field providing the key for the parent document.|
| `selectors.sourceContext` | The enrichment annotation that defines the granularity at which to map data into individual search documents. For more information, see [Skill context and input annotation language](cognitive-search-skill-annotation-language.md). |
| `selectors.mappings` | An array of mappings of enriched data to fields in the search index. Each mapping consists of: <br>`name`: The name of the field in the search index that the data should be indexed into. <br>`source`: The enrichment annotation path that the data should be pulled from. <br><br>Each `mapping` can also recursively define data with an optional `sourceContext` and `inputs` field, similar to the [knowledge store](knowledge-store-concept-intro.md) or [Shaper Skill](cognitive-search-skill-shaper.md). Depending on your application, these parameters allow you to shape data into fields of type `Edm.ComplexType` in the search index. Some LLMs don't accept a complex type in search results, so the LLM you're using determines whether a complex type mapping is helpful or not.|

The `mappings` parameter is important. You must explicitly map every field in the child index, except for the ID fields such as document key and the parent ID. 

This requirement is in contrast with other field mapping conventions in Azure AI Search. For some data source types, the indexer can implicitly map fields based on similar names, or known characteristics (for example, blob indexers use the unique metadata storage path as the default document key). However, for indexer projections, you must explicitly specify every field mapping on the "many" side of the relationship.

> [!IMPORTANT]
> Don't create a field mapping for the parent key field. Doing so disrupts change tracking and synchronized data refresh.

## Review field mappings

Indexers are affiliated with three different types of field mappings. Before you run the indexer, check your field mappings and know when to use each type.

[Field mappings](search-indexer-field-mappings.md) are defined in an indexer and used to map a source field to an index field. Field mappings are used for data paths that lift data from the source and pass it in for indexing, with no intermediate skills processing step. Typically, an indexer can automatically map fields that have the same name and type. Explicit field mappings are only required when there's discrepancies. In one-to-many indexing and the patterns discussed thus far, you might not need field mappings.

[Output field mappings](cognitive-search-output-field-mapping.md) are defined in an indexer and used to map enriched content generated by a skillset to a field into the main index. Chunks are considered enriched content due to creation by a skill (Text Split), but you don't need an output field mapping for chunks, or for index projections that are defined by a selector mapping.

[Selectors.mappings](#parameter-reference) are defined in a skillset and map to fields in the child index. In cases where the child index also includes parent fields (as in the [consolidated index solution](#single-index-schema-inclusive-of-parent-and-child-fields)), you should set up field mappings for every field that has content, including the parent-level title field, assuming you want the title to show up in each chunked document. If you're using [separate parent and child indexes](#example-of-separate-parent-child-indexes), the selector should have field mappings for just the child-level fields.

> [!NOTE]
> Both output field mappings and selector mappings accept enriched document tree nodes as source inputs. Knowing how to specify a path to each node is essential to setting up the data path. To learn more about path syntax, see [Reference a path to enriched nodes](cognitive-search-concept-annotations-syntax.md) and [skillset definition](cognitive-search-working-with-skillsets.md#skillset-definition) for examples.

## Run the indexer

Once you have created a data source, indexes, and skillset, you're ready to [create and run the indexer](search-howto-create-indexers.md#run-the-indexer). This step puts the pipeline into execution. 

You can query your search index after processing concludes to test your solution.

## Content lifecycle

Depending on the underlying data source, an indexer can usually provide ongoing change tracking and deletion detection. This section explains the content lifecycle of one-to-many indexing as it relates to data refresh.

For data sources that provide change tracking and deletion detection, an indexer process can pick up changes in your source data. Each time you run the indexer and skillset, the index projections are updated if the skillset or underlying source data has changed. Any changes picked up by the indexer are propagated through the enrichment process to the projections in the index, ensuring that your projected data is a current representation of content in the originating data source. Data refresh activity is captured in a projected key value for each chunk. This value gets updated when the underlying data changes.

> [!NOTE]
> While you can manually edit the data in the projected documents using the [index push API](search-how-to-load-search-index.md), you should avoid doing so. Manual updates to an index are overwritten on the next pipeline invocation, assuming the document in source data is updated and the data source has change tracking or deletion detection enabled.

### Updated content

If you add new content to your data source, new chunks or child documents are added to the index on the next indexer run.

If you modify existing content in the data source, chunks are updated incrementally in the search index if the data source you're using supports change tracking and deletion detection. For example, if a word or sentence changes in a document, the chunk in the target index that contains that word or sentence is updated on the next indexer run. Other types of updates, such as changing a field type and some attributions, aren't supported for existing fields. For more information about allowed updates, see [Update an index schema](search-howto-reindex.md#update-an-index-schema).

Some data sources like [Azure Storage](search-how-to-index-azure-blob-changed-deleted.md) support change and deletion tracking by default, based on the timestamp. Other data sources such as [Microsoft OneLake](search-how-to-index-onelake-files.md), [Azure SQL](search-how-to-index-sql-database.md), or [Azure Cosmos DB](search-how-to-index-cosmosdb-sql.md) must be configured for change tracking.

### Deleted content

If the source content no longer exists (for example, if text is shortened to have fewer chunks), the corresponding child document in the search index is deleted. The remaining child documents also get their key updated to include a new hash value, even if their content didn't otherwise change.

If a parent document is completely deleted from the datasource, the corresponding child documents only get deleted if the deletion is detected by a `dataDeletionDetectionPolicy` defined on the datasource definition. If you don't have a `dataDeletionDetectionPolicy` configured and need to delete a parent document from the datasource, then you should [manually delete the child documents](search-how-to-delete-documents.md) if they're no longer wanted.

### Projected key value

To ensure data integrity for updated and deleted content, data refresh in one-to-many indexing relies on a *projected key value* on the "many" side. If you're using integrated vectorization or the [**Import data (new)** wizard](search-import-data-portal.md), the projected key value is the `parent_id` field in a chunked or "many" side of the index.

A projected key value is a unique identifier that the indexer generates for each document. It ensures uniqueness and allows for change and deletion tracking to work correctly. This key contains the following segments:

- A random hash to guarantee uniqueness. This hash changes if the parent document is updated on subsequent indexer runs.
- The parent document's key.
- The enrichment annotation path that identifies the context for the generated document.

For example, if you split a parent document with key value "aa1b22c33" into four pages, and then each of those pages is projected as its own document via index projections:

- aa1b22c33
- aa1b22c33_pages_0
- aa1b22c33_pages_1
- aa1b22c33_pages_2

If the parent document is updated in the source data, perhaps resulting in more chunked pages, the random hash changes, more pages are added, and the content of each chunk is updated to match whatever is in the source document.

## Example of separate parent-child indexes

This section shows an example for separate parent and child indexes. It's an uncommon pattern, but it's possible you might have application requirements that are best met using this approach. In this scenario, you're projecting parent-child content into two separate indexes.

1. Create two index schemas.

   Each schema has the fields for its particular grain, with the parent ID field common to both indexes for use in a [lookup query](/rest/api/searchservice/documents/get). The primary search corpus is the child index, but you can issue a lookup query to retrieve the parent fields for each match in the result. Azure AI Search doesn't support joins at query time, so your application code or orchestration layer would need to merge or collate results that can be passed to an app or process.

    The parent index has a parent_id field and title. The parent_id is the document key. You don't need vector search configuration unless you want to vectorize fields at the parent document level.
    
    ```json
    {
        "name": "my-parent-index",
        "fields": [
    
            {"name": "parent_id", "type": "Edm.String", "key":true, "filterable": true},
            {"name": "title", "type": "Edm.String", "searchable": true, "filterable": true, "sortable": true, "retrievable": true}
        ]
    }
    ```
    
    The child index has the chunked fields, plus the parent_id field. If you're using integrated vectorization, scoring profiles, semantic ranker, or analyzers you would set these in the child index.
    
    ```json
    {
        "name": "my-child-index",
        "fields": [
            {"name": "chunk_id", "type": "Edm.String", "key": true, "filterable": true, "analyzer": "keyword"},
            {"name": "parent_id", "type": "Edm.String", "filterable": true},
             {"name": "chunk", "type": "Edm.String","searchable": true,"retrievable": true},
            {"name": "chunk_vector", "type": "Collection(Edm.Single)", "searchable": true, "retrievable": false, "stored": false, "dimensions": 1536, "vectorSearchProfile": "hnsw"}
        ],
        "vectorSearch": {
            "algorithms": [{"name": "hsnw", "kind": "hnsw", "hnswParameters": {}}],
            "profiles": [{"name": "hsnw", "algorithm": "hnsw"}]
        },
        "scoringProfiles": [],
        "semanticConfiguration": [],
        "analyzers": []
    }
    ```

1. Update the indexer to specify parent-index as the target.

    The indexer definition specifies the components of the pipeline. In the indexer definition, the index name to provide is the parent index. If you need field mappings for the parent-level fields, define them in outputFieldMappings. For one-to-many indexing that uses separate indexes, the indexer definition might look like the following example. 
    
    ```json
    {
      "name": "my-indexer",
      "dataSourceName": "my-ds",
      "targetIndexName": "my-parent-index",
      "skillsetName" : "my-skillset",
      "parameters": { },
      "fieldMappings": (optional) Maps fields in the underlying data source to fields in an index,
      "outputFieldMappings" : (required) Maps skill outputs to fields in an index,
    }
    ```

1. Add `indexProjections` to the skillset.

    Here's an example of an index projection definition that specifies the data path the indexer should use to index content. It specifies the child index name in the index projection definition, and it specifies the mappings of every child or chunk-level field. This is the only place the child index name is specified.

    Notice that `parameters` is null and is using the default `includeIndexingParentDocuments`. The indexer populates the parent index. The `selectors` array is used to project the chunk documents to the child index. 
    
    ```json
    "indexProjections": {
        "selectors": [
            {
                "targetIndexName": "my-child-index",
                "parentKeyFieldName": "parent_id",
                "sourceContext": "/document/pages/*",
                "mappings": [
                    {
                        "name": "chunk",
                        "source": "/document/pages/*",
                        "sourceContext": null,
                        "inputs": []
                    },
                    {
                        "name": "chunk_vector",
                        "source": "/document/pages/*/chunk_vector",
                        "sourceContext": null,
                        "inputs": []
                    }
                ]
            }
        ],
        "parameters": {}
    }
    ```

1. [Run the indexer](search-howto-run-reset-indexers.md). If you previously ran the indexer, remember to reset it first.

   You should have two indexes populated with the appropriate content. Query the indexes in Search Explorer to verify each one has the correct content.

## Next step

Data chunking and one-to-many indexing are part of the classic RAG pattern in Azure AI Search. Continue on to the following tutorial and code sample to learn more about it.

> [!div class="nextstepaction"]
> [How to build a classic RAG solution using Azure AI Search](https://github.com/Azure-Samples/azure-search-classic-rag/blob/main/README.md)
