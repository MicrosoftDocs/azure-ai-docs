---
title: Create a search index knowledge source
titleSuffix: Azure AI Search
description: A search index knowledge source specifies an index used by a knowledge agent for agentic retrieval workloads.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 10/10/2025
---

# Create a search index knowledge source

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

A *search index knowledge source* specifies a connection to an Azure AI Search index that provides searchable content in an agentic retrieval pipeline. [Knowledge sources](agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge agent](agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when an agent or chatbot calls a [retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-08-01-preview&preserve-view=true) action at query time.

Knowledge sources are new in the 2025-08-01-preview release.

## Prerequisites

You need a search index containing plain text or vector content with a semantic configuration. [Review the index criteria for agentic retrieval](agentic-retrieval-how-to-create-index.md#criteria-for-agentic-retrieval). The index must be on the same search service as the knowledge agent.

To try the examples in this article, we recommend [Visual Studio Code](https://code.visualstudio.com/download) with the [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for sending preview REST API calls to Azure AI Search. Currently, there's no portal support.

## Check for existing knowledge sources

[!INCLUDE [Check for existing knowledge sources](includes/how-tos/knowledge-source-check-rest.md)]

The following JSON is an example response for a `searchIndex` knowledge source. Notice that the knowledge source specifies a single index name and which fields in the index to include in the query.

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
> The `webParameters` property isn't operational in this preview and is reserved for future use.

## Create a knowledge source

To create a `searchIndex` knowledge source:

1. Set environment variables at the top of your file.

    ```http
    @search-url = <YOUR SEARCH SERVICE URL>
    @api-key = <YOUR ADMIN API KEY>
    @ks-name = <YOUR KNOWLEDGE SOURCE NAME>
    @index-name = <YOUR INDEX NAME>
    ```

1. Use the 2025-08-01-preview of [Knowledge Sources - Create or Update (REST API)](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-08-01-preview&preserve-view=true) or an Azure SDK preview package that provides equivalent functionality to formulate the request.

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

1. Select **Send Request**.

**Key points**:

+ `name` must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search.

+ `kind` must be `searchIndex` for a search index knowledge source.

+ `searchIndexName` is the name of your index, which must be [designed for agentic retrieval](agentic-retrieval-how-to-create-index.md).

+ `sourceDataSelect` is the list of index fields returned when you specify `includeReferenceSourceData` in the knowledge agent definition. These fields are used for citations and should be `retrievable`. Examples include the document name, file name, page numbers, or chapter numbers.

## Assign to a knowledge agent

If you're satisfied with the index, continue to the next step: specifying the knowledge source in a [knowledge agent](agentic-retrieval-how-to-create-knowledge-base.md).

Within the knowledge agent, there are more properties to set on the knowledge source that are specific to query operations.

## Delete a knowledge source

[!INCLUDE [Delete knowledge source](includes/how-tos/knowledge-source-delete-rest.md)]

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)

+ [Agentic RAG: build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)

+ [Azure OpenAI Demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
