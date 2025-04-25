---
title: Create an agent
titleSuffix: Azure AI Search
description: Learn how to create an agent for agentic retrieval workloads in Azure AI Search.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 04/30/2025
---

# Create an agent in Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

In Azure AI Search, an *agent* is a top-level object representing a connection to an LLM for use in agentic retrieval workloads. It specifies a model that provides agent capabilities, and it lists the search indexes that can use the agent at query time.

After you can create an agent, you can update it's properties at any time. If the agent is in use, updates take effect on the next job.

## Prerequisites

+ Familiarity with [agentic retrieval concepts and use cases](search-agentic-retrieval-concept.md).

+ A chat completion model, either an LLM or SLM, that provides reasoning and evaluation.

+ Azure AI Search with a managed identity for role-based access to a chat model.

+ A search index containing plain text, vectors, or image references. The index must have a [semantic configuration](semantic-how-to-configure.md).

+ Region requirements. Azure AI Search and your model should be in the same region.

+ API requirements. Use 2025-05-01-preview data plane REST API or a prerelease package of an Azure SDK that provides Agent APIs.

To follow the steps in this guide, we recommend [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for sending REST API calls to Azure AI Search.

## Deploy a model for agentic retrieval

Make sure you have a supported model that can be accessed by Azure AI Search. The following instruction assumes Azure AI Foundry Model as the provider.

1. Sign in to [Azure AI Foundry portal](https://ai.azure.com/).

1. Deploy a supported model using [these instructions](/azure/ai-foundry/how-to/deploy-models-openai).

### Supported models

Use Azure OpenAI or an equivalent open source model:

+ gpt-4o
+ gpt-4o-mini

## Configure access

Azure AI Search needs access to the chat completion model. You can use key-based or role-based authentication (recommended).

### Use role-based authentication

If you're using role-based authentication, on your Azure OpenAI resource, assign the **Cognitive Services User** role to a search service managed identity.

In Azure, you must have **Owner** or **User Access Administrator** permissions on the model provider to assign roles.

1. [Configure Azure AI Search to use a managed identity](search-howto-managed-identities-data-sources.md).

1. On your model provider, such Foundry Model, create a role assignment that gives the search service managed identity **Cognitive Services User** permissions. If you're testing locally, assign yourself to the same role. 

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
   api-key: {{search-api-key}}
   ```

## Check for existing agents

The following request lists agents by name. Within the agents collection, all agents must be uniquely named. It's helpful to know about existing agents for reuse or for naming purposes.

```http
# List Agents
GET https://{{search-url}}/agents?api-version=2025-05-01-preview
api-key: {{search-api-key}}
```

You can also return a single agent by name.

```http
# Get Agent
GET https://{{search-url}}/agents/{{agent-name}}?api-version=2025-05-01-preview
api-key: {{search-api-key}}
```

## Create an agent

A knowledge agent represents a connection to a model that you've deployed. Parameters on the model establish the connection.

To create an agent, use the 2025-05-01-preview data plane REST API or an Azure SDK prerelease package that provides equivalent functionality.

```http
@search-url=<YOUR SEARCH SERVICE URL>
@search-api-key=<YOUR SEARCH SERVICE ADMIN API KEY>
@agent-name=<YOUR AGENT NAME>
@index-name=<YOUR INDEX NAME>
@model-provider-url=<YOUR AZURE OPENAI RESOURCE URI>
@model-api-key=<YOUR AZURE OPENAI API KEY>

# Create Agent
PUT https://{{search-url}}/agents/{{agent-name}}?api-version=2025-05-01-preview
api-key: {{search-api-key}}
Content-Type: application/json

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
        "maxOutputSize": 10000,
        "maxRuntimeInSeconds": 60
    },
    "encryptionKey": { }
}
```

**Key points**:

+ `name` must be unique within the agents collection it must adhere to [naming rules](/rest/api/searchservice/naming-rules) for objects on Azure AI Search.

+ `targetIndexes` is required for agent creation. It lists the search indexes that can use the agent. Currently in this preview release, the `targetIndexes` array can contain only one index. *It must have a semantic configuration*, otherwise it can be any search index on the search service that has content you want to query.

+ `defaultRerankerThreshold` is the minimum semantic reranker score that's acceptable for inclusion in a response. [Reranker scores](semantic-search-overview.md#how-ranking-is-scored) range from 1 to 4. Plan on revising this value based on testing and what works for your content.

+ `defaultIncludeReferenceSourceData` is a boolean that determines whether the reference portion of the response includes source data. We recommend starting with this value set to true while you evaluate which properties give you the best configuration for your content. It gives you a basis of comparison between raw content and processed content. Once you no longer find this information useful, set it to false.

+ `defaultMaxDocsForReranker` is the maximum number of documents that can be sent to the semantic ranker. Each subquery can pass a maximum of 50 documents to the semantic reranker, so setting this value above 50 generates more subqueries until the maximum is reached. For example, if you set this value to 200, then four subqueries are generated to support this number.

+ `models` specifies one or more connections to an existing gpt-4o or gpt-4o-mini model. Currently in this preview release, models can contain just one model, and the model provider should be Azure AI Foundry Model. Obtain model information from the Azure AI Foundry portal or from a command line request. You can use role-based access control instead of API keys for the Azure AI Search connection to the model. For more information, see [How to deploy Azure OpenAI models with Azure AI Foundry](/azure/ai-foundry/how-to/deploy-models-openai).

+ `requestLimits` gives you control over the output generated during retrieval so that you can better manage inputs to the LLM.

+ `maxOutputSize` is the number of tokens, with 10,000 tokens as the minimum. The most relevant matches are preserved but the overall response is truncated at the last complete document to fit your token budget.

+ `encryptionKey` is optional. Include an encryption key definition if you're supplementing with [customer-managed keys](search-security-manage-encryption-keys.md).

## Confirm agent availability

Call the **retrieve** action on the agent object to confirm the model connection and return a response. Use the [2025-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-05-01-preview&preserve-view=true) data plane REST API or an Azure SDK prerelease package that provides equivalent functionality for this task.

Replace "hello world" with a query string that's valid for your search index.

```http
# Send Grounding Request
POST https://{{search-url}}/agents/{{agent-name}}/retrieve?api-version=2025-05-01-preview
api-key: {{search-api-key}}
Content-Type: application/json

{
    "messages" : [
            {
                "role" : "user",
                "content" : [
                  {
                    "text" : "hello world",
                    "type" : "text"
                  }
                ]
            }
        ],
    "targetIndexParams" :  [
        { 
            "indexName" : "{{index-name}}",
            "filterAddOn" : null, 
            "includeReferenceSourceData" : true 
        } 
    ]
}
```

For more information about the retrieve API, see [Retrieve data using an agent in Azure AI Search](search-agentic-retrieval-how-to-retrieve.md).

## Delete an agent

```http
# Delete Agent
DELETE https://{{search-url}}/agents/{{agent-name}}?api-version=2025-05-01-preview
api-key: {{search-api-key}}
```

## Related content

+ [Agentic retrieval in Azure AI Search](search-agentic-retrieval-concept.md)

+ [Azure OpenAI Demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
