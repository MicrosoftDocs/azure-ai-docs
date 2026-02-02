---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 02/02/2026
---

In this quickstart, you use the [Azure AI Search client library for JavaScript](/javascript/api/overview/azure/search-documents-readme) to create, load, and query a search index for [full-text search](../../search-lucene-query-architecture.md), also known as keyword search.

Full-text search uses Apache Lucene for indexing and queries and the BM25 ranking algorithm for scoring results. This quickstart uses fictional hotel data from the [azure-search-sample-data](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/hotels/hotel-json-documents) GitHub repository to populate the index.

> [!TIP]
> Want to get started right away? Download the [source code](https://github.com/Azure-Samples/azure-search-javascript-samples/tree/main/quickstart-keyword-search) on GitHub.

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

- An [Azure AI Search service](../../search-create-service-portal.md). You can use a free service for this quickstart.

- The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

- [Visual Studio Code](https://code.visualstudio.com/download) and the latest LTS version of [Node.js](https://nodejs.org/en/download/).

- [Git](https://git-scm.com/downloads) to clone the sample repository.

## Configure access

[!INCLUDE [resource authentication](../resource-authentication.md)]

## Get endpoint

[!INCLUDE [resource endpoint](../resource-endpoint.md)]

## Set up the environment

1. Use Git to clone the sample repository.

   ```console
   git clone https://github.com/Azure-Samples/azure-search-javascript-samples
   ```

1. Open the `azure-search-javascript-samples/quickstart-keyword-search` folder in Visual Studio Code.

1. Rename the `sample.env` file to `.env`, and then open the file.

1. Replace the placeholder value for `SEARCH_API_ENDPOINT` with the URL you obtained in [Get endpoint](#get-endpoint).

1. Install the dependencies from the `package.json` file.

    ```console
    npm install
    ```

1. For keyless authentication with Microsoft Entra ID, sign in to your Azure account. If you have multiple subscriptions, select the one that contains your Azure AI Search service.

    ```azurecli
    az login
    ```

## Run the code

Run the following command to run the application.

```console
node index.js
```

### Output

The output should be similar to the following:

```
Running Azure AI Search Javascript quickstart...
Checking if index exists...
Deleting index...
Creating index...
Index named hotels-quickstart-js has been created.
Uploading documents...
Index operations succeeded: true 
Querying the index...

Query #1 - search everything:
{"HotelId":"3","HotelName":"Gastronomic Landscape Hotel","Rating":4.8}
{"HotelId":"2","HotelName":"Old Century Hotel","Rating":3.6}
{"HotelId":"4","HotelName":"Sublime Palace Hotel","Rating":4.6}
{"HotelId":"1","HotelName":"Stay-Kay City Hotel","Rating":3.6}
Result count: 4

Query #2 - search with filter, orderBy, and select:
{"HotelId":"2","HotelName":"Old Century Hotel","Rating":3.6}

Query #3 - limit searchFields:
{"HotelId":"4","HotelName":"Sublime Palace Hotel","Rating":4.6}

Query #4 - limit searchFields and use facets:
{"HotelId":"3","HotelName":"Gastronomic Landscape Hotel","Rating":4.8}
{"HotelId":"2","HotelName":"Old Century Hotel","Rating":3.6}
{"HotelId":"4","HotelName":"Sublime Palace Hotel","Rating":4.6}
{"HotelId":"1","HotelName":"Stay-Kay City Hotel","Rating":3.6}

Query #5 - Lookup document:
HotelId: 3; HotelName: Gastronomic Landscape Hotel
```

## Understand the code

Now that you've run the code, let's break down the key steps:

1. [Create a search index](#create-a-search-index)
1. [Upload documents to the index](#upload-documents-to-the-index)
1. [Query the index](#query-the-index)

### Create a search index

The *hotels_quickstart_index.json* file defines how Azure AI Search works with the documents you load in the next step. Each field is identified by a `name` and has a specified `type`. Each field also has a series of index attributes that specify whether Azure AI Search can search, filter, sort, and facet upon the field. Most of the fields are simple data types, but some, like `AddressType` are complex types that allow you to create rich data structures in your index. You can read more about [supported data types](/rest/api/searchservice/supported-data-types) and index attributes described in [Create Index (REST)](/rest/api/searchservice/indexes/create). 

With our index definition in place, we want to import `hotels_quickstart_index.json` at the top of `index.js` so the main function can access the index definition.

```javascript
const indexDefinition = require('./hotels_quickstart_index.json');
```

Within the main function, we then create a `SearchIndexClient`, which is used to create and manage indexes for Azure AI Search. 

```javascript
const credential = new DefaultAzureCredential();
const searchIndexClient = new SearchIndexClient(searchServiceEndpoint, credential);
```

Next, we want to delete the index if it already exists. This operation is a common practice for test/demo code.

We do this by defining a simple function that tries to delete the index.

```javascript
async function deleteIndexIfExists(indexClient, indexName) {
    try {
        await indexClient.deleteIndex(indexName);
        console.log('Deleting index...');
    } catch {
        console.log('Index does not exist yet.');
    }
}
```

To run the function, we extract the index name from the index definition and pass the `indexName` along with the `indexClient` to the `deleteIndexIfExists()` function.

```javascript
const indexName = indexDefinition["name"];

console.log('Checking if index exists...');
await deleteIndexIfExists(indexClient, indexName);
```

After that, we're ready to create the index with the `createIndex()` method.

```javascript
console.log('Creating index...');
let index = await indexClient.createIndex(indexDefinition);

console.log(`Index named ${index.name} has been created.`);
```

### Upload documents to the index

In Azure AI Search, documents are data structures that are both inputs to indexing and outputs from queries. You can push such data to the index or use an [indexer](/azure/search/search-indexer-overview). In this case, we'll programmatically push the documents to the index.

Document inputs might be rows in a database, blobs in Blob storage, or, as in this sample, JSON documents on disk. Similar to what we did with the `indexDefinition`, we also need to import `hotels.json` at the top of `index.js` so that the data can be accessed in our main function.

```javascript
const hotelData = require('./hotels.json');
```

To index data into the search index, we now need to create a `SearchClient`. While the `SearchIndexClient` is used to create and manage an index, the `SearchClient` is used to upload documents and query the index.

You can use the `getSearchClient()` method of the `SearchIndexClient` to create the `SearchClient`:

```javascript
const searchClient = searchIndexClient.getSearchClient(indexName);
```

Now that the client is defined, upload the documents into the search index. In this case, we use the `mergeOrUploadDocuments()` method, which uploads the documents or merges them with an existing document if a document with the same key already exists.

```javascript
console.log('Uploading documents...');
let indexDocumentsResult = await searchClient.mergeOrUploadDocuments(hotelData['value']);

console.log(`Index operations succeeded: ${JSON.stringify(indexDocumentsResult.results[0].succeeded)}`);
```

### Query the index

With an index created and documents uploaded, you're ready to send queries to the index. In this section, we send five different queries to the search index to demonstrate different pieces of query functionality available to you.

The queries are written in a `sendQueries()` function that we call in the main function as follows:

```javascript
await sendQueries(searchClient);
```

Queries are sent using the `search()` method of `searchClient`. The first parameter is the search text and the second parameter specifies search options.

#### Query example 1

The first query searches `*`, which is equivalent to searching everything and selects three of the fields in the index. It's a best practice to only `select` the fields you need because pulling back unnecessary data can add latency to your queries.

The `searchOptions` for this query also has `includeTotalCount` set to `true`, which returns the number of matching results found.

```javascript
async function sendQueries(searchClient) {
    console.log('Query #1 - search everything:');
    let searchOptions = {
        includeTotalCount: true,
        select: ["HotelId", "HotelName", "Rating"]
    };

    let searchResults = await searchClient.search("*", searchOptions);
    for await (const result of searchResults.results) {
        console.log(`${JSON.stringify(result.document)}`);
    }
    console.log(`Result count: ${searchResults.count}`);

    // remaining queries go here
}
```

The remaining queries outlined below should also be added to the `sendQueries()` function. They're separated here for readability.

#### Query example 2

In the next query, we specify the search term `"wifi"` and also include a filter to only return results where the state is equal to `'FL'`. Results are also ordered by the Hotel's `Rating`.

```javascript
console.log('Query #2 - Search with filter, orderBy, and select:');
let state = 'FL';
searchOptions = {
    filter: odata`Address/StateProvince eq ${state}`,
    orderBy: ["Rating desc"],
    select: ["HotelId", "HotelName", "Rating"]
};

searchResults = await searchClient.search("wifi", searchOptions);
for await (const result of searchResults.results) {
    console.log(`${JSON.stringify(result.document)}`);
}
```

#### Query example 3

Next, the search is limited to a single searchable field using the `searchFields` parameter. This approach is a great option to make your query more efficient if you know you're only interested in matches in certain fields. 

```javascript
console.log('Query #3 - Limit searchFields:');
searchOptions = {
    select: ["HotelId", "HotelName", "Rating"],
    searchFields: ["HotelName"]
};

searchResults = await searchClient.search("Sublime Palace", searchOptions);
for await (const result of searchResults.results) {
    console.log(`${JSON.stringify(result.document)}`);
}
console.log();
```


#### Query example 4

Another common option to include in a query is `facets`. Facets allow you to build out filters on your UI to make it easy for users to know what values they can filter down to.

```javascript
console.log('Query #4 - Use facets:');
searchOptions = {
    facets: ["Category"],
    select: ["HotelId", "HotelName", "Rating"],
    searchFields: ["HotelName"]
};

searchResults = await searchClient.search("*", searchOptions);
for await (const result of searchResults.results) {
    console.log(`${JSON.stringify(result.document)}`);
}
```

#### Query example 5

The final query uses the `getDocument()` method of the `searchClient`. This allows you to efficiently retrieve a document by its key. 

```javascript
console.log('Query #5 - Lookup document:');
let documentResult = await searchClient.getDocument(key='3')
console.log(`HotelId: ${documentResult.HotelId}; HotelName: ${documentResult.HotelName}`)
```

#### Summary of queries

The previous queries show multiple ways of matching terms in a query: full-text search, filters, and autocomplete.

Full text search and filters are performed using the `searchClient.search` method. A search query can be passed in the `searchText` string, while a filter expression can be passed in the `filter` property of the `SearchOptions` class. To filter without searching, just pass "*" for the `searchText` parameter of the `search` method. To search without filtering, leave the `filter` property unset, or don't pass in a `SearchOptions` instance at all.
