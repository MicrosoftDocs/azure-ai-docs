---
title: Set up an indexer connection to Azure Cosmos DB using a managed identity
titleSuffix: Azure AI Search
description: Learn how to set up an indexer connection to an Azure Cosmos DB account using a managed identity.
author: arv100kri
ms.author: arjagann
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 08/27/2025
ms.update-cycle: 365-days
ms.custom:
  - subject-rbac-steps
  - ignite-2023
  - sfi-ropc-nochange
---

# Connect to Azure Cosmos DB using a managed identity (Azure AI Search)

This article explains how to set up an indexer connection to an Azure Cosmos DB database using a managed identity instead of providing credentials in the connection string.'

You can use a system-assigned managed identity or a user-assigned managed identity. Managed identities are Microsoft Entra logins and require Azure role assignments to access data in Azure Cosmos DB. You can optionally [enforce role-based access as the only authentication method](/azure/cosmos-db/how-to-setup-rbac#disable-local-auth) for data connections by setting `disableLocalAuth` to `true` for your Azure Cosmos DB for NoSQL account.

## Prerequisites

* [Create a managed identity](search-how-to-managed-identities.md) for your search service.

## Limitations

* Indexers that connect to Azure Cosmos DB for Gremlin and MongoDB (currently in preview) only support the _legacy_ approach.

## Supported approaches for managed identity authentication

Azure AI Search supports two mechanisms to connect to Azure Cosmos DB using managed identity. 

* The _legacy_ approach requires configuring the managed identity to have reader permissions on the control plane of the target Azure Cosmos DB account. Azure AI Search utilizes that identity to fetch the account keys of Cosmos DB account in the background to access the data. This approach won't work if the Cosmos DB account has `"disableLocalAuth": true`.

* The _modern_ approach requires configuring the managed identity appropriate roles on the control and data plane of the target Azure Cosmos DB account. Azure AI Search will then request an access token to access the data in the Cosmos DB account. This approach works even if the Cosmos DB account has `"disableLocalAuth": true`.

Indexers that connect to Azure Cosmos DB for NoSQL support both the _legacy_ and the _modern_ approach - the _modern_ approach is recommended.

## Connect to Azure Cosmos DB for NoSQL

This section outlines the steps to configure connecting to Azure Cosmos DB for NoSQL via the _modern_ approach.

### Configure control plane role assignments

1. Sign in to Azure portal and find your Cosmos DB for NoSQL account.

1. Select **Access control (IAM)**.

1. Select **Add** and then select **Role assignment**.

1. From the list of job function roles, select **Cosmos DB Account Reader**.

1. Select **Next**.

1. Select **Managed identity** and then select **Members**.

1. Filter by system-assigned managed identities or user-assigned managed identities. You should see the managed identity that you previously created for your search service. If you don't have one, see [Configure search to use a managed identity](search-how-to-managed-identities.md). If you already set one up but it's not available, give it a few minutes.

1. Select the identity and save the role assignment.

For more information, see [Use control plane role-based access control with Azure Cosmos DB for NoSQL](/azure/cosmos-db/nosql/security/how-to-grant-control-plane-role-based-access).

### Configure data plane role assignments

The managed identity needs to assigned a role to read from the Cosmos DB account's data plane. 
The Object (principal) ID for the search service's system/user assigned identity can be found from the search service's "Identity" tab.
This step can only be performed via Azure CLI at the moment. 

Set variables:

```azurecli
$cosmosdb_acc_name = <cosmos db account name>
$resource_group = <resource group name>
$subsciption = <subscription ID>
$system_assigned_principal = <Object (principal) ID for the search service's system/user assigned identity>
$readOnlyRoleDefinitionId = "00000000-0000-0000-0000-000000000001"
$scope=$(az cosmosdb show --name $cosmosdb_acc_name --resource-group $resource_group --query id --output tsv)
```

Define a role assignment for the system-assigned identity:

```azurecli
az cosmosdb sql role assignment create --account-name $cosmosdb_acc_name --resource-group $resource_group --role-definition-id $readOnlyRoleDefinitionId --principal-id $system_assigned_principal --scope $scope
```

For more information, see [Use data plane role-based access control with Azure Cosmos DB for NoSQL](/azure/cosmos-db/nosql/security/how-to-grant-data-plane-role-based-access)

### Configure the data source definition

Once you have configured **both** control plane and data plane role assignments on the Azure Cosmos DB for NoSQL account, you can set up a connection to it that operates under that role.

Indexers use a data source object for connections to an external data source. This section explains how to specify a system-assigned managed identity or a user-assigned managed identity on a data source connection string. You can find more [connection string examples](search-how-to-managed-identities.md#connection-string-examples) in the managed identity article.

> [!TIP]
> You can create a data source connection to Cosmos DB in the Azure portal, specifying either a system or user-assigned managed identity, and then view the JSON definition to see how the connection string is formulated.

The [REST API](/rest/api/searchservice/data-sources/create), Azure portal, and the [.NET SDK](/dotnet/api/azure.search.documents.indexes.models.searchindexerdatasourceconnection) support using a system-assigned or user-assigned managed identity.

#### Connect through system-assigned identity

When you're connecting with a system-assigned managed identity, the only change to the data source definition is the format of the "credentials" property. Provide a database name and a ResourceId that has no account key or password. The ResourceId must include the subscription ID of Azure Cosmos DB, the resource group, and the Azure Cosmos DB account name.

Here's an example using the [Create Data Source](/rest/api/searchservice/data-sources/create) REST API that exercises the _modern_ approach.

```http
POST https://[service name].search.windows.net/datasources?api-version=2025-09-01
{
    "name": "my-cosmosdb-ds",
    "type": "cosmosdb",
    "credentials": {
        "connectionString": "ResourceId=/subscriptions/[subscription-id]/resourceGroups/[rg-name]/providers/Microsoft.DocumentDB/databaseAccounts/[cosmos-account-name];Database=[cosmos-database];IdentityAuthType=AccessToken"
    },
    "container": { "name": "[my-cosmos-collection]" }
}
```

>[!NOTE]
> If the `IdentityAuthType` property isn't part of the connection string, then Azure AI Search defaults to the _legacy_ approach to ensure backward compatibility.

#### Connect through user-assigned identity (preview)

You need to add an "identity" property to the data source definition, where you specify the specific identity (out of several that can be assigned to the search service), that will be used to connect to the Azure Cosmos DB account.

Here's an example using user-assigned identity via the _modern_ approach.

```http
POST https://[service name].search.windows.net/datasources?api-version=2025-11-01-preview
{
    "name": "[my-cosmosdb-ds]",
    "type": "cosmosdb",
    "credentials": {
        "connectionString": "ResourceId=/subscriptions/[subscription-id]/resourceGroups/[rg-name]/providers/Microsoft.DocumentDB/databaseAccounts/[cosmos-account-name];Database=[cosmos-database];IdentityAuthType=AccessToken"
    },
    "container": { "name": "[my-cosmos-collection]"},
    "identity" : { 
        "@odata.type": "#Microsoft.Azure.Search.DataUserAssignedIdentity",
        "userAssignedIdentity": "/subscriptions/[subscription-id]/resourcegroups/[rg-name]/providers/Microsoft.ManagedIdentity/userAssignedIdentities/[my-user-managed-identity-name]" 
    }
}
```

## Connect to Azure Cosmos DB for Gremlin/MongoDB (preview)

This section outlines the steps to configure connecting to Azure Cosmos DB for Gremlin/Mongo via the _legacy_ approach.

### Configure control plane role assignments

Follow the same steps as before to assign the appropriate roles on the control plane of the Azure Cosmos DB for Gremlin/MongoDB.

### Set the connection string

* For MongoDB collections, add "ApiKind=MongoDb" to the connection string and use a preview REST API.
* For Gremlin graphs, add "ApiKind=Gremlin" to the connection string and use a preview REST API.
* For either kinds, only the __legacy__ approach is supported - that is, `IdentityAuthType=AccountKey` or omitting it entirely is the only valid connection string.

Here's an example to connect to MongoDB collections using system-assigned identity via the REST API

```http
POST https://[service name].search.windows.net/datasources?api-version=2025-11-01-preview
{
    "name": "my-cosmosdb-ds",
    "type": "cosmosdb",
    "credentials": {
        "connectionString": "ResourceId=/subscriptions/[subscription-id]/resourceGroups/[rg-name]/providers/Microsoft.DocumentDB/databaseAccounts/[cosmos-account-name];Database=[cosmos-database];ApiKind=MongoDb"
    },
    "container": { "name": "[my-cosmos-collection]", "query": null },
    "dataChangeDetectionPolicy": null
}
```

Here's an example to connect to Gremlin graphs using user-assigned identity.

```http
POST https://[service name].search.windows.net/datasources?api-version=2025-11-01-preview
{
    "name": "[my-cosmosdb-ds]",
    "type": "cosmosdb",
    "credentials": {
        "connectionString": "ResourceId=/subscriptions/[subscription-id]/resourceGroups/[rg-name]/providers/Microsoft.DocumentDB/databaseAccounts/[cosmos-account-name];Database=[cosmos-database];ApiKind=Gremlin"
    },
    "container": { "name": "[my-cosmos-collection]"},
    "identity" : { 
        "@odata.type": "#Microsoft.Azure.Search.DataUserAssignedIdentity",
        "userAssignedIdentity": "/subscriptions/[subscription-id]/resourcegroups/[rg-name]/providers/Microsoft.ManagedIdentity/userAssignedIdentities/[my-user-managed-identity-name]" 
    }
}
```

## Run the indexer to verify permissions

Connection information and permissions on the remote service are validated at run time during indexer execution. If the indexer is successful, the connection syntax and role assignments are valid. For more information, see [Run or reset indexers, skills, or documents](search-howto-run-reset-indexers.md).

## Troubleshoot connections

* For Azure Cosmos DB for NoSQL, check whether the account has its access restricted to select networks. You can rule out any firewall issues by trying the connection without restrictions in place. Refer to [Indexer access to content protected by Azure network security](search-indexer-securing-resources.md) for more information

* For Azure Cosmos DB for NoSQL, if the indexer fails due to authentication issues, ensure that the role assignments have been done **both** on the control plane and data plane of the Cosmos DB account.

* For Gremlin or MongoDB, if you recently rotated your Azure Cosmos DB account keys, you need to wait up to 15 minutes for the managed identity connection string to work.

## See also

* [Indexing via an Azure Cosmos DB for NoSQL](search-how-to-index-cosmosdb-sql.md)
* [Indexing via an Azure Cosmos DB for MongoDB](search-how-to-index-cosmosdb-mongodb.md)
* [Indexing via an Azure Cosmos DB for Apache Gremlin](search-how-to-index-cosmosdb-gremlin.md)
