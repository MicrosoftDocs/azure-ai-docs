---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 02/02/2026
---

In this quickstart, you use the [Azure AI Search client library for JavaScript](/javascript/api/overview/azure/search-documents-readme) (compatible with TypeScript) to create, load, and query a search index for [full-text search](../../search-lucene-query-architecture.md), also known as keyword search.

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

1. Install the dependencies and initialize the project for TypeScript.

    ```console
    npm install
    npm install typescript @types/node --save-dev
    npm pkg set type=module
    ```

1. For keyless authentication with Microsoft Entra ID, sign in to your Azure account. If you have multiple subscriptions, select the one that contains your Azure AI Search service.

    ```azurecli
    az login
    ```

## Run the code

1. Create a file named `tsconfig.json`, and then paste the following code into it.

    ```json
    {
      "compilerOptions": {
        "module": "NodeNext",
        "target": "ES2022",
        "moduleResolution": "NodeNext",
        "skipLibCheck": true,
        "strict": true,
        "resolveJsonModule": true
      },
      "include": ["*.ts"],
      "exclude": ["node_modules"]
    }
    ```

1. Rename the `index.ts` file to `index.ts`, and then replace the contents with the following code. This code converts the CommonJS syntax to ES module imports, which are required for TypeScript compilation.

    ```typescript
    // Import from the @azure/search-documents library
    import {
        SearchIndexClient,
        SearchClient,
        SearchFieldDataType,
        odata,
        SearchIndex
    } from "@azure/search-documents";
    
    // Import from the Azure Identity library
    import { DefaultAzureCredential } from "@azure/identity";
    
    // Importing the hotels sample data
    import hotelData from './hotels.json' with { type: "json" };
    
    // Load the .env file if it exists
    import "dotenv/config";
    
    // Defining the index definition
    const indexDefinition: SearchIndex = {
    	"name": "hotels-quickstart",
    	"fields": [
    		{
    			"name": "HotelId",
    			"type": "Edm.String" as SearchFieldDataType,
    			"key": true,
    			"filterable": true
    		},
    		{
    			"name": "HotelName",
    			"type": "Edm.String" as SearchFieldDataType,
    			"searchable": true,
    			"filterable": false,
    			"sortable": true,
    			"facetable": false
    		},
    		{
    			"name": "Description",
    			"type": "Edm.String" as SearchFieldDataType,
    			"searchable": true,
    			"filterable": false,
    			"sortable": false,
    			"facetable": false,
    			"analyzerName": "en.lucene"
    		},
    		{
    			"name": "Category",
    			"type": "Edm.String" as SearchFieldDataType,
    			"searchable": true,
    			"filterable": true,
    			"sortable": true,
    			"facetable": true
    		},
    		{
    			"name": "Tags",
    			"type": "Collection(Edm.String)",
    			"searchable": true,
    			"filterable": true,
    			"sortable": false,
    			"facetable": true
    		},
    		{
    			"name": "ParkingIncluded",
    			"type": "Edm.Boolean",
    			"filterable": true,
    			"sortable": true,
    			"facetable": true
    		},
    		{
    			"name": "LastRenovationDate",
    			"type": "Edm.DateTimeOffset",
    			"filterable": true,
    			"sortable": true,
    			"facetable": true
    		},
    		{
    			"name": "Rating",
    			"type": "Edm.Double",
    			"filterable": true,
    			"sortable": true,
    			"facetable": true
    		},
    		{
    			"name": "Address",
    			"type": "Edm.ComplexType",
    			"fields": [
    				{
    					"name": "StreetAddress",
    					"type": "Edm.String" as SearchFieldDataType,
    					"filterable": false,
    					"sortable": false,
    					"facetable": false,
    					"searchable": true
    				},
    				{
    					"name": "City",
    					"type": "Edm.String" as SearchFieldDataType,
    					"searchable": true,
    					"filterable": true,
    					"sortable": true,
    					"facetable": true
    				},
    				{
    					"name": "StateProvince",
    					"type": "Edm.String" as SearchFieldDataType,
    					"searchable": true,
    					"filterable": true,
    					"sortable": true,
    					"facetable": true
    				},
    				{
    					"name": "PostalCode",
    					"type": "Edm.String" as SearchFieldDataType,
    					"searchable": true,
    					"filterable": true,
    					"sortable": true,
    					"facetable": true
    				},
    				{
    					"name": "Country",
    					"type": "Edm.String" as SearchFieldDataType,
    					"searchable": true,
    					"filterable": true,
    					"sortable": true,
    					"facetable": true
    				}
    			]
    		}
    	],
    	"suggesters": [
    		{
    			"name": "sg",
    			"searchMode": "analyzingInfixMatching",
    			"sourceFields": [
    				"HotelName"
    			]
    		}
    	]
    };
    
    async function main() {
    
    	// Your search service endpoint (from .env file)
    	const searchServiceEndpoint = process.env.SEARCH_API_ENDPOINT || "";
    
    	// Use the recommended keyless credential instead of the AzureKeyCredential credential.
    	const credential = new DefaultAzureCredential();
    	//const credential = new AzureKeyCredential(Your search service admin key);
    
    	// Create a SearchIndexClient to send create/delete index commands
    	const searchIndexClient: SearchIndexClient = new SearchIndexClient(
    		searchServiceEndpoint,
    		credential
    	);
    
    	// Creating a search client to upload documents and issue queries
    	const indexName: string  = "hotels-quickstart";
        const searchClient: SearchClient<any> = searchIndexClient.getSearchClient(indexName);
    
        console.log('Checking if index exists...');
        await deleteIndexIfExists(searchIndexClient, indexName);
    
        console.log('Creating index...');
        let index: SearchIndex = await searchIndexClient.createIndex(indexDefinition);
        console.log(`Index named ${index.name} has been created.`);
    
        console.log('Uploading documents...');
        let indexDocumentsResult = await searchClient.mergeOrUploadDocuments(hotelData['value']);
        console.log(`Index operations succeeded: ${JSON.stringify(indexDocumentsResult.results[0].succeeded)} `);
    
        // waiting one second for indexing to complete (for demo purposes only)
        sleep(1000);
    
        console.log('Querying the index...');
        console.log();
        await sendQueries(searchClient);
    }
    
    async function deleteIndexIfExists(searchIndexClient: SearchIndexClient, indexName: string) {
        try {
            await searchIndexClient.deleteIndex(indexName);
            console.log('Deleting index...');
        } catch {
            console.log('Index does not exist yet.');
        }
    }
    
    async function sendQueries(searchClient: SearchClient<any>) {
        // Query 1
        console.log('Query #1 - search everything:');
        let searchOptions: any = {
            includeTotalCount: true,
            select: ["HotelId", "HotelName", "Rating"]
        };
    
        let searchResults = await searchClient.search("*", searchOptions);
        for await (const result of searchResults.results) {
            console.log(`${JSON.stringify(result.document)}`);
        }
        console.log(`Result count: ${searchResults.count}`);
        console.log();
    
    
        // Query 2
        console.log('Query #2 - search with filter, orderBy, and select:');
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
        console.log();
    
        // Query 3
        console.log('Query #3 - limit searchFields:');
        searchOptions = {
            select: ["HotelId", "HotelName", "Rating"],
            searchFields: ["HotelName"]
        };
    
        searchResults = await searchClient.search("sublime palace", searchOptions);
        for await (const result of searchResults.results) {
            console.log(`${JSON.stringify(result.document)}`);
        }
        console.log();
    
        // Query 4
        console.log('Query #4 - limit searchFields and use facets:');
        searchOptions = {
            facets: ["Category"],
            select: ["HotelId", "HotelName", "Rating"],
            searchFields: ["HotelName"]
        };
    
        searchResults = await searchClient.search("*", searchOptions);
        for await (const result of searchResults.results) {
            console.log(`${JSON.stringify(result.document)}`);
        }
        console.log();
    
        // Query 5
        console.log('Query #5 - Lookup document:');
        let documentResult = await searchClient.getDocument('3');
        console.log(`HotelId: ${documentResult.HotelId}; HotelName: ${documentResult.HotelName}`);
        console.log();
    }
    
    function sleep(ms: number) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    main().catch((err) => {
        console.error("The sample encountered an error:", err);
    });
    ```

1. Run the following command to transpile from TypeScript to JavaScript.

    ```console
    npx tsc
    ```

1. Run the application.

    ```console
    node index.js
    ```

### Output

Output includes query information and results.

## Understand the code

### Create the index

The `indexDefinition` object defines how Azure AI Search works with the documents you load in the next step. Each field is identified by a `name` and has a specified `type`. Each field also has a series of index attributes that specify whether Azure AI Search can search, filter, sort, and facet upon the field. Most of the fields are simple data types, but some, like `Address` are complex types that allow you to create rich data structures in your index. You can read more about [supported data types](/rest/api/searchservice/supported-data-types) and index attributes described in [Create Index (REST)](/rest/api/searchservice/indexes/create).

```typescript
const indexDefinition: SearchIndex = {
    "name": "hotels-quickstart",
    "fields": [
        {
            "name": "HotelId",
            "type": "Edm.String" as SearchFieldDataType,
            "key": true,
            "filterable": true
        },
        {
            "name": "HotelName",
            "type": "Edm.String" as SearchFieldDataType,
            "searchable": true,
            "filterable": false,
            "sortable": true,
            "facetable": false
        },
        // ... more fields
    ],
    "suggesters": [
        {
            "name": "sg",
            "searchMode": "analyzingInfixMatching",
            "sourceFields": ["HotelName"]
        }
    ]
};
```

Within the main function, a `SearchIndexClient` is created, which is used to create and manage indexes for Azure AI Search.

```typescript
const credential = new DefaultAzureCredential();
const searchIndexClient: SearchIndexClient = new SearchIndexClient(
    searchServiceEndpoint,
    credential
);
```

Next, the index is deleted if it already exists. This operation is a common practice for test/demo code.

```typescript
async function deleteIndexIfExists(searchIndexClient: SearchIndexClient, indexName: string) {
    try {
        await searchIndexClient.deleteIndex(indexName);
        console.log('Deleting index...');
    } catch {
        console.log('Index does not exist yet.');
    }
}
```

After that, the index is created with the `createIndex()` method.

```typescript
let index: SearchIndex = await searchIndexClient.createIndex(indexDefinition);
```

### Upload documents

In Azure AI Search, documents are data structures that are both inputs to indexing and outputs from queries. You can push such data to the index or use an [indexer](/azure/search/search-indexer-overview). In this case, the documents are programmatically pushed to the index.

Document inputs might be rows in a database, blobs in Azure Blob Storage, or JSON documents on disk, as in this quickstart. The hotel data is imported at the top of the file:

```typescript
import hotelData from './hotels.json' with { type: "json" };
```

To index data into the search index, a `SearchClient` is created. While the `SearchIndexClient` is used to create and manage an index, the `SearchClient` is used to upload documents and query the index.

```typescript
const searchClient: SearchClient<any> = searchIndexClient.getSearchClient(indexName);
```

The `mergeOrUploadDocuments()` method uploads the documents or merges them with an existing document if a document with the same key already exists.

```typescript
let indexDocumentsResult = await searchClient.mergeOrUploadDocuments(hotelData['value']);
```

Before running the queries, a `sleep` function has the program wait for one second. This is done just for test/demo purposes to ensure the indexing finishes and that the documents are available in the index for queries.

```typescript
function sleep(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
```

### Query the index

With an index created and documents uploaded, you're ready to send queries to the index. In this section, five different queries are sent to the search index to demonstrate different pieces of query functionality available to you.

The queries are written in a `sendQueries()` function that is called in the main function:

```typescript
await sendQueries(searchClient);
```

Queries are sent using the `search()` method of `searchClient`. The first parameter is the search text and the second parameter specifies search options.

#### Query example 1

The first query searches `*`, which is equivalent to searching everything, and selects three of the fields in the index. It's a best practice to only `select` the fields you need because pulling back unnecessary data can add latency to your queries.

The `searchOptions` for this query also has `includeTotalCount` set to `true`, which returns the number of matching results found.

```typescript
console.log('Query #1 - search everything:');
let searchOptions: any = {
    includeTotalCount: true,
    select: ["HotelId", "HotelName", "Rating"]
};

let searchResults = await searchClient.search("*", searchOptions);
for await (const result of searchResults.results) {
    console.log(`${JSON.stringify(result.document)}`);
}
console.log(`Result count: ${searchResults.count}`);
```

#### Query example 2

In the next query, the search term `"wifi"` is specified with a filter to only return results where the state is equal to `'FL'`. Results are also ordered by the Hotel's `Rating`.

```typescript
console.log('Query #2 - search with filter, orderBy, and select:');
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

The search is limited to a single searchable field using the `searchFields` parameter. This approach is a great option to make your query more efficient if you know you're only interested in matches in certain fields.

```typescript
console.log('Query #3 - limit searchFields:');
searchOptions = {
    select: ["HotelId", "HotelName", "Rating"],
    searchFields: ["HotelName"]
};

searchResults = await searchClient.search("sublime palace", searchOptions);
for await (const result of searchResults.results) {
    console.log(`${JSON.stringify(result.document)}`);
}
```

#### Query example 4

Another common option to include in a query is `facets`. Facets allow you to provide self-directed drilldown from the results in your UI. The facets results can be turned into checkboxes in the result pane.

```typescript
console.log('Query #4 - limit searchFields and use facets:');
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

```typescript
console.log('Query #5 - Lookup document:');
let documentResult = await searchClient.getDocument('3');
console.log(`HotelId: ${documentResult.HotelId}; HotelName: ${documentResult.HotelName}`);
```

#### Summary of queries

The previous queries show multiple ways of matching terms in a query: full-text search, filters, and autocomplete.

Full-text search and filters are performed using the `searchClient.search` method. A search query can be passed in the `searchText` string, while a filter expression can be passed in the `filter` property of the `SearchOptions` class. To filter without searching, just pass `*` for the `searchText` parameter of the `search` method. To search without filtering, leave the `filter` property unset, or don't pass in a `SearchOptions` instance at all.
