---
manager: nitinme
author: diberry
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 02/05/2026
ms.custom: dev-focus
ai-usage: ai-assisted
---

In this quickstart, you use the [Azure AI Search client library for JavaScript](/javascript/api/overview/azure/search-documents-readme) to create, load, and query a [vector index](../../vector-store.md). The JavaScript client library provides an abstraction over the REST APIs for index operations.

In Azure AI Search, a vector index has an index schema that defines vector and nonvector fields, a vector search configuration for algorithms that create the embedding space, and settings on vector field definitions that are evaluated at query time. [Indexes - Create or Update](/rest/api/searchservice/indexes/create-or-update) (REST API) creates the vector index.

> [!TIP]
> + Want to get started right away? Download the [source code](https://github.com/Azure-Samples/azure-search-javascript-samples/tree/main/quickstart-vector-js) on GitHub.
> + This quickstart omits the vectorization step and provides inline embeddings. For [integrated vectorization](../../vector-search-integrated-vectorization.md) over your own content, try the [**Import data (new)** wizard](../../search-get-started-portal-import-vectors.md).

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

- An [Azure AI Search service](../../search-create-service-portal.md). You can use the Free tier for most of this quickstart, but we recommend Basic or higher for larger data files.

- [Semantic ranker enabled on your search service](../../semantic-how-to-enable-disable.md) for the optional semantic hybrid query.

- [Node.js 20 LTS](https://nodejs.org/en/download/) or later.

- [Visual Studio Code](https://code.visualstudio.com/download).

- [Git](https://git-scm.com/downloads) to clone the sample repository.

- The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

## Configure access

[!INCLUDE [resource authentication](../resource-authentication.md)]

## Get endpoint

[!INCLUDE [resource endpoint](../resource-endpoint.md)]

## Set up the environment

1. Use Git to clone the sample repository.

   ```bash
   git clone https://github.com/Azure-Samples/azure-search-javascript-samples
   ```

1. Navigate to the quickstart folder and open it in Visual Studio Code.

   ```bash
   cd azure-search-javascript-samples/quickstart-vector-js
   code .
   ```

1. In `sample.env`, replace the placeholder value for `AZURE_SEARCH_ENDPOINT` with the URL you obtained in [Get endpoint](#get-endpoint).

1. Rename `sample.env` to `.env`.

   ```bash
   mv sample.env .env
   ```

1. Install the dependencies.

   ```bash
   npm install
   ```

   When the installation completes, you should see a `node_modules` folder in the project directory.

1. For keyless authentication with Microsoft Entra ID, sign in to your Azure account. If you have multiple subscriptions, select the one that contains your Azure AI Search service.

   ```azurecli
   az login
   ```

## Run the code

1. Create a vector index.

    ```bash
    node -r dotenv/config src/createIndex.js
    ```

1. Load documents that contain precomputed embeddings.

    ```bash
    node -r dotenv/config src/uploadDocuments.js
    ```

1. Run queries. Start with a single vector search.

    ```bash
    node -r dotenv/config src/searchSingle.js
    ```

1. (Optional) Run additional query variations.

    ```bash
    node -r dotenv/config src/searchSingleWithFilter.js
    node -r dotenv/config src/searchSingleWithFilterGeo.js
    node -r dotenv/config src/searchHybrid.js
    node -r dotenv/config src/searchSemanticHybrid.js
    ```

### Output

The output of `createIndex.js` shows the index name and confirmation.

```output
Using Azure Search endpoint: https://<search-service-name>.search.windows.net
Using Azure Search index: hotels-vector-quickstart
Creating index...
hotels-vector-quickstart created
```

The output of `uploadDocuments.js` shows the success status for each indexed document.

```output
Uploading documents...
Key: 1, Succeeded: true, ErrorMessage: none
Key: 2, Succeeded: true, ErrorMessage: none
Key: 3, Succeeded: true, ErrorMessage: none
Key: 4, Succeeded: true, ErrorMessage: none
Key: 48, Succeeded: true, ErrorMessage: none
Key: 49, Succeeded: true, ErrorMessage: none
Key: 13, Succeeded: true, ErrorMessage: none
Waiting for indexing... Current count: 0
All documents indexed successfully.
```

The output of `searchSingle.js` shows vector search results ranked by similarity score.

```output
Single Vector search found 5
- HotelId: 48, HotelName: Nordick's Valley Motel, Tags: ["continental breakfast","air conditioning","free wifi"], Score 0.6605852
- HotelId: 13, HotelName: Luxury Lion Resort, Tags: ["bar","concierge","restaurant"], Score 0.6333684
- HotelId: 4, HotelName: Sublime Palace Hotel, Tags: ["concierge","view","air conditioning"], Score 0.605672
- HotelId: 49, HotelName: Swirling Currents Hotel, Tags: ["air conditioning","laundry service","24-hour front desk service"], Score 0.6026341
- HotelId: 2, HotelName: Old Century Hotel, Tags: ["pool","free wifi","air conditioning","concierge"], Score 0.57902366
```

## Understand the code

Now that you've run the code, let's break down the key steps:

1. [Create a vector index](#create-a-vector-index)
1. [Upload documents to the index](#upload-documents-to-the-index)
1. [Query the index](#query-the-index)

### Create a vector index

The following code in `createIndex.js` creates the index schema, including the vector field `DescriptionVector`.

```javascript
const searchFields = [
    { name: "HotelId", type: "Edm.String", key: true, sortable: true, filterable: true, facetable: true },
    { name: "HotelName", type: "Edm.String", searchable: true, filterable: true },
    { name: "Description", type: "Edm.String", searchable: true },
    {
        name: "DescriptionVector",
        type: "Collection(Edm.Single)",
        searchable: true,
        vectorSearchDimensions: 1536,
        vectorSearchProfileName: "vector-profile"
    },
    { name: "Category", type: "Edm.String", filterable: true, facetable: true },
    { name: "Tags", type: "Collection(Edm.String)", filterable: true },
    // Additional fields: ParkingIncluded, LastRenovationDate, Rating, Address, Location
];

const vectorSearch = {
    profiles: [
        {
            name: "vector-profile",
            algorithmConfigurationName: "vector-search-algorithm"
        }
    ],
    algorithms: [
        {
            name: "vector-search-algorithm",
            kind: "hnsw",
            parameters: { m: 4, efConstruction: 400, efSearch: 1000, metric: "cosine" }
        }
    ]
};

const semanticSearch = {
    configurations: [
        {
            name: "semantic-config",
            prioritizedFields: {
                contentFields: [{ name: "Description" }],
                keywordsFields: [{ name: "Category" }],
                titleField: { name: "HotelName" }
            }
        }
    ]
};

const searchIndex = {
    name: indexName,
    fields: searchFields,
    vectorSearch: vectorSearch,
    semanticSearch: semanticSearch,
    suggesters: [{ name: "sg", searchMode: "analyzingInfixMatching", sourceFields: ["HotelName"] }]
};

const result = await indexClient.createOrUpdateIndex(searchIndex);
```

Key takeaways:

+ You define an index by creating a list of fields.

+ This particular index supports multiple search capabilities, including full-text keyword search, vector search (enables hybrid search by collocating vector and nonvector fields), semantic search, faceted search, geo-spatial search, and filtering.

+ Vector fields contain floating point values. The dimensions attribute has a minimum of 2 and a maximum of 4096 floating point values each. This quickstart sets the dimensions attribute to 1,536 because that's the size of embeddings generated by the `text-embedding-ada-002` model.

### Upload documents to the index

The following code in `uploadDocuments.js` uploads JSON-formatted documents to your search service.

```javascript
const DOCUMENTS = [
    // Array of hotel documents with embedded 1536-dimension vectors
    // Each document contains: HotelId, HotelName, Description, DescriptionVector,
    // Category, Tags, ParkingIncluded, LastRenovationDate, Rating, Address, Location
];

const searchClient = new SearchClient(searchEndpoint, indexName, credential);

const result = await searchClient.uploadDocuments(DOCUMENTS);
for (const r of result.results) {
    console.log(`Key: ${r.key}, Succeeded: ${r.succeeded}`);
}
```

Key takeaways:

+ Your code interacts with a specific search index hosted in your Azure AI Search service through the `SearchClient`, which is the main object provided by the @azure/search-documents package. The `SearchClient` provides access to index operations, such as:

    + Data ingestion: `uploadDocuments`, `mergeDocuments`, `deleteDocuments`

    + Search operations: `search`, `autocomplete`, `suggest`

    + Index management operations: `createIndex`, `deleteIndex`, `getIndex`

### Query the index

The queries in the search files demonstrate different search patterns. The example vector queries are based on two strings:

+ Search string: `historic hotel walk to restaurants and shopping`
+ Vector query string: `quintessential lodging near running trails, eateries, retail` (vectorized into a mathematical representation)

The vector query string is semantically similar to the search string, but it includes terms that don't exist in the search index. If you do a keyword search for `quintessential lodging near running trails, eateries, retail`, results are zero. This example shows how you can get relevant results even if there are no matching terms.

#### Single vector search

The `searchSingle.js` file demonstrates a basic scenario where you want to find document descriptions that closely match the search string.

```javascript
const vectorQuery = {
    vector: vector,
    kNearestNeighborsCount: 5,
    fields: ["DescriptionVector"],
    kind: "vector",
    exhaustive: true
};

const searchOptions = {
    top: 7,
    select: ["HotelId", "HotelName", "Description", "Category", "Tags"],
    includeTotalCount: true,
    vectorSearchOptions: {
        queries: [vectorQuery],
        filterMode: "postFilter"
    }
};

const results = await searchClient.search("*", searchOptions);

for await (const result of results.results) {
    const doc = result.document;
    console.log(`HotelId: ${doc.HotelId}, HotelName: ${doc.HotelName}, Score: ${result.score}`);
}
```

#### Single vector search with filter

In Azure AI Search, [filters](../../vector-search-filters.md) apply to nonvector fields in an index. The `searchSingleWithFilter.js` file filters on the `Tags` field to filter out any hotels that don't provide free Wi-Fi.

```javascript
const searchOptions = {
    top: 7,
    select: ["HotelId", "HotelName", "Description", "Category", "Tags"],
    includeTotalCount: true,
    filter: "Tags/any(tag: tag eq 'free wifi')", // Adding filter for "free wifi" tag
    vectorSearchOptions: {
        queries: [vectorQuery],
        filterMode: "postFilter"
    }
};

const results = await searchClient.search("*", searchOptions);
```

For a geo filter, you can specify a geospatial filter to limit results to a specific geographic area. The `searchSingleWithFilterGeo.js` file limits results to hotels within 300 kilometers of Washington D.C.

```javascript
const searchOptions = {
    top: 5,
    includeTotalCount: true,
    select: ["HotelId", "HotelName", "Category", "Description", "Address/City", "Address/StateProvince"],
    facets: ["Address/StateProvince"],
    filter: "geo.distance(Location, geography'POINT(-77.03241 38.90166)') le 300",
    vectorSearchOptions: {
        queries: [vectorQuery],
        filterMode: "postFilter"
    }
};
```

#### Hybrid search

[Hybrid search](../../hybrid-search-overview.md) combines keyword and vector queries in one request. The `searchHybrid.js` file runs the full-text and vector query strings concurrently.

```javascript
const vectorQuery = {
    vector: vector,
    kNearestNeighborsCount: 5,
    fields: ["DescriptionVector"],
    kind: "vector",
    exhaustive: true
};

const searchOptions = {
    top: 5,
    includeTotalCount: true,
    select: ["HotelId", "HotelName", "Description", "Category", "Tags"],
    vectorSearchOptions: {
        queries: [vectorQuery],
        filterMode: "postFilter"
    }
};

// Use search text for keyword search (hybrid search = vector + keyword)
const searchText = "historic hotel walk to restaurants and shopping";
const results = await searchClient.search(searchText, searchOptions);
```

Because Reciprocal Rank Fusion (RRF) merges results, it helps to review the inputs. In the full-text query only, the top two results are Sublime Palace Hotel and Luxury Lion Resort, with Sublime Palace Hotel having a stronger BM25 relevance score. In the vector-only query using HNSW, Sublime Palace Hotel drops to the fourth position. Luxury Lion, which was second in the full-text search and third in the vector search, doesn't experience the same range of fluctuation, so it appears as a top match in a homogenized result set.

#### Semantic hybrid search

Add [semantic ranking](../../semantic-search-overview.md) to rerank results based on language understanding. The `searchSemanticHybrid.js` file adds semantic ranking.

```javascript
const searchOptions = {
    top: 5,
    includeTotalCount: true,
    select: ["HotelId", "HotelName", "Category", "Description"],
    queryType: "semantic",
    semanticSearchOptions: {
        configurationName: "semantic-config"
    },
    vectorSearchOptions: {
        queries: [vectorQuery],
        filterMode: "postFilter"
    }
};

const searchText = "historic hotel walk to restaurants and shopping";
const results = await searchClient.search(searchText, searchOptions);

for await (const result of results.results) {
    console.log(`Score: ${result.score}, Re-ranker Score: ${result.rerankerScore}`);
}
```

With semantic ranking, the Swirling Currents Hotel moves to the top spot. Without semantic ranking, Nordick's Valley Motel is number one. With semantic ranking, the machine comprehension models recognize that `historic` applies to "hotel within walking distance to dining (restaurants) and shopping."

Key takeaways:

+ In a hybrid search, you can integrate vector search with full-text search over keywords. Filters, spell check, and semantic ranking apply to textual content only, and not vectors.

+ Actual results include more detail, including semantic captions and highlights. Results were modified for readability. To get the full structure of the response, run the request in the REST client.

## Clean up resources

[!INCLUDE [resource-cleanup-paid](../resource-cleanup-paid.md)]

Otherwise, run the following command to delete the index you created in this quickstart.

```bash
node -r dotenv/config src/deleteIndex.js
```
