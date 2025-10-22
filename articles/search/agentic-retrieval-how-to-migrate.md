---
title: Migrate Agentic Retrieval Code
titleSuffix: Azure AI Search
description: Learn how to migrate your agentic retrieval code to the latest REST API version. This article focuses on breaking changes and backwards compatibility.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 10/22/2025
---

# Migrate agentic retrieval code to the latest version

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

If you wrote [agentic retrieval](agentic-retrieval-overview.md) code using an early preview REST API, this article explains when and how to migrate to the latest version. It also describes breaking and nonbreaking changes for all REST API versions that support agentic retrieval.

Migration instructions are intended to help you run an existing solution on a newer API version. These instructions help you address breaking changes at the API level so that your app runs as before. For help with adding new functionality, start with [What's new](whats-new.md).

> [!TIP]
> Using Azure SDKs instead of REST? Read this article to learn about breaking changes, and then install a newer preview package to begin your updates. Before you start, check the SDK change logs to confirm feature availability: [Python](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md), [.NET](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md), [JavaScript](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md), [Java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md).

## When to migrate

Each new API version that supports agentic retrieval has introduced breaking changes, from the original [2025-05-01-preview](#2025-05-01-preview) to [2025-08-01-preview](#2025-08-01-preview-1), to the latest [2025-11-01-preview](#2025-11-01-preview-1).

You can continue to run older code with no updates if you retain the API version value. However, to benefit from bug fixes, improvements, and newer functionality, you must update your code.

## How to migrate

+ The supported migration path is incremental. If your code targets 2025-05-01-preview, first migrate to 2025-08-01-preview, and then migrate to 2025-11-01-preview.

+ To understand the scope of changes, review [breaking and nonbreaking changes](#version-specific-changes) for each version.

+ "Update" means creating new objects that implement the behaviors of the previous version. When you create new objects under the new API version, you can run old and new side by side.

+ For each object that you update, start by getting the current definition from the search service so that you can review existing properties before specifying the new one.

+ Delete older versions only after your migration is fully tested and deployed.

### [**2025-11-01-preview**](#tab/migrate-11-01)

If you're migrating from [2025-08-01-preview](#2025-08-01-preview-1), *knowledge agent* is renamed to *knowledge base*, and multiple properties are relocated to different objects and levels within an object definition.

1. [Update searchIndex knowledge sources](#update-a-searchindex-knowledge-source).
1. [Update azureBlob knowledge sources](#update-an-azureblob-knowledge-source).
1. [Replace knowledge agent with knowledge base](#replace-knowledge-agent-with-knowledge-base).
1. [Send a query to test the retrieval](#test-the-retrieval-for-2025-11-01-preview-updates).
1. [Update client code](#update-code-and-clients-for-2025-11-01-preview).

#### Update a searchIndex knowledge source

The underlying index requires no updates. Create a new knowledge source that points to the existing index.

1. List all knowledge sources by name.

   ```http
   ### List all knowledge sources by name
   GET {{search-endpoint}}/knowledge-sources?api-version=2025-08-01-preview&$select=name
   api-key: {{api-key}}
   Content-Type: application/json
   ```

1. [Get the current definition](/rest/api/searchservice/knowledge-sources/get?view=rest-searchservice-2025-08-01-preview&preserve-view=true) to review existing properties. The response should look similar to [this example](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-08-01-preview&preserve-view=true#searchservicecreateorupdateknowledgesource).

   ```http
   ### Get a specific knowledge source
   GET {{search-endpoint}}/knowledge-sources/search-index-ks?api-version=2025-08-01-preview
   api-key: {{api-key}}
   Content-Type: application/json
   ```

1. Set up a create request. The knowledge source you're updating might look like the following example.

    ```http
    POST {{url}}/knowledge-sources/search-index-ks?api-version={{api-version}}
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

1. Change the API version to `2025-11-01-preview`.

1. Rename `sourceDataSelect` to `sourceDataFields` and change the string to an array with name-value pairs for each retrievable field you want to query. These are the fields to return in the search results, similar to a `select` clause in a classic query.

1. [Create the new knowledge source](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true).

    ```http
    PUT {{url}}/knowledge-sources/search-index-ks-new?api-version=2025-11-01-preview
    api-key: {{key}}
    Content-Type: application/json
    
    {
        "name": "search-index-ks",
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

You now have a migrated `searchIndex` knowledge source that implements the previous version features, with the correct field specifications for the 2025-11-01-preview. For more information about new capabilities available to this knowledge source type, see [Create a search index knowledge source](agentic-knowledge-source-how-to-search-index.md).

#### Update an azureBlob knowledge source

The underlying index requires no updates. However, you should create a new knowledge source so that your existing solution remains operational. Another full set of the indexer pipeline is generated.

1. [Get the current definition](/rest/api/searchservice/knowledge-sources/get?view=rest-searchservice-2025-08-01-preview&preserve-view=true) of your knowledge source. The response should look similar to [this example](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-08-01-preview&preserve-view=true#searchservicecreateorupdateknowledgesourceazureblob).

   ```http
   ### Get a knowledge source by name
   GET {{search-endpoint}}/knowledge-sources/azure-blob-ks?api-version=2025-08-01-preview
   api-key: {{api-key}}
   Content-Type: application/json
   ```

1. Set up a create request. The knowledge source you're updating might look like the following example.

    ```http
    POST {{url}}/knowledge-sources/search-index-ks?api-version={{api-version}}
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

1. Change the API version to `2025-11-01-preview`.

1. Add `ingestionParameters`.

1. Remove obsolete parameters.

1. [Create the new knowledge source](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true).

    ```http
    PUT {{url}}/knowledge-sources/azure-blob-ks?api-version=2025-11-01-preview
    api-key: {{key}}
    Content-Type: application/json
    
    {
        "name": "azure-blob-ks",
        "kind": "azureBlob",
        "description": "A sample azure blob knowledge source",
        "azureBlobParameters": {
            "connectionString": "{{blob-connection-string}}",
            "containerName": "blobcontainer",
            "folderPath": null,
            "isADLSGen2": false,
            "ingestionParameters": {
                "identity": null,
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
                "ingestionPermissionOptions": [],
                "contentExtractionMode": "standard",
                "aiServices": {
                    "uri": "{{ai-endpoint}}",
                    "apiKey": "{{ai-key}}"
                }
            }
        }
    }
    ```

You now have an updated `azureBlob` knowledge source with the correct ingestion parameters for the 2025-11-01-preview.

#### Replace knowledge agent with knowledge base

1. Get the current definition of your knowledge agent. The response should look similar to [this example](/rest/api/searchservice/knowledge-agents/get?view=rest-searchservice-2025-08-01-preview&preserve-view=true#searchservicegetknowledgeagent).

   ```http
   ### Get a knowledge agent by name
   GET {{search-endpoint}}/agents/corporate-ka?api-version=2025-08-01-preview
   api-key: {{api-key}}
   Content-Type: application/json
   ```

1. Set up an update request and paste in the 2025-08-01-preview JSON.

    ```http
    PUT {{url}}/agents/0801-earth-at-night-ka?api-version=2025-08-01-preview  HTTP/1.1
    api-key: {{key}}
    Content-Type: application/json
    
    {
        "name": "0801-earth-at-night-ka",
        "knowledgeSources": [
            {
            "name": "0801-earth-at-night-ks",
            "rerankerThreshold": 2.5
            }
        ],
        "models": [
            {
                "kind": "azureOpenAI",
                "azureOpenAIParameters": {
                    "resourceUri": "{{aoai-endpoint}}",
                    "apiKey": "{{aoai-key}}",
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

1. Change the API version to `2025-11-01-preview`.

1. Replace the endpoint: `/knowledgebases/{{your-object-name}}`.

1. Replace `outputConfiguration`, `requestLimits`, and `retrievalInstructions`.

1. Send the request to update the object. You can't rename an existing object, but you can create a new one that's an updated version of the original agent if you want to change the name. The response should look similar to [this example](/rest/api/searchservice/knowledgebases/get?view=rest-searchservice-2025-11-01-preview&preserve-view=true#searchservicegetknowledgebase).

   ```http
    PUT {{url}}/knowledgebases/corporate-kb?api-version={{api-version}}
    api-key: {{key}}
    Content-Type: application/json
    
    {
      "name": "corporate-kb",
      "description": "A sample knowledge base with default medium reasoning",
      "knowledgeSources": [
        {
            "name": "sec-gics-communicationservices"
        },
        {
            "name": "sec-gics-financials"
        },
        {
            "name": "sec-gics-healthcare"
        }
      ],
      "models": [
        {
            "kind": "azureOpenAI",
            "azureOpenAIParameters": {
                "deploymentId": "gpt-5-mini",
                "modelName": "gpt-5-mini",
                "resourceUri": "{{aoai-endpoint}}",
                "apiKey": "{{aoai-key}}"
            }
        }
      ],
      "retrievalReasoningEffort": { "kind": "medium" },
      "outputMode": "answerSynthesis",
      "answerInstructions": "Provide a concise and accurate answer based on the retrieved information.",
      "retrievalInstructions": "Use sec-gics-financials to answer financial questions, never use sec-gis-healthcare for this"
    }
   ```

You now have a knowledge base instead of a knowledge agent.

#### Test the retrieval for 2025-11-01-preview updates

To test your knowledge base's output with a query, use the 2025-11-01-preview of [Knowledge Retrieval - Retrieve (REST API)](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview&preserve-view=true).

The retrieve request is modified in the latest preview to support more shapes, including a simpler request that minimizes LLM processing. For more information about retrieval in this preview, see [Retrieve data using a knowledge base](agentic-retrieval-how-to-retrieve.md). 

This variant is the most similar to the default 2025-08-010-preview experience.

```http
### Send a query to the knowledge base
POST {{url}}/knowledgebases/corporate-kb/retrieve?api-version=2025-11-01-preview
api-key: {{key}}
Content-Type: application/json

{
    "messages": [
        {
            "role": "user",
            "content": [
                { "type": "text", "text": "What companies are in the financial sector?" }
            ]
        }
    ],
    "includeActivity": true,
    "knowledgeSourceParams": [
        {
            "knowledgeSourceName": "sec-gics-financials",
            "kind": "searchIndex",
            "includeReferences": true,
            "includeReferenceSourceData": true
        },
        {
            "knowledgeSourceName": "sec-gics-communicationservices",
            "kind": "searchIndex",
            "includeReferences": false,
            "includeReferenceSourceData": false
        },
        {
            "knowledgeSourceName": "sec-gics-healthcare",
            "kind": "searchIndex",
            "includeReferences": true,
            "includeReferenceSourceData": false,
            "alwaysQuerySource": true
        }
    ]
}
```

If the response has a `200 OK` HTTP code, your knowledge base successfully retrieved content from the knowledge source.

#### Update code and clients for 2025-11-01-preview

To complete your migration, follow these cleanup steps:

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
  + `attemptFastPath` in `outputConfiguration` is removed entirely. The new `minimal` reasoning effort is considered to be the replacement.

+ Knowledge agent (base) `requestLimits` is removed. Its child properties of `maxRuntimeInSeconds` and `maxOutputSize` are moved onto the retrieval request object directly.

+ Knowledge agent (base) `knowledgeSources` parameters: The following child properties are moved to the `knowledgeSourceParams` properties of the retrieval request object: 

  + `rerankerThreshold`
  + `alwaysQuerySource`
  + `includeReferenceSourceData`
  + `includeReferences`.

  The `maxSubQueries` property is gone. Its replacement is the new retrieval reasoning effort property.

+ Knowledge agent (base) retrieval request object: The `semanticReranker` activity record is replaced with the `agenticReasoning` activity record type.

+ Knowledge sources for both `azureBlob` and `searchIndex`: top-level properties for `identity`, `embeddingModel`, `chatCompletionModel`, `disableImageVerbalization`, and `ingestionSchedule` are now part of an `ingestionParameters` object on the knowledge source. All knowledge sources that pull from a search index have an `ingestionParameters` object.

+ For `searchIndex` knowledge sources only: `sourceDataSelect` is renamed to `sourceDataFields` and is an array that accepts `fieldName` and `fieldToSearch`.

#### [**Nonbreaking changes**](#tab/nonbreaking-1)

+ Adds knowledge sources for OneLake, SharePoint (local), SharePoint (remote) that retrieves content directly from Sharepoint, Web (Bing) that pulls from the Bing indexes.

+ All knowledge sources that pull from a search index have new ingestion options: `ingestionPermissionOptions` to support source-specific access models, `contentExtractionMode` that enables Content Understanding integration, `aiServices` endpoint for Content Understanding.

+ All knowledge sources that pull from a search index have a `status` operation, which returns the synchronization status of the knowledge source with its data source.

+ The `searchIndex` knowledge source adds `semanticConfigurationName` that overrides the default semantic configuration used by the retrieval request.

+ Knowledge agent (base) retrieval responses now return HTTP 206 status codes for partial success. Retrieval requests now take an optional `retrievalReasoningEffort` property that specifies levels of LLM processing.

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
