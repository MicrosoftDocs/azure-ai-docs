---
author: KarlErickson
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom: devx-track-java
ms.topic: include
ms.date: 01/30/2026
ai-usage: ai-assisted
---

In this quickstart, you use the [Azure AI Search Java SDK](https://search.maven.org/artifact/com.azure/azure-search-documents) client library to add [semantic ranking](../../semantic-search-overview.md) to an existing search index.

In Azure AI Search, semantic ranking is query-side functionality that uses machine reading comprehension from Microsoft to rescore search results, promoting the most semantically relevant matches to the top of the list. Depending on the content and query, semantic ranking can [significantly improve search relevance](https://techcommunity.microsoft.com/t5/azure-ai-services-blog/azure-cognitive-search-outperforming-vector-search-with-hybrid/ba-p/3929167) with minimal developer effort.

You can add a semantic configuration to an existing index with no rebuild requirement. Semantic ranking is most effective for text that's informational or descriptive.

> [!TIP]
> Want to get started right away? Download the [source code](https://github.com/Azure-Samples/azure-search-java-samples/tree/main/quickstart-semantic-ranking) on GitHub.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](../../search-create-service-portal.md) with [semantic ranker enabled](../../semantic-how-to-enable-disable.md).

+ An [index](../../search-how-to-create-search-index.md) with descriptive text fields that are attributed as `searchable` and `retrievable`. This quickstart assumes the [hotels-sample-index](../../search-get-started-portal.md).

+ [Java 21 (LTS)](/java/openjdk/install) and [Maven](https://maven.apache.org/download.cgi).

+ [Visual Studio Code](https://code.visualstudio.com/download) with Java extensions, or [IntelliJ IDEA](https://www.jetbrains.com/idea/).

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
    git clone https://github.com/Azure-Samples/azure-search-java-samples
    ```

1. Navigate to the quickstart folder and open it in Visual Studio Code.

    ```bash
    cd azure-search-java-samples/quickstart-semantic-ranking
    code .
    ```

1. In `src/main/resources/application.properties`, replace the placeholder value for `azure.search.endpoint` with the URL you obtained in [Get endpoint](#get-endpoint).

1. Compile the project to resolve dependencies, including [azure-search-documents](https://search.maven.org/artifact/com.azure/azure-search-documents).

    ```bash
    mvn compile
    ```

    When the build completes, verify that no errors appear in the output.

1. For keyless authentication with Microsoft Entra ID, sign in to your Azure account. If you have multiple subscriptions, select the one that contains your Azure AI Search service.

    ```azurecli
    az login
    ```

## Run the code

Run each class in sequence to see the full progression from index settings to semantic queries.

1. Get the existing index settings.

    ```console
    mvn compile exec:java \
        -Dexec.mainClass="com.azure.search.quickstart.GetIndexSettings"
    ```

   Output is the name of the index, list of fields, and a statement indicating whether a semantic configuration exists. For the purposes of this quickstart, the message should say "No semantic configuration exists for this index".

1. Update the index with a semantic configuration.

    ```console
    mvn compile exec:java \
        -Dexec.mainClass="com.azure.search.quickstart.UpdateIndexSettings"
    ```

   Output is the semantic configuration you just added.

1. Run a semantic query.

    ```console
    mvn compile exec:java \
        -Dexec.mainClass="com.azure.search.quickstart.SemanticQuery"
    ```

   Output consists of 13 documents, ordered by the reranker score.

1. Run a semantic query with captions.

    ```console
    mvn compile exec:java \
        -Dexec.mainClass="com.azure.search.quickstart.SemanticQueryWithCaptions"
    ```

   Output includes a new caption element alongside search fields.

1. Run a semantic query with answers.

    ```console
    mvn compile exec:java \
        -Dexec.mainClass="com.azure.search.quickstart.SemanticAnswer"
    ```

### Output

Output from the captions query includes extractive captions with hit highlighting. Captions are the most relevant passages in a result. If your index includes larger text, a caption is helpful for extracting the most interesting sentences.

```output
Search result #1:
  Re-ranker Score: 2.61
  HotelName: Uptown Chic Hotel
  Description: Chic hotel near the city. High-rise hotel in
  downtown, within walking distance to theaters, art galleries,
  restaurants and shops. Visit Seattle Art Museum by day, and then
  head over to Benaroya Hall to catch the evening's concert
  performance.

  Caption with highlights: Chic hotel near the city. High-rise
  hotel in downtown, within walking distance to<em> theaters,
  </em>art galleries, restaurants and shops. Visit<em> Seattle Art
  Museum </em>by day, and then head over to<em> Benaroya Hall
  </em>to catch the evening's concert performance.
```

Output from the answers query includes a semantic answer (verbatim content) pulled from one of the results that best matches the question.

```output
Semantic Answer: Nature is Home on the beach. Explore the shore by
day, and then come home to our shared living space to relax around
a stone fireplace, sip something warm, and explore the<em> library
</em>by night. Save up to 30 percent. Valid Now through the end of
the year. Restrictions and blackouts may apply.
Semantic Answer Score: 0.98
```

Recall that answers are *verbatim content* pulled from your index and might be missing phrases that a user would expect to see. To get *composed answers* as generated by a chat completion model, consider using a [RAG pattern](../../retrieval-augmented-generation-overview.md) or [agentic retrieval](../../agentic-retrieval-overview.md).

## Understand the code

[!INCLUDE [understand code note](../understand-code-note.md)]

Now that you've run the code, let's break down the key steps:

1. [Configuration and authentication](#configuration-and-authentication)
1. [Update the index with a semantic configuration](#update-the-index-with-a-semantic-configuration)
1. [Run semantic queries](#run-semantic-queries)

### Configuration and authentication

The `SearchConfig.java` class loads properties from `application.properties` and creates a `DefaultAzureCredential` for keyless authentication.

```java
import com.azure.identity.DefaultAzureCredential;
import com.azure.identity.DefaultAzureCredentialBuilder;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class SearchConfig {
    private static final Properties properties =
        new Properties();

    static {
        try (InputStream input = SearchConfig.class
            .getClassLoader()
            .getResourceAsStream(
                "application.properties")) {
            properties.load(input);
        } catch (IOException e) {
            throw new RuntimeException(
                "Failed to load application.properties",
                e);
        }
    }

    public static final String SEARCH_ENDPOINT =
        properties.getProperty(
            "azure.search.endpoint");
    public static final String INDEX_NAME =
        properties.getProperty(
            "azure.search.index.name");
    public static final String SEMANTIC_CONFIG_NAME =
        properties.getProperty(
            "semantic.configuration.name");

    public static final DefaultAzureCredential
        CREDENTIAL = new DefaultAzureCredentialBuilder()
            .build();
}
```

Key takeaways:

+ `DefaultAzureCredential` provides keyless authentication using Microsoft Entra ID. It chains multiple credential types, including the Azure CLI credential from `az login`.

+ Properties are loaded from the `application.properties` file in the classpath.

+ Static fields (`SEARCH_ENDPOINT`, `INDEX_NAME`, `SEMANTIC_CONFIG_NAME`, `CREDENTIAL`) are shared across all classes in the project.

### Update the index with a semantic configuration

The `UpdateIndexSettings.java` class adds a semantic configuration to the existing `hotels-sample-index` index. No search documents are deleted by this operation and your index is still operational after the configuration is added.

```java
import com.azure.search.documents.indexes
    .SearchIndexClientBuilder;
import com.azure.search.documents.indexes.models
    .SearchIndex;
import com.azure.search.documents.indexes.models
    .SemanticConfiguration;
import com.azure.search.documents.indexes.models
    .SemanticField;
import com.azure.search.documents.indexes.models
    .SemanticPrioritizedFields;
import com.azure.search.documents.indexes.models
    .SemanticSearch;

import java.util.ArrayList;
import java.util.List;

var indexClient = new SearchIndexClientBuilder()
    .endpoint(SearchConfig.SEARCH_ENDPOINT)
    .credential(SearchConfig.CREDENTIAL)
    .buildClient();

SearchIndex existingIndex =
    indexClient.getIndex(SearchConfig.INDEX_NAME);

var prioritizedFields =
    new SemanticPrioritizedFields()
        .setTitleField(
            new SemanticField("HotelName"))
        .setKeywordsFields(
            List.of(new SemanticField("Tags")))
        .setContentFields(
            List.of(
                new SemanticField("Description")));

var newSemanticConfiguration =
    new SemanticConfiguration(
        SearchConfig.SEMANTIC_CONFIG_NAME,
        prioritizedFields);

SemanticSearch semanticSearch =
    existingIndex.getSemanticSearch();
if (semanticSearch == null) {
    semanticSearch = new SemanticSearch();
    existingIndex.setSemanticSearch(semanticSearch);
}

List<SemanticConfiguration> configurations =
    semanticSearch.getConfigurations();
if (configurations == null) {
    configurations = new ArrayList<>();
    semanticSearch.setConfigurations(configurations);
}

configurations.add(newSemanticConfiguration);

indexClient.createOrUpdateIndex(existingIndex);
```

Key takeaways:

+ `SemanticPrioritizedFields` defines which fields the semantic ranker evaluates. `setTitleField` sets the document title, `setContentFields` sets the main content, and `setKeywordsFields` sets the keyword or tag fields.

+ `SemanticConfiguration` pairs a name with the prioritized fields, identifying which semantic config to use at query time.

+ `createOrUpdateIndex` pushes the updated schema to the search service without rebuilding the index or deleting documents.

### Run semantic queries

Once the index has a semantic configuration, you can run queries that include semantic parameters. This code shows the minimum requirement for invoking semantic ranking.

```java
import com.azure.search.documents
    .SearchClientBuilder;
import com.azure.search.documents.SearchDocument;
import com.azure.search.documents.models.QueryType;
import com.azure.search.documents.models.SearchOptions;
import com.azure.search.documents.models.SearchResult;
import com.azure.search.documents.models
    .SemanticSearchOptions;
import com.azure.search.documents.util
    .SearchPagedIterable;

var searchClient = new SearchClientBuilder()
    .endpoint(SearchConfig.SEARCH_ENDPOINT)
    .indexName(SearchConfig.INDEX_NAME)
    .credential(SearchConfig.CREDENTIAL)
    .buildClient();

var searchOptions = new SearchOptions()
    .setQueryType(QueryType.SEMANTIC)
    .setSemanticSearchOptions(
        new SemanticSearchOptions()
            .setSemanticConfigurationName(
                SearchConfig.SEMANTIC_CONFIG_NAME))
    .setSelect("HotelId", "HotelName", "Description");

SearchPagedIterable results = searchClient.search(
    "walking distance to live music",
    searchOptions, null);

for (SearchResult result : results) {
    var document = result.getDocument(
        SearchDocument.class);
    double rerankerScore = result
        .getSemanticSearch().getRerankerScore();

    System.out.printf("Re-ranker Score: %.2f%n",
        rerankerScore);
    System.out.printf("HotelName: %s%n",
        document.get("HotelName"));
    System.out.printf("Description: %s%n%n",
        document.get("Description"));
}
```

Key takeaways:

+ `QueryType.SEMANTIC` enables semantic ranking on the query.

+ `setSemanticConfigurationName` specifies which semantic configuration to use.

+ `SearchPagedIterable` provides an iterable over the reranked results. Each `SearchResult` contains a `getSemanticSearch()` accessor for the reranker score.

#### Extractive captions

This code adds captions to extract portions of the text and apply hit highlighting to the important terms and phrases.

```java
import com.azure.search.documents.models
    .QueryCaption;
import com.azure.search.documents.models
    .QueryCaptionResult;
import com.azure.search.documents.models
    .QueryCaptionType;

var searchOptions = new SearchOptions()
    .setQueryType(QueryType.SEMANTIC)
    .setSemanticSearchOptions(
        new SemanticSearchOptions()
            .setSemanticConfigurationName(
                SearchConfig.SEMANTIC_CONFIG_NAME)
            .setQueryCaption(
                new QueryCaption(
                    QueryCaptionType.EXTRACTIVE)
                    .setHighlightEnabled(true)))
    .setSelect(
        "HotelId", "HotelName", "Description");

SearchPagedIterable results = searchClient.search(
    "walking distance to live music",
    searchOptions, null);

for (SearchResult result : results) {
    List<QueryCaptionResult> captions =
        result.getSemanticSearch()
            .getQueryCaptions();
    if (captions != null && !captions.isEmpty()) {
        QueryCaptionResult caption = captions.get(0);
        if (caption.getHighlights() != null) {
            System.out.printf(
                "Caption: %s%n",
                caption.getHighlights());
        }
    }
}
```

Key takeaways:

+ `QueryCaption(QueryCaptionType.EXTRACTIVE)` enables extractive captions from the content fields.

+ `setHighlightEnabled(true)` adds `<em>` tags around important terms in captions.

+ Each `SearchResult` provides `getQueryCaptions()` on the semantic search accessor.

#### Semantic answers

This code returns semantic answers for question-like queries. Semantic ranker can produce an answer to a query string that has the characteristics of a question. The generated answer is extracted verbatim from your content so it doesn't include composed content like what you might expect from a chat completion model.

To produce a semantic answer, the question and answer must be closely aligned, and the model must find content that clearly answers the question. If potential answers fail to meet a confidence threshold, the model doesn't return an answer.

```java
import com.azure.search.documents.models
    .QueryAnswer;
import com.azure.search.documents.models
    .QueryAnswerResult;
import com.azure.search.documents.models
    .QueryAnswerType;

var searchOptions = new SearchOptions()
    .setQueryType(QueryType.SEMANTIC)
    .setSemanticSearchOptions(
        new SemanticSearchOptions()
            .setSemanticConfigurationName(
                SearchConfig.SEMANTIC_CONFIG_NAME)
            .setQueryCaption(
                new QueryCaption(
                    QueryCaptionType.EXTRACTIVE))
            .setQueryAnswer(
                new QueryAnswer(
                    QueryAnswerType.EXTRACTIVE)))
    .setSelect(
        "HotelName", "Description", "Category");

SearchPagedIterable results = searchClient.search(
    "What's a good hotel for people who like to read",
    searchOptions, null);

List<QueryAnswerResult> semanticAnswers =
    results.getSemanticResults().getQueryAnswers();

for (QueryAnswerResult answer :
    semanticAnswers != null ? semanticAnswers
        : List.<QueryAnswerResult>of()) {
    if (answer.getHighlights() != null) {
        System.out.printf(
            "Semantic Answer: %s%n",
            answer.getHighlights());
    } else {
        System.out.printf(
            "Semantic Answer: %s%n",
            answer.getText());
    }
    System.out.printf(
        "Semantic Answer Score: %.2f%n",
        answer.getScore());
}
```

Key takeaways:

+ `QueryAnswer(QueryAnswerType.EXTRACTIVE)` enables extractive answers for question-like queries.

+ Answers are verbatim content extracted from your index, not generated text.

+ `results.getSemanticResults().getQueryAnswers()` retrieves the answer objects separately from the search results.

+ For composed answers, consider [RAG patterns](../../retrieval-augmented-generation-overview.md) or [agentic retrieval](../../agentic-retrieval-overview.md).
