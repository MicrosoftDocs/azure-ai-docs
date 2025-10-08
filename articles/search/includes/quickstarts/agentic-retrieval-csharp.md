---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 09/23/2025
---

[!INCLUDE [Feature preview](../previews/preview-generic.md)]

In this quickstart, you use [agentic retrieval](../../agentic-retrieval-overview.md) to create a conversational search experience powered by documents indexed in Azure AI Search and large language models (LLMs) from Azure OpenAI in Azure AI Foundry Models.

A *knowledge agent* orchestrates agentic retrieval by decomposing complex queries into subqueries, running the subqueries against one or more *knowledge sources*, and returning results with metadata. By default, the agent outputs raw content from your sources, but this quickstart uses the answer synthesis modality for natural-language answer generation.

Although you can provide your own data, this quickstart uses [sample JSON documents](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/nasa-e-book/earth-at-night-json) from NASA's Earth at Night e-book. The documents describe general science topics and images of Earth at night as observed from space.

> [!TIP]
> Want to get started right away? See the [azure-search-dotnet-samples](https://github.com/Azure-Samples/azure-search-dotnet-samples/tree/main/quickstart-agentic-retrieval) repository on GitHub.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](../../search-create-service-portal.md) on the Basic tier or higher with [semantic ranker enabled](../../semantic-how-to-enable-disable.md).

+ An [Azure AI Foundry project](/azure/ai-foundry/how-to/create-projects) and Azure AI Foundry resource. When you create a project, the resource is automatically created.

+ The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

[!INCLUDE [Setup](./agentic-retrieval-setup.md)]

## Set up the environment

To set up the console application for this quickstart:

1. Create a folder named `quickstart-agentic-retrieval` to contain the application.

1. Open the folder in Visual Studio Code.

1. Select **Terminal** > **New Terminal**, and then run the following command to create a console application.

    ```powershell
    dotnet new console
    ```

1. Install the [Azure AI Search client library](/dotnet/api/overview/azure/search.documents-readme) for .NET.

    ```console
    dotnet add package Azure.Search.Documents --version 11.7.0-beta.7
    ```

1. Install the `dotenv.net` package to load environment variables from a `.env` file.

    ```console
    dotnet add package dotenv.net
    ```

1. For keyless authentication with Microsoft Entra ID, install the [Azure.Identity](https://www.nuget.org/packages/Azure.Identity) package.

    ```console
    dotnet add package Azure.Identity
    ```

1. For keyless authentication with Microsoft Entra ID, sign in to your Azure account. If you have multiple subscriptions, select the one that contains your Azure AI Search service and Azure AI Foundry project.

    ```console
    az login
    ```

## Run the code

To create and run the agentic retrieval pipeline:

1. Create a file named `.env` in the `quickstart-agentic-retrieval` folder.

1. Add the following environment variables to the `.env` file.

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
    using Azure.Search.Documents.Models;
    using Azure.Search.Documents.Agents;
    using Azure.Search.Documents.Agents.Models;
    
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
                string knowledgeAgentName = "earth-knowledge-agent";
    
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
                        SourceDataSelect = "id,page_chunk,page_number"
                    }
                );
                await indexClient.CreateOrUpdateKnowledgeSourceAsync(indexKnowledgeSource);
                Console.WriteLine($"Knowledge source '{knowledgeSourceName}' created or updated successfully.");
    
                // Create a knowledge agent
                var openAiParameters = new AzureOpenAIVectorizerParameters
                {
                    ResourceUri = new Uri(aoaiEndpoint),
                    DeploymentName = aoaiGptDeployment,
                    ModelName = aoaiGptModel
                };
    
                var agentModel = new KnowledgeAgentAzureOpenAIModel(azureOpenAIParameters: openAiParameters);
                var outputConfig = new KnowledgeAgentOutputConfiguration
                {
                    Modality = KnowledgeAgentOutputConfigurationModality.AnswerSynthesis,
                    IncludeActivity = true
                };
    
                var agent = new KnowledgeAgent(
                    name: knowledgeAgentName,
                    models: new[] { agentModel },
                    knowledgeSources: new KnowledgeSourceReference[] {
                    new KnowledgeSourceReference(knowledgeSourceName) {
                            IncludeReferences = true,
                            IncludeReferenceSourceData = true,
                            RerankerThreshold = (float?)2.5
                        }
                    }
                )
    
                {
                    OutputConfiguration = outputConfig
                };
    
                await indexClient.CreateOrUpdateKnowledgeAgentAsync(agent);
                Console.WriteLine($"Knowledge agent '{knowledgeAgentName}' created or updated successfully.");
    
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
    
                // Use agentic retrieval to fetch results
                var agentClient = new KnowledgeAgentRetrievalClient(
                    endpoint: new Uri(searchEndpoint),
                    agentName: knowledgeAgentName,
                    tokenCredential: new DefaultAzureCredential()
                );
    
                messages.Add(new Dictionary<string, string>
                {
                    { "role", "user" },
                    { "content", @"Why do suburban belts display larger December brightening than urban cores even though absolute light levels are higher downtown?
                    Why is the Phoenix nighttime street grid is so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?" }
                });
    
                var retrievalResult = await agentClient.RetrieveAsync(
                    retrievalRequest: new KnowledgeAgentRetrievalRequest(
                        messages: messages
                            .Where(message => message["role"] != "system")
                            .Select(
                                message => new KnowledgeAgentMessage(content: new[] { new KnowledgeAgentMessageTextContent(message["content"]) }) { Role = message["role"] }
                            )
                            .ToList()
                    )
                );
    
                messages.Add(new Dictionary<string, string>
                {
                    { "role", "assistant" },
                    { "content", (retrievalResult.Value.Response[0].Content[0] as KnowledgeAgentMessageTextContent).Text }
                });
    
                // Print the response, activity, and results
                Console.WriteLine("Response:");
                Console.WriteLine((retrievalResult.Value.Response[0].Content[0] as KnowledgeAgentMessageTextContent).Text);
    
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
    
                Console.WriteLine("Results:");
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
                messages.Add(new Dictionary<string, string>
                {
                    { "role", "user" },
                    { "content", "How do I find lava at night?" }
                });
    
                retrievalResult = await agentClient.RetrieveAsync(
                    retrievalRequest: new KnowledgeAgentRetrievalRequest(
                        messages: messages
                            .Where(message => message["role"] != "system")
                            .Select(
                                message => new KnowledgeAgentMessage(content: new[] { new KnowledgeAgentMessageTextContent(message["content"]) }) { Role = message["role"] }
                            )
                            .ToList()
                    )
                );
    
                messages.Add(new Dictionary<string, string>
                {
                    { "role", "assistant" },
                    { "content", (retrievalResult.Value.Response[0].Content[0] as KnowledgeAgentMessageTextContent).Text }
                });
        
                // Print the new response, activity, and results
                Console.WriteLine("Response:");
                Console.WriteLine((retrievalResult.Value.Response[0].Content[0] as KnowledgeAgentMessageTextContent).Text);
    
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
    
                Console.WriteLine("Results:");
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
                await indexClient.DeleteKnowledgeAgentAsync(knowledgeAgentName);
                Console.WriteLine($"Knowledge agent '{knowledgeAgentName}' deleted successfully.");
                
                await indexClient.DeleteKnowledgeSourceAsync(knowledgeSourceName);
                Console.WriteLine($"Knowledge source '{knowledgeSourceName}' deleted successfully.");
    
                await indexClient.DeleteIndexAsync(indexName);
                Console.WriteLine($"Index '{indexName}' deleted successfully.");
            }
        }
    }
    ```

1. Build and run the application.

    ```shell
    dotnet run
    ```

### Output

The output of the application should be similar to the following:

```
Index 'earth-at-night' created or updated successfully.
Documents uploaded to index 'earth-at-night' successfully.
Knowledge source 'earth-knowledge-source' created or updated successfully.
Knowledge agent 'earth-knowledge-agent' created or updated successfully.
Response:
Suburban belts display larger December brightening than urban cores because holiday lights increase most dramatically in the suburbs and outskirts of major cities, where there is more yard space and a prevalence of single-family homes. Central urban areas, despite having higher absolute light levels, do not see as large an increase in lighting but still experience a brightening of 20 to 30 percent during the holidays [ref_id:2][ref_id:7].

The Phoenix nighttime street grid is sharply visible from space because the metropolitan area is laid out along a regular grid of city blocks and streets, with street lighting clearly visible from low-Earth orbit. The grid pattern is especially evident at night, with major street grids oriented north-south and diagonal corridors like Grand Avenue cutting across cities. The urban grid encourages outward growth along city borders, with extensive surface streets and freeways linking multiple municipalities. In contrast, large stretches of interstate highways between Midwestern cities remain comparatively dim because, although the interstate highways are major transportation corridors, the lighting along these highways is less intense and less continuous than the dense urban street lighting seen in Phoenix. Additionally, navigable rivers and less densely populated areas show less light, indicating that the brightness corresponds closely to urban density and street lighting patterns rather than just the presence of transportation routes [ref_id:0][ref_id:1][ref_id:4].
Activity:
Activity type: KnowledgeAgentModelQueryPlanningActivityRecord
{
  "InputTokens": 2062,
  "OutputTokens": 121,
  "Id": 0,
  "ElapsedMs": 2435
}
Activity type: KnowledgeAgentSearchIndexActivityRecord
{
  "SearchIndexArguments": {
    "Search": "Reasons for larger December brightening in suburban belts compared to urban cores despite higher downtown light levels",      
    "Filter": null
  },
  "KnowledgeSourceName": "earth-knowledge-source",
  "QueryTime": "2025-09-22T15:54:56.528+00:00",
  "Count": 4,
  "Id": 1,
  "ElapsedMs": 1921
}
Activity type: KnowledgeAgentSearchIndexActivityRecord
{
  "SearchIndexArguments": {
    "Search": "Factors making Phoenix nighttime street grid sharply visible from space",
    "Filter": null
  },
  "KnowledgeSourceName": "earth-knowledge-source",
  "QueryTime": "2025-09-22T15:55:06.991+00:00",
  "Count": 5,
  "Id": 2,
  "ElapsedMs": 10451
}
Activity type: KnowledgeAgentSearchIndexActivityRecord
{
  "SearchIndexArguments": {
    "Search": "Reasons why large stretches of interstate between Midwestern cities appear comparatively dim at night from space",
    "Filter": null
  },
  "KnowledgeSourceName": "earth-knowledge-source",
  "QueryTime": "2025-09-22T15:55:07.504+00:00",
  "Count": 13,
  "Id": 3,
  "ElapsedMs": 512
}
Activity type: KnowledgeAgentSemanticRerankerActivityRecord
{
  "InputTokens": 68754,
  "Id": 4,
  "ElapsedMs": null
}
Activity type: KnowledgeAgentModelAnswerSynthesisActivityRecord
{
  "InputTokens": 7231,
  "OutputTokens": 279,
  "Id": 5,
  "ElapsedMs": 6429
}
Results:
Reference type: KnowledgeAgentSearchIndexReference
{
  "DocKey": "earth_at_night_508_page_104_verbalized",
  "Id": "0",
  "ActivitySource": 2,
  "SourceData": {
    "id": "earth_at_night_508_page_104_verbalized",
    "page_chunk": "\u003C!-- PageHeader=\u0022Urban Structure\u0022 --\u003E\n\n### Location of Phoenix, Arizona\n\nThe image depicts a globe highlighting the location of Phoenix, Arizona, in the southwestern United States, marked with a blue pinpoint on the map of North America. Phoenix is situated in the central part of Arizona, which is in the southwestern region of the United States.\n\n---\n\n### Grid of City Blocks-Phoenix, Arizona\n\nLike many large urban areas of the central and western United States, the Phoenix metropolitan area is laid out along a regular grid of city blocks and streets. While visible during the day, this grid is most evident at night, when the pattern of street lighting is clearly visible from the low-Earth-orbit vantage point of the ISS.\n\nThis astronaut photograph, taken on March 16, 2013, includes parts of several cities in the metropolitan area, including Phoenix (image right), Glendale (center), and Peoria (left). While the major street grid is oriented north-south, the northwest-southeast oriented Grand Avenue cuts across the three cities at image center. Grand Avenue is a major transportation corridor through the western metropolitan area; the lighting patterns of large industrial and commercial properties are visible along its length. Other brightly lit properties include large shopping centers, strip malls, and gas stations, which tend to be located at the intersections of north-south and east-west trending streets.\n\nThe urban grid encourages growth outwards along a city\u0027s borders by providing optimal access to new real estate. Fueled by the adoption of widespread personal automobile use during the twentieth century, the Phoenix metropolitan area today includes 25 other municipalities (many of them largely suburban and residential) linked by a network of surface streets and freeways.\n\nWhile much of the land area highlighted in this image is urbanized, there are several noticeably dark areas. The Phoenix Mountains are largely public parks and recreational land. To the west, agricultural fields provide a sharp contrast to the lit streets of residential developments. The Salt River channel appears as a dark ribbon within the urban grid.\n\n\n\u003C!-- PageFooter=\u0022Earth at Night\u0022 --\u003E\n\u003C!-- PageNumber=\u002288\u0022 --\u003E",
    "page_number": 104
  },
  "RerankerScore": 2.6642752
}
Reference type: KnowledgeAgentSearchIndexReference
{
  "DocKey": "earth_at_night_508_page_105_verbalized",
  "Id": "3",
  "ActivitySource": 2,
  "SourceData": {
    "id": "earth_at_night_508_page_105_verbalized",
    "page_chunk": "# Urban Structure\n\n## March 16, 2013\n\n### Phoenix Metropolitan Area at Night\n\nThis figure presents a nighttime satellite view of the Phoenix metropolitan area, highlighting urban structure and transport corridors. City lights illuminate the layout of several cities and major thoroughfares.\n\n**Labeled Urban Features:**\n\n- **Phoenix:** Central and brightest area in the right-center of the image.\n- **Glendale:** Located to the west of Phoenix, this city is also brightly lit.\n- **Peoria:** Further northwest, this area is labeled and its illuminated grid is seen.\n- **Grand Avenue:** Clearly visible as a diagonal, brightly lit thoroughfare running from Phoenix through Glendale and Peoria.\n- **Salt River Channel:** Identified in the southeast portion, running through illuminated sections.\n- **Phoenix Mountains:** Dark, undeveloped region to the northeast of Phoenix.\n- **Agricultural Fields:** Southwestern corner of the image, grid patterns are visible but with much less illumination, indicating agricultural land use.\n\n**Additional Notes:**\n\n- The overall pattern shows a grid-like urban development typical of western U.S. cities, with scattered bright nodes at major intersections or city centers.\n- There is a clear transition from dense urban development to sparsely populated or agricultural land, particularly evident towards the bottom and left of the image.\n- The illuminated areas follow the existing road and street grids, showcasing the extensive spread of the metropolitan area.\n\n**Figure Description:**  \nA satellite nighttime image captured on March 16, 2013, showing Phoenix and surrounding areas (including Glendale and Peoria). Major landscape and infrastructural features, such as the Phoenix Mountains, Grand Avenue, the Salt River Channel, and agricultural fields, are labeled. The image reveals the extent of urbanization and the characteristic street grid illuminated by city lights.\n\n---\n\nPage 89",
    "page_number": 105
  },
  "RerankerScore": 2.5905457
}
... // Trimmed for brevity
Response:
Lava can be found at night by using satellite imagery that captures thermal infrared and near-infrared wavelengths, which highlight the heat emitted by active lava flows. For example, the Landsat 8 satellite's night view combines thermal, shortwave infrared, and near-infrared data to distinguish very hot lava (appearing bright white), cooling lava (red), and lava flows obscured by clouds (purple), as demonstrated in the monitoring of Kilauea's lava flows in Hawaii [ref_id:0]. Similarly, the Operational Land Imager (OLI) and Thermal Infrared Sensor (TIRS) on Landsat 8 have been used to detect the thermal infrared signature of lava flows during Mount Etna's flank eruption in Italy, highlighting active vents and lava flows at night [ref_id:1]. Additionally, the VIIRS Day/Night Band (DNB) on polar-orbiting satellites can detect faint light sources such as moonlight, which, combined with thermal data, allows for the observation of glowing lava flows at active volcanoes during nighttime [ref_id:1][ref_id:3]. Thus, by using satellite instruments sensitive to thermal and near-infrared wavelengths and leveraging natural illumination sources like moonlight, lava can be effectively located and monitored at night from space.
Activity:
Activity type: KnowledgeAgentModelQueryPlanningActivityRecord
{
  "InputTokens": 2357,
  "OutputTokens": 88,
  "Id": 0,
  "ElapsedMs": 1917
}
Activity type: KnowledgeAgentSearchIndexActivityRecord
{
  "SearchIndexArguments": {
    "Search": "How to locate lava flows at night",
    "Filter": null
  },
  "KnowledgeSourceName": "earth-knowledge-source",
  "QueryTime": "2025-09-22T15:55:16.919+00:00",
  "Count": 16,
  "Id": 1,
  "ElapsedMs": 433
}
Activity type: KnowledgeAgentSearchIndexActivityRecord
{
  "SearchIndexArguments": {
    "Search": "Methods for detecting lava at night",
    "Filter": null
  },
  "KnowledgeSourceName": "earth-knowledge-source",
  "QueryTime": "2025-09-22T15:55:17.389+00:00",
  "Count": 13,
  "Id": 2,
  "ElapsedMs": 468
}
Activity type: KnowledgeAgentSearchIndexActivityRecord
{
  "SearchIndexArguments": {
    "Search": "Safety tips for finding lava at night",
    "Filter": null
  },
  "KnowledgeSourceName": "earth-knowledge-source",
  "QueryTime": "2025-09-22T15:55:17.801+00:00",
  "Count": 3,
  "Id": 3,
  "ElapsedMs": 411
}
Activity type: KnowledgeAgentSemanticRerankerActivityRecord
{
  "InputTokens": 67218,
  "Id": 4,
  "ElapsedMs": null
}
Activity type: KnowledgeAgentModelAnswerSynthesisActivityRecord
{
  "InputTokens": 7345,
  "OutputTokens": 267,
  "Id": 5,
  "ElapsedMs": 6044
}
Results:
Reference type: KnowledgeAgentSearchIndexReference
{
  "DocKey": "earth_at_night_508_page_60_verbalized",
  "Id": "0",
  "ActivitySource": 1,
  "SourceData": {
    "id": "earth_at_night_508_page_60_verbalized",
    "page_chunk": "\u003C!-- PageHeader=\u0022Volcanoes\u0022 --\u003E\n\n## Volcanoes\n\n### The Infrared Glows of Kilauea\u0027s Lava Flows\u2014Hawaii\n\nIn early May 2018, an eruption on Hawaii\u0027s Kilauea volcano began to unfold. The eruption took a dangerous turn on May 3, 2018, when new fissures opened in the residential neighborhood of Leilani Estates. During the summer-long eruptive event, other fissures emerged along the East Rift Zone. Lava from vents along the rift zone flowed downslope, reaching the ocean in several areas, and filling in Kapoho Bay.\n\nA time series of Landsat 8 imagery shows the progression of the lava flows from May 16 to August 13. The night view combines thermal, shortwave infrared, and near-infrared wavelengths to tease out the very hot lava (bright white), cooling lava (red), and lava flows obstructed by clouds (purple).\n\n#### Figure: Location of Kilauea Volcano, Hawaii\n\nA globe is shown centered on North America, with a marker placed in the Pacific Ocean indicating the location of Hawaii, to the southwest of the mainland United States.\n\n\u003C!-- PageFooter=\u0022Earth at Night\u0022 --\u003E\n\u003C!-- PageNumber=\u002244\u0022 --\u003E",
    "page_number": 60
  },
  "RerankerScore": 2.779123
}
Reference type: KnowledgeAgentSearchIndexReference
{
  "DocKey": "earth_at_night_508_page_64_verbalized",
  "Id": "2",
  "ActivitySource": 1,
  "SourceData": {
    "id": "earth_at_night_508_page_64_verbalized",
    "page_chunk": "\u003C!-- PageHeader=\u0022Volcanoes\u0022 --\u003E\n\n### Nighttime Glow at Mount Etna - Italy\n\nAt about 2:30 a.m. local time on March 16, 2017, the VIIRS DNB on the Suomi NPP satellite captured this nighttime image of lava flowing on Mount Etna in Sicily, Italy. Etna is one of the world\u0027s most active volcanoes.\n\n#### Figure: Location of Mount Etna\nA world globe is depicted, with a marker indicating the location of Mount Etna in Sicily, Italy, in southern Europe near the center of the Mediterranean Sea.\n\n\u003C!-- PageFooter=\u0022Earth at Night\u0022 --\u003E\n\u003C!-- PageNumber=\u002248\u0022 --\u003E",
    "page_number": 64
  },
  "RerankerScore": 2.7684891
}
... // Trimmed for brevity
Knowledge agent 'earth-knowledge-agent' deleted successfully.
Knowledge source 'earth-knowledge-source' deleted successfully.
Index 'earth-at-night' deleted successfully.
```

## Understand the code

Now that you've run the code, let's break down the key steps:

1. [Create a search index](#create-a-search-index)
1. [Upload documents to the index](#upload-documents-to-the-index)
1. [Create a knowledge source](#create-a-knowledge-source)
1. [Create a knowledge agent](#create-a-knowledge-agent)
1. [Set up messages](#set-up-messages)
1. [Run the retrieval pipeline](#run-the-retrieval-pipeline)
1. [Continue the conversation](#continue-the-conversation)

### Create a search index

In Azure AI Search, an index is a structured collection of data. The following code defines an index named `earth-at-night`, which you previously specified using the `indexName` variable.

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

### Create a knowledge source

A knowledge source is a reusable reference to your source data. The following code defines a knowledge source named `earth-knowledge-source` that targets the `earth-at-night` index.

`SourceDataSelect` specifies which index fields are accessible for retrieval and citations. Our example includes only human-readable fields to avoid lengthy, uninterpretable embeddings in responses.

```csharp
// Create a knowledge source
var indexKnowledgeSource = new SearchIndexKnowledgeSource(
    name: knowledgeSourceNames,
    searchIndexParameters: new SearchIndexKnowledgeSourceParameters(searchIndexName: indexName)
    {
        SourceDataSelect = "id,page_chunk,page_number"
    }
);
await indexClient.CreateOrUpdateKnowledgeSourceAsync(indexKnowledgeSource);
Console.WriteLine($"Knowledge source '{knowledgeSourceName}' created or updated successfully.");
```

### Create a knowledge agent

To target `earth-knowledge-source` and your `gpt-5-mini` deployment at query time, you need a knowledge agent. Add and run a code cell with the following code to define a knowledge agent named `earth-knowledge-agent`, which you previously specified using the `knowledgeAgentName` variable.

`RerankerThreshold` ensures semantic relevance by excluding responses with a reranker score of `2.5` or lower. Meanwhile, `Modality` is set to `AnswerSynthesis`, enabling natural-language answers that cite the retrieved documents.

```csharp
// Create a knowledge agent
var openAiParameters = new AzureOpenAIVectorizerParameters
{
    ResourceUri = new Uri(aoaiEndpoint),
    DeploymentName = aoaiGptDeployment,
    ModelName = aoaiGptModel
};

var agentModel = new KnowledgeAgentAzureOpenAIModel(azureOpenAIParameters: openAiParameters);
var outputConfig = new KnowledgeAgentOutputConfiguration
{
    Modality = KnowledgeAgentOutputConfigurationModality.AnswerSynthesis,
    IncludeActivity = true
};

var agent = new KnowledgeAgent(
    name: knowledgeAgentName,
    models: new[] { agentModel },
    knowledgeSources: new KnowledgeSourceReference[] {
        new KnowledgeSourceReference(knowledgeSourceName) {
            IncludeReferences = true,
            IncludeReferenceSourceData = true,
            RerankerThreshold = (float?)2.5
        }
    }
)
{
    OutputConfiguration = outputConfig
};

await indexClient.CreateOrUpdateKnowledgeAgentAsync(agent);
Console.WriteLine($"Knowledge agent '{knowledgeAgentName}' created or updated successfully.");
```

### Set up messages

Messages are the input for the retrieval route and contain the conversation history. Each message includes a role that indicates its origin, such as `system` or `user`, and content in natural language. The LLM you use determines which roles are valid.

The following code creates a system message, which instructs `earth-knowledge-agent` to answer questions about the Earth at night and respond with "I don't know" when answers are unavailable.

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

You're ready to run agentic retrieval by sending a two-part user query to `earth-knowledge-agent`. Given the conversation history and retrieval parameters, the agent:

1. Analyzes the entire conversation to infer the user's information need.
1. Decomposes the compound query into focused subqueries.
1. Runs the subqueries concurrently against your knowledge source.
1. Uses semantic ranker to rerank and filter the results.
1. Synthesizes the top results into a natural-language answer.

```csharp
// Use agentic retrieval to fetch results
var agentClient = new KnowledgeAgentRetrievalClient(
    endpoint: new Uri(searchEndpoint),
    agentName: knowledgeAgentName,
    tokenCredential: new DefaultAzureCredential()
);

messages.Add(new Dictionary<string, string>
{
    { "role", "user" },
    { "content", @"Why do suburban belts display larger December brightening than urban cores even though absolute light levels are higher downtown?
    Why is the Phoenix nighttime street grid is so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?" }
});

var retrievalResult = await agentClient.RetrieveAsync(
    retrievalRequest: new KnowledgeAgentRetrievalRequest(
        messages: messages
            .Where(message => message["role"] != "system")
            .Select(
                message => new KnowledgeAgentMessage(content: new[] { new KnowledgeAgentMessageTextContent(message["content"]) }) { Role = message["role"] }
            )
            .ToList()
    )
);

messages.Add(new Dictionary<string, string>
{
    { "role", "assistant" },
    { "content", (retrievalResult.Value.Response[0].Content[0] as KnowledgeAgentMessageTextContent).Text }
});
```

#### Review the response, activity, and results

The following code displays the response, activity, and results of the retrieval pipeline, where:

+ `Response` provides a synthesized, LLM-generated answer to the query that cites the retrieved documents. When answer synthesis isn't enabled, this section contains content extracted directly from the documents.

+ `Activity` tracks the steps that were taken during the retrieval process, including the subqueries generated by your `gpt-5-mini` deployment and the tokens used for semantic ranking, query planning, and answer synthesis.

+ `Results` lists the documents that contributed to the response, each one identified by their `DocKey`.

```csharp
// Print the response, activity, and results
Console.WriteLine("Response:");
Console.WriteLine((retrievalResult.Value.Response[0].Content[0] as KnowledgeAgentMessageTextContent).Text);

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

Console.WriteLine("Results:");
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

The following code continues the conversation with `earth-knowledge-agent`. After you send this user query, the agent fetches relevant content from `earth-knowledge-source` and appends the response to the messages list.

```csharp
// Continue the conversation
messages.Add(new Dictionary<string, string>
{
    { "role", "user" },
    { "content", "How do I find lava at night?" }
});

retrievalResult = await agentClient.RetrieveAsync(
    retrievalRequest: new KnowledgeAgentRetrievalRequest(
        messages: messages
            .Where(message => message["role"] != "system")
            .Select(
                message => new KnowledgeAgentMessage(content: new[] { new KnowledgeAgentMessageTextContent(message["content"]) }) { Role = message["role"] }
            )
            .ToList()
    )
);

messages.Add(new Dictionary<string, string>
{
    { "role", "assistant" },
    { "content", (retrievalResult.Value.Response[0].Content[0] as KnowledgeAgentMessageTextContent).Text }
});
```

#### Review the new response, activity, and results

The following code displays the new response, activity, and results of the retrieval pipeline.

```csharp
// Print the response, activity, and results
Console.WriteLine("Response:");
Console.WriteLine((retrievalResult.Value.Response[0].Content[0] as KnowledgeAgentMessageTextContent).Text);

Console.WriteLine("Activities:");
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

Console.WriteLine("Results:");
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

When you work in your own subscription, it's a good idea to finish a project by determining whether you still need the resources you created. Resources that are left running can cost you money.

In the Azure portal, you can manage your Azure AI Search and Azure AI Foundry resources by selecting **All resources** or **Resource groups** from the left pane.

Otherwise, the following code from `Program.cs` deleted the objects you created in this quickstart.

### Delete the knowledge agent

```csharp
await indexClient.DeleteKnowledgeAgentAsync(knowledgeAgentName);
Console.WriteLine($"Knowledge agent '{knowledgeAgentName}' deleted successfully.");
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

