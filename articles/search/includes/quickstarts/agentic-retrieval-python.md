---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 05/05/2025
---

[!INCLUDE [Feature preview](../previews/preview-generic.md)]

In this quickstart, you use [agentic retrieval](../../search-agentic-retrieval-concept.md) to create a conversational search experience powered by large language models (LLMs) and your proprietary data. Agentic retrieval breaks down complex user queries into subqueries, runs the subqueries in parallel, and extracts grounding data from documents indexed in Azure AI Search. The output is intended for integration with custom chat solutions.

Although you can provide your own data, this quickstart uses [sample JSON documents](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/nasa-e-book/earth-at-night-json) from NASA's Earth at Night e-book. The documents describe the urban structures and lighting patterns of Phoenix, Arizona as observed from space.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

+ An [Azure AI Search service](../../search-create-service-portal.md) on the Basic tier or higher with [semantic ranker enabled](../../semantic-how-to-enable-disable.md).

+ An [Azure OpenAI resource](/azure/ai-services/openai/how-to/create-resource) in the [same region](#same-region-requirement) as your Azure AI Search service.

+ [Visual Studio Code](https://code.visualstudio.com/download) with the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [Jupyter package](https://pypi.org/project/jupyter/).

### Same-region requirement

Agentic retrieval invokes text-to-vector conversion during queries, which requires Azure AI Search and Azure OpenAI to be in the same region. To meet this requirement:

1. [Choose an Azure OpenAI region](/azure/ai-services/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions#global-standard-model-availability) in which `text-embedding-3-large` is available. Agentic retrieval supports other embedding models, but this quickstart assumes the one previously mentioned.

1. Confirm that [Azure AI Search is available in the same region](../../search-region-support.md#azure-public-regions). The region must also support semantic ranker, which is essential to query execution during agentic retrieval.

1. Deploy both resources in the same region.

## Deploy models

To use agentic retrieval, you must deploy two supported chat models (one for query planning, one for generating answers) and a supported embedding model (for vector queries) to your Azure OpenAI resource. This quickstart assumes `gpt-4o` and `gpt-4o-mini` for the chat models and `text-embedding-3-large` for the embedding model.

> [!IMPORTANT]
> Whatever models you use, make sure they meet the [same-region requirement](#same-region-requirement) for Azure AI Search and Azure OpenAI.

To deploy the Azure OpenAI models:

1. Sign in to the [Azure AI Foundry portal](https://ai.azure.com/).

1. On the home page, find the Azure OpenAI tile and select **Let's go**.

    :::image type="content" source="../../media/search-get-started-agentic-retrieval/azure-openai-lets-go-tile.png" alt-text="Screenshot of the Azure OpenAI tile in the Azure AI Foundry portal." border="true" lightbox="media/search-get-started-agentic-retrieval/azure-openai-lets-go-tile.png":::

   Your most recently used Azure OpenAI resource appears. If you have multiple Azure OpenAI resources, select **All resources** to switch between them.

1. From the left pane, select **Model catalog**.

1. Deploy `gpt-4o`, `gpt-4o-mini`, and `text-embedding-3-large` to your Azure OpenAI resource.

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

## Configure role-based access

Azure AI Search needs access to your Azure OpenAI models. For this task, you can use API keys or Microsoft Entra ID with role assignments. Keys are easier to start with, but roles are more secure. This quickstart assumes roles.

To configure the recommended role-based access:

1. Sign in to the [Azure portal](https://portal.azure.com/).

1. [Enable role-based access](../../search-security-enable-roles.md) on your Azure AI Search service.

1. [Create a system-assigned managed identity](../../search-howto-managed-identities-data-sources.md#create-a-system-managed-identity) on your Azure AI Search service.

1. On your Azure AI Search service, [assign the following roles](../../search-security-rbac.md#how-to-assign-roles-in-the-azure-portal) to yourself.

    + **Owner/Contributor** or **Search Service Contributor**
    + **Search Index Data Contributor**
    + **Search Index Data Reader**

1. On your Azure OpenAI resource, assign **Cognitive Services User** to the managed identity of your search service.

## Get service endpoints

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

You configured role-based access to interact with Azure AI Search and Azure OpenAI. From the command line, use the Azure CLI to sign in to the subscription and tenant for both services. For more information, see [Quickstart: Connect without keys](../../search-get-started-rbac.md).

```Azure CLI
az account show

az account set --subscription <PUT YOUR SUBSCRIPTION ID HERE>
    
az login --tenant <PUT YOUR TENANT ID HERE>
```

## Install packages and load connections

Before you run any code, install Python packages and define credentials, endpoints, and deployment details for connections to Azure AI Search and Azure OpenAI. These values are used in later sections of this quickstart.

To install the packages and load the connections:

1. In Visual Studio Code, create a `.ipynb` file.

1. In a new code cell, install the following Python packages.

    ```Python
    ! pip install azure-search-documents==11.6.0a20250505003 --quiet
    ! pip install https://pkgs.dev.azure.com/azure-sdk/public/_packaging/azure-sdk-for-python/pypi/simple/ --quiet
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
    index_name = "earth_at_night"
    azure_openai_endpoint = "PUT YOUR AZURE OPENAI ENDPOINT HERE"
    azure_openai_gpt_deployment = "gpt-4o-mini"
    azure_openai_gpt_model = "gpt-4o-mini"
    azure_openai_api_version = "2025-03-01-preview"
    azure_openai_embedding_deployment = "text-embedding-3-large"
    azure_openai_embedding_model = "text-embedding-3-large"
    agent_name = "earth-search-agent"
    answer_model = "gpt-4o"
    api_version = "2025-05-01-Preview"
    ```

1. Replace `endpoint` and `azure_openai_endpoint` with the values you obtained in [Get endpoints](#get-endpoints).

1. To verify the variables, run the code cell.

## Create a search index

In Azure AI Search, an index is a structured collection of searchable data. The following request defines a new index named `earth-at-night`, which you specified using the `@index-name` variable in the previous section.

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

## Upload documents to the index

Currently, the `earth-at-night` index is empty. Run the following code to populate the index with JSON documents from NASA's Earth at Night e-book. Each document contains embeddings for vectorization and metadata for page numbering.

```Python
from azure.search.documents import SearchIndexingBufferedSender
import requests

url = "https://raw.githubusercontent.com/Azure-Samples/azure-search-sample-data/refs/heads/main/nasa-e-book/earth-at-night-json/documents.json"
documents = requests.get(url).json()

with SearchIndexingBufferedSender(endpoint=endpoint, index_name=index_name, credential=credential) as client:
    client.upload_documents(documents=documents)

print(f"Documents uploaded to index '{index_name}'")
```

## Create a search agent

To connect Azure AI Search to your `gpt-4o-mini` deployment and target the `earth-at-night` index at query time, you need a search agent. The following request defines an agent named `earth-search-agent`, which you specified using the `@agent-name` variable in a previous section.

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

### Set up messages for the agent

The next step is to define how `earth-search-agent` should respond to user queries. In this case, you tell the agent to answer questions about the Earth at night, cite sources using their `ref_id`, and respond with "I don't know" when it can't find an answer.

```Python
instructions = """
An Q&A agent that can answer questions about the Earth at night.
Sources have a JSON format with a ref_id that must be cited in the answer.
If you do not have the answer, respond with "I don't know".
"""

messages = [
    {
        "role": "system",
        "content": instructions
    }
]
```

## Run the retrieval pipeline

You're ready to run the agentic retrieval pipeline. The following code sends a user query to `earth-search-agent`, which deconstructs the query into subqueries, processes the subqueries simultaneously, and merges and ranks results from the `earth-at-night` index. The response is then appended to the `messages` list.

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

To output the retrieval response, activity, and results, run the following code.

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

+ `Respone` provides a text string of the most relevant documents (or chunks) in the search index based on the user query.

+ `Activity` tracks the steps that were taken during the retrieval process, including the subqueries generated by your `gpt-4o-mini` deployment.

+ `Results` lists the documents that contributed to the response, identified by their `doc_key`.

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

To extend the retrieval pipeline from answer extraction to answer generation, set up the Azure OpenAI client to interact with your `gpt-4o` deployment, which you specified using the `@answer_model` variable in a previous section.

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

You can now use the Responses API to generate a detailed answer. The following code sends the `messages` list, which includes the user query and prior conversation context, to the `gpt-4o` model.

```Python
response = client.responses.create(
    model=answer_model,
    input=messages
)

wrapped = textwrap.fill(response.output_text, width=100)
print(wrapped)
```

The output should be similar to the following example, which combines insights from the indexed data and the reasoning capabilities of `gpt-4o`.

```
1. **Why do suburban belts display larger December brightening than urban cores even though absolute light levels are higher downtown?**   Suburban belts experience larger December brightening likely due to holiday-related displays such as decorative lighting on homes and public spaces, which become more widespread during the holiday season. In contrast, urban cores already have high levels of constant lighting from commercial areas, buildings, and streets year-round, leaving less room for noticeable seasonal changes in brightness. The suburban areas, with more residential lighting influence, therefore show a more significant relative increase in brightness during December holidays.    ---  2. **Why is the Phoenix nighttime street grid so sharply visible from space, whereas large stretches of the interstate between Midwestern cities remain comparatively dim?** The Phoenix metropolitan area is planned around a regular grid of streets, which are extensively lit at night, creating a clear and uniform pattern visible from space. Major corridors such as the Grand Avenue and intersections housing shopping centers, gas stations, and strip malls contribute further to the brightness. This urban development style, fueled by automobile use and outward expansion, results in more consistent lighting compared to the interstate highways between Midwestern cities, which are often surrounded by sparsely populated rural areas with fewer sources of light beyond the highways themselves.    **Sources:** [1], [0]
```

### Use the Chat Completions API to generate an answer

Alternatively, you can use the Chat Completions API to generate a detailed answer. The following code sends the `messages` list, which includes the user query and prior conversation context, to the `gpt-4o` model.

```Python
response = client.chat.completions.create(
    model=answer_model,
    messages=messages
)

wrapped = textwrap.fill(response.choices[0].message.content, width=100)
print(wrapped)
```

The output should be similar to the following example, which combines insights from the indexed data and the reasoning capabilities of `gpt-4o`.

```
1. Suburban belts tend to display larger December brightening compared to urban cores despite the higher absolute brightness in city centers due to differing sources of light emission. Urban cores are already saturated with high levels of static artificial lighting (e.g., from buildings and streetlights), so seasonal increases in illumination—such as decorative holiday lights in December—have a smaller proportional impact. In contrast, suburban areas typically start from a lower baseline level of lighting, making additional light sources, like holiday displays, more noticeable in satellite imagery.  2. The Phoenix nighttime street grid is sharply visible from space because of its regular, well-organized grid layout of city blocks, paired with consistent illumination provided by streetlights and commercial properties at intersections. The metropolitan area's design reflects the characteristic urban planning of the western United States, focusing on automobile infrastructure and outward expansion. In comparison, interstates between midwestern cities appear dimmer because they are primarily illuminated at major intersections or rest stops, with the vast stretches in between remaining largely unlit. Consequently, road lighting is sparse and unevenly distributed over rural areas, which are less populated and lack the dense, uniformly lit patterns seen in urban grids like Phoenix's [0][1].
```

## Continue the conversation

Continue the conversation by sending another user query to `earth-search-agent`. The following code retrieves relevant information from the `earth-at-night` index and appends the agent's response to the `messages` list. However, unlike before, you can now use the Azure OpenAI client to generate an answer based on the retrieved data.

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

To output the new retrieval response, activity, and results, run the following code.

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

The output should be similar to the following example.

```
Response
Response [{"ref_id":5,"content":"## Nature's Light Shows\n\nAt night, with the light of the Sun removed, nature's brilliant glow from Earth's surface becomes visible to the naked eye from space. Some of Earth's most spectacular light shows are natural, like the aurora borealis, or Northern Lights, in the Northern Hemisphere (aurora australis, or Southern Lights, in the Southern Hemisphere). The auroras are natural electrical phenomena caused by charged particles that race from the Sun toward Earth, inducing chemical reactions in the upper atmosphere and creating the appearance of streamers of reddish or greenish light in the sky, usually near the northern or southern magnetic pole. Other natural lights can indicate danger, like a raging forest fire encroaching on a city, town, or community, or lava spewing from an erupting volcano.\n\nWhatever the source, the ability of humans to monitor nature's light shows at night has practical applications for society. For example, tracking fires during nighttime hours allows for continuous monitoring and enhances our ability to protect humans and other animals, plants, and infrastructure. Combined with other data sources, our ability to observe the light of fires at night allows emergency managers to more efficiently and accurately issue warnings and evacuation orders and allows firefighting efforts to continue through the night. With enough moonlight (e.g., full-Moon phase), it's even possible to track the movement of smoke plumes at night, which can impact air quality, regardless of time of day.\n\nAnother natural source of light at night is emitted from glowing lava flows at the site of active volcanoes. Again, with enough moonlight, these dramatic scenes can be tracked and monitored for both scientific research and public safety.\n\n\n### Figure: The Northern Lights Viewed from Space\n\n**September 17, 2011**\n\nThis photo, taken from the International Space Station on September 17, 2011, shows a spectacular display of the aurora borealis (Northern Lights) as green and reddish light in the night sky above Earth. In the foreground, part of a Soyuz spacecraft is visible, silhouetted against the bright auroral light. The green glow is generated by energetic charged particles from the Sun interacting with Earth's upper atmosphere, exciting oxygen and nitrogen atoms, and producing characteristic colors. The image demonstrates the vividness and grandeur of natural night-time light phenomena as seen from orbit."},{"ref_id":4,"content":"# Volcanoes\n\n## Figure: Satellite Image of Sicily and Mount Etna Lava, March 16, 2017\n\nThe annotated satellite image below shows the island of Sicily and the surrounding region at night, highlighting city lights and volcanic activity.\n\n**Description:**\n\n- **Date of image:** March 16, 2017\n- **Geographical locations labeled:**\n    - Major cities: Palermo (northwest Sicily), Marsala (western Sicily), Catania (eastern Sicily)\n    - Significant feature: Mount Etna, labeled with an adjacent \"hot lava\" region showing the glow from active lava flows\n    - Surrounding water body: Mediterranean Sea\n    - Island: Malta to the south of Sicily\n- **Other details:** \n    - The image is shown at night, with bright spots indicating city lights.\n    - The position of \"hot lava\" near Mount Etna is distinctly visible as a bright spot different from other city lights, indicating volcanic activity.\n    - A scale bar is included showing a reference length of 50 km.\n    - North direction is indicated with an arrow.\n    - Cloud cover is visible in the southwest part of the image, partially obscuring the view near Marsala and Malta.\n\n**Summary of Features Visualized:**\n\n| Feature          | Description |\n|------------------|------------------------------------------------------|\n| Cities           | Bright clusters indicating locations: Palermo, Marsala, Catania |\n| Mount Etna       | Marked on the map, located on the eastern side of Sicily, with visible hot lava activity |\n| Malta            | Clearly visible to the south of Sicily |\n| Water bodies     | Mediterranean Sea labeled                            |\n| Scale & Direction| 50 km scale bar and North indicator                  |\n| Date             | March 16, 2017                                       |\n| Cloud Cover      | Visible in the lower left (southern) part of the image |\n\nThis figure demonstrates the visibility of volcanic activity at Mount Etna from space at night, distinguishing the light from hot lava against the background city lights of Sicily and Malta."},{"ref_id":3,"content":"# Volcanoes\n\n---\n\n### Mount Etna Erupts - Italy\n\nThe highly active Mount Etna in Italy sent red lava rolling down its flank on March 19, 2017. An astronaut onboard the ISS took the photograph below of the volcano and its environs that night. City lights surround the mostly dark volcanic area.\n\n---\n\n#### Figure 1: Location of Mount Etna, Italy\n\nA world map highlighting the location of Mount Etna in southern Italy. The marker indicates its geographic placement on the east coast of Sicily, Italy, in the Mediterranean region, south of mainland Europe and north of northern Africa.\n\n---\n\n#### Figure 2: Nighttime View of Mount Etna's Eruption and Surrounding Cities\n\nThis is a nighttime satellite image taken on March 19, 2017, showing the eruption of Mount Etna (southeastern cone) with visible bright red and orange coloring indicating flowing lava from a lateral vent. The surrounding areas are illuminated by city lights, with the following geographic references labeled:\n\n| Location | Position in Image         | Visible Characteristics |\n|-----------------|--------------------------|--------------------------------------------|\n| Mt. Etna (southeastern cone) | Top center-left | Bright red/orange lava flow                |\n| Lateral vent    | Left of the volcano       | Faint red/orange flow extending outwards   |\n| Resort          | Below the volcano, to the left   | Small cluster of lights                    |\n| Giarre          | Top right                 | Bright cluster of city lights |\n| Acireale        | Center right              | Large, bright area of city lights          |\n| Biancavilla     | Bottom left               | Smaller cluster of city lights             |\n\nAn arrow pointing north is shown on the image for orientation.\n\n---\n\n<!-- Earth at Night Page Footer -->\n<!-- Page Number: 50 -->"},{"ref_id":2,"content":"For the first time in perhaps a decade, Mount Etna experienced a \"flank eruption\"—erupting from its side instead of its summit—on December 24, 2018. The activity was accompanied by 130 earthquakes occurring over three hours that morning. Mount Etna, Europe’s most active volcano, has seen periodic activity on this part of the mountain since 2013. The Operational Land Imager (OLI) on the Landsat 8 satellite acquired the main image of Mount Etna on December 28, 2018.\n\nThe inset image highlights the active vent and thermal infrared signature from lava flows, which can be seen near the newly formed fissure on the southeastern side of the volcano. The inset was created with data from OLI and the Thermal Infrared Sensor (TIRS) on Landsat 8. Ash spewing from the fissure cloaked adjacent villages and delayed aircraft from landing at the nearby Catania airport. Earthquakes occurred in the subsequent days after the initial eruption and displaced hundreds of people from their homes.\n\nFor nighttime images of Mount Etna’s March 2017 eruption, see pages 48–51.\n\n---\n\n### Hazards of Volcanic Ash Plumes and Satellite Observation\n\nWith the help of moonlight, satellite instruments can track volcanic ash plumes, which present significant hazards to airplanes in flight. The volcanic ash—composed of tiny pieces of glass and rock—is abrasive to engine turbine blades, and can melt on the blades and other engine parts, causing damage and even engine stalls. This poses a danger to both the plane’s integrity and passenger safety. Volcanic ash also reduces visibility for pilots and can cause etching of windshields, further reducing pilots’ ability to see. Nightlight images can be combined with thermal images to provide a more complete view of volcanic activity on Earth’s surface.\n\nThe VIIRS Day/Night Band (DNB) on polar-orbiting satellites uses faint light sources such as moonlight, airglow (the atmosphere’s self- illumination through chemical reactions), zodiacal light (sunlight scattered by interplanetary dust), and starlight from the Milky Way. Using these dim light sources, the DNB can detect changes in clouds, snow cover, and sea ice:\n\n#### Table: Light Sources Used by VIIRS DNB\n\n| Light Source         | Description |\n|----------------------|------------------------------------------------------------------------------|\n| Moonlight | Reflected sunlight from the Moon, illuminating Earth's surface at night      |\n| Airglow              | Atmospheric self-illumination from chemical reactions                        |\n| Zodiacal Light       | Sunlight scattered by interplanetary dust                                    |\n| Starlight/Milky Way  | Faint illumination provided by stars in the Milky Way                        |\n\nGeostationary Operational Environmental Satellites (GOES), managed by NOAA, orbit over Earth’s equator and offer uninterrupted observations of North America. High-latitude areas such as Alaska benefit from polar-orbiting satellites like Suomi NPP, which provide overlapping coverage at the poles, enabling more data collection in these regions. During polar darkness (winter months), VIIRS DNB data allow scientists to:\n\n- Observe sea ice formation\n- Monitor snow cover extent at the highest latitudes\n- Detect open water for ship navigation\n\n#### Table: Satellite Coverage Overview\n\n| Satellite Type          | Orbit           | Coverage Area | Special Utility |\n|------------------------|-----------------|----------------------|----------------------------------------------|\n| GOES                   | Geostationary   | Equatorial/North America | Continuous regional monitoring              |\n| Polar-Orbiting (e.g., Suomi NPP) | Polar-orbiting    | Poles/high latitudes      | Overlapping passes; useful during polar night|\n\n---\n\n### Weather Forecasting and Nightlight Data\n\nThe use of nightlight data by weather forecasters is growing as the VIIRS instrument enables observation of clouds at night illuminated by sources such as moonlight and lightning. Scientists use these data to study the nighttime behavior of weather systems, including severe storms, which can develop and strike populous areas at night as well as during the day. Combined with thermal data, visible nightlight data allow the detection of clouds at various heights in the atmosphere, such as dense marine fog. This capability enables weather forecasters to issue marine advisories with higher confidence, leading to greater utility. (See \"Marine Layer Clouds—California\" on page 56.)\n\nIn this section of the book, you will see how nightlight data are used to observe nature’s spectacular light shows across a wide range of sources.\n\n---\n\n#### Notable Data from Mount Etna Flank Eruption (December 2018)\n\n| Event/Observation                  | Details |\n|-------------------------------------|---------------------------------------------------------------------------- |\n| Date of Flank Eruption              | December 24, 2018 |\n| Number of Earthquakes               | 130 earthquakes within 3 hours |\n| Image Acquisition                   | December 28, 2018 by Landsat 8 OLI |\n| Location of Eruption                | Southeastern side of Mount Etna |\n| Thermal Imaging Data                | From OLI and TIRS (Landsat 8), highlighting active vent and lava flows |\n| Impact on Villages/Air Transport    | Ash covered villages; delayed aircraft at Catania airport |\n| Displacement                        | Hundreds of residents displaced |\n| Ongoing Seismic Activity            | Earthquakes continued after initial eruption |\n\n---\n\n<!-- PageFooter=\"Earth at Night\" -->\n<!-- PageNumber=\"30\" -->"},{"ref_id":1,"content":"<!-- PageHeader=\"Volcanoes\" -->\n\n### Nighttime Glow at Mount Etna - Italy\n\nAt about 2:30 a.m. local time on March 16, 2017, the VIIRS DNB on the Suomi NPP satellite captured this nighttime image of lava flowing on Mount Etna in Sicily, Italy. Etna is one of the world's most active volcanoes.\n\n#### Figure: Location of Mount Etna\nA world globe is depicted, with a marker indicating the location of Mount Etna in Sicily, Italy, in southern Europe near the center of the Mediterranean Sea.\n\n<!-- PageFooter=\"Earth at Night\" -->\n<!-- PageNumber=\"48\" -->"},{"ref_id":0,"content":"<!-- PageHeader=\"Volcanoes\" -->\n\n## Volcanoes\n\n### The Infrared Glows of Kilauea's Lava Flows—Hawaii\n\nIn early May 2018, an eruption on Hawaii's Kilauea volcano began to unfold. The eruption took a dangerous turn on May 3, 2018, when new fissures opened in the residential neighborhood of Leilani Estates. During the summer-long eruptive event, other fissures emerged along the East Rift Zone. Lava from vents along the rift zone flowed downslope, reaching the ocean in several areas, and filling in Kapoho Bay.\n\nA time series of Landsat 8 imagery shows the progression of the lava flows from May 16 to August 13. The night view combines thermal, shortwave infrared, and near-infrared wavelengths to tease out the very hot lava (bright white), cooling lava (red), and lava flows obstructed by clouds (purple).\n\n#### Figure: Location of Kilauea Volcano, Hawaii\n\nA globe is shown centered on North America, with a marker placed in the Pacific Ocean indicating the location of Hawaii, to the southwest of the mainland United States.\n\n<!-- PageFooter=\"Earth at Night\" -->\n<!-- PageNumber=\"44\" -->"}]
Activity
[
  {
    "id": 0,
    "type": "ModelQueryPlanning",
    "input_tokens": 2283,
    "output_tokens": 203
  },
  {
    "id": 1,
    "type": "AzureSearchQuery",
    "target_index": "earth_at_night",
    "query": {
      "search": "how to locate lava flows at night"
    },
    "query_time": "2025-05-06T21:12:09.409Z",
    "count": 6,
    "elapsed_ms": 502
  },
  {
    "id": 2,
    "type": "AzureSearchQuery",
    "target_index": "earth_at_night",
    "query": {
      "search": "best practices for observing lava at night"
    },
    "query_time": "2025-05-06T21:12:09.676Z",
    "elapsed_ms": 266
  }
]
Results
[
  {
    "type": "AzureSearchDoc",
    "id": "0",
    "activity_source": 1,
    "doc_key": "earth_at_night_508_page_60_verbalized"
  },
  {
    "type": "AzureSearchDoc",
    "id": "1",
    "activity_source": 1,
    "doc_key": "earth_at_night_508_page_64_verbalized"
  },
  {
    "type": "AzureSearchDoc",
    "id": "2",
    "activity_source": 1,
    "doc_key": "earth_at_night_508_page_46_verbalized"
  },
  {
    "type": "AzureSearchDoc",
    "id": "3",
    "activity_source": 1,
    "doc_key": "earth_at_night_508_page_66_verbalized"
  },
  {
    "type": "AzureSearchDoc",
    "id": "4",
    "activity_source": 1,
    "doc_key": "earth_at_night_508_page_65_verbalized"
  },
  {
    "type": "AzureSearchDoc",
    "id": "5",
    "activity_source": 1,
    "doc_key": "earth_at_night_508_page_44_verbalized"
  }
]
```

## Generate an answer

```Python
response = client.responses.create(
    model=answer_model,
    input=messages
)

wrapped = textwrap.fill(response.output_text, width=100)
print(wrapped)
```

The output should be similar to the following example, which...

```
To find lava at night, you can rely on natural brightness emitted by the hot lava flows themselves. Volcanic eruptions produce infrared glow visible even from space, particularly in active zones like Mount Etna, Italy, or Kilauea, Hawaii. Key methods include:  1. **Thermal Infrared Imaging**: Satellites equipped with thermal sensors, like Landsat 8 or VIIRS on Suomi NPP, can detect heat signatures from lava and provide nighttime observations. Infrared light reveals hot lava flows by highlighting their brightness, even in darkness ([ref_id:2], [ref_id:0]).  2. **Moonlight-Enhanced Visibility**: Satellite instruments utilize moonlight and other weak light sources to distinguish lava flows. For example, images of Mount Etna captured at night use moonlight combined with infrared to reveal active lava zones ([ref_id:1], [ref_id:2]).  3. **Nighttime Monitoring Tools**: Tools like the VIIRS Day/Night Band on satellites are specifically adapted to detect faint sources of nighttime light such as glowing lava, aiding scientists in tracking eruptions and flows ([ref_id:2]).  So, if you want to locate lava at night, monitoring active volcanic regions with satellite data or infrared thermal imaging would be your best approach.
```
