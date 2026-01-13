---
title: Create a Blob Knowledge Source for Agentic Retrieval
titleSuffix: Azure AI Search
description: A blob knowledge source specifies a blob container that you want to read from. It also includes models and properties for creating an indexer, data source, skillset, and index used for agentic retrieval workloads.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 11/19/2025
zone_pivot_groups: agentic-retrieval-pivots
---

# Create a blob knowledge source from Azure Blob Storage and ADLS Gen2

::: zone pivot="csharp"
[!INCLUDE [C#](includes/how-tos/agentic-knowledge-source-how-to-blob-csharp.md)]
::: zone-end

::: zone pivot="python"
[!INCLUDE [Python](includes/how-tos/agentic-knowledge-source-how-to-blob-python.md)]
::: zone-end

::: zone pivot="rest"
[!INCLUDE [REST](includes/how-tos/agentic-knowledge-source-how-to-blob-rest.md)]
::: zone-end

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [Azure AI Search blob knowledge source Python sample](https://github.com/Azure/azure-search-vector-samples/blob/main/demo-python/code/knowledge/blob-knowledge-source.ipynb)
+ [Agentic RAG: Build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)
+ [Azure OpenAI demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)