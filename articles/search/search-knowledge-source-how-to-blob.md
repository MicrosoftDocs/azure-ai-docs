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

A blob knowledge source specifies a connection to a container on Azure Storage that provides searchable content to an agentic retrieval pipeline. It's created independently, and then referenced by a [knowledge agent](search-agentic-retrieval-how-to-create.md) and used at query time.

Knowledge sources are new in the 2025-08-01-preview release. In this release, a knowledge agent can use multiple knowledge sources. It's now possible to query multiple knowledge sources in the same request.

## Prerequisites

+ A search index containing plain text or vector content, with a semantic configuration, created using the 2025-08-01-preview API. The search index must be on the same search service as the knowledge agent 

+ A knowledge agent that connects to the knowledge source

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

A response for blob knowledge source might look like the following example. Notice that the knowledge source specifies a single index name and which fields in the index to include in the query.

```json

{
  "name": "earth-at-night-ks-blob",
  "kind": "azureBlob",
  "description": "This is a blob storage container containing pages from the Earth at Night PDF.",
  "encryptionKey": null,
  "searchIndexParameters": null,
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
    "createdResources": {
      "datasource": "earth-at-night-ks-blob-datasource",
      "indexer": "earth-at-night-ks-blob-indexer",
      "skillset": "earth-at-night-ks-blob-skillset",
      "index": "earth-at-night-ks-blob-index"
    }
  },
  "webParameters": null
}
```

## Create a knowledge source

To create an agent, use the 2025-08-01-preview data plane REST API or an Azure SDK preview package that provides equivalent functionality.

+ Choose an index [designed for agentic retrieval](search-agentic-retrieval-how-to-index.md)
+ Specify searchable fields by name, or leave empty to include all searchable fields

```http
@search-url=<YOUR SEARCH SERVICE URL>
@ks-name=<YOUR KNOWLEDGE SOURCE NAME>
@index-name=<YOUR INDEX NAME>
@api-key=<YOUR ADMIN API KEY>

POST {{endpoint}}/knowledgeSources?api-version={{api-version}}
api-key: {{api-key}}
Content-Type: application/json

{
    "name" : "{{ks-name}}",
    "kind" : "searchIndex",
    "description" : "Earth at night e-book knowledge source",
    "searchIndexParameters" :{
      "searchIndexName" : "{{index-name}}",
      "sourceDataSelect" : "page_chunk,page_number"
    }
}
```

**Key points**:

+ `name` must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects on Azure AI Search.

+ `sourceDataSelect` consists of searchable fields, either plain text or vector.

## Delete a knowledge source

If you no longer need the knowledge source, or if you need to rebuild it on the search service, use this request to delete the current object.

```http
# Delete agent
DELETE https://{{search-url}}/knowledgeSources/{{ks-name}}?api-version=2025-08-01-preview
api-key: {{api-key}}
```

## Learn more

+ [Agentic retrieval in Azure AI Search](search-agentic-retrieval-concept.md)

+ [Agentic RAG: build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)

+ [Azure OpenAI Demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)