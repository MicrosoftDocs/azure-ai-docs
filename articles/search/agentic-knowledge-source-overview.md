---
title: What is a Knowledge Source?
description: Learn about the knowledge source object used for agentic retrieval workloads in Azure AI Search.
ms.service: azure-ai-search
ms.topic: concept-article
ms.date: 06/02/2026
ai-usage: ai-assisted
---

# What is a knowledge source?

[!INCLUDE [GA announcement](./includes/previews/agentic-retrieval-ga-announcement.md)]

> [!IMPORTANT]
> These features and functionality are part of the 2026-05-01-preview REST API. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> The 2026-05-01-preview supports connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.
>
> It's your responsibility to manage whether your data will flow outside of your organization's compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
>
> You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. For more information, see the [Azure AI Search Transparency Note](/azure/foundry/responsible-ai/search/transparency-note).

A *knowledge source* is a top-level resource on your Azure AI Search service that defines the content used in an agentic retrieval pipeline. Each knowledge source is either indexed or remote, which determines how the content is ingested, processed, and queried. Knowledge sources are required components of a knowledge base.

You can reference multiple knowledge sources in a single knowledge base. The agentic retrieval engine queries all of them in a single request. Subqueries are generated for each knowledge source, and the top results are returned in the retrieval response.

## Supported knowledge sources

Azure AI Search supports the following knowledge sources for agentic retrieval workloads.

| Kind | Description | Indexed or remote |
|------|-------------|-------------------|
| [Search index](agentic-knowledge-source-how-to-search-index.md) | Wraps an existing index. | Indexed |
| [Azure blob](agentic-knowledge-source-how-to-blob.md) | Generates an indexer pipeline from a blob container. | Indexed |
| [Azure SQL](agentic-knowledge-source-how-to-azure-sql.md) (preview) | Generates an indexer pipeline from an Azure SQL table or view. | Indexed |
| [File](agentic-knowledge-source-how-to-file.md) (preview) | Uploads files directly to Azure AI Search. | Indexed |
| [OneLake](agentic-knowledge-source-how-to-onelake.md) | Generates an indexer pipeline from a lakehouse. | Indexed |
| [Indexed SharePoint](agentic-knowledge-source-how-to-sharepoint-indexed.md) (preview) | Generates an indexer pipeline from a SharePoint site. | Indexed |
| [Remote SharePoint](agentic-knowledge-source-how-to-sharepoint-remote.md) (preview) | Retrieves content from SharePoint. | Remote |
| [Fabric Data Agent](agentic-knowledge-source-how-to-fabric-data-agent.md) (preview) | Retrieves answers and embedded resources from a Microsoft Fabric data agent. | Remote |
| [Fabric Ontology](agentic-knowledge-source-how-to-fabric-ontology.md) (preview) | Retrieves entity- and relationship-based answers from a Microsoft Fabric ontology. | Remote |
| [MCP server](agentic-knowledge-source-how-to-mcp-server.md) (preview) | Retrieves live, tool-backed results from an external MCP server. | Remote |
| [Work IQ](agentic-knowledge-source-how-to-work-iq.md) (preview) | Retrieves organizational intelligence from Work IQ. | Remote |
| [Web](agentic-knowledge-source-how-to-web.md) | Retrieves real-time grounding data from Microsoft Bing. | Remote |

### Indexed knowledge sources

An indexed knowledge source points to a search index that [meets the criteria for agentic retrieval](agentic-retrieval-how-to-create-index.md). Content is ingested into the index before query time through one of three paths:

+ **Bring your own index:** Use a search index knowledge source to wrap an existing index on your search service.

+ **Direct file upload:** Use a file knowledge source to upload files directly to Azure AI Search. The service processes the files and stores extracted content in a generated search index, with no external storage or indexer pipeline required.

+ **Auto-generated indexer pipeline:** For all other indexed knowledge sources, Azure AI Search automatically creates a complete indexer pipeline from your external data source. This includes a [data source](search-data-sources-gallery.md), [skillset](cognitive-search-working-with-skillsets.md), [indexer](search-indexer-overview.md), and [index](search-what-is-an-index.md) that's populated and chunked.

Queries run locally on your search service using keyword (full text), vector, or hybrid queries.

### Remote knowledge sources

A remote knowledge source connects directly to an external platform. Content is never ingested into Azure AI Search. Instead, it's retrieved at query time via each platform's native APIs. The agentic retrieval engine makes the API call and surfaces results alongside any indexed knowledge sources in the same response.

Depending on the platform, remote connections reach content either over the public internet (such as Bing) or within your Microsoft tenant (such as SharePoint and Fabric).

### Unified ranking

For both indexed and remote knowledge sources, all retrieved content flows through the same ranking pipeline. Results are scored for relevance, merged across queries, and reranked before returning in the retrieval response.

## Working with knowledge sources

Knowledge sources are independent objects that you create and manage separately from knowledge bases. Keep the following in mind:

+ Create a knowledge source before you create a knowledge base. Knowledge bases reference knowledge sources by ID, so the knowledge source must exist first.

+ To delete a knowledge source, first update or delete any knowledge bases that reference it. You can then delete the knowledge source.

+ A knowledge source and its knowledge base must exist on the same search service.

## Creating knowledge sources

To create a knowledge source, you need [**Search Service Contributor** permissions](search-security-rbac.md) on your search service. If the knowledge source generates an indexer pipeline, you also need **Search Index Data Contributor** permissions to load an index. You can use an [admin API key](search-security-api-keys.md) as an alternative to role assignments.

Creation support in the Azure portal, Microsoft Foundry portal, REST API, and Azure SDKs varies by knowledge source kind. For per-kind instructions, see the links in [Supported knowledge sources](#supported-knowledge-sources).

### Ingest sensitivity labels (preview)

For blob, indexed OneLake, and indexed SharePoint knowledge sources, you can ingest [Microsoft Purview sensitivity labels](search-indexer-sensitivity-labels.md) by setting `ingestionPermissionOptions` to include `sensitivityLabel`. Follow all the prerequisites before you set this value. After they're synchronized to the index, labels are surfaced in retrieve responses and used to enforce document-level access at query time. For more information, see [Enforce permissions at query time (preview)](agentic-retrieval-how-to-retrieve.md#enforce-permissions-at-query-time-preview).

If your indexed knowledge source uses a chunked index, such as with integrated vectorization or a custom Text Split skill, you must also map the sensitivity label to each chunk row via [index projections in the skillset](search-indexer-sensitivity-labels.md#6-configure-index-projections-in-your-skillset-if-applicable). Otherwise, chunk-level references in retrieve responses won't be returned if they have labels in the source document.

### Surface document-embedded images (preview)

For blob, indexed OneLake, and indexed SharePoint knowledge sources, you can configure an `assetStore` in the knowledge source's `ingestionParameters` to persist images that are embedded in your source documents. When you also enable image serving on the knowledge base, the [retrieve action](agentic-retrieval-how-to-retrieve.md) injects those images into the answer synthesis prompt so the LLM can reason over diagrams, charts, and extracted image content. For more information, see [Surface document-embedded images in agentic retrieval (preview)](agentic-retrieval-how-to-image-serving.md).

## Using knowledge sources

After you create a knowledge source, reference it in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md). The knowledge base determines which knowledge sources to query. The following sections describe options for controlling which sources are included and how the engine selects among them.

### Always query a knowledge source

Set `alwaysQuery` to `true` on a knowledge source definition to include it in every query, regardless of the retrieval reasoning effort.

### Use the retrieval reasoning effort to control LLM usage (preview)

The retrieval reasoning effort controls how much LLM processing is applied to each query. Not all solutions benefit from LLM query planning. If simplicity and speed are the priority, use `minimal` effort to bypass LLM processing. At `low` and `medium` effort, the LLM plans and selects which knowledge sources to query, with `medium` adding an iterative pass for deeper results. For more information about each level, see [Set the retrieval reasoning effort (preview)](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md).

The following factors inform selection at `low` and `medium` effort:

+ The `name` of the knowledge source.

+ The `description` of an index (for indexed knowledge sources).

+ The `retrievalInstructions` specified in the knowledge base definition or the [retrieve action](agentic-retrieval-how-to-retrieve.md). Retrieval instructions guide which knowledge sources the LLM selects or skips. They work like a prompt: you can specify brevity, tone, and formatting.

## Related content

+ [Agentic retrieval overview](agentic-retrieval-overview.md)
+ [Create a search index for agentic retrieval](agentic-retrieval-how-to-create-index.md)
+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Query a knowledge base](agentic-retrieval-how-to-retrieve.md)
+ [Set the retrieval reasoning effort (preview)](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md)
