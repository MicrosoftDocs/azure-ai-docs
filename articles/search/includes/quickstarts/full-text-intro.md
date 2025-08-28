---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 06/26/2025
---

In this quickstart, you use the Azure.Search.Documents client library to create, load, and query a search index with sample data for [full-text search](../../search-lucene-query-architecture.md). Full-text search uses Apache Lucene for indexing and queries and the BM25 ranking algorithm for scoring results.

This quickstart uses fictional hotel data from the [azure-search-sample-data](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/hotels/hotel-json-documents) repo to populate the index.