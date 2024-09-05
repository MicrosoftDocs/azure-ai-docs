---
title: Build a RAG solution
titleSuffix: Azure AI Search
description: Learn how to build a generative search (RAG) app using LLMs and your proprietary grounding data in Azure AI Search.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: cognitive-search
ms.topic: tutorial
ms.date: 09/12/2024

---

# How to build a RAG solution using Azure AI Search

This tutorial series demonstrates a RAG pattern in Azure AI Search. It covers the components built in Azure AI Search, dependencies, optimizations, and deployment tasks.

Sample data is a [collection of PDFs](LINK-TBD) that are uploaded to Azure Storage. Sample code can be found in [this Python notebook](LINK-TBD).

## In this series

- Choose your models for embeddings and chat

- Design an index for conversational search

- Design an indexing pipeline that loads, chunks, embeds, and ingests searchable content

- Retrieve searchable content using queries and a chat model

- Optimize for relevance

- Optimize for speed and lower costs

- Deploy and secure an app

We omitted a few aspects of a RAG pattern to reduce complexity:

- No chat history and context. Chat history must be stored and managed separately from your grounding data, which means extra steps and code. This tutorial assumes atomic question and answers from the LLM.

- No per-user user access controls over results (what we refer to as "security trimming"). For more information and resources, start with [Security trimming](search-security-trimming-for-azure-search.md) and make sure to review the links at the end of the article.

This series covers the fundamentals of RAG solution development. Once you understand the basics, continue with accelerators and other code samples that provide more abstraction or are otherwise better suited for production environments and more complex workloads.

## Why use Azure AI Search for RAG?

Chat models face constraints on the amount of data they can accept on a request. You should use Azure AI Search because the *quality* of content passed to an LLM can make or break a RAG solution. 

To deliver the highest quality inputs to a chat model, Azure AI Search provides a best-in-class search engine with AI integration and comprehensive relevance tuning. The search engine supports vector similarity search (multiple algorithms), keyword search, fuzzy search, geospatial search, and filters. You can build hybrid query requests that include all of these components, and you can control how much each query contributes to the overall request.

## Next step

> [!div class="nextstepaction"]
> [Choose models](tutorial-rag-build-solution-models.md)