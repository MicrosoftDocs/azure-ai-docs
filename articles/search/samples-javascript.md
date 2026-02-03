---
title: JavaScript Samples
titleSuffix: Azure AI Search
description: Find Azure AI Search demo JavaScript code samples that use the Azure .NET SDK for JavaScript.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - devx-track-dotnet
  - devx-track-js
  - ignite-2023
ms.topic: concept-article
ms.date: 01/13/2026
---

# JavaScript samples for Azure AI Search

Learn about JavaScript code samples that demonstrate the functionality and workflow of an Azure AI Search solution. These samples use the [Azure AI Search client library](/javascript/api/overview/azure/search-documents-readme) for the [Azure SDK for JavaScript](/azure/developer/javascript/), which you can explore through the following links.

| Target | Link |
|--|--|
| Package download | [www.npmjs.com/package/@azure/search-documents](https://www.npmjs.com/package/@azure/search-documents) |
| API reference | [@azure/search-documents](/javascript/api/@azure/search-documents/) |
| API test cases | [github.com/Azure/azure-sdk-for-js/tree/main/sdk/search/search-documents/test](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/search/search-documents/test) |
| Source code | [github.com/Azure/azure-sdk-for-js/tree/main/sdk/search/search-documents](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/search/search-documents) |
| Change log | [github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) |

## SDK samples

Code samples from the Azure SDK development team demonstrate API usage. You can find these samples in [Azure/azure-sdk-for-js/tree/main/sdk/search/search-documents/samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/search/search-documents/samples) on GitHub.

### JavaScript samples

| Sample | Description |
|--|--|
| [indexes](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/search/search-documents/samples/v11/javascript) | Create, update, get, list, and delete [indexes](search-what-is-an-index.md). This sample category also includes a service statistic sample. |
| [indexers](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/search/search-documents/samples/v11/javascript) | Create, update, get, list, reset, and delete [indexers](search-indexer-overview.md). |
| [dataSourceConnections (for indexers)](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/samples/v11/javascript/dataSourceConnectionOperations.js) | Create, update, get, list, and delete data source connections, which are required for indexer-based indexing of [supported data sources](search-indexer-overview.md#supported-data-sources). |
| [skillsets](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/search/search-documents/samples/v11/javascript) | Create, update, get, list, and delete [skillsets](cognitive-search-working-with-skillsets.md) that are attached to indexers and perform AI-based enrichment during indexing. |
| [synonymMaps](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/search/search-documents/samples/v11/javascript) | Create, update, get, list, and delete [synonym maps](search-synonyms.md). |
| [vectorSearch](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/samples/v12-beta/javascript/vectorSearch.js) | Index vectors and send a [vector query](vector-search-how-to-query.md). |

### TypeScript samples

| Sample | Description |
|--|--|
| [indexes](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/search/search-documents/samples/v11/typescript/src) | Create, update, get, list, and delete [indexes](search-what-is-an-index.md). This sample category also includes a service statistic sample. |
| [indexers](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/search/search-documents/samples/v11/typescript/src) | Create, update, get, list, reset, and delete [indexers](search-indexer-overview.md). |
| [dataSourceConnections (for indexers)](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/samples/v11/typescript/src/dataSourceConnectionOperations.ts) | Create, update, get, list, and delete data source connections, which are required for indexer-based indexing of [supported data sources](search-indexer-overview.md#supported-data-sources). |
| [skillsets](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/samples/v11/typescript/src/skillSetOperations.ts) | Create, update, get, list, and delete [skillsets](cognitive-search-working-with-skillsets.md) that are attached to indexers and perform AI-based enrichment during indexing. |
| [synonymMaps](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/samples/v11/typescript/src/synonymMapOperations.ts) | Create, update, get, list, and delete [synonym maps](search-synonyms.md). |
| [vectorSearch](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/samples/v12/typescript/src/vectorSearch.ts) | Create, update, get, list, and delete [vector search](vector-search-how-to-query.md). |

## Doc samples

Code samples from the Azure AI Search team demonstrate features and workflows. The following samples are referenced in tutorials, quickstarts, and how-to articles. You can find these samples in [Azure-Samples/azure-search-javascript-samples](https://github.com/Azure-Samples/azure-search-javascript-samples) on GitHub.

### JavaScript samples

| Sample | Article | Description |
|--|--|--|
| [quickstart-keyword-search](https://github.com/Azure-Samples/azure-search-javascript-samples/tree/main/quickstart-keyword-search) | [Quickstart: Full-text search](search-get-started-text.md) | Create, load, and query a search index using sample data. |
| [quickstart-semantic-ranking-js](https://github.com/Azure-Samples/azure-search-javascript-samples/tree/main/quickstart-semantic-ranking-js) | [Quickstart: Semantic ranking](search-get-started-semantic.md) | Add semantic ranking to an index schema and run semantic queries. |
| [quickstart-vector-js](https://github.com/Azure-Samples/azure-search-javascript-samples/tree/main/quickstart-vector-js) | [Quickstart: Vector search](search-get-started-vector.md) | Index and query vector content. |

### TypeScript samples

| Sample | Article | Description |
|--|--|--|
| [quickstart-semantic-ranking-ts](https://github.com/Azure-Samples/azure-search-javascript-samples/tree/main/quickstart-semantic-ranking-ts) | [Quickstart: Semantic ranking](search-get-started-semantic.md) | Add semantic ranking to an index schema and run semantic queries. |
| [quickstart-vector-ts](https://github.com/Azure-Samples/azure-search-javascript-samples/tree/main/quickstart-vector-ts) | [Quickstart: Vector search](search-get-started-vector.md) | Index and query vector content. |

## Other samples

The following samples are also published by the Azure AI Search team but aren't referenced in documentation. Associated README files provide usage instructions.

| Sample | Description |
|--|--|
| [azure-search-classic-rag](https://github.com/Azure-Samples/azure-search-classic-rag/tree/main/quickstarts) | Single-shot RAG using the classic search engine as grounding data from Azure AI Search, with a chat completion model from Azure OpenAI. |
| [azure-search-vector-sample.js](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-javascript/readme.md) | JavaScript example of how to perform vector search. |
| [azure-function-search](https://github.com/Azure-Samples/azure-search-javascript-samples/tree/main/azure-function-search) | JavaScript example of an Azure function that sends queries to a search service. You can substitute this JavaScript version for the `api` code used in [Add search to web sites with .NET](tutorial-csharp-overview.md). |
| [bulk-insert](https://github.com/Azure-Samples/azure-search-javascript-samples/tree/main/bulk-insert) | JavaScript example of how to [use the push APIs](search-how-to-load-search-index.md) to upload and index documents. |

> [!TIP]
> Use the [samples browser](/samples/browse/?languages=javascript&products=azure-cognitive-search) to search for Microsoft code samples on GitHub. You can filter your search by product, service, and language.
