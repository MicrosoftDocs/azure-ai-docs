---
title: 'Tutorial: Configure Multiple Blob Indexers for One Search Index'
description: Learn how to configure three folder-scoped blob indexers that process DOCX, JSON, and CSV content for one union-schema Azure AI Search index.
ms.reviewer: gimondra
ms.service: azure-ai-search
ms.topic: tutorial
ms.date: 08/10/2026
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# Tutorial: Configure multiple blob indexers for one search index

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

In this tutorial, you configure independent blob indexers for DOCX, JSON, and CSV content that write to one Azure AI Search index. A nullable union schema lets each pipeline populate the fields it owns while your application queries all formats together. You can extend this pattern to other compatible indexer types when the indexers have compatible field mappings and target the same index. This tutorial demonstrates and verifies only folder-scoped blob indexers.

In this tutorial, you:

> [!div class="checklist"]
> + Prepare DOCX, JSON, and CSV sample data in separate blob folders
> + Create a union-schema index and three folder-scoped blob data sources
> + Configure three indexers with different parsing and enrichment paths
> + Run the indexers and verify the combined keyword, vector, and hybrid results
> + Review content ownership, troubleshooting, and cleanup practices

> [!IMPORTANT]
> Semantic chunking in the Azure Content Understanding skill is part of the 2026-08-01-preview REST API. The multi-indexer pattern, index projections, and the Content Understanding skill without semantic chunking are generally available. However, for consistency, this tutorial uses the 2026-08-01-preview across all requests.
>
> These features and functionality are part of the 2026-08-01-preview REST API. The 2026-08-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> The 2026-08-01-preview supports connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.
>
> It's your responsibility to manage whether your data flows outside of your organization's compliance and geographic boundaries and any related implications. Ensure that appropriate permissions, boundaries, and approvals are in place.
>
> You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This responsibility includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. For more information, see the [Azure AI Search Transparency Note](/azure/foundry/responsible-ai/search/transparency-note).

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

- An [Azure AI Search service](search-create-service-portal.md) with a [system-assigned managed identity](search-how-to-managed-identities.md). On the search service **Settings** > **Keys** page, set **API access control** to **Both** so that the service accepts either Microsoft Entra ID bearer tokens or API keys. This setting enables the bearer-token requests in this tutorial without breaking existing clients that use API keys. Select **Role-based access control** instead only if you no longer need key-based authentication. For more information, see [Enable role-based access control](search-security-enable-roles.md).

- Your user account must have the **Search Service Contributor**, **Search Index Data Contributor**, and **Search Index Data Reader** roles on the search service. These roles authorize the management and query operations sent with the bearer token throughout this tutorial. For more information, see [Connect to Azure AI Search using roles](search-security-rbac.md). If a request includes both a bearer token and an API key, the API key takes precedence.

- An [Azure Storage account](/azure/storage/common/storage-account-create) with a [blob container](/azure/storage/blobs/blob-containers-portal#create-a-container). Create `docx`, `json`, and `csv` folders in the container. Assign the **Storage Blob Data Reader** role at the storage-account scope to the search service's managed identity. Your user account needs **Storage Blob Data Contributor** at the storage-account scope to upload the sample files.

- A [Microsoft Foundry resource](/azure/foundry/tutorials/quickstart-create-foundry-resources) in a [region that supports Azure Content Understanding in Foundry Tools](/azure/ai-services/content-understanding/language-region-support). The search service can be in another supported region, but cross-region processing adds latency. The resource endpoint has the following format: `https://<foundry-resource-name>.services.ai.azure.com`.

- A `text-embedding-3-small` [model deployment](/azure/foundry/foundry-models/how-to/deploy-foundry-models) on the same Foundry resource used for Content Understanding. This tutorial uses that resource endpoint and deployment for both index-time and query-time vectorization with 1,536-dimensional embeddings. Assign the **Cognitive Services User** and **Cognitive Services OpenAI User** roles on the Foundry resource to the search service's managed identity.

- The [Azure CLI](/cli/azure/install-azure-cli) and a REST client that can send authenticated requests. Run `az login`, select the subscription that contains your search service, and request a bearer token for the Azure AI Search scope:

  ```azurecli
  az account get-access-token --scope https://search.azure.com/.default --query accessToken --output tsv
  ```

  Copy the returned token into the `<search-access-token>` placeholder used by every `Authorization: Bearer <search-access-token>` header in this tutorial. Access tokens expire, so request another token if you receive an authentication error. Replace every other [angle-bracketed placeholder](#placeholder-reference) before you send a request.

### Placeholder reference

This tutorial uses the following placeholders:

| Placeholder | Value |
|---|---|
| `<search-endpoint>` | `https://<search-service-name>.search.windows.net` |
| `<search-access-token>` | The Azure AI Search access token returned by the Azure CLI |
| `<storage-resource-id>` | `/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>/providers/Microsoft.Storage/storageAccounts/<storage-account-name>` |
| `<container-name>` | The name of your blob container |
| `<storage-account-name>` | Your storage account name |
| `<foundry-resource-endpoint>` | `https://<foundry-resource-name>.services.ai.azure.com` for the resource used by Content Understanding and the embedding deployment |
| `<embedding-deployment-name>` | The deployment name for `text-embedding-3-small` on the Foundry resource |

## Review the architecture

Three blob indexers write independently to the same index. You can apply the general design when multiple indexers have compatible field mappings and target the same index, but this tutorial demonstrates and verifies only folder-scoped blob indexers. Check the documentation for each [supported data source](search-data-sources-gallery.md) before adapting the design.

`sourceType` isn't an Azure AI Search system field. It's an article-defined discriminator that the JSON and CSV source records populate directly and the DOCX skillset adds during enrichment. Azure AI Search doesn't infer which indexer wrote a document.

| Pipeline | Source shape | Indexing path | Vector behavior |
|---|---|---|---|
| DOCX | One short `.docx` file | Content Understanding semantic chunking (preview), constant `sourceType` assignment, an embedding skill, and index projections | Populated |
| JSON | Two objects in a JSON array | Direct field mappings | Intentionally null |
| CSV | Two rows with first-line headers | Direct field mappings and an embedding skill | Populated |

If the sample DOCX produces one chunk, the sample result contains five search documents: one DOCX projected child, two JSON products, and two CSV tickets. The four directly indexed documents (2 JSON + 2 CSV) get their keys from the source data. The DOCX child gets a generated key from the index projection. Longer or more structured documents can produce multiple projected children.

> [!WARNING]
> Give every directly indexed source globally unique document key values, such as values prefixed with `json_` and `csv_`. Indexers use document update semantics that can combine or overwrite fields when two writes have the same key. A collision can create a document with unsafe mixed ownership.

The shared index has these fields:

- `id`, `parentId`, `sourceType`, `content`, `contentVector`, `sourceUri`, `title`, and `lastModified`.
- Nullable format-specific fields: `category`, `price`, `status`, and `priority`.

The `id` field is the index key field. Its `keyword` analyzer preserves each identifier as one exact value. JSON and CSV records supply unique document keys, while index projections generate DOCX child keys. Generated child keys can change when source content or projected chunk boundaries change, so don't predict or persist assumptions about their values.

## Prepare sample files

Each indexer reads one format from its associated folder. Create one small file per folder so that each pipeline has content to index and query from the shared index later in this tutorial.

To prepare the sample files:

1. In the `docx` folder, upload a small file named `search-overview.docx`. Add the title `Search overview` and this one-sentence paragraph: `Azure AI Search supports keyword and vector search over indexed content.` A short document normally produces one semantic chunk, but chunk count depends on document structure.

1. In the `json` folder, upload `products.json` with this two-element array:

   ```json
   [
     {
       "id": "json_product_001",
       "sourceType": "json",
       "content": "Compact wireless keyboard for shared workspaces.",
       "sourceUri": "https://<storage-account-name>.blob.core.windows.net/<container-name>/json/products.json#product-001",
       "title": "Compact wireless keyboard",
       "lastModified": "2026-08-07T00:00:00Z",
       "category": "Accessories",
       "price": 49.99
     },
     {
       "id": "json_product_002",
       "sourceType": "json",
       "content": "Adjustable monitor stand with cable management.",
       "sourceUri": "https://<storage-account-name>.blob.core.windows.net/<container-name>/json/products.json#product-002",
       "title": "Adjustable monitor stand",
       "lastModified": "2026-08-07T00:00:00Z",
       "category": "Office",
       "price": 89.50
     }
   ]
   ```

1. In the `csv` folder, upload `tickets.csv` with these two rows:

   ```csv
   id,sourceType,content,sourceUri,title,lastModified,status,priority
   csv_ticket_001,csv,"Search results omit a recently added product.","https://<storage-account-name>.blob.core.windows.net/<container-name>/csv/tickets.csv#ticket-001","Missing product",2026-08-07T00:00:00Z,open,high
   csv_ticket_002,csv,"A synonym rule needs review before deployment.","https://<storage-account-name>.blob.core.windows.net/<container-name>/csv/tickets.csv#ticket-002","Review synonym rule",2026-08-07T00:00:00Z,pending,medium
   ```

   The prefixes `json_` and `csv_` keep the directly indexed document key values unique across the two pipelines.

1. Verify that all three blobs exist in the container:

   ```azurecli
   az storage blob list \
     --account-name <storage-account-name> \
     --container-name <container-name> \
     --auth-mode login \
     --query "[].name" \
     --output tsv
   ```

   **Reference:** [az storage blob list (Azure CLI)](/cli/azure/storage/blob#az-storage-blob-list)

   Expected output:

   ```
   csv/tickets.csv
   docx/search-overview.docx
   json/products.json
   ```

   If the output doesn't list all three files, verify you uploaded each file to the correct folder path.

## Create the union-schema index

Create one index that accepts all three document shapes. Fields that a pipeline doesn't populate remain null. The vectorizer converts query text to vectors at query time, and the two skillsets use the same embedding model to generate index-time vectors.

To create the union-schema index:

1. Send the create request:

   ```http
   POST <search-endpoint>/indexes?api-version=2026-08-01-preview
   Content-Type: application/json
   Authorization: Bearer <search-access-token>

   {
     "name": "multi-source-index",
     "fields": [
       {
         "name": "id",
         "type": "Edm.String",
         "key": true,
         "searchable": true,
         "filterable": true,
         "retrievable": true,
         "analyzer": "keyword"
       },
       {
         "name": "parentId",
         "type": "Edm.String",
         "filterable": true,
         "retrievable": true
       },
       {
         "name": "sourceType",
         "type": "Edm.String",
         "filterable": true,
         "facetable": true,
         "retrievable": true
       },
       {
         "name": "content",
         "type": "Edm.String",
         "searchable": true,
         "retrievable": true
       },
       {
         "name": "contentVector",
         "type": "Collection(Edm.Single)",
         "searchable": true,
         "retrievable": false,
         "stored": false,
         "dimensions": 1536,
         "vectorSearchProfile": "content-vector-profile"
       },
       {
         "name": "sourceUri",
         "type": "Edm.String",
         "filterable": true,
         "retrievable": true
       },
       {
         "name": "title",
         "type": "Edm.String",
         "searchable": true,
         "retrievable": true
       },
       {
         "name": "lastModified",
         "type": "Edm.DateTimeOffset",
         "filterable": true,
         "sortable": true,
         "retrievable": true
       },
       {
         "name": "category",
         "type": "Edm.String",
         "filterable": true,
         "facetable": true,
         "retrievable": true
       },
       {
         "name": "price",
         "type": "Edm.Double",
         "filterable": true,
         "sortable": true,
         "retrievable": true
       },
       {
         "name": "status",
         "type": "Edm.String",
         "filterable": true,
         "facetable": true,
         "retrievable": true
       },
       {
         "name": "priority",
         "type": "Edm.String",
         "filterable": true,
         "facetable": true,
         "retrievable": true
       }
     ],
     "vectorSearch": {
       "algorithms": [
         {
           "name": "content-hnsw",
           "kind": "hnsw",
           "hnswParameters": {
             "metric": "cosine",
             "m": 4,
             "efConstruction": 400,
             "efSearch": 500
           }
         }
       ],
       "profiles": [
         {
           "name": "content-vector-profile",
           "algorithm": "content-hnsw",
           "vectorizer": "content-azure-openai-vectorizer"
         }
       ],
       "vectorizers": [
         {
           "name": "content-azure-openai-vectorizer",
           "kind": "azureOpenAI",
           "azureOpenAIParameters": {
             "resourceUri": "<foundry-resource-endpoint>",
             "deploymentId": "<embedding-deployment-name>",
             "modelName": "text-embedding-3-small"
           }
         }
       ]
     }
   }
   ```

   **Reference:** [Create Index (REST API)](/rest/api/searchservice/indexes/create?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

   The response returns HTTP `201 Created` with the full index definition.

1. Verify that the index was created:

   ```http
   GET <search-endpoint>/indexes/multi-source-index?api-version=2026-08-01-preview
   Authorization: Bearer <search-access-token>
   ```

   **Reference:** [Get Index (REST API)](/rest/api/searchservice/indexes/get?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

   The response contains `"name": "multi-source-index"` and 12 fields. Confirm the `fields` array length equals 12 and the `vectorSearch` section includes the `content-azure-openai-vectorizer`.

## Create three folder-scoped data sources

Create a separate data source for each blob folder. All three definitions can use the same storage connection and container. The `container.query` value limits each data source to one virtual folder. For example, `"query": "docx"` limits the DOCX data source to blobs under the `docx` folder.

Each indexer also uses `indexedFileNameExtensions` as a file-type allow list. The folder query and extension allow list are independent filters: the data source limits which folder the indexer enumerates, and the indexer configuration limits which file types in that folder are eligible. This example doesn't need `excludedFileNameExtensions` because each allow list contains only one extension.

To create the three folder-scoped data sources:

1. Create the DOCX data source:

   ```http
   POST <search-endpoint>/datasources?api-version=2026-08-01-preview
   Content-Type: application/json
   Authorization: Bearer <search-access-token>

   {
     "name": "docx-blob-datasource",
     "type": "azureblob",
     "credentials": {
       "connectionString": "ResourceId=<storage-resource-id>;"
     },
     "container": {
       "name": "<container-name>",
       "query": "docx"
     }
   }
   ```

   **Reference:** [Create Data Source (REST API)](/rest/api/searchservice/data-sources/create?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

   The response returns HTTP `201 Created`.

1. Create the JSON data source:

   ```http
   POST <search-endpoint>/datasources?api-version=2026-08-01-preview
   Content-Type: application/json
   Authorization: Bearer <search-access-token>

   {
     "name": "json-blob-datasource",
     "type": "azureblob",
     "credentials": {
       "connectionString": "ResourceId=<storage-resource-id>;"
     },
     "container": {
       "name": "<container-name>",
       "query": "json"
     }
   }
   ```

   **Reference:** [Create Data Source (REST API)](/rest/api/searchservice/data-sources/create?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

   The response returns HTTP `201 Created`.

1. Create the CSV data source:

   ```http
   POST <search-endpoint>/datasources?api-version=2026-08-01-preview
   Content-Type: application/json
   Authorization: Bearer <search-access-token>

   {
     "name": "csv-blob-datasource",
     "type": "azureblob",
     "credentials": {
       "connectionString": "ResourceId=<storage-resource-id>;"
     },
     "container": {
       "name": "<container-name>",
       "query": "csv"
     }
   }
   ```

   **Reference:** [Create Data Source (REST API)](/rest/api/searchservice/data-sources/create?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

   The response returns HTTP `201 Created`.

Verify that all three data sources exist:

```http
GET <search-endpoint>/datasources?api-version=2026-08-01-preview
Authorization: Bearer <search-access-token>
```

**Reference:** [List Data Sources (REST API)](/rest/api/searchservice/data-sources/list?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

The response `value` array contains `docx-blob-datasource`, `json-blob-datasource`, and `csv-blob-datasource`. If any are missing, review the corresponding creation step for errors.

## Configure the DOCX pipeline

The DOCX pipeline pairs a skillset with an indexer. The skillset uses semantic chunking (preview), assigns the `docx` discriminator, generates an embedding for each chunk, and projects each child into the shared index. The indexer binds that skillset to the `docx-blob-datasource`, reads the file by using `allowSkillsetToReadFileData`, and runs the skillset on each blob.

To configure the DOCX pipeline:

1. Create the skillset:

   ```http
   POST <search-endpoint>/skillsets?api-version=2026-08-01-preview
   Content-Type: application/json
   Authorization: Bearer <search-access-token>

   {
     "name": "docx-semantic-skillset",
     "description": "Chunk and vectorize DOCX files for the shared index.",
     "skills": [
       {
         "@odata.type": "#Microsoft.Skills.Util.ContentUnderstandingSkill",
         "name": "docx-content-understanding",
         "context": "/document",
         "chunkingProperties": {
           "method": "semantic",
           "unit": "tokens",
           "maximumLength": 500
         },
         "inputs": [
           {
             "name": "file_data",
             "source": "/document/file_data"
           }
         ],
         "outputs": [
           {
             "name": "text_sections",
             "targetName": "text_sections"
           }
         ]
       },
       {
         "@odata.type": "#Microsoft.Skills.Util.ConditionalSkill",
         "name": "docx-source-type",
         "context": "/document/text_sections/*",
         "inputs": [
           {
             "name": "condition",
             "source": "= true"
           },
           {
             "name": "whenTrue",
             "source": "= 'docx'"
           },
           {
             "name": "whenFalse",
             "source": "= null"
           }
         ],
         "outputs": [
           {
             "name": "output",
             "targetName": "source_type"
           }
         ]
       },
       {
         "@odata.type": "#Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill",
         "name": "docx-embedding",
         "context": "/document/text_sections/*",
         "resourceUri": "<foundry-resource-endpoint>",
         "deploymentId": "<embedding-deployment-name>",
         "modelName": "text-embedding-3-small",
         "dimensions": 1536,
         "inputs": [
           {
             "name": "text",
             "source": "/document/text_sections/*/content"
           }
         ],
         "outputs": [
           {
             "name": "embedding",
             "targetName": "content_vector"
           }
         ]
       }
     ],
     "cognitiveServices": {
       "@odata.type": "#Microsoft.Azure.Search.AIServicesByIdentity",
       "subdomainUrl": "<foundry-resource-endpoint>",
       "identity": null
     },
     "indexProjections": {
       "selectors": [
         {
           "targetIndexName": "multi-source-index",
           "parentKeyFieldName": "parentId",
           "sourceContext": "/document/text_sections/*",
           "mappings": [
             {
               "name": "sourceType",
               "source": "/document/text_sections/*/source_type"
             },
             {
               "name": "content",
               "source": "/document/text_sections/*/content"
             },
             {
               "name": "contentVector",
               "source": "/document/text_sections/*/content_vector"
             },
             {
               "name": "sourceUri",
               "source": "/document/metadata_storage_path"
             },
             {
               "name": "title",
               "source": "/document/metadata_storage_name"
             },
             {
               "name": "lastModified",
               "source": "/document/metadata_storage_last_modified"
             }
           ]
         }
       ],
       "parameters": {
         "projectionMode": "skipIndexingParentDocuments"
       }
     }
   }
   ```

   **Reference:** [Azure Content Understanding skill](cognitive-search-skill-content-understanding.md), [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md), and [Define an index projection](search-how-to-define-index-projections.md)

   The response returns HTTP `201 Created`.

   > [!IMPORTANT]
   > The `AIServicesByIdentity` attachment identifies the Foundry resource used for Content Understanding billing. The search service's system-assigned managed identity authenticates to that resource. Don't put endpoint or credential properties in the Content Understanding skill body.

   The Conditional skill doesn't select or exclude blobs. File selection already happens through `container.query` and `indexedFileNameExtensions` before the skillset runs. Its always-true condition only assigns the constant `docx` value to `sourceType` on each projected chunk.

1. Verify the skillset was created:

   ```http
   GET <search-endpoint>/skillsets/docx-semantic-skillset?api-version=2026-08-01-preview
   Authorization: Bearer <search-access-token>
   ```

   **Reference:** [Get Skillset (REST API)](/rest/api/searchservice/skillsets/get?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

   The response contains `"name": "docx-semantic-skillset"` and three skills in the `skills` array.

1. Create the DOCX indexer:

   ```http
   POST <search-endpoint>/indexers?api-version=2026-08-01-preview
   Content-Type: application/json
   Authorization: Bearer <search-access-token>

   {
     "name": "docx-indexer",
     "dataSourceName": "docx-blob-datasource",
     "targetIndexName": "multi-source-index",
     "skillsetName": "docx-semantic-skillset",
     "parameters": {
       "batchSize": 1,
       "configuration": {
         "dataToExtract": "contentAndMetadata",
         "parsingMode": "default",
         "indexedFileNameExtensions": ".docx",
         "allowSkillsetToReadFileData": true
       }
     },
     "fieldMappings": [],
     "outputFieldMappings": []
   }
   ```

   **Reference:** [Create Indexer (REST API)](/rest/api/searchservice/indexers/create?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

   The response returns HTTP `201 Created`. The indexer starts its first run automatically.

   Index projections create `id` and `parentId`. Don't map either field in the projection selector.

1. Check the status of the indexer:

   ```http
   GET <search-endpoint>/indexers/docx-indexer/status?api-version=2026-08-01-preview
   Authorization: Bearer <search-access-token>
   ```

   **Reference:** [Get Indexer Status (REST API)](/rest/api/searchservice/indexers/get-status?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

   Wait for `lastResult.status` to show `success` and confirm that `lastResult.itemsFailed` is `0`. If the status shows `inProgress`, wait 30 seconds and check again. You verify the projected DOCX output by querying the index later in this tutorial.

## Configure the JSON pipeline

The JSON pipeline uses an indexer alone, without a skillset. The indexer creates one search document for each array element, maps the source-owned key and other fields directly, and leaves `contentVector` null intentionally. Vector queries exclude these documents, while full-text and filtered queries can still return them.

To configure the JSON pipeline:

1. Create the JSON indexer:

   ```http
   POST <search-endpoint>/indexers?api-version=2026-08-01-preview
   Content-Type: application/json
   Authorization: Bearer <search-access-token>

   {
     "name": "json-indexer",
     "dataSourceName": "json-blob-datasource",
     "targetIndexName": "multi-source-index",
     "parameters": {
       "configuration": {
         "parsingMode": "jsonArray",
         "indexedFileNameExtensions": ".json"
       }
     },
     "fieldMappings": [
       {
         "sourceFieldName": "/id",
         "targetFieldName": "id"
       },
       {
         "sourceFieldName": "/sourceType",
         "targetFieldName": "sourceType"
       },
       {
         "sourceFieldName": "/content",
         "targetFieldName": "content"
       },
       {
         "sourceFieldName": "/sourceUri",
         "targetFieldName": "sourceUri"
       },
       {
         "sourceFieldName": "/title",
         "targetFieldName": "title"
       },
       {
         "sourceFieldName": "/lastModified",
         "targetFieldName": "lastModified"
       },
       {
         "sourceFieldName": "/category",
         "targetFieldName": "category"
       },
       {
         "sourceFieldName": "/price",
         "targetFieldName": "price"
       }
     ],
     "outputFieldMappings": []
   }
   ```

   **Reference:** [Create Indexer (REST API)](/rest/api/searchservice/indexers/create?view=rest-searchservice-2026-08-01-preview&preserve-view=true), [Index JSON blobs and files](search-how-to-index-azure-blob-json.md), and [Define field mappings](search-indexer-field-mappings.md)

   The response returns HTTP `201 Created`. The indexer starts its first run automatically.

1. Verify that the indexer processed both records:

   ```http
   GET <search-endpoint>/indexers/json-indexer/status?api-version=2026-08-01-preview
   Authorization: Bearer <search-access-token>
   ```

   **Reference:** [Get Indexer Status (REST API)](/rest/api/searchservice/indexers/get-status?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

   Wait for `lastResult.status` to show `success` and confirm that `lastResult.itemsFailed` is `0`. If the status shows `inProgress`, wait 15 seconds and check again. You verify both JSON records by querying the index later in this tutorial.

## Configure the CSV pipeline

The CSV pipeline pairs a skillset with an indexer. The indexer creates one search document for each row, maps the source-owned key and other fields directly, and maps the skillset's embedding to `contentVector`. Because these documents carry vectors, both full-text and vector queries can return them.

To configure the CSV pipeline:

1. Create the CSV skillset:

   ```http
   POST <search-endpoint>/skillsets?api-version=2026-08-01-preview
   Content-Type: application/json
   Authorization: Bearer <search-access-token>

   {
     "name": "csv-embedding-skillset",
     "description": "Vectorize CSV ticket content for the shared index.",
     "skills": [
       {
         "@odata.type": "#Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill",
         "name": "csv-embedding",
         "context": "/document",
         "resourceUri": "<foundry-resource-endpoint>",
         "deploymentId": "<embedding-deployment-name>",
         "modelName": "text-embedding-3-small",
         "dimensions": 1536,
         "inputs": [
           {
             "name": "text",
             "source": "/document/content"
           }
         ],
         "outputs": [
           {
             "name": "embedding",
             "targetName": "csv_content_vector"
           }
         ]
       }
     ]
   }
   ```

   **Reference:** [Create Skillset (REST API)](/rest/api/searchservice/skillsets/create?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

   The response returns HTTP `201 Created`.

1. Verify the skillset was created:

   ```http
   GET <search-endpoint>/skillsets/csv-embedding-skillset?api-version=2026-08-01-preview
   Authorization: Bearer <search-access-token>
   ```

   **Reference:** [Get Skillset (REST API)](/rest/api/searchservice/skillsets/get?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

   The response contains `"name": "csv-embedding-skillset"` and one skill in the `skills` array.

1. Create the CSV indexer:

   ```http
   POST <search-endpoint>/indexers?api-version=2026-08-01-preview
   Content-Type: application/json
   Authorization: Bearer <search-access-token>

   {
     "name": "csv-indexer",
     "dataSourceName": "csv-blob-datasource",
     "targetIndexName": "multi-source-index",
     "skillsetName": "csv-embedding-skillset",
     "parameters": {
       "configuration": {
         "parsingMode": "delimitedText",
         "firstLineContainsHeaders": true,
         "delimitedTextDelimiter": ",",
         "indexedFileNameExtensions": ".csv"
       }
     },
     "fieldMappings": [
       {
         "sourceFieldName": "id",
         "targetFieldName": "id"
       },
       {
         "sourceFieldName": "sourceType",
         "targetFieldName": "sourceType"
       },
       {
         "sourceFieldName": "content",
         "targetFieldName": "content"
       },
       {
         "sourceFieldName": "sourceUri",
         "targetFieldName": "sourceUri"
       },
       {
         "sourceFieldName": "title",
         "targetFieldName": "title"
       },
       {
         "sourceFieldName": "lastModified",
         "targetFieldName": "lastModified"
       },
       {
         "sourceFieldName": "status",
         "targetFieldName": "status"
       },
       {
         "sourceFieldName": "priority",
         "targetFieldName": "priority"
       }
     ],
     "outputFieldMappings": [
       {
         "sourceFieldName": "/document/csv_content_vector",
         "targetFieldName": "contentVector"
       }
     ]
   }
   ```

   **Reference:** [Create Indexer (REST API)](/rest/api/searchservice/indexers/create?view=rest-searchservice-2026-08-01-preview&preserve-view=true), [Index CSV blobs and files](search-how-to-index-azure-blob-csv.md), and [Output field mappings](cognitive-search-output-field-mapping.md)

   The response returns HTTP `201 Created`. The indexer starts its first run automatically.

1. Verify that the indexer processed both rows:

   ```http
   GET <search-endpoint>/indexers/csv-indexer/status?api-version=2026-08-01-preview
   Authorization: Bearer <search-access-token>
   ```

   **Reference:** [Get Indexer Status (REST API)](/rest/api/searchservice/indexers/get-status?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

   Wait for `lastResult.status` to show `success` and confirm that `lastResult.itemsFailed` is `0`. If the status shows `inProgress`, wait 15 seconds and check again. You verify both CSV rows by querying the index later in this tutorial.

## Run and monitor the indexers

Each indexer starts its first run automatically when you create it. To start another run and verify the results:

1. Run the three indexers:

   ```http
   POST <search-endpoint>/indexers/docx-indexer/run?api-version=2026-08-01-preview
   Content-Type: application/json
   Content-Length: 0
   Authorization: Bearer <search-access-token>
   ```

   ```http
   POST <search-endpoint>/indexers/json-indexer/run?api-version=2026-08-01-preview
   Content-Type: application/json
   Content-Length: 0
   Authorization: Bearer <search-access-token>
   ```

   ```http
   POST <search-endpoint>/indexers/csv-indexer/run?api-version=2026-08-01-preview
   Content-Type: application/json
   Content-Length: 0
   Authorization: Bearer <search-access-token>
   ```

   **Reference:** [Run Indexer (REST API)](/rest/api/searchservice/indexers/run?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

    Each run request returns HTTP `202 Accepted` with an empty body. Some REST clients require the `Content-Length: 0` header for a request without a body.

   > [!NOTE]
   > If the source data didn't change since the last run, an indexer might report `itemsProcessed` as `0`. This behavior is expected because indexers use change detection and skip blobs that aren't modified.

1. Check the status of each indexer:

   ```http
   GET <search-endpoint>/indexers/docx-indexer/status?api-version=2026-08-01-preview
   Authorization: Bearer <search-access-token>
   ```

   ```http
   GET <search-endpoint>/indexers/json-indexer/status?api-version=2026-08-01-preview
   Authorization: Bearer <search-access-token>
   ```

   ```http
   GET <search-endpoint>/indexers/csv-indexer/status?api-version=2026-08-01-preview
   Authorization: Bearer <search-access-token>
   ```

   **Reference:** [Get Indexer Status (REST API)](/rest/api/searchservice/indexers/get-status?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

   For each indexer, confirm that `lastResult.status` is `success` and `lastResult.itemsFailed` is `0`. The service reports processing details in `lastResult`; verify the indexed document counts in the next section because projected chunks and parsed records don't necessarily correspond one-to-one with source blobs.

## Query the shared index

Use the following requests to verify the combined result.

### Verify the union result

Return all documents written by the three indexers:

```http
POST <search-endpoint>/indexes/multi-source-index/docs/search?api-version=2026-08-01-preview
Content-Type: application/json
Authorization: Bearer <search-access-token>

{
  "search": "*",
  "select": "id,parentId,sourceType,title",
  "count": true
}
```

**Reference:** [Search Documents (REST API)](/rest/api/searchservice/documents/search-post?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

The result contains two JSON products, two CSV tickets, and one or more DOCX chunks. If the sample DOCX produces one chunk, `@odata.count` is `5`. Confirm all three `sourceType` values appear: `docx`, `json`, and `csv`.

### Query by discriminator

Return the two JSON products:

```http
POST <search-endpoint>/indexes/multi-source-index/docs/search?api-version=2026-08-01-preview
Content-Type: application/json
Authorization: Bearer <search-access-token>

{
  "search": "*",
  "filter": "sourceType eq 'json'",
  "select": "id,sourceType,title,category,price",
  "count": true
}
```

**Reference:** [Search Documents (REST API)](/rest/api/searchservice/documents/search-post?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

Confirm `@odata.count` is `2`. Both results have `category` and `price` values. The `status` and `priority` fields aren't in the select list because they belong to the CSV schema.

### Run a full-text query

Full-text search considers all documents with matching searchable text, including JSON records with null vectors.

```http
POST <search-endpoint>/indexes/multi-source-index/docs/search?api-version=2026-08-01-preview
Content-Type: application/json
Authorization: Bearer <search-access-token>

{
  "search": "search product",
  "searchFields": "content,title",
  "select": "id,parentId,sourceType,title,content",
  "count": true
}
```

**Reference:** [Search Documents (REST API)](/rest/api/searchservice/documents/search-post?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

Results include documents from any source type that contains "search" or "product" in their `content` or `title` fields. With the sample data, expect matches from the DOCX chunk (contains "search") and the CSV ticket (contains "product").

### Run a vector query

Send text to the index vectorizer instead of pasting 1,536 vector values. The results contain vector-bearing DOCX and CSV documents, not JSON documents whose `contentVector` is null.

```http
POST <search-endpoint>/indexes/multi-source-index/docs/search?api-version=2026-08-01-preview
Content-Type: application/json
Authorization: Bearer <search-access-token>

{
  "vectorQueries": [
    {
      "kind": "text",
      "text": "search indexing issue",
      "fields": "contentVector",
      "k": 3
    }
  ],
  "select": "id,parentId,sourceType,title,content"
}
```

**Reference:** [Search Documents (REST API)](/rest/api/searchservice/documents/search-post?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

Confirm that no results have `"sourceType": "json"`. JSON documents are excluded because their `contentVector` is null.

### Run a filtered vector query

Limit vector results to CSV tickets:

```http
POST <search-endpoint>/indexes/multi-source-index/docs/search?api-version=2026-08-01-preview
Content-Type: application/json
Authorization: Bearer <search-access-token>

{
  "filter": "sourceType eq 'csv'",
  "vectorFilterMode": "preFilter",
  "vectorQueries": [
    {
      "kind": "text",
      "text": "deployment review",
      "fields": "contentVector",
      "k": 2
    }
  ],
  "select": "id,sourceType,title,status,priority"
}
```

**Reference:** [Search Documents (REST API)](/rest/api/searchservice/documents/search-post?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

Confirm that all results have `"sourceType": "csv"` and include the `status` and `priority` fields.

### Run a hybrid query

Combine keyword and vector retrieval in one request:

```http
POST <search-endpoint>/indexes/multi-source-index/docs/search?api-version=2026-08-01-preview
Content-Type: application/json
Authorization: Bearer <search-access-token>

{
  "search": "search issue",
  "searchFields": "content,title",
  "vectorQueries": [
    {
      "kind": "text",
      "text": "search issue",
      "fields": "contentVector",
      "k": 3
    }
  ],
  "select": "id,parentId,sourceType,title,content"
}
```

**Reference:** [Search Documents (REST API)](/rest/api/searchservice/documents/search-post?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

Hybrid queries combine keyword matches (which can include JSON documents) with vector matches (which exclude null-vector documents). The merged result set can contain documents from all three source types when both keyword and vector terms match across pipelines.

For more query options, see [Create a vector query](vector-search-how-to-query.md) and [Create a hybrid query](hybrid-search-how-to-query.md).

## Operate and reconcile indexed content

Treat each indexer as an independent writer and define ownership and cleanup rules for its document key values.

- Monitor, schedule, run, and reset each indexer separately. A failure in one pipeline doesn't remove documents already written by another pipeline. For example, a malformed CSV can cause `csv-indexer` to fail without making existing documents or the other indexers unavailable. For scheduling options and detailed status fields, see [Schedule an indexer](search-howto-schedule-indexers.md) and [Monitor indexer status](search-monitor-indexers.md).

- Keep direct JSON and CSV keys stable and globally unique. Don't reuse a key between pipelines.

- Expect DOCX projection reruns to reconcile stale child documents through their parent relationship. Generated child keys can change, so identify a projected group by `parentId` instead of predicting child keys. For projection lifecycle details, see [Content lifecycle](search-how-to-define-index-projections.md#content-lifecycle).

- Configure an appropriate [blob deletion detection policy](search-how-to-index-azure-blob-changed-deleted.md) before relying on a deleted DOCX parent blob to remove its projected children.

> [!CAUTION]
> Direct one-to-many parsing requires application-owned cleanup. Blob deletion detection policies don't apply to the search documents created from JSON array elements or CSV rows. Removing an element or row, or deleting its source blob, can leave target documents in the index. Delete each orphan explicitly by key with [Delete documents](search-how-to-delete-documents.md) or rebuild the index from the authoritative set of document keys.

## Troubleshooting

The following table lists common issues and resolutions when running the three pipelines.

| Symptom | Possible cause | Resolution |
|---|---|---|
| Indexer status shows `transientFailure` or `persistentFailure` | The Foundry resource is unreachable, or the search service's managed identity lacks access. | Verify the `subdomainUrl` and `resourceUri` values. Confirm the search service's managed identity has the **Cognitive Services User** and **Cognitive Services OpenAI User** roles on the Foundry resource. |
| `lastResult.itemsFailed` is greater than zero | A source document has an unexpected format, or the embedding skill received empty text. | Check `lastResult.errors` in the indexer status response for the specific error message and the document key that failed. |
| `@odata.count` is lower than expected after all indexers succeed | An indexer hasn't finished its run, the DOCX produced a different number of chunks, or a key collision overwrote a document. | Wait for all three indexers to report `success`. Confirm all three `sourceType` values appear, and verify that JSON and CSV keys use distinct prefixes (`json_`, `csv_`). |
| Vector query returns zero results | The vectorizer configuration in the index doesn't match the embedding model used at index time, or no documents have populated `contentVector` values. | Confirm the vectorizer's `deploymentId` and `modelName` match the values in the skillsets. Confirm DOCX and CSV indexers completed with zero failures. |
| JSON documents appear in vector query results | The JSON indexer populated `contentVector` unexpectedly. | Confirm `json-indexer` has no `outputFieldMappings` that target `contentVector`. JSON records should leave `contentVector` null. |
| CSV indexer fails with parsing errors | The CSV file has unescaped commas, mismatched quotes, or encoding issues. | Open the CSV file and verify that fields with commas are enclosed in double quotes. Save the file with UTF-8 encoding. |
| Content Understanding skill fails with `403 Forbidden` | The search service's managed identity lacks access, or the resource doesn't support Content Understanding in the selected region. | Confirm the managed identity has the **Cognitive Services User** role on the Foundry resource, and confirm the resource is in a [supported region](/azure/ai-services/content-understanding/language-region-support). |
| `"The index 'multi-source-index' was not found"` error during queries | The index wasn't created, or you sent the query to the wrong search service. | Verify `<search-endpoint>` points to the correct service. Run `GET <search-endpoint>/indexes?api-version=2026-08-01-preview` to list indexes. |
| Run indexer request returns HTTP `411 Length Required` | The POST request has no body, and the REST client didn't send a `Content-Length` header. | Add `Content-Length: 0` to the request headers. Some REST clients require this header explicitly for POST requests with empty bodies. |
| Re-run shows `itemsProcessed` equal to `0` | The source blobs haven't changed since the last run. | This is expected behavior. Indexers use change detection and skip unchanged blobs. To force reprocessing, reset the indexer first by sending `POST <search-endpoint>/indexers/<indexer-name>/reset?api-version=2026-08-01-preview` with `Content-Length: 0` and the bearer token header. |

## Clean up resources

When you no longer need the Azure AI Search objects you created in this tutorial, delete them in the following dependency order:

1. Delete the indexers:

   ```http
   DELETE <search-endpoint>/indexers/docx-indexer?api-version=2026-08-01-preview
   Authorization: Bearer <search-access-token>
   ```

   ```http
   DELETE <search-endpoint>/indexers/json-indexer?api-version=2026-08-01-preview
   Authorization: Bearer <search-access-token>
   ```

   ```http
   DELETE <search-endpoint>/indexers/csv-indexer?api-version=2026-08-01-preview
   Authorization: Bearer <search-access-token>
   ```

   **Reference:** [Delete Indexer (REST API)](/rest/api/searchservice/indexers/delete?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

   Each delete operation returns HTTP `204 No Content` on success. If you receive `404 Not Found`, the indexer was already deleted.

1. Delete the skillsets:

   ```http
   DELETE <search-endpoint>/skillsets/docx-semantic-skillset?api-version=2026-08-01-preview
   Authorization: Bearer <search-access-token>
   ```

   ```http
   DELETE <search-endpoint>/skillsets/csv-embedding-skillset?api-version=2026-08-01-preview
   Authorization: Bearer <search-access-token>
   ```

   **Reference:** [Delete Skillset (REST API)](/rest/api/searchservice/skillsets/delete?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

   Each delete operation returns HTTP `204 No Content` on success.

1. Delete the data sources:

   ```http
   DELETE <search-endpoint>/datasources/docx-blob-datasource?api-version=2026-08-01-preview
   Authorization: Bearer <search-access-token>
   ```

   ```http
   DELETE <search-endpoint>/datasources/json-blob-datasource?api-version=2026-08-01-preview
   Authorization: Bearer <search-access-token>
   ```

   ```http
   DELETE <search-endpoint>/datasources/csv-blob-datasource?api-version=2026-08-01-preview
   Authorization: Bearer <search-access-token>
   ```

   **Reference:** [Delete Data Source (REST API)](/rest/api/searchservice/data-sources/delete?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

   Each delete operation returns HTTP `204 No Content` on success.

1. Delete the index:

   ```http
   DELETE <search-endpoint>/indexes/multi-source-index?api-version=2026-08-01-preview
   Authorization: Bearer <search-access-token>
   ```

   **Reference:** [Delete Index (REST API)](/rest/api/searchservice/indexes/delete?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

   Returns HTTP `204 No Content` on success.

1. Verify the indexers are removed:

   ```http
   GET <search-endpoint>/indexers?api-version=2026-08-01-preview
   Authorization: Bearer <search-access-token>
   ```

   **Reference:** [List Indexers (REST API)](/rest/api/searchservice/indexers/list?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

   Confirm that `docx-indexer`, `json-indexer`, and `csv-indexer` no longer appear in the response.

1. If you created a resource group for this exercise, delete it and all resources it contains:

   ```azurecli
   az group delete --name <resource-group-name> --yes --no-wait
   ```

   **Reference:** [az group delete (Azure CLI)](/cli/azure/group#az-group-delete)

   The command returns immediately and deletes the resource group and all its resources asynchronously.

## Related content

- [Create an indexer](search-how-to-create-indexers.md)
- [Index data from Azure Blob Storage](search-how-to-index-azure-blob-storage.md)
- [Define an index projection](search-how-to-define-index-projections.md)
- [Schedule an indexer](search-howto-schedule-indexers.md)
- [Monitor indexer status](search-monitor-indexers.md)
