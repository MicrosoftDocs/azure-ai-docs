---
title: .NET Samples
titleSuffix: Azure AI Search
description: Find Azure AI Search demo C# code samples that use the .NET client libraries.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - devx-track-dotnet
  - ignite-2023
ms.topic: concept-article
ms.date: 01/13/2026
---

# C# samples for Azure AI Search

Learn about C# code samples that demonstrate the functionality and workflow of an Azure AI Search solution. These samples use the [Azure AI Search client library](/dotnet/api/overview/azure/search) for the [Azure SDK for .NET](/dotnet/azure/), which you can explore through the following links.

| Target | Link |
|--|--|
| Package download | [nuget.org/packages/Azure.Search.Documents/](https://www.nuget.org/packages/Azure.Search.Documents/) |
| API reference | [Azure.Search.Documents](/dotnet/api/azure.search.documents)  |
| API test cases | [github.com/Azure/azure-sdk-for-net/tree/main/sdk/search/Azure.Search.Documents/tests](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/search/Azure.Search.Documents/tests) |
| Source code | [github.com/Azure/azure-sdk-for-net/tree/main/sdk/search/Azure.Search.Documents/src](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/search/Azure.Search.Documents/src)  |
| Change log | [github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) |

## SDK samples

Code samples from the Azure SDK development team demonstrate API usage. You can find these samples in [Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/samples](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/samples/) on GitHub.

| Sample | Description |
|--|--|
| [Hello world (synchronous)](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/samples/Sample01a_HelloWorld.md) | Create a client, authenticate, and handle errors using synchronous methods. |
| [Hello world (asynchronous)](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/samples/Sample01b_HelloWorldAsync.md) | Create a client, authenticate, and handle errors using asynchronous methods. |
| [Service-level operations](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/samples/Sample02_Service.md) | Get service statistics and create multiple search objects, including an index, indexer, data source, skillset, and synonym map. Finally, you query the index. |
| [Index operations](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/samples/Sample03_Index.md) | Get a count of documents stored in an index. |
| [FieldBuilderIgnore](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/samples/Sample04_FieldBuilderIgnore.md) | Use an attribute to work with unsupported data types. |
| [Indexing documents (push model)](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/samples/Sample05_IndexingDocuments.md) | Use the push model to index documents by sending a JSON payload to an index. |
| [Customer-managed encryption keys](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/samples/Sample06_EncryptedIndex.md) | Use a customer-managed encryption key to protect sensitive content. |
| [Vector search](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/samples/Sample07_VectorSearch.md) | Index a vector field and perform vector search. |
| [Semantic ranking](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/samples/Sample08_SemanticSearch.md) | Configure semantic ranker in an index and run semantic queries. |

## Doc samples

Code samples from the Azure AI Search team demonstrate features and workflows. The following samples are referenced in tutorials, quickstarts, and how-to articles that explain the code in detail. You can find these samples in [Azure-Samples/azure-search-dotnet-samples](https://github.com/Azure-Samples/azure-search-dotnet-samples) and [Azure-Samples/search-dotnet-getting-started](https://github.com/Azure-Samples/search-dotnet-getting-started/) on GitHub.

| Sample | Article | Description |
|--|--|--|
| [quickstart-agentic-retrieval](https://github.com/Azure-Samples/azure-search-dotnet-samples/tree/main/quickstart-agentic-retrieval) | [Quickstart: Agentic retrieval](search-get-started-agentic-retrieval.md) | Integrate semantic ranking with LLM-powered query planning and answer generation. |
| [quickstart-keyword-search](https://github.com/Azure-Samples/azure-search-dotnet-samples/tree/main/quickstart-keyword-search/AzureSearchQuickstart) | [Quickstart: Full-text search](search-get-started-text.md) | Create, load, and query an index using sample data. |
| [quickstart-semantic-ranking](https://github.com/Azure-Samples/azure-search-dotnet-samples/blob/main/quickstart-semantic-ranking/) | [Quickstart: Semantic ranking](search-get-started-semantic.md) | Add semantic ranking to an index schema and run semantic queries. |
| [quickstart-vector-search](https://github.com/Azure-Samples/azure-search-dotnet-samples/tree/main/quickstart-vector-search) | [Quickstart: Vector search](search-get-started-vector.md) | Index and query vector content. |
| [search-website](https://github.com/Azure-Samples/azure-search-static-web-app) | [Tutorial: Add search to web apps](tutorial-csharp-overview.md) | Build an end-to-end search app that uses the push API for bulk upload and a rich client for hosting the app and handling search requests. |
| [tutorial-ai-enrichment](https://github.com/Azure-Samples/azure-search-dotnet-samples/tree/main/tutorial-ai-enrichment) | [Tutorial: AI-generated searchable content from Azure blobs](tutorial-skillset.md) | Create a skillset that iterates over Azure blobs to extract information and infer structure. |
| [multiple-data-sources](https://github.com/Azure-Samples/azure-search-dotnet-scale/tree/main/multiple-data-sources) | [Tutorial: Index from multiple data sources](tutorial-multiple-data-sources.md) | Merge content from two data sources into one index. |
| [optimize-data-indexing](https://github.com/Azure-Samples/azure-search-dotnet-scale/tree/main/optimize-data-indexing) | [Tutorial: Optimize indexing with the push API](tutorial-optimize-indexing-push-api.md) | Use optimization techniques for pushing data into an index. |
| [DotNetHowTo](https://github.com/Azure-Samples/search-dotnet-getting-started/tree/master/DotNetHowTo) | [Use the .NET client library](search-howto-dotnet-sdk.md) | Create and manage multiple search objects while learning about the APIs. |
| [DotNetToIndexers](https://github.com/Azure-Samples/search-dotnet-getting-started/tree/master/DotNetHowToIndexers) | [Tutorial: Index Azure SQL data](search-indexer-tutorial.md) | Configure an Azure SQL indexer with a schedule, field mappings, and parameters. |
| [DotNetHowToEncryptionUsingCMK](https://github.com/Azure-Samples/search-dotnet-getting-started/tree/master/DotNetHowToEncryptionUsingCMK) | [Configure customer-managed keys for data encryption](search-security-manage-encryption-keys.md) | Create objects that are encrypted with a customer-managed key. |

## Demos

A demo repo provides proof-of-concept source code for examples or scenarios shown in demonstrations. Unlike accelerators, demo solutions aren't designed for adaptation.

| Sample | Description |
|--|--|
| [covid19search](https://github.com/liamca/covid19search) | Source code repo for the Azure AI Search-based Covid-19 search app. |
| [AzureSearch_JFK_Files](https://github.com/Microsoft/AzureSearch_JFK_Files) | Source code repo for the Azure AI Search-based JFK files solution. |

## Other samples

The following samples are also published by the Azure AI Search team but aren't referenced in documentation. Associated README files provide usage instructions.

| Sample | Description |
|--|--|
| [azure-search-classic-rag](https://github.com/Azure-Samples/azure-search-classic-rag/tree/main/quickstarts) | Single-shot RAG using the classic search engine as grounding data from Azure AI Search, with a chat completion model from Azure OpenAI. |
| [check-storage-usage](https://github.com/Azure-Samples/azure-search-dotnet-utilities/blob/main/check-storage-usage/README.md) | Check search service storage on a schedule using an Azure function. |
| [export-data](https://github.com/Azure-Samples/azure-search-dotnet-utilities/blob/main/export-data) | Partition and export a large index using a C# console app. |
| [index-backup-restore](https://github.com/Azure-Samples/azure-search-dotnet-utilities/blob/main/index-backup-restore) | Copy an index from one service to another, creating JSON files with the index schema and documents. |
| [data-lake-gen2-acl-indexing](https://github.com/Azure-Samples/azure-search-dotnet-utilities/blob/main/data-lake-gen2-acl-indexing) | Index Azure Data Lake Gen2 files and folders secured with Microsoft Entra ID and role-based access control. |
| [multiple-search-services](https://github.com/Azure-Samples/azure-search-dotnet-scale/tree/main/multiple-search-services) | Query multiple search services and combine results into a single page. |
| [search-aggregations](https://github.com/Azure-Samples/azure-search-dotnet-utilities/blob/main/search-aggregations) | Obtain and filter aggregations from an index. |
| [azure-search-power-skills](https://github.com/Azure-Samples/azure-search-power-skills/blob/main) | Incorporate consumable custom skills into your own solutions. |
| [DotNetVectorDemo](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-dotnet/DotNetVectorDemo) | Create, load, and query a vector index. |
| [DotNetIntegratedVectorizationDemo](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-dotnet/DotNetIntegratedVectorizationDemo) | Extend the vector workflow to include skills-based automation for data chunking and embedding. |

> [!TIP]
> Use the [samples browser](/samples/browse/?languages=csharp&products=azure-cognitive-search) to search for Microsoft code samples on GitHub. You can filter your search by product, service, and language.
