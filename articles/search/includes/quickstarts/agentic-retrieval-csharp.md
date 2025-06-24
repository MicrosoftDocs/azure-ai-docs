---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 6/24/2025
---

[!INCLUDE [Feature preview](../previews/preview-generic.md)]

In this quickstart, you use [agentic retrieval](../../search-agentic-retrieval-concept.md) to create a conversational search experience powered by large language models (LLMs) and your proprietary data. Agentic retrieval breaks down complex user queries into subqueries, runs the subqueries in parallel, and extracts grounding data from documents indexed in Azure AI Search. The output is intended for integration with agentic and custom chat solutions.

Although you can provide your own data, this quickstart uses [sample JSON documents](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/nasa-e-book/earth-at-night-json) from NASA's Earth at Night e-book. The documents describe general science topics and images of Earth at night as observed from space.

> [!TIP]
> To get started with a Jupyter notebook instead, see the [Azure-Samples/azure-search-dotnet-samples](https://github.com/Azure-Samples/azure-search-dotnet-samples/tree/main/quickstart-agentic-retrieval) repository on GitHub.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

+ An [Azure AI Search service](../../search-create-service-portal.md) on the Basic tier or higher with [semantic ranker enabled](../../semantic-how-to-enable-disable.md).

+ An [Azure AI Foundry project](/azure/ai-foundry/how-to/create-projects). You get an Azure AI Foundry resource (that you need for model deployments) when you create an Azure AI Foundry project.

+ The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

[!INCLUDE [Setup](./agentic-retrieval-setup.md)]

## Setup

1. Create a new folder `quickstart-agentic-retrieval` to contain the application and open Visual Studio Code in that folder with the following command:

    ```shell
    mkdir quickstart-agentic-retrieval && cd quickstart-agentic-retrieval
    ```

1. Create a new console application with the following command:

    ```shell
    dotnet new console
    ```

1. Install the Azure AI Search client library ([Azure.Search.Documents](/dotnet/api/overview/azure/search.documents-readme)) for .NET with:

    ```console
    dotnet add package Azure.Search.Documents --version 11.7.0-beta.4
    ```

1. Install the Azure OpenAI client library ([Azure.AI.OpenAI](/dotnet/api/overview/azure.ai.openai-readme)) for .NET with:

    ```console
    dotnet add package Azure.AI.OpenAI --version 2.1.0
    ```

1. Install the `dotenv` package to load environment variables from a `.env` file with:

    ```console
    dotnet add package dotenv.net
    ```

1. For the **recommended** keyless authentication with Microsoft Entra ID, install the [Azure.Identity](https://www.nuget.org/packages/Azure.Identity) package with:

    ```console
    dotnet add package Azure.Identity
    ```

1. For the **recommended** keyless authentication with Microsoft Entra ID, sign in to Azure with the following command:

    ```console
    az login
    ```


## Create the index and knowledge agent

1. Create a new file named `.env` in the `quickstart-agentic-retrieval` folder and add the following environment variables:

    ```plaintext
    AZURE_OPENAI_ENDPOINT=https://<your-ai-foundry-resource-name>.openai.azure.com/
    AZURE_OPENAI_GPT_DEPLOYMENT=gpt-4.1-mini
    AZURE_SEARCH_ENDPOINT=https://<your-search-service-name>.search.windows.net
    AZURE_SEARCH_INDEX_NAME=agentic-retrieval-sample
    ```

    Replace `<your-search-service-name>` and `<your-ai-foundry-resource-name>` with your actual Azure AI Search service name and Azure AI Foundry resource name.

1. In *Program.cs*, paste the following code.

    ```csharp
    using dotenv.net;
    using Azure.Identity;
    using Azure.Search.Documents.Indexes;
    using Azure.Search.Documents.Indexes.Models;
    using System.Net.Http;
    using System.Text.Json;
    using Azure.Search.Documents;
    using Azure.Search.Documents.Models;
    using Azure.Search.Documents.Agents;
    using Azure.Search.Documents.Agents.Models;
    using Azure.AI.OpenAI;
    using OpenAI.Chat;
    
    namespace AzureSearch.Quickstart
    {    class Program
        {
            static async Task Main(string[] args)
            {            
                // Load environment variables from .env file
                // Ensure you have a .env file in the same directory with the required variables.
                DotEnv.Load();
    
                string endpoint = Environment.GetEnvironmentVariable("AZURE_SEARCH_ENDPOINT") 
                    ?? throw new InvalidOperationException("AZURE_SEARCH_ENDPOINT is not set.");
                string azureOpenAIEndpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT") 
                    ?? throw new InvalidOperationException("AZURE_OPENAI_ENDPOINT is not set.");            string azureOpenAIGptDeployment = "gpt-4.1-mini";
                string azureOpenAIGptModel = "gpt-4.1-mini";
                string azureOpenAIEmbeddingDeployment = "text-embedding-3-large";
                string azureOpenAIEmbeddingModel = "text-embedding-3-large";
                
                string indexName = "earth_at_night";
                string agentName = "earth-search-agent";
    
                var credential = new DefaultAzureCredential();            
                // Define the fields for the index
                var fields = new List<SearchField>
                {
                    new SimpleField("id", SearchFieldDataType.String) { IsKey = true, IsFilterable = true, IsSortable = true, IsFacetable = true },
                    new SearchField("page_chunk", SearchFieldDataType.String) { IsFilterable = false, IsSortable = false, IsFacetable = false },
                    new SearchField("page_embedding_text_3_large", SearchFieldDataType.Collection(SearchFieldDataType.Single)) { VectorSearchDimensions = 3072, VectorSearchProfileName = "hnsw_text_3_large" },
                    new SimpleField("page_number", SearchFieldDataType.Int32) { IsFilterable = true, IsSortable = true, IsFacetable = true }
                };            
                // Define the vectorizer
                var vectorizer = new AzureOpenAIVectorizer(vectorizerName: "azure_openai_text_3_large")
                {
                    Parameters = new AzureOpenAIVectorizerParameters
                    {
                        ResourceUri = new Uri(azureOpenAIEndpoint),
                        DeploymentName = azureOpenAIEmbeddingDeployment,
                        ModelName = azureOpenAIEmbeddingModel
                    }
                };
    
                // Define the vector search profile and algorithm
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
    
                // Define semantic configuration
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
                    Configurations =
                    {
                        semanticConfig
                    }
                };
    
                // Create the index
                var index = new SearchIndex(indexName)
                {
                    Fields = fields,
                    VectorSearch = vectorSearch,
                    SemanticSearch = semanticSearch
                };
    
                // Create the index client and delete the index if it exists, then create it
                var indexClient = new SearchIndexClient(new Uri(endpoint), credential);
                try
                {
                    await indexClient.DeleteIndexAsync(indexName);
                    Console.WriteLine($"Index '{indexName}' deleted successfully (if it existed).");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Index '{indexName}' could not be deleted or did not exist: {ex.Message}");
                }
                await indexClient.CreateOrUpdateIndexAsync(index);
    
                Console.WriteLine($"Index '{indexName}' created or updated successfully");
    
                // Download the documents from the GitHub URL
                string url = "https://raw.githubusercontent.com/Azure-Samples/azure-search-sample-data/refs/heads/main/nasa-e-book/earth-at-night-json/documents.json";
                var httpClient = new HttpClient();
                var response = await httpClient.GetAsync(url);
                response.EnsureSuccessStatusCode();
                var json = await response.Content.ReadAsStringAsync();
    
                var documents = JsonSerializer.Deserialize<List<Dictionary<string, object>>>(json);
                var searchClient = new SearchClient(new Uri(endpoint), indexName, credential);
                var searchIndexingBufferedSender = new SearchIndexingBufferedSender<Dictionary<string, object>>(
                    searchClient,
                    new SearchIndexingBufferedSenderOptions<Dictionary<string, object>>
                    {
                        KeyFieldAccessor = doc => doc["id"].ToString(),
                    }
                );
    
                await searchIndexingBufferedSender.UploadDocumentsAsync(documents);
                await searchIndexingBufferedSender.FlushAsync();
    
                Console.WriteLine($"Documents uploaded to index '{indexName}'");            

                var openAiParameters = new AzureOpenAIVectorizerParameters
                {
                    ResourceUri = new Uri(azureOpenAIEndpoint),
                    DeploymentName = azureOpenAIGptDeployment,
                    ModelName = azureOpenAIGptModel
                };
    
                var agentModel = new KnowledgeAgentAzureOpenAIModel(azureOpenAIParameters: openAiParameters);
    
                var targetIndex = new KnowledgeAgentTargetIndex(indexName)
                {
                    DefaultRerankerThreshold = 2.5f
                };
    
                // Create the knowledge agent
                var agent = new KnowledgeAgent(
                    name: agentName,
                    models: new[] { agentModel },
                    targetIndexes: new[] { targetIndex });
                await indexClient.CreateOrUpdateKnowledgeAgentAsync(agent);
                Console.WriteLine($"Search agent '{agentName}' created or updated successfully");
    
    
                string instructions = @"
                A Q&A agent that can answer questions about the Earth at night.
                Sources have a JSON format with a ref_id that must be cited in the answer.
                If you do not have the answer, respond with ""I don't know"".
                ";
    
                var messages = new List<Dictionary<string, object>>
                {
                    new Dictionary<string, object>
                    {
                        { "role", "system" },
                        { "content", instructions }
                    }
                };
    
                var agentClient = new KnowledgeAgentRetrievalClient(
                    endpoint: new Uri(endpoint),
                    agentName: agentName,
                    tokenCredential: new DefaultAzureCredential()
                );            

                messages.Add(new Dictionary<string, object>
                {
                    { "role", "user" },
                    { "content", @"
                Why do suburban belts display larger December brightening than urban cores even though absolute light levels are higher downtown?
                Why is the Phoenix nighttime street grid is so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?
                " }
                });
    
                var retrievalResult = await agentClient.RetrieveAsync(
                    retrievalRequest: new KnowledgeAgentRetrievalRequest(
                            messages: messages
                                .Where(message => message["role"].ToString() != "system")
                                .Select(
                                message => new KnowledgeAgentMessage(
                                    role: message["role"].ToString(),
                                    content: new[] { new KnowledgeAgentMessageTextContent(message["content"].ToString()) }))
                                .ToList()
                            )
                        {
                            TargetIndexParams = { new KnowledgeAgentIndexParams { IndexName = indexName, RerankerThreshold = 2.5f } }
                        }
                    );
    
                messages.Add(new Dictionary<string, object>
                {
                    { "role", "assistant" },
                    { "content", (retrievalResult.Value.Response[0].Content[0] as KnowledgeAgentMessageTextContent).Text }
                });
    
                // Print 
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
    
                Console.WriteLine("Results");
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
    
    
                AzureOpenAIClient azureClient = new(
                    new Uri(azureOpenAIEndpoint),
                    new DefaultAzureCredential());
                ChatClient chatClient = azureClient.GetChatClient(azureOpenAIGptDeployment);            
                List<ChatMessage> chatMessages = messages
                    .Select<Dictionary<string, object>, ChatMessage>(m => m["role"].ToString() switch
                    {
                        "user" => new UserChatMessage(m["content"].ToString()),
                        "assistant" => new AssistantChatMessage(m["content"].ToString()),
                        "system" => new SystemChatMessage(m["content"].ToString()),
                        _ => null
                    })
                    .Where(m => m != null)
                    .ToList();
    
    
                var result = await chatClient.CompleteChatAsync(chatMessages);
    
                Console.WriteLine($"[ASSISTANT]: {result.Value.Content[0].Text.Replace(".", "\n")}");
    
                messages.Add(new Dictionary<string, object>
                {
                    { "role", "user" },
                    { "content", "How do I find lava at night?" }
                });
    
                var retrievalResult2 = await agentClient.RetrieveAsync(
                    retrievalRequest: new KnowledgeAgentRetrievalRequest(
                            messages: messages
                                .Where(message => message["role"].ToString() != "system")
                                .Select(
                                message => new KnowledgeAgentMessage(
                                    role: message["role"].ToString(),
                                    content: new[] { new KnowledgeAgentMessageTextContent(message["content"].ToString()) }))
                                .ToList()
                            )
                        {
                            TargetIndexParams = { new KnowledgeAgentIndexParams { IndexName = indexName, RerankerThreshold = 2.5f } }
                        }
                    );
    
                messages.Add(new Dictionary<string, object>
                {
                    { "role", "assistant" },
                    { "content", (retrievalResult2.Value.Response[0].Content[0] as KnowledgeAgentMessageTextContent).Text }
                });
    
                Console.WriteLine((retrievalResult2.Value.Response[0].Content[0] as KnowledgeAgentMessageTextContent).Text);
    
                Console.WriteLine("Activities:");
                foreach (var activity in retrievalResult2.Value.Activity)
                {
                    Console.WriteLine($"Activity Type: {activity.GetType().Name}");
                    string activityJson2 = JsonSerializer.Serialize(
                        activity,
                        activity.GetType(),
                        new JsonSerializerOptions { WriteIndented = true }
                    );
                    Console.WriteLine(activityJson2);
                }
    
                Console.WriteLine("Results");
                foreach (var reference in retrievalResult2.Value.References)
                {
                    Console.WriteLine($"Reference Type: {reference.GetType().Name}");
                    string referenceJson2 = JsonSerializer.Serialize(
                        reference,
                        reference.GetType(),
                        new JsonSerializerOptions { WriteIndented = true }
                    );
                    Console.WriteLine(referenceJson2);
                }            List<ChatMessage> chatMessages2 = messages
                    .Select<Dictionary<string, object>, ChatMessage>(m => m["role"].ToString() switch
                    {
                        "user" => new UserChatMessage(m["content"].ToString()),
                        "assistant" => new AssistantChatMessage(m["content"].ToString()),
                        "system" => new SystemChatMessage(m["content"].ToString()),
                        _ => null
                    })
                    .Where(m => m != null)
                    .ToList();
    
    
                var result2 = await chatClient.CompleteChatAsync(chatMessages2);
    
                Console.WriteLine($"[ASSISTANT]: {result2.Value.Content[0].Text.Replace(".", "\n")}");
    
                await indexClient.DeleteKnowledgeAgentAsync(agentName);
                System.Console.WriteLine($"Search agent '{agentName}' deleted successfully");
    
                await indexClient.DeleteIndexAsync(indexName);
                System.Console.WriteLine($"Index '{indexName}' deleted successfully");
    
    
            }
        }
    }
    ```

1. Build and run the application with the following command:

    ```shell
    dotnet run
    ```

## Output

The output of the application should look similar to the following:

```plaintext
Index 'earth_at_night' deleted successfully (if it existed).
Index 'earth_at_night' created or updated successfully
Documents uploaded to index 'earth_at_night'
Search agent 'earth-search-agent' created or updated successfully
[]
Activities:
Activity Type: KnowledgeAgentModelQueryPlanningActivityRecord
{
  "InputTokens": 1265,
  "OutputTokens": 536,
  "ElapsedMs": null,
  "Id": 0
}
Activity Type: KnowledgeAgentSearchActivityRecord
{
  "TargetIndex": "earth_at_night",
  "Query": {
    "Search": "Reasons for larger December brightening in suburban belts compared to urban cores despite higher absolute light levels downtown",
    "Filter": null
  },
  "QueryTime": "2025-06-19T14:02:27.504+00:00",
  "Count": 0,
  "ElapsedMs": 768,
  "Id": 1
}
Activity Type: KnowledgeAgentSearchActivityRecord
{
  "TargetIndex": "earth_at_night",
  "Query": {
    "Search": "Why is the Phoenix nighttime street grid sharply visible from space while large stretches of interstate between Midwestern cities are comparatively dim?",
    "Filter": null
  },
  "QueryTime": "2025-06-19T14:02:27.817+00:00",
  "Count": 0,
  "ElapsedMs": 292,
  "Id": 2
}
Activity Type: KnowledgeAgentSemanticRankerActivityRecord
{
  "InputTokens": 52609,
  "ElapsedMs": null,
  "Id": 3
}
Results
[ASSISTANT]: The suburban belts display larger December brightening than urban cores because suburban areas often have more residential lighting that increases during December holidays, such as decorative lights, leading to a noticeable rise in brightness
 In contrast, urban cores already have very high absolute light levels, so the relative increase from additional lighting is less significant


Regarding Phoenix's nighttime street grid visibility from space, it is sharply visible because the city has a distinctive, well-lit, and uniformly spaced street grid pattern that emits consistent light
 In contrast, large stretches of interstate highways between Midwestern cities remain comparatively dim because highways have less continuous lighting, with fewer lights spread over longer distances, making them less prominent from space [ref_id: night_earth_study_2021]

[{"ref_id":0,"content":"<!-- PageHeader=\"Volcanoes\" -->\n\n## Volcanoes\n\n### The Infrared Glows of Kilauea's Lava Flows—Hawaii\n\nIn early May 2018, an eruption on Hawaii's Kilauea volcano began to unfold. The eruption took a dangerous turn on May 3, 2018, when new fissures opened in the residential neighborhood of Leilani Estates. During the summer-long eruptive event, other fissures emerged along the East Rift Zone. Lava from vents along the rift zone flowed downslope, reaching the ocean in several areas, and filling in Kapoho Bay.\n\nA time series of Landsat 8 imagery shows the progression of the lava flows from May 16 to August 13. The night view combines thermal, shortwave infrared, and near-infrared wavelengths to tease out the very hot lava (bright white), cooling lava (red), and lava flows obstructed by clouds (purple).\n\n#### Figure: Location of Kilauea Volcano, Hawaii\n\nA globe is shown centered on North America, with a marker placed in the Pacific Ocean indicating the location of Hawaii, to the southwest of the mainland United States.\n\n<!-- PageFooter=\"Earth at Night\" -->\n<!-- PageNumber=\"44\" -->"},{"ref_id":1,"content":"<!-- PageHeader=\"Volcanoes\" -->\n\n### Nighttime Glow at Mount Etna - Italy\n\nAt about 2:30 a.m. local time on March 16, 2017, the VIIRS DNB on the Suomi NPP satellite captured this nighttime image of lava flowing on Mount Etna in Sicily, Italy. Etna is one of the world's most active volcanoes.\n\n#### Figure: Location of Mount Etna\nA world globe is depicted, with a marker indicating the location of Mount Etna in Sicily, Italy, in southern Europe near the center of the Mediterranean Sea.\n\n<!-- PageFooter=\"Earth at Night\" -->\n<!-- PageNumber=\"48\" -->"},{"ref_id":2,"content":"For the first time in perhaps a decade, Mount Etna experienced a \"flank eruption\"—erupting from its side instead of its summit—on December 24, 2018. The activity was accompanied by 130 earthquakes occurring over three hours that morning. Mount Etna, Europe’s most active volcano, has seen periodic activity on this part of the mountain since 2013. The Operational Land Imager (OLI) on the Landsat 8 satellite acquired the main image of Mount Etna on December 28, 2018.\n\nThe inset image highlights the active vent and thermal infrared signature from lava flows, which can be seen near the newly formed fissure on the southeastern side of the volcano. The inset was created with data from OLI and the Thermal Infrared Sensor (TIRS) on Landsat 8. Ash spewing from the fissure cloaked adjacent villages and delayed aircraft from landing at the nearby Catania airport. Earthquakes occurred in the subsequent days after the initial eruption and displaced hundreds of people from their homes.\n\nFor nighttime images of Mount Etna’s March 2017 eruption, see pages 48–51.\n\n---\n\n### Hazards of Volcanic Ash Plumes and Satellite Observation\n\nWith the help of moonlight, satellite instruments can track volcanic ash plumes, which present significant hazards to airplanes in flight. The volcanic ash—composed of tiny pieces of glass and rock—is abrasive to engine turbine blades, and can melt on the blades and other engine parts, causing damage and even engine stalls. This poses a danger to both the plane’s integrity and passenger safety. Volcanic ash also reduces visibility for pilots and can cause etching of windshields, further reducing pilots’ ability to see. Nightlight images can be combined with thermal images to provide a more complete view of volcanic activity on Earth’s surface.\n\nThe VIIRS Day/Night Band (DNB) on polar-orbiting satellites uses faint light sources such as moonlight, airglow (the atmosphere’s self-illumination through chemical reactions), zodiacal light (sunlight scattered by interplanetary dust), and starlight from the Milky Way. Using these dim light sources, the DNB can detect changes in clouds, snow cover, and sea ice:\n\n#### Table: Light Sources Used by VIIRS DNB\n\n| Light Source         | Description                                                        
          |\n|----------------------|------------------------------------------------------------------------------|\n| Moonlight            | Reflected sunlight from the Moon, illuminating Earth's surface at night      |\n| Airglow              | Atmospheric self-illumination from chemical reactions                        |\n| Zodiacal Light       | Sunlight scattered by interplanetary dust                                    |\n| Starlight/Milky Way  | Faint illumination provided by stars in the Milky Way                        |\n\nGeostationary Operational Environmental Satellites (GOES), managed by NOAA, orbit over Earth’s equator and offer uninterrupted observations of North America. High-latitude areas such as Alaska benefit from polar-orbiting satellites like Suomi NPP, which provide overlapping coverage at the poles, enabling more data collection in these regions. During polar darkness (winter months), VIIRS DNB data allow scientists to:\n\n- Observe sea ice formation\n- Monitor snow cover extent at the highest latitudes\n- Detect open water for ship navigation\n\n#### Table: Satellite Coverage Overview\n\n| Satellite Type          | Orbit           | Coverage Area         | Special Utility                              |\n|------------------------|-----------------|----------------------|----------------------------------------------|\n| GOES              
     | Geostationary   | Equatorial/North America | Continuous regional monitoring              |\n| Polar-Orbiting (e.g., Suomi NPP) | Polar-orbiting    | Poles/high latitudes      | Overlapping passes; useful during polar night|\n\n---\n\n### Weather Forecasting and Nightlight Data\n\nThe use of nightlight data by weather forecasters is growing as the VIIRS instrument enables observation of clouds at night illuminated by sources such as moonlight and lightning. Scientists use these data to study the nighttime behavior of weather systems, including severe storms, which can develop and strike populous areas at night as well as during the day. Combined with thermal data, visible nightlight data allow the detection of clouds at various heights in the atmosphere, such as dense marine fog. This capability enables weather forecasters to issue marine advisories with higher confidence, leading to greater utility. (See \"Marine Layer Clouds—California\" on page 56.)\n\nIn this section of the book, you will see how nightlight data are used to observe nature’s spectacular light shows across a wide range of sources.\n\n---\n\n#### Notable Data from Mount Etna Flank Eruption (December 2018)\n\n| Event/Observation                  | Details                                        
                            |\n|-------------------------------------|----------------------------------------------------------------------------|\n| Date of Flank Eruption              | December 24, 2018                                                          |\n| Number of Earthquakes               | 130 earthquakes within 3 hours                                              |\n| Image Acquisition                   | December 28, 2018 by Landsat 8 OLI                                   
      |\n| Location of Eruption                | Southeastern side of Mount Etna                   
                         |\n| Thermal Imaging Data                | From OLI and TIRS (Landsat 8), highlighting active vent and lava flows     |\n| Impact on Villages/Air Transport    | Ash covered villages; delayed aircraft at Catania airport                  |\n| Displacement                   
     | Hundreds of residents displaced                                            |\n| Ongoing Seismic Activity            | Earthquakes continued after initial eruption                             
  |\n\n---\n\n<!-- PageFooter=\"Earth at Night\" -->\n<!-- PageNumber=\"30\" -->"},{"ref_id":3,"content":"# Volcanoes\n\n---\n\n### Mount Etna Erupts - Italy\n\nThe highly active Mount Etna in Italy sent red lava rolling down its flank on March 19, 2017. An astronaut onboard the ISS took the photograph below of the volcano and its environs that night. City lights surround the mostly dark volcanic area.\n\n---\n\n#### Figure 1: Location of Mount Etna, Italy\n\nA world map highlighting the location of Mount Etna in southern Italy. The marker indicates its geographic placement on the east coast of Sicily, Italy, in the Mediterranean region, south of mainland Europe and north of northern Africa.\n\n---\n\n#### Figure 2: Nighttime View of Mount Etna's Eruption and Surrounding Cities\n\nThis is a nighttime satellite image taken on March 19, 2017, showing the eruption of Mount Etna (southeastern cone) with visible bright red and orange coloring indicating flowing lava from a lateral vent. The surrounding areas are illuminated by city lights, with the following geographic references labeled:\n\n| Location        | Position in Image         | Visible Characteristics             
       |\n|-----------------|--------------------------|--------------------------------------------|\n| Mt. Etna (southeastern cone) | Top center-left | Bright red/orange lava flow                |\n| Lateral vent    | Left of the volcano       | Faint red/orange flow extending outwards   |\n| Resort          | Below the volcano, to the left   | Small cluster of lights                    |\n| Giarre          | Top right                 | Bright cluster of city lights              |\n| Acireale        | Center right              | Large, bright area of city lights          |\n| Biancavilla     | Bottom left               | Smaller cluster of city lights             |\n\nAn arrow pointing north is shown on the image for orientation.\n\n---\n\n<!-- Earth at Night Page Footer -->\n<!-- Page Number: 50 -->"},{"ref_id":4,"content":"# Volcanoes\n\n## Figure: Satellite Image of Sicily and Mount Etna Lava, March 16, 2017\n\nThe annotated satellite image below shows the island of Sicily and the surrounding region at night, highlighting city lights and volcanic activity.\n\n**Description:**\n\n- **Date of image:** March 16, 2017\n- **Geographical locations labeled:**\n    - Major cities: Palermo (northwest Sicily), Marsala (western Sicily), Catania (eastern Sicily)\n    - Significant feature: Mount Etna, labeled with an adjacent \"hot lava\" region showing the glow from active lava flows\n    - Surrounding water body: Mediterranean Sea\n    - Island: Malta to the south of Sicily\n- **Other details:** \n    - The image is shown at night, with bright spots indicating city lights.\n    - The position of \"hot lava\" near Mount Etna is distinctly visible as a bright spot different from other city lights, indicating volcanic activity.\n    - A scale bar is included showing a reference length of 50 km.\n    - North direction is indicated with an arrow.\n    - Cloud cover is visible in the southwest part of the image, partially obscuring the view near Marsala and Malta.\n\n**Summary of Features Visualized:**\n\n| Feature          | Description                 
                          |\n|------------------|------------------------------------------------------|\n| Cities           | Bright clusters indicating locations: Palermo, Marsala, Catania |\n| Mount Etna       | Marked on the map, located on the eastern side of Sicily, with visible hot lava activity |\n| Malta            | Clearly visible to the south of Sicily               |\n| Water bodies     | Mediterranean Sea labeled                            |\n| Scale & Direction| 50 km scale bar and North indicator                  |\n| Date             | March 16, 2017                     
                  |\n| Cloud Cover      | Visible in the lower left (southern) part of the image |\n\nThis figure demonstrates the visibility of volcanic activity at Mount Etna from space at night, distinguishing the light from hot lava against the background city lights of Sicily and Malta."},{"ref_id":5,"content":"## Nature's Light Shows\n\nAt night, with the light of the Sun removed, nature's brilliant glow from Earth's surface becomes visible to the naked eye from space. Some of Earth's most spectacular light shows are natural, like the aurora borealis, or Northern Lights, in the Northern Hemisphere (aurora australis, or Southern Lights, in the Southern Hemisphere). The auroras are natural electrical phenomena caused by charged particles that race from the Sun toward Earth, inducing chemical reactions in the upper atmosphere and creating the appearance of streamers of reddish or greenish light in the sky, usually near the northern or southern magnetic pole. Other natural lights can indicate danger, like a raging forest fire encroaching on a city, town, or community, or lava spewing from an erupting volcano.\n\nWhatever the source, the ability of humans to monitor nature's light shows at night has practical applications for society. For example, tracking fires during nighttime hours allows for continuous monitoring and enhances our ability to protect humans and other animals, plants, and infrastructure. Combined with other data sources, our ability to observe the light of fires at night allows emergency managers to more efficiently and accurately issue warnings and evacuation orders and allows firefighting efforts to continue through the night. With enough moonlight (e.g., full-Moon phase), it's even possible to track the movement of smoke plumes at night, which can impact air quality, regardless of time of day.\n\nAnother natural source of light at night is emitted from glowing lava flows at the site of active volcanoes. Again, with enough moonlight, these dramatic scenes can be tracked and monitored for both scientific research and public safety.\n\n\n### Figure: The Northern Lights Viewed from Space\n\n**September 17, 2011**\n\nThis photo, taken from the International Space Station on September 17, 2011, shows a spectacular display of the aurora borealis (Northern Lights) as green and reddish light in the night sky above Earth. In the foreground, part of a Soyuz spacecraft is visible, silhouetted against the bright auroral light. The green glow is generated by energetic charged particles from the Sun interacting with Earth's upper atmosphere, exciting oxygen and nitrogen atoms, and producing characteristic colors. The image demonstrates the vividness and grandeur of natural night-time light phenomena as seen from orbit."}]
Activities:
Activity Type: KnowledgeAgentModelQueryPlanningActivityRecord
{
  "InputTokens": 1289,
  "OutputTokens": 116,
  "ElapsedMs": null,
  "Id": 0
}
Activity Type: KnowledgeAgentSearchActivityRecord
{
  "TargetIndex": "earth_at_night",
  "Query": {
    "Search": "How to locate lava flows at night?",
    "Filter": null
  },
  "QueryTime": "2025-06-19T14:02:44.67+00:00",
  "Count": 6,
  "ElapsedMs": 235,
  "Id": 1
}
Activity Type: KnowledgeAgentSemanticRankerActivityRecord
{
  "InputTokens": 24807,
  "ElapsedMs": null,
  "Id": 2
}
Results
Reference Type: KnowledgeAgentAzureSearchDocReference
{
  "DocKey": "earth_at_night_508_page_60_verbalized",
  "SourceData": {},
  "Id": "0",
  "ActivitySource": 1
}
Reference Type: KnowledgeAgentAzureSearchDocReference
{
  "DocKey": "earth_at_night_508_page_64_verbalized",
  "SourceData": {},
  "Id": "1",
  "ActivitySource": 1
}
Reference Type: KnowledgeAgentAzureSearchDocReference
{
  "DocKey": "earth_at_night_508_page_46_verbalized",
  "SourceData": {},
  "Id": "2",
  "ActivitySource": 1
}
Reference Type: KnowledgeAgentAzureSearchDocReference
{
  "DocKey": "earth_at_night_508_page_66_verbalized",
  "SourceData": {},
  "Id": "3",
  "ActivitySource": 1
}
Reference Type: KnowledgeAgentAzureSearchDocReference
{
  "DocKey": "earth_at_night_508_page_65_verbalized",
  "SourceData": {},
  "Id": "4",
  "ActivitySource": 1
}
Reference Type: KnowledgeAgentAzureSearchDocReference
{
  "DocKey": "earth_at_night_508_page_44_verbalized",
  "SourceData": {},
  "Id": "5",
  "ActivitySource": 1
}
[ASSISTANT]: You can find lava at night primarily by using satellite imagery that captures the thermal and visible light emissions from active volcanoes
 Very hot lava emits strong infrared radiation and glows visibly, which can be detected from space, especially when combined with moonlight or other faint light sources
 For example, satellites like Landsat 8 and VIIRS on Suomi NPP have captured nighttime images of lava flows on volcanoes such as Kilauea in Hawaii and Mount Etna in Italy
 These images show bright white-hot areas indicating very hot lava and reddish areas for cooling lava flows (ref_id 0, 1, 3, 4)


Lava glows visibly due to its intense heat, which makes it stand out even at night against the darkness and city lights
 Nighttime satellite images combine thermal infrared wavelengths and near-infrared to distinguish active lava from surrounding cooler ground
 Monitoring these nighttime glows allows scientists to study volcanic activity and also helps with hazard assessment


So, at night, the best way to find lava is through thermal and infrared satellite imagery that detects the glow and heat signatures of lava flows from active volcanoes


References: 0, 1, 3, 4
Search agent 'earth-search-agent' deleted successfully
Index 'earth_at_night' deleted successfully
```

## Explanation of the code

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

In Azure AI Search, an index is a structured collection of data. The following code defines an index named `earth_at_night` to contain plain text and vector content. You can use an existing index, but it must meet the criteria for [agentic retrieval workloads](../../search-agentic-retrieval-how-to-index.md). 

```csharp
// Define the fields for the index
var fields = new List<SearchField>
{
    new SimpleField("id", SearchFieldDataType.String) { IsKey = true, IsFilterable = true, IsSortable = true, IsFacetable = true },
    new SearchField("page_chunk", SearchFieldDataType.String) { IsFilterable = false, IsSortable = false, IsFacetable = false },
    new SearchField("page_embedding_text_3_large", SearchFieldDataType.Collection(SearchFieldDataType.Single)) { VectorSearchDimensions = 3072, VectorSearchProfileName = "hnsw_text_3_large" },
    new SimpleField("page_number", SearchFieldDataType.Int32) { IsFilterable = true, IsSortable = true, IsFacetable = true }
};            
// Define the vectorizer
var vectorizer = new AzureOpenAIVectorizer(vectorizerName: "azure_openai_text_3_large")
{
    Parameters = new AzureOpenAIVectorizerParameters
    {
        ResourceUri = new Uri(azureOpenAIEndpoint),
        DeploymentName = azureOpenAIEmbeddingDeployment,
        ModelName = azureOpenAIEmbeddingModel
    }
};

// Define the vector search profile and algorithm
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

// Define semantic configuration
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
    Configurations =
    {
        semanticConfig
    }
};

// Create the index
var index = new SearchIndex(indexName)
{
    Fields = fields,
    VectorSearch = vectorSearch,
    SemanticSearch = semanticSearch
};

// Create the index client and delete the index if it exists, then create it
var indexClient = new SearchIndexClient(new Uri(endpoint), credential);
try
{
    await indexClient.DeleteIndexAsync(indexName);
    Console.WriteLine($"Index '{indexName}' deleted successfully (if it existed).");
}
catch (Exception ex)
{
    Console.WriteLine($"Index '{indexName}' could not be deleted or did not exist: {ex.Message}");
}
await indexClient.CreateOrUpdateIndexAsync(index);

Console.WriteLine($"Index '{indexName}' created or updated successfully");
```

The index schema contains fields for document identification and page content, embeddings, and numbers. It also includes configurations for semantic ranking and vector queries, which use the `text-embedding-3-large` model you previously deployed.

### Upload documents to the index

Currently, the `earth_at_night` index is empty. Run the following code to populate the index with JSON documents from [NASA's Earth at Night e-book](https://raw.githubusercontent.com/Azure-Samples/azure-search-sample-data/refs/heads/main/nasa-e-book/earth-at-night-json/documents.json). As required by Azure AI Search, each document conforms to the fields and data types defined in the index schema.

```csharp
// Download the documents from the GitHub URL
string url = "https://raw.githubusercontent.com/Azure-Samples/azure-search-sample-data/refs/heads/main/nasa-e-book/earth-at-night-json/documents.json";
var httpClient = new HttpClient();
var response = await httpClient.GetAsync(url);
response.EnsureSuccessStatusCode();
var json = await response.Content.ReadAsStringAsync();

var documents = JsonSerializer.Deserialize<List<Dictionary<string, object>>>(json);
var searchClient = new SearchClient(new Uri(endpoint), indexName, credential);
var searchIndexingBufferedSender = new SearchIndexingBufferedSender<Dictionary<string, object>>(
    searchClient,
    new SearchIndexingBufferedSenderOptions<Dictionary<string, object>>
    {
        KeyFieldAccessor = doc => doc["id"].ToString(),
    }
);

await searchIndexingBufferedSender.UploadDocumentsAsync(documents);
await searchIndexingBufferedSender.FlushAsync();

Console.WriteLine($"Documents uploaded to index '{indexName}'");
```

### Create a knowledge agent

To connect Azure AI Search to your `gpt-4.1-mini` deployment and target the `earth_at_night` index at query time, you need a knowledge agent. The following code defines a knowledge agent named `earth-search-agent` that uses the `KnowledgeAgentAzureOpenAIModel` to process queries and retrieve relevant documents from the `earth_at_night` index.

To ensure relevant and semantically meaningful responses, `DefaultRerankerThreshold` is set to exclude responses with a reranker score of `2.5` or lower.

```csharp
var openAiParameters = new AzureOpenAIVectorizerParameters
{
    ResourceUri = new Uri(azureOpenAIEndpoint),
    DeploymentName = azureOpenAIGptDeployment,
    ModelName = azureOpenAIGptModel
};

var agentModel = new KnowledgeAgentAzureOpenAIModel(azureOpenAIParameters: openAiParameters);

var targetIndex = new KnowledgeAgentTargetIndex(indexName)
{
    DefaultRerankerThreshold = 2.5f
};

// Create the knowledge agent
var agent = new KnowledgeAgent(
    name: agentName,
    models: new[] { agentModel },
    targetIndexes: new[] { targetIndex });
await indexClient.CreateOrUpdateKnowledgeAgentAsync(agent);
Console.WriteLine($"Search agent '{agentName}' created or updated successfully");
```

### Set up messages

Messages are the input for the retrieval route and contain the conversation history. Each message includes a role that indicates its origin, such as assistant or user, and content in natural language. The LLM you use determines which roles are valid.

A user message represents the query to be processed, while an assistant message guides the knowledge agent on how to respond. During the retrieval process, these messages are sent to an LLM to extract relevant responses from indexed documents.

This assistant message instructs `earth-search-agent` to answer questions about the Earth at night, cite sources using their `ref_id`, and respond with "I don't know" when answers are unavailable.

```csharp
string instructions = @"
A Q&A agent that can answer questions about the Earth at night.
Sources have a JSON format with a ref_id that must be cited in the answer.
If you do not have the answer, respond with ""I don't know"".
";

var messages = new List<Dictionary<string, object>>
{
    new Dictionary<string, object>
    {
        { "role", "system" },
        { "content", instructions }
    }
};
```

### Run the retrieval pipeline

This step runs the retrieval pipeline to extract relevant information from your search index. Based on the messages and parameters on the retrieval request, the LLM:
1. Analyzes the entire conversation history to determine the underlying information need.
1. Breaks down the compound user query into focused subqueries.
1. Runs each subquery simultaneously against text fields and vector embeddings in your index.
1. Uses semantic ranker to rerank the results of all subqueries.
1. Merges the results into a single string.

The following code sends a two-part user query to `earth-search-agent`, which deconstructs the query into subqueries, runs the subqueries against both text fields and vector embeddings in the `earth_at_night` index, and ranks and merges the results. The response is then appended to the `messages` list.

```csharp
var agentClient = new KnowledgeAgentRetrievalClient(
    endpoint: new Uri(endpoint),
    agentName: agentName,
    tokenCredential: new DefaultAzureCredential()
);            

messages.Add(new Dictionary<string, object>
{
    { "role", "user" },
    { "content", @"
Why do suburban belts display larger December brightening than urban cores even though absolute light levels are higher downtown?
Why is the Phoenix nighttime street grid is so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?
" }
});

var retrievalResult = await agentClient.RetrieveAsync(
    retrievalRequest: new KnowledgeAgentRetrievalRequest(
            messages: messages
                .Where(message => message["role"].ToString() != "system")
                .Select(
                message => new KnowledgeAgentMessage(
                    role: message["role"].ToString(),
                    content: new[] { new KnowledgeAgentMessageTextContent(message["content"].ToString()) }))
                .ToList()
            )
        {
            TargetIndexParams = { new KnowledgeAgentIndexParams { IndexName = indexName, RerankerThreshold = 2.5f } }
        }
    );

messages.Add(new Dictionary<string, object>
{
    { "role", "assistant" },
    { "content", (retrievalResult.Value.Response[0].Content[0] as KnowledgeAgentMessageTextContent).Text }
});
```

### Review the response, activity, and results

Now you want to display the response, activity, and results of the retrieval pipeline.

Each retrieval response from Azure AI Search includes:

+ A unified string that represents grounding data from the search results.

+ The query plan.

+ Reference data that shows which chunks of the source documents contributed to the unified string.

```csharp
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

Console.WriteLine("Results");
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

The output should include:

+ `Response` provides a text string of the most relevant documents (or chunks) in the search index based on the user query. As shown later in this quickstart, you can pass this string to an LLM for answer generation.

+ `Activity` tracks the steps that were taken during the retrieval process, including the subqueries generated by your `gpt-4.1-mini` deployment and the tokens used for query planning and execution.

+ `Results` lists the documents that contributed to the response, each one identified by their `DocKey`.

### Create the Azure OpenAI client

To extend the retrieval pipeline from answer *extraction* to answer *generation*, set up the Azure OpenAI client to interact with your `gpt-4.1-mini` deployment, which you specified using the `answer_model` variable in a previous section.

```csharp
AzureOpenAIClient azureClient = new(
    new Uri(azureOpenAIEndpoint),
    new DefaultAzureCredential());
```

### Use the Chat Completions API to generate an answer

One option for answer generation is the Chat Completions API, which passes the conversation history to the LLM for processing.

```csharp
ChatClient chatClient = azureClient.GetChatClient(azureOpenAIGptDeployment);            
List<ChatMessage> chatMessages = messages
    .Select<Dictionary<string, object>, ChatMessage>(m => m["role"].ToString() switch
    {
        "user" => new UserChatMessage(m["content"].ToString()),
        "assistant" => new AssistantChatMessage(m["content"].ToString()),
        "system" => new SystemChatMessage(m["content"].ToString()),
        _ => null
    })
    .Where(m => m != null)
    .ToList();


var result = await chatClient.CompleteChatAsync(chatMessages);

Console.WriteLine($"[ASSISTANT]: {result.Value.Content[0].Text.Replace(".", "\n")}");
```

### Continue the conversation

Continue the conversation by sending another user query to `earth-search-agent`. The following code reruns the retrieval pipeline, fetching relevant content from the `earth_at_night` index and appending the response to the `messages` list. However, unlike before, you can now use the Azure OpenAI client to generate an answer based on the retrieved content.

```csharp
messages.Add(new Dictionary<string, object>
{
    { "role", "user" },
    { "content", "How do I find lava at night?" }
});

var retrievalResult2 = await agentClient.RetrieveAsync(
    retrievalRequest: new KnowledgeAgentRetrievalRequest(
            messages: messages
                .Where(message => message["role"].ToString() != "system")
                .Select(
                message => new KnowledgeAgentMessage(
                    role: message["role"].ToString(),
                    content: new[] { new KnowledgeAgentMessageTextContent(message["content"].ToString()) }))
                .ToList()
            )
        {
            TargetIndexParams = { new KnowledgeAgentIndexParams { IndexName = indexName, RerankerThreshold = 2.5f } }
        }
    );

messages.Add(new Dictionary<string, object>
{
    { "role", "assistant" },
    { "content", (retrievalResult2.Value.Response[0].Content[0] as KnowledgeAgentMessageTextContent).Text }
});
```

## Clean up resources

When working in your own subscription, it's a good idea to finish a project by determining whether you still need the resources you created. Resources that are left running can cost you money. You can delete resources individually, or you can delete the resource group to delete the entire set of resources.

In the Azure portal, you can find and manage resources by selecting **All resources** or **Resource groups** from the left pane. You can also run the following code to delete the objects you created in this quickstart.

### Delete the knowledge agent

The knowledge agent created in this quickstart was deleted using the following code snippet from *Program.cs*:

```csharp
await indexClient.DeleteKnowledgeAgentAsync(agentName);
Console.WriteLine($"Search agent '{agentName}' deleted successfully");
```

### Delete the search index

The search index created in this quickstart was deleted using the following code snippet from *Program.cs*:

```csharp
await indexClient.DeleteIndexAsync(indexName);
Console.WriteLine($"Index '{indexName}' deleted successfully");        
```

