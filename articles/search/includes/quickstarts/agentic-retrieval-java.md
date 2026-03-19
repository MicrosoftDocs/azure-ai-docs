---
ms.service: azure-ai-search
ms.topic: include
ms.date: 02/23/2026
ms.custom: dev-focus
ai-usage: ai-assisted
---

[!INCLUDE [Feature preview](../previews/preview-generic.md)]

In this quickstart, you use [agentic retrieval](../../agentic-retrieval-overview.md) to create a conversational search experience powered by documents indexed in Azure AI Search and a large language model (LLM) from Azure OpenAI in Foundry Models.

A *knowledge base* orchestrates agentic retrieval by decomposing complex queries into subqueries, running the subqueries against one or more *knowledge sources*, and returning results with metadata. By default, the knowledge base outputs raw content from your sources, but this quickstart uses the answer synthesis output mode for natural-language answer generation.

Although you can use your own data, this quickstart uses [sample JSON documents](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/nasa-e-book/earth-at-night-json) from NASA's Earth at Night e-book.

> [!TIP]
> Want to get started right away? Download the [source code](https://github.com/Azure-Samples/azure-search-java-samples/tree/main/quickstart-agentic-retrieval) on GitHub.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](../../search-create-service-portal.md) in any [region that provides agentic retrieval](../../search-region-support.md). This quickstart requires the Basic tier or higher for managed identity support.

+ A [Microsoft Foundry project](/azure/ai-foundry/how-to/create-projects) and resource. When you create a project, the resource is automatically created.

+ An embedding model [deployed to your project](/azure/ai-foundry/how-to/deploy-models-openai) for text-to-vector conversion. You can use any `text-embedding` model, such as `text-embedding-3-large`.

+ An LLM [deployed to your project](/azure/ai-foundry/how-to/deploy-models-openai) for query planning and answer generation. You can use any [supported LLM](../../agentic-retrieval-how-to-create-knowledge-base.md#supported-models), such as `gpt-5-mini`.

+ [Java 11](https://www.oracle.com/java/technologies/downloads/) or later and [Maven](https://maven.apache.org/download.cgi).

+ [Git](https://git-scm.com/downloads) to clone the sample repository.

+ The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

[!INCLUDE [agentic retrieval setup](agentic-retrieval-setup.md)]

## Set up the environment

1. Use Git to clone the sample repository.

    ```bash
    git clone https://github.com/Azure-Samples/azure-search-java-samples
    ```

1. Navigate to the quickstart folder.

    ```bash
    cd azure-search-java-samples/quickstart-agentic-retrieval
    ```

1. In `sample.env`, replace the placeholder values for `SEARCH_ENDPOINT` and `AOAI_ENDPOINT` with the URLs you obtained in [Get endpoints](#get-endpoints).

1. Rename `sample.env` to `.env`.

    ```bash
    mv sample.env .env
    ```

1. Install the dependencies, including the [Azure AI Search client library](/java/api/overview/azure/search) and [Azure Identity client library](https://mvnrepository.com/artifact/com.azure/azure-identity) for Java.

    ```bash
    mvn clean dependency:copy-dependencies
    ```

1. For keyless authentication with Microsoft Entra ID, sign in to your Azure account. If you have multiple subscriptions, select the one that contains your Azure AI Search and Microsoft Foundry resources.

    ```bash
    az login
    ```

## Run the code

Build and run the application to create an index, upload documents, configure a knowledge source and knowledge base, and run agentic retrieval queries.

### [Windows](#tab/windows)

```bash
javac AgenticRetrievalQuickstart.java -cp ".;target\dependency\*"
java -cp ".;target\dependency\*" AgenticRetrievalQuickstart
```

### [macOS](#tab/macos)

```bash
javac AgenticRetrievalQuickstart.java -cp ".:target/dependency/*"
java -cp ".:target/dependency/*" AgenticRetrievalQuickstart
```

### [Linux](#tab/linux)

```bash
javac AgenticRetrievalQuickstart.java -cp ".:target/dependency/*"
java -cp ".:target/dependency/*" AgenticRetrievalQuickstart
```

---

### Output

The output of the application should be similar to the following:

```
Index 'earth-at-night' created or updated successfully.
Documents uploaded to index 'earth-at-night' successfully.
Knowledge source 'earth-knowledge-source' created or updated successfully.
Knowledge base 'earth-knowledge-base' created or updated successfully.
Running the query...Why do suburban belts display larger December brightening than urban cores even though absolute light levels are higher downtown? Why is the Phoenix nighttime street grid is so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?
Response:
December percent brightening is larger in suburban belts because many houses add seasonal residential/holiday lighting on yards and roofs, so a relatively dark suburban baseline can increase by 20-50% when those lights turn on, while dense urban cores already have high continuous lighting so the same added lights make a smaller percentage change [ref_id:2][ref_id:5][ref_id:8]. Phoenix's street grid appears sharply from space because the metropolitan layout is a regular, continuous north-south/east-west street and block grid with a major diagonal artery (Grand Avenue) and concentrated, continuous arterial and commercial lighting along intersections and corridors [ref_id:3][ref_id:0][ref_id:1]. ...
Activity:
Activity Type: KnowledgeBaseModelQueryPlanningActivityRecord
{
  "id" : 0,
  "elapsedMs" : 5229,
  "type" : "modelQueryPlanning",
  "inputTokens" : 1489,
  "outputTokens" : 383
}
Activity Type: KnowledgeBaseSearchIndexActivityRecord
{
  "id" : 1,
  "elapsedMs" : 2670,
  "knowledgeSourceName" : "earth-knowledge-source",
  "queryTime" : "2026-02-24T15:28:36.776Z",
  "count" : 3,
  "type" : "searchIndex",
  "searchIndexArguments" : {
    "search" : "December brightening suburban belts vs urban cores light pollution causes seasonal variation reasons \"December brightening\"",
    "sourceDataFields" : [ {
      "name" : "page_chunk"
    }, {
      "name" : "id"
    }, {
      "name" : "page_number"
    } ],
    "searchFields" : [ ],
    "semanticConfigurationName" : "semantic_config"
  }
}
... // Trimmed for brevity
References:
Reference Type: KnowledgeBaseSearchIndexReference
{
  "id" : "0",
  "activitySource" : 2,
  "rerankerScore" : 2.7486389,
  "type" : "searchIndex",
  "docKey" : "earth_at_night_508_page_105_verbalized"
}
... // Trimmed for brevity
Continue the conversation with this query: How do I find lava at night?
Response:
... // Trimmed for brevity
Activity:
... // Trimmed for brevity
References:
... // Trimmed for brevity
Knowledge base 'earth-knowledge-base' deleted successfully.
Knowledge source 'earth-knowledge-source' deleted successfully.
Index 'earth-at-night' deleted successfully.
```

## Understand the code

[!INCLUDE [understand code note](../understand-code-note.md)]

Now that you've run the code, let's break down the key steps:

1. [Create a search index](#create-a-search-index)
1. [Upload documents to the index](#upload-documents-to-the-index)
1. [Create a knowledge source](#create-a-knowledge-source)
1. [Create a knowledge base](#create-a-knowledge-base)
1. [Set up messages](#set-up-messages)
1. [Run the retrieval pipeline](#run-the-retrieval-pipeline)
1. [Continue the conversation](#continue-the-conversation)

### Create a search index

In Azure AI Search, an index is a structured collection of data. The following code defines an index named `earth-at-night`.

The index schema contains fields for document identification and page content, embeddings, and numbers. The schema also includes configurations for semantic ranking and vector search, which uses your `text-embedding-3-large` deployment to vectorize text and match documents based on semantic or conceptual similarity.

```java
List<SearchField> fields = Arrays.asList(
    new SearchField("id", SearchFieldDataType.STRING)
        .setKey(true)
        .setFilterable(true)
        .setSortable(true)
        .setFacetable(true),
    new SearchField("page_chunk", SearchFieldDataType.STRING)
        .setFilterable(false)
        .setSortable(false)
        .setFacetable(false),
    new SearchField("page_embedding_text_3_large",
            SearchFieldDataType.collection(
                SearchFieldDataType.SINGLE))
        .setVectorSearchDimensions(3072)
        .setVectorSearchProfileName("hnsw_text_3_large"),
    new SearchField("page_number", SearchFieldDataType.INT32)
        .setFilterable(true)
        .setSortable(true)
        .setFacetable(true)
);

AzureOpenAIVectorizer vectorizer = new AzureOpenAIVectorizer(
        "azure_openai_text_3_large")
    .setParameters(new AzureOpenAIVectorizerParameters()
        .setResourceUrl(aoaiEndpoint)
        .setDeploymentName(aoaiEmbeddingDeployment)
        .setModelName(
            AzureOpenAIModelName.fromString(
                aoaiEmbeddingModel)));

VectorSearch vectorSearch = new VectorSearch()
    .setProfiles(Arrays.asList(
        new VectorSearchProfile("hnsw_text_3_large", "alg")
            .setVectorizerName("azure_openai_text_3_large")
    ))
    .setAlgorithms(Arrays.asList(
        new HnswAlgorithmConfiguration("alg")
    ))
    .setVectorizers(Arrays.asList(vectorizer));

SemanticSearch semanticSearch = new SemanticSearch()
    .setDefaultConfigurationName("semantic_config")
    .setConfigurations(Arrays.asList(
        new SemanticConfiguration("semantic_config",
            new SemanticPrioritizedFields()
                .setContentFields(Arrays.asList(
                    new SemanticField("page_chunk")
                ))
        )
    ));

SearchIndex index = new SearchIndex(indexName)
    .setFields(fields)
    .setVectorSearch(vectorSearch)
    .setSemanticSearch(semanticSearch);

indexClient.createOrUpdateIndex(index);
```

**Reference:** [SearchField](/java/api/com.azure.search.documents.indexes.models.searchfield), [VectorSearch](/java/api/com.azure.search.documents.indexes.models.vectorsearch), [SemanticSearch](/java/api/com.azure.search.documents.indexes.models.semanticsearch), [SearchIndex](/java/api/com.azure.search.documents.indexes.models.searchindex), [SearchIndexClient](/java/api/com.azure.search.documents.indexes.searchindexclient)

### Upload documents to the index

Currently, the `earth-at-night` index is empty. The following code populates the index with JSON documents from [NASA's Earth at Night e-book](https://raw.githubusercontent.com/Azure-Samples/azure-search-sample-data/refs/heads/main/nasa-e-book/earth-at-night-json/documents.json). As required by Azure AI Search, each document conforms to the fields and data types defined in the index schema.

```java
String url = "https://raw.githubusercontent.com/Azure-Samples/"
    + "azure-search-sample-data/refs/heads/main/nasa-e-book/"
    + "earth-at-night-json/documents.json";

java.net.http.HttpClient httpClient =
    java.net.http.HttpClient.newHttpClient();
java.net.http.HttpRequest httpRequest =
    java.net.http.HttpRequest.newBuilder()
        .uri(URI.create(url))
        .build();

java.net.http.HttpResponse<String> response =
    httpClient.send(httpRequest,
        java.net.http.HttpResponse.BodyHandlers.ofString());

if (response.statusCode() != 200) {
    throw new IOException(
        "Failed to fetch documents: " + response.statusCode());
}

ObjectMapper mapper = new ObjectMapper();
JsonNode jsonArray = mapper.readTree(response.body());

List<SearchDocument> documents = new ArrayList<>();
for (int i = 0; i < jsonArray.size(); i++) {
    JsonNode doc = jsonArray.get(i);
    SearchDocument searchDoc = new SearchDocument();

    searchDoc.put("id", doc.has("id")
        ? doc.get("id").asText() : String.valueOf(i + 1));
    searchDoc.put("page_chunk", doc.has("page_chunk")
        ? doc.get("page_chunk").asText() : "");

    if (doc.has("page_embedding_text_3_large")
            && doc.get("page_embedding_text_3_large")
                .isArray()) {
        List<Double> embeddings = new ArrayList<>();
        for (JsonNode embedding
                : doc.get("page_embedding_text_3_large")) {
            embeddings.add(embedding.asDouble());
        }
        searchDoc.put(
            "page_embedding_text_3_large", embeddings);
    } else {
        List<Double> fallback = new ArrayList<>();
        for (int j = 0; j < 3072; j++) {
            fallback.add(0.1);
        }
        searchDoc.put(
            "page_embedding_text_3_large", fallback);
    }

    searchDoc.put("page_number",
        doc.has("page_number")
            ? doc.get("page_number").asInt() : i + 1);

    documents.add(searchDoc);
}

SearchClient searchClient = new SearchClientBuilder()
    .endpoint(searchEndpoint)
    .indexName(indexName)
    .credential(credential)
    .buildClient();

searchClient.uploadDocuments(documents);
```


**Reference:** [SearchClient](/java/api/com.azure.search.documents.searchclient), [SearchDocument](/java/api/com.azure.search.documents.searchdocument)

### Create a knowledge source

A knowledge source is a reusable reference to source data. The following code defines a knowledge source named `earth-knowledge-source` that targets the `earth-at-night` index.

`sourceDataFields` specifies which index fields are included in citation references. This example includes only human-readable fields to avoid lengthy, uninterpretable embeddings in responses.

```java
SearchIndexKnowledgeSource indexKnowledgeSource =
    new SearchIndexKnowledgeSource(
        knowledgeSourceName,
        new SearchIndexKnowledgeSourceParameters(indexName)
            .setSourceDataFields(Arrays.asList(
                new SearchIndexFieldReference("id"),
                new SearchIndexFieldReference("page_chunk"),
                new SearchIndexFieldReference("page_number")
            ))
    );

indexClient.createOrUpdateKnowledgeSource(indexKnowledgeSource);
```

**Reference:** [SearchIndexKnowledgeSource](/java/api/com.azure.search.documents.indexes.models.searchindexknowledgesource)

### Create a knowledge base

To target `earth-knowledge-source` and your `gpt-5-mini` deployment at query time, you need a knowledge base. The following code defines a knowledge base named `earth-knowledge-base`.

`OutputMode` is set to `ANSWER_SYNTHESIS`, enabling natural-language answers that cite the retrieved documents and follow the provided `AnswerInstructions`.

```java
AzureOpenAIVectorizerParameters openAiParameters =
    new AzureOpenAIVectorizerParameters()
        .setResourceUrl(aoaiEndpoint)
        .setDeploymentName(aoaiGptDeployment)
        .setModelName(
            AzureOpenAIModelName.fromString(aoaiGptModel));

KnowledgeBaseAzureOpenAIModel model =
    new KnowledgeBaseAzureOpenAIModel(openAiParameters);

KnowledgeBase knowledgeBase = new KnowledgeBase(
        knowledgeBaseName,
        Arrays.asList(
            new KnowledgeSourceReference(knowledgeSourceName))
    )
    .setRetrievalReasoningEffort(
        new KnowledgeRetrievalLowReasoningEffort())
    .setOutputMode(
        KnowledgeRetrievalOutputMode.ANSWER_SYNTHESIS)
    .setAnswerInstructions(
        "Provide a two sentence concise and informative answer "
        + "based on the retrieved documents.")
    .setModels(Arrays.asList(model));

indexClient.createOrUpdateKnowledgeBase(knowledgeBase);
```

**Reference:** [KnowledgeBaseAzureOpenAIModel](/java/api/com.azure.search.documents.indexes.models.knowledgebaseazureopenaimodel), [KnowledgeBase](/java/api/com.azure.search.documents.indexes.models.knowledgebase)

### Set up messages

Messages are the input for the retrieval route and contain the conversation history. Each message includes a role that indicates its origin, such as `system` or `user`, and content in natural language. The LLM you use determines which roles are valid.

The following code creates a system message, which instructs `earth-knowledge-base` to answer questions about the Earth at night and respond with "I don't know" when answers are unavailable.

```java
String instructions =
    "A Q&A agent that can answer questions about the "
    + "Earth at night.\n"
    + "If you don't have the answer, respond with "
    + "\"I don't know\".";

List<Map<String, String>> messages = new ArrayList<>();
Map<String, String> systemMessage = new HashMap<>();
systemMessage.put("role", "system");
systemMessage.put("content", instructions);
messages.add(systemMessage);
```

### Run the retrieval pipeline

You're ready to run agentic retrieval. The following code sends a two-part user query to `earth-knowledge-base`, which:

1. Analyzes the entire conversation to infer the user's information need.
1. Decomposes the compound query into focused subqueries.
1. Runs the subqueries concurrently against your knowledge source.
1. Uses semantic ranker to rerank and filter the results.
1. Synthesizes the top results into a natural-language answer.

```java
SearchKnowledgeBaseClient baseClient =
    new SearchKnowledgeBaseClientBuilder()
        .endpoint(searchEndpoint)
        .knowledgeBaseName(knowledgeBaseName)
        .credential(
            new DefaultAzureCredentialBuilder().build())
        .buildClient();

String query = "Why do suburban belts display larger "
    + "December brightening than urban cores even "
    + "though absolute light levels are higher "
    + "downtown? Why is the Phoenix nighttime street "
    + "grid is so sharply visible from space, whereas "
    + "large stretches of the interstate between "
    + "midwestern cities remain comparatively dim?";

messages.add(Map.of("role", "user", "content", query));

KnowledgeBaseRetrievalResponse retrievalResult =
    retrieve(baseClient, messages);

String responseText =
    ((KnowledgeBaseMessageTextContent) retrievalResult
        .getResponse().get(0).getContent().get(0))
        .getText();

messages.add(
    Map.of("role", "assistant", "content", responseText));
```

The `retrieve` helper method builds `KnowledgeBaseMessage` objects from the conversation history and sends the retrieval request:

```java
private static KnowledgeBaseRetrievalResponse retrieve(
        SearchKnowledgeBaseClient client,
        List<Map<String, String>> messages) {
    List<KnowledgeBaseMessage> kbMessages = new ArrayList<>();
    for (Map<String, String> msg : messages) {
        if (!"system".equals(msg.get("role"))) {
            kbMessages.add(
                new KnowledgeBaseMessage(Arrays.asList(
                    new KnowledgeBaseMessageTextContent(
                        msg.get("content"))
                )).setRole(msg.get("role"))
            );
        }
    }

    KnowledgeBaseRetrievalRequest request =
        new KnowledgeBaseRetrievalRequest();
    request.setMessages(kbMessages);
    request.setRetrievalReasoningEffort(
        new KnowledgeRetrievalLowReasoningEffort());

    return client.retrieve(request, null);
}
```

**Reference:** [SearchKnowledgeBaseClient](/java/api/com.azure.search.documents.knowledgebases.searchknowledgebaseclient?view=azure-java-preview&preserve-view=true), [KnowledgeBaseRetrievalRequest](/java/api/com.azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest?view=azure-java-preview&preserve-view=true)

#### Review the response, activity, and references

The following code displays the response, activity, and references from the retrieval pipeline, where:

+ `Response` provides a synthesized, LLM-generated answer to the query that cites the retrieved documents. When answer synthesis isn't enabled, this section contains content extracted directly from the documents.

+ `Activity` tracks the steps that were taken during the retrieval process, including the subqueries generated by your `gpt-5-mini` deployment and the tokens used for semantic ranking, query planning, and answer synthesis.

+ `References` lists the documents that contributed to the response, each one identified by their `docKey`.

```java
System.out.println("Response:");
System.out.println(responseText);

System.out.println("Activity:");
for (KnowledgeBaseActivityRecord activity
        : retrievalResult.getActivity()) {
    System.out.println("Activity Type: "
        + activity.getClass().getSimpleName());
    System.out.println(toJsonString(activity));
}

System.out.println("References:");
for (KnowledgeBaseReference reference
        : retrievalResult.getReferences()) {
    System.out.println("Reference Type: "
        + reference.getClass().getSimpleName());
    System.out.println(toJsonString(reference));
}
```

### Continue the conversation

The following code continues the conversation with `earth-knowledge-base`. After you send this user query, the knowledge base fetches relevant content from `earth-knowledge-source` and appends the response to the messages list.

```java
String nextQuery = "How do I find lava at night?";
messages.add(
    Map.of("role", "user", "content", nextQuery));

retrievalResult = retrieve(baseClient, messages);
```

#### Review the new response, activity, and references

The following code extracts the response text and calls `printResult` to display the new response, activity, and references.

```java
responseText =
    ((KnowledgeBaseMessageTextContent) retrievalResult
        .getResponse().get(0).getContent().get(0))
        .getText();
messages.add(
    Map.of("role", "assistant", "content", responseText));

printResult(responseText, retrievalResult);
```

## Clean up resources

[!INCLUDE [clean up resources (paid)](../resource-cleanup-paid.md)]

Otherwise, the following code from `AgenticRetrievalQuickstart.java` deleted the objects you created in this quickstart.

### Delete the knowledge base

```java
indexClient.deleteKnowledgeBase(knowledgeBaseName);
System.out.println("Knowledge base '" + knowledgeBaseName
    + "' deleted successfully.");
```

### Delete the knowledge source

```java
indexClient.deleteKnowledgeSource(knowledgeSourceName);
System.out.println("Knowledge source '" + knowledgeSourceName
    + "' deleted successfully.");
```

### Delete the search index

```java
indexClient.deleteIndex(indexName);
System.out.println("Index '" + indexName
    + "' deleted successfully.");
```
