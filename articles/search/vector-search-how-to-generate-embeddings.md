---
title: Generate embeddings
titleSuffix: Azure AI Search
description: Learn how to generate embeddings for downstream indexing into an Azure AI Search index.

author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: how-to
ms.date: 05/21/2025
---

# Generate embeddings for search queries and documents

Azure AI Search doesn't host embedding models, so one of your challenges is creating vectors for query inputs and outputs. You can use any supported embedding model, but this article assumes Azure OpenAI embedding models for illustration.

We recommend [integrated vectorization](vector-search-integrated-vectorization.md), which provides built-in data chunking and vectorization. Integrated vectorization takes a dependency on indexers, skillsets, and built-in or custom skills that point to a model that executes externally from Azure AI Search. Several built-in skills point to embedding models in Azure AI Foundry, which makes integrated vectorization your easiest solution for solving the embedding challenge.

If you want to handle data chunking and vectorization yourself, we provide demos in the [sample repository](https://github.com/Azure/azure-search-vector-samples/tree/main) that show you how to integrate with other community solutions.

## How embedding models are used in vector queries

+ Query inputs are either vectors, or text or images that are converted to vectors during query processing. The built-in solution in Azure AI Search is to use a vectorizer. 

  Alternatively, you can also handle the conversion yourself by passing the query input to an embedding model of your choice. To avoid [rate limiting](/azure/ai-services/openai/quotas-limits), you can implement retry logic in your workload. For the Python demo, we used [tenacity](https://pypi.org/project/tenacity/).

+ Query outputs are any matching documents found in a search index. Your search index must have been previously loaded with documents having one or more vector fields with embeddings. Whatever embedding model you used for indexing, use that same model for queries.

## Create resources in the same region

Integrated vectorization usually requires resources to be in the same region:

1. [Check regions for a text embedding model](/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability).

1. [Find the same region for Azure AI Search](search-region-support.md). 

1. To support hybrid queries that include [semantic ranking](semantic-how-to-query-request.md), or if you want to try machine learning model integration using a [custom skill](cognitive-search-custom-skill-interface.md) in an [AI enrichment pipeline](cognitive-search-concept-intro.md), select an Azure AI Search region that provides those features.

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
