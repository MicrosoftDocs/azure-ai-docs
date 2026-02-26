---  
title: 'Tutorial: Index ADLS Gen2 permission metadata'
titleSuffix: Azure AI Search  
description: Learn how to index Access Control Lists (ACLs) and Azure Role-Based Access Control (RBAC) scope from ADLS Gen2 and query with permission-filtered results in Azure AI Search.
ms.service: azure-ai-search  
ms.update-cycle: 180-days
ms.topic: tutorial  
ms.date: 08/27/2025
author: wlifuture
ms.author: haileytapia
---  

# Tutorial: Index permission metadata from ADLS Gen2 and query with permission-filtered results

This tutorial demonstrates how to index Azure Data Lake Storage (ADLS) Gen2 [Access Control Lists (ACLs)](/azure/storage/blobs/data-lake-storage-access-control-model#access-control-lists-acls) and [role-based access control (RBAC)](/azure/storage/blobs/data-lake-storage-access-control-model#role-based-access-control-azure-rbac) scope into a search index using an indexer.

It also shows you how to structure a query that respects user access permissions. A successful query outcome confirms the permission transfer that occurred during index.

<!-- Add a link to Addison doc-perm concept doc -->
For more information about indexing ACLs, see [Use an ADLS Gen2 indexer to ingest permission metadata](search-indexer-access-control-lists-and-role-based-access.md).

In this tutorial, you learn how to:

> [!div class="checklist"]
> + Configure RBAC scope and ACLs on an `adlsgen2` data source
> + Create an Azure AI Search index containing permission information fields
> + Create and run an indexer to ingest permission information into an index from a data source
> + Search the index you just created

Use a REST client to complete this tutorial and the [latest preview REST API](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true). Currently, there's no support for ACL indexing in the Azure portal.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ Microsoft Entra ID authentication and authorization. Services and apps must be in the same tenant. Role assignments are used for each authenticated connection. Users and groups must be in the same tenant. You should have user and groups to work with. Creating tenants and security principals is out-of-scope for this tutorial.

+ [ADLS Gen2](/azure/storage/blobs/create-data-lake-storage-account) with a hierarchical namespace.

+ Files in a hierarchical folder structure. This tutorial assumes the ADLS Gen2 demo of folder structure for file [`/Oregon/Portland/Data.txt`](/azure/storage/blobs/data-lake-storage-access-control#common-scenarios-related-to-acl-permissions). This tutorial guides you through ACL assignment on folders and files so that you can complete the exercise successfully.

+ [Azure AI Search](search-create-service-portal.md), any region. Basic tier or higher is required for managed identity support.

+ [Visual Studio Code](https://code.visualstudio.com/download) with the [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client).

## Prepare sample data

Upload the [state parks sample data](https://github.com/Azure-Samples/azure-search-sample-data) to a container in ADLS Gen2. The container name should be "parks" and it should have two folders: "Oregon" and "Washington".

## Check search service configuration

You search service must be configured for Microsoft Entra ID authentication and authorization. Review this checklist to make sure you're prepared.

+ [Enable role-based access](search-security-enable-roles.md)

+ [Configure a system-assigned managed identity](search-how-to-managed-identities.md).

## Get a personal identity token for local testing

This tutorial assumes a REST client on a local system, connecting to Azure over a public internet connection.

[Follow these steps](search-get-started-rbac.md) to acquire a personal identity token and set up Visual Studio Code for local connections to your Azure resources.

## Set permissions in ADLS Gen2

As a best practice, use [`Group` sets](search-indexer-access-control-lists-and-role-based-access.md#recommendations-and-best-practices) rather than directly assigning `User` sets.

1. Grant the search service identity read access to the container. The indexer connects to Azure Storage under the search service identity. The search service must have **Storage Blob Data Reader** permissions to retrieve data.

1. Grant per-group or user permissions in the file hierarchy. In the file hierarchy, identify all `Group` and `User` sets that are assigned to containers, directories, and files. 

1. You can use the Azure portal to manage ACLs. In Storage Browser, select the Oregon directory and then select **Manage ACL** from the context menu.

1. Add new security principals for users and groups.

1. Remove existing principals for owning groups, owning users, and other.  These principals aren't supported for ACL indexing during the public preview.

## Create a search index for permission metadata

[Create an index](search-how-to-create-search-index.md#create-an-index) that contains fields for content and [permission metadata](search-indexer-access-control-lists-and-role-based-access.md#create-permission-fields-in-the-index).

Be sure to use the [latest preview REST API](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) or a preview Azure SDK package that provides equivalent functionality. The permission filter properties are only available in the preview APIs.

For demo purposes, the permission field has `retrievable` enabled so that you can check the values from the index. In a production environment, you should disable `retrievable` to avoid leaking sensitive information.

```json
{
  "name" : "my-adlsgen2-acl-index",
  "fields": [
    {
      "name": "name", "type": "Edm.String",
      "searchable": true, "filterable": false, "retrievable": true
    },
    {
      "name": "description", "type": "Edm.String",
      "searchable": true, "filterable": false, "retrievable": true    
    },
    {
      "name": "location", "type": "Edm.String",
      "searchable": true, "filterable": false, "retrievable": true
    },
    {
      "name": "state", "type": "Edm.String",
      "searchable": true, "filterable": false, "retrievable": true
    },
    {
      "name": "AzureSearch_DocumentKey", "type": "Edm.String",
      "searchable": true, "filterable": false, "retrievable": true
      "stored": true,
      "key": true
    },
    { 
      "name": "UserIds", "type": "Collection(Edm.String)", 
      "permissionFilter": "userIds", 
      "searchable": true, "filterable": false, "retrievable": true
    },
    { 
      "name": "GroupIds", "type": "Collection(Edm.String)", 
      "permissionFilter": "groupIds", 
      "searchable": true, "filterable": false, "retrievable": true
    },
    { 
      "name": "RbacScope", "type": "Edm.String", 
      "permissionFilter": "rbacScope", 
      "searchable": true, "filterable": false, "retrievable": true
    }
  ],
  "permissionFilterOption": "enabled"
}
```

## Create a data source

Modify [data source configuration](search-indexer-access-control-lists-and-role-based-access.md#create-the-data-source) to specify indexer permission ingestion and the types of permission metadata that you want to index.

A data source needs `indexerPermissionOptions`.

In this tutorial, use a system-assigned managed identity for the authenticated connection.

```json
{
    "name" : "my-adlsgen2-acl-datasource",
    "type": "adlsgen2",
    "indexerPermissionOptions": ["userIds", "groupIds", "rbacScope"],
    "credentials": {
    "connectionString": "ResourceId=/subscriptions/<your subscription ID>/resourceGroups/<your resource group name>/providers/Microsoft.Storage/storageAccounts/<your storage account name>/;"
    },
    "container": {
    "name": "parks",
    "query": null
    }
}
```

## Create and run the indexer

Indexer configuration for permission ingestion is primarily about defining `fieldMappings` from [permission metadata](search-indexer-access-control-lists-and-role-based-access.md#).

```json
{
  "name" : "my-adlsgen2-acl-indexer",
  "dataSourceName" : "my-adlsgen2-acl-datasource",
  "targetIndexName" : "my-adlsgen2-acl-index",
  "parameters": {
    "batchSize": null,
    "maxFailedItems": 0,
    "maxFailedItemsPerBatch": 0,
    "configuration": {
      "dataToExtract": "contentAndMetadata",
      "parsingMode": "delimitedText",
      "firstLineContainsHeaders": true,
      "delimitedTextDelimiter": ",",
      "delimitedTextHeaders": ""
      },
  "fieldMappings": [
    { "sourceFieldName": "metadata_user_ids", "targetFieldName": "UserIds" },
    { "sourceFieldName": "metadata_group_ids", "targetFieldName": "GroupIds" },
    { "sourceFieldName": "metadata_rbac_scope", "targetFieldName": "RbacScope" }
    ]
  }
}
```

After indexer creation and immediate run, the file content along with permission metadata information are indexed into the index.

## Run a query to check results

Now that documents are loaded, you can issue queries against them by using [Documents - Search Post (REST)](/rest/api/searchservice/documents/search-post).

The URI is extended to include a query input, which is specified by using the `/docs/search` operator. The query token is passed in the request header. For more information, see [Query-time ACL and RBAC enforcement](search-query-access-control-rbac-enforcement.md).

```http
POST  {{endpoint}}/indexes/stateparks/docs/search?api-version=2025-11-01-preview
Authorization: Bearer {{search-token}}
x-ms-query-source-authorization: {{search-token}}
Content-Type: application/json

{
    "search": "*",
    "select": "name,description,location,GroupIds",
    "orderby": "name asc"
}
```

## Related content

+ [https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/acl](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/acl)
