---
title: Create a knowledge agent
titleSuffix: Azure AI Search
description: Learn how to create a knowledge agent for agentic retrieval workloads in Azure AI Search.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.update-cycle: 90-days
ms.topic: how-to
ms.date: 05/30/2025
---

# Create a knowledge agent in Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

In Azure AI Search, a *knowledge agent* is a top-level resource representing a connection to a chat completion model for use in agentic retrieval workloads. A knowledge agent is used by the [retrieve method](search-agentic-retrieval-how-to-retrieve.md) in an LLM-powered information retrieval pipeline.

A knowledge agent specifies:

+ A model that provides reasoning capabilities
+ A target search index used at query time
+ Parameters on the index for setting default behaviors and response shaping

After you create a knowledge agent, you can update its properties at any time. If the knowledge agent is in use, updates take effect on the next job.

## Prerequisites

+ Familiarity with [agentic retrieval concepts and use cases](search-agentic-retrieval-concept.md).

+ A [supported chat completion model](#supported-models) on Azure OpenAI.

+ Azure AI Search, in any [region that provides semantic ranker](search-region-support.md), on the basic pricing tier or higher. Your search service must have a [managed identity](search-how-to-managed-identities.md) for role-based access to the model.

+ Permissions on Azure AI Search. **Search Service Contributor** can create and manage a knowledge agent. **Search Index Data Reader** can run queries. Instructions are provided in this article.

+ A search index containing plain text or vectors. The index must [meet the requirements for agentic retrieval](search-agentic-retrieval-how-to-index.md), including a [semantic configuration](semantic-how-to-configure.md) with the `defaultConfiguration` specified.

+ API requirements. To create or use a knowledge agent, use the [2025-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-05-01-preview&preserve-view=true) data plane REST API. Or, use a prerelease package of an Azure SDK that provides knowledge agent APIs: [Azure SDK for Python](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md), [Azure SDK for .NET](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md#1170-beta3-2025-03-25), [Azure SDK for Java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md).

To follow the steps in this guide, we recommend [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for sending preview REST API calls to Azure AI Search. There's no portal support at this time.

## Deploy a model for agentic retrieval

Make sure you have a supported model that Azure AI Search can access. The following instruction assumes Azure AI Foundry Model as the provider.

1. Sign in to [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs).

1. Deploy a supported model using [these instructions](/azure/ai-foundry/how-to/deploy-models-openai).

1. Verify the search service managed identity has **Cognitive Services User** permissions on the Azure OpenAI resource. 

   If you're testing locally, you also need **Cognitive Services User** permissions.

### Supported models

Use Azure OpenAI or an equivalent open source model:

+ `gpt-4o`
+ `gpt-4o-mini`
+ `gpt-4.1`
+ `gpt-4.1-nano`
+ `gpt-4.1-mini`

## Configure access

Azure AI Search needs access to the chat completion model. You can use key-based or role-based authentication (recommended).

### Use role-based authentication

If you're using role-based authentication, on your Azure OpenAI resource, assign the **Cognitive Services User** role to a search service managed identity.

In Azure, you must have **Owner** or **User Access Administrator** permissions on the model provider to assign roles.

1. [Configure Azure AI Search to use a managed identity](search-how-to-managed-identities.md).

1. On your model provider, such as Foundry Model, create a role assignment that gives the search service managed identity **Cognitive Services User** permissions. If you're testing locally, assign yourself to the same role. 

1. For local testing, follow the steps in [Quickstart: Connect without keys](search-get-started-rbac.md) to get a personal access token and to ensure you're logged in to a specific subscription and tenant. Paste your personal identity token into the `@accessToken` variable. A request that connects using your personal identity should look similar to the following example:

    ```http
    @search-url=<YOUR SEARCH SERVICE URL>
    @accessToken=<YOUR PERSONAL ID>
    
    # List Indexes
    GET https://{{search-url}}/indexes?api-version=2025-05-01-preview
    Authorization: Bearer {{accessToken}}
    ```

> [!IMPORTANT]
> If you use role-based authentication, be sure to remove all references to the API key in your requests. In a request that specifies both approaches, the API key is used instead of roles.

### Use key-based authentication

You can use API keys if you don't have permission to create role assignments.

1. [Copy a Azure AI Search admin API key](search-security-api-keys.md#find-existing-keys) and paste it as an `api-key` variable into your HTTP or REST file: `@api-key`.

1. Specify an API key on each request. A request that connects using an API key should look similar to the following example:

   ```http
    @search-url=<YOUR SEARCH SERVICE URL>
    @search-api-key=<YOUR SEARCH SERVICE ADMIN API KEY>

   # List Indexes
   GET https://{{search-url}}/indexes?api-version=2025-05-01-preview
      Content-Type: application/json
      @api-key: {{search-api-key}}
   ```

## Check for existing knowledge agents

The following request lists knowledge agents by name. Within the knowledge agents collection, all knowledge agents must be uniquely named. It's helpful to know about existing knowledge agents for reuse or for naming new agents.

<!-- ### [**REST APIs**](#tab/rest-get) -->

```http
# List knowledge agents
GET https://{{search-url}}/agents?api-version=2025-05-01-preview
   Content-Type: application/json
   Authorization: Bearer {{accessToken}}
```

You can also return a single agent by name to review its JSON definition.

```http
# Get knowledge agent
GET https://{{search-url}}/agents/{{agent-name}}?api-version=2025-05-01-preview
   Content-Type: application/json
   Authorization: Bearer {{accessToken}}
```

<!-- --- -->

## Create a knowledge agent

A knowledge agent represents a connection between a model that you've deployed in Azure OpenAI and a target index on Azure AI Search. Parameters on the model establish the connection. Parameters on the index establish defaults that inform query execution and the response.

<!-- ### [**REST APIs**](#tab/rest-create) -->

To create an agent, use the 2025-05-01-preview data plane REST API or an Azure SDK prerelease package that provides equivalent functionality.

```http
@search-url=<YOUR SEARCH SERVICE URL>
@agent-name=<YOUR AGENT NAME>
@index-name=<YOUR INDEX NAME>
@model-provider-url=<YOUR AZURE OPENAI RESOURCE URI>
@accessToken = <a long GUID>

# Create knowledge agent
PUT https://{{search-url}}/agents/{{agent-name}}?api-version=2025-05-01-preview
   Content-Type: application/json
   Authorization: Bearer {{accessToken}}

{
    "name" : "{{agent-name}}",
    "targetIndexes" : [
        {
            "indexName" : "{{index-name}}",
            "defaultRerankerThreshold": 2.5,
            "defaultIncludeReferenceSourceData": true,
            "defaultMaxDocsForReranker": 200
        }
    ],
    "models" : [ 
        {
            "kind": "azureOpenAI",
            "azureOpenAIParameters": {
                "resourceUri": "{{model-provider-url}}",
                "apiKey": "{{model-api-key}}",
                "deploymentId": "gpt-4o-mini",
                "modelName": "gpt-4o-mini"
            }
        }
    ],
    "requestLimits": {
        "maxOutputSize": 5000,
        "maxRuntimeInSeconds": 60
    },
    "encryptionKey": { }
}
```

**Key points**:

+ `name` must be unique within the knowledge agents collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects on Azure AI Search.

+ `targetIndexes` is required for knowledge agent creation. It lists the search indexes that can use the knowledge agent. Currently in this preview release, the `targetIndexes` array can contain only one index. *It must have a default semantic configuration* (`defaultConfiguration`). For more information, see [Design an index for agentic retrieval](search-agentic-retrieval-how-to-index.md).

    ```json
    "semantic": {
        "defaultConfiguration": "my-default-semantic-config",
        "configurations": [ ]
    }
    ```

+ `defaultRerankerThreshold` is the minimum semantic reranker score that's acceptable for inclusion in a response. [Reranker scores](semantic-search-overview.md#how-results-are-scored) range from 1 to 4. Plan on revising this value based on testing and what works for your content.

+ `defaultIncludeReferenceSourceData` is a boolean that determines whether the reference portion of the response includes source data. We recommend starting with this value set to true if you want to shape your own response using output from the search engine. Otherwise, if you want to use the output in the response `content` string, you can set it to false.

+ `defaultMaxDocsForReranker` is the maximum number of documents that can be sent to the semantic ranker. Each subquery can pass a maximum of 50 documents to the semantic reranker, so setting this value above 50 generates more subqueries until the maximum is reached. For example, if you set this value to 200, then four subqueries are generated to support this number. This 

+ `models` specifies one or more connections to an existing gpt-4o or gpt-4o-mini model. Currently in this preview release, models can contain just one model, and the model provider must be Azure OpenAI. Obtain model information from the Azure AI Foundry portal or from a command line request. You can use role-based access control instead of API keys for the Azure AI Search connection to the model. For more information, see [How to deploy Azure OpenAI models with Azure AI Foundry](/azure/ai-foundry/how-to/deploy-models-openai).

<!--  Check minimum 10k  -->
+ `requestLimits` gives you control over the output generated during retrieval so that you can better manage inputs to the LLM. 

  + `maxOutputSize` is the maximum number of tokens in the response `content` string, with 5,000 tokens as the minimum and recommended value, and no explicit maximum. The most relevant matches are preserved but the overall response is truncated at the last complete document to fit your token budget. 

  + `maxRuntimeInSeconds` sets the maximum amount of processing time for the entire request, inclusive of both Azure OpenAI and Azure AI Search.

+ `encryptionKey` is optional. Include an encryption key definition if you're supplementing with [customer-managed keys](search-security-manage-encryption-keys.md).

<!-- --- -->

## Confirm knowledge agent operations

Call the **retrieve** action on the knowledge agent object to confirm the model connection and return a response. Use the [2025-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-05-01-preview&preserve-view=true) data plane REST API or an Azure SDK prerelease package that provides equivalent functionality for this task.

Replace "What are my vision benefits?" with a query string that's valid for your search index.

```http
# Send grounding request
POST https://{{search-url}}/agents/{{agent-name}}/retrieve?api-version=2025-05-01-preview
   Content-Type: application/json
   Authorization: Bearer {{accessToken}}

{
    "messages" : [
            {
                "role" : "assistant",
                "content" : [
                  { "type" : "text", "text" : "You are a helpful assistant for Contoso Human Resources. You have access to a search index containing guidelines about health care coverage for Washington state. If you can't find the answer in the search, say you don't know." }
                ]
            },
            {
                "role" : "user",
                "content" : [
                  { "type" : "text", "text" : "What are my vision benefits?" }
                ]
            }
        ],
    "targetIndexParams" :  [
        { 
            "indexName" : "{{index-name}}",
            "filterAddOn" : "State eq 'WA'",
            "IncludeReferenceSourceData": true,
            "rerankerThreshold" : 2.5
            "maxDocsForReranker": 250
        } 
    ]
}
```

For more information about the **retrieve** API and the shape of the response, see [Retrieve data using a knowledge agent in Azure AI Search](search-agentic-retrieval-how-to-retrieve.md).

## Delete an agent

If you no longer need the agent, or if you need to rebuild it on the search service, use this request to delete the current object.

```http
# Delete agent
DELETE https://{{search-url}}/agents/{{agent-name}}?api-version=2025-05-01-preview
   Authorization: Bearer {{accessToken}}
```

## Related content

+ [Agentic retrieval in Azure AI Search](search-agentic-retrieval-concept.md)

+ [Agentic RAG: build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)

+ [Azure OpenAI Demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
