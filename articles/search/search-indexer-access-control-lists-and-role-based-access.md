---  
title: Use ADLS Gen2 indexer to ingest permission metadata
titleSuffix: Azure AI Search  
description: Learn how to configure Azure AI Search indexers for ingesting Access Control Lists (ACLs) and Azure Role-Based Access (RBAC) metadata on Azure Data Lake Storage (ADLS) Gen2 blobs.
ms.service: azure-ai-search  
ms.topic: how-to
ms.date: 04/29/2025  
author: wlifuture
ms.author: wli
---  

# Use an ADLS Gen2 indexer to ingest permission metadata and filter search results based on user access rights

> [!IMPORTANT]
> This feature is in public preview. It's offered "as-is", under [Supplemental Terms of Use](https://azure.microsoft.com/support/legal/preview-supplemental-terms/) and supported on best effort only. Preview features aren't recommended for production workloads and aren't guaranteed to become generally available.

The permission model in Azure Data Lake Storage (ADLS) Gen2 can be used for per-user access to specific directories or files. Starting in 2025-05-01-preview, you can now include user permissions alongside document ingestion in Azure AI Search and use those permissions to control access to search results. If a user lacks permissions on a specific directory or file in ADLS Gen2, that user doesn't have access to the corresponding documents in Azure AI Search results.

You can use the push APIs to upload and index content and permission metadata manually, or you can use an indexer to automate data ingestion. This article focuses on the indexer approach.

The indexer approach is built on this foundation:

+ [The ADLS Gen2 access control model](/azure/storage/blobs/data-lake-storage-access-control-model) that provides [Access control lists (ACLs)](/azure/storage/blobs/data-lake-storage-access-control-model#access-control-lists-acls) and [Role-based access control (Azure RBAC)](/azure/storage/blobs/data-lake-storage-access-control-model#role-based-access-control-azure-rbac). There's no support for Attribute-based access control (Azure ABAC).

+ [An Azure AI Search indexer for ADLS Gen2](search-howto-index-azure-data-lake-storage.md) that retrieves and ingests data and metadata, including permission filters. To get permission filter support, you must use the 2025-05-01-preview REST API or a prerelease package of an Azure SDK that supports the feature.

+ [An index in Azure AI Search](search-how-to-create-search-index.md) containing the ingested documents and corresponding permissions. Permission metadata is stored as fields in the index. To set up queries that respect the permission filters, you must use the 2025-05-01-preview REST API or a prerelease package of an Azure SDK that supports the feature.

<!-- Addison has a concept article for doc-level permission concept. we should link to that instead. -->
This functionality helps align [document-level permissions](search-security-trimming-for-azure-search.md) in the search index with the access controls defined in ADLS Gen2, allowing users to retrieve content in a way that reflects their existing permissions.

This article supplements [**Index data from ADLS  Gen2**](search-howto-index-azure-data-lake-storage.md) with information that's specific to ingesting permissions alongside document content into an Azure AI Search index. 

## Prerequisites

+ Microsoft Entra ID authentication and authorization. Services and apps must be in the same tenant. Role assignments are used for each authenticated connection.

+ Azure AI Search, any region, but you must have a billable tier (basic and higher) for managed identity support. The search service must be [configured for role-based access](search-security-enable-roles.md) and it must [have a managed identity (either system or user)](search-howto-managed-identities-data-sources.md).

+ ADLS Gen2 blobs in a hierarchical namespace, with user permissions granted through ACLs or roles.

## Limitations

+ [Limits on Azure role assignments and ACL entries](/azure/storage/blobs/data-lake-storage-access-control-model#limits-on-azure-role-assignments-and-acl-entries) in ADLS Gen2 impose a maximum number of role assignments and ACL entries.

+ The `Other` ACL category isn't supported during public preview. Attribute-based access control (Azure ABAC) isn't supported.

+ Some indexer features are unavailable when enabling permission ingestion feature.

  + [Custom Web API skill](cognitive-search-custom-skill-web-api.md)
  + [GenAI Prompt skill](cognitive-search-skill-genai-prompt.md)
  + [Knowledge store](knowledge-store-concept-intro.md)
  + [Indexer enrichment cache](search-howto-incremental-index.md)
  + [Debug sessions](cognitive-search-debug-session.md)

## About ACL hierarchical permissions

Indexers can retrieve ACL assignments from the specified container and all directories leading to each file by following the ADLS Gen2 [hierarchical access evaluation flow](/azure/storage/blobs/data-lake-storage-access-control#common-scenarios-related-to-acl-permissions). The final effective access lists for each file are computed and the different access categories are indexed into the corresponding index fields.

For example, in [ADLS Gen2 common scenarios related to permissions](/azure/storage/blobs/data-lake-storage-access-control#common-scenarios-related-to-acl-permissions) as the file path /Oregon/Portland/Data.txt.

| Operation |	/ |	Oregon/ |	Portland/ |	Data.txt |
| - | - | - | - | - |
| Read Data.txt	| --X	| --X	| --X	| R-- |

The indexer fetches ACLs from each container and directory, resolves them into the retained effective access of lower levels, and continues this process until it determines the effective access for each file.

```txt
/ assigned access vs Oregon/ assigned access
  => Oregon/ effective access vs Portland/ assigned access
    => Portland/ effective access vs Data.txt assigned access
      => Data.txt effective access
```

## Configure ADLS Gen2 for indexing permission filters

An indexer can retrieve ACLs on a storage account if the following criteria are met. For more information about ACL assignments, see [ADLS Gen2 ACL assignments](/azure/storage/blobs/data-lake-storage-access-control#how-to-set-acls).

### Authorization

For indexer execution, your search service identity must have **Storage Blob Data Reader** permission. 

If you're testing locally, you should also have a **Storage Blob Data Reader** role assignment. For more information, see [Connect to Azure Storage using a managed identity](search-howto-managed-identities-storage.md).

### Root container permissions:

1. Assign all `Group` and `User` sets (security principals) at the root container `/` with `Read` and `Execute` permissions.

1. Ensure both `Read` and `Execute` are added as "Default permissions" so they propagate to newly created files and directories automatically.

### Propagate permissions down the file hierarchy

Although new directories and files inherit permissions, existing directories and files don't automatically inherit these assignments. 

Use the ADLS Gen2 tool to [apply ACLs recursively](/azure/storage/blobs/data-lake-storage-acl-azure-portal#apply-an-acl-recursively) for assignments propagation on existing content. This tool propagates the root container's ACL assignments to all underlying directories and files.

### Remove excess permissions

After applying ACLs recursively, review permissions for each directory and file. 

Remove any `Group` or `User` sets that shouldn't have access to specific directories or files. For example, remove `User2` on folder `Portland/`, and for folder `Idaho` remove `Group2` and `User2` from its assignments, and so on.

### Sample ACL assignments structure

Here's a diagram of the ACL assignment structure for the [fictitious directory hierarchy](/azure/storage/blobs/data-lake-storage-access-control#common-scenarios-related-to-acl-permissions) in the ADLS Gen2 documentation.

![Diagram of an ACL assignment structure.](media/search-security-acl/acl-assignment-structure-sample.png)

### Updating ACL assignments over time

Over time, as any new ACL assignments are added or modified, repeat the above steps to ensure proper propagation and permissions alignment. Updated permissions in ADLS Gen2 are updated in the search index when you re-ingest the content using the indexer.

## Configure Azure AI Search for indexing permission filters

Recall that the search service must have:

+ [Role-based access enabled](search-security-enable-roles.md)
+ [Managed identity configured](search-howto-managed-identities-data-sources.md)

### Authorization

For indexer execution, the client issuing the API call must have **Search Service Contributor** permission to create objects, **Search Index Data Contributor** permission to perform data import, and **Search Index Data Reader** to query an index. 

If you're testing locally, you should have the same role assignments. For more information, see [Connect to Azure AI Search using roles](search-security-rbac.md).

## Indexing permission metadata

In Azure AI Search, configure an indexer, data source, and index to pull permission metadata from ADLS Gen2 blobs.

### Configure the data source

This section supplements  [**Index data from ADLS  Gen2**](search-howto-index-azure-data-lake-storage.md) with information that's specific to ingesting permissions alongside document content into an Azure AI Search index.

+ Data Source type must be `adlsgen2`.

+ Data source must have `indexerPermissionOptions` with `userIds`, `groupIds` and/or `rbacScope`.

  + For`rbacScope`, configure the [connection string](search-howto-index-azure-data-lake-storage.md#supported-credentials-and-connection-strings) with managed identity format.
  
  + For connection strings using a [user-assigned managed identity](search-howto-managed-identities-storage.md#user-assigned-managed-identity), you must also specify the `identity` property.

<!-- Question/Comment: check this example -->
JSON example with system managed identity:

```json
{
    "name" : "my-adlsgen2-acl-datasource",
    "type": "adlsgen2",
    "indexerPermissionOptions": ["userIds", "groupIds", "rbacScope"],
    "credentials": {
    "connectionString": "ResourceId=/subscriptions/<your subscription ID>/resourceGroups/<your resource group name>/providers/Microsoft.Storage/storageAccounts/<your storage account name>/;"
    },
    "container": {
    "name": "<your container name>",
    "query": "<optional-virtual-directory-name>"
    }
}
```

JSON schema example with a user-managed identity in the connection string:

```json
{
    "name" : "my-adlsgen2-acl-datasource",
    "type": "adlsgen2",
    "indexerPermissionOptions": ["userIds", "groupIds", "rbacScope"],
    "credentials": {
    "connectionString": "ResourceId=/subscriptions/<your subscription ID>/resourceGroups/<your resource group name>/providers/Microsoft.Storage/storageAccounts/<your storage account name>/;"
    },
    "container": {
    "name": "<your container name>",
    "query": "<optional-virtual-directory-name>"
    },
    "identity": {
    "@odata.type": "#Microsoft.Azure.Search.DataUserAssignedIdentity",
    "userAssignedIdentity": "/subscriptions/{subscription-ID}/resourceGroups/{resource-group-name}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{user-assigned-managed-identity-name}"
    }
}
```

### Create permission fields in the index

In Azure AI Search, make sure your index contains field definitions for the permission metadata. Permission metadata can be indexed when `indexerPermissionOptions` is specified in the data source definition.

Recommended schema attributes for ACL (UserIds, GroupIds) and RBAC Scope:

+ User IDs field with `userIds` permissionFilter value.
+ Group IDs filed with `groupIds` permissionFilter value.
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
    { "name": "UserIds", "type": "Collection(Edm.String)", "permissionFilter": "userIds", "filterable": true, "retrievable": false },
    { "name": "GroupIds", "type": "Collection(Edm.String)", "permissionFilter": "groupIds", "filterable": true, "retrievable": false },
    { "name": "RbacScope", "type": "Edm.String", "permissionFilter": "rbacScope", "filterable": true, "retrievable": false }
  ],
  "permissionFilterOption": "enabled"
}
```

### Configure the indexer

Field mappings within an indexer set the data path to fields in an index. Target and destination fields that vary by name or data type require an explicit field mapping. The following metadata fields in ADLS Gen2 might need field mappings if you vary the field name:

+ **metadata_user_ids** (`Collection(Edm.String)`) - the ACL user IDs list.
+ **metadata_group_ids** (`Collection(Edm.String)`) - the ACL group IDs list.
+ **metadata_rbac_scope** (`Edm.String`) - the container RBAC scope.

Specify `fieldMappings` in the indexer to route the permission metadata to target fields during indexing.

JSON schema example:

```json
{
  ...
  "fieldMappings": [
    { "sourceFieldName": "metadata_user_ids", "targetFieldName": "UserIds" },
    { "sourceFieldName": "metadata_group_ids", "targetFieldName": "GroupIds" },
    { "sourceFieldName": "metadata_rbac_scope", "targetFieldName": "RbacScope" }
  ]
}
```

## Recommendations and best practices

+ Plan the ADLS Gen2 folder structure carefully before creating any folders.

+ Organize identities into groups and use groups whenever possible, rather than granting access directly to individual users. Continuously adding individual users instead of applying groups increases the number of access control entries that must be tracked and evaluated. Not following this best practice can lead to more frequent security metadata updates required to the index as this metadata changes, causing increased delays and inefficiencies in the refresh process.

## Re-ingest permission metadata as needed

If permission metadata like ACLs or RBAC scope needs to be re-ingested after regular indexer runs, consider the following options:

+ For a few blobs, consider renewing the `Last modified` timestamp of these blobs from source, so that **both permission metadata as well as the blob data content** will be re-ingested from the next indexer run.

+ For a moderate amount of blobs, consider issuing a request with the [`/resetdocs (preview)`](search-howto-run-reset-indexers.md#how-to-reset-docs-preview) API of these blobs, so that **both permission metadata as well as the blob data content** of these blobs can be re-ingested again.

  ```http
  POST https://[service name].search.windows.net/indexers/[indexer name]/resetdocs?api-version=2025-05-01-preview
  {
      "documentKeys" : [
          "1001",
          "4452"
      ]
  }
  ```

+ For all blobs from the source, consider issuing a request with the [`/resync`](search-howto-run-reset-indexers.md#how-to-resync-indexers-preview) API. Then from the next indexer run, **only the permission metadata** of all blobs will be re-synced again with the source.

  ```http
  POST https://[service name].search.windows.net/indexers/[indexer name]/resync?api-version=2025-05-01-preview
  {
      "options" : [
          "permissions"
      ]
  }
  ```
