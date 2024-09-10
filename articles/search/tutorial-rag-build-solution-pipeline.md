---
title: 'RAG Tutorial: Build an indexing pipeline'
titleSuffix: Azure AI Search
description: Create an indexer-driven pipeline that loads, chunks, embeds, and ingests content for RAG solutions on Azure AI Search.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: cognitive-search
ms.topic: tutorial
ms.date: 09/12/2024

---

# Tutorial: Build an indexing pipeline (RAG in Azure AI Search)

In this tutorial, learn how to build an automated indexing pipeline for a RAG solution on Azure AI Search.

An indexer drives indexing and skillset execution that provides [integrated data chunking and vectorization](vector-search-integrated-vectorization.md) on a one-time or recurring basis for incremental updates. You create an indexer, data source connection, skillset, and provide the index schema you created in the previous tutorial. This exercise uses Azure Blob storage as the data source.

If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/?WT.mc_id=A261C142F) before you begin.

<!-- Objective:

- Create objects and run the indexer to produce an operational search index with chunked and vectorized content.

Key points:

- Dependency on a supported data source. Use Azure blob storage for this tutorial.
- Indexer pulls from the data source, pushes to the index.
- Large PDF files can't be chunked. Indexer shows success, but doesn't even attempt to chunk/ingest the docs. Individual files have to be less than 16 MB.
- Skillset (example 1) has two skills: text split and embedding. Embedding model is also be used for vectorization at query time (assume text-to-vector conversion).
- Skillset (example 2) add a custom skill that points to external embedding model, or document intelligence.
- Skillset (example 3) add an entity recognition skill to lift locations from raw content into the index?
- Duplicated content is expected due to overlap and repetition of parent info. It won't affect your LLM.

Tasks:

- H2: Configure access to Azure Storage and upload sample data.
- H2: Create a data source
- H2: Create a skillset (choose one skillset)
- H2: Use alternative skillsets (present the other two skillsets)
- H2: Create and run the indexer
- H2: Check your data in the search index (hide vectors) -->

<!-- 
## Prerequisites

TBD

## Create a blob data source

1. Create a baseline data source definition with required elements. Provide a valid connection string to your Azure Storage account. Provide the name of the container that has the sample data.

    ```http
    ### Create a data source
    POST {{baseUrl}}/datasources?api-version=2024-05-01-preview  HTTP/1.1
      Content-Type: application/json
      Authorization: Bearer {{token}}
    
        {
            "name": "demo-rag-ds",
            "description": null,
            "type": "azureblob",
            "subtype": null,
            "credentials": {
                "connectionString": "{{storageConnectionString}}"
            },
            "container": {
                "name": "{{blobContainer}}",
                "query": null
            },
            "dataChangeDetectionPolicy": null,
            "dataDeletionDetectionPolicy": null
        }
    ```

1. Review the [Datasource REST API](/rest/api/searchservice/data-sources/create) for information about other properties. For more information about blob indexers, see [Index data from Azure Blob Storage](search-howto-indexing-azure-blob-storage.md).

1. Send the request to save the data source to Azure AI Search.

## Create an indexer

1. Create a baseline indexer definition with required elements. In this example, the indexer is disabled so that it doesn't immediately run when it's saved to the search service. In later steps, you'll add a skillset and output field mappings, and run the indexer once it's fully specified.

   ```http
    ### Create and run an indexer
    POST {{baseUrl}}/indexers?api-version=2023-11-01  HTTP/1.1
      Content-Type: application/json
      Authorization: Bearer {{token}}

       {   
        "name" : "demo-rag-idxr",  
        "dataSourceName" : "demo-rag-ds",  
        "targetIndexName" : "demo-rag-index",  
        "skillsetName" : null,
        "disabled" : true,
        "fieldMappings" : null,
        "outputFieldMappings" : null
        }
   ```

1. Review the [Indexer REST API](/rest/api/searchservice/indexers/create) for information about other properties. For more information about indexers, see [Create an indexer](search-howto-create-indexers.md).

1. Send the request to save the data source to Azure AI Search.

## About indexer execution

An indexer connects to a supported data source, retrieves data, serializes it into JSON, calls a skillset, and populates a predefined index with raw content from the source and generated content from a skillset.

An indexer requires a data source and an index, and accepts a skillset definition. All of these objects are distinct. 

- An indexer object provides configuration information and field mappings.
- A data source has connection information.
- An index is the destination of an indexer pipeline and it defines the physical structure of your data in Azure AI Search.
- A skillset is optional, but necessary for RAG workloads if you want integrated data chunking and vectorization.

If you're already familiar with indexers and data sources, the definitions don't change in a RAG solution. 

## Checklist for indexer execution

Before you run an indexer, review this checklist to avoid problems during indexing. This checklist applies equally to RAG and non-RAG scenarios:

- Is the data source accessible to Azure AI Search? Check network configuration and permissions. Indexers connect under a search service identity. Consider configuring your search service for a managed identity and then granting it read permissions. 
- Does the data source support change tracking? Enable it so that your search service can keep your index up to date.
- Is the data ready for indexing? Indexers consume a single table (or view), or a collection of documents from a single directory. You can either consolidate files into one location, or you could create multiple data sources and indexers that send data to the same index.
- Do you need vectorization? Most RAG apps built on Azure AI Search include vector content in the index to support similarity search and hybrid queries. If you need vectorization and chunking, create a skillset and add it to your indexer.
- Do you need field mappings? If source and destination field names or types are different, add field mappings. 
- If you have a skillset that generates content that you need to store in your index, add output field mappings. Data chunks fall into this category. More information about output field mappings is covered in the skillset exercise.

## Check index

duplicated content in the index

chunks aren't intended for classic search experience. Chunks might start or end mid-sentence or contain duplicated content if you specified an overlap.

Combined index means duplicated parent fields. Document grain is the chunk so each chunk has its copy of parent fields.
Overlapping text also duplicates content.

All of this duplicated content is acceptable for LLMS because they aren't returning verbatim results.

if you're sending search results directly to a search page, it's a poor experience.
 -->

## Next step

> [!div class="nextstepaction"]
> [Chat with your data](tutorial-rag-build-solution-query.md)