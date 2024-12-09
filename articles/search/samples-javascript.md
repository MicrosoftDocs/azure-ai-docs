---
title: JavaScript samples
titleSuffix: Azure AI Search
description: Find Azure AI Search demo JavaScript code samples that use the Azure .NET SDK for JavaScript.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.custom:
  - devx-track-dotnet
  - devx-track-js
  - ignite-2023
ms.topic: concept-article
ms.date: 10/18/2024
---

# JavaScript samples for Azure AI Search

Learn about the JavaScript code samples that demonstrate the functionality and workflow of an Azure AI Search solution. These samples use the [**Azure AI Search client library**](/javascript/api/overview/azure/search-documents-readme) for the [**Azure SDK for JavaScript**](/azure/developer/javascript/), which you can explore through the following links.

| Target | Link |
|--------|------|
| Package download | [www.npmjs.com/package/@azure/search-documents](https://www.npmjs.com/package/@azure/search-documents) |
| API reference | [@azure/search-documents](/javascript/api/@azure/search-documents/) |
| API test cases | [github.com/Azure/azure-sdk-for-js/tree/main/sdk/search/search-documents/test](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/search/search-documents/test) |
| Source code | [github.com/Azure/azure-sdk-for-js/tree/main/sdk/search/search-documents](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/search/search-documents) |
| Change log | [https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) |

## SDK samples

Code samples from the Azure SDK development team demonstrate API usage. You can find these samples in [**azure-sdk-for-js/tree/main/sdk/search/search-documents/samples**](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/search/search-documents/samples) on GitHub.

### JavaScript SDK samples

| Samples | Description |
|---------|-------------|
| [indexes](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/search/search-documents/samples/v11/javascript) | Demonstrates how to create, update, get, list, and delete [search indexes](search-what-is-an-index.md). This sample category also includes a service statistic sample. |
| [dataSourceConnections (for indexers)](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/samples/v11/javascript/dataSourceConnectionOperations.js) | Demonstrates how to create, update, get, list, and delete indexer data sources, required for indexer-based indexing of [supported Azure data sources](search-indexer-overview.md#supported-data-sources). |
| [indexers](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/search/search-documents/samples/v11/javascript) | Demonstrates how to create, update, get, list, reset, and delete [indexers](search-indexer-overview.md).|
| [skillSet](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/search/search-documents/samples/v11/javascript) | Demonstrates how to create, update, get, list, and delete [skillsets](cognitive-search-working-with-skillsets.md) that are attached indexers, and that perform AI-based enrichment during indexing. |
| [synonymMaps](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/search/search-documents/samples/v11/javascript) | Demonstrates how to create, update, get, list, and delete [synonym maps](search-synonyms.md). |
| [VectorSearch](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/samples/v12-beta/javascript/vectorSearch.js) | Demonstrates how to index vectors and send a [vector query](vector-search-how-to-query.md). |

### TypeScript samples

| Samples | Description |
|---------|-------------|
| [indexes](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/search/search-documents/samples/v11/typescript/src) | Demonstrates how to create, update, get, list, and delete [search indexes](search-what-is-an-index.md). This sample category also includes a service statistic sample. |
| [dataSourceConnections (for indexers)](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/samples/v11/typescript/src/dataSourceConnectionOperations.ts) | Demonstrates how to create, update, get, list, and delete indexer data sources, required for indexer-based indexing of [supported Azure data sources](search-indexer-overview.md#supported-data-sources). |
| [indexers](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/search/search-documents/samples/v11/typescript/src) | Demonstrates how to create, update, get, list, reset, and delete [indexers](search-indexer-overview.md).|
| [skillSet](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/samples/v11/typescript/src/skillSetOperations.ts) | Demonstrates how to create, update, get, list, and delete [skillsets](cognitive-search-working-with-skillsets.md) that are attached indexers, and that perform AI-based enrichment during indexing. |
| [synonymMaps](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/samples/v11/typescript/src/synonymMapOperations.ts) | Demonstrates how to create, update, get, list, and delete [synonym maps](search-synonyms.md). |
| [VectorSearch](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/samples/v12/typescript/src/vectorSearch.ts) | Demonstrates how to index vectors and send a [vector query](vector-search-how-to-query.md). |

## Doc samples

Code samples from the Azure AI Search team demonstrate features and workflows. Many of these samples are referenced in tutorials, quickstarts, and how-to articles. You can find these samples in [**Azure-Samples/azure-search-javascript-samples**](https://github.com/Azure-Samples/azure-search-javascript-samples) on GitHub.

| Samples | Article |
|---------|---------|
| [quickstart](https://github.com/Azure-Samples/azure-search-javascript-samples/tree/main/quickstart) | Source code for the JavaScript portion of [Quickstart: Full text search using the Azure SDKs](search-get-started-text.md). Covers the basic workflow for creating, loading, and querying a search index using sample data. |
| [bulk-insert](https://github.com/Azure-Samples/azure-search-javascript-samples/tree/main/bulk-insert) | Source code for the JavaScript example of how to [use the push APIs](search-how-to-load-search-index.md) to upload and index documents. |
| [azure-functions](https://github.com/Azure-Samples/azure-search-javascript-samples/tree/main/azure-function-search) | Source code for the JavaScript example of an Azure function that sends queries to a search service. You can substitute this JavaScript version of the `api` code used in the [Add search to web sites](tutorial-csharp-overview.md) C# sample. |
> [!TIP]
> Try the [Samples browser](/samples/browse/?languages=javascript&products=azure-cognitive-search) to search for Microsoft code samples in GitHub, filtered by product, service, and language.

## Other samples

The following samples are also published by the Azure AI Search team, but aren't referenced in documentation. Associated readme files provide usage instructions.

| Samples | Description |
|---------|-------------|
| [azure-search-vector-sample.js](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-javascript/readme.md) | Vector search sample using the Azure SDK for JavaScript |
