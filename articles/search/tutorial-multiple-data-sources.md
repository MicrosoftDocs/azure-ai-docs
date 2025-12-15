---
title: 'C# Tutorial: Index Multiple Azure Data Sources'
titleSuffix: Azure AI Search
description: Learn how to import data from multiple data sources into a single Azure AI Search index using indexers. This tutorial and sample code are in C#.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.topic: tutorial
ms.date: 11/20/2025
ms.custom:
  - devx-track-csharp
  - devx-track-dotnet
  - ignite-2023
  - sfi-ropc-nochange
---

# Tutorial: Index from multiple data sources using the .NET SDK

Azure AI Search supports importing, analyzing, and indexing data from multiple data sources into a single consolidated search index.

This C# tutorial uses the [Azure.Search.Documents](/dotnet/api/overview/azure/search) client library in the Azure SDK for .NET to index sample hotel data from an Azure Cosmos DB instance. You then merge the data with hotel room details drawn from Azure Blob Storage documents. The result is a combined hotel search index containing hotel documents, with rooms as complex data types.

In this tutorial, you:

> [!div class="checklist"]
> * Upload sample data to data sources
> * Identify the document key
> * Define and create the index
> * Index hotel data from Azure Cosmos DB
> * Merge hotel room data from Blob Storage

## Overview

This tutorial uses [Azure.Search.Documents](/dotnet/api/overview/azure/search) to create and run multiple indexers. You upload sample data to two Azure data sources and configure an indexer that pulls from both sources to populate a single search index. The two data sets must have a value in common to support the merge. In this tutorial, that field is an ID. As long as there's a field in common to support the mapping, an indexer can merge data from disparate resources: structured data from Azure SQL, unstructured data from Blob Storage, or any combination of [supported data sources](search-indexer-overview.md#supported-data-sources) on Azure.

A finished version of the code in this tutorial can be found in the following project:

* [multiple-data-sources/v11 (GitHub)](https://github.com/Azure-Samples/azure-search-dotnet-scale/tree/main/multiple-data-sources/v11)

## Prerequisites

* An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* An [Azure Cosmos DB for NoSQL account](/azure/cosmos-db/create-cosmosdb-resources-portal).
* An [Azure Storage account](/azure/storage/common/storage-account-create).
* An [Azure AI Search service](search-create-service-portal.md).
* [Visual Studio](https://visualstudio.microsoft.com/).

> [!NOTE]
> You can use a free search service for this tutorial. The free tier limits you to three indexes, three indexers, and three data sources. This tutorial creates one of each. Before you start, make sure you have room on your service to accept the new resources.

## Prepare services

This tutorial uses Azure AI Search for indexing and queries, Azure Cosmos DB for the first data set, and Azure Blob Storage for the second data set.

If possible, create all services in the same region and resource group for proximity and manageability. In practice, your services can be in any region.

This sample uses two small sets of data describing seven fictional hotels. One set describes the hotels themselves and will be loaded into an Azure Cosmos DB database. The other set contains hotel room details and is provided as seven separate JSON files to be uploaded into Azure Blob Storage.

### Start with Azure Cosmos DB

1. Sign in to the [Azure portal](https://portal.azure.com) and select your Azure Cosmos DB account.

1. From the left pane, select **Data Explorer**.

1. Select **New Container** > **New Database**.

   :::image type="content" source="media/tutorial-multiple-data-sources/cosmos-newdb.png" alt-text="Create a new database" border="true":::

1. Enter **hotel-rooms-db** for the name. Accept the default values for the remaining settings.

   :::image type="content" source="media/tutorial-multiple-data-sources/cosmos-dbname.png" alt-text="Configure database" border="true":::

1. Create a container that targets the database you previously created. Enter **hotels** for the container name and **/HotelId** for the partition key.

   :::image type="content" source="media/tutorial-multiple-data-sources/cosmos-add-container.png" alt-text="Add container" border="true":::

1. Select **hotels** > **Items**, and then select **Upload Item** on the command bar.

1. Upload the JSON file from the `cosmosdb` folder in [multiple-data-sources/v11](https://github.com/Azure-Samples/azure-search-dotnet-scale/tree/main/multiple-data-sources/v11).

   :::image type="content" source="media/tutorial-multiple-data-sources/cosmos-upload.png" alt-text="Upload to Azure Cosmos DB collection" border="true":::

1. Use the refresh button to refresh your view of the items in the hotels collection. You should see seven new database documents listed.

1. From the left pane, select **Settings** > **Keys**.

1. Make a note of a connection string. You need this value for **appsettings.json** in a later step. If you didn't use the suggested **hotel-rooms-db** database name, copy the database name as well.

### Azure Blob Storage

1. Sign in to the [Azure portal](https://portal.azure.com) and select your Azure Storage account.

1. From the left pane, select **Data storage** > **Containers**.

1. [Create a blob container](/azure/storage/blobs/storage-quickstart-blobs-portal) named **hotel-rooms** to store the sample hotel room JSON files. You can set the access level to any valid value.

   :::image type="content" source="media/tutorial-multiple-data-sources/blob-add-container.png" alt-text="Create a blob container" border="true":::

1. Open the container, and then select **Upload** on the command bar.

1. Upload the seven JSON files from the `blob` folder in [multiple-data-sources/v11](https://github.com/Azure-Samples/azure-search-dotnet-scale/tree/main/multiple-data-sources/v11).

   :::image type="content" source="media/tutorial-multiple-data-sources/blob-upload.png" alt-text="Upload files" border="false":::

1. From the left pane, select **Security + networking** > **Access keys**.

1. Make a note of the account name and a connection string. You need both values for **appsettings.json** in a later step.

### Azure AI Search

The third component is Azure AI Search, which you can [create in the Azure portal](search-create-service-portal.md) or [find an existing search service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices) in your Azure resources.

### Copy an admin key and URL for Azure AI Search

To authenticate to your search service, you need the service URL and an access key. Having a valid key establishes trust on a per-request basis between the application sending the request and the service handling it.

1. Sign in to the [Azure portal](https://portal.azure.com) and select your search service.

1. From the left pane, select **Overview**.

1. Make a note of the URL, which should look like `https://my-service.search.windows.net`.

1. From the left pane, select **Settings** > **Keys**.

1. Make a note of an admin key for full rights on the service. There are two interchangeable admin keys, provided for business continuity in case you need to roll one over. You can use either key on requests for adding, modifying, and deleting objects.

## Set up your environment

1. Open the `AzureSearchMultipleDataSources.sln` file from [multiple-data-sources/v11](https://github.com/Azure-Samples/azure-search-dotnet-scale/tree/main/multiple-data-sources/v11) in Visual Studio.

1. In Solution Explorer, right-click the project and select **Manage NuGet Packages for Solution...**.

1. On the **Browse** tab, find and install the following packages:

    + **Azure.Search.Documents** (version 11.0 or later)

    + **Microsoft.Extensions.Configuration**

    + **Microsoft.Extensions.Configuration.Json**

1. In Solution Explorer, edit the `appsettings.json` file with the connection information you collected in the previous steps.

    ```json
    {
      "SearchServiceUri": "<YourSearchServiceURL>",
      "SearchServiceAdminApiKey": "<YourSearchServiceAdminApiKey>",
      "BlobStorageAccountName": "<YourBlobStorageAccountName>",
      "BlobStorageConnectionString": "<YourBlobStorageConnectionString>",
      "CosmosDBConnectionString": "<YourCosmosDBConnectionString>",
      "CosmosDBDatabaseName": "hotel-rooms-db"
    }
    ```

## Map key fields

Merging content requires that both data streams are targeting the same documents in the search index.

In Azure AI Search, the key field uniquely identifies each document. Every search index must have exactly one key field of type `Edm.String`. That key field must be present for each document in a data source that is added to the index. (In fact, it's the only required field.)

When indexing data from multiple data sources, make sure each incoming row or document contains a common document key. This allows you to merge data from two physically distinct source documents into a new search document in the combined index.

It often requires some up-front planning to identify a meaningful document key for your index and to make sure it exists in both data sources. In this demo, the `HotelId` key for each hotel in Azure Cosmos DB is also present in the rooms JSON blobs in Blob Storage.

Azure AI Search indexers can use field mappings to rename and even reformat data fields during the indexing process, so that source data can be directed to the correct index field. For example, in Azure Cosmos DB, the hotel identifier is called `HotelId`, but in the JSON blob files for the hotel rooms, the hotel identifier is  named `Id`. The program handles this discrepancy by mapping the `Id` field from the blobs to the `HotelId` key field in the indexer.

> [!NOTE]
> In most cases, autogenerated document keys, such as those created by default by some indexers, don't make good document keys for combined indexes. In general, use a meaningful, unique key value that already exists in your data sources or can be easily added.

## Explore the code

When the data and configuration settings are in place, the sample program in `AzureSearchMultipleDataSources.sln` should be ready to build and run.

This simple C#/.NET console app performs the following tasks:

* Creates a new index based on the data structure of the C# Hotel class, which also references the Address and Room classes.
* Creates a new data source and an indexer that maps Azure Cosmos DB data to index fields. These are both objects in Azure AI Search.
* Runs the indexer to load hotel data from Azure Cosmos DB.
* Creates a second data source and an indexer that maps JSON blob data to index fields.
* Runs the second indexer to load hotel room data from Blob Storage.

Before you run the program, take a minute to study the code, index definition, and indexer definition. The relevant code is in two files:

* `Hotel.cs` contains the schema that defines the index.
* `Program.cs` contains functions that create the Azure AI Search index, data sources, and indexers, and load the combined results into the index.

### Create an index

This sample program uses [CreateIndexAsync](/dotnet/api/azure.search.documents.indexes.searchindexclient.createindexasync) to define and create an Azure AI Search index. It takes advantage of the [FieldBuilder](/dotnet/api/azure.search.documents.indexes.fieldbuilder) class to generate an index structure from a C# data model class.

The data model is defined by the Hotel class, which also contains references to the Address and Room classes. The FieldBuilder drills down through multiple class definitions to generate a complex data structure for the index. Metadata tags are used to define the attributes of each field, such as whether it's searchable or sortable.

The program deletes any existing index of the same name before creating the new one, in case you want to run this example more than once.

The following snippets from the `Hotel.cs` file show single fields, followed by a reference to another data model class, Room[], which in turn is defined in `Room.cs` file (not shown).

```csharp
. . .
[SimpleField(IsFilterable = true, IsKey = true)]
public string HotelId { get; set; }

[SearchableField(IsFilterable = true, IsSortable = true)]
public string HotelName { get; set; }
. . .
public Room[] Rooms { get; set; }
. . .
```

In the `Program.cs` file, a [SearchIndex](/dotnet/api/azure.search.documents.indexes.models.searchindex) is defined with a name and a field collection generated by the `FieldBuilder.Build` method, and then created as follows:

```csharp
private static async Task CreateIndexAsync(string indexName, SearchIndexClient indexClient)
{
    // Create a new search index structure that matches the properties of the Hotel class.
    // The Address and Room classes are referenced from the Hotel class. The FieldBuilder
    // will enumerate these to create a complex data structure for the index.
    FieldBuilder builder = new FieldBuilder();
    var definition = new SearchIndex(indexName, builder.Build(typeof(Hotel)));

    await indexClient.CreateIndexAsync(definition);
}
```

### Create Azure Cosmos DB data source and indexer

The main program includes logic to create the Azure Cosmos DB data source for the hotels data.

First, it concatenates the Azure Cosmos DB database name to the connection string. It then defines a [SearchIndexerDataSourceConnection](/dotnet/api/azure.search.documents.indexes.models.searchindexerdatasourceconnection) object.

```csharp
private static async Task CreateAndRunCosmosDbIndexerAsync(string indexName, SearchIndexerClient indexerClient)
{
    // Append the database name to the connection string
    string cosmosConnectString =
        configuration["CosmosDBConnectionString"]
        + ";Database="
        + configuration["CosmosDBDatabaseName"];

    SearchIndexerDataSourceConnection cosmosDbDataSource = new SearchIndexerDataSourceConnection(
        name: configuration["CosmosDBDatabaseName"],
        type: SearchIndexerDataSourceType.CosmosDb,
        connectionString: cosmosConnectString,
        container: new SearchIndexerDataContainer("hotels"));

    // The Azure Cosmos DB data source does not need to be deleted if it already exists,
    // but the connection string might need to be updated if it has changed.
    await indexerClient.CreateOrUpdateDataSourceConnectionAsync(cosmosDbDataSource);
```

After the data source is created, the program sets up an Azure Cosmos DB indexer named `hotel-rooms-cosmos-indexer`.

The program updates any existing indexers with the same name, overwriting the existing indexer with the content of the previous code. It also includes reset and run actions, in case you want to run this example more than once.

The following example defines a schedule for the indexer, so that it runs once per day. You can remove the schedule property from this call if you don't want the indexer to automatically run again in the future.

```csharp
SearchIndexer cosmosDbIndexer = new SearchIndexer(
    name: "hotel-rooms-cosmos-indexer",
    dataSourceName: cosmosDbDataSource.Name,
    targetIndexName: indexName)
{
    Schedule = new IndexingSchedule(TimeSpan.FromDays(1))
};

// Indexers keep metadata about how much they have already indexed.
// If we already ran the indexer, it "remembers" and does not run again.
// To avoid this, reset the indexer if it exists.
try
{
    await indexerClient.GetIndexerAsync(cosmosDbIndexer.Name);
    // Reset the indexer if it exists.
    await indexerClient.ResetIndexerAsync(cosmosDbIndexer.Name);
}
catch (RequestFailedException ex) when (ex.Status == 404)
{
    // If the indexer does not exist, 404 will be thrown.
}

await indexerClient.CreateOrUpdateIndexerAsync(cosmosDbIndexer);

Console.WriteLine("Running Azure Cosmos DB indexer...\n");

try
{
    // Run the indexer.
    await indexerClient.RunIndexerAsync(cosmosDbIndexer.Name);
}
catch (RequestFailedException ex) when (ex.Status == 429)
{
    Console.WriteLine("Failed to run indexer: {0}", ex.Message);
}
```

This example includes a simple try-catch block to report any errors that might occur during execution.

After the Azure Cosmos DB indexer runs, the search index contains a full set of sample hotel documents. However, the rooms field for each hotel is an empty array, since the Azure Cosmos DB data source omits room details. Next, the program pulls from Blob Storage to load and merge the room data.

### Create Blob Storage data source and indexer

To get the room details, the program first sets up a Blob Storage data source to reference a set of individual JSON blob files.

```csharp
private static async Task CreateAndRunBlobIndexerAsync(string indexName, SearchIndexerClient indexerClient)
{
    SearchIndexerDataSourceConnection blobDataSource = new SearchIndexerDataSourceConnection(
        name: configuration["BlobStorageAccountName"],
        type: SearchIndexerDataSourceType.AzureBlob,
        connectionString: configuration["BlobStorageConnectionString"],
        container: new SearchIndexerDataContainer("hotel-rooms"));

    // The blob data source does not need to be deleted if it already exists,
    // but the connection string might need to be updated if it has changed.
    await indexerClient.CreateOrUpdateDataSourceConnectionAsync(blobDataSource);
```

After the data source is created, the program sets up a blob indexer named `hotel-rooms-blob-indexer`, as shown below.

The JSON blobs contain a key field named **`Id`** instead of **`HotelId`**. The code uses the `FieldMapping` class to tell the indexer to direct the **`Id`** field value to the **`HotelId`** document key in the index.

Blob Storage indexers can use [IndexingParameters](/dotnet/api/azure.search.documents.indexes.models.indexingparameters) to specify a parsing mode. You should set different parsing modes depending on whether blobs represent a single document or multiple documents within the same blob. In this example, each blob represents a single JSON document, so the code uses the `json` parsing mode. For more information about indexer parsing parameters for JSON blobs, see [Index JSON blobs](search-how-to-index-azure-blob-json.md).

This example defines a schedule for the indexer, so that it runs once per day. You can remove the schedule property from this call if you don't want the indexer to automatically run again in the future.

```csharp
IndexingParameters parameters = new IndexingParameters();
parameters.Configuration.Add("parsingMode", "json");

SearchIndexer blobIndexer = new SearchIndexer(
    name: "hotel-rooms-blob-indexer",
    dataSourceName: blobDataSource.Name,
    targetIndexName: indexName)
{
    Parameters = parameters,
    Schedule = new IndexingSchedule(TimeSpan.FromDays(1))
};

// Map the Id field in the Room documents to the HotelId key field in the index
blobIndexer.FieldMappings.Add(new FieldMapping("Id") { TargetFieldName = "HotelId" });

// Reset the indexer if it already exists
try
{
    await indexerClient.GetIndexerAsync(blobIndexer.Name);
    await indexerClient.ResetIndexerAsync(blobIndexer.Name);
}
catch (RequestFailedException ex) when (ex.Status == 404) { }

await indexerClient.CreateOrUpdateIndexerAsync(blobIndexer);

try
{
    // Run the indexer.
    await searchService.Indexers.RunAsync(blobIndexer.Name);
}
catch (CloudException e) when (e.Response.StatusCode == (HttpStatusCode)429)
{
    Console.WriteLine("Failed to run indexer: {0}", e.Response.Content);
}
```

Because the index is already populated with hotel data from the Azure Cosmos DB database, the blob indexer updates the existing documents in the index and adds the room details.

> [!NOTE]
> If you have the same non-key fields in both of your data sources, and the data in those fields doesn't match, the index contains the values from whichever indexer ran most recently. In our example, both data sources contain a `HotelName` field. If for some reason the data in this field is different, for documents with the same key value, the `HotelName` data from the most recently indexed data source is the value stored in the index.

## Search

After you run the program, you can explore the populated search index using [**Search explorer**](search-explorer.md) in the Azure portal.

1. Sign in to the [Azure portal](https://portal.azure.com) and select your search service.

1. From the left pane, select **Search management** > **Indexes**.

1. Select **hotel-rooms-sample** from the list of indexes.

1. On the **Search explorer** tab, enter a query for a term like `Luxury`.

   You should see at least one document in the results. This document should contain a list of room objects in its `Rooms` array.

## Reset and rerun

In the early experimental stages of development, the most practical approach for design iteration is to delete the objects from Azure AI Search and allow your code to rebuild them. Resource names are unique. Deleting an object lets you recreate it using the same name.

The sample code checks for existing objects and deletes or updates them so that you can rerun the program. You can also use the Azure portal to delete indexes, indexers, and data sources.

## Clean up resources

When you're working in your own subscription, at the end of a project, it's a good idea to remove the resources you no longer need. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

You can find and manage resources in the Azure portal using the All resources or Resource groups link in the left pane.

## Next step

Now that you're familiar with ingesting data from multiple sources, take a closer look at indexer configuration, starting with Azure Cosmos DB:

> [!div class="nextstepaction"]
> [Configure an Azure Cosmos DB for NoSQL indexer](search-how-to-index-cosmosdb-sql.md)
