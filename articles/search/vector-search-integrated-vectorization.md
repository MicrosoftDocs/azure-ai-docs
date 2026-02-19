---
title: Integrated vectorization
titleSuffix: Azure AI Search
description: Add a vector embedding step in an Azure AI Search skillset to vectorize content during indexing or queries.
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.custom:
  - ignite-2023
ms.topic: concept-article
ms.date: 01/23/2026
---

# Integrated vector embedding in Azure AI Search

Integrated vectorization is an extension of the indexing and query pipelines in Azure AI Search. It adds the following capabilities:

+ Vector encoding during indexer-driven indexing
+ Vector encoding during queries

[Data chunking](vector-search-how-to-chunk-documents.md) isn't a hard requirement, but unless your raw documents are small, chunking is necessary for meeting the token input requirements of embedding models.

Vector conversions are one-way: nonvector-to-vector. For example, there's no vector-to-text conversion for queries or results, such as converting a vector result to a human-readable string, which is why indexes contain both vector and nonvector fields.

Integrated vectorization speeds up the development and minimizes maintenance tasks during data ingestion and query time because there are fewer operations that you have to implement manually. 

## Using integrated vectorization during indexing

For integrated data chunking and vector conversions, you're taking a dependency on the following components:

+ [An indexer](search-indexer-overview.md), which retrieves raw data from a [supported data source](search-indexer-overview.md#supported-data-sources) and drives the pipeline engine.

+ [A search index](search-what-is-an-index.md) to receive the chunked and vectorized content.

+ [A skillset](cognitive-search-working-with-skillsets.md) configured for:

  + A chunking strategy: [Text Split skill](cognitive-search-skill-textsplit.md), [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md), [Azure Content Understanding skill](cognitive-search-skill-content-understanding.md), or one of the [document parsing modes](vector-search-how-to-chunk-documents.md#common-chunking-techniques). 
  
  + An embedding skill, used to generate vector arrays, which can be any of the following:

    + [AzureOpenAIEmbedding skill](cognitive-search-skill-azure-openai-embedding.md), attached to text-embedding-ada-002,text-embedding-3-small, text-embedding-3-large on Azure OpenAI.

    + [Custom skill](cognitive-search-custom-skill-web-api.md) that points to another embedding model on Azure or on another site.

    + [Azure Vision multimodal embeddings skill (preview)](cognitive-search-skill-vision-vectorize.md) that points to the multimodal API for Azure Vision.

    + [AML skill](cognitive-search-aml-skill.md) that points to select models in the Microsoft Foundry model catalog.

## Using integrated vectorization in queries

For text-to-vector conversion during queries, you take a dependency on these components:

+ A query that specifies one or more vector fields.

+ A text string that's converted to a vector at query time.

+ [A vectorizer](vector-search-how-to-configure-vectorizer.md), defined in the index schema, assigned to a vector field, and used automatically at query time to convert a text query to a vector. The vectorizer you set up must match the embedding model used to encode your content. 

    | Embedding skill | Vectorizer |
    |-----------------|------------|
    | [AzureOpenAIEmbedding skill](cognitive-search-skill-azure-openai-embedding.md) | [Azure OpenAI vectorizer](vector-search-vectorizer-azure-open-ai.md) |
    | [Custom skill](cognitive-search-custom-skill-web-api.md) | [Custom Web API vectorizer](vector-search-vectorizer-custom-web-api.md) |
    | [Azure Vision multimodal embeddings skill (preview)](cognitive-search-skill-vision-vectorize.md)  | [Azure Vision vectorizer](vector-search-vectorizer-ai-services-vision.md) |
    | [AML skill pointing to the model catalog in Foundry portal](cognitive-search-aml-skill.md) | [Microsoft Foundry model catalog vectorizer](vector-search-vectorizer-azure-machine-learning-ai-studio-catalog.md) |

## Component diagram

The following diagram shows the components of integrated vectorization.

:::image type="content" source="media/vector-search-integrated-vectorization/integrated-vectorization-architecture.png" alt-text="Diagram of components in an integrated vectorization workflow." border="false" lightbox="media/vector-search-integrated-vectorization/integrated-vectorization-architecture.png":::

The workflow is an indexer pipeline. Indexers retrieve data from supported data sources and initiate data enrichment (or applied AI) by calling Azure OpenAI or Foundry Tools or custom code for text-to-vector conversions or other processing.

The diagram focuses on integrated vectorization, but your solution isn't limited to this list. You can add more skills for AI enrichment, create a knowledge store, add semantic ranking, add relevance tuning, and other query features.

## Availability and pricing

Integrated vectorization is available in all regions and tiers. However, if you're using skills and vectorizers for AI enrichment, regional requirements might apply. For more information, see [Attach a Foundry resource to a skillset](cognitive-search-attach-cognitive-services.md).

If you're using a custom skill and an Azure hosting mechanism (such as an Azure function app, Azure Web App, and Azure Kubernetes), check the [Azure product by region page](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/?products=search) for feature availability. 

Data chunking (Text Split skill) is free and available on all Foundry Tools in all regions.

> [!NOTE]
> Some older search services created before January 1, 2019 are deployed on infrastructure that doesn't support vector workloads. If you try to add a vector field to a schema and get an error, it's a result of outdated services. In this situation, you must create a new search service to try out the vector feature.

## What scenarios can integrated vectorization support?

+ Subdivide large documents into chunks, useful for vector and nonvector scenarios. For vectors, chunks help you meet the input constraints of embedding models. For nonvector scenarios, you might have a chat-style search app where GPT is assembling responses from indexed chunks. You can use vectorized or nonvectorized chunks for chat-style search.

+ Build a vector store where all of the fields are vector fields, and the document ID (required for a search index) is the only string field. Query the vector store to retrieve document IDs, and then send the document's vector fields to another model.

+ Combine vector and text fields for hybrid search, with or without semantic ranking. Integrated vectorization simplifies all of the [scenarios supported by vector search](vector-search-overview.md#what-scenarios-can-vector-search-support).

## How to use integrated vectorization

For query-only vectorization:

1. [Add a vectorizer](vector-search-how-to-configure-vectorizer.md#define-a-vectorizer-and-vector-profile) to an index. It should be the same embedding model used to generate vectors in the index.
1. [Assign the vectorizer](vector-search-how-to-configure-vectorizer.md#define-a-vectorizer-and-vector-profile) to a vector profile, and then assign a vector profile to the vector field.
1. [Formulate a vector query](vector-search-how-to-configure-vectorizer.md#test-a-vectorizer) that specifies the text string to vectorize.

A more common scenario - data chunking and vectorization during indexing:

1. [Create a data source](search-howto-create-indexers.md#prepare-a-data-source) connection to a supported data source for indexer-based indexing.
1. [Create a skillset](cognitive-search-defining-skillset.md) that calls [Text Split skill](cognitive-search-skill-textsplit.md) for chunking and [Azure OpenAI Embedding](cognitive-search-skill-azure-openai-embedding.md) or another embedding skill to vectorize the chunks.
1. [Create an index](search-how-to-create-search-index.md) that specifies a [vectorizer](vector-search-how-to-configure-vectorizer.md) for query time, and assign it to vector fields.
1. [Create an indexer](search-howto-create-indexers.md) to drive everything, from data retrieval, to skillset execution, through indexing. We recommend running the indexer [on a schedule](search-howto-schedule-indexers.md) to pick up changed documents or any documents that were missed due to throttling.

Optionally, [create secondary indexes](index-projections-concept-intro.md) for advanced scenarios where chunked content is in one index, and nonchunked in another index. Chunked indexes (or secondary indexes) are useful for RAG apps.

> [!TIP]
> [Try the **Import data (new)** wizard](search-get-started-portal-import-vectors.md) in the Azure portal to explore integrated vectorization before writing any code.

### Secure connections to vectorizers and models

If your architecture requires private connections that bypass the internet, you can create a [shared private link connection](search-indexer-howto-access-private.md) to the embedding models used by skills during indexing and vectorizers at query time. 

Shared private links only work for Azure-to-Azure connections. If you're connecting to OpenAI or another external model, the connection must be over the public internet.

For vectorization scenarios, you would use:

+ `openai_account` for embedding models hosted on an Azure OpenAI resource.

+ `sites` for embedding models accessed as a [custom skill](cognitive-search-custom-skill-interface.md) or [custom vectorizer](vector-search-vectorizer-custom-web-api.md). The `sites` group ID is for App services and Azure functions, which you could use to host an embedding model that isn't one of the Azure OpenAI embedding models.

## Benefits

Here are some of the key benefits of the integrated vectorization: 

+ No separate data chunking and vectorization pipeline. Code is simpler to write and maintain.  

+ Automate indexing end-to-end. When data changes in the source (such as in Azure Storage, Azure SQL, or Cosmos DB), the indexer can move those updates through the entire pipeline, from retrieval, to document cracking, through optional AI-enrichment, data chunking, vectorization, and indexing.

+ Batching and retry logic is built in (non-configurable). Azure AI Search has internal retry policies for throttling errors that surface due to the Azure OpenAI endpoint maxing out on token quotas for the embedding model. We recommend putting the indexer on a schedule (for example, every 5 minutes) so the indexer can process any calls that are throttled by the Azure OpenAI endpoint despite of the retry policies.

+ Projecting chunked content to secondary indexes. Secondary indexes are created as you would any search index (a schema with fields and other constructs), but they're populated in tandem with a primary index by an indexer. Content from each source document flows to fields in primary and secondary indexes during the same indexing run. 

  Secondary indexes are intended for question and answer or chat style apps. The secondary index contains granular information for more specific matches, but the parent index has more information and can often produce a more complete answer. When a match is found in the secondary index, the query returns the parent document from the primary index. For example, assuming a large PDF as a source document, the primary index might have basic information (title, date, author, description), while a secondary index has chunks of searchable content.

## Limitations

Make sure you know the [Azure OpenAI quotas and limits for embedding models](/azure/ai-services/openai/quotas-limits). Azure AI Search has retry policies, but if the quota is exhausted, retries fail.

Azure OpenAI token-per-minute limits are per model, per subscription. Keep this in mind if you're using an embedding model for both query and indexing workloads. If possible, [follow best practices](/azure/ai-services/openai/quotas-limits#general-best-practices-to-remain-within-rate-limits). Have an embedding model for each workload, and try to deploy them in different subscriptions.

On Azure AI Search, remember there are [service limits](search-limits-quotas-capacity.md) by tier and workloads.

## Next steps

+ [Set up integrated vectorization](search-how-to-integrated-vectorization.md)
+ [Configure a vectorizer in a search index](vector-search-how-to-configure-vectorizer.md)
+ [Configure index projections in a skillset](index-projections-concept-intro.md)
