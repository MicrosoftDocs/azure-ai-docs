---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 01/14/2026
ms.custom: dev-focus
ai-usage: ai-assisted
---

[!INCLUDE [Feature preview](../previews/preview-generic.md)]

In this quickstart, you use [agentic retrieval](../../agentic-retrieval-overview.md) to create a conversational search experience powered by documents indexed in Azure AI Search and a large language model (LLM) from Azure OpenAI in Foundry Models.

A *knowledge base* orchestrates agentic retrieval by decomposing complex queries into subqueries, running the subqueries against one or more *knowledge sources*, and returning results with metadata. By default, the knowledge base outputs raw content from your sources, but this quickstart uses the answer synthesis output mode for natural-language answer generation.

Although you can provide your own data, this quickstart uses [sample JSON documents](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/nasa-e-book/earth-at-night-json) from NASA's Earth at Night e-book. The documents describe general science topics and images of Earth at night as observed from space.

> [!TIP]
> Want to get started right away? See the [azure-search-dotnet-samples](https://github.com/Azure-Samples/azure-search-dotnet-samples/tree/main/quickstart-agentic-retrieval) GitHub repository.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](../../search-create-service-portal.md) in any [region that provides agentic retrieval](../../search-region-support.md).

+ A [Microsoft Foundry project](/azure/ai-foundry/how-to/create-projects) and resource. When you create a project, the resource is automatically created.

+ The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

+ [Visual Studio Code](https://code.visualstudio.com/download).

[!INCLUDE [Setup](./agentic-retrieval-setup.md)]

## Set up the environment

To set up the console application for this quickstart:

1. Create a folder named `quickstart-agentic-retrieval` to contain the application.

1. Open the folder in Visual Studio Code.

1. Select **Terminal** > **New Terminal**, and then run the following command to create a console application.

    ```console
    dotnet new console
    ```

1. Install the [Azure AI Search client library for .NET](/dotnet/api/overview/azure/search.documents-readme).

    ```console
    dotnet add package Azure.Search.Documents --version 11.8.0-beta.1
    ```

1. Install the `dotenv.net` package to load environment variables from a `.env` file.

    ```console
    dotnet add package dotenv.net
    ```

1. For keyless authentication with Microsoft Entra ID, install the [Azure.Identity](https://www.nuget.org/packages/Azure.Identity) package.

    ```console
    dotnet add package Azure.Identity
    ```

1. For keyless authentication with Microsoft Entra ID, sign in to your Azure account. If you have multiple subscriptions, select the one that contains your Azure AI Search service and Microsoft Foundry project.

    ```console
    az login
    ```

## Run the code

To create and run the agentic retrieval pipeline:

1. Create a file named `.env` in the `quickstart-agentic-retrieval` folder.

1. Paste the following environment variables into the `.env` file.

    ```
    SEARCH_ENDPOINT = PUT-YOUR-SEARCH-SERVICE-URL-HERE
    AOAI_ENDPOINT = PUT-YOUR-AOAI-FOUNDRY-URL-HERE
    ```

1. Set `SEARCH_ENDPOINT` and `AOAI_ENDPOINT` to the values you obtained in [Get endpoints](#get-endpoints).

1. Paste the following code into the `Program.cs` file.

    ```csharp
    using dotenv.net;
    using System.Text.Json;
    using Azure.Identity;
    using Azure.Search.Documents;
    using Azure.Search.Documents.Indexes;
    using Azure.Search.Documents.Indexes.Models;
    using Azure.Search.Documents.KnowledgeBases;
    using Azure.Search.Documents.KnowledgeBases.Models;
    
    namespace AzureSearch.Quickstart
    {
        class Program
        {
            static async Task Main(string[] args)
            {
                // Load environment variables from the .env file
                // Ensure your .env file is in the same directory with the required variables
                DotEnv.Load();
    
                string searchEndpoint = Environment.GetEnvironmentVariable("SEARCH_ENDPOINT")
                    ?? throw new InvalidOperationException("SEARCH_ENDPOINT isn't set.");
                string aoaiEndpoint = Environment.GetEnvironmentVariable("AOAI_ENDPOINT")
                    ?? throw new InvalidOperationException("AOAI_ENDPOINT isn't set.");
    
                string aoaiEmbeddingModel = "text-embedding-3-large";
                string aoaiEmbeddingDeployment = "text-embedding-3-large";
                string aoaiGptModel = "gpt-5-mini";
                string aoaiGptDeployment = "gpt-5-mini";
    
                string indexName = "earth-at-night";
                string knowledgeSourceName = "earth-knowledge-source";
                string knowledgeBaseName = "earth-knowledge-base";
    
                var credential = new DefaultAzureCredential();
    
                // Define fields for the index
                var fields = new List<SearchField>
                {
                    new SimpleField("id", SearchFieldDataType.String) { IsKey = true, IsFilterable = true, IsSortable = true, IsFacetable = true },
                    new SearchField("page_chunk", SearchFieldDataType.String) { IsFilterable = false, IsSortable = false, IsFacetable = false },
                    new SearchField("page_embedding_text_3_large", SearchFieldDataType.Collection(SearchFieldDataType.Single)) { VectorSearchDimensions = 3072, VectorSearchProfileName = "hnsw_text_3_large" },
                    new SimpleField("page_number", SearchFieldDataType.Int32) { IsFilterable = true, IsSortable = true, IsFacetable = true }
                };
    
                // Define a vectorizer
                var vectorizer = new AzureOpenAIVectorizer(vectorizerName: "azure_openai_text_3_large")
                {
                    Parameters = new AzureOpenAIVectorizerParameters
                    {
                        ResourceUri = new Uri(aoaiEndpoint),
                        DeploymentName = aoaiEmbeddingDeployment,
                        ModelName = aoaiEmbeddingModel
                    }
                };
    
                // Define a vector search profile and algorithm
                var vectorSearch = new VectorSearch()
                {
                    Profiles =
                    {
                        new VectorSearchProfile(
                            name: "hnsw_text_3_large",
                            algorithmConfigurationName: "alg"
                        )
                        {
                            VectorizerName = "azure_openai_text_3_large"
                        }
                    },
                    Algorithms =
                    {
                        new HnswAlgorithmConfiguration(name: "alg")
                    },
                    Vectorizers =
                    {
                        vectorizer
                    }
                };
    
                // Define a semantic configuration
                var semanticConfig = new SemanticConfiguration(
                    name: "semantic_config",
                    prioritizedFields: new SemanticPrioritizedFields
                    {
                        ContentFields = { new SemanticField("page_chunk") }
                    }
                );
    
                var semanticSearch = new SemanticSearch()
                {
                    DefaultConfigurationName = "semantic_config",
                    Configurations = { semanticConfig }
                };
    
                // Create the index
                var index = new SearchIndex(indexName)
                {
                    Fields = fields,
                    VectorSearch = vectorSearch,
                    SemanticSearch = semanticSearch
                };
    
                // Create the index client, deleting and recreating the index if it exists
                var indexClient = new SearchIndexClient(new Uri(searchEndpoint), credential);
                await indexClient.CreateOrUpdateIndexAsync(index);
                Console.WriteLine($"Index '{indexName}' created or updated successfully.");
    
                // Upload sample documents from the GitHub URL
                string url = "https://raw.githubusercontent.com/Azure-Samples/azure-search-sample-data/refs/heads/main/nasa-e-book/earth-at-night-json/documents.json";
                var httpClient = new HttpClient();
                var response = await httpClient.GetAsync(url);
                response.EnsureSuccessStatusCode();
                var json = await response.Content.ReadAsStringAsync();
                var documents = JsonSerializer.Deserialize<List<Dictionary<string, object>>>(json);
                var searchClient = new SearchClient(new Uri(searchEndpoint), indexName, credential);
                var searchIndexingBufferedSender = new SearchIndexingBufferedSender<Dictionary<string, object>>(
                    searchClient,
                    new SearchIndexingBufferedSenderOptions<Dictionary<string, object>>
                    {
                        KeyFieldAccessor = doc => doc["id"].ToString(),
                    }
                );

                await searchIndexingBufferedSender.UploadDocumentsAsync(documents);
                await searchIndexingBufferedSender.FlushAsync();
                Console.WriteLine($"Documents uploaded to index '{indexName}' successfully.");
    
                // Create a knowledge source
                var indexKnowledgeSource = new SearchIndexKnowledgeSource(
                    name: knowledgeSourceName,
                    searchIndexParameters: new SearchIndexKnowledgeSourceParameters(searchIndexName: indexName)
                    {
                        SourceDataFields = { new SearchIndexFieldReference(name: "id"), new SearchIndexFieldReference(name: "page_chunk"), new SearchIndexFieldReference(name: "page_number") }
                    }
                );
    
                await indexClient.CreateOrUpdateKnowledgeSourceAsync(indexKnowledgeSource);
                Console.WriteLine($"Knowledge source '{knowledgeSourceName}' created or updated successfully.");
    
                // Create a knowledge base
                var openAiParameters = new AzureOpenAIVectorizerParameters
                {
                    ResourceUri = new Uri(aoaiEndpoint),
                    DeploymentName = aoaiGptDeployment,
                    ModelName = aoaiGptModel
                };
    
                var model = new KnowledgeBaseAzureOpenAIModel(azureOpenAIParameters: openAiParameters);
    
                var knowledgeBase = new KnowledgeBase(
                    name: knowledgeBaseName,
                    knowledgeSources: new KnowledgeSourceReference[] { new KnowledgeSourceReference(knowledgeSourceName) }
                )
                {
                    RetrievalReasoningEffort = new KnowledgeRetrievalLowReasoningEffort(),
                    AnswerInstructions = "Provide a two sentence concise and informative answer based on the retrieved documents.",
                    Models = { model }
                };
    
                await indexClient.CreateOrUpdateKnowledgeBaseAsync(knowledgeBase);
                Console.WriteLine($"Knowledge base '{knowledgeBaseName}' created or updated successfully.");
    
                // Set up messages
                string instructions = @"A Q&A agent that can answer questions about the Earth at night.
                If you don't have the answer, respond with ""I don't know"".";

                var messages = new List<Dictionary<string, string>>
                {
                    new Dictionary<string, string>
                    {
                        { "role", "system" },
                        { "content", instructions }
                    }
                };
    
                // Run agentic retrieval
                var baseClient = new KnowledgeBaseRetrievalClient(
                    endpoint: new Uri(searchEndpoint),
                    knowledgeBaseName: knowledgeBaseName,
                    tokenCredential: new DefaultAzureCredential()
                );

                string query = @"Why do suburban belts display larger December brightening than urban cores even though absolute light levels are higher downtown? Why is the Phoenix nighttime street grid is so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?";

                messages.Add(new Dictionary<string, string>
                {
                    { "role", "user" },
                    { "content", query }
                });

                Console.WriteLine($"Running the query...{query}");
                var retrievalRequest = new KnowledgeBaseRetrievalRequest();
                foreach (Dictionary<string, string> message in messages) {
                    if (message["role"] != "system") {
                        retrievalRequest.Messages.Add(new KnowledgeBaseMessage(content: new[] { new KnowledgeBaseMessageTextContent(message["content"]) }) { Role = message["role"] });
                    }
                }
                retrievalRequest.RetrievalReasoningEffort = new KnowledgeRetrievalLowReasoningEffort();
                var retrievalResult = await baseClient.RetrieveAsync(retrievalRequest);
    
                messages.Add(new Dictionary<string, string>
                {
                    { "role", "assistant" },
                    { "content", (retrievalResult.Value.Response[0].Content[0] as KnowledgeBaseMessageTextContent)!.Text }
                });
    
                // Print the response, activity, and references
                Console.WriteLine("Response:");
                Console.WriteLine((retrievalResult.Value.Response[0].Content[0] as KnowledgeBaseMessageTextContent)!.Text);
    
                Console.WriteLine("Activity:");
                foreach (var activity in retrievalResult.Value.Activity)
                {
                    Console.WriteLine($"Activity Type: {activity.GetType().Name}");
                    string activityJson = JsonSerializer.Serialize(
                        activity,
                        activity.GetType(),
                        new JsonSerializerOptions { WriteIndented = true }
                    );
                    Console.WriteLine(activityJson);
                }
    
                Console.WriteLine("References:");
                foreach (var reference in retrievalResult.Value.References)
                {
                    Console.WriteLine($"Reference Type: {reference.GetType().Name}");
                    string referenceJson = JsonSerializer.Serialize(
                        reference,
                        reference.GetType(),
                        new JsonSerializerOptions { WriteIndented = true }
                    );
                    Console.WriteLine(referenceJson);
                }
    
                // Continue the conversation
                string nextQuery = "How do I find lava at night?";
                Console.WriteLine($"Continue the conversation with this query: {nextQuery}");
                messages.Add(new Dictionary<string, string>
                {
                    { "role", "user" },
                    { "content", nextQuery }
                });
    
                retrievalRequest = new KnowledgeBaseRetrievalRequest();
                foreach (Dictionary<string, string> message in messages) {
                    if (message["role"] != "system") {
                        retrievalRequest.Messages.Add(new KnowledgeBaseMessage(content: new[] { new KnowledgeBaseMessageTextContent(message["content"]) }) { Role = message["role"] });
                    }
                }
                retrievalRequest.RetrievalReasoningEffort = new KnowledgeRetrievalLowReasoningEffort();
                retrievalResult = await baseClient.RetrieveAsync(retrievalRequest);
    
                messages.Add(new Dictionary<string, string>
                {
                    { "role", "assistant" },
                    { "content", (retrievalResult.Value.Response[0].Content[0] as KnowledgeBaseMessageTextContent)!.Text }
                });
    
                // Print the new response, activity, and references
                Console.WriteLine("Response:");
                Console.WriteLine((retrievalResult.Value.Response[0].Content[0] as KnowledgeBaseMessageTextContent)!.Text);
    
                Console.WriteLine("Activity:");
                foreach (var activity in retrievalResult.Value.Activity)
                {
                    Console.WriteLine($"Activity Type: {activity.GetType().Name}");
                    string activityJson = JsonSerializer.Serialize(
                        activity,
                        activity.GetType(),
                        new JsonSerializerOptions { WriteIndented = true }
                    );
                    Console.WriteLine(activityJson);
                }
    
                Console.WriteLine("References:");
                foreach (var reference in retrievalResult.Value.References)
                {
                    Console.WriteLine($"Reference Type: {reference.GetType().Name}");
                    string referenceJson = JsonSerializer.Serialize(
                        reference,
                        reference.GetType(),
                        new JsonSerializerOptions { WriteIndented = true }
                    );
                    Console.WriteLine(referenceJson);
                }
    
                // Clean up resources
                await indexClient.DeleteKnowledgeBaseAsync(knowledgeBaseName);
                Console.WriteLine($"Knowledge base '{knowledgeBaseName}' deleted successfully.");
    
                await indexClient.DeleteKnowledgeSourceAsync(knowledgeSourceName);
                Console.WriteLine($"Knowledge source '{knowledgeSourceName}' deleted successfully.");
    
                await indexClient.DeleteIndexAsync(indexName);
                Console.WriteLine($"Index '{indexName}' deleted successfully.");
            }
        }
    }
    ```

1. Build and run the application.

    ```console
    dotnet run
    ```

### Output

The output of the application should be similar to the following:

```
Index 'earth-at-night' created or updated successfully.
Documents uploaded to index 'earth-at-night' successfully.
Knowledge source 'earth-knowledge-source' created or updated successfully.
Knowledge base 'earth-knowledge-base' created or updated successfully.
Response:
Suburban belts show larger December brightening because holiday displays concentrate in suburbs and outskirts where there is more yard space and many single‑family homes [ref_id:5], while urban cores—already having higher absolute light levels—tend to show smaller relative increases (central areas typically brighten ~20–30%) [ref_id:8][ref_id:5]. Phoenix’s nighttime street grid is sharply visible because the metropolitan area is laid out on a regular, continuously lit grid with bright commercial and industrial nodes along major corridors like Grand Avenue [ref_id:0][ref_id:3], whereas long interstate stretches between Midwestern cities cross sparsely populated or rural regions with far fewer continuous roadside lights and so appear comparatively dim [ref_id:8].
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
    "Search": "Causes of December brightening in satellite nightlights: why suburban belts show larger relative December brightening than urban cores (roles of holiday residential lighting, snow albedo, urban heat island, commercial lighting patterns)",
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
    "Search": "Why is Phoenix\u0019s nighttime street grid so sharply visible from space? (effects of streetlight density, luminaire type/aiming, spacing, urban grid layout, traffic vs roadway lighting)",
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
Activity Type: KnowledgeBaseSearchIndexActivityRecord
{
  "SearchIndexArguments": {
    "Search": "How do satellite nightlight sensor characteristics (VIIRS DNB, DMSP-OLS) \u2014 spatial resolution, dynamic range, saturation, blooming \u2014 affect observed brightness and structure of urban cores, suburbs, and long interstate stretches?",
    "Filter": null,
    "SourceDataFields": [],
    "SearchFields": [],
    "SemanticConfigurationName": null
  },
  "KnowledgeSourceName": "earth-knowledge-source",
  "QueryTime": "2025-11-05T21:56:27.786+00:00",
  "Count": 23,
  "Id": 3,
  "ElapsedMs": 604,
  "Error": null
}
Activity Type: KnowledgeBaseAgenticReasoningActivityRecord
{
  "ReasoningTokens": 70232,
  "RetrievalReasoningEffort": {},
  "Id": 4,
  "ElapsedMs": null,
  "Error": null
}
Activity Type: KnowledgeBaseModelAnswerSynthesisActivityRecord
{
  "InputTokens": 7467,
  "OutputTokens": 1710,
  "Id": 5,
  "ElapsedMs": 26663,
  "Error": null
}
Results:
Reference Type: KnowledgeBaseSearchIndexReference
{
  "DocKey": "earth_at_night_508_page_104_verbalized",
  "Id": "0",
  "ActivitySource": 2,
  "SourceData": {},
  "RerankerScore": 2.6344998
}
... // Trimmed for brevity
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

```csharp
// Define fields for the index
var fields = new List<SearchField>
{
    new SimpleField("id", SearchFieldDataType.String) { IsKey = true, IsFilterable = true, IsSortable = true, IsFacetable = true },
    new SearchField("page_chunk", SearchFieldDataType.String) { IsFilterable = false, IsSortable = false, IsFacetable = false },
    new SearchField("page_embedding_text_3_large", SearchFieldDataType.Collection(SearchFieldDataType.Single)) { VectorSearchDimensions = 3072, VectorSearchProfileName = "hnsw_text_3_large" },
    new SimpleField("page_number", SearchFieldDataType.Int32) { IsFilterable = true, IsSortable = true, IsFacetable = true }
};

// Define a vectorizer
var vectorizer = new AzureOpenAIVectorizer(vectorizerName: "azure_openai_text_3_large")
{
    Parameters = new AzureOpenAIVectorizerParameters
    {
        ResourceUri = new Uri(aoaiEndpoint),
        DeploymentName = aoaiEmbeddingDeployment,
        ModelName = aoaiEmbeddingModel
    }
};

// Define a vector search profile and algorithm
var vectorSearch = new VectorSearch()
{
    Profiles =
    {
        new VectorSearchProfile(
            name: "hnsw_text_3_large",
            algorithmConfigurationName: "alg"
        )
        {
            VectorizerName = "azure_openai_text_3_large"
        }
    },
    Algorithms =
    {
        new HnswAlgorithmConfiguration(name: "alg")
    },
    Vectorizers =
    {
        vectorizer
    }
};

// Define a semantic configuration
var semanticConfig = new SemanticConfiguration(
    name: "semantic_config",
    prioritizedFields: new SemanticPrioritizedFields
    {
        ContentFields = { new SemanticField("page_chunk") }
    }
);

var semanticSearch = new SemanticSearch()
{
    DefaultConfigurationName = "semantic_config",
    Configurations = { semanticConfig }
};

// Create the index
var index = new SearchIndex(indexName)
{
    Fields = fields,
    VectorSearch = vectorSearch,
    SemanticSearch = semanticSearch
};

// Create the index client, deleting and recreating the index if it exists
var indexClient = new SearchIndexClient(new Uri(searchEndpoint), credential);
await indexClient.CreateOrUpdateIndexAsync(index);
Console.WriteLine($"Index '{indexName}' created or updated successfully.");
```

**Reference:** [SearchField](/dotnet/api/azure.search.documents.indexes.models.searchfield), [SimpleField](/dotnet/api/azure.search.documents.indexes.models.simplefield), [VectorSearch](/dotnet/api/azure.search.documents.indexes.models.vectorsearch), [SemanticSearch](/dotnet/api/azure.search.documents.indexes.models.semanticsearch), [SearchIndex](/dotnet/api/azure.search.documents.indexes.models.searchindex), [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient)

### Upload documents to the index

Currently, the `earth-at-night` index is empty. The following code populates the index with JSON documents from [NASA's Earth at Night e-book](https://raw.githubusercontent.com/Azure-Samples/azure-search-sample-data/refs/heads/main/nasa-e-book/earth-at-night-json/documents.json). As required by Azure AI Search, each document conforms to the fields and data types defined in the index schema.

```csharp
// Upload sample documents from the GitHub URL
string url = "https://raw.githubusercontent.com/Azure-Samples/azure-search-sample-data/refs/heads/main/nasa-e-book/earth-at-night-json/documents.json";
var httpClient = new HttpClient();
var response = await httpClient.GetAsync(url);
response.EnsureSuccessStatusCode();
var json = await response.Content.ReadAsStringAsync();
var documents = JsonSerializer.Deserialize<List<Dictionary<string, object>>>(json);
var searchClient = new SearchClient(new Uri(searchEndpoint), indexName, credential);
var searchIndexingBufferedSender = new SearchIndexingBufferedSender<Dictionary<string, object>>(
    searchClient,
    new SearchIndexingBufferedSenderOptions<Dictionary<string, object>>
    {
        KeyFieldAccessor = doc => doc["id"].ToString(),
    }
);

await searchIndexingBufferedSender.UploadDocumentsAsync(documents);
await searchIndexingBufferedSender.FlushAsync();
Console.WriteLine($"Documents uploaded to index '{indexName}' successfully.");
```

**Reference:** [SearchClient](/dotnet/api/azure.search.documents.searchclient), [SearchIndexingBufferedSender](/dotnet/api/azure.search.documents.searchindexingbufferedsender-1)

### Create a knowledge source

A knowledge source is a reusable reference to source data. The following code defines a knowledge source named `earth-knowledge-source` that targets the `earth-at-night` index.

`SourceDataFields` specifies which index fields are included in citation references. This example includes only human-readable fields to avoid lengthy, uninterpretable embeddings in responses.

```csharp
// Create a knowledge source
var indexKnowledgeSource = new SearchIndexKnowledgeSource(
    name: knowledgeSourceName,
    searchIndexParameters: new SearchIndexKnowledgeSourceParameters(searchIndexName: indexName)
    {
        SourceDataFields = { new SearchIndexFieldReference(name: "id"), new SearchIndexFieldReference(name: "page_chunk"), new SearchIndexFieldReference(name: "page_number") }
    }
);

await indexClient.CreateOrUpdateKnowledgeSourceAsync(indexKnowledgeSource);
Console.WriteLine($"Knowledge source '{knowledgeSourceName}' created or updated successfully.");
```

**Reference:** [SearchIndexKnowledgeSource](/dotnet/api/azure.search.documents.indexes.models.searchindexknowledgesource)

### Create a knowledge base

To target `earth-knowledge-source` and your `gpt-5-mini` deployment at query time, you need a knowledge base. The following code defines a knowledge base named `earth-knowledge-base`.

`OutputMode` is set to `AnswerSynthesis`, enabling natural-language answers that cite the retrieved documents and follow the provided `AnswerInstructions`.

```csharp
// Create a knowledge base
var openAiParameters = new AzureOpenAIVectorizerParameters
{
    ResourceUri = new Uri(aoaiEndpoint),
    DeploymentName = aoaiGptDeployment,
    ModelName = aoaiGptModel
};

var model = new KnowledgeBaseAzureOpenAIModel(azureOpenAIParameters: openAiParameters);

var knowledgeBase = new KnowledgeBase(
    name: knowledgeBaseName,
    knowledgeSources: new KnowledgeSourceReference[] { new KnowledgeSourceReference(knowledgeSourceName) }
)
{
    RetrievalReasoningEffort = new KnowledgeRetrievalLowReasoningEffort(),
    OutputMode = KnowledgeRetrievalOutputMode.AnswerSynthesis,
    AnswerInstructions = "Provide a two sentence concise and informative answer based on the retrieved documents.",
    Models = { model }
};

await indexClient.CreateOrUpdateKnowledgeBaseAsync(knowledgeBase);
Console.WriteLine($"Knowledge base '{knowledgeBaseName}' created or updated successfully.");
```

**Reference:** [KnowledgeBaseAzureOpenAIModel](/dotnet/api/azure.search.documents.indexes.models.knowledgebaseazureopenaimodel), [KnowledgeBase](/dotnet/api/azure.search.documents.indexes.models.knowledgebase)

### Set up messages

Messages are the input for the retrieval route and contain the conversation history. Each message includes a role that indicates its origin, such as `system` or `user`, and content in natural language. The LLM you use determines which roles are valid.

The following code creates a system message, which instructs `earth-knowledge-base` to answer questions about the Earth at night and respond with "I don't know" when answers are unavailable.

```csharp
// Set up messages
string instructions = @"A Q&A agent that can answer questions about the Earth at night.
If you don't have the answer, respond with ""I don't know"".";

var messages = new List<Dictionary<string, string>>
{
    new Dictionary<string, string>
    {
        { "role", "system" },
        { "content", instructions }
    }
};
```

### Run the retrieval pipeline

You're ready to run agentic retrieval. The following code sends a two-part user query to `earth-knowledge-base`, which:

1. Analyzes the entire conversation to infer the user's information need.
1. Decomposes the compound query into focused subqueries.
1. Runs the subqueries concurrently against your knowledge source.
1. Uses semantic ranker to rerank and filter the results.
1. Synthesizes the top results into a natural-language answer.

```csharp
// Run agentic retrieval
var baseClient = new KnowledgeBaseRetrievalClient(
    endpoint: new Uri(searchEndpoint),
    knowledgeBaseName: knowledgeBaseName,
    tokenCredential: new DefaultAzureCredential()
);

messages.Add(new Dictionary<string, string>
{
    { "role", "user" },
    { "content", @"Why do suburban belts display larger December brightening than urban cores even though absolute light levels are higher downtown? Why is the Phoenix nighttime street grid is so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?" }
});

var retrievalRequest = new KnowledgeBaseRetrievalRequest();
foreach (Dictionary<string, string> message in messages) {
    if (message["role"] != "system") {
        retrievalRequest.Messages.Add(new KnowledgeBaseMessage(content: new[] { new KnowledgeBaseMessageTextContent(message["content"]) }) { Role = message["role"] });
    }
}
retrievalRequest.RetrievalReasoningEffort = new KnowledgeRetrievalLowReasoningEffort();
var retrievalResult = await baseClient.RetrieveAsync(retrievalRequest);

messages.Add(new Dictionary<string, string>
{
    { "role", "assistant" },
    { "content", (retrievalResult.Value.Response[0].Content[0] as KnowledgeBaseMessageTextContent).Text }
});
```

**Reference:** [KnowledgeBaseRetrievalClient](/dotnet/api/azure.search.documents.knowledgebases.knowledgebaseretrievalclient?view=azure-dotnet-preview&preserve-view=true), [KnowledgeBaseRetrievalRequest](/dotnet/api/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest?view=azure-dotnet-preview&preserve-view=true)

#### Review the response, activity, and references

The following code displays the response, activity, and references from the retrieval pipeline, where:

+ `Response` provides a synthesized, LLM-generated answer to the query that cites the retrieved documents. When answer synthesis isn't enabled, this section contains content extracted directly from the documents.

+ `Activity` tracks the steps that were taken during the retrieval process, including the subqueries generated by your `gpt-5-mini` deployment and the tokens used for semantic ranking, query planning, and answer synthesis.

+ `References` lists the documents that contributed to the response, each one identified by their `DocKey`.

```csharp
// Print the response, activity, and references
Console.WriteLine("Response:");
Console.WriteLine((retrievalResult.Value.Response[0].Content[0] as KnowledgeBaseMessageTextContent).Text);

Console.WriteLine("Activity:");
foreach (var activity in retrievalResult.Value.Activity)
{
    Console.WriteLine($"Activity Type: {activity.GetType().Name}");
    string activityJson = JsonSerializer.Serialize(
        activity,
        activity.GetType(),
        new JsonSerializerOptions { WriteIndented = true }
    );
    Console.WriteLine(activityJson);
}

Console.WriteLine("References:");
foreach (var reference in retrievalResult.Value.References)
{
    Console.WriteLine($"Reference Type: {reference.GetType().Name}");
    string referenceJson = JsonSerializer.Serialize(
        reference,
        reference.GetType(),
        new JsonSerializerOptions { WriteIndented = true }
    );
    Console.WriteLine(referenceJson);
}
```

### Continue the conversation

The following code continues the conversation with `earth-knowledge-base`. After you send this user query, the knowledge base fetches relevant content from `earth-knowledge-source` and appends the response to the messages list.

```csharp
// Continue the conversation
messages.Add(new Dictionary<string, string>
{
    { "role", "user" },
    { "content", "How do I find lava at night?" }
});

retrievalRequest = new KnowledgeBaseRetrievalRequest();
foreach (Dictionary<string, string> message in messages) {
    if (message["role"] != "system") {
        retrievalRequest.Messages.Add(new KnowledgeBaseMessage(content: new[] { new KnowledgeBaseMessageTextContent(message["content"]) }) { Role = message["role"] });
    }
}
retrievalRequest.RetrievalReasoningEffort = new KnowledgeRetrievalLowReasoningEffort();
retrievalResult = await baseClient.RetrieveAsync(retrievalRequest);

messages.Add(new Dictionary<string, string>
{
    { "role", "assistant" },
    { "content", (retrievalResult.Value.Response[0].Content[0] as KnowledgeBaseMessageTextContent).Text }
});
```

#### Review the new response, activity, and references

The following code displays the new response, activity, and references from the retrieval pipeline.

```csharp
// Print the new response, activity, and references
Console.WriteLine("Response:");
Console.WriteLine((retrievalResult.Value.Response[0].Content[0] as KnowledgeBaseMessageTextContent).Text);

Console.WriteLine("Activity:");
foreach (var activity in retrievalResult.Value.Activity)
{
    Console.WriteLine($"Activity Type: {activity.GetType().Name}");
    string activityJson = JsonSerializer.Serialize(
        activity,
        activity.GetType(),
        new JsonSerializerOptions { WriteIndented = true }
    );
    Console.WriteLine(activityJson);
}

Console.WriteLine("References:");
foreach (var reference in retrievalResult.Value.References)
{
    Console.WriteLine($"Reference Type: {reference.GetType().Name}");
    string referenceJson = JsonSerializer.Serialize(
        reference,
        reference.GetType(),
        new JsonSerializerOptions { WriteIndented = true }
    );
    Console.WriteLine(referenceJson);
}
```

## Clean up resources

[!INCLUDE [clean up resources (paid)](../resource-cleanup-paid.md)]

Otherwise, the following code from `Program.cs` deleted the objects you created in this quickstart.

### Delete the knowledge base

```csharp
await indexClient.DeleteKnowledgeBaseAsync(knowledgeBaseName);
Console.WriteLine($"Knowledge base '{knowledgeBaseName}' deleted successfully.");
```

### Delete the knowledge source

```csharp
await indexClient.DeleteKnowledgeSourceAsync(knowledgeSourceName);
Console.WriteLine($"Knowledge source '{knowledgeSourceName}' deleted successfully.");
```

### Delete the search index

```csharp
await indexClient.DeleteIndexAsync(indexName);
Console.WriteLine($"Index '{indexName}' deleted successfully.");     
```
