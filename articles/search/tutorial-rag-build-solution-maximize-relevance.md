---
title: 'RAG tutorial: Tune relevance'
titleSuffix: Azure AI Search
description: Learn how to use the relevance tuning capabilities to return high quality results for generative search.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.custom:
  - ignite-2024
ms.topic: tutorial
ms.date: 06/11/2025
---

# Tutorial: Maximize relevance (RAG in Azure AI Search)

In this tutorial, learn how to improve the relevance of search results used in RAG solutions. Relevance tuning can be an important factor in delivering a RAG solution that meets user expectations. In Azure AI Search, relevance tuning includes L2 semantic ranking and scoring profiles. 

To implement these capabilities, you revisit the index schema to add configurations for semantic ranking and scoring profiles. You then rerun the queries using the new constructs.

In this tutorial, you modify the existing search index and queries to use:

> [!div class="checklist"]
> - L2 semantic ranking
> - Scoring profile for document boosting

This tutorial updates the search index created by the [indexing pipeline](tutorial-rag-build-solution-pipeline.md). Updates don't affect the existing content, so no rebuild is necessary and you don't need to rerun the indexer.

> [!NOTE]
> There are more relevance features in preview, including vector query weighting and setting minimum thresholds, but we omit them from this tutorial because they're in preview.

## Prerequisites

- [Visual Studio Code](https://code.visualstudio.com/download) with the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and the [Jupyter package](https://pypi.org/project/jupyter/).

- [Azure AI Search](search-create-service-portal.md), Basic tier or higher for managed identity and semantic ranking.

- [Azure OpenAI](/azure/ai-services/openai/how-to/create-resource), with a deployment of text-embedding-002 and gpt-35-turbo.

## Download the sample

The [sample notebook](https://github.com/Azure-Samples/azure-search-python-samples/blob/main/Tutorial-RAG/Tutorial-rag.ipynb) includes an updated index and query request.

## Run a baseline query for comparison

Let's start with a new query, "Are there any cloud formations specific to oceans and large bodies of water?".

To compare outcomes after adding relevance features, run the query against the existing index schema, before you add semantic ranking or a scoring profile.

For the Azure Government cloud, modify the API endpoint on the token provider to `"https://cognitiveservices.azure.us/.default"`.

```python
from azure.search.documents import SearchClient
from openai import AzureOpenAI

token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
openai_client = AzureOpenAI(
     api_version="2024-06-01",
     azure_endpoint=AZURE_OPENAI_ACCOUNT,
     azure_ad_token_provider=token_provider
 )

deployment_name = "gpt-4o"

search_client = SearchClient(
     endpoint=AZURE_SEARCH_SERVICE,
     index_name=index_name,
     credential=credential
 )

GROUNDED_PROMPT="""
You are an AI assistant that helps users learn from the information found in the source material.
Answer the query using only the sources provided below.
Use bullets if the answer has multiple points.
If the answer is longer than 3 sentences, provide a summary.
Answer ONLY with the facts listed in the list of sources below. Cite your source when you answer the question
If there isn't enough information below, say you don't know.
Do not generate answers that don't use the sources below.
Query: {query}
Sources:\n{sources}
"""

# Focused query on cloud formations and bodies of water
query="Are there any cloud formations specific to oceans and large bodies of water?"
vector_query = VectorizableTextQuery(text=query, k_nearest_neighbors=50, fields="text_vector")

search_results = search_client.search(
    search_text=query,
    vector_queries= [vector_query],
    select=["title", "chunk", "locations"],
    top=5,
)

sources_formatted = "=================\n".join([f'TITLE: {document["title"]}, CONTENT: {document["chunk"]}, LOCATIONS: {document["locations"]}' for document in search_results])

response = openai_client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": GROUNDED_PROMPT.format(query=query, sources=sources_formatted)
        }
    ],
    model=deployment_name
)

print(response.choices[0].message.content)
```

Output from this request might look like the following example.

```
Yes, there are cloud formations specific to oceans and large bodies of water. 
A notable example is "cloud streets," which are parallel rows of clouds that form over 
the Bering Strait in the Arctic Ocean. These cloud streets occur when wind blows from 
a cold surface like sea ice over warmer, moister air near the open ocean, leading to 
the formation of spinning air cylinders. Clouds form along the upward cycle of these cylinders, 
while skies remain clear along the downward cycle (Source: page-21.pdf).
```

## Update the index for semantic ranking and scoring profiles

In a previous tutorial, you [designed an index schema](tutorial-rag-build-solution-index-schema.md) for RAG workloads. We purposely omitted relevance enhancements from that schema so that you could focus on the fundamentals. Deferring relevance to a separate exercise gives you a before-and-after comparison of the quality of search results after the updates are made.

1. Update the import statements to include classes for semantic ranking and scoring profiles.

   ```python
    from azure.identity import DefaultAzureCredential
    from azure.identity import get_bearer_token_provider
    from azure.search.documents.indexes import SearchIndexClient
    from azure.search.documents.indexes.models import (
        SearchField,
        SearchFieldDataType,
        VectorSearch,
        HnswAlgorithmConfiguration,
        VectorSearchProfile,
        AzureOpenAIVectorizer,
        AzureOpenAIVectorizerParameters,
        SearchIndex,
        SemanticConfiguration,
        SemanticPrioritizedFields,
        SemanticField,
        SemanticSearch,
        ScoringProfile,
        TagScoringFunction,
        TagScoringParameters
    )
    ```

1. Add the following semantic configuration to the search index. This example can be found in the update schema step in the notebook.

    ```python
    # New semantic configuration
    semantic_config = SemanticConfiguration(
        name="my-semantic-config",
        prioritized_fields=SemanticPrioritizedFields(
            title_field=SemanticField(field_name="title"),
            keywords_fields=[SemanticField(field_name="locations")],
            content_fields=[SemanticField(field_name="chunk")]
        )
    )
    
    # Create the semantic settings with the configuration
    semantic_search = SemanticSearch(configurations=[semantic_config])
    ```

   A semantic configuration has a name and a prioritized list of fields to help optimize the inputs to semantic ranker. For more information, see [Configure semantic ranking](/azure/search/semantic-how-to-configure).

1. Next, add a scoring profile definition. As with semantic configuration, a scoring profile can be added to an index schema at any time. This example is also in the update schema step in the notebook, following the semantic configuration.

    ```python
    # New scoring profile
    scoring_profiles = [  
        ScoringProfile(  
            name="my-scoring-profile",
            functions=[
                TagScoringFunction(  
                    field_name="locations",  
                    boost=5.0,  
                    parameters=TagScoringParameters(  
                        tags_parameter="tags",  
                    ),  
                ) 
            ]
        )
    ]
    ```

   This profile uses the tag function which boosts the scores of documents where a match was found in the locations field. Recall that the search index has a vector field, and multiple nonvector fields for title, chunks, and locations. The locations field is a string collection, and string collections can be boosted using the tags function in a scoring profile. For more information, see [Add a scoring profile](index-add-scoring-profiles.md) and [Enhancing Search Relevance with Document Boosting (blog post)](https://farzzy.hashnode.dev/enhance-azure-ai-search-document-boosting).

1. Update the index definition on the search service.

   ```python
   # Update the search index with the semantic configuration
    index = SearchIndex(name=index_name, fields=fields, vector_search=vector_search, semantic_search=semantic_search, scoring_profiles=scoring_profiles)  
    result = index_client.create_or_update_index(index)  
    print(f"{result.name} updated")  
    ```

## Update queries for semantic ranking and scoring profiles

In a previous tutorial, you [ran queries](tutorial-rag-build-solution-query.md) that execute on the search engine, passing the response and other information to an LLM for chat completion.

This example modifies the query request to include the semantic configuration and scoring profile.

For the Azure Government cloud, modify the API endpoint on the token provider to `"https://cognitiveservices.azure.us/.default"`.

```python
# Import libraries
from azure.search.documents import SearchClient
from openai import AzureOpenAI

token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
openai_client = AzureOpenAI(
     api_version="2024-06-01",
     azure_endpoint=AZURE_OPENAI_ACCOUNT,
     azure_ad_token_provider=token_provider
 )

deployment_name = "gpt-4o"

search_client = SearchClient(
     endpoint=AZURE_SEARCH_SERVICE,
     index_name=index_name,
     credential=credential
 )

# Prompt is unchanged in this update
GROUNDED_PROMPT="""
You are an AI assistant that helps users learn from the information found in the source material.
Answer the query using only the sources provided below.
Use bullets if the answer has multiple points.
If the answer is longer than 3 sentences, provide a summary.
Answer ONLY with the facts listed in the list of sources below.
If there isn't enough information below, say you don't know.
Do not generate answers that don't use the sources below.
Query: {query}
Sources:\n{sources}
"""

# Queries are unchanged in this update
query="Are there any cloud formations specific to oceans and large bodies of water?"
vector_query = VectorizableTextQuery(text=query, k_nearest_neighbors=50, fields="text_vector")

# Add query_type semantic and semantic_configuration_name
# Add scoring_profile and scoring_parameters
search_results = search_client.search(
    query_type="semantic",
    semantic_configuration_name="my-semantic-config",
    scoring_profile="my-scoring-profile",
    scoring_parameters=["tags-ocean, 'sea surface', seas, surface"],
    search_text=query,
    vector_queries= [vector_query],
    select="title, chunk, locations",
    top=5,
)
sources_formatted = "=================\n".join([f'TITLE: {document["title"]}, CONTENT: {document["chunk"]}, LOCATIONS: {document["locations"]}' for document in search_results])

response = openai_client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": GROUNDED_PROMPT.format(query=query, sources=sources_formatted)
        }
    ],
    model=deployment_name
)

print(response.choices[0].message.content)
```

Output from a semantically ranked and boosted query might look like the following example.

```
Yes, there are specific cloud formations influenced by oceans and large bodies of water:

- **Stratus Clouds Over Icebergs**: Low stratus clouds can frame holes over icebergs, 
such as Iceberg A-56 in the South Atlantic Ocean, likely due to thermal instability caused 
by the iceberg (source: page-39.pdf).

- **Undular Bores**: These are wave structures in the atmosphere created by the collision 
of cool, dry air from a continent with warm, moist air over the ocean, as seen off the 
coast of Mauritania (source: page-23.pdf).

- **Ship Tracks**: These are narrow clouds formed by water vapor condensing around tiny 
particles from ship exhaust. They are observed over the oceans, such as in the Pacific Ocean 
off the coast of California (source: page-31.pdf).

These specific formations are influenced by unique interactions between atmospheric conditions 
and the presence of large water bodies or objects within them.
```

Adding semantic ranking and scoring profiles positively affects the response from the LLM by promoting results that meet scoring criteria and are semantically relevant. 

Now that you have a better understanding of index and query design, let's move on to optimizing for speed and concision. We revisit the schema definition to implement quantization and storage reduction, but the rest of the pipeline and models remain intact.

<!-- ## Update queries for minimum thresholds ** NOT AVAILABLE IN PYTHON SDK

Keyword search only returns results if there's match found in the index, up to a maximum of 50 results by default. In contrast, vector search returns `k`-results every time, even if the matching vectors aren't a close match.

In the vector query portion of the request, add a threshold object and set a minimum value for including vector matches in the results.

Vector scores range from 0.333 to 1.00. For more information, see [Set thresholds to exclude low-scoring results](vector-search-how-to-query.md#set-thresholds-to-exclude-low-scoring-results-preview) and [Scores in a vector search results](vector-search-ranking.md#scores-in-a-vector-search-results).

```python
# Update the vector_query to include a minimum threshold.
query="how much of earth is covered by water"
vector_query = VectorizableTextQuery(text=query, k_nearest_neighbors=1, fields="text_vector", threshold.kind="vectorSImiliarty", threshold.value=0.8, exhaustive=True) -->

<!-- ## Update queries for vector weighting

<!-- Using preview features, you can unpack a hybrid search score to review the individual component scores. Based on that information, you can set minimum thresholds to exclude any match that falls below it.

Semantic ranking and scoring profiles operate on nonvector content, but you can tune the vector portion of a hybrid query to amplify or diminish its importance based on how much value it adds to the results. For example, if you run keyword search and vector search independently and find that one of them is outperforming the other, you can adjust the weight on the vector side to higher or lower. This approach gives you more control over query processing.
 -->

<!-- Key points:

- How to measure relevance (?) to determine if changes are improving results
- Try different algorithms (HNSW vs eKnn)
- Change query structure (hybrid with vector/non over same content (double-down), hybrid over multiple fields)
- semantic ranking
- scoring profiles
- thresholds for minimum score
- set weights
- filters
- analyzers and normalizers
- advanced query formats (regular expressions, fuzzy search) -->

## Next step

> [!div class="nextstepaction"]
> [Minimize vector storage and costs](tutorial-rag-build-solution-minimize-storage.md)
