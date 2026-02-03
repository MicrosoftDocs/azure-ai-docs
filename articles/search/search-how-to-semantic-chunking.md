---
title: Chunk and Vectorize by Document Layout
titleSuffix: Azure AI Search
description: Chunk textual content by headings and semantically coherent fragments, generate embeddings, and send the results to a searchable index.
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 01/16/2026
ms.custom:
  - references_regions
  - ignite-2024
---

# Chunk and vectorize by document layout or structure

Text data chunking strategies play a key role in optimizing RAG responses and performance. By using the **Document Layout** skill, you can chunk content based on document structure, capturing headings and chunking the content body based on semantic coherence, such as paragraphs and sentences. Chunks are processed independently. Because LLMs work with multiple chunks, when those chunks are of higher quality and semantically coherent, the overall relevance of the query is improved.

The Document Layout skill calls the [layout model](/azure/ai-services/document-intelligence/prebuilt/layout) from Azure Document Intelligence in Foundry Tools. The model articulates content structure in JSON using Markdown syntax (headings and content), with fields for headings and content stored in a search index on Azure AI Search. The searchable content produced from the Document Layout skill is plain text but you can apply integrated vectorization to generate embeddings for any field in your source documents, including images.

In this article, learn how to:

> [!div class="checklist"]
> + Use the Document Layout skill to recognize document structure
> + Use the Text Split skill to constrain chunk size to each Markdown section
> + Generate embeddings for each chunk
> + Use index projections to map embeddings to fields in a search index

For illustration purposes, this article uses the [sample health plan PDFs](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/health-plan) uploaded to Azure Blob Storage and then indexed using the **Import data (new)** wizard.

## Prerequisites

+ [An indexer-based indexing pipeline](search-indexer-overview.md) with an index that accepts the output. The index must have fields for receiving headings and content.

+ [An index projection](search-how-to-define-index-projections.md) for one-to-many indexing.

+ [A supported data source](search-indexer-overview.md#supported-data-sources) having text content that you want to chunk.

+ A skillset with these two skills:

  + [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md) that splits documents based on paragraph boundaries. If you use [key-based billing](cognitive-search-attach-cognitive-services.md), this skill requires Microsoft Foundry to be in the same region as Azure AI Search for AI enrichment. Region requirements are relaxed for keyless billing (preview).

  + [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md) that generates vector embeddings. This skill *doesn't* have region requirements.

## Prepare data files

You must use a [supported data source](search-indexer-overview.md#supported-data-sources) for the raw inputs, and the file must be in a format supported by the [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md).

+ Supported file formats include PDF, JPEG, JPG, PNG, BMP, TIFF, DOCX, XLSX, PPTX, and HTML.

+ Supported indexers are any indexer that can handle the supported file formats. These indexers include [Blob indexers](search-how-to-index-azure-blob-storage.md), [Microsoft OneLake indexers](search-how-to-index-onelake-files.md), and [File indexers](search-file-storage-integration.md).

+ Supported regions for the portal experience of this feature include East US, West Europe, and North Central US. If you're setting up your skillset programmatically, you can use any Azure Document Intelligence region that also provides the AI enrichment feature of Azure AI Search. For more information, see [Supported regions for the Document Layout skill](cognitive-search-skill-document-intelligence-layout.md#supported-regions).

You can use the Azure portal, REST APIs, or an Azure SDK package to [create a data source](search-how-to-index-azure-blob-storage.md).

> [!TIP]
> To try the Document Layout skill and structure-aware chunking on your own search service, upload the [health plan PDF](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/health-plan) sample files to your supported data source. The [**Import data (new)** wizard](search-get-started-portal-import-vectors.md) is an easy code-free approach for trying out this skill. Be sure to select the **default parsing mode** to use structure-aware chunking. Otherwise, the [Markdown parsing mode](search-how-to-index-azure-blob-markdown.md) is used.

## Create an index for one-to-many indexing

The following example shows a single search document designed around chunks. When you work with chunks, you need a chunk field and a parent field that identifies the chunk's origin. In this example, parent fields are the `text_parent_id` fields. Child fields are the vector and nonvector chunks of the Markdown section.

The Document Layout skill outputs headings and content. In this example, `header_1` through `header_3` store document headings, as detected by the skill. Other content, such as paragraphs, is stored in `chunk`. The `text_vector` field is a vector representation of the chunk field content.

You can use the **Import data (new)** wizard in the Azure portal, REST APIs, or an Azure SDK to [create an index](search-how-to-load-search-index.md). The following index is very similar to what the wizard creates by default. You might have more fields if you add image vectorization.

If you aren't using the wizard, the index must exist on the search service before you create the skillset or run the indexer.

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

## Define a skillset for structure-aware chunking and vectorization

The following example shows a skillset definition that projects individual Markdown sections, chunks, and their vector equivalents as fields in the search index. It uses the [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md) to detect headings and populate a content field based on semantically coherent paragraphs and sentences in the source document. It uses the [Text Split skill](cognitive-search-skill-textsplit.md) to split the Markdown content into chunks. It uses the [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md) to vectorize chunks and any other field for which you want embeddings.

Besides skills, the skillset includes `indexProjections` and `cognitiveServices`:

+ `indexProjections` are used for indexes containing chunked documents. The projections specify how parent-child content is mapped to fields in a search index for one-to-many indexing. For more information, see [Define an index projection](search-how-to-define-index-projections.md).

+ `cognitiveServices` [attaches a Microsoft Foundry resource](cognitive-search-attach-cognitive-services.md) for billing purposes. The Document Layout skill is available through [Standard pricing](https://azure.microsoft.com/pricing/details/ai-document-intelligence/).

```https
POST {endpoint}/skillsets?api-version=2025-09-01

{
  "name": "my_skillset",
  "description": "A skillset for structure-aware chunking and vectorization with an index projection around markdown section",
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

## Configure and run the indexer

After you create a data source, index, and skillset, [create and run the indexer](search-howto-create-indexers.md#run-the-indexer). This step puts the pipeline into execution.

When you use the [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md), set the following parameters on the indexer definition:

+ Set the `allowSkillsetToReadFileData` parameter to `true`.
+ Set the `parsingMode` parameter to `default`.

You don't need to set `outputFieldMappings` in this scenario because `indexProjections` handle the source field to search field associations. Index projections handle field associations for the Document Layout skill and also regular chunking with the split skill for imported and vectorized data workloads. You still need output field mappings for transformations or complex data mappings with functions which apply in other cases. However, for n-chunks per document, index projections handle this functionality natively.

Here's an example of an indexer creation request.

```https
POST {endpoint}/indexers?api-version=2025-09-01

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

When you send the request to the search service, the indexer runs.

## Verify results

You can query your search index after processing concludes to test your solution.

To check the results, run a query against the index. Use [Search Explorer](search-explorer.md) as a search client, or any tool that sends HTTP requests. The following query selects fields that contain the output of Markdown section nonvector content and its vector.

For Search Explorer, you can copy just the JSON and paste it into the JSON view for query execution.

```http
POST /indexes/[index name]/docs/search?api-version=[api-version]
{
  "search": "copay for in-network providers",
  "count": true,
  "searchMode": "all",
  "vectorQueries": [
    {
      "kind": "text",
      "text": "*",
      "fields": "text_vector,image_vector"
    }
  ],
  "queryType": "semantic",
  "semanticConfiguration": "healthplan-doc-layout-test-semantic-configuration",
  "captions": "extractive",
  "answers": "extractive|count-3",
  "select": "header_1, header_2, header_3"
}
```

If you used the health plan PDFs to test this skill, Search Explorer results for the example query should look similar to the results in the following screenshot. 

+ The query is a [hybrid query](hybrid-search-how-to-query.md) over text and vectors, so you see a `@search.rerankerScore` and results are ranked by that score. `searchMode=all` means that *all* query terms must be considered for a match (the default is *any*).

+ The query uses semantic ranking, so you see `captions`. It also has `answers`, but they aren't shown in the screenshot. The results are the most semantically relevant to the query input, as determined by the [semantic ranker](semantic-search-overview.md).

+ The `select` statement (not shown in the screenshot) specifies the header fields that the Document Layout skill detects and populates. You can add more fields to the select clause to inspect the content of chunks, title, or any other human readable field.

:::image type="content" source="media/search-how-to-semantic-chunking/query-results-doc-layout.png" lightbox="media/search-how-to-semantic-chunking/query-results-doc-layout.png" alt-text="Screenshot of hybrid query results that include doc layout skill output fields.":::

## Related content

+ [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md)
+ [Text Split skill](cognitive-search-skill-textsplit.md)
+ [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md)
+ [Define an index projection for parent-child indexing](search-how-to-define-index-projections.md)
