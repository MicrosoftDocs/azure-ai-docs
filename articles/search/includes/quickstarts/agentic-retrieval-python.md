---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 01/14/2026
ms.custom: dev-focus
ai-usage: ai-assisted
---

[!INCLUDE [Feature preview](../previews/preview-generic.md)]

In this quickstart, you use [agentic retrieval](../../agentic-retrieval-overview.md) to create a conversational search experience powered by documents indexed in Azure AI Search and a large language model (LLM) from Azure OpenAI in Foundry Models.

A *knowledge base* orchestrates agentic retrieval by decomposing complex queries into subqueries, running the subqueries against one or more *knowledge sources*, and returning results with metadata. By default, the knowledge base outputs raw content from your sources, but this quickstart uses the answer synthesis output mode for natural-language answer generation.

Although you can provide your own data, this quickstart uses [sample JSON documents](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/nasa-e-book/earth-at-night-json) from NASA's Earth at Night e-book. The documents describe general science topics and images of Earth at night as observed from space.

> [!TIP]
> Want to get started right away? See the [azure-search-python-samples](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/Quickstart-Agentic-Retrieval) GitHub repository.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](../../search-create-service-portal.md) in any [region that provides agentic retrieval](../../search-region-support.md).

+ A [Microsoft Foundry project](/azure/ai-foundry/how-to/create-projects) and resource. When you create a project, the resource is automatically created.

+ The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

+ The latest version of [Python](https://www.python.org/downloads/).

+ [Visual Studio Code](https://code.visualstudio.com/download) with the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python).

[!INCLUDE [Setup](./agentic-retrieval-setup.md)]

## Connect from your local system

You configured role-based access to interact with Azure AI Search and Azure OpenAI in Foundry Models. Use the Azure CLI to sign in to the same subscription and tenant for both resources. For more information, see [Quickstart: Connect without keys](../../search-get-started-rbac.md).

To connect from your local system:

1. Create a folder named `quickstart-agentic-retrieval`.

1. Open the folder in Visual Studio Code.

1. Select **Terminal** > **New Terminal**.

1. Run the following command to sign in to your Azure account. If you have multiple subscriptions, select the one that contains your Azure AI Search service and Foundry project.

    ```azurecli
    az login
    ```

## Run the code

To create and run the agentic retrieval pipeline:

1. Run the following command to install the required packages.

    ```console
    pip install azure-identity requests azure-search-documents --pre
    ```

1. Create a file named `agentic-retrieval.py` in the `quickstart-agentic-retrieval` folder.

1. Paste the following code into the file.

    ```python
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    from azure.search.documents.indexes.models import SearchIndex, SearchField, VectorSearch, VectorSearchProfile, HnswAlgorithmConfiguration, AzureOpenAIVectorizer, AzureOpenAIVectorizerParameters, SemanticSearch, SemanticConfiguration, SemanticPrioritizedFields, SemanticField, SearchIndexKnowledgeSource, SearchIndexKnowledgeSourceParameters, SearchIndexFieldReference, KnowledgeBase, KnowledgeBaseAzureOpenAIModel, KnowledgeSourceReference, KnowledgeRetrievalOutputMode, KnowledgeRetrievalLowReasoningEffort
    from azure.search.documents.indexes import SearchIndexClient
    from azure.search.documents import SearchIndexingBufferedSender
    from azure.search.documents.knowledgebases import KnowledgeBaseRetrievalClient
    from azure.search.documents.knowledgebases.models import KnowledgeBaseRetrievalRequest, KnowledgeBaseMessage, KnowledgeBaseMessageTextContent, SearchIndexKnowledgeSourceParams
    import requests
    import json
    
    # Define variables
    search_endpoint = "PUT-YOUR-SEARCH-SERVICE-URL-HERE"
    aoai_endpoint = "PUT-YOUR-AOAI-FOUNDRY-URL-HERE"
    aoai_embedding_model = "text-embedding-3-large"
    aoai_embedding_deployment = "text-embedding-3-large"
    aoai_gpt_model = "gpt-5-mini"
    aoai_gpt_deployment = "gpt-5-mini"
    index_name = "earth-at-night"
    knowledge_source_name = "earth-knowledge-source"
    knowledge_base_name = "earth-knowledge-base"
    search_api_version = "2025-11-01-preview"
    
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(credential, "https://search.azure.com/.default")
    
    # Create an index
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
    
    # Upload documents
    url = "https://raw.githubusercontent.com/Azure-Samples/azure-search-sample-data/refs/heads/main/nasa-e-book/earth-at-night-json/documents.json"
    documents = requests.get(url).json()
    
    with SearchIndexingBufferedSender(endpoint=search_endpoint, index_name=index_name, credential=credential) as client:
        client.upload_documents(documents=documents)
    
    print(f"Documents uploaded to index '{index_name}' successfully.")
    
    # Create a knowledge source
    ks = SearchIndexKnowledgeSource(
        name=knowledge_source_name,
        description="Knowledge source for Earth at night data",
        search_index_parameters=SearchIndexKnowledgeSourceParameters(
            search_index_name=index_name,
            source_data_fields=[SearchIndexFieldReference(name="id"), SearchIndexFieldReference(name="page_number")]
        ),
    )
    
    index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
    index_client.create_or_update_knowledge_source(knowledge_source=ks)
    print(f"Knowledge source '{knowledge_source_name}' created or updated successfully.")
    
    # Create a knowledge base
    aoai_params = AzureOpenAIVectorizerParameters(
        resource_url=aoai_endpoint,
        deployment_name=aoai_gpt_deployment,
        model_name=aoai_gpt_model,
    )
    
    knowledge_base = KnowledgeBase(
        name=knowledge_base_name,
        models=[KnowledgeBaseAzureOpenAIModel(azure_open_ai_parameters=aoai_params)],
        knowledge_sources=[
            KnowledgeSourceReference(
                name=knowledge_source_name
            )
        ],
        output_mode=KnowledgeRetrievalOutputMode.ANSWER_SYNTHESIS,
        answer_instructions="Provide a two sentence concise and informative answer based on the retrieved documents."
    )
    
    index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
    index_client.create_or_update_knowledge_base(knowledge_base)
    print(f"Knowledge base '{knowledge_base_name}' created or updated successfully.")
    
    # Set up messages
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
    
    # Run agentic retrieval
    agent_client = KnowledgeBaseRetrievalClient(endpoint=search_endpoint, knowledge_base_name=knowledge_base_name, credential=credential)
    query_1 = """
        Why do suburban belts display larger December brightening than urban cores even though absolute light levels are higher downtown?
        Why is the Phoenix nighttime street grid is so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?
        """
    
    messages.append({
        "role": "user",
        "content": query_1
    })
    
    req = KnowledgeBaseRetrievalRequest(
        messages=[
            KnowledgeBaseMessage(
                role=m["role"],
                content=[KnowledgeBaseMessageTextContent(text=m["content"])]
            ) for m in messages if m["role"] != "system"
        ],
        knowledge_source_params=[
            SearchIndexKnowledgeSourceParams(
                knowledge_source_name=knowledge_source_name,
                include_references=True,
                include_reference_source_data=True,
                always_query_source=True
            )
        ],
        include_activity=True,
        retrieval_reasoning_effort=KnowledgeRetrievalLowReasoningEffort
    )
    
    result = agent_client.retrieve(retrieval_request=req)
    print(f"Retrieved content from '{knowledge_base_name}' successfully.")
    
    # Display the response, activity, and references
    response_contents = []
    activity_contents = []
    references_contents = []
    
    response_parts = []
    for resp in result.response:
        for content in resp.content:
            response_parts.append(content.text)
    response_content = "\n\n".join(response_parts) if response_parts else "No response found on 'result'"
    
    response_contents.append(response_content)
    
    # Print the three string values
    print("response_content:\n", response_content, "\n")

    messages.append({
        "role": "assistant",
        "content": response_content
    })
    
    if result.activity:
        activity_content = json.dumps([a.as_dict() for a in result.activity], indent=2)
    else:
        activity_content = "No activity found on 'result'"
        
    activity_contents.append(activity_content)
    print("activity_content:\n", activity_content, "\n")
    
    if result.references:
        references_content = json.dumps([r.as_dict() for r in result.references], indent=2)
    else:
        references_content = "No references found on 'result'"
        
    references_contents.append(references_content)
    print("references_content:\n", references_content)
    
    # Continue the conversation
    query_2 = "How do I find lava at night?"
    messages.append({
        "role": "user",
        "content": query_2
    })
    
    req = KnowledgeBaseRetrievalRequest(
        messages=[
            KnowledgeBaseMessage(
                role=m["role"],
                content=[KnowledgeBaseMessageTextContent(text=m["content"])]
            ) for m in messages if m["role"] != "system"
        ],
        knowledge_source_params=[
            SearchIndexKnowledgeSourceParams(
                knowledge_source_name=knowledge_source_name,
                include_references=True,
                include_reference_source_data=True,
                always_query_source=True
            )
        ],
        include_activity=True,
        retrieval_reasoning_effort=KnowledgeRetrievalLowReasoningEffort
    )
    
    result = agent_client.retrieve(retrieval_request=req)
    print(f"Retrieved content from '{knowledge_base_name}' successfully.")
    
    # Display the new retrieval response, activity, and references
    response_parts = []
    for resp in result.response:
        for content in resp.content:
            response_parts.append(content.text)
    response_content = "\n\n".join(response_parts) if response_parts else "No response found on 'result'"
    
    response_contents.append(response_content)
    
    # Print the three string values
    print("response_content:\n", response_content, "\n")
    
    if result.activity:
        activity_content = json.dumps([a.as_dict() for a in result.activity], indent=2)
    else:
        activity_content = "No activity found on 'result'"
        
    activity_contents.append(activity_content)
    print("activity_content:\n", activity_content, "\n")
    
    if result.references:
        references_content = json.dumps([r.as_dict() for r in result.references], indent=2)
    else:
        references_content = "No references found on 'result'"
        
    references_contents.append(references_content)
    print("references_content:\n", references_content)
    
    # Clean up resources
    index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
    index_client.delete_knowledge_base(knowledge_base_name)
    print(f"Knowledge base '{knowledge_base_name}' deleted successfully.")
    
    index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
    index_client.delete_knowledge_source(knowledge_source=knowledge_source_name)
    print(f"Knowledge source '{knowledge_source_name}' deleted successfully.")
    
    index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
    index_client.delete_index(index_name)
    print(f"Index '{index_name}' deleted successfully.")
    ```

1. Set `search_endpoint` and `aoai_endpoint` to the values you obtained in [Get endpoints](#get-endpoints).

1. Run the following command to execute the code.

    ```console
    python agentic-retrieval.py
    ```

### Output

The output of the code should look similar to the following:

```
Documents uploaded to index 'earth-at-night' successfully.
Knowledge source 'earth-knowledge-source' created or updated successfully.
Knowledge base 'earth-knowledge-base' created or updated successfully.
Retrieved content from 'earth-knowledge-base' successfully.
response_content:
 Suburban belts brighten more in December because holiday lighting is concentrated in suburbs and outskirts—where yard space and single-family homes allow more displays—while central urban cores already have much higher absolute light levels so their fractional increase is smaller [ref_id:4][ref_id:7].
The Phoenix street grid is sharply visible from space because its regular block pattern plus continuous street, commercial, and corridor lighting (including the diagonal Grand Avenue) produce a bright, grid-like signature at night [ref_id:3][ref_id:0], whereas interstate corridors between Midwestern cities often appear comparatively dim because light is concentrated at urban nodes and ports while long stretches of highway and rivers lack continuous lighting [ref_id:7][ref_id:2].

activity_content:
 [
  {
    "id": 0,
    "type": "modelQueryPlanning",
    "elapsed_ms": 16946,
    "input_tokens": 1354,
    "output_tokens": 906
  },
  {
    "id": 1,
    "type": "searchIndex",
    "elapsed_ms": 887,
    "knowledge_source_name": "earth-knowledge-source",
    "query_time": "2025-11-05T16:17:48.345Z",
    "count": 22,
    "search_index_arguments": {
      "search": "December brightening in satellite nighttime lights: why do suburban belts show larger relative increases in December than urban cores despite higher absolute downtown light levels?"
    }
  },
  {
    "id": 2,
    "type": "searchIndex",
    "elapsed_ms": 632,
    "knowledge_source_name": "earth-knowledge-source",
    "query_time": "2025-11-05T16:17:48.985Z",
    "count": 10,
    "search_index_arguments": {
      "search": "Why is Phoenix's nighttime street grid so sharply visible from space? factors: street-light layout, lamp type, urban form, light scattering, and satellite sensor characteristics in Phoenix, Arizona."
    }
  },
  {
    "id": 3,
    "type": "searchIndex",
    "elapsed_ms": 420,
    "knowledge_source_name": "earth-knowledge-source",
    "query_time": "2025-11-05T16:17:49.406Z",
    "count": 11,
    "search_index_arguments": {
      "search": "Why are long stretches of interstate highways between Midwestern cities comparatively dim in satellite nighttime images? factors: highway lighting design, lamp spacing and type, vehicle headlights vs fixed lighting, and detection limits of nighttime sensors"
    }
  },
  {
    "id": 4,
    "type": "agenticReasoning",
    "reasoning_tokens": 72191,
    "retrieval_reasoning_effort": {
      "kind": "low"
    }
  },
  {
    "id": 5,
    "type": "modelAnswerSynthesis",
    "elapsed_ms": 22353,
    "input_tokens": 7564,
    "output_tokens": 1645
  }
]

references_content:
 [
  {
    "type": "searchIndex",
    "id": "0",
    "activity_source": 2,
    "source_data": {
      "id": "earth_at_night_508_page_105_verbalized",
      "page_chunk": "# Urban Structure\n\n## March 16, 2013\n\n### Phoenix Metropolitan Area at Night\n\nThis figure presents a nighttime satellite view of the Phoenix metropolitan area, highlighting urban structure and transport corridors. City lights illuminate the layout of several cities and major thoroughfares.\n\n**Labeled Urban Features:**\n\n- **Phoenix:** Central and brightest area in the right-center of the image.\n- **Glendale:** Located to the west of Phoenix, this city is also brightly lit.\n- **Peoria:** Further northwest, this area is labeled and its illuminated grid is seen.\n- **Grand Avenue:** Clearly visible as a diagonal, brightly lit thoroughfare running from Phoenix through Glendale and Peoria.\n- **Salt River Channel:** Identified in the southeast portion, running through illuminated sections.\n- **Phoenix Mountains:** Dark, undeveloped region to the northeast of Phoenix.\n- **Agricultural Fields:** Southwestern corner of the image, grid patterns are visible but with much less illumination, indicating agricultural land use.\n\n**Additional Notes:**\n\n- The overall pattern shows a grid-like urban development typical of western U.S. cities, with scattered bright nodes at major intersections or city centers.\n- There is a clear transition from dense urban development to sparsely populated or agricultural land, particularly evident towards the bottom and left of the image.\n- The illuminated areas follow the existing road and street grids, showcasing the extensive spread of the metropolitan area.\n\n**Figure Description:**  \nA satellite nighttime image captured on March 16, 2013, showing Phoenix and surrounding areas (including Glendale and Peoria). Major landscape and infrastructural features, such as the Phoenix Mountains, Grand Avenue, the Salt River Channel, and agricultural fields, are labeled. The image reveals the extent of urbanization and the characteristic street grid illuminated by city lights.\n\n---\n\nPage 89",
      "page_number": 105
    },
    "reranker_score": 2.722408,
    "doc_key": "earth_at_night_508_page_105_verbalized"
  },
  ... // Trimmed for brevity
]
Retrieved content from 'earth-knowledge-base' successfully.
response_content:
  ... // Trimmed for brevity

activity_content:
 [
  ... // Trimmed for brevity
]

references_content:
 [
  ... // Trimmed for brevity
]
Knowledge base 'earth-knowledge-base' deleted successfully.
Knowledge source 'earth-knowledge-source' deleted successfully.
Index 'earth-at-night' deleted successfully.
```

## Understand the code

Now that you've run the code, let's break down the key steps:

1. [Create a search index](#create-a-search-index)
1. [Upload documents to the index](#upload-documents-to-the-index)
1. [Create a knowledge source](#create-a-knowledge-source)
1. [Create a knowledge base](#create-a-knowledge-base)
1. [Set up messages](#set-up-messages)
1. [Run the retrieval pipeline](#run-the-retrieval-pipeline)
1. [Continue the conversation](#continue-the-conversation)

### Create a search index

In Azure AI Search, an index is a structured collection of data. The following code defines an index named `earth-at-night`.

The index schema contains fields for document identification and page content, embeddings, and numbers. The schema also includes configurations for semantic ranking and vector search, which uses your `text-embedding-3-large` deployment to vectorize text and match documents based on semantic similarity.

```python
# Create an index
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

**Reference:** [SearchField](/python/api/azure-search-documents/azure.search.documents.indexes.models.searchfield), [VectorSearch](/python/api/azure-search-documents/azure.search.documents.indexes.models.vectorsearch), [SemanticSearch](/python/api/azure-search-documents/azure.search.documents.indexes.models.semanticsearch), [SearchIndex](/python/api/azure-search-documents/azure.search.documents.indexes.models.searchindex), [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient)

### Upload documents to the index

Currently, the `earth-at-night` index is empty. The following code populates the index with JSON documents from [NASA's Earth at Night e-book](https://raw.githubusercontent.com/Azure-Samples/azure-search-sample-data/refs/heads/main/nasa-e-book/earth-at-night-json/documents.json). As required by Azure AI Search, each document conforms to the fields and data types defined in the index schema.

```python
# Upload documents
url = "https://raw.githubusercontent.com/Azure-Samples/azure-search-sample-data/refs/heads/main/nasa-e-book/earth-at-night-json/documents.json"
documents = requests.get(url).json()

with SearchIndexingBufferedSender(endpoint=search_endpoint, index_name=index_name, credential=credential) as client:
    client.upload_documents(documents=documents)

print(f"Documents uploaded to index '{index_name}' successfully.")
```

**Reference:** [SearchIndexingBufferedSender](/python/api/azure-search-documents/azure.search.documents.searchindexingbufferedsender)

### Create a knowledge source

A knowledge source is a reusable reference to source data. The following code defines a knowledge source named `earth-knowledge-source` that targets the `earth-at-night` index.

`source_data_fields` specifies which index fields are included in citation references. This example includes only human-readable fields to avoid lengthy, uninterpretable embeddings in responses.

```python
# Create a knowledge source
ks = SearchIndexKnowledgeSource(
    name=knowledge_source_name,
    description="Knowledge source for Earth at night data",
    search_index_parameters=SearchIndexKnowledgeSourceParameters(
        search_index_name=index_name,
        source_data_fields=[SearchIndexFieldReference(name="id"), SearchIndexFieldReference(name="page_number")]
    ),
)

index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
index_client.create_or_update_knowledge_source(knowledge_source=ks)
print(f"Knowledge source '{knowledge_source_name}' created or updated successfully.")
```

**Reference:** [SearchIndexKnowledgeSource](/python/api/azure-search-documents/azure.search.documents.indexes.models.searchindexknowledgesource)

### Create a knowledge base

To target `earth-knowledge-source` and your `gpt-5-mini` deployment at query time, you need a knowledge base. The following code defines a knowledge base named `earth-knowledge-base`.

`output_mode` is set to `ANSWER_SYNTHESIS`, enabling natural-language answers that cite the retrieved documents and follow the provided `answer_instructions`.

```python
# Create a knowledge base
aoai_params = AzureOpenAIVectorizerParameters(
    resource_url=aoai_endpoint,
    deployment_name=aoai_gpt_deployment,
    model_name=aoai_gpt_model,
)

knowledge_base = KnowledgeBase(
    name=knowledge_base_name,
    models=[KnowledgeBaseAzureOpenAIModel(azure_open_ai_parameters=aoai_params)],
    knowledge_sources=[
        KnowledgeSourceReference(
            name=knowledge_source_name
        )
    ],
    output_mode=KnowledgeRetrievalOutputMode.ANSWER_SYNTHESIS,
    answer_instructions="Provide a two sentence concise and informative answer based on the retrieved documents."
)

index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
index_client.create_or_update_knowledge_base(knowledge_base)
print(f"Knowledge base '{knowledge_base_name}' created or updated successfully.")
```

**Reference:** [KnowledgeBase](/python/api/azure-search-documents/azure.search.documents.indexes.models.knowledgebase)

### Set up messages

Messages are the input for the retrieval route and contain the conversation history. Each message includes a role that indicates its origin, such as `system` or `user`, and content in natural language. The LLM you use determines which roles are valid.

The following code creates a system message that instructs `earth-knowledge-base` to answer questions about the Earth at night and respond with "I don't know" when answers are unavailable.

```python
# Set up messages
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

### Run the retrieval pipeline

You're ready to run agentic retrieval. The following code sends a two-part user query to `earth-knowledge-base`, which:

1. Analyzes the entire conversation to infer the user's information need.
1. Decomposes the compound query into focused subqueries.
1. Runs the subqueries concurrently against your knowledge source.
1. Uses semantic ranker to rerank and filter the results.
1. Synthesizes the top results into a natural-language answer.

```python
# Run agentic retrieval
agent_client = KnowledgeBaseRetrievalClient(endpoint=search_endpoint, knowledge_base_name=knowledge_base_name, credential=credential)
query_1 = """
    Why do suburban belts display larger December brightening than urban cores even though absolute light levels are higher downtown?
    Why is the Phoenix nighttime street grid is so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?
    """

messages.append({
    "role": "user",
    "content": query_1
})

req = KnowledgeBaseRetrievalRequest(
    messages=[
        KnowledgeBaseMessage(
            role=m["role"],
            content=[KnowledgeBaseMessageTextContent(text=m["content"])]
        ) for m in messages if m["role"] != "system"
    ],
    knowledge_source_params=[
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name=knowledge_source_name,
            include_references=True,
            include_reference_source_data=True,
            always_query_source=True
        )
    ],
    include_activity=True,
    retrieval_reasoning_effort=KnowledgeRetrievalLowReasoningEffort
)

result = agent_client.retrieve(retrieval_request=req)
print(f"Retrieved content from '{knowledge_base_name}' successfully.")
```

**Reference:** [KnowledgeBaseRetrievalClient](/python/api/azure-search-documents/azure.search.documents.knowledgebases.knowledgebaseretrievalclient), [KnowledgeBaseRetrievalRequest](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest)

#### Review the response, activity, and references

The following code displays the response, activity, and references from the retrieval pipeline, where:

+ `response_contents` provides a synthesized, LLM-generated answer to the query that cites the retrieved documents. When answer synthesis isn't enabled, this section contains content extracted directly from the documents.

+ `activity_contents` tracks the steps that were taken during the retrieval process, including the subqueries generated by your `gpt-5-mini` deployment and the tokens used for semantic ranking, query planning, and answer synthesis.

+ `references_contents` lists the documents that contributed to the response, each one identified by their `doc_key`.

```python
# Display the response, activity, and references
response_contents = []
activity_contents = []
references_contents = []

response_parts = []
for resp in result.response:
    for content in resp.content:
        response_parts.append(content.text)
response_content = "\n\n".join(response_parts) if response_parts else "No response found on 'result'"

response_contents.append(response_content)

# Print the three string values
print("response_content:\n", response_content, "\n")

messages.append({
    "role": "assistant",
    "content": response_content
})

if result.activity:
    activity_content = json.dumps([a.as_dict() for a in result.activity], indent=2)
else:
    activity_content = "No activity found on 'result'"
    
activity_contents.append(activity_content)
print("activity_content:\n", activity_content, "\n")

if result.references:
    references_content = json.dumps([r.as_dict() for r in result.references], indent=2)
else:
    references_content = "No references found on 'result'"
    
references_contents.append(references_content)
print("references_content:\n", references_content)
```

### Continue the conversation

The following code continues the conversation with `earth-knowledge-base`. After you send this user query, the knowledge base fetches relevant content from `earth-knowledge-source` and appends the response to the messages list.

```python
# Continue the conversation
query_2 = "How do I find lava at night?"
messages.append({
    "role": "user",
    "content": query_2
})

req = KnowledgeBaseRetrievalRequest(
    messages=[
        KnowledgeBaseMessage(
            role=m["role"],
            content=[KnowledgeBaseMessageTextContent(text=m["content"])]
        ) for m in messages if m["role"] != "system"
    ],
    knowledge_source_params=[
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name=knowledge_source_name,
            include_references=True,
            include_reference_source_data=True,
            always_query_source=True
        )
    ],
    include_activity=True,
    retrieval_reasoning_effort=KnowledgeRetrievalLowReasoningEffort
)

result = agent_client.retrieve(retrieval_request=req)
print(f"Retrieved content from '{knowledge_base_name}' successfully.")
```

#### Review the new response, activity, and references

The following code displays the new response, activity, and references from the retrieval pipeline.

```python
# Display the new retrieval response, activity, and references
response_parts = []
for resp in result.response:
    for content in resp.content:
        response_parts.append(content.text)
response_content = "\n\n".join(response_parts) if response_parts else "No response found on 'result'"

response_contents.append(response_content)

# Print the three string values
print("response_content:\n", response_content, "\n")

if result.activity:
    activity_content = json.dumps([a.as_dict() for a in result.activity], indent=2)
else:
    activity_content = "No activity found on 'result'"
    
activity_contents.append(activity_content)
print("activity_content:\n", activity_content, "\n")

if result.references:
    references_content = json.dumps([r.as_dict() for r in result.references], indent=2)
else:
    references_content = "No references found on 'result'"
    
references_contents.append(references_content)
print("references_content:\n", references_content)
```

## Clean up resources

[!INCLUDE [clean up resources (paid)](../resource-cleanup-paid.md)]

Otherwise, the following code from `agentic-retrieval.py` deleted the objects you created in this quickstart.

### Delete the knowledge base

```python
index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
index_client.delete_knowledge_base(knowledge_base_name)
print(f"Knowledge base '{knowledge_base_name}' deleted successfully.")
```

### Delete the knowledge source

```python
index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
index_client.delete_knowledge_source(knowledge_source=knowledge_source_name)
print(f"Knowledge source '{knowledge_source_name}' deleted successfully.")
```

### Delete the search index

```python
index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
index_client.delete_index(index_name)
print(f"Index '{index_name}' deleted successfully.")
```
