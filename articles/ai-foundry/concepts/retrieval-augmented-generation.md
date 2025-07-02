---
title: Retrieval augmented generation in Azure AI Foundry portal
titleSuffix: Azure AI Foundry
description: This article introduces retrieval augmented generation for use in generative AI applications.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
ms.topic: concept-article
ms.date: 06/09/2025
ms.reviewer: sgilley
ms.author: sgilley
author: sdgilley
---

# Retrieval augmented generation and indexes

This article talks about the importance and need for Retrieval Augmented Generation (RAG) and index in generative AI.

## What is RAG?

Some basics first. Large language models (LLMs) like ChatGPT are trained on public internet data that was available at the point in time when they were trained. They can answer questions related to the data they were trained on. The public data might not be sufficient to meet all your needs. You might want questions answered based on your private data. Or, the public data might just be out of date. The solution to this problem is Retrieval Augmented Generation (RAG), a pattern used in AI that uses an LLM to generate answers with your own data.

## How does RAG work?

RAG is a pattern that uses your data with an LLM to generate answers specific to your data. When a user asks a question, the data store is searched based on user input. The user question is then combined with the matching results and sent to the LLM using a prompt (explicit instructions to an AI or machine learning model) to generate the desired answer. This process can be illustrated as follows.

:::image type="content" source="../media/index-retrieve/rag-pattern.png" alt-text="Screenshot of the RAG pattern." lightbox="../media/index-retrieve/rag-pattern.png":::


## What is an index and why do I need it?

RAG uses your data to generate answers to the user question. For RAG to work well, we need to find a way to search and send your data in an easy and cost efficient manner to the LLMs. An index solves this problem. An index is a data store that allows you to search data efficiently. This index is very useful in RAG. An index can be optimized for LLMs by creating vectors (text data converted to number sequences using an embedding model). A good index usually has efficient search capabilities like keyword searches, semantic searches, vector searches, or a combination of these features. This optimized RAG pattern can be illustrated as follows.

:::image type="content" source="../media/index-retrieve/rag-pattern-with-index.png" alt-text="Screenshot of the RAG pattern with index." lightbox="../media/index-retrieve/rag-pattern-with-index.png":::

Azure AI provides an index asset to use with RAG pattern. The index asset contains important information such as:

* Where is your index stored?
* How to access your index?
* What are the modes in which your index can be searched?
* Does your index have vectors?
* What is the embedding model used for vectors?

The Azure AI index uses [Azure AI Search](/azure/search/search-what-is-azure-search) as the primary and recommended index store. Azure AI Search is an Azure resource that supports information retrieval over your vector and textual data stored in search indexes.

## Next steps

- [Create a vector index](../how-to/index-add.md)
