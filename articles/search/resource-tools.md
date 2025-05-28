---
title: Productivity tools
titleSuffix: Azure AI Search
description: Use existing code samples or build your own tools for working with a search index in Azure AI Search.

author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: conceptual
ms.date: 02/25/2025
---

# Productivity tools and accelerators - Azure AI Search

Productivity tools are built by engineers at Microsoft, but aren't part of the Azure AI Search service and aren't under Service Level Agreement (SLA). These tools are provided as source code that you can download, modify, and build to create an app that helps you develop or maintain a search solution.

## Tools

| Tool name | Description | Source code |
|-----------|------------ |-------------|
| [Azure AI Search Lab](https://github.com/jelledruyts/azure-ai-search-lab) | Learning and experimentation lab to try out AI-enabled search scenarios in Azure. It provides a web application front-end which uses Azure AI Search and Azure OpenAI to execute searches with a variety of options - ranging from simple keyword search, to semantic ranking, vector and hybrid search, and using generative AI to answer search queries. | [https://github.com/jelledruyts/azure-ai-search-lab](https://github.com/jelledruyts/azure-ai-search-lab)  |
| [Back up and Restore (C#)](https://github.com/Azure-Samples/azure-search-dotnet-utilities/blob/main/index-backup-restore) | Download the retrievable fields of an index to your local device and then upload the index and its content to a new search service. | [https://github.com/Azure-Samples/azure-search-dotnet-utilities/blob/main/index-backup-restore](https://github.com/Azure-Samples/azure-search-dotnet-utilities/blob/main/index-backup-restore) |
| [Back up and Restore (Python)](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-python/code/utilities/index-backup-restore) | Download the retrievable fields of an index to your local device and then upload the index and its content to a new search service. | [https://github.com/Azure/azure-search-vector-samples/tree/main/demo-python/code/utilities/index-backup-restore](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-python/code/utilities/index-backup-restore) |
| [Performance testing solution](https://github.com/Azure-Samples/azure-search-performance-testing/blob/main/README.md) | This solution helps you load test Azure AI Search. It uses Apache JMeter as an open source load and performance testing tool and Terraform to dynamically provision and destroy the required infrastructure on Azure. | [https://github.com/Azure-Samples/azure-search-performance-testing](https://github.com/Azure-Samples/azure-search-performance-testing) |
| [Visual Studio Code extension](https://github.com/microsoft/vscode-azurecognitivesearch) | Although the extension is no longer available in the Visual Studio Code Marketplace, the code is open source. You can clone and modify the tool for your own use. | [https://github.com/microsoft/vscode-azurecognitivesearch](https://github.com/microsoft/vscode-azurecognitivesearch) |

## Accelerators

| Accelerator | Description | Source code |
|-----------|------------ |-------------|
| [Build your own copilot Solution Accelerator](https://github.com/microsoft/Build-your-own-copilot-Solution-Accelerator) | Code and docs to build a copilot for specific use cases.| [Client advisor](https://github.com/microsoft/Build-your-own-copilot-Solution-Accelerator/tree/main) <br>[Generic document generator](https://github.com/microsoft/Generic-Build-your-own-copilot-Solution-Accelerator) <br>[Research assistant](https://github.com/microsoft/Build-your-own-copilot-Solution-Accelerator/tree/main) |
| [Chat with your data solution accelerator](https://github.com/Azure-Samples/chat-with-your-data-solution-accelerator/blob/main/README.md) |  Code and docs to create interactive search solution in production environments.  | [https://github.com/Azure-Samples/chat-with-your-data-solution-accelerator](https://github.com/Azure-Samples/chat-with-your-data-solution-accelerator) |
| [Document knowledge mining solution accelerator](https://github.com/microsoft/Document-Knowledge-Mining-Solution-Accelerator/blob/main/README.md) |  Code and docs built on Azure OpenAI in Azure AI Foundry Models and Azure AI Document Intelligence to process and extract summaries, entities, and metadata from unstructured, multimodal documents and enable searching and chatting over this data.  | [https://github.com/microsoft/Document-Knowledge-Mining-Solution-Accelerator](https://github.com/microsoft/Document-Knowledge-Mining-Solution-Accelerator) |
| [Knowledge Mining accelerator](https://github.com/Azure-Samples/azure-search-knowledge-mining/blob/main/README.md) | Code and docs to jump start a knowledge store using your data. | [https://github.com/Azure-Samples/azure-search-knowledge-mining](https://github.com/Azure-Samples/azure-search-knowledge-mining) |
