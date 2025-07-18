---
title: Azure Cosmos DB NoSQL indexer
titleSuffix: Azure AI Search
description: Set up a search indexer to index data stored in Azure Cosmos DB for vector and full text search in Azure AI Search. This article explains how index data using the NoSQL API protocol.

manager: nitinme
author: mgottein
ms.author: magottei
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 05/08/2025
ms.custom:
  - devx-track-dotnet
  - ignite-2023
  - sfi-ropc-nochange
---

# Index data from Azure Cosmos DB for NoSQL for queries in Azure AI Search

In this article, learn how to configure an [**indexer**](search-indexer-overview.md) that imports content from [Azure Cosmos DB for NoSQL](/azure/cosmos-db/nosql/) and makes it searchable in Azure AI Search.

This article supplements [**Create an indexer**](search-howto-create-indexers.md) with information that's specific to Cosmos DB. It uses the Azure portal and REST APIs to demonstrate a three-part workflow common to all indexers: create a data source, create an index, create an indexer. Data extraction occurs when you submit the Create Indexer request.

Because terminology can be confusing, it's worth noting that [Azure Cosmos DB indexing](/azure/cosmos-db/index-overview) and [Azure AI Search indexing](search-what-is-an-index.md) are different operations. Indexing in Azure AI Search creates and loads a search index on your search service.

## Prerequisites

+ An [Azure Cosmos DB account, database, container, and items](/azure/cosmos-db/sql/create-cosmosdb-resources-portal). Use the same region for both Azure AI Search and Azure Cosmos DB for lower latency and to avoid bandwidth charges.

+ An [automatic indexing policy](/azure/cosmos-db/index-policy) on the Azure Cosmos DB collection, set to [Consistent](/azure/cosmos-db/index-policy#indexing-mode). This is the default configuration. Lazy indexing isn't recommended and can result in missing data.

+ Read permissions. A "full access" connection string includes a key that grants access to the content, but if you're using identities (Microsoft Entra ID), make sure the [search service managed identity](search-howto-managed-identities-data-sources.md) is assigned as both **Cosmos DB Account Reader Role** and [**Cosmos DB Built-in Data Reader Role**](/azure/cosmos-db/how-to-setup-rbac#built-in-role-definitions).

To work through the examples in this article, you need the Azure portal or a [REST client](search-get-started-text.md). If you're using Azure portal, make sure that access to all public networks is enabled. Other approaches for creating a Cosmos DB indexer include Azure SDKs.

## Try with sample data

Use these instructions to create a container and database in Cosmos DB for testing purposes.

1. [Download HotelsData_toCosmosDB.JSON](https://github.com/HeidiSteen/azure-search-sample-data/blob/main/hotels/HotelsData_toCosmosDB.JSON) from GitHub to create a container in Cosmos DB that contains a subset of the sample hotels data set.

1. Sign in to the Azure portal and [create an account, database, and container](/azure/cosmos-db/nosql/quickstart-portal) on Cosmos DB. 

1. In Cosmos DB, select **Data Explorer**  for the new container, provide the following values.

    | Property | Value |
    |----------|-------|
    | Database | Create new |
    | Database ID | hotelsdb |
    | Share throughput across containers | Don't select |
    | Container ID | hotels |
    | Partition key | /HotelId |
    | Container throughput (autoscale) | Autoscale |
    | Container Max RU/s | 1000 |

1. In **Data Explorer**, expand *hotelsdb* and *hotels*, and then select **Items**.

1. Select **Upload Item** and then select *HotelsData_toCosmosDB.JSON* file that you downloaded from GitHub.

1. Right-click **Items** and select **New SQL query**. The default query is `SELECT * FROM c`.

1. Select **Execute query** to run the query and view results. You should have 50 hotel documents.

Now that you have a container, you can use the Azure portal, REST client, or an Azure SDK to index your data.

The Description field provides the most verbose content. You should target this field for full text search and optional vector queries.

## Use the Azure portal

You can use either the **Import data** wizard or **Import and vectorize data wizard** to automate indexing from an SQL database table or view. The data source configuration is similar for both wizards.

1. [Start the wizard](search-import-data-portal.md#starting-the-wizards).

1. On **Connect to your data**, select or verify that the data source type is either *Azure Cosmos DB* or a *NoSQL account*.

   The data source name refers to the data source connection object in Azure AI Search. If you use the vector wizard, your data source name is autogenerated using a custom prefix specified at the end of the wizard workflow.

1. Specify the database name and collection. The query is optional. It's useful if you have hierarchical data and you want to import a specific slice.

1. Specify an authentication method, either a managed identity or built-in API key. If you don't specify a managed identity connection, the Azure portal uses the key.

   If you [configure Azure AI Search to use a managed identity](search-howto-managed-identities-data-sources.md), and you create a [role assignment on Cosmos DB](/azure/cosmos-db/how-to-setup-rbac#built-in-role-definitions) that grants **Cosmos DB Account Reader** and **Cosmos DB Built-in Data Reader** permissions to the identity, your indexer can connect to Cosmos DB using Microsoft Entra ID and roles.

1. For the **Import and vectorize data wizard**, you can specify options for change and deletion tracking.

   [Change detection](#incremental-indexing-and-custom-queries) is supported by default through a `_ts` field (timestamp). If you upload content using the approach described in [Try with sample data](#try-with-sample-data), the collection is created with a `_ts` field.

   [Deletion detection](#indexing-deleted-documents) requires that you have a preexisting top-level field in the collection that can be used as a soft-delete flag. It should be a Boolean field (you could name it IsDeleted). Specify `true` as the soft-deleted value. In the search index, add a corresponding search field called *IsDeleted* set to retrievable and filterable.

1. Continue with the remaining steps to complete the wizard:

   + [Import data wizard](search-get-started-portal.md)

   + [Import and vectorize data wizard](search-get-started-portal-import-vectors.md)

## Use the REST APIs

This section demonstrates the REST API calls that create a data source, index, and indexer.

### Define the data source

The data source definition specifies the data to index, credentials, and policies for identifying changes in the data. A data source is an independent resource that can be used by multiple indexers.

1. [Create or update a data source](/rest/api/searchservice/data-sources/create-or-update) to set its definition: 

    ```http
    POST https://[service name].search.windows.net/datasources?api-version=2024-07-01
    Content-Type: application/json
    api-key: [Search service admin key]
    {
        "name": "[my-cosmosdb-ds]",
        "type": "cosmosdb",
        "credentials": {
          "connectionString": "AccountEndpoint=https://[cosmos-account-name].documents.azure.com;AccountKey=[cosmos-account-key];Database=[cosmos-database-name]"
        },
        "container": {
          "name": "[my-cosmos-db-collection]",
          "query": null
        },
        "dataChangeDetectionPolicy": {
          "@odata.type": "#Microsoft.Azure.Search.HighWaterMarkChangeDetectionPolicy",
        "  highWaterMarkColumnName": "_ts"
        },
        "dataDeletionDetectionPolicy": null,
        "encryptionKey": null,
        "identity": null
    }
    ```

1. Set "type" to `"cosmosdb"` (required). If you're using an older Search API version 2017-11-11, the syntax for "type" is `"documentdb"`. Otherwise, for 2019-05-06 and later, use `"cosmosdb"`. 

1. Set "credentials" to a connection string. The next section describes the supported formats.

1. Set "container" to the collection. The "name" property is required and it specifies the ID of the database collection to be indexed. The "query" property is optional. Use it to [flatten an arbitrary JSON document](#flatten-structures) into a flat schema that Azure AI Search can index.

1. [Set "dataChangeDetectionPolicy"](#DataChangeDetectionPolicy) if data is volatile and you want the indexer to pick up just the new and updated items on subsequent runs.

1. [Set "dataDeletionDetectionPolicy"](#DataDeletionDetectionPolicy) if you want to remove search documents from a search index when the source item is deleted. 

<a name="credentials"></a>

#### Supported credentials and connection strings

Indexers can connect to a collection using the following connections.

Avoid port numbers in the endpoint URL. If you include the port number, the connection fails. 

| Full access connection string |
|-----------------------------------------------|
|`{ "connectionString" : "AccountEndpoint=https://<Cosmos DB account name>.documents.azure.com;AccountKey=<Cosmos DB auth key>;Database=<Cosmos DB database id>`" }` |
| You can get the connection string from the Azure Cosmos DB account page in the Azure portal by selecting **Keys** in the left pane. Make sure to select a full connection string and not just a key. |

| (Modern approach) Managed identity connection string for NoSQL accounts |
|------------------------------------------------------------------------------|
|`{ "connectionString" : "ResourceId=/subscriptions/<your subscription ID>/resourceGroups/<your resource group name>/providers/Microsoft.DocumentDB/databaseAccounts/<your cosmos db account name>/;(ApiKind=[api-kind];)/(IdentityAuthType=AccessToken)" }`|
|This connection string, supported only for Azure Cosmos DB for NoSQL accounts, ensures that the search service will never use account keys (even in the background) when attempting to access data from Cosmos DB. This is recommended, as it works even if the NoSQL account has account keys disabled. For more information, see [Setting up an indexer connection to an Azure Cosmos DB database using a managed identity](search-howto-managed-identities-cosmos-db.md)|

| (Legacy approach) Managed identity connection string |
|------------------------------------------------------|
|`{ "connectionString" : "ResourceId=/subscriptions/<your subscription ID>/resourceGroups/<your resource group name>/providers/Microsoft.DocumentDB/databaseAccounts/<your cosmos db account name>/;(ApiKind=[api-kind];)/(IdentityAuthType=AccountKey)" }`|
|This connection string doesn't require an account key to be specified directly, but the search service will utilize the managed identity to fetch the account keys in the background. Though this is supported for all Cosmos DB account types, it isn't recommended for the NoSQL account type. Such a connection string won't work if account keys are disabled for the Cosmos DB account. If the `IdentityAuthType` property is omitted, the search service will still default to fetching the account key in the background. For connections targeting the [SQL API](/azure/cosmos-db/sql-query-getting-started), you can omit `ApiKind` from the connection string. For more information about `ApiKind`, `IdentityAuthType` see [Setting up an indexer connection to an Azure Cosmos DB database using a managed identity](search-howto-managed-identities-cosmos-db.md)|

<a name="flatten-structures"></a>

#### Using queries to shape indexed data

In the "query" property under "container", you can specify a SQL query to flatten nested properties or arrays, project JSON properties, and filter the data to be indexed. 

Example document:

```http
    {
        "userId": 10001,
        "contact": {
            "firstName": "andy",
            "lastName": "hoh"
        },
        "company": "microsoft",
        "tags": ["azure", "cosmosdb", "search"]
    }
```

Filter query:

```sql
SELECT * FROM c WHERE c.company = "microsoft" and c._ts >= @HighWaterMark ORDER BY c._ts
```

Flattening query:

```sql
SELECT c.id, c.userId, c.contact.firstName, c.contact.lastName, c.company, c._ts FROM c WHERE c._ts >= @HighWaterMark ORDER BY c._ts
```

Projection query:

```sql
SELECT VALUE { "id":c.id, "Name":c.contact.firstName, "Company":c.company, "_ts":c._ts } FROM c WHERE c._ts >= @HighWaterMark ORDER BY c._ts
```

Array flattening query:

```sql
SELECT c.id, c.userId, tag, c._ts FROM c JOIN tag IN c.tags WHERE c._ts >= @HighWaterMark ORDER BY c._ts
```

<a name="SelectDistinctQuery"></a>

##### Unsupported queries (DISTINCT and GROUP BY)

Queries using the [DISTINCT keyword](/azure/cosmos-db/sql-query-keywords#distinct) or [GROUP BY clause](/azure/cosmos-db/sql-query-group-by) aren't supported. Azure AI Search relies on [SQL query pagination](/azure/cosmos-db/sql-query-pagination) to fully enumerate the results of the query. Neither the DISTINCT keyword or GROUP BY clauses are compatible with the [continuation tokens](/azure/cosmos-db/sql-query-pagination#continuation-tokens) used to paginate results.

Examples of unsupported queries:

```sql
SELECT DISTINCT c.id, c.userId, c._ts FROM c WHERE c._ts >= @HighWaterMark ORDER BY c._ts

SELECT DISTINCT VALUE c.name FROM c ORDER BY c.name

SELECT TOP 4 COUNT(1) AS foodGroupCount, f.foodGroup FROM Food f GROUP BY f.foodGroup
```

Although Azure Cosmos DB has a workaround to support [SQL query pagination with the DISTINCT keyword by using the ORDER BY clause](/azure/cosmos-db/sql-query-pagination#continuation-tokens), it isn't compatible with Azure AI Search. The query returns a single JSON value, whereas Azure AI Search expects a JSON object.

```sql
-- The following query returns a single JSON value and isn't supported by Azure AI Search
SELECT DISTINCT VALUE c.name FROM c ORDER BY c.name
```

### Add search fields to an index

In a [search index](search-what-is-an-index.md), add fields to accept the source JSON documents or the output of your custom query projection. Ensure that the search index schema is compatible with source data. For content in Azure Cosmos DB, your search index schema should correspond to the [Azure Cosmos DB items](/azure/cosmos-db/resource-model#azure-cosmos-db-items) in your data source.

1. [Create or update an index](/rest/api/searchservice/indexes/create) to define search fields that store data:

    ```http
    POST https://[service name].search.windows.net/indexes?api-version=2024-07-01
    Content-Type: application/json
    api-key: [Search service admin key]
    {
        "name": "mysearchindex",
        "fields": [{
            "name": "rid",
            "type": "Edm.String",
            "key": true,
            "searchable": false
        }, 
        {
            "name": "description",
            "type": "Edm.String",
            "filterable": false,
            "searchable": true,
            "sortable": false,
            "facetable": false,
            "suggestions": true
        }
      ]
    }
    ```

1. Create a document key field ("key": true). For partitioned collections, the default document key is the Azure Cosmos DB `_rid` property, which Azure AI Search automatically renames to `rid` because field names can’t start with an underscore character. Also, Azure Cosmos DB `_rid` values contain characters that are invalid in Azure AI Search keys. For this reason, the `_rid` values are Base64 encoded. 

1. Create more fields for more searchable content. See [Create an index](search-how-to-create-search-index.md) for details.

#### Mapping data types

| JSON data types | Azure AI Search field types |
| --- | --- |
| Bool |Edm.Boolean, Edm.String |
| Numbers that look like integers |Edm.Int32, Edm.Int64, Edm.String |
| Numbers that look like floating-points |Edm.Double, Edm.String |
| String |Edm.String |
| Arrays of primitive types such as ["a", "b", "c"] |Collection(Edm.String) |
| Strings that look like dates |Edm.DateTimeOffset, Edm.String |
| GeoJSON objects such as { "type": "Point", "coordinates": [long, lat] } |Edm.GeographyPoint |
| Other JSON objects |N/A |

### Configure and run the Azure Cosmos DB for NoSQL indexer

Once the index and data source have been created, you're ready to create the indexer. Indexer configuration specifies the inputs, parameters, and properties controlling run time behaviors.

1. [Create or update an indexer](/rest/api/searchservice/indexers/create) by giving it a name and referencing the data source and target index:

    ```http
    POST https://[service name].search.windows.net/indexers?api-version=2024-07-01
    Content-Type: application/json
    api-key: [search service admin key]
    {
        "name" : "[my-cosmosdb-indexer]",
        "dataSourceName" : "[my-cosmosdb-ds]",
        "targetIndexName" : "[my-search-index]",
        "disabled": null,
        "schedule": null,
        "parameters": {
            "batchSize": null,
            "maxFailedItems": 0,
            "maxFailedItemsPerBatch": 0,
            "base64EncodeKeys": false,
            "configuration": {}
            },
        "fieldMappings": [],
        "encryptionKey": null
    }
    ```

1. [Specify field mappings](search-indexer-field-mappings.md) if there are differences in field name or type, or if you need multiple versions of a source field in the search index.

1. See [Create an indexer](search-howto-create-indexers.md) for more information about other properties.

An indexer runs automatically when it's created. You can prevent this by setting "disabled" to true. To control indexer execution, [run an indexer on demand](search-howto-run-reset-indexers.md) or [put it on a schedule](search-howto-schedule-indexers.md).

## Check indexer status

To monitor the indexer status and execution history, check the indexer execution history in the Azure portal, or send a [Get Indexer Status](/rest/api/searchservice/indexers/get-status) REST APIrequest

### [**Portal**](#tab/portal-check-indexer)

1. On the search service page, open **Search management** > **Indexers**.

1. Select an indexer to access configuration and execution history.

1. Select a specific indexer job to view details, warnings, and errors.

### [**REST**](#tab/rest-check-indexer)
```http
GET https://myservice.search.windows.net/indexers/myindexer/status?api-version=2024-07-01
  Content-Type: application/json  
  api-key: [admin key]
```

The response includes status and the number of items processed. It should look similar to the following example:

```json
    {
        "status":"running",
        "lastResult": {
            "status":"success",
            "errorMessage":null,
            "startTime":"2022-02-21T00:23:24.957Z",
            "endTime":"2022-02-21T00:36:47.752Z",
            "errors":[],
            "itemsProcessed":1599501,
            "itemsFailed":0,
            "initialTrackingState":null,
            "finalTrackingState":null
        },
        "executionHistory":
        [
            {
                "status":"success",
                "errorMessage":null,
                "startTime":"2022-02-21T00:23:24.957Z",
                "endTime":"2022-02-21T00:36:47.752Z",
                "errors":[],
                "itemsProcessed":1599501,
                "itemsFailed":0,
                "initialTrackingState":null,
                "finalTrackingState":null
            },
            ... earlier history items
        ]
    }
```

---

Execution history contains up to 50 of the most recently completed executions, which are sorted in the reverse chronological order so that the latest execution comes first.

<a name="DataChangeDetectionPolicy"></a>

## Indexing new and changed documents

Once an indexer has fully populated a search index, you might want subsequent indexer runs to incrementally index just the new and changed documents in your database.

To enable incremental indexing, set the "dataChangeDetectionPolicy" property in your data source definition. This property tells the indexer which change tracking mechanism is used on your data.

For Azure Cosmos DB indexers, the only supported policy is the [`HighWaterMarkChangeDetectionPolicy`](/dotnet/api/azure.search.documents.indexes.models.highwatermarkchangedetectionpolicy) using the `_ts` (timestamp) property provided by Azure Cosmos DB. 

The following example shows a [data source definition](#define-the-data-source) with a change detection policy:

```http
"dataChangeDetectionPolicy": {
    "@odata.type": "#Microsoft.Azure.Search.HighWaterMarkChangeDetectionPolicy",
"  highWaterMarkColumnName": "_ts"
},
```

> [!NOTE]
> When you assign a `null` value to a field in your Azure Cosmos DB, the AI Search indexer is unable to distinguish between `null` and a missing field value. Therefore, if a field in the index is empty, it will not be substituted with a `null` value, even if that modification was made in your database.

<a name="IncrementalProgress"></a>

### Incremental indexing and custom queries

If you're using a [custom query to retrieve documents](#flatten-structures), make sure the query orders the results by the `_ts` column. This enables periodic check-pointing that Azure AI Search uses to provide incremental progress in the presence of failures.

In some cases, even if your query contains an `ORDER BY [collection alias]._ts` clause, Azure AI Search might not infer that the query is ordered by the `_ts`. You can tell Azure AI Search that results are ordered by setting the `assumeOrderByHighWaterMarkColumn` configuration property. 

To specify this hint, [create or update your indexer definition](#configure-and-run-the-azure-cosmos-db-for-nosql-indexer) as follows: 

```http
{
    ... other indexer definition properties
    "parameters" : {
        "configuration" : { "assumeOrderByHighWaterMarkColumn" : true } }
} 
```

<a name="DataDeletionDetectionPolicy"></a>

## Indexing deleted documents

When rows are deleted from the collection, you normally want to delete those rows from the search index as well. The purpose of a data deletion detection policy is to efficiently identify deleted data items. Currently, the only supported policy is the `Soft Delete` policy (deletion is marked with a flag of some sort), which is specified in the data source definition as follows:

```http
"dataDeletionDetectionPolicy"": {
    "@odata.type" : "#Microsoft.Azure.Search.SoftDeleteColumnDeletionDetectionPolicy",
    "softDeleteColumnName" : "the property that specifies whether a document was deleted",
    "softDeleteMarkerValue" : "the value that identifies a document as deleted"
}
```

If you're using a custom query, make sure that the property referenced by `softDeleteColumnName` is projected by the query.

The `softDeleteColumnName` must be a top-level field in the index. Using nested fields within complex data types as the `softDeleteColumnName` isn't supported.

The following example creates a data source with a soft-deletion policy:

```http
POST https://[service name].search.windows.net/datasources?api-version=2024-07-01
Content-Type: application/json
api-key: [Search service admin key]

{
    "name": "[my-cosmosdb-ds]",
    "type": "cosmosdb",
    "credentials": {
        "connectionString": "AccountEndpoint=https://[cosmos-account-name].documents.azure.com;AccountKey=[cosmos-account-key];Database=[cosmos-database-name]"
    },
    "container": { "name": "[my-cosmos-collection]" },
    "dataChangeDetectionPolicy": {
        "@odata.type": "#Microsoft.Azure.Search.HighWaterMarkChangeDetectionPolicy",
        "highWaterMarkColumnName": "_ts"
    },
    "dataDeletionDetectionPolicy": {
        "@odata.type": "#Microsoft.Azure.Search.SoftDeleteColumnDeletionDetectionPolicy",
        "softDeleteColumnName": "isDeleted",
        "softDeleteMarkerValue": "true"
    }
}
```

## Use .NET

For data accessed through the SQL API protocol, you can use the .NET SDK to automate with indexers. We recommend that you review the previous REST API sections to learn concepts, workflow, and requirements. You can then refer to following .NET API reference documentation to implement a JSON indexer in managed code:

+ [azure.search.documents.indexes.models.searchindexerdatasourceconnection](/dotnet/api/azure.search.documents.indexes.models.searchindexerdatasourceconnection)
+ [azure.search.documents.indexes.models.searchindexerdatasourcetype](/dotnet/api/azure.search.documents.indexes.models.searchindexerdatasourcetype)
+ [azure.search.documents.indexes.models.searchindex](/dotnet/api/azure.search.documents.indexes.models.searchindex)
+ [azure.search.documents.indexes.models.searchindexer](/dotnet/api/azure.search.documents.indexes.models.searchindexer)

## Next steps

You can now control how you [run the indexer](search-howto-run-reset-indexers.md), [monitor status](search-howto-monitor-indexers.md), or [schedule indexer execution](search-howto-schedule-indexers.md). The following articles apply to indexers that pull content from Azure Cosmos DB:

+ [Set up an indexer connection to an Azure Cosmos DB database using a managed identity](search-howto-managed-identities-cosmos-db.md)
+ [Index large data sets](search-howto-large-index.md)
+ [Indexer access to content protected by Azure network security features](search-indexer-securing-resources.md)
