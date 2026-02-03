---
title: Python Samples
titleSuffix: Azure AI Search
description: Find Azure AI Search demo Python code samples that use the Azure .NET SDK for Python or REST.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - devx-track-dotnet
  - devx-track-python
  - ignite-2023
ms.topic: concept-article
ms.date: 01/13/2026
---

# Python samples for Azure AI Search

Learn about Python code samples that demonstrate the functionality and workflow of an Azure AI Search solution. These samples use the [Azure AI Search client library](/python/api/overview/azure/search-documents-readme) for the [Azure SDK for Python](/azure/developer/python/), which you can explore through the following links.

| Target | Link |
|--------|------|
| Package download | [pypi.org/project/azure-search-documents/](https://pypi.org/project/azure-search-documents/) |
| API reference | [azure-search-documents](/python/api/azure-search-documents)  |
| API test cases | [github.com/Azure/azure-sdk-for-python/tree/main/sdk/search/azure-search-documents/tests](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/search/azure-search-documents/tests) |
| Source code | [github.com/Azure/azure-sdk-for-python/tree/main/sdk/search/azure-search-documents](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/search/azure-search-documents)  |
| Change log | [github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) |

## SDK samples

Code samples from the Azure SDK development team demonstrate API usage. You can find these samples in [Azure/azure-sdk-for-python/tree/main/sdk/search/azure-search-documents/samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/search/azure-search-documents/samples) on GitHub.

## Doc samples

Code samples from the Azure AI Search team demonstrate features and workflows. The following samples are referenced in tutorials, quickstarts, and how-to articles. You can find these samples in [Azure-Samples/azure-search-python-samples](https://github.com/Azure-Samples/azure-search-python-samples) on GitHub.

| Sample | Article | Description |
|--|--|--|
| [Quickstart-Agentic-Retrieval](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/Quickstart-Agentic-Retrieval) | [Quickstart: Agentic retrieval](search-get-started-agentic-retrieval.md) | Integrate semantic ranking with LLM-powered query planning and answer generation. |
| [Quickstart-Keyword-Search](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/Quickstart-Keyword-Search) | [Quickstart: Full-text search](search-get-started-text.md) | Create, load, and query a search index using sample data. |
| [Quickstart-Semantic-Ranking](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/Quickstart-Semantic-Ranking) | [Quickstart: Semantic ranking](search-get-started-semantic.md) | Add semantic ranking to an index schema and run semantic queries. |
| [Quickstart-Vector-Search](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/Quickstart-Vector-Search) | [Quickstart: Vector search](search-get-started-vector.md) | Index and query vector content. |
| [agentic-retrieval-pipeline-example](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/agentic-retrieval-pipeline-example) | [Tutorial: Build an end-to-end agentic retrieval solution](agentic-retrieval-how-to-create-pipeline.md) | Unlike [Quickstart-Agentic-Retrieval](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/Quickstart-Agentic-Retrieval), this sample incorporates Foundry Agent Service for request orchestration. |

## Accelerators

An accelerator is an end-to-end solution that includes code and documentation you can adapt for your own implementation of a specific scenario.

| Sample | Description |
|--|--|
| [rag-experiment-accelerator](https://github.com/microsoft/rag-experiment-accelerator) | Conduct experiments and evaluations using Azure AI Search and the RAG pattern. This sample has code for loading multiple data sources, using various models, and creating various search indexes and queries. |

## Demos

A demo repo provides proof-of-concept source code for examples or scenarios shown in demonstrations. Unlike accelerators, demo solutions aren't designed for adaptation.

| Sample | Description |
|--|--|
| [azure-search-vector-samples](https://github.com/Azure/azure-search-vector-samples/blob/main) | Comprehensive collection of samples for vector search scenarios, organized by scenario or technology. |
| [azure-search-openai-demo](https://github.com/Azure-Samples/azure-search-openai-demo/blob/main) | ChatGPT-like experience over enterprise data with Azure OpenAI Python code showing how to use Azure AI Search with large language models in Azure OpenAI. For background, see this [blog post](https://techcommunity.microsoft.com/blog/azure-ai-services-blog/revolutionize-your-enterprise-data-with-chatgpt-next-gen-apps-w-azure-openai-and/3762087). |
| [aisearch-openai-rag-audio](https://github.com/Azure-Samples/aisearch-openai-rag-audio) | "Voice to RAG." This sample demonstrates a simple architecture for voice-based generative AI applications that enables Azure AI Search RAG on top of the real-time audio API with full-duplex audio streaming from client devices. It also securely handles access to both the model and the retrieval system. Backend code is written in Python, while frontend code is written in JavaScript. For an introduction, watch this [video](https://www.youtube.com/watch?v=vXJka8xZ9Ko). |

## Other samples

The following samples are also published by the Azure AI Search team but aren't referenced in documentation. Associated README files provide usage instructions.

| Sample | Description |
|--|--|
| [azure-search-classic-rag](https://github.com/Azure-Samples/azure-search-classic-rag/tree/main/quickstarts) | Single-shot RAG using the classic search engine as grounding data from Azure AI Search, with a chat completion model from Azure OpenAI. |
| [Quickstart-Document-Permissions-Pull-API](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/Quickstart-Document-Permissions-Pull-API) | Using an indexer "pull API" approach, flow access control lists from a data source to search results and apply permission filters that restrict access to authorized content. |
| [Quickstart-Document-Permissions-Push-API](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/Quickstart-Document-Permissions-Push-API) | Using the push APIs for indexing a JSON payload, flow embedded permission metadata to indexed documents and search results that are filtered based on user access to authorized content. |
| [azure-function-search](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/azure-function-search) | Use an Azure function to send queries to a search service. You can substitute this Python version for the `api` code used in [Add search to web sites with .NET](tutorial-csharp-overview.md). |
| [bulk-insert](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/bulk-insert) | [Use the push APIs](search-how-to-load-search-index.md) to upload and index documents. |
| [index-backup-and-restore.ipynb](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-python/code/utilities/index-backup-restore) | Make a local copy of retrievable fields in an index and push those fields to a new index. |
| [resumable-index-backup-restore](https://github.com/Azure/azure-search-vector-samples/blob/main/demo-python/code/utilities/resumable-index-backup-restore/backup-and-restore.ipynb) | Back up and restore larger indexes that exceed 100,000 documents. |

> [!TIP]
> Use the [samples browser](/samples/browse/?languages=python&products=azure-cognitive-search) to search for Microsoft code samples on GitHub. You can filter your search by product, service, and language.
