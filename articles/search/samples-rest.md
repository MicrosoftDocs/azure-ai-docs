---
title: REST Samples
titleSuffix: Azure AI Search
description: Find Azure AI Search demo REST code samples that use the Search or Management REST APIs.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: concept-article
ms.date: 01/13/2026
---

# REST samples for Azure AI Search

Learn about REST API samples that demonstrate the functionality and workflow of an Azure AI Search solution. These samples use the [Search Service REST APIs](/rest/api/searchservice).

REST is the definitive programming interface for Azure AI Search, offering a language-agnostic way to interact with the service. For this reason, most examples in our documentation use the REST APIs to demonstrate and explain important concepts.

You can use any client that supports HTTP calls. To learn how to formulate the HTTP request using Visual Studio Code with the REST Client extension, see the REST portion of [Quickstart: Full-text search](search-get-started-text.md).

## Doc samples

Code samples from the Azure AI Search team demonstrate features and workflows. The following samples are referenced in tutorials, quickstarts, and how-to articles. You can find these samples in [Azure-Samples/azure-search-rest-samples](https://github.com/Azure-Samples/azure-search-rest-samples) on GitHub.

| Sample | Article | Description |
|--|--|--|
| [quickstart-agentic-retrieval](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/Quickstart-agentic-retrieval) | [Quickstart: Agentic retrieval](search-get-started-agentic-retrieval.md) | Integrate semantic ranking with LLM-powered query planning and answer generation. |
| [quickstart-keyword-search](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/Quickstart-keyword-search) | [Quickstart: Full-text search](search-get-started-text.md) | Create, load, and query a search index using sample data. |
| [quickstart-semantic-ranking](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/Quickstart-semantic-ranking) | [Quickstart: Semantic ranking](search-get-started-semantic.md) | Add semantic ranking to an index schema and run semantic queries. |
| [quickstart-vectors](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/Quickstart-vectors) | [Quickstart: Vector search](search-get-started-vector.md) | Index and query vector content. |
| [acl](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/acl) | [Query-time ACL and RBAC enforcement](search-query-access-control-rbac-enforcement.md) | Implement query-time access control using role-based access control (RBAC) and access control lists (ACLs). |
| [custom-analyzers](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/custom-analyzers) | [Tutorial: Create a custom analyzer for phone numbers](tutorial-create-custom-analyzer.md) | Use an analyzer to preserve patterns and special characters in searchable content. |
| [debug-sessions](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/debug-sessions) | [Tutorial: Fix a skillset using Debug Sessions](cognitive-search-tutorial-debug-sessions.md) | Create search objects that you later debug in the Azure portal. |
| [index-json-blobs](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/index-json-blobs) | [Tutorial: Index JSON blobs from Azure Storage](search-semi-structured-data.md) | Create an indexer, data source, and index for nested JSON within a JSON array. Demonstrates the jsonArray parsing model and documentRoot parameters. |
| [knowledge-store](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/knowledge-store) | [Create a knowledge store using REST](knowledge-store-create-rest.md) | Populate a knowledge store for knowledge mining workflows. |
| [projections](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/projections) | [Define projections in a knowledge store](knowledge-store-projections-examples.md) | Specify the physical data structures in a knowledge store. |
| [skillset-tutorial](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/skillset-tutorial) | [Tutorial: AI-generated searchable content from Azure blobs](tutorial-skillset.md) | Create a skillset that iterates over Azure blobs to extract information and infer structure. |

## Other samples

The following samples are also published by the Azure AI Search team but aren't referenced in documentation. Associated README files provide usage instructions.

| Sample | Description |
|--|--|
| [azure-search-classic-rag](https://github.com/Azure-Samples/azure-search-classic-rag/tree/main/quickstarts) | Single-shot RAG using the classic search engine as grounding data from Azure AI Search, with a chat completion model from Azure OpenAI. |

> [!TIP]
> Use the [samples browser](/samples/browse/?expanded=azure&languages=http&products=azure-cognitive-search) to search for Microsoft code samples on GitHub. You can filter your search by product, service, and language.
