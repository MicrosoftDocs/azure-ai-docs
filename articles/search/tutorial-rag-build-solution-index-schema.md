---
title: 'RAG tutorial: Design an index'
titleSuffix: Azure AI Search
description: Design an index for RAG patterns in Azure AI Search.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: tutorial
ms.date: 12/18/2024

---

# Tutorial: Design an index for RAG in Azure AI Search

An index contains searchable text and vector content, plus configurations. In a RAG pattern that uses a chat model for responses, you want an index designed around chunks of content that can be passed to an LLM at query time. 

In this tutorial, you:

> [!div class="checklist"]
> - Learn the characteristics of an index schema built for RAG
> - Create an index that accommodates vector and hybrid queries
> - Add vector profiles and configurations
> - Add structured data
> - Add filtering

## Prerequisites

[Visual Studio Code](https://code.visualstudio.com/download) with the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and the [Jupyter package](https://pypi.org/project/jupyter/). For more information, see [Python in Visual Studio Code](https://code.visualstudio.com/docs/languages/python).

The output of this exercise is an index definition in JSON. At this point, it's not uploaded to Azure AI Search, so there are no requirements for cloud services or permissions in this exercise.

## Review schema considerations for RAG

In conversational search, LLMs compose the response that the user sees, not the search engine, so you don't need to think about what fields to show in your search results, and whether the representations of individual search documents are coherent to the user. Depending on the question, the LLM might return verbatim content from your index, or more likely, repackage the content for a better answer.

### Organized around chunks

When LLMs generate a response, they operate on chunks of content for message inputs, and while they need to know where the chunk came from for citation purposes, what matters most is the quality of message inputs and its relevance to the user's question. Whether the chunks come from one document or a thousand, the LLM ingests the information or *grounding data*, and formulates the response using instructions provided in a system prompt.

Chunks are the focus of the schema, and each chunk is the defining element of a search document in a RAG pattern. You can think of your index as a large collection of chunks, as opposed to traditional search documents that probably have more structure, such as fields containing uniform content for a name, descriptions, categories, and addresses.

### Enhanced with generated data

In this tutorial, sample data consists of PDFs and content from the [NASA Earth Book](https://www.nasa.gov/ebooks/earth/). This content is descriptive and informative, with numerous references to geographies, countries, and areas across the world. All of the textual content is captured in chunks, but recurring instances of place names create an opportunity for adding structure to the index. Using skills, it's possible to recognize entities in the text and capture them in an index for use in queries and filters. In this tutorial, we include an [entity recognition skill](cognitive-search-skill-entity-recognition-v3.md) that recognizes and extracts location entities, loading it into a searchable and filterable `locations` field. Adding structured content to your index gives you more options for filtering, improved relevance, and more focused answers.

### Parent-child fields in one or two indexes?

Chunked content typically derives from a larger document. And although the schema is organized around chunks, you also want to capture properties and content at the parent level. Examples of these properties might include the parent file path, title, authors, publication date, or a summary.

An inflection point in schema design is whether to have two indexes for parent and child/chunked content, or a single index that repeats parent elements for each chunk.

In this tutorial, because all of the chunks of text originate from a single parent (NASA Earth Book), you don't need a separate index dedicated to up level the parent fields. However, if you're indexing from multiple parent PDFs, you might want a parent-child index pair to capture level-specific fields and then send [lookup queries](/rest/api/searchservice/documents/get) to the parent index to retrieve those fields relevant to each chunk.

### Checklist of schema considerations

In Azure AI Search, an index that works best for RAG workloads has these qualities:

- Returns chunks that are relevant to the query and readable to the LLM. LLMs can handle a certain level of dirty data in chunks, such as mark up, redundancy, and incomplete strings. While chunks need to be readable and relevant to the question, they don't need to be pristine.

- Maintains a parent-child relationship between chunks of a document and the properties of the parent document, such as the file name, file type, title, author, and so forth. To answer a query, chunks could be pulled from anywhere in the index. Association with the parent document providing the chunk is useful for context, citations, and follow up queries.

- Accommodates the queries you want create. You should have fields for vector and hybrid content, and those fields should be attributed to support specific query behaviors, such as searchable or filterable. You can only query one index at a time (no joins) so your fields collection should define all of your searchable content.

- Your schema should either be flat (no complex types or structures), or you should [format the complext type output as JSON](search-get-started-rag.md#send-a-complex-rag-query) before sending it to the LLM. This requirement is specific to the RAG pattern in Azure AI Search.

> [!NOTE]
> Schema design affects storage and costs. This exercise is focused on schema fundamentals. In the [Minimize storage and costs](tutorial-rag-build-solution-minimize-storage.md) tutorial, you revisit schemas to learn how narrow data types, compression, and storage options significantly reduce the amount of storage used by vectors.

## Create an index for RAG workloads

A minimal index for LLM is designed to store chunks of content. It typically includes vector fields if you want similarity search for highly relevant results. It also includes nonvector fields for human-readable inputs to the LLM for conversational search. Nonvector chunked content in the search results becomes the grounding data sent to the LLM.

1. Open Visual Studio Code and create a new file. It doesn't have to be a Python file type for this exercise.

1. Here's a minimal index definition for RAG solutions that support vector and hybrid search. Review it for an introduction to required elements: index name, fields, and a configuration section for vector fields.

    ```json
    {
      "name": "example-minimal-index",
      "fields": [
        { "name": "id", "type": "Edm.String", "key": true },
        { "name": "chunked_content", "type": "Edm.String", "searchable": true, "retrievable": true },
        { "name": "chunked_content_vectorized", "type": "Edm.Single", "dimensions": 1536, "vectorSearchProfile": "my-vector-profile", "searchable": true, "retrievable": false, "stored": false },
        { "name": "metadata", "type": "Edm.String", "retrievable": true, "searchable": true, "filterable": true }
      ],
      "vectorSearch": {
          "algorithms": [
              { "name": "my-algo-config", "kind": "hnsw", "hnswParameters": { }  }
          ],
          "profiles": [ 
            { "name": "my-vector-profile", "algorithm": "my-algo-config" }
          ]
      }
    }
    ```

   Fields must include key field (`"id"` in this example) and should include vector chunks for similarity search, and nonvector chunks for inputs to the LLM. 

   Vector fields are associated with algorithms that determine the search paths at query time. The index has a vectorSearch section for specifying multiple algorithm configurations. Vector fields also have [specific types](/rest/api/searchservice/supported-data-types#edm-data-types-for-vector-fields) and extra attributes for embedding model dimensions. `Edm.Single` is a data type that works for commonly used LLMs. For more information about vector fields, see [Create a vector index](vector-search-how-to-create-index.md).

   Metadata fields might be the parent file path, creation date, or content type and are useful for [filters](vector-search-filters.md).

1. Here's the index schema for the [tutorial source code](https://github.com/Azure-Samples/azure-search-python-samples/blob/main/Tutorial-RAG/Tutorial-rag.ipynb) and the [Earth Book content](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/nasa-e-book/earth_book_2019_text_pages). 

   Like the basic schema, it's organized around chunks. The `chunk_id` uniquely identifies each chunk. The `text_vector` field is an embedding of the chunk. The nonvector `chunk` field is a readable string. The `title` maps to a unique metadata storage path for the blobs. The `parent_id` is the only parent-level field, and it's a base64-encoded version of the parent file URI. 

   In integrated vectorization workloads like the one used in this tutorial series, the `dimensions` property on your vector fields should be identical to the number of `dimensions` generated by the embedding skill used to vectorize your data. In this series, we use the Azure OpenAI embedding skill, which calls the text-embedding-3-large model on Azure OpenAI. The skill is specified in the next tutorial. We set dimensions to 1024 in both the vector field and in the skill definition.

   The schema also includes a `locations` field for storing generated content that's created by the [indexing pipeline](tutorial-rag-build-solution-pipeline.md).

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

1. For an index schema that more closely mimics structured content, you would have separate indexes for parent and child (chunked) fields. You would need [index projections](index-projections-concept-intro.md) to coordinate the indexing of the two indexes simultaneously. Queries execute against the child index. Query logic includes a lookup query, using the parent_idt  retrieve content from the parent index.

   Fields in the child index:

   - ID
   - chunk
   - chunkVectcor
   - parent_id

   Fields in the parent index (everything that you want "one of"):

   - parent_id
   - parent-level fields (name, title, category)

<!-- Objective:

- Design an index schema that generates results in a format that works for LLMs.

Key points:

- schema for rag is designed for producing chunks of content
- schema should be flat (no complex types or structures)
- schema determines what queries you can create (be generous in attribute assignments)
- schema must cover all the queries you want to run. You can only query one index at a time (no joins), but you can create indexes that preserve parent-child relationship, and then use nested queries or parallel queries in your search logic to pull from both.
- schema has impact on storage/size. Consider narrow data types, attribution, vector configuration.
- show schema patterns: one for parent-child all-up, one for paired indexes via index projections
- note metadata for filters
- TBD: add fields for location and use entity recognition to pull this values out of the PDFs? Not sure how the extraction will work on chunked documents or how it will query, but goal would be to show that you can add structured data to the schema.

Tasks:

- H2 How to create an index for chunked and vectorized data (show examples for parent-child variants)
- H2 How to define vector profiles and configuration (discuss pros and cons, shouldn't be a rehash of existing how-to)
- H2 How to add filters
- H2 How to add structured data (example is "location", top-level field, data aquisition is through the pipeline) -->

## Next step

> [!div class="nextstepaction"]
> [Create an indexing pipeline](tutorial-rag-build-solution-pipeline.md)
