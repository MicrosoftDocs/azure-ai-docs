---
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: include
ms.date: 06/27/2025
---

[!INCLUDE [Semantic ranker introduction](semantic-ranker-intro.md)]

> [!TIP]
> You can [download a finished notebook](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/Quickstart-Semantic-Search) to start with a finished project or follow these steps to create your own. 

## Set up the client

In this quickstart, use a Jupyter notebook and the [**azure-search-documents**](/python/api/overview/azure/search-documents-readme) library in the Azure SDK for Python to learn about semantic ranking.

We recommend [Visual Studio Code](https://code.visualstudio.com/download) with Python 3.10 or later and the [Python extension](https://code.visualstudio.com/docs/languages/python) for this quickstart.

We recommend a virtual environment for this quickstart:

1. Start Visual Studio Code.

1. Open the **semantic-search-quickstart.ipynb** file or create a new notebook.

1. Open the Command Palette by using **Ctrl+Shift+P**.

1. Search for **Python: Create Environment**.

1. Select **`Venv.`**

1. Select a Python interpreter. Choose 3.10 or later.

It can take a minute to set up. If you run into problems, see [Python environments in VS Code](https://code.visualstudio.com/docs/python/environments).

### Install packages and set environment variables

1. Install packages, including [azure-search-documents](/python/api/azure-search-documents). 

    ```python
   ! pip install -r requirements.txt --quiet
    ```

1. Rename `sample.env` to `.env`, and provide your search service endpoint. You can get the endpoint from the Azure portal on the search service **Overview** page.

    ```python
    AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
    AZURE_SEARCH_INDEX_NAME=hotels-sample-index
    ```

### Sign in to Azure

If you signed in to the [Azure portal](https://portal.azure.com), you're signed into Azure. If you aren't sure, use the Azure CLI or Azure PowerShell to log in: `az login` or `az connect`. If you have multiple tenants and subscriptions, see [Quickstart: Connect without keys](../../search-get-started-rbac.md) for help on how to connect.

## Update and query the index

This section presents the code for updating a search index and sending a query that invokes semantic ranking. Visual Studio Code displays the response after you run each cell. There are two parts:

+ [Add a semantic configuration to an index](#add-a-semantic-configuration-to-the-hotels-sample-index)
+ [Add semantic parameters to a query](#add-semantic-parameters-to-a-query)

### Add a semantic configuration to the hotels-sample-index

```python
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents import SearchClient
from azure.search.documents.indexes.models import (
    ComplexField,
    SimpleField,
    SearchFieldDataType,
    SearchableField,
    SearchIndex,
    SemanticConfiguration,
    SemanticField,
    SemanticPrioritizedFields,
    SemanticSearch
)

# Update search schema
index_client = SearchIndexClient(
    endpoint=search_endpoint, credential=credential)
fields = [
        SimpleField(name="HotelId", type=SearchFieldDataType.String, key=True, facetable=True, filterable=True, sortable=False),
        SearchableField(name="HotelName", type=SearchFieldDataType.String, facetable=False, filterable=False, sortable=False, retrievable=True, analyzer_name="en.microsoft"),
        SearchableField(name="Description", type=SearchFieldDataType.String, analyzer_name="en.microsoft"),
        SearchableField(name="Description_fr", type=SearchFieldDataType.String, analyzer_name="fr.microsoft"),
        SearchableField(name="Category", type=SearchFieldDataType.String, facetable=True, filterable=True, sortable=False, analyzer_name="en.microsoft"),

        SearchableField(name="Tags", collection=True, type=SearchFieldDataType.String, facetable=True, filterable=True, sortable=False, analyzer_name="en.microsoft"),

        SimpleField(name="ParkingIncluded", type=SearchFieldDataType.Boolean, facetable=True, filterable=True, sortable=False),
        SimpleField(name="LastRenovationDate", type=SearchFieldDataType.DateTimeOffset, facetable=False, filterable=False, sortable=True),
        SimpleField(name="Rating", type=SearchFieldDataType.Double, facetable=True, filterable=True, sortable=True),

        ComplexField(name="Address", fields=[
            SearchableField(name="StreetAddress", type=SearchFieldDataType.String, facetable=False, filterable=False, sortable=False, analyzer_name="en.microsoft"),
            SearchableField(name="City", type=SearchFieldDataType.String, facetable=True, filterable=True, sortable=False, analyzer_name="en.microsoft"),
            SearchableField(name="StateProvince", type=SearchFieldDataType.String, facetable=True, filterable=True, sortable=False, analyzer_name="en.microsoft"),
            SearchableField(name="PostalCode", type=SearchFieldDataType.String, facetable=True, filterable=True, sortable=False, analyzer_name="en.microsoft"),
            SearchableField(name="Country", type=SearchFieldDataType.String, facetable=True, filterable=True, sortable=False, analyzer_name="en.microsoft"),
        ])        ,
        SimpleField(name="Location", type=SearchFieldDataType.GeographyPoint, facetable=False, filterable=True, sortable=True),
        ComplexField(name="Rooms",collection=True,fields=[
                SearchableField(name="Description", type=SearchFieldDataType.String, analyzer_name="en.microsoft"),
                SearchableField(name="Description_fr", type=SearchFieldDataType.String, analyzer_name="fr.microsoft"),
                SearchableField(name="Type", type=SearchFieldDataType.String, analyzer_name="en.microsoft", facetable=True, filterable=True),
                SimpleField(name="BaseRate", type=SearchFieldDataType.Double, facetable=True, filterable=True),
                SearchableField(name="BedOptions", type=SearchFieldDataType.String, analyzer_name="en.microsoft", facetable=True, filterable=True),
                SimpleField(name="SleepsCount", type=SearchFieldDataType.Int64, facetable=True, filterable=True),
                SimpleField(name="SmokingAllowed", type=SearchFieldDataType.Boolean, facetable=True, filterable=True),
                SearchableField(name="Tags", collection=True, type=SearchFieldDataType.String, analyzer_name="en.microsoft", facetable=True, filterable=True)
            ]
        ),
        SimpleField(name="id", type=SearchFieldDataType.String, searchable=False, retrievable=False, facetable=False, filterable=False, sortable=False), 
        SimpleField(name="rid", type=SearchFieldDataType.String, searchable=False, retrievable=False, facetable=False, filterable=False, sortable=False)
        ]

semantic_config = SemanticConfiguration(
    name="semantic-config",
    prioritized_fields=SemanticPrioritizedFields(
        title_field=SemanticField(field_name="HotelName"),
        keywords_fields=[SemanticField(field_name="Category")],
        content_fields=[SemanticField(field_name="Description")]
    )
)

# Specify the semantic settings with the configuration
semantic_search  = SemanticSearch(default_configuration_name="semantic_config", configurations=[semantic_config])
scoring_profiles = []
suggester = [{'name': 'sg', 'source_fields': ['Rooms/Tags', 'Rooms/Type', 'Address/City', 'Address/Country']}]

# Update the search index with the semantic settings
index = SearchIndex(name=index_name, fields=fields, suggesters=suggester, scoring_profiles=scoring_profiles, semantic_search=semantic_search)
result = index_client.create_or_update_index(index)
print(f' {result.name} updated')
```

### Add semantic parameters to a query

```python
# Set up the search client
search_client = SearchClient(endpoint=search_endpoint,
                      index_name=index_name,
                      credential=credential)

# Runs a semantic query
results =  search_client.search(query_type='semantic', semantic_configuration_name='semantic-config',
    search_text="walking distance to live music", 
    select='HotelName,Description,Category', query_caption='extractive')

for result in results:
    print(result["@search.reranker_score"])
    print(result["HotelName"])
    print(f"Description: {result['Description']}")

    captions = result["@search.captions"]
    if captions:
        caption = captions[0]
        if caption.highlights:
            print(f"Caption: {caption.highlights}\n")
        else:
            print(f"Caption: {caption.text}\n")
```

## Explaining the code

This section explains the updates to the index and queries. If you're updating an existing index, the addition of a semantic configuration doesn't require a reindexing because the structure of your documents is unchanged.

### Index updates

To update the index, provide the existing schema in its entirety, plus the new `SemanticConfiguration` section. We recommend retrieving the index schema from the search service to ensure you're working with the current version. If the original and updated schemas differ in field definitions or other constructs, the update fails.

This example highlights the Python code that adds a semantic configuration to an index.

```python
# New semantic configuration section in the index
semantic_config = SemanticConfiguration(
    name="semantic-config",
    prioritized_fields=SemanticPrioritizedFields(
        title_field=SemanticField(field_name="HotelName"),
        keywords_fields=[SemanticField(field_name="Category")],
        content_fields=[SemanticField(field_name="Description")]
    )
)

# Create the semantic settings using the configuration
semantic_search  = SemanticSearch(configurations=[semantic_config])

# Update the search index on the search service
index = SearchIndex(name=index_name, fields=fields, semantic_search=semantic_search)
result = index_client.create_or_update_index(index)
print(f' {result.name} updated')
```

### Query parameters

Required semantic parameters include `query_type` and `semantic_configuration_name`. Here's an example of a basic semantic query using the minimum parameters.

```python
# Runs a semantic query
results =  search_client.search(query_type='semantic', semantic_configuration_name='semantic-config',
    search_text="walking distance to live music", 
    select='HotelName,HotelId,Description', query_caption='extractive')

for result in results:
    print(result["@search.reranker_score"])
    print(result["HotelId"])
    print(result["HotelName"])
    print(f"Description: {result['Description']}")
```

Output for this query (truncated) should look similar to the following example. Results are ranked by the semantic `rerankerScore` property. Scores ranging from 2.0 to 3.0 are considered to be [moderately relevant](../../semantic-search-overview.md#how-ranking-is-scored).

```
2.567150592803955
24
Uptown Chic Hotel
Description: Chic hotel near the city. High-rise hotel in downtown, within walking distance to theaters, art galleries, restaurants and shops. Visit Seattle Art Museum by day, and then head over to Benaroya Hall to catch the evening's concert performance.
2.362976312637329
2
Old Century Hotel
Description: The hotel is situated in a nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts. The hotel also regularly hosts events like wine tastings, beer dinners, and live music.
2.1515355110168457
4
Sublime Palace Hotel
Description: Sublime Cliff Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Cliff is part of a lovingly restored 19th century resort, updated for every modern convenience.
2.0363330841064453
15
By the Market Hotel
Description: Book now and Save up to 30%. Central location. Walking distance from the Empire State Building & Times Square, in the Chelsea neighborhood. Brand new rooms. Impeccable service.
2.029420852661133
39
White Mountain Lodge & Suites
Description: Live amongst the trees in the heart of the forest. Hike along our extensive trail system. Visit the Natural Hot Springs, or enjoy our signature hot stone massage in the Cathedral of Firs. Relax in the meditation gardens, or join new friends around the communal firepit. Weekend evening entertainment on the patio features special guest musicians or poetry readings.
1.9624263048171997
49
Swirling Currents Hotel
Description: Spacious rooms, glamorous suites and residences, rooftop pool, walking access to shopping, dining, entertainment and the city center. Each room comes equipped with a microwave, a coffee maker and a minifridge. In-room entertainment includes complimentary W-Fi and flat-screen TVs. 
1.9409809112548828
...
1.396693468093872
35
Bellevue Suites
Description: Comfortable city living in the very center of downtown Bellevue. Newly reimagined, this hotel features apartment-style suites with sleeping, living and work spaces. Located across the street from the Light Rail to downtown. Free shuttle to the airport.
```

### Return captions

Optionally, you can add captions to extract portions of the text and apply hit highlighting to the important terms and phrases. This query adds captions.

```python
# Runs a semantic query that returns captions
results =  search_client.search(query_type='semantic', semantic_configuration_name='semantic-config',
    search_text="walking distance to live music", 
    select='HotelName,HotelId,Description', query_caption='extractive')

for result in results:
    print(result["@search.reranker_score"])
    print(result["HotelId"])
    print(result["HotelName"])
    print(f"Description: {result['Description']}")

    captions = result["@search.captions"]
    if captions:
        caption = captions[0]
        if caption.highlights:
            print(f"Caption: {caption.highlights}\n")
        else:
            print(f"Caption: {caption.text}\n")
```

Output (truncated) for this query adds a `caption` after each description. Notice that captions include hit highlighting over relevant terms and phrases.

```
2.567150592803955
24
Uptown Chic Hotel
Description: Chic hotel near the city. High-rise hotel in downtown, within walking distance to theaters, art galleries, restaurants and shops. Visit Seattle Art Museum by day, and then head over to Benaroya Hall to catch the evening's concert performance.
Caption: Chic hotel near the city. High-rise hotel in downtown, within walking distance to<em> theaters, </em>art galleries, restaurants and shops. Visit<em> Seattle Art Museum </em>by day, and then head over to<em> Benaroya Hall </em>to catch the evening's<em> concert </em>performance.

2.362976312637329
2
Old Century Hotel
Description: The hotel is situated in a nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts. The hotel also regularly hosts events like wine tastings, beer dinners, and live music.
Caption: The hotel is situated in a nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts. The hotel also regularly hosts events like wine tastings, beer dinners, and live.

2.1515355110168457
4
Sublime Palace Hotel
Description: Sublime Cliff Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Cliff is part of a lovingly restored 19th century resort, updated for every modern convenience.
Caption: Sublime Cliff Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within<em> short walking distance </em>to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Cliff is part of a lovingly restored 19th century resort,.

```

### Return semantic answers

In this final query, return semantic answers.

Semantic ranker can produce an answer to a query string that has the characteristics of a question. The generated answer is extracted verbatim from your content so it won't include composed content like what you might expect from a chat completion model. If the semantic answer isn't useful for your scenario, you can omit `semantic_answers` from your code.

To get a semantic answer, the question and answer must be closely aligned, and the model must find content that clearly answers the question. If potential answers fail to meet a confidence threshold, the model doesn't return an answer. For demonstration purposes, the question in this example is designed to get a response so that you can see the syntax.

```python
# Run a semantic query that returns semantic answers  
results =  search_client.search(query_type='semantic', semantic_configuration_name='semantic-config',
 search_text="what's a good hotel for people who like to read",
 select='HotelName,Description,Category', query_caption='extractive', query_answer="extractive",)

semantic_answers = results.get_answers()
for answer in semantic_answers:
    if answer.highlights:
        print(f"Semantic Answer: {answer.highlights}")
    else:
        print(f"Semantic Answer: {answer.text}")
    print(f"Semantic Answer Score: {answer.score}\n")

for result in results:
    print(result["@search.reranker_score"])
    print(result["HotelName"])
    print(f"Description: {result['Description']}")

    captions = result["@search.captions"]
    if captions:
        caption = captions[0]
        if caption.highlights:
            print(f"Caption: {caption.highlights}\n")
        else:
            print(f"Caption: {caption.text}\n")
```

Output (truncated) for this query should look similar to the following example, where the answer is pulled from the second result.

Recall that answers are verbatim content pulled from your index and might be missing phrases that a user would expect to see. To get composed answers as generated by a chat completion model, considering using a [RAG pattern](../../retrieval-augmented-generation-overview.md) or [agentic retrieval](../../search-agentic-retrieval-concept.md).

```
Semantic Answer: Nature is Home on the beach. Explore the shore by day, and then come home to our shared living space to relax around a stone fireplace, sip something warm, and explore<em> the library </em>by night. Save up to 30 percent. Valid Now through the end of the year. Restrictions and blackouts may apply.
Semantic Answer Score: 0.9890000224113464

2.192565441131592
Stay-Kay City Hotel
Description: This classic hotel is fully-refurbished and ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Times Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.
Caption: This<em> classic </em>hotel is<em> fully-refurbished </em>and ideally located on the<em> main commercial artery of the </em>city in the<em> heart of New York.</em> A few minutes away is Times Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.

2.0917632579803467
Lakeside B & B
Description: Nature is Home on the beach. Explore the shore by day, and then come home to our shared living space to relax around a stone fireplace, sip something warm, and explore the library by night. Save up to 30 percent. Valid Now through the end of the year. Restrictions and blackouts may apply.
Caption: Nature is Home on the beach. Explore the shore by day, and then come home to our shared living space to relax around a stone fireplace, sip something warm, and explore<em> the library </em>by night. Save up to 30 percent. Valid Now through the end of the year. Restrictions and blackouts may apply.

2.084540843963623
Double Sanctuary Resort
Description: 5 star Luxury Hotel - Biggest Rooms in the city. #1 Hotel in the area listed by Traveler magazine. Free WiFi, Flexible check in/out, Fitness Center & espresso in room.
Caption: <em>5 star Luxury Hotel </em>-<em> Biggest </em>Rooms in the<em> city. #1 </em>Hotel in the area listed by Traveler magazine. Free WiFi, Flexible check in/out, Fitness Center & espresso in room.
```
