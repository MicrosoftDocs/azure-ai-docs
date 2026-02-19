---
title: Productivity Tools
titleSuffix: Azure AI Search
description: Use existing code samples or build your own tools for working with a search index in Azure AI Search.
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: concept-article
ms.date: 07/28/2025
ms.update-cycle: 365-days
---

# Productivity tools and accelerators for Azure AI Search

Microsoft engineers build productivity tools that aren't part of the Azure AI Search service and aren't covered by service-level agreements (SLAs). You can download, modify, and build these tools to create an app that helps you develop or maintain a search solution.

## Accelerators

| Accelerator | Description |
|--|--|
| [RAG Experiment Accelerator](https://github.com/microsoft/rag-experiment-accelerator) | Conduct experiments and evaluations using Azure AI Search and the RAG pattern. This accelerator has code for loading multiple data sources, using a variety of models, and creating a variety of search indexes and queries. |
| [Build your own copilot solution accelerator](https://github.com/microsoft/Build-your-own-copilot-Solution-Accelerator) | Code and docs to build a copilot for specific use cases. |
| [Chat with your data solution accelerator](https://github.com/Azure-Samples/chat-with-your-data-solution-accelerator/blob/main/README.md) | Code and docs to create interactive search solution in production environments. |
| [Document knowledge mining solution accelerator](https://github.com/microsoft/Document-Knowledge-Mining-Solution-Accelerator/blob/main/README.md) | Code and docs built on Azure OpenAI in Foundry Models and Azure Document Intelligence in Foundry Tools. It processes and extracts summaries, entities, and metadata from unstructured, multimodal documents to enable searching and chatting over this data. |

## Tools

| Tool name | Description |
|--|--|
| [Azure AI Search Lab](https://github.com/jelledruyts/azure-ai-search-lab) | Learning and experimentation lab to try out AI-enabled search scenarios in Azure. It provides a web application front end that uses Azure AI Search and Azure OpenAI to execute searches with various options. These options range from simple keyword search to semantic ranking, vector and hybrid search, and using generative AI to answer search queries. |
| [Back up and restore (C#)](https://github.com/Azure-Samples/azure-search-dotnet-utilities/blob/main/index-backup-restore) | Download the retrievable fields of an index to your local device and then upload the index and its content to a new search service. |
| [Back up and restore (Python)](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-python/code/utilities/index-backup-restore) | Download the retrievable fields of an index to your local device and then upload the index and its content to a new search service. |
| [Performance testing solution](https://github.com/Azure-Samples/azure-search-performance-testing/blob/main/README.md) | This solution helps you load test Azure AI Search. It uses Apache JMeter as an open source load and performance testing tool and Terraform to dynamically provision and destroy the required infrastructure on Azure. |
| [Visual Studio Code extension](https://github.com/microsoft/vscode-azurecognitivesearch) | Although the extension is no longer available on the Visual Studio Code Marketplace, the code is open source. You can clone and modify the tool for your own use. |

