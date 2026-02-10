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

In this quickstart, you use the [Azure AI Search client library for JavaScript](/javascript/api/overview/azure/search-documents-readme) (compatible with TypeScript) to create, load, and query a [vector index](../../vector-store.md). The JavaScript client library provides an abstraction over the REST APIs for index operations.

In Azure AI Search, a vector index has an index schema that defines vector and nonvector fields, a vector search configuration for algorithms that create the embedding space, and settings on vector field definitions that are evaluated at query time. [Indexes - Create or Update](/rest/api/searchservice/indexes/create-or-update) (REST API) creates the vector index.

> [!TIP]
> + Want to get started right away? Download the [source code](https://github.com/Azure-Samples/azure-search-javascript-samples/tree/main/quickstart-vector-ts) on GitHub.
> + This quickstart omits the vectorization step and provides inline embeddings. For [integrated vectorization](../../vector-search-integrated-vectorization.md) over your own content, try the [**Import data (new)** wizard](../../search-get-started-portal-import-vectors.md).

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

- An [Azure AI Search service](../../search-create-service-portal.md). You can use the Free tier for most of this quickstart, but we recommend Basic or higher for larger data files.

- [Semantic ranker enabled on your search service](../../semantic-how-to-enable-disable.md) for the optional semantic hybrid query.

- [Node.js 20 LTS](https://nodejs.org/en/download/) or later to run the compiled code.

- [TypeScript](https://www.typescriptlang.org/download/) to compile TypeScript to JavaScript.

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
   cd azure-search-javascript-samples/quickstart-vector-ts
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
    npm run build && node -r dotenv/config dist/createIndex.js
    ```

1. Load documents that contain precomputed embeddings.

    ```bash
    npm run build && node -r dotenv/config dist/uploadDocuments.js
    ```

1. Run a vector search query.

    ```bash
    npm run build && node -r dotenv/config dist/searchSingle.js
    ```

1. (Optional) Run additional query variations.

    ```bash
    npm run build && node -r dotenv/config dist/searchSingleWithFilter.js
    npm run build && node -r dotenv/config dist/searchSingleWithFilterGeo.js
    npm run build && node -r dotenv/config dist/searchHybrid.js
    npm run build && node -r dotenv/config dist/searchSemanticHybrid.js
    ```

> [!NOTE]
> The `npm run build` command compiles the TypeScript files in `src/` to JavaScript in `dist/`.

### Output

The output of `createIndex.ts` shows the index name and confirmation.

```output
Using Azure Search endpoint: https://<search-service-name>.search.windows.net
Using index name: hotels-vector-quickstart
Creating index...
hotels-vector-quickstart created
```

The output of `uploadDocuments.ts` shows the success status for each indexed document.

```output
Uploading documents...
Key: 1, Succeeded: true, ErrorMessage: none
Key: 2, Succeeded: true, ErrorMessage: none
Key: 3, Succeeded: true, ErrorMessage: none
Key: 4, Succeeded: true, ErrorMessage: none
Key: 48, Succeeded: true, ErrorMessage: none
Key: 49, Succeeded: true, ErrorMessage: none
Key: 13, Succeeded: true, ErrorMessage: none
All documents indexed successfully.
```

The output of `searchSingle.ts` shows vector search results ranked by similarity score.

```output
Single Vector search found 5
- HotelId: 48, HotelName: Nordick's Valley Motel, Tags: ["continental breakfast","air conditioning","free wifi"], Score 0.6605852
- HotelId: 13, HotelName: Luxury Lion Resort, Tags: ["bar","concierge","restaurant"], Score 0.6333684
- HotelId: 4, HotelName: Sublime Palace Hotel, Tags: ["concierge","view","air conditioning"], Score 0.605672
- HotelId: 49, HotelName: Swirling Currents Hotel, Tags: ["air conditioning","laundry service","24-hour front desk service"], Score 0.6026341
- HotelId: 2, HotelName: Old Century Hotel, Tags: ["pool","free wifi","air conditioning","concierge"], Score 0.57902366
```

## Understand the code

[!INCLUDE [understand code note](../understand-code-note.md)]

Now that you've run the code, let's break down the key steps:

1. [Create a vector index](#create-a-vector-index)
1. [Upload documents to the index](#upload-documents-to-the-index)
1. [Query the index](#query-the-index)

### Create a vector index

Before you add content to Azure AI Search, you must create an index to define how the content is stored and structured.

The index schema is organized around hotel content. Sample data consists of vector and nonvector descriptions of fictitious hotels. The following code in `createIndex.ts` creates the index schema, including the vector field `DescriptionVector`.

```typescript
const searchFields: SearchField[] = [
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

const vectorSearch: VectorSearch = {
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

const semanticSearch: SemanticSearch = {
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

const searchIndex: SearchIndex = {
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

+ This particular index supports multiple search capabilities:

    + [Full-text search](../../search-lucene-query-architecture.md) (`searchable: true`)

    + [Vector search](../../vector-search-overview.md) (`DescriptionVector` with `vectorSearchProfileName`)

    + [Semantic ranking](../../semantic-search-overview.md) (`semanticSearch`)

    + [Faceted search](../../search-faceted-navigation.md) (fields marked with `facetable`)

    + [Geo-spatial search](../../search-query-odata-geo-spatial-functions.md) (`Location` field with `Edm.GeographyPoint`)

    + [Filtering](../../search-filters.md) and sorting (fields marked with `filterable` and `sortable`)

+ The `vectorSearchDimensions` property must match the output size of your embedding model. This quickstart uses 1,536 dimensions to match the `text-embedding-ada-002` model.

+ The `vectorSearch` configuration defines the Approximate Nearest Neighbor (ANN) algorithm. Supported algorithms include Hierarchical Navigable Small World (HNSW) and exhaustive K-Nearest Neighbor (KNN). For more information, see [Relevance in vector search](../../vector-search-ranking.md).

### Upload documents to the index

Newly created indexes are empty. To populate an index and make it searchable, you must upload JSON documents that conform to the index schema.

In Azure AI Search, documents serve as both inputs for indexing and outputs for queries. For simplicity, this quickstart provides sample hotel documents with precomputed vectors. In production scenarios, content is often pulled from connected data sources and transformed into JSON using [indexers](../../search-indexer-overview.md).

The following code in `uploadDocuments.ts` uploads documents to your search service.

```typescript
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

Your code interacts with a specific search index hosted in your Azure AI Search service through the `SearchClient`, which is the main object provided by the [`@azure/search-documents`](/javascript/api/overview/azure/search-documents-readme) package. The `SearchClient` provides access to index operations, such as:

+ Data ingestion: `uploadDocuments`, `mergeDocuments`, `deleteDocuments`

+ Search operations: `search`, `autocomplete`, `suggest`

### Query the index

The queries in the search files demonstrate different search patterns. The example vector queries are based on two strings:

+ Full-text search string: `"historic hotel walk to restaurants and shopping"`

+ Vector query string: `"quintessential lodging near running trails, eateries, retail"` (vectorized into a mathematical representation)

The vector query string is semantically similar to the full-text search string, but it includes terms that don't exist in the index. A keyword-only search for the vector query string returns zero results. However, vector search finds relevant matches based on meaning rather than exact keywords.

The following examples start with a basic vector query and progressively add filters, keyword search, and semantic reranking.

#### Single vector search

`searchSingle.ts` demonstrates a basic scenario where you want to find document descriptions that closely match the vector query string. The `VectorQuery` object configures the vector search:

+ `kNearestNeighborsCount` limits how many results are returned based on vector similarity.
+ `fields` specifies the vector field to search against.

```typescript
const vectorQuery: VectorQuery<HotelDocument> = {
    vector: vector,
    kNearestNeighborsCount: 5,
    fields: ["DescriptionVector"],
    kind: "vector",
    exhaustive: true
};

const searchOptions: SearchOptions<HotelDocument> = {
    top: 7,
    select: ["HotelId", "HotelName", "Description", "Category", "Tags"] as const,
    includeTotalCount: true,
    vectorSearchOptions: {
        queries: [vectorQuery],
        filterMode: "postFilter"
    }
};

const results: SearchDocumentsResult<HotelDocument> = await searchClient.search("*", searchOptions);

for await (const result of results.results) {
    const doc = result.document;
    console.log(`HotelId: ${doc.HotelId}, HotelName: ${doc.HotelName}, Score: ${result.score}`);
}
```

#### Single vector search with a filter

In Azure AI Search, [filters](../../vector-search-filters.md) apply to nonvector fields in an index. `searchSingleWithFilter.ts` filters on the `Tags` field to filter out any hotels that don't provide free Wi-Fi.

```typescript
const searchOptions: SearchOptions<HotelDocument> = {
    top: 7,
    select: ["HotelId", "HotelName", "Description", "Category", "Tags"] as const,
    includeTotalCount: true,
    filter: "Tags/any(tag: tag eq 'free wifi')", // Adding filter for "free wifi" tag
    vectorSearchOptions: {
        queries: [vectorQuery],
        filterMode: "postFilter"
    }
};

const results: SearchDocumentsResult<HotelDocument> = await searchClient.search("*", searchOptions);
```

#### Single vector search with a geo filter

You can specify a [geo-spatial filter](../../search-query-odata-geo-spatial-functions.md) to limit results to a specific geographic area. `searchSingleWithGeoFilter.ts` specifies a geographic point (Washington D.C., using longitude and latitude coordinates) and returns hotels within 300 kilometers. The `filterMode` property determines when the filter runs. In this case, `postFilter` runs the filter after the vector search.

```typescript
const searchOptions: SearchOptions<HotelDocument> = {
    top: 5,
    includeTotalCount: true,
    select: ["HotelId", "HotelName", "Category", "Description", "Address/City", "Address/StateProvince"] as const,
    facets: ["Address/StateProvince"],
    filter: "geo.distance(Location, geography'POINT(-77.03241 38.90166)') le 300",
    vectorSearchOptions: {
        queries: [vectorQuery],
        filterMode: "postFilter"
    }
};
```

#### Hybrid search

[Hybrid search](../../hybrid-search-overview.md) combines full-text and vector queries in a single request. `searchHybrid.ts` runs both query types concurrently, and then uses Reciprocal Rank Fusion (RRF) to merge the results into a unified ranking. RRF uses the inverse of result rankings from each result set to produce a merged ranking. Notice that hybrid search scores are uniformly smaller than single-query scores.

```typescript
const vectorQuery: VectorQuery<HotelDocument> = {
    vector: vector,
    kNearestNeighborsCount: 5,
    fields: ["DescriptionVector"],
    kind: "vector",
    exhaustive: true
};

const searchOptions: SearchOptions<HotelDocument> = {
    top: 5,
    includeTotalCount: true,
    select: ["HotelId", "HotelName", "Description", "Category", "Tags"] as const,
    vectorSearchOptions: {
        queries: [vectorQuery],
        filterMode: "postFilter"
    }
};

// Use search text for keyword search (hybrid search = vector + keyword)
const searchText = "historic hotel walk to restaurants and shopping";
const results: SearchDocumentsResult<HotelDocument> = await searchClient.search(searchText, searchOptions);
```

#### Semantic hybrid search

`searchSemanticHybrid.ts` demonstrates [semantic ranking](../../semantic-search-overview.md), which reranks results based on language understanding.

```typescript
const searchOptions: SearchOptions<HotelDocument> = {
    top: 5,
    includeTotalCount: true,
    select: ["HotelId", "HotelName", "Category", "Description"] as const,
    queryType: "semantic" as const,
    semanticSearchOptions: {
        configurationName: "semantic-config"
    },
    vectorSearchOptions: {
        queries: [vectorQuery],
        filterMode: "postFilter"
    }
};

const searchText = "historic hotel walk to restaurants and shopping";
const results: SearchDocumentsResult<HotelDocument> = await searchClient.search(searchText, searchOptions);

for await (const result of results.results) {
    console.log(`Score: ${result.score}, Re-ranker Score: ${result.rerankerScore}`);
}
```

Compare these results with the hybrid search results from the previous query. Without semantic reranking, Sublime Palace Hotel ranks first because Reciprocal Rank Fusion (RRF) combines the text and vector scores to produce a merged result. After semantic reranking, Swirling Currents Hotel moves to the top spot.

The semantic ranker uses machine comprehension models to evaluate how well each result matches the intent of the query. Swirling Currents Hotel's description mentions `"walking access to shopping, dining, entertainment and the city center"`, which aligns closely with the search query's `"walk to restaurants and shopping"`. This semantic match for nearby dining and shopping elevates it above Sublime Palace Hotel, which doesn't emphasize walkable amenities in its description.

Key takeaways:

+ In a hybrid search, you can integrate vector search with full-text search over keywords. Filters and semantic ranking apply to textual content only, not vectors.

+ Actual results include more detail, including semantic captions and highlights. This quickstart modifies results for readability. To get the full structure of the response, use REST to run the request.

## Clean up resources

[!INCLUDE [resource-cleanup-paid](../resource-cleanup-paid.md)]

Otherwise, run the following command to delete the index you created in this quickstart.

```bash
npm run build && node -r dotenv/config dist/deleteIndex.js
```
