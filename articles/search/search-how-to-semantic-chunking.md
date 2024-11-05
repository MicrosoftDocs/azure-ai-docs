---
title: Semantic Chunking and vectorization
titleSuffix: Azure AI Search
description: Use skill set and index projection to do semantic chunking, vectorization, and write into a search index in Azure AI Search pipelines.
author: rawan
ms.author: rawan
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 10/12/2024
ms.custom:
  - references_regions
---

# Semantic chunking and vectorization using the Document Layout skill and index projections

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Text data chunking strategies play a key role in optimizing the RAG response and performance. Semantic chunking is to find semantically coherent fragments of a sentence representation. These fragments can then be processed independently and recombined as semantic representations without loss of information, interpretation, or semantic relevance. The inherent meaning of the text is used as a guide for the chunking process. Markdown is a structured and formatted markup language and a popular input for enabling semantic chunking in RAG (Retrieval-Augmented Generation)

The Document Layout skill offers a comprehensive solution for advanced content extraction and chunk functionality. With the Layout skill, you can easily extract document layout and content as markdown format and utilize markdown parsing mode to produce a set of document chunks

This article shows:
+ How to use the Document Layout skill to extract markdown sections
+ How to apply split skill to constrain chunk size within each markdown section 
+ Generate embeddings for the content within those sections
+ How to use index projections to compile and write them into a search index.

## Prerequisites

+ An [indexer-based indexing pipeline](search-indexer-overview.md).
+ An index that accepts the output of the indexer pipeline.
+ A [supported data source](search-indexer-overview.md#supported-data-sources) having content that you want to chunk. 
+ A [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md) that splits documents based on paragraph boundaries.
+ An [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md) that generates vector embeddings  
+ An [index projection](search-how-to-define-index-projections.md) for one-to-many indexing

## Prepare data files

The raw inputs must be in a [supported data source](search-indexer-overview.md#supported-data-sources) and the file needs to be a format which [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md) supports.

+ Supported file format: PDF, JPEG, JPG, PNG, BMP, TIFF, DOCX, XLSX,PPTX,HTML

You can use the Azure portal, REST APIs, or an Azure SDK to [create a data source](search-howto-indexing-azure-blob-storage.md).

## Create an index for one-to-many indexing

Here's an example payload of a single designed around chunks. In this example, parent fields are the text_parent_id. Child fields are the vector and nonvector chunk of the markdown section.

You can use the Azure portal, REST APIs, or an Azure SDK to [create an index](search-how-to-load-search-index.md).

An index must exist on the search service before you create the skill set or run the indexer

```json
{
  "name": "my_consolidated_index",
  "fields": [
    {
      "name": "chunk_id",
      "type": "Edm.String",
      "searchable": true,
      "filterable": false,
      "retrievable": true,
      "stored": true,
      "sortable": true,
      "facetable": false,
      "key": true,
      "analyzer": "keyword"
    },
    {
      "name": "text_parent_id",
      "type": "Edm.String",
      "searchable": false,
      "filterable": true,
      "retrievable": true,
      "stored": true,
      "sortable": false,
      "facetable": false,
      "key": false
    },
    {
      "name": "chunk",
      "type": "Edm.String",
      "searchable": true,
      "filterable": false,
      "retrievable": true,
      "stored": true,
      "sortable": false,
      "facetable": false,
      "key": false
    },
    {
      "name": "title",
      "type": "Edm.String",
      "searchable": true,
      "filterable": false,
      "retrievable": true,
      "stored": true,
      "sortable": false,
      "facetable": false,
      "key": false
    },
    {
      "name": "header_1",
      "type": "Edm.String",
      "searchable": true,
      "filterable": false,
      "retrievable": true,
      "stored": true,
      "sortable": false,
      "facetable": false,
      "key": false
    },
    {
      "name": "header_2",
      "type": "Edm.String",
      "searchable": true,
      "filterable": false,
      "retrievable": true,
      "stored": true,
      "sortable": false,
      "facetable": false,
      "key": false
    },
    {
      "name": "header_3",
      "type": "Edm.String",
      "searchable": true,
      "filterable": false,
      "retrievable": true,
      "stored": true,
      "sortable": false,
      "facetable": false,
      "key": false
    },
    {
      "name": "text_vector",
      "type": "Collection(Edm.Single)",
      "searchable": true,
      "filterable": false,
      "retrievable": true,
      "stored": true,
      "sortable": false,
      "facetable": false,
      "key": false,
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

## Define skill set for semantic chunking and vectorization

You can use the REST APIs to [create or update a skill set](cognitive-search-defining-skillset.md).

Here's an example skill set definition payload to project individual markdown sections chunks and their vector outputs as documents in the search index using the [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md) and [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md)

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
          "targetName": "markdownDocument"
        }
      ],
      "markdownHeaderDepth": "h3"
    },
    {
      "@odata.type": "#Microsoft.Skills.Text.SplitSkill",
      "name": "my_markdown_section_split_skill",
      "description": "A skill that splits text into chunks",
      "context": "/document/markdownDocument/*",
      "inputs": [
        {
          "name": "text",
          "source": "/document/markdownDocument/*/content",
          "inputs": []
        }
      ],
      "outputs": [
        {
          "name": "textItems",
          "targetName": "pages"
        }
      ],
      "defaultLanguageCode": "en",
      "textSplitMode": "pages",
      "maximumPageLength": 2000,
      "pageOverlapLength": 500,
      "unit": "characters"
    },
    {
      "@odata.type": "#Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill",
      "name": "my_azure_openai_embedding_skill",
      "context": "/document/markdownDocument/*/pages/*",
      "inputs": [
        {
          "name": "text",
          "source": "/document/markdownDocument/*/pages/*",
          "inputs": []
        }
      ],
      "outputs": [
        {
          "name": "embedding",
          "targetName": "text_vector"
        }
      ],
      "resourceUri": "https://<subdomain>.openai.azure.com",
      "deploymentId": "text-embedding-3-small",
      "apiKey": "<Azure OpenAI api key>",
      "modelName": "text-embedding-3-small"
    }
  ],
  "cognitiveServices": {
    "@odata.type": "#Microsoft.Azure.Search.CognitiveServicesByKey",
    "key": "<Cognitive Services api key>"
  },
  "indexProjections": {
    "selectors": [
      {
        "targetIndexName": "my_consolidated_index",
        "parentKeyFieldName": "text_parent_id",
        "sourceContext": "/document/markdownDocument/*/pages/*",
        "mappings": [
          {
            "name": "text_vector",
            "source": "/document/markdownDocument/*/pages/*/text_vector"
          },
          {
            "name": "chunk",
            "source": "/document/markdownDocument/*/pages/*"
          },
          {
            "name": "title",
            "source": "/document/title"
          },
          {
            "name": "header_1",
            "source": "/document/markdownDocument/*/sections/h1"
          },
          {
            "name": "header_2",
            "source": "/document/markdownDocument/*/sections/h2"
          },
          {
            "name": "header_3",
            "source": "/document/markdownDocument/*/sections/h3"
          }
        ]
      }
    ],
    "parameters": {
      "projectionMode": "skipIndexingParentDocuments"
    }
  }
}

```

## Run the indexer
Once you create a data source, indexes, and skill set, you're ready to [create and run the indexer](search-howto-create-indexers.md#run-the-indexer). This step puts the pipeline into execution.

When using the [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md), make sure to set the following parameters on the indexer definition:
+ The `allowSkillsetToReadFileData` parameter should be set to "true."
+ the `parsingMode` parameter should be set to "default."

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
        "dataToExtract": "contentAndMetadata",
        "parsingMode": "default",
        "allowSkillsetToReadFileData": true
    }
  },
  "fieldMappings": [
    {
      "sourceFieldName": "metadata_storage_path",
      "targetFieldName": "title"
    }
  ],
  "outputFieldMappings": []
}
```

## Verify results
You can query your search index after processing concludes to test your solution.

To check the results, run a query against the index. Use [Search Explorer](search-explorer.md) as a search client, or any tool that sends HTTP requests. The following query selects fields that contain the output of markdown section nonvector content and its vector.

```http
POST /indexes/[index name]/docs/search?api-version=[api-version]
{
    "search": "*",
    "select": "metadata_storage_path, markdown_section, vector"
}
```

## See also

+ [Create a data source](search-howto-indexing-azure-blob-storage.md)
+ [Define an index projection](search-how-to-define-index-projections.md)
+ [How to define a skill set](cognitive-search-defining-skillset.md)
+ [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md)
+ [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md)
+ [Create indexer (REST)](/rest/api/searchservice/indexers/create)
+ [Search Explorer](search-explorer.md)

