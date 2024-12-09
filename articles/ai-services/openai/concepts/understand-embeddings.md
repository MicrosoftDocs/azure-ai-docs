---
title: Azure OpenAI Service embeddings
titleSuffix: Azure OpenAI - embeddings and cosine similarity
description: Learn more about how the Azure OpenAI embeddings API uses cosine similarity for document search and to measure similarity between texts.
#services: cognitive-services
manager: nitinme
ms.service: azure-ai-openai
ms.topic: tutorial
ms.date: 10/6/2024
author: mrbullwinkle
ms.author: mbullwin
recommendations: false
ms.custom:
---

# Understand embeddings in Azure OpenAI Service

An embedding is a special format of data representation that machine learning models and algorithms can easily use. The embedding is an information dense representation of the semantic meaning of a piece of text. Each embedding is a vector of floating-point numbers, such that the distance between two embeddings in the vector space is correlated with semantic similarity between two inputs in the original format. For example, if two texts are similar, then their vector representations should also be similar. Embeddings power vector similarity search in retrieval systems such as [Azure AI Search](/azure/search) (recommended) and in Azure databases such as [Azure Cosmos DB for MongoDB vCore](/azure/cosmos-db/mongodb/vcore/vector-search) ,  [Azure SQL Database](/azure/azure-sql/database/ai-artificial-intelligence-intelligent-applications?view=azuresql&preserve-view=true#vector-search), and [Azure Database for PostgreSQL - Flexible Server](/azure/postgresql/flexible-server/how-to-use-pgvector).

## Embedding models

Embeddings make it easier to do machine learning on large inputs representing words by capturing the semantic similarities in a vector space. Therefore, you can use embeddings to determine if two text chunks are semantically related or similar, and provide a score to assess similarity.

## Cosine similarity

Azure OpenAI embeddings often rely on cosine similarity to compute similarity between documents and a query.

From a mathematic perspective, cosine similarity measures the cosine of the angle between two vectors projected in a multidimensional space. This measurement is beneficial, because if two documents are far apart by Euclidean distance because of size, they could still have a smaller angle between them and therefore higher cosine similarity. For more information about cosine similarity equations, see [Cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity).

An alternative method of identifying similar documents is to count the number of common words between documents. This approach doesn't scale since an expansion in document size is likely to lead to a greater number of common words detected even among disparate topics. For this reason, cosine similarity can offer a more effective alternative.

## Next steps

* Learn more about using Azure OpenAI and embeddings to perform document search with our [embeddings tutorial](../tutorials/embeddings.md).
* Store your embeddings and perform vector (similarity) search using [Azure Cosmos DB for MongoDB vCore](/azure/cosmos-db/mongodb/vcore/vector-search), [Azure Cosmos DB for NoSQL](/azure/cosmos-db/rag-data-openai) ,  [Azure SQL Database](/azure/azure-sql/database/ai-artificial-intelligence-intelligent-applications?view=azuresql&preserve-view=true#vector-search) or [Azure Database for PostgreSQL - Flexible Server](/azure/postgresql/flexible-server/how-to-use-pgvector).
* Use an Eventhouse in Real-Time Intelligence in Microsoft Fabric as a [Vector database](/fabric/real-time-intelligence/vector-database)
    * Use the [series_cosine_similarity](/kusto/query/series-cosine-similarity-function?view=microsoft-fabric&preserve-view=true) function for similarity search.
