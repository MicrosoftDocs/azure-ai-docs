---  
title: Indexing Access Control Lists and Azure Role-Based Access scopes using Indexers in Azure AI Search  
titleSuffix: Azure AI Search  
description: Learn how to configure Azure AI Search indexers for ingesting Access Control Lists (ACL) and Azure Role-Based Access (RBAC) metadata.  
ms.service: azure-ai-search  
ms.topic: conceptual  
ms.date: 04/29/2025  
author: wlifuture
ms.author: wli
---  

> [!IMPORTANT]
> **Preview** – Indexing Access Control Lists and Azure Role-Based Access scopes using Indexers in Azure AI Search functionality is first available in the **2025-05-01-preview** REST API. 
> This feature is in public preview. It's offered "as-is", under [Supplemental Terms of Use](https://azure.microsoft.com/support/legal/preview-supplemental-terms/) and supported on best effort only. Preview features aren't recommended for production workloads and aren't guaranteed to become generally available.

# Indexing Access Control Lists and Azure Role-Based Access scopes using Indexers in Azure AI Search

[Azure AI Search ADLS Gen2 indexers](search-howto-index-azure-data-lake-storage.md) can ingest access control metadata like Access Control Lists (ACL) and Azure Role-Based Access (RBAC) scopes directly from Azure Data Lake Gen2 (ADLS Gen2), enabling secure and compliant document retrieval.

 - [Azure RBAC scope](/azure/storage/blobs/data-lake-storage-access-control-model#role-based-access-control-azure-rbac) in Azure Data Lake Storage Gen2 assigns certain security principals with certain roles, as a coarse-grain access control method.
 - [Access control list (ACL)](/azure/storage/blobs/data-lake-storage-access-control-model#access-control-lists-acls) from Azure Data Lake Storage Gen2 is a POSIX-liked fine-grain access control model.
 
This document provides guidance on using the ADLS Gen2 built-in indexer to ingest permission access control metadata alongside document content into the Azure AI Search index. This helps with secure, compliant, and efficient document retrieval through the Azure AI Search service.

## Requirements
- Azure Data Lake Storage Gen2 ([adlsgen2](search-howto-index-azure-data-lake-storage.md#define-the-data-source)) as the data source type.
- Newly introduced data source property [indexerIngestionOptions]() with a variety of permission ingestion options from the indexer.
- ACL indexer ingestion supports different [credentials and connection strings](search-howto-index-azure-data-lake-storage.md#supported-credentials-and-connection-strings): full access storage account connection string, or managed identity connection string.
- RBAC scope ingestion requires [managed identity](search-howto-managed-identities-data-sources.md) credentials and [connection strings](search-howto-index-azure-data-lake-storage.md#supported-credentials-and-connection-strings) format of managed identity only.
- Indexer execution credential should have at least [Storage Blob Data Reader](data-lake-storage-access-control-model.md#role-based-access-control-azure-rbac) role from the ADLS Gen2 data source.

## Limitations
- [ACL and RBAC limits in ADLS Gen2](/storage/blobs/data-lake-storage-access-control-model#limits-on-azure-role-assignments-and-acl-entries).
- [ADLS Gen2 ACL assignments](/azure/storage/blobs/data-lake-storage-access-control#how-to-set-acls) are restricted with following guidelines for indexer at during Public Preview:
  - At the root container, assign all groups and users that will have access to any file, with both `read` and `execute` permissions.

    Also, assign all these security principals as part of container "Default permissions", with both `read` and `execute` permissions as well.
  - For existing containers that already have hierarchical file structure, use the ADLS Gen2 tool [apply ACL recursively](/azure/storage/blobs/data-lake-storage-acl-azure-portal#apply-an-acl-recursively) to propagate these ACL assignments to all underlying directories and files.
  - Then go to each underlying directory and file to remove the assignments that should not access contents of the directory or file.
  - If any new ACL assignment is added, repeat above steps.
- `other` ACL category is not supported during Public Preview.

## Supported Scenarios  
- Extraction of ACL and RBAC metadata from Azure Data Lake Storage Gen2.
- Tailored for RAG (Retrieval Augmented Generation) applications and enterprise search.
  
## Indexing with Indexers
### 1. Search Service configuration
- For RBAC scope ingestion, [managed identity](search-howto-managed-identities-data-sources.md) is required, either system managed identiy or user-assigned managed identity.

### 2. Data source configuration
- Configure data source with `adlsgen2` type.
- Configure data source on selective indexerIngestionOption with `userIds`, `groupIds` and/or `rbacScope`.
- If `bacScope` option is part of the selection, configure [connection string](search-howto-index-azure-data-lake-storage.md#supported-credentials-and-connection-strings) with managed identity format.
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

### 3. Index Schema Design
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

## ACL Hierarchical Permissions  
Indexers retrieve ACL assignments from the specified container and all directories leading to each file by following the ADLS Gen2 [hierarchical access evaluation flow](/storage/blobs/data-lake-storage-access-control#common-scenarios-related-to-acl-permissions). They compute the final effective access lists for each file and index the different access categories into the corresponding index fields.

For example, in [ADLS Gen2 common scenarios related to permissions](/data-lake-storage-access-control#common-scenarios-related-to-acl-permissions) as the file path /Oregon/Portland/Data.txt.

  | Operation |	/ |	Oregon/ |	Portland/ |	Data.txt |
  | - | - | - | - | - |
  | Read Data.txt	| --X	| --X	| --X	| R-- |
  
  ACLs from each container/directory are fetched by indexer and solved as retained effective access of lower level, until solved out effective access for the file.
  ```txt
  / assigned access vs Oregon/ assigned access
    => Oregon/ effective access vs Portland/ assigned access
      => Portland/ effective access vs Data.txt assigned access
        => Data.txt effective access
  ```

## Recommendations and best practices
- Plan the ADLS Gen2 folder structure carefully before creating any folders.
- Organize identities into groups and use groups whenever possible, rather than granting access directly to individual users. Continuously adding individual users instead of leveraging groups increases the number of access control entries that must be tracked and evaluated. This can lead to more frequent updates to the index as security data changes, causing increased delays and inefficiencies in the refresh process.

