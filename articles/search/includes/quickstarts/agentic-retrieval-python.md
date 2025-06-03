---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 05/30/2025
---

[!INCLUDE [Feature preview](../previews/preview-generic.md)]

In this quickstart, you use [agentic retrieval](../../search-agentic-retrieval-concept.md) to create a conversational search experience powered by large language models (LLMs) and your proprietary data. Agentic retrieval breaks down complex user queries into subqueries, runs the subqueries in parallel, and extracts grounding data from documents indexed in Azure AI Search. The output is intended for integration with agentic and custom chat solutions.

Although you can provide your own data, this quickstart uses [sample JSON documents](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/nasa-e-book/earth-at-night-json) from NASA's Earth at Night e-book. The documents describe general science topics and images of Earth at night as observed from space.

This quickstart is based on the [Quickstart-Agentic-Retrieval](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/Quickstart-Agentic-Retrieval) Jupyter notebook on GitHub.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

+ An [Azure AI Search service](../../search-create-service-portal.md) on the Basic tier or higher with [semantic ranker enabled](../../semantic-how-to-enable-disable.md).

+ An [Azure OpenAI resource](/azure/ai-services/openai/how-to/create-resource).

+ [Visual Studio Code](https://code.visualstudio.com/download) with the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [Jupyter package](https://pypi.org/project/jupyter/).

## Deploy models

To run agentic retrieval, you must deploy the following models to your Azure OpenAI resource:

+ An LLM for query planning.

+ An LLM for answer generation.

+ (Optional) An embedding model for vector queries.

Agentic retrieval [supports several models](../../search-agentic-retrieval-how-to-create.md#supported-models), but this quickstart assumes `gpt-4o-mini` for both LLMs and `text-embedding-3-large` for the embedding model.

To deploy the Azure OpenAI models:

1. Sign in to the [Azure AI Foundry portal](https://ai.azure.com/) and select your Azure OpenAI resource.

1. From the left pane, select **Model catalog**.

1. Select **gpt-4o-mini**, and then select **Use this model**.

1. Specify a deployment name. To simplify your code, we recommend **gpt-4o-mini**.

1. Accept the defaults.

1. Select **Deploy**.

1. Repeat the previous steps for **text-embedding-3-large**.

## Configure role-based access

Azure AI Search needs access to your Azure OpenAI models. For this task, you can use API keys or Microsoft Entra ID with role assignments. Keys are easier to start with, but roles are more secure. This quickstart assumes roles.

To configure the recommended role-based access:

1. Sign in to the [Azure portal](https://portal.azure.com/).

1. [Enable role-based access](../../search-security-enable-roles.md) on your Azure AI Search service.

1. [Create a system-assigned managed identity](../../search-howto-managed-identities-data-sources.md#create-a-system-managed-identity) on your Azure AI Search service.

1. On your Azure AI Search service, [assign the following roles](../../search-security-rbac.md#how-to-assign-roles-in-the-azure-portal) to yourself.

    + **Search Service Contributor**

    + **Search Index Data Contributor**

    + **Search Index Data Reader**

1. On your Azure OpenAI resource, assign **Cognitive Services User** to the managed identity of your search service.

## Get endpoints

In your code, you specify the following endpoints to establish connections with Azure AI Search and Azure OpenAI. These steps assume that you configured role-based access in the previous section.

To obtain your service endpoints:

1. Sign in to the [Azure portal](https://portal.azure.com/).

1. On your Azure AI Search service:

    1. From the left pane, select **Overview**.

    1. Copy the URL, which should be similar to `https://my-service.search.windows.net`.

1. On your Azure OpenAI resource:

    1. From the left pane, select **Resource Management** > **Keys and Endpoint**.

    1. Copy the URL, which should be similar to `https://my-resource.openai.azure.com`.

## Connect from your local system

You configured role-based access to interact with Azure AI Search and Azure OpenAI. From the command line, use the Azure CLI to sign in to the same subscription and tenant for both services. For more information, see [Quickstart: Connect without keys](../../search-get-started-rbac.md).

```azurecli
az account show

az account set --subscription <PUT YOUR SUBSCRIPTION ID HERE>
    
az login --tenant <PUT YOUR TENANT ID HERE>
```

## Install packages and load connections

Before you run any code, install Python packages and define credentials, endpoints, and deployment details for connections to Azure AI Search and Azure OpenAI. These values are used in subsequent operations.

To install the packages and load the connections:

1. In Visual Studio Code, create a `.ipynb` file.

1. Install the following packages.

    ```Python
    ! pip install azure-search-documents==11.6.0b12 --quiet
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

    endpoint = "PUT YOUR SEARCH SERVICE ENDPOINT HERE"
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(credential, "https://search.azure.com/.default")
    azure_openai_endpoint = "PUT YOUR AZURE OPENAI ENDPOINT HERE"
    azure_openai_gpt_deployment = "gpt-4o-mini"
    azure_openai_gpt_model = "gpt-4o-mini"
    azure_openai_api_version = "2025-03-01-preview"
    azure_openai_embedding_deployment = "text-embedding-3-large"
    azure_openai_embedding_model = "text-embedding-3-large"
    index_name = "earth_at_night"
    agent_name = "earth-search-agent"
    answer_model = "gpt-4o-mini"
    api_version = "2025-05-01-Preview"
    ```

1. Replace `endpoint` and `azure_openai_endpoint` with the values you obtained in [Get endpoints](#get-endpoints).

1. To verify the variables, run the code cell.

## Create a search index

In Azure AI Search, an index is a structured collection of data. The following code defines an index named `earth_at_night`, which you specified using the `index_name` variable in the previous section.

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

The index schema contains fields for document identification and page content, embeddings, and numbers. It also includes configurations for semantic ranking and vector queries, which use the `text-embedding-3-large` model you previously deployed.

> [!IMPORTANT]
> Agentic retrieval has two token-based billing models:
>
> + Billing from Azure OpenAI for query planning.
> + Billing from Azure AI Search for query execution (semantic ranking).
>
> Semantic ranking is free in the initial public preview. After the preview, standard token billing applies. For more information, see [Availability and pricing of agentic retrieval](../../search-agentic-retrieval-concept.md#availability-and-pricing).

## Upload documents to the index

Currently, the `earth_at_night` index is empty. Run the following code to populate the index with JSON documents from NASA's Earth at Night e-book. As required by Azure AI Search, each document conforms to the fields and data types defined in the index schema.

```Python
from azure.search.documents import SearchIndexingBufferedSender
import requests

url = "https://raw.githubusercontent.com/Azure-Samples/azure-search-sample-data/refs/heads/main/nasa-e-book/earth-at-night-json/documents.json"
documents = requests.get(url).json()

with SearchIndexingBufferedSender(endpoint=endpoint, index_name=index_name, credential=credential) as client:
    client.upload_documents(documents=documents)

print(f"Documents uploaded to index '{index_name}'")
```

## Create a knowledge agent

To connect Azure AI Search to your `gpt-4o-mini` deployment and target the `earth_at_night` index at query time, you need a knowledge agent. The following code defines a knowledge agent named `earth-search-agent`, which you specified using the `agent_name` variable in a previous section.

To ensure relevant and semantically meaningful responses, `default_reranker_threshold` is set to exclude responses with a reranker score of `2.5` or lower.

```Python
from azure.search.documents.indexes.models import KnowledgeAgent, KnowledgeAgentAzureOpenAIModel, KnowledgeAgentTargetIndex, KnowledgeAgentRequestLimits, AzureOpenAIVectorizerParameters

agent = KnowledgeAgent(
    name=agent_name,
    models=[
        KnowledgeAgentAzureOpenAIModel(
            azure_open_ai_parameters=AzureOpenAIVectorizerParameters(
                resource_url=azure_openai_endpoint,
                deployment_name=azure_openai_gpt_deployment,
                model_name=azure_openai_gpt_model
            )
        )
    ],
    target_indexes=[
        KnowledgeAgentTargetIndex(
            index_name=index_name,
            default_reranker_threshold=2.5
        )
    ],
)

index_client.create_or_update_agent(agent)
print(f"Knowledge agent '{agent_name}' created or updated successfully")
```

## Set up messages

The next step is to define the knowledge agent instructions and conversation context using the `messages` array. Each message includes a `role`, such as `user` or `assistant`, and `content` in natural language. A user message represents the query to be processed, while an assistant message guides the knowledge agent on how to respond. During the retrieval process, these messages are sent to an LLM to extract relevant responses from indexed documents.

For now, create the following assistant message, which instructs `earth-search-agent` to answer questions about the Earth at night, cite sources using their `ref_id`, and respond with "I don't know" when answers are unavailable.

```Python
instructions = """
An Q&A agent that can answer questions about the Earth at night.
Sources have a JSON format with a ref_id that must be cited in the answer.
If you do not have the answer, respond with "I don't know".
"""

messages = [
    {
        "role": "assistant",
        "content": instructions
    }
]
```

## Run the retrieval pipeline

You're ready to initiate the agentic retrieval pipeline. The input for this pipeline is the `messages` array, whose conversation history includes the instructions you previously provided and user queries. Additionally, `target_index_params` specifies the index to query and other configurations, such as the semantic ranker threshold.

The following code sends a two-part user query to `earth-search-agent`, which deconstructs the query into subqueries, runs the subqueries against both text fields and vector embeddings in the `earth_at_night` index, and ranks and merges the results. The response is then appended to the `messages` array.

```Python
from azure.search.documents.agent import KnowledgeAgentRetrievalClient
from azure.search.documents.agent.models import KnowledgeAgentRetrievalRequest, KnowledgeAgentMessage, KnowledgeAgentMessageTextContent, KnowledgeAgentIndexParams

agent_client = KnowledgeAgentRetrievalClient(endpoint=endpoint, agent_name=agent_name, credential=credential)

messages.append({
    "role": "user",
    "content": """
    Why do suburban belts display larger December brightening than urban cores even though absolute light levels are higher downtown?
    Why is the Phoenix nighttime street grid is so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?
    """
})

retrieval_result = agent_client.knowledge_retrieval.retrieve(
    retrieval_request=KnowledgeAgentRetrievalRequest(
        messages=[KnowledgeAgentMessage(role=msg["role"], content=[KnowledgeAgentMessageTextContent(text=msg["content"])]) for msg in messages],
        target_index_params=[KnowledgeAgentIndexParams(index_name=index_name, reranker_threshold=2.5)]
    )
)
messages.append({
    "role": "assistant",
    "content": retrieval_result.response[0].content[0].text
})
```

### Review the response, activity, and results

To output the response, activity, and results of the retrieval pipeline, run the following code.

```Python
import textwrap
import json

print("Response")
print(textwrap.fill(retrieval_result.response[0].content[0].text, width=120))

print("Activity")
print(json.dumps([a.as_dict() for a in retrieval_result.activity], indent=2))

print("Results")
print(json.dumps([r.as_dict() for r in retrieval_result.references], indent=2))
```

The output should be similar to the following example, where:

+ `Response` provides a text string of the most relevant documents (or chunks) in the search index based on the user query. As shown later in this quickstart, you can pass this string to an LLM for answer generation.

+ `Activity` tracks the steps that were taken during the retrieval process, including the subqueries generated by your `gpt-4o-mini` deployment and the tokens used for query planning and execution.

+ `Results` lists the documents that contributed to the response, each one identified by their `doc_key`.

```
Response
[{"ref_id":1,"content":"# Urban Structure\n\n## March 16, 2013\n\n### Phoenix Metropolitan Area at Night\n\nThis figure presents a nighttime satellite view of the Phoenix metropolitan area, highlighting urban structure and transport corridors. City lights illuminate the layout of several cities and major thoroughfares.\n\n**Labeled Urban Features:**\n\n- **Phoenix:** Central and brightest area in the right-center of the image.\n- **Glendale:** Located to the west of Phoenix, this city is also brightly lit.\n- **Peoria:** Further northwest, this area is labeled and its illuminated grid is seen.\n- **Grand Avenue:** Clearly visible as a diagonal, brightly lit thoroughfare running from Phoenix through Glendale and Peoria.\n- **Salt River Channel:** Identified in the southeast portion, running through illuminated sections.\n- **Phoenix Mountains:** Dark, undeveloped region to the northeast of Phoenix.\n- **Agricultural Fields:** Southwestern corner of the image, grid patterns are visible but with much less illumination, indicating agricultural land use.\n\n**Additional Notes:**\n\n- The overall pattern shows a grid-like urban development typical of western U.S. cities, with scattered bright nodes at major intersections or city centers.\n- There is a clear transition from dense urban development to sparsely populated or agricultural land, particularly evident towards the bottom and left of the image.\n- The illuminated areas follow the existing road and street grids, showcasing the extensive spread of the metropolitan area.\n\n**Figure Description:**  \nA satellite nighttime image captured on March 16, 2013, showing Phoenix and surrounding areas (including Glendale and Peoria). Major landscape and infrastructural features, such as the Phoenix Mountains, Grand Avenue, the Salt River Channel, and agricultural fields, are labeled. The image reveals the extent of urbanization and the characteristic street grid illuminated by city lights.\n\n---\n\nPage 89"},{"ref_id":0,"content":"<!-- PageHeader=\"Urban Structure\" -->\n\n### Location of Phoenix, Arizona\n\nThe image depicts a globe highlighting the location of Phoenix, Arizona, in the southwestern United States, marked with a blue pinpoint on the map of North America. Phoenix is situated in the central part of Arizona, which is in the southwestern region of the United States.\n\n---\n\n### Grid of City Blocks-Phoenix, Arizona\n\nLike many large urban areas of the central and western United States, the Phoenix metropolitan area is laid out along a regular grid of city blocks and streets. While visible during the day, this grid is most evident at night, when the pattern of street lighting is clearly visible from the low-Earth-orbit vantage point of the ISS.\n\nThis astronaut photograph, taken on March 16, ... highlighted in this image is urbanized, there are several noticeably dark areas. The Phoenix Mountains are largely public parks and recreational land. To the west, agricultural fields provide a sharp contrast to the lit streets of residential developments. The Salt River channel appears as a dark ribbon within the urban grid.\n\n\n<!-- PageFooter=\"Earth at Night\" -->\n<!-- PageNumber=\"88\" -->"}]
Activity
[
  {
    "id": 0,
    "type": "ModelQueryPlanning",
    "input_tokens": 1407,
    "output_tokens": 309
  },
  {
    "id": 1,
    "type": "AzureSearchQuery",
    "target_index": "earth_at_night",
    "query": {
      "search": "suburban belts December brightening urban cores light levels"
    },
    "query_time": "2025-05-06T20:47:01.814Z",
    "elapsed_ms": 714
  },
  {
    "id": 2,
    "type": "AzureSearchQuery",
    "target_index": "earth_at_night",
    "query": {
      "search": "Phoenix nighttime street grid visibility from space"
    },
    "query_time": "2025-05-06T20:47:02.230Z",
    "count": 2,
    "elapsed_ms": 416
  }
]
Results
[
  {
    "type": "AzureSearchDoc",
    "id": "0",
    "activity_source": 2,
    "doc_key": "earth_at_night_508_page_104_verbalized"
  },
  {
    "type": "AzureSearchDoc",
    "id": "1",
    "activity_source": 2,
    "doc_key": "earth_at_night_508_page_105_verbalized"
  }
]
```

## Create the Azure OpenAI client

To extend the retrieval pipeline from answer *extraction* to answer *generation*, set up the Azure OpenAI client to interact with your `gpt-4o-mini` deployment, which you specified using the `answer_model` variable in a previous section.

```Python
from openai import AzureOpenAI
from azure.identity import get_bearer_token_provider

azure_openai_token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
client = AzureOpenAI(
    azure_endpoint=azure_openai_endpoint,
    azure_ad_token_provider=azure_openai_token_provider,
    api_version=azure_openai_api_version
)
```

### Use the Responses API to generate an answer

You can now use the Responses API to generate a detailed answer based on the indexed documents. The following code sends the `messages` array, which contains the conversation history, to your `gpt-4o-mini` deployment.

```Python
response = client.responses.create(
    model=answer_model,
    input=messages
)

wrapped = textwrap.fill(response.output_text, width=100)
print(wrapped)
```

The output should be similar to the following example, which uses the reasoning capabilities of `gpt-4o-mini` to provide contextually relevant answers.

```
Suburban belts often exhibit larger December brightening than urban cores primarily because of the type of development and light distribution in those areas. Suburbs tend to have more uniform and expansive lighting, making them more visible in nighttime satellite images. In contrast, urban cores, although having higher absolute light levels, often contain dense building clusters that can cause light to be obscured or concentrated in smaller areas, leading to less visible brightening when viewed from space.  Regarding the visibility of the Phoenix nighttime street grid from space, it is attributed to the city's grid layout and the intensity of its street lighting. The grid pattern of the streets and the significant development around them create a stark contrast against less developed areas. Conversely, large stretches of interstate in the Midwest may remain dimmer due to fewer densely populated structures and less intensive street lighting, resulting in less illumination overall.  For more detailed insights, you can refer to the sources: [0] and [1].
```

### Use the Chat Completions API to generate an answer

Alternatively, you can use the Chat Completions API for answer generation.

```Python
response = client.chat.completions.create(
    model=answer_model,
    messages=messages
)

wrapped = textwrap.fill(response.choices[0].message.content, width=100)
print(wrapped)
```

The output should be similar to the following example.

```
Suburban belts tend to display larger December brightening than urban cores, despite the absolute light levels being higher in downtown areas, due to the differing density of light sources and how light scatters. In urban cores, the intense concentration of lights may result in a more uniform light distribution that can obscure the brightening effect, whereas suburban areas, with their lower density of lights and more open spaces, allow for clearer visibility of atmospheric light scattering, thus enhancing the brightening effect in those regions.  As for why the Phoenix nighttime street grid is sharply visible from space compared to the dim stretches of the interstate between Midwestern cities, it primarily relates to urban planning and development patterns. The Phoenix metropolitan area is laid out along a regular grid of city blocks that include extensive street lighting, making the urban structure distinctly visible from space. In contrast, the interstates between Midwestern cities often traverse areas with less concentrated development and fewer bright lighting sources, leading to these sections appearing dimmer in nighttime imagery [1; ref_id:1].
```

## Continue the conversation

Continue the conversation by sending another user query to `earth-search-agent`. The following code reruns the retrieval pipeline, fetching relevant content from the `earth_at_night` index and appending the response to the `messages` array. However, unlike before, you can now use the Azure OpenAI client to generate an answer based on the retrieved content.

```Python
messages.append({
    "role": "user",
    "content": "How do I find lava at night?"
})

retrieval_result = agent_client.knowledge_retrieval.retrieve(
    retrieval_request=KnowledgeAgentRetrievalRequest(
        messages=[KnowledgeAgentMessage(role=msg["role"], content=[KnowledgeAgentMessageTextContent(text=msg["content"])]) for msg in messages],
        target_index_params=[KnowledgeAgentIndexParams(index_name=index_name, reranker_threshold=2.5)]
    )
)
messages.append({
    "role": "assistant",
    "content": retrieval_result.response[0].content[0].text
})
```

### Review the new response, activity, and results

To output the latest response, activity, and results of the retrieval pipeline, run the following code.

```Python
import textwrap
import json

print("Response")
print(textwrap.fill(retrieval_result.response[0].content[0].text, width=120))

print("Activity")
print(json.dumps([a.as_dict() for a in retrieval_result.activity], indent=2))

print("Results")
print(json.dumps([r.as_dict() for r in retrieval_result.references], indent=2))
```

## Generate an LLM-powered answer

Now that you've sent multiple user queries, use the Responses API to generate an answer based on the indexed documents and conversation history, which is captured in the `messages` array.

```Python
response = client.responses.create(
    model=answer_model,
    input=messages
)

wrapped = textwrap.fill(response.output_text, width=100)
print(wrapped)
```

The output should be similar to the following example.

```
To find lava at night, you can look for the following signs:  1. **Active Volcanoes**: Research volcanoes that are currently active. Notable examples include Mount Etna in Italy and Kilauea in Hawaii. Both have had significant eruptions that can be observed at night due to the glow of lava. 2. **Satellite Imagery**: Use satellite imagery, especially those from sources like VIIRS (Visible Infrared Imaging Radiometer Suite) on the Suomi NPP satellite, which captures nighttime images of active lava flows. During eruptions, lava glows brightly in thermal infrared images, making it detectable from space.  3. **Safe Viewing Locations**: If you’re near an active volcano, find designated viewing areas for safety. Many national parks with volcanoes offer nighttime lava viewing experiences.  4. **Moonlight**: The presence of moonlight can enhance visibility, allowing you to spot lava flows more easily against the backdrop of the dark landscape.  5. **Monitoring Reports**: Follow updates from geological services or local authorities that monitor volcanic activity, which often provide real-time information about eruptions and visible lava flows at night.  6. **Photography**: If you're an enthusiast, consider using long-exposure photography techniques to capture the glow of lava flows at night.  For more information on observing volcanic activity, satellite imagery can provide vital data for detecting lava flows and volcanic eruptions.
```

## Clean up resources

When working in your own subscription, it's a good idea to finish a project by determining whether you still need the resources you created. Resources that are left running can cost you money. You can delete resources individually, or you can delete the resource group to delete the entire set of resources.

In the Azure portal, you can find and manage resources by selecting **All resources** or **Resource groups** from the left pane. You can also run the following code to delete the objects you created in this quickstart.

### Delete the knowledge agent

```Python
index_client = SearchIndexClient(endpoint=endpoint, credential=credential)
index_client.delete_agent(agent_name)
print(f"Knowledge agent '{agent_name}' deleted successfully")
```

### Delete the search index

```Python
index_client = SearchIndexClient(endpoint=endpoint, credential=credential)
index_client.delete_index(index_name)
print(f"Index '{index_name}' deleted successfully")
```
