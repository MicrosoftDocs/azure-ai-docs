---
author: KarlErickson
ms.author: karler
ms.service: azure-ai-search
ms.custom: devx-track-java, dev-focus
ms.topic: include
ms.date: 01/14/2026
ai-usage: ai-assisted
---

In this quickstart, you use Java to create, load, and query a [vector index](../../vector-store.md). The code performs these operations by using the [Azure AI Search client library for Java](/java/api/overview/azure/search-documents-readme), which provides an abstraction over the REST APIs to access index operations.

In Azure AI Search, a vector index has an index schema that defines vector and nonvector fields, a vector search configuration for algorithms that create the embedding space, and settings on vector field definitions that are evaluated at query time. [Indexes - Create or Update](/rest/api/searchservice/indexes/create-or-update) (REST API) creates the vector index.

> [!NOTE]
> This quickstart omits the vectorization step and provides inline embeddings. If you want to add [built-in data chunking and vectorization](../../vector-search-integrated-vectorization.md) over your own content, try the [**Import data (new)** wizard](../../search-get-started-portal-import-vectors.md) for an end-to-end walkthrough.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](../../search-create-service-portal.md).

    + You can use the Free tier for most of this quickstart, but we recommend Basic or higher for larger data files.

    + For [keyless authentication](../../search-get-started-rbac.md) with Microsoft Entra ID, assign the **Search Index Data Contributor role** to your user account.
    
    + To run the semantic hybrid query, you must [enable semantic ranker](../../semantic-how-to-enable-disable.md).

+ [Java 21 (LTS)](/java/openjdk/install).

+ [Maven](https://maven.apache.org/download.cgi).

## Get service information

In the remaining sections, you set up API calls to Azure OpenAI and Azure AI Search. Get the service endpoints so that you can provide them as variables in your code.

To get the service endpoint:

1. Sign in to the [Azure portal](https://portal.azure.com).

1. [Find your search service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices).

1. On the **Overview** home page, copy the URL. An example endpoint might look like `https://example.search.windows.net`.

## Set up the Java project

1. Create a new Maven project directory.

   ```bash
   mkdir vector-quickstart && cd vector-quickstart
   ```

1. Create a `pom.xml` file with required dependencies.

   :::code language="xml" source="~/azure-search-java-samples/quickstart-vector-search/pom.xml" :::

1. Compile the project to resolve the dependencies.

    ```bash
    mvn compile
    ```

1. Create the source directory structure.

   ```bash
   mkdir -p src/main/java/com/example/search
   mkdir -p src/main/resources
   ```

1. Create an `application.properties` file in the `src/main/resources` directory and provide your search service endpoint.

    ```properties
    azure.search.endpoint=<YOUR AZURE AI SEARCH ENDPOINT>
    azure.search.index-name=hotels-vector-quickstart
    ```

## Sign in to Azure

You're using Microsoft Entra ID and role assignments for the connection. Make sure you're logged in to the same tenant and subscription as Azure AI Search and Azure OpenAI. You can use the Azure CLI on the command line to show current properties, change properties, and to sign in. For more information, see [Connect without keys](../../search-get-started-rbac.md).

Run each of the following commands in sequence.

```azurecli
az account show

az account set --subscription <PUT YOUR SUBSCRIPTION ID HERE>

az login --tenant <PUT YOUR TENANT ID HERE>
```

You should now be logged in to Azure from your local device.

## Create a vector index

In this section, you create a vector index in Azure AI Search with [SearchIndexClient](/java/api/com.azure.search.documents.indexes.searchindexclient).[createOrUpdateIndex](/java/api/com.azure.search.documents.indexes.searchindexclient#com-azure-search-documents-indexes-searchindexclient-createorupdateindex(com-azure-search-documents-indexes-models-searchindex)). The index schema defines the fields, including the vector field `DescriptionVector`.

To create a vector index:

1. Create a `CreateIndex.java` file in the the `src/main/java/com/example/search` directory.

1. Copy the following code into the file.

   :::code language="java" source="~/azure-search-java-samples/quickstart-vector-search/src/main/java/com/example/search/CreateIndex.java" :::

   The code file creates the index and defines the index schema, including the `DescriptionVector` vector field.

1. Run the file.

    ```bash
    mvn compile exec:java -Dexec.mainClass="com.example.search.CreateIndex"
    ```

    The output of this code shows that the index is created successfully.

    ```output
    Using Azure Search endpoint: https://<search-service-name>.search.windows.net
    Using Azure Search index: <vector-index-name>
    Creating index...
    hotels-vector-quickstart created
    ```

   Key takeaways:

   + You define an index by creating a list of fields.

   + This particular index supports multiple search capabilities, such as:

      + Full-text keyword search (`setSearchable`)

      + Vector search (enables hybrid search by collocating vector and nonvector fields) fields (`DescriptionVector` with `setVectorSearchProfileName`)
      
      + Semantic search 

      + Faceted search (`SearchSuggester`)

      + Geo-spatial search (`Location` field with `SearchFieldDataType.GEOGRAPHY_POINT`)

      + Filtering, sorting (many fields marked filterable and sortable)

## Upload documents to the index

Creating and loading the index are separate steps. You created the index schema in the previous step. You now need to load documents into the index with [SearchClient](/java/api/com.azure.search.documents.searchclient).[uploadDocuments](/java/api/com.azure.search.documents.searchclient#com-azure-search-documents-searchclient-uploaddocuments(java-lang-iterable(-))). The documents contain the vectorized version of the article's description, which enables similarity search based on meaning rather than exact keywords.

In Azure AI Search, the index stores all searchable content, while the search engine executes queries against that index.

To upload documents to the index:

1. Create an `UploadDocuments.java` file in the `src/main/java/com/example/search` directory.

1. Copy the following code into the file.

   :::code language="java" source="~/azure-search-java-samples/quickstart-vector-search/src/main/java/com/example/search/UploadDocuments.java" :::

    This code loads a collection of documents. Each document includes the vectorized version of the article's `Description`. This vector enables similarity search, where matching is based on meaning rather than exact keywords.

    Because this quickstart article searches the index immediately, the `waitUntilIndexed` method waits until the index is ready for search operations. This is important because the index needs to be fully populated with documents before you can perform searches.

1. Build and run the file.

    ```bash
    mvn compile exec:java -Dexec.mainClass="com.example.search.UploadDocuments"
    ```

    The output of this code shows that the documents are indexed and ready for search.

    ```output
    Using Azure Search endpoint: https://<search-service-name>.search.windows.net
    Using Azure Search index: <vector-index-name>
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

    Key takeaways:

    * Your code interacts with a specific search index hosted in your Azure AI Search service through the `SearchClient`. The `SearchClient` provides access to operations such as:

        * Data ingestion: `uploadDocuments`, `mergeDocuments`, `deleteDocuments`, and so on.

        * Search operations: `search`, `autocomplete`, `suggest`

    * Vector fields contain floating point values. The dimensions attribute has a minimum of 2 and a maximum of 4096 floating point values each. This quickstart sets the dimensions attribute to 1,536 because that's the size of embeddings generated by the `text-embedding-ada-002` model.

## Create the query as a vector

The example vector queries are based on two strings:

+ Search string: `historic hotel walk to restaurants and shopping`
+ Vector query string: `quintessential lodging near running trails, eateries, retail` (vectorized into a mathematical representation)

The vector query string is semantically similar to the search string, but it includes terms that don't exist in the search index. If you do a keyword search for `quintessential lodging near running trails, eateries, retail`, results are zero. We use this example to show how you can get relevant results even if there are no matching terms.

Create a `QueryVector.java` file in the `src/main/java/com/example/search` directory and add the code to create the query vector.

:::code language="java" source="~/azure-search-java-samples/quickstart-vector-search/src/main/java/com/example/search/QueryVector.java" :::

This code is used in the following sections to perform vector searches. The query vector is created using an embedding model from Azure OpenAI.

## Create a single vector search

The first example demonstrates a basic scenario where you want to find document descriptions that closely match the search string using the [SearchClient](/java/api/com.azure.search.documents.searchclient).[search](/java/api/com.azure.search.documents.searchasyncclient#com-azure-search-documents-searchasyncclient-search(java-lang-string)) and the [VectorQuery](/java/api/com.azure.search.documents.models.vectorquery) and [SearchOptions](/java/api/com.azure.search.documents.models.searchoptions).

To create a single vector search:

1. Create a `SearchSingle.java` file in the `src/main/java/com/example/search` directory.

1. Copy the following code into the file.

    :::code language="java" source="~/azure-search-java-samples/quickstart-vector-search/src/main/java/com/example/search/SearchSingle.java" :::

    The `vectorQuery` contains the configuration of the vectorized query including the vectorized text of the query input as retrieved through `QueryVector.getVectorList`. `setFields` determines which vector fields are searched and `setKNearestNeighborsCount` specifies the number of nearest neighbors to return.

    The vector query string is `quintessential lodging near running trails, eateries, retail`, which is vectorized into 1,536 embeddings for this query.

1. Build and run the file.

    ```bash
    mvn compile exec:java -Dexec.mainClass="com.example.search.SearchSingle"
    ```

    The output of this code shows the relevant docs for the query `quintessential lodging near running trails, eateries, retail`.

    ```output
    Using Azure Search endpoint: https://<search-service-name>.search.windows.net
    Using Azure Search index: <vector-index-name>
    
    Single Vector search found 5
    - HotelId: 48, HotelName: Nordick's Valley Motel, Tags: ["continental breakfast","air conditioning","free wifi"], Score 0.6605852
    - HotelId: 13, HotelName: Luxury Lion Resort, Tags: ["bar","concierge","restaurant"], Score 0.6333684
    - HotelId: 4, HotelName: Sublime Palace Hotel, Tags: ["concierge","view","air conditioning"], Score 0.605672
    - HotelId: 49, HotelName: Swirling Currents Hotel, Tags: ["air conditioning","laundry service","24-hour front desk service"], Score 0.6026341
    - HotelId: 2, HotelName: Old Century Hotel, Tags: ["pool","free wifi","air conditioning","concierge"], Score 0.57902366
    ```

    The response for the vector equivalent of `quintessential lodging near running trails, eateries, retail` consists of 5 results with only the fields specified by the select returned.

## Create a single vector search with a filter

You can add filters, but the filters are applied to the nonvector content in your index. In this example, the filter applies to the `Tags` field to filter out any hotels that don't provide free Wi-Fi. This search uses [SearchClient](/java/api/com.azure.search.documents.searchclient).[SearchClient](/java/api/com.azure.search.documents.searchclient) and [SearchOptions](/java/api/com.azure.search.documents.models.searchoptions). 

To create a single vector search with a filter:

1. Create a `SearchSingleWithFilter.java` file in the `src/main/java/com/example/search` directory.

1. Copy the following code into the file.

    :::code language="java" source="~/azure-search-java-samples/quickstart-vector-search/src/main/java/com/example/search/SearchSingleWithFilter.java" :::

    This code has the same search functionality as the previous search, but it adds a post-processing exclusion filter for hotels with `free wifi`.

1. Build and run the file.

    ```bash
    mvn compile exec:java -Dexec.mainClass="com.example.search.SearchSingleWithFilter"
    ```

    The output of this code shows the relevant documents for the query with the filter for `free wifi` applied.

    ```output
    Using Azure Search endpoint: https://<search-service-name>.search.windows.net
    Using Azure Search index: <vector-index-name>
    
    Single Vector search found 2
    - HotelId: 48, HotelName: Nordick's Valley Motel, Tags: ["continental breakfast","air conditioning","free wifi"], Score 0.6605852
    - HotelId: 2, HotelName: Old Century Hotel, Tags: ["pool","free wifi","air conditioning","concierge"], Score 0.57902366
    ```

## Create a search with a geospatial filter

You can specify a geospatial filter to limit results to a specific geographic area. In this example, the filter limits results to hotels within 300 kilometers of Washington D.C. (coordinates: `-77.03241 38.90166`). Geospatial distances are always in kilometers. This search uses [SearchClient](/java/api/com.azure.search.documents.searchclient).[SearchClient](/java/api/com.azure.search.documents.searchclient) and [SearchOptions](/java/api/com.azure.search.documents.models.searchoptions).

To create a single vector search with a geospatial filter:

1. Create a `SearchSingleWithFilterGeo.java` file in the `src/main/java/com/example/search` directory.

1. Copy the following code into the file.

    :::code language="java" source="~/azure-search-java-samples/quickstart-vector-search/src/main/java/com/example/search/SearchSingleWithFilterGeo.java" :::

1. Build and run the file.

    ```bash
    mvn compile exec:java -Dexec.mainClass="com.example.search.SearchSingleWithFilterGeo"
    ```

    The output of this code shows the relevant documents for the query with the geospatial post-processing exclusion filter applied.

    ```output
    Using Azure Search endpoint: https://<search-service-name>.search.windows.net
    Using Azure Search index: <vector-index-name>
    
    Single Vector search found 2
    - HotelId: 48, HotelName: Nordick's Valley Motel, Tags: N/A, Score 0.6605852246284485
    - HotelId: 49, HotelName: Swirling Currents Hotel, Tags: N/A, Score 0.602634072303772
    ```

## Create a hybrid search

[Hybrid search](../../hybrid-search-overview.md) combines keyword and vector queries in one request. This example runs the following full-text and vector query strings concurrently:

+ Search string: `historic hotel walk to restaurants and shopping`
+ Vector query string: `quintessential lodging near running trails, eateries, retail` (vectorized into a mathematical representation)

This search uses [SearchClient](/java/api/com.azure.search.documents.searchclient).[SearchClient](/java/api/com.azure.search.documents.searchclient) and [SearchOptions](/java/api/com.azure.search.documents.models.searchoptions).

Tp create a hybrid search:

1. Create a `SearchHybrid.java` file in the `src/main/java/com/example/search` directory.

1. Copy the following code into the file.

    :::code language="java" source="~/azure-search-java-samples/quickstart-vector-search/src/main/java/com/example/search/SearchHybrid.java" :::

1. Build and run the file.

    ```bash
    mvn compile exec:java -Dexec.mainClass="com.example.search.SearchHybrid"
    ```

    The output of this code shows the relevant documents for the hybrid search.

    ```output
    Using Azure Search endpoint: https://<search-service-name>.search.windows.net
    Using Azure Search index: <vector-index-name>
    
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

    Because Reciprocal Rank Fusion (RRF) merges results, it helps to review the inputs. The following results are from the full-text query only. The top two results are Sublime Palace Hotel and Luxury Lion Resort. The Sublime Palace Hotel has a stronger BM25 relevance score.

    ```json
       {
           "@search.score": 2.2626662,
           "HotelName": "Sublime Palace Hotel",
           "Description": "Sublime Palace Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Palace is part of a lovingly restored 1800 palace."
       },
       {
           "@search.score": 0.86421645,
           "HotelName": "Luxury Lion Resort",
           "Description": "Unmatched Luxury.  Visit our downtown hotel to indulge in luxury accommodations. Moments from the stadium, we feature the best in comfort"
       },
    ```

    In the vector-only query, which uses HNSW for finding matches, the Sublime Palace Hotel drops to the fourth position. Luxury Lion, which was second in the full-text search and third in the vector search, doesn't experience the same range of fluctuation, so it appears as a top match in a homogenized result set.

   ```json
   "value": [
       {
           "@search.score": 0.857736,
           "HotelId": "48",
           "HotelName": "Nordick's Valley Motel",
           "Description": "Only 90 miles (about 2 hours) from the nation's capital and nearby most everything the historic valley has to offer.  Hiking? Wine Tasting? Exploring the caverns?  It's all nearby and we have specially priced packages to help make our B&B your home base for fun while visiting the valley.",
           "Category": "Boutique"
       },
       {
           "@search.score": 0.8399129,
           "HotelId": "49",
           "HotelName": "Swirling Currents Hotel",
           "Description": "Spacious rooms, glamorous suites and residences, rooftop pool, walking access to shopping, dining, entertainment and the city center.",
           "Category": "Luxury"
       },
       {
           "@search.score": 0.8383954,
           "HotelId": "13",
           "HotelName": "Luxury Lion Resort",
           "Description": "Unmatched Luxury.  Visit our downtown hotel to indulge in luxury accommodations. Moments from the stadium, we feature the best in comfort",
           "Category": "Resort and Spa"
       },
       {
           "@search.score": 0.8254346,
           "HotelId": "4",
           "HotelName": "Sublime Palace Hotel",
           "Description": "Sublime Palace Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Palace is part of a lovingly restored 1800 palace.",
           "Category": "Boutique"
       },
       {
           "@search.score": 0.82380056,
           "HotelId": "1",
           "HotelName": "Stay-Kay City Hotel",
           "Description": "The hotel is ideally located on the main commercial artery of the city in the heart of New York.",
           "Category": "Boutique"
       },
       {
           "@search.score": 0.81514084,
           "HotelId": "2",
           "HotelName": "Old Century Hotel",
           "Description": "The hotel is situated in a  nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts.",
           "Category": "Boutique"
       },
       {
           "@search.score": 0.8133763,
           "HotelId": "3",
           "HotelName": "Gastronomic Landscape Hotel",
           "Description": "The Hotel stands out for its gastronomic excellence under the management of William Dough, who advises on and oversees all of the Hotel's restaurant services.",
           "Category": "Resort and Spa"
       }
   ]
   ```

## Create a semantic hybrid search

Here's the last query in the collection to extend the semantic hybrid search with the additional search text `historic hotel walk to restaurants and shopping`.

This search uses [SearchClient](/java/api/com.azure.search.documents.searchclient).[SearchClient](/java/api/com.azure.search.documents.searchclient) and [SearchOptions](/java/api/com.azure.search.documents.models.searchoptions). 

To create a semantic hybrid search:

1. Create a `SearchSemanticHybrid.java` file in the `src/main/java/com/example/search` directory.

1. Copy the following code into the file.

    :::code language="java" source="~/azure-search-java-samples/quickstart-vector-search/src/main/java/com/example/search/SearchSemanticHybrid.java" :::

1. Build and run the file.

    ```bash
    mvn compile exec:java -Dexec.mainClass="com.example.search.SearchSemanticHybrid"
    ```

    The output of this code shows the relevant documents for the semantic hybrid search.

    ```output
    Using Azure Search endpoint: https://<search-service-name>.search.windows.net
    Using Azure Search index: <vector-index-name>
    
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
      Description: The Gastronomic Hotel stands out for its culinary excellence under the management of William Dough, who advises on and oversees all of the Hotel's restaurant services.
      Category: Suite
    ```

    You can think of the semantic ranking as a way to improve the relevance of search results by understanding the meaning behind the words in the query and the content of the documents. In this case, the semantic ranking helps to identify hotels that are not only relevant to the keywords but also match the intent of the query:

    Key takeaways:

    - Vector search is specified through the `VectorSearchOptions` class. Keyword search is specified through the `SemanticSearchOptions` class.

    - In a hybrid search, you can integrate vector search with full-text search over keywords. Filters, spell check, and semantic ranking apply to textual content only, and not vectors. In this final query, there's no semantic `answer` because the system didn't produce one that was sufficiently strong.

    - Actual results include more detail, including semantic captions and highlights. Results were modified for readability. To get the full structure of the response, run the request in the REST client.

## Clean up resources

When you're working in your own subscription, it's a good idea at the end of a project to identify whether you still need the resources you created. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

You can find and manage resources in the Azure portal by using the **All resources** or **Resource groups** link in the leftmost pane.

Alternatively, to delete the vector index you created in this quickstart programmatically:

1. Create a `DeleteIndex.java` file in the `src/main/java/com/example/search` directory.

1. Add the following code to the file.

    :::code language="java" source="~/azure-search-java-samples/quickstart-vector-search/src/main/java/com/example/search/DeleteIndex.java" :::

1. Build and run the file.

    ```bash
    mvn compile exec:java -Dexec.mainClass="com.example.search.DeleteIndex"
    ```

## Next steps

+ Review the repository of code samples for vector search capabilities in Azure AI Search for [Java](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-java).
