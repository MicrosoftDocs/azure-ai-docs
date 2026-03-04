---
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
  - dev-focus
ms.topic: include
ms.date: 03/04/2026
ai-usage: ai-assisted
---

In this quickstart, you use the [Azure AI Search client library for Python](/python/api/overview/azure/search-documents-readme) to add [semantic ranking](../../semantic-search-overview.md) to an existing search index and query the index.

Semantic ranking is query-side functionality that uses machine reading comprehension to rescore search results, promoting the most semantically relevant matches to the top of the list. You can add a semantic configuration to an existing index with no rebuild requirement.  Semantic ranking is most effective for informational or descriptive text.

> [!TIP]
> Want to get started right away? Download the [source code](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/Quickstart-Semantic-Ranking) on GitHub.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](../../search-create-service-portal.md) with [semantic ranker enabled](../../semantic-how-to-enable-disable.md).

+ An [index](../../search-how-to-create-search-index.md) with descriptive text fields attributed as `searchable` and `retrievable`.  This quickstart assumes the [hotels-sample](../../search-get-started-portal.md) index.

+ [Python 3.10](https://www.python.org/downloads/) or later.

+ [Visual Studio Code](https://code.visualstudio.com/download) with the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python).

+ [Git](https://git-scm.com/downloads) to clone the sample repository.

+ The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

## Configure access

[!INCLUDE [resource authentication](../resource-authentication-semantic.md)]

## Get endpoint

[!INCLUDE [resource endpoint](../resource-endpoint.md)]

## Start with an index

[!INCLUDE [start with an index](semantic-ranker-index.md)]

## Set up the environment

1. Use Git to clone the sample repository.

    ```bash
    git clone https://github.com/Azure-Samples/azure-search-python-samples
    ```

1. Navigate to the quickstart folder and open it in Visual Studio Code.

    ```bash
    cd azure-search-python-samples/Quickstart-Semantic-Ranking
    code .
    ```

1. In `sample.env`, replace the placeholder value for `AZURE_SEARCH_ENDPOINT` with the URL you obtained in [Get endpoint](#get-endpoint).

1. Rename `sample.env` to `.env`.

    ```bash
    mv sample.env .env
    ```

1. Open `semantic-ranking-quickstart.ipynb`.

1. Press **Ctrl+Shift+P**, select **Notebook: Select Notebook Kernel**, and follow the prompts to create a virtual environment. Select **requirements.txt** for the dependencies.

   When complete, you should see a `.venv` folder in the project directory.

1. For keyless authentication with Microsoft Entra ID, sign in to your Azure account. If you have multiple subscriptions, select the one that contains your Azure AI Search service.

    ```azurecli
    az login
    ```

## Run the code

1. Run the `Install packages and set variables` cells to install the required packages and load environment variables.

1. Run the remaining cells sequentially to add a semantic configuration and query the index.

### Output

The output of the `Get the index definition` cell is the name of the index, its fields, and any existing semantic configurations.

```output
Index name: hotels-sample
Number of fields: 23
Field: HotelId, Type: Edm.String, Searchable: True
Field: HotelName, Type: Edm.String, Searchable: True
Field: Description, Type: Edm.String, Searchable: True
Field: Description_fr, Type: Edm.String, Searchable: True
Field: Category, Type: Edm.String, Searchable: True
Field: Tags, Type: Collection(Edm.String), Searchable: True
// Trimmed for brevity
Semantic config: hotels-sample-semantic-configuration
Title field: HotelName
```

The output of the `Add a semantic configuration to the index` cell lists all semantic configurations on the index, including the one the code added, followed by a success message.

```output
Semantic configurations:
----------------------------------------
  Configuration: hotels-sample-semantic-configuration
    Title field: HotelName
    Keywords fields: Category
    Content fields: Description

  Configuration: semantic-config
    Title field: HotelName
    Keywords fields: Tags
    Content fields: Description

✅ Semantic configuration successfully added!
```

The output of the `Run a term query` cell returns all matching documents ordered by BM25 score. This baseline query doesn't use semantic ranking.

```output
5.360838
4
Sublime Palace Hotel
Description: Sublime Cliff Hotel is located in the heart of the
historic center of Sublime in an extremely vibrant and lively area
within short walking distance to the sites and landmarks of the city
and is surrounded by the extraordinary beauty of churches, buildings,
shops and monuments. Sublime Cliff is part of a lovingly restored
19th century resort, updated for every modern convenience.
4.691083
2
Old Century Hotel
Description: The hotel is situated in a nineteenth century plaza,
which has been expanded and renovated to the highest architectural
standards to create a modern, functional and first-class hotel in
which art and unique historical elements coexist with the most
modern comforts. The hotel also regularly hosts events like wine
tastings, beer dinners, and live music.
// Trimmed for brevity
```

The output of the `Run a semantic query` cell returns all matching documents ordered by the semantic re-ranker score.

```output
2.613231658935547
24
Uptown Chic Hotel
Description: Chic hotel near the city. High-rise hotel in downtown,
within walking distance to theaters, art galleries, restaurants and
shops. Visit Seattle Art Museum by day, and then head over to
Benaroya Hall to catch the evening's concert performance.
2.271434783935547
2
Old Century Hotel
Description: The hotel is situated in a nineteenth century plaza,
which has been expanded and renovated to the highest architectural
standards to create a modern, functional and first-class hotel in
which art and unique historical elements coexist with the most
modern comforts. The hotel also regularly hosts events like wine
tastings, beer dinners, and live music.
// Trimmed for brevity
```

The output of the `Return captions` cell adds a caption element with hit highlighting alongside search fields. Captions are the most relevant passages in a result. If your index includes larger text, captions help extract the most interesting sentences.

```output
2.613231658935547
24
Uptown Chic Hotel
Description: Chic hotel near the city. High-rise hotel in downtown,
within walking distance to theaters, art galleries, restaurants and
shops. Visit Seattle Art Museum by day, and then head over to
Benaroya Hall to catch the evening's concert performance.
Caption: Chic hotel near the city. High-rise hotel in downtown,
within walking distance to<em> theaters, </em>art galleries,
restaurants and shops. Visit<em> Seattle Art Museum </em>by day, and
then head over to<em> Benaroya Hall </em>to catch the evening's
concert performance.
// Trimmed for brevity
```

The output of the `Return semantic answers` cell includes a semantic answer pulled from one of the results that best matches the question, followed by search results with captions.

```output
Semantic Answer: Nature is Home on the beach. Explore the shore by
day, and then come home to our shared living space to relax around a
stone fireplace, sip something warm, and explore the<em> library
</em>by night. Save up to 30 percent. Valid Now through the end of
the year. Restrictions and blackouts may apply.
Semantic Answer Score: 0.9829999804496765
```

## Understand the code

[!INCLUDE [understand code note](../understand-code-note.md)]

Now that you've run the code, let's break down the key steps:

1. [Configuration and authentication](#configuration-and-authentication)
1. [Update the index with a semantic configuration](#update-the-index-with-a-semantic-configuration)
1. [Query the index](#query-the-index)

### Configuration and authentication

The `Install packages and set variables` cell loads environment variables and creates a `DefaultAzureCredential` for authentication.

```python
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.identity import get_bearer_token_provider
import os

load_dotenv(override=True)

search_endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
credential = DefaultAzureCredential()
index_name = os.getenv(
    "AZURE_SEARCH_INDEX", "hotels-sample"
)
```

Key takeaways:

+ `DefaultAzureCredential` provides keyless authentication using Microsoft Entra ID. It chains multiple credential types, including the Azure CLI credential from `az login`.
+ Environment variables are loaded from the `.env` file using `python-dotenv`.

### Update the index with a semantic configuration

The `Add a semantic configuration to the index` cell adds a semantic configuration to the existing `hotels-sample` index. This operation doesn't delete any search documents, and your index remains operational after the configuration is added.

```python
from azure.search.documents.indexes.models import (
    SemanticConfiguration,
    SemanticField,
    SemanticPrioritizedFields,
    SemanticSearch
)

new_semantic_config = SemanticConfiguration(
    name="semantic-config",
    prioritized_fields=SemanticPrioritizedFields(
        title_field=SemanticField(field_name="HotelName"),
        keywords_fields=[
            SemanticField(field_name="Tags")
        ],
        content_fields=[
            SemanticField(field_name="Description")
        ]
    )
)

if existing_index.semantic_search is None:
    existing_index.semantic_search = SemanticSearch(
        configurations=[new_semantic_config]
    )
else:
    existing_index.semantic_search.configurations.append(
        new_semantic_config
    )

result = index_client.create_or_update_index(existing_index)
```

Key takeaways:

+ A semantic configuration specifies the fields used for semantic ranking. `title_field` sets the document title, `content_fields` sets the main content, and `keywords_fields` sets the keyword or tag fields.
+ You create the configuration with `SemanticConfiguration` and its associated `SemanticPrioritizedFields` model, and then append it to the existing index.
+ `create_or_update_index` pushes the updated schema to the search service without rebuilding the index or deleting documents.

### Query the index

The query cells run four queries in sequence: a baseline keyword search followed by three semantic ranking variations with increasing functionality.

#### Term query (baseline)

The `Run a term query` cell runs a keyword search using BM25 scoring. This baseline query doesn't use semantic ranking and serves as a comparison point.

```python
from azure.search.documents import SearchClient

search_client = SearchClient(
    endpoint=search_endpoint,
    index_name=index_name,
    credential=credential
)

results = search_client.search(
    query_type='simple',
    search_text="walking distance to live music",
    select='HotelId,HotelName,Description',
    include_total_count=True
)
```

Key takeaways:

+ `query_type='simple'` specifies a keyword search using BM25 scoring.
+ The `@search.score` in results indicates the BM25 relevance score.

#### Semantic query (no captions, no answers)

The `Run a semantic query` cell shows the minimum requirement for invoking semantic ranking.

```python
from azure.search.documents import SearchClient

search_client = SearchClient(
    endpoint=search_endpoint,
    index_name=index_name,
    credential=credential
)

results = search_client.search(
    query_type='semantic',
    semantic_configuration_name='semantic-config',
    search_text="walking distance to live music",
    select='HotelId,HotelName,Description',
    query_caption='extractive'
)
```

Key takeaways:

+ `query_type='semantic'` enables semantic ranking on the query.
+ `semantic_configuration_name` specifies which semantic configuration to use.
+ The `@search.reranker_score` in results indicates semantic relevance (higher is better).

#### Semantic query with captions

The `Return captions` cell adds captions to extract the most relevant passages from each result, with hit highlighting applied to the important terms and phrases.

```python
results = search_client.search(
    query_type='semantic',
    semantic_configuration_name='semantic-config',
    search_text="walking distance to live music",
    select='HotelName,HotelId,Description',
    query_caption='extractive'
)

for result in results:
    captions = result["@search.captions"]
    if captions:
        caption = captions[0]
        if caption.highlights:
            print(f"Caption: {caption.highlights}\n")
```

Key takeaways:

+ `query_caption='extractive'` enables extractive captions from the content fields.
+ Captions surface the most relevant passages and add `<em>` tags around important terms.

#### Semantic query with answers

The `Return semantic answers` cell adds semantic answers. This query uses a question as the search text because semantic answers work best when the query is phrased as a question. The answer is a verbatim passage extracted from your index, not a composed response from a chat completion model.

The query and the indexed content must be closely aligned for an answer to be returned. If no candidate meets the confidence threshold, the response doesn't include an answer. This example uses a question that's known to produce a result so that you can see the syntax. If answers aren't useful for your scenario, omit `query_answer` from your code. For composed answers, consider a [RAG pattern](../../retrieval-augmented-generation-overview.md) or [agentic retrieval](../../agentic-retrieval-overview.md).

```python
results = search_client.search(
    query_type='semantic',
    semantic_configuration_name='semantic-config',
    search_text="what's a good hotel for people who "
                "like to read",
    select='HotelName,Description,Category',
    query_caption='extractive',
    query_answer="extractive",
)

semantic_answers = results.get_answers()
for answer in semantic_answers:
    if answer.highlights:
        print(f"Semantic Answer: {answer.highlights}")
    else:
        print(f"Semantic Answer: {answer.text}")
    print(f"Semantic Answer Score: {answer.score}\n")
```

Key takeaways:

+ `query_answer="extractive"` enables extractive answers for question-like queries.
+ Answers are verbatim content extracted from your index, not generated text.
+ `results.get_answers()` retrieves the answer objects separately from the search results.
