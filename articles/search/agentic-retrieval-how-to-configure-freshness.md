---
title: Configure freshness-aware retrieval
description: Learn how to configure freshness-aware retrieval for indexed knowledge sources in Azure AI Search using a preview API.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 05/15/2026
ai-usage: ai-assisted
---

# Configure freshness-aware retrieval in Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Freshness-aware retrieval lets an indexed knowledge source prefer newer
content during retrieval. In the `2026-05-01-preview` API, the knowledge
source can include a freshness policy so Azure AI Search biases ranking
toward recent documents without requiring callers to send custom ranking
logic on each retrieve request.

Freshness is a ranking bias, not a hard filter. Older documents can still
appear when they're strongly relevant to the query.

## Prerequisites

+ An Azure AI Search service that supports the `2026-05-01-preview` REST API
  or an equivalent preview SDK.

+ An ingestion-type knowledge source, such as an Azure Blob knowledge source,
  that creates and maintains an Azure AI Search index.

+ Permission to create or update knowledge sources and query the associated
  [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

## When to enable freshness-aware retrieval

Enable freshness-aware retrieval when newer content is generally more useful
or trustworthy than older content. Common examples include release notes,
policy updates, runbooks, service advisories, and operational guidance.

Don't use freshness as a replacement for filtering. If a query must only
return content from a specific date range, use a filter in the retrieval
request or knowledge source configuration instead.

## Configure the freshness policy

Add a freshness policy to the indexed knowledge source definition. The
preview contract uses the policy to apply a recency-aware ranking signal
while preserving the rest of the retrieval pipeline.

The following example shows an Azure Blob knowledge source with a freshness
policy:

```http
PUT {{search-url}}/knowledgesources/news-articles-ks?api-version=2026-05-01-preview
Content-Type: application/json
api-key: {{search-api-key}}

{
  "name": "news-articles-ks",
  "kind": "azureBlob",
  "description": "A knowledge source for recent news articles.",
  "azureBlobParameters": {
    "connectionString": "{{blob-connection-string}}",
    "containerName": "news",
    "ingestionParameters": {
      "freshnessPolicy": {
        "boostingDuration": "P90D"
      }
    }
  }
}
```

The freshness policy is part of the source ingestion parameters. For the
preview, the service maps source modification metadata to a generated
`Edm.DateTimeOffset` freshness field in the underlying index. The generated
field is filterable, retrievable, and sortable. The `boostingDuration` value
uses the same ISO 8601 duration format as scoring profile freshness functions,
such as `P90D` for 90 days.

## Validate ranking behavior

After you update the knowledge source, run queries that can return both recent
and older content. A successful configuration surfaces newer relevant
documents earlier without turning retrieval into a simple date sort.

Use the following validation workflow:

1. Run a retrieve request before enabling freshness-aware retrieval and save
   the references returned by the response.
1. Enable the freshness policy on the indexed knowledge source.
1. Run the same retrieve request again.
1. Compare the reference order and verify that recent, relevant documents move
   higher in the result set.

If ranking doesn't change as expected, inspect the freshness field in the
underlying index. Missing, stale, or inconsistent date values reduce the
quality of the freshness signal.

## Understand interaction with scoring profiles

Freshness-aware retrieval builds on Azure AI Search ranking behavior instead
of replacing relevance scoring. The final ranking still considers query
relevance, configured retrieval settings, and other ranking signals.

In this preview, freshness-aware retrieval is implemented with an Azure AI
Search scoring profile that applies a freshness function to the generated
freshness field. The scoring profile influences the initial ranking set before
semantic reranking, so freshness complements query relevance instead of
replacing it. Existing knowledge sources that don't have the generated
freshness field continue to work, but the freshness scoring profile isn't
applied until the source is recreated or updated to produce that field.

## Related content

+ [Create an Azure Blob knowledge source](agentic-knowledge-source-how-to-blob.md)
+ [Query a knowledge base using the retrieve action or MCP endpoint](agentic-retrieval-how-to-retrieve.md)
+ [Add scoring profiles to boost search scores](index-add-scoring-profiles.md)
+ [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true)
