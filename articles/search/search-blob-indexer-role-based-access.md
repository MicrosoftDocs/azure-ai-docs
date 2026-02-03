---  
title: Use a Blob Indexer or Knowledge Source to Ingest RBAC Scopes Metadata
titleSuffix: Azure AI Search  
description: Learn how to configure Azure AI Search knowledge sources and indexers for ingesting Azure Role-Based Access (RBAC) metadata on Azure blobs.
ms.service: azure-ai-search  
ms.topic: how-to
ms.date: 11/18/2025
author: vaishalishah
ms.author: vaishalishah
---  

# Use a blob indexer or knowledge source to ingest RBAC scopes metadata

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Azure Storage allows for role-based access on containers in blob storage, where roles like **Storage Blob Data Reader** or **Storage Blob Data Contributor** determine whether someone has access to content. Preview APIs in Azure AI Search now support ingestion of user permissions alongside document ingestion so that you can use those permissions to control access to search results. If a user lacks permissions on a specific directory or file in Azure Storage, that user doesn't have access to the corresponding documents in Azure AI Search results, even if you personally have a **Search Index Data Reader** assignment *on the index*.

+ 2025-05-01-preview and later, RBAC scopes metadata can be ingested using the [Blob indexer](search-how-to-index-azure-data-lake-storage.md).
+ 2025-11-01-preview provides equivalent support for [Blob knowledge sources](agentic-knowledge-source-how-to-blob.md) in Azure Storage.

RBAC scope is set at the container level and flows to all blobs (documents) through permission inheritance. RBAC scope is captured during indexing as permission metadata. You can use the push APIs to upload and index content and permission metadata manually (see [Indexing Permissions using the push REST API](search-index-access-control-lists-and-rbac-push-api.md)), or you can use an indexer or knowledge source to automate data ingestion. This article focuses on indexing automation.

At query time, the identity of the caller is included in the request header via the `x-ms-query-source-authorization` parameter. The identity must match the permission metadata on documents if the user is to see the search results.

This article focuses on the indexing automation approaches, built on this foundation:

+ [Azure Storage blobs secured using role-based access control (Azure RBAC)](/azure/storage/blobs/data-lake-storage-access-control-model#role-based-access-control-azure-rbac). There's no support for Attribute-based access control (Azure ABAC).

+ [Azure Blob indexer](#configure-indexer-based-indexing) or a [Blob knowledge source](#configure-a-knowledge-source) that retrieves and ingests data and metadata, including permission filters. To get permission filter support, use the latest preview REST API or a preview package of an Azure SDK that supports the feature.

+ [An index in Azure AI Search](search-how-to-create-search-index.md) containing the ingested documents and corresponding permissions. Permission metadata is stored as fields in the index. 

+ [A query that uses permission filters](search-query-access-control-rbac-enforcement.md). To set up queries that respect the permission filters, use the latest preview REST API or a preview package of an Azure SDK that supports the feature.

## Prerequisites

+ [Microsoft Entra ID authentication and authorization](/entra/identity/authentication/overview-authentication). Services and apps must be in the same tenant. Users can be in different tenants as long as all of the tenants are Microsoft Entra ID. Role assignments are used for each authenticated connection.

+ Azure AI Search, any region, but you must have a billable tier (basic and higher) for managed identity support. The search service must be [configured for role-based access](search-security-enable-roles.md) and it must [have a managed identity (either system or user)](search-how-to-managed-identities.md).

+ Azure Storage, Standard performance (general-purpose v2), on hot, cool, and cold access tiers, with RBAC-secured containers or blobs.

+ You should understand how indexers and knowledge sources work and how to create an index. This article explains the configuration settings for the data source and indexer, but doesn't provide steps for creating the index. For more information about indexes designed for permission filters, see [Create an index with permission filter fields](search-index-access-control-lists-and-rbac-push-api.md#create-an-index-with-permission-filter-fields).

+ This functionality is currently not supported in the Azure portal, this includes Permission filters created through the [Import wizards](search-import-data-portal.md). Use a programmatic approach to create or modify existing objects for document-level access. 

## Configure Blob storage

Verify your blob container uses role-based access.

1. Sign in to the Azure portal and find your storage account.

1. Expand **containers** and select the container that has the blobs you want to index.

1. Select **Access Control (IAM)** to check role assignments. Users and groups with **Storage Blob Data Reader** or **Storage Blob Data Contributor** will have access to search documents in the index after the container is indexed.

### Authorization

For indexer execution, your search service identity must have **Storage Blob Data Reader** permission. For more information, see [Connect to Azure Storage using a managed identity](search-howto-managed-identities-storage.md).

## Configure Azure AI Search

Recall that the search service must have:

+ [Role-based access enabled](search-security-enable-roles.md)
+ [Managed identity configured](search-how-to-managed-identities.md)

### Authorization

For indexer execution, the client issuing the API call must have **Search Service Contributor** permission to create objects, **Search Index Data Contributor** permission to perform data import, and **Search Index Data Reader** to query an index see [Connect to Azure AI Search using roles](search-security-rbac.md).

## Configure a knowledge source

If you're using a knowledge source, definitions in the knowledge source are used to generate a full indexing pipeline (indexer, data source, and index). RBAC scope is detected and automatically included in the generated index. There's no need to modify any of the generated objects if you want permission inheritance in your indexed content.

Key points about the configuration that make it work for this scenario:

+ `isADLSGen2` is set to false, which means the data source is Azure Blob storage.
+ `ingestionPermissionOptions` specifies `rbacScope`.

```http
# Create / Update Azure Blob Knowledge Source
###
PUT {{url}}/knowledgesources/azure-blob-ks?api-version=2025-11-01-preview
api-key: {{key}}
Content-Type: application/json
 
{
    "name": "azure-blob-ks",
    "kind": "azureBlob",
    "description": "A sample azure blob knowledge source",
    "azureBlobParameters": {
        "connectionString": "{{blob-connection-string}}",
        "containerName": "blobcontainer",
        "folderPath": null,
        "isADLSGen2": false,
        "ingestionParameters": {
            "identity": null,
            "embeddingModel": {
                "kind": "azureOpenAI",
                "azureOpenAIParameters": {
                    "deploymentId": "text-embedding-3-large",
                    "modelName": "text-embedding-3-large",
                    "resourceUri": "{{aoai-endpoint}}",
                    "apiKey": "{{aoai-key}}"
                }
            },
            "chatCompletionModel": null,
            "disableImageVerbalization": true,
            "ingestionSchedule": null,
            "ingestionPermissionOptions": ["rbacScope"],
            "contentExtractionMode": "minimal",
            "aiServices": {
                "uri": "{{ai-endpoint}}",
                "apiKey": "{{ai-key}}"
            }
        }
    }
}
```

## Configure indexer-based indexing

If you're using an indexer, configure it, the data source, and the index to pull permission metadata from blobs.

### Create the data source

+ Data Source type must be `azureblob`.

+ Data source parsing mode must be the default.

+ Data source must have `indexerPermissionOptions` with `rbacScope`.

  + For `rbacScope`, configure the [connection string](search-how-to-index-azure-data-lake-storage.md#supported-credentials-and-connection-strings) with managed identity format.
  
  + For connection strings using a [user-assigned managed identity](search-howto-managed-identities-storage.md#user-assigned-managed-identity-preview), you must also specify the `identity` property.

<!-- Question/Comment: check this example -->
JSON example with system managed identity and `indexerPermissionOptions`:

```json
{
    "name" : "my-blob-datasource",
    "type": "azureblob",
    "indexerPermissionOptions": ["rbacScope"],
    "credentials": {
    "connectionString": "ResourceId=/subscriptions/<your subscription ID>/resourceGroups/<your resource group name>/providers/Microsoft.Storage/storageAccounts/<your storage account name>/;"
    },
    "container": {
        "name": "<your-container-name>",
        "query": "<optional-query-used-for-selecting-specific-blobs>"
    }
}
```

JSON schema example with a user-managed identity in the connection string:

```json
{
    "name" : "my-blob-datasource",
    "type": "azureblob",
    "indexerPermissionOptions": ["rbacScope"],
    "credentials": {
    "connectionString": "ResourceId=/subscriptions/<your subscription ID>/resourceGroups/<your resource group name>/providers/Microsoft.Storage/storageAccounts/<your storage account name>/;"
    },
    "container": {
        "name": "<your-container-name>",
        "query": "<optional-query-used-for-selecting-specific-blobs>"
    },
    "identity": {
        "@odata.type": "#Microsoft.Azure.Search.DataUserAssignedIdentity",
        "userAssignedIdentity": "/subscriptions/{subscription-ID}/resourceGroups/{resource-group-name}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{user-assigned-managed-identity-name}"
    }
}
```

### Create permission fields in the index

In Azure AI Search, make sure your index contains field definitions for the permission metadata. Permission metadata can be indexed when `indexerPermissionOptions` is specified in the data source definition.

Recommended schema attributes RBAC Scope:

+ RBAC scope field with `rbacScope` permissionFilter value.
+ Property `permissionFilterOption` to enable filtering at querying time.
+ Use string fields for permission metadata
+ Set `filterable` to true on all fields.

Notice that `retrievable` is false. You can set it true during development to verify permissions are present, but remember to set to back to false before deploying to a production environment so that security principal identities aren't visible in results.

JSON schema example:

```json
{
  ...
  "fields": [
    ...
    { 
        "name": "RbacScope", 
        "type": "Edm.String", 
        "permissionFilter": "rbacScope", 
        "filterable": true, 
        "retrievable": false 
    }
  ],
  "permissionFilterOption": "enabled"
}
```

### Configure the indexer

Field mappings within an indexer set the data path to fields in an index. Target and destination fields that vary by name or data type require an explicit field mapping. The following metadata fields in Azure Blob Storage might need field mappings if you vary the field name:

+ **metadata_rbac_scope** (`Edm.String`) - the container RBAC scope.

Specify `fieldMappings` in the indexer to route the permission metadata to target fields during indexing.

JSON schema example:

```json
{
  ...
  "fieldMappings": [
    { "sourceFieldName": "metadata_rbac_scope", "targetFieldName": "RbacScope" }
  ]
}
```

### Run the indexer

Once your indexer, data source, and index are configured, run the indexer to set the process in motion. If there's a problem with configuration or permissions, those problems will surface in this step.

By default, an indexer runs as soon as you post it to a search service, but if the indexer configuration includes `disabled` set to true, the indexer is posted in a disabled state so that you can run the indexer manually.

We recommend [running the indexer from the Azure portal](search-howto-run-reset-indexers.md#how-to-reset-and-run-indexers) so that you can monitor status and messages.

Assuming no errors, the index is now populated and you can move forward with [queries and testing](search-query-access-control-rbac-enforcement.md).

## Deletion tracking 

To effectively manage blob deletion, ensure that you have enabled [deletion tracking](search-how-to-index-azure-blob-changed-deleted.md) before your indexer runs for the first time. This feature allows the system to detect deleted blobs from your source and delete the corresponding content from the index.  

## See also

+ [Connect to Azure AI Search using roles](search-security-rbac.md)
- [Query-time ACL and RBAC enforcement](search-query-access-control-rbac-enforcement.md)
- [azure-search-python-samples/Quickstart-Document-Permissions-Push-API](https://github.com/Azure-Samples/azure-search-python-samples/blob/main/Quickstart-Document-Permissions-Push-API)
+ [Search over Azure Blob Storage content](search-blob-storage-integration.md)
+ [Configure a blob indexer](search-how-to-index-azure-blob-storage.md)
