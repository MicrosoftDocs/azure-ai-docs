---
title: Agentic Retrieval Overview
description: Learn about agentic retrieval in Azure AI Search, a pipeline that uses LLMs to decompose complex queries into subqueries for better RAG and agent workflows.
ms.date: 06/02/2026
ms.service: azure-ai-search
ms.topic: concept-article
ms.custom:
  - references_regions
  - build-2025
ai-usage: ai-assisted
---

# Agentic retrieval in Azure AI Search

[!INCLUDE [GA announcement](./includes/previews/agentic-retrieval-ga-announcement.md)]

> [!IMPORTANT]
> These features and functionality are part of the 2026-05-01-preview REST API. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> The 2026-05-01-preview supports connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.
>
> It's your responsibility to manage whether your data will flow outside of your organization's compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
>
> You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. For more information, see the [Azure AI Search Transparency Note](/azure/foundry/responsible-ai/search/transparency-note).

In Azure AI Search, *agentic retrieval* is a multi-query pipeline designed for complex questions posed by users or agents in chat and copilot apps. It's intended for [retrieval-augmented generation](retrieval-augmented-generation-overview.md) (RAG) patterns and agent-to-agent workflows. 

Here's what it does:

+ Can use a large language model (LLM) to break down a complex query into smaller, focused subqueries for better coverage over proprietary and external content. Subqueries can include chat history for extra context.

+ Runs subqueries in parallel. Each subquery is semantically reranked to promote the most relevant matches.

+ Combines the best results into a unified response that an LLM can use to generate grounded answers.

+ Can return source references and an activity log alongside the merged content, so you can use just the grounding data or pass it to an LLM for a full answer.

This high-performance pipeline helps you generate high-quality grounding data or answers for your chat application, with the ability to answer complex questions quickly.

## Why use agentic retrieval?

There are two use cases for agentic retrieval. First, it powers [Foundry IQ](/azure/ai-foundry/agents/concepts/what-is-foundry-iq) in the Microsoft Foundry portal by providing the knowledge layer for agent solutions. Second, it's the basis for custom agentic solutions you build using the Azure AI Search APIs.

Use agentic retrieval when you want to provide agents and apps with the most relevant content for answering harder questions, drawing on chat context, your proprietary content, and external sources.

Agentic retrieval adds latency compared to a single-query pipeline, but it handles query complexity that a single query can't. For example, it can handle:

+ Questions with multiple asks, such as "find me a hotel near the beach, with airport transportation, and that's within walking distance of vegetarian restaurants."

+ Questions that depend on earlier context in the conversation.

+ Queries that benefit from rewriting, using synonym maps and LLM-generated paraphrasing to expand coverage across your content.

+ Spelling mistakes.

:::image type="content" source="media/agentic-retrieval/agentric-retrieval-example.png" alt-text="Diagram of a complex query showing how agentic retrieval handles implied context and an intentional typo." lightbox="media/agentic-retrieval/agentric-retrieval-example.png" :::

## Architecture and workflow

The agentic retrieval process works as follows:

1. **Workflow initiation:** Your application calls a knowledge base with a retrieve action that provides a query and conversation history.

1. **Query planning:** At `low` and `medium` retrieval reasoning effort, the knowledge base sends your query and conversation history to an LLM, which generates focused subqueries. At `minimal` effort, this step is skipped and queries are issued directly to knowledge sources. Reasoning effort defaults to `low` and is configured on the knowledge base.

1. **Query execution:** The knowledge base sends the subqueries to your knowledge sources. All subqueries run simultaneously and can be keyword, vector, or hybrid search. Each subquery undergoes semantic reranking to find the most relevant matches. References are extracted and retained for citation purposes.

1. **Result synthesis:** The system combines all results into a unified response. Merged content is always returned. Source references and an execution activity log are optional.

:::image type="content" source="media/agentic-retrieval/agentic-retrieval-architecture.png" alt-text="Diagram of agentic retrieval workflow using an example query." lightbox="media/agentic-retrieval/agentic-retrieval-architecture.png" :::

### Components

For all agentic retrieval scenarios, a knowledge base and at least one knowledge source are required. Other components are optional and depend on your configuration.

| Component | Service | Role |
|-----------|---------|------|
| Knowledge base | Azure AI Search | Orchestrates the pipeline, managing knowledge sources and query parameters. |
| Knowledge source | Azure AI Search | Defines the content used in the pipeline. Can be indexed (backed by a search index on your service) or remote (content retrieved at query time from an external platform). |
| Search index | Azure AI Search | Stores searchable content (text and vectors) with a semantic configuration. Determines which query types run and which optimizations apply. Required for indexed knowledge sources only. |
| Semantic ranker | Azure AI Search | Used internally by the agentic retrieval pipeline to rerank results for relevance (L2 reranking). |
| LLM | Azure OpenAI | Plans queries and selects knowledge sources. Used at `low` and `medium` retrieval reasoning effort only. Bypassed at `minimal` effort. |

### Integration requirements

Your application drives the pipeline by calling the knowledge base and handling the response. The pipeline returns grounding data that you can pass to an LLM for answer generation or use directly in your conversation interface. For implementation details, see [Tutorial: Build an end-to-end agentic retrieval solution](agentic-retrieval-how-to-create-pipeline.md).

## Availability and pricing

Agentic retrieval is available in [select regions](search-region-support.md). Knowledge sources and knowledge bases also have [maximum limits](search-limits-quotas-capacity.md#agentic-retrieval-limits) that vary by pricing tier and retrieval reasoning effort.

### Billing

Agentic retrieval incurs charges from two services:

+ **Azure AI Search** bills for retrieval tokens consumed during subquery execution and semantic ranking. The free plan (default) provides a monthly token allowance. The standard plan enables pay-as-you-go pricing after the free allowance is consumed. For more information, see [Enable or disable agentic retrieval billing](agentic-retrieval-how-to-enable-disable.md).

+ **Azure OpenAI** bills for input and output tokens used in LLM-based query planning and [answer synthesis](agentic-retrieval-how-to-answer-synthesis.md). Pricing is always pay-as-you-go and based on the model you assign to the knowledge base. Charges appear on your Azure OpenAI bill. For rates, see [Azure OpenAI pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/#pricing).

The following table compares billing between the classic single-query pipeline and the agentic retrieval multi-query pipeline. In the classic pipeline, the billable component is [semantic ranker](semantic-search-overview.md).

| Aspect | Classic pipeline | Agentic retrieval |
|--|--|--|
| Unit | Query based | Token based |
| Cost per unit | Uniform cost per query | Variable cost per token (depends on reasoning effort) |
| Cost estimation | Estimate query count | Estimate token usage |
| Free allowance | Monthly free query allowance | Monthly free token allowance |

### Example: Estimate costs

This example helps illustrate the cost estimation process for query planning and query execution, but not answer synthesis. Your costs could be lower. For current rates, see [Azure AI Search pricing](https://azure.microsoft.com/pricing/details/search) and [Azure OpenAI pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/#pricing).

To estimate the query plan costs as pay-as-you-go in Azure OpenAI, let's assume gpt-4o-mini:

+ 15 cents for 1 million input tokens.
+ 60 cents for 1 million output tokens.
+ 2,000 input tokens for average chat conversation size.
+ 350 tokens for average output plan size.

#### Estimated billing costs for query execution

To estimate agentic retrieval token counts, start with an idea of what an average document in your index looks like. For example, you might approximate:

+ 10,000 chunks, where each chunk is one to two paragraphs of a PDF.
+ 500 tokens per chunk.
+ Each subquery reranks up to 50 chunks.
+ On average, there are three subqueries per query plan.

#### Calculating price of execution

1. Assume we make 2,000 agentic retrievals with three subqueries per plan. This gives us about 6,000 total queries.

1. Rerank 50 chunks per subquery, which is 300,000 total chunks.

1. Average chunk is 500 tokens, so the total tokens for reranking is 150 million.

1. Given a hypothetical price of 0.022 per token, $3.30 is the total cost for reranking in US dollars.

1. Moving on to query plan costs: 2,000 input tokens multiplied by 2,000 agentic retrievals equal 4 million input tokens for a total of 60 cents.

1. Estimate the output costs based on an average of 350 tokens. If we multiply 350 by 2,000 agentic retrievals, we get 700,000 output tokens total for a total of 42 cents.

Putting it all together, you'd pay about $3.30 for agentic retrieval in Azure AI Search, 60 cents for input tokens in Azure OpenAI, and 42 cents for output tokens in Azure OpenAI, for $1.02 for query planning total. The combined cost for the full execution is $4.32.

#### Tips for controlling costs

+ Review the activity log in the response to find out what queries were issued to which sources and the parameters used. You can reissue those queries against your indexes and use a public tokenizer to estimate tokens and compare to API-reported usage. Precise reconstruction of a query or response isn't guaranteed however. Factors include the type of knowledge source, such as public web data or a remote SharePoint knowledge source that's predicated on a user identity, which can affect query reproduction.

+ Reduce the number of knowledge sources (indexes); consolidating content can lower fan-out and token volume. 

+ Lower the reasoning effort to reduce LLM usage during query planning and query expansion (iterative search). 

+ Organize content so the most relevant information can be found with fewer sources and documents (for example, curated summaries or tables).

## How to get started

To create an agentic retrieval solution, you can use the Azure portal, Microsoft Foundry (new) portal, REST APIs, or an equivalent Azure SDK package.

### [**Quickstarts**](#tab/quickstarts)

+ [Quickstart: Agentic retrieval in the Azure portal](get-started-portal-agentic-retrieval.md)
+ [Quickstart: Agentic retrieval](search-get-started-agentic-retrieval.md) (C#, Java, JavaScript, Python, TypeScript, REST)

### [**How-to guides**](#tab/how-to-guides)

The following articles cover core pipeline setup. For all how-to guides, see the table of contents.

+ [Create a search index for agentic retrieval](agentic-retrieval-how-to-create-index.md)
+ [Create a knowledge source](agentic-knowledge-source-overview.md#supported-knowledge-sources) (links to how-to guide for each knowledge source kind)
+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Query a knowledge base using the retrieve action or MCP endpoint](agentic-retrieval-how-to-retrieve.md)

### [**Tutorials**](#tab/tutorials)

+ [Tutorial: Build an end-to-end agentic retrieval solution](agentic-retrieval-how-to-create-pipeline.md)

### [**Code samples**](#tab/sample-code)

+ [Quickstart-Agentic-Retrieval: Python](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/Quickstart-Agentic-Retrieval)
+ [Quickstart-Agentic-Retrieval: .NET](https://github.com/Azure-Samples/azure-search-dotnet-samples/blob/main/quickstart-agentic-retrieval)
+ [Quickstart-Agentic-Retrieval: REST](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/Quickstart-agentic-retrieval)
+ [End-to-end with Azure AI Search and Foundry Agent Service](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/agentic-retrieval-pipeline-example)

### [**REST API references**](#tab/rest-api-references)

+ [Knowledge Sources](/rest/api/searchservice/knowledge-sources)
+ [Knowledge Bases](/rest/api/searchservice/knowledge-bases)
+ [Knowledge Retrieval](/rest/api/searchservice/knowledge-retrieval/retrieve)

### [**Demos**](#tab/demos)

+ [Azure OpenAI Demo](https://github.com/Azure-Samples/azure-search-openai-demo) has been updated to use agentic retrieval.

---

## Next step

> [!div class="nextstepaction"]
> [Quickstart: Agentic retrieval](search-get-started-agentic-retrieval.md)