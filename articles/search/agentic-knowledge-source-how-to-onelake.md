---
title: Create a OneLake Knowledge Source for Agentic Retrieval
titleSuffix: Azure AI Search
description: Learn how to create a OneLake knowledge source in Azure AI Search. A OneLake knowledge source specifies a lakehouse, models, and properties that create an enrichment pipeline for agentic retrieval workloads.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - ignite-2025
ms.topic: how-to
ms.date: 10/16/2025
---

# Create a OneLake knowledge source

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Use a *OneLake knowledge source* to index and query Microsoft OneLake files in an agentic retrieval pipeline. [Knowledge sources](agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when an agent or chatbot calls a [retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-08-01-preview&preserve-view=true) action at query time.

When you create a OneLake knowledge source, you specify an external data source, models, and properties to automatically generate the following Azure AI Search objects:

+ A data source that represents a lakehouse.
+ A skillset that chunks and optionally vectorizes multimodal content from the lakehouse.
+ An index that stores enriched content and meets the criteria for agentic retrieval.
+ An indexer that uses the previous objects to drive the indexing and enrichment pipeline.

The generated indexer conforms to the *OneLake indexer*, whose prerequisites, supported tasks, supported document formats, supported shortcuts, and limitations also apply to OneLake knowledge sources. For more information, see the [OneLake indexer documentation](search-how-to-index-onelake-files.md).

## Prerequisites

+ Completion of the [OneLake indexer prerequisites](search-how-to-index-onelake-files.md#prerequisites).

+ Completion of the [OneLake indexer data preparation](search-how-to-index-onelake-files.md#prepare-data-for-indexing).

+ [Visual Studio Code](https://code.visualstudio.com/) with the [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) or a preview package of an Azure SDK that provides the latest knowledge source REST APIs. Currently, there's no portal support.

## Check for existing knowledge sources

[!INCLUDE [Check for existing knowledge sources](includes/how-tos/knowledge-source-check-rest.md)]

<!--
The following JSON is an example response for an `indexedOneLake` knowledge source.

```json

```
-->

## Create a knowledge source

To create an `indexedOneLake` knowledge source:

1. Set environment variables at the top of your file.

    ```http
    @search-url = <YOUR SEARCH SERVICE URL>
    @api-key = <YOUR SEARCH ADMIN API KEY>
    @ks-name = <YOUR KNOWLEDGE SOURCE NAME>
    @fabric-workspace-guid = <YOUR FABRIC WORKSPACE GUID>
    @lakehouse-guid = <YOUR LAKEHOUSE GUID>
    ```

1. Use the 2025-11-01-preview of [Knowledge Sources - Create or Update (REST API)](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) or an Azure SDK preview package that provides equivalent functionality to formulate the request.

    ```http
    PUT {{search-url}}/knowledgesources/indexed-onelake-ks?api-version=2025-11-01-preview
    api-key: {{api-key}}
    Content-Type: application/json
    
    {
        "name": "{{ks-name}}",
        "kind": "indexedOneLake",
        "description": "This knowledge source pulls content from a lakehouse.",
        "indexedOneLakeParameters": {
            "fabricWorkspaceId": "{{fabric-workspace-guid}}",
            "lakehouseId": "{{lakehouse-guid}}",
            "targetPath": null,
            "dataSoftDeleteTracking": true,
            "ingestionParameters": {
                "identity": null,
                "embeddingModel": {
                    // Redacted for brevity
                },
                "chatCompletionModel": {
                    // Redacted for brevity
                },
                "contentExtractionMode": "minimal",
                "disableImageVerbalization": null,
                "ingestionSchedule": null,
                "ingestionPermissionOptions": []
            }
        }
    }
    ```

1. Select **Send Request**.

**Key points:**

+ `name` must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search.

+ `kind` must be `indexedOneLake` for a OneLake knowledge source.

+ `targetPath` (optional) is a folder or shortcut within your lakehouse. When unspecified, the entire lakehouse is indexed.

+ `dataSoftDeleteTracking` (optional) tracks and removes soft-deleted files from the generated index. Valid values are `true` (default) and `false`. To use this property, you must [set custom metadata](search-how-to-index-onelake-files.md#detect-deletions-via-custom-metadata) on your lakehouse.

+ `embeddingModel` (optional) is a text embedding model that vectorizes text and image content during indexing and at query time. Use a model supported by the [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md), [Azure AI Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md), [AML skill](cognitive-search-aml-skill.md), or [Custom Web API skill](cognitive-search-custom-skill-web-api.md). The embedding skill will be included in the generated skillset, and its equivalent vectorizer will be included in the generated index.

+ `chatCompletionModel` (optional) is a chat completion model that verbalizes images or extracts content. Use a model supported by the [GenAI Prompt skill](cognitive-search-skill-genai-prompt.md), which will be included in the generated skillset. To skip image verbalization, omit this object and set `"disableImageVerbalization": true`.

+ `contentExtractionMode` (optional) controls how content is extracted from files. Valid values are `minimal` (default) and `standard`.

  + `minimal` uses basic extraction for text and images.

  + `standard` uses [Azure Content Understanding in Foundry Tools](/azure/ai-services/content-understanding/overview) for advanced document cracking, document chunking, and image verbalization. This mode requires a billable Azure AI Foundry Tools multi-service resource for the Content Understanding skill, which will be included in the generated skillset. You can also use the optional `AssetStore` object to save extracted images in a blob container.

+ `ingestionSchedule` (optional) adds scheduling information to the generated indexer. You can also [add a schedule](search-howto-schedule-indexers.md) later to automate data refresh.

+ If you get errors, make sure the embedding and chat completion models exist at the endpoints you provided.

## Review the created objects

When you create a OneLake knowledge source, your search service also creates an indexer, data source, skillset, and index. Exercise caution when you edit these objects, as introducing an error or incompatibility can break the pipeline.

After you create a knowledge source, the response lists the created objects. These objects are created according to a fixed template, and their names are based on the name of the knowledge source. You can't change the object names.

We recommend using the Azure portal to validate output creation. The workflow is:

1. Check the indexer for success or failure messages. Connection or quota errors appear here.
1. Check the index for searchable content. Use Search Explorer to run queries.
1. Check the skillset to learn how your content is chunked and optionally vectorized.
1. Modify the data source if you want to change connection details, such as authentication and authorization. Our example uses API keys for simplicity, but you can use Microsoft Entra ID authentication and role-based access.

## Assign to a knowledge base

If you're satisfied with the index, continue to the next step: specify the knowledge source in a [knowledge base](search-agentic-retrieval-how-to-create.md).

Within the knowledge base, there are more properties to set on the knowledge source that are specific to query operations.

After the knowledge base is configured, use the retrieve action to query the knowledge source.

## Delete a knowledge source

[!INCLUDE [Delete knowledge source](includes/how-tos/knowledge-source-delete-rest.md)]

## Related content

+ [Agentic retrieval in Azure AI Search](search-agentic-retrieval-concept.md)

+ [Agentic RAG: Build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)

+ [Azure OpenAI Demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
