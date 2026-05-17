---
title: Create an Azure SQL Knowledge Source for Agentic Retrieval
description: Learn how to create an indexed Azure SQL knowledge source in Azure AI Search that ingests rows from a SQL table or view for agentic retrieval.
author: gmndrg
ms.author: gimondra
ms.service: azure-ai-search
ms.custom:
  - build-2026
ms.topic: how-to
ms.date: 05/16/2026
ai-usage: ai-assisted
---

# Create an indexed Azure SQL knowledge source

[!INCLUDE [Preview feature](./includes/previews/agentic-retrieval-preview-feature.md)]

Use an *indexed Azure SQL knowledge source* to ingest rows from Azure SQL Database or Azure SQL Managed Instance into an agentic retrieval pipeline. [Knowledge sources](agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when an agent or chatbot calls a [retrieve action](agentic-retrieval-how-to-retrieve.md) at query time.

Unlike file-based knowledge sources such as Azure Blob Storage and OneLake, each SQL row is treated as one logical document. The index schema is customer driven through explicit column mappings rather than a fixed document schema.

When you create an indexed Azure SQL knowledge source, you specify a SQL data source, optional column mappings, and optional models to automatically generate the following Azure AI Search objects:

+ A data source that represents the SQL table or view.
+ An index whose fields are derived from your column mappings.
+ A skillset that generates embeddings. The service creates a skillset only when you specify `embeddingColumns`.
+ An indexer that uses the previous objects to drive the ingestion pipeline.

The generated indexer conforms to the *Azure SQL indexer*, whose prerequisites, change detection policies, and limitations also apply to indexed Azure SQL knowledge sources. For more information, see the [Azure SQL indexer documentation](search-how-to-index-sql-database.md).

## Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources) |
|--|--|--|--|--|--|--|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ Azure AI Search in any [region that provides agentic retrieval](search-region-support.md).

+ Azure SQL Database or Azure SQL Managed Instance with a table or view to ingest. Completion of the [Azure SQL indexer prerequisites](search-how-to-index-sql-database.md#prerequisites).

+ A single-valued primary key on the source table or view.

+ For views, a column suitable for high-water-mark change detection. A `rowversion` column is strongly recommended.

+ Permission to create and use objects on Azure AI Search. For best results, use [role-based access](search-security-rbac.md), but you can use [API keys](search-security-api-keys.md) if a role assignment isn't feasible. For more information, see [Connect to a search service](search-get-started-rbac.md).

+ The [Search Service 2026-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-05-01-preview&preserve-view=true) REST API.

## Check for existing knowledge sources

A knowledge source is a top-level, reusable object. Knowing about existing knowledge sources is helpful for reuse or for naming new objects. Run the following request to list knowledge sources by name and kind.

```http
### List knowledge sources
GET {{search-url}}/knowledgesources?api-version=2026-05-01-preview&$select=name,kind
api-key: {{api-key}}
```

**Reference:** [Knowledge Sources - List](/rest/api/searchservice/knowledge-sources/list?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

The following JSON is an example response for an indexed Azure SQL knowledge source.

```json
{
  "name": "indexedsqlks",
  "kind": "indexedSql",
  "description": "Sample indexed Azure SQL knowledge source.",
  "encryptionKey": null,
  "indexedSqlParameters": {
    "connectionString": "<SQL data base connection string>",
    "tableOrView": "dbo.tbl_hotels",
    "contentColumns": [
      { "name": "hotelName", "sourceField": "HotelName", "searchFieldType": "Edm.String" },
      { "name": "description", "sourceField": "Description", "searchFieldType": "Edm.String" }
    ],
    "filterColumns": [
      { "name": "category", "sourceField": "Category", "searchFieldType": "Edm.String" },
      { "name": "lastUpdatedTime", "sourceField": "LastUpdatedTime", "searchFieldType": "Edm.DateTimeOffset" }
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

The generated resources appear at the end of the response under `createdResources`.

## Create a knowledge source

Run the following request to create an indexed Azure SQL knowledge source.

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
    "filterColumns": [
      { "name": "category", "sourceField": "Category", "searchFieldType": "Edm.String" }
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

### Top-level properties

| Property | Description | Required |
|--|--|--|
| `name` | The name of the knowledge source. The name must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | Yes |
| `description` | A description of the knowledge source. | No |
| `kind` | Must be `indexedSql`. | Yes |
| `encryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | No |
| `indexedSqlParameters` | Parameters specific to indexed Azure SQL knowledge sources. | Yes |

### `indexedSqlParameters`

| Property | Description | Required |
|--|--|--|
| `connectionString` | A SQL authentication or managed-identity connection string for Azure SQL Database or Azure SQL Managed Instance. For supported credential formats, see [Azure SQL indexer prerequisites](search-how-to-index-sql-database.md#prerequisites). | Yes |
| `tableOrView` | The fully qualified name of the SQL table or view to ingest, in the form `schema.objectName`. A knowledge source ingests from exactly one table or one view. | Yes |
| `highWaterMarkColumn` | Required when `tableOrView` refers to a view. The name of the column used for high-water-mark change detection. A `rowversion` column is strongly recommended. For more information, see [High water mark change detection policy](search-how-to-index-sql-database.md#high-water-mark-change-detection-policy). | Conditional |
| `contentColumns` | An array of [column mappings](#column-mapping) that defines which SQL columns are treated as searchable text content in the generated index. Each mapping must use `Edm.String` as the `searchFieldType`. | No |
| `filterColumns` | An array of [column mappings](#column-mapping) that defines which SQL columns are added to the generated index as filterable, sortable, or facetable fields. | No |
| `embeddingColumns` | An array of [embedding mappings](#embedding-mapping) that defines which SQL columns are used to generate vector fields. | No |
| `ingestionParameters` | A subset of the standard knowledge source [ingestion parameters](#ingestion-parameters). | No |

### Column mapping

`contentColumns` and `filterColumns` use the following column mapping shape.

| Property | Description |
|--|--|
| `name` | The name of the field as it appears in the generated Azure AI Search index. |
| `sourceField` | The SQL column whose value populates the target field. |
| `searchFieldType` | The Azure AI Search field type for the generated field. For `contentColumns`, this must be `Edm.String`. For `filterColumns`, use the type that matches the SQL column. The samples on this page use `Edm.String` for text columns and `Edm.DateTimeOffset` for date and time columns. |

### Embedding mapping

`embeddingColumns` uses the following embedding mapping shape.

| Property | Description |
|--|--|
| `name` | The name of the target vector field that the service creates in the generated index (for example, `descriptionVector`). |
| `sourceField` | The SQL column whose text content is sent to the embedding model. |

### Ingestion parameters

For indexed Azure SQL knowledge sources, the `ingestionParameters` schema is unchanged, but only the following properties apply:

| Property | Description |
|--|--|
| `contentExtractionMode` | Must be `"minimal"`. Other modes aren't supported because Azure SQL ingestion is row based and doesn't extract content from binary documents. |
| `embeddingModel` | An Azure OpenAI embedding model used to vectorize the columns listed in `embeddingColumns`. Required only when `embeddingColumns` is specified. |
| `identity` | An optional user-assigned managed identity used to authenticate to Azure SQL and Azure OpenAI. |
| `ingestionSchedule` | An optional schedule that controls how often the generated indexer runs. |

Image extraction and image verbalization aren't supported for indexed Azure SQL knowledge sources, so `chatCompletionModel`, `assetStore`, `aiServices`, and image-related settings have no effect.

## Defaulting and validation rules

The following defaults apply when you create an indexed Azure SQL knowledge source:

+ If you omit `contentColumns`, the service automatically maps SQL columns that can be safely represented as text to `Edm.String` fields in the generated index, using a 1:1 mapping where `name` equals `sourceField`.
+ If you omit `embeddingColumns`, the service doesn't create vector fields and doesn't configure an embedding skill.
+ `embeddingColumns` is independent of `contentColumns`. To make vectors correspond to retrievable text, include the same SQL column in both arrays.
+ The primary key of the source table or view is auto-discovered. Explicit overrides aren't supported, and the source must have a single-valued primary key.

## Configure change detection

The generated indexer uses standard [Azure SQL indexer change detection](search-how-to-index-sql-database.md#indexing-new-changed-and-deleted-rows):

+ **Tables.** The service applies [SQL integrated change tracking](search-how-to-index-sql-database.md#sql-integrated-change-tracking-policy) automatically. Enable [SQL change tracking](/sql/relational-databases/track-changes/about-change-tracking-sql-server) on the source table before you create the knowledge source.

+ **Views.** The service applies [high-water-mark change detection](search-how-to-index-sql-database.md#high-water-mark-change-detection-policy). Specify the column to use in `highWaterMarkColumn`. A `rowversion` column is strongly recommended. To detect deletions in a view, include a soft-delete marker column in the view as described in [Soft delete column deletion detection policy](search-how-to-index-sql-database.md#soft-delete-column-deletion-detection-policy).

## Authentication

The generated indexer supports two authentication options:

+ **SQL authentication.** Provide a username and password in the connection string.

+ **Managed identity authentication.** Use a system-assigned or user-assigned managed identity that has Azure RBAC and database-level roles on the SQL resource.

For connection string formats, role requirements, and setup steps, see [Azure SQL indexer prerequisites](search-how-to-index-sql-database.md#prerequisites) and [Connect through a managed identity](search-how-to-managed-identities.md).

## Limitations

+ A knowledge source can ingest from exactly one table or one view.
+ The source table or view must have a single-valued primary key. Composite keys aren't supported.
+ The primary key is auto-discovered and can't be overridden.
+ `contentExtractionMode` supports only `"minimal"`.
+ Image extraction and image verbalization aren't supported.
+ Real-time synchronization isn't supported. The generated indexer is schedule based.
+ Query-time federation to SQL isn't supported. The knowledge source is indexed, not federated.
+ Available only through the [`2026-05-01-preview`](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-05-01-preview&preserve-view=true) REST API.

## Related content

+ [What is a knowledge source?](agentic-knowledge-source-overview.md)
+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Retrieve action](agentic-retrieval-how-to-retrieve.md)
+ [Azure SQL indexer in Azure AI Search](search-how-to-index-sql-database.md)
