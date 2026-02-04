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

In this quickstart, you use a Jupyter notebook to create, load, and query a [vector index](../../vector-store.md). The code performs these operations by using the [Azure AI Search client library for Python](/python/api/overview/azure/search-documents-readme), which provides an abstraction over the REST APIs to access index operations.

In Azure AI Search, a vector index has an index schema that defines vector and nonvector fields, a vector search configuration for algorithms that create the embedding space, and settings on vector field definitions that are evaluated at query time. [Indexes - Create or Update](/rest/api/searchservice/indexes/create-or-update) (REST API) creates the vector index.

> [!NOTE]
> This quickstart omits the vectorization step and provides inline embeddings. If you want to add [built-in data chunking and vectorization](../../vector-search-integrated-vectorization.md) over your own content, try the [**Import data (new)** wizard](../../search-get-started-portal-import-vectors.md) for an end-to-end walkthrough.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](../../search-create-service-portal.md).

    + You can use the Free tier for most of this quickstart, but we recommend Basic or higher for larger data files.

    + For [keyless authentication](../../search-get-started-rbac.md) with Microsoft Entra ID, assign the **Search Index Data Contributor role** to your user account.
    
    + To run the semantic hybrid query, you must [enable semantic ranker](../../semantic-how-to-enable-disable.md).

+ The latest version of [Python](https://www.python.org/downloads/).

+ [Visual Studio Code](https://code.visualstudio.com/download) with the [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) extensions.

+ [Git](https://git-scm.com/downloads) to clone the sample repo.

## Get service information

Requests to the search endpoint must be authenticated and authorized. While it's possible to use API keys for this task, we recommend [using a keyless connection via Microsoft Entra ID](../../search-get-started-rbac.md).

This quickstart uses `DefaultAzureCredential`, which simplifies authentication in both development and production scenarios. However, for production scenarios, you might have more advanced requirements that require a different approach. See [Authenticate Python apps to Azure services by using the Azure SDK for Python](/azure/developer/python/sdk/authentication/overview) to understand all of your options.

## Clone the code and setup environment

1. Clone the repo containing the code for this quickstart. 

   ```bash
   git clone https://github.com/Azure-Samples/azure-search-python-samples
   ```
  
1. In Visual Studio Code, open the `Quickstart-Vector-Search` folder.

1. Rename the `sample.env` file to `.env`.

1. Set `AZURE_SEARCH_ENDPOINT` to your search service URL, which should be similar to `https://mydemo.search.windows.net`.

1. Set `AZURE_SEARCH_INDEX_NAME` to a unique name for your index. You can also use the default `vector-search-quickstart` name.

1. Select **View** > **New Terminal**, and then run the following commands to create and activate a virtual environment.

   ```bash
   python -m venv .venv
   source .venv/scripts/activate
   where python
   ```
   
   > [!Note] 
   > + This step assumes you're using Git Bash in your terminal and running on Windows. If you're using a different shell and/or operating system, adjust these instructions to your specific environment.
   >
   > + The `where python` command validates that you're working from the virtual environment by listing `python.exe` in the `Quickstart-Vector-Search\.venv\` folder and other locations from your machine's directory.

1. If prompted, allow Visual Studio Code to use the new environment.

1. Install the required libraries.

   ```bash
   pip install requirements.txt
   ```

1. Open the `vector-search-quickstart.ipynb` file.

1. Run the `Install packages and set variables` code cell to load the environment variables.

   ```python
   # Load environment variables from .env file
   # Rename the samples.env to .env and fill in the values
   from azure.identity import DefaultAzureCredential
   from dotenv import load_dotenv
   import os

   load_dotenv(override=True) # take environment variables from .env.

   search_endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
   credential = DefaultAzureCredential()
   index_name = os.getenv("AZURE_SEARCH_INDEX", "vector-search-quickstart")

   print(f"Using Azure Search endpoint: {search_endpoint}")
   print(f"Using Azure Search index: {index_name}")
   !pip list 
   ```
   The output includes some of the installed packages.

   ```output
   Using Azure Search endpoint: https://<search-service-name>.search.windows.net
   Using Azure Search index: <vector-index-name>
   Package                 Version
   ----------------------- -----------
   aiohappyeyeballs        2.6.1
   aiohttp                 3.12.13
   aiosignal               1.3.2
   asttokens               3.0.0
   attrs                   25.3.0
   azure-ai-agents         1.0.0
   azure-ai-projects       1.0.0b11
   azure-common            1.1.28
   azure-core              1.34.0
   azure-identity          1.23.0
   azure-search-documents  11.6.0b12
   azure-storage-blob      12.25.1
   ...
   ```
  
## Create a vector index

The code in `vector-search-quickstart.ipynb` uses several methods from the `azure.search.documents` library to create the vector index and searchable fields.

To create the vector index:

1. Run the `Create an index` code cell.

   ```python
   from azure.search.documents.indexes import SearchIndexClient
   from azure.search.documents import SearchClient
   from azure.search.documents.models import VectorizedQuery
   from azure.search.documents.indexes.models import (
       SimpleField,
       ComplexField,
       SearchField,
       SearchFieldDataType,    
       SearchableField,
       SearchIndex,
       SemanticConfiguration,
       SemanticField,
       SemanticPrioritizedFields,
       SemanticSearch,
       VectorSearch, 
       VectorSearchProfile,
       HnswAlgorithmConfiguration,
       ExhaustiveKnnAlgorithmConfiguration    
   )
   
   # Create a search schema
   index_client = SearchIndexClient(
       endpoint=search_endpoint, credential=credential)
   fields = [
       SimpleField(name="HotelId", type=SearchFieldDataType.String, key=True, filterable=True),
       SearchableField(name="HotelName", type=SearchFieldDataType.String, sortable=True),
       SearchableField(name="Description", type=SearchFieldDataType.String),
       SearchField(
           name="DescriptionVector",
           type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
           searchable=True,
           vector_search_dimensions=1536,
           vector_search_profile_name="my-vector-profile"
       ),
       SearchableField(name="Category", type=SearchFieldDataType.String, sortable=True, filterable=True, facetable=True),
       SearchField(name="Tags", type=SearchFieldDataType.Collection(SearchFieldDataType.String), searchable=True, filterable=True, facetable=True),
       SimpleField(name="ParkingIncluded", type=SearchFieldDataType.Boolean, filterable=True, sortable=True, facetable=True),
       SimpleField(name="LastRenovationDate", type=SearchFieldDataType.DateTimeOffset, filterable=True, sortable=True, facetable=True),
       SimpleField(name="Rating", type=SearchFieldDataType.Double, filterable=True, sortable=True, facetable=True),
       ComplexField(name="Address", fields=[
           SearchableField(name="StreetAddress", type=SearchFieldDataType.String),
           SearchableField(name="City", type=SearchFieldDataType.String, filterable=True, sortable=True, facetable=True),
           SearchableField(name="StateProvince", type=SearchFieldDataType.String, filterable=True, sortable=True, facetable=True),
           SearchableField(name="PostalCode", type=SearchFieldDataType.String, filterable=True, sortable=True, facetable=True),
           SearchableField(name="Country", type=SearchFieldDataType.String, filterable=True, sortable=True, facetable=True),
       ]),
       SimpleField(name="Location", type=SearchFieldDataType.GeographyPoint, filterable=True, sortable=True),
   ]
   
   vector_search = VectorSearch(
           algorithms=[
               HnswAlgorithmConfiguration(name="my-hnsw-vector-config-1", kind="hnsw"),
               ExhaustiveKnnAlgorithmConfiguration(name="my-eknn-vector-config", kind="exhaustiveKnn")
           ],
           profiles=[
               VectorSearchProfile(name="my-vector-profile", algorithm_configuration_name="my-hnsw-vector-config-1")
           ]
       )
   
   semantic_config = SemanticConfiguration(
           name="my-semantic-config",
           prioritized_fields=SemanticPrioritizedFields(
              title_field=SemanticField(field_name="HotelName"), 
              content_fields=[SemanticField(field_name="Description")], 
              keywords_fields=[SemanticField(field_name="Category")]
           )
       )
   
   # Create the semantic settings with the configuration
   semantic_search = SemanticSearch(configurations=[semantic_config])
   
   semantic_settings = SemanticSearch(configurations=[semantic_config])
   scoring_profiles = []
   suggester = [{'name': 'sg', 'source_fields': ['Tags', 'Address/City', 'Address/Country']}]
   
   # Create the search index with the semantic settings
   index = SearchIndex(name=index_name, fields=fields, vector_search=vector_search, semantic_search=semantic_search)
   result = index_client.create_or_update_index(index)
   print(f' {result.name} created')
   ```

   If the index is created successfully, the following output is displayed below the code cell.

   ```output
   vector-search-quickstart created
   ```

   Key takeaways:

   + You define an index by creating a list of fields. Each field is created using a helper method that defines the field type and its settings.

   + This particular index supports multiple search capabilities, such as:

      + Full-text keyword search (`SearchableField(name="HotelName", ...)`, `SearchableField(name="Description", ...)`)

      + Vector search (enables hybrid search by collocating vector and nonvector fields) fields (`DescriptionVector`)

      + Semantic search (`semantic_search=SemanticSearch(configurations=[semantic_config])`)

      + Faceted search (`facetable=True`)

      + Geo-spatial search (`Location` field is `GeographyPoint`)

      + Filtering, sorting (many fields marked filterable and sortable)

## Upload documents to the index

Creating and loading the index are separate steps. You created the index schema in the previous step. You now need to load documents into the index.
 
In Azure AI Search, the index stores all searchable content, while the search engine executes queries against that index.

To upload documents to the index:

1. Run the `Create documents payload` code cell.

   ```python
      # Create a documents payload
      documents = [
          {
              "@search.action": "mergeOrUpload",
              "HotelId": "1",
              "HotelName": "Stay-Kay City Hotel",
              "Description": "This classic hotel is fully-refurbished and ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Times Square and the historic center of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.",
              "DescriptionVector": [-0.048865054,-0.020307425,
              # <truncated>
              -0.018120624,-0.012772904],
              "Category": "Boutique",
              "Tags": [
                  "view",
                  "air conditioning",
                  "concierge"
              ],
              "ParkingIncluded": "false",
              "LastRenovationDate": "2022-01-18T00:00:00Z",
              "Rating": 3.60,
              "Address": {
                  "StreetAddress": "677 5th Ave",
                  "City": "New York",
                  "StateProvince": "NY",
                  "PostalCode": "10022",
                  "Country": "USA"
              },
              "Location": {
                  "type": "Point",
                  "coordinates": [
                      -73.975403,
                      40.760586
                  ]
              }
          },
          # <truncated>
      ]
   ```
   
   This cell loads a variable named `documents` with a JSON object describing each document, along with the vectorized version of the article's description. This vector enables similarity search, where matching is based on meaning rather than exact keywords.
   
   > [!IMPORTANT]
   > The code in this example isn't runnable. Several characters or lines are removed for brevity. Instead, run the code in the Jupyter notebook.
   
1. Run the `Upload the documents` code cell.

   ```python
   # Upload documents to the index
   search_client = SearchClient(endpoint=search_endpoint,
                         index_name=index_name,
                         credential=credential)
   try:
       result = search_client.upload_documents(documents=documents)
       for r in result:
           print(f"Key: {r.key}, Succeeded: {r.succeeded}, ErrorMessage: {r.error_message}")
   except Exception as ex:
       print("Failed to upload documents:", ex)

   # Create the index client which will be used later in the query examples
   index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
   ```

   This creates an instance of the search client by calling the `SearchClient()` constructor and then calling the `upload_documents()` method on the object. 

   After you run the cell, the status of each document is printed below it.

   ```output
   Key: 1, Succeeded: True, ErrorMessage: None
   Key: 2, Succeeded: True, ErrorMessage: None
   Key: 3, Succeeded: True, ErrorMessage: None
   Key: 4, Succeeded: True, ErrorMessage: None
   Key: 48, Succeeded: True, ErrorMessage: None
   Key: 49, Succeeded: True, ErrorMessage: None
   Key: 13, Succeeded: True, ErrorMessage: None
   ```

   Key takeaways:

   + Your code interacts with a specific search index hosted in your Azure AI Search service through the `SearchClient`, which is the main object provided by the `azure-search-documents` package. The `SearchClient` provides access to index operations, such as:

      + Data ingestion: `upload_documents()`, `merge_documents()`, `delete_documents()`, etc.
      
      + Search operations: `search()`, `autocomplete()`, `suggest()`

      + Index management operations: `get_index_statistics()`, `get_document_count()`

   + Vector fields contain floating point values. The dimensions attribute has a minimum of 2 and a maximum of 4096 floating point values each. This quickstart sets the dimensions attribute to 1,536 because that's the size of embeddings generated by the `text-embedding-ada-002` model.

## Run queries

Now that documents are loaded, you can issue vector queries against them by calling `search_client.search()` and passing in a `VectorizedQuery` object, the fields you want returned, the number of results, and so on.

Queries in this section:

+ [Single vector search](#single-vector-search)
+ [Single vector search with filter](#single-vector-search-with-filter)
+ [Hybrid search](#hybrid-search)
+ [Semantic hybrid search](#semantic-hybrid-search)

### Create the vector query string

The example vector queries are based on two strings:

+ Search string: `historic hotel walk to restaurants and shopping`
+ Vector query string: `quintessential lodging near running trails, eateries, retail` (vectorized into a mathematical representation)

The vector query string is semantically similar to the search string, but it includes terms that don't exist in the search index. If you do a keyword search for `quintessential lodging near running trails, eateries, retail`, results are zero. We use this example to show how you can get relevant results even if there are no matching terms.

1. Run the `Create the vector query string` code cell. This loads the `vector` variable with the vectorized query data required to run all of the searches in the next sections.

### Single vector search

The first example demonstrates a basic scenario where you want to find document descriptions that closely match the search string.

1. Run the `Single vector search` code cell. This block contains the request to query the search index.

   ```python
   # IMPORTANT: Before you run this code, make sure the documents were successfully
   # created in the previous step. Sometimes it may take a few seconds for the index to be ready.
   # Check the "Document count" for the index in the Azure portal.
   
   # Execute vector search
   if vector:
       try:
           vector_query = VectorizedQuery(
               vector=vector,
               k_nearest_neighbors=5,
               fields="DescriptionVector",
               kind="vector",
               exhaustive=True
           )

           results = search_client.search(
               vector_queries=[vector_query],
               select=["HotelId", "HotelName", "Description", "Category", "Tags"],
               top=5,
               include_total_count=True
           )
   
           print(f"Total results: {results.get_count()}")
           for result in results:
               doc = result  # result is a dict-like object
               print(f"- HotelId: {doc['HotelId']}, HotelName: {doc['HotelName']}, Category: {doc.get('Category')}")
       except Exception as ex:
           print("Vector search failed:", ex)
   else:
      print("No vector loaded, skipping search.")
   ```

   This vector query is shortened for brevity. The `vectorQueries.vector` contains the vectorized text of the query input, `fields` determines which vector fields are searched, and `k` specifies the number of nearest neighbors to return.

   The vector query string is `quintessential lodging near running trails, eateries, retail`, which is vectorized into 1,536 embeddings for this query.

   <!-- retain numeric references to 5 and 7. Too hard to spot these values if they are written out. -->
   The response for the vector equivalent of `quintessential lodging near running trails, eateries, retail` consists of 7 results but the code specifies `top=5` so only the first 5 results are returned. Furthermore, only the fields specified by the `select` are returned. 

   `search_client.search()` returns a dict-like object. Each result provides a search score, which can be accessed using `score = result.get("@search.score", "N/A")`. While not displayed in this example, in a similarity search, the response always includes `k` results ordered by the value similarity score.

   After you run the cell, the status of each document is printed below it.

   ```output
   Total results: 5
   - HotelId: 48, HotelName: Nordick's Valley Motel, Category: Boutique
   - HotelId: 13, HotelName: Luxury Lion Resort, Category: Luxury
   - HotelId: 4, HotelName: Sublime Palace Hotel, Category: Boutique
   - HotelId: 49, HotelName: Swirling Currents Hotel, Category: Suite
   - HotelId: 2, HotelName: Old Century Hotel, Category: Boutique
   ```

### Single vector search with filter

You can add filters, but the filters are applied to the nonvector content in your index. In this example, the filter applies to the `Tags` field to filter out any hotels that don't provide free Wi-Fi.

To create a single vector search with a filter:

1. Run the `Single vector search with filter` code cell. This cell contains the request to query the search index.

    ```python
   if vector:
       try:
           vector_query = VectorizedQuery(
               vector=vector,
               k_nearest_neighbors=5,
               fields="DescriptionVector",
               kind="vector",
               exhaustive=True
           )
   
           results = search_client.search(
               vector_queries=[vector_query],
               filter="Tags/any(tag: tag eq 'free wifi')",  # <--- NOTICE THE FILTER IS ADDED HERE
               select=["HotelId", "HotelName", "Description", "Category", "Tags"],
               top=7,
               include_total_count=True
           )
   
           print(f"Total filtered results: {results.get_count()}")
           for result in results:
               doc = result
               print(f"- HotelId: {doc['HotelId']}, HotelName: {doc['HotelName']}, Tags: {doc.get('Tags')}")
       except Exception as ex:
           print("Vector search with filter failed:", ex)
   else:
       print("No vector loaded, skipping search.")
    ``` 

   After you run the cell, the status of each document is printed below it:

   ```output
   Total filtered results: 2
   - HotelId: 48, HotelName: Nordick's Valley Motel, Tags: ['continental breakfast', 'air conditioning', 'free wifi']
   - HotelId: 2, HotelName: Old Century Hotel, Tags: ['pool', 'free wifi', 'air conditioning', 'concierge']
   ```

   The query was the same as the previous [single vector search example](#single-vector-search), but it includes a post-processing exclusion filter and returns only the two hotels that have free Wi-Fi.

1. The next filter example uses a geo filter. Run the `Vector query with a geo filter` code cell. This block contains the request to query the search index.

   ```python
   if vector:
      try:
         vector_query = VectorizedQuery(
         vector=vector,
         k_nearest_neighbors=5,
         fields="DescriptionVector",
         kind="vector",
         exhaustive=True
      )
   
      results = search_client.search(
         include_total_count=True,
         top=5,
         select=[
             "HotelId", "HotelName", "Category", "Description", "Address/City", "Address/StateProvince"
         ],
         facets=["Address/StateProvince"],
         filter="geo.distance(Location, geography'POINT(-77.03241 38.90166)') le 300",
         vector_filter_mode="postFilter",
         vector_queries=[vector_query]
      )
   
      print(f"Total semantic hybrid results: {results.get_count()}")
      for result in results:
         doc = result
         score = result.get("@search.score", "N/A")
         print(f"- HotelId: {doc['HotelId']}")
         print(f"  HotelName: {doc['HotelName']}")
         print(f"  Score: {score}")
         print(f"  City/State: {doc['Address']['City']}, {doc['Address']['StateProvince']}")
         print(f"  Description: {doc.get('Description')}\n")

      except Exception as ex:
         print("Semantic hybrid search failed:", ex)
   else:
      print("No vector loaded, skipping search.")
   ```
   
   The query was the same as the previous [single vector search example](#single-vector-search), but it includes a post-processing exclusion filter and returns only the two hotels within 300 kilometers.
   
   ```output
   Total semantic hybrid results: 2
   - HotelId: 48
     HotelName: Nordick's Valley Motel
     Score: 0.6605852246284485
     City/State: Washington D.C., null
     Description: Only 90 miles (about 2 hours) from the nation's capital and nearby most everything the historic valley has to offer. Hiking? Wine Tasting? Exploring the caverns? It's all nearby and we have specially priced packages to help make our B&B your home base for fun while visiting the valley.

   - HotelId: 49
     HotelName: Swirling Currents Hotel
     Score: 0.602634072303772
     City/State: Arlington, VA
     Description: Spacious rooms, glamorous suites and residences, rooftop pool, walking access to shopping, dining, entertainment and the city center. Each room comes equipped with a microwave, a coffee maker and a minifridge. In-room entertainment includes complimentary Wi-Fi and flat-screen TVs.
   ```

### Hybrid search

Hybrid search consists of keyword queries and vector queries in a single search request. This example runs the vector query and full-text search concurrently:

+ Search string: `historic hotel walk to restaurants and shopping`
+ Vector query string: `quintessential lodging near running trails, eateries, retail` (vectorized into a mathematical representation)

To create a hybrid search:

1. Run the `Hybrid search` code cell. This block contains the request to query the search index.

   ```python
   if vector:
       try:
           vector_query = VectorizedQuery(
               vector=vector,
               k_nearest_neighbors=5,
               fields="DescriptionVector",
               kind="vector",
               exhaustive=True
           )

           results = search_client.search(
               include_total_count=True,
               search_text="historic hotel walk to restaurants and shopping",  # keyword part
               select=["HotelId", "HotelName", "Description", "Category", "Tags"],
               top=5,
               vector_queries=[vector_query]
           )
   
           print(f"Total hybrid results: {results.get_count()}")
           for result in results:
               doc = result
               score = result.get("@search.score", "N/A")
               print(f"- Score: {score}")
               print(f"  HotelId: {doc['HotelId']}")            
               print(f"  HotelName: {doc['HotelName']}")
               print(f"  Description: {doc.get('Description')}")
               print(f"  Category: {doc.get('Category')}")
               print(f"  Tags: {doc.get('Tags', 'N/A')}\n")

      except Exception as ex:
         print("Hybrid search failed:", ex)
   else:
      print("No vector loaded, skipping search.")    
   ```

1. Review the output below the cell.

   ```output
   Total hybrid results: 7
   - Score: 0.03279569745063782
     HotelId: 4
     HotelName: Sublime Palace Hotel
     Description: Sublime Palace Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Cliff is part of a lovingly restored 19th century resort, updated for every modern convenience.
     Category: Boutique
     Tags: ['concierge', 'view', 'air conditioning']
   
   - Score: 0.032522473484277725
     HotelId: 13
     HotelName: Luxury Lion Resort
     Description: Unmatched Luxury. Visit our downtown hotel to indulge in luxury accommodations. Moments from the stadium and transportation hubs, we feature the best in convenience and comfort.
     Category: Luxury
     Tags: ['bar', 'concierge', 'restaurant']
   
   - Score: 0.03205128386616707
     HotelId: 48
     HotelName: Nordick's Valley Motel
     Description: Only 90 miles (about 2 hours) from the nation's capital and nearby most everything the historic valley has to offer. Hiking? Wine Tasting? Exploring the caverns? It's all nearby and we have specially priced packages to help make our B&B your home base for fun while visiting the valley.
     Category: Boutique
     Tags: ['continental breakfast', 'air conditioning', 'free wifi']
   
   - Score: 0.0317460335791111
     HotelId: 49
     HotelName: Swirling Currents Hotel
     Description: Spacious rooms, glamorous suites and residences, rooftop pool, walking access to shopping, dining, entertainment and the city center. Each room comes equipped with a microwave, a coffee maker and a minifridge. In-room entertainment includes complimentary Wi-Fi and flat-screen TVs.
     Category: Suite
     Tags: ['air conditioning', 'laundry service', '24-hour front desk service']
   
   - Score: 0.03125
     HotelId: 2
     HotelName: Old Century Hotel
     Description: The hotel is situated in a nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts. The hotel also regularly hosts events like wine tastings, beer dinners, and live music.
     Category: Boutique
     Tags: ['pool', 'free wifi', 'air conditioning', 'concierge']
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

### Semantic hybrid search

Here's the last query in the collection. This hybrid query specifies the semantic query type and a semantic configuration, demonstrating that you can build a hybrid query that uses semantic reranking.

To create a semantic hybrid search:

1. Run the `Semantic hybrid search` code cell. This code block contains the request to query the search index.

   ```python
   if semantic_hybrid_query_vector:
      try:
         vector_query = VectorizedQuery(
            vector=vector,
            k_nearest_neighbors=5,
            fields="DescriptionVector",
            kind="vector",
            exhaustive=True
         )

         results = search_client.search(
            include_total_count=True,
            search_text="historic hotel walk to restaurants and shopping",
            select=[
               "HotelId", "HotelName", "Category", "Description"
            ],
            query_type="semantic",
            semantic_configuration_name="my-semantic-config",
            top=7,            
            vector_queries=[vector_query]
         )

         print(f"Total semantic hybrid results: {results.get_count()}")
         for result in results:
            doc = result
            score = result.get("@search.score", "N/A")
            reranker_score = result.get("@search.reranker_score", "N/A")
            print(f"- Score: {score}")
            print(f"  Re-ranker Score: {reranker_score}")
            print(f"  HotelId: {doc['HotelId']}")
            print(f"  HotelName: {doc['HotelName']}")
            print(f"  Description: {doc.get('Description')}")
            print(f"  Category: {doc.get('Category')}")

   except Exception as ex:
      print("Semantic hybrid search failed:", ex)
   else:
      print("No vector loaded, skipping search.")
   ```

1. Review the output below the cell.

   With semantic ranking, the Swirling Currents Hotel now moves into the top spot.

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
     Description: The Gastronomic Hotel stands out for its culinary excellence under the management of William Dough, who advises on and oversees all of the Hotel’s restaurant services.
     Category: Suite
   ```

    You can think of the semantic ranking as a way to improve the relevance of search results by understanding the meaning behind the words in the query and the content of the documents. In this case, the semantic ranking helps to identify hotels that are not only relevant to the keywords but also match the intent of the query:
    
    Key takeaways:
    
    + Vector search is specified through the `vectors.value` property. Keyword search is specified through the `search` property.
    
    + In a hybrid search, you can integrate vector search with full-text search over keywords. Filters, spell check, and semantic ranking apply to textual content only, and not vectors. In this final query, there's no semantic `answer` because the system didn't produce one that was sufficiently strong.
    
    + Actual results include more detail, including semantic captions and highlights. Results were modified for readability. To get the full structure of the response, run the request in the REST client.

## Clean up resources

When you're working in your own subscription, it's a good idea at the end of a project to identify whether you still need the resources you created. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

You can find and manage resources in the Azure portal by using the **All resources** or **Resource groups** link in the leftmost pane.

Alternatively, you can run the `Clean up` code cell to delete the vector index created in this quickstart.

```python
index_client.delete_index(index_name)
print(f"Index '{index_name}' deleted successfully.")
```

## Next steps

+ Review the repository of code samples for vector search capabilities in Azure AI Search for [Python](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-python).
+ Review the other Python and Azure AI Search code samples in the [azure-search-python-samples repo](https://github.com/Azure-Samples/azure-search-python-samples).
