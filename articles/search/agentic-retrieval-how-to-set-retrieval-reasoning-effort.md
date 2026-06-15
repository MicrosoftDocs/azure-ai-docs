---
title: Set the Retrieval Reasoning Effort
description: Learn how to set the level of LLM processing for agentic retrieval in Azure AI Search.
ms.date: 06/08/2026
ms.service: azure-ai-search
ms.topic: how-to
ms.custom:
  - references_regions
ai-usage: ai-assisted
---

# Set the retrieval reasoning effort (preview)

[!INCLUDE [Preview feature](./includes/previews/agentic-retrieval-preview-feature.md)]

> [!IMPORTANT]
> These features and functionality are part of the 2026-05-01-preview REST API. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> The 2026-05-01-preview supports connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.
>
> It's your responsibility to manage whether your data will flow outside of your organization's compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
>
> You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. For more information, see the [Azure AI Search Transparency Note](/azure/foundry/responsible-ai/search/transparency-note).

In agentic retrieval, you can specify the level of large language model (LLM) processing for query planning and answer formulation. Use the *retrieval reasoning effort* (preview) to set LLM processing levels that affect costs and latency. Extra LLM processing improves relevance, but it also takes longer and uses billable LLM resources.

You can set this property in a knowledge base or a retrieve request. The knowledge base setting establishes the default for all queries, while the retrieve request setting overrides the default on a query-by-query basis.

## Prerequisites

- An Azure AI Search service with a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

- Permissions to update knowledge bases. Configure [keyless authentication](search-get-started-rbac.md) with the **Search Service Contributor** role assigned to your user account (recommended) or use an [API key](search-security-api-keys.md).

- If the knowledge base specifies an LLM, the search service must have a [managed identity](search-how-to-managed-identities.md) with **Cognitive Services User** permissions on the Microsoft Foundry resource.

- The [2026-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-05-01-preview&preserve-view=true) REST API or an equivalent Azure SDK preview package: [.NET](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [Python](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md)

## Choose a reasoning effort

Choose a reasoning effort based on the tradeoff you want between
latency, cost, and retrieval depth.

### Reasoning effort levels

| Level | Description | Recommendation | Limits |
| --- | --- | --- | --- |
| `minimal` | Disables LLM-based query planning to deliver the lowest cost and latency for agentic retrieval. It issues direct text and vector searches across the knowledge sources listed in the knowledge base, and returns the best-matching passages. Because all knowledge sources in the knowledge base are always searched and no query expansion is performed, behavior is predictable and easy to control. It also means the `alwaysQueryKnowledgeSource` property on a retrieve request is ignored. | Use `minimal` for migrations from the [Search API](/rest/api/searchservice/documents/search-post) or when you want to manage query planning yourself. | <ul><li>`outputMode` must be set to `extractiveData`.</li><li>[Answer synthesis](agentic-retrieval-how-to-answer-synthesis.md) and [web knowledge](agentic-knowledge-source-how-to-web.md) aren't supported.</li><li>Maximum of [10 knowledge sources per knowledge base](search-limits-quotas-capacity.md#agentic-retrieval-limits).</li></ul> |
| `low` | The default mode of agentic retrieval, running a single pass of LLM-based query planning and knowledge source selection. The agentic retrieval engine generates subqueries and fans them out to the selected knowledge sources, then merges the results. You can enable answer synthesis to produce a grounded natural-language response with inline citations. | Use `low` when you want a balance between minimal latency and deeper processing. | <ul><li>5,000 answer tokens.</li><li>In the 2026-05-01-preview, maximum of [10 knowledge sources per knowledge base on most paid tiers](search-limits-quotas-capacity.md#agentic-retrieval-limits).</li><li>In earlier preview API versions, maximum of three subqueries from three knowledge sources per knowledge base.</li><li>Maximum of 50 documents for semantic ranking, and 10 documents if the semantic ranker uses L3 classification.</li></ul> |
| `medium` | Adds deeper search and an enhanced retrieval stack to agentic retrieval to maximize completeness. After the first search is performed, a [high-precision semantic classifier](search-relevance-overview.md) evaluates the retrieved documents to determine whether further processing and L3 ranking is required. If the initial results from the first pass are insufficiently relevant to the query, a follow-up iteration is performed using a revised query plan. This revised query plan takes the previous results into account and iterates by fine-tuning queries, broadening terms, or adding other knowledge sources such as the web. It also increases resource limits compared to low and minimal effort. This reasoning level optimizes for relevance rather than exhaustive recall. | Use `medium` to maximize the utility of LLM-assisted knowledge retrieval. | <ul><li>10,000 answer tokens.</li><li>In the 2026-05-01-preview, maximum of [10 knowledge sources per knowledge base on most paid tiers](search-limits-quotas-capacity.md#agentic-retrieval-limits).</li><li>In earlier preview API versions, maximum of five subqueries from five knowledge sources per knowledge base.</li><li>Maximum of 50 documents for semantic ranking, and 20 documents if the semantic ranker uses L3 classification.</li><li>Available in [select regions](#region-support-for-medium-retrieval).</li></ul> |

### Iterative search for medium retrieval

A medium retrieval reasoning effort provides iterative search if initial results aren't sufficiently relevant. An extra *semantic classifier model* is called to determine if a second iteration is necessary.

The semantic classifier:

- Recognizes when there's enough context to answer the question.

- Retries on insufficient results, using existing information for context. New queries might drill down for more focused detail, or broaden the search. The activity log in the response shows the generated queries used for a more comprehensive answer.

- Rescores using L3 classification. The range is identical to L2 ranking, an absolute range of zero through 4.0.

There's only one retry. Each iteration adds latency and cost, so the system constrains retry to one pass. A second iteration adds input tokens to the query pipeline, which adds to the overall billable input token count.

Iteration can reuse or choose different sources. The second pass selects the most promising knowledge resource to provide the missing information.

### Region support for medium retrieval

You can set a medium retrieval reasoning effort if your search service is in one of the following regions:

- East US 2
- East US
- South Central US
- West US 3
- West US 2
- West US
- Germany West Central
- North Europe
- Switzerland North
- Sweden Central
- Spain Central
- UK South
- Korea Central
- Japan East
- Southeast Asia

## Set the reasoning effort in a knowledge base

This section demonstrates how to set the retrieval reasoning effort in an existing knowledge base. Although you can use this configuration for new knowledge bases, knowledge base creation is beyond the scope of this article.

To establish the default behavior, set `retrievalReasoningEffort` in the knowledge base definition.

```http
### Set retrieval reasoning effort in a knowledge base
PUT {{search-url}}/knowledgebases/{{knowledge-base-name}}?api-version=2026-05-01-preview
Content-Type: application/json
api-key: {{api-key}}

{
  "name": "{{knowledge-base-name}}",
  "knowledgeSources": [ ... // OMITTED FOR BREVITY ],
  "retrievalReasoningEffort": {
    "kind": "low"
  }
}
```

**Reference:** [Knowledge Bases - Create or Update](/rest/api/searchservice/knowledge-bases/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

## Set the reasoning effort in a retrieve request

To override the default on a query-by-query basis, set `retrievalReasoningEffort` in the retrieve request body.

```http
### Override retrieval reasoning effort in a retrieve request
POST {{search-url}}/knowledgebases/{{knowledge-base-name}}/retrieve?api-version=2026-05-01-preview
Content-Type: application/json
api-key: {{api-key}}

{
  "messages": [ ... // OMITTED FOR BREVITY ],
  "retrievalReasoningEffort": {
    "kind": "low"
  },
  "outputMode": "answerSynthesis",
  "maxRuntimeInSeconds": 30,
  "maxOutputSize": 6000
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

## Related content

- [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
- [Create a knowledge base in Azure AI Search](agentic-retrieval-how-to-create-knowledge-base.md)
- [Query a knowledge base using the retrieve action or MCP endpoint](agentic-retrieval-how-to-retrieve.md)
