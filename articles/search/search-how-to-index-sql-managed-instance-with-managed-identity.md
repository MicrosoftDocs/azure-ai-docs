---
title: Connect to Azure SQL Managed Instance Using a Managed Identity
titleSuffix: Azure AI Search
description: Learn how to set up an Azure AI Search indexer connection to an Azure SQL Managed Instance using a managed identity.
author: gmndrg
ms.author: gimondra
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 01/21/2026
ms.update-cycle: 180-days
ms.custom:
  - ignite-2023
  - sfi-image-nochange
  - sfi-ga-nochange
  - sfi-ropc-nochange
---

# Set up an indexer connection to Azure SQL Managed Instance using a managed identity

This article describes how to set up an Azure AI Search indexer connection to [SQL Managed Instance](/azure/azure-sql/managed-instance/sql-managed-instance-paas-overview) using a managed identity instead of providing credentials in the connection string.

You can use a system-assigned managed identity or a user-assigned managed identity (preview). Managed identities are Microsoft Entra logins and require Azure role assignments to access data in SQL Managed Instance.

Before you learn more about this feature, you should understand what an indexer is and how to set up an indexer for your data source. For more information, see [Indexers in Azure AI Search](search-indexer-overview.md) and [Index data from Azure SQL Database](search-how-to-index-sql-database.md).

## Prerequisites

* [Create a managed identity](search-how-to-managed-identities.md) for your search service.

* Microsoft Entra admin role on SQL Managed Instance:

  To assign read permissions on SQL Managed Instance, you must be an Azure Global Admin with a SQL Managed Instance. See [Configure and manage Microsoft Entra authentication with SQL Managed Instance](/azure/azure-sql/database/authentication-aad-configure) and follow the steps to provision a Microsoft Entra admin (SQL Managed Instance).

* [Configure a public endpoint and network security group in SQL Managed Instance](search-how-to-index-sql-managed-instance.md) to allow connections from Azure AI Search. Connecting through a shared private link when using a managed identity isn't currently supported.

## Assign permissions to read the database

Follow these steps to assign the search service system managed identity permission to read the SQL Managed database.

1. Connect to your SQL Managed Instance through SQL Server Management Studio (SSMS) by using one of the following methods:

    - [Configure a point-to-site connection from on-premises](/azure/azure-sql/managed-instance/point-to-site-p2s-configure)
    - [Configure an Azure virtual machine](/azure/azure-sql/managed-instance/connect-vm-instance-configure)

1. Authenticate by using your Microsoft Entra account.

   :::image type="content" source="./media/search-index-azure-sql-managed-instance-with-managed-identity/sql-login.png" alt-text="Showing screenshot of the Connect to Server dialog.":::

1. From the left pane, locate the SQL database you're using as data source for indexing and right-click it. Select **New Query**.

   :::image type="content" source="./media/search-index-azure-sql-managed-instance-with-managed-identity/new-sql-query.png" alt-text="Showing screenshot of new SQL query.":::

1. In the T-SQL window, copy the following commands and include the brackets around your search service name. Select **Execute**.

    ```sql
    CREATE USER [insert your search service name here or user-assigned managed identity name] FROM EXTERNAL PROVIDER;
    EXEC sp_addrolemember 'db_datareader', [insert your search service name here or user-assigned managed identity name];
    ```

    :::image type="content" source="./media/search-index-azure-sql-managed-instance-with-managed-identity/execute-sql-query.png" alt-text="Showing screenshot of how to execute SQL query.":::

If you later change the search service system identity after assigning permissions, you must remove the role membership and remove the user in the SQL database, then repeat the permission assignment. To remove the role membership and user, run the following commands:

```sql
sp_droprolemember 'db_datareader', [insert your search service name or user-assigned managed identity name];

DROP USER IF EXISTS [insert your search service name or user-assigned managed identity name];
```

## Add a role assignment

In this step, you give your Azure AI Search service permission to read data from your SQL Managed Instance.

1. In the Azure portal, go to your SQL Managed Instance page.
1. Select **Access control (IAM)**.
1. Select **Add** > **Add role assignment**.

   :::image type="content" source="./media/search-index-azure-sql-managed-instance-with-managed-identity/access-control-add-role-assignment.png" alt-text="Showing screenshot of the Access Control page." lightbox="media/search-index-azure-sql-managed-instance-with-managed-identity/access-control-add-role-assignment.png":::

1. Select the **Reader** role.
1. Leave **Assign access to** as **Microsoft Entra user, group, or service principal**.
1. If you're using a system-assigned managed identity, search for your search service and select it. If you're using a user-assigned managed identity, search for the name of the user-assigned managed identity and select it. Select **Save**.

    Here's an example for SQL Managed Instance using a system-assigned managed identity:

    :::image type="content" source="./media/search-index-azure-sql-managed-instance-with-managed-identity/add-role-assignment.png" alt-text="Showing screenshot of the member role assignment.":::

## Create the data source

Create the data source and provide a system-assigned managed identity. 

### System-assigned managed identity

The [REST API](/rest/api/searchservice/data-sources/create), Azure portal, and the [.NET SDK](/dotnet/api/azure.search.documents.indexes.models.searchindexerdatasourceconnection) support system-assigned managed identity.

When you connect by using a system-assigned managed identity, the only change to the data source definition is the format of the "credentials" property. You provide an Initial Catalog or Database name and a `ResourceId` that has no account key or password. The `ResourceId` must include the subscription ID of SQL Managed Instance, the resource group of SQL Managed instance, and the name of the SQL database.

Here's an example of how to create a data source to index data from a SQL Managed Instance using the [Create Data Source](/rest/api/searchservice/data-sources/create) REST API and a managed identity connection string. The managed identity connection string format is the same for the REST API, .NET SDK, and the Azure portal.  

```http
POST https://[service name].search.windows.net/datasources?api-version=2025-09-01
Content-Type: application/json
api-key: [admin key]

{
    "name" : "sql-mi-datasource",
    "type" : "azuresql",
    "credentials" : { 
        "connectionString" : "Database=[SQL database name];ResourceId=/subscriptions/[subscription ID]/resourcegroups/[resource group name]/providers/Microsoft.Sql/managedInstances/[SQL Managed Instance name];Connection Timeout=100;"
    },
    "container" : { 
        "name" : "my-table" 
    }
} 
```

## Create the index

The index specifies the fields in a document, attributes, and other constructs that shape the search experience.

Here's a [Create Index](/rest/api/searchservice/indexes/create) REST API call with a searchable `booktitle` field:

```http
POST https://[service name].search.windows.net/indexes?api-version=2025-09-01
Content-Type: application/json
api-key: [admin key]

{
    "name" : "my-target-index",
    "fields": [
        { "name": "id", "type": "Edm.String", "key": true, "searchable": false },
        { "name": "booktitle", "type": "Edm.String", "searchable": true, "filterable": false, "sortable": false, "facetable": false }
    ]
}
```

## Create the indexer

An indexer connects a data source with a target search index and provides a schedule to automate the data refresh. After you create the index and data source, create the indexer.

Here's a [Create Indexer](/rest/api/searchservice/indexers/create) REST API call with an Azure SQL indexer definition. The indexer runs when you submit the request.

```http
POST https://[service name].search.windows.net/indexers?api-version=2025-09-01
Content-Type: application/json
api-key: [admin key]

{
    "name" : "sql-mi-indexer",
    "dataSourceName" : "sql-mi-datasource",
    "targetIndexName" : "my-target-index"
}
```    

## Troubleshooting

If you get an error when the indexer tries to connect to the data source that says that the client isn't allowed to access the server, see the [common indexer errors](./search-indexer-troubleshooting.md).

You can also rule out any firewall problems by trying the connection with and without restrictions in place.

## See also

* [SQL Managed Instance and Azure SQL Database indexer](search-how-to-index-sql-database.md)
