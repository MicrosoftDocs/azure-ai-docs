---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 11/10/2025
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

+ [Visual Studio Code](https://code.visualstudio.com/download) and the latest version of [Python](https://www.python.org/downloads/).

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
  {
    "type": "searchIndex",
    "id": "3",
    "activity_source": 2,
    "source_data": {
      "id": "earth_at_night_508_page_104_verbalized",
      "page_chunk": "<!-- PageHeader=\"Urban Structure\" -->\n\n### Location of Phoenix, Arizona\n\nThe image depicts a globe highlighting the location of Phoenix, Arizona, in the southwestern United States, marked with a blue pinpoint on the map of North America. Phoenix is situated in the central part of Arizona, which is in the southwestern region of the United States.\n\n---\n\n### Grid of City Blocks-Phoenix, Arizona\n\nLike many large urban areas of the central and western United States, the Phoenix metropolitan area is laid out along a regular grid of city blocks and streets. While visible during the day, this grid is most evident at night, when the pattern of street lighting is clearly visible from the low-Earth-orbit vantage point of the ISS.\n\nThis astronaut photograph, taken on March 16, 2013, includes parts of several cities in the metropolitan area, including Phoenix (image right), Glendale (center), and Peoria (left). While the major street grid is oriented north-south, the northwest-southeast oriented Grand Avenue cuts across the three cities at image center. Grand Avenue is a major transportation corridor through the western metropolitan area; the lighting patterns of large industrial and commercial properties are visible along its length. Other brightly lit properties include large shopping centers, strip malls, and gas stations, which tend to be located at the intersections of north-south and east-west trending streets.\n\nThe urban grid encourages growth outwards along a city's borders by providing optimal access to new real estate. Fueled by the adoption of widespread personal automobile use during the twentieth century, the Phoenix metropolitan area today includes 25 other municipalities (many of them largely suburban and residential) linked by a network of surface streets and freeways.\n\nWhile much of the land area highlighted in this image is urbanized, there are several noticeably dark areas. The Phoenix Mountains are largely public parks and recreational land. To the west, agricultural fields provide a sharp contrast to the lit streets of residential developments. The Salt River channel appears as a dark ribbon within the urban grid.\n\n\n<!-- PageFooter=\"Earth at Night\" -->\n<!-- PageNumber=\"88\" -->",
      "page_number": 104
    },
    "reranker_score": 2.6451337,
    "doc_key": "earth_at_night_508_page_104_verbalized"
  },
  {
    "type": "searchIndex",
    "id": "1",
    "activity_source": 1,
    "source_data": {
      "id": "earth_at_night_508_page_174_verbalized",
      "page_chunk": "<!-- PageHeader=\"Holiday Lights\" -->\n\n## Holiday Lights\n\n### Bursting with Holiday Energy-United States\n\nNASA researchers found that nighttime lights in the United States shine 20 to 50 percent brighter in December due to holiday light displays and other activities during Christmas and New Year's when compared to light output during the rest of the year.\n\nThe next five maps (see also pages 161-163), created using data from the VIIRS DNB on the Suomi NPP satellite, show changes in lighting intensity and location around many major cities, comparing the nighttime light signals from December 2012 and beyond.\n\n---\n\n#### Figure 1. Location Overview\n\nA map of the western hemisphere with a marker indicating the mid-Atlantic region of the eastern United States, where the study of holiday lighting intensity was focused.\n\n---\n\n#### Figure 2. Holiday Lighting Intensity: Mid-Atlantic United States (2012\u20132014)\n\nA map showing Maryland, New Jersey, Delaware, Virginia, West Virginia, Ohio, Kentucky, Tennessee, North Carolina, South Carolina, and surrounding areas. Major cities labeled include Washington, D.C., Richmond, Norfolk, and Raleigh.\n\nThe map uses colors to indicate changes in holiday nighttime lighting intensity between 2012 and 2014:\n\n- **Green/bright areas**: More holiday lighting (areas shining 20\u201350% brighter in December).\n- **Yellow areas**: No change in lighting.\n- **Dim/grey areas**: Less holiday lighting.\n\nKey observations from the map:\n\n- The Washington, D.C. metropolitan area shows significant increases in lighting during the holidays, extending into Maryland and Virginia.\n- Urban centers such as Richmond (Virginia), Norfolk (Virginia), Raleigh (North Carolina), and clusters in Tennessee and South Carolina also experience notable increases in light intensity during December.\n- Rural areas and the interiors of West Virginia, Kentucky, and North Carolina show little change or less holiday lighting, corresponding to population density and urbanization.\n\n**Legend:**\n\n| Holiday Lighting Change | Color on Map   |\n|------------------------|---------------|\n| More                   | Green/bright  |\n| No Change              | Yellow        |\n| Less         
          | Dim/grey      |\n\n_The scale bar indicates a distance of 100 km for reference._\n\n---\n\n<!-- PageFooter=\"158 Earth at Night\" -->",
      "page_number": 174
    },
    "reranker_score": 2.476761,
    "doc_key": "earth_at_night_508_page_174_verbalized"
  },
  {
    "type": "searchIndex",
    "id": "2",
    "activity_source": 3,
    "source_data": {
      "id": "earth_at_night_508_page_124_verbalized",
      "page_chunk": "# Urban Development\n\n## Figure: Location Highlight on Globe\n\nThis figure depicts a globe focused on North America, with a marker pinpointing the central region of the United States. The highlighted location represents the geographical focus of the text discussion on US urban development and transportation networks.\n\n---\n\n## Urban Development\n\n### Lighting Paths\u2014Across the United States\n\nThe United States has more miles of roads than any other nation in the world\u20144.1 million miles (6.6 million kilometers) to be precise, which is roughly 40 percent more than second-ranked India. About 47,000 miles (75,639 kilometers) of those roads are part of the Interstate Highway System, established by President Dwight Eisenhower in the 1950s. The country/region also has 127,000 miles (204,000 kilometers) of railroad tracks and about 25,000 miles (40,000 kilometers) of navigable rivers and canals (not including the Great Lakes). The imprint of that transportation web becomes easy to see at night.\n\nThe VIIRS DNB on the Suomi NPP satellite acquired this nighttime view (top image, right) of the continental United States on October 1, 2013. The roadway map (bottom image, right) traces the path of the major interstate highways, railroads, and rivers of the United States. Comparing the two images, you quickly see how the cities and settlements align with the transportation corridors. In the early days of the republic, post roads and toll roads for horse-drawn carts and carriages were built to connect eastern cities like Boston, New York, Baltimore, and Philadelphia, though relatively few travelers made the long, unlit journeys. Railroads became the dominant transportation method for people and cargo in the middle of the nineteenth century, establishing longer links across the Nation and waypoints across the Midwest, the Great Plains, and the Rockies. Had nighttime satellite images existed in that era, they probably would show only dim pearls of light around major cities in the east and scattered across the country/region; the strands of steel tracks and cobbled roads that connected them would be invisible from space.\n\nEventually, cars and trucks became the dominant form of transportation in the United States. Drivers then needed roads and lighting to keep them safe on those roads. As the Nation grew in the twentieth century, the development of new cities and suburbs often conformed to the path of the interstate highways, adding light along the paths between the cities.\n\nOver the years, the length of navigable rivers has been a constant, as is their relative lack of light. Even today the only light seems to be the occasional port cities along riverbanks and the light of ships themselves.\n\n---\n\n**Table: Summary of U.S. Transportation Infrastructure**\n\n| Infrastructure Type     | Total Mileage (mi) | Total Mileage (km) |\n|------------------------|--------------------|--------------------|\n| Roads (All)            | 4,100,000          | 6,600,000          |\n| Interstate Highways    | 47,000             | 75,639             |\n| Railroads              | 127,000            | 204,000            |\n| Navigable Rivers/Canals| 25,000             | 40,000             |\n\n---\n\n<!-- PageFooter=\"108 Earth at Night\" -->",
      "page_number": 124
    },
    "reranker_score": 2.466304,
    "doc_key": "earth_at_night_508_page_124_verbalized"
  },
  {
    "type": "searchIndex",
    "id": "4",
    "activity_source": 1,
    "source_data": {
      "id": "earth_at_night_508_page_176_verbalized",
      "page_chunk": "# Holiday Lights\n\n## Figure 1: Location Marker on Globe\n\n**Description:**  \nA world map focused on the Western Hemisphere, with a marker placed in the eastern United States. This image serves to indicate the geographic focus of the following data and discussion about holiday lighting patterns, particularly those observed in the United States.\n\n---\n\nHoliday lights increase most dramatically in the suburbs and outskirts of major cities, where there is more yard space and a prevalence of single-family homes. Central urban areas do not see as large an increase in lighting, but they still experience a brightening of 20 to 30 percent during the holidays. This pattern holds true across the U.S., which remains ethnically and religiously diverse but participates in a nationally shared tradition of increased holiday lighting during holiday seasons.\n\nBeyond the cultural implications, this trend has significant consequences for energy consumption. The availability of a daily, global dynamic dataset of nighttime lights offers new insights into the broad societal forces influencing energy decisions. As noted by the Intergovernmental Panel on Climate Change, improvements in energy efficiency and conservation are essential to reducing greenhouse gas emissions. Examining daily nightlight data provides a valuable perspective on urban and suburban life, helping to reveal the underlying patterns and drivers of energy use.\n\n*(Images continue on pages 161-163)*\n\n---\n\n*Page 160 Earth at Night*",
      "page_number": 176
    },
    "reranker_score": 2.3416197,
    "doc_key": "earth_at_night_508_page_176_verbalized"
  },
  {
    "type": "searchIndex",
    "id": "6",
    "activity_source": 1,
    "source_data": {
      "id": "earth_at_night_508_page_175_verbalized",
      "page_chunk": "# Holiday Lights\n\nFrom 2013 to the average light output for the rest of 2012 to 2014, the change in light usage is subtle on any given night. However, when averaged over days and weeks, the pattern becomes more perceptible. Areas where light usage increased in December are marked in green, areas with little change are marked in yellow, and areas where less light was used are marked in red.\n\nThe light output from 70 U.S. cities was examined as a first step toward determining patterns in urban energy use. Researchers found that light intensity increased by 30 to 50 percent in December in many areas, which may be related to holiday lighting.\n\n---\n\n## Figure 1: Location Reference\n\nA globe highlights the southeastern region of the United States, pinpointing the area of interest for the study of holiday light usage, focusing on states like Tennessee, North Carolina, South Carolina, Georgia, and Alabama.\n\n---\n\n## Figure 2: Holiday Lighting Patterns in the Southeastern United States (2012\u20132014)\n\nThis map highlights several cities in the southeastern United States, including Nashville, Charlotte, Columbia, Birmingham, and Atlanta. The states of Tennessee, North Carolina, South Carolina, Alabama, and Georgia are outlined, along with the Atlantic Ocean to the east.\n\n### Key Observations:\n- The most significant concentrations of nighttime lighting are seen in major metropolitan areas, with Atlanta having the largest and most intense area of light.\n- Other notable clusters of increased light output are visible in Nashville, Charlotte, Birmingham, and Columbia.\n- The map reflects changes in light usage during December of 2012\u20132014, with \u201cmore\u201d lighting (green shading) concentrated around urban areas, indicating an increase due to holiday lighting displays.\n\n**Map Details:**\n- Time frame: 2012\u20132014\n- Locations marked: Nashville (Tennessee), Charlotte (North Carolina), Columbia (South Carolina), Birmingham (Alabama), Atlanta (Georgia)\n- Scale: 100 km bar provided\n- North directional arrow included\n\n---\n\n### Legend:\n- **Green Shading**: Areas where light usage increased in December (likely due to holiday lights)\n- **Yellow Shading**: Areas with little change in light usage\n- **Red Shading**: Areas where less light was used\n\n---\n\n#### Page Footer: \u201cno change\u201d\n#### Page Number: 159",
      "page_number": 175
    },
    "reranker_score": 2.3052866,
    "doc_key": "earth_at_night_508_page_175_verbalized"
  },
  {
    "type": "searchIndex",
    "id": "9",
    "activity_source": 1,
    "source_data": {
      "id": "earth_at_night_508_page_177_verbalized",
      "page_chunk": "# Holiday Lights\n\n## Holiday Lighting in Florida (2012\u20132014)\n\nThis figure presents a nighttime satellite map of Florida, highlighting changes in holiday lighting between 2012 and 2014. The map covers major urban areas including Jacksonville, Orlando, Tampa Bay, and Miami, with the Gulf of Mexico to the west.\n\nKey observations from the figure:\n- The map displays areas of increased, decreased, or unchanged outdoor lighting intensity during the holiday season.\n- Major metropolitan regions such as Miami, Tampa Bay, Orlando, and Jacksonville show noticeable concentrations of holiday lighting, with many surrounding areas experiencing changes in brightness compared to the non-holiday period.\n- Color coding (not described in the image but referenced):  \n  - **Less**: Areas where holiday lighting decreased  \n  - **No change**: Areas where lighting remained stable  \n  - **More**: Areas where holiday lighting increased\n\n**Legend:**\n- The figure includes a scale bar indicating a span of 100 km for distance estimation.\n- The map is oriented with north at the top.\n\n**Geographic Labels:**\n- Jacksonville (northeast Florida)\n- Orlando (central Florida)\n- Tampa Bay (west-central Florida)\n- Miami (southeast Florida)\n- The Gulf of Mexico (to the west of the peninsula)\n\n**Takeaway:**\nThe map visualizes spatial patterns in holiday lighting, indicating that urban and suburban areas in Florida experience substantial increases in nighttime brightness during the holiday period, particularly in and around major cities.\n\n<!-- PageNumber=\"161\" -->",
      "page_number": 177
    },
    "reranker_score": 2.2241132,
    "doc_key": "earth_at_night_508_page_177_verbalized"
  },
  {
    "type": "searchIndex",
    "id": "5",
    "activity_source": 3,
    "source_data": {
      "id": "earth_at_night_508_page_12_verbalized",
      "page_chunk": "## Preface\n\nTo keen observers, the nocturnal Earth is not pitch black, featureless, or static. The stars and the Moon provide illumination that differs from, and complements, daylight. Natural Earth processes such as volcanic eruptions, auroras, lightning, and meteors entering the atmosphere generate localized visible light on timescales ranging from subsecond (lightning), to days, weeks (forest fires), and months (volcanic eruptions).\n\nMost interesting and unique (as far as we know) to Earth, is the nighttime visible illumination emitted from our planet that is associated with human activities. Whether purposefully designed to banish darkness (such as lighting for safety, industrial activities, commerce, and transportation) or a secondary result of (such as gas flares associated with mining and hydrocarbon extraction activities, or nocturnal commercial fishing), anthropogenic sources of nighttime light are often broadly distributed in space and sustained in time\u2014over years and even decades. Because these light sources are inextricably tied to human activities and societies, extensive and long-term measurement and monitoring of Earth's anthropogenic nocturnal lights can provide valuable insights into the spatial distribution of our species and the ways in which society is changing\u2014and is changed by\u2014the environment on a wide range of time scales.\n\nOver the past four decades, sensitive imaging instruments have been operated on low-Earth-orbiting satellites to measure natural and human-caused visible nocturnal illumination, both reflected and Earth-generated. The satellite sensors provide unique imagery: global coverage yet with high spatial resolution, and frequent measurements over long periods of time.\n\nThe combined, multisatellite global nocturnal illumination dataset contains a treasure trove of unique information about our planet and our species\u2014and the",
      "page_number": 12
    },
    "reranker_score": 2.128052,
    "doc_key": "earth_at_night_508_page_12_verbalized"
  },
  {
    "type": "searchIndex",
    "id": "7",
    "activity_source": 3,
    "source_data": {
      "id": "earth_at_night_508_page_125_verbalized",
      "page_chunk": "# Urban Development\n\n**Date:** October 1, 2013\n\n---\n\n## Figure: Urban Development and Infrastructure in the United States\n\nThis figure comprises two maps of the continental United States, highlighting the patterns of urban development and infrastructure.\n\n### Top Panel: Nighttime Lights Map (October 1, 2013)\n\nThis map displays the United States as seen from space at night on October 1, 2013. Major observations include:\n\n- A dense concentration of bright spots representing urban and suburban areas with prominent lighting, especially along the east coast, the Midwest (notably around Chicago), Texas, and California.\n- The west and central parts of the country/region, such as the Rocky Mountains and deserts, appear much darker, indicating sparse population and fewer urban centers.\n- The boundaries of the United States are outlined for reference.\n- Major urban corridors are clearly visible, including the heavily lit regions running from Boston through New York City, Philadelphia, Baltimore, D.C., Atlanta, and further south, as well as the line of cities from Los Angeles through southern California.\n\n### Bottom Panel: Major Transport and River Networks\n\nThis map outlines the primary interstate highways, railroad lines, and major river systems in the continental United States, using different colors to distinguish among them:\n\n| Feature    | Color       | Description                                                                       |\n|------------|-------------|-----------------------------------------------------------------------------------|\n| Interstate | Red         | Key high-speed roadways, forming a vast national network and connecting cities     |\n| Railroad   | Green       | Major rail lines paralleling some highway routes, providing freight and passenger service |\n| River      | Blue        | Major river systems used historically for transport, industry, and urban siting    |\n\n- The locations of interstate highways closely follow the distribution of nighttime lights, as seen in the top panel.\n- Railroad networks are especially dense in the Midwest and northeast, regions with both high population density and industrial activity.\n- Major rivers, such as the Mississippi, Missouri, and Ohio, are marked in blue, reflecting their importance for historical urban development.\n\n**Scale:** Both maps include a scale bar representing 500 km and a North arrow for orientation.\n\n---\n\n**Summary:**  \nThe figure visually demonstrates the relationship between urban development (as observed through nighttime satellite imagery) and the underlying networks of interstates, railroads, and rivers that have historically influenced the growth and connectivity of American cities. Most urbanized and densely lit areas correspond to nodes and crossroads within this transportation and river network.\n\n---\n\n**Page 109**",
      "page_number": 125
    },
    "reranker_score": 2.108246,
    "doc_key": "earth_at_night_508_page_125_verbalized"
  },
  {
    "type": "searchIndex",
    "id": "8",
    "activity_source": 2,
    "source_data": {
      "id": "earth_at_night_508_page_179_verbalized",
      "page_chunk": "# Holiday Lights\n\n## Figure 1: Geographic Context of Holiday Lighting Study\n\nThis figure shows a map of the globe focused on North America, with a blue marker pointing to the region in the southwestern United States. This highlighted area includes parts of California, Nevada, and Arizona, encompassing the cities of Los Angeles, San Diego, Las Vegas, and Phoenix. This is the region of the study of holiday lighting.\n\n---\n\n## Figure 2: Changes in Holiday Lighting (2012\u20132014)\n\nThis figure is a satellite map of the southwestern United States and northwestern Mexico, annotated with state and city names:\n\n- **California** (including Los Angeles and San Diego)\n- **Nevada** (including Las Vegas)\n- **Arizona** (including Phoenix)\n- **Mexico** (including Tijuana)\n\nThe map shows holiday lighting patterns, using color to indicate change in light intensity during the holiday period (presumably Christmas season) between 2012 and 2014.\n\n### Map Legend\n\n| Color      | Meaning                     |\n|------------|-----------------------------|\n| Greenish   | More holiday lighting       |\n| Yellow     | No change in lighting       |\n| Red        | Less holiday lighting       |\n\n### Observations\n\n- Major urban areas such as Los Angeles, San Diego, Las Vegas, and Phoenix show increased lighting during the holiday period (marked primarily in green).\n- Some areas show no significant change, especially in less densely populated zones.\n- A few small areas may show a decrease in holiday lighting (if red is present).\n\n- The scale of the map includes a reference bar showing 50 km for distance.\n\n---\n\n### Holiday Lighting Change Key\n\n- **Less** (Red)\n- **No change** (Yellow)\n- **More** (Green)\n\n---\n\n<!-- PageNumber=\"163\" -->",
      "page_number": 179
    },
    "reranker_score": 2.1016884,
    "doc_key": "earth_at_night_508_page_179_verbalized"
  }
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

In Azure AI Search, an index is a structured collection of data. The following code defines an index named `earth-at-night`, which you previously specified using the `index_name` variable.

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

### Create a knowledge source

A knowledge source is a reusable reference to source data. The following code defines a knowledge source named `earth-knowledge-source` that targets the `earth-at-night` index.

`source_data_fields` specifies which index fields are accessible for retrieval and citations. Our example includes only human-readable fields to avoid lengthy, uninterpretable embeddings in responses.

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

### Create a knowledge base

To target `earth-knowledge-source` and your `gpt-5-mini` deployment at query time, you need a knowledge base. The following code defines a knowledge base named `earth-knowledge-base`, which you previously specified using the `knowledge_base_name` variable.

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

When you work in your own subscription, it's a good idea to finish a project by determining whether you still need the resources you created. Resources that are left running can cost you money.

In the [Azure portal](https://portal.azure.com/), you can manage your Azure AI Search and Microsoft Foundry resources by selecting **All resources** or **Resource groups** from the left pane.

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
