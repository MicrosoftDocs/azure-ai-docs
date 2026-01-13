---
title: Migrate Agentic Retrieval Code
titleSuffix: Azure AI Search
description: Learn how to migrate your agentic retrieval code to the latest REST API version. This article focuses on breaking changes and backwards compatibility.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 11/10/2025
---

# Migrate agentic retrieval code to the latest version

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

If you wrote [agentic retrieval](agentic-retrieval-overview.md) code using an early preview REST API, this article explains when and how to migrate to a newer version. It also describes breaking and nonbreaking changes for all REST API versions that support agentic retrieval.

Migration instructions are intended to help you run an existing solution on a newer API version. The instructions in this article help you address breaking changes at the API level so that your app runs as before. For help with adding new functionality, start with [What's new](whats-new.md).

> [!TIP]
> Using Azure SDKs instead of REST? Read this article to learn about breaking changes, and then install a newer preview package to begin your updates. Before you start, check the SDK change logs to confirm API updates: [Python](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md), [.NET](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md), [JavaScript](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md), [Java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md).

## When to migrate

Each new API version that supports agentic retrieval has introduced breaking changes, from the original [2025-05-01-preview](#2025-05-01-preview) to [2025-08-01-preview](#2025-08-01-preview-1), to the latest [2025-11-01-preview](#2025-11-01-preview-1).

You can continue to run older code with no updates if you retain the API version value. However, to benefit from bug fixes, improvements, and newer functionality, you must update your code.

## How to migrate

+ The supported migration path is incremental. If your code targets 2025-05-01-preview, first migrate to 2025-08-01-preview, and then migrate to 2025-11-01-preview.

+ To understand the scope of changes, review [breaking and nonbreaking changes](#version-specific-changes) for each version.

+ "Migration" means creating new, uniquely named objects that implement the behaviors of the previous version. You can't overwrite an existing object if properties are added or deleted on the API. One advantage of creating new objects is the ability to preserve existing objects while new ones are developed and tested.

+ For each object that you migrate, start by getting the current definition from the search service so that you can review existing properties before specifying the new one.

+ Delete older versions only after your migration is fully tested and deployed.

### [**2025-11-01-preview**](#tab/migrate-11-01)

If you're migrating from [2025-08-01-preview](#2025-08-01-preview-1), "knowledge agent" is renamed to "knowledge base," and multiple properties are relocated to different objects and levels within an object definition.

1. [Update searchIndex knowledge sources](#update-a-searchindex-knowledge-source).
1. [Update azureBlob knowledge sources](#update-an-azureblob-knowledge-source).
1. [Replace knowledge agent with knowledge base](#replace-knowledge-agent-with-knowledge-base).
1. [Update the retrieval request and send a query to test your updates](#update-and-test-the-retrieval-for-2025-11-01-preview-updates).
1. [Update client code](#update-code-and-clients-for-2025-11-01-preview).

#### Update a searchIndex knowledge source

This procedure creates a new 2025-11-01-preview `searchIndex` knowledge source at the same functional level as the previous 2025-08-01 version. The underlying index itself requires no updates.

1. List all knowledge sources by name to find your knowledge source.

   ```http
   ### List all knowledge sources by name
   GET {{search-endpoint}}/knowledge-sources?api-version=2025-08-01-preview&$select=name
   api-key: {{api-key}}
   Content-Type: application/json
   ```

1. [Get the current definition](/rest/api/searchservice/knowledge-sources/get?view=rest-searchservice-2025-08-01-preview&preserve-view=true) to review existing properties.

   ```http
   ### Get a specific knowledge source
   GET {{search-endpoint}}/knowledge-sources/search-index-ks?api-version=2025-08-01-preview
   api-key: {{api-key}}
   Content-Type: application/json
   ```

   The response should look similar to the following example.

   ```json
   {
        "name": "search-index-ks",
        "kind": "searchIndex",
        "description": "This knowledge source pulls from a search index created using the 2025-08-01-preview.",
        "encryptionKey": null,
        "searchIndexParameters": {
        "searchIndexName": "earth-at-night-idx",
        "sourceDataSelect": "id, page_chunk, page_number"
        },
        "azureBlobParameters": null
   }
   ```

1. Formulate a [Create Knowledge Source](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) request as the basis for your migration.

    Start with the 08-01-preview JSON.

    ```http
    POST {{url}}/knowledge-sources/search-index-ks?api-version=2025-08-01-preview
    api-key: {{key}}
    Content-Type: application/json
    
    {
        "name": "search-index-ks",
        "kind": "searchIndex",
        "description": "A sample search index knowledge source",
        "encryptionKey": null,
        "searchIndexParameters": {
            "searchIndexName": "my-search-index",
            "sourceDataSelect": "id, page_chunk, page_number"
      }
    }
    ```

   Make the following updates for a 2025-11-01-preview migration:

   + Give the knowledge source a new name.

   + Change the API version to `2025-11-01-preview`.

   + Rename `sourceDataSelect` to `sourceDataFields` and change the string to an array with name-value pairs for each retrievable field you want to query. These are the fields to return in the search results, similar to a `select` clause in a classic query.

1. Review your updates and then send the request to create the object.

    ```http
    PUT {{url}}/knowledge-sources/search-index-ks-11-01?api-version=2025-11-01-preview
    api-key: {{key}}
    Content-Type: application/json
    
    {
        "name": "search-index-ks-11-01",
        "kind": "searchIndex",
        "description": "knowledge source migrated to 2025-11-01-preview",
        "encryptionKey": null,
        "searchIndexParameters": {
            "searchIndexName": "my-search-index",
            "sourceDataFields": [
                { "name": "id" }, { "name": "page_chunk" }, { "name": "page_number" }
            ]
        }
    }
    ```

You now have a migrated `searchIndex` knowledge source is backwards compatible with the previous version, using the correct property specifications for the 2025-11-01-preview. 

The response includes the full definition of the new object. For more information about new properties available to this knowledge source type, which you can now do through updates, see [How to create a search index knowledge source](agentic-knowledge-source-how-to-search-index.md).

#### Update an azureBlob knowledge source

This procedure creates a new 2025-11-01-preview `azureBlob` knowledge source at the same functional level as the previous 2025-08-01 version. It creates a new set of generated objects: data source, skillset, indexer, index.

1. List all knowledge sources by name to find your knowledge source.

   ```http
   ### List all knowledge sources by name
   GET {{search-endpoint}}/knowledge-sources?api-version=2025-08-01-preview&$select=name
   api-key: {{api-key}}
   Content-Type: application/json
   ```

1. [Get the current definition](/rest/api/searchservice/knowledge-sources/get?view=rest-searchservice-2025-08-01-preview&preserve-view=true) to review existing properties.

   ```http
   ### Get a specific knowledge source
   GET {{search-endpoint}}/knowledge-sources/azure-blob-ks?api-version=2025-08-01-preview
   api-key: {{api-key}}
   Content-Type: application/json
   ```

   The response might look similar to the following example if your workflow includes a model. Notice that a response includes the names of the generated objects. These objects are fully independent of the knowledge source and remain operational even if you update or delete their knowledge source.

   ```json
    {
      "name": "azure-blob-ks",
      "kind": "azureBlob",
      "description": "A sample azure blob knowledge source.",
      "encryptionKey": null,
      "searchIndexParameters": null,
      "azureBlobParameters": {
        "connectionString": "<redacted>",
        "containerName": "blobcontainer",
        "folderPath": null,
        "disableImageVerbalization": false,
        "identity": null,
        "embeddingModel": {
          "name": "embedding-model",
          "kind": "azureOpenAI",
          "azureOpenAIParameters": {
            "resourceUri": "<redacted>",
            "deploymentId": "text-embedding-3-large",
            "apiKey": "<redacted>",
            "modelName": "text-embedding-3-large",
            "authIdentity": null
          },
          "customWebApiParameters": null,
          "aiServicesVisionParameters": null,
          "amlParameters": null
        },
        "chatCompletionModel": {
          "kind": "azureOpenAI",
          "azureOpenAIParameters": {
            "resourceUri": "<redacted>",
            "deploymentId": "gpt-4o-mini",
            "apiKey": "<redacted>",
            "modelName": "gpt-4o-mini",
            "authIdentity": null
          }
    },
        "ingestionSchedule": null,
        "createdResources": {
          "datasource": "azure-blob-ks-datasource",
          "indexer": "azure-blob-ks-indexer",
          "skillset": "azure-blob-ks-skillset",
          "index": "azure-blob-ks-index"
        }
      }
    }
    ```

1. Formulate a [Create Knowledge Source](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) request as the basis for your migration.

    Start with the 08-01-preview JSON.

    ```http
    POST {{url}}/knowledge-sources/azure-blob-ks?api-version=2025-08-01-preview
    api-key: {{key}}
    Content-Type: application/json
    
    {
        "name": "azure-blob-ks",
        "kind": "azureBlob",
        "description": "A sample azure blob knowledge source.",
        "encryptionKey": null,
        "azureBlobParameters": {
            "connectionString": "<redacted>",
            "containerName": "blobcontainer",
            "folderPath": null,
            "disableImageVerbalization": false,
            "identity": null,
            "embeddingModel": {
                "name": "embedding-model",
                "kind": "azureOpenAI",
                "azureOpenAIParameters": {
                "resourceUri": "<redacted>",
                "deploymentId": "text-embedding-3-large",
                "apiKey": "<redacted>",
                "modelName": "text-embedding-3-large",
                "authIdentity": null
                },
                "customWebApiParameters": null,
                "aiServicesVisionParameters": null,
                "amlParameters": null
            },
            "chatCompletionModel": null,
            "ingestionSchedule": null
      }
    }
    ```

   Make the following updates for a 2025-11-01-preview migration:

   + Give the knowledge source a new name.

   + Change the API version to `2025-11-01-preview`.

   + Add `ingestionParameters` as a container for the following child properties: `"embeddingModel"`, `"chatCompletionModel"`, `"ingestionSchedule"`, `"contentExtractionMode"`.

1. Review your updates and then send the request to create the object. New generated objects are created for the indexer pipeline.

    ```http
    PUT {{url}}/knowledge-sources/azure-blob-ks-11-01?api-version=2025-11-01-preview
    api-key: {{key}}
    Content-Type: application/json
    
    {
        "name": "azure-blob-ks",
        "kind": "azureBlob",
        "description": "A sample azure blob knowledge source",
        "encryptionKey": null,
        "azureBlobParameters": {
            "connectionString": "{{blob-connection-string}}",
            "containerName": "blobcontainer",
            "folderPath": null,
            "ingestionParameters": {
                "embeddingModel": {
                    "kind": "azureOpenAI",
                    "azureOpenAIParameters": {
                        "deploymentId": "text-embedding-3-large",
                        "modelName": "text-embedding-3-large",
                        "resourceUri": "{{aoai-endpoint}}",
                        "apiKey": "{{aoai-key}}"
                    }
                },
                "chatCompletionModel": null,
                "disableImageVerbalization": false,
                "ingestionSchedule": null,
                "contentExtractionMode": "minimal"
            }
        }
    }
    ```

You now have a migrated `azureBlob` knowledge source that is backwards compatible with the previous version, using the correct property specifications for the 2025-11-01-preview. 

The response includes the full definition of the new object. For more information about new properties available to this knowledge source type, which you can now do through updates, see [How to create an Azure Blob knowledge source](agentic-knowledge-source-how-to-blob.md).

#### Replace knowledge agent with knowledge base

1. Knowledge bases require a knowledge source. Make sure you have a knowledge source that targets 2025-11-01-preview before you start.

1. [Get the current definition](/rest/api/searchservice/knowledge-agents/get?view=rest-searchservice-2025-08-01-preview&preserve-view=true) to review existing properties.

   ```http
   ### Get a knowledge agent by name
   GET {{search-endpoint}}/agents/earth-at-night?api-version=2025-08-01-preview
   api-key: {{api-key}}
   Content-Type: application/json
   ```

   The response might look similar to the following example.

    ```json
    {
      "name": "earth-at-night",
      "description": "A sample knowledge agent that retrieves from the earth-at-night knowledge source.",
      "retrievalInstructions": null,
      "requestLimits": null,
      "encryptionKey": null,
      "knowledgeSources": [
        {
          "name": "earth-at-night",
          "alwaysQuerySource": null,
          "includeReferences": null,
          "includeReferenceSourceData": null,
          "maxSubQueries": null,
          "rerankerThreshold": 2.5
        }
      ],
      "models": [
        {
          "kind": "azureOpenAI",
          "azureOpenAIParameters": {
            "resourceUri": "<redacted>",
            "deploymentId": "gpt-5-mini",
            "apiKey": "<redacted>",
            "modelName": "gpt-5-mini",
            "authIdentity": null
          }
        }
      ],
      "outputConfiguration": {
        "modality": "answerSynthesis",
        "answerInstructions": null,
        "attemptFastPath": false,
        "includeActivity": null
      }
    }
    ```

1. Formulate a [Create Knowledge Base](/rest/api/searchservice/knowledge-bases/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) request as the basis for your migration.

    Start with the 08-01-preview JSON.

    ```http
    PUT {{url}}/knowledgebases/earth-at-night?api-version=2025-08-01-preview  HTTP/1.1
    api-key: {{key}}
    Content-Type: application/json
    
    {
        "name": "earth-at-night",
        "description": "A sample knowledge agent that retrieves from the earth-at-night knowledge source.",
        "retrievalInstructions": null,
        "encryptionKey": null,
        "knowledgeSources": [
            {
              "name": "earth-at-night",
              "alwaysQuerySource": null,
              "includeReferences": null,
              "includeReferenceSourceData": null,
              "maxSubQueries": null,
              "rerankerThreshold": 2.5
            }
        ],
        "models": [
            {
                "kind": "azureOpenAI",
                "azureOpenAIParameters": {
                    "resourceUri": "<redacted>",
                    "apiKey": "<redacted>",
                    "deploymentId": "gpt-5-mini",
                    "modelName": "gpt-5-mini"
                }
            }
        ],
        "outputConfiguration": {
            "modality": "answerSynthesis"
        }
    }
    ```

   Make the following updates for a 2025-11-01-preview migration:

   + Replace the endpoint: `/knowledgebases/{{your-object-name}}`. Give the knowledge base a unique name.

   + Change the API version to `2025-11-01-preview`.

   + Delete `requestLimits`. The `maxRuntimeInSeconds` and `maxOutputSize` properties are now specified on the retrieval request object directly

   + Update `knowledgeSources`:

     + Delete `maxSubQueries` and replace with a retrievalReasoningEffort` (see [Set the retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md)).

     + Move `alwaysQuerySource`, `includeReferenceSourceData`, `includeReferences`, and `rerankerThreshold` to the `knowledgeSourcesParams` section of a [retrieve action](agentic-retrieval-how-to-retrieve.md).

   + No changes for `models`.

   + Update `outputConfiguration`:

     + Replace `outputConfiguration` with `outputMode`.

     + Delete `attemptFastPath`. It no longer exists. Equivalent behavior is implemented through `retrievalReasoningEffort` set to minimum  (see [Set the retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md)).

     + If modality is set to `answerSynthesis`, make sure you set the retrieval reasoning effort to low (default) or medium.

   + Add `ingestionParameters` as a requirement for creating a 2025-11-01-preview azureBlob knowledge source.

1. Review your updates and then send the request to create the object. New generated objects are created for the indexer pipeline.

   ```http
    PUT {{url}}/knowledgebases/earth-at-night-11-01?api-version={{api-version}}
    api-key: {{key}}
    Content-Type: application/json
    
    {
      "name": "earth-at-night-11-01",
      "description": "A sample knowledge base at the same functional level as the previous knowledge agent.",
      "retrievalInstructions": null,
      "encryptionKey": null,
      "knowledgeSources": [
        {
            "name": "earth-at-night-ks"
        }
      ],
      "models": [
        {
          "kind": "azureOpenAI",
          "azureOpenAIParameters": {
              "resourceUri": "<redacted>",
              "apiKey": "<redacted>",
              "deploymentId": "gpt-5-mini",
              "modelName": "gpt-5-mini"
            }
        }
      ],
      "retrievalReasoningEffort": null,
      "outputMode": "answerSynthesis",
      "answerInstructions": "Provide a concise and accurate answer based on the retrieved information.",

    }
   ```

You now have a knowledge base instead of a knowledge agent, and the object is backwards compatible with the previous version 

The response includes the full definition of the new object. For more information about new properties available to a knowledge base, which you can now do through updates, see [How to create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

#### Update and test the retrieval for 2025-11-01-preview updates

The retrieval request is modified for the 2025-11-01-preview to support more shapes, including a simpler request that minimizes LLM processing. For more information about retrieval in this preview, see [Retrieve data using a knowledge base](agentic-retrieval-how-to-retrieve.md). This section explains how to update your code.

1. Change the `/agents/retrieve` endpoint to `/knowledgebases/retrieve`.

1. Change the API version to `2025-11-01-preview`.

1. No changes to `messages` are required if you are using a `low` or `medium` retrievalReasoningEffort. Replace messages with `intent` if you use `minimal `reasoning (see [Set the retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md)).

1. Modify `knowledgeSourceParams` to include any properties that were removed from the agent: `rerankerThreshold`, `alwaysQuerySource`, `includeReferenceSourceData`, `includeReferences`.

1. Add `retrievalReasoningEffort` set to `minimum` if you were using `attemptFastPath`. If you were using `maxSubQueries`, it no longer exists. Use the `retrievalReasoningEffort` setting to specify subquery processing (see [Set the retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md)).

To test your knowledge base's output with a query, use the 2025-11-01-preview of [Knowledge Retrieval - Retrieve (REST API)](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview&preserve-view=true).

```http
### Send a query to the knowledge base
POST {{url}}/knowledgebases/earth-at-night-11-01/retrieve?api-version=2025-11-01-preview
api-key: {{key}}
Content-Type: application/json

{
    "messages": [
        {
            "role": "user",
            "content": [
                { "type": "text", "text": "What are some light sources on the ocean at night" }
            ]
        }
    ],
    "includeActivity": true,
    "retrievalReasoningEffort": { "kind": "medium" },
    "outputMode": "answerSynthesis",
    "maxRuntimeInSeconds": 30,
    "maxOutputSize": 6000
}
```

If the response has a `200 OK` HTTP code, your knowledge base successfully retrieved content from the knowledge source.

#### Update code and clients for 2025-11-01-preview

To complete your migration, follow these cleanup steps:

1. For Azure Blob knowledge sources only, update clients to use the new index. If you have code or script that runs an indexer or references a data source, index, or skillset, make sure you update the references to the new objects.

1. Replace all agent references with `knowledgeBases` in configuration files, code, scripts, and tests.

1. Update client calls to use the 2025-11-01-preview.

1. Clear or regenerate cached definitions that were created using the old shapes.

### [**2025-08-01-preview**](#tab/migrate-08-01)

If you created a knowledge agent using the [2025-05-01-preview](#2025-05-01-preview), your agent's definition includes an inline `targetIndexes` array and an optional `defaultMaxDocsForReranker` property.

Starting with the [2025-08-01-preview](#2025-08-01-preview-1), reusable knowledge sources replace `targetIndexes`, and `defaultMaxDocsForReranker` is no longer supported. These breaking changes require you to:

1. [Get the current `targetIndexes` configuration](#get-the-current-configuration).
1. [Create an equivalent knowledge source](#create-a-knowledge-source).
1. [Update the agent to use `knowledgeSources` instead of `targetIndexes`](#update-the-agent).
1. [Send a query to test the retrieval](#test-the-retrieval-for-2025-08-01-preview-updates).
1. [Remove code that uses `targetIndexes` and update clients](#update-code-and-clients-for-2025-08-01-preview).

#### Get the current configuration

To retrieve your agent's definition, use the 2025-05-01-preview of [Knowledge Agents - Get (REST API)](/rest/api/searchservice/knowledge-agents/get?view=rest-searchservice-2025-05-01-preview&preserve-view=true).

```http
@search-url = <YourSearchServiceUrl>
@agent-name = <YourAgentName>
@api-key = <YourApiKey>

### Get agent definition
GET https://{{search-url}}/agents/{{agent-name}}?api-version=2025-05-01-preview  HTTP/1.1
    api-key: {{api-key}}
```

The response should be similar to the following example. Copy the `indexName`, `defaultRerankerThreshold`, and `defaultIncludeReferenceSourceData` values for use in the upcoming steps. `defaultMaxDocsForReranker` is deprecated, so you can ignore its value.

```json
{
  "@odata.etag": "0x1234568AE7E58A1",
  "name": "my-knowledge-agent",
  "description": "My description of the agent",
  "targetIndexes": [
    {
      "indexName": "my-index", // Copy this value
      "defaultRerankerThreshold": 2.5, // Copy this value
      "defaultIncludeReferenceSourceData": true, // Copy this value
      "defaultMaxDocsForReranker": 100
    }
  ],
  ... // Redacted for brevity
}
```

#### Create a knowledge source

To create a `searchIndex` knowledge source, use the 2025-08-01-preview of [Knowledge Sources - Create (REST API)](/rest/api/searchservice/knowledge-sources/create?view=rest-searchservice-2025-08-01-preview&preserve-view=true). Set `searchIndexName` to the value you previously copied.

```http
@source-name = <YourSourceName>

### Create a knowledge source
PUT https://{{search-url}}/knowledgeSources/{{source-name}}?api-version=2025-08-01-preview  HTTP/1.1
    Content-Type: application/json
    api-key: {{api-key}}
    
    {
        "name": "{{source-name}}",
        "description": "My description of the knowledge source",
        "kind": "searchIndex",
        "searchIndexParameters": {
            "searchIndexName": "my-index" // Use the previous value
        }
    }
```

This example creates a knowledge source that represents one index, but you can target multiple indexes or an Azure blob. For more information, see [Create a knowledge source](agentic-knowledge-source-overview.md).

#### Update the agent

To replace `targetIndexes` with `knowledgeSources` in your agent's definition, use the 2025-08-01-preview of [Knowledge Agents - Create or Update (REST API)](/rest/api/searchservice/knowledge-agents/create-or-update?view=rest-searchservice-2025-08-01-preview&preserve-view=true). Set `rerankerThreshold` and `includeReferenceSourceData` to the values you previously copied.

```http
### Replace targetIndexes with knowledgeSources
POST https://{{search-url}}/agents/{{agent-name}}?api-version=2025-08-01-preview  HTTP/1.1
    Content-Type: application/json
    api-key: {{api-key}}

    { 
        "name": "{{agent-name}}", 
        "knowledgeSources": [  
            {  
                "name": "{{source-name}}",
                "rerankerThreshold": 2.5, // Use the previous value
                "includeReferenceSourceData": true // Use the previous value
            }
        ]
    } 
```

This example updates the definition to reference one knowledge source, but you can target multiple knowledge sources. You can also use other properties to control the retrieval behavior, such as `alwaysQuerySource`. For more information, see [Create a knowledge agent](agentic-retrieval-how-to-create-knowledge-base.md).

#### Test the retrieval for 2025-08-01-preview updates

To test your agent's output with a query, use the 2025-08-01-preview of [Knowledge Retrieval - Retrieve (REST API)](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-08-01-preview&preserve-view=true).

```http
### Send a query to the agent
POST https://{{search-url}}/agents/{{agent-name}}/retrieve?api-version=2025-08-01-preview  HTTP/1.1
    Content-Type: application/json
    api-key: {{api-key}}
        
    {
      "messages": [
            {
                "role": "user",
                "content" : [
                    {
                        "text": "<YourQueryText>",
                        "type": "text"
                    }
                ]
            }
        ]
    }
```

If the response has a `200 OK` HTTP code, your agent successfully retrieved content from the knowledge source.

#### Update code and clients for 2025-08-01-preview

To complete your migration, follow these cleanup steps:

+ Replace all `targetIndexes` references with `knowledgeSources` in configuration files, code, scripts, and tests.
+ Update client calls to use the 2025-08-01-preview.
+ Clear or regenerate cached agent definitions that were created using the old shape.

---

## Version-specific changes

This section covers breaking and nonbreaking changes for the following REST API versions:

+ [2025-11-01-preview](#2025-11-01-preview-1)
+ [2025-08-01-preview](#2025-08-01-preview-1)
+ [2025-05-01-preview](#2025-05-01-preview)

### 2025-11-01-preview

To review the [REST API reference documentation](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) for this version, make sure the 2025-11-01-preview API version is selected in the filter at the top of the page.

#### [**Breaking changes**](#tab/breaking-1)

+ Knowledge agent is renamed to knowledge base.
  
  | Previous Route | New Route |
  |-----|-----|
  | `/agents` | `/knowledgebases` |
  | `/agents/agent-name` | `/knowledgebases/knowledge-base-name` |
  | `/agents/agent-name/retrieve` | `/knowledgebases/knowledge-base-name/retrieve` |

+ Knowledge agent (base) `outputConfiguration` is renamed to `outputMode` and changed from an object to a string enumerator. Several properties are impacted:

  + `includeActivity` is moved from `outputConfiguration` onto the retrieval request object directly.  
  + `attemptFastPath` in `outputConfiguration` is removed entirely. The new `minimal` reasoning effort is the replacement.

+ Knowledge agent (base) `requestLimits` is removed. Its child properties of `maxRuntimeInSeconds` and `maxOutputSize` are moved onto the retrieval request object directly.

+ Knowledge agent (base) `knowledgeSources` parameters now only list the names of knowledge source used by a knowledge base. Other child properties that used to be under `knowledgeSources` are moved to the `knowledgeSourceParams` properties of the retrieval request object: 

  + `rerankerThreshold`
  + `alwaysQuerySource`
  + `includeReferenceSourceData`
  + `includeReferences`

  The `maxSubQueries` property is gone. Its replacement is the new retrieval reasoning effort property.

+ Knowledge agent (base) retrieval request object: The `semanticReranker` activity record is replaced with the `agenticReasoning` activity record type.

+ Knowledge sources for both `azureBlob` and `searchIndex`: top-level properties for `identity`, `embeddingModel`, `chatCompletionModel`, `disableImageVerbalization`, and `ingestionSchedule` are now part of an `ingestionParameters` object on the knowledge source. All knowledge sources that pull from a search index have an `ingestionParameters` object.

+ For `searchIndex` knowledge sources only: `sourceDataSelect` is renamed to `sourceDataFields` and is an array that accepts `fieldName` and `fieldToSearch`.

#### [**Nonbreaking changes**](#tab/nonbreaking-1)

+ Adds knowledge sources for OneLake, SharePoint (local), SharePoint (remote) that retrieves content directly from SharePoint, Web (Bing) that pulls from the Bing indexes.

+ All knowledge sources that pull from a search index have new ingestion options: `ingestionPermissionOptions` to support source-specific access models, `contentExtractionMode` that enables Azure Content Understanding in Foundry Tools integration, `aiServices` endpoint for Azure Content Understanding when `"contentExtractionMode": "minimal"`.

+ All knowledge sources that pull from a search index have a `status` operation, which returns the synchronization status of the knowledge source with its data source.

+ The `searchIndex` knowledge source adds `semanticConfigurationName` that overrides the default semantic configuration used by the retrieval request.

+ The `searchIndex` knowledge source adds `sourceDataFields` and `searchDataFields` to specify which fields are used at query time and also returned in a response.

+ Knowledge agent (base) retrieval responses now return HTTP 206 status codes for partial success. Retrieval requests now take an optional `retrievalReasoningEffort` property that specifies levels of LLM processing  (see [Set the retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md)).

+ Knowledge agent (base) adds a new `intent` object for `minimal` retrieval reasoning effort, where `intent` replaces `messages` to the LLM. An `intent` is a query string passed directly to the search engine, with no intermediate LLM query planning step.

+ Activity records in the retrieval response now have an optional `error` output, which indicates if the activity represents a failed operation.

---

### 2025-08-01-preview

To review the [REST API reference documentation](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-08-01-preview&preserve-view=true) for this version, make sure the 2025-08-01-preview API version is selected in the filter at the top of the page.

#### [**Breaking changes**](#tab/breaking)

+ Introduces knowledge sources as the new way to define data sources, supporting both `searchIndex` (one or multiple indexes) and `azureBlob` kinds. For more information, see [Create a search index knowledge source](agentic-knowledge-source-how-to-search-index.md) and [Create a blob knowledge source](agentic-knowledge-source-how-to-blob.md).

+ Requires `knowledgeSources` instead of `targetIndexes` in agent definitions. For migration steps, see [How to migrate](#how-to-migrate).

+ Removes `defaultMaxDocsForReranker` support. This property previously existed in `targetIndexes`, but there's no replacement in `knowledgeSources`.

#### [**Nonbreaking changes**](#tab/nonbreaking)

+ Adds `knowledgeSources`, `outputConfiguration`, and `retrievalInstructions` to agent definitions. For information about supported properties, see [Create a knowledge agent](agentic-retrieval-how-to-create-knowledge-base.md).

+ Renames `defaultRerankerThreshold` to `rerankerThreshold` and `defaultIncludeReferenceSourceData` to `includeReferenceSourceData`. These properties previously existed in `targetIndexes`, but you now specify them within each knowledge source reference in `knowledgeSources`.

---

### 2025-05-01-preview

This REST API version introduces agentic retrieval and knowledge agents. Each agent definition requires a `targetIndexes` array that specifies a single index and optional properties, such as `defaultRerankerThreshold` and `defaultIncludeReferenceSourceData`.

To review the [REST API reference documentation](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-05-01-preview&preserve-view=true) for this version, make sure the 2025-05-01-preview API version is selected in the filter at the top of the page.

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [Create a knowledge agent](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Create a knowledge source](agentic-knowledge-source-overview.md)
