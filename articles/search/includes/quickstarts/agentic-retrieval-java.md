---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 11/05/2025
---

[!INCLUDE [Feature preview](../previews/preview-generic.md)]

In this quickstart, you use [agentic retrieval](../../agentic-retrieval-overview.md) to create a conversational search experience powered by large language models (LLMs) and your proprietary data. Agentic retrieval breaks down complex user queries into subqueries, runs the subqueries in parallel, and extracts grounding data from documents indexed in Azure AI Search. The output is intended for integration with agentic and custom chat solutions.

Although you can use your own data, this quickstart uses [sample JSON documents](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/nasa-e-book/earth-at-night-json) from NASA's Earth at Night e-book. The documents describe general science topics and images of Earth at night as observed from space.

> [!TIP]
> The Java version of this quickstart uses the 2025-05-01-preview REST API version, which uses the previous "knowledge agent" terminology and doesn't support the latest features available in the 2025-11-01-preview. To use these features, see the C#, Python, or REST version.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](../../search-create-service-portal.md) in any [region that provides agentic retrieval](../../search-region-support.md).

+ A [Microsoft Foundry project](/azure/ai-foundry/how-to/create-projects) and resource. When you create a project, the resource is automatically created.

+ The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

[!INCLUDE [Setup](./agentic-retrieval-setup.md)]

## Set up the environment

The sample in this quickstart works with the Java Runtime. Install a Java Development Kit such as [Azul Zulu OpenJDK](https://www.azul.com/downloads/?package=jdk). The [Microsoft Build of OpenJDK](https://www.microsoft.com/openjdk) or your preferred JDK should also work.

1. Install [Apache Maven](https://maven.apache.org/install.html). Then run `mvn -v` to confirm successful installation.
1. Create a new folder `quickstart-agentic-retrieval` to contain the application and open Visual Studio Code in that folder with the following command:

    ```console
    mkdir quickstart-agentic-retrieval && cd quickstart-agentic-retrieval
    ```
1. Create a new `pom.xml` file in the root of your project, and copy the following code into it:

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
                <source>1.8</source>
                <target>1.8</target>
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
                <groupId>com.azure</groupId>
                <artifactId>azure-ai-openai</artifactId>
                <version>1.0.0-beta.16</version>
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
            <dependency>
                <groupId>org.apache.httpcomponents.client5</groupId>
                <artifactId>httpclient5</artifactId>
                <version>5.3.1</version>
            </dependency>
        </dependencies>
    </project>
    ```

1. Install the dependencies including the Azure AI Search client library ([Azure.Search.Documents](/java/api/overview/azure/search)) for Java and [Azure Identity client library for Java](https://mvnrepository.com/artifact/com.azure/azure-identity) with:

   ```console
   mvn clean dependency:copy-dependencies
   ```

## Run the code

1. Create a new file named `.env` in the `quickstart-agentic-retrieval` folder and add the following environment variables:

    ```
    AZURE_OPENAI_ENDPOINT=https://<your-ai-foundry-resource-name>.openai.azure.com/
    AZURE_OPENAI_GPT_DEPLOYMENT=gpt-5-mini
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
    AZURE_SEARCH_ENDPOINT=https://<your-search-service-name>.search.windows.net
    AZURE_SEARCH_INDEX_NAME=agentic-retrieval-sample
    ```

    Replace `<your-search-service-name>` and `<your-ai-foundry-resource-name>` with your actual Azure AI Search service name and Foundry resource name.

1. Paste the following code into a new file named `AgenticRetrievalQuickstart.java` in the `quickstart-agentic-retrieval` folder:

    ```java
    import com.azure.ai.openai.OpenAIAsyncClient;
    import com.azure.ai.openai.OpenAIClientBuilder;
    import com.azure.ai.openai.models.*;
    import com.azure.core.credential.TokenCredential;
    import com.azure.core.http.HttpClient;
    import com.azure.core.http.HttpHeaders;
    import com.azure.core.http.HttpMethod;
    import com.azure.core.http.HttpRequest;
    import com.azure.core.http.HttpResponse;
    import com.azure.core.util.BinaryData;
    import com.azure.identity.DefaultAzureCredential;
    import com.azure.identity.DefaultAzureCredentialBuilder;
    import com.azure.search.documents.SearchClient;
    import com.azure.search.documents.SearchClientBuilder;
    import com.azure.search.documents.SearchDocument;
    import com.azure.search.documents.indexes.SearchIndexClient;
    import com.azure.search.documents.indexes.SearchIndexClientBuilder;
    import com.azure.search.documents.indexes.models.*;
    import com.azure.search.documents.agents.SearchKnowledgeAgentClient;
    import com.azure.search.documents.agents.SearchKnowledgeAgentClientBuilder;
    import com.azure.search.documents.agents.models.*;
    import com.fasterxml.jackson.databind.JsonNode;
    import com.fasterxml.jackson.databind.ObjectMapper;
    import com.fasterxml.jackson.databind.node.ObjectNode;
    import io.github.cdimascio.dotenv.Dotenv;
    
    import java.io.IOException;
    import java.net.URI;
    import java.net.http.HttpRequest.Builder;
    import java.time.Duration;
    import java.util.*;
    import java.util.concurrent.TimeUnit;
    
    public class AgenticRetrievalQuickstart {
        
        // Configuration - Update these values for your environment
        private static final String SEARCH_ENDPOINT;
        private static final String AZURE_OPENAI_ENDPOINT;
        private static final String AZURE_OPENAI_GPT_DEPLOYMENT;
        private static final String AZURE_OPENAI_GPT_MODEL = "gpt-5-mini";
        private static final String AZURE_OPENAI_EMBEDDING_DEPLOYMENT;
        private static final String AZURE_OPENAI_EMBEDDING_MODEL = "text-embedding-3-large";
        private static final String INDEX_NAME = "earth_at_night";
        private static final String AGENT_NAME = "earth-search-agent";
        private static final String SEARCH_API_VERSION = "2025-05-01-Preview";
        
        static {
            // Load environment variables from .env file
            Dotenv dotenv = Dotenv.configure().ignoreIfMissing().load();
            
            SEARCH_ENDPOINT = getEnvVar(dotenv, "AZURE_SEARCH_ENDPOINT", 
                "https://contoso-agentic-search-service.search.windows.net");
            AZURE_OPENAI_ENDPOINT = getEnvVar(dotenv, "AZURE_OPENAI_ENDPOINT",
                "https://contoso-proj-agentic-foundry-res.openai.azure.com/");
            AZURE_OPENAI_GPT_DEPLOYMENT = getEnvVar(dotenv, "AZURE_OPENAI_GPT_DEPLOYMENT", "gpt-5-mini");
            AZURE_OPENAI_EMBEDDING_DEPLOYMENT = getEnvVar(dotenv, "AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-large");
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
                SearchIndexClient searchIndexClient = new SearchIndexClientBuilder()
                    .endpoint(SEARCH_ENDPOINT)
                    .credential(credential)
                    .buildClient();
                    
                SearchClient searchClient = new SearchClientBuilder()
                    .endpoint(SEARCH_ENDPOINT)
                    .indexName(INDEX_NAME)
                    .credential(credential)
                    .buildClient();
                
                // Create Azure OpenAI client
                OpenAIAsyncClient openAIClient = new OpenAIClientBuilder()
                    .endpoint(AZURE_OPENAI_ENDPOINT)
                    .credential(credential)
                    .buildAsyncClient();
                
                // Step 1: Create search index with vector and semantic capabilities
                createSearchIndex(searchIndexClient);
                
                // Step 2: Upload documents
                uploadDocuments(searchClient);
                
                // Step 3: Create knowledge agent
                createKnowledgeAgent(credential);
                
                // Step 4: Run agentic retrieval with conversation
                runAgenticRetrieval(credential, openAIClient);
                
                // Step 5: Clean up - Delete knowledge agent and search index
                deleteKnowledgeAgent(credential);
                deleteSearchIndex(searchIndexClient);
                
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
        
        private static void createKnowledgeAgent(TokenCredential credential) {
            System.out.println("[WAIT] Creating knowledge agent...");
            
            // Delete agent if it exists
            deleteKnowledgeAgent(credential);
            
            try {
                ObjectMapper mapper = new ObjectMapper();
                ObjectNode agentDefinition = mapper.createObjectNode();
                agentDefinition.put("name", AGENT_NAME);
                agentDefinition.put("description", "Knowledge agent for Earth at Night e-book content");
                
                ObjectNode model = mapper.createObjectNode();
                model.put("kind", "azureOpenAI");
                ObjectNode azureOpenAIParams = mapper.createObjectNode();
                azureOpenAIParams.put("resourceUri", AZURE_OPENAI_ENDPOINT);
                azureOpenAIParams.put("deploymentId", AZURE_OPENAI_GPT_DEPLOYMENT);
                azureOpenAIParams.put("modelName", AZURE_OPENAI_GPT_MODEL);
                model.set("azureOpenAIParameters", azureOpenAIParams);
                agentDefinition.set("models", mapper.createArrayNode().add(model));
                
                ObjectNode targetIndex = mapper.createObjectNode();
                targetIndex.put("indexName", INDEX_NAME);
                targetIndex.put("defaultRerankerThreshold", 2.5);
                agentDefinition.set("targetIndexes", mapper.createArrayNode().add(targetIndex));
                
                String token = getAccessToken(credential, "https://search.azure.com/.default");
                
                java.net.http.HttpClient httpClient = java.net.http.HttpClient.newHttpClient();
                java.net.http.HttpRequest request = java.net.http.HttpRequest.newBuilder()
                    .uri(URI.create(SEARCH_ENDPOINT + "/agents/" + AGENT_NAME + "?api-version=" + SEARCH_API_VERSION))
                    .header("Content-Type", "application/json")
                    .header("Authorization", "Bearer " + token)
                    .PUT(java.net.http.HttpRequest.BodyPublishers.ofString(mapper.writeValueAsString(agentDefinition)))
                    .build();
                
                java.net.http.HttpResponse<String> response = httpClient.send(request,
                    java.net.http.HttpResponse.BodyHandlers.ofString());
                
                if (response.statusCode() >= 400) {
                    throw new RuntimeException("Failed to create knowledge agent: " + response.statusCode() + " " + response.body());
                }
                
                System.out.println("[DONE] Knowledge agent '" + AGENT_NAME + "' created successfully.");
                
            } catch (Exception e) {
                System.err.println("[ERROR] Error creating knowledge agent: " + e.getMessage());
                throw new RuntimeException(e);
            }
        }
        
        private static void runAgenticRetrieval(TokenCredential credential, OpenAIAsyncClient openAIClient) {
            System.out.println("[SEARCH] Running agentic retrieval...");
            
            // Initialize messages with system instructions
            List<Map<String, String>> messages = new ArrayList<>();
            
            Map<String, String> systemMessage = new HashMap<>();
            systemMessage.put("role", "system");
            systemMessage.put("content", "A Q&A agent that can answer questions about the Earth at night.\n" +
                "Sources have a JSON format with a ref_id that must be cited in the answer.\n" +
                "If you do not have the answer, respond with \"I don't know\".");
            messages.add(systemMessage);
            
            Map<String, String> userMessage = new HashMap<>();
            userMessage.put("role", "user");
            userMessage.put("content", "Why do suburban belts display larger December brightening than urban cores even though absolute light levels are higher downtown? Why is the Phoenix nighttime street grid is so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?");
            messages.add(userMessage);
            
            try {
                // Call agentic retrieval API (excluding system message)
                List<Map<String, String>> userMessages = messages.stream()
                    .filter(m -> !"system".equals(m.get("role")))
                    .collect(java.util.stream.Collectors.toList());
                
                String retrievalResponse = callAgenticRetrieval(credential, userMessages);
                
                // Add assistant response to conversation history
                Map<String, String> assistantMessage = new HashMap<>();
                assistantMessage.put("role", "assistant");
                assistantMessage.put("content", retrievalResponse);
                messages.add(assistantMessage);
                
                System.out.println(retrievalResponse);
                
                // Now do chat completion with full conversation history
                generateFinalAnswer(openAIClient, messages);
                
                // Continue conversation with second question
                continueConversation(credential, openAIClient, messages);
                
            } catch (Exception e) {
                System.err.println("[ERROR] Error in agentic retrieval: " + e.getMessage());
                throw new RuntimeException(e);
            }
        }
        
        private static String callAgenticRetrieval(TokenCredential credential, List<Map<String, String>> messages) {
            try {
                ObjectMapper mapper = new ObjectMapper();
                ObjectNode retrievalRequest = mapper.createObjectNode();
                
                // Convert messages to the correct format expected by the Knowledge agent
                com.fasterxml.jackson.databind.node.ArrayNode agentMessages = mapper.createArrayNode();
                for (Map<String, String> msg : messages) {
                    ObjectNode agentMessage = mapper.createObjectNode();
                    agentMessage.put("role", msg.get("role"));
                    
                    com.fasterxml.jackson.databind.node.ArrayNode content = mapper.createArrayNode();
                    ObjectNode textContent = mapper.createObjectNode();
                    textContent.put("type", "text");
                    textContent.put("text", msg.get("content"));
                    content.add(textContent);
                    agentMessage.set("content", content);
                    
                    agentMessages.add(agentMessage);
                }
                retrievalRequest.set("messages", agentMessages);
                
                com.fasterxml.jackson.databind.node.ArrayNode targetIndexParams = mapper.createArrayNode();
                ObjectNode indexParam = mapper.createObjectNode();
                indexParam.put("indexName", INDEX_NAME);
                indexParam.put("rerankerThreshold", 2.5);
                indexParam.put("maxDocsForReranker", 100);
                indexParam.put("includeReferenceSourceData", true);
                targetIndexParams.add(indexParam);
                retrievalRequest.set("targetIndexParams", targetIndexParams);
                
                String token = getAccessToken(credential, "https://search.azure.com/.default");
                
                java.net.http.HttpClient httpClient = java.net.http.HttpClient.newHttpClient();
                java.net.http.HttpRequest request = java.net.http.HttpRequest.newBuilder()
                    .uri(URI.create(SEARCH_ENDPOINT + "/agents/" + AGENT_NAME + "/retrieve?api-version=" + SEARCH_API_VERSION))
                    .header("Content-Type", "application/json")
                    .header("Authorization", "Bearer " + token)
                    .POST(java.net.http.HttpRequest.BodyPublishers.ofString(mapper.writeValueAsString(retrievalRequest)))
                    .build();
                
                java.net.http.HttpResponse<String> response = httpClient.send(request,
                    java.net.http.HttpResponse.BodyHandlers.ofString());
                
                if (response.statusCode() >= 400) {
                    throw new RuntimeException("Agentic retrieval failed: " + response.statusCode() + " " + response.body());
                }
                
                JsonNode responseJson = mapper.readTree(response.body());
                
                // Log activities and results
                logActivitiesAndResults(responseJson);
                
                // Extract response content
                if (responseJson.has("response") && responseJson.get("response").isArray()) {
                    com.fasterxml.jackson.databind.node.ArrayNode responseArray = (com.fasterxml.jackson.databind.node.ArrayNode) responseJson.get("response");
                    if (responseArray.size() > 0) {
                        JsonNode firstResponse = responseArray.get(0);
                        if (firstResponse.has("content") && firstResponse.get("content").isArray()) {
                            com.fasterxml.jackson.databind.node.ArrayNode contentArray = (com.fasterxml.jackson.databind.node.ArrayNode) firstResponse.get("content");
                            if (contentArray.size() > 0) {
                                JsonNode textContent = contentArray.get(0);
                                if (textContent.has("text")) {
                                    return textContent.get("text").asText();
                                }
                            }
                        }
                    }
                }
                
                return "No response content available";
                
            } catch (Exception e) {
                System.err.println("[ERROR] Error in agentic retrieval call: " + e.getMessage());
                throw new RuntimeException(e);
            }
        }
        
        private static void logActivitiesAndResults(JsonNode responseJson) {
            ObjectMapper mapper = new ObjectMapper();
            
            // Log activities
            System.out.println("\nActivities:");
            if (responseJson.has("activity") && responseJson.get("activity").isArray()) {
                for (JsonNode activity : responseJson.get("activity")) {
                    String activityType = "UnknownActivityRecord";
                    if (activity.has("InputTokens")) {
                        activityType = "KnowledgeAgentModelQueryPlanningActivityRecord";
                    } else if (activity.has("TargetIndex")) {
                        activityType = "KnowledgeAgentSearchActivityRecord";
                    } else if (activity.has("QueryTime")) {
                        activityType = "KnowledgeAgentSemanticRankerActivityRecord";
                    }
                    
                    System.out.println("Activity Type: " + activityType);
                    try {
                        System.out.println(mapper.writerWithDefaultPrettyPrinter().writeValueAsString(activity));
                    } catch (Exception e) {
                        System.out.println(activity.toString());
                    }
                }
            }
            
            // Log results
            System.out.println("Results");
            if (responseJson.has("references") && responseJson.get("references").isArray()) {
                for (JsonNode reference : responseJson.get("references")) {
                    String referenceType = "KnowledgeAgentAzureSearchDocReference";
                    
                    System.out.println("Reference Type: " + referenceType);
                    try {
                        System.out.println(mapper.writerWithDefaultPrettyPrinter().writeValueAsString(reference));
                    } catch (Exception e) {
                        System.out.println(reference.toString());
                    }
                }
            }
        }
        
        private static void generateFinalAnswer(OpenAIAsyncClient openAIClient, List<Map<String, String>> messages) {
            System.out.println("\n[ASSISTANT]: ");
            
            try {
                List<ChatRequestMessage> chatMessages = new ArrayList<>();
                for (Map<String, String> msg : messages) {
                    String role = msg.get("role");
                    String content = msg.get("content");
                    
                    switch (role) {
                        case "system":
                            chatMessages.add(new ChatRequestSystemMessage(content));
                            break;
                        case "user":
                            chatMessages.add(new ChatRequestUserMessage(content));
                            break;
                        case "assistant":
                            chatMessages.add(new ChatRequestAssistantMessage(content));
                            break;
                    }
                }
                
                ChatCompletionsOptions chatOptions = new ChatCompletionsOptions(chatMessages)
                    .setMaxTokens(1000)
                    .setTemperature(0.7);
                
                ChatCompletions completion = openAIClient.getChatCompletions(AZURE_OPENAI_GPT_DEPLOYMENT, chatOptions).block();
                
                if (completion != null && completion.getChoices() != null && !completion.getChoices().isEmpty()) {
                    String answer = completion.getChoices().get(0).getMessage().getContent();
                    System.out.println(answer.replace(".", "\n"));
                    
                    // Add this response to conversation history
                    Map<String, String> assistantResponse = new HashMap<>();
                    assistantResponse.put("role", "assistant");
                    assistantResponse.put("content", answer);
                    messages.add(assistantResponse);
                }
                
            } catch (Exception e) {
                System.err.println("[ERROR] Error generating final answer: " + e.getMessage());
                throw new RuntimeException(e);
            }
        }
        
        private static void continueConversation(TokenCredential credential, OpenAIAsyncClient openAIClient, List<Map<String, String>> messages) {
            System.out.println("\n === Continuing Conversation ===");
            
            // Add follow-up question
            String followUpQuestion = "How do I find lava at night?";
            System.out.println("[QUESTION] Follow-up question: " + followUpQuestion);
            
            Map<String, String> userMessage = new HashMap<>();
            userMessage.put("role", "user");
            userMessage.put("content", followUpQuestion);
            messages.add(userMessage);
            
            try {
                // FILTER OUT SYSTEM MESSAGE - only send user/assistant messages to agentic retrieval
                List<Map<String, String>> userAssistantMessages = messages.stream()
                    .filter(m -> !"system".equals(m.get("role")))
                    .collect(java.util.stream.Collectors.toList());
                
                String newRetrievalResponse = callAgenticRetrieval(credential, userAssistantMessages);
                
                // Add assistant response to conversation history
                Map<String, String> assistantMessage = new HashMap<>();
                assistantMessage.put("role", "assistant");
                assistantMessage.put("content", newRetrievalResponse);
                messages.add(assistantMessage);
                
                System.out.println(newRetrievalResponse);
                
                // Generate final answer for follow-up
                generateFinalAnswer(openAIClient, messages);
                
                System.out.println("\n === Conversation Complete ===");
                
            } catch (Exception e) {
                System.err.println("[ERROR] Error in conversation continuation: " + e.getMessage());
                throw new RuntimeException(e);
            }
        }
        
        private static void deleteKnowledgeAgent(TokenCredential credential) {
            System.out.println("[DELETE] Deleting knowledge agent...");
            
            try {
                String token = getAccessToken(credential, "https://search.azure.com/.default");
                
                java.net.http.HttpClient httpClient = java.net.http.HttpClient.newHttpClient();
                java.net.http.HttpRequest request = java.net.http.HttpRequest.newBuilder()
                    .uri(URI.create(SEARCH_ENDPOINT + "/agents/" + AGENT_NAME + "?api-version=" + SEARCH_API_VERSION))
                    .header("Authorization", "Bearer " + token)
                    .DELETE()
                    .build();
                
                java.net.http.HttpResponse<String> response = httpClient.send(request,
                    java.net.http.HttpResponse.BodyHandlers.ofString());
                
                if (response.statusCode() == 404) {
                    System.out.println("[INFO] Knowledge agent '" + AGENT_NAME + "' does not exist or was already deleted.");
                    return;
                }
                
                if (response.statusCode() >= 400) {
                    throw new RuntimeException("Failed to delete knowledge agent: " + response.statusCode() + " " + response.body());
                }
                
                System.out.println("[DONE] Knowledge agent '" + AGENT_NAME + "' deleted successfully.");
                
            } catch (Exception e) {
                System.err.println("[ERROR] Error deleting knowledge agent: " + e.getMessage());
                // Don't throw - this is cleanup
            }
        }
        
        private static void deleteSearchIndex(SearchIndexClient indexClient) {
            System.out.println("[DELETE] Deleting search index...");
            
            try {
                indexClient.deleteIndex(INDEX_NAME);
                System.out.println("[DONE] Search index '" + INDEX_NAME + "' deleted successfully.");
                
            } catch (Exception e) {
                if (e.getMessage() != null && (e.getMessage().contains("404") || e.getMessage().contains("IndexNotFound"))) {
                    System.out.println("[INFO] Search index '" + INDEX_NAME + "' does not exist or was already deleted.");
                    return;
                }
                System.err.println("[ERROR] Error deleting search index: " + e.getMessage());
                // Don't throw - this is cleanup
            }
        }
        
        private static String getAccessToken(TokenCredential credential, String scope) {
            try {
                return credential.getToken(new com.azure.core.credential.TokenRequestContext().addScopes(scope)).block().getToken();
            } catch (Exception e) {
                throw new RuntimeException("Failed to get access token", e);
            }
        }
    }
    ```
    
1. Sign in to Azure with the following command:

    ```console
    az login
    ```

1. Run your new console application:

    ```console
    javac Address.java App.java Hotel.java -cp ".;target\dependency\*"
    java -cp ".;target\dependency\*" App
    ```

### Output

The output of the application should be similar to the following:

```
Starting Azure AI Search agentic retrieval quickstart...

[WAIT] Creating search index...
[DELETE] Deleted existing index 'earth_at_night'
[DONE] Index 'earth_at_night' created successfully.
[WAIT] Uploading documents...
[WAIT] Fetching Earth at Night documents from GitHub...
[DONE] Fetched 194 documents from GitHub
[DONE] Uploaded 194 documents successfully.
[WAIT] Waiting for document indexing to complete...
[DONE] Document indexing completed.
[WAIT] Creating knowledge agent...
[DELETE] Deleting knowledge agent...
[INFO] Knowledge agent 'earth-search-agent' does not exist or was already deleted.
[DONE] Knowledge agent 'earth-search-agent' created successfully.
[SEARCH] Running agentic retrieval...

Activities:
Activity Type: UnknownActivityRecord
{
  "type" : "ModelQueryPlanning",
  "id" : 0,
  "inputTokens" : 1379,
  "outputTokens" : 545
}
Activity Type: UnknownActivityRecord
{
  "type" : "AzureSearchQuery",
  "id" : 1,
  "targetIndex" : "earth_at_night",
  "query" : {
    "search" : "Why do suburban areas show greater December brightening compared to urban cores despite higher absolute light levels downtown?",
    "filter" : null
  },
  "queryTime" : "2025-07-21T15:07:04.024Z",
  "count" : 0,
  "elapsedMs" : 2609
}
Activity Type: UnknownActivityRecord
{
  "type" : "AzureSearchQuery",
  "id" : 2,
  "targetIndex" : "earth_at_night",
  "query" : {
    "search" : "Why is the Phoenix nighttime street grid sharply visible from space, while large stretches of interstate highways between Midwestern cities appear comparatively dim?",
    "filter" : null
  },
  "queryTime" : "2025-07-21T15:07:04.267Z",
  "count" : 0,
  "elapsedMs" : 243
}
Activity Type: UnknownActivityRecord
{
  "type" : "AzureSearchSemanticRanker",
  "id" : 3,
  "inputTokens" : 48602
}
Results
[]

[ASSISTANT]: 
The suburban belts display larger December brightening than urban cores despite higher absolute light levels downtown likely because suburban areas have more seasonal variation in lighting usage, such as increased outdoor and holiday lighting in December
 Urban cores, being brightly lit throughout the year, show less relative change


Regarding Phoenix's nighttime street grid visibility, it is sharply visible from space due to the structured and continuous lighting of the city's streets
 In contrast, large stretches of interstate highways between Midwestern cities are comparatively dim because highways typically have less intense and less frequent lighting compared to urban street grids


[Note: This explanation is based on general knowledge; no specific source with ref_id was provided
]

 === Continuing Conversation ===
[QUESTION] Follow-up question: How do I find lava at night?

Activities:
Activity Type: UnknownActivityRecord
{
  "type" : "ModelQueryPlanning",
  "id" : 0,
  "inputTokens" : 1545,
  "outputTokens" : 127
}
Activity Type: UnknownActivityRecord
{
  "type" : "AzureSearchQuery",
  "id" : 1,
  "targetIndex" : "earth_at_night",
  "query" : {
    "search" : "How can I find lava at night?",
    "filter" : null
  },
  "queryTime" : "2025-07-21T15:07:15.445Z",
  "count" : 6,
  "elapsedMs" : 370
}
Activity Type: UnknownActivityRecord
{
  "type" : "AzureSearchSemanticRanker",
  "id" : 2,
  "inputTokens" : 22994
}
Results
Reference Type: KnowledgeAgentAzureSearchDocReference
{
  "type" : "AzureSearchDoc",
  "id" : "0",
  "activitySource" : 1,
  "docKey" : "earth_at_night_508_page_44_verbalized",
  "sourceData" : {
    "id" : "earth_at_night_508_page_44_verbalized",
    "page_chunk" : "## Nature's Light Shows\n\nAt night, with the light of the Sun removed, nature's brilliant glow from Earth's surface becomes visible to the naked eye from space. Some of Earth's most spectacular light shows are natural, like the aurora borealis, or Northern Lights, in the Northern Hemisphere (aurora australis, or Southern Lights, in the Southern Hemisphere). The auroras are natural electrical phenomena caused by charged particles that race from the Sun toward Earth, inducing chemical reactions in the upper atmosphere and creating the appearance of streamers of reddish or greenish light in the sky, usually near the northern or southern magnetic pole. Other natural lights can indicate danger, like a raging forest fire encroaching on a city, town, or community, or lava spewing from an erupting volcano.\n\nWhatever the source, the ability of humans to monitor nature's light shows at night has practical applications for society. For example, tracking fires during nighttime hours allows for continuous monitoring and enhances our ability to protect humans and other animals, plants, and infrastructure. Combined with other data sources, our ability to observe the light of fires at night allows emergency managers to more efficiently and accurately issue warnings and evacuation orders and allows firefighting efforts to continue through the night. With enough moonlight (e.g., full-Moon phase), it's even possible to track the movement of smoke plumes at night, which can impact air quality, regardless of time of day.\n\nAnother natural source of light at night is emitted from glowing lava flows at the site of active volcanoes. Again, with enough moonlight, these dramatic scenes can be tracked and monitored for both scientific research and public safety.\n\n\n### Figure: The Northern Lights Viewed from Space\n\n**September 17, 2011**\n\nThis photo, taken from the International Space Station on September 17, 2011, shows a spectacular display of the aurora borealis (Northern Lights) as green and reddish light in the night sky above Earth. In the foreground, part of a Soyuz spacecraft is visible, silhouetted against the bright auroral light. The green glow is generated by energetic charged particles from the Sun interacting with Earth's upper atmosphere, exciting oxygen and nitrogen atoms, and producing characteristic colors. The image demonstrates the vividness and grandeur of natural night-time light phenomena as seen from orbit."
  }
}
Reference Type: KnowledgeAgentAzureSearchDocReference
{
  "type" : "AzureSearchDoc",
  "id" : "1",
  "activitySource" : 1,
  "docKey" : "earth_at_night_508_page_65_verbalized",
  "sourceData" : {
    "id" : "earth_at_night_508_page_65_verbalized",
    "page_chunk" : "# Volcanoes\n\n## Figure: Satellite Image of Sicily and Mount Etna Lava, March 16, 2017\n\nThe annotated satellite image below shows the island of Sicily and the surrounding region at night, highlighting city lights and volcanic activity.\n\n**Description:**\n\n- **Date of image:** March 16, 2017\n- **Geographical locations labeled:**\n    - Major cities: Palermo (northwest Sicily), Marsala (western Sicily), Catania (eastern Sicily)\n    - Significant feature: Mount Etna, labeled with an adjacent \"hot lava\" region showing the glow from active lava flows\n    - Surrounding water body: Mediterranean Sea\n    - Island: Malta to the south of Sicily\n- **Other details:** \n    - The image is shown at night, with bright spots indicating city lights.\n    - The position of \"hot lava\" near Mount Etna is distinctly visible as a bright spot different from other city lights, indicating volcanic activity.\n    - A scale bar is included showing a reference length of 50 km.\n    - North direction is indicated with an arrow.\n    - Cloud cover is visible in the southwest part of the image, partially obscuring the view near Marsala and Malta.\n\n**Summary of Features Visualized:**\n\n| Feature          | Description                                           |\n|------------------|------------------------------------------------------|\n| Cities           | Bright clusters indicating locations: Palermo, Marsala, Catania |\n| Mount Etna       | Marked on the map, located on the eastern side of Sicily, with visible hot lava activity |\n| Malta            | Clearly visible to the south of Sicily               |\n| Water bodies     | Mediterranean Sea labeled                            |\n| Scale & Direction| 50 km scale bar and North indicator                  |\n| Date             | March 16, 2017                                       |\n| Cloud Cover      | Visible in the lower left (southern) part of the image |\n\nThis figure demonstrates the visibility of volcanic activity at Mount Etna from space at night, distinguishing the light from hot lava against the background city lights of Sicily and Malta."
  }
}
Reference Type: KnowledgeAgentAzureSearchDocReference
{
  "type" : "AzureSearchDoc",
  "id" : "2",
  "activitySource" : 1,
  "docKey" : "earth_at_night_508_page_64_verbalized",
  "sourceData" : {
    "id" : "earth_at_night_508_page_64_verbalized",
    "page_chunk" : "<!-- PageHeader=\"Volcanoes\" -->\n\n### Nighttime Glow at Mount Etna - Italy\n\nAt about 2:30 a.m. local time on March 16, 2017, the VIIRS DNB on the Suomi NPP satellite captured this nighttime image of lava flowing on Mount Etna in Sicily, Italy. Etna is one of the world's most active volcanoes.\n\n#### Figure: Location of Mount Etna\nA world globe is depicted, with a marker indicating the location of Mount Etna in Sicily, Italy, in southern Europe near the center of the Mediterranean Sea.\n\n<!-- PageFooter=\"Earth at Night\" -->\n<!-- PageNumber=\"48\" -->"
  }
}
Reference Type: KnowledgeAgentAzureSearchDocReference
{
  "type" : "AzureSearchDoc",
  "id" : "3",
  "activitySource" : 1,
  "docKey" : "earth_at_night_508_page_66_verbalized",
  "sourceData" : {
    "id" : "earth_at_night_508_page_66_verbalized",
    "page_chunk" : "# Volcanoes\n\n---\n\n### Mount Etna Erupts - Italy\n\nThe highly active Mount Etna in Italy sent red lava rolling down its flank on March 19, 2017. An astronaut onboard the ISS took the photograph below of the volcano and its environs that night. City lights surround the mostly dark volcanic area.\n\n---\n\n#### Figure 1: Location of Mount Etna, Italy\n\nA world map highlighting the location of Mount Etna in southern Italy. The marker indicates its geographic placement on the east coast of Sicily, Italy, in the Mediterranean region, south of mainland Europe and north of northern Africa.\n\n---\n\n#### Figure 2: Nighttime View of Mount Etna's Eruption and Surrounding Cities\n\nThis is a nighttime satellite image taken on March 19, 2017, showing the eruption of Mount Etna (southeastern cone) with visible bright red and orange coloring indicating flowing lava from a lateral vent. The surrounding areas are illuminated by city lights, with the following geographic references labeled:\n\n| Location        | Position in Image         | Visible Characteristics                    |\n|-----------------|--------------------------|--------------------------------------------|\n| Mt. Etna (southeastern cone) | Top center-left | Bright red/orange lava flow                |\n| Lateral vent    | Left of the volcano       | Faint red/orange flow extending outwards   |\n| Resort          | Below the volcano, to the left   | Small cluster of lights                    |\n| Giarre          | Top right                 | Bright cluster of city lights              |\n| Acireale        | Center right              | Large, bright area of city lights          |\n| Biancavilla     | Bottom left               | Smaller cluster of city lights             |\n\nAn arrow pointing north is shown on the image for orientation.\n\n---\n\n<!-- Earth at Night Page Footer -->\n<!-- Page Number: 50 -->"
  }
}
Reference Type: KnowledgeAgentAzureSearchDocReference
{
  "type" : "AzureSearchDoc",
  "id" : "4",
  "activitySource" : 1,
  "docKey" : "earth_at_night_508_page_46_verbalized",
  "sourceData" : {
    "id" : "earth_at_night_508_page_46_verbalized",
    "page_chunk" : "For the first time in perhaps a decade, Mount Etna experienced a \"flank eruption\"�erupting from its side instead of its summit�on December 24, 2018. The activity was accompanied by 130 earthquakes occurring over three hours that morning. Mount Etna, Europe�s most active volcano, has seen periodic activity on this part of the mountain since 2013. The Operational Land Imager (OLI) on the Landsat 8 satellite acquired the main image of Mount Etna on December 28, 2018.\n\nThe inset image highlights the active vent and thermal infrared signature from lava flows, which can be seen near the newly formed fissure on the southeastern side of the volcano. The inset was created with data from OLI and the Thermal Infrared Sensor (TIRS) on Landsat 8. Ash spewing from the fissure cloaked adjacent villages and delayed aircraft from landing at the nearby Catania airport. Earthquakes occurred in the subsequent days after the initial eruption and displaced hundreds of people from their homes.\n\nFor nighttime images of Mount Etna�s March 2017 eruption, see pages 48�51.\n\n---\n\n### Hazards of Volcanic Ash Plumes and Satellite Observation\n\nWith the help of moonlight, satellite instruments can track volcanic ash plumes, which present significant hazards to airplanes in flight. The volcanic ash�composed of tiny pieces of glass and rock�is abrasive to engine turbine blades, and can melt on the blades and other engine parts, causing damage and even engine stalls. This poses a danger to both the plane�s integrity and passenger safety. Volcanic ash also reduces visibility for pilots and can cause etching of windshields, further reducing pilots� ability to see. Nightlight images can be combined with thermal images to provide a more complete view of volcanic activity on Earth�s surface.\n\nThe VIIRS Day/Night Band (DNB) on polar-orbiting satellites uses faint light sources such as moonlight, airglow (the atmosphere�s self-illumination through chemical reactions), zodiacal light (sunlight scattered by interplanetary dust), and starlight from the Milky Way. Using these dim light sources, the DNB can detect changes in clouds, snow cover, and sea ice:\n\n#### Table: Light Sources Used by VIIRS DNB\n\n| Light Source         | Description                                                                  |\n|----------------------|------------------------------------------------------------------------------|\n| Moonlight            | Reflected sunlight from the Moon, illuminating Earth's surface at night      |\n| Airglow              | Atmospheric self-illumination from chemical reactions                        |\n| Zodiacal Light       | Sunlight scattered by interplanetary dust                                    |\n| Starlight/Milky Way  | Faint illumination provided by stars in the Milky Way                        |\n\nGeostationary Operational Environmental Satellites (GOES), managed by NOAA, orbit over Earth�s equator and offer uninterrupted observations of North America. High-latitude areas such as Alaska benefit from polar-orbiting satellites like Suomi NPP, which provide overlapping coverage at the poles, enabling more data collection in these regions. During polar darkness (winter months), VIIRS DNB data allow scientists to:\n\n- Observe sea ice formation\n- Monitor snow cover extent at the highest latitudes\n- Detect open water for ship navigation\n\n#### Table: Satellite Coverage Overview\n\n| Satellite Type          | Orbit           | Coverage Area         | Special Utility                              |\n|------------------------|-----------------|----------------------|----------------------------------------------|\n| GOES                   | Geostationary   | Equatorial/North America | Continuous regional monitoring              |\n| Polar-Orbiting (e.g., Suomi NPP) | Polar-orbiting    | Poles/high latitudes      | Overlapping passes; useful during polar night|\n\n---\n\n### Weather Forecasting and Nightlight Data\n\nThe use of nightlight data by weather forecasters is growing as the VIIRS instrument enables observation of clouds at night illuminated by sources such as moonlight and lightning. Scientists use these data to study the nighttime behavior of weather systems, including severe storms, which can develop and strike populous areas at night as well as during the day. Combined with thermal data, visible nightlight data allow the detection of clouds at various heights in the atmosphere, such as dense marine fog. This capability enables weather forecasters to issue marine advisories with higher confidence, leading to greater utility. (See \"Marine Layer Clouds�California\" on page 56.)\n\nIn this section of the book, you will see how nightlight data are used to observe nature�s spectacular light shows across a wide range of sources.\n\n---\n\n#### Notable Data from Mount Etna Flank Eruption (December 2018)\n\n| Event/Observation                  | Details                                                                    |\n|-------------------------------------|----------------------------------------------------------------------------|\n| Date of Flank Eruption              | December 24, 2018                                                          |\n| Number of Earthquakes               | 130 earthquakes within 3 hours                                              |\n| Image Acquisition                   | December 28, 2018 by Landsat 8 OLI                                         |\n| Location of Eruption                | Southeastern side of Mount Etna                                            |\n| Thermal Imaging Data                | From OLI and TIRS (Landsat 8), highlighting active vent and lava flows     |\n| Impact on Villages/Air Transport    | Ash covered villages; delayed aircraft at Catania airport                  |\n| Displacement                        | Hundreds of residents displaced                                            |\n| Ongoing Seismic Activity            | Earthquakes continued after initial eruption                               |\n\n---\n\n<!-- PageFooter=\"Earth at Night\" -->\n<!-- PageNumber=\"30\" -->"
  }
}
Reference Type: KnowledgeAgentAzureSearchDocReference
{
  "type" : "AzureSearchDoc",
  "id" : "5",
  "activitySource" : 1,
  "docKey" : "earth_at_night_508_page_60_verbalized",
  "sourceData" : {
    "id" : "earth_at_night_508_page_60_verbalized",
    "page_chunk" : "<!-- PageHeader=\"Volcanoes\" -->\n\n## Volcanoes\n\n### The Infrared Glows of Kilauea's Lava Flows�Hawaii\n\nIn early May 2018, an eruption on Hawaii's Kilauea volcano began to unfold. The eruption took a dangerous turn on May 3, 2018, when new fissures opened in the residential neighborhood of Leilani Estates. During the summer-long eruptive event, other fissures emerged along the East Rift Zone. Lava from vents along the rift zone flowed downslope, reaching the ocean in several areas, and filling in Kapoho Bay.\n\nA time series of Landsat 8 imagery shows the progression of the lava flows from May 16 to August 13. The night view combines thermal, shortwave infrared, and near-infrared wavelengths to tease out the very hot lava (bright white), cooling lava (red), and lava flows obstructed by clouds (purple).\n\n#### Figure: Location of Kilauea Volcano, Hawaii\n\nA globe is shown centered on North America, with a marker placed in the Pacific Ocean indicating the location of Hawaii, to the southwest of the mainland United States.\n\n<!-- PageFooter=\"Earth at Night\" -->\n<!-- PageNumber=\"44\" -->"
  }
}
[{"ref_id":0,"content":"## Nature's Light Shows\n\nAt night, with the light of the Sun removed, nature's brilliant glow from Earth's surface becomes visible to the naked eye from space. Some of Earth's most spectacular light shows are natural, like the aurora borealis, or Northern Lights, in the Northern Hemisphere (aurora australis, or Southern Lights, in the Southern Hemisphere). The auroras are natural electrical phenomena caused by charged particles that race from the Sun toward Earth, inducing chemical reactions in the upper atmosphere and creating the appearance of streamers of reddish or greenish light in the sky, usually near the northern or southern magnetic pole. Other natural lights can indicate danger, like a raging forest fire encroaching on a city, town, or community, or lava spewing from an erupting volcano.\n\nWhatever the source, the ability of humans to monitor nature's light shows at night has practical applications for society. For example, tracking fires during nighttime hours allows for continuous monitoring and enhances our ability to protect humans and other animals, plants, and infrastructure. Combined with other data sources, our ability to observe the light of fires at night allows emergency managers to more efficiently and accurately issue warnings and evacuation orders and allows firefighting efforts to continue through the night. With enough moonlight (e.g., full-Moon phase), it's even possible to track the movement of smoke plumes at night, which can impact air quality, regardless of time of day.\n\nAnother natural source of light at night is emitted from glowing lava flows at the site of active volcanoes. Again, with enough moonlight, these dramatic scenes can be tracked and monitored for both scientific research and public safety.\n\n\n### Figure: The Northern Lights Viewed from Space\n\n**September 17, 2011**\n\nThis photo, taken from the International Space Station on September 17, 2011, shows a spectacular display of the aurora borealis (Northern Lights) as green and reddish light in the night sky above Earth. In the foreground, part of a Soyuz spacecraft is visible, silhouetted against the bright auroral light. The green glow is generated by energetic charged particles from the Sun interacting with Earth's upper atmosphere, exciting oxygen and nitrogen atoms, and producing characteristic colors. The image demonstrates the vividness and grandeur of natural night-time light phenomena as seen from orbit."},{"ref_id":1,"content":"# Volcanoes\n\n## Figure: Satellite Image of Sicily and Mount Etna Lava, March 16, 2017\n\nThe annotated satellite image below shows the island of Sicily and the surrounding region at night, highlighting city lights and volcanic activity.\n\n**Description:**\n\n- **Date of image:** March 16, 2017\n- **Geographical locations labeled:**\n    - Major cities: Palermo (northwest Sicily), Marsala (western Sicily), Catania (eastern Sicily)\n    - Significant feature: Mount Etna, labeled with an adjacent \"hot lava\" region showing the glow from active lava flows\n    - Surrounding water body: Mediterranean Sea\n    - Island: Malta to the south of Sicily\n- **Other details:** \n    - The image is shown at night, with bright spots indicating city lights.\n    - The position of \"hot lava\" near Mount Etna is distinctly visible as a bright spot different from other city lights, indicating volcanic activity.\n    - A scale bar is included showing a reference length of 50 km.\n    - North direction is indicated with an arrow.\n    - Cloud cover is visible in the southwest part of the image, partially obscuring the view near Marsala and Malta.\n\n**Summary of Features Visualized:**\n\n| Feature          | Description                                           |\n|------------------|------------------------------------------------------|\n| Cities           | Bright clusters indicating locations: Palermo, Marsala, Catania |\n| Mount Etna       | Marked on the map, located on the eastern side of Sicily, with visible hot lava activity |\n| Malta            | Clearly visible to the south of Sicily               |\n| Water bodies     | Mediterranean Sea labeled                            |\n| Scale & Direction| 50 km scale bar and North indicator                  |\n| Date             | March 16, 2017                                       |\n| Cloud Cover      | Visible in the lower left (southern) part of the image |\n\nThis figure demonstrates the visibility of volcanic activity at Mount Etna from space at night, distinguishing the light from hot lava against the background city lights of Sicily and Malta."},{"ref_id":2,"content":"<!-- PageHeader=\"Volcanoes\" -->\n\n### Nighttime Glow at Mount Etna - Italy\n\nAt about 2:30 a.m. local time on March 16, 2017, the VIIRS DNB on the Suomi NPP satellite captured this nighttime image of lava flowing on Mount Etna in Sicily, Italy. Etna is one of the world's most active volcanoes.\n\n#### Figure: Location of Mount Etna\nA world globe is depicted, with a marker indicating the location of Mount Etna in Sicily, Italy, in southern Europe near the center of the Mediterranean Sea.\n\n<!-- PageFooter=\"Earth at Night\" -->\n<!-- PageNumber=\"48\" -->"},{"ref_id":3,"content":"# Volcanoes\n\n---\n\n### Mount Etna Erupts - Italy\n\nThe highly active Mount Etna in Italy sent red lava rolling down its flank on March 19, 2017. An astronaut onboard the ISS took the photograph below of the volcano and its environs that night. City lights surround the mostly dark volcanic area.\n\n---\n\n#### Figure 1: Location of Mount Etna, Italy\n\nA world map highlighting the location of Mount Etna in southern Italy. The marker indicates its geographic placement on the east coast of Sicily, Italy, in the Mediterranean region, south of mainland Europe and north of northern Africa.\n\n---\n\n#### Figure 2: Nighttime View of Mount Etna's Eruption and Surrounding Cities\n\nThis is a nighttime satellite image taken on March 19, 2017, showing the eruption of Mount Etna (southeastern cone) with visible bright red and orange coloring indicating flowing lava from a lateral vent. The surrounding areas are illuminated by city lights, with the following geographic references labeled:\n\n| Location        | Position in Image         | Visible Characteristics                    |\n|-----------------|--------------------------|--------------------------------------------|\n| Mt. Etna (southeastern cone) | Top center-left | Bright red/orange lava flow                |\n| Lateral vent    | Left of the volcano       | Faint red/orange flow extending outwards   |\n| Resort          | Below the volcano, to the left   | Small cluster of lights                    |\n| Giarre          | Top right                 | Bright cluster of city lights              |\n| Acireale        | Center right              | Large, bright area of city lights          |\n| Biancavilla     | Bottom left               | Smaller cluster of city lights             |\n\nAn arrow pointing north is shown on the image for orientation.\n\n---\n\n<!-- Earth at Night Page Footer -->\n<!-- Page Number: 50 -->"},{"ref_id":4,"content":"For the first time in perhaps a decade, Mount Etna experienced a \"flank eruption\"�erupting from its side instead of its summit�on December 24, 2018. The activity was accompanied by 130 earthquakes occurring over three hours that morning. Mount Etna, Europe�s most active volcano, has seen periodic activity on this part of the mountain since 2013. The Operational Land Imager (OLI) on the Landsat 8 satellite acquired the main image of Mount Etna on December 28, 2018.\n\nThe inset image highlights the active vent and thermal infrared signature from lava flows, which can be seen near the newly formed fissure on the southeastern side of the volcano. The inset was created with data from OLI and the Thermal Infrared Sensor (TIRS) on Landsat 8. Ash spewing from the fissure cloaked adjacent villages and delayed aircraft from landing at the nearby Catania airport. Earthquakes occurred in the subsequent days after the initial eruption and displaced hundreds of people from their homes.\n\nFor nighttime images of Mount Etna�s March 2017 eruption, see pages 48�51.\n\n---\n\n### Hazards of Volcanic Ash Plumes and Satellite Observation\n\nWith the help of moonlight, satellite instruments can track volcanic ash plumes, which present significant hazards to airplanes in flight. The volcanic ash�composed of tiny pieces of glass and rock�is abrasive to engine turbine blades, and can melt on the blades and other engine parts, causing damage and even engine stalls. This poses a danger to both the plane�s integrity and passenger safety. Volcanic ash also reduces visibility for pilots and can cause etching of windshields, further reducing pilots� ability to see. Nightlight images can be combined with thermal images to provide a more complete view of volcanic activity on Earth�s surface.\n\nThe VIIRS Day/Night Band (DNB) on polar-orbiting satellites uses faint light sources such as moonlight, airglow (the atmosphere�s self-illumination through chemical reactions), zodiacal light (sunlight scattered by interplanetary dust), and starlight from the Milky Way. Using these dim light sources, the DNB can detect changes in clouds, snow cover, and sea ice:\n\n#### Table: Light Sources Used by VIIRS DNB\n\n| Light Source         | Description                                                                  |\n|----------------------|------------------------------------------------------------------------------|\n| Moonlight            | Reflected sunlight from the Moon, illuminating Earth's surface at night      |\n| Airglow              | Atmospheric self-illumination from chemical reactions                        |\n| Zodiacal Light       | Sunlight scattered by interplanetary dust                                    |\n| Starlight/Milky Way  | Faint illumination provided by stars in the Milky Way                        |\n\nGeostationary Operational Environmental Satellites (GOES), managed by NOAA, orbit over Earth�s equator and offer uninterrupted observations of North America. High-latitude areas such as Alaska benefit from polar-orbiting satellites like Suomi NPP, which provide overlapping coverage at the poles, enabling more data collection in these regions. During polar darkness (winter months), VIIRS DNB data allow scientists to:\n\n- Observe sea ice formation\n- Monitor snow cover extent at the highest latitudes\n- Detect open water for ship navigation\n\n#### Table: Satellite Coverage Overview\n\n| Satellite Type          | Orbit           | Coverage Area         | Special Utility                              |\n|------------------------|-----------------|----------------------|----------------------------------------------|\n| GOES                   | Geostationary   | Equatorial/North America | Continuous regional monitoring              |\n| Polar-Orbiting (e.g., Suomi NPP) | Polar-orbiting    | Poles/high latitudes      | Overlapping passes; useful during polar night|\n\n---\n\n### Weather Forecasting and Nightlight Data\n\nThe use of nightlight data by weather forecasters is growing as the VIIRS instrument enables observation of clouds at night illuminated by sources such as moonlight and lightning. Scientists use these data to study the nighttime behavior of weather systems, including severe storms, which can develop and strike populous areas at night as well as during the day. Combined with thermal data, visible nightlight data allow the detection of clouds at various heights in the atmosphere, such as dense marine fog. This capability enables weather forecasters to issue marine advisories with higher confidence, leading to greater utility. (See \"Marine Layer Clouds�California\" on page 56.)\n\nIn this section of the book, you will see how nightlight data are used to observe nature�s spectacular light shows across a wide range of sources.\n\n---\n\n#### Notable Data from Mount Etna Flank Eruption (December 2018)\n\n| Event/Observation                  | Details                                                                    |\n|-------------------------------------|----------------------------------------------------------------------------|\n| Date of Flank Eruption              | December 24, 2018                                                          |\n| Number of Earthquakes               | 130 earthquakes within 3 hours                                              |\n| Image Acquisition                   | December 28, 2018 by Landsat 8 OLI                                         |\n| Location of Eruption                | Southeastern side of Mount Etna                                            |\n| Thermal Imaging Data                | From OLI and TIRS (Landsat 8), highlighting active vent and lava flows     |\n| Impact on Villages/Air Transport    | Ash covered villages; delayed aircraft at Catania airport                  |\n| Displacement                        | Hundreds of residents displaced                                            |\n| Ongoing Seismic Activity            | Earthquakes continued after initial eruption                               |\n\n---\n\n<!-- PageFooter=\"Earth at Night\" -->\n<!-- PageNumber=\"30\" -->"},{"ref_id":5,"content":"<!-- PageHeader=\"Volcanoes\" -->\n\n## Volcanoes\n\n### The Infrared Glows of Kilauea's Lava Flows�Hawaii\n\nIn early May 2018, an eruption on Hawaii's Kilauea volcano began to unfold. The eruption took a dangerous turn on May 3, 2018, when new fissures opened in the residential neighborhood of Leilani Estates. During the summer-long eruptive event, other fissures emerged along the East Rift Zone. Lava from vents along the rift zone flowed downslope, reaching the ocean in several areas, and filling in Kapoho Bay.\n\nA time series of Landsat 8 imagery shows the progression of the lava flows from May 16 to August 13. The night view combines thermal, shortwave infrared, and near-infrared wavelengths to tease out the very hot lava (bright white), cooling lava (red), and lava flows obstructed by clouds (purple).\n\n#### Figure: Location of Kilauea Volcano, Hawaii\n\nA globe is shown centered on North America, with a marker placed in the Pacific Ocean indicating the location of Hawaii, to the southwest of the mainland United States.\n\n<!-- PageFooter=\"Earth at Night\" -->\n<!-- PageNumber=\"44\" -->"}]

[ASSISTANT]: 
To find lava at night, you can look for the visible glow of active lava flows from erupting volcanoes, which emit light detectable from space during nighttime
 For example:

- The active lava flows of Mount Etna in Sicily, Italy, have been clearly observed at night by satellites and astronauts aboard the International Space Station
 The bright red and orange glow of lava distinguishes it from surrounding city lights (refs 1, 3)


- Similarly, the Kilauea volcano in Hawaii emits an infrared glow from its lava flows, which can be captured in nighttime satellite imagery combining thermal and near-infrared wavelengths (ref 5)


- Nighttime satellite instruments like the VIIRS Day/Night Band (DNB) on the Suomi NPP satellite use faint light sources such as moonlight to detect the glow of lava and volcanic activity even when direct sunlight is absent (refs 2, 4)


Therefore, to find lava at night, monitoring nighttime satellite imagery over active volcanic regions is effective, as the glowing lava stands out distinctly against the dark landscape and city lights


References: [1], [2], [3], [4], [5]

 === Conversation Complete ===
[DELETE] Deleting knowledge agent...
[DONE] Knowledge agent 'earth-search-agent' deleted successfully.
[DELETE] Deleting search index...
[DONE] Search index 'earth_at_night' deleted successfully.
[DONE] Quickstart completed successfully!
```

## Understand the code

Now that you have the code, let's break down the key components:

- [Create a search index](#create-a-search-index)
- [Upload documents to the index](#upload-documents-to-the-index)
- [Create a knowledge agent](#create-a-knowledge-agent)
- [Set up messages](#set-up-messages)
- [Run the retrieval pipeline](#run-the-retrieval-pipeline)
- [Review the response, activity, and results](#review-the-response-activity-and-results)
- [Create the Azure OpenAI client](#create-the-azure-openai-client)
- [Use the Chat Completions API to generate an answer](#use-the-chat-completions-api-to-generate-an-answer)
- [Continue the conversation](#continue-the-conversation)

### Create a search index

In Azure AI Search, an index is a structured collection of data. The following code defines an index named `earth_at_night` to contain plain text and vector content. You can use an existing index, but it must meet the criteria for [agentic retrieval workloads](../../agentic-retrieval-how-to-create-index.md). 

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

The index schema contains fields for document identification and page content, embeddings, and numbers. It also includes configurations for semantic ranking and vector queries, which use the `text-embedding-3-large` model you previously deployed.

### Upload documents to the index

Currently, the `earth_at_night` index is empty. Run the following code to populate the index with JSON documents from [NASA's Earth at Night e-book](https://raw.githubusercontent.com/Azure-Samples/azure-search-sample-data/refs/heads/main/nasa-e-book/earth-at-night-json/documents.json). As required by Azure AI Search, each document conforms to the fields and data types defined in the index schema.

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

### Create a knowledge agent

To connect Azure AI Search to your `gpt-5-mini` deployment and target the `earth_at_night` index at query time, you need a knowledge agent. The following code defines a knowledge agent named `earth-search-agent` that uses the agent definition to process queries and retrieve relevant documents from the `earth_at_night` index.

To ensure relevant and semantically meaningful responses, `defaultRerankerThreshold` is set to exclude responses with a reranker score of `2.5` or lower.

```java
ObjectMapper mapper = new ObjectMapper();
ObjectNode agentDefinition = mapper.createObjectNode();
agentDefinition.put("name", AGENT_NAME);
agentDefinition.put("description", "Knowledge agent for Earth at Night e-book content");

ObjectNode model = mapper.createObjectNode();
model.put("kind", "azureOpenAI");
ObjectNode azureOpenAIParams = mapper.createObjectNode();
azureOpenAIParams.put("resourceUri", AZURE_OPENAI_ENDPOINT);
azureOpenAIParams.put("deploymentId", AZURE_OPENAI_GPT_DEPLOYMENT);
azureOpenAIParams.put("modelName", AZURE_OPENAI_GPT_MODEL);
model.set("azureOpenAIParameters", azureOpenAIParams);
agentDefinition.set("models", mapper.createArrayNode().add(model));

ObjectNode targetIndex = mapper.createObjectNode();
targetIndex.put("indexName", INDEX_NAME);
targetIndex.put("defaultRerankerThreshold", 2.5);
agentDefinition.set("targetIndexes", mapper.createArrayNode().add(targetIndex));

String token = getAccessToken(credential, "https://search.azure.com/.default");

java.net.http.HttpClient httpClient = java.net.http.HttpClient.newHttpClient();
java.net.http.HttpRequest request = java.net.http.HttpRequest.newBuilder()
    .uri(URI.create(SEARCH_ENDPOINT + "/agents/" + AGENT_NAME + "?api-version=" + SEARCH_API_VERSION))
    .header("Content-Type", "application/json")
    .header("Authorization", "Bearer " + token)
    .PUT(java.net.http.HttpRequest.BodyPublishers.ofString(mapper.writeValueAsString(agentDefinition)))
    .build();

java.net.http.HttpResponse<String> response = httpClient.send(request,
    java.net.http.HttpResponse.BodyHandlers.ofString());
```

### Set up messages

Messages are the input for the retrieval route and contain the conversation history. Each message includes a role that indicates its origin, such as assistant or user, and content in natural language. The LLM you use determines which roles are valid.

A user message represents the query to be processed, while an assistant message guides the knowledge agent on how to respond. During the retrieval process, these messages are sent to an LLM to extract relevant responses from indexed documents.

This assistant message instructs `earth-search-agent` to answer questions about the Earth at night, cite sources using their `ref_id`, and respond with "I don't know" when answers are unavailable.

```java
List<Map<String, String>> messages = new ArrayList<>();

Map<String, String> systemMessage = new HashMap<>();
systemMessage.put("role", "system");
systemMessage.put("content", "A Q&A agent that can answer questions about the Earth at night.\n" +
    "Sources have a JSON format with a ref_id that must be cited in the answer.\n" +
    "If you do not have the answer, respond with \"I don't know\".");
messages.add(systemMessage);

Map<String, String> userMessage = new HashMap<>();
userMessage.put("role", "user");
userMessage.put("content", "Why do suburban belts display larger December brightening than urban cores even though absolute light levels are higher downtown? Why is the Phoenix nighttime street grid is so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?");
messages.add(userMessage);
```

### Run the retrieval pipeline

This step runs the retrieval pipeline to extract relevant information from your search index. Based on the messages and parameters on the retrieval request, the LLM:
1. Analyzes the entire conversation history to determine the underlying information need.
1. Breaks down the compound user query into focused subqueries.
1. Runs each subquery simultaneously against text fields and vector embeddings in your index.
1. Uses semantic ranker to rerank the results of all subqueries.
1. Merges the results into a single string.

The following code sends a two-part user query to `earth-search-agent`, which deconstructs the query into subqueries, runs the subqueries against both text fields and vector embeddings in the `earth_at_night` index, and ranks and merges the results. The response is then appended to the `messages` list.

```java
ObjectMapper mapper = new ObjectMapper();
ObjectNode retrievalRequest = mapper.createObjectNode();

// Convert messages to the correct format expected by the Knowledge agent
com.fasterxml.jackson.databind.node.ArrayNode agentMessages = mapper.createArrayNode();
for (Map<String, String> msg : messages) {
    ObjectNode agentMessage = mapper.createObjectNode();
    agentMessage.put("role", msg.get("role"));
    
    com.fasterxml.jackson.databind.node.ArrayNode content = mapper.createArrayNode();
    ObjectNode textContent = mapper.createObjectNode();
    textContent.put("type", "text");
    textContent.put("text", msg.get("content"));
    content.add(textContent);
    agentMessage.set("content", content);
    
    agentMessages.add(agentMessage);
}
retrievalRequest.set("messages", agentMessages);

com.fasterxml.jackson.databind.node.ArrayNode targetIndexParams = mapper.createArrayNode();
ObjectNode indexParam = mapper.createObjectNode();
indexParam.put("indexName", INDEX_NAME);
indexParam.put("rerankerThreshold", 2.5);
indexParam.put("maxDocsForReranker", 100);
indexParam.put("includeReferenceSourceData", true);
targetIndexParams.add(indexParam);
retrievalRequest.set("targetIndexParams", targetIndexParams);

String token = getAccessToken(credential, "https://search.azure.com/.default");

java.net.http.HttpClient httpClient = java.net.http.HttpClient.newHttpClient();
java.net.http.HttpRequest request = java.net.http.HttpRequest.newBuilder()
    .uri(URI.create(SEARCH_ENDPOINT + "/agents/" + AGENT_NAME + "/retrieve?api-version=" + SEARCH_API_VERSION))
    .header("Content-Type", "application/json")
    .header("Authorization", "Bearer " + token)
    .POST(java.net.http.HttpRequest.BodyPublishers.ofString(mapper.writeValueAsString(retrievalRequest)))
    .build();

java.net.http.HttpResponse<String> response = httpClient.send(request,
    java.net.http.HttpResponse.BodyHandlers.ofString());
```

### Review the response, activity, and results

Now you want to display the response, activity, and results of the retrieval pipeline.

Each retrieval response from Azure AI Search includes:

+ A unified string that represents grounding data from the search results.

+ The query plan.

+ Reference data that shows which chunks of the source documents contributed to the unified string.

```java
ObjectMapper mapper = new ObjectMapper();
        
// Log activities
System.out.println("\nActivities:");
if (responseJson.has("activity") && responseJson.get("activity").isArray()) {
    for (JsonNode activity : responseJson.get("activity")) {
        String activityType = "UnknownActivityRecord";
        if (activity.has("InputTokens")) {
            activityType = "KnowledgeAgentModelQueryPlanningActivityRecord";
        } else if (activity.has("TargetIndex")) {
            activityType = "KnowledgeAgentSearchActivityRecord";
        } else if (activity.has("QueryTime")) {
            activityType = "KnowledgeAgentSemanticRankerActivityRecord";
        }
        
        System.out.println("Activity Type: " + activityType);
        try {
            System.out.println(mapper.writerWithDefaultPrettyPrinter().writeValueAsString(activity));
        } catch (Exception e) {
            System.out.println(activity.toString());
        }
    }
}

// Log results
System.out.println("Results");
if (responseJson.has("references") && responseJson.get("references").isArray()) {
    for (JsonNode reference : responseJson.get("references")) {
        String referenceType = "KnowledgeAgentAzureSearchDocReference";
        
        System.out.println("Reference Type: " + referenceType);
        try {
            System.out.println(mapper.writerWithDefaultPrettyPrinter().writeValueAsString(reference));
        } catch (Exception e) {
            System.out.println(reference.toString());
        }
    }
}
```

The output should include:

+ `Response` provides a text string of the most relevant documents (or chunks) in the search index based on the user query. As shown later in this quickstart, you can pass this string to an LLM for answer generation.

+ `Activity` tracks the steps that were taken during the retrieval process, including the subqueries generated by your `gpt-5-mini` deployment and the tokens used for query planning and execution.

+ `Results` lists the documents that contributed to the response, each one identified by their `DocKey`.

### Create the Azure OpenAI client

To extend the retrieval pipeline from answer *extraction* to answer *generation*, set up the Azure OpenAI client to interact with your `gpt-5-mini` deployment.

```java
OpenAIAsyncClient openAIClient = new OpenAIClientBuilder()
    .endpoint(AZURE_OPENAI_ENDPOINT)
    .credential(credential)
    .buildAsyncClient();
```

### Use the Chat Completions API to generate an answer

One option for answer generation is the Chat Completions API, which passes the conversation history to the LLM for processing.

```java
List<ChatRequestMessage> chatMessages = new ArrayList<>();
for (Map<String, String> msg : messages) {
    String role = msg.get("role");
    String content = msg.get("content");
    
    switch (role) {
        case "system":
            chatMessages.add(new ChatRequestSystemMessage(content));
            break;
        case "user":
            chatMessages.add(new ChatRequestUserMessage(content));
            break;
        case "assistant":
            chatMessages.add(new ChatRequestAssistantMessage(content));
            break;
    }
}

ChatCompletionsOptions chatOptions = new ChatCompletionsOptions(chatMessages)
    .setMaxTokens(1000)
    .setTemperature(0.7);

ChatCompletions completion = openAIClient.getChatCompletions(AZURE_OPENAI_GPT_DEPLOYMENT, chatOptions).block();
```

### Continue the conversation

Continue the conversation by sending another user query to `earth-search-agent`. The following code reruns the retrieval pipeline, fetching relevant content from the `earth_at_night` index and appending the response to the `messages` list. However, unlike before, you can now use the Azure OpenAI client to generate an answer based on the retrieved content.

```java
String followUpQuestion = "How do I find lava at night?";
System.out.println("[QUESTION] Follow-up question: " + followUpQuestion);

Map<String, String> userMessage = new HashMap<>();
userMessage.put("role", "user");
userMessage.put("content", followUpQuestion);
messages.add(userMessage);
```

## Clean up resources

[!INCLUDE [clean up resources (paid)](../resource-cleanup-paid.md)]

You can also run the following code to delete the objects you created in this quickstart.

### Delete the knowledge agent

The knowledge agent created in this quickstart was deleted using the following code snippet:

```java
String token = getAccessToken(credential, "https://search.azure.com/.default");
            
java.net.http.HttpClient httpClient = java.net.http.HttpClient.newHttpClient();
java.net.http.HttpRequest request = java.net.http.HttpRequest.newBuilder()
    .uri(URI.create(SEARCH_ENDPOINT + "/agents/" + AGENT_NAME + "?api-version=" + SEARCH_API_VERSION))
    .header("Authorization", "Bearer " + token)
    .DELETE()
    .build();

java.net.http.HttpResponse<String> response = httpClient.send(request,
    java.net.http.HttpResponse.BodyHandlers.ofString());
```

### Delete the search index

The search index created in this quickstart was deleted using the following code snippet:

```java
indexClient.deleteIndex(INDEX_NAME);
System.out.println("[DONE] Search index '" + INDEX_NAME + "' deleted successfully.");
```
