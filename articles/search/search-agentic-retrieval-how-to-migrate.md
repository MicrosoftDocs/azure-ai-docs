---
title: Migrate Agentic Retrieval Code
titleSuffix: Azure AI Search
description: Learn how to migrate your agentic retrieval code to the latest REST API version. Starting with the 2025-08-01-preview, you must update knowledge agents to use knowledgeSources instead of targetIndexes due to breaking changes.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 08/19/2025
---

# Migrate agentic retrieval code to the latest version

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

If your agentic retrieval code was written against an early preview REST API, this article explains when and how to migrate to the latest version. It also describes breaking and nonbreaking changes for all REST API versions that provide agentic retrieval.

## When to migrate

Migrate your agentic retrieval code when any of the following apply:

+ The REST API version you use is announced for retirement or enters a deprecation window.

+ A newer REST API version introduces breaking changes that affect features you use. For example, you must address breaking changes if your code targets the [2025-05-01-preview](#2025-05-01-preview), which uses `targetIndexes` in agent definitions.

+ You want features that are only available in a newer REST API version.

+ Your code fails when unrecognized properties are returned in a REST API response. As a best practice, your application should ignore properties it doesn't understand.

## How to migrate

If you created a knowledge agent using the [2025-05-01-preview](#2025-05-01-preview), your agent definition includes an inline `targetIndexes` array. Starting with the [2025-08-01-preview](#2025-08-01-preview), reusable knowledge sources have replaced `targetIndexes`. This breaking change requires you to create a knowledge source, update your agent's definition to use `knowledgeSources`, and update client code that interacts with the agent.

To migrate an agent that uses `targetIndexes` to `knowledgeSources`:

1. [Get the current `targetIndexes` configuration](#capture-the-current-targetindexes).
2. [Port the configuration to a new knowledge source](#create-a-knowledge-source).
3. [Update the agent to use `knowledgeSources` instead of `targetIndexes`](#update-the-agent).
4. [Send a query to test the retrieval](#test-the-retrieval).
5. [Remove code that uses `targetIndexes` and update clients](#update-code-and-clients).

### Get the current configuration

To retrieve your agent's definition, use the 2025-05-01-preview of [Knowledge Agents - Get (REST API)](/rest/api/searchservice/knowledge-agents/get?view=rest-searchservice-2025-05-01-preview&preserve-view=true).

```http
@search-url = <YourSearchServiceUrl>
@agent-name = <YourAgentName>
@api-key = <YourApiKey>

### Get agent definition
GET https://{{search-url}}/agents/{{agent-name}}?api-version=2025-05-01-preview  HTTP/1.1
    api-key: {{api-key}}
```

The response should be similar to the following example. Copy the properties in the `targetIndexes` array, which you'll use to create a knowledge source in the next step.

```json
{
  "@odata.etag": "0x1234568AE7E58A1",
  "name": "my-knowledge-agent",
  "description": "My description of the agent",
  "targetIndexes": [
    {
      "indexName": "my-index", // Copy this property
      "defaultRerankerThreshold": 2.5, // Copy this property
      "defaultIncludeReferenceSourceData": true, // Copy this property
      "defaultMaxDocsForReranker": 100 // Copy this property
    }
  ],
  ... // Redacted for brevity
}
```

### Create a knowledge source

To define a `searchIndex` knowledge source, use the 2025-08-01-preview of [Knowledge Sources - Create (REST API)](/rest/api/searchservice/knowledge-sources/create?view=rest-searchservice-2025-08-01-preview&preserve-view=true). The new `searchIndexParameters` has the same syntax as `targetIndexes`, so you can use the properties from your previous configuration.

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
            "indexName": "my-index", // Same property as before
            "defaultRerankerThreshold": 2.5, // Same property as before
            "defaultIncludeReferenceSourceData": true, // Same property as before
            "defaultMaxDocsForReranker": 100 // Same property as before
        }
    }
```

This example creates a knowledge source that represents one index, but you can target multiple indexes or an Azure Storage container. For more information, see [Create a search index knowledge source](search-knowledge-source-how-to-index.md) and [Create a blob knowledge source](search-knowledge-source-how-to-blob.md).

### Update the agent

To replace `targetIndexes` with `knowledgeSources` in your agent's definition, use the 2025-08-01-preview of [Knowledge Agents - Create or Update (REST API)](/rest/api/searchservice/knowledge-agents/create-or-update?view=rest-searchservice-2025-08-01-preview&preserve-view=true).

```http
### Replace targetIndexes with knowledgeSources
POST https://{{search-url}}/agents/{{agent-name}}?api-version=2025-08-01-preview  HTTP/1.1
    Content-Type: application/json
    api-key: {{api-key}}

    { 
        "name": "{{agent-name}}", 
        "knowledgeSources": [  
            {"name": "{{source-name}}", "alwaysInclude": true},  
        ]
    } 
```

This example updates the agent's definition to reference one knowledge source, but you can target multiple knowledge sources. For more information, see [Create a knowledge agent](search-agentic-retrieval-how-to-create.md).

### Test the retrieval

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

<!--
The response should be similar to the following example, which includes...

```json

```
-->

### Update code and clients

To complete your migration, follow these cleanup steps:

+ Replace all `targetIndexes` references with `knowledgeSources` in configuration files, code, scripts, and tests.
+ Update client calls to use the 2025-08-01-preview REST API version.
+ Clear or regenerate cached agent definitions that were created using the old shape.

## Version-specific changes

This section covers breaking and nonbreaking changes for the following REST API versions:

+ [2025-08-01-preview](#2025-08-01-preview)
+ [2025-05-01-preview](#2025-05-01-preview)

### 2025-08-01-preview

#### [Breaking changes](#tab/breaking)

+ Introduces knowledge sources as the way to define data sources, supporting both `searchIndex` (one or multiple indexes) and `azureBlob`. For more information, see [Create a search index knowledge source](search-knowledge-source-how-to-index.md) and [Create a blob knowledge source](search-knowledge-source-how-to-blob.md).
+ Requires `knowledgeSources` instead of `targetIndexes` in agent definitions. For migration steps, see [How to migrate](#how-to-migrate).

#### [Nonbreaking changes](#tab/nonbreaking)

Adds the following properties to knowledge agents. For more information about each property, see [Create a knowledge agent](search-agentic-retrieval-how-to-create.md).

+ `answerSynthesis`
+ `retrievalInstructions`
+ `alwaysInclude`
+ `includeReferences`
+ `includeActivity`

### 2025-05-01-preview

This REST API version introduces [agentic retrieval](search-agentic-retrieval-concept.md) and [knowledge agents](search-agentic-retrieval-how-to-create.md).
