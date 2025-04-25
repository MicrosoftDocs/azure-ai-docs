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

In Azure AI Search, *agentic retrieval* is a new parallel query processing architecture that generates multiple subqueries from a single retriever request, producing high quality grounding data for chat and generative AI solutions. 

Programmatically, agentic retrieval is supported through a new Agents object class in the newest preview data plane REST API, 2025-05-01-preview. An agent's retriever response is designed for downstream consumption by other agents and chat apps based on generative AI.

## Why use agentic retrieval

You should use agentic retrieval when you want to customize a chat experience with high quality inputs that include your proprietary data. The grounding data exists as indexed documents (plain text and vectors) in Azure AI Search. The custom experience is powered by a new agent capability in AI Search that adds query expansion powered by a chat completion model for query planning and execution. 

The *agentic* aspect is an evaluation and reasoning step in query planning processing that's performed by a large language model (LLM). The LLM is tasked with designing multiple subqueries based on the inputs and parameters you provide. All queries execute in parallel and return a rich response that can be used holistically or partially, depending on your scenario. 

Agentic retrieval adds latency to query processing, but it adds these capabilities:

+ Reads the existing chat history as an input to the retrieval pipeline.
+ Rewrites an original query into multiple subqueries using both synonym maps (optional) *and* LLM-generated paraphrasing.
+ Corrects spelling mistakes.
+ Deconstructs a complex query, such as hybrid query with filters, into component parts.
+ Executes all subqueries in parallel.
+ Outputs a unified result as a single string. Alternatively, you can extract parts of the response for your solution.

Agentic retrieval invokes the entire query processing pipeline multiple times for each query request, but it does so in parallel, preserving the efficiency and performance necessary for a satisfactory user experience.

## Agentic retrieval architecture

Agentic retrieval is designed for a conversational search experience that includes a chat completion model.

An important part of agentic retrieval is that an entire chat conversation can be included as inputs in subsequent queries, providing context and nuance for more relevant responses.

<!-- Insert architecture diagram here -->
Agentic retrieval has these components:

+ An index on Azure AI Search containing plain text, vector content, and image references.
+ An LLM that you deploy in Azure AI Foundry Model.
+ An agent that connects to a model, providing parameters and inputs to build a query plan. This agent is created using Azure AI Search APIs and exists on your search service.
+ A multithreaded query processing engine in Azure AI Search that executes on the LLM query plan and other parameters, returning a rich response that includes content and system data.

<!-- Insert multiquery pipeline diagram here -->
Agentic retrieval has these processes:

+ Request for agentic retrieval is initiated when your app passes in a query and conversation history to an agent.
+ Agent connects to an LLM for a query planning step, converting chat history into multiple subqueries.
+ All subqueries execute simultaneously on Azure AI Search and generate structured results and extracted references.
+ Results are merged.
+ Response is formulated and returned as a three part response consisting of a unified result, a reference array, and an activities array that enumerates all operations.

## Availability and pricing

Agentic retrieval is available in all supported regions and tiers, including the free tier. 

Agentic retrieval has a hybrid billing system:

+ Billing for search queries and semantic ranking remains intact. In US currency, semantic ranker is one dollar per thousand queries.

+ Billing for agentic retrieval is token-based. Because there are multiple subqueries, this workload is billed by tokens to stabilize costs because the number of queries varies dynamically based on inputs and parameters.

  | Aspect | Classic single-query pipeline | Agentic retrieval mulit-query pipeline |
  |--------|------------------------|----------------------------|
  | Unit | Query-based (1,000 queries) per unit of currency| Token-based (1 million tokens per unit of currency) |
  | Cost per unit | Uniform cost per query | Uniform cost per token |
  | Cost estimation | Estimate query count | Estimate token usage |
  | Free tier| 1,000 free queries | 50 million free tokens |

The model you assign to the agent is the one charged for token usage. For example, if you use gpt-4o, the token charge appears in the bill for gpt-4o.

Semantic ranker, which is a premium feature, is an integral part of agentic retrieval. You're charged on the Azure AI Search side for token inputs to the semantic ranking models.

## Development tasks

Development tasks on the Azure AI Search side include:

+ Create an agent on Azure AI Search that maps to a deployed model in Azure AI Foundry Model.
+ Call retrieve with a query, conversation, and override parameters.
+ Parse the response for parts you want to include in your chat application.

## How to get started

You must use the REST APIs or a prerelease Azure SDK page that provides the functionality. There's no Azure portal or Azure AI Foundry portal support at this time.

Choose any of these options for you next step.

<!-- + Watch this demo. -->
+ Quickstart. Learn the basic workflow using sample data and a prepared index and queries.

+ How-to guides for a closer look at building an agentic retrieval pipeline: [Create an agent](search-agentic-retrieval-how-to-create.md) and [Use an agent to retrieve data](search-agentic-retrieval-how-to-retrieve.md).

+ REST API reference, Agents.

+ Azure OpenAI Demo, updated to use agentic retrieval.

<!-- From the web

Agentic Retrieval-Augmented Generation (Agentic RAG) transcends traditional RAG systems by embedding autonomous AI agents into the RAG pipeline. These agents leverage agentic design patterns such as reflection, planning, tool use, and multi-agent collaboration to dynamically manage retrieval strategies, iteratively refine contextual understanding, and adapt workflows to meet complex task requirements. This integration enables Agentic RAG systems to deliver unparalleled flexibility, scalability, and context awareness across diverse applications -->

<!-- 
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

•Features under each model: Comparison of features under traditional search model: BYOM Query planning and Reranking are listed, with a section for answers left blank -->