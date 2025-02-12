---
title: 'RAG tutorial: Minimize storage and costs'
titleSuffix: Azure AI Search
description: Compress vectors using narrow data types and scalar quantization. Remove extra copies of stored vectors to further save on space.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: tutorial
ms.date: 02/05/2025

---

# Tutorial: Minimize storage and costs (RAG in Azure AI Search)

Azure AI Search offers several approaches for reducing the size of vector indexes. These approaches range from vector compression, to being more selective over what you store on your search service.

In this tutorial, you modify the existing search index to use:

> [!div class="checklist"]
> - Narrow data types
> - Scalar quantization
> - Reduced storage by opting out of vectors in search results

This tutorial reprises the search index created by the [indexing pipeline](tutorial-rag-build-solution-pipeline.md). All of these updates affect the existing content, requiring you to rerun the indexer. However, instead of deleting the search index, you create a second one so that you can compare reductions in vector index size after adding the new capabilities.

Altogether, the techniques illustrated in this tutorial can reduce vector storage by about half.

The following screenshot compares the [first index](tutorial-rag-build-solution-pipeline.md) from a previous tutorial to the index built in this one.

:::image type="content" source="media/tutorial-rag-solution/side-by-side-comparison.png" lightbox="media/tutorial-rag-solution/side-by-side-comparison.png" alt-text="Screenshot of the original vector index with the index created using the schema in this tutorial.":::

## Prerequisites

This tutorial is essentially a rerun of the [indexing pipeline](tutorial-rag-build-solution-pipeline.md). You need all of the Azure resources and permissions described in that tutorial.

For comparison, you should have an existing *py-rag-tutorial-idx* index on your Azure AI Search service. It should be almost 2 MB in size, and the vector index portion should be 348 KB.

You should also have the following objects:

- py-rag-tutorial-ds (data source)

- py-rag-tutorial-ss (skillset)

## Download the sample

[Download a Jupyter notebook](https://github.com/Azure-Samples/azure-search-python-samples/blob/main/Tutorial-RAG/Tutorial-rag.ipynb) from GitHub to send the requests to Azure AI Search. For more information, see [Downloading files from GitHub](https://docs.github.com/get-started/start-your-journey/downloading-files-from-github).

## Update the index for reduced storage

Azure AI Search has multiple approaches for reducing vector size, which lowers the cost of vector workloads. In this step, create a new index that uses the following capabilities:

- Vector compression. Scalar quantization provides this capability.

- Eliminate optional storage. If you only need vectors for queries and not in a response payload, you can drop the vector copy used for search results.

- Narrow data types. You can specify `Collection(Edm.Half)` on the text_vector field to store incoming float32 dimensions as float16, which takes up less space in the index.

All of these capabilities are specified in a search index. After you load the index, compare the difference between the original index and the new one.

1. Name the new index `py-rag-tutorial-small-vectors-idx`.

1. Use the following definition for the new index. The difference between this schema and the previous schema updates in [Maximize relevance](tutorial-rag-build-solution-maximize-relevance.md) are new classes for scalar quantization and a new compressions section, a new data type (`Collection(Edm.Half)`) for the text_vector field, and a new property `stored` set to false.

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
        ScalarQuantizationCompression,
        ScalarQuantizationParameters,
        SearchIndex,
        SemanticConfiguration,
        SemanticPrioritizedFields,
        SemanticField,
        SemanticSearch,
        ScoringProfile,
        TagScoringFunction,
        TagScoringParameters
    )
    
    credential = DefaultAzureCredential()
    
    index_name = "py-rag-tutorial-small-vectors-idx"
    index_client = SearchIndexClient(endpoint=AZURE_SEARCH_SERVICE, credential=credential)  
    fields = [
        SearchField(name="parent_id", type=SearchFieldDataType.String),  
        SearchField(name="title", type=SearchFieldDataType.String),
        SearchField(name="locations", type=SearchFieldDataType.Collection(SearchFieldDataType.String), filterable=True),
        SearchField(name="chunk_id", type=SearchFieldDataType.String, key=True, sortable=True, filterable=True, facetable=True, analyzer_name="keyword"),  
        SearchField(name="chunk", type=SearchFieldDataType.String, sortable=False, filterable=False, facetable=False),  
        SearchField(name="text_vector", type="Collection(Edm.Half)", vector_search_dimensions=1024, vector_search_profile_name="myHnswProfile", stored= False)
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
                compression_name="myScalarQuantization",
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
        compressions=[
            ScalarQuantizationCompression(
                compression_name="myScalarQuantization",
                rerank_with_original_vectors=True,
                default_oversampling=10,
                parameters=ScalarQuantizationParameters(quantized_data_type="int8"),
            )
        ]
    )
    
    semantic_config = SemanticConfiguration(
        name="my-semantic-config",
        prioritized_fields=SemanticPrioritizedFields(
            title_field=SemanticField(field_name="title"),
            keywords_fields=[SemanticField(field_name="locations")],
            content_fields=[SemanticField(field_name="chunk")]
        )
    )
    
    semantic_search = SemanticSearch(configurations=[semantic_config])
    
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
    
    index = SearchIndex(name=index_name, fields=fields, vector_search=vector_search, semantic_search=semantic_search, scoring_profiles=scoring_profiles)  
    result = index_client.create_or_update_index(index)  
    print(f"{result.name} created")
    ```

## Create or reuse the data source

Here's the definition of the data source from the previous tutorial. If you already have this data source on your search service, you can skip creating a new one.

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

## Create or reuse the skillset

The skillset is also unchanged from the previous tutorial. Here it is again so that you can review it.

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

## Create a new indexer and load the index

Although you could reset and rerun the existing indexer using the new index, it's just as easy to create a new indexer. Having two indexes and indexers preserves the execution history and allows for closer comparisons.

This indexer is identical to the previous indexer, except that it specifies the new index from this tutorial.

```python
from azure.search.documents.indexes.models import (
    SearchIndexer
)

# Create an indexer  
indexer_name = "py-rag-tutorial-small-vectors-idxr" 

indexer_parameters = None

indexer = SearchIndexer(  
    name=indexer_name,  
    description="Indexer to index documents and generate embeddings",
    target_index_name="py-rag-tutorial-small-vectors-idx",
    skillset_name="py-rag-tutorial-ss", 
    data_source_name="py-rag-tutorial-ds",
    parameters=indexer_parameters
)  

# Create and run the indexer  
indexer_client = SearchIndexerClient(endpoint=AZURE_SEARCH_SERVICE, credential=credential)  
indexer_result = indexer_client.create_or_update_indexer(indexer)  

print(f' {indexer_name} is created and running. Give the indexer a few minutes before running a query.')
```

As a final step, switch to the Azure portal to compare the vector storage requirements for the two indexes. You should results similar to the following screenshot.

:::image type="content" source="media/tutorial-rag-solution/side-by-side-comparison.png" lightbox="media/tutorial-rag-solution/side-by-side-comparison.png" alt-text="Screenshot of the original vector index with the index created using the schema in this tutorial.":::

The index created in this tutorial uses half-precision floating-point numbers (float16) for the text vectors. This reduces the storage requirements for the vectors by half compared to the previous index that used single-precision floating-point numbers (float32). Scalar compression and the omission of one set of the vectors account for the remaining storage savings. For more information about reducing vector size, see [Choose an approach for optimizing vector storage and processing](vector-search-how-to-configure-compression-storage.md).

Consider revisiting the [queries from the previous tutorial](tutorial-rag-build-solution-query.md) so that you can compare query speed and utility. You should expect some variation in LLM output whenever you repeat a query, but in general the storage-saving techniques you implemented shouldn't degrade the quality of your search results.

## Next step

There are code samples in all of the Azure SDKs that provide Azure AI Search programmability. You can also review vector sample code for specific use cases and technology combinations.

> [!div class="nextstepaction"]
> [azure-search-vector-samples](https://github.com/Azure/azure-search-vector-samples)