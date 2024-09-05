---
title: 'RAG tutorial: Set up models'
titleSuffix: Azure AI Search
description: Set up an embedding model and chat model for generative search (RAG).

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: cognitive-search
ms.topic: tutorial
ms.date: 09/12/2024

---

# Choose embedding and chat models (RAG tutorial - Azure AI Search)

A RAG solution built on Azure AI Search takes a dependency on embedding models for vectorization, and chat models for conversational search over your data. 

In this tutorial, review your options for choosing embedding and chat models for Learn how to set up connections so that Azure AI Search can connect securely during indexing and at query time for generative AI responses and text-to-vector conversions of query strings.

Objective:

- Identify an embedding model and chat model for your RAG workflow.

Key points:

- Built-in integration for models hosted in the Azure cloud.
- For chunking, use the native Text Split skill with overlapping text -- or -- for semantic chunking, use Document Intelligence.
- For embedding during indexing, use a skill that points to Azure OpenAI, Azure AI Vision, or the model catalog. Alternatively, use custom skill with HTTP endpoint to external model.
- For queries, same embedding models as above, but you're wrapping it in a "vectorizer" instead of a "skill".
- Use the same embedding model for indexing and text-to-vector queries. If you want to try a different model, it's a rebuild. An indexer pipeline like the one used in this tutorial makes this step easy.
- For chat, same location requirements and providers, except no Azure AI Vision. You specify a chat model in your query logic. Unlike embedding, you can swap these around at query time to see what they do.

Tasks:

- H2: Identify the models for which we have skills/vectorizers and provide locations (model catalog, Azure OpenAI, etc). Crosslink to model deployment instructions. Include steps for getting endpoints, model version, deployment name, REST API version.
- H2: How to use other models (create a custom skill, create a custom vectorizer).
- H2: How to configure access. Set up an Azure AI Search managed identity, give it permissions on Azure-hosted models.

<!-- 
The GPT-35-Turbo and GPT-4 models are optimized to work with inputs formatted as a conversation. 

The messages variable passes an array of dictionaries with different roles in the conversation delineated by system, user, and assistant. 

The system message can be used to prime the model by including context or instructions on how the model should respond. -->

## Next step

> [!div class="nextstepaction"]
> [Design an index](tutorial-rag-build-solution-index-schema.md)