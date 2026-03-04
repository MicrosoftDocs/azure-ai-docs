---
author: KarlErickson
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom: devx-track-java
ms.topic: include
ms.date: 03/04/2026
ai-usage: ai-assisted
---

In this quickstart, you use the [Azure AI Search client library for Java](/java/api/overview/azure/search-documents-readme) to add [semantic ranking](../../semantic-search-overview.md) to an existing search index and query the index.

Semantic ranking is query-side functionality that uses machine reading comprehension to rescore search results, promoting the most semantically relevant matches to the top of the list. You can add a semantic configuration to an existing index with no rebuild requirement.  Semantic ranking is most effective for informational or descriptive text.

> [!TIP]
> Want to get started right away? Download the [source code](https://github.com/Azure-Samples/azure-search-java-samples/tree/main/quickstart-semantic-ranking) on GitHub.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](../../search-create-service-portal.md) with [semantic ranker enabled](../../semantic-how-to-enable-disable.md).

+ An [index](../../search-how-to-create-search-index.md) with descriptive text fields attributed as `searchable` and `retrievable`.  This quickstart assumes the [hotels-sample](../../search-get-started-portal.md) index.

+ [Java 21 (LTS)](/java/openjdk/install) and [Maven](https://maven.apache.org/download.cgi).

+ [Visual Studio Code](https://code.visualstudio.com/download).

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

1. Get the existing index settings.

    ```bash
    mvn compile exec:java "-Dexec.mainClass=com.azure.search.quickstart.GetIndexSettings"
    ```

1. Update the index with a semantic configuration.

    ```bash
    mvn compile exec:java "-Dexec.mainClass=com.azure.search.quickstart.UpdateIndexSettings"
    ```

1. Run a semantic query.

    ```bash
    mvn compile exec:java "-Dexec.mainClass=com.azure.search.quickstart.SemanticQuery"
    ```

1. Run a semantic query with captions.

    ```bash
    mvn compile exec:java "-Dexec.mainClass=com.azure.search.quickstart.SemanticQueryWithCaptions"
    ```

1. Run a semantic query with answers.

    ```bash
    mvn compile exec:java "-Dexec.mainClass=com.azure.search.quickstart.SemanticAnswer"
    ```

### Output

The output of `GetIndexSettings.java` is the name of the index, its fields, and its semantic configurations. Before you add a new configuration, the index has only the default one.

```output
Index name: hotels-sample
Number of fields: 23
Field: HotelId, Type: Edm.String, Searchable: true
Field: HotelName, Type: Edm.String, Searchable: true
Field: Description, Type: Edm.String, Searchable: true
// Trimmed for brevity
Semantic search configurations: 1
Configuration name: hotels-sample-semantic-configuration
```

The output of `UpdateIndexSettings.java` lists all semantic configurations on the index, including the one the code added, followed by a success message.

```output
// Trimmed for brevity
Configuration name: semantic-config
Title field: HotelName
Keywords fields: Tags
Content fields: Description
----------------------------------------
Semantic configuration updated successfully.
```

The output of `SemanticQuery.java` returns all matching documents ordered by the semantic ranking re-ranker score.

```output
Search result #1:
  Re-ranker Score: 2.61
  HotelId: 24
  HotelName: Uptown Chic Hotel
  Description: Chic hotel near the city. High-rise hotel in downtown, within walking distance to theaters, art galleries, restaurants and shops. Visit Seattle Art Museum by day, and then head over to Benaroya Hall to catch the evening's concert performance.

Search result #2:
  Re-ranker Score: 2.27
  HotelId: 2
  HotelName: Old Century Hotel
  Description: The hotel is situated in a nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts. The hotel also regularly hosts events like wine tastings, beer dinners, and live music.

Search result #3:
  Re-ranker Score: 1.99
  HotelId: 4
  HotelName: Sublime Palace Hotel
  Description: Sublime Cliff Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Cliff is part of a lovingly restored 19th century resort, updated for every modern convenience.
// Trimmed for brevity
```

The output of `SemanticQueryWithCaptions.java` adds a caption element with hit highlighting alongside search fields. Captions are the most relevant passages in a result. If your index includes larger text, captions help extract the most interesting sentences.

```output
Search result #1:
  Re-ranker Score: 2.61
  HotelName: Uptown Chic Hotel
  Description: Chic hotel near the city. High-rise hotel in downtown, within walking distance to theaters, art galleries, restaurants and shops. Visit Seattle Art Museum by day, and then head over to Benaroya Hall to catch the evening's concert performance.

  Caption with highlights: Chic hotel near the city. High-rise hotel in downtown, within walking distance to<em> theaters, </em>art galleries, restaurants and shops. Visit<em> Seattle Art Museum </em>by day, and then head over to<em> Benaroya Hall </em>to catch the evening's concert performance.
------------------------------------------------------------
Search result #2:
  Re-ranker Score: 2.27
  HotelName: Old Century Hotel
  Description: The hotel is situated in a nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts. The hotel also regularly hosts events like wine tastings, beer dinners, and live music.

  Caption text: The hotel is situated in a nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts. The hotel also regularly hosts events like wine tastings, beer dinners, and live.
------------------------------------------------------------
// Trimmed for brevity
```

The output of `SemanticAnswer.java` includes a semantic answer pulled from one of the results that best matches the question, followed by search results with captions.

```output
Semantic answer result #1:
Semantic Answer: Nature is Home on the beach. Explore the shore by day, and then come home to our shared living space to relax around a stone fireplace, sip something warm, and explore the<em> library </em>by night. Save up to 30 percent. Valid Now through the end of the year. Restrictions and blackouts may apply.
Semantic Answer Score: 0.98

Search Results:

Search result #1:
Re-ranker Score: 2.12
Hotel: Stay-Kay City Hotel
Description: This classic hotel is fully-refurbished and ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Times Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.
Caption: This classic hotel is<em> fully-refurbished </em>and ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Times Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.

Search result #2:
Re-ranker Score: 2.07
Hotel: Double Sanctuary Resort
Description: 5 star Luxury Hotel - Biggest Rooms in the city. #1 Hotel in the area listed by Traveler magazine. Free WiFi, Flexible check in/out, Fitness Center & espresso in room.
Caption: <em>5 star Luxury Hotel </em>-<em> Biggest </em>Rooms in the city. #1 Hotel in the area listed by Traveler magazine. Free WiFi, Flexible check in/out, Fitness Center & espresso in room.
// Trimmed for brevity
```

## Understand the code

[!INCLUDE [understand code note](../understand-code-note.md)]

Now that you've run the code, let's break down the key steps:

1. [Configuration and authentication](#configuration-and-authentication)
1. [Update the index with a semantic configuration](#update-the-index-with-a-semantic-configuration)
1. [Query the index](#query-the-index)

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

The `UpdateIndexSettings.java` class adds a semantic configuration to the existing `hotels-sample` index. This operation doesn't delete any search documents, and your index remains operational after the configuration is added.

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
+ `SemanticConfiguration` pairs a name with the prioritized fields, identifying which semantic configuration to use at query time.
+ `createOrUpdateIndex` pushes the updated schema to the search service without rebuilding the index or deleting documents.

### Query the index

The following three classes query the index in sequence, progressing from a basic semantic search to semantic ranking with captions and answers.

#### Semantic query (no captions, no answers)

The first query adds semantic ranking with no captions or answers. The `SemanticQuery.java` class shows the minimum requirement for invoking semantic ranking.

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

#### Semantic query with captions

The `SemanticQueryWithCaptions.java` class adds captions to extract the most relevant passages from each result, with hit highlighting applied to the important terms and phrases.

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

#### Semantic query with answers

The `SemanticAnswer.java` class adds semantic answers. This class uses a question as the search text because semantic answers work best when the query is phrased as a question. The answer is a verbatim passage extracted from your index, not a composed response from a chat completion model.

The query and the indexed content must be closely aligned for an answer to be returned. If no candidate meets the confidence threshold, the response doesn't include an answer. This example uses a question that's known to produce a result so that you can see the syntax. If answers aren't useful for your scenario, omit `setQueryAnswer` from your code. For composed answers, consider a [RAG pattern](../../retrieval-augmented-generation-overview.md) or [agentic retrieval](../../agentic-retrieval-overview.md).

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
