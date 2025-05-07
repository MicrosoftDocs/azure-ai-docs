---
title: Agentic retrieval
titleSuffix: Azure AI Search
description: Learn about agentic retrieval concepts, architecture, and use cases.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: concept-article
ms.custom: references_regions
ms.date: 05/06/2025
---

# Agentic retrieval in Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

In Azure AI Search, *agentic retrieval* is a new parallel query processing architecture that uses conversational language models to generate multiple subqueries for a single retrieval request, incorporating conversation history and semantic ranking to produce high quality grounding data for custom chat and generative AI solutions.

Programmatically, agentic retrieval is supported through a new Agents object in the newest preview data plane REST API 2025-05-01-preview and in Azure SDK prerelease packages that provide the feature. An agent's retrieval response is designed for downstream consumption by other agents and chat apps that provide natural language user interactions.

## Why use agentic retrieval

You should use agentic retrieval when you want to customize a chat experience with high quality inputs that include your proprietary data.

The *agentic* aspect is a reasoning step in query planning processing that's performed by a supported large language model (LLM) that you provide. The LLM is tasked with designing multiple subqueries based on: user questions, chat history, and parameters on the request. The subqueries target your indexed documents (plain text and vectors) in Azure AI Search.

The *retrieval* component is the ability to run subqueries simultaneously, merge results, semantically rank results, and return a 3-part response that includes grounding data for the next conversation turn, reference data so that you can inspect the source content, and an activity plan that shows query execution steps.

<!-- Queries target a new retrieval pipeline in AI Search supports parallel processing, expanding the scope of single request to include subqueries Query execution runs on your search service, utilizing the best and most effective relevance enhancements in Azure AI Search, including semantic ranker. Output is intended for integration into custom chat solutions, particularly those patterned after an agent-to-agent approach. -->

Agentic retrieval adds latency to query processing, but it makes up for it by adding these capabilities:

+ Reads in chat history as an input to the retrieval pipeline.
+ Rewrites an original query into multiple subqueries using both synonym maps (optional) *and* LLM-generated paraphrasing.
+ Corrects spelling mistakes.
+ Deconstructs a complex query that contains multiple "asks" into component parts (for example, "find me a hotel near the beach, with airport transportation, and that's within walking distance of vegetarian restaurants")
+ Executes all subqueries in simultaneously.
+ Outputs a unified result as a single string. Alternatively, you can extract parts of the response for your solution. Metadata about query execution and reference data is included in the response.

Agentic retrieval invokes the entire query processing pipeline multiple times for each query request, but it does so in parallel, preserving the efficiency and performance necessary for a reasonable user experience.

> [!NOTE]
> Including an LLM in query planning adds latency to a query pipeline. You can mitigate by using faster models such as gpt-4o-mini and summarizing the message threads, but you should expect longer query times with this pipeline.

## Agentic retrieval architecture

Agentic retrieval is designed for a conversational search experience that includes an LLM. An important part of agentic retrieval is that an entire chat conversation can be included as inputs in subsequent queries, providing context and nuance for more relevant responses.

<!-- Insert architecture diagram here -->
Agentic retrieval has these components:

| Component | Resource | Usage |
|-----------|----------|-------|
| LLM (gpt-4o and gpt-4.1 series) | Azure OpenAI | Formulates subqueries for the query plan. Potentially used to provide an answer based on the grounding data, but you can use any supported model for this step. |
 Search index | Azure AI Search | Contains plain text and vector content, a semantic configuration, other elements as needed. |
| Agent | Azure AI Search | Connects to your model, providing parameters and inputs to build a query plan. |
| Retrieval engine | Azure AI Search | Executes on the LLM-generated query plan and other parameters, returning a rich response that includes content and query plan metadata. Queries are keyword, vector, and hybrid. Results are merged and ranked. |
| Semantic ranker | Azure AI Search | Provides L2 reranking, promoting the most relevant matches. Semantic ranker is required for agentic retrieval. |

Your solution should include a tool or app that drives the pipeline. An agentic retrieval pipeline concludes with the response object that provides grounding data. Your solution should handle the response, including passing it to an LLM to generate an answer, which you render inline in the user conversation. For more information about this step, see [Build an agent-to-agent retrieval solution](search-agentic-retrieval-how-to-pipeline.md).

<!-- Insert multiquery pipeline diagram here -->
Agentic retrieval has these processes:

+ Requests for agentic retrieval are initiated by calls to an agent on Azure AI Search.
+ Agents connect to an LLM and provides conversation history as an input (how much history is configurable by the number of messages you provide).
+ LLMs look at the conversation and determine whether to break it up into subqueries. The number of subqueries depends on what the LLM decides, and also whether `maxDocsForReranker` parameter is higher than 50. A new subquery is defined for each 50 document batch sent to the semantic ranker.
+ Subqueries execute simultaneously on Azure AI Search and generate structured results and extracted references.
+ Results are merged and ranked.
+ Agent responses are formulated and returned as a three part response consisting of a unified result (a long string), a reference array, and an activities array that enumerates all operations.

Query execution and any optimizations that occur during query execution are determined by your search index. Namely, your semantic configuration, but also optionally: scoring profiles, synonym maps, analyzers and normalizers if you add filters.

## Availability and pricing

Agentic retrieval is available in [all regions that provide semantic ranker](search-region-support.md), on all tiers except the free tier.

Agentic retrieval billing has two parts:

+ Billing for query planning is pay-as-you-go in Azure OpenAI. It's token based for both input and output tokens. The model you assign to the agent is the one charged for token usage. For example, if you use gpt-4o, the token charge appears in the bill for gpt-4o.

+ Billing for semantic ranking during query execution. Billing is suspended during the initial roll-out phase, from May 19 through June 30, 2025. On July 1, billing will be token based and is pay-as-you-go on the Azure AI Search side through the semantic ranker. Semantic ranker, which is a premium billable feature, is an integral part of agentic retrieval. You're charged on the Azure AI Search side for token inputs to the semantic ranking models. 

Semantic ranking is performed for every subquery in the plan. Semantic ranking charges are based on the number of tokens returned by each subquery.

  | Aspect | Classic single-query pipeline | Agentic retrieval multi-query pipeline |
  |--------|------------------------|----------------------------|
  | Unit | Query-based (1,000 queries) per unit of currency| Token-based (1 million tokens per unit of currency) |
  | Cost per unit | Uniform cost per query | Uniform cost per token |
  | Cost estimation | Estimate query count | Estimate token usage |
  | Free tier| 1,000 free queries | 50 million free tokens |

> [!NOTE]
> Existing semantic ranker billing is unchanged if you're using it outside of agentic retrieval. For pricing without agentic retrieval, see the [Azure AI Search pricing page](https://azure.microsoft.com/pricing/details/search/).

### Example: Estimate costs

There are two billing models in effect for agentic retrieval. Billing from Azure AI Search for semantic ranking (query execution) and billing from Azure OpenAI (query planning).

The prices shown in this article are hypothetical. They're used to illustrate the estimation process. Your costs could be lower. For the actual price of transactions, see [Azure OpenAI pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/#pricing). For query execution, there's no charge for semantic ranking for agentic retrieval in the initial public preview.

#### Estimated billing costs for query planning

To estimate the query plan costs as pay-as-you-go in Azure OpenAI, let's assume gpt-4o-mini:

+ 15 cents for 1 million input tokens
+ 60 cents for 1 million output tokens
+ Assume small chat conversations of 2,000 input tokens
+ Assume an average output plan size of 350 tokens

#### Estimated billing costs for query execution

To estimate the semantic ranking costs associated with agentic retrieval, start with an idea of what an average document in your index looks like. For example, you might approximate:

+ 10,000 chunks, where each chunk is one to two paragraphs of a PDF.
+ 500 tokens per chunk.
+ Each subquery reranks up to 50 chunks.
+ On average, there are three subqueries per query plan.

#### Calculating price of execution

1. Assume we make 2,000 agentic retrievals with three subqueries per plan. This gives us about 6,000 total queries.

1. Rerank 50 chunks per subquery, which is 300,000 total chunks.

1. Average chunk is 500 tokens, so total tokens for reranking is 150 million.

1. Given a hypothetical price of 0.022 per token, $3.30 is the total cost for reranking in US dollars.

1. Moving on to query plan costs: 2,000 input tokens multiplied by 2,000 agentic retrievals equal 4 million input tokens for a total of 60 cents.

1. Estimate output costs based on an average of 350 tokens. If we multiply 350 by 2,000 agentic retrievals, we get 700,000 output tokens total for a total of 42 cents.

Putting it all together, you'd pay about $3.30 for the semantic ranking in Azure AI Search, 60 cents for input tokens in Azure OpenAI, and 42 cents for output tokens in Azure OpenAI, for $1.02 for query planning total. Combined cost for the full execution is $4.02.

## How to get started

You must use the REST APIs or a prerelease Azure SDK page that provides the functionality. There's no Azure portal or Azure AI Foundry portal support at this time.

Choose any of these options for you next step.

<!-- + Watch this demo. -->
+ Quickstart. Learn the basic workflow using sample data and a prepared index and queries.

+ How-to guides for a closer look at building an agentic retrieval pipeline:

  + [Create an agent](search-agentic-retrieval-how-to-create.md)
  + [Use an agent to retrieve data](search-agentic-retrieval-how-to-retrieve.md)
  + [Build an agent-to-agent retrieval solution](search-agentic-retrieval-how-to-pipeline.md).

+ REST API reference, Agents.

+ [Azure OpenAI Demo](https://github.com/Azure-Samples/azure-search-openai-demo), updated to use agentic retrieval.

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