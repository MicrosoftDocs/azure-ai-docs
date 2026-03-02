---
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
  - dev-focus
ms.topic: include
ms.date: 01/30/2026
ai-usage: ai-assisted
---

In this quickstart, you use the [Azure AI Search client library for Python](/python/api/overview/azure/search-documents-readme) to add [semantic ranking](../../semantic-search-overview.md) to an existing search index.

In Azure AI Search, semantic ranking is query-side functionality that uses machine reading comprehension from Microsoft to rescore search results, promoting the most semantically relevant matches to the top of the list. Depending on the content and query, semantic ranking can [significantly improve search relevance](https://techcommunity.microsoft.com/t5/azure-ai-services-blog/azure-cognitive-search-outperforming-vector-search-with-hybrid/ba-p/3929167) with minimal developer effort.

You can add a semantic configuration to an existing index with no rebuild requirement. Semantic ranking is most effective for text that's informational or descriptive.

> [!TIP]
> Want to get started right away? Download the [source code](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/Quickstart-Semantic-Ranking) on GitHub.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](../../search-create-service-portal.md) with [semantic ranker enabled](../../semantic-how-to-enable-disable.md).

+ An [index](../../search-how-to-create-search-index.md) with descriptive text fields that are attributed as `searchable` and `retrievable`. This quickstart assumes the [hotels-sample-index](../../search-get-started-portal.md).

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

This quickstart uses a Jupyter notebook with multiple code cells. Run each cell in sequence.

### Output

Output from the first cell is the name of the index, list of fields, and a statement indicating whether a semantic configuration exists. For the purposes of this quickstart, the message should say "No semantic configuration exists for this index".

Output from the semantic configuration cell shows the configuration you just added.

Output from the semantic query cell consists of 13 documents, ordered by the `"@search.reranker_score"`.

Output from the captions cell includes a new caption element alongside search fields. Captions are the most relevant passages in a result. If your index includes larger text, a caption is helpful for extracting the most interesting sentences.

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
```

Output from the answers cell includes a semantic answer (verbatim content) pulled from one of the results that best matches the question.

```output
Semantic Answer: Nature is Home on the beach. Explore the shore by
day, and then come home to our shared living space to relax around a
stone fireplace, sip something warm, and explore the<em> library
</em>by night. Save up to 30 percent. Valid Now through the end of
the year. Restrictions and blackouts may apply.
Semantic Answer Score: 0.9829999804496765
```

Recall that answers are *verbatim content* pulled from your index and might be missing phrases that a user would expect to see. To get *composed answers* as generated by a chat completion model, consider using a [RAG pattern](../../retrieval-augmented-generation-overview.md) or [agentic retrieval](../../agentic-retrieval-overview.md).

## Understand the code

[!INCLUDE [understand code note](../understand-code-note.md)]

Now that you've run the code, let's break down the key steps:

1. [Configuration and authentication](#configuration-and-authentication)
1. [Update the index with a semantic configuration](#update-the-index-with-a-semantic-configuration)
1. [Run semantic queries](#run-semantic-queries)

### Configuration and authentication

The first cell loads environment variables and creates a `DefaultAzureCredential` for authentication.

```python
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.identity import get_bearer_token_provider
import os

load_dotenv(override=True)

search_endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
credential = DefaultAzureCredential()
index_name = os.getenv(
    "AZURE_SEARCH_INDEX", "hotels-sample-index"
)
```

Key takeaways:

+ `DefaultAzureCredential` provides keyless authentication using Microsoft Entra ID. It chains multiple credential types, including the Azure CLI credential from `az login`.

+ Environment variables are loaded from the `.env` file using `python-dotenv`.

### Update the index with a semantic configuration

This code adds a semantic configuration to the existing `hotels-sample-index` index. No search documents are deleted by this operation and your index is still operational after the configuration is added.

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

### Run semantic queries

Once the index has a semantic configuration, you can run queries that include semantic parameters. This code shows the minimum requirement for invoking semantic ranking.

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

#### Extractive captions

This code adds captions to extract portions of the text and apply hit highlighting to the important terms and phrases.

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

#### Semantic answers

This code returns semantic answers for question-like queries. Semantic ranker can produce an answer to a query string that has the characteristics of a question. The generated answer is extracted verbatim from your content so it doesn't include composed content like what you might expect from a chat completion model.

To produce a semantic answer, the question and answer must be closely aligned, and the model must find content that clearly answers the question. If potential answers fail to meet a confidence threshold, the model doesn't return an answer.

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

+ For composed answers, consider [RAG patterns](../../retrieval-augmented-generation-overview.md) or [agentic retrieval](../../agentic-retrieval-overview.md).
