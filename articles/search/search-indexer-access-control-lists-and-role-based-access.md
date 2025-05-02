---  
title: Indexing Access Control Lists and Azure Role-Based Access scopes using Indexers in Azure AI Search  
titleSuffix: Azure AI Search  
description: Learn how to configure Azure AI Search indexers for ingesting Access Control Lists (ACLs) and Azure Role-Based Access (RBAC) metadata.  
ms.service: azure-ai-search  
ms.topic: conceptual  
ms.date: 04/29/2025  
author: wlifuture
ms.author: wli
---  


# Indexing Access Control Lists and Azure Role-Based Access Control scope using Indexers

> [!IMPORTANT]
> Indexing Access Control Lists and Azure Role-Based Access scopes using Indexers in Azure AI Search functionality is first available in the **2025-05-01-preview** REST API. 
> This feature is in public preview. It's offered "as-is", under [Supplemental Terms of Use](https://azure.microsoft.com/support/legal/preview-supplemental-terms/) and supported on best effort only. Preview features aren't recommended for production workloads and aren't guaranteed to become generally available.


[Azure AI Search ADLS Gen2 indexers](search-howto-index-azure-data-lake-storage.md) enable the ingestion of access control metadata, such as Access Control Lists (ACLs) and Azure Role-Based Access Control (RBAC) scope, directly from Azure Data Lake Storage (ADLS) Gen2. This functionality helps align [document-level permissions](search-security-trimming-for-azure-search.md) in the search index with the access controls defined in ADLS Gen2, allowing users to retrieve content in a way that reflects their existing permissions.

 - [Azure RBAC scope](/azure/storage/blobs/data-lake-storage-access-control-model#role-based-access-control-azure-rbac) in Azure Data Lake Storage Gen2 assigns certain security principals with certain roles, as a coarse-grain access control model.
 - [Access control lists (ACLs)](/azure/storage/blobs/data-lake-storage-access-control-model#access-control-lists-acls) from Azure Data Lake Storage Gen2 is a POSIX-liked fine-grain access control model.

This document supplements [**Index data from Azure Data Lake Storage Gen2**](search-howto-index-azure-data-lake-storage.md) with information that's specific to ingest permission access control metadata alongside document content into the Azure AI Search index. 

## ACL Hierarchical Permissions  
Indexers retrieve ACL assignments from the specified container and all directories leading to each file by following the ADLS Gen2 [hierarchical access evaluation flow](/azure/storage/blobs/data-lake-storage-access-control#common-scenarios-related-to-acl-permissions). The final effective access lists for each file are computed and the different access categories are indexed into the corresponding index fields.

For example, in [ADLS Gen2 common scenarios related to permissions](/azure/storage/blobs/data-lake-storage-access-control#common-scenarios-related-to-acl-permissions) as the file path /Oregon/Portland/Data.txt.

  | Operation |	/ |	Oregon/ |	Portland/ |	Data.txt |
  | - | - | - | - | - |
  | Read Data.txt	| --X	| --X	| --X	| R-- |
  
  The indexer fetches ACLs from each container and directory, resolves them into the retained effective access of lower levels, and continues this process until it determines the effective access for the file.
  
  ```txt
  / assigned access vs Oregon/ assigned access
    => Oregon/ effective access vs Portland/ assigned access
      => Portland/ effective access vs Data.txt assigned access
        => Data.txt effective access
  ```

## Restrictions
Some indexer features will be unavailable when enabling permission ingestion feature.
  - Custom Web API skill
  - Chat Completion skill
  - Knowledge Store
  - Indexer Cache

## Requirements
- Azure Data Lake Storage Gen2 ([adlsgen2](search-howto-index-azure-data-lake-storage.md#define-the-data-source)) as the data source type.
- Datasource property [indexerIngestionOptions]() with various permission ingestion options from the indexer.
- ACLs indexer ingestion supports different [credentials and connection strings](search-howto-index-azure-data-lake-storage.md#supported-credentials-and-connection-strings): full access storage account connection string, or managed identity connection string.
- RBAC scope ingestion requires [managed identity](search-howto-managed-identities-data-sources.md) credentials and [connection strings](search-howto-index-azure-data-lake-storage.md#supported-credentials-and-connection-strings) format of managed identity only.
- Indexer execution credential should have at least [Storage Blob Data Reader](/azure/storage/blobs/data-lake-storage-access-control-model#role-based-access-control-azure-rbac) role from the ADLS Gen2 data source.

## Limitations
- Refer to the [ACLs and RBAC limits in ADLS Gen2](/azure/storage/blobs/data-lake-storage-access-control-model#limits-on-azure-role-assignments-and-acl-entries) for the maximum number of role assignments and ACL entries supported.
- The `Other` ACL category is not supported during Public Preview.
- Guidelines for [ADLS Gen2 ACL assignments](/azure/storage/blobs/data-lake-storage-access-control#how-to-set-acls) during Public Preview:
  ### Root Container Permissions:
  1. Assign all groups and users (security principals) that require access to any file within the container both `read` and `execute` permissions at the root container level.
  1. Ensure both `read` and `execute` permissions are also added as "Default permissions" for the container, so they propagate to newly created files and directories automatically.
  ### Existing Hierarchical File Structures:
  For containers with existing hierarchical file structures, use the ADLS Gen2 tool to [apply ACLs recursively](/azure/storage/blobs/data-lake-storage-acl-azure-portal#apply-an-acl-recursively). This will propagate the root container's ACL assignments to all underlying directories and files.
  ### Remove Excess Permissions:
  After applying ACLs recursively, review permissions for each directory and file.
  Remove any permissions for security principals that should not have access to specific directories or files.
  ### Updating ACL Assignments:
  If any new ACL assignments are added, repeat the above steps to ensure proper propagation and permissions alignment.
  ### Sample ACL assignments structure
  ![alt text](acl-assignment-structure-sample.png)

## Supported Scenarios  
- Extraction of ACL and Azure RBAC container metadata from Azure Data Lake Storage Gen2.
- Tailored for RAG (Retrieval Augmented Generation) applications and enterprise search.

## Indexing Permission Metadata
Permission metadata can be indexed when `indexerPermissionOptions` are chosen from Data Source definition, as opt-in for permission ingestion from Indexer.
  - **metadata_user_ids** (`Collection(Edm.String)`) - the ACL user ids list.
  - **metadata_group_ids** (`Collection(Edm.String)`) - the ACL group ids list.
  - **metadata_rbac_scope** (`Edm.String`) - the container RBAC scope.

## Indexing with Indexers
### 1. Search Service configuration
- For RBAC scope ingestion, [managed identity](search-howto-managed-identities-data-sources.md) is required, either system managed identity or user-assigned managed identity.

### 2. Data Source configuration
- Configure data source with `adlsgen2` type.
- Configure data source on selective `indexerIngestionOption` with `userIds`, `groupIds` and/or `rbacScope`.
- If `rbacScope` option is part of the selection, configure [connection string](search-howto-index-azure-data-lake-storage.md#supported-credentials-and-connection-strings) with managed identity format.
- If [user-assigned managed identity](search-howto-managed-identities-storage.md#user-assigned-managed-identity) is used, configure the `identity` property, otherwise the `identity` property don't need to be specified.
- JSON schema example:
  ```json
  {
    ...
    "type": "adlsgen2",
    "indexerPermissionOptions": ["userIds", "groupIds", "rbacScope"],
    "credentials": {
      "connectionString": "ResourceId=/subscriptions/<your subscription ID>/resourceGroups/<your resource group name>/providers/Microsoft.Storage/storageAccounts/<your storage account name>/;"
    },
    "identity": {
      "@odata.type": "#Microsoft.Azure.Search.DataUserAssignedIdentity",
      "userAssignedIdentity": "/subscriptions/{subscription-ID}/resourceGroups/{resource-group-name}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{user-assigned-managed-identity-name}"
    }
  }
  ```

### 3. Index Permission fields
- Recommended schema attributes for ACL (UserIds, GroupIds) and RBAC Scope.
  - User IDs field with `userIds` permissionFilter value, and set filterable to true.
  - Group IDs filed with `groupIds` permissionFilter value, and set filterable to true.
  - RBAC scope field with `rbacScope` permissionFilter value, and set filterable to true.
  - Property `permissionFilterOption` to enable filtering at querying time.
- JSON schema example:
  ```json
  {
    ...
    "fields": [
      ...
      { "name": "UserIds", "type": "Collection(Edm.String)", "permissionFilter": "userIds", "filterable": true },
      { "name": "GroupIds", "type": "Collection(Edm.String)", "permissionFilter": "groupIds", "filterable": true },
      { "name": "RbacScope", "type": "Edm.String", "permissionFilter": "rbacScope", "filterable": true }
    ],
    "permissionFilterOption": "enabled"
  }
  ```

### 4. Indexer configuration
- Specify `fieldMappings` in the indexer to output the permission fields for indexing.
- JSON schema example:
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
- Plan the ADLS Gen2 folder structure carefully before creating any folders.
- Organize identities into groups and use groups whenever possible, rather than granting access directly to individual users. Continuously adding individual users instead of applying groups increases the number of access control entries that must be tracked and evaluated. Not following this best practice can lead to more frequent security metadata updates required to the index as this metadata changes, causing increased delays and inefficiencies in the refresh process.

## Re-ingest Permission Metadata as needed
If permission metadta like ACLs and/or RBAC scope need to be re-ingested after normal indexer runs. There are a few options for certain scenarios:
- For a few blobs, consider renewing the `Last modified` timestamp of these blobs from source, so that **both permission metadata as well as the blob data content** will be re-ingested from the next indexer run.
- For a moderate amount of blobs, consider issuing a request with the [`/resetdocs (preview)`](search-howto-run-reset-indexers.md#how-to-reset-docs-preview) API of these blobs, so that **both permission metadata as well as the blob data content** of these blobs will be re-ingested again.

    ```http
    POST https://[service name].search.windows.net/indexers/[indexer name]/resetdocs?api-version=2025-05-01-preview
    {
        "documentKeys" : [
            "1001",
            "4452"
        ]
    }
    ```

- For all blobs from the source, consider issuing a request with the [`/resync`](search-howto-run-reset-indexers.md#how-to-resync-indexers-preview) API. Then from the next indexer run, **only the permission metadata** of all blobs will be re-synced again with the source.

    ```http
    POST https://[service name].search.windows.net/indexers/[indexer name]/resync?api-version=2025-05-01-preview
    {
        "options" : [
            "permissions"
        ]
    }
    ```
