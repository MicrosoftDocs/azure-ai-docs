---
title: What is custom question answering?
titleSuffix: Foundry Tools
description: Custom question answering is a cloud-based NLP service that creates conversational layers over your data to deliver accurate answers for natural language queries.
ms.service: azure-ai-language
author: laujan
ms.author: lajanuar
recommendations: false
ms.topic: overview
ms.date: 12/10/2025 
keywords: "low code chat bots, multi-turn conversations"
ms.custom: language-service-question-answering
---
# What is custom question answering?

Custom question answering (CQA) is a cloud-based Natural Language Processing (NLP) service that creates conversational AI applications over your data. Build knowledge bases from FAQs, manuals, and documents to deliver accurate answers through chat bots, virtual assistants, and interactive interfaces.

## Key capabilities

Custom question answering provides enterprise-grade features for building and maintaining conversational AI solutions:

* **Knowledge base creation** - Import content from URLs, files, and documents. The service automatically extracts question-answer pairs from structured and semi-structured sources.
* **Multi-turn conversations** - Create guided conversation flows with follow-up prompts that navigate users through complex information.
* **Metadata filtering** - Tag answers by content type, domain, or freshness to deliver contextually relevant responses.
* **Active learning** - Improve answer quality based on real-world usage patterns and user queries.
* **Deep learning ranking** - Multi-stage ranking architecture combines Azure AI Search with NLP reranking for optimal answer selection.

## Architecture and workflow

The service follows a structured pipeline from project creation to production deployment:

1. **Create a project** - Build a knowledge base by importing content sources or manually adding question-answer pairs in [Microsoft Foundry (classic)](https://ai.azure.com/).
1. **Test and refine** - Use the test interface to validate responses and adjust answer quality before deployment.
1. **Deploy** - Publish your project to create a REST API endpoint accessible by client applications.
1. **Integrate** - Client applications send queries and receive JSON responses with answers, confidence scores, and follow-up prompts.

## Development options

Choose from multiple development approaches based on your technical requirements and expertise:

* **Microsoft Foundry (classic)** - Low-code authoring with automatic QA extraction, markdown support, and [chit-chat](./how-to/chit-chat.md) integration. Deploy directly to [Azure Bot Service](https://azure.microsoft.com/services/bot-service/).
* **REST APIs** - Programmatic access for custom integrations and automated workflows. See the [Azure Language REST API reference](/rest/api/language/) for endpoint documentation.
* **Client libraries** - SDK packages for .NET and Python enable programmatic project management and query integration:
  * [.NET (C#) packages](https://www.nuget.org/packages/Azure.AI.Language.QuestionAnswering/) - Runtime and authoring SDKs for C# applications
  * [Python packages](https://pypi.org/project/azure-ai-language-questionanswering/) - Runtime and authoring SDKs for Python applications

## Next steps

* [Quickstart: Create and deploy a CQA project](./quickstart/sdk.md)
* [Manage knowledge bases](./how-to/manage-knowledge-base.md)
* [Configure multi-turn conversations](./tutorials/guided-conversations.md)
