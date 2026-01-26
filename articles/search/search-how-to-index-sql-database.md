---
title: Azure SQL indexer
titleSuffix: Azure AI Search
description: Set up a search indexer to index tables in Azure SQL Database for vector and full text search in Azure AI Search.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 11/21/2025
ms.update-cycle: 180-days
ms.custom:
  - ignite-2023
  - sfi-ropc-nochange
---

# Index data from Azure SQL Database

In this article, learn how to configure an [**indexer**](search-indexer-overview.md) that imports content from Azure SQL Database or an Azure SQL managed instance and makes it searchable in Azure AI Search. 

This article supplements [**Create an indexer**](search-howto-create-indexers.md) with information that's specific to Azure SQL. It uses the Azure portal and REST APIs to demonstrate a three-part workflow common to all indexers: create a data source, create an index, create an indexer. Data extraction occurs when you submit the Create Indexer request.

This article also provides:

+ A description of the [change detection policies](#indexing-new-changed-and-deleted-rows) supported by the Azure SQL indexer so that you can set up incremental indexing.

+ A [frequently-asked-questions (FAQ) section](#faq) for answers to questions about feature compatibility.

> [!NOTE]
> Real-time data synchronization isn't possible with an indexer. An indexer can reindex your table at most every five minutes. If data updates need to be reflected in the index sooner, we recommend [pushing updated rows directly](tutorial-optimize-indexing-push-api.md).

## Prerequisites

+ An [Azure SQL database](/azure/azure-sql/database/sql-database-paas-overview) or a [SQL Managed Instance with a public endpoint](search-how-to-index-sql-managed-instance.md).

+ A single table or view.

  Use a table if your data is large or if you need incremental indexing using SQL's native change detection capabilities ([SQL integrated change tracking](#indexing-new-changed-and-deleted-rows)) to reflect new, changed, and deleted rows in the search index.

  Use a view if you need to consolidate data from multiple tables. Large views aren't ideal for SQL indexer. A workaround is to create a new table just for ingestion into your Azure AI Search index. If you choose to go with a view, you can use [High Water Mark](#indexing-new-changed-and-deleted-rows) for change detection, but must use a workaround for deletion detection.

+ Primary key must be single-valued. On a table, it must also be non-clustered for full SQL integrated change tracking.

+ Read permissions. Azure AI Search supports SQL Server authentication, where the user name and password are provided on the connection string. Alternatively, you can [set up a managed identity and use Azure roles](search-howto-managed-identities-sql.md) with membership in **SQL Server Contributor** or **SQL DB Contributor** roles.

To work through the examples in this article, you need the Azure portal or a [REST client](search-get-started-text.md). If you're using Azure portal, make sure that access to all public networks is enabled in the Azure SQL firewall and that the client has access via an inbound rule. For a REST client that runs locally, configure the SQL Server firewall to allow inbound access from your device IP address. Other approaches for creating an Azure SQL indexer include Azure SDKs.

## Try with sample data

Use these instructions to create and load a table in Azure SQL Database for testing purposes.

1. [Download hotels-azure-sql.sql](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/hotels/hotel-sql) from GitHub to create a table on Azure SQL Database that contains a subset of the sample hotels data set.

1. Sign in to the Azure portal and [create an Azure SQL database and database server](/azure/azure-sql/database/single-database-create-quickstart). Consider configuring both SQL Server authentication and Microsoft Entra ID authentication. If you don't have permissions to configure roles on Azure, you can use SQL authentication as a workaround.

1. Configure the server firewall to all inbound requests from your local device.

1. On your Azure SQL database, select **Query editor (preview)** and then select **New Query**.

1. Paste in and then run the T-SQL script that creates the hotels table. A non-clustered primary key is a requirement for SQL integrated change tracking.

   ```tsql
   CREATE TABLE tbl_hotels
    (
        Id TINYINT PRIMARY KEY NONCLUSTERED,
        Modified DateTime NULL DEFAULT '0000-00-00 00:00:00',
        IsDeleted TINYINT,
        HotelName VARCHAR(40),
        Category VARCHAR(20),
        City VARCHAR(30),
        State VARCHAR(4),
        Description VARCHAR(500)
    );
    ```

1. Paste in and then run the T-SQL script that inserts records.

   ```tsql
    -- Insert rows
    INSERT INTO tbl_hotels (Id, Modified, IsDeleted, HotelName, Category, City, State, Description) VALUES (1, CURRENT_TIMESTAMP, 0,  'Stay-Kay City Hotel', 'Boutique', 'New York', 'NY', 'This classic hotel is fully-refurbished and ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Times Square and the historic centre of the city, as well as other places of interest that make New York one of Americas most attractive and cosmopolitan cities.');
    INSERT INTO tbl_hotels (Id, Modified, IsDeleted, HotelName, Category, City, State, Description) VALUES (10, CURRENT_TIMESTAMP, 0, 'Countryside Hotel', 'Extended-Stay', 'Durham', 'NC', 'Save up to 50% off traditional hotels. Free WiFi, great location near downtown, full kitchen, washer & dryer, 24\/7 support, bowling alley, fitness center and more.');
    INSERT INTO tbl_hotels (Id, Modified, IsDeleted, HotelName, Category, City, State, Description) VALUES (11, CURRENT_TIMESTAMP, 0, 'Royal Cottage Resort', 'Extended-Stay', 'Bothell', 'WA', 'Your home away from home. Brand new fully equipped premium rooms, fast WiFi, full kitchen, washer & dryer, fitness center. Inner courtyard includes water features and outdoor seating. All units include fireplaces and small outdoor balconies. Pets accepted.');
    INSERT INTO tbl_hotels (Id, Modified, IsDeleted, HotelName, Category, City, State, Description) VALUES (12, CURRENT_TIMESTAMP, 0, 'Winter Panorama Resort', 'Resort and Spa', 'Wilsonville', 'OR', 'Plenty of great skiing, outdoor ice skating, sleigh rides, tubing and snow biking. Yoga, group exercise classes and outdoor hockey are available year-round, plus numerous options for shopping as well as great spa services. Newly-renovated with large rooms, free 24-hr airport shuttle & a new restaurant. Rooms\/suites offer mini-fridges & 49-inch HDTVs.');
    INSERT INTO tbl_hotels (Id, Modified, IsDeleted, HotelName, Category, City, State, Description) VALUES (13, CURRENT_TIMESTAMP, 0, 'Luxury Lion Resort', 'Luxury', 'St. Louis', 'MO', 'Unmatched Luxury. Visit our downtown hotel to indulge in luxury accommodations. Moments from the stadium and transportation hubs, we feature the best in convenience and comfort.');
    INSERT INTO tbl_hotels (Id, Modified, IsDeleted, HotelName, Category, City, State, Description) VALUES (14, CURRENT_TIMESTAMP, 0, 'Twin Vortex Hotel', 'Luxury', 'Dallas', 'TX', 'New experience in the making. Be the first to experience the luxury of the Twin Vortex. Reserve one of our newly-renovated guest rooms today.');
    INSERT INTO tbl_hotels (Id, Modified, IsDeleted, HotelName, Category, City, State, Description) VALUES (15, CURRENT_TIMESTAMP, 0, 'By the Market Hotel', 'Budget', 'New York', 'NY', 'Book now and Save up to 30%. Central location. Walking distance from the Empire State Building & Times Square, in the Chelsea neighborhood. Brand new rooms. Impeccable service.');
    INSERT INTO tbl_hotels (Id, Modified, IsDeleted, HotelName, Category, City, State, Description) VALUES (16, CURRENT_TIMESTAMP, 0, 'Double Sanctuary Resort', 'Resort and Spa', 'Seattle', 'WA', '5 Star Luxury Hotel - Biggest Rooms in the city. #1 Hotel in the area listed by Traveler magazine. Free WiFi, Flexible check in\/out, Fitness Center & espresso in room.');
    INSERT INTO tbl_hotels (Id, Modified, IsDeleted, HotelName, Category, City, State, Description) VALUES (17, CURRENT_TIMESTAMP, 0, 'City Skyline Antiquity Hotel', 'Boutique', 'New York', 'NY', 'In vogue since 1888, the Antiquity Hotel takes you back to bygone era. From the crystal chandeliers that adorn the Green Room, to the arched ceilings of the Grand Hall, the elegance of old New York beckons. Elevate Your Experience. Upgrade to a premiere city skyline view for less, where old world charm combines with dramatic views of the city, local cathedral and midtown.');
    INSERT INTO tbl_hotels (Id, Modified, IsDeleted, HotelName, Category, City, State, Description) VALUES (18, CURRENT_TIMESTAMP, 0, 'Ocean Water Resort & Spa', 'Luxury', 'Tampa', 'FL', 'New Luxury Hotel for the vacation of a lifetime. Bay views from every room, location near the pier, rooftop pool, waterfront dining & more.');
    INSERT INTO tbl_hotels (Id, Modified, IsDeleted, HotelName, Category, City, State, Description) VALUES (19, CURRENT_TIMESTAMP, 0, 'Economy Universe Motel', 'Budget', 'Redmond', 'WA', 'Local, family-run hotel in bustling downtown Redmond. We are a pet-friendly establishment, near expansive Marymoor park, haven to pet owners, joggers, and sports enthusiasts. Close to the highway and just a short drive away from major cities.');
    INSERT INTO tbl_hotels (Id, Modified, IsDeleted, HotelName, Category, City, State, Description) VALUES (20, CURRENT_TIMESTAMP, 0, 'Delete Me Hotel', 'Unknown', 'Nowhere', 'XX', 'Test-case row for change detection and delete detection . For change detection, modify any value, and then re-run the indexer. For soft-delete, change IsDelete from zero to a one, and then re-run the indexer.');
    
    ```

1. Run a query to confirm the upload.

   ```tsql
   SELECT Description FROM tbl_hotels;
    ```

   You should see results similar to the following screenshot.

   :::image type="content" source="media/search-how-to-index-sql-database/tsql-query-results.png" alt-text="Screenshot of query results showing the description field.":::

The Description field provides the most verbose content. You should target this field for full text search and optional vectorization.

Now that you have a database table, you can use the Azure portal, REST client, or an Azure SDK to index your data.

> [!TIP]
> Another resource that provides sample content and code can be found on [Azure-Samples/SQL-AI-samples](https://github.com/Azure-Samples/SQL-AI-samples/tree/main/AzureSQLACSSamples/src).

## Set up the indexer pipeline

In this step, specify the data source, index, and indexer.

### [**Azure portal**](#tab/portal-sql)

1. Make sure your SQL database is active and not paused due to inactivity. In the Azure portal, navigate to the database server page and verify the database status is *online*. You can run a query on any table to activate the database.

   :::image type="content" source="media/search-how-to-index-sql-database/database-online.png" alt-text="Screenshot of the database status page in the Azure portal.":::

1. Make sure you have a table or view that meets the requirements for indexers and change detection.

   First, you can only pull from a single table or view. We recommend tables because they support SQL integrated change tracking policy, which detects new, updated, and deleted rows. A high water mark policy doesn't support row deletion and is harder to implement.

   Second, the primary key must be a single value (compound keys aren't supported) and non-clustered.

1. Switch to your search service and create a data source. Under **Search management** > **Data sources**, select **Add data source**:

   1. For data source type, choose *Azure SQL Database*.
   1. Provide a name for the data source object on Azure AI Search.
   1. Use the dropdowns to select the subscription, account type, server, database, table or view, schema, and table name.
   1. For change tracking we recommend **SQL Integrated Change Tracking Policy**.
   1. For authentication, we recommend connecting with a [managed identity](search-how-to-managed-identities.md). Your search service must have **SQL Server Contributor** or **SQL DB Contributor** role membership on the database.
   1. Select **Create** to create the data source.

   :::image type="content" source="media/search-how-to-index-sql-database/search-data-source.png" alt-text="Screenshot of the data source creation page in the Azure portal.":::

1. Use an [import wizard](search-import-data-portal.md) to create the index and indexer.

   1. On the **Overview** page, select **Import data** or **Import data (new)**.

   1. Select the data source you just created.

   1. Skip the step for adding AI enrichments.

   1. Name the index, set the key to your primary key in the table, attribute all fields as **Retrievable** and **Searchable**, and optionally add **Filterable** and **Sortable** for short strings or numeric values.

   1. Name the indexer and finish the wizard to create the necessary objects.

### [**REST**](#tab/test-sql)

This section demonstrates the REST API calls that create a data source, index, and indexer.

### Define the data source

The data source definition specifies the data to index, credentials, and policies for identifying changes in the data. A data source is defined as an independent resource so that it can be used by multiple indexers.

1. [Create Data Source](/rest/api/searchservice/data-sources/create) or [Create or Update Data Source](/rest/api/searchservice/data-sources/create-or-update) to set its definition: 

   ```http
    POST https://myservice.search.windows.net/datasources?api-version=2025-09-01
    Content-Type: application/json
    api-key: admin-key

    {
        "name" : "myazuresqldatasource",
        "description" : "A database for testing Azure AI Search indexes.",
        "type" : "azuresql",
        "credentials" : { "connectionString" : "Server=tcp:<your server>.database.windows.net,1433;Database=<your database>;User ID=<your user name>;Password=<your password>;Trusted_Connection=False;Encrypt=True;Connection Timeout=30;" },
        "container" : { 
            "name" : "name of the table or view that you want to index",
            "query" : null (not supported in the Azure SQL indexer)
            },
        "dataChangeDetectionPolicy": null,
        "dataDeletionDetectionPolicy": null,
        "encryptionKey": null,
        "identity": null
    }
   ```

1. Provide a unique name for the data source that follows Azure AI Search [naming conventions](/rest/api/searchservice/naming-rules).

1. Set "type" to `"azuresql"` (required).

1. Set "credentials" to a connection string:

   + You can get a full access connection string from the [Azure portal](https://portal.azure.com). Use the `ADO.NET connection string` option. Set the user name and password.

   + Alternatively, you can specify a managed identity connection string that doesn't include database secrets with the following format: `Initial Catalog|Database=<your database name>;ResourceId=/subscriptions/<your subscription ID>/resourceGroups/<your resource group name>/providers/Microsoft.Sql/servers/<your SQL Server name>/;Connection Timeout=connection timeout length;`.

    For more information, see [Connect to Azure SQL Database indexer using a managed identity](search-howto-managed-identities-sql.md).

> [!NOTE]
> For the container name property, the value is restricted to only allow letters, numbers, underscores (_), dots (.), single dashes (-), and square brackets ([])

### Add search fields to an index

In a [search index](search-what-is-an-index.md), add fields that correspond to the fields in SQL database. Ensure that the search index schema is compatible with source schema by using [equivalent data types](#TypeMapping).

1. [Create or update an index](/rest/api/searchservice/indexes/create) to define search fields that store data:

    ```http
    POST https://[service name].search.windows.net/indexes?api-version=2025-09-01
    Content-Type: application/json
    api-key: [Search service admin key]
    {
        "name": "mysearchindex",
        "fields": [{
            "name": "id",
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

1. Create a document key field ("key": true) that uniquely identifies each search document. This is the only field that's required in a search index. Typically, the table's primary key is mapped to the index key field. The document key must be unique and non-null. The values can be numeric in source data, but in a search index, a key is always a string.

1. Create more fields to add more searchable content. See [Create an index](search-how-to-create-search-index.md) for guidance.

<a name="TypeMapping"></a>

#### Mapping data types

| SQL data type | Azure AI Search field types | Notes |
| ------------- | -------------------------------- | --- |
| bit |Edm.Boolean, Edm.String | |
| int, smallint, tinyint |Edm.Int32, Edm.Int64, Edm.String | |
| bigint |Edm.Int64, Edm.String | |
| real, float |Edm.Double, Edm.String | |
| smallmoney, money decimal numeric |Edm.String |Azure AI Search doesn't support converting decimal types into `Edm.Double` because doing so would lose precision |
| char, nchar, varchar, nvarchar |Edm.String<br/>Collection(Edm.String) |A SQL string can be used to populate a Collection(`Edm.String`) field if the string represents a JSON array of strings: `["red", "white", "blue"]` |
| smalldatetime, datetime, datetime2, date, datetimeoffset |Edm.DateTimeOffset, Edm.String | |
| uniqueidentifer |Edm.String | |
| geography |Edm.GeographyPoint |Only geography instances of type POINT with SRID 4326 (which is the default) are supported |
| rowversion |Not applicable |Row-version columns can't be stored in the search index, but they can be used for change tracking |
| time, timespan, binary, varbinary, image, xml, geometry, CLR types |Not applicable |Not supported |

### Configure and run the Azure SQL indexer

Once the index and data source have been created, you're ready to create the indexer. Indexer configuration specifies the inputs, parameters, and properties controlling run time behaviors.

1. [Create or update an indexer](/rest/api/searchservice/indexers/create) by giving it a name and referencing the data source and target index:

    ```http
    POST https://[service name].search.windows.net/indexers?api-version=2025-09-01
    Content-Type: application/json
    api-key: [search service admin key]
    {
        "name" : "[my-sqldb-indexer]",
        "dataSourceName" : "[my-sqldb-ds]",
        "targetIndexName" : "[my-search-index]",
        "disabled": null,
        "schedule": null,
        "parameters": {
            "batchSize": null,
            "maxFailedItems": 0,
            "maxFailedItemsPerBatch": 0,
            "base64EncodeKeys": false,
            "configuration": {
                "queryTimeout": "00:04:00",
                "convertHighWaterMarkToRowVersion": false,
                "disableOrderByHighWaterMarkColumn": false
            }
        },
        "fieldMappings": [],
        "encryptionKey": null
    }
    ```

1. Under parameters, the configuration section has parameters that are specific to Azure SQL:

   + Default query timeout for SQL query execution is 5 minutes, which you can override.

   + "convertHighWaterMarkToRowVersion" optimizes for the [High Water Mark Change Detection policy](#HighWaterMarkPolicy). Change detection policies are set in the data source. If you're using the native change detection policy, this parameter has no effect.

   + "disableOrderByHighWaterMarkColumn" causes the SQL query used by the [high water mark policy](#HighWaterMarkPolicy) to omit the ORDER BY clause. If you're using the native change detection policy, this parameter has no effect.

1. [Specify field mappings](search-indexer-field-mappings.md) if there are differences in field name or type, or if you need multiple versions of a source field in the search index.

1. See [Create an indexer](search-howto-create-indexers.md) for more information about other properties.

An indexer runs automatically when it's created. You can prevent this by setting "disabled" to true. To control indexer execution, [run an indexer on demand](search-howto-run-reset-indexers.md) or [put it on a schedule](search-howto-schedule-indexers.md).

---

## Check indexer status

To monitor the indexer status and execution history, check the indexer execution history in the Azure portal, or send a [Get Indexer Status](/rest/api/searchservice/indexers/get-status) REST API request

### [**Portal**](#tab/portal-check-indexer)

1. On the search service page, open **Search management** > **Indexers**.

1. Select an indexer to access configuration and execution history.

1. Select a specific indexer job to view details, warnings, and errors.

### [**REST**](#tab/rest-check-indexer)

```http
GET https://myservice.search.windows.net/indexers/myindexer/status?api-version=2025-09-01
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

<a name="CaptureChangedRows"></a>

## Indexing new, changed, and deleted rows

If your SQL database supports [change tracking](/sql/relational-databases/track-changes/about-change-tracking-sql-server), a search indexer can pick up just the new and updated content on subsequent indexer runs. 

To enable incremental indexing, set the "dataChangeDetectionPolicy" property in your data source definition. This property tells the indexer which change tracking mechanism is used on your table or view. 

For Azure SQL indexers, there are two change detection policies: 

+ "SqlIntegratedChangeTrackingPolicy" (applies to tables only)

+ "HighWaterMarkChangeDetectionPolicy" (works for views)

### SQL integrated change tracking policy

We recommend using "SqlIntegratedChangeTrackingPolicy" for its efficiency and its ability to identify deleted rows.

Database requirements:

+ Azure SQL Database or SQL Managed Instance. SQL Server 2016 or later if you're using an Azure VM.
+ Database must have [change tracking enabled](/sql/relational-databases/track-changes/enable-and-disable-change-tracking-sql-server)
+ Tables only (no views).
+ Tables can't be clustered. To meet this requirement, drop the clustered index and recreate it as non-clustered index. This workaround often degrades performance. Duplicating content in a second table that's dedicated to indexer processing can be a helpful mitigation. 
+ Tables can't be empty. If you use TRUNCATE TABLE to clear rows, a reset and rerun of the indexer won't remove the corresponding search documents. To remove orphaned search documents, you must [index them with a delete action](search-how-to-delete-documents.md#delete-a-single-document).
+ Primary key can't be a compound key (containing more than one column).
+ Primary key must be non-clustered if you want deletion detection.

Change detection policies are added to data source definitions. To use this policy, edit the data source definition in the Azure portal, or use REST to update your data source like this:

```http
POST https://myservice.search.windows.net/datasources?api-version=2025-09-01
Content-Type: application/json
api-key: admin-key
    {
        "name" : "myazuresqldatasource",
        "type" : "azuresql",
        "credentials" : { "connectionString" : "connection string" },
        "container" : { "name" : "table name" },
        "dataChangeDetectionPolicy" : {
            "@odata.type" : "#Microsoft.Azure.Search.SqlIntegratedChangeTrackingPolicy"
        }
    }
```

When using SQL integrated change tracking policy, don't specify a separate data deletion detection policy. The SQL integrated change tracking policy has built-in support for identifying deleted rows. However, for the deleted rows to be detected automatically, the document key in your search index must be the same as the primary key in the SQL table, and the primary key must be non-clustered.

<a name="HighWaterMarkPolicy"></a>

### High water mark change detection policy

This change detection policy relies on a "high water mark" column in your table or view that captures the version or time when a row was last updated. If you're using a view, you must use a high water mark policy. 

The high water mark column must meet the following requirements:

+ All inserts specify a value for the column.
+ All updates to an item also change the value of the column.
+ The value of this column increases with each insert or update.
+ Queries with the following WHERE and ORDER BY clauses can be executed efficiently: `WHERE [High Water Mark Column] > [Current High Water Mark Value] ORDER BY [High Water Mark Column]`

> [!NOTE]
> We strongly recommend using the [rowversion](/sql/t-sql/data-types/rowversion-transact-sql) data type for the high water mark column. If any other data type is used, change tracking isn't guaranteed to capture all changes in the presence of transactions executing concurrently with an indexer query. When using **rowversion** in a configuration with read-only replicas, you must point the indexer at the primary replica. Only a primary replica can be used for data sync scenarios.

Change detection policies are added to data source definitions. To use this policy, create or update your data source like this:

```http
POST https://myservice.search.windows.net/datasources?api-version=2025-09-01
Content-Type: application/json
api-key: admin-key
    {
        "name" : "myazuresqldatasource",
        "type" : "azuresql",
        "credentials" : { "connectionString" : "connection string" },
        "container" : { "name" : "table or view name" },
        "dataChangeDetectionPolicy" : {
            "@odata.type" : "#Microsoft.Azure.Search.HighWaterMarkChangeDetectionPolicy",
            "highWaterMarkColumnName" : "[a rowversion or last_updated column name]"
        }
    }
```

> [!NOTE]
> If the source table doesn't have an index on the high water mark column, queries used by the SQL indexer may time out. In particular, the `ORDER BY [High Water Mark Column]` clause requires an index to run efficiently when the table contains many rows.

<a name="convertHighWaterMarkToRowVersion"></a>

##### convertHighWaterMarkToRowVersion

If you're using a [rowversion](/sql/t-sql/data-types/rowversion-transact-sql) data type for the high water mark column, consider setting the `convertHighWaterMarkToRowVersion` property in indexer configuration. Setting this property to true results in the following behaviors: 

+ Uses the rowversion data type for the high water mark column in the indexer SQL query. Using the correct data type improves indexer query performance.

+ Subtracts one from the rowversion value before the indexer query runs. Views with one-to-many joins might have rows with duplicate rowversion values. Subtracting one ensures the indexer query doesn't miss these rows.

To enable this property, create or update the indexer with the following configuration:

```http
    {
      ... other indexer definition properties
     "parameters" : {
            "configuration" : { "convertHighWaterMarkToRowVersion" : true } }
    }
```

<a name="queryTimeout"></a>

##### queryTimeout

If you encounter timeout errors, set the `queryTimeout` indexer configuration setting to a value higher than the default 5-minute timeout. For example, to set the timeout to 10 minutes, create or update the indexer with the following configuration:

```http
    {
      ... other indexer definition properties
     "parameters" : {
            "configuration" : { "queryTimeout" : "00:10:00" } }
    }
```

<a name="disableOrderByHighWaterMarkColumn"></a>

##### disableOrderByHighWaterMarkColumn

You can also disable the `ORDER BY [High Water Mark Column]` clause. However, this isn't recommended because if the indexer execution is interrupted by an error, the indexer has to reprocess all rows if it runs later, even if the indexer has already processed almost all the rows at the time it was interrupted. To disable the `ORDER BY` clause, use the `disableOrderByHighWaterMarkColumn` setting in the indexer definition:  

```http
    {
     ... other indexer definition properties
     "parameters" : {
            "configuration" : { "disableOrderByHighWaterMarkColumn" : true } }
    }
```

### Soft delete column deletion detection policy

When rows are deleted from the source table, you probably want to delete those rows from the search index as well. If you use the SQL integrated change tracking policy, this is taken care of for you. However, the high water mark change tracking policy doesn’t help you with deleted rows. What to do?

If the rows are physically removed from the table, Azure AI Search has no way to infer the presence of records that no longer exist. However, you can use the “soft-delete” technique to logically delete rows without removing them from the table. Add a column to your table or view and mark rows as deleted using that column.

When using the soft-delete technique, you can specify the soft delete policy as follows when creating or updating the data source:

```http
    {
        …,
        "dataDeletionDetectionPolicy" : {
           "@odata.type" : "#Microsoft.Azure.Search.SoftDeleteColumnDeletionDetectionPolicy",
           "softDeleteColumnName" : "[a column name]",
           "softDeleteMarkerValue" : "[the value that indicates that a row is deleted]"
        }
    }
```

The **softDeleteMarkerValue** must be a string in the JSON representation of your data source. Use the string representation of your actual value. For example, if you have an integer column where deleted rows are marked with the value 1, use `"1"`. If you have a BIT column where deleted rows are marked with the Boolean true value, use the string literal `"True"` or `"true"`, the case doesn't matter.

If you're setting up a soft delete policy from the Azure portal, don't add quotes around the soft delete marker value. The field contents are already understood as a string and are translated automatically into a JSON string for you. In the previous examples, simply type `1`, `True` or `true` into the Azure portal's field.

## FAQ

**Q: Can I index Always Encrypted columns?**

No, [Always Encrypted](/sql/relational-databases/security/encryption/always-encrypted-database-engine) columns aren't currently supported by Azure AI Search indexers.

**Q: Can I use Azure SQL indexer with SQL databases running on IaaS VMs in Azure?**

Yes. However, you need to allow your search service to connect to your database. For more information, see [Configure a connection from an Azure AI Search indexer to SQL Server on an Azure VM](search-how-to-index-sql-server.md).

**Q: Can I use Azure SQL indexer with SQL databases running on-premises?**

Not directly. We don't recommend or support a direct connection, as doing so would require you to open your databases to Internet traffic. Customers have succeeded with this scenario using bridge technologies like Azure Data Factory. For more information, see [Push data to an Azure AI Search index using Azure Data Factory](/azure/data-factory/connector-azure-search).

**Q: Can I use a secondary replica in a [failover cluster](/azure/azure-sql/database/auto-failover-group-overview) as a data source?**

It depends. For full indexing of a table or view, you can use a secondary replica. 

For incremental indexing, Azure AI Search supports two change detection policies: SQL integrated change tracking and High Water Mark.

On read-only replicas, SQL Database doesn't support integrated change tracking. Therefore, you must use High Water Mark policy. 

Our standard recommendation is to use the rowversion data type for the high water mark column. However, using rowversion relies on the `MIN_ACTIVE_ROWVERSION` function, which isn't supported on read-only replicas. Therefore, you must point the indexer to a primary replica if you're using rowversion.

If you attempt to use rowversion on a read-only replica, you get the following error: 

"Using a rowversion column for change tracking isn't supported on secondary (read-only) availability replicas. Update the datasource and specify a connection to the primary availability replica. Current database 'Updateability' property is 'READ_ONLY'".

**Q: Can I use an alternative, non-rowversion column for high water mark change tracking?**

It's not recommended. Only **rowversion** allows for reliable data synchronization. However, depending on your application logic, it can be safe if:

+ You can ensure that when the indexer runs, there are no outstanding transactions on the table that’s being indexed (for example, all table updates happen as a batch on a schedule, and the Azure AI Search indexer schedule is set to avoid overlapping with the table update schedule).  

+ You periodically do a full reindex to pick up any missed rows.
