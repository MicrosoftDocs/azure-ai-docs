---
title: Create a knowledge agent
titleSuffix: Azure AI Search
description: Learn how to create a knowledge agent for agentic retrieval workloads in Azure AI Search.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 09/30/2025
---

# Create a knowledge agent in Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

In Azure AI Search, a *knowledge agent* is a top-level resource representing a connection to a chat completion model for use in agentic retrieval workloads. A knowledge agent is used by the [retrieve method](agentic-retrieval-how-to-retrieve.md) in an LLM-powered information retrieval pipeline.

A knowledge agent specifies:

+ A knowledge source (one or more) that points to a searchable content
+ A chat completion model that provides reasoning capabilities for query planning and answer formulation
+ Properties for performance optimization (constrain query processing time)

After you create a knowledge agent, you can update its properties at any time. If the knowledge agent is in use, updates take effect on the next job.

> [!IMPORTANT]
> 2025-08-01-preview introduces breaking changes for existing knowledge agents. This preview version requires one or more `knowledgeSource` definitions. We recommend [migrating existing code](agentic-retrieval-how-to-migrate.md) to the new APIs as soon as possible.

## Prerequisites

+ Familiarity with [agentic retrieval concepts and use cases](agentic-retrieval-overview.md).

+ Azure AI Search, in any [region that provides semantic ranker](search-region-support.md), on the basic pricing tier or higher. Your search service must have a [managed identity](search-how-to-managed-identities.md) for role-based access to the model.

+ A [supported chat completion model](#supported-models) on Azure OpenAI.

+ Permission requirements. **Search Service Contributor** can create and manage a knowledge agent. **Search Index Data Reader** can run queries. Instructions are provided in this article. [Quickstart: Connect to a search service](/azure/search/search-get-started-rbac?pivots=rest) explains how to configure roles and get a personal access token for REST calls.

+ Content requirements. A [knowledge source](agentic-knowledge-source-overview.md) that identifies searchable content used by the agent. It can be either a [search index knowledge source](agentic-knowledge-source-how-to-search-index.md) or a [blob knowledge source](agentic-knowledge-source-how-to-blob.md)

+ API requirements. To create or use a knowledge agent, use the [2025-08-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-08-01-preview&preserve-view=true) data plane REST API. Or, use a preview package of an Azure SDK that provides knowledge agent APIs: [Azure SDK for Python](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md), [Azure SDK for .NET](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md#1170-beta3-2025-03-25), [Azure SDK for Java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md). **There's no Azure portal support knowledge agents at this time**.

To follow the steps in this guide, we recommend [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for sending preview REST API calls to Azure AI Search or the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [Jupyter package](https://pypi.org/project/jupyter/).

## Deploy a model for agentic retrieval

Make sure you have a supported model that Azure AI Search can access. The following instructions assume Azure AI Foundry Model as the provider.

1. Sign in to [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs).

1. Deploy a supported model using [these instructions](/azure/ai-foundry/how-to/deploy-models-openai).

1. Verify the search service managed identity has **Cognitive Services User** permissions on the Azure OpenAI resource. 

   If you're testing locally, you also need **Cognitive Services User** permissions.

### Supported models

Use Azure OpenAI or an equivalent open-source model:

+ `gpt-4o`
+ `gpt-4o-mini`
+ `gpt-4.1`
+ `gpt-4.1-nano`
+ `gpt-4.1-mini`
+ `gpt-5`
+ `gpt-5-nano`
+ `gpt-5-mini`

## Configure access

Azure AI Search needs access to the chat completion model. You can use key-based or role-based authentication (recommended).

### [**Use roles**](#tab/rbac)

If you're using role-based authentication, on your Azure OpenAI resource, assign the **Cognitive Services User** role to a search service managed identity.

In Azure, you must have **Owner** or **User Access Administrator** permissions on the model provider to assign roles.

1. [Configure Azure AI Search to use a managed identity](search-how-to-managed-identities.md).

1. On your model provider, such as Foundry Model, create a role assignment that gives the search service managed identity **Cognitive Services User** permissions. If you're testing locally, assign yourself to the same role. 

1. For local testing, follow the steps in [Quickstart: Connect without keys](search-get-started-rbac.md) to get a personal access token and to ensure you're logged in to a specific subscription and tenant. Paste your personal identity token into the `@accessToken` variable. A request that connects using your personal identity should look similar to the following example:

    ```http
    @search-url=<YOUR SEARCH SERVICE URL>
    @accessToken=<YOUR PERSONAL ID>
    
    # List Indexes
    GET https://{{search-url}}/indexes?api-version=2025-08-01-preview
    Authorization: Bearer {{accessToken}}
    ```

> [!IMPORTANT]
> If you use role-based authentication, be sure to remove all references to the API key in your requests. In a request that specifies both approaches, the API key is used instead of roles.

### [**Use keys**](#tab/keys)

You can use API keys if you don't have permission to create role assignments.

1. [Copy a Azure AI Search admin API key](search-security-api-keys.md#find-existing-keys) and paste it as an `api-key` variable into your HTTP or REST file: `@api-key`.

1. Specify an API key on each request. A request that connects using an API key should look similar to the following example:

   ```http
    @search-url=<YOUR SEARCH SERVICE URL>
    @search-api-key=<YOUR SEARCH SERVICE ADMIN API KEY>

   # List Indexes
   GET {{search-url}}/indexes?api-version=2025-08-01-preview
      Content-Type: application/json
      @api-key: {{search-api-key}}
   ```

---

## Check for existing knowledge agents

The following request lists knowledge agents by name. Within the knowledge agents collection, all knowledge agents must be uniquely named. It's helpful to know about existing knowledge agents for reuse or for naming new agents.

### [**Python**](#tab/python-get-agents)

```python
# List existing knowledge agents on the search service
from azure.search.documents.indexes import SearchIndexClient

index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)

try:
    agents = {agent.name: agent for agent in index_client.list_agents(api_version=search_api_version)}
    print(f"\nKnowledge agents on search service '{search_endpoint}':")
    
    if agents:
        print(f"Found {len(agents)} knowledge agent(s):")
        for i, (name, agent) in enumerate(sorted(agents.items()), 1):
            print(f"{i}. Name: {name}")
            if agent.knowledge_sources:
                ks_names = [ks.name for ks in agent.knowledge_sources]
                print(f"   Knowledge Sources: {', '.join(ks_names)}")
            print()
    else:
        print("No knowledge agents found.")
        
except Exception as e:
    print(f"Error listing knowledge agents: {str(e)}")
```

You can also return a single agent by name to review its JSON definition.

```python
# Get knowledge agent definition for earth-knowledge-agent-2
from azure.search.documents.indexes import SearchIndexClient
import json

index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)

try:
    agent_name = "earth-knowledge-agent-2"
    agent = index_client.get_agent(agent_name, api_version=search_api_version)
    
    print(f"Knowledge agent '{agent_name}':")
    print(f"Name: {agent.name}")
    
    if agent.description:
        print(f"Description: {agent.description}")
    
    if agent.models:
        print(f"\nModels ({len(agent.models)}):")
        for i, model in enumerate(agent.models, 1):
            print(f"  {i}. {type(model).__name__}")
            if hasattr(model, 'azure_open_ai_parameters'):
                params = model.azure_open_ai_parameters
                print(f"     Resource: {params.resource_url}")
                print(f"     Deployment: {params.deployment_name}")
                print(f"     Model: {params.model_name}")
    
    if agent.knowledge_sources:
        print(f"\nKnowledge Sources ({len(agent.knowledge_sources)}):")
        for i, ks in enumerate(agent.knowledge_sources, 1):
            print(f"  {i}. {ks.name} (threshold: {ks.reranker_threshold})")
    
    if agent.output_configuration:
        config = agent.output_configuration
        print(f"\nOutput: {config.modality} (activity: {config.include_activity})")
    
    # Full JSON definition
    print(f"\nJSON definition:")
    print(json.dumps(agent.as_dict(), indent=2))
    
except Exception as e:
    print(f"Error: {str(e)}")
    
    # Show available agents
    try:
        agents = {agent.name: agent for agent in index_client.list_agents(api_version=search_api_version)}
        print(f"\nAvailable agents: {list(agents.keys())}")
    except Exception:
        print("Could not list available agents.")
```

### [**REST**](#tab/rest-get-agents)

```http
# List knowledge agents
GET {{search-url}}/agents?api-version=2025-08-01-preview
   Content-Type: application/json
   Authorization: Bearer {{accessToken}}
```

You can also return a single agent by name to review its JSON definition.

```http
# Get knowledge agent
GET {{search-url}}/agents/{{agent-name}}?api-version=2025-08-01-preview
   Content-Type: application/json
   Authorization: Bearer {{accessToken}}
```

---

## Create a knowledge agent

A knowledge agent drives the agentic retrieval pipeline. In application code, it's called by other agents or chat bots. 

Its composition consists of connections between *knowledge sources* (searchable content) and chat completion models that you've deployed in Azure OpenAI. Properties on the model establish the connection. Properties on the knowledge source establish defaults that inform query execution and the response.

To create an agent, use the 2025-08-01-preview data plane REST API or an Azure SDK preview package that provides equivalent functionality.

Recall that you must have an existing [knowledge source](agentic-knowledge-source-overview.md) to give to the agent.

### [**Python**](#tab/python-create-agent)

```python
from azure.search.documents.indexes.models import KnowledgeAgent, KnowledgeAgentAzureOpenAIModel, KnowledgeSourceReference, AzureOpenAIVectorizerParameters, KnowledgeAgentOutputConfiguration, KnowledgeAgentOutputConfigurationModality
from azure.search.documents.indexes import SearchIndexClient

aoai_params = AzureOpenAIVectorizerParameters(
    resource_url=aoai_endpoint,
    deployment_name=aoai_gpt_deployment,
    model_name=aoai_gpt_model,
)

output_cfg = KnowledgeAgentOutputConfiguration(
    modality=KnowledgeAgentOutputConfigurationModality.ANSWER_SYNTHESIS,
    include_activity=True,
)

agent = KnowledgeAgent(
    name=knowledge_agent_name,
    models=[KnowledgeAgentAzureOpenAIModel(azure_open_ai_parameters=aoai_params)],
    knowledge_sources=[
        KnowledgeSourceReference(
            name=knowledge_source_name,
            reranker_threshold=2.5,
        )
    ],
    output_configuration=output_cfg,
)

index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
index_client.create_or_update_agent(agent, api_version=search_api_version)
print(f"Knowledge agent '{knowledge_agent_name}' created or updated successfully.")
```

### [**REST**](#tab/rest-create-agent)

```http
@search-url=<YOUR SEARCH SERVICE URL>
@agent-name=<YOUR AGENT NAME>
@index-name=<YOUR INDEX NAME>
@model-provider-url=<YOUR AZURE OPENAI RESOURCE URI>
@model-api-key=<YOUR AZURE OPENAI API KEY>
@accessToken = <a long GUID>

# Create knowledge agent
PUT {{search-url}}/agents/{{agent-name}}?api-version=2025-08-01-preview
   Content-Type: application/json
   Authorization: Bearer {{accessToken}}

{
    "name" : "{{agent-name}}",
    "description": "This knowledge agent handles questions directed at two unrelated sample indexes."
    "retrievalInstructions": "Use the hotels knowledge source only for queries about hotels or where to stay, otherwise use the earth at night knowledge source.",
    "knowledgeSources": [
        {
            "name": "earth-at-night-blob-ks",
            "alwaysQuerySource": false,
            "includeReferences": true,
            "includeReferenceSourceData": true,
            "maxSubQueries": 30,
            "rerankerThreshold": null
        },
        {
            "name": "hotels-index-ks",
            "alwaysQuerySource": false,
            "includeReferences": true,
            "includeReferenceSourceData": true,
            "maxSubQueries": 5,
            "rerankerThreshold": null
        }
    ],
    "models" : [ 
        {
            "kind": "azureOpenAI",
            "azureOpenAIParameters": {
                "resourceUri": "{{model-provider-url}}",
                "apiKey": "{{model-api-key}}",
                "deploymentId": "gpt-5-mini",
                "modelName": "gpt-5-mini"
            }
        }
    ],
    "outputConfiguration": {
        "modality": "extractiveData",
        "answerInstructions": "Provide a concise answer to the question.",
        "attemptFastPath": false,
        "includeActivity": true
    },
    "requestLimits": {
        "maxOutputSize": 5000,
        "maxRuntimeInSeconds": 60
    }
}
```

**Key points**:

+ `name` must be unique within the knowledge agents collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects on Azure AI Search.

+ `description` is recommended for query planning. The LLM uses the description to inform query planning. 

+ `retrievalInstructions` is recommended for query planning when you have multiple knowledge sources. The instructions are passed as a prompt to the LLM to determine whether a knowledge source should be in scope for a query. This field influences both knowledge source selection and query formulation. For example, instructions could append information or prioritize a knowledge source. Instructions are passed directly to the LLM, which means it's possible to provide instructions that break query planning (for example, if instructions resulted in bypassing an essential knowledge source). If you set `retrievalInstructions`, make sure `alwaysQuerySource` is set to false.

+ `knowledgeSources` is required for knowledge agent creation. It specifies the search indexes or Azure blobs used by the knowledge agent. New in this preview release, the `knowledgeSources` is an array, and it replaces the previous `targetIndexes` array. 

    + `name` is a reference to either a [search index knowledge source](agentic-knowledge-source-how-to-search-index.md) or a [blob knowledge source](agentic-knowledge-source-how-to-blob.md).
    
    + `alwaysQuerySource` is a boolean that specifies whether a knowledge source must always be used (true), or only used if the query planning step determines it's useful. The default is false, which means source selection can skip this source if the model doesn’t think the query needs it. Source descriptions and retrieval instructions are used in this assessment. If you're using `attemptFastPath` on a specific knowledge source, `alwaysQuerySource` must be set to true.
    
    + `includeReferences` is a boolean that determines whether the reference portion of the response includes source data. We recommend starting with this value set to true if you want to shape your own response using output from the search engine. Otherwise, if you want to use the output in the response `content` string, you can set it to false.
    
    + `maxSubQueries` is the maximum number of queries the query planning step will generate. Each query can return up to 50 documents, which are reranked by semantic ranker. The `maxSubQueries` property must be between 2 and 40.

    + `rerankerThreshold` is the minimum semantic reranker score that's acceptable for inclusion in a response. [Reranker scores](semantic-search-overview.md#how-results-are-scored) range from 1 to 4. Plan on revising this value based on testing and what works for your content.

+ `models` specifies a connection to a [supported chat completion model](#supported-models). In this preview, `models` can contain just one model, and the model provider must be Azure OpenAI. Obtain model information from the Azure AI Foundry portal or from a command line request. You can use role-based access control instead of API keys for the Azure AI Search connection to the model. For more information, see [How to deploy Azure OpenAI models with Azure AI Foundry](/azure/ai-foundry/how-to/deploy-models-openai).

+ `outputConfiguration` gives you control over query execution logic and output.

  + `modality` determines the shape of the results. Valid values are `extractiveData` (default) or `answerSynthesis` (see [Use answer synthesis for citation-backed responses](agentic-retrieval-how-to-answer-synthesis.md)).

  + `answerInstructions` is used for shaping answers (see [Use answer synthesis for citation-backed responses](agentic-retrieval-how-to-answer-synthesis.md)). The default is null.

  + `attemptFastPath` is a boolean that can be used to enable a fast path to query execution. If `true`, the search engine skips query planning if the query is less than 512 characters and the semantic ranker score on the small query is above 1.9, indicating sufficient relevance. If the query is larger or the score is lower, query planning is invoked. You must have at least one knowledge source that has `alwaysQuerySource` enabled. If there are multiple knowledge sources, they must all have `alwaysQuerySource` enabled to be considered for fast path. The small query runs on all of them. The default is `false`.

  + `includeActivity` indicates whether retrieval results should include the query plan. The default is `true`.

<!--  Check minimum 10k  -->
+ `requestLimits` sets numeric limits over query processing.

  + `maxOutputSize` is the maximum number of tokens in the response `content` string, with 5,000 tokens as the minimum and recommended value, and no explicit maximum. The most relevant matches are preserved but the overall response is truncated at the last complete document to fit your token budget. 

  + `maxRuntimeInSeconds` sets the maximum amount of processing time for the entire request, inclusive of both Azure OpenAI and Azure AI Search.

+ `encryptionKey` is optional. Include an encryption key definition if you're supplementing with [customer-managed keys](search-security-manage-encryption-keys.md).

---

## Query the knowledge agent

Call the **retrieve** action on the knowledge agent object to confirm the model connection and return a response. Use the [2025-08-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-08-01-preview&preserve-view=true) data plane REST API or an Azure SDK preview package that provides equivalent functionality for this task. For more information about the **retrieve** API and the shape of the response, see [Retrieve data using a knowledge agent in Azure AI Search](agentic-retrieval-how-to-retrieve.md).

Replace "where does the ocean look green?" with a query string that's valid for your search index.

### [**Python**](#tab/python-query-agent)

Start with instructions.

```python
instructions = """
A Q&A agent that can answer questions about the Earth at night.
If you don't have the answer, respond with "I don't know".
"""

messages = [
    {
        "role": "system",
        "content": instructions
    }
]
```

Then send the query.

```python
from azure.search.documents.agent import KnowledgeAgentRetrievalClient
from azure.search.documents.agent.models import KnowledgeAgentRetrievalRequest, KnowledgeAgentMessage, KnowledgeAgentMessageTextContent, SearchIndexKnowledgeSourceParams

agent_client = KnowledgeAgentRetrievalClient(endpoint=search_endpoint, agent_name=knowledge_agent_name, credential=credential)
query_1 = """
    where does the ocean look green??
    """

messages.append({
    "role": "user",
    "content": query_1
})

req = KnowledgeAgentRetrievalRequest(
    messages=[
        KnowledgeAgentMessage(
            role=m["role"],
            content=[KnowledgeAgentMessageTextContent(text=m["content"])]
        ) for m in messages if m["role"] != "system"
    ],
    knowledge_source_params=[
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name=knowledge_source_name,
        )
    ]
)

result = agent_client.retrieve(retrieval_request=req, api_version=search_api_version)
print(f"Retrieved content from '{knowledge_source_name}' successfully.")
```

### [**REST**](#tab/rest-query-agent)

```http
# Send grounding request
POST {{search-url}}/agents/{{agent-name}}/retrieve?api-version=2025-08-01-preview
   Content-Type: application/json
   Authorization: Bearer {{accessToken}}

{
  "messages" : [
        { "role" : "assistant",
                "content" : [
                  { "type" : "text", "text" : "Use the earth at night index to answer the question. If you can't find relevant content, say you don't know." }
                ]
        },
        {
            "role" : "user",
            "content" : [
                {
                    "text" : "where does the ocean look green?",
                    "type" : "text"
                }
            ]
        }
    ],
  "knowledgeSourceParams": [
    {
      "filterAddOn": null,
      "knowledgeSourceName": "earth-at-night-blob-ks",
      "kind": "searchIndex"
    }
  ]
}
```

[messages](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-08-01-preview#knowledgeagentmessage&preserve-view=true) is required, but you can run this example using just "user" role that provides the query.

[`knowledgeSourceParams`](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-08-01-preview#searchindexknowledgesourceparams&preserve-view=true) is optional. Specify a knowledge source if the agent is configured for multiple sources and you want to focus the retrieve action on just one of them.

A knowledge source specification on the retrieve action describes the target search index on the search service. So even if the knowledge source "kind" is Azure blob, the valid value here is `searchIndex`. In this first public preview release, `knowledgeSourceParams.kind` is always `searchIndex`.

The response to the previous query might look like this:

```http
  "response": [
    {
      "content": [
        {
          "type": "text",
          "text": "The ocean appears green off the coast of Antarctica due to phytoplankton flourishing in the water, particularly in Granite Harbor near Antarctica’s Ross Sea, where they can grow in large quantities during spring, summer, and even autumn under the right conditions [ref_id:0]. Additionally, off the coast of Namibia, the ocean can also look green due to blooms of phytoplankton and yellow-green patches of sulfur precipitating from bacteria in oxygen-depleted waters [ref_id:1]. In the Strait of Georgia, Canada, the waters turned bright green due to a massive bloom of coccolithophores, a type of phytoplankton [ref_id:5]. Furthermore, a milky green and blue bloom was observed off the coast of Patagonia, Argentina, where nutrient-rich waters from different currents converge [ref_id:6]. Lastly, a large bloom of cyanobacteria was captured in the Baltic Sea, which can also give the water a green appearance [ref_id:9]."
        }
      ]
    }
  ]
```

---

## Delete an agent

If you no longer need the agent, or if you need to rebuild it on the search service, use this request to delete the current object.

### [**Python**](#tab/python-delete-agent)

```python
from azure.search.documents.indexes import SearchIndexClient

index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
index_client.delete_agent(knowledge_agent_name)
print(f"Knowledge agent '{knowledge_agent_name}' deleted successfully.")
```

### [**REST**](#tab/rest-delete-agent)
```http
# Delete agent
DELETE {{search-url}}/agents/{{agent-name}}?api-version=2025-08-01-preview
   Authorization: Bearer {{accessToken}}
```

---

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)

+ [Agentic RAG: build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)

+ [Azure OpenAI Demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
