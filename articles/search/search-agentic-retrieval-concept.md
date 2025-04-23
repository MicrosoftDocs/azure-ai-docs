---
title: Agentic retrieval
titleSuffix: Azure AI Search
description: Learn about agentic retrieval concepts, architecture, and use cases.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: concept-article
ms.date: 04/30/2025
---

# Agentic retrieval in Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

In Azure AI Search, *agentic retrieval* is a new parallel query processing architecture that generates multiple inputs from each query  and adds a chat completion model for query planning and execution. The *agentic* aspect is an evaluation and reasoning step in query processing: if the answers returned from the query engine aren't satisfactory, the system autonomously rewrites queries to improve the results.

Programmatically, agentic retrieval is supported through a new Agents object class in the newest preview data plane REST API, 2025-05-01-preview. A query response that's based on the Agents class is optimized for downstream consumption by other agents.

## Why use agentic retrieval

Agentic retrieval adds latency to query processing, but it's offset by these powerful capabilities:

+ Convert chat history into a subquery.
+ Rewrite original query into multiple subqueries using both synonym maps and LLM-powered paraphrasing.
+ Correct spelling mistakes.
+ Deconstruct a complex query, such as hybrid query with filters and semantic L2 ranking, into component parts.
+ Outputs a unified result as a single string. Alternatively, you can extract parts of the response for your solution.

Agentic retrieval invokes the entire query processing pipeline multiple times for each query request, but it does so in parallel, preserving the efficiency and performance necessary for knowledge-centric applications.

## Agentic retrieval architecture

TBD

## Availability and pricing

Billing is token-based.

Agentic retrieval is available in all supported regions and tiers, including the free tier. The free tier is limited to 1,000 free queries for full text search and 50 million free tokens for agentic search.

## How to get started

Choose any of these options for you next step.

<!-- + Watch this demo. -->
+ Quickstart. Learn the basic workflow using sample data and a prepared index and queries.

+ How-to guide for a closer look at building an agentic retrieval pipeline.

+ REST API reference, Agents.

+ Azure OpenAI Demo, updated to use agentic retrieval.

<!-- From the web

Agentic Retrieval-Augmented Generation (Agentic RAG) transcends traditional RAG systems by embedding autonomous AI agents into the RAG pipeline. These agents leverage agentic design patterns such as reflection, planning, tool use, and multi-agent collaboration to dynamically manage retrieval strategies, iteratively refine contextual understanding, and adapt workflows to meet complex task requirements. This integration enables Agentic RAG systems to deliver unparalleled flexibility, scalability, and context awareness across diverse applications -->



•Query Pipeline Recap: The query pipeline includes stages: Query Preprocessing (Query Rewriting, Vectorization, Text analysis), Ranking (Vector Search, Keyword Search, Fusion, Semantic Ranking), and Synthesis (Results for LLM, Extractive Answers, Contextualized Captions).

•RAG Query Challenges: RAG queries fail due to difficulties in retrieving relevant results, exact match searches, chatbot clarifications, and filter conditions. Examples and reasons for failures are discussed.

Agentic Retrieval Engine: The Agentic Retrieval Engine uses an AOAI model for query planning, producing sub-queries, and merging results. It supports explainability and debugging, and includes all existing search functionalities.

•Query Planning: Query planning involves processing conversation history with an AOAI Model (gpt-4o-mini) to classify queries into categories like 'Xbox sign-in troubleshooting' and 'Xbox PIN rejection troubleshooting'.

•Query Activity: Query activity involves planning and executing queries using the AOAI Model, producing sub-queries, and processing them through a pipeline for ranking and extracting references.

•Extracted Response for LLM: The process of extracting responses for troubleshooting guides involves a query pipeline, reference extraction, and merging results. A table lists extracted documents with reference IDs.

Extracted Response Example: Troubleshooting steps for Xbox sign-in issues include verifying email/password, checking internet, and updating software. For PIN issues, check sequence and reset if needed. Sources are cited.

•Agentic Retrieval vs Query Pipeline: Comparison of Agentic Retrieval and Query Pipeline: Agentic Retrieval supports multi-turn input, plans subqueries, and provides document references and activity logs, while Query Pipeline uses a single query and lists results.

•Cost Comparison: Cost comparison between Query Pipeline and Agentic Retrieval Engine: Query Pipeline has a uniform cost per query with a free tier of 1,000 queries, while Agentic Retrieval Engine has a uniform cost per token with a free tier of 50 million tokens.

Token Usage: Token usage in query planning and ranking involves AOAI input tokens generating subqueries, and ranking input tokens used in a query pipeline for document retrieval and semantic ranking.

•Roadmap: Potential features include Multiple Index Search, Iterative Search, Filtered Search, Query Planning Customization, Federation, Answer Generation, and Authority Checking.

•Features under each model: Comparison of features under traditional search model: BYOM Query planning and Reranking are listed, with a section for answers left blank