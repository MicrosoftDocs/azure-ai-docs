---
manager: nitinme
author: rotabor
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 01/14/2026
ms.custom: dev-focus
ai-usage: ai-assisted
---

In this quickstart, you use a .NET app to create, populate, and query a [vector index](../../vector-store.md). The code performs these operations by using the [Azure AI Search client library for .NET](/dotnet/api/overview/azure/search), which provides an abstraction over the REST APIs for access to index operations.

In Azure AI Search, a vector index has an index schema that defines vector and nonvector fields, a vector search configuration for algorithms that create the embedding space, and settings on vector field definitions that are evaluated at query time. [Indexes - Create or Update](/rest/api/searchservice/indexes/create-or-update) (REST API) creates the vector index.

> [!NOTE]
> This quickstart omits the vectorization step and provides inline embeddings. If you want to add [built-in data chunking and vectorization](../../vector-search-integrated-vectorization.md) over your own content, try the [**Import data (new)** wizard](../../search-get-started-portal-import-vectors.md) for an end-to-end walkthrough.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](../../search-create-service-portal.md).

    + You can use the Free tier for most of this quickstart, but we recommend Basic or higher for larger data files.

    + For [keyless authentication](../../search-get-started-rbac.md) with Microsoft Entra ID, assign the **Search Index Data Contributor role** to your user account or service principal.
    
    + To run the semantic hybrid query, you must [enable semantic ranker](../../semantic-how-to-enable-disable.md).

+ [Visual Studio Code](https://code.visualstudio.com/download) or [Visual Studio](https://visualstudio.com") to run the code.

+ [Git](https://git-scm.com/downloads) to clone the sample repo.

## Get service information

Requests to the search endpoint must be authenticated and authorized. While it's possible to use API keys for this task, we recommend [using a keyless connection via Microsoft Entra ID](../../search-get-started-rbac.md).

This quickstart uses `DefaultAzureCredential`, which simplifies authentication in both development and production scenarios. However, for production scenarios, you might have more advanced requirements that require a different approach. To understand all of your options, see [Authenticate .NET apps to Azure services by using the Azure SDK for .NET](/dotnet/azure/sdk/authentication/).

## Clone the code and setup environment

1. Clone the repo containing the code for this quickstart.

   ```bash
   git clone https://github.com/Azure-Samples/azure-search-dotnet-samples
   ```

1. Open the `quickstart-vector-search` folder in Visual Studio Code or double-click the `VectorSearchQuickstart.sln` file to open the solution in Visual Studio.

1. Open `appsettings.json` in both `VectorSearchCreatePopulateIndex` and `VectorSearchExamples` folders. 

1. Set `Endpoint` to your search service URL, which should be similar to `https://mydemo.search.windows.net`.

1. Set `IndexName` to a unique name for your index. You can also use the default `hotels-vector-quickstart` name.

## Create the vector index and upload documents

To run search queries against your Azure AI Search service, you must first create a search index and upload documents to the index.

To create and populate the index:

1. Open a terminal in the `VectorSearchCreatePopulateIndex` folder.

1. Use the `dotnet run` command to run the project.

    ```dotnetcli
    dotnet run
    ```

    The following code executes to create an index:
    
    :::code language="csharp" source="~/azure-search-dotnet-samples/quickstart-vector-search/vectorsearchcreatepopulateindex/program.cs" id="CreateSearchindex":::
    
    The following code uploads JSON-formatted documents in the `hotel-samples.json` file to your search service.
    
    :::code language="csharp" source="~/azure-search-dotnet-samples/quickstart-vector-search/vectorsearchcreatepopulateindex/program.cs" id="UploadDocs":::
    
    After you run the project, the following output is printed.
    
    ```output
    Key: 1, Succeeded: True
    Key: 2, Succeeded: True
    Key: 3, Succeeded: True
    Key: 4, Succeeded: True
    Key: 48, Succeeded: True
    Key: 49, Succeeded: True
    Key: 13, Succeeded: True
    ```
    
    Key takeaways:

    + Your code interacts with a specific search index hosted in your Azure AI Search service through the SearchClient, which is the main object provided by the azure-search-documents package. The SearchClient provides access to index operations such as:

        + Data ingestion: `UploadDocuments()`, `MergeDocuments()`, `DeleteDocuments()`

        + Search operations: `Search()`, `Autocomplete()`, `Suggest()`
        
        + Index management operations: `CreateOrUpdateIndex()`
    
    + Vector fields contain floating point values. The dimensions attribute has a minimum of 2 and a maximum of 4096 floating point values each. This quickstart sets the dimensions attribute to 1,536 because that's the size of embeddings generated by the `text-embedding-ada-002` model.

## Run search queries

To issue the vector queries in this section, open `Program.cs` in the `VectorSearchExamples` folder, and then open a terminal in the `VectorSearchExamples` folder.

Queries in this section:

+ [Single vector search](#single-vector-search)
+ [Single vector search with filter](#single-vector-search-with-filter)
+ [Hybrid search](#hybrid-search)
+ [Semantic hybrid search with filter](#semantic-hybrid-search-with-a-filter)

### Single vector search

The first query demonstrates a basic scenario where you want to find document descriptions that closely match the search string.

To issue a single vector search:

1. In the `Program.cs` file of the `VectorSearchExamples` folder, uncomment the `SearchExamples.SearchSingleVector(searchClient, vectorizedResult);` method call.

    This method executes the following search function in the `SearchExamples.cs` class.

    :::code language="csharp" source="~/azure-search-dotnet-samples/quickstart-vector-search/vectorsearchexamples/SearchExamples.cs" id="SearchSingleVector":::

1. Run `dotnet run` to execute the query, which returns the following results.
    
    ```output
    Single Vector Search Results:
    Score: 0.6605852, HotelId: 48, HotelName: Nordick's Valley Motel
    Score: 0.6333684, HotelId: 13, HotelName: Luxury Lion Resort
    Score: 0.605672, HotelId: 4, HotelName: Sublime Palace Hotel
    Score: 0.6026341, HotelId: 49, HotelName: Swirling Currents Hotel
    Score: 0.57902366, HotelId: 2, HotelName: Old Century Hotel
    ```

### Single vector search with filter

In Azure AI Search, [filters](../../vector-search-filters.md) apply to nonvector fields in an index. This example filters on the `Tags` field to filter out any hotels that don't provide free Wi-Fi.

To issue a single vector search with a filter:

1. In the `Program.cs` file of the `VectorSearchExamples` folder, uncomment the `SearchExamples.SearchSingleVectorWithFilter(searchClient, vectorizedResult);` method call.

    This method executes the following search function in the `SearchExamples.cs` class.

    :::code language="csharp" source="~/azure-search-dotnet-samples/quickstart-vector-search/vectorsearchexamples/SearchExamples.cs" id="SearchSingleVectorWithFilter":::

1.  Run `dotnet run` to execute the query, which returns only hotels that provide free Wi-Fi. 
    
       ```output
        Single Vector Search With Filter Results:
        Score: 0.6605852, HotelId: 48, HotelName: Nordick's Valley Motel, Tags: continental breakfastair conditioningfree wifi
        Score: 0.57902366, HotelId: 2, HotelName: Old Century Hotel, Tags: poolfree wifiair conditioningconcierge
       ```

1. For a [geo filter](/dotnet/api/azure.search.documents.models.searchfilter.create), uncomment `SearchExamples.SingleSearchWithGeoFilter(searchClient, vectorizedResult);` in `Program.cs`.

    This method executes the following search function in the `SearchExamples.cs` class.

    :::code language="csharp" source="~/azure-search-dotnet-samples/quickstart-vector-search/vectorsearchexamples/SearchExamples.cs" id="SingleSearchWithGeoFilter":::

1.  Run `dotnet run` to execute the query, which returns only hotels within 300 km.
   
    ```output
    Vector query with a geo filter:
    -HotelId: 48
    HotelName: Nordick's Valley Motel
    Score: 0.6605852246284485
    City/State: Washington D.C./null
    Description: Only 90 miles (about 2 hours) from the nation's capital and nearby most everything the historic valley has to offer. Hiking? Wine Tasting? Exploring the caverns? It's all nearby and we have specially priced packages to help make our B&B your home base for fun while visiting the valley.
    
    -HotelId: 49
    HotelName: Swirling Currents Hotel
    Score: 0.602634072303772
    City/State: Arlington/VA
    Description: Spacious rooms, glamorous suites and residences, rooftop pool, walking access to shopping, dining, entertainment and the city center. Each room comes equipped with a microwave, a coffee maker and a minifridge. In-room entertainment includes complimentary Wi-Fi and flat-screen TVs.
    ```

### Hybrid search

[Hybrid search](../../hybrid-search-overview.md) combines keyword and vector queries in one request. This example runs the following full-text and vector query strings concurrently:

+ Search string: `historic hotel walk to restaurants and shopping`
+ Vector query string: `quintessential lodging near running trails, eateries, retail` (vectorized into a mathematical representation)

To issue a hybrid search:

1. In the `Program.cs` file, uncomment the `SearchExamples.SearchHybridVectorAndText(searchClient, vectorizedResult);` method call.

    This method executes the following search function in the `SearchExamples.cs` class.

    :::code language="csharp" source="~/azure-search-dotnet-samples/quickstart-vector-search/vectorsearchexamples/SearchExamples.cs" id="SearchHybridVectorAndText":::

1.  Run `dotnet run` to execute the query, which returns the following results.

       ```output
       Hybrid search results:
       Score: 0.03279569745063782
       HotelId: 4
       HotelName: Sublime Palace Hotel
       Description: Sublime Palace Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Cliff is part of a lovingly restored 19th   century resort, updated for every modern convenience.
       Category: Boutique
       Tags: conciergeviewair conditioning
       
       Score: 0.032786883413791656
       HotelId: 13
       HotelName: Luxury Lion Resort
       Description: Unmatched Luxury. Visit our downtown hotel to indulge in luxury accommodations. Moments from the stadium and transportation hubs, we feature the best in convenience and comfort.
       Category: Luxury
       Tags: barconciergerestaurant
       
       Score: 0.03205128386616707
       HotelId: 48
       HotelName: Nordick's Valley Motel
       Description: Only 90 miles (about 2 hours) from the nation's capital and nearby most everything the historic valley has to offer. Hiking? Wine Tasting? Exploring the caverns? It's all nearby and we have specially priced packages to help make our B&B your home base for fun while visiting the valley.
       Category: Boutique
       Tags: continental breakfastair conditioningfree wifi
       
       Score: 0.0317460335791111
       HotelId: 49
       HotelName: Swirling Currents Hotel
       Description: Spacious rooms, glamorous suites and residences, rooftop pool, walking access to shopping, dining, entertainment and the city center. Each room comes equipped with a microwave, a coffee maker and a minifridge. In-room entertainment includes complimentary W-Fi and flat-screen TVs.
       Category: Suite
       Tags: air conditioninglaundry service24-hour front desk service
       
       Score: 0.03077651560306549
       HotelId: 2
       HotelName: Old Century Hotel
       Description: The hotel is situated in a nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts. The hotel also regularly hosts events like wine tastings, beer   dinners, and live music.
       Category: Boutique
       Tags: poolfree wifiair conditioningconcierge
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
            "Description": "The Hotel stands out for its gastronomic excellence under the management of William Dough, who advises on and oversees all of the Hotel’s restaurant services.",
            "Category": "Resort and Spa"
        }
    ]
    ```

### Semantic hybrid search with a filter

Add [semantic ranking](../../semantic-search-overview.md) to rerank results based on language understanding.

To issue a semantic hybrid search with a filter:

1. In the `Program.cs` file, uncomment `SearchExamples.SearchHybridVectorAndSemantic(searchClient, vectorizedResult);` method call.

    This method executes the following search function in the `SearchExamples.cs` class.

    :::code language="csharp" source="~/azure-search-dotnet-samples/quickstart-vector-search/vectorsearchexamples/SearchExamples.cs" id="SearchHybridVectorAndSemantic":::

1. Run `dotnet run` to execute the query, which returns the following hotels. The hotels are filtered by location, faceted by `StateProvince`, and semantically reranked to promote results that are closest to the search string query (`historic hotel walk to restaurants and shopping`).

    The Swirling Currents Hotel now moves to the top spot. Without semantic ranking, Nordick's Valley Motel is number one. With semantic ranking, the machine comprehension models recognize that `historic` applies to "hotel within walking distance to dining (restaurants) and shopping."
    
    ```output
    Total semantic hybrid results: 7
    - Score: 0.0317460335791111
      Re-ranker Score: 2.6550590991973877
      HotelId: 49
      HotelName: Swirling Currents Hotel
      Description: Spacious rooms, glamorous suites and residences, rooftop pool, walking access to shopping, dining, entertainment and the city center. Each room comes equipped with a microwave, a coffee maker and a minifridge. In-room entertainment includes complimentary Wi-Fi and flat-screen TVs.
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
      Description: This classic hotel is fully-refurbished and ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Times Square and the historic center of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.
      Category: Boutique
    - Score: 0.01515151560306549
      Re-ranker Score: 2.0582215785980225
      HotelId: 3
      HotelName: Gastronomic Landscape Hotel
      Description: The Gastronomic Hotel stands out for its culinary excellence under the management of William Dough, who advises on and oversees all of the Hotel's restaurant services.
      Category: Suite
    ```
    
    Key takeaways:

    + In a hybrid search, you can integrate vector search with full-text search over keywords. Filters, spell check, and semantic ranking apply to textual content only, and not vectors. In this final query, there's no semantic `answer` because the system didn't produce one that was sufficiently strong.
    
    + Actual results include more detail, including semantic captions and highlights. Results were modified for readability. To get the full structure of the response, run the request in the REST client.

## Clean up resources

When you're working in your own subscription, it's a good idea at the end of a project to identify whether you still need the resources you created. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

You can find and manage resources in the Azure portal by using the **All resources** or **Resource groups** link in the leftmost pane.

## Next steps

+ Review the repository of code samples for vector search capabilities in Azure AI Search for [.NET](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-dotnet)
+ Review the other .NET and Azure AI Search code samples in the [azure-search-dotnet-samples repo](https://github.com/Azure-Samples/azure-search-dotnet-samples)