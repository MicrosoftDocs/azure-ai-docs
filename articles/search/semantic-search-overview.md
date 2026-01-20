---
title: Semantic ranking
titleSuffix: Azure AI Search
description: Learn how Azure AI Search uses deep learning semantic ranking models from Bing to make search results more intuitive.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.custom:
  - ignite-2023
ms.topic: concept-article
ms.date: 01/15/2026
---

# Semantic ranking in Azure AI Search

In Azure AI Search, *semantic ranker* is a feature that measurably improves search relevance by using Microsoft's language understanding models to rerank search results. Semantic ranker is also built into [agentic retrieval](agentic-retrieval-overview.md). This article is a high-level introduction to help you understand the behaviors and benefits of semantic ranker.

Semantic ranker is a premium feature that's billed by usage, but you can use it for free subject to [service limits](/azure/search/search-limits-quotas-capacity#index-limits) for the free tier. We recommend this article for background, but if you'd rather get started, [follow these steps](#how-to-get-started-with-semantic-ranker).

## What is semantic ranking?

Semantic ranker is a collection of query-side capabilities that improve the quality of an initial [BM25-ranked](index-similarity-and-scoring.md) or [RRF-ranked](hybrid-search-ranking.md) search result for text-based queries, the text portion of vector queries, and hybrid queries. Semantic ranking extends the query execution pipeline in three ways:

* First, it always adds secondary ranking over an initial result set that was scored using BM25 or Reciprocal Rank Fusion (RRF). This secondary ranking uses multilingual, deep learning models adapted from Microsoft Bing to promote the most semantically relevant results.

* Second, it returns captions and optionally extracts answers in the response, which you can render on a search page to improve the user's search experience.

* Third, if you enable query rewrite, it expands an initial query string into multiple semantically similar query strings. 

Secondary ranking and "answers" apply to the query response. Query rewrite is part of the query request.

Here are the capabilities of the semantic reranker.

| Capability | Description |
|---------|-------------|
| L2 ranking | Uses the context or semantic meaning of a query to compute a new relevance score over preranked results. |
| [Semantic captions and highlights](semantic-how-to-query-request.md) | Extracts verbatim sentences and phrases from fields that best summarize the content, with highlights over key passages for easy scanning. Captions that summarize a result are useful when individual content fields are too dense for the search results page. Highlighted text elevates the most relevant terms and phrases so that users can quickly determine why a match was considered relevant. |
| [Semantic answers](semantic-answers.md) | An optional and extra substructure returned from a semantic query. It provides a direct answer to a query that looks like a question. It requires that a document has text with the characteristics of an answer. |
| [Query rewrite](semantic-how-to-query-rewrite.md) | Using text queries or the text portion of a vector query, semantic ranker creates up to 10 variants of the query, perhaps correcting typos or spelling errors, or rephrasing a query using generated synonyms. The rewritten query runs on the search engine. The results are scored using BM25 or RRF scoring, and then rescored by semantic ranker.  |

## How semantic ranker works

Semantic ranker takes a query and results, then sends them to language understanding models hosted by Microsoft. It scans for better matches. 

The following illustration explains the concept. Consider the term "capital". It has different meanings depending on whether the context is finance, law, geography, or grammar. Through language understanding, the semantic ranker detects context and promotes results that fit query intent.

:::image type="content" source="media/semantic-search-overview/semantic-vector-representation.png" alt-text="Illustration of vector representation for context." border="true":::

Semantic ranking uses a lot of resources and time. To finish processing within the expected latency of a query operation, the system consolidates and reduces inputs to the semantic ranker. This approach helps complete the reranking step as quickly as possible.

Semantic ranking has three steps:

1. Collect and summarize inputs
1. Score results by using the semantic ranker
1. Output rescored results, captions, and answers

### How the system collects and summarizes inputs

In semantic ranking, the query subsystem passes search results as an input to summarization and ranking models. Because the ranking models have input size constraints and are processing intensive, search results must be sized and structured (summarized) for efficient handling.

1. The semantic ranker starts with a [BM25-ranked result](index-ranking-similarity.md) from a text query or an [RRF-ranked result](hybrid-search-ranking.md) from a vector or hybrid query. The reranking exercise uses only text. Even if results include more than 50 results, only the top 50 results progress to semantic ranking. Typically, semantic ranking uses informational and descriptive fields.

1. For each document in the search result, the summarization model accepts up to 2,000 tokens, where a token is approximately 10 characters. The model assembles inputs from the "title", "keyword", and "content" fields listed in the [semantic configuration](semantic-how-to-configure.md). 

1. The system trims excessively long strings to ensure the overall length meets the input requirements of the summarization step. This trimming exercise is why it's important to add fields to your semantic configuration in priority order. If you have very large documents with text-heavy fields, the system ignores anything after the maximum limit.

   | Semantic field | Token limit |
   |-----------|-------------|
   | "title"   | 128 tokens |
   | "keywords | 128 tokens |
   | "content" | remaining tokens |

1. The summarization output is a summary string for each document, composed of the most relevant information from each field. The system sends summary strings to the ranker for scoring, and to machine reading comprehension models for captions and answers.

   As of November 2024, the maximum length of each generated summary string passed to the semantic ranker is 2,048 tokens. Previously, it was 256 tokens.

## How results are scored

The system scores results based on the caption and any other content from the summary string that fills out the 2,048 token length.

1. The system evaluates captions for conceptual and semantic relevance, relative to the query you provide.

1. The system assigns a **@search.rerankerScore** to each document based on the semantic relevance of the document for the given query. Scores range from 4 to 0 (high to low), where a higher score indicates higher relevance.

   | Score | Meaning |
   |-------|---------|
   | 4.0   | The document is highly relevant and answers the question completely, though the passage might contain extra text unrelated to the question. |
   | 3.0   | The document is relevant but lacks details that would make it complete.|
   | 2.0   | The document is somewhat relevant; it answers the question either partially or only addresses some aspects of the question. |
   | 1.0   | The document is related to the question, and it answers a small part of it. |
   | 0.0   | The document is irrelevant. |

1. The system lists matches in descending order by score and includes them in the query response payload. The payload includes answers, plain text and highlighted captions, and any fields that you marked as retrievable or specified in a select clause.

> [!NOTE]
> For any given query, the distributions of **@search.rerankerScore** can exhibit slight variations due to conditions at the infrastructure level. Ranking model updates can also affect the distribution. For these reasons, if you're writing custom code for minimum thresholds or [setting the threshold property](vector-search-how-to-query.md#set-thresholds-to-exclude-low-scoring-results-preview) for vector and hybrid queries, don't make the limits too granular.

### Outputs of semantic ranker

From each summary string, the machine reading comprehension models find passages that are the most representative.

The outputs are:

* A [semantic caption](semantic-how-to-query-request.md) for the document. Each caption is available in a plain text version and a highlight version, and is frequently fewer than 200 words per document.

* An optional [semantic answer](semantic-answers.md), assuming you specified the `answers` parameter, the query was posed as a question, and a passage is found in the long string that provides a likely answer to the question.

Captions and answers are always verbatim text from your index. There's no generative AI model in this workflow that creates or composes new content.

## Semantic capabilities and limitations

What semantic ranker *can* do:

* Promote matches that are semantically closer to the intent of original query.

* Find strings to use as captions and answers. The response returns captions and answers, which you can render on a search results page.

What semantic ranker *can't* do is rerun the query over the entire corpus to find semantically relevant results. Semantic ranking reranks the existing result set, consisting of the top 50 results as scored by the default ranking algorithm. Furthermore, semantic ranker can't create new information or strings. The language models extract captions and answers verbatim from your content, so if the results don't include answer-like text, they won't produce one.

Although semantic ranking isn't beneficial in every scenario, certain content can benefit significantly from its capabilities. The language models in semantic ranker work best on searchable content that is information-rich and structured as prose. A knowledge base, online documentation, or documents that contain descriptive content see the most gains from semantic ranker capabilities.

The underlying technology is from Bing and Microsoft Research, and integrated into the Azure AI Search infrastructure as an add-on feature. For more information about the research and AI investments backing semantic ranker, see [How AI from Bing is powering Azure AI Search (Microsoft Research Blog)](https://www.microsoft.com/research/blog/the-science-behind-semantic-search-how-ai-from-bing-is-powering-azure-cognitive-search/).

The following video provides an overview of the capabilities.

> [!VIDEO https://www.youtube.com/embed/yOf0WfVd_V0]

## How semantic ranker uses synonym maps

If you enable support for [synonym maps associated to a field](search-synonyms.md#assign-synonyms-to-fields) in your search index, and include that field in the [semantic ranker configuration](semantic-how-to-configure.md), the semantic ranker automatically applies the configured synonyms during the reranking process.

## Availability and pricing

Semantic ranker is available [in selected regions](search-region-support.md). Use it as a standalone feature and as a built-in component of [agentic retrieval](agentic-retrieval-overview.md).

You can disable semantic ranker for your search service, use it on a limited basis for free, or use it more expansively with pay-as-you-go billing:

| Plan | Description |
|------|-------------|
| Free | A free tier search service provides 1,000 semantic ranker requests per month and 50 million free agentic reasoning tokens per month. Higher tiers can also use the free plan. |
| Standard | The standard plan is pay-as-you-go pricing once the monthly free quota is consumed. After the first 1,000 semantic ranker requests, you pay for each additional 1,000 requests. After the first 50 million agentic reasoning tokens per month, you pay a nominal fee for each one million agentic reasoning tokens. The transition from Free to Standard is seamless. You aren't notified when the transition occurs. For more information about charges by currency, see the [Azure AI Search pricing page](https://azure.microsoft.com/pricing/details/search). |

The [Azure AI Search pricing page](https://azure.microsoft.com/pricing/details/search/) shows you the billing rate for different currencies and intervals.

Charges for semantic ranker occur when query requests include `queryType=semantic` and the search string isn't empty (for example, `search=pet friendly hotels in New York`). If your search string is empty (`search=*`), you aren't charged, even if the queryType is set to semantic.

## How to get started with semantic ranker

1. [Check regional availability](search-region-support.md).

1. [Sign in to Azure portal](https://portal.azure.com).

1. [Configure semantic ranker for the search service, choosing a pricing plan](semantic-how-to-enable-disable.md). The free plan is the default.

1. [Configure semantic ranker in a search index](semantic-how-to-configure.md).

1. [Set up queries to return semantic captions and highlights](semantic-how-to-query-request.md).

1. [Optionally, return semantic answers](semantic-answers.md).

## See also

* [Blog: Outperforming vector search with hybrid retrieval and ranking capabilities](https://techcommunity.microsoft.com/t5/azure-ai-services-blog/azure-cognitive-search-outperforming-vector-search-with-hybrid/ba-p/3929167)
