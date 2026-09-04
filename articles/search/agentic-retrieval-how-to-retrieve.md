---
title: Query Knowledge Base via API or MCP
description: Learn how to query a knowledge base using the retrieve action or MCP endpoint in Azure AI Search using REST APIs, Azure SDKs, or any MCP-compatible client.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 09/04/2026
ms.custom:
  - dev-focus
  - doc-kit-assisted
ai-usage: ai-assisted
zone_pivot_groups: search-csharp-python-rest
---

# Query a knowledge base using the retrieve action or MCP endpoint

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

[!INCLUDE [GA feature](./includes/previews/agentic-retrieval-ga-feature.md)]

> [!IMPORTANT]
> These features and functionality are part of the 2026-08-01-preview REST API. The 2026-08-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> The 2026-08-01-preview supports connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.
>
> It's your responsibility to manage whether your data will flow outside of your organization's compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
>
> You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. For more information, see the [Azure AI Search Transparency Note](/azure/foundry/responsible-ai/search/transparency-note).

In an agentic retrieval pipeline, the [retrieve action](/rest/api/searchservice/knowledge-retrieval/retrieve) invokes parallel query processing from a knowledge base. You can call the retrieve action directly using the Search Service REST APIs or an Azure SDK. Each knowledge base also exposes a Model Context Protocol (MCP) endpoint for consumption by MCP-compatible agents.

This article explains how to call both retrieval methods with optional permissions enforcement. It covers the retrieve action first and the MCP endpoint later because the MCP tool result currently differs from the REST and SDK response shape.

To set up a pipeline that connects Azure AI Search to Foundry Agent Service via MCP, see [Tutorial: Build an end-to-end agentic retrieval solution](agentic-retrieval-how-to-create-pipeline.md).

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-retrieval/retrieve) |
| -- | -- | -- | -- | -- | -- | -- |
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ An Azure AI Search service with a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

+ For shared model access and client setup, see [Prerequisites for creating a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md#prerequisites).

+ Permission to query knowledge bases. Configure [keyless authentication](search-get-started-rbac.md) with the **Search Index Data Reader** role assigned to your user account (recommended) or use a [query API key](search-security-api-keys.md).

::: zone pivot="csharp"

+ If you [call the MCP endpoint through the Azure OpenAI Responses API](#authenticate-to-the-mcp-endpoint), you need:

  + A deployed LLM and the **Cognitive Services OpenAI User** role (or an API key) on the Foundry resource. You can reuse the LLM and resource specified in your knowledge base, if applicable.

  + The [`Azure.AI.OpenAI`](https://www.nuget.org/packages/Azure.AI.OpenAI) package: `dotnet add package Azure.AI.OpenAI`

+ Required [`Azure.Search.Documents`](https://www.nuget.org/packages/Azure.Search.Documents) package:

  + For `2026-08-01-preview` features, the latest preview package: `dotnet add package Azure.Search.Documents --prerelease`

  + For `2026-04-01` features, the latest stable package: `dotnet add package Azure.Search.Documents`

+ For keyless authentication, the [`Azure.Identity`](https://www.nuget.org/packages/Azure.Identity) package: `dotnet add package Azure.Identity`

::: zone-end

::: zone pivot="python"

+ If you [call the MCP endpoint through the Azure OpenAI Responses API](#authenticate-to-the-mcp-endpoint), you need:

  + A deployed LLM and the **Cognitive Services OpenAI User** role (or an API key) on the Foundry resource. You can reuse the LLM and resource specified in your knowledge base, if applicable.

  + The [`openai`](https://pypi.org/project/openai/) package: `pip install openai`

+ Required [`azure-search-documents`](https://pypi.org/project/azure-search-documents/#history) package:

  + For `2026-08-01-preview` features, the latest preview package: `pip install --pre azure-search-documents`

  + For `2026-04-01` features, the latest stable package: `pip install azure-search-documents`

+ For keyless authentication, the [`azure-identity`](https://pypi.org/project/azure-identity/) package: `pip install azure-identity`

::: zone-end

::: zone pivot="rest"

+ Required Search Service REST API version:

  + For preview features: [2026-08-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

  + For generally available features: [2026-04-01](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-04-01&preserve-view=true)

+ For keyless authentication, include a [Microsoft Entra ID token](search-get-started-rbac.md?pivots=rest#get-token) in the `Authorization` header of each HTTP request.

::: zone-end

## Limitations

For search index knowledge sources, when you enable reranking, retrieve uses the knowledge source's semantic configuration. It doesn't apply the underlying index's [scoring profiles](index-add-scoring-profiles.md), including `defaultScoringProfile`. Retrieve responses also don't surface `@search.rerankerBoostedScore`.

## Call the retrieve action

You specify the retrieve action on a knowledge base. The request body includes the query input and an optional list of knowledge sources to target.

The `2026-04-01` API version only supports the `intents` input and minimal, extractive retrieval. Preview-only capabilities, including the `messages` input, query planning, answer synthesis, and configurable reasoning effort, aren't supported. Use `2026-08-01-preview` for full functionality.

:::zone pivot="csharp"

# [2026-08-01-preview](#tab/2026-08-01-preview)

```csharp
using Azure.Identity;
using Azure;
using Azure.Search.Documents.KnowledgeBases;
using Azure.Search.Documents.KnowledgeBases.Models;

// Create knowledge base retrieval client
var kbClient = new KnowledgeBaseRetrievalClient(
    endpoint: new Uri("<search-endpoint>"),
    knowledgeBaseName: "<knowledge-base-name>",
    credential: new DefaultAzureCredential()
);

var retrievalRequest = new KnowledgeBaseRetrievalRequest();
retrievalRequest.Messages.Add(
    new KnowledgeBaseMessage(
        content: new[] {
            new KnowledgeBaseMessageTextContent(
                "You can answer questions about the Earth at night. "
                + "Sources have a JSON format with a ref_id that must be cited in the answer. "
                + "If you do not have the answer, respond with 'I do not know'."
            )
        }
    ) { Role = "assistant" }
);
retrievalRequest.Messages.Add(
    new KnowledgeBaseMessage(
        content: new[] {
            new KnowledgeBaseMessageTextContent(
                "Why is the Phoenix nighttime street grid so sharply visible from space, "
                + "whereas large stretches of the interstate between midwestern cities remain comparatively dim?"
            )
        }
    ) { Role = "user" }
);

var result = await kbClient.RetrieveAsync(retrievalRequest);
Console.WriteLine(
    (result.Value.Response[0].Content[0] as KnowledgeBaseMessageTextContent)!.Text
);
```

**Reference:** [KnowledgeBaseRetrievalClient](/dotnet/api/azure.search.documents.knowledgebases.knowledgebaseretrievalclient?view=azure-dotnet-preview&preserve-view=true), [KnowledgeBaseRetrievalRequest](/dotnet/api/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest?view=azure-dotnet-preview&preserve-view=true)

# [2026-04-01](#tab/2026-04-01)

```csharp
using Azure.Identity;
using Azure;
using Azure.Search.Documents.KnowledgeBases;
using Azure.Search.Documents.KnowledgeBases.Models;

// Create knowledge base retrieval client
var kbClient = new KnowledgeBaseRetrievalClient(
    endpoint: new Uri("<search-endpoint>"),
    knowledgeBaseName: "<knowledge-base-name>",
    credential: new DefaultAzureCredential()
);

var retrievalRequest = new KnowledgeBaseRetrievalRequest();
retrievalRequest.Intents.Add(
    new KnowledgeRetrievalSemanticIntent(
        "Why is the Phoenix nighttime street grid so sharply visible from space, "
        + "whereas large stretches of the interstate between midwestern cities remain comparatively dim?"
    )
);

var result = await kbClient.RetrieveAsync(retrievalRequest);
Console.WriteLine(
    (result.Value.Response[0].Content[0] as KnowledgeBaseMessageTextContent)!.Text
);
```

**Reference:** [KnowledgeBaseRetrievalClient](/dotnet/api/azure.search.documents.knowledgebases.knowledgebaseretrievalclient?view=azure-dotnet&preserve-view=true), [KnowledgeBaseRetrievalRequest](/dotnet/api/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest?view=azure-dotnet&preserve-view=true)

---

:::zone-end

:::zone pivot="python"

# [2026-08-01-preview](#tab/2026-08-01-preview)

```python
from azure.identity import DefaultAzureCredential
from azure.search.documents.knowledgebases import KnowledgeBaseRetrievalClient
from azure.search.documents.knowledgebases.models import (
    KnowledgeBaseMessage,
    KnowledgeBaseMessageTextContent,
    KnowledgeBaseRetrievalRequest,
    SearchIndexKnowledgeSourceParams,
)

# Create knowledge base retrieval client
kb_client = KnowledgeBaseRetrievalClient(
    endpoint="<search-endpoint>",
    knowledge_base_name="<knowledge-base-name>",
    credential=DefaultAzureCredential(),
)

request = KnowledgeBaseRetrievalRequest(
    messages=[
        KnowledgeBaseMessage(
            role="assistant",
            content=[
                KnowledgeBaseMessageTextContent(
                    text="You can answer questions about the Earth at night. "
                    "Sources have a JSON format with a ref_id that must be cited in the answer. "
                    "If you do not have the answer, respond with 'I do not know'."
                )
            ],
        ),
        KnowledgeBaseMessage(
            role="user",
            content=[
                KnowledgeBaseMessageTextContent(
                    text="Why is the Phoenix nighttime street grid so sharply visible from space, "
                    "whereas large stretches of the interstate between midwestern cities remain comparatively dim?"
                )
            ],
        ),
    ],
    knowledge_source_params=[
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name="earth-at-night-blob-ks",
        )
    ],
)

result = kb_client.retrieve(request)
print(result.response[0].content[0].text)
```

**Reference:** [KnowledgeBaseRetrievalClient](/python/api/azure-search-documents/azure.search.documents.knowledgebases.knowledgebaseretrievalclient), [KnowledgeBaseRetrievalRequest](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest)

# [2026-04-01](#tab/2026-04-01)

```python
from azure.identity import DefaultAzureCredential
from azure.search.documents.knowledgebases import KnowledgeBaseRetrievalClient
from azure.search.documents.knowledgebases.models import (
    KnowledgeRetrievalSemanticIntent,
    KnowledgeBaseRetrievalRequest,
    SearchIndexKnowledgeSourceParams,
)

# Create knowledge base retrieval client
kb_client = KnowledgeBaseRetrievalClient(
    endpoint="<search-endpoint>",
    knowledge_base_name="<knowledge-base-name>",
    credential=DefaultAzureCredential(),
)

request = KnowledgeBaseRetrievalRequest(
    intents=[
        KnowledgeRetrievalSemanticIntent(
            search="Why is the Phoenix nighttime street grid so sharply visible from space, "
            "whereas large stretches of the interstate between midwestern cities remain comparatively dim?"
        )
    ],
    knowledge_source_params=[
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name="earth-at-night-blob-ks",
        )
    ],
)

result = kb_client.retrieve(request)
print(result.response[0].content[0].text)
```

**Reference:** [KnowledgeBaseRetrievalClient](/python/api/azure-search-documents/azure.search.documents.knowledgebases.knowledgebaseretrievalclient), [KnowledgeBaseRetrievalRequest](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest)

---

:::zone-end

:::zone pivot="rest"

# [2026-08-01-preview](#tab/2026-08-01-preview)

```http
@search-endpoint = <search-endpoint> // Example: https://my-service.search.windows.net
@search-access-token = <search-access-token> // Run: az account get-access-token --scope https://search.azure.com/.default --query accessToken -o tsv

POST {{search-endpoint}}/knowledgebases/{{knowledge-base-name}}/retrieve?api-version=2026-08-01-preview
Content-Type: application/json
Authorization: Bearer {{search-access-token}}

{
    "messages": [
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "You can answer questions about the Earth at night. Sources have a JSON format with a ref_id that must be cited in the answer. If you do not have the answer, respond with 'I do not know'."
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Why is the Phoenix nighttime street grid so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?"
                }
            ]
        }
    ],
    "knowledgeSourceParams": [
        {
            "knowledgeSourceName": "earth-at-night-blob-ks",
            "kind": "searchIndex"
        }
    ]
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

# [2026-04-01](#tab/2026-04-01)

```http
@search-endpoint = <search-endpoint> // Example: https://my-service.search.windows.net
@search-access-token = <search-access-token> // Run: az account get-access-token --scope https://search.azure.com/.default --query accessToken -o tsv

POST {{search-endpoint}}/knowledgebases/{{knowledge-base-name}}/retrieve?api-version=2026-04-01
Content-Type: application/json
Authorization: Bearer {{search-access-token}}

{
    "intents": [
        {
            "type": "semantic",
            "search": "Why is the Phoenix nighttime street grid so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?"
        }
    ],
    "knowledgeSourceParams": [
        {
            "knowledgeSourceName": "earth-at-night-blob-ks",
            "kind": "searchIndex"
        }
    ]
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-04-01&preserve-view=true)

---

:::zone-end

### Supply images to answer synthesis (preview)

For [blob](agentic-knowledge-source-how-to-blob.md), [indexed OneLake](agentic-knowledge-source-how-to-onelake.md), and [indexed SharePoint](agentic-knowledge-source-how-to-sharepoint-indexed.md) knowledge sources that you configure with an asset store, you can supply document-embedded images to the downstream answer-synthesis model alongside text. Set `enableImageServing` on the matching entry in `knowledgeSourceParams` to override the default that's set on the knowledge base definition. The retrieve response doesn't include dedicated fields for the individual image paths or image bytes supplied to the model.

Image serving runs only when `outputMode` is `answerSynthesis` and isn't supported for knowledge sources that configure `ingestionPermissionOptions`. For setup steps, the precedence table, and how to inspect image serving statistics, see [Surface document-embedded images in agentic retrieval (preview)](agentic-retrieval-how-to-image-serving.md).

### Disable reranking for a knowledge source (preview)

Starting with the `2026-08-01-preview` API version, set `"resultsProcessing": "none"` on a `knowledgeSourceParams` entry to bypass reranking for a specific knowledge source and preserve its underlying result order. You can also store `resultsProcessing` on the knowledge source as its default. All knowledge source kinds support this property.

The following example bypasses reranking for `product-catalog-ks` on one retrieve request.

:::zone pivot="csharp"

```csharp
using System;
using System.Linq;
using Azure.Identity;
using Azure.Search.Documents.Indexes.Models;
using Azure.Search.Documents.KnowledgeBases;
using Azure.Search.Documents.KnowledgeBases.Models;

var client = new KnowledgeBaseRetrievalClient(
    new Uri("<search-endpoint>"),
    "product-catalog-kb",
    new DefaultAzureCredential());

var request = new KnowledgeBaseRetrievalRequest
{
    IncludeActivity = true
};
request.Intents.Add(
    new KnowledgeRetrievalSemanticIntent(
        "Find the power adapter for SKU 88421."));
request.KnowledgeSourceParams.Add(
    new SearchIndexKnowledgeSourceParams("product-catalog-ks")
    {
        AlwaysQuerySource = true,
        IncludeReferences = true,
        ResultsProcessing = KnowledgeSourceResultsProcessing.None
    });

var result = await client.RetrieveAsync(request);
Console.WriteLine(
    $"References with a reranker score: "
    + $"{result.Value.References.Count(x => x.RerankerScore.HasValue)}");
```

**Reference:** [KnowledgeBaseRetrievalClient](/dotnet/api/azure.search.documents.knowledgebases.knowledgebaseretrievalclient?view=azure-dotnet-preview&preserve-view=true), [SearchIndexKnowledgeSourceParams](/dotnet/api/azure.search.documents.knowledgebases.models.searchindexknowledgesourceparams?view=azure-dotnet-preview&preserve-view=true)

:::zone-end

:::zone pivot="python"

```python
from azure.identity import DefaultAzureCredential
from azure.search.documents.knowledgebases import (
    KnowledgeBaseRetrievalClient,
)
from azure.search.documents.knowledgebases.models import (
    KnowledgeBaseRetrievalRequest,
    KnowledgeRetrievalSemanticIntent,
    SearchIndexKnowledgeSourceParams,
)

client = KnowledgeBaseRetrievalClient(
    endpoint="<search-endpoint>",
    knowledge_base_name="product-catalog-kb",
    credential=DefaultAzureCredential(),
)

request = KnowledgeBaseRetrievalRequest(
    intents=[
        KnowledgeRetrievalSemanticIntent(
            search="Find the power adapter for SKU 88421."
        )
    ],
    include_activity=True,
    knowledge_source_params=[
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name="product-catalog-ks",
            always_query_source=True,
            include_references=True,
            results_processing="none",
        )
    ],
)

result = client.retrieve(request)
reranked_count = sum(
    reference.reranker_score is not None
    for reference in result.references
)
print("References with a reranker score:", reranked_count)
```

**Reference:** [KnowledgeBaseRetrievalClient](/python/api/azure-search-documents/azure.search.documents.knowledgebases.knowledgebaseretrievalclient), [SearchIndexKnowledgeSourceParams](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.searchindexknowledgesourceparams)

:::zone-end

:::zone pivot="rest"

```http
@search-endpoint = <search-endpoint>
@search-access-token = <search-access-token> // Run: az account get-access-token --scope https://search.azure.com/.default --query accessToken -o tsv
@knowledge-base-name = product-catalog-kb

POST {{search-endpoint}}/knowledgebases/{{knowledge-base-name}}/retrieve?api-version=2026-08-01-preview
Content-Type: application/json
Authorization: Bearer {{search-access-token}}

{
  "intents": [
    {
      "type": "semantic",
      "search": "Find the power adapter for SKU 88421."
    }
  ],
  "includeActivity": true,
  "knowledgeSourceParams": [
    {
      "knowledgeSourceName": "product-catalog-ks",
      "kind": "searchIndex",
      "alwaysQuerySource": true,
      "includeReferences": true,
      "resultsProcessing": "none"
    }
  ]
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

:::zone-end

Set `"resultsProcessing": "rerank"`, or omit it when no stored default exists, to use the reranking pipeline. Azure AI Search resolves the effective value for each source in this order:

1. `resultsProcessing` in `knowledgeSourceParams` on the retrieve request.
1. `resultsProcessing` stored on the knowledge source.
1. `rerank` when neither property is present.

For an [MCP server knowledge source](agentic-knowledge-source-how-to-mcp-server.md), a `resultsProcessing` value set on an individual tool takes precedence over the request and stored values.

> [!TIP]
> `resultsProcessing` changes how results are processed, not which sources are queried. Set `alwaysQuerySource` to `true` if the knowledge source must be queried.

When the effective value is `none`:

+ References from the knowledge source omit `rerankerScore`, and results keep their underlying order within the source's retrieval activity.
+ When any source bypasses reranking, Azure AI Search distributes final results across activities in round-robin order, following knowledge source declaration order. Reranked activities stay ordered by score.
+ Deduplication and per-source, document, and token limits still apply, so not every retrieved result appears in the response.

Azure AI Search validates `rerankerThreshold` in this order:

1. Search resolves `resultsProcessing` from the retrieve request and the stored knowledge source value.
1. If the resolved value is `none` and the request includes `rerankerThreshold`, Search returns `400 Bad Request`.
1. For an MCP server tool, Search applies the tool-level `resultsProcessing` value after validating the request.

As a result, an MCP tool setting doesn't change whether the request passes validation. A tool-level `none` value doesn't cause a threshold error, and a tool-level `rerank` value doesn't prevent an error when the request or stored value resolves to `none`.

To confirm which mode ran, check whether the knowledge source's references include `rerankerScore`. Don't rely on `semanticConfigurationName`, which can be `null` rather than omitted.

### Search index behavior

For knowledge sources that target a search index, the implied query type is `semantic`, and there's no search mode. When reranking runs, query execution uses `semanticConfigurationName`. Other source settings, including `searchFields` and `sourceDataFields`, apply in both modes.

Agentic retrieval doesn't accept `scoringProfile` or `scoringParameters` inputs. If you need recency bias for indexed knowledge sources, use [freshness-aware retrieval](agentic-retrieval-how-to-configure-freshness.md) instead of an index scoring profile.

If the index includes vector fields, you need a valid vectorizer definition so the agentic retrieval engine can vectorize query inputs. Otherwise, vector fields are ignored.

For more information, see [Create an index for agentic retrieval](agentic-retrieval-how-to-create-index.md).

## Stream retrieve results (preview)

Starting with the `2026-08-01-preview` API version, you can receive retrieve results as a stream of server-sent events (SSE) instead of waiting for a single JSON response. By using streaming, your client can display the query planning, source activity, and synthesized answer or extracted response in that order as each part becomes available.

:::zone pivot="csharp"

```csharp
using Azure.Identity;
using Azure.Search.Documents.Indexes.Models;
using Azure.Search.Documents.KnowledgeBases;
using Azure.Search.Documents.KnowledgeBases.Models;

var client = new KnowledgeBaseRetrievalClient(
    new Uri("<search-endpoint>"),
    "<knowledge-base-name>",
    new DefaultAzureCredential());

var request = new KnowledgeBaseRetrievalRequest
{
    OutputMode = KnowledgeRetrievalOutputMode.ExtractiveData,
    RetrievalReasoningEffort =
        new KnowledgeRetrievalMinimalReasoningEffort(),
    IncludeActivity = true,
};
request.Intents.Add(
    new KnowledgeRetrievalSemanticIntent("What is the return policy?"));
request.KnowledgeSourceParams.Add(
    new SearchIndexKnowledgeSourceParams(
        "<knowledge-source-name>")
    {
        ResultsProcessing = KnowledgeSourceResultsProcessing.None,
        IncludeReferences = true,
    });

var eventCounts = new Dictionary<string, int>();

await foreach (var item in client.RetrieveStreamAsync(request))
{
    eventCounts.TryGetValue(item.EventType, out var count);
    eventCounts[item.EventType] = count + 1;
}

foreach (var (eventType, count) in eventCounts)
{
    Console.WriteLine($"{eventType}: {count}");
}
```

**Reference:** [KnowledgeBaseRetrievalClient](/dotnet/api/azure.search.documents.knowledgebases.knowledgebaseretrievalclient?view=azure-dotnet-preview&preserve-view=true)

:::zone-end

:::zone pivot="python"

```python
from collections import Counter

from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes.models import (
    KnowledgeSourceResultsProcessing,
)
from azure.search.documents.knowledgebases import (
    KnowledgeBaseRetrievalClient,
)
from azure.search.documents.knowledgebases.models import (
    KnowledgeBaseRetrievalRequest,
    KnowledgeRetrievalMinimalReasoningEffort,
    KnowledgeRetrievalOutputMode,
    KnowledgeRetrievalSemanticIntent,
    SearchIndexKnowledgeSourceParams,
)


client = KnowledgeBaseRetrievalClient(
    endpoint="<search-endpoint>",
    knowledge_base_name="<knowledge-base-name>",
    credential=DefaultAzureCredential(),
)

request = KnowledgeBaseRetrievalRequest(
    intents=[
        KnowledgeRetrievalSemanticIntent(
            search="What is the return policy?"
        )
    ],
    output_mode=KnowledgeRetrievalOutputMode.EXTRACTIVE_DATA,
    retrieval_reasoning_effort=KnowledgeRetrievalMinimalReasoningEffort(),
    include_activity=True,
    knowledge_source_params=[
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name="<knowledge-source-name>",
            results_processing=KnowledgeSourceResultsProcessing.NONE,
            include_references=True,
        )
    ],
)

event_counts = Counter()

with client.retrieve_stream(request) as stream:
    for event in stream:
        event_counts[event.event_type] += 1

for event_type, count in event_counts.items():
    print(f"{event_type}: {count}")
```

**Reference:** [KnowledgeBaseRetrievalClient](/python/api/azure-search-documents/azure.search.documents.knowledgebases.knowledgebaseretrievalclient)

:::zone-end

:::zone pivot="rest"

To opt in to streaming, include the `Accept: text/event-stream` header in a retrieve request. Without this header, the retrieve action returns its standard JSON response.

```http
POST {{search-endpoint}}/knowledgebases/{{knowledge-base-name}}/retrieve?api-version=2026-08-01-preview
Content-Type: application/json
Accept: text/event-stream
Authorization: Bearer {{search-access-token}}

{
    "intents": [
        {
            "type": "semantic",
            "search": "What is the return policy?"
        }
    ],
    "outputMode": "extractiveData",
    "retrievalReasoningEffort": {
        "kind": "minimal"
    },
    "includeActivity": true,
    "knowledgeSourceParams": [
        {
            "knowledgeSourceName": "{{knowledge-source-name}}",
            "kind": "searchIndex",
            "resultsProcessing": "none",
            "includeReferences": true
        }
    ]
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

:::zone-end

### Event lifecycle

Instead of returning a single response, the service keeps one HTTP connection open (content type `text/event-stream; charset=utf-8`) and sends a sequence of events as data becomes available. Each event has an `event:` line that names the event type, a `data:` line with a JSON value, and a blank line that marks the end of the event.

A successful stream uses the following lifecycle:

| Event | When it's sent | What it contains |
| --- | --- | --- |
| `retrieval.started` | First event on every streamed request. | The request ID, knowledge base name, output mode, and effective reasoning effort after the service resolves request and knowledge base defaults. If the effective `kind` is `auto`, the event reports `auto`; it doesn't predict later escalation. |
| `activity.started` | When the service begins a query-planning, source, or model activity. Multiple activities can start before an earlier activity completes. | The activity `id`, `type`, start time, and optional knowledge source name. |
| `activity.completed` | When that activity finishes. Correlate it to its `activity.started` event by matching `id`. | The completed [activity record](#activity-array). |
| `answer.completed` | Once, only when `outputMode` is `answerSynthesis`. | `messageIndex` identifies the message's position in the final response array, and `message` contains the complete synthesized answer. There's no token-by-token delta event. |
| `references.completed` | After all references are resolved. | The event data is the full [references array](#references-array), without an object wrapper. |
| `response.completed` | The terminal event for a successful or partially successful stream. | `200` or `206` status code and the complete retrieve response body, which has the same shape as a non-streaming JSON call. For information about what each status code means, see [Troubleshoot the retrieve action](#troubleshoot-the-retrieve-action). |
| `error` | Instead of `references.completed` and `response.completed` when retrieval fails after the stream opens. | The error and any activity records that completed before the failure. |

Events arrive in order. Each `activity.started` event precedes the `activity.completed` event with the same `id`, but activities can interleave. Completed activity records also include `startedAt` and `completedAt` timestamps. While the stream is idle, the server sends a `: heartbeat` comment approximately every 15 seconds to keep the connection open. SSE clients can ignore these comments.

The following example shows a streamed response, with payloads shortened for readability.

```text
event: retrieval.started
data: {"requestId":"<request-id>","outputMode":"answerSynthesis"}

event: activity.started
data: {"id":0,"type":"searchIndex","startedAt":"<timestamp>"}

: heartbeat

event: activity.completed
data: {"id":0,"startedAt":"<start>","completedAt":"<end>"}

event: answer.completed
data: {"messageIndex":0,"message":{"content":[{"type":"text","text":"..."}]}}

event: references.completed
data: [{"type":"searchIndex","id":"0","activitySource":0}]

event: response.completed
data: {"statusCode":200,"response":{}}
```

### Handle errors, cancellation, and fallback

+ **Preflight failures**: If request validation fails before the stream opens, such as for a malformed request body, the retrieve action returns a standard JSON error response and never opens the stream.

+ **Midstream failures**: If retrieval fails after the stream opens, the terminal event is `error` instead of `references.completed` and `response.completed`. The event can include any activity records that completed before the failure. The HTTP status code remains `200` once the stream starts, so check the terminal event, not the HTTP status code, to determine success.

+ **Cancellation or disconnect**: If your client cancels the request or disconnects before the stream finishes, the service cancels retrieval and ends the stream without a terminal event. Treat any events received before cancellation or disconnect as incomplete.

+ **JSON fallback**: With `2026-08-01-preview`, a missing `Accept` header or a value such as `application/json`, `*/*`, `text/*`, or `text/event-stream;q=0` returns the standard JSON response described in [Review the response](#review-the-response). Requesting `text/event-stream` from an earlier API version returns `406 Not Acceptable`.

## Filter search index knowledge sources at query time

When retrieving from a search index knowledge source, you can apply an [OData filter](search-query-odata-filter.md) at query time to narrow the results to specific documents or fields. The filter expression uses OData syntax and is passed via the `filterAddOn` parameter.

### Filter syntax and examples

The `filterAddOn` parameter accepts OData filter expressions. Example patterns include:

- **Metadata fields**: `city eq 'Phoenix'`, `status eq 'active'`
- **Date ranges**: `publishDate ge 2024-01-01 and publishDate le 2024-12-31`
- **Numeric ranges**: `price ge 100 and price le 5000`
- **Text matching**: `substringof('climate', description)`, `indexof(title, 'urgent') ge 0`
- **Logical operators**: `(category eq 'News' or category eq 'Analysis') and status eq 'published'`

:::zone pivot="csharp"

```csharp
using Azure;
using Azure.Search.Documents.KnowledgeBases;
using Azure.Search.Documents.KnowledgeBases.Models;

var kbClient = new KnowledgeBaseRetrievalClient(
    endpoint: new Uri("<search-endpoint>"),
    knowledgeBaseName: "<knowledge-base-name>",
    credential: new DefaultAzureCredential()
);

var retrievalRequest = new KnowledgeBaseRetrievalRequest();

retrievalRequest.Messages.Add(
    new KnowledgeBaseMessage(
        content: new[] {
            new KnowledgeBaseMessageTextContent(
                "You are a support agent. Answer questions based on published documentation. "
                + "If you don't know the answer, say so."
            )
        }
    ) { Role = "assistant" }
);

retrievalRequest.Messages.Add(
    new KnowledgeBaseMessage(
        content: new[] {
            new KnowledgeBaseMessageTextContent(
                "What is the process for submitting an expense report?"
            )
        }
    ) { Role = "user" }
);

// Apply a filter to search only published documents
var searchIndexParams = new SearchIndexKnowledgeSourceParams(
    knowledgeSourceName: "internal-documentation-ks"
);
searchIndexParams.FilterAddOn = "status eq 'published'";

retrievalRequest.KnowledgeSourceParams.Add(searchIndexParams);

var result = await kbClient.RetrieveAsync(retrievalRequest);
Console.WriteLine(
    (result.Value.Response[0].Content[0] as KnowledgeBaseMessageTextContent)!.Text
);
```

:::zone-end

:::zone pivot="python"

```python
from azure.identity import DefaultAzureCredential
from azure.search.documents.knowledgebases import KnowledgeBaseRetrievalClient
from azure.search.documents.knowledgebases.models import (
    KnowledgeBaseMessage,
    KnowledgeBaseMessageTextContent,
    KnowledgeBaseRetrievalRequest,
    SearchIndexKnowledgeSourceParams,
)

kb_client = KnowledgeBaseRetrievalClient(
    endpoint="<search-endpoint>",
    knowledge_base_name="<knowledge-base-name>",
    credential=DefaultAzureCredential(),
)

request = KnowledgeBaseRetrievalRequest(
    messages=[
        KnowledgeBaseMessage(
            role="assistant",
            content=[
                KnowledgeBaseMessageTextContent(
                    text="You are a support agent. Answer questions based on published documentation. "
                    "If you don't know the answer, say so."
                )
            ],
        ),
        KnowledgeBaseMessage(
            role="user",
            content=[
                KnowledgeBaseMessageTextContent(
                    text="What is the process for submitting an expense report?"
                )
            ],
        ),
    ],
    knowledge_source_params=[
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name="internal-documentation-ks",
            # Apply a filter to search only published documents
            filter_add_on="status eq 'published'",
        )
    ],
)

result = kb_client.retrieve(request)
print(result.response[0].content[0].text)
```

:::zone-end

:::zone pivot="rest"

```http
POST {{search-endpoint}}/knowledgebases/{{knowledge-base-name}}/retrieve?api-version=2026-08-01-preview
Content-Type: application/json
Authorization: Bearer {{search-access-token}}

{
    "messages": [
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "You are a support agent. Answer questions based on published documentation. If you don't know the answer, say so."
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What is the process for submitting an expense report?"
                }
            ]
        }
    ],
    "knowledgeSourceParams": [
        {
            "knowledgeSourceName": "internal-documentation-ks",
            "kind": "searchIndex",
            "filterAddOn": "status eq 'published'"
        }
    ]
}
```

:::zone-end

### Multi-filter example

You can combine multiple filters to further refine results.

:::zone pivot="csharp"

```csharp
searchIndexParams.FilterAddOn = "(status eq 'published' or status eq 'internal') and created ge 2025-01-01";
```

:::zone-end

:::zone pivot="python"

```python
filter_add_on="(status eq 'published' or status eq 'internal') and created ge 2025-01-01"
```

:::zone-end

:::zone pivot="rest"

```json
{
    "knowledgeSourceName": "internal-documentation-ks",
    "kind": "searchIndex",
    "filterAddOn": "(status eq 'published' or status eq 'internal') and created ge 2025-01-01"
}
```

:::zone-end

## Override stored query hints at query time (preview)

Starting with the `2026-08-01-preview` API version, you can override the query hints stored on a search index knowledge source for a single retrieve request by setting `queryHintOverrides` on its `knowledgeSourceParams` entry.

The override replaces the entire stored `queryHints` object rather than merging entry by entry, so include every hint that you want to apply. Omit `queryHintOverrides` to use the stored hints.

When the retrieval reasoning effort isn't `minimal`, an HTTP 400 response depends on the stored filter hints, not the override contents or boost kind. The service validates stored filter hints against the knowledge base model before applying `queryHintOverrides`. Therefore, a GPT-4o or GPT-4.1 family model rejects the request even when the override is empty or contains only boosts. Stored boosts alone don't trigger this validation. Use a compatible model or remove the stored filter hints first.

The following example replaces all stored hints with one `fieldValue` boost for Japanese content. The service doesn't apply any stored filter or other stored boost to this request.

::: zone pivot="csharp"

```csharp
using System;
using Azure.Identity;
using Azure.Search.Documents.Indexes.Models;
using Azure.Search.Documents.KnowledgeBases;
using Azure.Search.Documents.KnowledgeBases.Models;

var endpoint = new Uri("<search-endpoint>");
var retrievalClient = new KnowledgeBaseRetrievalClient(
    endpoint,
    "product-kb",
    new DefaultAzureCredential());

var languageBoost =
    new SearchIndexKnowledgeSourceFieldValueBoost(
        "language",
        2.0);
languageBoost.FieldValues.Add("ja-JP");
var queryHintOverrides =
    new SearchIndexKnowledgeSourceQueryHints();
queryHintOverrides.Boosts.Add(languageBoost);

var request = new KnowledgeBaseRetrievalRequest
{
    RetrievalReasoningEffort =
        new KnowledgeRetrievalLowReasoningEffort(),
    IncludeActivity = true
};
request.Messages.Add(
    new KnowledgeBaseMessage([
        new KnowledgeBaseMessageTextContent(
            "Find Japanese service guidance for Model-X200.")
    ])
    {
        Role = "user"
    });
request.KnowledgeSourceParams.Add(
    new SearchIndexKnowledgeSourceParams(
        "product-docs-ks")
    {
        QueryHintOverrides = queryHintOverrides
    });

var result = await retrievalClient.RetrieveAsync(request);
```

**Reference:** [KnowledgeBaseRetrievalClient](/dotnet/api/azure.search.documents.knowledgebases.knowledgebaseretrievalclient?view=azure-dotnet-preview&preserve-view=true), [SearchIndexKnowledgeSourceParams](/dotnet/api/azure.search.documents.knowledgebases.models.searchindexknowledgesourceparams?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes.models import (
    SearchIndexKnowledgeSourceFieldValueBoost,
    SearchIndexKnowledgeSourceQueryHints,
)
from azure.search.documents.knowledgebases import (
    KnowledgeBaseRetrievalClient,
)
from azure.search.documents.knowledgebases.models import (
    KnowledgeBaseMessage,
    KnowledgeBaseMessageTextContent,
    KnowledgeBaseRetrievalRequest,
    KnowledgeRetrievalLowReasoningEffort,
    SearchIndexKnowledgeSourceParams,
)

retrieval_client = KnowledgeBaseRetrievalClient(
    endpoint="<search-endpoint>",
    credential=DefaultAzureCredential(),
    knowledge_base_name="product-kb",
)

query_hint_overrides = SearchIndexKnowledgeSourceQueryHints(
    boosts=[
        SearchIndexKnowledgeSourceFieldValueBoost(
            field="language",
            field_values=["ja-JP"],
            boost=2.0,
        )
    ]
)

request = KnowledgeBaseRetrievalRequest(
    messages=[
        KnowledgeBaseMessage(
            role="user",
            content=[
                KnowledgeBaseMessageTextContent(
                    text="Find Japanese service guidance for Model-X200."
                )
            ],
        )
    ],
    knowledge_source_params=[
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name="product-docs-ks",
            query_hint_overrides=query_hint_overrides,
        )
    ],
    retrieval_reasoning_effort=(
        KnowledgeRetrievalLowReasoningEffort()
    ),
    include_activity=True,
)

result = retrieval_client.retrieve(request)
```

**Reference:** [KnowledgeBaseRetrievalClient](/python/api/azure-search-documents/azure.search.documents.knowledgebases.knowledgebaseretrievalclient), [SearchIndexKnowledgeSourceParams](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.searchindexknowledgesourceparams)

::: zone-end

::: zone pivot="rest"

```http
POST {{search-endpoint}}/knowledgebases('product-kb')/retrieve?api-version=2026-08-01-preview
Content-Type: application/json
Authorization: Bearer {{search-access-token}}

{
  "messages": [{
    "role": "user",
    "content": [{
      "type": "text",
      "text": "Find Japanese service guidance for Model-X200."
    }]
  }],
  "knowledgeSourceParams": [{
    "knowledgeSourceName": "product-docs-ks",
    "kind": "searchIndex",
    "queryHintOverrides": {
      "boosts": [{
        "kind": "fieldValue",
        "field": "language",
        "fieldValues": ["ja-JP"],
        "boost": 2.0
      }]
    }
  }],
  "retrievalReasoningEffort": {"kind": "low"},
  "includeActivity": true
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

::: zone-end

To confirm that the service applied your override, set `includeActivity` on the request and inspect the returned `searchIndex` activity. Its `queryHintProcessing` object reports what the model generated. For this example, it contains a `generatedBoost` for the language boost, but no `generatedFilter` because the override replaced the stored filter hint. Because query hints are best effort, treat this activity as confirmation rather than checking for an exact expression.

```json
{
  "type": "searchIndex",
  "queryHintProcessing": {
    "generatedBoost": "language:(ja\\-JP)^2"
  },
  "searchIndexArguments": {
    "queryType": "full"
  }
}
```

For the stored definition, supported hint types, and composition with deterministic filters, see [Configure query hints (preview)](agentic-knowledge-source-how-to-search-index.md#configure-query-hints-preview).

## Enforce permissions at query time (preview)

Changes to access permissions that you set outside of `2026-08-01-preview` can take time to appear in `2026-08-01-preview` retrieval results.

If your knowledge sources contain permission-protected content, pass the end user's identity on the retrieve request so that each user sees only content they're authorized to access. For indexed sources, the retrieval engine uses this identity to filter results and returns unfiltered results if it's omitted. Remote sources also use authorization from the retrieve request but enforce permissions at the source and might require a source-specific token and header.

Permissions enforcement has two parts:

- [**Ingestion time**](#ingestion-time-configuration): For indexed knowledge sources only, set `ingestionPermissionOptions` to ingest permission metadata alongside content.

- [**Query time**](#query-time-authorization): Pass the user's authorization in the header required by the knowledge source. Most sources use `x-ms-query-source-authorization`. The exception is Work IQ, which uses `x-ms-query-work-iq-source-authorization`.

### Ingestion-time configuration

The following table shows which knowledge sources require ingestion-time configuration and how each source enforces permissions.

| Knowledge source | Requires `ingestionPermissionOptions` | How permissions are enforced |
| --- | --- | --- |
| [Blob or ADLS Gen2](agentic-knowledge-source-how-to-blob.md) | ✅ | Ingested RBAC scopes, ACLs, or Microsoft Purview matched against user identity. |
| [OneLake](agentic-knowledge-source-how-to-onelake.md) | ✅ | Ingested document Microsoft Purview sensitivity labels matched against user identity. |
| [Indexed SharePoint](agentic-knowledge-source-how-to-sharepoint-indexed.md) | ✅ | Ingested SharePoint ACLs or Microsoft Purview sensitivity labels matched against user identity. |
| [Remote SharePoint](agentic-knowledge-source-how-to-sharepoint-remote.md#assign-to-a-knowledge-base) | ❌ | Copilot Retrieval API queries SharePoint directly using the user's token. |
| [Fabric Data Agent](agentic-knowledge-source-how-to-fabric-data-agent.md#enforce-permissions-at-query-time) | ❌ | The retrieval engine exchanges the user's token for a Microsoft Fabric–scoped token and queries the data agent on their behalf. |
| [Fabric Ontology](agentic-knowledge-source-how-to-fabric-ontology.md#enforce-permissions-at-query-time) | ❌ | The retrieval engine exchanges the user's token for a Microsoft Fabric–scoped token and queries the ontology item on their behalf. |
| [Work IQ](agentic-knowledge-source-how-to-work-iq.md#enforce-permissions-at-query-time) | ❌ | The retrieval engine exchanges an app-audience user assertion from `x-ms-query-work-iq-source-authorization` for a Work IQ–scoped token. |

If you don't configure `ingestionPermissionOptions` when you create the indexed knowledge source, the index doesn't contain permission metadata. The system returns results unfiltered, regardless of the header. To fix this problem, recreate the knowledge source with the appropriate `ingestionPermissionOptions` values.

### Query-time authorization

For non–Work IQ knowledge sources, pass the end user's identity by including an access token scoped to `https://search.azure.com/.default` on the retrieve request. This token is separate from the service credential used to access the search service. It doesn't need search service permissions and only represents the user whose content access is evaluated. For more information, see [Query-time ACL and RBAC enforcement](search-query-access-control-rbac-enforcement.md).

For Work IQ knowledge sources, this section doesn't apply. Use the Work IQ–specific user assertion flow described in [Enforce permissions at query time](agentic-knowledge-source-how-to-work-iq.md#enforce-permissions-at-query-time).

:::zone pivot="csharp"

In the .NET SDK, pass the token as the `querySourceAuthorization` parameter on `RetrieveAsync`:

```csharp
using Azure;
using Azure.Identity;
using Azure.Search.Documents.KnowledgeBases;
using Azure.Search.Documents.KnowledgeBases.Models;

// Service credential: Authenticates to the search service
var serviceCredential = new DefaultAzureCredential();

// User identity token: Represents the end user for document-level permissions filtering
var userTokenContext = new Azure.Core.TokenRequestContext(
    new[] { "https://search.azure.com/.default" }
);
string userToken = (await serviceCredential.GetTokenAsync(userTokenContext)).Token;

// Create the retrieval client with the service credential
var kbClient = new KnowledgeBaseRetrievalClient(
    endpoint: new Uri("<search-endpoint>"),
    knowledgeBaseName: "<knowledge-base-name>",
    credential: serviceCredential
);

var request = new KnowledgeBaseRetrievalRequest();
request.Messages.Add(
    new KnowledgeBaseMessage(
        content: new[] {
            new KnowledgeBaseMessageTextContent(
                "What companies are in the financial sector?")
        }
    ) { Role = "user" }
);

// Pass the user identity token for permissions filtering
var result = await kbClient.RetrieveAsync(
    request, querySourceAuthorization: userToken);

var text = (result.Value.Response[0].Content[0] as KnowledgeBaseMessageTextContent)!.Text;
Console.WriteLine(text);
```

**Reference:** [KnowledgeBaseRetrievalClient](/dotnet/api/azure.search.documents.knowledgebases.knowledgebaseretrievalclient?view=azure-dotnet-preview&preserve-view=true), [KnowledgeBaseRetrievalRequest](/dotnet/api/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest?view=azure-dotnet-preview&preserve-view=true)

:::zone-end

:::zone pivot="python"

In the Python SDK, pass the token as the `query_source_authorization` parameter on `retrieve`:

```python
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.search.documents.knowledgebases import KnowledgeBaseRetrievalClient
from azure.search.documents.knowledgebases.models import (
    KnowledgeBaseMessage, KnowledgeBaseMessageTextContent,
    KnowledgeBaseRetrievalRequest,
)

# Service credential: Authenticates to the search service
service_credential = DefaultAzureCredential()

# User identity token: Represents the end user for document-level permissions filtering
user_token_provider = get_bearer_token_provider(
    service_credential, "https://search.azure.com/.default")
user_token = user_token_provider()

# Create the retrieval client with the service credential
kb_client = KnowledgeBaseRetrievalClient(
    endpoint="<search-endpoint>",
    knowledge_base_name="<knowledge-base-name>",
    credential=service_credential,
)

request = KnowledgeBaseRetrievalRequest(
    messages=[
        KnowledgeBaseMessage(
            role="user",
            content=[KnowledgeBaseMessageTextContent(
                text="What companies are in the financial sector?")],
        )
    ]
)

# Pass the user identity token for permissions filtering
result = kb_client.retrieve(
    retrieval_request=request, query_source_authorization=user_token)
print(result.response[0].content[0].text)
```

**Reference:** [KnowledgeBaseRetrievalClient](/python/api/azure-search-documents/azure.search.documents.knowledgebases.knowledgebaseretrievalclient), [KnowledgeBaseRetrievalRequest](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest)

:::zone-end

:::zone pivot="rest"

In the REST API, include the `x-ms-query-source-authorization` header with the user's access token:

```http
@search-endpoint = <search-endpoint>
@search-access-token = <search-access-token> // Service credential
@user-access-token = <user-access-token> // User identity token

POST {{search-endpoint}}/knowledgebases/{{knowledge-base-name}}/retrieve?api-version=2026-08-01-preview
Authorization: Bearer {{search-access-token}}
Content-Type: application/json
x-ms-query-source-authorization: {{user-access-token}}

{
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What companies are in the financial sector?"
                }
            ]
        }
    ]
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

:::zone-end

## Review the response

The retrieve action returns three main components:

# [2026-08-01-preview](#tab/2026-08-01-preview)

+ [Extracted response](#extracted-response) or [synthesized answer](agentic-retrieval-how-to-answer-synthesis.md) (depending on output mode)
+ [Activity array](#activity-array)
+ [References array](#references-array)

# [2026-04-01](#tab/2026-04-01)

+ [Extracted response](#extracted-response) (`2026-04-01` doesn't support answer synthesis)
+ [Activity array](#activity-array)
+ [References array](#references-array)

---

### Extracted response

The extracted response is a single, unified string that you typically pass to an LLM. The LLM consumes the string as grounding data and uses it to formulate a response. Your API call to the LLM includes the unified string and instructions for the model, such as whether to use the grounding exclusively or as a supplement.

The body of the response is structured in the chat message style format, and the content is serialized JSON.

```json
"response": [
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "[{\"ref_id\":\"0\",\"title\":\"Urban Structure\",\"terms\":\"Location of Phoenix, Grid of City Blocks, Phoenix Metropolitan Area at Night\",\"content\":\"<content chunk redacted>\"}]"
            }
        ]
    }
]
```

Key points:

+ `content.type` has one valid value: `text`.

+ `content.text` is a JSON-encoded string containing the most relevant documents (or chunks) found in the search index, given the query and chat history inputs. This string is your grounding data that an LLM uses to formulate a response to the user's question.

  + This portion of the response consists of 200 chunks or fewer, excluding any results that fail to meet the minimum threshold of a 2.5 reranker score.

  + The string starts with the reference ID of the chunk (used for citation purposes), and any fields specified in the semantic configuration of the target index. In this example, assume the semantic configuration in the target index has a "title" field, a "terms" field, and a "content" field.

+ Retrieve responses don't include `@search.rerankerBoostedScore`.

+ The `maxOutputSizeInTokens` property (`maxOutputSize` in `2026-05-01-preview` and later) on the retrieve request determines the length of the string.

  + A document that exceeds the `maxOutputSizeInTokens` output budget can be omitted from the response. The activity array includes a warning when the most relevant document exceeds the maximum output size. To retain more content, increase `maxOutputSizeInTokens`. For more information, see [Empty responses](#empty-responses).

### Activity array

The activity array outputs the query plan, which provides operational transparency for tracking operations, billing implications, and resource invocations. It also includes subqueries sent to the retrieval pipeline. For a `206 Partial Content` response, the array includes errors for failed knowledge sources. A `502 Bad Gateway` response might provide failure details only in the top-level error.

The activity array includes the following components:

# [2026-08-01-preview](#tab/2026-08-01-preview)

| Section | Description |
| --------- | ------------- |
| Source-specific activity | For each knowledge source included in the query, this section reports on elapsed time and which arguments were used in the query, including semantic ranker. Knowledge source types include `searchIndex`, `azureBlob`, and other [supported knowledge sources](agentic-knowledge-source-overview.md#supported-knowledge-sources). |
| `agenticReasoning` | This section reports on token consumption for agentic reasoning during retrieval, which depends on the specified [retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md). |
| `modelQueryPlanning` | For knowledge bases that use an LLM for query planning, this section reports on the token count used for input and the token count for the subqueries. It includes a `model` field with a `modelName` field containing the public model name, not the deployment name, of the model that ran the activity. |
| `modelAnswerSynthesis` | For knowledge bases that use [answer synthesis](agentic-retrieval-how-to-answer-synthesis.md), this section reports on the token count for formulating the answer and the token count of the answer output. It includes a `model` field with a `modelName` field containing the public model name, not the deployment name, of the model that ran the activity. |
| `modelWebSummarization` | For knowledge bases that use web summarization, this section reports on token consumption for summarizing web results. It includes a `model` field with a `modelName` field containing the public model name, not the deployment name, of the model that ran the activity. |
| `model` | For model-backed activity records, this section identifies the model used to perform the activity. This section appears only when you set `includeActivity` to `true`. |
| `imageServing` | For knowledge sources that have [image serving](agentic-retrieval-how-to-image-serving.md) enabled, this section reports `imagesRetrieved`, `imagesSentToModel`, `totalImageSizeBytes`, and whether indexing-time `verbalizationUsed` was on. Inspect `verbalizationUsed` and `imagesSentToModel` independently. A response can report `verbalizationUsed` as `true` and still send images to the downstream model. To find the number of dropped images, subtract `imagesSentToModel` from `imagesRetrieved`. |

# [2026-04-01](#tab/2026-04-01)

| Section | Description |
| --- | --- |
| Source-specific activity | For each knowledge source included in the query, this section reports on elapsed time and which arguments were used in the query, including semantic ranker. Knowledge source types include `searchIndex`, `azureBlob`, and other [supported knowledge sources](agentic-knowledge-source-overview.md#supported-knowledge-sources). |
| `agenticReasoning` | This section reports on token consumption for agentic reasoning during retrieval. |

---

The following example shows the activity array.

# [2026-08-01-preview](#tab/2026-08-01-preview)

```json
  "activity": [
    {
      "type": "modelQueryPlanning",
      "id": 0,
      "inputTokens": 2302,
      "outputTokens": 109,
      "elapsedMs": 2396
    },
    {
      "type": "searchIndex",
      "id": 1,
      "knowledgeSourceName": "demo-financials-ks",
      "queryTime": "2025-11-04T19:25:23.683Z",
      "count": 26,
      "elapsedMs": 1137,
      "searchIndexArguments": {
        "search": "List of companies in the financial sector according to SEC GICS classification",
        "filter": null,
        "sourceDataFields": [ ],
        "searchFields": [ ],
        "semanticConfigurationName": "en-semantic-config"
      }
    },
    {
      "type": "searchIndex",
      "id": 2,
      "knowledgeSourceName": "demo-healthcare-ks",
      "queryTime": "2025-11-04T19:25:24.186Z",
      "count": 17,
      "elapsedMs": 494,
      "searchIndexArguments": {
        "search": "List of companies in the financial sector according to SEC GICS classification",
        "filter": null,
        "sourceDataFields": [ ],
        "searchFields": [ ],
        "semanticConfigurationName": "en-semantic-config"
      }
    },
    {
      "type": "agenticReasoning",
      "id": 3,
      "retrievalReasoningEffort": {
        "kind": "low"
      },
      "reasoningTokens": 103368
    },
    {
      "type": "modelAnswerSynthesis",
      "id": 4,
      "inputTokens": 5821,
      "outputTokens": 344,
      "elapsedMs": 3837
    }
  ]
```

# [2026-04-01](#tab/2026-04-01)

```json
  "activity": [
    {
      "type": "searchIndex",
      "id": 0,
      "knowledgeSourceName": "demo-financials-ks",
      "queryTime": "2025-11-04T19:25:23.683Z",
      "count": 26,
      "elapsedMs": 1137,
      "searchIndexArguments": {
        "search": "List of companies in the financial sector according to SEC GICS classification",
        "filter": null,
        "sourceDataFields": [ ],
        "searchFields": [ ],
        "semanticConfigurationName": "en-semantic-config"
      }
    },
    {
      "type": "searchIndex",
      "id": 1,
      "knowledgeSourceName": "demo-healthcare-ks",
      "queryTime": "2025-11-04T19:25:24.186Z",
      "count": 17,
      "elapsedMs": 494,
      "searchIndexArguments": {
        "search": "List of companies in the financial sector according to SEC GICS classification",
        "filter": null,
        "sourceDataFields": [ ],
        "searchFields": [ ],
        "semanticConfigurationName": "en-semantic-config"
      }
    },
    {
      "type": "agenticReasoning",
      "id": 2,
      "reasoningTokens": 103368
    }
  ]
```

---

### References array

The references array comes directly from the underlying grounding data. It includes the `sourceData` used to generate the response and consists of every document the agentic retrieval engine finds and semantically ranks.

The references array includes the following components:

# [2026-08-01-preview](#tab/citation-2026-08-01-preview)

| Field | Description |
| --- | --- |
| `type` | The knowledge source type that produced the reference, such as `searchIndex`. |
| `id` | The reference ID for an item within a response. It's not the document key in the search index. Use it to provide citations. |
| `activitySource` | Cross-references the `id` of the activity entry that produced the reference, which is useful for citation linking. |
| `docKey` | For an indexed reference, the document key in the backing search index. |
| `sourceData` | The grounding data used to generate the response. For an indexed reference, fields can include an `id` and semantic fields, such as `title`, `terms`, and `content`. The shape varies by reference type. |
| `citationUrl` (preview) | A service-generated, read-only URL that resolves to the reference's document in the backing index. Returned only for [indexed knowledge sources](agentic-knowledge-source-overview.md#indexed-knowledge-sources). To follow the URL, see [Look up documents with citation URLs (preview)](#look-up-documents-with-citation-urls-preview). |

# [2026-04-01](#tab/citation-2026-04-01)

| Field | Description |
| --- | --- |
| `type` | The knowledge source type that produced the reference, such as `searchIndex`. |
| `id` | The reference ID for an item within a response. It's not the document key in the search index. Use it to provide citations. |
| `activitySource` | Cross-references the `id` of the activity entry that produced the reference, which is useful for citation linking. |
| `docKey` | For an indexed reference, the document key in the backing search index. |
| `sourceData` | The grounding data used to generate the response. For an indexed reference, fields can include an `id` and semantic fields, such as `title`, `terms`, and `content`. The shape varies by reference type. |

---

The following example shows the references array.

# [2026-08-01-preview](#tab/citation-2026-08-01-preview)

```json
  "references": [
    {
      "type": "searchIndex",
      "id": "0",
      "activitySource": 2,
      "docKey": "policy=aug-2026",
      "citationUrl": "https://my-search-service.search.windows.net/indexes/my-index/docs/policy%3Daug-2026?$select=title%2Ccontent%2Ccategory%2Cid%2Clanguage&api-version=2026-08-01-preview",
      "sourceData": null
    },
    {
      "type": "searchIndex",
      "id": "1",
      "activitySource": 2,
      "docKey": "2",
      "citationUrl": "https://my-search-service.search.windows.net/indexes/my-index/docs/2?$select=title%2Ccontent%2Ccategory%2Cid%2Clanguage&api-version=2026-08-01-preview",
      "sourceData": null
    }
  ]
```

# [2026-04-01](#tab/citation-2026-04-01)

```json
  "references": [
    {
      "type": "searchIndex",
      "id": "0",
      "activitySource": 2,
      "docKey": "earth_at_night_508_page_104_verbalized",
      "sourceData": null
    },
    {
      "type": "searchIndex",
      "id": "1",
      "activitySource": 2,
      "docKey": "earth_at_night_508_page_105_verbalized",
      "sourceData": null
    }
  ]
```

---

### Look up documents with citation URLs (preview)

Starting with the `2026-08-01-preview` API version, a reference from an indexed knowledge source can include a `citationUrl` in the retrieve response. Use this URL to fetch the indexed fields for that reference, such as `title` and `content`, so you can render a citation preview showing where an answer came from without opening the original source document. The `citationUrl` is an authenticated lookup into the backing index, separate from the source `docUrl` and `blobUrl`.

The following example shows a sanitized citation URL.

```json
"citationUrl": "https://my-search-service.search.windows.net/indexes/my-index/docs/policy%3Daug-2026?$select=title%2Ccontent%2Ccategory%2Cid%2Clanguage&api-version=2026-08-01-preview"
```

The selected fields and their order depend on the indexed source and retrieval configuration.

> [!IMPORTANT]
> Follow the complete URL from the response verbatim and render the returned JSON fields in your app. Don't construct, parse, or normalize the URL.

Given a citation URL, the following examples get an access token for the search service. They call the URL with that token in the `Authorization` header. The signed-in identity needs the **Search Index Data Reader** role.

Azure AI Search SDK document lookup methods require the endpoint, index name, document key, selected fields, and API version as separate inputs. They don't accept an absolute citation URL. These examples use an authenticated HTTP GET to preserve the complete service-generated URL.

:::zone pivot="csharp"

```csharp
using System;
using System.Net.Http;
using System.Net.Http.Headers;
using Azure.Core;
using Azure.Identity;

// citationUrl comes from a retrieve response
string citationUrl = "<citation-url>";

var credential = new DefaultAzureCredential();
AccessToken token = await credential.GetTokenAsync(
    new TokenRequestContext(
        new[] { "https://search.azure.com/.default" }));

using var httpClient = new HttpClient();
httpClient.DefaultRequestHeaders.Authorization =
    new AuthenticationHeaderValue("Bearer", token.Token);

string document = await httpClient.GetStringAsync(citationUrl);
Console.WriteLine(document);
```

**Reference:** [DefaultAzureCredential](/dotnet/api/azure.identity.defaultazurecredential?view=azure-dotnet&preserve-view=true)

:::zone-end

:::zone pivot="python"

```python
import json
from urllib.request import Request, urlopen

from azure.identity import DefaultAzureCredential

# citation_url comes from a retrieve response
citation_url = "<citation-url>"

credential = DefaultAzureCredential()
token = credential.get_token("https://search.azure.com/.default")
document_request = Request(
    citation_url,
    headers={"Authorization": f"Bearer {token.token}"},
)
with urlopen(document_request) as response:
    document = json.load(response)

print(json.dumps(document, indent=2))
```

**Reference:** [DefaultAzureCredential](/python/api/azure-identity/azure.identity.defaultazurecredential)

:::zone-end

:::zone pivot="rest"

```http
GET {{citation-url}}
Authorization: Bearer {{search-access-token}}
```

**Reference:** [Documents - Get](/rest/api/searchservice/documents/get?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

:::zone-end

The document lookup returns the selected index fields as JSON:

```json
{
  "id": "policy=aug-2026",
  "title": "Escaped citation key",
  "content": "Citation interoperability uses an escaped document key for the August preview.",
  "category": "release",
  "language": "en-US"
}
```

When you consume a citation URL, keep the following in mind:

+ Check for `citationUrl` before you render a citation. It can be absent if the response omits references or the service can't resolve the backing index or document key.

+ If the retrieve request includes `x-ms-query-source-authorization` for document-level access control, use the same user token when you follow the URL.

+ The URL remains valid only while the backing index and document key remain unchanged.

## Inspect sensitivity label metadata in the response (preview)

The same timing behavior described in [Enforce permissions at query time](#enforce-permissions-at-query-time-preview) applies here: changes to access permissions that you set outside of `2026-08-01-preview` can take time to appear in `2026-08-01-preview` retrieve responses.

When you query a knowledge base that ingests [Microsoft Purview sensitivity labels](search-indexer-sensitivity-labels.md), the retrieve response includes label metadata at two levels:

| Location | Field | Description |
| --- | --- | --- |
| Per reference | `sensitivityLabelInfo` | The sensitivity label applied to each document returned in the `references` array. |
| Response | `metadata.responseSensitivityLabelInfo` | An aggregate label that represents the highest-priority sensitivity label across all referenced documents in the response. Useful for client-side display banners and policy enforcement. |

Microsoft Graph computes the response-level label from the per-reference labels using the [Microsoft Purview label inheritance rules](/purview/sensitivity-labels). Typically, the most restrictive label wins.

The following example shows a retrieve response with two referenced documents (one `Confidential`, one `Internal`) and the resulting response-level label.

```json
{
  "response": [
    {
      "role": "assistant",
      "content": [
        { "type": "text", "text": "[ ... grounding data ... ]" }
      ]
    }
  ],
  "references": [
    {
      "type": "azureBlob",
      "id": "0",
      "activitySource": 1,
      "docKey": "contract-2026.pdf",
      "sensitivityLabelInfo": {
        "labelId": "<label-guid>",
        "labelName": "Confidential",
        "color": "#FF0000",
        "tooltip": "Confidential — Recipients can read but not forward.",
        "isEncrypted": true,
        "priority": 3
      },
      "sourceData": null
    },
    {
      "type": "azureBlob",
      "id": "1",
      "activitySource": 1,
      "docKey": "policy-overview.pdf",
      "sensitivityLabelInfo": {
        "labelId": "<label-guid>",
        "labelName": "Internal",
        "color": "#FFA500",
        "tooltip": "For internal use only.",
        "isEncrypted": false,
        "priority": 1
      },
      "sourceData": null
    }
  ],
  "metadata": {
    "responseSensitivityLabelInfo": {
      "labelId": "<label-guid>",
      "labelName": "Confidential",
      "color": "#FF0000",
      "tooltip": "Confidential — Recipients can read but not forward.",
      "isEncrypted": true,
      "priority": 3
    }
  }
}
```

### Reference types that surface sensitivity labels

The field name and availability of label metadata depend on the knowledge source type that produced each reference.

| Reference `type` | Label field | Available when... |
| --- | --- | --- |
| `azureBlob` | `sensitivityLabelInfo` | The blob knowledge source includes `sensitivityLabel` in `ingestionPermissionOptions`. |
| `indexedOneLake` | `sensitivityLabelInfo` | The OneLake knowledge source includes `sensitivityLabel` in `ingestionPermissionOptions`. |
| `indexedSharePoint` | `sensitivityLabelInfo` | The SharePoint-indexed knowledge source includes `sensitivityLabel` in `ingestionPermissionOptions`. |
| `searchIndex` | `sensitivityLabelInfo` | The underlying index has `purviewEnabled` set to `true` and a field marked with `sensitivityLabel: true`. |

### Display and audit recommendations

- Use `sensitivityLabelInfo.labelId` to look up the full label definition through the [Microsoft Graph sensitivity label APIs](/graph/api/sensitivitylabel-get) when you need additional properties, such as policy controls or permissions.

- Use `metadata.responseSensitivityLabelInfo` to render a response-level sensitivity banner or apply policy controls, such as disabling copy and share, across the answer.

- If your knowledge source points to a chunked index, such as one populated through integrated vectorization or a custom Text Split skill, make sure the skillset [projects the sensitivity label to each chunk row](search-indexer-sensitivity-labels.md#6-configure-index-projections-in-your-skillset-if-applicable). Without this mapping, chunk-level references aren't filtered correctly at query time.

- For auditable administrative access to labeled content, see [Elevated read for administrative investigations](search-query-sensitivity-labels.md#elevated-read-for-administrative-investigations-preview).

### MCP server behavior

The MCP endpoint exposed by each knowledge base surfaces the same sensitivity label fields as the REST API. When an MCP-compatible client invokes the `knowledge_base_retrieve` tool, the tool result contains the same per-reference `sensitivityLabelInfo` and response-level `metadata.responseSensitivityLabelInfo` documented earlier in this section. MCP clients enforce label-aware display and policy controls based on these fields.

## Retrieve action examples (preview)

The following examples show different ways to call the retrieve action by using the `2026-08-01-preview` API version. This version supports the full feature set, including answer synthesis and a configurable reasoning effort. For `2026-04-01` usage, see the previous sections.

+ [Inspect model names in activity logs](#inspect-model-names-in-activity-logs)
+ [Require a knowledge source to succeed](#require-a-knowledge-source-to-succeed)
+ [Exclude a knowledge source from a request](#exclude-a-knowledge-source-from-a-request)
+ [Tune candidate documents per knowledge source](#tune-candidate-documents-per-knowledge-source)
+ [Limit final grounding documents](#limit-final-grounding-documents)
+ [Verify knowledge base retrieve defaults](#verify-knowledge-base-retrieve-defaults)
+ [Override default reasoning effort and set request limits](#override-default-reasoning-effort-and-set-request-limits)
+ [Let the service choose the reasoning effort](#let-the-service-choose-the-reasoning-effort)
+ [Set references for each knowledge source](#set-references-for-each-knowledge-source)
+ [Use minimal reasoning effort](#use-minimal-reasoning-effort)

### Inspect model names in activity logs

Set `includeActivity` to `true` to return model identity fields in model-backed activity records. Use these fields to confirm which configured model handled query planning, answer synthesis, or web summarization during a retrieve request. The following example overrides the stored result processing for the selected source on the request.

:::zone pivot="csharp"

```csharp
using Azure.Identity;
using Azure.Search.Documents.Indexes.Models;
using Azure.Search.Documents.KnowledgeBases;
using Azure.Search.Documents.KnowledgeBases.Models;

var kbClient = new KnowledgeBaseRetrievalClient(
    new Uri("<search-endpoint>"),
    "<knowledge-base-name>",
    new DefaultAzureCredential()
);

var retrievalRequest = new KnowledgeBaseRetrievalRequest();
retrievalRequest.Messages.Add(
    new KnowledgeBaseMessage(
        content: new[]
        {
            new KnowledgeBaseMessageTextContent(
                "Which policy applies to returns?"
            )
        }
    ) { Role = "user" }
);
retrievalRequest.IncludeActivity = true;
retrievalRequest.KnowledgeSourceParams.Add(
    new SearchIndexKnowledgeSourceParams(
        "<knowledge-source-name>"
    )
    {
        ResultsProcessing = KnowledgeSourceResultsProcessing.None
    }
);

var result = await kbClient.RetrieveAsync(retrievalRequest);
foreach (var activity in result.Value.Activity)
{
    KnowledgeBaseActivityRecordModel? model = activity switch
    {
        KnowledgeBaseModelQueryPlanningActivityRecord queryPlanning =>
            queryPlanning.Model,
        KnowledgeBaseModelAnswerSynthesisActivityRecord answerSynthesis =>
            answerSynthesis.Model,
        KnowledgeBaseModelWebSummarizationActivityRecord webSummarization =>
            webSummarization.Model,
        _ => null
    };

    if (model is not null)
    {
        Console.WriteLine(
            $"modelName={model.ModelName}, deploymentId={model.DeploymentId}");
    }
}
```

**Reference:** [KnowledgeBaseRetrievalClient](/dotnet/api/azure.search.documents.knowledgebases.knowledgebaseretrievalclient?view=azure-dotnet-preview&preserve-view=true), [KnowledgeBaseRetrievalRequest](/dotnet/api/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest?view=azure-dotnet-preview&preserve-view=true)

:::zone-end

:::zone pivot="python"

```python
from azure.identity import DefaultAzureCredential
from azure.search.documents.knowledgebases import (
    KnowledgeBaseRetrievalClient,
)
from azure.search.documents.knowledgebases.models import (
    KnowledgeBaseMessage,
    KnowledgeBaseMessageTextContent,
    KnowledgeBaseModelAnswerSynthesisActivityRecord,
    KnowledgeBaseModelQueryPlanningActivityRecord,
    KnowledgeBaseModelWebSummarizationActivityRecord,
    KnowledgeBaseRetrievalRequest,
    SearchIndexKnowledgeSourceParams,
)

kb_client = KnowledgeBaseRetrievalClient(
    "<search-endpoint>",
    DefaultAzureCredential(),
    knowledge_base_name="<knowledge-base-name>",
)

model_activity_types = (
    KnowledgeBaseModelQueryPlanningActivityRecord,
    KnowledgeBaseModelAnswerSynthesisActivityRecord,
    KnowledgeBaseModelWebSummarizationActivityRecord,
)

request = KnowledgeBaseRetrievalRequest(
    messages=[
        KnowledgeBaseMessage(
            role="user",
            content=[
                KnowledgeBaseMessageTextContent(
                    text="Which policy applies to returns?"
                )
            ],
        )
    ],
    include_activity=True,
    knowledge_source_params=[
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name="<knowledge-source-name>",
            results_processing="none",
        )
    ],
)

result = kb_client.retrieve(request)
for entry in result.activity or []:
    if isinstance(entry, model_activity_types) and entry.model:
        print(
            "modelName=", entry.model.model_name,
            "deploymentId=", entry.model.deployment_id,
        )
```

**Reference:** [KnowledgeBaseRetrievalClient](/python/api/azure-search-documents/azure.search.documents.knowledgebases.knowledgebaseretrievalclient?view=azure-python-preview&preserve-view=true), [KnowledgeBaseRetrievalRequest](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest?view=azure-python-preview&preserve-view=true)

:::zone-end

:::zone pivot="rest"

```http
POST {{search-endpoint}}/knowledgebases/{{knowledge-base-name}}/retrieve?api-version=2026-08-01-preview
Authorization: Bearer {{search-access-token}}
Content-Type: application/json

{
    "messages": [
        {
            "role": "user",
            "content": [
                { "type": "text", "text": "Which policy applies to returns?" }
            ]
        }
    ],
    "includeActivity": true,
    "knowledgeSourceParams": [
        {
            "knowledgeSourceName": "{{knowledge-source-name}}",
            "kind": "searchIndex",
            "resultsProcessing": "none"
        }
    ]
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

:::zone-end

The following response excerpt shows the nested model identity:

```json
{
  "activity": [
    {
      "type": "modelQueryPlanning",
      "id": 0,
      "model": {
        "modelName": "gpt-5-mini",
        "deploymentId": "gpt-5-mini-deployment"
      },
      "inputTokens": 1842,
      "outputTokens": 87,
      "elapsedMs": 1923
    },
    {
      "type": "searchIndex",
      "id": 1,
      "knowledgeSourceName": "operations-ks",
      "count": 12,
      "elapsedMs": 234
    },
    {
      "type": "modelAnswerSynthesis",
      "id": 2,
      "model": {
        "modelName": "gpt-5-mini",
        "deploymentId": "gpt-5-mini-deployment"
      },
      "inputTokens": 2418,
      "outputTokens": 179,
      "elapsedMs": 931
    }
  ]
}
```

### Require a knowledge source to succeed

Set `failOnError` in `knowledgeSourceParams` to mark a knowledge source as required. Use this parameter when a partial answer would be misleading or noncompliant if that source is unavailable. The request returns `502 Bad Gateway` if a required source fails, even if another source succeeds. For handling guidance, see [Troubleshoot the retrieve action](#troubleshoot-the-retrieve-action).

:::zone pivot="csharp"

```csharp
var retrievalRequest = new KnowledgeBaseRetrievalRequest();
retrievalRequest.Messages.Add(
    new KnowledgeBaseMessage(
        content: new[] {
            new KnowledgeBaseMessageTextContent("Which HR policy applies?")
        }
    ) { Role = "user" }
);
retrievalRequest.KnowledgeSourceParams.Add(
    new SearchIndexKnowledgeSourceParams("hr-policy-ks")
    {
        FailOnError = true,
        AlwaysQuerySource = true
    }
);
retrievalRequest.KnowledgeSourceParams.Add(
    new SearchIndexKnowledgeSourceParams("hr-faq-ks")
);

var result = await kbClient.RetrieveAsync(retrievalRequest);
```

**Reference:** [SearchIndexKnowledgeSourceParams](/dotnet/api/azure.search.documents.knowledgebases.models.searchindexknowledgesourceparams?view=azure-dotnet-preview&preserve-view=true)

:::zone-end

:::zone pivot="python"

```python
request = KnowledgeBaseRetrievalRequest(
    messages=[
        KnowledgeBaseMessage(
            role="user",
            content=[KnowledgeBaseMessageTextContent(text="Which HR policy applies?")],
        )
    ],
    knowledge_source_params=[
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name="hr-policy-ks",
            fail_on_error=True,
            always_query_source=True,
        ),
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name="hr-faq-ks",
        ),
    ],
)

result = kb_client.retrieve(request)
```

**Reference:** [SearchIndexKnowledgeSourceParams](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.searchindexknowledgesourceparams)

:::zone-end

:::zone pivot="rest"

```http
POST {{search-endpoint}}/knowledgebases/{{knowledge-base-name}}/retrieve?api-version=2026-08-01-preview
Authorization: Bearer {{search-access-token}}
Content-Type: application/json

{
    "messages": [
        {
            "role": "user",
            "content": [
                { "type": "text", "text": "Which HR policy applies?" }
            ]
        }
    ],
    "knowledgeSourceParams": [
        {
            "knowledgeSourceName": "hr-policy-ks",
            "kind": "searchIndex",
            "failOnError": true,
            "alwaysQuerySource": true
        },
        {
            "knowledgeSourceName": "hr-faq-ks",
            "kind": "searchIndex"
        }
    ]
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

:::zone-end

### Exclude a knowledge source from a request

Starting with the `2026-08-01-preview` API version, set `neverQuerySource` to `true` for each knowledge source you want to exclude from a retrieve request. Request-time `neverQuerySource` overrides a stored `alwaysQuerySource` value for that request without changing the stored value.

The following example queries a knowledge base that contains `product-docs-ks` and `troubleshooting-ks`, excluding `troubleshooting-ks` from the request.

:::zone pivot="csharp"

```csharp
var retrievalRequest = new KnowledgeBaseRetrievalRequest();
retrievalRequest.Messages.Add(
    new KnowledgeBaseMessage(
        content: new[] {
            new KnowledgeBaseMessageTextContent(
                "Explain the official SSO provisioning steps.")
        }
    ) { Role = "user" }
);
retrievalRequest.KnowledgeSourceParams.Add(
    new SearchIndexKnowledgeSourceParams("product-docs-ks")
);
retrievalRequest.KnowledgeSourceParams.Add(
    new SearchIndexKnowledgeSourceParams("troubleshooting-ks")
    {
        NeverQuerySource = true
    }
);

var result = await kbClient.RetrieveAsync(retrievalRequest);
```

**Reference:** [SearchIndexKnowledgeSourceParams](/dotnet/api/azure.search.documents.knowledgebases.models.searchindexknowledgesourceparams?view=azure-dotnet-preview&preserve-view=true)

:::zone-end

:::zone pivot="python"

```python
request = KnowledgeBaseRetrievalRequest(
    messages=[
        KnowledgeBaseMessage(
            role="user",
            content=[
                KnowledgeBaseMessageTextContent(
                    text="Explain the official SSO provisioning steps."
                )
            ],
        )
    ],
    knowledge_source_params=[
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name="product-docs-ks",
        ),
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name="troubleshooting-ks",
            never_query_source=True,
        ),
    ],
)

result = kb_client.retrieve(request)
```

**Reference:** [SearchIndexKnowledgeSourceParams](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.searchindexknowledgesourceparams)

:::zone-end

:::zone pivot="rest"

```http
POST {{search-endpoint}}/knowledgebases/{{knowledge-base-name}}/retrieve?api-version=2026-08-01-preview
Authorization: Bearer {{search-access-token}}
Content-Type: application/json

{
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Explain the official SSO provisioning steps."
                }
            ]
        }
    ],
    "knowledgeSourceParams": [
        {
            "knowledgeSourceName": "product-docs-ks",
            "kind": "searchIndex"
        },
        {
            "knowledgeSourceName": "troubleshooting-ks",
            "kind": "searchIndex",
            "neverQuerySource": true
        }
    ]
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

:::zone-end

### Tune candidate documents per knowledge source

Set `maxOutputDocuments` in `knowledgeSourceParams` to cap how many candidate documents a specific knowledge source contributes before final result selection. Use this parameter when you want to bound one source's input to the pipeline without affecting others.

:::zone pivot="csharp"

```csharp
var retrievalRequest = new KnowledgeBaseRetrievalRequest();
retrievalRequest.Messages.Add(
    new KnowledgeBaseMessage(
        content: new[] {
            new KnowledgeBaseMessageTextContent("What safety procedures apply?")
        }
    ) { Role = "user" }
);
retrievalRequest.KnowledgeSourceParams.Add(
    new SearchIndexKnowledgeSourceParams("operations-ks")
    {
        MaxOutputDocuments = 50
    }
);

var result = await kbClient.RetrieveAsync(retrievalRequest);
```

**Reference:** [SearchIndexKnowledgeSourceParams](/dotnet/api/azure.search.documents.knowledgebases.models.searchindexknowledgesourceparams?view=azure-dotnet-preview&preserve-view=true)

:::zone-end

:::zone pivot="python"

```python
request = KnowledgeBaseRetrievalRequest(
    messages=[
        KnowledgeBaseMessage(
            role="user",
            content=[KnowledgeBaseMessageTextContent(text="What safety procedures apply?")],
        )
    ],
    knowledge_source_params=[
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name="operations-ks",
            max_output_documents=50,
        ),
    ],
)

result = kb_client.retrieve(request)
```

**Reference:** [SearchIndexKnowledgeSourceParams](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.searchindexknowledgesourceparams)

:::zone-end

:::zone pivot="rest"

```http
POST {{search-endpoint}}/knowledgebases/operations-kb/retrieve?api-version=2026-08-01-preview
Authorization: Bearer {{search-access-token}}
Content-Type: application/json

{
    "messages": [
        {
            "role": "user",
            "content": [
                { "type": "text", "text": "What safety procedures apply?" }
            ]
        }
    ],
    "knowledgeSourceParams": [
        {
            "knowledgeSourceName": "operations-ks",
            "kind": "searchIndex",
            "maxOutputDocuments": 50
        }
    ]
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

:::zone-end


### Limit final grounding documents

The top-level `maxOutputDocuments` parameter caps how many grounding documents are returned in the final retrieve response. Use this parameter when your application needs a predictable citation or reference count.

:::zone pivot="csharp"

```csharp
var retrievalRequest = new KnowledgeBaseRetrievalRequest();
retrievalRequest.Messages.Add(
    new KnowledgeBaseMessage(
        content: new[] {
            new KnowledgeBaseMessageTextContent("What is the return policy?")
        }
    ) { Role = "user" }
);
retrievalRequest.OutputMode = "extractedData";
retrievalRequest.MaxOutputDocuments = 3;
retrievalRequest.MaxOutputSizeInTokens = 6000;

var result = await kbClient.RetrieveAsync(retrievalRequest);
```

**Reference:** [KnowledgeBaseRetrievalRequest](/dotnet/api/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest?view=azure-dotnet-preview&preserve-view=true)

:::zone-end

:::zone pivot="python"

```python
request = KnowledgeBaseRetrievalRequest(
    messages=[
        KnowledgeBaseMessage(
            role="user",
            content=[KnowledgeBaseMessageTextContent(text="What is the return policy?")],
        )
    ],
    output_mode="extractedData",
    max_output_documents=3,
    max_output_size_in_tokens=6000,
)

result = kb_client.retrieve(request)
```

**Reference:** [KnowledgeBaseRetrievalRequest](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest)

:::zone-end

:::zone pivot="rest"

```http
POST {{search-endpoint}}/knowledgebases/{{knowledge-base-name}}/retrieve?api-version=2026-08-01-preview
Authorization: Bearer {{search-access-token}}
Content-Type: application/json

{
    "messages": [
        {
            "role": "user",
            "content": [
                { "type": "text", "text": "What is the return policy?" }
            ]
        }
    ],
    "outputMode": "extractedData",
    "maxOutputDocuments": 3,
    "maxOutputSizeInTokens": 6000
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

:::zone-end

The following table shows how `maxOutputDocuments` and `maxOutputSizeInTokens` interact across all four combinations.

| `maxOutputDocuments` | `maxOutputSizeInTokens` | Behavior |
| --- | --- | --- |
| Unspecified | Unspecified | Uses the default `maxOutputSizeInTokens` response limit behavior. |
| Unspecified | Specified | Discards documents once the payload-size limit is reached. |
| Specified | Unspecified | Returns up to the specified number of grounding documents and doesn't apply a `maxOutputSizeInTokens` limit. |
| Specified | Specified | Returns up to `maxOutputDocuments` documents or however many documents fit under `maxOutputSizeInTokens`, whichever limit applies first. |

### Verify knowledge base retrieve defaults

A knowledge base can store request-wide defaults in `retrieveDefaults`. Send two retrieve requests to verify inheritance and request-specific overrides.

Before you begin, complete [Configure default retrieve limits (preview)](agentic-retrieval-how-to-create-knowledge-base.md#configure-default-retrieve-limits-preview). The first request omits all three request-wide limits, so the stored values of 45 seconds, eight documents, and 12,000 tokens apply. The second request overrides them with 20 seconds, one document, and 5,000 tokens.

::: zone pivot="csharp"

```csharp
using System;
using Azure.Identity;
using Azure.Search.Documents;
using Azure.Search.Documents.KnowledgeBases;
using Azure.Search.Documents.KnowledgeBases.Models;

string searchEndpoint = "<search-endpoint>";

var options = new SearchClientOptions(
    SearchClientOptions.ServiceVersion.V2026_08_01_Preview);
var kbClient = new KnowledgeBaseRetrievalClient(
    new Uri(searchEndpoint),
    "your-knowledge-base",
    new DefaultAzureCredential(),
    options);

KnowledgeBaseRetrievalRequest CreateRequest()
{
    var request = new KnowledgeBaseRetrievalRequest();
    request.Intents.Add(new KnowledgeRetrievalSemanticIntent(
        "Summarize the latest support guidance."));
    return request;
}

var inherited = await kbClient.RetrieveAsync(CreateRequest());
Console.WriteLine(
    $"Stored defaults: {inherited.Value.References.Count} references");

KnowledgeBaseRetrievalRequest overriddenRequest = CreateRequest();
overriddenRequest.MaxRuntimeInSeconds = 20;
overriddenRequest.MaxOutputDocuments = 1;
overriddenRequest.MaxOutputSize = 5000;

var overridden = await kbClient.RetrieveAsync(overriddenRequest);
Console.WriteLine(
    $"Request overrides: {overridden.Value.References.Count} references");
```

**Reference:** [KnowledgeBaseRetrievalClient](/dotnet/api/azure.search.documents.knowledgebases.knowledgebaseretrievalclient?view=azure-dotnet-preview&preserve-view=true), [KnowledgeBaseRetrievalRequest](/dotnet/api/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
from azure.identity import DefaultAzureCredential
from azure.search.documents.knowledgebases import KnowledgeBaseRetrievalClient
from azure.search.documents.knowledgebases.models import (
    KnowledgeBaseRetrievalRequest,
    KnowledgeRetrievalSemanticIntent,
)

kb_client = KnowledgeBaseRetrievalClient(
    endpoint="<search-endpoint>",
    knowledge_base_name="your-knowledge-base",
    credential=DefaultAzureCredential(),
    api_version="2026-08-01-preview",
)


def create_request(**limits):
    return KnowledgeBaseRetrievalRequest(
        intents=[
            KnowledgeRetrievalSemanticIntent(
                search="Summarize the latest support guidance.",
            )
        ],
        **limits,
    )


inherited = kb_client.retrieve(create_request())
print(f"Stored defaults: {len(inherited.references or [])} references")

overridden = kb_client.retrieve(
    create_request(
        max_runtime_in_seconds=20,
        max_output_documents=1,
        max_output_size=5000,
    )
)
print(f"Request overrides: {len(overridden.references or [])} references")
```

**Reference:** [KnowledgeBaseRetrievalClient](/python/api/azure-search-documents/azure.search.documents.knowledgebases.knowledgebaseretrievalclient), [KnowledgeBaseRetrievalRequest](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest)

::: zone-end

::: zone pivot="rest"

First, send a request that omits the three request-wide limit fields.

```http
POST {{search-endpoint}}/knowledgebases/your-knowledge-base/retrieve?api-version=2026-08-01-preview
Content-Type: application/json
Authorization: Bearer {{search-access-token}}

{
  "intents": [
    {
      "type": "semantic",
      "search": "Summarize the latest support guidance."
    }
  ]
}
```

Next, override all three values for one request.

```http
POST {{search-endpoint}}/knowledgebases/your-knowledge-base/retrieve?api-version=2026-08-01-preview
Content-Type: application/json
Authorization: Bearer {{search-access-token}}

{
  "intents": [
    {
      "type": "semantic",
      "search": "Summarize the latest support guidance."
    }
  ],
  "maxRuntimeInSeconds": 20,
  "maxOutputDocuments": 1,
  "maxOutputSize": 5000
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

::: zone-end

The reference count shows whether the stored or request-level `maxOutputDocuments` value applies: the first response contains at most eight references, and the second contains at most one. A response can contain fewer references when fewer documents match. The response doesn't report the effective runtime or output token budget, but those values still govern request processing. Request overrides don't change the stored defaults.

### Override default reasoning effort and set request limits

The following example specifies [answer synthesis](agentic-retrieval-how-to-answer-synthesis.md), so the retrieval reasoning effort must be `low` or `medium`. It also sets `maxRuntimeInSeconds` to limit retrieval runtime and `maxOutputSizeInTokens` to limit response payload size.

`maxRuntimeInSeconds` accepts values from 10 through 600 seconds and defaults to 90 seconds. The 600-second (10-minute) maximum applies only to the Azure AI Search retrieve request.

:::zone pivot="csharp"

```csharp
var retrievalRequest = new KnowledgeBaseRetrievalRequest();
retrievalRequest.Messages.Add(
    new KnowledgeBaseMessage(
        content: new[] {
            new KnowledgeBaseMessageTextContent("What companies are in the financial sector?")
        }
    ) { Role = "user" }
);
retrievalRequest.RetrievalReasoningEffort = new KnowledgeRetrievalLowReasoningEffort();
retrievalRequest.OutputMode = "answerSynthesis";
retrievalRequest.MaxRuntimeInSeconds = 30;
retrievalRequest.MaxOutputSizeInTokens = 6000;

var result = await kbClient.RetrieveAsync(retrievalRequest);
Console.WriteLine(
    (result.Value.Response[0].Content[0] as KnowledgeBaseMessageTextContent)!.Text
);
```

**Reference:** [KnowledgeBaseRetrievalClient](/dotnet/api/azure.search.documents.knowledgebases.knowledgebaseretrievalclient?view=azure-dotnet-preview&preserve-view=true), [KnowledgeBaseRetrievalRequest](/dotnet/api/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest?view=azure-dotnet-preview&preserve-view=true)

:::zone-end

:::zone pivot="python"

```python
from azure.search.documents.knowledgebases.models import (
    KnowledgeRetrievalLowReasoningEffort,
    KnowledgeRetrievalOutputMode,
)

request = KnowledgeBaseRetrievalRequest(
    messages=[
        KnowledgeBaseMessage(
            role="user",
            content=[KnowledgeBaseMessageTextContent(text="What companies are in the financial sector?")],
        )
    ],
    retrieval_reasoning_effort=KnowledgeRetrievalLowReasoningEffort(),
    output_mode=KnowledgeRetrievalOutputMode.ANSWER_SYNTHESIS,
    max_runtime_in_seconds=30,
    max_output_size_in_tokens=6000,
)

result = kb_client.retrieve(request)
print(result.response[0].content[0].text)
```

**Reference:** [KnowledgeBaseRetrievalClient](/python/api/azure-search-documents/azure.search.documents.knowledgebases.knowledgebaseretrievalclient), [KnowledgeBaseRetrievalRequest](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest)

:::zone-end

:::zone pivot="rest"

```http
POST {{search-endpoint}}/knowledgebases/kb-override/retrieve?api-version=2026-08-01-preview
Authorization: Bearer {{search-access-token}}
Content-Type: application/json

{
    "messages": [
        {
            "role": "user",
            "content": [
                { "type": "text", "text": "What companies are in the financial sector?" }
            ]
        }
    ],
    "retrievalReasoningEffort": { "kind": "low" },
    "outputMode": "answerSynthesis",
    "maxRuntimeInSeconds": 30,
    "maxOutputSizeInTokens": 6000
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

:::zone-end

### Let the service choose the reasoning effort

Set `retrievalReasoningEffort.kind` to `auto` in a retrieve request to override the knowledge base default. For more information about automatic reasoning, see [Set the retrieval reasoning effort (preview)](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md).

```json
{
  "retrievalReasoningEffort": {
    "kind": "auto"
  }
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

### Set references for each knowledge source

Use `includeReferences` and `includeReferenceSourceData` in `knowledgeSourceParams` to control which sources appear in the references array and how much source data each entry includes. The following example uses the knowledge base's default reasoning effort.

:::zone pivot="csharp"

```csharp
var retrievalRequest = new KnowledgeBaseRetrievalRequest();
retrievalRequest.Messages.Add(
    new KnowledgeBaseMessage(
        content: new[] {
            new KnowledgeBaseMessageTextContent("What companies are in the financial sector?")
        }
    ) { Role = "user" }
);
retrievalRequest.IncludeActivity = true;
retrievalRequest.KnowledgeSourceParams.Add(
    new SearchIndexKnowledgeSourceParams("demo-financials-ks")
    {
        IncludeReferences = true,
        IncludeReferenceSourceData = true
    }
);

retrievalRequest.KnowledgeSourceParams.Add(
    new SearchIndexKnowledgeSourceParams("demo-communicationservices-ks")
    {
        IncludeReferences = false,
        IncludeReferenceSourceData = false
    }
);

retrievalRequest.KnowledgeSourceParams.Add(
    new SearchIndexKnowledgeSourceParams("demo-healthcare-ks")
    {
        IncludeReferences = true,
        IncludeReferenceSourceData = false,
        AlwaysQuerySource = true
    }
);

var result = await kbClient.RetrieveAsync(retrievalRequest);
Console.WriteLine(
    (result.Value.Response[0].Content[0] as KnowledgeBaseMessageTextContent)!.Text
);
```

**Reference:** [KnowledgeBaseRetrievalClient](/dotnet/api/azure.search.documents.knowledgebases.knowledgebaseretrievalclient?view=azure-dotnet-preview&preserve-view=true), [KnowledgeBaseRetrievalRequest](/dotnet/api/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest?view=azure-dotnet-preview&preserve-view=true)

:::zone-end

:::zone pivot="python"

```python
from azure.search.documents.knowledgebases.models import SearchIndexKnowledgeSourceParams

request = KnowledgeBaseRetrievalRequest(
    messages=[
        KnowledgeBaseMessage(
            role="user",
            content=[KnowledgeBaseMessageTextContent(text="What companies are in the financial sector?")],
        )
    ],
    include_activity=True,
    knowledge_source_params=[
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name="demo-financials-ks",
            include_references=True,
            include_reference_source_data=True,
        ),
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name="demo-communicationservices-ks",
            include_references=False,
            include_reference_source_data=False,
        ),
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name="demo-healthcare-ks",
            include_references=True,
            include_reference_source_data=False,
            always_query_source=True,
        ),
    ],
)

result = kb_client.retrieve(request)
print(result.response[0].content[0].text)
```

**Reference:** [KnowledgeBaseRetrievalClient](/python/api/azure-search-documents/azure.search.documents.knowledgebases.knowledgebaseretrievalclient), [SearchIndexKnowledgeSourceParams](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.searchindexknowledgesourceparams)

:::zone-end

:::zone pivot="rest"

```http
POST {{search-endpoint}}/knowledgebases/kb-medium-example/retrieve?api-version=2026-08-01-preview
Authorization: Bearer {{search-access-token}}
Content-Type: application/json

{
    "messages": [
        {
            "role": "user",
            "content": [
                { "type": "text", "text": "What companies are in the financial sector?" }
            ]
        }
    ],
    "includeActivity": true,
    "knowledgeSourceParams": [
        {
            "knowledgeSourceName": "demo-financials-ks",
            "kind": "searchIndex",
            "includeReferences": true,
            "includeReferenceSourceData": true
        },
        {
            "knowledgeSourceName": "demo-communicationservices-ks",
            "kind": "searchIndex",
            "includeReferences": false,
            "includeReferenceSourceData": false
        },
        {
            "knowledgeSourceName": "demo-healthcare-ks",
            "kind": "searchIndex",
            "includeReferences": true,
            "includeReferenceSourceData": false,
            "alwaysQuerySource": true
        }
    ]
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

:::zone-end


### Use minimal reasoning effort

In the following example, there's no LLM for intelligent query planning or answer synthesis. The query string goes to the agentic retrieval engine for keyword search or hybrid search.

:::zone pivot="csharp"

```csharp
var retrievalRequest = new KnowledgeBaseRetrievalRequest();
retrievalRequest.Intents.Add(
    new KnowledgeRetrievalSemanticIntent("what is a brokerage")
);

var result = await kbClient.RetrieveAsync(retrievalRequest);
Console.WriteLine(
    (result.Value.Response[0].Content[0] as KnowledgeBaseMessageTextContent)!.Text
);
```

**Reference:** [KnowledgeBaseRetrievalClient](/dotnet/api/azure.search.documents.knowledgebases.knowledgebaseretrievalclient?view=azure-dotnet&preserve-view=true), [KnowledgeBaseRetrievalRequest](/dotnet/api/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest?view=azure-dotnet&preserve-view=true)

:::zone-end

:::zone pivot="python"

```python
from azure.search.documents.knowledgebases.models import (
    KnowledgeBaseRetrievalRequest,
    KnowledgeRetrievalSemanticIntent,
)

request = KnowledgeBaseRetrievalRequest(
    intents=[
        KnowledgeRetrievalSemanticIntent(
            search="what is a brokerage",
        )
    ]
)

result = kb_client.retrieve(request)
print(result.response[0].content[0].text)
```

**Reference:** [KnowledgeBaseRetrievalClient](/python/api/azure-search-documents/azure.search.documents.knowledgebases.knowledgebaseretrievalclient), [KnowledgeBaseRetrievalRequest](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest)

:::zone-end

:::zone pivot="rest"

```http
POST {{search-endpoint}}/knowledgebases/kb-minimal/retrieve?api-version=2026-08-01-preview
Authorization: Bearer {{search-access-token}}
Content-Type: application/json

{
    "intents": [
        {
            "type": "semantic",
            "search": "what is a brokerage"
        }
    ]
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

:::zone-end

## Troubleshoot the retrieve action

In `2026-08-01-preview`, the response status indicates whether retrieval succeeded, partly succeeded, or failed, and what to do next. Use the following table to map each status to its meaning, and then see the corresponding section for troubleshooting guidance.

| Status | Meaning |
| --- | --- |
| `200 OK` | Retrieval succeeded. A document can still be omitted if its content exceeds the output budget. For more information, see [Empty responses](#empty-responses). |
| [`400 Bad Request`](#400-bad-request) | The retrieve request failed validation before retrieval began. |
| [`206 Partial Content`](#206-partial-content) | At least one source succeeded, and no failed source is marked [`failOnError`](#require-a-knowledge-source-to-succeed). The response contains results from the sources that succeeded. |
| [`502 Bad Gateway`](#502-bad-gateway) | Every selected source failed, or a source marked `failOnError: true` failed. |

For any non-`200` response, record the API version, timestamp, sanitized request body, response headers, and request or correlation ID. These details help you diagnose the failure and share the issue with support, if necessary.

### `400 Bad Request`

Use the top-level error to identify the invalid request property. Common causes include:

+ A `knowledgeSourceName` in `knowledgeSourceParams` isn't attached to the knowledge base, or its `kind` doesn't match the attached source.
+ A request value is outside its supported range, or one option requires another option that isn't enabled. For example, `includeReferenceSourceData` requires `includeReferences`.
+ `retrievalReasoningEffort.kind` is `auto`, but the request uses an API version earlier than `2026-08-01-preview`.
+ The request uses `auto`, `low`, or `medium`, but the knowledge base doesn't define a model.
+ For [request-time source exclusion (preview)](#exclude-a-knowledge-source-from-a-request), the same entry sets both `alwaysQuerySource` and `neverQuerySource` to `true`, or every attached knowledge source is excluded.

Before you retry the request, correct the property identified by the top-level error.

### `206 Partial Content`

Inspect each [`activity`](#activity-array) entry that contains an `error`. A source retrieval activity identifies the failed knowledge source, and a model activity identifies the failed processing stage. The response body still contains the results that succeeded.

For source retrieval activity errors, common causes include:

+ Invalid query-time input, such as a malformed [`filterAddOn`](#filter-search-index-knowledge-sources-at-query-time) expression.
+ Knowledge source or index configuration drift, such as a renamed field, missing [semantic configuration](semantic-how-to-configure.md), or invalid [vectorizer](vector-search-how-to-configure-vectorizer.md).
+ Missing or invalid dependency authorization, or insufficient [permissions](#enforce-permissions-at-query-time-preview) for the identity used to query the source.
+ Dependency [throttling](search-limits-quotas-capacity.md), timeout, or transient availability failures.

For a model activity error, use the activity `type` to identify the failed processing stage. For example, a `modelWebSummarization` error indicates that [web result summarization](agentic-knowledge-source-how-to-web.md) failed.

If your application permits partial results, process the successful results and record each failed source or model stage. Correct configuration, authorization, and permission errors before you retry. For throttling, timeout, or transient availability failures, use bounded retries with backoff.

If results are unsafe without a specific source and its source type supports [`alwaysQuerySource`](#require-a-knowledge-source-to-succeed), set both `alwaysQuerySource` and `failOnError`. The first option ensures the source is selected, and the second returns a hard error if querying it fails. [MCP server knowledge sources](agentic-knowledge-source-how-to-mcp-server.md) don't support `alwaysQuerySource`; for those sources, `failOnError` applies only when the source is selected. `failOnError` doesn't apply to model activity failures.

### `502 Bad Gateway`

The top-level error describes one of two hard-failure paths:

+ **Every selected source failed:** Each selected source returned an error. A source that completes successfully with zero matching documents isn't a failed source. Inspect every source failure for a shared configuration, authorization, dependency, or availability issue.
+ **A `failOnError` source failed:** A required source couldn't be queried. Other sources might have succeeded, but the service doesn't return a partial result because the required source failed.

The underlying source failures are generally the same kinds as those described for `206 Partial Content`: invalid source-specific input, source or index configuration drift, dependency authorization or permissions, throttling, timeouts, or transient dependency availability.

A hard `502` response might omit the `activity` array and provide the source name and underlying failure only in the top-level error message. Correct configuration, authorization, and permission errors before you retry. Use bounded retries with backoff only for throttling, timeout, or transient availability failures. Don't interpret a `502 Bad Gateway` response as an Azure AI Search outage without examining the underlying source failure.

### Empty responses

The search step might find a document, but the service can still omit it from the final response if its grounded content exceeds the `maxOutputSizeInTokens` output budget (`maxOutputSize` in `2026-05-01-preview` and later). When this condition occurs, the activity array shows that matches were found, and the activity record includes a warning that the most relevant document exceeded the maximum output size. The references array and grounded response content are empty for that document. To retain more content, increase `maxOutputSizeInTokens`.

To avoid this behavior, index large source documents as smaller chunks with stable identifiers and source metadata. This applies especially to long manuals, policies, or knowledge base articles.

## Call the MCP endpoint

> [!IMPORTANT]
> MCP implementations are susceptible to risks, such as attacks, cascading failures, and loss of human oversight. You can mitigate these risks by vetting MCP servers for security and reliability, following [Microsoft's recommended practices](/azure/api-management/secure-mcp-servers) and [industry best practices](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices), and implementing approval mechanisms and monitoring cascading behaviors.

[MCP](https://modelcontextprotocol.io/) is an open protocol that standardizes how AI applications connect to external data sources and tools.

In Azure AI Search, each knowledge base is a standalone MCP server that exposes the `knowledge_base_retrieve` tool. Any MCP-compatible client, including [Foundry Agent Service](/azure/ai-foundry/agents/overview), [GitHub Copilot](https://github.com/features/copilot), [Claude](https://claude.ai), and [Cursor](https://cursor.com), can invoke this tool to query the knowledge base.

### Authenticate to the MCP endpoint

Each knowledge base has an MCP endpoint at the following URL:

```
https://<search-service-name>.search.windows.net/knowledgebases/<knowledge-base-name>/mcp?api-version=<api-version>
```

The API version you specify determines what the connection returns. By using `2026-08-01-preview`, the knowledge base returns synthesized answers when the underlying knowledge base is configured with an LLM and a compatible reasoning effort. By using `2026-04-01`, retrieval is always minimal and extractive, and the connection returns grounding data only.

How you authenticate to this endpoint depends on your MCP client. When you use the Azure OpenAI Responses API with the `knowledge_base_retrieve` MCP tool, you authenticate both the Responses API call to Azure OpenAI and the MCP request to Azure AI Search. If your MCP client calls this endpoint directly, you authenticate only to Azure AI Search.

For Azure AI Search authentication, use one of the following methods:

+ [Pass a bearer token](#use-a-bearer-token-for-mcp-authentication) in the `Authorization` header (recommended)
+ [Pass an admin key](#use-an-admin-key-for-mcp-authentication) in the `api-key` header

> [!NOTE]
> MCP clients configure custom headers differently. For example, [Foundry Agent Service](/azure/ai-foundry/agents/how-to/foundry-iq-connect) injects headers through project connections, while clients such as [GitHub Copilot](https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp/extend-copilot-chat-with-mcp) require headers in MCP server JSON.

### Use a bearer token for MCP authentication

The recommended method for MCP authentication is a bearer token, which avoids storing sensitive keys in configuration files. The identity behind the token must have the **Search Index Data Reader** role assigned on the search service. For more information, see [Connect your app to Azure AI Search using identities](search-security-rbac-client-code.md).

:::zone pivot="csharp"

```csharp
#pragma warning disable OPENAI001

using Azure.AI.OpenAI;
using Azure.Core;
using Azure.Identity;
using OpenAI.Responses;
using System;
using System.Collections.Generic;

string openAiEndpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT")!; // Example: https://<resource-name>.openai.azure.com
string mcpServerUrl = Environment.GetEnvironmentVariable("AZURE_SEARCH_MCP_ENDPOINT")!; // Example: https://<search-service-name>.search.windows.net/knowledgebases/<knowledge-base-name>/mcp?api-version=<api-version>
DefaultAzureCredential credential = new();

// Create the Azure OpenAI Responses client
AzureOpenAIClient azureClient = new(new Uri(openAiEndpoint), credential);
ResponsesClient openAIClient = azureClient.GetResponsesClient();

// Get a bearer token for Azure AI Search
string searchToken = credential.GetToken(
    new TokenRequestContext(new[] { "https://search.azure.com/.default" })
).Token;

// Configure the MCP tool for knowledge base retrieval
McpTool mcpTool = ResponseTool.CreateMcpTool(
    serverLabel: "search_kb",
    serverUri: new Uri(mcpServerUrl),
    headers: new Dictionary<string, string>
    {
        ["Authorization"] = $"Bearer {searchToken}",
    },
    allowedTools: new McpToolFilter { ToolNames = { "knowledge_base_retrieve" } },
    toolCallApprovalPolicy: new McpToolCallApprovalPolicy(
        GlobalMcpToolCallApprovalPolicy.NeverRequireApproval)
);

// Build the response request with the MCP tool attached
CreateResponseOptions options = new()
{
    Model = "MODEL_NAME",
    InputItems =
    {
        ResponseItem.CreateUserMessageItem(
            "What causes the strongest nighttime brightness patterns in this dataset?")
    },
    Tools = { mcpTool }
};

ResponseResult response = await openAIClient.CreateResponseAsync(options);
Console.WriteLine(response.GetOutputText());
```

**Reference:** [Use the Azure OpenAI Responses API](/azure/foundry/openai/how-to/responses?tabs=csharp#authentication)

:::zone-end

:::zone pivot="python"

```python
import os
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI

openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"] # Example: https://<resource-name>.openai.azure.com
mcp_server_url = os.environ["AZURE_SEARCH_MCP_ENDPOINT"] # Example: https://<search-service-name>.search.windows.net/knowledgebases/<knowledge-base-name>/mcp?api-version=<api-version>
credential = DefaultAzureCredential()

# Create token providers for Azure OpenAI and Azure AI Search
openai_token_provider = get_bearer_token_provider(
    credential, "https://cognitiveservices.azure.com/.default"
)
search_token_provider = get_bearer_token_provider(
    credential, "https://search.azure.com/.default"
)

# Create the Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=openai_endpoint,
    azure_ad_token_provider=openai_token_provider,
    api_version=os.environ["OPENAI_API_VERSION"], # Example: 2025-04-01-preview
)

# Create a response using the MCP tool configuration
response = client.responses.create(
    model="MODEL_NAME",
    input="What causes the strongest nighttime brightness patterns in this dataset?",
    tools=[
        {
            "type": "mcp",
            "server_label": "search_kb",
            "server_url": mcp_server_url,
            "allowed_tools": ["knowledge_base_retrieve"],
            "headers": {
                "Authorization": f"Bearer {search_token_provider()}"
            },
            "require_approval": "never",
        }
    ],
)

print(response.output_text)
```

**Reference:** [Use the Azure OpenAI Responses API](/azure/foundry/openai/how-to/responses?tabs=python#authentication)

:::zone-end

:::zone pivot="rest"

```http
// This code snippet is currently unavailable.
```

:::zone-end

### Use an admin key for MCP authentication

An admin key grants full read-write access to the search service, so use it only in development environments or when a bearer token isn't available. For more information, see [Connect to Azure AI Search using API keys](search-security-api-keys.md).

> [!TIP]
> The following example shows only the header that differs from the bearer token example. For the full setup, see [Use a bearer token for MCP authentication](#use-a-bearer-token-for-mcp-authentication).

:::zone pivot="csharp"

```csharp
#pragma warning disable OPENAI001

using OpenAI.Responses;
using System;
using System.Collections.Generic;

string mcpServerUrl = Environment.GetEnvironmentVariable("AZURE_SEARCH_MCP_ENDPOINT")!; // Example: https://<search-service-name>.search.windows.net/knowledgebases/<knowledge-base-name>/mcp?api-version=<api-version>
string searchAdminKey = Environment.GetEnvironmentVariable("AZURE_SEARCH_ADMIN_KEY")!; // Example: <search-api-key>

McpTool mcpTool = ResponseTool.CreateMcpTool(
    serverLabel: "search_kb",
    serverUri: new Uri(mcpServerUrl),
    headers: new Dictionary<string, string> { ["api-key"] = searchAdminKey },
    allowedTools: new McpToolFilter { ToolNames = { "knowledge_base_retrieve" } },
    toolCallApprovalPolicy: new McpToolCallApprovalPolicy(
        GlobalMcpToolCallApprovalPolicy.NeverRequireApproval)
);
```

**Reference:** [Use the Azure OpenAI Responses API](/azure/foundry/openai/how-to/responses?tabs=csharp#authentication)

:::zone-end

:::zone pivot="python"

```python
import os

mcp_server_url = os.environ["AZURE_SEARCH_MCP_ENDPOINT"] # Example: https://<search-service-name>.search.windows.net/knowledgebases/<knowledge-base-name>/mcp?api-version=<api-version>
search_admin_key = os.environ["AZURE_SEARCH_ADMIN_KEY"] # Example: <search-api-key>

tools = [
    {
        "type": "mcp",
        "server_label": "search_kb",
        "server_url": mcp_server_url,
        "allowed_tools": ["knowledge_base_retrieve"],
        "headers": {"api-key": search_admin_key},
        "require_approval": "never",
    }
]
```

**Reference:** [Use the Azure OpenAI Responses API](/azure/foundry/openai/how-to/responses?tabs=python#authentication)

:::zone-end

:::zone pivot="rest"

```http
// This code snippet is currently unavailable.
```

:::zone-end

## Review the MCP response

When an MCP client invokes `knowledge_base_retrieve`, it receives an MCP tool result instead of the retrieve action's `response`, `activity`, and `references` envelope. Many MCP clients surface that tool result under a top-level `result` object, so the payload you should expect is `result.content[]`.

```json
{
  "result": {
    "content": [
      {
        "type": "text",
        "text": "[{\"ref_id\":\"0\",\"title\":\"Urban Structure\",\"terms\":\"Location of Phoenix, Grid of City Blocks, Phoenix Metropolitan Area at Night\",\"content\":\"<content chunk redacted>\"}]"
      }
    ]
  }
}
```

Key points:

+ `result.content[]` contains the MCP tool output returned by the knowledge base.

+ `result.content[].type` is `text`.

+ `result.content[].text` contains the retrieved grounding data as a JSON-encoded string.

+ Unlike the retrieve action, the current MCP response doesn't return separate `activity` or `references` arrays, and it doesn't populate `resource` entries for the returned content.

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [Query-time ACL and RBAC enforcement](search-query-access-control-rbac-enforcement.md)
+ [Use a blob indexer or knowledge source to ingest RBAC scopes metadata](search-blob-indexer-role-based-access.md)
+ [Agentic RAG: Build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)
+ [Azure OpenAI demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
