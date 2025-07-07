---
title: 'RAG tutorial: Build an indexing pipeline'
titleSuffix: Azure AI Search
description: Create an indexer-driven pipeline that loads, chunks, embeds, and ingests content for RAG solutions on Azure AI Search.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.custom:
  - ignite-2024
ms.topic: tutorial
ms.date: 06/11/2025
---

# Tutorial: Build an indexing pipeline for RAG on Azure AI Search

Learn how to build an automated indexing pipeline for a RAG solution on Azure AI Search. Indexing automation is through an indexer that drives indexing and skillset execution, providing [integrated data chunking and vectorization](vector-search-integrated-vectorization.md) on a one-time or recurring basis for incremental updates.

In this tutorial, you:

> [!div class="checklist"]
> - Provide the index schema from the previous tutorial
> - Create a data source connection
> - Create an indexer
> - Create a skillset that chunks, vectorizes, and recognizes entities
> - Run the indexer and check results

If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/?WT.mc_id=A261C142F) before you begin.

> [!TIP]
> You can use the [Import and vectorize data wizard](search-import-data-portal.md) to create your pipeline. Try some quickstarts [Image search](search-get-started-portal-image-search.md) or [Vector search](search-get-started-portal-import-vectors.md), to learn more about the pipeline and its moving parts.

## Prerequisites

- [Visual Studio Code](https://code.visualstudio.com/download) with the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and the [Jupyter package](https://pypi.org/project/jupyter/). For more information, see [Python in Visual Studio Code](https://code.visualstudio.com/docs/languages/python).

- [Azure Storage](/azure/storage/common/storage-account-create) general purpose account. This exercise uploads PDF files into blob storage for automated indexing.

- [Azure AI Search](search-create-service-portal.md), Basic tier or above for managed identity and semantic ranking. Choose a region that's shared with Azure AI services.

- [Azure OpenAI](/azure/ai-services/openai/how-to/create-resource), with a deployment of text-embedding-3-large. For more information about embedding models used in RAG solutions, see [Choose embedding models for RAG in Azure AI Search](tutorial-rag-build-solution-models.md).

- [Azure AI services multi-service account](/azure/ai-services/multi-service-resource#azure-ai-services-resource-for-azure-ai-search-skills), in the same region as Azure AI Search. This resource is used for the Entity Recognition skill that detects locations in your content.

## Download the sample

[Download a Jupyter notebook](https://github.com/Azure-Samples/azure-search-python-samples/blob/main/Tutorial-RAG/Tutorial-rag.ipynb) from GitHub to send the requests to Azure AI Search. For more information, see [Downloading files from GitHub](https://docs.github.com/get-started/start-your-journey/downloading-files-from-github).

## Provide the index schema

Open or create a Jupyter notebook (`.ipynb`) in Visual Studio Code to contain the scripts that comprise the pipeline. Initial steps install packages and collect variables for the connections. After you complete the setup steps, you're ready to begin with the components of the indexing pipeline. 

Let's start with the index schema from the [previous tutorial](tutorial-rag-build-solution-index-schema.md). It's organized around vectorized and nonvectorized chunks. It includes a `locations` field that stores AI-generated content created by the skillset.

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
    SearchIndex
)

credential = DefaultAzureCredential()

# Create a search index  
index_name = "py-rag-tutorial-idx"
index_client = SearchIndexClient(endpoint=AZURE_SEARCH_SERVICE, credential=credential)  
fields = [
    SearchField(name="parent_id", type=SearchFieldDataType.String),  
    SearchField(name="title", type=SearchFieldDataType.String),
    SearchField(name="locations", type=SearchFieldDataType.Collection(SearchFieldDataType.String), filterable=True),
    SearchField(name="chunk_id", type=SearchFieldDataType.String, key=True, sortable=True, filterable=True, facetable=True, analyzer_name="keyword"),  
    SearchField(name="chunk", type=SearchFieldDataType.String, sortable=False, filterable=False, facetable=False),  
    SearchField(name="text_vector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single), vector_search_dimensions=1024, vector_search_profile_name="myHnswProfile")
    ]  
  
# Configure the vector search configuration  
vector_search = VectorSearch(  
    algorithms=[  
        HnswAlgorithmConfiguration(name="myHnsw"),
    ],  
    profiles=[  
        VectorSearchProfile(  
            name="myHnswProfile",  
            algorithm_configuration_name="myHnsw",  
            vectorizer_name="myOpenAI",  
        )
    ],  
    vectorizers=[  
        AzureOpenAIVectorizer(  
            vectorizer_name="myOpenAI",  
            kind="azureOpenAI",  
            parameters=AzureOpenAIVectorizerParameters(  
                resource_url=AZURE_OPENAI_ACCOUNT,  
                deployment_name="text-embedding-3-large",
                model_name="text-embedding-3-large"
            ),
        ),  
    ], 
)  
  
# Create the search index
index = SearchIndex(name=index_name, fields=fields, vector_search=vector_search)  
result = index_client.create_or_update_index(index)  
print(f"{result.name} created")  
```

## Create a data source connection

In this step, set up the sample data and a connection from Azure AI Search to Azure Blob Storage. The indexer retrieves PDFs from a container. You create the container and upload files in this step.

The original ebook is large, over 100 pages and 35 MB in size. We broke it up into smaller PDFs, one per page of text, to stay under the [document limit for indexers](search-limits-quotas-capacity.md#indexer-limits) of 16 MB per API call and also the [AI enrichment data limits](search-limits-quotas-capacity.md#data-limits-ai-enrichment). For simplicity, we omit image vectorization for this exercise.

1. Sign in to the [Azure portal](https://portal.azure.com) and find your Azure Storage account.

1. Create a container and upload the PDFs from [earth_book_2019_text_pages](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/nasa-e-book/earth_book_2019_text_pages).

1. Make sure your [Azure AI Search managed identity](search-howto-managed-identities-data-sources.md) has a [**Storage Blob Data Reader**](/azure/role-based-access-control/role-assignments-portal) role assignment on Azure Storage.

1. Next, in Visual Studio Code, define an indexer data source that provides connection information during indexing.

    ```python
    from azure.search.documents.indexes import SearchIndexerClient
    from azure.search.documents.indexes.models import (
        SearchIndexerDataContainer,
        SearchIndexerDataSourceConnection
    )
    
    # Create a data source 
    indexer_client = SearchIndexerClient(endpoint=AZURE_SEARCH_SERVICE, credential=credential)
    container = SearchIndexerDataContainer(name="nasa-ebooks-pdfs-all")
    data_source_connection = SearchIndexerDataSourceConnection(
        name="py-rag-tutorial-ds",
        type="azureblob",
        connection_string=AZURE_STORAGE_CONNECTION,
        container=container
    )
    data_source = indexer_client.create_or_update_data_source_connection(data_source_connection)
    
    print(f"Data source '{data_source.name}' created or updated")
    ```

If you set up a [managed identity for an Azure AI Search connection to Azure Storage](search-howto-managed-identities-storage.md), the data source connection string includes a `ResourceId=` suffix. It should look similar to the following example: `"ResourceId=/subscriptions/FAKE-SUBSCRIPTION-ID/resourceGroups/FAKE-RESOURCE-GROUP/providers/Microsoft.Storage/storageAccounts/FAKE-ACCOUNT;"`

## Create a skillset

Skills are the basis for integrated data chunking and vectorization. At a minimum, you want a Text Split skill to chunk your content, and an embedding skill that create vector representations of your chunked content.

In this skillset, an extra skill is used to create structured data in the index. The [Entity Recognition skill](cognitive-search-skill-entity-recognition-v3.md) is used to identify locations, which can range from proper names to generic references, such as "ocean" or "mountain". Having structured data gives you more options for creating interesting queries and boosting relevance.

The AZURE_AI_MULTISERVICE_KEY is needed even if you're using role-based access control. Azure AI Search uses the key for billing purposes and it's required unless your workloads stay under the free limit. You can also set up a keyless connection if you're using the most recent preview API or beta packages. For more information, see [Attach an Azure AI services multi-service resource to a skillset](cognitive-search-attach-cognitive-services.md).

```python
from azure.search.documents.indexes.models import (
    SplitSkill,
    InputFieldMappingEntry,
    OutputFieldMappingEntry,
    AzureOpenAIEmbeddingSkill,
    EntityRecognitionSkill,
    SearchIndexerIndexProjection,
    SearchIndexerIndexProjectionSelector,
    SearchIndexerIndexProjectionsParameters,
    IndexProjectionMode,
    SearchIndexerSkillset,
    CognitiveServicesAccountKey
)

# Create a skillset  
skillset_name = "py-rag-tutorial-ss"

split_skill = SplitSkill(  
    description="Split skill to chunk documents",  
    text_split_mode="pages",  
    context="/document",  
    maximum_page_length=2000,  
    page_overlap_length=500,  
    inputs=[  
        InputFieldMappingEntry(name="text", source="/document/content"),  
    ],  
    outputs=[  
        OutputFieldMappingEntry(name="textItems", target_name="pages")  
    ],  
)  
  
embedding_skill = AzureOpenAIEmbeddingSkill(  
    description="Skill to generate embeddings via Azure OpenAI",  
    context="/document/pages/*",  
    resource_url=AZURE_OPENAI_ACCOUNT,  
    deployment_name="text-embedding-3-large",  
    model_name="text-embedding-3-large",
    dimensions=1024,
    inputs=[  
        InputFieldMappingEntry(name="text", source="/document/pages/*"),  
    ],  
    outputs=[  
        OutputFieldMappingEntry(name="embedding", target_name="text_vector")  
    ],  
)

entity_skill = EntityRecognitionSkill(
    description="Skill to recognize entities in text",
    context="/document/pages/*",
    categories=["Location"],
    default_language_code="en",
    inputs=[
        InputFieldMappingEntry(name="text", source="/document/pages/*")
    ],
    outputs=[
        OutputFieldMappingEntry(name="locations", target_name="locations")
    ]
)
  
index_projections = SearchIndexerIndexProjection(  
    selectors=[  
        SearchIndexerIndexProjectionSelector(  
            target_index_name=index_name,  
            parent_key_field_name="parent_id",  
            source_context="/document/pages/*",  
            mappings=[  
                InputFieldMappingEntry(name="chunk", source="/document/pages/*"),  
                InputFieldMappingEntry(name="text_vector", source="/document/pages/*/text_vector"),
                InputFieldMappingEntry(name="locations", source="/document/pages/*/locations"),  
                InputFieldMappingEntry(name="title", source="/document/metadata_storage_name"),  
            ],  
        ),  
    ],  
    parameters=SearchIndexerIndexProjectionsParameters(  
        projection_mode=IndexProjectionMode.SKIP_INDEXING_PARENT_DOCUMENTS  
    ),  
) 

cognitive_services_account = CognitiveServicesAccountKey(key=AZURE_AI_MULTISERVICE_KEY)

skills = [split_skill, embedding_skill, entity_skill]

skillset = SearchIndexerSkillset(  
    name=skillset_name,  
    description="Skillset to chunk documents and generating embeddings",  
    skills=skills,  
    index_projection=index_projections,
    cognitive_services_account=cognitive_services_account
)
  
client = SearchIndexerClient(endpoint=AZURE_SEARCH_SERVICE, credential=credential)  
client.create_or_update_skillset(skillset)  
print(f"{skillset.name} created")
```

## Create and run the indexer

Indexers are the component that sets all of the processes in motion. You can create an indexer in a disabled state, but the default is to run it immediately. In this tutorial, create and run the indexer to retrieve the data from Blob storage, execute the skills, including chunking and vectorization, and load the index.

The indexer takes several minutes to run. When it's done, you can move on to the final step: querying your index.

```python
from azure.search.documents.indexes.models import (
    SearchIndexer,
    FieldMapping
)

# Create an indexer  
indexer_name = "py-rag-tutorial-idxr" 

indexer_parameters = None

indexer = SearchIndexer(  
    name=indexer_name,  
    description="Indexer to index documents and generate embeddings",  
    skillset_name=skillset_name,  
    target_index_name=index_name,  
    data_source_name=data_source.name,
    # Map the metadata_storage_name field to the title field in the index to display the PDF title in the search results  
    field_mappings=[FieldMapping(source_field_name="metadata_storage_name", target_field_name="title")],
    parameters=indexer_parameters
)  

# Create and run the indexer  
indexer_client = SearchIndexerClient(endpoint=AZURE_SEARCH_SERVICE, credential=credential)  
indexer_result = indexer_client.create_or_update_indexer(indexer)  

print(f' {indexer_name} is created and running. Give the indexer a few minutes before running a query.')    
```

## Run a query to check results

Send a query to confirm your index is operational. This request converts the text string "`what's NASA's website?`" into a vector for a vector search. Results consist of the fields in the select statement, some of which are printed as output.

There's no chat or generative AI at this point. The results are verbatim content from your search index.

```python
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizableTextQuery

# Vector Search using text-to-vector conversion of the querystring
query = "what's NASA's website?"  

search_client = SearchClient(endpoint=AZURE_SEARCH_SERVICE, credential=credential, index_name=index_name)
vector_query = VectorizableTextQuery(text=query, k_nearest_neighbors=50, fields="text_vector")
  
results = search_client.search(  
    search_text=query,  
    vector_queries= [vector_query],
    select=["chunk"],
    top=1
)  
  
for result in results:  
    print(f"Score: {result['@search.score']}")
    print(f"Chunk: {result['chunk']}")
```

This query returns a single match (`top=1`) consisting of the one chunk determined by the search engine to be the most relevant. Results from the query should look similar to the following example:

```
Score: 0.01666666753590107
Chunk: national Aeronautics and Space Administration

earth Science

NASA Headquarters 

300 E Street SW 

Washington, DC 20546

www.nasa.gov

np-2018-05-2546-hQ
```

Try a few more queries to get a sense of what the search engine returns directly so that you can compare it with an LLM-enabled response. Rerun the previous script with this query: `"patagonia geography"` and set `top` to 3 to return more than one response.

Results from this second query should look similar to the following results, which are lightly edited for concision. The output is copied from the notebook, which truncates the response to what you see in this example. You can expand the cell output to review the complete answer.

```
Score: 0.03306011110544205
Chunk: 

Swirling Bloom off Patagonia
Argentina

Interesting art often springs out of the convergence of different ideas and influences. 
And so it is with nature. 

Off the coast of Argentina, two strong ocean currents converge and often stir up a colorful 
brew, as shown in this Aqua image from 

December 2010. 

This milky green and blue bloom formed on the continental shelf off of Patagonia, where warmer, 
saltier waters from the subtropics 

meet colder, fresher waters flowing from the south. Where these currents collide, turbulent 
eddies and swirls form, pulling nutrients 

up from the deep ocean. The nearby Rio de la Plata also deposits nitrogen- and iron-laden 
sediment into the sea. Add in some 
...

while others terminate in water. The San Rafael and San Quintín glaciers (shown at the right) 
are the icefield’s largest. Both have 

been receding rapidly in the past 30 years.
```

With this example, it's easier to spot how chunks are returned verbatim, and how keyword and similarity search identify top matches. This specific chunk definitely has information about Patagonia and geography, but it's not exactly relevant to the query. Semantic ranker would promote more relevant chunks for a better answer, but as a next step, let's see how to connect Azure AI Search to an LLM for conversational search.

<!-- Objective:

- Create objects and run the indexer to produce an operational search index with chunked and vectorized content.

Key points:

- Dependency on a supported data source. Use Azure blob storage for this tutorial.
- Indexer pulls from the data source, pushes to the index.
- Large PDF files can't be chunked. Indexer shows success, but doesn't even attempt to chunk/ingest the docs. Individual files have to be less than 16 MB.
- Skillset (example 1) has two skills: text split and embedding. Embedding model is also be used for vectorization at query time (assume text-to-vector conversion).
- Skillset (example 2) add a custom skill that points to external embedding model, or document intelligence.
- Skillset (example 3) add an entity recognition skill to lift locations from raw content into the index?
- Duplicated content is expected due to overlap and repetition of parent info. It won't affect your LLM.

Tasks:

- H2: Configure access to Azure Storage and upload sample data.
- H2: Create a data source
- H2: Create a skillset (choose one skillset)
- H2: Use alternative skillsets (present the other two skillsets)
- H2: Create and run the indexer
- H2: Check your data in the search index (hide vectors) -->

## Next step

> [!div class="nextstepaction"]
> [Chat with your data](tutorial-rag-build-solution-query.md)
