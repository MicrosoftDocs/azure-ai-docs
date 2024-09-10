---
title: 'RAG Tutorial: Build an indexing pipeline'
titleSuffix: Azure AI Search
description: Create an indexer-driven pipeline that loads, chunks, embeds, and ingests content for RAG solutions on Azure AI Search.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: cognitive-search
ms.topic: tutorial
ms.date: 09/12/2024

---

# Tutorial: Build an indexing pipeline for RAG on Azure AI Search

Learn how to build an automated indexing pipeline for a RAG solution on Azure AI Search. Indexing automation is through an indexer that drives indexing and skillset execution, providing [integrated data chunking and vectorization](vector-search-integrated-vectorization.md) on a one-time or recurring basis for incremental updates.

In this tutorial, you:

> [!div class="checklist"]
> - Provide the index schema from the previous tutorial 
> - Create a data source connection
> - Create an indexer
> - Create a skillset
> - Run the indexer and check results

If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/?WT.mc_id=A261C142F) before you begin.

> [!TIP]
> You can use the [Import and vectorize data wizard](search-import-data-portal.md) to create your pipeline. For some quickstarts, see [Image search](search-get-started-portal-image-search.md) and [Vector search](search-get-started-portal-import-vectors.md).

## Prerequisites

- [Visual Studio Code](https://code.visualstudio.com/download) with the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and the [Jupyter package](https://pypi.org/project/jupyter/). For more information, see [Python in Visual Studio Code](https://code.visualstudio.com/docs/languages/python).

- Azure Storage general purpose account. This exercise uploads PDF files into blob storage for automated indexing.

- Azure AI Search, Basic tier or above for managed identity and semantic ranking. Choose a region that's shared with Azure OpenAI.

- Azure OpenAI, with a deployment of text-embedding-002. For more information about embedding models used in RAG solutions, see [Choose embedding models for RAG in Azure AI Search](tutorial-rag-build-solution-models.md)

## Download file

[Download a Jupyter notebook](https://github.com/Azure-Samples/azure-search-python-samples/blob/main/Tutorial-RAG/Tutorial-rag.ipynb) from GitHub to send the requests in this quickstart. For more information, see [Downloading files from GitHub](https://docs.github.com/get-started/start-your-journey/downloading-files-from-github).

## Provide the index schema

Here's the index schema from the [previous tutorial](tutorial-rag-build-solution-index-schema.md). It's organized around vectorized and nonvectorized chunks. It includes a `locations` field that stores AI-generated content created by the skillset.  

```python
index_name = "py-rag-tutorial-idx"
index_client = SearchIndexClient(endpoint=AZURE_SEARCH_SERVICE, credential=AZURE_SEARCH_CREDENTIAL)  
fields = [
    SearchField(name="parent_id", type=SearchFieldDataType.String),  
    SearchField(name="title", type=SearchFieldDataType.String),
    SearchField(name="locations", type=SearchFieldDataType.Collection(SearchFieldDataType.String), filterable=True),
    SearchField(name="chunk_id", type=SearchFieldDataType.String, key=True, sortable=True, filterable=True, facetable=True, analyzer_name="keyword"),  
    SearchField(name="chunk", type=SearchFieldDataType.String, sortable=False, filterable=False, facetable=False),  
    SearchField(name="text_vector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single), vector_search_dimensions=1536, vector_search_profile_name="myHnswProfile")
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
            vectorizer="myOpenAI",  
        )
    ],  
    vectorizers=[  
        AzureOpenAIVectorizer(  
            name="myOpenAI",  
            kind="azureOpenAI",  
            azure_open_ai_parameters=AzureOpenAIParameters(  
                resource_uri=AZURE_OPENAI_ACCOUNT,  
                deployment_id="text-embedding-ada-002",
                model_name="text-embedding-ada-002"
            ),
        ),  
    ],  
)  
    
# Create the search index on Azure AI Search
index = SearchIndex(name=index_name, fields=fields, vector_search=vector_search)  
result = index_client.create_or_update_index(index)  
print(f"{result.name} created")  
```

## Create a data source connection

In this step, set up a connection to Azure Blob Storage. The indexer retrieves PDFs from a container. You can create the container and upload files in the Azure portal.

1. Sign in to the Azure portal and find your Azure Storage account.

1. Create a container and upload the PDFs from [earth_book_2019_text_pages](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/nasa-e-book/earth_book_2019_text_pages).

1. Make sure Azure AI Search has **Storage Blob Data Reader** permissions on the resource.

1. Next, in Visual Studio Code, define an indexer data source that provides connection information during indexing.

    ```python
    from azure.search.documents.indexes import SearchIndexerClient
    from azure.search.documents.indexes.models import (
        SearchIndexerDataContainer,
        SearchIndexerDataSourceConnection
    )
    
    # Create a data source 
    indexer_client = SearchIndexerClient(endpoint=AZURE_SEARCH_SERVICE, credential=AZURE_SEARCH_CREDENTIAL)
    container = SearchIndexerDataContainer(name="nasa-ebook-pdfs-all")
    data_source_connection = SearchIndexerDataSourceConnection(
        name="py-rag-tutorial-ds",
        type="azureblob",
        connection_string=AZURE_STORAGE_CONNECTION,
        container=container
    )
    data_source = indexer_client.create_or_update_data_source_connection(data_source_connection)
    
    print(f"Data source '{data_source.name}' created or updated")
    ```

## Create a skillset

Skills are the basis for integrated data chunking and vectorization. At a minimum, you want a Text Split skill to chunk your content, and an embedding skill that create vector representations of your chunked content.

In this skillset, an extra skill is used to create structured data in the index. The Entity Recognition skill is used to identify locations, which can range from proper names to generic references, such as "ocean" or "mountain". Having structured data gives you more options for creating interesting queries and boosting relevance.

```python
from azure.search.documents.indexes.models import (
    SplitSkill,
    InputFieldMappingEntry,
    OutputFieldMappingEntry,
    AzureOpenAIEmbeddingSkill,
    EntityRecognitionSkill,
    SearchIndexerIndexProjections,
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
    resource_uri=AZURE_OPENAI_ACCOUNT,  
    deployment_id="text-embedding-ada-002",  
    model_name="text-embedding-ada-002",
    dimensions=1536,
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
  
index_projections = SearchIndexerIndexProjections(  
    selectors=[  
        SearchIndexerIndexProjectionSelector(  
            target_index_name=index_name,  
            parent_key_field_name="parent_id",  
            source_context="/document/pages/*",  
            mappings=[  
                InputFieldMappingEntry(name="chunk", source="/document/pages/*"),  
                InputFieldMappingEntry(name="text_vector", source="/document/pages/*/text_vector"),  
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
    index_projections=index_projections,
    cognitive_services_account=cognitive_services_account
)
  
client = SearchIndexerClient(endpoint=AZURE_SEARCH_SERVICE, credential=AZURE_SEARCH_CREDENTIAL)  
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

indexer_client = SearchIndexerClient(endpoint=AZURE_SEARCH_SERVICE, credential=AZURE_SEARCH_CREDENTIAL)  
indexer_result = indexer_client.create_or_update_indexer(indexer)  
  
# Run the indexer  
indexer_client.run_indexer(indexer_name)  
print(f' {indexer_name} is created and running. Give the indexer a few minutes before running a query.')  
```

## Run hybrid search to check results

Send a query to confirm your index is operational. A hybrid query is useful for verifying text and vector search.

```python
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizableTextQuery

# Hybrid Search
query = "where are the nasa headquarters located?"  

search_client = SearchClient(endpoint=AZURE_SEARCH_SERVICE, credential=AZURE_SEARCH_CREDENTIAL, index_name=index_name)
vector_query = VectorizableTextQuery(text=query, k_nearest_neighbors=1, fields="text_vector", exhaustive=True)
  
results = search_client.search(  
    search_text=query,  
    vector_queries= [vector_query],
    select=["parent_id", "chunk_id", "title", "chunk", "locations"],
    top=1
)  
  
for result in results:  
    print(f"Score: {result['@search.score']}")
    print(f"Title: {result['title']}")  
    print(f"Content: {result['chunk']}") 
```

This query returns a single match (`top=1`) consisting of the one chunk determined by the search engine to be the most relevant. Results from the query should look similar to the following example:

```
Score: 0.03306011110544205
Content: national Aeronautics and Space Administration

earth Science

NASA Headquarters 

300 E Street SW 

Washington, DC 20546

www.nasa.gov

np-2018-05-2546-hQ
```

Try a few more queries to get a sense of what the search engine returns directly so that you can compare it with an LLM-enabled response. Re-run the previous script with this query: "how much of the earth is covered in water"?

Results from this second query should look similar to the following results, which are lightly edited for concision. 

With this example, it's easier to spot how chunks are returned verbatim, and how keyword and similarity search identify top matches. This specific chunk definitely has information about water and coverage over the earth, but it's not exactly relevant to the query. Semantic ranking would find a better answer, but as a next step, let's see how to connect Azure AI Search to an LLM for conversational search.

```
Score: 0.03333333507180214
Content:

Land of Lakes
Canada

During the last Ice Age, nearly all of Canada was covered by a massive ice sheet. Thousands of years later, the landscape still shows 

the scars of that icy earth-mover. Surfaces that were scoured by retreating ice and flooded by Arctic seas are now dotted with 

millions of lakes, ponds, and streams. In this false-color view from the Terra satellite, water is various shades of blue, green, tan, and 

black, depending on the amount of suspended sediment and phytoplankton; vegetation is red.

The region of Nunavut Territory is sometimes referred to as the “Barren Grounds,” as it is nearly treeless and largely unsuitable for 

agriculture. The ground is snow-covered for much of the year, and the soil typically remains frozen (permafrost) even during the 

summer thaw. Nonetheless, this July 2001 image shows plenty of surface vegetation in midsummer, including lichens, mosses, 

shrubs, and grasses. The abundant fresh water also means the area is teeming with flies and mosquitoes.
```

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

<!-- 
## Prerequisites

TBD

## Create a blob data source

1. Create a baseline data source definition with required elements. Provide a valid connection string to your Azure Storage account. Provide the name of the container that has the sample data.

    ```http
    ### Create a data source
    POST {{baseUrl}}/datasources?api-version=2024-05-01-preview  HTTP/1.1
      Content-Type: application/json
      Authorization: Bearer {{token}}
    
        {
            "name": "demo-rag-ds",
            "description": null,
            "type": "azureblob",
            "subtype": null,
            "credentials": {
                "connectionString": "{{storageConnectionString}}"
            },
            "container": {
                "name": "{{blobContainer}}",
                "query": null
            },
            "dataChangeDetectionPolicy": null,
            "dataDeletionDetectionPolicy": null
        }
    ```

1. Review the [Datasource REST API](/rest/api/searchservice/data-sources/create) for information about other properties. For more information about blob indexers, see [Index data from Azure Blob Storage](search-howto-indexing-azure-blob-storage.md).

1. Send the request to save the data source to Azure AI Search.

## Create an indexer

1. Create a baseline indexer definition with required elements. In this example, the indexer is disabled so that it doesn't immediately run when it's saved to the search service. In later steps, you'll add a skillset and output field mappings, and run the indexer once it's fully specified.

   ```http
    ### Create and run an indexer
    POST {{baseUrl}}/indexers?api-version=2023-11-01  HTTP/1.1
      Content-Type: application/json
      Authorization: Bearer {{token}}

       {   
        "name" : "demo-rag-idxr",  
        "dataSourceName" : "demo-rag-ds",  
        "targetIndexName" : "demo-rag-index",  
        "skillsetName" : null,
        "disabled" : true,
        "fieldMappings" : null,
        "outputFieldMappings" : null
        }
   ```

1. Review the [Indexer REST API](/rest/api/searchservice/indexers/create) for information about other properties. For more information about indexers, see [Create an indexer](search-howto-create-indexers.md).

1. Send the request to save the data source to Azure AI Search.

## About indexer execution

An indexer connects to a supported data source, retrieves data, serializes it into JSON, calls a skillset, and populates a predefined index with raw content from the source and generated content from a skillset.

An indexer requires a data source and an index, and accepts a skillset definition. All of these objects are distinct. 

- An indexer object provides configuration information and field mappings.
- A data source has connection information.
- An index is the destination of an indexer pipeline and it defines the physical structure of your data in Azure AI Search.
- A skillset is optional, but necessary for RAG workloads if you want integrated data chunking and vectorization.

If you're already familiar with indexers and data sources, the definitions don't change in a RAG solution. 

## Checklist for indexer execution

Before you run an indexer, review this checklist to avoid problems during indexing. This checklist applies equally to RAG and non-RAG scenarios:

- Is the data source accessible to Azure AI Search? Check network configuration and permissions. Indexers connect under a search service identity. Consider configuring your search service for a managed identity and then granting it read permissions. 
- Does the data source support change tracking? Enable it so that your search service can keep your index up to date.
- Is the data ready for indexing? Indexers consume a single table (or view), or a collection of documents from a single directory. You can either consolidate files into one location, or you could create multiple data sources and indexers that send data to the same index.
- Do you need vectorization? Most RAG apps built on Azure AI Search include vector content in the index to support similarity search and hybrid queries. If you need vectorization and chunking, create a skillset and add it to your indexer.
- Do you need field mappings? If source and destination field names or types are different, add field mappings. 
- If you have a skillset that generates content that you need to store in your index, add output field mappings. Data chunks fall into this category. More information about output field mappings is covered in the skillset exercise.

## Check index

duplicated content in the index

chunks aren't intended for classic search experience. Chunks might start or end mid-sentence or contain duplicated content if you specified an overlap.

Combined index means duplicated parent fields. Document grain is the chunk so each chunk has its copy of parent fields.
Overlapping text also duplicates content.

All of this duplicated content is acceptable for LLMS because they aren't returning verbatim results.

if you're sending search results directly to a search page, it's a poor experience.
 -->

## Next step

> [!div class="nextstepaction"]
> [Chat with your data](tutorial-rag-build-solution-query.md)