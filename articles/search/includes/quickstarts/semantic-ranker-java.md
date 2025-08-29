---
author: KarlErickson
ms.author: karler
ms.service: azure-ai-search
ms.custom: devx-track-java
ms.topic: include
ms.date: 08/22/2025
ai-usage: ai-assisted
---

[!INCLUDE [Semantic ranker introduction](semantic-ranker-intro.md)]

## Set up the client

In this quickstart, you use an IDE and the [**Azure AI Search Java SDK**](https://search.maven.org/artifact/com.azure/azure-search-documents) client library to add semantic ranking to an existing search index.

The quickstart assumes the following is available on your computer:
- [Visual Studio Code](https://code.visualstudio.com/) with Java extensions or IntelliJ IDEA
- [Java 21 (LTS)](/java/openjdk/install).
- [Maven](https://maven.apache.org/download.cgi).

### Set up local development environment

1. Create a new Maven project directory.

   ```bash
   mkdir semantic-ranking-quickstart && cd semantic-ranking-quickstart
   code .
   ```

1. Create a `pom.xml` file with required dependencies.

   ```xml
   <project xmlns="http://maven.apache.org/POM/4.0.0"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
            http://maven.apache.org/xsd/maven-4.0.0.xsd">
       <modelVersion>4.0.0</modelVersion>
   
       <groupId>com.azure.search</groupId>
       <artifactId>semantic-ranking-quickstart</artifactId>
       <version>1.0-SNAPSHOT</version>
   
       <properties>
           <maven.compiler.source>21</maven.compiler.source>
           <maven.compiler.target>21</maven.compiler.target>
           <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
       </properties>
   
       <dependencies>
           <dependency>
               <groupId>com.azure</groupId>
               <artifactId>azure-search-documents</artifactId>
               <version>11.7.8</version>
           </dependency>
           <dependency>
               <groupId>com.azure</groupId>
               <artifactId>azure-identity</artifactId>
               <version>1.17.0</version>
           </dependency>
       </dependencies>
   </project>
   ```

1. Compile the project to resolve the dependencies:

    ```bash
    mvn compile
    ```

1. Create the source directory structure.

   ```bash
   mkdir -p src/main/java/com/azure/search/quickstart
   mkdir -p src/main/resources
   ```

1. Create `src/main/resources/application.properties` and provide your search service endpoint. You can get the endpoint from the Azure portal on the search service **Overview** page.

    ```properties
    azure.search.endpoint=YOUR-SEARCH-SERVICE-ENDPOINT
    azure.search.index.name=hotels-sample-index
    semantic.configuration.name=semantic-config
    ```

### Sign in to Azure

If you signed in to the [Azure portal](https://portal.azure.com), you're signed into Azure. If you aren't sure, use the Azure CLI to log in: `az login`. If you have multiple tenants and subscriptions, see [Quickstart: Connect without keys](../../search-get-started-rbac.md) for help on how to connect.

## Create a common configuration class

Create a file in `src/main/java/com/azure/search/quickstart` called `SearchConfig.java` to read the properties file and hold the environment variables and authentication credential.

```java
package com.azure.search.quickstart;

import com.azure.identity.DefaultAzureCredential;
import com.azure.identity.DefaultAzureCredentialBuilder;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class SearchConfig {
    private static final Properties properties = new Properties();

    static {
        try (InputStream input = SearchConfig.class.getClassLoader()
            .getResourceAsStream("application.properties")) {
            properties.load(input);
        } catch (IOException e) {
            throw new RuntimeException(
                "Failed to load application.properties", e);
        }
    }

    public static final String SEARCH_ENDPOINT =
        properties.getProperty("azure.search.endpoint");
    public static final String INDEX_NAME =
        properties.getProperty("azure.search.index.name");
    public static final String SEMANTIC_CONFIG_NAME =
        properties.getProperty("semantic.configuration.name");

    public static final DefaultAzureCredential CREDENTIAL =
        new DefaultAzureCredentialBuilder().build();

    static {
        System.out.println("Using Azure Search endpoint: " + SEARCH_ENDPOINT);
        System.out.println("Using index name: " + INDEX_NAME + "\n");
    }
}
```

## Get the index schema

In this section, you get settings for the existing `hotels-sample-index` index on your search service.

1. Create a file in `src/main/java/com/azure/search/quickstart` called `GetIndexSettings.java`.

    ```java
    package com.azure.search.quickstart;
    
    import com.azure.search.documents.indexes.SearchIndexClientBuilder;
    import com.azure.search.documents.indexes.models.SearchField;
    import com.azure.search.documents.indexes.models.SearchIndex;
    import com.azure.search.documents.indexes.models.SemanticConfiguration;
    import com.azure.search.documents.indexes.models.SemanticField;
    import com.azure.search.documents.indexes.models.SemanticSearch;
    
    public class GetIndexSettings {
        public static void main(String[] args) {
            var indexClient = new SearchIndexClientBuilder()
                .endpoint(SearchConfig.SEARCH_ENDPOINT)
                .credential(SearchConfig.CREDENTIAL)
                .buildClient();
    
            System.out.println("Getting semantic search index settings...");
    
            SearchIndex index = indexClient.getIndex(SearchConfig.INDEX_NAME);
    
            System.out.println("Index name: " + index.getName());
            System.out.println("Number of fields: " + index.getFields().size());
    
            for (SearchField field : index.getFields()) {
                System.out.printf("Field: %s, Type: %s, Searchable: %s%n",
                    field.getName(), field.getType(), field.isSearchable());
            }
    
            SemanticSearch semanticSearch = index.getSemanticSearch();
            if (semanticSearch != null &&
                semanticSearch.getConfigurations() != null) {
                System.out.println("Semantic search configurations: " +
                    semanticSearch.getConfigurations().size());
                for (SemanticConfiguration config :
                    semanticSearch.getConfigurations()) {
                    System.out.println("Configuration name: " + config.getName());
                    SemanticField titleField = config.getPrioritizedFields().getTitleField();
                    if (titleField != null) {
                        System.out.println("Title field: " +
                            titleField.getFieldName());
                    }
                }
            } else {
                System.out.println(
                    "No semantic configuration exists for this index.");
            }
    
            System.exit(0);
        }
    }
    ```

1. Compile and run the code:

    ```bash
    mvn compile exec:java -Dexec.mainClass="com.azure.search.quickstart.GetIndexSettings"
    ```

1. Output is the name of the index, list of fields, and a statement indicating whether a semantic configuration exists. For the purposes of this quickstart, the message should say `No semantic configuration exists for this index`.

## Update the index with a semantic configuration

1. Create a file in `src/main/java/com/azure/search/quickstart` called `UpdateIndexSettings.java` to add a semantic configuration to the existing `hotels-sample-index` index on your search service.

    ```java
    package com.azure.search.quickstart;
    
    import com.azure.search.documents.indexes.SearchIndexClientBuilder;
    import com.azure.search.documents.indexes.models.SearchIndex;
    import com.azure.search.documents.indexes.models.SemanticConfiguration;
    import com.azure.search.documents.indexes.models.SemanticField;
    import com.azure.search.documents.indexes.models.SemanticPrioritizedFields;
    import com.azure.search.documents.indexes.models.SemanticSearch;
    
    import java.util.ArrayList;
    import java.util.List;
    
    public class UpdateIndexSettings {
        public static void main(String[] args) {
            try {
                var indexClient = new SearchIndexClientBuilder()
                    .endpoint(SearchConfig.SEARCH_ENDPOINT)
                    .credential(SearchConfig.CREDENTIAL)
                    .buildClient();
    
                SearchIndex existingIndex =
                    indexClient.getIndex(SearchConfig.INDEX_NAME);
    
                // Create prioritized fields for semantic configuration
                var prioritizedFields = new SemanticPrioritizedFields()
                    .setTitleField(new SemanticField("HotelName"))
                    .setKeywordsFields(List.of(new SemanticField("Tags")))
                    .setContentFields(List.of(new SemanticField("Description")));
    
                var newSemanticConfiguration = new SemanticConfiguration(
                    SearchConfig.SEMANTIC_CONFIG_NAME, prioritizedFields);
    
                // Add the semantic configuration to the index
                SemanticSearch semanticSearch = existingIndex.getSemanticSearch();
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
    
                // Check if configuration already exists
                boolean configExists = configurations.stream()
                    .anyMatch(config -> SearchConfig.SEMANTIC_CONFIG_NAME
                        .equals(config.getName()));
    
                if (!configExists) {
                    configurations.add(newSemanticConfiguration);
                }
    
                indexClient.createOrUpdateIndex(existingIndex);
    
                SearchIndex updatedIndex =
                    indexClient.getIndex(SearchConfig.INDEX_NAME);
    
                System.out.println("Semantic configurations:");
                System.out.println("-".repeat(40));
    
                SemanticSearch updatedSemanticSearch =
                    updatedIndex.getSemanticSearch();
                if (updatedSemanticSearch != null &&
                    updatedSemanticSearch.getConfigurations() != null) {
                    for (SemanticConfiguration config :
                        updatedSemanticSearch.getConfigurations()) {
                        System.out.println("Configuration name: " + config.getName());
    
                        SemanticPrioritizedFields fields =
                            config.getPrioritizedFields();
                        if (fields.getTitleField() != null) {
                            System.out.println("Title field: " +
                                fields.getTitleField().getFieldName());
                        }
                        if (fields.getKeywordsFields() != null) {
                            List<String> keywords = fields.getKeywordsFields().stream()
                                .map(SemanticField::getFieldName)
                                .toList();
                            System.out.println("Keywords fields: " +
                                String.join(", ", keywords));
                        }
                        if (fields.getContentFields() != null) {
                            List<String> content = fields.getContentFields().stream()
                                .map(SemanticField::getFieldName)
                                .toList();
                            System.out.println("Content fields: " +
                                String.join(", ", content));
                        }
                        System.out.println("-".repeat(40));
                    }
                } else {
                    System.out.println("No semantic configurations found.");
                }
    
                System.out.println("Semantic configuration updated successfully.");
    
                System.exit(0);
            } catch (Exception e) {
                System.err.println("Error updating semantic configuration: " +
                    e.getMessage());
            }
        }
    }
    ```

1. Run the code.

    ```bash
    mvn compile exec:java -Dexec.mainClass="com.azure.search.quickstart.UpdateIndexSettings"
    ```

1. Output is the semantic configuration you just added, `Semantic configuration updated successfully.`.

## Run semantic queries

Once the `hotels-sample-index` index has a semantic configuration, you can run queries that include semantic parameters.

1. Create a file in `src/main/java/com/azure/search/quickstart` called `SemanticQuery.java` to create a semantic query of the index.

    ```java
    package com.azure.search.quickstart;
    
    import com.azure.search.documents.SearchClientBuilder;
    import com.azure.search.documents.SearchDocument;
    import com.azure.search.documents.models.QueryType;
    import com.azure.search.documents.models.SearchOptions;
    import com.azure.search.documents.models.SearchResult;
    import com.azure.search.documents.models.SemanticSearchOptions;
    import com.azure.search.documents.util.SearchPagedIterable;
    
    public class SemanticQuery {
        public static void main(String[] args) {
            var searchClient = new SearchClientBuilder()
                .endpoint(SearchConfig.SEARCH_ENDPOINT)
                .indexName(SearchConfig.INDEX_NAME)
                .credential(SearchConfig.CREDENTIAL)
                .buildClient();
    
            var searchOptions = new SearchOptions()
                .setQueryType(QueryType.SEMANTIC)
                .setSemanticSearchOptions(new SemanticSearchOptions()
                    .setSemanticConfigurationName(SearchConfig.SEMANTIC_CONFIG_NAME))
                .setSelect("HotelId", "HotelName", "Description");
    
            SearchPagedIterable results = searchClient.search(
                "walking distance to live music", searchOptions, null);
    
            int rowNumber = 1;
            for (SearchResult result : results) {
                var document = result.getDocument(SearchDocument.class);
                double rerankerScore = result.getSemanticSearch().getRerankerScore();
    
                System.out.printf("Search result #%d:%n", rowNumber++);
                System.out.printf("  Re-ranker Score: %.2f%n", rerankerScore);
                System.out.printf("  HotelId: %s%n", document.get("HotelId"));
                System.out.printf("  HotelName: %s%n", document.get("HotelName"));
                System.out.printf("  Description: %s%n%n",
                    document.get("Description") != null ?
                        document.get("Description") : "N/A");
            }
    
            System.exit(0);
        }
    }
    ```

1. Run the code.

    ```bash
    mvn compile exec:java -Dexec.mainClass="com.azure.search.quickstart.SemanticQuery"
    ```

1. Output should consist of 13 documents, ordered by the reranker score.

### Return captions

Optionally, you can add captions to extract portions of the text and apply hit highlighting to the important terms and phrases.

1. Create a file in `src/main/java/com/azure/search/quickstart` called `SemanticQueryWithCaptions.java`.

    ```java
    package com.azure.search.quickstart;
    
    import com.azure.search.documents.SearchClientBuilder;
    import com.azure.search.documents.SearchDocument;
    import com.azure.search.documents.models.QueryCaption;
    import com.azure.search.documents.models.QueryCaptionResult;
    import com.azure.search.documents.models.QueryCaptionType;
    import com.azure.search.documents.models.QueryType;
    import com.azure.search.documents.models.SearchOptions;
    import com.azure.search.documents.models.SearchResult;
    import com.azure.search.documents.models.SemanticSearchOptions;
    import com.azure.search.documents.util.SearchPagedIterable;

    import java.util.List;
    
    public class SemanticQueryWithCaptions {
        public static void main(String[] args) {
            var searchClient = new SearchClientBuilder()
                .endpoint(SearchConfig.SEARCH_ENDPOINT)
                .indexName(SearchConfig.INDEX_NAME)
                .credential(SearchConfig.CREDENTIAL)
                .buildClient();
    
            System.out.println("Using semantic configuration: " +
                SearchConfig.SEMANTIC_CONFIG_NAME);
            System.out.println("Search query: walking distance to live music");
    
            var searchOptions = new SearchOptions()
                .setQueryType(QueryType.SEMANTIC)
                .setSemanticSearchOptions(new SemanticSearchOptions()
                    .setSemanticConfigurationName(SearchConfig.SEMANTIC_CONFIG_NAME)
                    .setQueryCaption(new QueryCaption(QueryCaptionType.EXTRACTIVE)
                        .setHighlightEnabled(true)))
                .setSelect("HotelId", "HotelName", "Description");
    
            SearchPagedIterable results = searchClient.search(
                "walking distance to live music", searchOptions, null);
    
            System.out.printf("Found results with semantic search%n%n");
            int rowNumber = 1;
    
            for (SearchResult result : results) {
                var document = result.getDocument(SearchDocument.class);
                double rerankerScore = result.getSemanticSearch().getRerankerScore();
    
                System.out.printf("Search result #%d:%n", rowNumber++);
                System.out.printf("  Re-ranker Score: %.2f%n", rerankerScore);
                System.out.printf("  HotelName: %s%n", document.get("HotelName"));
                System.out.printf("  Description: %s%n%n",
                    document.get("Description") != null ?
                        document.get("Description") : "N/A");
    
                // Handle captions
                List<QueryCaptionResult> captions =
                    result.getSemanticSearch().getQueryCaptions();
                if (captions != null && !captions.isEmpty()) {
                    QueryCaptionResult caption = captions.get(0);
    
                    if (caption.getHighlights() != null &&
                        !caption.getHighlights().trim().isEmpty()) {
                        System.out.printf("  Caption with highlights: %s%n",
                            caption.getHighlights());
                    } else if (caption.getText() != null &&
                        !caption.getText().trim().isEmpty()) {
                        System.out.printf("  Caption text: %s%n",
                            caption.getText());
                    } else {
                        System.out.println(
                            "  Caption exists but has no text or highlights content");
                    }
                } else {
                    System.out.println("  No captions found for this result");
                }
                System.out.println("-".repeat(60));
            }
    
            System.exit(0);
        }
    }
    ```

1. Run the code.

    ```bash
    mvn compile exec:java -Dexec.mainClass="com.azure.search.quickstart.SemanticQueryWithCaptions"
    ```

1. Output should include a new caption element alongside search field. Captions are the most relevant passages in a result. If your index includes larger chunks of text, a caption is helpful for extracting the most interesting sentences.

    ```console
    Search result #1:
      Re-ranker Score: 2.613231658935547
      HotelName: Uptown Chic Hotel
      Description: Chic hotel near the city. High-rise hotel in downtown, within walking distance to theaters, art galleries, restaurants and shops. Visit Seattle Art Museum by day, and then head over to Benaroya Hall to catch the evening's concert performance.

      Caption with highlights: Chic hotel near the city. High-rise hotel in downtown, within walking distance to<em> theaters, </em>art galleries, restaurants and shops. Visit<em> Seattle Art Museum </em>by day, and then head over to<em> Benaroya Hall </em>to catch the evening's concert performance.
    ```

### Return semantic answers

In this final query, return semantic answers.

Semantic ranker can produce an answer to a query string that has the characteristics of a question. The generated answer is extracted verbatim from your content so it won't include composed content like what you might expect from a chat completion model.

To produce a semantic answer, the question and answer must be closely aligned, and the model must find content that clearly answers the question. If potential answers fail to meet a confidence threshold, the model doesn't return an answer. For demonstration purposes, the question in this example is designed to get a response so that you can see the syntax.

1. Create a file in `src/main/java/com/azure/search/quickstart` called `SemanticAnswer.java`.

    ```java
    package com.azure.search.quickstart;
    
    import com.azure.search.documents.SearchClientBuilder;
    import com.azure.search.documents.SearchDocument;
    import com.azure.search.documents.models.QueryAnswer;
    import com.azure.search.documents.models.QueryAnswerResult;
    import com.azure.search.documents.models.QueryAnswerType;
    import com.azure.search.documents.models.QueryCaption;
    import com.azure.search.documents.models.QueryCaptionResult;
    import com.azure.search.documents.models.QueryCaptionType;
    import com.azure.search.documents.models.QueryType;
    import com.azure.search.documents.models.SearchOptions;
    import com.azure.search.documents.models.SearchResult;
    import com.azure.search.documents.models.SemanticSearchOptions;
    import com.azure.search.documents.util.SearchPagedIterable;
    
    import java.util.List;
    
    public class SemanticAnswer {
        public static void main(String[] args) {
            var searchClient = new SearchClientBuilder()
                .endpoint(SearchConfig.SEARCH_ENDPOINT)
                .indexName(SearchConfig.INDEX_NAME)
                .credential(SearchConfig.CREDENTIAL)
                .buildClient();
    
            var searchOptions = new SearchOptions()
                .setQueryType(QueryType.SEMANTIC)
                .setSemanticSearchOptions(new SemanticSearchOptions()
                    .setSemanticConfigurationName(SearchConfig.SEMANTIC_CONFIG_NAME)
                    .setQueryCaption(new QueryCaption(QueryCaptionType.EXTRACTIVE))
                    .setQueryAnswer(new QueryAnswer(QueryAnswerType.EXTRACTIVE)))
                .setSelect("HotelName", "Description", "Category");
    
            SearchPagedIterable results = searchClient.search(
                "What's a good hotel for people who like to read",
                searchOptions, null);
    
            System.out.println("Answers:\n");
    
            // Extract semantic answers
            List<QueryAnswerResult> semanticAnswers =
                results.getSemanticResults().getQueryAnswers();
            int answerNumber = 1;
    
            if (semanticAnswers != null) {
                for (QueryAnswerResult answer : semanticAnswers) {
                    System.out.printf("Semantic answer result #%d:%n",
                        answerNumber++);
    
                    if (answer.getHighlights() != null &&
                        !answer.getHighlights().trim().isEmpty()) {
                        System.out.printf("Semantic Answer: %s%n",
                            answer.getHighlights());
                    } else {
                        System.out.printf("Semantic Answer: %s%n", answer.getText());
                    }
                    System.out.printf("Semantic Answer Score: %.2f%n%n",
                        answer.getScore());
                }
            }
    
            System.out.println("Search Results:\n");
            int rowNumber = 1;
    
            // Iterate through search results
            for (SearchResult result : results) {
                var document = result.getDocument(SearchDocument.class);
                double rerankerScore = result.getSemanticSearch().getRerankerScore();
    
                System.out.printf("Search result #%d:%n", rowNumber++);
                System.out.printf("Re-ranker Score: %.2f%n", rerankerScore);
                System.out.printf("Hotel: %s%n", document.get("HotelName"));
                System.out.printf("Description: %s%n",
                    document.get("Description") != null ?
                        document.get("Description") : "N/A");
    
                List<QueryCaptionResult> captions =
                    result.getSemanticSearch().getQueryCaptions();
                if (captions != null && !captions.isEmpty()) {
                    QueryCaptionResult caption = captions.get(0);
                    if (caption.getHighlights() != null &&
                        !caption.getHighlights().trim().isEmpty()) {
                        System.out.printf("Caption: %s%n%n",
                            caption.getHighlights());
                    } else {
                        System.out.printf("Caption: %s%n%n", caption.getText());
                    }
                } else {
                    System.out.println();
                }
            }
    
            System.exit(0);
        }
    }
    ```

1. Run the code.

    ```bash
    mvn compile exec:java -Dexec.mainClass="com.azure.search.quickstart.SemanticAnswer"
    ```

1. Output should look similar to the following example, where the best answer to question is pulled from one of the results.

    Recall that answers are *verbatim content* pulled from your index and might be missing phrases that a user would expect to see. To get *composed answers* as generated by a chat completion model, considering using a [RAG pattern](../../retrieval-augmented-generation-overview.md) or [agentic retrieval](../../search-agentic-retrieval-concept.md).

    ```console
    Semantic answer result #1:
    Semantic Answer: Nature is Home on the beach. Explore the shore by day, and then come home to our shared living space to relax around a stone fireplace, sip something warm, and explore the<em> library </em>by night. Save up to 30 percent. Valid Now through the end of the year. Restrictions and blackouts may apply.
    Semantic Answer Score: 0.9829999804496765
    ```
