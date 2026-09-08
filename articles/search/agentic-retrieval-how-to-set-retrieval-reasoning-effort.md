---
title: Set the Retrieval Reasoning Effort
description: Learn how to set the level of LLM processing for agentic retrieval in Azure AI Search.
ms.date: 08/17/2026
ms.service: azure-ai-search
ms.topic: how-to
ms.custom:
  - references_regions
  - dev-focus
  - doc-kit-assisted
ai-usage: ai-assisted
zone_pivot_groups: search-csharp-python-rest
---

# Set the retrieval reasoning effort (preview)

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

[!INCLUDE [Preview feature](./includes/previews/agentic-retrieval-preview-feature.md)]

> [!IMPORTANT]
> These features and functionality are part of the 2026-08-01-preview REST API. The 2026-08-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> The 2026-08-01-preview supports connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.
>
> It's your responsibility to manage whether your data will flow outside of your organization's compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
>
> You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. For more information, see the [Azure AI Search Transparency Note](/azure/foundry/responsible-ai/search/transparency-note).

In agentic retrieval, you can specify the level of large language model (LLM) processing for query planning and answer formulation. Use the *retrieval reasoning effort* (preview) to set LLM processing levels that affect costs and latency. Extra LLM processing improves relevance, but it also takes longer and uses billable LLM resources.

You can set this property in a knowledge base or a retrieve request. The knowledge base setting establishes the default for all queries, while the retrieve request setting overrides the default on a query-by-query basis. If neither setting is present, the service uses `low`.

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-08-01-preview&preserve-view=true) |
| -- | -- | -- | -- | -- | -- | -- |
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

- An existing [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md) with at least one knowledge source and a model configuration.

- Permission to update and query knowledge bases. Configure [keyless authentication](search-get-started-rbac.md) with the **Search Service Contributor** and **Search Index Data Reader** roles assigned to your user account (recommended) or use an [admin API key](search-security-api-keys.md).

::: zone pivot="csharp"

- The latest [`Azure.Search.Documents`](https://www.nuget.org/packages/Azure.Search.Documents) preview package: `dotnet add package Azure.Search.Documents --prerelease`

- For keyless authentication, the [`Azure.Identity`](https://www.nuget.org/packages/Azure.Identity) package: `dotnet add package Azure.Identity`

::: zone-end

::: zone pivot="python"

- The latest [`azure-search-documents`](https://pypi.org/project/azure-search-documents/#history) preview package: `pip install --pre azure-search-documents`

- For keyless authentication, the [`azure-identity`](https://pypi.org/project/azure-identity/) package: `pip install azure-identity`

::: zone-end

::: zone pivot="rest"

- The [2026-08-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-08-01-preview&preserve-view=true) version of the Search Service REST API.

- For keyless authentication, include a [Microsoft Entra ID token](search-get-started-rbac.md?pivots=rest#get-token) in the `Authorization` header of each HTTP request.

::: zone-end

## Choose a reasoning effort

Choose a reasoning effort based on the tradeoff you want between latency, cost, and retrieval depth.

### Reasoning effort levels

| Level | Description | Recommendation | Limits |
| --- | --- | --- | --- |
| `minimal` | Disables LLM-based query planning to deliver the lowest cost and latency for agentic retrieval. It issues direct text and vector searches across the knowledge sources listed in the knowledge base, and returns the best-matching passages. Because all knowledge sources in the knowledge base are always searched and no query expansion is performed, behavior is predictable and easy to control. It also means the `alwaysQueryKnowledgeSource` property on a retrieve request is ignored. | Use `minimal` for migrations from the [Search API](/rest/api/searchservice/documents/search-post) or when you want to manage query planning yourself. | <ul><li>`outputMode` must be set to `extractiveData`.</li><li>[Answer synthesis (preview)](agentic-retrieval-how-to-answer-synthesis.md) and [web knowledge](agentic-knowledge-source-how-to-web.md) aren't supported.</li><li>Maximum of [10 knowledge sources per knowledge base](search-limits-quotas-capacity.md#agentic-retrieval-limits).</li></ul> |
| `low` | The default mode of agentic retrieval, running a single pass of LLM-based query planning and knowledge source selection. The agentic retrieval engine generates subqueries and fans them out to the selected knowledge sources, then merges the results. You can enable answer synthesis (preview) to produce a grounded natural-language response with inline citations. | Use `low` when you want a balance between minimal latency and deeper processing. | <ul><li>5,000 answer tokens.</li><li>Maximum of 50 documents for semantic ranking, and 10 documents if the semantic ranker uses L3 classification.</li></ul> |
| `medium` | Adds deeper search and an enhanced retrieval stack to agentic retrieval to maximize completeness. After the first search, a high-precision semantic classifier evaluates the retrieved documents. If the initial results aren't sufficiently relevant, the service performs one follow-up iteration using a revised query plan. | Use `medium` to maximize the utility of LLM-assisted knowledge retrieval. | <ul><li>10,000 answer tokens.</li><li>Maximum of 50 documents for semantic ranking, and 20 documents if the semantic ranker uses L3 classification.</li><li>Available in [select regions](#region-support-for-medium-retrieval).</li></ul> |
| `auto` | Starts with a lightweight retrieval pass. If the first pass provides enough grounding, the service returns the result. Otherwise, it continues with LLM-based query planning, up to medium effort. | Use `auto` when you want the service to balance retrieval depth and latency for each request. | <ul><li>Requires the 2026-08-01-preview REST API.</li><li>Requires a model on the knowledge base.</li><li>Available in all [regions that support agentic retrieval](search-region-support.md).</li><li>Earlier API versions return `400 Bad Request`.</li></ul> |

### Iterative search for medium retrieval

A medium retrieval reasoning effort provides iterative search if initial results aren't sufficiently relevant. An extra *semantic classifier model* is called to determine if a second iteration is necessary.

The semantic classifier:

- Recognizes when there's enough context to answer the question.

- Retries on insufficient results, using existing information for context. New queries might drill down for more focused detail, or broaden the search. The activity log in the response shows the generated queries used for a more comprehensive answer.

- Rescores using L3 classification. The range is identical to L2 ranking, an absolute range of zero through 4.0.

There's only one retry. Each iteration adds latency and cost, so the system constrains retry to one pass. A second iteration adds input tokens to the query pipeline, which adds to the overall billable input token count.

Iteration can reuse existing knowledge sources or choose different sources. The second pass selects the most promising knowledge source to provide the missing information.

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

Set `retrievalReasoningEffort` in a knowledge base definition to establish the default for its queries. The `auto` reasoning effort requires a model configuration. The following example preserves the existing `knowledgeSources` and `models` configuration, sets the reasoning effort to `auto`, and updates the knowledge base.

::: zone pivot="csharp"

```csharp
using Azure.Identity;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;
using Azure.Search.Documents.KnowledgeBases.Models;

var endpoint = new Uri("<search-endpoint>");
var credential = new DefaultAzureCredential();
var knowledgeBaseName = "<knowledge-base-name>";

var indexClient = new SearchIndexClient(endpoint, credential);
var knowledgeBase = (
    await indexClient.GetKnowledgeBaseAsync(knowledgeBaseName)).Value;
knowledgeBase.RetrievalReasoningEffort =
    new KnowledgeRetrievalAutoReasoningEffort();
await indexClient.CreateOrUpdateKnowledgeBaseAsync(knowledgeBase);
```

**Reference:** [KnowledgeBase](/dotnet/api/azure.search.documents.indexes.models.knowledgebase?view=azure-dotnet-preview&preserve-view=true)

To use another level, replace `KnowledgeRetrievalAutoReasoningEffort` with `KnowledgeRetrievalMinimalReasoningEffort`, `KnowledgeRetrievalLowReasoningEffort`, or `KnowledgeRetrievalMediumReasoningEffort`.

::: zone-end

::: zone pivot="python"

```python
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.knowledgebases.models import (
    KnowledgeRetrievalAutoReasoningEffort,
)

endpoint = "<search-endpoint>"
credential = DefaultAzureCredential()
knowledge_base_name = "<knowledge-base-name>"

index_client = SearchIndexClient(endpoint, credential)
knowledge_base = index_client.get_knowledge_base(knowledge_base_name)
knowledge_base.retrieval_reasoning_effort = (
    KnowledgeRetrievalAutoReasoningEffort()
)
index_client.create_or_update_knowledge_base(knowledge_base)
```

**Reference:** [KnowledgeBase](/python/api/azure-search-documents/azure.search.documents.indexes.models.knowledgebase)

To use another level, replace `KnowledgeRetrievalAutoReasoningEffort` with `KnowledgeRetrievalMinimalReasoningEffort`, `KnowledgeRetrievalLowReasoningEffort`, or `KnowledgeRetrievalMediumReasoningEffort`.

::: zone-end

::: zone pivot="rest"

```http
@api-version = 2026-08-01-preview
@knowledge-base-url = {{search-endpoint}}/knowledgebases/{{knowledge-base-name}}

PUT {{knowledge-base-url}}?api-version={{api-version}}
Content-Type: application/json
Authorization: Bearer {{search-access-token}}

{
  "name": "{{knowledge-base-name}}",
  "knowledgeSources": [
    {
      "name": "{{knowledge-source-name}}"
    }
  ],
  "models": [
    {
      "kind": "azureOpenAI",
      "azureOpenAIParameters": {
        "resourceUri": "{{aoai-endpoint}}",
        "authIdentity": null,
        "deploymentId": "{{model-deployment-name}}",
        "modelName": "{{model-name}}"
      }
    }
  ],
  "retrievalReasoningEffort": {
    "kind": "auto"
  }
}
```

**Reference:** [Knowledge Bases - Create or Update](/rest/api/searchservice/knowledge-bases/create-or-update?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

To use another level, set `retrievalReasoningEffort.kind` to `minimal`, `low`, or `medium`.

::: zone-end

## Set the reasoning effort in a retrieve request

Set `retrievalReasoningEffort` in a retrieve request to override the knowledge base default for that request. The following example sends a message, uses `low` to override the `auto` default from the previous section, and enables answer synthesis (preview).

::: zone pivot="csharp"

```csharp
using Azure.Identity;
using Azure.Search.Documents.KnowledgeBases;
using Azure.Search.Documents.KnowledgeBases.Models;

var endpoint = new Uri("<search-endpoint>");
var credential = new DefaultAzureCredential();
var knowledgeBaseName = "<knowledge-base-name>";

var kbClient = new KnowledgeBaseRetrievalClient(
    endpoint, knowledgeBaseName, credential);
var request = new KnowledgeBaseRetrievalRequest
{
    RetrievalReasoningEffort =
        new KnowledgeRetrievalLowReasoningEffort(),
    OutputMode = KnowledgeRetrievalOutputMode.AnswerSynthesis
};

request.Messages.Add(
    new KnowledgeBaseMessage(
        content: new[] {
            new KnowledgeBaseMessageTextContent("What is the return policy?")
        }
    ) { Role = "user" }
);

var result = await kbClient.RetrieveAsync(request);
```

**Reference:** [KnowledgeBaseRetrievalRequest](/dotnet/api/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
from azure.identity import DefaultAzureCredential
from azure.search.documents.knowledgebases import KnowledgeBaseRetrievalClient
from azure.search.documents.knowledgebases.models import (
    KnowledgeBaseMessage,
    KnowledgeBaseMessageTextContent,
    KnowledgeBaseRetrievalRequest,
    KnowledgeRetrievalOutputMode,
    KnowledgeRetrievalLowReasoningEffort,
)

endpoint = "<search-endpoint>"
credential = DefaultAzureCredential()
knowledge_base_name = "<knowledge-base-name>"

kb_client = KnowledgeBaseRetrievalClient(
    endpoint,
    credential,
    knowledge_base_name=knowledge_base_name,
)
request = KnowledgeBaseRetrievalRequest(
    messages=[
        KnowledgeBaseMessage(
            role="user",
            content=[
                KnowledgeBaseMessageTextContent(
                    text="What is the return policy?"
                )
            ],
        )
    ],
    retrieval_reasoning_effort=KnowledgeRetrievalLowReasoningEffort(),
    output_mode=KnowledgeRetrievalOutputMode.ANSWER_SYNTHESIS,
)

result = kb_client.retrieve(request)
```

**Reference:** [KnowledgeBaseRetrievalRequest](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest)

::: zone-end

::: zone pivot="rest"

```http
@api-version = 2026-08-01-preview
@retrieve-url = {{search-endpoint}}/knowledgebases/{{knowledge-base-name}}/retrieve

POST {{retrieve-url}}?api-version={{api-version}}
Content-Type: application/json
Authorization: Bearer {{search-access-token}}

{
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What is the return policy?"
        }
      ]
    }
  ],
  "retrievalReasoningEffort": {
    "kind": "low"
  },
  "outputMode": "answerSynthesis"
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

::: zone-end

The retrieve request returns a grounded answer based on the knowledge sources configured in the knowledge base.

## Related content

- [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
- [Create a knowledge base in Azure AI Search](agentic-retrieval-how-to-create-knowledge-base.md)
- [Query a knowledge base using the retrieve action or MCP endpoint](agentic-retrieval-how-to-retrieve.md)
