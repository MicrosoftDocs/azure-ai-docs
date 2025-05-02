---
title: "Quickstart: Agentic Retrieval Using REST APIs or Python"
titleSuffix: Azure AI Search
description: Learn how to create a search agent that processes multi-turn conversations, retrieves relevant information from an Azure AI Search index, and generates answers using your own Azure OpenAI chat model.
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: quickstart
ms.date: 05/02/2025
---

# Quickstart: Agentic retrieval in Azure AI Search using REST or Python

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

In this quickstart, you use agentic retrieval in Azure AI Search to build a conversational search experience. The retrieval engine uses LLMs to plan queries, generate subqueries, and retrieve high-quality grounding data from indexed documents.

<!--Flesh out the intro. Add information about the sample data, chat model, and embedding model.-->

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

+ An [Azure AI Search service](search-create-service-portal.md) on the Basic tier or higher with [semantic ranker enabled](semantic-how-to-enable-disable.md).

+ An [Azure OpenAI resource](/azure/ai-services/openai/how-to/create-resource) in the [same region](#same-region-requirement) as your Azure AI Search service.

+ [Sample JSON data](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/nasa-e-book/earth-at-night-json).

+ [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) or the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [Jupyter package](https://pypi.org/project/jupyter/).

### Same-region requirement

Agentic retrieval requires that Azure AI Search and Azure OpenAI be in the same region. To meet this requirement:

1. [Choose an Azure OpenAI region](/azure/ai-services/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions#global-standard-model-availability) in which `gpt-4o-mini` and `text-embedding-3-large` are available. Agentic retrieval supports other chat and embedding models, but this quickstart assumes the aforementioned ones.

1. Confirm that [Azure AI Search is available in the same region](search-region-support.md#azure-public-regions). The region must also support semantic ranker, which is essential to query execution during agentic retrieval.

1. Deploy both resources in the same region.

## Deploy models

For agentic retrieval, you must deploy a supported chat model and a supported embedding model to your Azure OpenAI resource. This quickstart assumes `gpt-4o-mini` and `text-embedding-3-large`, respectively.

> [!IMPORTANT]
> Regardless of the chat model and embedding model that you use, make sure they meet the [same-region requirement](#same-region-requirement) for Azure AI Search and Azure OpenAI.

To deploy both Azure OpenAI models:

1. Sign in to the [Azure AI Foundry portal](https://ai.azure.com/).

1. On the home page, find the Azure OpenAI tile and select **Let's go**.

    :::image type="content" source="media/search-get-started-agentic-retrieval/azure-openai-lets-go-tile.png" alt-text="Screenshot of the Azure OpenAI tile in the Azure AI Foundry portal." border="true" lightbox="media/search-get-started-agentic-retrieval/azure-openai-lets-go-tile.png":::

   Your most recently used Azure OpenAI resource appears. If you have multiple Azure OpenAI resources, select **All resources** to switch between them.

1. From the left pane, select **Model catalog**.

1. Deploy `gpt-4o-mini` and `text-embedding-3-large` to your Azure OpenAI resource.

   > [!NOTE]
   > To simplify your code, don't use a custom deployment name for either model. This quickstart assumes the deployment and model names are the same.

<!--
### Supported models

Agentic retrieval supports the following Azure OpenAI models:

+ `gpt-4o`
+ `gpt-4o-mini`
+ `gpt-4.1`
+ `gpt-4.1-nano`
+ `gpt-4.1-mini`

| Model type | Description | Supported models |
| -- | -- | -- |
| Chat model | XYZ | `gpt-4o`, `gpt-4o-mini`, `gpt-4.1`, `gpt-4.1-nano`, and `gpt-4.1-mini` |
| Embedding model | XYZ | `text-embedding-ada-002`, `text-embedding-3-small`, and `text-embedding-3-large` |
-->

## Configure access

Azure AI Search needs access to your Azure OpenAI models. For this task, you can use API keys or Microsoft Entra ID with role assignments. Keys are easier to start with, but roles are more secure. This quickstart assumes roles.

To configure the recommended role-based access:

1. Sign in to the [Azure portal](https://portal.azure.com/).

1. [Enable role-based access](search-security-enable-roles.md) on your Azure AI Search service.

1. [Create a system-assigned managed identity](search-howto-managed-identities-data-sources.md#create-a-system-managed-identity) on your Azure AI Search service.

1. [Assign the following roles](search-security-rbac.md#how-to-assign-roles-in-the-azure-portal) on Azure AI Search and Azure OpenAI.

   | Service | Roles |
   | -- | -- |
   | Azure AI Search | Assign **Owner/Contributor** or **Search Service Contributor** (to create and manage an agent) and **Search Index Data Reader** (to run queries) to yourself. |
   | Azure OpenAI | Assign **Cognitive Services User** to the managed identity of your search service. |

## Get endpoints

In your code, you specify the following endpoints to establish connections with Azure AI Search and Azure OpenAI. These steps assume that you configured role-based access in the [previous section](#configure-access).

To obtain your service endpoints:

1. Sign in to the [Azure portal](https://portal.azure.com/).

1. On your Azure AI Search service:

    1. From the left pane, select **Overview**.

    1. Copy the URL, which should be similar to `https://my-service.search.windows.net`.

1. On your Azure OpenAI resource:

    1. From the left pane, select **Resource Management** > **Keys and Endpoint**.

    1. Copy the URL, which should be similar to `https://my-resource.openai.azure.com`.

## Connect from your local system

You're using Microsoft Entra ID and role assignments to interact with Azure AI Search and Azure OpenAI. Make sure you're logged in to the same tenant and subscription for both services. For more information, see [Quickstart: Connect without keys](search-get-started-rbac.md).

To connect from your local system:

1. Run the following commands in sequence.

    ```Azure CLI
    az account show
    
    az account set --subscription <PUT YOUR SUBSCRIPTION ID HERE>
    
    az login --tenant <PUT YOUR TENANT ID HERE>
    ```

1. (Optional) If you're using REST, obtain your Microsoft Entra token by running the following command. You specify this value in the [next section](#load-connections).

   ```Azure CLI
   az account get-access-token --scope https://search.azure.com/.default --query accessToken --output tsv
   ```

## Load connections

<!--Add information.-->

Select the tab that corresponds to your interaction method: REST or Python.

### [REST](#tab/load-connections-rest)

1. In Visual Studio Code, paste the following placeholders into a `.rest` or `.http` file.

    ```HTTP
    @baseUrl=PUT-YOUR-SEARCH-SERVICE-URL-HERE
    @token = PUT-YOUR-MICROSOFT-ENTRA-TOKEN-HERE
    @api-version=2025-05-01-Preview
    @aoaiBaseUrl=PUT-YOUR-AOAI-URL-HERE
    @aoaiGptModel=gpt-4o-mini
    @aoaiGptDeployment=gpt-4o-mini
    @aoaiEmbeddingModel=text-embedding-3-large
    @aoaiEmbeddingDeployment=text-embedding-3-large
    @index-name=earth_at_night
    @agent-name=earth-search-agent
    ```

1. Replace `baseUrl` and `aoaiBaseUrl` with the values you obtained in [Get endpoints](#get-endpoints).

1. Replace `token` with the Microsoft Entra token you obtained in [Connect from your local system](#connect-from-your-local-system).

1. To verify the variables, send the following request.

    ```HTTP
    ### List existing indexes by name
    GET {{baseUrl}}/indexes?api-version={{api-version}}
        Content-Type: application/json
        Authorization: Bearer {{token}}
    ```

    A response should appear in an adjacent pane. If you have existing indexes, they're listed. Otherwise, the list is empty. If the HTTP code is `200 OK`, you're ready to proceed.

### [Python](#tab/load-connections-python)

1. In Visual Studio Code, create a `.ipynb` file.

1. Install the following Python packages.

    ```Python
    ! pip install azure-search-documents==11.6.0b11 --quiet
    ! pip install azure-identity --quiet
    ! pip install openai --quiet
    ! pip install aiohttp --quiet
    ! pip install ipykernel --quiet
    ! pip install requests --quiet
    ```

1. In another code cell, paste the following import statements and variables.

    ```Python
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    import os

    answer_model = "gpt-4o"
    endpoint = "PUT YOUR SEARCH SERVICE ENDPOINT HERE"
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(credential, "https://search.azure.com/.default")
    index_name = "earth_at_night"
    azure_openai_endpoint = "PUT YOUR AZURE OPENAI ENDPOINT HERE"
    azure_openai_gpt_deployment = "gpt-4o"
    azure_openai_gpt_model = "gpt-4o"
    azure_openai_api_version = "2025-03-01-preview"
    azure_openai_embedding_deployment = "text-embedding-3-large"
    azure_openai_embedding_model = "text-embedding-3-large"
    agent_name = "earth-search-agent"
    api_version = "2025-05-01-Preview"
    ```

1. Replace `endpoint` and `azure_openai_endpoint` with the values you obtained in [Get endpoints](#get-endpoints).

1. To verify the variables, run the code cell.

---

## Create an index

A search index provides grounding data for the chat model. <!--Add information.-->

### [REST](#tab/create-index-rest)

```HTTP
### Create an index
PUT {{baseUrl}}/indexes/{{index-name}}?api-version={{api-version}}
    Content-Type: application/json
    Authorization: Bearer {{token}}

    {
    "name": "{{index-name}}",
    "fields": [
        {
        "name": "id",
        "type": "Edm.String",
        "key": true
        },
        {
        "name": "page_chunk",
        "type": "Edm.String",
        "searchable": true
        },
        {
        "name": "page_embedding_text_3_large",
        "type": "Collection(Edm.Single)",
        "stored": false,
        "dimensions": 3072,
        "vectorSearchProfile": "hnsw_text_3_large"
        },
        {
        "name": "page_number",
        "type": "Edm.Int32",
        "filterable": true
        }
    ],
    "semantic": {
        "defaultConfiguration": "semantic_config",
        "configurations": [
        {
            "name": "semantic_config",
            "prioritizedFields": {
            "prioritizedContentFields": [
                {
                "fieldName": "page_chunk"
                }
            ]
            }
        }
        ]
    },
    "vectorSearch": {
        "profiles": [
        {
            "name": "hnsw_text_3_large",
            "algorithm": "alg",
            "vectorizer": "azure_openai_text_3_large"
        }
        ],
        "algorithms": [
        {
            "name": "alg",
            "kind": "hnsw"
        }
        ],
        "vectorizers": [
        {
            "name": "azure_openai_text_3_large",
            "kind": "azureOpenAI",
            "azureOpenAIParameters": {
            "resourceUri": "{{aoaiBaseUrl}}",
            "deploymentId": "{{aoaiEmbeddingDeployment}}",
            "modelName": "{{aoaiEmbeddingModel}}"
            }
        }
        ]
    }
    }
```

### [Python](#tab/create-index-python)

```Python
from azure.search.documents.indexes.models import SearchIndex, SearchField, VectorSearch, VectorSearchProfile, HnswAlgorithmConfiguration, AzureOpenAIVectorizer, AzureOpenAIVectorizerParameters, SemanticSearch, SemanticConfiguration, SemanticPrioritizedFields, SemanticField
from azure.search.documents.indexes import SearchIndexClient

index = SearchIndex(
    name=index_name,
    fields=[
        SearchField(name="id", type="Edm.String", key=True, filterable=True, sortable=True, facetable=True),
        SearchField(name="page_chunk", type="Edm.String", filterable=False, sortable=False, facetable=False),
        SearchField(name="page_embedding_text_3_large", type="Collection(Edm.Single)", stored=False, vector_search_dimensions=3072, vector_search_profile_name="hnsw_text_3_large"),
        SearchField(name="page_number", type="Edm.Int32", filterable=True, sortable=True, facetable=True)
    ],
    vector_search=VectorSearch(
        profiles=[VectorSearchProfile(name="hnsw_text_3_large", algorithm_configuration_name="alg", vectorizer_name="azure_openai_text_3_large")],
        algorithms=[HnswAlgorithmConfiguration(name="alg")],
        vectorizers=[
            AzureOpenAIVectorizer(
                vectorizer_name="azure_openai_text_3_large",
                parameters=AzureOpenAIVectorizerParameters(
                    resource_url=azure_openai_endpoint,
                    deployment_name=azure_openai_embedding_deployment,
                    model_name=azure_openai_embedding_model
                )
            )
        ]
    ),
    semantic_search=SemanticSearch(
        default_configuration_name="semantic_config",
        configurations=[
            SemanticConfiguration(
                name="semantic_config",
                prioritized_fields=SemanticPrioritizedFields(
                    content_fields=[
                        SemanticField(field_name="page_chunk")
                    ]
                )
            )
        ]
    )
)

index_client = SearchIndexClient(endpoint=endpoint, credential=credential)
index_client.create_or_update_index(index)
print(f"Index '{index_name}' created or updated successfully")
```

---

## Upload documents

## Create a search agent

## Clean up resources

When you're working in your own subscription, it's a good idea at the end of a project to identify whether you still need the resources you created. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

In the Azure portal, you can find and manage resources by selecting **All resources** or **Resource groups** from the left pane.

## Next step

In this quickstart, you...
