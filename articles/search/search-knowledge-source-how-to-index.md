---
title: Create a search index knowledge source
titleSuffix: Azure AI Search
description: A search index knowledge source specifies an index used by a knowledge agent for agentic retrieval workloads.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 08/29/2025
---

# Create a search index knowledge source

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

A *search index knowledge source* specifies a connection to a search index on Azure AI Search that provides searchable content in an agentic retrieval pipeline. It's created independently, and then referenced by a [knowledge agent](search-agentic-retrieval-how-to-create.md) and used at query time when an agent or chat bot calls a [retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-08-01-preview&preserve-view=true) action.

Knowledge sources are new in the 2025-08-01-preview release. You create them first, and then reference them in a knowledge agent.

## Prerequisites

You need a search index containing plain text or vector content, with a semantic configuration, created using the 2025-08-01-preview API and [designed for agentic retrieval](search-agentic-retrieval-how-to-index.md). The search index must be on the same search service as the knowledge agent.

To try the examples in this article, we recommend [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for sending preview REST API calls to Azure AI Search. There's no portal support at this time.

## Check for existing knowledge sources

A knowledge source is a top-level, reusable object. All knowledge sources must be uniquely named within the knowledge sources collection. It's helpful to know about existing knowledge sources for either reuse or for naming new objects.

Example request: List all knowledge sources on a search service by name and type.

```http
# List knowledge sources by name and type
GET {{search-url}}/knowledgeSources?api-version=2025-08-01-preview&$select=name,kind
api-key: {{api-key}}
Content-Type: application/json
```

Example request: Return a single knowledge source by name to review its JSON definition.

```http
### Get a knowledge source definition
GET {{search-url}}/knowledgeSources/{{knowledge-source-name}}?api-version=2025-08-01-preview
api-key: {{api-key}}
Content-Type: application/json
```

An example response for a `searchIndex` knowledge source might look like the following JSON. Notice that the knowledge source specifies a single index name and which fields in the index to include in the query.

```json
{

  "name": "earth-at-night-ks",
  "kind": "searchIndex",
  "description": "Earth at night e-book knowledge source",
  "encryptionKey": null,
  "searchIndexParameters": {
    "searchIndexName": "earth_at_night",
    "sourceDataSelect": "page_chunk,page_number"
  },
  "azureBlobParameters": null,
  "webParameters": null
}
```

> [!NOTE]
> The `webParameters` property isn't operational in this preview and it's reserved for future use.

## Create a knowledge source

To create a knowledge source, use the 2025-08-01-preview data plane REST API or an Azure SDK preview package that provides equivalent functionality.

A knowledge source can contain exactly one of the following: `searchIndexParameters` *or* `azureBlobParameters`. The `webParameters` property isn't supported in this release. If you specify `searchIndexParameters`, then `azureBlobParameters` must be null.

For `searchIndexParameters`:

+ Choose an index [designed for agentic retrieval](search-agentic-retrieval-how-to-index.md)
+ Specify any `retrievable` fields that can be used for citations, such as a file name or page number.

1. Use the [Create or Update Knowledge Source](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-08-01-preview&preserve-view=true) preview REST API.

1. Set environment variables at the top of your file.

    ```http
    @search-url=<YOUR SEARCH SERVICE URL>
    @api-key=<YOUR ADMIN API KEY>
    @ks-name=<YOUR KNOWLEDGE SOURCE NAME>
    @index-name=<YOUR INDEX NAME>
    ```

1. Formulate the request and then **Send**.

    ```http
    POST {{search-url}}/knowledgeSources?api-version=2025-08-01-preview
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

+ `sourceDataSelect` is the list of fields returned if you specify `includeReferenceSourceData` in the knowledge agent definition. These fields are used for the citation view experience and should include fields like a document or file name, page or chapter number, and so forth.

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

## Learn more

+ [Agentic retrieval in Azure AI Search](search-agentic-retrieval-concept.md)

+ [Agentic RAG: build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)

+ [Azure OpenAI Demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
