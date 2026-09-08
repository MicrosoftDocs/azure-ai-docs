---
title: Create an Azure SQL Knowledge Source for Agentic Retrieval
description: Learn how to create an indexed Azure SQL knowledge source in Azure AI Search that ingests rows from a SQL table or view for agentic retrieval.
ms.reviewer: gimondra
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 08/14/2026
ai-usage: ai-assisted
zone_pivot_groups: search-csharp-python-rest
---

# Create an indexed Azure SQL knowledge source (preview)

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

> [!IMPORTANT]
> These features and functionality are part of the 2026-08-01-preview REST API. The 2026-08-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> The 2026-08-01-preview supports connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.
>
> It's your responsibility to manage whether your data will flow outside of your organization's compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
>
> You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. For more information, see the [Azure AI Search Transparency Note](/azure/foundry/responsible-ai/search/transparency-note).

An *indexed Azure SQL knowledge source* (preview) ingests rows from Azure SQL Database or Azure SQL Managed Instance into an agentic retrieval pipeline in Azure AI Search. [Knowledge sources](agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when the knowledge base is [queried at runtime](agentic-retrieval-how-to-retrieve.md).

Unlike file-based knowledge sources, such as Azure Blob Storage and OneLake, each SQL row is treated as one logical document. You drive the index schema through explicit column mappings rather than using a fixed document schema.

When you create an indexed Azure SQL knowledge source, you specify a SQL data source, optional column mappings, and optional models to automatically generate the following Azure AI Search objects:

+ A data source that represents the SQL table or view.
+ An index whose fields are derived from your column mappings.
+ A skillset that generates embeddings. The service creates a skillset only when you specify `embeddingColumns`.
+ An indexer that uses the previous objects to drive the ingestion pipeline.

The generated indexer conforms to the *Azure SQL indexer*, whose prerequisites, change detection policies, and limitations also apply to indexed Azure SQL knowledge sources. For more information, see the [Azure SQL indexer documentation](search-how-to-index-sql-database.md).

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2026-08-01-preview&preserve-view=true) |
| -- | -- | -- | -- | -- | -- | -- |
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ An Azure AI Search service in any [region that provides agentic retrieval](search-region-support.md).

+ Completion of the [Azure SQL indexer prerequisites](search-how-to-index-sql-database.md#prerequisites), including:

  + An [Azure SQL Database](/azure/azure-sql/database/sql-database-paas-overview) or [Azure SQL Managed Instance](/azure/azure-sql/managed-instance/sql-managed-instance-paas-overview) with a table or view to ingest.

  + A single-valued primary key on the source table or view.

  + For views, a column suitable for high-water-mark change detection. We strongly recommend a `rowversion` column.

+ Permission to create knowledge sources. Configure [keyless authentication](search-get-started-rbac.md) with the **Search Service Contributor** and **Search Index Data Contributor** roles assigned to your user account (recommended) or use an [admin API key](search-security-api-keys.md).

+ If you specify `embeddingColumns`, the search service must have a [managed identity](search-how-to-managed-identities.md) with **Cognitive Services User** permissions on the Microsoft Foundry resource that hosts the embedding model.

+ If you set `networkAccessMode` to `private`, complete the following requirements:

  + Use an [S2, S3, L1, or L2 search service](search-sku-tier.md#tier-descriptions).

  + Create and approve a shared private link to the SQL server with the `sqlServer` group ID. For SQL Managed Instance, use the `managedInstance` group ID.

  + Use either SQL authentication or managed identity authentication. For managed identity, grant the identity the required Azure and database roles, and use a connection string with `Database=<database-name>` and the resource ID of the [SQL server](search-howto-managed-identities-sql.md) or [SQL Managed Instance](search-how-to-index-sql-managed-instance-with-managed-identity.md). Set `ingestionParameters.identity` only for a user-assigned identity. If you omit it, the indexer uses the search service's system-assigned identity.

  + Create and approve a shared private link for each protected model endpoint. Use the `openai_account` group ID for Azure OpenAI endpoints and `foundry_account` for Foundry resource endpoints.

::: zone pivot="csharp"

+ The latest [`Azure.Search.Documents`](https://www.nuget.org/packages/Azure.Search.Documents) preview package: `dotnet add package Azure.Search.Documents --prerelease`

+ For keyless authentication, the [`Azure.Identity`](https://www.nuget.org/packages/Azure.Identity) package: `dotnet add package Azure.Identity`

::: zone-end

::: zone pivot="python"

+ The latest [`azure-search-documents`](https://pypi.org/project/azure-search-documents/#history) preview package: `pip install --pre azure-search-documents`

+ For keyless authentication, the [`azure-identity`](https://pypi.org/project/azure-identity/) package: `pip install azure-identity`

::: zone-end

::: zone pivot="rest"

+ The [2026-08-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-08-01-preview&preserve-view=true) version of the Search Service REST API.

+ For keyless authentication, include a [Microsoft Entra ID token](search-get-started-rbac.md?pivots=rest#get-token) in the `Authorization` header of each HTTP request.

::: zone-end

## Limitations and considerations

+ A knowledge source can ingest from exactly one table or one view.
+ The source table or view must have a single-valued primary key. Composite keys aren't supported.
+ The primary key is auto-discovered and can't be overridden.
+ `contentExtractionMode` supports only `"minimal"`.
+ Image extraction and image verbalization aren't supported.
+ Real-time synchronization isn't supported. The generated indexer is schedule-based.
+ Real-time SQL retrieval isn't supported. The knowledge source is indexed, not remote.

## Prepare the generated indexer

An indexed Azure SQL knowledge source automatically creates an indexer to drive ingestion. Review the following details before you create the knowledge source.

### Change detection

The generated indexer uses standard [Azure SQL indexer change detection](search-how-to-index-sql-database.md#indexing-new-changed-and-deleted-rows):

+ **Tables:** The service applies [SQL integrated change tracking](search-how-to-index-sql-database.md#sql-integrated-change-tracking-policy) automatically. Enable [SQL change tracking](/sql/relational-databases/track-changes/about-change-tracking-sql-server) on the source table before you create the knowledge source.

+ **Views:** The service applies [high-water-mark change detection](search-how-to-index-sql-database.md#high-water-mark-change-detection-policy). Specify the column to use in `highWaterMarkColumn`. A `rowversion` column is strongly recommended. To detect deletions in a view, include a soft-delete marker column in the view as described in [Soft delete column deletion detection policy](search-how-to-index-sql-database.md#soft-delete-column-deletion-detection-policy).

### Authentication

The generated indexer supports two authentication options:

+ **SQL authentication:** Provide a username and password in the connection string.

+ **Managed identity authentication:** Use a system-assigned or user-assigned managed identity that has Azure RBAC and database-level roles on the SQL resource.

For connection string formats, role requirements, and setup steps, see the [Azure SQL indexer prerequisites](search-how-to-index-sql-database.md#prerequisites) and [Connect through a managed identity](search-how-to-managed-identities.md).

## Check for existing knowledge sources

[!INCLUDE [Check for existing knowledge sources](includes/how-tos/knowledge-source-check.md)]

The following JSON is an example response for an indexed Azure SQL knowledge source.

```json
{
  "name": "indexedsqlks",
  "kind": "indexedSql",
  "description": "Sample indexed Azure SQL knowledge source.",
  "encryptionKey": null,
  "indexedSqlParameters": {
    "connectionString": "<sql-connection-string>",
    "tableOrView": "dbo.tbl_hotels",
    "contentColumns": [
      { "name": "hotelName", "sourceField": "HotelName", "searchFieldType": "Edm.String" },
      { "name": "description", "sourceField": "Description", "searchFieldType": "Edm.String" }
    ],
    "embeddingColumns": [
      { "name": "descriptionVector", "sourceField": "Description" }
    ],
    "ingestionParameters": {
      "contentExtractionMode": "minimal",
      "embeddingModel": {
        "kind": "azureOpenAI",
        "azureOpenAIParameters": {
          "resourceUri": "<aoai-endpoint>",
          "deploymentId": "text-embedding-3-large",
          "modelName": "text-embedding-3-large"
        }
      },
      "createdResources": {
        "datasource": "indexedsqlks-datasource",
        "indexer": "indexedsqlks-indexer",
        "skillset": "indexedsqlks-skillset",
        "index": "indexedsqlks-index"
      }
    }
  }
}
```

## Create a knowledge source

Run the following code to create an indexed Azure SQL knowledge source.

::: zone pivot="csharp"

```csharp
using Azure.Identity;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;
using Azure.Search.Documents.KnowledgeBases.Models;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new DefaultAzureCredential());

var embeddingParams = new AzureOpenAIVectorizerParameters
{
    ResourceUri = new Uri(aoaiEndpoint),
    DeploymentName = aoaiEmbeddingDeployment,
    ModelName = aoaiEmbeddingModel
};

var ingestionParams = new KnowledgeSourceIngestionParameters
{
    NetworkAccessMode = KnowledgeSourceNetworkAccessMode.Public,
    ContentExtractionMode = "minimal",
    EmbeddingModel = new KnowledgeSourceAzureOpenAIVectorizer
    {
        AzureOpenAIParameters = embeddingParams
    }
};

var sqlParams = new IndexedSqlKnowledgeSourceParameters(
    connectionString: sqlConnectionString,
    tableOrView: "dbo.tbl_hotels")
{
    ContentColumns =
    {
        new ContentColumnMapping("hotelName", "HotelName", "Edm.String"),
        new ContentColumnMapping("description", "Description", "Edm.String")
    },
    EmbeddingColumns =
    {
        new EmbeddingColumnMapping("descriptionVector", "Description")
    },
    IngestionParameters = ingestionParams
};

var knowledgeSource = new IndexedSqlKnowledgeSource(
    name: "indexedsqlks",
    indexedSqlParameters: sqlParams)
{
    Description = "Indexed Azure SQL knowledge source."
};

await indexClient.CreateOrUpdateKnowledgeSourceAsync(knowledgeSource);
Console.WriteLine($"Knowledge source '{knowledgeSource.Name}' created or updated successfully.");
```

**Reference:** [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient?view=azure-dotnet-preview&preserve-view=true), [IndexedSqlKnowledgeSource](/dotnet/api/azure.search.documents.indexes.models.indexedsqlknowledgesource?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    AzureOpenAIVectorizerParameters,
    ContentColumnMapping,
    EmbeddingColumnMapping,
    IndexedSqlKnowledgeSource,
    IndexedSqlKnowledgeSourceParameters,
)
from azure.search.documents.knowledgebases.models import (
    KnowledgeSourceAzureOpenAIVectorizer,
    KnowledgeSourceIngestionParameters,
    KnowledgeSourceNetworkAccessMode,
)

index_client = SearchIndexClient(endpoint="<search-endpoint>", credential=DefaultAzureCredential())

embedding_params = AzureOpenAIVectorizerParameters(
    resource_url="<aoai-endpoint>",
    deployment_name="<aoai-embedding-deployment>",
    model_name="<aoai-embedding-model>",
)

ingestion_params = KnowledgeSourceIngestionParameters(
    network_access_mode=KnowledgeSourceNetworkAccessMode.PUBLIC,
    content_extraction_mode="minimal",
    embedding_model=KnowledgeSourceAzureOpenAIVectorizer(
        azure_open_ai_parameters=embedding_params
    ),
)

knowledge_source = IndexedSqlKnowledgeSource(
    name="indexedsqlks",
    description="Indexed Azure SQL knowledge source.",
    indexed_sql_parameters=IndexedSqlKnowledgeSourceParameters(
        connection_string="Server=tcp:{server}.database.windows.net,1433;Database={db};...;",
        table_or_view="dbo.tbl_hotels",
        content_columns=[
            ContentColumnMapping(
                name="hotelName",
                source_field="HotelName",
                search_field_type="Edm.String",
            ),
            ContentColumnMapping(
                name="description",
                source_field="Description",
                search_field_type="Edm.String",
            ),
        ],
        embedding_columns=[
            EmbeddingColumnMapping(
                name="descriptionVector",
                source_field="Description",
            )
        ],
        ingestion_parameters=ingestion_params,
    ),
)

index_client.create_or_update_knowledge_source(knowledge_source=knowledge_source)
print(f"Knowledge source '{knowledge_source.name}' created or updated successfully.")
```

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient?view=azure-python-preview&preserve-view=true)

::: zone-end

::: zone pivot="rest"

```http
### Create an indexed Azure SQL knowledge source
PUT {{search-endpoint}}/knowledgesources/indexedsqlks?api-version=2026-08-01-preview
Authorization: Bearer {{search-access-token}}
Content-Type: application/json

{
  "name": "indexedsqlks",
  "kind": "indexedSql",
  "description": "Indexed Azure SQL knowledge source.",
  "indexedSqlParameters": {
    "connectionString": "Server=tcp:{server}.database.windows.net,1433;Database={db};...;",
    "tableOrView": "dbo.tbl_hotels",
    "contentColumns": [
      { "name": "hotelName", "sourceField": "HotelName", "searchFieldType": "Edm.String" },
      { "name": "description", "sourceField": "Description", "searchFieldType": "Edm.String" }
    ],
    "embeddingColumns": [
      { "name": "descriptionVector", "sourceField": "Description" }
    ],
    "ingestionParameters": {
      "networkAccessMode": "public",
      "contentExtractionMode": "minimal",
      "embeddingModel": {
        "kind": "azureOpenAI",
        "azureOpenAIParameters": {
          "resourceUri": "{{aoai-endpoint}}",
          "deploymentId": "{{aoai-embedding-deployment}}",
          "modelName": "{{aoai-embedding-model}}"
        }
      }
    }
  }
}
```

**Reference:** [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

::: zone-end

Use `indexedSqlParameters` to identify the SQL table or view to ingest and to define the column mappings that become fields in the generated index. For views, specify the high-water-mark column used for change detection.

### Column mapping

Use `contentColumns` to map SQL text columns into searchable fields in the generated Azure AI Search index. Each content column mapping names the target index field, the source SQL column, and the Azure AI Search field type. For `contentColumns`, use `Edm.String`.

### Embedding mapping

Use `embeddingColumns` to map SQL text columns into generated vector fields. Specify an embedding model in `ingestionParameters` when you use embedding columns.

For indexed Azure SQL knowledge sources, `contentExtractionMode` must be `"minimal"` because SQL ingestion is row-based and doesn't extract content from binary documents. Image extraction and image verbalization aren't supported, so `chatCompletionModel`, `assetStore`, `aiServices`, and image-related settings have no effect.

### Defaulting and validation rules

The following defaults apply when you create an indexed Azure SQL knowledge source.

+ If you omit `contentColumns`, the service automatically maps SQL columns that can be safely represented as text to `Edm.String` fields in the generated index, using a 1:1 mapping where `name` equals `sourceField`.

+ If you omit `embeddingColumns`, the service doesn't create vector fields and doesn't configure an embedding skill.

+ `embeddingColumns` is independent of `contentColumns`. To make vectors correspond to retrievable text, include the same SQL column in both arrays.

+ The primary key of the source table or view is auto-discovered. Explicit overrides aren't supported, and the source must have a single-valued primary key.

### Restrict ingestion to a private network

Starting with the `2026-08-01-preview` API version, `networkAccessMode` controls the network environment in which the generated indexer for an indexed Azure SQL knowledge source runs. This setting affects ingestion only and doesn't change knowledge base retrieve requests or responses.

`networkAccessMode` defaults to `public`, which preserves existing public network behavior. When `networkAccessMode` is `private`, the generated indexer runs in the [private execution environment](search-howto-run-reset-indexers.md#indexer-execution-environment). It uses approved [shared private links](search-indexer-howto-access-private.md) to access the Azure SQL Database or SQL Managed Instance source connection and supported Azure dependencies, such as Azure OpenAI models and Microsoft Foundry resources.

To configure and verify private network access:

[!INCLUDE [Configure private network ingestion](includes/how-tos/knowledge-source-private-network.md)]

## Check ingestion status

[!INCLUDE [Check ingestion status](includes/how-tos/knowledge-source-status.md)]

## Review the generated objects

[!INCLUDE [Review the generated objects](includes/how-tos/knowledge-source-review-objects.md)]

## Assign to a knowledge base

If you're satisfied with the knowledge source, [add it to a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

## Query a knowledge base

After the knowledge base is configured, [call the retrieve action or MCP endpoint](agentic-retrieval-how-to-retrieve.md) to query the knowledge source.

## Delete a knowledge source

[!INCLUDE [Delete a knowledge source](includes/how-tos/knowledge-source-delete.md)]

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [What is a knowledge source?](agentic-knowledge-source-overview.md)
+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Query a knowledge base](agentic-retrieval-how-to-retrieve.md)
+ [Azure SQL indexer in Azure AI Search](search-how-to-index-sql-database.md)
