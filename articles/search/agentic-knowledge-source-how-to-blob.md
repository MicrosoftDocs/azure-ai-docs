---
title: Create a blob knowledge source
titleSuffix: Azure AI Search
description: A blob knowledge source specifies a blob container that you want to read from. It also includes models and properties for creating an indexer, data source, skillset, and index used for agentic retrieval workloads.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 10/13/2025
---

# Create a blob knowledge source

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Use a *blob knowledge source* to index and query Azure blob content in an agentic retrieval pipeline. [Knowledge sources](agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge agent](agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when an agent or chatbot calls a [retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-08-01-preview&preserve-view=true) action at query time.

Unlike a [search index knowledge source](agentic-knowledge-source-how-to-search-index.md), which specifies an existing and qualified index, a blob knowledge source specifies an external data source, models, and properties to automatically generate the following Azure AI Search objects:

+ A data source that represents a blob container.
+ A skillset that chunks and optionally vectorizes multimodal content from the container.
+ An index that stores enriched content and meets the criteria for agentic retrieval.
+ An indexer that uses the previous objects to drive the indexing and enrichment pipeline.

Knowledge sources are new in the 2025-08-01-preview release.

## Prerequisites

+ Azure Storage with a blob container containing [supported content types](search-how-to-index-azure-blob-storage.md#supported-document-formats) for text content. For optional image verbalization, the supported content type depends on whether your chat completion model can analyze and describe the image file.

+ Azure AI Search on the Basic tier or higher with [semantic ranker enabled](semantic-how-to-enable-disable.md).

To try the examples in this article, we recommend [Visual Studio Code](https://code.visualstudio.com/download) with the [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for sending preview REST API calls to Azure AI Search. Currently, there's no portal support.

## Check for existing knowledge sources

[!INCLUDE [Check for existing knowledge sources](includes/how-tos/knowledge-source-check-rest.md)]

The following JSON is an example response for an `azureBlob` knowledge source.

```json
{
  "name": "earth-at-night-blob-ks",
  "kind": "azureBlob",
  "description": "This knowledge source pull from a blob storage container containing pages from the Earth at Night PDF.",
  "encryptionKey": null,
  "searchIndexParameters": null,
  "azureBlobParameters": {
    "connectionString": "<REDACTED>",
    "folderPath": null,
    "disableImageVerbalization": null,
    "identity": null,
    "embeddingModel": {
      "name": "demo-blob-embedding-vectorizer",
      "kind": "azureOpenAI",
      "azureOpenAIParameters": {
        "resourceUri": "<REDACTED>",
        "deploymentId": "text-embedding-ada-002",
        "apiKey": "<REDACTED>",
        "modelName": "text-embedding-ada-002",
        "authIdentity": null
      },
      "customWebApiParameters": null,
      "aiServicesVisionParameters": null,
      "amlParameters": null
    },
    "chatCompletionModel": {
      "kind": "azureOpenAI",
      "azureOpenAIParameters": {
        "resourceUri": "<REDACTED>",
        "deploymentId": "gpt-5-mini",
        "apiKey": "<REDACTED>",
        "modelName": "gpt-5-mini",
        "authIdentity": null
      }
    },
    "ingestionSchedule": null,
    "createdResources": {
      "datasource": "earth-at-night-blob-ks-datasource",
      "indexer": "earth-at-night-blob-ks-indexer",
      "skillset": "earth-at-night-blob-ks-skillset",
      "index": "earth-at-night-blob-ks-index"
    }
  },
  "webParameters": null
}
```

> [!NOTE]
> Sensitive information is redacted. The generated resources appear at the end of the response. The `webParameters` property isn't operational in this preview and is reserved for future use.

## Create a knowledge source

To create an `azureBlob` knowledge source:

1. Set environment variables at the top of your file.

    ```http
    @search-url = <YOUR SEARCH SERVICE URL>
    @api-key = <YOUR SEARCH ADMIN API KEY>
    @ks-name = <YOUR KNOWLEDGE SOURCE NAME>
    @connection-string = <YOUR FULL ACCESS CONNECTION STRING TO AZURE STORAGE>
    @container-name = <YOUR BLOB CONTAINER NAME>
    ```

1. Use the 2025-08-01-preview of [Knowledge Sources - Create or Update (REST API)](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-08-01-preview&preserve-view=true) or an Azure SDK preview package that provides equivalent functionality to formulate the request.

    ```http
    PUT {{search-url}}/knowledgeSources/earth-at-night-blob-ks?api-version=2025-08-01-preview
    api-key: {{api-key}}
    Content-Type: application/json
    
    {
      "name": "{{ks-name}}",
      "kind": "azureBlob",
      "description": "This knowledge source pulls from a blob storage container containing pages from the Earth at Night PDF.",
      "encryptionKey": null,
      "azureBlobParameters": {
        "connectionString": "{{connection-string}}",
        "containerName": "{{container-name}}",
        "folderPath": null,
        "disableImageVerbalization": null,
        "identity": null,
        "embeddingModel": {
          // Redacted for brevity
        },
        "chatCompletionModel": {
          // Redacted for brevity
        },
        "ingestionSchedule": {
          // Redacted for brevity
        }
      }
    }
    ```

1. Select **Send Request**.

**Key points:**

+ `name` must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search.

+ `kind` must be `azureBlob` for a blob knowledge source.

+ `encryptionKey` (optional) is an encryption key in Azure Key Vault. Use this property to doubly encrypt sensitive information in both the knowledge source and the generated objects.

+ `embeddingModel` (optional) is a text embedding model that vectorizes text and image content during indexing and at query time. Use a model supported by the [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md), [Azure AI Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md), [AML skill](cognitive-search-aml-skill.md), or [Custom Web API skill](cognitive-search-custom-skill-web-api.md). The embedding skill will be included in the generated skillset, and its equivalent vectorizer will be included in the generated index.

+ `chatCompletionModel` (optional) is a chat completion model that verbalizes images or extracts content. Use a model supported by the [GenAI Prompt skill](cognitive-search-skill-genai-prompt.md), which will be included in the generated skillset. To skip image verbalization, omit this object and set `"disableImageVerbalization": true`.

+ `ingestionSchedule` (optional) adds scheduling information to the generated indexer. You can also [add a schedule](search-howto-schedule-indexers.md) later to automate data refresh.

+ If you get errors, make sure the embedding and chat completion models exist at the endpoints you provided.

## Review the created objects

When you create a blob knowledge source, your search service also creates an indexer, data source, skillset, and index. Exercise caution when you edit these objects, as introducing an error or incompatibility can break the pipeline.

After you create a knowledge source, the response lists the created objects. These objects are created according to a fixed template, and their names are based on the name of the knowledge source. You can't change the object names.

We recommend using the Azure portal to validate output creation. The workflow is:

1. Check the indexer for success or failure messages. Connection or quota errors appear here.
1. Check the index for searchable content. Use Search Explorer to run queries.
1. Check the skillset to learn how your content is chunked and optionally vectorized.
1. Modify the data source if you want to change connection details, such as authentication and authorization. Our example uses API keys for simplicity, but you can use Microsoft Entra ID authentication and role-based access.

## Assign to a knowledge agent

If you're satisfied with the index, continue to the next step: specify the knowledge source in a [knowledge agent](agentic-retrieval-how-to-create-knowledge-base.md).

Within the knowledge agent, there are more properties to set on the knowledge source that are specific to query operations.

After the knowledge agent is configured, use the retrieve action to query the knowledge source.

## Delete a knowledge source

[!INCLUDE [Delete knowledge source](includes/how-tos/knowledge-source-delete-rest.md)]

## Related content

+ [Azure AI Search Blob knowledge source Python sample](https://github.com/Azure/azure-search-vector-samples/blob/main/demo-python/code/knowledge/blob-knowledge-source.ipynb)

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)

+ [Agentic RAG: build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)

+ [Azure OpenAI Demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)