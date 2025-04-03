---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 03/04/2025
---

[!INCLUDE [Full text introduction](full-text-intro.md)]

> [!TIP]
> You can [download the source code](https://github.com/Azure-Samples/azure-search-javascript-samples/tree/main/quickstart) to start with a finished project or follow these steps to create your own.

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).
- An Azure AI Search service. [Create a service](../../search-create-service-portal.md) if you don't have one. For this quickstart, you can use a free service.

## Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign both of the `Search Service Contributor` and `Search Index Data Contributor` roles to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**. For more information, see [Connect to Azure AI Search using roles](../../search-security-rbac.md).

## Retrieve resource information

[!INCLUDE [resource authentication](../resource-authentication.md)]

## Set up

1. Create a new folder `full-text-quickstart` to contain the application and open Visual Studio Code in that folder with the following command:

    ```shell
    mkdir full-text-quickstart && cd full-text-quickstart
    ```

1. Create the `package.json` with the following command:

    ```shell
    npm init -y
    ```

1. Install the Azure AI Search client library ([Azure.Search.Documents](/javascript/api/overview/azure/search-documents-readme)) for JavaScript with:

    ```console
    npm install @azure/search-documents
    ```

1. For the **recommended** passwordless authentication, install the Azure Identity client library with:

    ```console
    npm install @azure/identity
    ```



## Create, load, and query a search index

In the prior [set up](#set-up) section, you installed the Azure AI Search client library and other dependencies. 

In this section, you add code to create a search index, load it with documents, and run queries. You run the program to see the results in the console. For a detailed explanation of the code, see the [explaining the code](#explaining-the-code) section.

The sample code in this quickstart uses Microsoft Entra ID for the recommended keyless authentication. If you prefer to use an API key, you can replace the `DefaultAzureCredential` object with a `AzureKeyCredential` object. 

#### [Microsoft Entra ID](#tab/keyless)

```java
String searchServiceEndpoint = "https://<Put your search service NAME here>.search.windows.net/";
DefaultAzureCredential credential = new DefaultAzureCredentialBuilder().build();
```

#### [API key](#tab/api-key)

```java
String searchServiceEndpoint = "https://<Put your search service NAME here>.search.windows.net/";
AzureKeyCredential credential = new AzureKeyCredential("<Your search service admin key>");
```
---

1. Create a new file named *index.js* and paste the following code into *index.js*:

    ```javascript
    // Import from the @azure/search-documents library
    import { SearchIndexClient, odata } from "@azure/search-documents";
    // Import from the Azure Identity library
    import { DefaultAzureCredential } from "@azure/identity";
    // Importing the hotels sample data
    import hotelData from './hotels.json' assert { type: "json" };
    // Load the .env file if it exists
    import * as dotenv from "dotenv";
    dotenv.config();
    // Defining the index definition
    const indexDefinition = {
        "name": "hotels-quickstart",
        "fields": [
            {
                "name": "HotelId",
                "type": "Edm.String",
                "key": true,
                "filterable": true
            },
            {
                "name": "HotelName",
                "type": "Edm.String",
                "searchable": true,
                "filterable": false,
                "sortable": true,
                "facetable": false
            },
            {
                "name": "Description",
                "type": "Edm.String",
                "searchable": true,
                "filterable": false,
                "sortable": false,
                "facetable": false,
                "analyzerName": "en.lucene"
            },
            {
                "name": "Description_fr",
                "type": "Edm.String",
                "searchable": true,
                "filterable": false,
                "sortable": false,
                "facetable": false,
                "analyzerName": "fr.lucene"
            },
            {
                "name": "Category",
                "type": "Edm.String",
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
                        "type": "Edm.String",
                        "filterable": false,
                        "sortable": false,
                        "facetable": false,
                        "searchable": true
                    },
                    {
                        "name": "City",
                        "type": "Edm.String",
                        "searchable": true,
                        "filterable": true,
                        "sortable": true,
                        "facetable": true
                    },
                    {
                        "name": "StateProvince",
                        "type": "Edm.String",
                        "searchable": true,
                        "filterable": true,
                        "sortable": true,
                        "facetable": true
                    },
                    {
                        "name": "PostalCode",
                        "type": "Edm.String",
                        "searchable": true,
                        "filterable": true,
                        "sortable": true,
                        "facetable": true
                    },
                    {
                        "name": "Country",
                        "type": "Edm.String",
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
        // Your search service endpoint
        const searchServiceEndpoint = "https://<Put your search service NAME here>.search.windows.net/";
        // Use the recommended keyless credential instead of the AzureKeyCredential credential.
        const credential = new DefaultAzureCredential();
        //const credential = new AzureKeyCredential(Your search service admin key);
        // Create a SearchIndexClient to send create/delete index commands
        const searchIndexClient = new SearchIndexClient(searchServiceEndpoint, credential);
        // Creating a search client to upload documents and issue queries
        const indexName = "hotels-quickstart";
        const searchClient = searchIndexClient.getSearchClient(indexName);
        console.log('Checking if index exists...');
        await deleteIndexIfExists(searchIndexClient, indexName);
        console.log('Creating index...');
        let index = await searchIndexClient.createIndex(indexDefinition);
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
    async function deleteIndexIfExists(searchIndexClient, indexName) {
        try {
            await searchIndexClient.deleteIndex(indexName);
            console.log('Deleting index...');
        }
        catch {
            console.log('Index does not exist yet.');
        }
    }
    async function sendQueries(searchClient) {
        // Query 1
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
        console.log();
        // Query 2
        console.log('Query #2 - search with filter, orderBy, and select:');
        let state = 'FL';
        searchOptions = {
            filter: odata `Address/StateProvince eq ${state}`,
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
        searchResults = await searchClient.search("sublime cliff", searchOptions);
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
    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    main().catch((err) => {
        console.error("The sample encountered an error:", err);
    });
    ```

1. Create a file named *hotels.json* and paste the following code into *hotels.json*:

    ```json
    {
        "value": [
            {
                "HotelId": "1",
                "HotelName": "Secret Point Motel",
                "Description": "The hotel is ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Time's Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.",
                "Description_fr": "L'hôtel est idéalement situé sur la principale artère commerciale de la ville en plein cœur de New York. A quelques minutes se trouve la place du temps et le centre historique de la ville, ainsi que d'autres lieux d'intérêt qui font de New York l'une des villes les plus attractives et cosmopolites de l'Amérique.",
                "Category": "Boutique",
                "Tags": ["pool", "air conditioning", "concierge"],
                "ParkingIncluded": false,
                "LastRenovationDate": "1970-01-18T00:00:00Z",
                "Rating": 3.6,
                "Address": {
                    "StreetAddress": "677 5th Ave",
                    "City": "New York",
                    "StateProvince": "NY",
                    "PostalCode": "10022"
                }
            },
            {
                "HotelId": "2",
                "HotelName": "Twin Dome Motel",
                "Description": "The hotel is situated in a  nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts.",
                "Description_fr": "L'hôtel est situé dans une place du XIXe siècle, qui a été agrandie et rénovée aux plus hautes normes architecturales pour créer un hôtel moderne, fonctionnel et de première classe dans lequel l'art et les éléments historiques uniques coexistent avec le confort le plus moderne.",
                "Category": "Boutique",
                "Tags": ["pool", "free wifi", "concierge"],
                "ParkingIncluded": "false",
                "LastRenovationDate": "1979-02-18T00:00:00Z",
                "Rating": 3.6,
                "Address": {
                    "StreetAddress": "140 University Town Center Dr",
                    "City": "Sarasota",
                    "StateProvince": "FL",
                    "PostalCode": "34243"
                }
            },
            {
                "HotelId": "3",
                "HotelName": "Triple Landscape Hotel",
                "Description": "The Hotel stands out for its gastronomic excellence under the management of William Dough, who advises on and oversees all of the Hotel’s restaurant services.",
                "Description_fr": "L'hôtel est situé dans une place du XIXe siècle, qui a été agrandie et rénovée aux plus hautes normes architecturales pour créer un hôtel moderne, fonctionnel et de première classe dans lequel l'art et les éléments historiques uniques coexistent avec le confort le plus moderne.",
                "Category": "Resort and Spa",
                "Tags": ["air conditioning", "bar", "continental breakfast"],
                "ParkingIncluded": "true",
                "LastRenovationDate": "2015-09-20T00:00:00Z",
                "Rating": 4.8,
                "Address": {
                    "StreetAddress": "3393 Peachtree Rd",
                    "City": "Atlanta",
                    "StateProvince": "GA",
                    "PostalCode": "30326"
                }
            },
            {
                "HotelId": "4",
                "HotelName": "Sublime Cliff Hotel",
                "Description": "Sublime Cliff Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Cliff is part of a lovingly restored 1800 palace.",
                "Description_fr": "Le sublime Cliff Hotel est situé au coeur du centre historique de sublime dans un quartier extrêmement animé et vivant, à courte distance de marche des sites et monuments de la ville et est entouré par l'extraordinaire beauté des églises, des bâtiments, des commerces et Monuments. Sublime Cliff fait partie d'un Palace 1800 restauré avec amour.",
                "Category": "Boutique",
                "Tags": ["concierge", "view", "24-hour front desk service"],
                "ParkingIncluded": true,
                "LastRenovationDate": "1960-02-06T00:00:00Z",
                "Rating": 4.6,
                "Address": {
                    "StreetAddress": "7400 San Pedro Ave",
                    "City": "San Antonio",
                    "StateProvince": "TX",
                    "PostalCode": "78216"
                }
            }
        ]
    }
    ```

1. Create a file named *hotels_quickstart_index.json* and paste the following code into *hotels_quickstart_index.json*:

    ```json
    {
    	"name": "hotels-quickstart",
    	"fields": [
    		{
    			"name": "HotelId",
    			"type": "Edm.String",
    			"key": true,
    			"filterable": true
    		},
    		{
    			"name": "HotelName",
    			"type": "Edm.String",
    			"searchable": true,
    			"filterable": false,
    			"sortable": true,
    			"facetable": false
    		},
    		{
    			"name": "Description",
    			"type": "Edm.String",
    			"searchable": true,
    			"filterable": false,
    			"sortable": false,
    			"facetable": false,
    			"analyzerName": "en.lucene"
    		},
    		{
    			"name": "Description_fr",
    			"type": "Edm.String",
    			"searchable": true,
    			"filterable": false,
    			"sortable": false,
    			"facetable": false,
    			"analyzerName": "fr.lucene"
    		},
    		{
    			"name": "Category",
    			"type": "Edm.String",
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
    					"type": "Edm.String",
    					"filterable": false,
    					"sortable": false,
    					"facetable": false,
    					"searchable": true
    				},
    				{
    					"name": "City",
    					"type": "Edm.String",
    					"searchable": true,
    					"filterable": true,
    					"sortable": true,
    					"facetable": true
    				},
    				{
    					"name": "StateProvince",
    					"type": "Edm.String",
    					"searchable": true,
    					"filterable": true,
    					"sortable": true,
    					"facetable": true
    				},
    				{
    					"name": "PostalCode",
    					"type": "Edm.String",
    					"searchable": true,
    					"filterable": true,
    					"sortable": true,
    					"facetable": true
    				},
    				{
    					"name": "Country",
    					"type": "Edm.String",
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
    }
    ```

1. Sign in to Azure with the following command:

    ```shell
    az login
    ```

1. Run the JavaScript code with the following command:

    ```shell
    node index.js
    ```

## Explaining the code

### Create index

The *hotels_quickstart_index.json* file defines how Azure AI Search works with the documents you load in the next step. Each field is identified by a `name` and have a specified `type`. Each field also has a series of index attributes that specify whether Azure AI Search can search, filter, sort, and facet upon the field. Most of the fields are simple data types, but some, like `AddressType` are complex types that allow you to create rich data structures in your index. You can read more about [supported data types](/rest/api/searchservice/supported-data-types) and index attributes described in [Create Index (REST)](/rest/api/searchservice/indexes/create). 

With our index definition in place, we want to import *hotels_quickstart_index.json* at the top of *index.js* so the main function can access the index definition.

```javascript
const indexDefinition = require('./hotels_quickstart_index.json');
```

Within the main function, we then create a `SearchIndexClient`, which is used to create and manage indexes for Azure AI Search. 

```javascript
const indexClient = new SearchIndexClient(endpoint, new AzureKeyCredential(apiKey));
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

### Load documents 

In Azure AI Search, documents are data structures that are both inputs to indexing and outputs from queries. You can push such data to the index or use an [indexer](/azure/search/search-indexer-overview). In this case, we'll programatically push the documents to the index.

Document inputs might be rows in a database, blobs in Blob storage, or, as in this sample, JSON documents on disk. Similar to what we did with the `indexDefinition`, we also need to import `hotels.json` at the top of *index.js* so that the data can be accessed in our main function.

```javascript
const hotelData = require('./hotels.json');
```

To index data into the search index, we now need to create a `SearchClient`. While the `SearchIndexClient` is used to create and manage an index, the `SearchClient` is used to upload documents and query the index.

There are two ways to create a `SearchClient`. The first option is to create a `SearchClient` from scratch:

```javascript
 const searchClient = new SearchClient(endpoint, indexName, new AzureKeyCredential(apiKey));
```

Alternatively, you can use the `getSearchClient()` method of the `SearchIndexClient` to create the `SearchClient`:

```javascript
const searchClient = indexClient.getSearchClient(indexName);
```

Now that the client is defined, upload the documents into the search index. In this case, we use the `mergeOrUploadDocuments()` method, which uploads the documents or merges them with an existing document if a document with the same key already exists.

```javascript
console.log('Uploading documents...');
let indexDocumentsResult = await searchClient.mergeOrUploadDocuments(hotelData['value']);

console.log(`Index operations succeeded: ${JSON.stringify(indexDocumentsResult.results[0].succeeded)}`);
```

### Search an index

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
