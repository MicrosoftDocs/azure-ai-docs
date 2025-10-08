---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 09/05/2025
---

[!INCLUDE [Feature preview](../previews/preview-generic.md)]

In this quickstart, you use [agentic retrieval](../../agentic-retrieval-overview.md) to create a conversational search experience powered by documents indexed in Azure AI Search and large language models (LLMs) from Azure OpenAI in Azure AI Foundry Models.

A *knowledge agent* orchestrates agentic retrieval by decomposing complex queries into subqueries, running the subqueries against one or more *knowledge sources*, and returning results with metadata. By default, the agent outputs raw content from your sources, but this quickstart uses the answer synthesis modality for natural-language answer generation.

Although you can provide your own data, this quickstart uses [sample JSON documents](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/nasa-e-book/earth-at-night-json) from NASA's Earth at Night e-book. The documents describe general science topics and images of Earth at night as observed from space.

> [!TIP]
> Want to get started right away? See the [azure-search-python-samples](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/Quickstart-Agentic-Retrieval) repository on GitHub.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](../../search-create-service-portal.md) on the Basic tier or higher with [semantic ranker enabled](../../semantic-how-to-enable-disable.md).

+ An [Azure AI Foundry project](/azure/ai-foundry/how-to/create-projects) and Azure AI Foundry resource. When you create a project, the resource is automatically created.

+ The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

+ [Visual Studio Code](https://code.visualstudio.com/download) with the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [Jupyter package](https://pypi.org/project/jupyter/).

[!INCLUDE [Setup](./agentic-retrieval-setup.md)]

## Connect from your local system

You configured role-based access to interact with Azure AI Search and Azure OpenAI in Azure AI Foundry. Use the Azure CLI to sign in to the same subscription and tenant for both resources. For more information, see [Quickstart: Connect without keys](../../search-get-started-rbac.md).

To connect from your local system:

1. In Visual Studio Code, open the folder where you want to save your files.

1. Select **Terminal** > **New Terminal**.

1. Run the following command to sign in to your Azure account. If you have multiple subscriptions, select the one that contains your Azure AI Search service and Azure AI Foundry project.

    ```azurecli
    az login
    ```

## Install packages and load connections

Before you run any code, install Python packages and define endpoints, credentials, and deployment details for connections to Azure AI Search and Azure OpenAI in Azure AI Foundry. These values are used in the following sections.

To install the packages and load the connections:

1. In the same folder in Visual Studio Code, create a file named `quickstart-agentic-retrieval.ipynb`.

1. Add a code cell, and then paste the following `pip install` commands.

    ```python
    ! pip install azure-search-documents==11.7.0b1 --quiet
    ! pip install azure-identity --quiet
    ! pip install openai --quiet
    ! pip install aiohttp --quiet
    ! pip install ipykernel --quiet
    ! pip install requests --quiet
    ```

1. Select **Execute Cell** to install the packages.

1. Add another code cell, and then paste the following import statements and variables.

    ```python
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    import os

    search_endpoint = "PUT-YOUR-SEARCH-SERVICE-URL-HERE"
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(credential, "https://search.azure.com/.default")
    aoai_endpoint = "PUT-YOUR-AOAI-FOUNDRY-URL-HERE"
    aoai_embedding_model = "text-embedding-3-large"
    aoai_embedding_deployment = "text-embedding-3-large"
    aoai_gpt_model = "gpt-5-mini"
    aoai_gpt_deployment = "gpt-5-mini"
    index_name = "earth-at-night"
    knowledge_source_name = "earth-knowledge-source"
    knowledge_agent_name = "earth-knowledge-agent"
    search_api_version = "2025-08-01-preview"
    ```

1. Set `search_endpoint` and `aoai_endpoint` to the values you obtained in [Get endpoints](#get-endpoints).

1. Select **Execute Cell** to load the variables.

## Create a search index

In Azure AI Search, an index is a structured collection of data. Add and run a code cell with the following code to define an index named `earth-at-night`, which you previously specified using the `index_name` variable.

The index schema contains fields for document identification and page content, embeddings, and numbers. The schema also includes configurations for semantic ranking and vector search, which uses your `text-embedding-3-large` deployment to vectorize text and match documents based on semantic similarity.

```python
from azure.search.documents.indexes.models import SearchIndex, SearchField, VectorSearch, VectorSearchProfile, HnswAlgorithmConfiguration, AzureOpenAIVectorizer, AzureOpenAIVectorizerParameters, SemanticSearch, SemanticConfiguration, SemanticPrioritizedFields, SemanticField
from azure.search.documents.indexes import SearchIndexClient
from openai import AzureOpenAI
from azure.identity import get_bearer_token_provider

azure_openai_token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
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
                    resource_url=aoai_endpoint,
                    deployment_name=aoai_embedding_deployment,
                    model_name=aoai_embedding_model
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

index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
index_client.create_or_update_index(index)
print(f"Index '{index_name}' created or updated successfully.")
```

## Upload documents to the index

Currently, the `earth-at-night` index is empty. Add and run a code cell with the following code to populate the index with JSON documents from [NASA's Earth at Night e-book](https://raw.githubusercontent.com/Azure-Samples/azure-search-sample-data/refs/heads/main/nasa-e-book/earth-at-night-json/documents.json). As required by Azure AI Search, each document conforms to the fields and data types defined in the index schema.

```python
import requests
from azure.search.documents import SearchIndexingBufferedSender

url = "https://raw.githubusercontent.com/Azure-Samples/azure-search-sample-data/refs/heads/main/nasa-e-book/earth-at-night-json/documents.json"
documents = requests.get(url).json()

with SearchIndexingBufferedSender(endpoint=search_endpoint, index_name=index_name, credential=credential) as client:
    client.upload_documents(documents=documents)

print(f"Documents uploaded to index '{index_name}' successfully.")
```

## Create a knowledge source

A knowledge source is a reusable reference to your source data. Add and run a code cell with the following code to define a knowledge source named `earth-knowledge-source` that targets the `earth-at-night` index.

`source_data_select` specifies which index fields are accessible for retrieval and citations. Our example includes only human-readable fields to avoid lengthy, uninterpretable embeddings in responses.

```python
from azure.search.documents.indexes.models import SearchIndexKnowledgeSource, SearchIndexKnowledgeSourceParameters
from azure.search.documents.indexes import SearchIndexClient

ks = SearchIndexKnowledgeSource(
    name=knowledge_source_name,
    description="Knowledge source for Earth at night data",
    search_index_parameters=SearchIndexKnowledgeSourceParameters(
        search_index_name=index_name,
        source_data_select="id,page_chunk,page_number",
    ),
)

index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
index_client.create_or_update_knowledge_source(knowledge_source=ks, api_version=search_api_version)
print(f"Knowledge source '{knowledge_source_name}' created or updated successfully.")
```

## Create a knowledge agent

To target `earth-knowledge-source` and your `gpt-5-mini` deployment at query time, you need a knowledge agent. Add and run a code cell with the following code to define a knowledge agent named `earth-knowledge-agent`, which you previously specified using the `knowledge_agent_name` variable.

`reranker_threshold` ensures semantic relevance by excluding responses with a reranker score of `2.5` or lower. Meanwhile, `modality` is set to `ANSWER_SYNTHESIS`, enabling natural-language answers that cite the retrieved documents.

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

## Set up messages

Messages are the input for the retrieval route and contain the conversation history. Each message includes a role that indicates its origin, such as `system` or `user`, and content in natural language. The LLM you use determines which roles are valid.

Add and run a code cell with the following code to create a system message, which instructs `earth-knowledge-agent` to answer questions about the Earth at night and respond with "I don't know" when answers are unavailable.

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

## Run the retrieval pipeline

You're ready to run agentic retrieval. Add and run a code cell with the following code to send a two-part user query to `earth-knowledge-agent`.

Given the conversation history and retrieval parameters, the agent:

1. Analyzes the entire conversation to infer the user's information need.
1. Decomposes the compound query into focused subqueries.
1. Runs the subqueries concurrently against your knowledge source.
1. Uses semantic ranker to rerank and filter the results.
1. Synthesizes the top results into a natural-language answer.

```python
from azure.search.documents.agent import KnowledgeAgentRetrievalClient
from azure.search.documents.agent.models import KnowledgeAgentRetrievalRequest, KnowledgeAgentMessage, KnowledgeAgentMessageTextContent, SearchIndexKnowledgeSourceParams

agent_client = KnowledgeAgentRetrievalClient(endpoint=search_endpoint, agent_name=knowledge_agent_name, credential=credential)
query_1 = """
    Why do suburban belts display larger December brightening than urban cores even though absolute light levels are higher downtown?
    Why is the Phoenix nighttime street grid is so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?
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
            kind="searchIndex"
        )
    ]
)

result = agent_client.retrieve(retrieval_request=req, api_version=search_api_version)
print(f"Retrieved content from '{knowledge_source_name}' successfully.")
```

### Review the response, activity, and results

Add and run a code cell with the following code to display the response, activity, and results of the retrieval pipeline.

```python
import textwrap
import json

print("Response")
print(textwrap.fill(result.response[0].content[0].text, width=120))

print("Activity")
print(json.dumps([a.as_dict() for a in result.activity], indent=2))

print("Results")
print(json.dumps([r.as_dict() for r in result.references], indent=2))
```

The output should be similar to the following example, where:

+ `Response` provides a synthesized, LLM-generated answer to the query that cites the retrieved documents. When answer synthesis isn't enabled, this section contains content extracted directly from the documents.

+ `Activity` tracks the steps that were taken during the retrieval process, including the subqueries generated by your `gpt-5-mini` deployment and the tokens used for semantic ranking, query planning, and answer synthesis.

+ `Results` lists the documents that contributed to the response, each one identified by their `doc_key`.

```
Response
Suburban belts display larger December brightening than urban cores despite higher absolute light levels downtown
because the urban grid encourages outward growth along city borders, fueled by widespread personal automobile use,
leading to extensive suburban and residential municipalities linked by surface streets and freeways. This expansion
results in increased lighting in suburban areas during December, reflecting growth and development patterns rather than
just absolute light intensity downtown [ref_id:0].  The Phoenix nighttime street grid is sharply visible from space
because the metropolitan area is laid out along a regular grid of city blocks and streets, with major street lighting
clearly visible from low-Earth orbit. The grid pattern is especially evident at night due to street lighting, and major
transportation corridors like Grand Avenue and brightly lit commercial properties enhance this visibility. In contrast,
large stretches of interstate highways between Midwestern cities remain comparatively dim because, although the United
States has extensive road networks, the lighting along interstate highways is less intense and continuous than the dense
urban street grids. Additionally, navigable rivers and less urbanized areas show less light, indicating that lighting
intensity correlates with urban density and development patterns rather than just the presence of transportation
corridors [ref_id:0][ref_id:1][ref_id:2].
Activity
[
  {
    "id": 0,
    "type": "modelQueryPlanning",
    "elapsed_ms": 4572,
    "input_tokens": 2071,
    "output_tokens": 166
  },
  {
    "id": 1,
    "type": "searchIndex",
    "elapsed_ms": 608,
    "knowledge_source_name": "earth-knowledge-source",
    "query_time": "2025-09-05T17:38:49.330Z",
    "count": 0,
    "search_index_arguments": {
      "search": "Reasons for larger December brightening in suburban belts compared to urban cores despite higher downtown light levels"
    }
  },
    ... // Trimmed for brevity
  {
    "id": 4,
    "type": "semanticReranker",
    "input_tokens": 68989
  },
  {
    "id": 5,
    "type": "modelAnswerSynthesis",
    "elapsed_ms": 5619,
    "input_tokens": 3931,
    "output_tokens": 249
  }
]
Results
[
  {
    "type": "searchIndex",
    "id": "0",
    "activity_source": 2,
    "reranker_score": 2.6642752,
    "doc_key": "earth_at_night_508_page_104_verbalized"
  },
  ... // Trimmed for brevity
]
```

## Continue the conversation

Add and run a code cell with the following code to continue the conversation with `earth-knowledge-agent`. After you send this user query, the agent fetches relevant content from `earth-knowledge-source` and appends the response to the `messages` list.

```python
query_2 = "How do I find lava at night?"
messages.append({
    "role": "user",
    "content": query_2
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
            kind="searchIndex"
        )
    ]
)

result = agent_client.retrieve(retrieval_request=req, api_version=search_api_version)
print(f"Retrieved content from '{knowledge_source_name}' successfully.")
```

### Review the new response, activity, and results

Add and run a code cell with the following code to display the new response, activity, and results of the retrieval pipeline.

```python
import textwrap
import json

print("Response")
print(textwrap.fill(result.response[0].content[0].text, width=120))

print("Activity")
print(json.dumps([a.as_dict() for a in result.activity], indent=2))

print("Results")
print(json.dumps([r.as_dict() for r in result.references], indent=2))
```

## Clean up resources

When you work in your own subscription, it's a good idea to finish a project by determining whether you still need the resources you created. Resources that are left running can cost you money.

In the [Azure portal](https://portal.azure.com/), you can manage your Azure AI Search and Azure AI Foundry resources by selecting **All resources** or **Resource groups** from the left pane.

Otherwise, add and run code cells with the following code to delete the objects you created in this quickstart.

### Delete the knowledge agent

```python
from azure.search.documents.indexes import SearchIndexClient

index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
index_client.delete_agent(knowledge_agent_name)
print(f"Knowledge agent '{knowledge_agent_name}' deleted successfully.")
```

### Delete the knowledge source

```python
from azure.search.documents.indexes import SearchIndexClient

index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
index_client.delete_knowledge_source(knowledge_source=knowledge_source_name)
print(f"Knowledge source '{knowledge_source_name}' deleted successfully.")
```

### Delete the search index

```python
from azure.search.documents.indexes import SearchIndexClient

index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
index_client.delete_index(index_name)
print(f"Index '{index_name}' deleted successfully.")
```
