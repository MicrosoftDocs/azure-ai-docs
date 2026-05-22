---
title: Agentic Retrieval Overview
description: Learn about agentic retrieval in Azure AI Search, a pipeline that uses LLMs to decompose complex queries into subqueries for better RAG and agent workflows.
ms.date: 06/02/2026
ms.service: azure-ai-search
ms.topic: concept-article
ms.custom:
  - references_regions
  - build-2025
---

# Agentic retrieval in Azure AI Search

[!INCLUDE [GA announcement](./includes/previews/agentic-retrieval-ga-announcement.md)]

> [!IMPORTANT]
> These features and functionality are part of the 2026-05-01-preview REST API. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> These 2026-05-01-preview features and functionality support connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.
>
> The 2026-05-01-preview can't modify access permissions that were set outside of the 2026-05-01-preview. If you use the 2026-05-01-preview with access- or permission-restricted content, a timing lag will occur before the 2026-05-01-preview recognizes changes to those access or permission restrictions.
>
> You can use the 2026-05-01-preview to enable cross-origin resource sharing (CORS), which allows browser-based applications to request data directly from the service. Depending on your CORS configuration, external web pages might be able to access or invoke the service and its data using the user's browser context, as well as create other security threats. Enabling CORS is at your own risk.

In Azure AI Search, *agentic retrieval* is a multi-query pipeline designed for complex questions posed by users or agents in chat and copilot apps. It's intended for [retrieval-augmented generation](retrieval-augmented-generation-overview.md) (RAG) patterns and agent-to-agent workflows. 

Here's what it does:

+ Uses a large language model (LLM) to break down a complex query into smaller, focused subqueries for better coverage over your indexed content. Subqueries can include chat history for extra context.

+ Runs subqueries in parallel. Each subquery is semantically reranked to promote the most relevant matches.

+ Combines the best results into a unified response that an LLM can use to generate answers with your proprietary content.

+ The response is modular yet comprehensive in how it also includes a query plan and source documents. You can choose to use just the search results as grounding data, or invoke the LLM to formulate an answer.

This high-performance pipeline helps you generate high-quality grounding data (or an answer) for your chat application, with the ability to answer complex questions quickly.

Programmatically, agentic retrieval is supported through a [knowledge base object](/rest/api/searchservice/knowledge-bases) in the latest stable (2026-04-01) and preview (2026-05-01-preview) REST API versions, as well as the equivalent Azure SDK packages. A knowledge base's retrieval response is designed for downstream consumption by other agents and chat apps.

## Why use agentic retrieval

There are two use cases for agentic retrieval. First, it's the basis of the [Foundry IQ](/azure/ai-foundry/agents/concepts/what-is-foundry-iq) experience in the Microsoft Foundry (new) portal. It provides the knowledge layer for agent solutions in Microsoft Foundry. Second, it's the basis for custom agentic solutions that you create using the Azure AI Search APIs.

You should use agentic retrieval when you want to provide agents and apps with the most relevant content for answering harder questions, leveraging chat context and your proprietary content.

The *agentic* aspect is a reasoning step in query planning processing that's performed by a supported large language model (LLM) that you provide. The LLM analyzes the entire chat thread to identify the underlying information need. Instead of a single, catch-all query, the LLM breaks down compound questions into focused subqueries based on: user questions, chat history, and parameters on the request. The subqueries target your indexed documents (plain text and vectors) in Azure AI Search. This hybrid approach ensures you surface both keyword matches and semantic similarities at once, dramatically improving recall. 

The *retrieval* component is the ability to run subqueries simultaneously, merge results, semantically rank results, and return a three-part response that includes grounding data for the next conversation turn, reference data so that you can inspect the source content, and an activity plan that shows query execution steps.

Query expansion and parallel execution, plus the retrieval response, are the key capabilities of agentic retrieval that make it the best choice for generative AI (RAG) applications.

:::image type="content" source="media/agentic-retrieval/agentric-retrieval-example.png" alt-text="Diagram of a complex query showing how agentic retrieval handles implied context and an intentional typo." lightbox="media/agentic-retrieval/agentric-retrieval-example.png" :::

Agentic retrieval adds latency to query processing, but it makes up for it by adding these capabilities:

+ Reads in chat history as an input to the retrieval pipeline.
+ Deconstructs a complex query that contains multiple "asks" into component parts. For example: "find me a hotel near the beach, with airport transportation, and that's within walking distance of vegetarian restaurants."
+ Rewrites an original query into multiple subqueries using synonym maps (optional) and LLM-generated paraphrasing.
+ Corrects spelling mistakes.
+ Executes all subqueries simultaneously. 
+ Outputs a unified result as a single string. Alternatively, you can extract parts of the response for your solution. Metadata about query execution and reference data is included in the response.

Agentic retrieval invokes the entire query processing pipeline multiple times for each subquery, but it does so in parallel, preserving the efficiency and performance necessary for a reasonable user experience.


## Architecture and workflow

Agentic retrieval is designed for conversational search experiences that use an LLM to intelligently break down complex queries. The system coordinates multiple Azure services to deliver comprehensive search results.

:::image type="content" source="media/agentic-retrieval/agentic-retrieval-architecture.png" alt-text="Diagram of agentic retrieval workflow using an example query." lightbox="media/agentic-retrieval/agentic-retrieval-architecture.png" :::

### How it works

The agentic retrieval process works as follows:

1. **Workflow initiation**: Your application calls a knowledge base with retrieve action that provides a query and conversation history.

1. **Query planning**: A knowledge base sends your query and conversation history to an LLM, which analyzes the context and breaks down complex questions into focused subqueries. This step is automated and not customizable.

1. **Query execution**: The knowledge base sends the subqueries to your knowledge sources. All subqueries run simultaneously and can be keyword, vector, and hybrid search. Each subquery undergoes semantic reranking to find the most relevant matches. References are extracted and retained for citation purposes.

1. **Result synthesis**: The system combines all results into a unified response with three parts: merged content, source references, and execution details.

Your search index determines query execution and any optimizations that occur during query execution. Specifically, if your index includes searchable text and vector fields, a hybrid query executes. If the only searchable field is a vector field, then only pure vector search is used. The index semantic configuration, plus optional scoring profiles, synonym maps, analyzers, and normalizers (if you add filters) are all used during query execution. You must have named defaults for a semantic configuration and a scoring profile.

### Required components

| Component | Service | Role |
|-----------|---------|------|
| **LLM** | Azure OpenAI | Creates subqueries from conversation context and later uses grounding data for answer generation |
| **Knowledge base** | Azure AI Search | Orchestrates the pipeline, connecting to your LLM and managing query parameters |
| **Knowledge source** | Azure AI Search | Wraps the search index with properties pertaining to knowledge base usage |
| **Search index** | Azure AI Search | Stores your searchable content (text and vectors) with semantic configuration |
| **Semantic ranker** | Azure AI Search | Used internally by the agentic retrieval pipeline to rerank results for relevance (L2 reranking) |

### Integration requirements

Your application drives the pipeline by calling the knowledge base and handling the response. The pipeline returns grounding data that you pass to an LLM for answer generation in your conversation interface. For implementation details, see [Tutorial: Build an end-to-end agentic retrieval solution](agentic-retrieval-how-to-create-pipeline.md).


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

+ Organize content so the most relevant information can be found with fewer sources and documents (For example, curated summaries or tables).


## How to get started

To create an agentic retrieval solution, you can use the Azure portal, REST APIs, or an Azure SDK package that provides the functionality.

### [**Quickstarts**](#tab/quickstarts)

+ [Quickstart: Agentic retrieval in the Azure portal](get-started-portal-agentic-retrieval.md)
+ [Quickstart: Agentic retrieval](search-get-started-agentic-retrieval.md) (C#, Java, JavaScript, Python, TypeScript, REST)

### [**How-to guides**](#tab/how-to-guides)

+ Create a knowledge source:
  + [Blob](agentic-knowledge-source-how-to-blob.md)
  + [OneLake](agentic-knowledge-source-how-to-onelake.md)
  + [Remote SharePoint](agentic-knowledge-source-how-to-sharepoint-remote.md)
  + [Indexed SharePoint](agentic-knowledge-source-how-to-sharepoint-indexed.md)
  + [Search index](agentic-knowledge-source-how-to-search-index.md)
  + [Web](agentic-knowledge-source-how-to-web.md)
+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Use answer synthesis for citation-backed responses](agentic-retrieval-how-to-answer-synthesis.md)
+ [Image serving in agentic retrieval (preview)](agentic-retrieval-how-to-image-serving.md)
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
> [Enable or disable agentic retrieval billing](agentic-retrieval-how-to-enable-disable.md)