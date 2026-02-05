---
manager: nitinme
author: rotabor
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 02/05/2026
ms.custom: dev-focus
ai-usage: ai-assisted
---

In this quickstart, you use the [Azure AI Search client library for Python](/python/api/overview/azure/search-documents-readme) to create, load, and query a [vector index](../../vector-store.md). The Python client library provides an abstraction over the REST APIs for index operations.

In Azure AI Search, a vector index has an index schema that defines vector and nonvector fields, a vector search configuration for algorithms that create the embedding space, and settings on vector field definitions that are evaluated at query time. [Indexes - Create or Update](/rest/api/searchservice/indexes/create-or-update) (REST API) creates the vector index.

> [!TIP]
> + Want to get started right away? Download the [source code](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/Quickstart-Vector-Search) on GitHub.
> + This quickstart omits the vectorization step and provides inline embeddings. For [integrated chunking and vectorization](../../vector-search-integrated-vectorization.md) over your own content, try the [**Import data (new)** wizard](../../search-get-started-portal-import-vectors.md).

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

- An [Azure AI Search service](../../search-create-service-portal.md). You can use the Free tier for most of this quickstart, but we recommend Basic or higher for larger data files.

- [Semantic ranker enabled on your search service](../../semantic-how-to-enable-disable.md) for the optional semantic hybrid query.

- The latest version of [Python](https://www.python.org/downloads/).

- [Visual Studio Code](https://code.visualstudio.com/download) with the [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) extensions.

- [Git](https://git-scm.com/downloads) to clone the sample repository.

- The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

## Configure access

[!INCLUDE [resource authentication](../resource-authentication.md)]

## Get endpoint

[!INCLUDE [resource endpoint](../resource-endpoint.md)]

## Set up the environment

1. Use Git to clone the sample repository.

   ```bash
   git clone https://github.com/Azure-Samples/azure-search-python-samples
   ```

1. Open the quickstart folder in Visual Studio Code.

   ```bash
   cd azure-search-python-samples/Quickstart-Vector-Search
   code .
   ```

1. Open `vector-search-quickstart.ipynb`.

1. Press **Ctrl+Shift+P**, select **Python: Create Environment**, and then follow the prompts to create a virtual environment.

   When the environment is created, you should see a `.venv` folder in the project directory.

1. Run the first code cell to install the required packages.

1. In the second code cell, replace the placeholder value for `search_endpoint` with the URL you obtained in [Get endpoint](#get-endpoint), and then run the cell.

1. For keyless authentication with Microsoft Entra ID, sign in to your Azure account. If you have multiple subscriptions, select the one that contains your Azure AI Search service.

    ```azurecli
    az login
    ```

## Run the code

1. Run the `Install packages and set variables` cell to load environment variables and verify the package installation.

1. Run the `Create an index` cell to create a vector index in Azure AI Search.

1. Run the `Create documents payload` cell to prepare the documents for upload.

1. Run the `Upload the documents` cell to upload documents to the index.

1. Run the `Create the vector query string` cell to load the vectorized query data.

1. Run the search cells. Start with `Single vector search`, and then try `Single vector search with filter`, `Hybrid search`, and `Semantic hybrid search`.

### Output

The `Upload the documents` cell shows the status of each document:

```output
Key: 1, Succeeded: True, ErrorMessage: None
Key: 2, Succeeded: True, ErrorMessage: None
Key: 3, Succeeded: True, ErrorMessage: None
Key: 4, Succeeded: True, ErrorMessage: None
Key: 48, Succeeded: True, ErrorMessage: None
Key: 49, Succeeded: True, ErrorMessage: None
Key: 13, Succeeded: True, ErrorMessage: None
```

The `Single vector search` cell returns results similar to:

```output
Total results: 7
- HotelId: 48, HotelName: Nordick's Valley Motel, Category: Boutique
- HotelId: 13, HotelName: Luxury Lion Resort, Category: Luxury
- HotelId: 4, HotelName: Sublime Palace Hotel, Category: Boutique
- HotelId: 49, HotelName: Swirling Currents Hotel, Category: Suite
- HotelId: 2, HotelName: Old Century Hotel, Category: Boutique
```

## Understand the code

Now that you've run the code, let's break down the key steps:

1. [Create a vector index](#create-a-vector-index)
1. [Upload documents to the index](#upload-documents-to-the-index)
1. [Query the index](#query-the-index)

### Create a vector index

The `Create an index` cell in the notebook creates a vector index in Azure AI Search. The index schema defines the fields, including the vector field `DescriptionVector`.

Key takeaways:

+ You define an index by creating a list of fields. Each field is created using a helper method that defines the field type and its settings.

+ This particular index supports multiple search capabilities, including full-text keyword search, vector search (enables hybrid search by collocating vector and nonvector fields), semantic search, faceted search, geo-spatial search, and filtering.

+ Vector fields contain floating point values. The dimensions attribute has a minimum of 2 and a maximum of 4096 floating point values each. This quickstart sets the dimensions attribute to 1,536 because that's the size of embeddings generated by the `text-embedding-ada-002` model.

### Upload documents to the index

The `Create documents payload` and `Upload the documents` cells load documents into the index. Each document includes the vectorized version of the article's description, which enables similarity search based on meaning rather than exact keywords.

Key takeaways:

+ Your code interacts with a specific search index hosted in your Azure AI Search service through the `SearchClient`, which is the main object provided by the `azure-search-documents` package. The `SearchClient` provides access to index operations, such as:

    + Data ingestion: `upload_documents()`, `merge_documents()`, `delete_documents()`
    
    + Search operations: `search()`, `autocomplete()`, `suggest()`

    + Index management operations: `get_index_statistics()`, `get_document_count()`

### Query the index

The queries in the notebook demonstrate different search patterns. The example vector queries are based on two strings:

+ Search string: `historic hotel walk to restaurants and shopping`
+ Vector query string: `quintessential lodging near running trails, eateries, retail` (vectorized into a mathematical representation)

The vector query string is semantically similar to the search string, but it includes terms that don't exist in the search index. If you do a keyword search for `quintessential lodging near running trails, eateries, retail`, results are zero. This example shows how you can get relevant results even if there are no matching terms.

#### Single vector search

The `Single vector search` cell demonstrates a basic scenario where you want to find document descriptions that closely match the search string. The `VectorizedQuery` contains the configuration of the vectorized query.

#### Single vector search with filter

In Azure AI Search, [filters](../../vector-search-filters.md) apply to nonvector fields in an index. The `Single vector search with filter` cell filters on the `Tags` field to filter out any hotels that don't provide free Wi-Fi.

#### Hybrid search

[Hybrid search](../../hybrid-search-overview.md) combines keyword and vector queries in one request. The `Hybrid search` cell runs the full-text and vector query strings concurrently.

Because Reciprocal Rank Fusion (RRF) merges results, it helps to review the inputs. In the full-text query only, the top two results are Sublime Palace Hotel and Luxury Lion Resort, with Sublime Palace Hotel having a stronger BM25 relevance score. In the vector-only query using HNSW, Sublime Palace Hotel drops to the fourth position. Luxury Lion, which was second in the full-text search and third in the vector search, doesn't experience the same range of fluctuation, so it appears as a top match in a homogenized result set.

#### Semantic hybrid search

Add [semantic ranking](../../semantic-search-overview.md) to rerank results based on language understanding. The `Semantic hybrid search` cell adds semantic ranking.

With semantic ranking, the Swirling Currents Hotel moves to the top spot. Without semantic ranking, Nordick's Valley Motel is number one. With semantic ranking, the machine comprehension models recognize that `historic` applies to "hotel within walking distance to dining (restaurants) and shopping."

Key takeaways:

+ In a hybrid search, you can integrate vector search with full-text search over keywords. Filters, spell check, and semantic ranking apply to textual content only, and not vectors.

+ Actual results include more detail, including semantic captions and highlights. Results were modified for readability. To get the full structure of the response, run the request in the REST client.

## Clean up resources

When you're working in your own subscription, it's a good idea at the end of a project to identify whether you still need the resources you created. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

You can find and manage resources in the Azure portal by using the **All resources** or **Resource groups** link in the leftmost pane.

Alternatively, you can run the `Clean up` code cell to delete the vector index created in this quickstart.

## Related content

+ [Vector search in Azure AI Search](../../vector-search-overview.md)
