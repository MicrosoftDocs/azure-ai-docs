---
title: Azure OpenAI in Microsoft Foundry Models embeddings tutorial
titleSuffix: Azure OpenAI
description: Learn how to use Azure OpenAI's embeddings API for document search with the BillSum dataset
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: tutorial
ms.date: 11/04/2025
author: mrbullwinkle #noabenefraim
ms.author: mbullwin
recommendations: false
monikerRange: 'foundry-classic || foundry'
ms.custom: devx-track-python
---

# Tutorial: Explore Azure OpenAI in Microsoft Foundry Models embeddings and document search

This tutorial will walk you through using the Azure OpenAI [embeddings](../concepts/understand-embeddings.md) API to perform **document search** where you'll query a knowledge base to find the most relevant document.

In this tutorial, you learn how to:

> [!div class="checklist"]
> * Download a sample dataset and prepare it for analysis.
> * Create environment variables for your resources endpoint and API key.
> * Use one of the following models: text-embedding-ada-002 (Version 2), text-embedding-3-large, text-embedding-3-small  models.
> * Use [cosine similarity](../concepts/understand-embeddings.md) to rank search results.

[!INCLUDE [Python](../includes/embeddings-python.md)]

Using this approach, you can use embeddings as a search mechanism across documents in a knowledge base. The user can then take the top search result and use it for their downstream task, which prompted their initial query.

## Clean up resources

If you created an Azure OpenAI resource solely for completing this tutorial and want to clean up and remove an Azure OpenAI resource, you'll need to delete your deployed models, and then delete the resource or associated resource group if it's dedicated to your test resource. Deleting the resource group also deletes any other resources associated with it.

- [Azure portal](../../../ai-services/multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../../ai-services/multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

Learn more about Azure OpenAI's models:
> [!div class="nextstepaction"]
> [Azure OpenAI models](../../foundry-models/concepts/models-sold-directly-by-azure.md)
* Store your embeddings and perform vector (similarity) search using your choice of Azure service:
  * [Azure AI Search](/azure/search/vector-search-overview)
  * [Azure SQL Database](/azure/azure-sql/database/ai-artificial-intelligence-intelligent-applications?view=azuresql&preserve-view=true#vector-search)
  * [Azure Cosmos DB for MongoDB vCore](/azure/cosmos-db/mongodb/vcore/vector-search)
  * [Azure SQL Database](/azure/azure-sql/database/ai-artificial-intelligence-intelligent-applications?view=azuresql&preserve-view=true#vector-search)
  * [Azure Cosmos DB for NoSQL](/azure/cosmos-db/vector-search)
  * [Azure Cosmos DB for PostgreSQL](/azure/cosmos-db/postgresql/howto-use-pgvector)
  * [Azure Cache for Redis](/azure/azure-cache-for-redis/cache-tutorial-vector-similarity)
