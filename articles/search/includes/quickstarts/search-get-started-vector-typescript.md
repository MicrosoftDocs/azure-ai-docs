---
manager: nitinme
author: rotabor
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 06/26/2025
---

In this quickstart, you use TypeScript to create, load, and query vectors. The code examples perform these operations by using the [Azure AI Search client library](/python/api/overview/azure/search-documents-readme). The library provides an abstraction over the REST API for access to index operations such as data ingestion, search operations, and index management operations.

In Azure AI Search, a [vector store](../../vector-store.md) has an index schema that defines vector and nonvector fields, a vector search configuration for algorithms that create the embedding space, and settings on vector field definitions that are evaluated at query time. The [Create Index](/rest/api/searchservice/indexes/create-or-update) REST API creates the vector store.

> [!NOTE]
> This quickstart omits the vectorization step and provides inline embeddings. If you want to add [built-in data chunking and vectorization](../../vector-search-integrated-vectorization.md) over your own content, try the [**Import and vectorize data wizard**](../../search-get-started-portal-import-vectors.md) for an end-to-end walkthrough.

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

- An Azure AI Search service. [Create a service](../../search-create-service-portal.md) or [find an existing service](https://portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/CognitiveSearch) in your current subscription.
    - You can use a free search service for most of this quickstart, but we recommend the Basic tier or higher for larger data files.
    - To run the query example that invokes [semantic reranking](../../semantic-search-overview.md), your search service must be at the Basic tier or higher with [semantic ranker enabled](../../semantic-how-to-enable-disable.md).

- [Visual Studio Code](https://code.visualstudio.com/download) with the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [Jupyter package](https://pypi.org/project/jupyter/).

- [Node.JS with LTS](https://nodejs.org/en/download/).
- [TypeScript](https://www.typescriptlang.org/download). You can globally install TypeScript using npm:

   ```bash
   npm install -g typescript
   ```

---

## Get service endpoints

In the remaining sections, you set up API calls to Azure OpenAI and Azure AI Search. Get the service endpoints so that you can provide them as variables in your code.

1. Sign in to the [Azure portal](https://portal.azure.com).

1. [Find your search service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices).

1. On the **Overview** home page, copy the URL. An example endpoint might look like `https://example.search.windows.net`. 

1. [Find your Azure OpenAI service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.CognitiveServices%2Faccounts).

1. On the **Overview** home page, select the link to view the endpoints. Copy the URL. An example endpoint might look like `https://example.openai.azure.com/`.

## Set up environment variables for local development

1. Create a `.env` file.
1. Add the following environment variables to the `.env` file, replacing the values with your own service endpoints and keys.

   ```plaintext
   AZURE_SEARCH_ENDPOINT=<YOUR AZURE AI SEARCH ENDPOINT>
   AZURE_SEARCH_INDEX_NAME=hotels-sample-index
   ```


## Set up the Node.JS project

Set up project with Visual Studio Code and TypeScript.

1. Start Visual Studio Code in a new directory.

   ```bash
   mkdir vector-quickstart && cd vector-quickstart
   code .
   ```
1. Create a new package for ESM modules in your project directory.

   ```bash
   npm init -y
   npm pkg set type=module
   ```

   This creates a `package.json` file with default values.

1. Install the following npm packages.

   ```bash
   npm install @azure/identity @azure/search-documents dotenv @types/node
   ``` 

1. Create a `src` directory in your project directory.

   ```bash
   mkdir src
   ```

1. Create a `tsconfig.json` file in the project directory for ESM with the following content.

    ```json
    {
      "compilerOptions": {
        "target": "esnext",
        "module": "NodeNext",
        "moduleResolution": "nodenext",
        "rootDir": "./src",
        "outDir": "./dist/",
        "esModuleInterop": true,
        "forceConsistentCasingInFileNames": true,
        "strict": true,
        "skipLibCheck": true,
        "declaration": true,
        "sourceMap": true,
        "resolveJsonModule": true,
        "moduleDetection": "force", // Add this for ESM
        "allowSyntheticDefaultImports": true // Helpful for ESM interop
      },
      "include": [
        "src/**/*.ts"
      ]
    }
   ```

## Sign in to Azure

You're using Microsoft Entra ID and role assignments for the connection. Make sure you're logged in to the same tenant and subscription as Azure AI Search and Azure OpenAI. You can use the Azure CLI on the command line to show current properties, change properties, and to sign in. For more information, see [Connect without keys](../../search-get-started-rbac.md). 

Run each of the following commands in sequence.

```azure-cli
az account show

az account set --subscription <PUT YOUR SUBSCRIPTION ID HERE>

az login --tenant <PUT YOUR TENANT ID HERE>
```

You should now be logged in to Azure from your local device.

## Create the vector quickstart

This quickstart creates several TypeScript files that perform the following operations:

* `manageIndex.ts`: Create a vector index and upload documents to it.
    * [**Create the index**](#create-the-vector-index): Create a vector index.
    * [**Upload documents**](#upload-documents-to-the-index): Upload documents to the index. Wait until the index is ready for search operations.

* `search.ts`: Create vector searches to find documents related to a query.
    * [**Create a single vector search**](#create-a-single-vector-search): Perform a single vector search.
    * [**Create a single vector search with a filter**](#create-a-single-vector-search-with-a-filter): Perform a single vector search with a filter.
    * [**Create a search with a geospatial filter**](#create-a-search-with-a-geospatial-filter): Perform a vector search with a geospatial filter.
    * [**Create a hybrid search**](#create-a-hybrid-search): Perform a hybrid search combining keyword and vector search.
    * [**Create a semantic hybrid search**](#create-a-semantic-hybrid-search): Perform a semantic hybrid search combining semantic and vector search.
* [**Create documents array**](#create-the-documents): Create array of documents with vectorized descriptions.
* [**Create vectorized query**](#create-the-query-vector): Create vector of query `quintessential lodging near running trails, eateries, retail`.
* [**Create the main function**](#create-the-main-function): Execute the main function to perform all operations.
 
## Create the vector index 
In this section, you create a vector index in Azure AI Search. The index schema defines the fields, including the vector field `DescriptionVector`. Once the index is created, you upload documents to the index. The documents contain the vectorized version of the article's description, which enables similarity search based on meaning rather than exact keywords.

1. Create a `manageIndex.ts` file in the `src` directory with the following code.

2. Add the dependencies, environment variables, and TypeScript type for `HotelDocument` to the top of the file. 

    :::code language="typescript" source="~/azure-search-javascript-samples/quickstart-vector-ts/src/manageIndex.ts" id="Index_dependencies":::    

3. Add the `createIndex` function to create the vector index. The function defines the index schema, including the vector field `DescriptionVector`.

    :::code language="typescript" source="~/azure-search-javascript-samples/quickstart-vector-ts/src/manageIndex.ts" id="Index_createIndex":::

When this code is run you can see the index is created: 

```console
Using Azure Search endpoint: https://my-service.search.windows.net
Using index name: hotels-vector-quickstart
Creating index...
hotels-vector-quickstart created
```

## Upload documents to the index

4. Add the `uploadDocuments` function to upload documents to the index. The function uses an array of `HotelDocument` objects ([defined in a different section of this article](#create-the-documents)) and uploads them to the index. 
1. Because this quickstart searches the index immediately, add the `waitUntilIndexed` function to wait until the index is ready for search operations. This is important because the index needs to be fully populated with documents before you can perform searches.

    :::code language="typescript" source="~/azure-search-javascript-samples/quickstart-vector-ts/src/manageIndex.ts" id="Index_waitTilIndexed":::

When this code is run you can see the documents are uploaded to the index and ready to search: 

```console
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

## Create the vector searches

In this section, you create vector queries to search the index. The queries are based on a vectorized query string that is semantically similar to the search string. The queries demonstrate how to perform single vector searches, hybrid searches, and semantic hybrid searches.

1. Create a `search.ts` file in the `src` directory with the following code.

2. Add the dependencies, and create the the searchClient for the index to the top of the file. 

    :::code language="typescript" source="~/azure-search-javascript-samples/quickstart-vector-ts/src/search.ts" id="Search_dependencies":::    


## Create a single vector search

Continue to add to the `./src/search.ts` file for the vector searches. The `vector` is added to the quickstart in [a later section](#create-the-vector-query-string) and represents a vectorization of the query string `quintessential lodging near running trails, eateries, retail`. 

Add the `singleVectorSearch` function to perform a single vector search. This function uses the `DescriptionVector` field to find documents that are semantically similar to the query vector.

:::code language="typescript" source="~/azure-search-javascript-samples/quickstart-vector-ts/src/search.ts" id="Search_singleVectorSearch":::

When this code is run you can see the relevant documents: 

```console
Single Vector search found 5
- HotelId: 48, HotelName: Nordick's Valley Motel, Category: Boutique, Score 0.6605852
- HotelId: 13, HotelName: Luxury Lion Resort, Category: Luxury, Score 0.6333684
- HotelId: 4, HotelName: Sublime Palace Hotel, Category: Boutique, Score 0.605672
- HotelId: 49, HotelName: Swirling Currents Hotel, Category: Suite, Score 0.6026341
- HotelId: 2, HotelName: Old Century Hotel, Category: Boutique, Score 0.57902366
```

## Create a single vector search with a filter

Continue to add to the `./src/search.ts` file for the vector searches. Add a filter to find hotels with free wifi using the filter: `Tags/any(tag: tag eq 'free wifi')`. 

:::code language="typescript" source="~/azure-search-javascript-samples/quickstart-vector-ts/src/search.ts" id="Search_singleVectorSearchWithFilter":::

When this code is run you can see the relevant documents: 

```console
Single Vector search with filter found 2 
- HotelId: 48, HotelName: Nordick's Valley Motel, Tags: ["continental breakfast","air conditioning","free wifi"], Score 0.6605852
- HotelId: 2, HotelName: Old Century Hotel, Tags: ["pool","free wifi","air conditioning","concierge"], Score 0.57902366
```

## Create a search with a geospatial filter    

Continue to add to the `./src/search.ts` file for the vector searches. Add a geospatial filter to find hotels less than (`le`) 300 miles of a specific location, `-77.03241 38.90166`, which is Washington D.C., USA. The filter uses the `geo.distance` function to calculate the distance between the hotel location and the specified point.

:::code language="typescript" source="~/azure-search-javascript-samples/quickstart-vector-ts/src/search.ts" id="Search_vectorQueryWithGeoFilter":::

When this code is run you can see the relevant documents: 

```console
Vector search with geo filter found 2
- HotelId: 48
  HotelName: Nordick's Valley Motel
  Score: 0.6605852246284485
  City/State: Washington D.C., null
  Description: Only 90 miles (about 2 hours) from the nation's capital and nearby most everything the historic valley has to offer. Hiking? Wine Tasting? Exploring the caverns? It's all nearby and we have specially priced packages to help make our B&B your home base for fun while visiting the valley.
  Score: 0.6605852246284485

- HotelId: 49
  HotelName: Swirling Currents Hotel
  Score: 0.602634072303772
  City/State: Arlington, VA
  Description: Spacious rooms, glamorous suites and residences, rooftop pool, walking access to shopping, dining, entertainment and the city center. Each room comes equipped with a microwave, a coffee maker and a minifridge. In-room entertainment includes complimentary W-Fi and flat-screen TVs.
  Score: 0.602634072303772
```

## Create a hybrid search

Continue to add to the `./src/search.ts` file for the vector searches. A hybrid search combines keyword search with vector search. The `hybridSearch` function performs a hybrid search using the `DescriptionVector` field and a keyword search on the `Description` field.

:::code language="typescript" source="~/azure-search-javascript-samples/quickstart-vector-ts/src/search.ts" id="Search_hybridSearch":::

When this code is run you can see the relevant documents: 

```console
Hybrid search found 7 then limited to top 5
- Score: 0.03279569745063782
  HotelId: 4
  HotelName: Sublime Palace Hotel
  Description: Sublime Palace Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Cliff is part of a lovingly restored 19th century resort, updated for every modern convenience.
  Category: Boutique
  Tags: ["concierge","view","air conditioning"]

- Score: 0.032522473484277725
  HotelId: 13
  HotelName: Luxury Lion Resort
  Description: Unmatched Luxury. Visit our downtown hotel to indulge in luxury accommodations. Moments from the stadium and transportation hubs, we feature the best in convenience and comfort.
  Category: Luxury
  Tags: ["bar","concierge","restaurant"]

- Score: 0.03205128386616707
  HotelId: 48
  HotelName: Nordick's Valley Motel
  Description: Only 90 miles (about 2 hours) from the nation's capital and nearby most everything the historic valley has to offer. Hiking? Wine Tasting? Exploring the caverns? It's all nearby and we have specially priced packages to help make our B&B your home base for fun while visiting the valley.
  Category: Boutique
  Tags: ["continental breakfast","air conditioning","free wifi"]

- Score: 0.0317460335791111
  HotelId: 49
  HotelName: Swirling Currents Hotel
  Description: Spacious rooms, glamorous suites and residences, rooftop pool, walking access to shopping, dining, entertainment and the city center. Each room comes equipped with a microwave, a coffee maker and a minifridge. In-room entertainment includes complimentary W-Fi and flat-screen TVs.
  Category: Suite
  Tags: ["air conditioning","laundry service","24-hour front desk service"]

- Score: 0.03125
  HotelId: 2
  HotelName: Old Century Hotel
  Description: The hotel is situated in a nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts. The hotel also regularly hosts events like wine tastings, beer dinners, and live music.
  Category: Boutique
  Tags: ["pool","free wifi","air conditioning","concierge"]
```

## Create a semantic hybrid search

Continue to add to the `./src/search.ts` file for the vector searches. A semantic hybrid search combines semantic search with vector search. The `semanticHybridSearch` function performs a semantic hybrid search using the `DescriptionVector` field and a semantic search on the `Description` field.

:::code language="typescript" source="~/azure-search-javascript-samples/quickstart-vector-ts/src/search.ts" id="Search_semanticHybridSearch":::

When this code is run you can see the relevant documents: 

```console
Semantic hybrid search found 7 then limited to top 5
- Score: 0.0317460335791111
  Re-ranker Score: 2.6550590991973877
  HotelId: 49
  HotelName: Swirling Currents Hotel
  Description: Spacious rooms, glamorous suites and residences, rooftop pool, walking access to shopping, dining, entertainment and the city center. Each room comes equipped with a microwave, a coffee maker and a minifridge. In-room entertainment includes complimentary W-Fi and flat-screen TVs.
  Category: Suite

- Score: 0.03279569745063782
  Re-ranker Score: 2.599761724472046
  HotelId: 4
  HotelName: Sublime Palace Hotel
  Description: Sublime Palace Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Cliff is part of a lovingly restored 19th century resort, updated for every modern convenience.
  Category: Boutique

- Score: 0.03125
  Re-ranker Score: 2.3480887413024902
  HotelId: 2
  HotelName: Old Century Hotel
  Description: The hotel is situated in a nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts. The hotel also regularly hosts events like wine tastings, beer dinners, and live music.
  Category: Boutique

- Score: 0.016393441706895828
  Re-ranker Score: 2.2718777656555176
  HotelId: 1
  HotelName: Stay-Kay City Hotel
  Description: This classic hotel is fully-refurbished and ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Times Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.
  Category: Boutique

- Score: 0.01515151560306549
  Re-ranker Score: 2.0582215785980225
  HotelId: 3
  HotelName: Gastronomic Landscape Hotel
  Description: The Gastronomic Hotel stands out for its culinary excellence under the management of William Dough, who advises on and oversees all of the Hotel’s restaurant services.
  Category: Suite
```

### Create the documents 

The code in the previous section creates a vector index and uploads documents to it. The documents contain hotel information, including a vectorized description field. The vectorized description is created using an embedding model from Azure OpenAI.

Create a `documents.ts` file in the `src` directory with the following code.

:::code language="typescript" source="~/azure-search-javascript-samples/quickstart-vector-ts/src/documents.ts" :::    

### Create the vector query string

In this section, you create a vector query string that is semantically similar to the search string. The vector query string is vectorized into a mathematical representation that can be used for similarity search.

Create a `queryVector.ts` file in the `src` directory with the following code.

:::code language="typescript" source="~/azure-search-javascript-samples/quickstart-vector-ts/src/queryVector.ts" :::

### Create the main function 

The main function orchestrates the creation of the index, uploading documents, and running vector searches. It calls the functions defined in the previous sections to perform these operations.

Create a `index.ts` file in the `src` directory with the following code.

:::code language="typescript" source="~/azure-search-javascript-samples/quickstart-vector-ts/src/index.ts" :::

## Run the quickstart

To run the quickstart, you need to compile the TypeScript code to JavaScript and then execute the main function.

1. Build the TypeScript code to JavaScript.

   ```bash
   tsc
   ```

   This command compiles the TypeScript code in the `src` directory and outputs the JavaScript files in the `dist` directory.


1. Run the following command in a terminal to execute the quickstart:

    ```bash
    node -r dotenv/config dist/query.js
    ```

    The `.env` is passed into the runtime using the `-r dotenv/config`. 


1. The output is presented in each section above next to the code that produces it. 


## Clean up

When you're working in your own subscription, it's a good idea at the end of a project to identify whether you still need the resources you created. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

You can find and manage resources in the Azure portal by using the **All resources** or **Resource groups** link in the leftmost pane.

## Next steps

- Review the repository of code samples for vector search capabilities in Azure AI Search for [JavaScript](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-javascript)
-