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
An indexer-based indexing pipeline.
An index that accepts the output of the indexer pipeline.
A supported data source having content that you want to chunk. 
A **Document Intelligence Layout** skill that splits documents based on paragraph boundaries.
An Azure Open AI Embedding skill that generate vector embeddings  
An index projection for one-to-many indexing

## Create an index for one-to-many indexing

You can use the Azure portal, REST APIs, or an Azure SDK to create an index.
Here's an example payload


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
An index must exist on the search service before you create the skillset or run the indexer


## Define skillsets for semantic chunking and vectorization

Here's an example payload for a skillset definition that you might use to project individual markdown sections and its vector output by the **Document Intelligence Layout** skill and Azure Open AI Embedding skill as their own documents in the search index.

```json
{
  "skills": [
    {
      "@odata.type": "#Microsoft.Skills.Util.DocumentIntelligenceLayoutSkill",
      "name": "document-intelligence-layout-skill",
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
      "name": "azure-openai-embedding-skill",
      "description": "Custom Azure OpenAI Embedding Skill",
      "context": "/document/markdownDocument/*",
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
  "name": "index-projection",
  "description": "A skillset for semantic chunking and vectorization",
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
Once you have created a data source, indexes, and skillset, you're ready to create and run the indexer. This step puts the pipeline into execution.

You can query your search index after processing concludes to test your solution.

```json
{
  "name": "ipidxr-jzrpok",
  "dataSourceName": "ipds-yojaui",
  "targetIndexName": "ipidx-jngcnu",
  "skillsetName": "ipss-knnbwj",
  "parameters": {
    "maxFailedItems": -1,
    "maxFailedItemsPerBatch": 0,
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
      "sourceFieldName": "/document/markdownDocument",
      "targetFieldName": "markdownDocument"
    }
  ]
}
```

## Verify results

Run a query against the index to check the results of image processing. Use [Search Explorer](search-explorer.md) as a search client, or any tool that sends HTTP requests. The following query selects fields that contain the output of image processing.

```http
POST /indexes/[index name]/docs/search?api-version=[api-version]
{
    "search": "*",
    "select": "metadata_storage_name, text, layoutText, imageCaption, imageTags"
}
```



## See also

+ [Create indexer (REST)](/rest/api/searchservice/indexers/create)
+ [Image Analysis skill](cognitive-search-skill-image-analysis.md)
+ [OCR skill](cognitive-search-skill-ocr.md)
+ [Text merge skill](cognitive-search-skill-textmerger.md)
+ [How to define a skillset](cognitive-search-defining-skillset.md)
+ [How to map enriched fields](cognitive-search-output-field-mapping.md)
