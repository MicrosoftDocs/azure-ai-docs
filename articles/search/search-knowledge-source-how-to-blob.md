---
title: Create a blob knowledge source
titleSuffix: Azure AI Search
description: A blob knowledge source specifies a blob container that you want to read from. It also includes models and properties for creating an indexer, data source, skillset, and index used for agentic retrieval workloads.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 08/29/2025
---

# Create a blob knowledge source

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

A *blob knowledge source* specifies all of the information necessary for indexing and querying multimodal Azure blob content in an Azure AI Search agentic pipeline. It's created independently, and then referenced by a [knowledge agent](search-agentic-retrieval-how-to-create.md) and used at query time when an agent or chat bot calls a [retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-08-01-preview&preserve-view=true) action.

In contrast with a [search index knowledge source](search-knowledge-source-how-to-index.md) that specifies an existing and qualified index, a blob knowledge source specifies an external data source (a blob container) plus models and properties that are used to create an entire enrichment pipeline:

+ The generated data source specifies the blob container
+ The generated skillset chunks and vectorizes multimodal content
+ The generated index stores indexed content and meets the criteria for agentic retrieval
+ The generated indexer drives the indexing and enrichment pipeline

The generated index provides the content that's used by a knowledge agent.

Knowledge sources are new in the 2025-08-01-preview release.

## Prerequisites

You need a blob container containing [supported content types](search-howto-indexing-azure-blob-storage.md#supported-document-formats) for text content. For images, the supported content type depends on your chat completion model and whether it an analyze and describe the image file.

To try the examples in this article, we recommend [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for sending preview REST API calls to Azure AI Search. There's no portal support at this time.

## Check for existing knowledge sources

A knowledge source is a top-level, reusable object. All knowledge sources must be uniquely named within the knowledge sources collection. It's helpful to know about existing knowledge sources for either reuse or for naming new objects.

The following request lists knowledge sources by name and type.

```http
# List knowledge sources by name and type
GET {{search-url}}/knowledgeSources?api-version=2025-08-01-preview&$select=name,kind
api-key: {{api-key}}
Content-Type: application/json
```

You can also return a single knowledge source by name to review its JSON definition.

```http
### Get a knowledge source definition
GET {{search-url}}/knowledgeSources/{{knowledge-source-name}}?api-version=2025-08-01-preview
api-key: {{api-key}}
Content-Type: application/json
```

A response for blob knowledge source might look like the following example. 

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
        "deploymentId": "gpt-4o-mini",
        "apiKey": "<REDACTED>",
        "modelName": "gpt-4o-mini",
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
> Sensitive information is redacted. The generated resources appear at the end of the response. The `webParameters` property isn't operational in this preview and it's reserved for future use.

## Create a knowledge source

To create a knowledge source, use the 2025-08-01-preview data plane REST API or an Azure SDK preview package that provides equivalent functionality.

A knowledge source can contain exactly one of the following: `searchIndexParameters` *or* `azureBlobParameters`. The `webParameters` property isn't supported in this release. If you specify `azureBlobParameters`, then `searchIndexParameters` must be null.

For `azureBlobParameters`:

+ Provide a connection to Azure AI Search
+ Provide a full access connection string for Azure Storage and the container name
+ Provide a text embedding model. This model is used to vectorize text content during indexing and queries.
+ Provide a chat completion model used for describing image content.
+ Provide an encryption key to doubly encrypt sensitive information in this knowledge source and in the generated resources.

Models are referenced in the skillset and as vectorizer for encoding text strings at query time.

A blob knowledge source can include an `ingestionSchedule` that adds scheduling information to an indexer. You can also [add a schedule](search-howto-schedule-indexers.md) later if you want to automate data refresh

1. Use the [Create or Update Knowledge Source](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-08-01-preview&preserve-view=true) preview REST API.

1. Set environment variables at the top of your file.

    ```http
    @search-url=<YOUR SEARCH SERVICE URL>
    @api-key=<YOUR SEARCH ADMIN API KEY>
    @connection-string=<YOUR FULL ACCESS CONNECTION STRING TO AZURE STORAGE>
    @aoai-endpoint=<YOUR AZURE OPENAI ENDPOINT>
    @aoai-key=<YOUR AZURE OPENAI API KEY>
    ```

1. Formulate the request and then **Send**.

    ```http
    PUT {{search-url}}/knowledgeSources/earth-at-night-blob-ks?api-version=2025-08-01-preview
    api-key: {{api-key}}
    Content-Type: application/json
    
    {
      "name": "earth-at-night-blob-ks",
      "kind": "azureBlob",
      "description": "This knowledge source pull from a blob storage container containing pages from the Earth at Night PDF.",
      "encryptionKey": null,
      "azureBlobParameters": {
        "connectionString": "{{connection-string}}",
        "containerName": "nasa-ebook",
        "folderPath": null,
        "disableImageVerbalization": null,
        "identity": null,
        "embeddingModel": {
          "kind": "azureOpenAI",
          "azureOpenAIParameters": {
            "resourceUri": "{{aoai-endpoint}}",
            "deploymentId": "text-embedding-3-small",
            "apiKey": "{{aoai-key}}",
            "modelName": "text-embedding-3-small",
            "authIdentity": null
          },
          "customWebApiParameters": null,
          "aiServicesVisionParameters": null,
          "amlParameters": null
        },
        "chatCompletionModel": {
          "kind": "azureOpenAI",
          "azureOpenAIParameters": {
            "resourceUri": "{{aoai-endpoint}}",
            "deploymentId": "gpt-4o-mini",
            "apiKey": "{{aoai-key}}",
            "modelName": "gpt-4o-mini",
            "authIdentity": null
          }
        },
        "ingestionSchedule": {
          "interval": "P1D",
          "startTime": "2025-01-07T19:30:00Z"
      }
    }
    ```

If you get errors, make sure the embedding model and chat completion models exist at the endpoint you provided.

## Check output

When you create a blob knowledge source, the search service also creates the following objects: an indexer, data source, skillset, and index. Exercise caution when editing these objects because you can break the pipeline if you introduce an error or incompatibility.

The response on knowledge source creation lists the created resources. Objects are created according to a fixed template and naming is based on the knowledge source. You can't change the object names.

We recommend using the Azure portal to validate output creation.

1. Check the indexer for success or failure messages. Connection or quota errors appear here. If the indexer failed, try reset and rerun.

1. Check the index for searchable content. Use Search Explorer to run your queries.

1. Check the skillset to learn more about how your content is chunked and vectorized.

1. Modify the data source if you want to change connection details, such as authentication and authorization. The example uses API keys for simplicity but you can use Microsoft Entra ID authentication and role-based access.

## Assign to a knowledge agent

If you're satisfied with the index, continue to the next step: specifying the knowledge source in a [knowledge agent](search-agentic-retrieval-how-to-create.md).

Within the knowledge agent, there are more properties to set on the knowledge source that are specific to query operations.

## Delete a knowledge source

If you no longer need the knowledge source, or if you need to rebuild it on the search service, use this request to delete the current object.

```http
# Delete agent
DELETE {{search-url}}/knowledgeSources/{{ks-name}}?api-version=2025-08-01-preview
api-key: {{api-key}}
```

> [!IMPORTANT]
> Before you can delete a knowledge source, you must first update the knowledge agent to remove all references to the knowledge source.
>
> Deleting a blob knowledge source also deletes the objects it created. The indexer, data source, skillset, and index are automatically deleted when the blob knowledge source is deleted.
>

## Learn more

+ [Agentic retrieval in Azure AI Search](search-agentic-retrieval-concept.md)

+ [Agentic RAG: build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)

+ [Azure OpenAI Demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)