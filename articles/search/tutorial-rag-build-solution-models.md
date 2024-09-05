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

- Model location requirements (Azure cloud).
- For chunking, use Text Split skill with overlap,
- For semantic chunking, add Document Intelligence
- For embedding during indexing, use Azure OpenAI, Azure AI Vision, model catalog, custom skill with HTTP endpoint to external model
- For queries, same as above, but you're creating "vectorizers"
- For chat, same location requirements and providers, except for Azure AI Vision. You specify a chat model in your query logic.

<!-- 
The GPT-35-Turbo and GPT-4 models are optimized to work with inputs formatted as a conversation. 

The messages variable passes an array of dictionaries with different roles in the conversation delineated by system, user, and assistant. 

The system message can be used to prime the model by including context or instructions on how the model should respond. -->


## Next step

> [!div class="nextstepaction"]
> TBD