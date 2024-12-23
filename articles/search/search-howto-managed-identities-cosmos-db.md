---
title: Set up an indexer connection to Azure Cosmos DB using a managed identity
titleSuffix: Azure AI Search
description: Learn how to set up an indexer connection to an Azure Cosmos DB account using a managed identity.
author: arv100kri
ms.author: arjagann

ms.service: azure-ai-search
ms.topic: how-to
ms.date: 12/23/2024
ms.custom:
  - subject-rbac-steps
  - ignite-2023
---

# Connect to Azure Cosmos DB using a managed identity (Azure AI Search)

This article explains how to set up an indexer connection to an Azure Cosmos DB database using a managed identity instead of providing credentials in the connection string.'

You can use a system-assigned managed identity or a user-assigned managed identity. Managed identities are Microsoft Entra logins and require Azure role assignments to access data in Azure Cosmos DB. 

## Background

Azure AI Search supports two mechanisms to connect using managed identity. 

1. The _legacy_ approach requires configuring the managed identity to have reader permissions on the management plane of the target Azure Cosmos DB account. Azure AI Search will then utilize that identity to fetch the account keys of Cosmos DB account in the background to access the data. This approach won't work if the Cosmos DB account has `"disableLocalAuth": true`. This approach is no longer recommended when connecting to Azure Cosmos DB accounts for NoSQL accounts.

1. The _recommended_ approach requires configuring the managed identity appropriate roles on the management and data plane of the target Azure Cosmos DB account. Azure AI Search will then request an access token to access the data in the Cosmos DB account. This approach works if the Cosmos DB account has `"disableLocalAuth": true`, and is therefore recommended as the more secure option when connecting to Azure Cosmos DB accounts for NoSQL accounts.

The rest of this document walks through the steps for the _recommended_ approach, with callouts as needed comparing it with the _legacy_ approach.

### Limitations

Indexer support for Azure Cosmos DB for Gremlin and MongoDB Collections is currently in preview and only supports the _legacy_ approach. The _recommended_ approach only works with Azure Cosmos DB for NoSQL. 

## Prerequisites

* [Create a managed identity](search-howto-managed-identities-data-sources.md) for your search service.

* You can optionally [enforce role-based access as the only authentication method](/azure/cosmos-db/how-to-setup-rbac#disable-local-auth) for data connections by setting `disableLocalAuth` to `true` for your Azure Cosmos DB for NoSQL account.

## Step 1: Configure role assignments on Azure Cosmos DB control plane

### [**Azure portal**](#tab/portal)

1. Sign in to Azure portal and find your Cosmos DB for NoSQL account.

1. Select **Access control (IAM)**.

1. Select **Add** and then select **Role assignment**.

1. From the list of job function roles, select **Cosmos DB Account Reader**.

1. Select **Next**.

1. Select **Managed identity** and then select **Members**.

1. Filter by system-assigned managed identities or user-assigned managed identities. You should see the managed identity that you previously created for your search service. If you don't have one, see [Configure search to use a managed identity](search-howto-managed-identities-data-sources.md). If you already set one up but it's not available, give it a few minutes.

1. Select the identity and save the role assignment.

For more information, see [Use control plane role-based access control with Azure Cosmos DB for NoSQL](/azure/cosmos-db/nosql/security/how-to-grant-control-plane-role-based-access).

## Step 2: Configure role assignments on Azure Cosmos DB data plane

The managed identity needs to assigned a role to read from the Cosmos DB account's data plane. This step can only be performed via Azure CLI at the moment. The Object (principal) ID for the search service's system/user assigned identity can be found from the search service's "Identity" tab.

### [**Azure CLI**](#tab/azcli)

Set variables:

```azurecli
$cosmosdb_acc_name = <cosmos db account name>
$resource_group = <resource group name>
$subsciption = <subscription ID>
$system_assigned_principal = <Object (principal) ID for the search service's system/user assigned identity>
$readOnlyRoleDefinitionId = "00000000-0000-0000-0000-00000000000"
$scope=$(az cosmosdb show --name $cosmosdbname --resource-group $resourcegroup --query id --output tsv)
```

Define a role assignment for the system-assigned identity:

```azurecli
az cosmosdb sql role assignment create --account-name $cosmosdbname --resource-group $resourcegroup --role-definition-id $readOnlyRoleDefinitionId --principal-id $sys_principal --scope $scope
```

For more information, see [Use data plane role-based access control with Azure Cosmos DB for NoSQL](/azure/cosmos-db/nosql/security/how-to-grant-data-plane-role-based-access)

## Step 3: Configure Azure AI Search data source with managed identity connection string

Once you have configured **both** control plane and data plane role assignments on the Azure Cosmos DB for NoSQL account, you can set up a connection to it that operates under that role.

Indexers use a data source object for connections to an external data source. This section explains how to specify a system-assigned managed identity or a user-assigned managed identity on a data source connection string. You can find more [connection string examples](search-howto-managed-identities-data-sources.md#connection-string-examples) in the managed identity article.

> [!TIP]
> You can create a data source connection to CosmosDB in the Azure portal, specifying either a system or user-assigned managed identity, and then view the JSON definition to see how the connection string is formulated.

### System-assigned managed identity

The [REST API](/rest/api/searchservice/data-sources/create), Azure portal, and the [.NET SDK](/dotnet/api/azure.search.documents.indexes.models.searchindexerdatasourceconnection) support using a system-assigned managed identity. 

When you're connecting with a system-assigned managed identity, the only change to the data source definition is the format of the "credentials" property. Provide a database name and a ResourceId that has no account key or password. The ResourceId must include the subscription ID of Azure Cosmos DB, the resource group, and the Azure Cosmos DB account name.

* For SQL collections, the connection string doesn't require "ApiKind". 
* For SQL collections, add "IdentityAuthType=AccessToken" to go through the _recommended_ approach, that is more secure and will work even if the account is configured to enforce role-based access as the only authentication method (that is, `"disableLocalAuth": true`)
    * When using the REST API or the SDK, if this property isn't specified on the connection string, Azure AI Search defaults to using the _legacy_ approach. Azure portal appends this property to the connection string as the default.
* For MongoDB collections, add "ApiKind=MongoDb" to the connection string and use a preview REST API.
* For Gremlin graphs, add "ApiKind=Gremlin" to the connection string and use a preview REST API.

MongoDB and Gremlin don't yet support the _recommended_ approach.

Here's an example of how to create a data source to index data from a Cosmos DB account using the [Create Data Source](/rest/api/searchservice/data-sources/create) REST API and a managed identity connection string that exercises the _recommended_ approach.

```http
POST https://[service name].search.windows.net/datasources?api-version=2024-07-01
{
    "name": "my-cosmosdb-ds",
    "type": "cosmosdb",
    "credentials": {
        "connectionString": "ResourceId=/subscriptions/[subscription-id]/resourceGroups/[rg-name]/providers/Microsoft.DocumentDB/databaseAccounts/[cosmos-account-name];Database=[cosmos-database];ApiKind=SQL;IdentityAuthType=AccessToken"
    },
    "container": { "name": "[my-cosmos-collection]", "query": null },
    "dataChangeDetectionPolicy": null

 
}
```

For completeness, here's the same example presented that goes through the _legacy_ approach

```http
POST https://[service name].search.windows.net/datasources?api-version=2024-07-01
{
    "name": "my-cosmosdb-ds",
    "type": "cosmosdb",
    "credentials": {
        "connectionString": "ResourceId=/subscriptions/[subscription-id]/resourceGroups/[rg-name]/providers/Microsoft.DocumentDB/databaseAccounts/[cosmos-account-name];Database=[cosmos-database];ApiKind=SQL;IdentityAuthType=AccountKey"
    },
    "container": { "name": "[my-cosmos-collection]", "query": null },
    "dataChangeDetectionPolicy": null
}
```

>[!NOTE]
> If the `IdentityAuthType` property is not specified at all, then Azure AI Search defaults to the _legacy_ approach to ensure backward compatibility.

### User-assigned managed identity

When you're connecting with a user-assigned managed identity, the connection string definition remains the same as before.

You'll need to add an "identity" property to the data source definition, where you specify the specific identity (out of several that can be assigned to the search service), that will be used to connect to the Azure Cosmos DB account.

Here's an example of how to configure the data source definition, for an Azure Cosmos DB for NOSQL account, using user-assigned identity via the _recommended_ approach.

```http
POST https://[service name].search.windows.net/datasources?api-version=2024-07-01

{
    "name": "[my-cosmosdb-ds]",
    "type": "cosmosdb",
    "credentials": {
        "connectionString": "ResourceId=/subscriptions/[subscription-id]/resourceGroups/[rg-name]/providers/Microsoft.DocumentDB/databaseAccounts/[cosmos-account-name];Database=[cosmos-database];ApiKind=SQL;IdentityAuthType=AccessToken"
    },
    "container": { 
        "name": "[my-cosmos-collection]", "query": null 
    },
    "identity" : { 
        "@odata.type": "#Microsoft.Azure.Search.DataUserAssignedIdentity",
        "userAssignedIdentity": "/subscriptions/[subscription-id]/resourcegroups/[rg-name]/providers/Microsoft.ManagedIdentity/userAssignedIdentities/[my-user-managed-identity-name]" 
    },
    "dataChangeDetectionPolicy": null
}
```

## Step 4: Run the indexer and validate the outcome

Connection information and permissions on the remote service are validated at run time during indexer execution. If the indexer is successful, the connection syntax and role assignments are valid. For more information, see [Run or reset indexers, skills, or documents](search-howto-run-reset-indexers.md).

## Troubleshooting

* For Azure Cosmos DB for NoSQL, check whether the account has its access restricted to select networks. You can rule out any firewall issues by trying the connection without restrictions in place. Refer to [Indexer access to content protected by Azure network security](search-indexer-securing-resources) for more information

* For Azure Cosmos DB for NoSQL, if the indexer fails due to authentication issues, ensure that the role assignments have been done **both** on the control plane and data plane of the Cosmos DB account.

* For Gremlin or MongoDB, if you recently rotated your Azure Cosmos DB account keys, you need to wait up to 15 minutes for the managed identity connection string to work.

## See also

* [Indexing via an Azure Cosmos DB for NoSQL](search-howto-index-cosmosdb.md)
* [Indexing via an Azure Cosmos DB for MongoDB](search-howto-index-cosmosdb-mongodb.md)
* [Indexing via an Azure Cosmos DB for Apache Gremlin](search-howto-index-cosmosdb-gremlin.md)
