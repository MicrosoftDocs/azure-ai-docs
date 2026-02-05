---
author: KarlErickson
ms.author: karler
ms.service: azure-ai-search
ms.custom: devx-track-java, dev-focus
ms.topic: include
ms.date: 02/05/2026
ai-usage: ai-assisted
---

In this quickstart, you use the [Azure AI Search client library for Java](/java/api/overview/azure/search-documents-readme) to create, load, and query a [vector index](../../vector-store.md). The Java client library provides an abstraction over the REST APIs for index operations.

In Azure AI Search, a vector index has an index schema that defines vector and nonvector fields, a vector search configuration for algorithms that create the embedding space, and settings on vector field definitions that are evaluated at query time. [Indexes - Create or Update](/rest/api/searchservice/indexes/create-or-update) (REST API) creates the vector index.

> [!TIP]
> + Want to get started right away? Download the [source code](https://github.com/Azure-Samples/azure-search-java-samples/tree/main/quickstart-vector-search) on GitHub.
> + This quickstart omits the vectorization step and provides inline embeddings. For [integrated chunking and vectorization](../../vector-search-integrated-vectorization.md) over your own content, try the [**Import data (new)** wizard](../../search-get-started-portal-import-vectors.md).

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

- An [Azure AI Search service](../../search-create-service-portal.md). You can use the Free tier for most of this quickstart, but we recommend Basic or higher for larger data files.

- [Semantic ranker enabled on your search service](../../semantic-how-to-enable-disable.md) for the optional semantic hybrid query.

- [Java 21 (LTS)](/java/openjdk/install) and [Maven](https://maven.apache.org/download.cgi).

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
   git clone https://github.com/Azure-Samples/azure-search-java-samples
   ```

1. Open the quickstart folder in Visual Studio Code.

   ```bash
   cd azure-search-java-samples/quickstart-vector-search
   code .
   ```

1. In `src/main/resources/application.properties`, replace the placeholder value for `azure.search.endpoint` with the URL you obtained in [Get endpoint](#get-endpoint).

1. Install the dependencies.

   ```bash
   mvn clean dependency:copy-dependencies
   ```

   When the build completes, you should see a `target/dependency` folder in the project directory.

1. For keyless authentication with Microsoft Entra ID, sign in to your Azure account.

    ```azurecli
    az login
    ```

## Run the code

1. Create the index.

    ```bash
    mvn compile exec:java -Dexec.mainClass="com.example.search.CreateIndex"
    ```

1. Upload documents to the index.

    ```bash
    mvn compile exec:java -Dexec.mainClass="com.example.search.UploadDocuments"
    ```

1. Run queries. Start with a single vector search.

    ```bash
    mvn compile exec:java -Dexec.mainClass="com.example.search.SearchSingle"
    ```

1. (Optional) Run additional query variations.

    ```bash
    mvn compile exec:java -Dexec.mainClass="com.example.search.SearchSingleWithFilter"
    mvn compile exec:java -Dexec.mainClass="com.example.search.SearchSingleWithFilterGeo"
    mvn compile exec:java -Dexec.mainClass="com.example.search.SearchHybrid"
    mvn compile exec:java -Dexec.mainClass="com.example.search.SearchSemanticHybrid"
    ```

### Output

`CreateIndex.java` creates the index:

```output
Using Azure Search endpoint: https://<search-service-name>.search.windows.net
Using Azure Search index: hotels-vector-quickstart
Creating index...
hotels-vector-quickstart created
```

`UploadDocuments.java` uploads documents:

```output
Using Azure Search endpoint: https://<search-service-name>.search.windows.net
Using Azure Search index: hotels-vector-quickstart
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

`SearchSingle.java` returns single vector search results:

```output
Using Azure Search endpoint: https://<search-service-name>.search.windows.net
Using Azure Search index: hotels-vector-quickstart

Single Vector search found 5
- HotelId: 48, HotelName: Nordick's Valley Motel, Tags: ["continental breakfast","air conditioning","free wifi"], Score 0.6605852
- HotelId: 13, HotelName: Luxury Lion Resort, Tags: ["bar","concierge","restaurant"], Score 0.6333684
- HotelId: 4, HotelName: Sublime Palace Hotel, Tags: ["concierge","view","air conditioning"], Score 0.605672
- HotelId: 49, HotelName: Swirling Currents Hotel, Tags: ["air conditioning","laundry service","24-hour front desk service"], Score 0.6026341
- HotelId: 2, HotelName: Old Century Hotel, Tags: ["pool","free wifi","air conditioning","concierge"], Score 0.57902366
```

## Understand the code

Now that you've run the code, let's break down the key steps:

1. [Create a vector index](#create-a-vector-index)
1. [Upload documents to the index](#upload-documents-to-the-index)
1. [Query the index](#query-the-index)

### Create a vector index

The following code in `CreateIndex.java` creates the index schema, including the vector field `DescriptionVector`:

:::code language="java" source="~/azure-search-java-samples/quickstart-vector-search/src/main/java/com/example/search/CreateIndex.java" :::

Key takeaways:

+ You define an index by creating a list of fields.

+ This particular index supports multiple search capabilities, including full-text keyword search, vector search (enables hybrid search by collocating vector and nonvector fields), semantic search, faceted search, geo-spatial search, and filtering.

+ Vector fields contain floating point values. The dimensions attribute has a minimum of 2 and a maximum of 4096 floating point values each. This quickstart sets the dimensions attribute to 1,536 because that's the size of embeddings generated by the `text-embedding-ada-002` model.

### Upload documents to the index

The following code in `UploadDocuments.java` uploads JSON-formatted documents to your search service:

:::code language="java" source="~/azure-search-java-samples/quickstart-vector-search/src/main/java/com/example/search/UploadDocuments.java" :::

Key takeaways:

+ Your code interacts with a specific search index hosted in your Azure AI Search service through the `SearchClient`, which is the main object provided by the Azure Search Documents package. The `SearchClient` provides access to operations such as:

    + Data ingestion: `uploadDocuments`, `mergeDocuments`, `deleteDocuments`

    + Search operations: `search`, `autocomplete`, `suggest`

### Query the index

The queries in the search files demonstrate different search patterns. The example vector queries are based on two strings:

+ Search string: `historic hotel walk to restaurants and shopping`
+ Vector query string: `quintessential lodging near running trails, eateries, retail` (vectorized into a mathematical representation)

The vector query string is semantically similar to the search string, but it includes terms that don't exist in the search index. If you do a keyword search for `quintessential lodging near running trails, eateries, retail`, results are zero. This example shows how you can get relevant results even if there are no matching terms.

#### Single vector search

The `SearchSingle.java` demonstrates a basic scenario where you want to find document descriptions that closely match the search string:

:::code language="java" source="~/azure-search-java-samples/quickstart-vector-search/src/main/java/com/example/search/SearchSingle.java" :::

#### Single vector search with filter

In Azure AI Search, [filters](../../vector-search-filters.md) apply to nonvector fields in an index. The `SearchSingleWithFilter.java` file filters on the `Tags` field to filter out any hotels that don't provide free Wi-Fi:

:::code language="java" source="~/azure-search-java-samples/quickstart-vector-search/src/main/java/com/example/search/SearchSingleWithFilter.java" :::

For a geo filter, you can specify a geospatial filter to limit results to a specific geographic area. The `SearchSingleWithFilterGeo.java` file limits results to hotels within 300 kilometers of Washington D.C.:

:::code language="java" source="~/azure-search-java-samples/quickstart-vector-search/src/main/java/com/example/search/SearchSingleWithFilterGeo.java" :::

#### Hybrid search

[Hybrid search](../../hybrid-search-overview.md) combines keyword and vector queries in one request. The `SearchHybrid.java` file runs the full-text and vector query strings concurrently:

:::code language="java" source="~/azure-search-java-samples/quickstart-vector-search/src/main/java/com/example/search/SearchHybrid.java" :::

Because Reciprocal Rank Fusion (RRF) merges results, it helps to review the inputs. In the full-text query only, the top two results are Sublime Palace Hotel and Luxury Lion Resort, with Sublime Palace Hotel having a stronger BM25 relevance score. In the vector-only query using HNSW, Sublime Palace Hotel drops to the fourth position. Luxury Lion, which was second in the full-text search and third in the vector search, doesn't experience the same range of fluctuation, so it appears as a top match in a homogenized result set.

#### Semantic hybrid search

Add [semantic ranking](../../semantic-search-overview.md) to rerank results based on language understanding. The `SearchSemanticHybrid.java` file adds semantic ranking:

:::code language="java" source="~/azure-search-java-samples/quickstart-vector-search/src/main/java/com/example/search/SearchSemanticHybrid.java" :::

With semantic ranking, the Swirling Currents Hotel moves to the top spot. Without semantic ranking, Nordick's Valley Motel is number one. With semantic ranking, the machine comprehension models recognize that `historic` applies to "hotel within walking distance to dining (restaurants) and shopping."

Key takeaways:

+ In a hybrid search, you can integrate vector search with full-text search over keywords. Filters, spell check, and semantic ranking apply to textual content only, and not vectors.

+ Actual results include more detail, including semantic captions and highlights. Results were modified for readability. To get the full structure of the response, run the request in the REST client.

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

## Related content

+ Review the repository of code samples for vector search capabilities in Azure AI Search for [Java](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-java).
