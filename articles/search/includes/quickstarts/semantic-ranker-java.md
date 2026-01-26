---
author: KarlErickson
ms.author: karler
ms.service: azure-ai-search
ms.custom: devx-track-java
ms.topic: include
ms.date: 12/15/2025
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

   :::code language="xml" source="~/azure-search-java-samples/quickstart-semantic-ranking/pom.xml" :::

1. Compile the project to resolve the dependencies.

    ```bash
    mvn compile
    ```

1. Create the source directory structure.

   ```bash
   mkdir -p src/main/java/com/azure/search/quickstart
   mkdir -p src/main/resources
   ```

1. Create an `application.properties` file in the `src/main/resources` directory and provide your search service endpoint. You can get the endpoint from the Azure portal on the search service **Overview** page.

    ```properties
    azure.search.endpoint=YOUR-SEARCH-SERVICE-ENDPOINT
    azure.search.index.name=hotels-sample-index
    semantic.configuration.name=semantic-config
    ```

### Sign in to Azure

If you signed in to the [Azure portal](https://portal.azure.com), you're signed into Azure. If you aren't sure, use the Azure CLI to log in: `az login`. If you have multiple tenants and subscriptions, see [Quickstart: Connect without keys](../../search-get-started-rbac.md) for help on how to connect.

## Create a common configuration class

Create a `SearchConfig.java` file in the `src/main/java/com/azure/search/quickstart` directory to read the properties file and hold the configuration values and authentication credential.

:::code language="java" source="~/azure-search-java-samples/quickstart-semantic-ranking/src/main/java/com/azure/search/quickstart/SearchConfig.java" :::

## Get the index schema

In this section, you get settings for the existing `hotels-sample-index` index on your search service.

1. Create a `GetIndexSettings.java` file in the `src/main/java/com/azure/search/quickstart` directory.

   :::code language="java" source="~/azure-search-java-samples/quickstart-semantic-ranking/src/main/java/com/azure/search/quickstart/GetIndexSettings.java" :::

1. Compile and run the code.

    ```bash
    mvn compile exec:java -Dexec.mainClass="com.azure.search.quickstart.GetIndexSettings"
    ```

1. Output is the name of the index, list of fields, and a statement indicating whether a semantic configuration exists. For the purposes of this quickstart, the message should say `No semantic configuration exists for this index`.

## Update the index with a semantic configuration

1. Create an `UpdateIndexSettings.java` file in the `src/main/java/com/azure/search/quickstart` directory to add a semantic configuration to the existing `hotels-sample-index` index on your search service.

   :::code language="java" source="~/azure-search-java-samples/quickstart-semantic-ranking/src/main/java/com/azure/search/quickstart/UpdateIndexSettings.java" :::

1. Compile and run the code.

    ```bash
    mvn compile exec:java -Dexec.mainClass="com.azure.search.quickstart.UpdateIndexSettings"
    ```

1. Output is the semantic configuration you just added, `Semantic configuration updated successfully.`.

## Run semantic queries

After the `hotels-sample-index` index has a semantic configuration, you can run queries that include semantic parameters.

1. Create a `SemanticQuery.java` file in the `src/main/java/com/azure/search/quickstart` directory to create a semantic query of the index.

   :::code language="java" source="~/azure-search-java-samples/quickstart-semantic-ranking/src/main/java/com/azure/search/quickstart/SemanticQuery.java" :::

1. Compile and run the code.

    ```bash
    mvn compile exec:java -Dexec.mainClass="com.azure.search.quickstart.SemanticQuery"
    ```

1. Output should consist of 13 documents, ordered by the reranker score.

### Return captions

Optionally, you can add captions to extract portions of the text and apply hit highlighting to the important terms and phrases.

1. Create a `SemanticQueryWithCaptions.java` file in the `src/main/java/com/azure/search/quickstart` directory.

   :::code language="java" source="~/azure-search-java-samples/quickstart-semantic-ranking/src/main/java/com/azure/search/quickstart/SemanticQueryWithCaptions.java" :::

1. Compile and run the code.

    ```bash
    mvn compile exec:java -Dexec.mainClass="com.azure.search.quickstart.SemanticQueryWithCaptions"
    ```

1. Output should include a new caption element alongside search field. Captions are the most relevant passages in a result. If your index includes larger chunks of text, a caption is helpful for extracting the most interesting sentences.

    ```output
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

1. Create a `SemanticAnswer.java` file in the `src/main/java/com/azure/search/quickstart` directory.

   :::code language="java" source="~/azure-search-java-samples/quickstart-semantic-ranking/src/main/java/com/azure/search/quickstart/SemanticAnswer.java" :::

1. Compile and run the code.

    ```bash
    mvn compile exec:java -Dexec.mainClass="com.azure.search.quickstart.SemanticAnswer"
    ```

1. Output should look similar to the following example, where the best answer to question is pulled from one of the results.

    Recall that answers are *verbatim content* pulled from your index and might be missing phrases that a user would expect to see. To get *composed answers* as generated by a chat completion model, considering using a [RAG pattern](../../retrieval-augmented-generation-overview.md) or [agentic retrieval](../../agentic-retrieval-overview.md).

    ```output
    Semantic answer result #1:
    Semantic Answer: Nature is Home on the beach. Explore the shore by day, and then come home to our shared living space to relax around a stone fireplace, sip something warm, and explore the<em> library </em>by night. Save up to 30 percent. Valid Now through the end of the year. Restrictions and blackouts may apply.
    Semantic Answer Score: 0.9829999804496765
    ```
