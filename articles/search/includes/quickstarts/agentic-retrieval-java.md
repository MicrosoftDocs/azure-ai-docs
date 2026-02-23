---
manager: nitinme
author: haileytap
ms.author: haileytapia
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
> Source code for the Java version of this quickstart isn't available yet. You can copy the code directly from this article.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](../../search-create-service-portal.md) in any [region that provides agentic retrieval](../../search-region-support.md).

+ A [Microsoft Foundry project](/azure/ai-foundry/how-to/create-projects) and resource. When you create a project, the resource is automatically created.

+ An embedding model [deployed to your project](/azure/ai-foundry/how-to/deploy-models-openai) for text-to-vector conversion. This quickstart uses `text-embedding-3-large`, but you can use any `text-embedding` model.

+ An LLM [deployed to your project](/azure/ai-foundry/how-to/deploy-models-openai) for query planning and answer generation. This quickstart uses `gpt-5-mini`, but you can use any [supported LLM](../../agentic-retrieval-how-to-create-knowledge-base.md#supported-models).

+ [Java 11 or later](https://www.oracle.com/java/technologies/downloads/) and [Maven](https://maven.apache.org/download.cgi).

+ The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

[!INCLUDE [agentic retrieval setup](agentic-retrieval-setup.md)]

## Set up the environment

1. Create a folder named `quickstart-agentic-retrieval` to contain the application.

1. Open the folder in Visual Studio Code.

1. Create a file named `pom.xml`, and then paste the following XML into the file.

    ```xml
    <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>
        <groupId>azure.search.sample</groupId>
        <artifactId>azuresearchquickstart</artifactId>
        <version>1.0.0-SNAPSHOT</version>
        <build>
            <sourceDirectory>src</sourceDirectory>
            <plugins>
            <plugin>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.7.0</version>
                <configuration>
                <source>11</source>
                <target>11</target>
                </configuration>
            </plugin>
            </plugins>
        </build>
        <dependencies>
            <dependency>
                <groupId>junit</groupId>
                <artifactId>junit</artifactId>
                <version>4.11</version>
                <scope>test</scope>
            </dependency>
            <dependency>
                <groupId>com.azure</groupId>
                <artifactId>azure-search-documents</artifactId>
                <version>11.8.0-beta.7</version>
            </dependency>
            <dependency>
                <groupId>com.azure</groupId>
                <artifactId>azure-core</artifactId>
                <version>1.53.0</version>
            </dependency>
            <dependency>
                <groupId>com.azure</groupId>
                <artifactId>azure-identity</artifactId>
                <version>1.15.1</version>
            </dependency>
            <dependency>
                <groupId>com.fasterxml.jackson.core</groupId>
                <artifactId>jackson-databind</artifactId>
                <version>2.16.1</version>
            </dependency>
            <dependency>
                <groupId>io.github.cdimascio</groupId>
                <artifactId>dotenv-java</artifactId>
                <version>3.0.0</version>
            </dependency>
        </dependencies>
    </project>
    ```

1. Select **Terminal** > **New Terminal**, and then run the following command to install the dependencies, including the [Azure AI Search client library](/java/api/overview/azure/search) and [Azure Identity client library](https://mvnrepository.com/artifact/com.azure/azure-identity) for Java.

    ```console
    mvn clean dependency:copy-dependencies
    ```

1. For keyless authentication with Microsoft Entra ID, sign in to your Azure account. If you have multiple subscriptions, select the one that contains your Azure AI Search service and Microsoft Foundry project.

    ```console
    az login
    ```

## Run the code

1. Create a file named `.env` in the `quickstart-agentic-retrieval` folder, and then paste the following content. Replace the placeholder values with the endpoints you obtained in [Get endpoints](#get-endpoints).

    ```
    SEARCH_ENDPOINT=PUT-YOUR-SEARCH-SERVICE-URL-HERE
    AOAI_ENDPOINT=PUT-YOUR-AOAI-FOUNDRY-URL-HERE
    ```

1. Create a file named `AgenticRetrievalQuickstart.java`, and then paste the following code into the file.

    ```java
    import com.azure.core.credential.TokenCredential;
    import com.azure.identity.DefaultAzureCredentialBuilder;
    import com.azure.search.documents.SearchClient;
    import com.azure.search.documents.SearchClientBuilder;
    import com.azure.search.documents.SearchDocument;
    import com.azure.search.documents.indexes.SearchIndexClient;
    import com.azure.search.documents.indexes.SearchIndexClientBuilder;
    import com.azure.search.documents.indexes.models.*;
    import com.azure.search.documents.knowledgebases.KnowledgeBaseRetrievalClient;
    import com.azure.search.documents.knowledgebases.KnowledgeBaseRetrievalClientBuilder;
    import com.azure.search.documents.knowledgebases.models.*;
    import com.fasterxml.jackson.databind.JsonNode;
    import com.fasterxml.jackson.databind.ObjectMapper;
    import io.github.cdimascio.dotenv.Dotenv;
    
    import java.io.IOException;
    import java.net.URI;
    import java.util.*;
    
    public class AgenticRetrievalQuickstart {
        
        // Configuration - Update these values for your environment
        private static final String SEARCH_ENDPOINT;
        private static final String AZURE_OPENAI_ENDPOINT;
        private static final String AZURE_OPENAI_GPT_DEPLOYMENT = "gpt-5-mini";
        private static final String AZURE_OPENAI_GPT_MODEL = "gpt-5-mini";
        private static final String AZURE_OPENAI_EMBEDDING_DEPLOYMENT = "text-embedding-3-large";
        private static final String AZURE_OPENAI_EMBEDDING_MODEL = "text-embedding-3-large";
        private static final String INDEX_NAME = "earth-at-night";
        private static final String KNOWLEDGE_SOURCE_NAME = "earth-knowledge-source";
        private static final String KNOWLEDGE_BASE_NAME = "earth-knowledge-base";
        
        static {
            // Load environment variables from .env file
            Dotenv dotenv = Dotenv.configure().ignoreIfMissing().load();
            
            SEARCH_ENDPOINT = getEnvVar(dotenv, "SEARCH_ENDPOINT", 
                "https://contoso-agentic-search-service.search.windows.net");
            AZURE_OPENAI_ENDPOINT = getEnvVar(dotenv, "AOAI_ENDPOINT",
                "https://contoso-proj-agentic-foundry-res.openai.azure.com/");
        }
        
        private static String getEnvVar(Dotenv dotenv, String key, String defaultValue) {
            String value = dotenv.get(key);
            return (value != null && !value.isEmpty()) ? value : defaultValue;
        }
        
        public static void main(String[] args) {
            try {
                System.out.println("Starting Azure AI Search agentic retrieval quickstart...\n");
                
                // Initialize Azure credentials using managed identity (recommended)
                TokenCredential credential = new DefaultAzureCredentialBuilder().build();
                
                // Create search clients
                SearchIndexClient indexClient = new SearchIndexClientBuilder()
                    .endpoint(SEARCH_ENDPOINT)
                    .credential(credential)
                    .buildClient();
                    
                SearchClient searchClient = new SearchClientBuilder()
                    .endpoint(SEARCH_ENDPOINT)
                    .indexName(INDEX_NAME)
                    .credential(credential)
                    .buildClient();
                
                // Step 1: Create search index with vector and semantic capabilities
                createSearchIndex(indexClient);
                
                // Step 2: Upload documents
                uploadDocuments(searchClient);
                
                // Step 3: Create knowledge source
                createKnowledgeSource(indexClient);
                
                // Step 4: Create knowledge base
                createKnowledgeBase(indexClient);
                
                // Step 5: Run agentic retrieval with conversation
                runAgenticRetrieval(credential);
                
                // Step 6: Clean up
                deleteKnowledgeBase(indexClient);
                deleteKnowledgeSource(indexClient);
                deleteSearchIndex(indexClient);
                
                System.out.println("[DONE] Quickstart completed successfully!");
                
            } catch (Exception e) {
                System.err.println("[ERROR] Error in main execution: " + e.getMessage());
                e.printStackTrace();
            }
        }
        
        private static void createSearchIndex(SearchIndexClient indexClient) {
            System.out.println("[WAIT] Creating search index...");
            
            try {
                // Delete index if it exists
                try {
                    indexClient.deleteIndex(INDEX_NAME);
                    System.out.println("[DELETE] Deleted existing index '" + INDEX_NAME + "'");
                } catch (Exception e) {
                    // Index doesn't exist, which is fine
                }
                
                // Define fields
                List<SearchField> fields = Arrays.asList(
                    new SearchField("id", SearchFieldDataType.STRING)
                        .setKey(true)
                        .setFilterable(true)
                        .setSortable(true)
                        .setFacetable(true),
                    new SearchField("page_chunk", SearchFieldDataType.STRING)
                        .setSearchable(true)
                        .setFilterable(false)
                        .setSortable(false)
                        .setFacetable(false),
                    new SearchField("page_embedding_text_3_large", SearchFieldDataType.collection(SearchFieldDataType.SINGLE))
                        .setSearchable(true)
                        .setFilterable(false)
                        .setSortable(false)
                        .setFacetable(false)
                        .setVectorSearchDimensions(3072)
                        .setVectorSearchProfileName("hnsw_text_3_large"),
                    new SearchField("page_number", SearchFieldDataType.INT32)
                        .setFilterable(true)
                        .setSortable(true)
                        .setFacetable(true)
                );
                
                // Create vectorizer
                AzureOpenAIVectorizer vectorizer = new AzureOpenAIVectorizer("azure_openai_text_3_large")
                    .setParameters(new AzureOpenAIVectorizerParameters()
                        .setResourceUrl(AZURE_OPENAI_ENDPOINT)
                        .setDeploymentName(AZURE_OPENAI_EMBEDDING_DEPLOYMENT)
                        .setModelName(AzureOpenAIModelName.TEXT_EMBEDDING_3_LARGE));
                
                // Create vector search configuration
                VectorSearch vectorSearch = new VectorSearch()
                    .setProfiles(Arrays.asList(
                        new VectorSearchProfile("hnsw_text_3_large", "alg")
                            .setVectorizerName("azure_openai_text_3_large")
                    ))
                    .setAlgorithms(Arrays.asList(
                        new HnswAlgorithmConfiguration("alg")
                    ))
                    .setVectorizers(Arrays.asList(vectorizer));
                
                // Create semantic search configuration
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
                
                // Create the index
                SearchIndex index = new SearchIndex(INDEX_NAME)
                    .setFields(fields)
                    .setVectorSearch(vectorSearch)
                    .setSemanticSearch(semanticSearch);
                
                indexClient.createOrUpdateIndex(index);
                System.out.println("[DONE] Index '" + INDEX_NAME + "' created successfully.");
                
            } catch (Exception e) {
                System.err.println("[ERROR] Error creating index: " + e.getMessage());
                throw new RuntimeException(e);
            }
        }
        
        private static void uploadDocuments(SearchClient searchClient) {
            System.out.println("[WAIT] Uploading documents...");
            
            try {
                // Fetch documents from GitHub
                List<SearchDocument> documents = fetchEarthAtNightDocuments();
                
                searchClient.uploadDocuments(documents);
                System.out.println("[DONE] Uploaded " + documents.size() + " documents successfully.");
                
                // Wait for indexing to complete
                System.out.println("[WAIT] Waiting for document indexing to complete...");
                Thread.sleep(5000);
                System.out.println("[DONE] Document indexing completed.");
                
            } catch (Exception e) {
                System.err.println("[ERROR] Error uploading documents: " + e.getMessage());
                throw new RuntimeException(e);
            }
        }
        
        private static List<SearchDocument> fetchEarthAtNightDocuments() {
            System.out.println("[WAIT] Fetching Earth at Night documents from GitHub...");
            
            String documentsUrl = "https://raw.githubusercontent.com/Azure-Samples/azure-search-sample-data/refs/heads/main/nasa-e-book/earth-at-night-json/documents.json";
            
            try {
                java.net.http.HttpClient httpClient = java.net.http.HttpClient.newHttpClient();
                java.net.http.HttpRequest request = java.net.http.HttpRequest.newBuilder()
                    .uri(URI.create(documentsUrl))
                    .build();
                
                java.net.http.HttpResponse<String> response = httpClient.send(request, 
                    java.net.http.HttpResponse.BodyHandlers.ofString());
                
                if (response.statusCode() != 200) {
                    throw new IOException("Failed to fetch documents: " + response.statusCode());
                }
                
                ObjectMapper mapper = new ObjectMapper();
                JsonNode jsonArray = mapper.readTree(response.body());
                
                List<SearchDocument> documents = new ArrayList<>();
                for (int i = 0; i < jsonArray.size(); i++) {
                    JsonNode doc = jsonArray.get(i);
                    SearchDocument searchDoc = new SearchDocument();
                    
                    searchDoc.put("id", doc.has("id") ? doc.get("id").asText() : String.valueOf(i + 1));
                    searchDoc.put("page_chunk", doc.has("page_chunk") ? doc.get("page_chunk").asText() : "");
                    
                    // Handle embeddings
                    if (doc.has("page_embedding_text_3_large") && doc.get("page_embedding_text_3_large").isArray()) {
                        List<Double> embeddings = new ArrayList<>();
                        for (JsonNode embedding : doc.get("page_embedding_text_3_large")) {
                            embeddings.add(embedding.asDouble());
                        }
                        searchDoc.put("page_embedding_text_3_large", embeddings);
                    } else {
                        // Fallback embeddings
                        List<Double> fallbackEmbeddings = new ArrayList<>();
                        for (int j = 0; j < 3072; j++) {
                            fallbackEmbeddings.add(0.1);
                        }
                        searchDoc.put("page_embedding_text_3_large", fallbackEmbeddings);
                    }
                    
                    searchDoc.put("page_number", doc.has("page_number") ? doc.get("page_number").asInt() : i + 1);
                    
                    documents.add(searchDoc);
                }
                
                System.out.println("[DONE] Fetched " + documents.size() + " documents from GitHub");
                return documents;
                
            } catch (Exception e) {
                System.err.println("[ERROR] Error fetching documents from GitHub: " + e.getMessage());
                System.out.println("🔄 Falling back to sample documents...");
                
                // Fallback to sample documents
                List<SearchDocument> fallbackDocs = new ArrayList<>();
                
                SearchDocument doc1 = new SearchDocument();
                doc1.put("id", "1");
                doc1.put("page_chunk", "The Earth at night reveals the patterns of human settlement and economic activity. City lights trace the contours of civilization, creating a luminous map of where people live and work.");
                List<Double> embeddings1 = new ArrayList<>();
                for (int i = 0; i < 3072; i++) {
                    embeddings1.add(0.1);
                }
                doc1.put("page_embedding_text_3_large", embeddings1);
                doc1.put("page_number", 1);
                
                SearchDocument doc2 = new SearchDocument();
                doc2.put("id", "2");
                doc2.put("page_chunk", "From space, the aurora borealis appears as shimmering curtains of green and blue light dancing across the polar regions.");
                List<Double> embeddings2 = new ArrayList<>();
                for (int i = 0; i < 3072; i++) {
                    embeddings2.add(0.2);
                }
                doc2.put("page_embedding_text_3_large", embeddings2);
                doc2.put("page_number", 2);
                
                fallbackDocs.add(doc1);
                fallbackDocs.add(doc2);
                
                return fallbackDocs;
            }
        }
        
        private static void createKnowledgeSource(SearchIndexClient indexClient) {
            System.out.println("[WAIT] Creating knowledge source...");
            
            try {
                SearchIndexKnowledgeSource ks = new SearchIndexKnowledgeSource(KNOWLEDGE_SOURCE_NAME)
                    .setDescription("Knowledge source for Earth at Night data")
                    .setSearchIndexParameters(
                        new SearchIndexKnowledgeSourceParameters(INDEX_NAME)
                            .setSourceDataFields(Arrays.asList(
                                new SearchIndexFieldReference("id"),
                                new SearchIndexFieldReference("page_chunk"),
                                new SearchIndexFieldReference("page_number")
                            ))
                    );
                
                indexClient.createOrUpdateKnowledgeSource(ks);
                System.out.println("[DONE] Knowledge source '" + KNOWLEDGE_SOURCE_NAME + "' created successfully.");
                
            } catch (Exception e) {
                System.err.println("[ERROR] Error creating knowledge source: " + e.getMessage());
                throw new RuntimeException(e);
            }
        }
        
        private static void createKnowledgeBase(SearchIndexClient indexClient) {
            System.out.println("[WAIT] Creating knowledge base...");
            
            try {
                AzureOpenAIVectorizerParameters openAIParams = new AzureOpenAIVectorizerParameters()
                    .setResourceUrl(AZURE_OPENAI_ENDPOINT)
                    .setDeploymentName(AZURE_OPENAI_GPT_DEPLOYMENT)
                    .setModelName(AZURE_OPENAI_GPT_MODEL);
                
                KnowledgeBaseAzureOpenAIModel model = new KnowledgeBaseAzureOpenAIModel(openAIParams);
                
                KnowledgeBase knowledgeBase = new KnowledgeBase(
                    KNOWLEDGE_BASE_NAME,
                    Arrays.asList(new KnowledgeSourceReference(KNOWLEDGE_SOURCE_NAME))
                );
                knowledgeBase.setModels(Arrays.asList(model));
                knowledgeBase.setOutputMode(KnowledgeRetrievalOutputMode.ANSWER_SYNTHESIS);
                knowledgeBase.setAnswerInstructions(
                    "Provide a two sentence concise and informative answer based on the retrieved documents.");
                
                indexClient.createOrUpdateKnowledgeBase(knowledgeBase);
                System.out.println("[DONE] Knowledge base '" + KNOWLEDGE_BASE_NAME + "' created successfully.");
                
            } catch (Exception e) {
                System.err.println("[ERROR] Error creating knowledge base: " + e.getMessage());
                throw new RuntimeException(e);
            }
        }
        
        private static void runAgenticRetrieval(TokenCredential credential) {
            System.out.println("[SEARCH] Running agentic retrieval...");
            
            // Create retrieval client
            KnowledgeBaseRetrievalClient retrievalClient = new KnowledgeBaseRetrievalClientBuilder()
                .endpoint(SEARCH_ENDPOINT)
                .knowledgeBaseName(KNOWLEDGE_BASE_NAME)
                .credential(credential)
                .buildClient();
            
            // Initialize messages with system instructions
            List<Map<String, String>> messages = new ArrayList<>();
            
            Map<String, String> systemMessage = new HashMap<>();
            systemMessage.put("role", "system");
            systemMessage.put("content", "A Q&A agent that can answer questions about the Earth at night.\n" +
                "If you don't have the answer, respond with \"I don't know\".");
            messages.add(systemMessage);
            
            // First query
            String query1 = "Why do suburban belts display larger December brightening than urban cores " +
                "even though absolute light levels are higher downtown? Why is the Phoenix nighttime street " +
                "grid is so sharply visible from space, whereas large stretches of the interstate between " +
                "midwestern cities remain comparatively dim?";
            
            Map<String, String> userMessage = new HashMap<>();
            userMessage.put("role", "user");
            userMessage.put("content", query1);
            messages.add(userMessage);
            
            try {
                // Run first retrieval
                KnowledgeBaseRetrievalResult result = retrieveFromKnowledgeBase(retrievalClient, messages);
                
                // Extract and display response
                String responseText = extractResponseText(result);
                System.out.println("Response:");
                System.out.println(responseText);
                
                // Log activity and references
                logActivityAndReferences(result);
                
                // Add assistant response to conversation history
                Map<String, String> assistantMessage = new HashMap<>();
                assistantMessage.put("role", "assistant");
                assistantMessage.put("content", responseText);
                messages.add(assistantMessage);
                
                // Continue conversation with follow-up question
                System.out.println("\n === Continuing Conversation ===");
                String followUpQuestion = "How do I find lava at night?";
                System.out.println("[QUESTION] Follow-up question: " + followUpQuestion);
                
                Map<String, String> followUpMessage = new HashMap<>();
                followUpMessage.put("role", "user");
                followUpMessage.put("content", followUpQuestion);
                messages.add(followUpMessage);
                
                KnowledgeBaseRetrievalResult result2 = retrieveFromKnowledgeBase(retrievalClient, messages);
                
                String responseText2 = extractResponseText(result2);
                System.out.println("Response:");
                System.out.println(responseText2);
                
                logActivityAndReferences(result2);
                
                messages.add(Map.of("role", "assistant", "content", responseText2));
                
                System.out.println("\n === Conversation Complete ===");
                
            } catch (Exception e) {
                System.err.println("[ERROR] Error in agentic retrieval: " + e.getMessage());
                throw new RuntimeException(e);
            }
        }
        
        private static KnowledgeBaseRetrievalResult retrieveFromKnowledgeBase(
                KnowledgeBaseRetrievalClient client, List<Map<String, String>> messages) {
            
            KnowledgeBaseRetrievalRequest request = new KnowledgeBaseRetrievalRequest();
            
            for (Map<String, String> msg : messages) {
                if (!"system".equals(msg.get("role"))) {
                    request.getMessages().add(
                        new KnowledgeBaseMessage(
                            Arrays.asList(new KnowledgeBaseMessageTextContent(msg.get("content")))
                        ).setRole(msg.get("role"))
                    );
                }
            }
            
            request.setRetrievalReasoningEffort(new KnowledgeRetrievalLowReasoningEffort());
            
            return client.retrieve(request);
        }
        
        private static String extractResponseText(KnowledgeBaseRetrievalResult result) {
            if (result.getResponse() != null) {
                for (KnowledgeBaseMessage response : result.getResponse()) {
                    if (response.getContent() != null) {
                        for (KnowledgeBaseMessageContent content : response.getContent()) {
                            if (content instanceof KnowledgeBaseMessageTextContent) {
                                return ((KnowledgeBaseMessageTextContent) content).getText();
                            }
                        }
                    }
                }
            }
            return "No response content available";
        }
        
        private static void logActivityAndReferences(KnowledgeBaseRetrievalResult result) {
            ObjectMapper mapper = new ObjectMapper();
            
            System.out.println("Activity:");
            if (result.getActivity() != null) {
                for (KnowledgeBaseActivityRecord activity : result.getActivity()) {
                    System.out.println("Activity Type: " + activity.getClass().getSimpleName());
                    try {
                        System.out.println(mapper.writerWithDefaultPrettyPrinter()
                            .writeValueAsString(activity));
                    } catch (Exception e) {
                        System.out.println(activity.toString());
                    }
                }
            }
            
            System.out.println("References:");
            if (result.getReferences() != null) {
                for (KnowledgeBaseReference reference : result.getReferences()) {
                    System.out.println("Reference Type: " + reference.getClass().getSimpleName());
                    try {
                        System.out.println(mapper.writerWithDefaultPrettyPrinter()
                            .writeValueAsString(reference));
                    } catch (Exception e) {
                        System.out.println(reference.toString());
                    }
                }
            }
        }
        
        private static void deleteKnowledgeBase(SearchIndexClient indexClient) {
            try {
                indexClient.deleteKnowledgeBase(KNOWLEDGE_BASE_NAME);
                System.out.println("[DONE] Knowledge base '" + KNOWLEDGE_BASE_NAME + "' deleted successfully.");
            } catch (Exception e) {
                System.err.println("[ERROR] Error deleting knowledge base: " + e.getMessage());
            }
        }
        
        private static void deleteKnowledgeSource(SearchIndexClient indexClient) {
            try {
                indexClient.deleteKnowledgeSource(KNOWLEDGE_SOURCE_NAME);
                System.out.println("[DONE] Knowledge source '" + KNOWLEDGE_SOURCE_NAME + "' deleted successfully.");
            } catch (Exception e) {
                System.err.println("[ERROR] Error deleting knowledge source: " + e.getMessage());
            }
        }
        
        private static void deleteSearchIndex(SearchIndexClient indexClient) {
            try {
                indexClient.deleteIndex(INDEX_NAME);
                System.out.println("[DONE] Search index '" + INDEX_NAME + "' deleted successfully.");
            } catch (Exception e) {
                System.err.println("[ERROR] Error deleting search index: " + e.getMessage());
            }
        }
    }
    ```
    
1. Build and run the application.

    ```console
    javac AgenticRetrievalQuickstart.java -cp ".;target\dependency\*"
    java -cp ".;target\dependency\*" AgenticRetrievalQuickstart
    ```

### Output

The output of the application should be similar to the following:

```
Starting Azure AI Search agentic retrieval quickstart...

[WAIT] Creating search index...
[DELETE] Deleted existing index 'earth-at-night'
[DONE] Index 'earth-at-night' created successfully.
[WAIT] Uploading documents...
[WAIT] Fetching Earth at Night documents from GitHub...
[DONE] Fetched 194 documents from GitHub
[DONE] Uploaded 194 documents successfully.
[WAIT] Waiting for document indexing to complete...
[DONE] Document indexing completed.
[WAIT] Creating knowledge source...
[DONE] Knowledge source 'earth-knowledge-source' created successfully.
[WAIT] Creating knowledge base...
[DONE] Knowledge base 'earth-knowledge-base' created successfully.
[SEARCH] Running agentic retrieval...
Response:
Suburban belts show larger December brightening because holiday displays concentrate in
suburbs and outskirts where there is more yard space and many single-family homes, while
urban cores—already having higher absolute light levels—tend to show smaller relative
increases. Phoenix's nighttime street grid is sharply visible because the metropolitan
area is laid out on a regular, continuously lit grid with bright commercial and industrial
nodes, whereas long interstate stretches between Midwestern cities cross sparsely populated
or rural regions with far fewer continuous roadside lights.
Activity:
Activity Type: KnowledgeBaseModelQueryPlanningActivityRecord
{
  "InputTokens": 1350,
  "OutputTokens": 1314,
  "Id": 0,
  "ElapsedMs": 14162,
  "Error": null
}
Activity Type: KnowledgeBaseSearchIndexActivityRecord
{
  "SearchIndexArguments": {
    "Search": "Causes of December brightening in satellite nightlights: why suburban belts
    show larger relative December brightening than urban cores",
    "Filter": null,
    "SourceDataFields": [],
    "SearchFields": [],
    "SemanticConfigurationName": null
  },
  "KnowledgeSourceName": "earth-knowledge-source",
  "QueryTime": "2025-11-05T21:56:26.747+00:00",
  "Count": 19,
  "Id": 1,
  "ElapsedMs": 537,
  "Error": null
}
Activity Type: KnowledgeBaseSearchIndexActivityRecord
{
  "SearchIndexArguments": {
    "Search": "Why is Phoenix's nighttime street grid so sharply visible from space?",
    "Filter": null,
    "SourceDataFields": [],
    "SearchFields": [],
    "SemanticConfigurationName": null
  },
  "KnowledgeSourceName": "earth-knowledge-source",
  "QueryTime": "2025-11-05T21:56:27.182+00:00",
  "Count": 7,
  "Id": 2,
  "ElapsedMs": 434,
  "Error": null
}
Activity Type: KnowledgeBaseAgenticReasoningActivityRecord
{
  "ReasoningTokens": 70232,
  "RetrievalReasoningEffort": {},
  "Id": 3,
  "ElapsedMs": null,
  "Error": null
}
Activity Type: KnowledgeBaseModelAnswerSynthesisActivityRecord
{
  "InputTokens": 7467,
  "OutputTokens": 1710,
  "Id": 4,
  "ElapsedMs": 26663,
  "Error": null
}
References:
Reference Type: KnowledgeBaseSearchIndexReference
{
  "DocKey": "earth_at_night_508_page_104_verbalized",
  "Id": "0",
  "ActivitySource": 2,
  "SourceData": {},
  "RerankerScore": 2.6344998
}
... // Trimmed for brevity

 === Continuing Conversation ===
[QUESTION] Follow-up question: How do I find lava at night?
Response:
... // Trimmed for brevity
Activity:
... // Trimmed for brevity
References:
... // Trimmed for brevity

 === Conversation Complete ===
Knowledge base 'earth-knowledge-base' deleted successfully.
Knowledge source 'earth-knowledge-source' deleted successfully.
Index 'earth-at-night' deleted successfully.
```

## Understand the code

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
        .setSearchable(true)
        .setFilterable(false)
        .setSortable(false)
        .setFacetable(false),
    new SearchField("page_embedding_text_3_large", SearchFieldDataType.collection(SearchFieldDataType.SINGLE))
        .setSearchable(true)
        .setFilterable(false)
        .setSortable(false)
        .setFacetable(false)
        .setVectorSearchDimensions(3072)
        .setVectorSearchProfileName("hnsw_text_3_large"),
    new SearchField("page_number", SearchFieldDataType.INT32)
        .setFilterable(true)
        .setSortable(true)
        .setFacetable(true)
);

// Create vectorizer
AzureOpenAIVectorizer vectorizer = new AzureOpenAIVectorizer("azure_openai_text_3_large")
    .setParameters(new AzureOpenAIVectorizerParameters()
        .setResourceUrl(AZURE_OPENAI_ENDPOINT)
        .setDeploymentName(AZURE_OPENAI_EMBEDDING_DEPLOYMENT)
        .setModelName(AzureOpenAIModelName.TEXT_EMBEDDING_3_LARGE));

// Create vector search configuration
VectorSearch vectorSearch = new VectorSearch()
    .setProfiles(Arrays.asList(
        new VectorSearchProfile("hnsw_text_3_large", "alg")
            .setVectorizerName("azure_openai_text_3_large")
    ))
    .setAlgorithms(Arrays.asList(
        new HnswAlgorithmConfiguration("alg")
    ))
    .setVectorizers(Arrays.asList(vectorizer));

// Create semantic search configuration
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

// Create the index
SearchIndex index = new SearchIndex(INDEX_NAME)
    .setFields(fields)
    .setVectorSearch(vectorSearch)
    .setSemanticSearch(semanticSearch);

indexClient.createOrUpdateIndex(index);
```

**Reference:** [SearchField](/java/api/com.azure.search.documents.indexes.models.searchfield), [VectorSearch](/java/api/com.azure.search.documents.indexes.models.vectorsearch), [SemanticSearch](/java/api/com.azure.search.documents.indexes.models.semanticsearch), [SearchIndex](/java/api/com.azure.search.documents.indexes.models.searchindex), [SearchIndexClient](/java/api/com.azure.search.documents.indexes.searchindexclient)

### Upload documents to the index

Currently, the `earth-at-night` index is empty. The following code populates the index with JSON documents from [NASA's Earth at Night e-book](https://raw.githubusercontent.com/Azure-Samples/azure-search-sample-data/refs/heads/main/nasa-e-book/earth-at-night-json/documents.json). As required by Azure AI Search, each document conforms to the fields and data types defined in the index schema.

```java
String documentsUrl = "https://raw.githubusercontent.com/Azure-Samples/azure-search-sample-data/refs/heads/main/nasa-e-book/earth-at-night-json/documents.json";
        
try {
    java.net.http.HttpClient httpClient = java.net.http.HttpClient.newHttpClient();
    java.net.http.HttpRequest request = java.net.http.HttpRequest.newBuilder()
        .uri(URI.create(documentsUrl))
        .build();
    
    java.net.http.HttpResponse<String> response = httpClient.send(request, 
        java.net.http.HttpResponse.BodyHandlers.ofString());
    
    if (response.statusCode() != 200) {
        throw new IOException("Failed to fetch documents: " + response.statusCode());
    }
    
    ObjectMapper mapper = new ObjectMapper();
    JsonNode jsonArray = mapper.readTree(response.body());
    
    List<SearchDocument> documents = new ArrayList<>();
    for (int i = 0; i < jsonArray.size(); i++) {
        JsonNode doc = jsonArray.get(i);
        SearchDocument searchDoc = new SearchDocument();
        
        searchDoc.put("id", doc.has("id") ? doc.get("id").asText() : String.valueOf(i + 1));
        searchDoc.put("page_chunk", doc.has("page_chunk") ? doc.get("page_chunk").asText() : "");
        
        // Handle embeddings
        if (doc.has("page_embedding_text_3_large") && doc.get("page_embedding_text_3_large").isArray()) {
            List<Double> embeddings = new ArrayList<>();
            for (JsonNode embedding : doc.get("page_embedding_text_3_large")) {
                embeddings.add(embedding.asDouble());
            }
            searchDoc.put("page_embedding_text_3_large", embeddings);
        } else {
            // Fallback embeddings
            List<Double> fallbackEmbeddings = new ArrayList<>();
            for (int j = 0; j < 3072; j++) {
                fallbackEmbeddings.add(0.1);
            }
            searchDoc.put("page_embedding_text_3_large", fallbackEmbeddings);
        }
        
        searchDoc.put("page_number", doc.has("page_number") ? doc.get("page_number").asInt() : i + 1);
        
        documents.add(searchDoc);
    }
    
    System.out.println("[DONE] Fetched " + documents.size() + " documents from GitHub");
    return documents;
    
}
```


**Reference:** [SearchClient](/java/api/com.azure.search.documents.searchclient), [SearchDocument](/java/api/com.azure.search.documents.models.searchdocument)

### Create a knowledge source

A knowledge source is a reusable reference to source data. The following code defines a knowledge source named `earth-knowledge-source` that targets the `earth-at-night` index.

`SourceDataFields` specifies which index fields are included in citation references. This example includes only human-readable fields to avoid lengthy, uninterpretable embeddings in responses.

```java
SearchIndexKnowledgeSource knowledgeSource = new SearchIndexKnowledgeSource(
        KNOWLEDGE_SOURCE_NAME,
        new SearchIndexKnowledgeSourceParameters(INDEX_NAME)
            .setSourceDataFields(Arrays.asList(
                new SearchIndexFieldReference("id"),
                new SearchIndexFieldReference("page_chunk"),
                new SearchIndexFieldReference("page_number")
            ))
    );

indexClient.createOrUpdateKnowledgeSource(knowledgeSource);
```

**Reference:** [SearchIndexKnowledgeSource](/java/api/com.azure.search.documents.indexes.models.searchindexknowledgesource)

### Create a knowledge base

To target `earth-knowledge-source` and your `gpt-5-mini` deployment at query time, you need a knowledge base. The following code defines a knowledge base named `earth-knowledge-base`.

`OutputMode` is set to `AnswerSynthesis`, enabling natural-language answers that cite the retrieved documents and follow the provided `AnswerInstructions`.

```java
KnowledgeBaseAzureOpenAIModel model = new KnowledgeBaseAzureOpenAIModel(
        new AzureOpenAIVectorizerParameters()
            .setResourceUrl(AZURE_OPENAI_ENDPOINT)
            .setDeploymentName(AZURE_OPENAI_GPT_DEPLOYMENT)
            .setModelName(AZURE_OPENAI_GPT_MODEL)
    );

KnowledgeBase knowledgeBase = new KnowledgeBase(
        KNOWLEDGE_BASE_NAME,
        Arrays.asList(new KnowledgeSourceReference(KNOWLEDGE_SOURCE_NAME))
    )
    .setRetrievalReasoningEffort(new KnowledgeRetrievalLowReasoningEffort())
    .setOutputMode(KnowledgeRetrievalOutputMode.ANSWER_SYNTHESIS)
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
List<Map<String, String>> messages = new ArrayList<>();

Map<String, String> systemMessage = new HashMap<>();
systemMessage.put("role", "system");
systemMessage.put("content",
    "A Q&A agent that can answer questions about the Earth at night.\n"
    + "If you don't have the answer, respond with \"I don't know\".");
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
KnowledgeBaseRetrievalClient baseClient = new KnowledgeBaseRetrievalClientBuilder()
    .endpoint(SEARCH_ENDPOINT)
    .knowledgeBaseName(KNOWLEDGE_BASE_NAME)
    .credential(credential)
    .buildClient();

messages.add(Map.of("role", "user", "content",
    "Why do suburban belts display larger December brightening than urban "
    + "cores even though absolute light levels are higher downtown? "
    + "Why is the Phoenix nighttime street grid is so sharply visible "
    + "from space, whereas large stretches of the interstate between "
    + "midwestern cities remain comparatively dim?"));

KnowledgeBaseRetrievalRequest retrievalRequest =
    new KnowledgeBaseRetrievalRequest();

for (Map<String, String> msg : messages) {
    if (!"system".equals(msg.get("role"))) {
        retrievalRequest.getMessages().add(
            new KnowledgeBaseMessage(Arrays.asList(
                new KnowledgeBaseMessageTextContent(msg.get("content"))
            )).setRole(msg.get("role"))
        );
    }
}
retrievalRequest.setRetrievalReasoningEffort(
    new KnowledgeRetrievalLowReasoningEffort());

KnowledgeBaseRetrievalResult result =
    baseClient.retrieveFromKnowledgeBase(retrievalRequest);

String responseText = ((KnowledgeBaseMessageTextContent)
    result.getResponse().get(0).getContent().get(0)).getText();

messages.add(Map.of("role", "assistant", "content", responseText));
```

**Reference:** [KnowledgeBaseRetrievalClient](/java/api/com.azure.search.documents.knowledgebases.knowledgebaseretrievalclient), [KnowledgeBaseRetrievalRequest](/java/api/com.azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest)

#### Review the response, activity, and references

The following code displays the response, activity, and references from the retrieval pipeline, where:

+ `Response` provides a synthesized, LLM-generated answer to the query that cites the retrieved documents. When answer synthesis isn't enabled, this section contains content extracted directly from the documents.

+ `Activity` tracks the steps that were taken during the retrieval process, including the subqueries generated by your `gpt-5-mini` deployment and the tokens used for semantic ranking, query planning, and answer synthesis.

+ `References` lists the documents that contributed to the response, each one identified by their `DocKey`.

```java
System.out.println("Response:");
System.out.println(responseText);

System.out.println("Activity:");
for (KnowledgeBaseActivityRecord activity : result.getActivity()) {
    System.out.println("Activity Type: "
        + activity.getClass().getSimpleName());
    System.out.println(activity);
}

System.out.println("References:");
for (KnowledgeBaseReference reference : result.getReferences()) {
    System.out.println("Reference Type: "
        + reference.getClass().getSimpleName());
    System.out.println(reference);
}
```

### Continue the conversation

The following code continues the conversation with `earth-knowledge-base`. After you send this user query, the knowledge base fetches relevant content from `earth-knowledge-source` and appends the response to the messages list.

```java
messages.add(Map.of("role", "user", "content",
    "How do I find lava at night?"));

KnowledgeBaseRetrievalRequest followUpRequest =
    new KnowledgeBaseRetrievalRequest();

for (Map<String, String> msg : messages) {
    if (!"system".equals(msg.get("role"))) {
        followUpRequest.getMessages().add(
            new KnowledgeBaseMessage(Arrays.asList(
                new KnowledgeBaseMessageTextContent(msg.get("content"))
            )).setRole(msg.get("role"))
        );
    }
}
followUpRequest.setRetrievalReasoningEffort(
    new KnowledgeRetrievalLowReasoningEffort());

KnowledgeBaseRetrievalResult followUpResult =
    baseClient.retrieveFromKnowledgeBase(followUpRequest);
```

#### Review the new response, activity, and references

The following code displays the new response, activity, and references from the retrieval pipeline.

```java
String followUpResponseText = ((KnowledgeBaseMessageTextContent)
    followUpResult.getResponse().get(0).getContent().get(0)).getText();

System.out.println("Response:");
System.out.println(followUpResponseText);

System.out.println("Activity:");
for (KnowledgeBaseActivityRecord activity
        : followUpResult.getActivity()) {
    System.out.println("Activity Type: "
        + activity.getClass().getSimpleName());
    System.out.println(activity);
}

System.out.println("References:");
for (KnowledgeBaseReference reference
        : followUpResult.getReferences()) {
    System.out.println("Reference Type: "
        + reference.getClass().getSimpleName());
    System.out.println(reference);
}
```

## Clean up resources

[!INCLUDE [clean up resources (paid)](../resource-cleanup-paid.md)]

Otherwise, the following code from `AgenticRetrievalQuickstart.java` deleted the objects you created in this quickstart.

### Delete the knowledge base

```java
indexClient.deleteKnowledgeBase(KNOWLEDGE_BASE_NAME);
System.out.println("[DONE] Knowledge base '" + KNOWLEDGE_BASE_NAME
    + "' deleted successfully.");
```

### Delete the knowledge source

```java
indexClient.deleteKnowledgeSource(KNOWLEDGE_SOURCE_NAME);
System.out.println("[DONE] Knowledge source '" + KNOWLEDGE_SOURCE_NAME
    + "' deleted successfully.");
```

### Delete the search index

```java
indexClient.deleteIndex(INDEX_NAME);
System.out.println("[DONE] Search index '" + INDEX_NAME
    + "' deleted successfully.");
```
