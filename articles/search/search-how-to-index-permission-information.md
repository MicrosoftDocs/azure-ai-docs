---  
title: 'Tutorial: Index permission metadata from ADLS Gen2 and query with permission-filtered results'
titleSuffix: Azure AI Search  
description: Learn how to index Access Control Lists (ACLs) and Azure Role-Based Access Control (RBAC) scope from ADLS Gen2 and query with permission-filtered results in Azure AI Search.
ms.service: azure-ai-search  
ms.topic: tutorial  
ms.date: 04/30/2025
author: wlifuture
ms.author: wli
---  

# Tutorial: Index permission metadata from ADLS Gen2 with indexer and query with permission-filtered results

This tutorial demonstrates how to index Azure Data Lake Storage (ADLS) Gen2 [Access Control Lists (ACLs)](/azure/storage/blobs/data-lake-storage-access-control-model#access-control-lists-acls) and [role-based access control (RBAC)](/azure/storage/blobs/data-lake-storage-access-control-model#role-based-access-control-azure-rbac) scope into a search index using indexer, and how to confirm the permission transfer during querying. For more information about indexing ACLs, see [Indexing Access Control Lists and Azure Role-Based Access Control scope using Indexers](search-indexer-access-control-lists-and-role-based-access.md).

> [!div class="checklist"]
> + Configure RBAC scope and ACLs on `adlsgen2` data source
> + Create an Azure AI Search index containing permission information fields
> + Create and run an indexer to ingest permission information into an index from a data source
> + Search the index you just created

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

+ [Azure Data Lake Storage Gen2](/azure/storage/blobs/create-data-lake-storage-account).

+ [Azure AI Search](search-what-is-azure-search.md). [Create a service](search-create-service-portal.md) or [find an existing service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices) in your current subscription.

+ [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client).

> [!NOTE]
> You can use a free search service for this tutorial. The Free tier limits you to three indexes, three indexers, and three data sources. This tutorial creates one of each. Before you start, make sure you have room on your service to accept the new resources.

## Configure RBAC and ACLs in ADLS Gen2 storage account
Follow the guidance from [ADLS Gen2 on RBAC configuration](/azure/storage/blobs/data-lake-storage-access-control-model#role-based-access-control-azure-rbac) and [setting up ACLs](/azure/storage/blobs/data-lake-storage-access-control#how-to-set-acls). Be sure to review the [Azure AI Search limitations](search-indexer-access-control-lists-and-role-based-access.md#limitations) for ACL indexing before you continue.

We recommend the following best practices:
  - Plan with hierarchical folder structure. This demo reuses ADLS Gen2 demo of folder structure for file [`/Oregon/Portland/Data.txt`](/azure/storage/blobs/data-lake-storage-access-control#common-scenarios-related-to-acl-permissions)
  - Plan and collect all `Group` and `User` sets that are assigned for the container, directories, and files.
  
    [Follow the recommendations](search-indexer-access-control-lists-and-role-based-access.md#recommendations-and-best-practices) for using `Group` sets as much as possible, rather than directly assigning `User` sets. The recommendations help you avoid [ADLS Gen2 limitation](/azure/storage/blobs/data-lake-storage-access-control#what-are-the-limits-for-azure-role-assignments-and-acl-entries), and also give you well-organized member structures for the whole organization.
    - Assign all `Group` and `User` sets onto the container `/` with `Read` and `Execute` permissions, for example, Group1, Group2, User1, User2.

      Also assign these `Group` and `User` sets into the "Default permissions" of the container `/` with `Read` and `Execute` permissions. This step makes sure underlying new directories and files automatically inherit these ACL assignments.

    - For any existing directories and files, they don't automatically inherit these assignments. Use the ADLS Gen2 tool to [apply ACLs recursively](/azure/storage/blobs/data-lake-storage-acl-azure-portal#apply-an-acl-recursively) for assignments propagation.
    - Finally remove any `Group` or `User` that shouldn't have access to specific directories or files, for example, remove `User2` on folder `Portland/`, and for folder `Idaho` remove `Group2` and `User2` from its assignments, and so on.
    - Repeat the previous steps if any new assignments are brought into play.
  - The `Other` ACL category isn't supported in Azure AI Search for now.
  - Sample ACL assignments structure

    ![Diagram of an ACL assignment structure.](acl-assignment-structure-sample.png)

## Create an Azure AI Search index containing permission information fields
[Create an index](search-how-to-create-search-index.md#create-an-index) that meets your service requirements, and add [permission fields](search-indexer-access-control-lists-and-role-based-access.md#3-index-permission-fields) to receive the respective ACLs and rbacScope metadata during indexing.
> [!NOTE]
> For demo purposes, the permission field has `retrievable` enabled so that you can check the values from the index. In production setup, you should disable `retrievable` to avoid leaking sensitive permission information.

```json
{
  "name" : "my-adlsgen2-acl-index",
  "fields": [
    ...
    { "name": "UserIds", "type": "Collection(Edm.String)", "permissionFilter": "userIds", "filterable": true, "retrievable": true },
    { "name": "GroupIds", "type": "Collection(Edm.String)", "permissionFilter": "groupIds", "filterable": true, "retrievable": true },
    { "name": "RbacScope", "type": "Edm.String", "permissionFilter": "rbacScope", "filterable": true, "retrievable": true }
  ],
  "permissionFilterOption": "enabled"
}
```

## Create and run an indexer to ingest permission information into an index from a data source
### Search service configuration
With RBAC scope ingestion, [managed identity](search-howto-managed-identities-data-sources.md) is required, either system managed identity or user-assigned managed identity.
- [system managed identity](search-howto-managed-identities-data-sources.md#create-a-system-managed-identity)
![Turn on system assigned identity](turn-on-system-assigned-identity.png)
- [user-assigned managed identity](search-howto-managed-identities-data-sources.md#create-a-user-assigned-managed-identity)
    ```http
    PUT https://management.azure.com/subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Search/searchServices/mysearchservice?api-version=2025-05-01-preview
    {
        "location": "[region]",
        "sku": {
            "name": "[sku]"
        },
        "properties": {
            "replicaCount": [replica count],
            "partitionCount": [partition count],
            "hostingMode": "default"
        },
        "identity": {
            "type": "UserAssigned",
            "userAssignedIdentities": {
            "/subscriptions/[subscription ID]/resourcegroups/[resource group name]/providers/Microsoft.ManagedIdentity/userAssignedIdentities/[name of managed identity]": {}
            }
        }
    } 
    ```

### Data Source creation
Modify [data source configuration](search-indexer-access-control-lists-and-role-based-access.md#2-data-source-configuration) to specify indexer permission ingestion and the types of permission metadata that you want to index.
  - `adlsgen2` type is required.
  - `indexerPermissionOptions` with candidate options to opt in: `userIds`, `groupIds`, and `rbacScope`.
  - If `rbacScope` option is part of the selection, configure a [connection string](search-howto-index-azure-data-lake-storage.md#supported-credentials-and-connection-strings) with managed identity format.
  - If [user-assigned managed identity](search-howto-managed-identities-storage.md#user-assigned-managed-identity) is used, configure the `identity` property, otherwise the `identity` property doesn't need to be specified.
  
Here are some scenario examples:
  - System managed identity schema example:
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

  - User-assigned managed identity schema example:
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

### Indexer creation
Indexer configuration for permission ingestion is primarily about defining `fieldMappings` from [permission metadata](search-indexer-access-control-lists-and-role-based-access.md#indexing-permission-metadata).
  ```json
  {
    "name" : "my-adlsgen2-acl-indexer",
    "dataSourceName" : "my-adlsgen2-acl-datasource",
    "targetIndexName" : "my-adlsgen2-acl-index",
    "parameters": {
      ...
    }
    "fieldMappings": [
      { "sourceFieldName": "metadata_user_ids", "targetFieldName": "UserIds" },
      { "sourceFieldName": "metadata_group_ids", "targetFieldName": "GroupIds" },
      { "sourceFieldName": "metadata_rbac_scope", "targetFieldName": "RbacScope" }
    ]
  }
  ```
After indexer creation and immediate run, the file content along with permission metadata information are indexed into the index.

### Re-ingest permission metadata as needed
There are different scenarios to [re-ingest permission metadata](search-indexer-access-control-lists-and-role-based-access.md#re-ingest-permission-metadata-as-needed).
- For a few blobs, consider renewing the `Last modified` timestamp of these blobs from source, so that **both permission metadata as well as the blob data content** will be re-ingested from the next indexer run.
- For a moderate amount of blobs, consider issuing a request with the [`/resetdocs (preview)`](search-howto-run-reset-indexers.md#how-to-reset-docs-preview) API of these blobs, so that **both permission metadata as well as the blob data content** of these blobs can be re-ingested again.
    ```http
    POST https://[service name].search.windows.net/indexers/[indexer name]/resetdocs?api-version=2025-05-01-preview
    {
        "documentKeys" : [
            "1001",
            "4452"
        ]
    }
    ```
- For all blobs from the source, consider issuing a request with the [`/resync`]() API. Then from the next indexer run, **only the permission metadata** of all blobs will be re-synced again with the source.
    ```http
    POST https://[service name].search.windows.net/indexers/[indexer name]/resync?api-version=2025-05-01-preview
    {
        "options" : [
            "permissions"
        ]
    }
    ```
