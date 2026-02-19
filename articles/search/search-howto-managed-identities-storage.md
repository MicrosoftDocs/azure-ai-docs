---
title: Connect to Azure Storage
titleSuffix: Azure AI Search
description: Learn how to set up an indexer connection to an Azure Storage account using a managed identity.
author: gmndrg
ms.author: gimondra
manager: vinodva
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 08/27/2025
ms.update-cycle: 365-days
ms.custom:
  - subject-rbac-steps
  - ignite-2023
  - sfi-ropc-nochange
---

# Connect to Azure Storage using a managed identity (Azure AI Search)

This article explains how to configure a search service connection to an Azure Storage account using a managed identity instead of providing credentials in the connection string.

You can use a system-assigned managed identity or a user-assigned managed identity. Managed identities are Microsoft Entra logins and require role assignments for access to Azure Storage. 

## Prerequisites

+ Azure AI Search, Basic tier or higher, with a [managed identity](search-how-to-managed-identities.md).

> [!NOTE]
> If storage is network-protected and in the same region as your search service, you must use a system-assigned managed identity and either one of the following network options: [connect as a trusted service](search-indexer-howto-access-trusted-service-exception.md), or [connect using the resource instance rule](/azure/storage/common/storage-network-security#grant-access-from-azure-resource-instances). 

## Create a role assignment in Azure Storage

1. Sign in to Azure portal and find your storage account.

1. Select **Access control (IAM)**.

1. Select **Add** and then select **Role assignment**.

1. From the list of job function roles, select the roles needed for your search service:

   | Task | Role assignment |
   |------|-----------------|
   | Blob indexing using an indexer | Add **Storage Blob Data Reader** |
   | ADLS Gen2 indexing using an indexer | Add **Storage Blob Data Reader** |
   | Table indexing using an indexer | Add **Storage Table Data Reader** |
   | File indexing using an indexer | Add **Reader and Data Access** |
   | Write to a [knowledge store](knowledge-store-concept-intro.md) | Add **Storage Blob Data Contributor** for object and file projections, and **Reader and Data Access** for table projections. |
   | Write to an [enrichment cache](enrichment-cache-how-to-configure.md) | Add **Storage Blob Data Contributor** and **Storage Table Data Contributor** |
   | Save [debug session state](cognitive-search-debug-session.md) | Add **Storage Blob Data Contributor**  |

1. Select **Next**.

1. Select **Managed identity** and then select **Members**.

1. Filter by system-assigned managed identities or user-assigned managed identities. You should see the managed identity that you previously created for your search service. If you don't have one, see [Configure search to use a managed identity](search-how-to-managed-identities.md). If you already set one up but it's not available, give it a few minutes.

1. Select the identity and save the role assignment.

## Specify a managed identity in a connection string

Once you have a role assignment, you can set up a connection to Azure Storage that operates under that role.

[Indexers](search-indexer-overview.md) use a data source object for connections to an external data source. This section explains how to specify a system-assigned managed identity or a user-assigned managed identity on a data source connection string. You can find more [connection string examples](search-how-to-managed-identities.md#connection-string-examples) in the managed identity article.

> [!TIP]
> You can create a data source connection to Azure Storage in the Azure portal, specifying either a system or user-assigned managed identity, and then view the JSON definition to see how the connection string is formulated.

### System-assigned managed identity

You must have a [system-assigned managed identity already configured](search-how-to-managed-identities.md), and it must have a role-assignment on Azure Storage. 

For connections made using a system-assigned managed identity, the only change to the [data source definition](/rest/api/searchservice/data-sources/create) is the format of the `credentials` property. 

Provide a connection string that contains a `ResourceId`, with no account key or password. The `ResourceId` must include the subscription ID of the storage account, the resource group of the storage account, and the storage account name.

```http
POST https://[service name].search.windows.net/datasources?api-version=2025-09-01

{
    "name" : "blob-datasource",
    "type" : "azureblob",
    "credentials" : { 
        "connectionString" : "ResourceId=/subscriptions/00000000-0000-0000-0000-00000000/resourceGroups/MY-DEMO-RESOURCE-GROUP/providers/Microsoft.Storage/storageAccounts/MY-DEMO-STORAGE-ACCOUNT/;" 
    },
    "container" : { 
        "name" : "my-container", "query" : "<optional-virtual-directory-name>" 
    }
}   
```

### User-assigned managed identity (preview)

You must have a [user-assigned managed identity already configured](search-how-to-managed-identities.md) and associated with your search service, and the identity must have a role-assignment on Azure Storage. 

Connections made through user-assigned managed identities use the same credentials as a system-assigned managed identity, plus an extra identity property that contains the collection of user-assigned managed identities. Only one user-assigned managed identity should be provided when creating the data source. 

Provide a connection string that contains a `ResourceId`, with no account key or password. The `ResourceId` must include the subscription ID of the storage account, the resource group of the storage account, and the storage account name.

Provide an `identity` using the syntax shown in the following example. Set `userAssignedIdentity` to the user-assigned managed identity.

```http
POST https://[service name].search.windows.net/datasources?api-version=2025-11-01-preview

{
    "name" : "blob-datasource",
    "type" : "azureblob",
    "credentials" : { 
        "connectionString" : "ResourceId=/subscriptions/00000000-0000-0000-0000-00000000/resourceGroups/MY-DEMO-RESOURCE-GROUP/providers/Microsoft.Storage/storageAccounts/MY-DEMO-STORAGE-ACCOUNT/;" 
    },
    "container" : { 
        "name" : "my-container", "query" : "<optional-virtual-directory-name>" 
    },
    "identity" : { 
        "@odata.type": "#Microsoft.Azure.Search.DataUserAssignedIdentity",
        "userAssignedIdentity" : "/subscriptions/00000000-0000-0000-0000-00000000/resourcegroups/MY-DEMO-RESOURCE-GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/MY-DEMO-USER-MANAGED-IDENTITY" 
    }
}   
```

Connection information and permissions on the remote service are validated at run time during indexer execution. If the indexer is successful, the connection syntax and role assignments are valid. For more information, see [Run or reset indexers, skills, or documents](search-howto-run-reset-indexers.md).

## Accessing network secured data in storage accounts

Azure storage accounts can be further secured using firewalls and virtual networks. If you want to index content from a storage account that is secured using a firewall or virtual network, see [Make indexer connections to Azure Storage as a trusted service](search-indexer-howto-access-trusted-service-exception.md).

## See also

+ [Azure blob indexer](search-how-to-index-azure-blob-storage.md)
+ [ADLS Gen2 indexer](search-how-to-index-azure-data-lake-storage.md)
+ [Azure table indexer](search-how-to-index-azure-tables.md)
+ [C# Example: Index Data Lake Gen2 using Microsoft Entra ID (GitHub)](https://github.com/Azure-Samples/azure-search-dotnet-utilities/blob/main/data-lake-gen2-acl-indexing/README.md)
