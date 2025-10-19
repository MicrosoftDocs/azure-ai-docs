---
title: Migrate Agentic Retrieval Code
titleSuffix: Azure AI Search
description: Learn how to migrate your agentic retrieval code to the latest REST API version. This article focuses on breaking changes and backwards compatibility.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 10/19/2025
---

# Migrate agentic retrieval code to the latest version

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

If you wrote [agentic retrieval](agentic-retrieval-overview.md) code using an early preview REST API, this article explains when and how to migrate to the latest version. It also describes breaking and nonbreaking changes for all REST API versions that support agentic retrieval.

## When to migrate

Each new API version that supports agentic retrieval introduces breaking changes, from the original [2025-05-01-preview](#2025-05-01-preview) to [2025-08-01-preview](#2025-08-01-preview), on to [2025-11-01-preview](#2025-11-01-preview).

You can continue to run older code if you retain the API version value, but to benefit from bug fixes, improvements, and newer functionality, you must update your code.

## How to migrate

+ If your code targets 2025-05-01-preview, migrate to 2025-08-01-preview first, and then migrate to 2025-11-01-preview.

+ Review [breaking and nonbreaking changes](#version-specific-changes) for each version.

+ For each incremental update, start by getting the current object definitions from the search service. Save a copy of the original definition in case you need to restore it. Consider [backing up search index content](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-python/code/utilities/index-backup-restore) if you can't easily rebuild the index.

+ Run old and new objects side by side, deleting older versions only after new ones are fully tested and deployed.

### [2025-11-01-preview](#tab/migrate-11-01)

If you're migrating from [2025-08-01-preview](#2025-08-01-preview), knowledge agent is renamed to knowledge base, and multiple properties are relocated to different objects and levels within an object definition.

1. [Get the current knowledge agent definition](#get-the-current-definition).
1. [Create an equivalent knowledge base](#create-a-knowledge-base).
1. [Update the agent to use `knowledgeSources` instead of `targetIndexes`](#update-the-agent).
1. [Send a query to test the retrieval](#test-the-retrieval).
1. [Remove code that uses `targetIndexes` and update clients](#update-code-and-clients).

#### Get the current definition

TBD

#### Create a knowledge base

TBD

#### TBD heading

TBD

#### Test the retrieval

TBD

#### Update code and clients

TBD

---

### [2025-08-01-preview](#tab/migrate-08-01)

If you created a knowledge agent using the [2025-05-01-preview](#2025-05-01-preview), your agent's definition includes an inline `targetIndexes` array and an optional `defaultMaxDocsForReranker` property.

Starting with the [2025-08-01-preview](#2025-08-01-preview), reusable knowledge sources replace `targetIndexes`, and `defaultMaxDocsForReranker` is no longer supported. These breaking changes require you to:

1. [Get the current `targetIndexes` configuration](#get-the-current-configuration).
1. [Create an equivalent knowledge source](#create-a-knowledge-source).
1. [Update the agent to use `knowledgeSources` instead of `targetIndexes`](#update-the-agent).
1. [Send a query to test the retrieval](#test-the-retrieval).
1. [Remove code that uses `targetIndexes` and update clients](#update-code-and-clients).

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

#### Test the retrieval

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

#### Update code and clients

To complete your migration, follow these cleanup steps:

+ Replace all `targetIndexes` references with `knowledgeSources` in configuration files, code, scripts, and tests.
+ Update client calls to use the 2025-08-01-preview.
+ Clear or regenerate cached agent definitions that were created using the old shape.

---

## Version-specific changes

This section covers breaking and nonbreaking changes for the following REST API versions:

+ [2025-11-01-preview](#2025-11-01-preview)
+ [2025-08-01-preview](#2025-08-01-preview)
+ [2025-05-01-preview](#2025-05-01-preview)

### 2025-11-01-preview

To review the [REST API reference documentation](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) for this version, make sure the API version is selected in the filter at the top of the page.

#### [Breaking changes](#tab/breaking-1)

+ TBD

#### [Nonbreaking changes](#tab/nonbreaking-1)

+ TBD

---

### 2025-08-01-preview

To review the [REST API reference documentation](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-08-01-preview&preserve-view=true) for this version, make sure the API version is selected in the filter at the top of the page.

#### [Breaking changes](#tab/breaking)

+ Introduces knowledge sources as the new way to define data sources, supporting both `searchIndex` (one or multiple indexes) and `azureBlob` kinds. For more information, see [Create a search index knowledge source](agentic-knowledge-source-how-to-search-index.md) and [Create a blob knowledge source](agentic-knowledge-source-how-to-blob.md).

+ Requires `knowledgeSources` instead of `targetIndexes` in agent definitions. For migration steps, see [How to migrate](#how-to-migrate).

+ Removes `defaultMaxDocsForReranker` support. This property previously existed in `targetIndexes`, but there's no replacement in `knowledgeSources`.

#### [Nonbreaking changes](#tab/nonbreaking)

+ Adds `knowledgeSources`, `outputConfiguration`, and `retrievalInstructions` to agent definitions. For information about supported properties, see [Create a knowledge agent](agentic-retrieval-how-to-create-knowledge-base.md).

+ Renames `defaultRerankerThreshold` to `rerankerThreshold` and `defaultIncludeReferenceSourceData` to `includeReferenceSourceData`. These properties previously existed in `targetIndexes`, but you now specify them within each knowledge source reference in `knowledgeSources`.

---

### 2025-05-01-preview

This REST API version introduces agentic retrieval and knowledge agents. Each agent definition requires a `targetIndexes` array that specifies a single index and optional properties, such as `defaultRerankerThreshold` and `defaultIncludeReferenceSourceData`.

To review the [REST API reference documentation](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-05-01-preview&preserve-view=true) for this version, make sure the API version is selected in the filter at the top of the page.

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [Create a knowledge agent](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Create a knowledge source](agentic-knowledge-source-overview.md)
