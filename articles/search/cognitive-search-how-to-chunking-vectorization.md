---
title: Semantic Chunking and vectorization
titleSuffix: Azure AI Search
description: Use skillset and index projection to do semantic chunking, vectorization and write into a search index in Azure AI Search pipelines.
author: rawan
ms.author: rawan
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 10/12/2024
ms.custom:
  - ignite-2024
---

# Semantic Chunking and Vectorization using Document Intelligence Layout skill and index projection
Text data chunking strategies play a key role in optimizing the RAG response and performance. Semantic chunking is to find semantically coherent fragments of a sentence representation. These fragments can then be processed independently and recombined as semantic representations without loss of information, interpretation, or semantic relevance. The inherent meaning of the text is used as a guide for the chunking process. Markdown is a structured and formatted markup language and a popular input for enabling semantic chunking in RAG (Retrieval-Augmented Generation)

The Document Intelligence Layout skill offers a comprehensive solution for advanced content extraction and chunk functionality. With the Layout skill, you can easily extract document layout and content as markdown format and utilize markdown parsing mode to produce a set of document chunks

This article explains how to use document intelligence layout skill to get markdown sections, then generate embeddings for content in markdown sections , Finally, use index projections to compose them and write into a search index.

## Prerequisites
An [indexer-based indexing pipeline](search-indexer-overview.md).
An index that accepts the output of the indexer pipeline.
A [supported data source](search-indexer-overview.md#supported-data-sources) having content that you want to chunk. 
A [Document Intelligence Layout skill](cognitive-search-skill-document-intelligence-layout.md) that splits documents based on paragraph boundaries.
An [Azure Open AI Embedding skill](cognitive-search-skill-azure-openai-embedding.md) that generate vector embeddings  
An [index projection](search-how-to-define-index-projections.md) for one-to-many indexing

## Prepare data files

The raw inputs must be in a [supported data source](search-indexer-overview.md#supported-data-sources) and the file needs to be a format which [Document Intelligence Layout skill](cognitive-search-skill-document-intelligence-layout.md) supports.

+ Supported file format: PDF, JPEG, JPG, PNG, BMP, TIFF, DOCX, XLSX,PPTX,HTML

You can use the Azure portal, REST APIs, or an Azure SDK to [create a data source](search-howto-indexing-azure-blob-storage.md).

## Create an index for one-to-many indexing

Here's an example payload of a single designed around chunks. In this example, parent fields are the parent_id. Child fields are the vector and nonvector chunk - the markdown section.

You can use the Azure portal, REST APIs, or an Azure SDK to [create an index](search-how-to-load-search-index.md).

An index must exist on the search service before you create the skillset or run the indexer

```json
{
  "name": "my_consolidated_index",
  "fields": [
    {
      "name": "chunk_id",
      "type": "Edm.String",
      "key": true,
      "filterable": true,
      "analyzer": "keyword"
    },
    {
      "name": "parent_id",
      "type": "Edm.String",
      "filterable": true
    },
    {
      "name": "markdown_section",
      "type": "Edm.String",
      "searchable": true,
      "retrievable": true
    },
    {
      "name": "vector",
      "type": "Collection(Edm.Single)",
      "retrievable": false,
      "searchable": true,
      "dimensions": 1536,
      "stored": false,
      "vectorSearchProfile": "profile"
    }
  ],
  "vectorSearch": {
    "profiles": [
      {
        "name": "profile",
        "algorithm": "algorithm"
      }
    ],
    "algorithms": [
      {
        "name": "algorithm",
        "kind": "hnsw"
      }
    ]
  }
}
```

## Define skillsets for semantic chunking and vectorization

You can use the REST APIs to [create or update a skillset](cognitive-search-defining-skillset.md).

Here's an example payload for a skillset definition that you might use to project individual markdown sections and its vector output by the [Document Intelligence Layout skill](cognitive-search-skill-document-intelligence-layout.md) and [Azure Open AI Embedding skill](cognitive-search-skill-azure-openai-embedding.md) as their own documents in the search index.

```json
{
  "name": "my_skillset",
  "description": "A skillset for semantic chunking and vectorization with a indexprojection around markdown section",
  "skills": [
    {
      "@odata.type": "#Microsoft.Skills.Util.DocumentIntelligenceLayoutSkill",
      "name": "my_document_intelligence_layout_skill",
      "context": "/document",
      "outputMode": "oneToMany",
      "inputs": [
        {
          "name": "file_data",
          "source": "/document/file_data"
        }
      ],
      "outputs": [
        {
          "name": "markdown_document",
          "targetName": "markdown_sections"
        }
      ],
      "markdownHeaderDepth": "h6"
    },
    {
      "@odata.type": "#Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill",
      "name": "my_azure_openai_embedding_skill",
      "description": "Custom Azure OpenAI Embedding Skill",
      "context": "/document/markdown_sections/*",
      "resourceUri": "<Azure Open AI resource endpoint>",
      "deploymentId": "<Azure Open AI Embedding Deployment Id>",
      "apiKey": "<Azure Open AI Key>",
      "inputs": [
        {
          "name": "text",
          "source": "/document/markdown_sections/*/content"
        }
      ],
      "outputs": [
        {
          "name": "embedding",
          "targetName": "embedding"
        }
      ],
      "modelName": "text-embedding-ada-002"
    }
  ],
  "indexProjections": {
    "selectors": [
      {
        "targetIndexName": "my_consolidated_index",
        "parentKeyFieldName": "parent_id",
        "sourceContext": "/document/markdown_sections/*",
        "mappings": [
          {
            "name": "markdown_section",
            "source": "/document/markdown_sections/*/content"
          },
          {
            "name": "vector",
            "source": "/document/markdown_sections/*/embedding"
          }
        ]
      }
    ]
  }
}

```

## Run the indexer
Once you have created a data source, indexes, and skillset, you're ready to [create and run the indexer](search-howto-create-indexers.md#run-the-indexer). This step puts the pipeline into execution.

Here's an example payload

```json
{
  "name": "my_indexer",
  "dataSourceName": "my_blob_datasource",
  "targetIndexName": "my_consolidated_index",
  "skillsetName": "my_skillset",
  "parameters": {
    "batchSize": 1,
    "configuration": {
      "dataToExtract": "allMetadata",
      "allowSkillsetToReadFileData": true
    }
  },
  "fieldMappings": [
    {
      "sourceFieldName": "metadata_storage_path",
      "targetFieldName": "id",
      "mappingFunction": {
        "name": "base64Encode"
      }
    }
  ],
  "outputFieldMappings": [
    {
      "sourceFieldName": "/document/markdown_section",
      "targetFieldName": "markdown_section"
    }
  ]
}
```

## Verify results
You can query your search index after processing concludes to test your solution.

Run a query against the index to check the results. Use [Search Explorer](search-explorer.md) as a search client, or any tool that sends HTTP requests. The following query selects fields that contain the output of markdown section nonvector content and its vector.

```http
POST /indexes/[index name]/docs/search?api-version=[api-version]
{
    "search": "*",
    "select": "metadata_storage_path, markdown_section, vector"
}
```

## See also
+ [create a data source](search-howto-indexing-azure-blob-storage.md)
+ [Define an index projection](search-how-to-define-index-projections.md)
+ [How to define a skillset](cognitive-search-defining-skillset.md)
+ [Document Intelligence Layout skill](cognitive-search-skill-document-intelligence-layout.md)
+ [Azure Open AI Embedding skill](cognitive-search-skill-azure-openai-embedding.md)
+ [Create indexer (REST)](/rest/api/searchservice/indexers/create)
+ [Search Explorer](search-explorer.md)

