---
title: Python samples
titleSuffix: Azure AI Search
description: Find Azure AI Search demo Python code samples that use the Azure .NET SDK for Python or REST.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: cognitive-search
ms.custom:
  - devx-track-dotnet
  - devx-track-python
  - ignite-2023
ms.topic: conceptual
ms.date: 10/07/2024
---

# Python samples for Azure AI Search

Learn about the Python code samples that demonstrate the functionality and workflow of an Azure AI Search solution. These samples use the [**Azure AI Search client library**](/python/api/overview/azure/search-documents-readme) for the [**Azure SDK for Python**](/azure/developer/python/), which you can explore through the following links.

| Target | Link |
|--------|------|
| Package download | [pypi.org/project/azure-search-documents/](https://pypi.org/project/azure-search-documents/) |
| API reference | [azure-search-documents](/python/api/azure-search-documents)  |
| API test cases | [github.com/Azure/azure-sdk-for-python/tree/main/sdk/search/azure-search-documents/tests](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/search/azure-search-documents/tests) |
| Source code | [github.com/Azure/azure-sdk-for-python/tree/main/sdk/search/azure-search-documents](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/search/azure-search-documents)  |

## SDK samples

[**azure-sdk-for-python/tree/main/sdk/search/azure-search-documents/samples**](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/search/azure-search-documents/samples) on GitHub provides code samples from the Azure SDK development team, demonstrating API usage.

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

We also recommend [**azure-search-openai-demo**](https://github.com/Azure-Samples/azure-search-openai-demo/blob/main/README.md). This is a ChatGPT-like experience over enterprise data with Azure OpenAI Python code showing how to use Azure AI Search with the large language models in Azure OpenAI. For background, see this Tech Community blog post: [Revolutionize your Enterprise Data with ChatGPT](https://techcommunity.microsoft.com/t5/ai-applied-ai-blog/revolutionize-your-enterprise-data-with-chatgpt-next-gen-apps-w/ba-p/3762087). |

## Other samples

The following samples are also published by the Azure AI Search team, but aren't referenced in documentation. Associated readme files provide usage instructions.

| Repository | Description |
|------------|-------------|
| [aisearch-openai-rag-audio](https://github.com/Azure-Samples/aisearch-openai-rag-audio) | A simple architecture for voice-based generative AI applications that enables Azure AI Search RAG on top of the real-time audio API with full-duplex audio streaming from client devices, while securely handling access to both model and retrieval system. Backend code is written in Python. Frontend code is JavaScript. |
| [azure-search-backup-and-restore.ipynb](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-python/code/index-backup-restore) | Uses the **azure.search.documents** library in the Azure SDK for Python to make a local copy of the retrievable fields of a search index, and then push those fields to a new search index. |

> [!TIP]
> Try the [Samples browser](/samples/browse/?languages=python&products=azure-cognitive-search) to search for Microsoft code samples in GitHub, filtered by product, service, and language.
