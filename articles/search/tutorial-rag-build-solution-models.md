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

In this tutorial, review your options for choosing embedding models for vectors and chat models for conversational search over your data. 

Key points:

- Model location requirement (Azure cloud).
- For chunking, use Text Split skill with overlap -- or --
- For semantic chunking, add Document Intelligence
- For embedding during indexing, use Azure OpenAI, Azure AI Vision, model catalog, custom skill with HTTP endpoint to external model
- For queries, same as above, but you're creating "vectorizers". It's doing the same thing.
- For chat, same location requirements and providers, except no Azure AI Vision. You specify a chat model in your query logic. Unlike embedding, you can swap this out to what they do.
- To do's for accessing models: permissions, endpoints. Include a "configure access" step.

<!-- 
The GPT-35-Turbo and GPT-4 models are optimized to work with inputs formatted as a conversation. 

The messages variable passes an array of dictionaries with different roles in the conversation delineated by system, user, and assistant. 

The system message can be used to prime the model by including context or instructions on how the model should respond. -->

## Next step

> [!div class="nextstepaction"]
> [Design an index](tutorial-rag-build-solution-index-schema.md)