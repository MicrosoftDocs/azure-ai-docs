---
title: Generate embeddings
titleSuffix: Azure AI Search
description: Learn how to generate embeddings for downstream indexing into an Azure AI Search index.

author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.custom:
  - ignite-2023
ms.topic: how-to
ms.date: 08/04/2025
---

# Generate embeddings for search queries and documents

Azure AI Search doesn't host embedding models, so you're responsible for creating vectors for query inputs and outputs. Choose one of the following approaches:

| Approach | Description |
| --- | --- |
| [Integrated vectorization](vector-search-integrated-vectorization.md) | Use built-in data chunking and vectorization in Azure AI Search. This approach takes a dependency on indexers, skillsets, and built-in or custom skills that point to external embedding models, such as those in Azure AI Foundry. |
| Manual vectorization | Manage data chunking and vectorization yourself. For indexing, you [push prevectorized documents](vector-search-how-to-create-index.md#load-vector-data-for-indexing) into vector fields in a search index. For queries, you provide precomputed vectors to the search engine. For demos of this approach, see the [azure-search-vector-samples](https://github.com/Azure/azure-search-vector-samples/tree/main) GitHub repository. |

We recommend integrated vectorization for most scenarios and use it for illustration in this article. Although you can use any supported embedding model, this article assumes Azure OpenAI embedding models.

## How embedding models are used in vector queries

Embedding models are used to generate vectors for both [query inputs](#query-inputs) and [query outputs](#query-outputs).

### Query inputs

Query inputs are one of the following:

+ Text or images that are converted to vectors during query processing. With integrated vectorization, a [vectorizer](vector-search-how-to-configure-vectorizer.md) handles this task.

+ Precomputed vectors. You can generate these vectors by passing the query input to an embedding model of your choice. To avoid [rate limiting](/azure/ai-services/openai/quotas-limits), implement retry logic in your workload. We use [tenacity](https://pypi.org/project/tenacity/) in our Python demo.

### Query outputs

Query outputs are the matching documents retrieved from a search index based on the query input.

Your search index must have been previously loaded with documents containing one or more vector fields with embeddings. These embeddings can be generated using either integrated or manual vectorization. To ensure accurate results, use the same embedding model for both indexing and querying.

## Create resources in the same region

Although integrated vectorization with Azure OpenAI embedding models doesn't require resources to be in the same region, using the same region can improve performance and reduce latency.

To use the same region for your resources:

1. Check the [regional availability of text embedding models](/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability).

1. Check the [regional availability of Azure AI Search](search-region-support.md).

1. Create an Azure OpenAI resource and Azure AI Search service in the same region.

> [!NOTE]
> To use [semantic ranking](semantic-how-to-query-request.md) for hybrid queries or machine learning models for [AI enrichment](cognitive-search-concept-intro.md), choose an Azure AI Search region that provides those features.

## Generate an embedding for an improvised query

The following Python code generates an embedding that you can paste into the "values" property of a vector query.

```python
!pip install openai

import openai

openai.api_type = "azure"
openai.api_key = "YOUR-API-KEY"
openai.api_base = "https://YOUR-OPENAI-RESOURCE.openai.azure.com"
openai.api_version = "2024-02-01"

response = openai.Embedding.create(
    input="How do I use Python in VS Code?",
    engine="text-embedding-ada-002"
)
embeddings = response['data'][0]['embedding']
print(embeddings)
```

Output is a vector array of 1,536 dimensions.

## Choose an embedding model in Azure AI Foundry

In the Azure AI Foundry portal, you have the option of creating a search index when you add knowledge to your agent workflow. A wizard guides you through the steps. When asked to provide an embedding model that vectorizes your plain text content, you can use one of the following supported models:

+ text-embedding-3-large
+ text-embedding-3-small
+ text-embedding-ada-002
+ Cohere-embed-v3-english
+ Cohere-embed-v3-multilingual

Your model must already be deployed and you must have permission to access it. For more information, see [Deploy AI models in Azure AI Foundry portal](/azure/ai-foundry/concepts/deployments-overview).

## Tips and recommendations for embedding model integration

+ **Identify use cases**: Evaluate the specific use cases where embedding model integration for vector search features can add value to your search solution. This can include multimodal or matching image content with text content, multilingual search, or similarity search.

+ **Design a chunking strategy**: Embedding models have limits on the number of tokens they can accept, which introduces a data chunking requirement for large files. For more information, see [Chunk large documents for vector search solutions](vector-search-how-to-chunk-documents.md).

+ **Optimize cost and performance**: Vector search can be resource-intensive and is subject to maximum limits, so consider only vectorizing the fields that contain semantic meaning. [Reduce vector size](vector-search-how-to-configure-compression-storage.md) so that you can store more vectors for the same price.

+ **Choose the right embedding model:** Select an appropriate model for your specific use case, such as word embeddings for text-based searches or image embeddings for visual searches. Consider using pretrained models like **text-embedding-ada-002** from OpenAI or **Image Retrieval** REST API from [Azure AI Computer Vision](/azure/ai-services/computer-vision/how-to/image-retrieval).

+ **Normalize Vector lengths**: Ensure that the vector lengths are normalized before storing them in the search index to improve the accuracy and performance of similarity search. Most pretrained models already are normalized but not all.

+ **Fine-tune the model**: If needed, fine-tune the selected model on your domain-specific data to improve its performance and relevance to your search application.

+ **Test and iterate**: Continuously test and refine your embedding model integration to achieve the desired search performance and user satisfaction.

## Next steps

+ [Understanding embeddings in Azure OpenAI in Azure AI Foundry Models](/azure/ai-services/openai/concepts/understand-embeddings)
+ [Learn how to generate embeddings](/azure/ai-services/openai/how-to/embeddings?tabs=console)
+ [Tutorial: Explore Azure OpenAI embeddings and document search](/azure/ai-services/openai/tutorials/embeddings?tabs=command-line)
+ [Tutorial: Choose a model (RAG solutions in Azure AI Search)](tutorial-rag-build-solution-models.md)
