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

1. Create a new .ipynb file.

1. Open the Command Palette by using **Ctrl+Shift+P**.

1. Search for **Python: Create Environment**.

1. Select **`Venv.`**

1. Select a Python interpreter. Choose 3.10 or later.

It can take a minute to set up. If you run into problems, see [Python environments in VS Code](https://code.visualstudio.com/docs/python/environments).

### Install packages and set variables

1. Install packages, including [azure-search-documents](/python/api/azure-search-documents). 

    ```python
    ! pip install azure-search-documents==11.6.0b1 --quiet
    ! pip install azure-identity --quiet
    ! pip install python-dotenv --quiet
    ```

1. Provide your endpoint and API keys:

    ```python
    search_endpoint: str = "PUT-YOUR-SEARCH-SERVICE-ENDPOINT-HERE"
    search_api_key: str = "PUT-YOUR-SEARCH-SERVICE-ADMIN-API-KEY-HERE"
    index_name: str = "hotels-quickstart"
    ```

## Update and query the index

In this section, you update a search index and send a query that invokes semantic ranking. Visual Studio Code displays the response after you run each cell. For more information about each step, see [Explaining the code](#explaining-the-code).

## Explaining the code

Add `SemanticConfiguration` to a search index definition. If you're updating an existing index, this modification doesn't require a reindexing because the structure of your documents is unchanged.

Provide the entire schema plus the new SemanticConfiguration section. We recommend getting the index schema from the search service to ensure you're updating the correct schema.

This example is the Python code for the Hotels sample index schema, plus the semantic configuration.

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

# Update the search schema, providing the entire schema plus the changes.
index_client = SearchIndexClient(
    endpoint=search_endpoint, credential=credential)
fields = [
        SimpleField(name="HotelId", type=SearchFieldDataType.String, key=True),
        SearchableField(name="HotelName", type=SearchFieldDataType.String, sortable=True),
        SearchableField(name="Description", type=SearchFieldDataType.String, analyzer_name="en.lucene"),
        SearchableField(name="Category", type=SearchFieldDataType.String, facetable=True, filterable=True, sortable=True),

        SearchableField(name="Tags", collection=True, type=SearchFieldDataType.String, facetable=True, filterable=True),

        SimpleField(name="ParkingIncluded", type=SearchFieldDataType.Boolean, facetable=True, filterable=True, sortable=True),
        SimpleField(name="LastRenovationDate", type=SearchFieldDataType.DateTimeOffset, facetable=True, filterable=True, sortable=True),
        SimpleField(name="Rating", type=SearchFieldDataType.Double, facetable=True, filterable=True, sortable=True),

        ComplexField(name="Address", fields=[
            SearchableField(name="StreetAddress", type=SearchFieldDataType.String),
            SearchableField(name="City", type=SearchFieldDataType.String, facetable=True, filterable=True, sortable=True),
            SearchableField(name="StateProvince", type=SearchFieldDataType.String, facetable=True, filterable=True, sortable=True),
            SearchableField(name="PostalCode", type=SearchFieldDataType.String, facetable=True, filterable=True, sortable=True),
            SearchableField(name="Country", type=SearchFieldDataType.String, facetable=True, filterable=True, sortable=True),
        ])
    ]

semantic_config = SemanticConfiguration(
    name="semantic-config",
    prioritized_fields=SemanticPrioritizedFields(
        title_field=SemanticField(field_name="HotelName"),
        keywords_fields=[SemanticField(field_name="Category")],
        content_fields=[SemanticField(field_name="Description")]
    )
)

# Create the semantic settings with the configuration
semantic_search = SemanticSearch(configurations=[semantic_config])

scoring_profiles = []
suggester = [{'name': 'sg', 'source_fields': ['Tags', 'Address/City', 'Address/Country']}]

# Create the search index with the semantic settings
index = SearchIndex(name=index_name, fields=fields, suggesters=suggester, scoring_profiles=scoring_profiles, semantic_search=semantic_search)
result = index_client.create_or_update_index(index)
print(f' {result.name} created')
```

### Run your first query

Start with an empty query as a verification step, proving that the index is operational. You should get an unordered list of hotel names and descriptions, with a count of 4 indicating that there are four documents in the index.

```python
# Run an empty query (returns selected fields, all documents)
results =  search_client.search(query_type='simple',
    search_text="*" ,
    select='HotelName,Description',
    include_total_count=True)

print ('Total Documents Matching Query:', results.get_count())
for result in results:
    print(result["@search.score"])
    print(result["HotelName"])
    print(f"Description: {result['Description']}")
```

### Run a text query

For comparison purposes, run a text query with BM25 relevance scoring. Full text search is invoked when you provide a query string. The response consists of ranked results, where higher scores are awarded to documents having more instances of matching terms, or more important terms.

In this query for *restaurant on site*, Sublime Palace Hotel comes out on top because its description includes *site*. Terms that occur infrequently raise the search score of the document. 

```python
# Run a text query (returns a BM25-scored result set)
results =  search_client.search(query_type='simple',
    search_text="restaurant on site" ,
    select='HotelName,HotelId,Description',
    include_total_count=True)
    
for result in results:
    print(result["@search.score"])
    print(result["HotelName"])
    print(f"Description: {result['Description']}")
```

### Run a semantic query

Now add semantic ranking. New parameters include `query_type` and `semantic_configuration_name`.

It's the same query, but notice that the semantic ranker correctly identifies Gastronomic Landscape Hotel as a more relevant result given the initial query. This query also returns captions generated by the models. The inputs are too minimal in this sample to create interesting captions, but the example succeeds in demonstrating the syntax.

```python
# Runs a semantic query (runs a BM25-ranked query and promotes the most relevant matches to the top)
results =  search_client.search(query_type='semantic', semantic_configuration_name='semantic-config',
    search_text="restaurant on site", 
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

### Return semantic answers

In this final query, return semantic answers.

Semantic ranker can generate answers to a query string that has the characteristics of a question. The generated answer is extracted verbatim from your content. To get a semantic answer, the question and answer must be closely aligned, and the model must find content that clearly answers the question. If potential answers fail to meet a confidence threshold, the model doesn't return an answer. For demonstration purposes, the question in this example is designed to get a response so that you can see the syntax.

```python
# Run a semantic query that returns semantic answers  
results =  search_client.search(query_type='semantic', semantic_configuration_name='semantic-config',
 search_text="what hotel is in a historic building",
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
