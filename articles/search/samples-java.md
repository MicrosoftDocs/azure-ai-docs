---
title: Java Samples
titleSuffix: Azure AI Search
description: Find Azure AI Search demo Java code samples that use the Azure .NET SDK for Java.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.custom:
  - devx-track-dotnet
  - devx-track-extended-java
  - ignite-2023
ms.topic: concept-article
ms.date: 01/13/2026
---

# Java samples for Azure AI Search

Learn about Java code samples that demonstrate the functionality and workflow of an Azure AI Search solution. These samples use the [Azure AI Search client library](/java/api/overview/azure/search-documents-readme) for the [Azure SDK for Java](/azure/developer/java/sdk), which you can explore through the following links.

| Target | Link |
|--|--|
| Package download | [search.maven.org/artifact/com.azure/azure-search-documents](https://search.maven.org/artifact/com.azure/azure-search-documents) |
| API reference | [com.azure.search.documents](/java/api/com.azure.search.documents)  |
| API test cases | [github.com/Azure/azure-sdk-for-java/tree/main/sdk/search/azure-search-documents/src/test](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/search/azure-search-documents/src/test) |
| Source code | [github.com/Azure/azure-sdk-for-java/tree/main/sdk/search/azure-search-documents](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/search/azure-search-documents)  |
| Change log | [github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) |

## SDK samples

Code samples from the Azure SDK development team demonstrate API usage. You can find these samples in [Azure/azure-sdk-for-java/tree/main/sdk/search/azure-search-documents/src/samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/search/azure-search-documents/src/samples) on GitHub.

| Sample | Description |
|--|--|
| [Index creation](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/src/samples/java/com/azure/search/documents/indexes/CreateIndexExample.java) | Create an [index](search-what-is-an-index.md). |
| [Indexer creation](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/src/samples/java/com/azure/search/documents/indexes/CreateIndexerExample.java) | Create an [indexer](search-indexer-overview.md). |
| [Data source creation](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/src/samples/java/com/azure/search/documents/indexes/DataSourceExample.java) | Create a data source connection, which is required for indexer-based indexing of [supported data sources](search-indexer-overview.md#supported-data-sources). |
| [Skillset creation](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/src/samples/java/com/azure/search/documents/indexes/CreateSkillsetExample.java) | Create a [skillset](cognitive-search-working-with-skillsets.md) that's attached to an indexer and perform AI-based enrichment during indexing. |
| [Synonym creation](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/src/samples/java/com/azure/search/documents/SynonymMapsCreateExample.java) | Create a [synonym map](search-synonyms.md).  |
| [Load documents](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/src/samples/java/com/azure/search/documents/IndexContentManagementExample.java) | Upload or merge documents into an index in a [data import](search-what-is-data-import.md) operation. |
| [Query syntax](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/src/samples/java/com/azure/search/documents/SearchAsyncWithFullyTypedDocumentsExample.java) | Send a [basic query](search-query-overview.md). |
| [Vector search](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/src/samples/java/com/azure/search/documents/VectorSearchExample.java) | Create a vector field and send a [vector query](vector-search-how-to-query.md). |

## Doc samples

Code samples from the Azure AI Search team demonstrate features and workflows. The following samples are referenced in tutorials, quickstarts, and how-to articles that explain the code in detail. You can find these samples in [Azure-Samples/azure-search-java-samples](https://github.com/Azure-Samples/azure-search-java-samples) on GitHub.

| Sample | Article | Description |
|--|--|--|
| [quickstart-keyword-search](https://github.com/Azure-Samples/azure-search-java-samples/tree/main/quickstart-keyword-search) | [Quickstart: Full-text search](search-get-started-text.md) | Create, load, and query a search index using sample data. |
| [quickstart-semantic-ranking](https://github.com/Azure-Samples/azure-search-java-samples/tree/main/quickstart-semantic-ranking) | [Quickstart: Semantic ranking](search-get-started-semantic.md) | Add semantic ranking to an index schema and run semantic queries. |
| [quickstart-vector-search](https://github.com/Azure-Samples/azure-search-java-samples/tree/main/quickstart-vector-search) | [Quickstart: Vector search](search-get-started-vector.md) | Index and query vector content. |

> [!TIP]
> Use the [samples browser](/samples/browse/?languages=java&products=azure-cognitive-search) to search for Microsoft code samples on GitHub. You can filter your search by product, service, and language.
