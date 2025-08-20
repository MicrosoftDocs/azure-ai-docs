---
title: Create a blob knowledge source
titleSuffix: Azure AI Search
description: A blob knowledge source specifies one or more Azure blobs to associate with a knowledge agent for agentic retrieval workloads.
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

A blob knowledge source has these components:

+ A blob container and connection string
+ An embedding model used to vectorize any text content
+ A chat completion model used for image verbalizations

Knowledge sources are new in the 2025-08-01-preview release. In this release, a knowledge agent can use multiple knowledge sources. It's now possible to query multiple knowledge sources in the same request.

## Prerequisites

You need a blob container containing [supported content types](search-howto-indexing-azure-blob-storage.md#supported-document-formats) for text content. For images, the supported content type is determined by your chat completion model and the image formats it supports.

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
  "name": "earth-at-night-ks-blob",
  "kind": "azureBlob",
  "description": "This is a blob storage container containing pages from the Earth at Night PDF.",
  "azureBlobParameters": {
    "connectionString": "<redacted>",
    "containerName": "nasa-ebook",
    "folderPath": null,
    "disableImageVerbalization": null,
    "identity": null,
    "embeddingModel": {
      "name": "demo-blob-embedding-vectorizer",
      "kind": "azureOpenAI",
      "azureOpenAIParameters": {
        "resourceUri": "https://demo-openai-eus.openai.azure.com",
        "deploymentId": "text-embedding-3-small",
        "apiKey": "<redacted>",
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
        "resourceUri": "https://demo-openai-eus.openai.azure.com",
        "deploymentId": "gpt-4o-mini",
        "apiKey": "<redacted>",
        "modelName": "gpt-4o-mini",
        "authIdentity": null
      }
    },
    "ingestionSchedule": null,
  }
}
```

## Create a knowledge source

To create an agent, use the 2025-08-01-preview data plane REST API or an Azure SDK preview package that provides equivalent functionality.

+ Provide a connection to Azure AI Search
+ Provide a full access connection string for Azure Storage and the container name
+ Provide an embedding model, either a text embedding model or a multimodal embedding model. This model is used to vectorize content during indexing and queries.
+ Provide a chat completion model used for describing image content.

Models are referenced in the skillset and as vectorizer for encoding text strings at query time.

You can include a schedule definition if you want to automate data refresh for the indexer.

```http
@search-url=<YOUR SEARCH SERVICE URL>
@api-key=<YOUR SEARCH ADMIN API KEY>
@connection-string=<YOUR FULL ACCESS CONNECTION STRING TO AZURE STORAGE>
@aoai-endpoint=<YOUR AZURE OPENAI ENDPOINT>
@aoai-key=<YOUR AZURE OPENAI API KEY>

PUT {{search-url}}/agents/?api-version=2025-08-01-preview
api-key: {{api-key}}
Content-Type: application/json

{
  "name": "earth-at-night-ks-blob",
  "kind": "azureBlob",
  "description": "This is a blob storage container containing pages from the Earth at Night PDF.",
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
    "ingestionSchedule": null,
  }
}
```

If you get errors, make sure the embedding model and chat completion models exist at the endpoint you provided.

## Resources created by a knowledge source

When you create a blob knowledge source, the search service also creates the following objects: an indexer, data source, skillset, and index. Objects are created according to a fixed template. Be cautious about editing these objects because you can break the pipeline if you introduce an error or incompatibility.

The response on knowledge source creation lists the created resources.

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