---
title: Create an Azure SQL Knowledge Source for Agentic Retrieval
description: Learn how to create an indexed Azure SQL knowledge source in Azure AI Search that ingests rows from a SQL table or view for agentic retrieval.
ms.reviewer: gimondra
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 06/02/2026
ai-usage: ai-assisted
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

Use an *indexed Azure SQL knowledge source* (preview) to ingest rows from Azure SQL Database or Azure SQL Managed Instance into an agentic retrieval pipeline. [Knowledge sources](agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when an agent or chatbot calls a [retrieve action](agentic-retrieval-how-to-retrieve.md) at query time.

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

+ Azure AI Search in any [region that provides agentic retrieval](search-region-support.md).

+ Completion of the [Azure SQL indexer prerequisites](search-how-to-index-sql-database.md#prerequisites), including:

    + An [Azure SQL Database](/azure/azure-sql/database/sql-database-paas-overview) or [Azure SQL Managed Instance](/azure/azure-sql/managed-instance/sql-managed-instance-paas-overview) with a table or view to ingest.
        
    + A single-valued primary key on the source table or view.
        
    + For views, a column suitable for high-water-mark change detection. We strongly recommend a `rowversion` column.

+ Permission to create and use objects on Azure AI Search. We recommend [role-based access](search-security-rbac.md), but you can use [API keys](search-security-api-keys.md) if a role assignment isn't feasible. For more information, see [Connect to a search service](search-get-started-rbac.md).

+ The [2026-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-05-01-preview&preserve-view=true) version of the Search Service REST APIs.

## Limitations and considerations

+ A knowledge source can ingest from exactly one table or one view.
+ The source table or view must have a single-valued primary key. Composite keys aren't supported.
+ The primary key is auto-discovered and can't be overridden.
+ `contentExtractionMode` supports only `"minimal"`.
+ Image extraction and image verbalization aren't supported.
+ Real-time synchronization isn't supported. The generated indexer is schedule based.
+ Real-time SQL retrieval isn't supported. The knowledge source is indexed, not remote.

## Check for existing knowledge sources

A knowledge source is a top-level, reusable object. Knowing about existing knowledge sources is helpful for either reuse or naming new objects.

Run the following code to list knowledge sources by name and type.

```http
### List knowledge sources by name and type
GET {{search-url}}/knowledgesources?api-version={{api-version}}&$select=name,kind
api-key: {{api-key}}
```

**Reference:** [Knowledge Sources - List](/rest/api/searchservice/knowledge-sources/list)

You can also return a single knowledge source by name to review its JSON definition.

```http
### Get a knowledge source definition
GET {{search-url}}/knowledgesources/{{knowledge-source-name}}?api-version={{api-version}}
api-key: {{api-key}}
```

**Reference:** [Knowledge Sources - Get](/rest/api/searchservice/knowledge-sources/get)

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

The generated resources appear at the end of the response under `createdResources`.

## Create a knowledge source

Run the following code to create an indexed Azure SQL knowledge source.

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

### Source-specific properties

The following properties apply to indexed Azure SQL knowledge sources.

| Property | Description | Required |
|--|--|--|
| `name` | The name of the knowledge source. The name must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | Yes |
| `kind` | The kind of knowledge source, which is `indexedSql` in this case. | Yes |
| `description` | A description of the knowledge source. | No |
| `encryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | No |
| `indexedSqlParameters` | Parameters specific to indexed Azure SQL knowledge sources, which are described in the following section. | Yes |

### `indexedSqlParameters` properties

The following properties are specific to the `indexedSqlParameters` object of an indexed Azure SQL knowledge source.

| Property | Description | Required |
|--|--|--|
| `connectionString` | A SQL authentication or managed-identity connection string for Azure SQL Database or Azure SQL Managed Instance. For supported credential formats, see the [Azure SQL indexer prerequisites](search-how-to-index-sql-database.md#prerequisites). | Yes |
| `tableOrView` | The fully qualified name of the SQL table or view to ingest, specified in the `schema.objectName` format. A knowledge source ingests from exactly one table or one view. | Yes |
| `highWaterMarkColumn` | Required when `tableOrView` refers to a view. The name of the column used for high-water-mark change detection. We strongly recommend a `rowversion` column. For more information, see [High water mark change detection policy](search-how-to-index-sql-database.md#high-water-mark-change-detection-policy). | Conditional |
| `contentColumns` | An array of [column mappings](#column-mapping) that defines which SQL columns are treated as searchable text content in the generated index. Each mapping must use `Edm.String` as the `searchFieldType`. | No |
| `embeddingColumns` | An array of [embedding mappings](#embedding-mapping) that defines which SQL columns are used to generate vector fields. | No |
| `ingestionParameters` | A subset of the standard knowledge source [ingestion parameters](#ingestionparameters-properties). | No |

### Column mapping

`contentColumns` uses the following column mapping shape.

| Property | Description |
|--|--|
| `name` | The name of the field as it appears in the generated Azure AI Search index. |
| `sourceField` | The SQL column whose value populates the target field. |
| `searchFieldType` | The Azure AI Search field type for the generated field. For `contentColumns`, this must be `Edm.String`. |

### Embedding mapping

`embeddingColumns` uses the following embedding mapping shape.

| Property | Description |
|--|--|
| `name` | The name of the target vector field that the service creates in the generated index. For example, it could be `descriptionVector`. |
| `sourceField` | The SQL column whose text content is sent to the embedding model. |

### `ingestionParameters` properties

For indexed Azure SQL knowledge sources, the existing `ingestionParameters` schema is unchanged, but only the following properties apply.

| Property | Description |
|--|--|
| `contentExtractionMode` | Must be `"minimal"`. Other modes aren't supported because Azure SQL ingestion is row based and doesn't extract content from binary documents. |
| `embeddingModel` | An Azure OpenAI embedding model used to vectorize the columns listed in `embeddingColumns`. Required only when `embeddingColumns` is specified. |
| `identity` | An optional user-assigned managed identity used to authenticate to Azure SQL and Azure OpenAI. |
| `ingestionSchedule` | An optional schedule that controls how often the generated indexer runs. |

Image extraction and image verbalization aren't supported for indexed Azure SQL knowledge sources, so `chatCompletionModel`, `assetStore`, `aiServices`, and image-related settings have no effect.

### Defaulting and validation rules

The following defaults apply when you create an indexed Azure SQL knowledge source:

+ If you omit `contentColumns`, the service automatically maps SQL columns that can be safely represented as text to `Edm.String` fields in the generated index, using a 1:1 mapping where `name` equals `sourceField`.

+ If you omit `embeddingColumns`, the service doesn't create vector fields and doesn't configure an embedding skill.

+ `embeddingColumns` is independent of `contentColumns`. To make vectors correspond to retrievable text, include the same SQL column in both arrays.

+ The primary key of the source table or view is auto-discovered. Explicit overrides aren't supported, and the source must have a single-valued primary key.

## Configure the generated indexer

An indexed Azure SQL knowledge source automatically creates an indexer to drive ingestion. The following sections cover change detection and authentication options for the generated indexer.

### Change detection

The generated indexer uses standard [Azure SQL indexer change detection](search-how-to-index-sql-database.md#indexing-new-changed-and-deleted-rows):

+ **Tables:** The service applies [SQL integrated change tracking](search-how-to-index-sql-database.md#sql-integrated-change-tracking-policy) automatically. Enable [SQL change tracking](/sql/relational-databases/track-changes/about-change-tracking-sql-server) on the source table before you create the knowledge source.

+ **Views:** The service applies [high-water-mark change detection](search-how-to-index-sql-database.md#high-water-mark-change-detection-policy). Specify the column to use in `highWaterMarkColumn`. A `rowversion` column is strongly recommended. To detect deletions in a view, include a soft-delete marker column in the view as described in [Soft delete column deletion detection policy](search-how-to-index-sql-database.md#soft-delete-column-deletion-detection-policy).

### Authentication

The generated indexer supports two authentication options:

+ **SQL authentication:** Provide a username and password in the connection string.

+ **Managed identity authentication:** Use a system-assigned or user-assigned managed identity that has Azure RBAC and database-level roles on the SQL resource.

For connection string formats, role requirements, and setup steps, see the [Azure SQL indexer prerequisites](search-how-to-index-sql-database.md#prerequisites) and [Connect through a managed identity](search-how-to-managed-identities.md).

## Assign to a knowledge base

If you're satisfied with the knowledge source, continue to the next step: specify the knowledge source in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

After the knowledge base is configured, use the [retrieve action](agentic-retrieval-how-to-retrieve.md) to query the knowledge source.

## Delete a knowledge source

Before you can delete a knowledge source, you must delete any knowledge base that references it or update the knowledge base definition to remove the reference. For knowledge sources that generate an index and indexer pipeline, all *generated objects* are also deleted. However, if you used an existing index to create a knowledge source, your index isn't deleted.

If you try to delete a knowledge source that's in use, the action fails and returns a list of affected knowledge bases.

To delete a knowledge source:

1. Get a list of all knowledge bases on your search service.

    ```http
    ### Get knowledge bases
    GET {{search-url}}/knowledgebases?api-version={{api-version}}&$select=name
    api-key: {{api-key}}
    ```

   **Reference:** [Knowledge Bases - List](/rest/api/searchservice/knowledge-bases/list)

   An example response might look like the following:

   ```json
    {
        "@odata.context": "https://my-search-service.search.windows.net/$metadata#knowledgebases(name)",
        "value": [
        {
            "name": "my-kb"
        },
        {
            "name": "my-kb-2"
        }
        ]
    }
   ```

1. Get an individual knowledge base definition to check for knowledge source references.

    ```http
    ### Get a knowledge base definition
    GET {{search-url}}/knowledgebases/{{knowledge-base-name}}?api-version={{api-version}}
    api-key: {{api-key}}
    ```

   **Reference:** [Knowledge Bases - Get](/rest/api/searchservice/knowledge-bases/get)

   An example response might look like the following:

   ```json
    {
      "name": "my-kb",
      "description": null,
      "retrievalInstructions": null,
      "answerInstructions": null,
      "outputMode": null,
      "knowledgeSources": [
        {
          "name": "my-blob-ks",
        }
      ],
      "models": [],
      "encryptionKey": null,
      "retrievalReasoningEffort": {
        "kind": "low"
      }
    }
   ```

1. Either delete the knowledge base or, if you have multiple knowledge sources, update the knowledge base to remove the source. This example shows deletion.

    ```http
    ### Delete a knowledge base
    DELETE {{search-url}}/knowledgebases/{{knowledge-base-name}}?api-version={{api-version}}
    api-key: {{api-key}}
    ```

   **Reference:** [Knowledge Bases - Delete](/rest/api/searchservice/knowledge-bases/delete)

1. Delete the knowledge source.

    ```http
    ### Delete a knowledge source
    DELETE {{search-url}}/knowledgesources/{{knowledge-source-name}}?api-version={{api-version}}
    api-key: {{api-key}}
    ```

   **Reference:** [Knowledge Sources - Delete](/rest/api/searchservice/knowledge-sources/delete)

## Related content

+ [What is a knowledge source?](agentic-knowledge-source-overview.md)
+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Query a knowledge base](agentic-retrieval-how-to-retrieve.md)
+ [Azure SQL indexer in Azure AI Search](search-how-to-index-sql-database.md)
