---  
title: Use a Blob indexer to ingest Rbac scopes metadata
titleSuffix: Azure AI Search  
description: Learn how to configure Azure AI Search indexers for ingesting Azure Role-Based Access (RBAC) metadata on Azure Blobs.
ms.service: azure-ai-search  
ms.topic: how-to
ms.date: 07/07/2025  
author: vaishalishah
ms.author: vaishalishah
---  

# Use a Blob indexer to ingest Rbac scopes metadata

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Starting in 2025-05-01-preview, you can now include Rbac scope alongside document ingestion in Azure AI Search and use those permissions to control access to search results.

You can use the push APIs to upload and index content and permission metadata manually see [Indexing Permissions using the push REST API](search-index-access-control-lists-and-rbac-push-api.md), or you can use an indexer to automate data ingestion. This article focuses on the indexer approach.

The indexer approach is built on this foundation:

+ [Role-based access control (Azure RBAC)](/azure/storage/blobs/data-lake-storage-access-control-model#role-based-access-control-azure-rbac). There's no support for Attribute-based access control (Azure ABAC).

+ [An Azure AI Search indexer for Blob](search-howto-indexing-azure-blob-storage.md) that retrieves and ingests data and metadata, including permission filters. To get permission filter support, you must use the 2025-05-01-preview REST API or a prerelease package of an Azure SDK that supports the feature.

+ [An index in Azure AI Search](search-how-to-create-search-index.md) containing the ingested documents and corresponding permissions. Permission metadata is stored as fields in the index. To set up queries that respect the permission filters, you must use the 2025-05-01-preview REST API or a prerelease package of an Azure SDK that supports the feature.

## Prerequisites

+ Microsoft Entra ID authentication and authorization. Services and apps must be in the same tenant. Role assignments are used for each authenticated connection.

+ Azure AI Search, any region, but you must have a billable tier (basic and higher) for managed identity support. The search service must be [configured for role-based access](search-security-enable-roles.md) and it must [have a managed identity (either system or user)](search-howto-managed-identities-data-sources.md).

## Limitations

+ The following indexer features don't support permission preservation capabilities but are otherwise operational for Azure Blob content-only indexing:
  + One-to-many [parsing modes](/rest/api/searchservice/indexers/create?view=rest-searchservice-2025-05-01-preview&preserve-view=true#blobindexerparsingmode), such as: `delimitedText`, `jsonArray`, `jsonLines`, and `markdown` with sub-mode `oneToMany`


### Authorization

For indexer execution, your search service identity must have **Storage Blob Data Reader** permission. 

If you're testing locally, you should also have a **Storage Blob Data Reader** role assignment. For more information, see [Connect to Azure Storage using a managed identity](search-howto-managed-identities-storage.md).

## Configure Azure AI Search for indexing permission filters

Recall that the search service must have:

+ [Role-based access enabled](search-security-enable-roles.md)
+ [Managed identity configured](search-howto-managed-identities-data-sources.md)

### Authorization

For indexer execution, the client issuing the API call must have **Search Service Contributor** permission to create objects, **Search Index Data Contributor** permission to perform data import, and **Search Index Data Reader** to query an index. 

If you're testing locally, you should have the same role assignments. For more information, see [Connect to Azure AI Search using roles](search-security-rbac.md).

## Indexing permission metadata

In Azure AI Search, configure an indexer, data source, and index to pull permission metadata from blobs.

### Configure the data source

+ Data Source type must be `azureblob`.

+ Data source must have `indexerPermissionOptions` with `rbacScope`.

  + For`rbacScope`, configure the [connection string](search-howto-index-azure-data-lake-storage.md#supported-credentials-and-connection-strings) with managed identity format.
  
  + For connection strings using a [user-assigned managed identity](search-howto-managed-identities-storage.md#user-assigned-managed-identity), you must also specify the `identity` property.

<!-- Question/Comment: check this example -->
JSON example with system managed identity:

```json
{
    "name" : "my-blob-datasource",
    "type": "azureblob",
    "indexerPermissionOptions": ["rbacScope"],
    "credentials": {
    "connectionString": "ResourceId=/subscriptions/<your subscription ID>/resourceGroups/<your resource group name>/providers/Microsoft.Storage/storageAccounts/<your storage account name>/;"
    },
    "container": {
        "name": "<your container name>",
        "query": "<optional-query>"
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
        "name": "<your container name>",
        "query": "<optional-query>"
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

Notice that `retrievable` is false. You can set it true during development to verify permissions are present, but remember to set to back to false before deploying to a production environment.

JSON schema example:

```json
{
  ...
  "fields": [
    ...
    { "name": "RbacScope", "type": "Edm.String", "permissionFilter": "rbacScope", "filterable": true, "retrievable": false }
  ],
  "permissionFilterOption": "enabled"
}
```

### Configure the indexer

Field mappings within an indexer set the data path to fields in an index. Target and destination fields that vary by name or data type require an explicit field mapping. The following metadata fields in Azure Blob might need field mappings if you vary the field name:

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

## Deletion tracking 

To effectively manage blob deletion, ensure that you have enabled [deletion tracking](search-howto-index-changed-deleted-blobs.md) before your indexer runs for the first time. This feature allows the system to detect deleted blobs from your source and have them deleted from the index.  

