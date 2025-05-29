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
ms.date: 05/29/2025
---

# Python samples for Azure AI Search

Learn about the Python code samples that demonstrate the functionality and workflow of an Azure AI Search solution. These samples use the [**Azure AI Search client library**](/python/api/overview/azure/search-documents-readme) for the [**Azure SDK for Python**](/azure/developer/python/), which you can explore through the following links.

| Target | Link |
|--------|------|
| Package download | [pypi.org/project/azure-search-documents/](https://pypi.org/project/azure-search-documents/) |
| API reference | [azure-search-documents](/python/api/azure-search-documents)  |
| API test cases | [github.com/Azure/azure-sdk-for-python/tree/main/sdk/search/azure-search-documents/tests](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/search/azure-search-documents/tests) |
| Source code | [github.com/Azure/azure-sdk-for-python/tree/main/sdk/search/azure-search-documents](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/search/azure-search-documents)  |
| Change log | [https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) |

## SDK samples

Code samples from the Azure SDK development team demonstrate API usage. You can find these samples in [**azure-sdk-for-python/tree/main/sdk/search/azure-search-documents/samples**](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/search/azure-search-documents/samples) on GitHub.

## Doc samples

Code samples from the Azure AI Search team demonstrate features and workflows. Many of these samples are referenced in tutorials, quickstarts, and how-to articles. You can find these samples in [**Azure-Samples/azure-search-python-samples**](https://github.com/Azure-Samples/azure-search-python-samples) on GitHub.

| Samples | Article |
|---------|---------|
| [Tutorial-RAG](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/Tutorial-RAG) | Source code for the Python portion of [How to build a RAG solution using Azure AI Search](tutorial-rag-build-solution.md).|
| [Quickstart](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/Quickstart) | Source code for the Python portion of [Quickstart: Full text search using the Azure SDKs](search-get-started-text.md). This article covers the basic workflow for creating, loading, and querying a search index using sample data. |
| [Quickstart-RAG](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/Quickstart-RAG) | Source code for the Python portion of [Quickstart: Generative search (RAG) with grounding data from Azure AI Search](search-get-started-rag.md). |
| [Quickstart-Semantic-Search](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/Quickstart-Semantic-Search) | Source code for the Python portion of [Quickstart: Semantic ranking using the Azure SDKs](search-get-started-semantic.md). It shows the index schema and query request for invoking semantic ranker. |
| [bulk-insert](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/bulk-insert) | Source code for the Python example of how to [use the push APIs](search-how-to-load-search-index.md) to upload and index documents. |
| [azure-function-search](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/azure-function-search) | Source code for the Python example of an Azure function that sends queries to a search service. You can substitute this Python version of the `api` code used in the [Add search to web sites](tutorial-csharp-overview.md) C# sample. |

## Demos

[**azure-search-vector-samples**](https://github.com/Azure/azure-search-vector-samples/blob/main/README.md) on GitHub provides a comprehensive collection of samples for vector search scenarios, organized by scenario or technology.

[**azure-search-openai-demo**](https://github.com/Azure-Samples/azure-search-openai-demo/blob/main/README.md) is a ChatGPT-like experience over enterprise data with Azure OpenAI Python code showing how to use Azure AI Search with the large language models in Azure OpenAI. For background, see this [Tech Community blog post](https://techcommunity.microsoft.com/blog/azure-ai-services-blog/revolutionize-your-enterprise-data-with-chatgpt-next-gen-apps-w-azure-openai-and/3762087).

[**aisearch-openai-rag-audio**](https://github.com/Azure-Samples/aisearch-openai-rag-audio) is "voice to RAG". This sample demonstrates a simple architecture for voice-based generative AI applications that enables Azure AI Search RAG on top of the real-time audio API with full-duplex audio streaming from client devices, while securely handling access to both the model and retrieval system. Backend code is written in Python, while frontend code is written in JavaScript. For an introduction, watch this [video](https://www.youtube.com/watch?v=vXJka8xZ9Ko).

## Other samples

The following samples are also published by the Azure AI Search team but aren't referenced in documentation. Associated readme files provide usage instructions.

| Repository | Description |
|------------|-------------|
| [index-backup-and-restore.ipynb](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-python/code/utilities/index-backup-restore) | Uses the **azure.search.documents** library in the Azure SDK for Python to make a local copy of the retrievable fields of a search index and then push those fields to a new search index. |
| [resumable-index-backup-restore](https://github.com/Azure/azure-search-vector-samples/blob/main/demo-python/code/utilities/resumable-index-backup-restore/backup-and-restore.ipynb) | This sample accommodates larger indexes exceeding 100,000 documents.|

> [!TIP]
> Try the [Samples browser](/samples/browse/?languages=python&products=azure-cognitive-search) to search for Microsoft code samples in GitHub, filtered by product, service, and language.
