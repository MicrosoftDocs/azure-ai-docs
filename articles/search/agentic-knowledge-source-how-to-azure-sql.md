---
title: Create an Azure SQL Knowledge Source for Agentic Retrieval
description: Learn how to create an indexed Azure SQL knowledge source in Azure AI Search that ingests rows from a SQL table or view for agentic retrieval.
ms.reviewer: gimondra
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 06/02/2026
ai-usage: ai-assisted
zone_pivot_groups: search-csharp-python-rest
---

# Create an indexed Azure SQL knowledge source (preview)

> [!IMPORTANT]
> These features and functionality are part of the 2026-05-01-preview REST API. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> The 2026-05-01-preview supports connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.
>
> It's your responsibility to manage whether your data will flow outside of your organization's compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
>
> You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. For more information, see the [Azure AI Search Transparency Note](/azure/foundry/responsible-ai/search/transparency-note).

An *indexed Azure SQL knowledge source* (preview) ingests rows from Azure SQL Database or Azure SQL Managed Instance into an agentic retrieval pipeline in Azure AI Search. [Knowledge sources](agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when the knowledge base is [queried at runtime](agentic-retrieval-how-to-retrieve.md).

Unlike file-based knowledge sources, such as Azure Blob Storage and OneLake, each SQL row is treated as one logical document. The index schema is customer driven through explicit column mappings rather than a fixed document schema.

When you create an indexed Azure SQL knowledge source, you specify a SQL data source, optional column mappings, and optional models to automatically generate the following Azure AI Search objects:

+ A data source that represents the SQL table or view.
+ An index whose fields are derived from your column mappings.
+ A skillset that generates embeddings. The service creates a skillset only when you specify `embeddingColumns`.
+ An indexer that uses the previous objects to drive the ingestion pipeline.

The generated indexer conforms to the *Azure SQL indexer*, whose prerequisites, change detection policies, and limitations also apply to indexed Azure SQL knowledge sources. For more information, see the [Azure SQL indexer documentation](search-how-to-index-sql-database.md).

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources) |
|--|--|--|--|--|--|--|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ An Azure AI Search service in any [region that provides agentic retrieval](search-region-support.md).

+ Completion of the [Azure SQL indexer prerequisites](search-how-to-index-sql-database.md#prerequisites), including:

    + An [Azure SQL Database](/azure/azure-sql/database/sql-database-paas-overview) or [Azure SQL Managed Instance](/azure/azure-sql/managed-instance/sql-managed-instance-paas-overview) with a table or view to ingest.
        
    + A single-valued primary key on the source table or view.
        
    + For views, a column suitable for high-water-mark change detection. We strongly recommend a `rowversion` column.

+ Permissions to create knowledge sources. Configure [keyless authentication](search-get-started-rbac.md) with the **Search Service Contributor** and **Search Index Data Contributor** roles assigned to your user account (recommended) or use an [API key](search-security-api-keys.md).

+ If you specify `embeddingColumns`, the search service must have a [managed identity](search-how-to-managed-identities.md) with **Cognitive Services User** permissions on the Microsoft Foundry resource that hosts the embedding model.

::: zone pivot="csharp"

+ The latest [`Azure.Search.Documents`](https://www.nuget.org/packages/Azure.Search.Documents) preview package: `dotnet add package Azure.Search.Documents --prerelease`

::: zone-end

::: zone pivot="python"

+ The latest [`azure-search-documents`](https://pypi.org/project/azure-search-documents/#history) preview package: `pip install --pre azure-search-documents`

::: zone-end

::: zone pivot="rest"

+ The [2026-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-05-01-preview&preserve-view=true) version of the Search Service REST APIs.

::: zone-end

## Limitations and considerations

+ A knowledge source can ingest from exactly one table or one view.
+ The source table or view must have a single-valued primary key. Composite keys aren't supported.
+ The primary key is auto-discovered and can't be overridden.
+ `contentExtractionMode` supports only `"minimal"`.
+ Image extraction and image verbalization aren't supported.
+ Real-time synchronization isn't supported. The generated indexer is schedule based.
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

For connection string formats, role requirements, and set up steps, see the [Azure SQL indexer prerequisites](search-how-to-index-sql-database.md#prerequisites) and [Connect through a managed identity](search-how-to-managed-identities.md).

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
    "connectionString": "<SQL database connection string>",
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
          "resourceUri": "<Foundry resource endpoint URI>",
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
using Azure;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;
using Azure.Search.Documents.KnowledgeBases.Models;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new AzureKeyCredential(apiKey));

var embeddingParams = new AzureOpenAIVectorizerParameters
{
    ResourceUri = new Uri(aoaiEndpoint),
    DeploymentName = aoaiEmbeddingDeployment,
    ModelName = aoaiEmbeddingModel,
    ApiKey = aoaiKey
};

var ingestionParams = new KnowledgeSourceIngestionParameters
{
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
from azure.core.credentials import AzureKeyCredential
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
)

index_client = SearchIndexClient(endpoint="search_url", credential=AzureKeyCredential("api_key"))

embedding_params = AzureOpenAIVectorizerParameters(
    resource_url="aoai_endpoint",
    deployment_name="aoai_embedding_deployment",
    model_name="aoai_embedding_model",
    api_key="aoai_key",
)

ingestion_params = KnowledgeSourceIngestionParameters(
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
PUT {{search-url}}/knowledgesources/indexedsqlks?api-version=2026-05-01-preview
api-key: {{api-key}}
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
      "contentExtractionMode": "minimal",
      "embeddingModel": {
        "kind": "azureOpenAI",
        "azureOpenAIParameters": {
          "resourceUri": "{{aoai-endpoint}}",
          "deploymentId": "{{aoai-embedding-deployment}}",
          "modelName": "{{aoai-embedding-model}}",
          "apiKey": "{{aoai-key}}"
        }
      }
    }
  }
}
```

**Reference:** [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

::: zone-end

### Source-specific properties

The following properties apply to indexed Azure SQL knowledge sources.

| Property | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source. The name must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | Yes | Yes |
| `kind` | The kind of knowledge source, which is `indexedSql` in this case. | String | No | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | Object | Yes | No |
| `indexedSqlParameters` | Parameters specific to indexed Azure SQL knowledge sources, which are described in the following section. | Object | | Yes |

### `indexedSqlParameters` properties

The following properties are specific to the `indexedSqlParameters` object of an indexed Azure SQL knowledge source.

| Property | Description | Type | Editable | Required |
|--|--|--|--|--|
| `connectionString` | A SQL authentication or managed-identity connection string for Azure SQL Database or Azure SQL Managed Instance. For supported credential formats, see the [Azure SQL indexer prerequisites](search-how-to-index-sql-database.md#prerequisites). | String | No | Yes |
| `tableOrView` | The fully qualified name of the SQL table or view to ingest, specified in the `schema.objectName` format. A knowledge source ingests from exactly one table or one view. | String | No | Yes |
| `highWaterMarkColumn` | Required when `tableOrView` refers to a view. The name of the column used for high-water-mark change detection. We strongly recommend a `rowversion` column. For more information, see [High water mark change detection policy](search-how-to-index-sql-database.md#high-water-mark-change-detection-policy). | String | No | Conditional |
| `contentColumns` | An array of [column mappings](#column-mapping) that defines which SQL columns are treated as searchable text content in the generated index. Each mapping must use `Edm.String` as the `searchFieldType`. | Array | No | No |
| `embeddingColumns` | An array of [embedding mappings](#embedding-mapping) that defines which SQL columns are used to generate vector fields. | Array | No | No |
| `ingestionParameters` | A subset of the standard knowledge source [ingestion parameters](#ingestionparameters-properties). | Object | | No |

### Column mapping

`contentColumns` uses the following column mapping shape.

| Property | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the field as it appears in the generated Azure AI Search index. | String | No | Yes |
| `sourceField` | The SQL column whose value populates the target field. | String | No | Yes |
| `searchFieldType` | The Azure AI Search field type for the generated field. For `contentColumns`, this must be `Edm.String`. | String | No | Yes |

### Embedding mapping

`embeddingColumns` uses the following embedding mapping shape.

| Property | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the target vector field that the service creates in the generated index. For example, it could be `descriptionVector`. | String | No | Yes |
| `sourceField` | The SQL column whose text content is sent to the embedding model. | String | No | Yes |

### `ingestionParameters` properties

For indexed Azure SQL knowledge sources, the existing `ingestionParameters` schema is unchanged, but only the following properties apply.

| Property | Description | Type | Editable | Required |
|--|--|--|--|--|
| `contentExtractionMode` | Must be `"minimal"`. Other modes aren't supported because Azure SQL ingestion is row based and doesn't extract content from binary documents. | String | No | No |
| `embeddingModel` | An Azure OpenAI embedding model used to vectorize the columns listed in `embeddingColumns`. Required only when `embeddingColumns` is specified. | Object | Only `apiKey` and `deploymentId` are editable | Conditional |
| `identity` | An optional user-assigned managed identity used to authenticate to Azure SQL and Azure OpenAI. | Object | Yes | No |
| `ingestionSchedule` | An optional schedule that controls how often the generated indexer runs. | Object | Yes | No |

Image extraction and image verbalization aren't supported for indexed Azure SQL knowledge sources, so `chatCompletionModel`, `assetStore`, `aiServices`, and image-related settings have no effect.

### Defaulting and validation rules

The following defaults apply when you create an indexed Azure SQL knowledge source.

+ If you omit `contentColumns`, the service automatically maps SQL columns that can be safely represented as text to `Edm.String` fields in the generated index, using a 1:1 mapping where `name` equals `sourceField`.

+ If you omit `embeddingColumns`, the service doesn't create vector fields and doesn't configure an embedding skill.

+ `embeddingColumns` is independent of `contentColumns`. To make vectors correspond to retrievable text, include the same SQL column in both arrays.

+ The primary key of the source table or view is auto-discovered. Explicit overrides aren't supported, and the source must have a single-valued primary key.

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
