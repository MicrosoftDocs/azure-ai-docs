---
title: Configure Freshness-Aware Retrieval
description: Learn how to configure freshness-aware retrieval for indexed knowledge sources in Azure AI Search using a preview API.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 06/02/2026
ai-usage: ai-assisted
zone_pivot_groups: search-csharp-python-rest
---

# Configure freshness-aware retrieval in Azure AI Search (preview)

> [!IMPORTANT]
> These features and functionality are part of the 2026-05-01-preview REST API. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

Freshness-aware retrieval lets an indexed knowledge source prefer newer
content during retrieval. The knowledge source can include a freshness
policy so Azure AI Search biases ranking toward recent documents without
requiring callers to send custom ranking logic on each retrieve request.

Freshness is a ranking bias, not a hard filter. Older documents can still
appear when they're strongly relevant to the query.

## Prerequisites

+ An ingestion-type knowledge source, such as an Azure Blob knowledge source,
  that creates and maintains an Azure AI Search index.

+ A [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md) that
  references the knowledge source.

+ Permission to create and use objects on Azure AI Search. We recommend [role-based access](search-security-rbac.md), but you can use [API keys](search-security-api-keys.md) if a role assignment isn't feasible. For more information, see [Connect to a search service](search-get-started-rbac.md).

+ The [2026-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-05-01-preview&preserve-view=true) version of the Search Service REST APIs.

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

::: zone pivot="csharp"

```csharp
var knowledgeSource = new AzureBlobKnowledgeSource(
    name: "news-articles-ks",
    azureBlobParameters: new AzureBlobKnowledgeSourceParameters(connectionString: blobConnectionString, containerName: "news")
    {
        IngestionParameters = new IngestionParameters
        {
            FreshnessPolicy = new FreshnessPolicy
            {
                BoostingDuration = TimeSpan.FromDays(90)
            }
        }
    }
)
{
    Description = "A knowledge source for recent news articles."
};

await indexClient.CreateOrUpdateKnowledgeSourceAsync(knowledgeSource);
```

**Reference:** [AzureBlobKnowledgeSourceParameters](/dotnet/api/azure.search.documents.indexes.models.azureblobknowledgesourceparameters?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
knowledge_source = AzureBlobKnowledgeSource(
    name="news-articles-ks",
    description="A knowledge source for recent news articles.",
    azure_blob_parameters=AzureBlobKnowledgeSourceParameters(
        connection_string=blob_connection_string,
        container_name="news",
        ingestion_parameters=IngestionParameters(
            freshness_policy=FreshnessPolicy(boosting_duration="P90D"),
        ),
    ),
)

index_client.create_or_update_knowledge_source(knowledge_source)
```

**Reference:** [AzureBlobKnowledgeSourceParameters](/python/api/azure-search-documents/azure.search.documents.indexes.models.azureblobknowledgesourceparameters)

::: zone-end

::: zone pivot="rest"

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

**Reference:** [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

::: zone-end

The freshness policy is part of the source ingestion parameters. The index
schema is modified to support a generated freshness field that's compatible with
Azure AI Search [scoring profile](index-add-scoring-profiles.md) freshness
functions. The `boostingDuration` value uses the same ISO 8601 duration format
as scoring profile freshness functions, such as `P90D` for 90 days. Freshness
adds a recency signal to ranking, but query relevance, configured retrieval
settings, semantic reranking, and other ranking signals still apply.

You can change `boostingDuration` on an existing knowledge source by sending
another create-or-update request with the new value. The scoring profile
updates in place without requiring reingestion.

You can't remove the freshness policy from an existing knowledge source. To
disable freshness-aware retrieval, delete the knowledge source and create a new
one without `freshnessPolicy`.

## Validate ranking behavior

The freshness field is generated at ingestion time, so the policy applies to
content that's ingested after the policy is in place. Once content is
ingested, run retrieve requests that can return both recent and older
content. A successful configuration surfaces newer relevant documents earlier
without turning retrieval into a simple date sort.

If ranking doesn't reflect freshness as expected, inspect the `last_modified`
field in the underlying index. Missing, stale, or inconsistent date values
reduce the quality of the freshness signal.

## Related content

+ [Create an Azure Blob knowledge source](agentic-knowledge-source-how-to-blob.md)
+ [Query a knowledge base using the retrieve action or MCP endpoint](agentic-retrieval-how-to-retrieve.md)
+ [Add scoring profiles to boost search scores](index-add-scoring-profiles.md)
+ [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true)
