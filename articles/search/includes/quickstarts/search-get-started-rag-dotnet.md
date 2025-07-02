---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 06/05/2025
---
## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

- An [Azure OpenAI resource](/azure/ai-services/openai/how-to/create-resource).
  - [Choose a region](/azure/ai-services/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions#global-standard-model-availability) that supports the chat completion model you want to use (gpt-4o, gpt-4o-mini, or an equivalent model).
  - [Deploy the chat completion model](/azure/ai-foundry/how-to/deploy-models-openai) in Azure AI Foundry or [use another approach](/azure/ai-services/openai/how-to/working-with-models).
- An [Azure AI Search resource](../../search-create-service-portal.md).
  - We recommend using the Basic tier or higher.
  - [Enable semantic ranking](../../semantic-how-to-enable-disable.md).
- [Visual Studio Code](https://code.visualstudio.com/download) with the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and the [Jupyter package](https://pypi.org/project/jupyter/). For more information, see [Python in Visual Studio Code](https://code.visualstudio.com/docs/languages/python).

## Configure access

Requests to the search endpoint must be authenticated and authorized. You can use API keys or roles for this task. Keys are easier to start with, but roles are more secure. This quickstart assumes roles.

You're setting up two clients, so you need permissions on both resources.

Azure AI Search is receiving the query request from your local system. Assign yourself the **Search Index Data Reader** role assignment if the hotels sample index already exists. If it doesn't exist, assign yourself **Search Service Contributor** and **Search Index Data Contributor** roles so that you can create and query the index.

Azure OpenAI is receiving the query and the search results from your local system. Assign yourself the **Cognitive Services OpenAI User** role on Azure OpenAI.

1. Sign in to the [Azure portal](https://portal.azure.com).

1. Configure Azure AI Search for role-based access:

    1. In the Azure portal, find your Azure AI Search service.

    1. On the left menu, select **Settings** > **Keys**, and then select either **Role-based access control** or **Both**.

1. Assign roles:

    1. On the left menu, select **Access control (IAM)**.

    1. On Azure AI Search, select these roles to create, load, and query a search index, and then assign them to your Microsoft Entra ID user identity:

       - **Search Index Data Contributor**
       - **Search Service Contributor**

    1. On Azure OpenAI, select **Access control (IAM)** to assign this role to yourself on Azure OpenAI:

       - **Cognitive Services OpenAI User**

It can take several minutes for permissions to take effect.

## Create an index

A search index provides grounding data for the chat model. We recommend the hotels-sample-index, which can be created in minutes and runs on any search service tier. This index is created using built-in sample data.

1. In the Azure portal, [find your search service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices).

1. On the **Overview** home page, select [**Import data**](../../search-get-started-portal.md) to start the wizard.

1. On the **Connect to your data** page, select **Samples** from the dropdown list.

1. Choose the **hotels-sample**.

1. Select **Next** through the remaining pages, accepting the default values.

1. Once the index is created, select **Search management** > **Indexes** from the left menu to open the index.

1. Select **Edit JSON**. 

1. Scroll to the end of the index, where you can find placeholders for constructs that can be added to an index.

   ```json
   "analyzers": [],
   "tokenizers": [],
   "tokenFilters": [],
   "charFilters": [],
   "normalizers": [],
   ```

1. On a new line after "normalizers", paste in the following semantic configuration. This example specifies a `"defaultConfiguration"`, which is important to the running of this quickstart.

    ```json
    "semantic":{
       "defaultConfiguration":"semantic-config",
       "configurations":[
          {
             "name":"semantic-config",
             "prioritizedFields":{
                "titleField":{
                   "fieldName":"HotelName"
                },
                "prioritizedContentFields":[
                   {
                      "fieldName":"Description"
                   }
                ],
                "prioritizedKeywordsFields":[
                   {
                      "fieldName":"Category"
                   },
                   {
                      "fieldName":"Tags"
                   }
                ]
             }
          }
       ]
    },
    ```

1. **Save** your changes.

1. Run the following query in [Search Explorer](../../search-explorer.md) to test your index: `complimentary breakfast`.

   Output should look similar to the following example. Results that are returned directly from the search engine consist of fields and their verbatim values, along with metadata like a search score and a semantic ranking score and caption if you use semantic ranker. We used a [select statement](../../search-query-odata-select.md) to return just the HotelName, Description, and Tags fields.

   ```
   {
   "@odata.count": 18,
   "@search.answers": [],
   "value": [
      {
         "@search.score": 2.2896252,
         "@search.rerankerScore": 2.506816864013672,
         "@search.captions": [
         {
            "text": "Head Wind Resort. Suite. coffee in lobby\r\nfree wifi\r\nview. The best of old town hospitality combined with views of the river and cool breezes off the prairie. Our penthouse suites offer views for miles and the rooftop plaza is open to all guests from sunset to 10 p.m. Enjoy a **complimentary continental breakfast** in the lobby, and free Wi-Fi throughout the hotel..",
            "highlights": ""
         }
         ],
         "HotelName": "Head Wind Resort",
         "Description": "The best of old town hospitality combined with views of the river and cool breezes off the prairie. Our penthouse suites offer views for miles and the rooftop plaza is open to all guests from sunset to 10 p.m. Enjoy a complimentary continental breakfast in the lobby, and free Wi-Fi throughout the hotel.",
         "Tags": [
         "coffee in lobby",
         "free wifi",
         "view"
         ]
      },
      {
         "@search.score": 2.2158256,
         "@search.rerankerScore": 2.288334846496582,
         "@search.captions": [
         {
            "text": "Swan Bird Lake Inn. Budget. continental breakfast\r\nfree wifi\r\n24-hour front desk service. We serve a continental-style breakfast each morning, featuring a variety of food and drinks. Our locally made, oh-so-soft, caramel cinnamon rolls are a favorite with our guests. Other breakfast items include coffee, orange juice, milk, cereal, instant oatmeal, bagels, and muffins..",
            "highlights": ""
         }
         ],
         "HotelName": "Swan Bird Lake Inn",
         "Description": "We serve a continental-style breakfast each morning, featuring a variety of food and drinks. Our locally made, oh-so-soft, caramel cinnamon rolls are a favorite with our guests. Other breakfast items include coffee, orange juice, milk, cereal, instant oatmeal, bagels, and muffins.",
         "Tags": [
         "continental breakfast",
         "free wifi",
         "24-hour front desk service"
         ]
      },
      {
         "@search.score": 0.92481667,
         "@search.rerankerScore": 2.221315860748291,
         "@search.captions": [
         {
            "text": "White Mountain Lodge & Suites. Resort and Spa. continental breakfast\r\npool\r\nrestaurant. Live amongst the trees in the heart of the forest. Hike along our extensive trail system. Visit the Natural Hot Springs, or enjoy our signature hot stone massage in the Cathedral of Firs. Relax in the meditation gardens, or join new friends around the communal firepit. Weekend evening entertainment on the patio features special guest musicians or poetry readings..",
            "highlights": ""
         }
         ],
         "HotelName": "White Mountain Lodge & Suites",
         "Description": "Live amongst the trees in the heart of the forest. Hike along our extensive trail system. Visit the Natural Hot Springs, or enjoy our signature hot stone massage in the Cathedral of Firs. Relax in the meditation gardens, or join new friends around the communal firepit. Weekend evening entertainment on the patio features special guest musicians or poetry readings.",
         "Tags": [
         "continental breakfast",
         "pool",
         "restaurant"
         ]
      },
      . . .
   ]}
   ```

## Get service endpoints

In the remaining sections, you set up API calls to Azure OpenAI and Azure AI Search. Get the service endpoints so that you can provide them as variables in your code.

1. Sign in to the [Azure portal](https://portal.azure.com).

1. [Find your search service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices).

1. On the **Overview** home page, copy the URL. An example endpoint might look like `https://example.search.windows.net`. 

1. [Find your Azure OpenAI service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.CognitiveServices%2Faccounts).

1. On the **Overview** home page, select the link to view the endpoints. Copy the URL. An example endpoint might look like `https://example.openai.azure.com/`.

## Sign in to Azure

You're using Microsoft Entra ID and role assignments for the connection. Make sure you're logged in to the same tenant and subscription as Azure AI Search and Azure OpenAI. You can use the Azure CLI on the command line to show current properties, change properties, and to sign in. For more information, see [Connect without keys](../../search-get-started-rbac.md). 

Run each of the following commands in sequence.

```azure-cli
az account show

az account set --subscription <PUT YOUR SUBSCRIPTION ID HERE>

az login --tenant <PUT YOUR TENANT ID HERE>
```

You should now be logged in to Azure from your local device.

## Create the .NET app

Complete the following steps to create a .NET console app to connect to an AI model.

1. In an empty directory on your computer, use the `dotnet new` command to create a new console app:

    ```dotnetcli
    dotnet new console -o AISearchRag
    ```

1. Change directory into the app folder:

    ```dotnetcli
    cd AISearchRag
    ```

1. Install the required packages:

    ```bash
    dotnet add package Azure.AI.OpenAI
    dotnet add package Azure.Identity
    dotnet add package Azure.Search.Documents
    ```

1. Open the app in Visual Studio Code (or your editor of choice).

    ```bash
    code .
    ```

## Set up the query and chat thread

Add the following code to connect to and query the Azure AI Search and Azure OpenAI services.

```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Azure.Identity;
using Azure.Search.Documents;
using Azure.Search.Documents.Models;
using Azure.AI.OpenAI;
using OpenAI.Chat;

// Azure resource endpoints and deployment info
string azureSearchService = "<your-ai-search-endpoint>";
string azureOpenAIAccount = "<your-openai-endpoint";
string azureDeploymentModel = "<openai-deployment-name>";
string indexName = "hotels-sample-index";

// Authenticate using DefaultAzureCredential
var credential = new DefaultAzureCredential();

// Create the Azure Search client
var searchClient = new SearchClient(new Uri(azureSearchService), indexName, credential);

// Create the Azure OpenAI client
var openAIClient = new AzureOpenAIClient(new Uri(azureOpenAIAccount), credential);

// Prompt template for grounding the LLM response in search results
string GROUNDED_PROMPT = @"You are a friendly assistant that recommends hotels based on activities and amenities.
    Answer the query using only the sources provided below in a friendly and concise bulleted manner
    Answer ONLY with the facts listed in the list of sources below.
    If there isn't enough information below, say you don't know.
    Do not generate answers that don't use the sources below.
    Query: {0}
    Sources: {1}";

// The user's query
string query = "Can you recommend a few hotels with complimentary breakfast?";

// Configure search options: top 5 results, select relevant fields
var options = new SearchOptions { Size = 5 };
options.Select.Add("Description");
options.Select.Add("HotelName");
options.Select.Add("Tags");

// Execute the search
var searchResults = await searchClient.SearchAsync<SearchDocument>(query, options);
var sources = new List<string>();
await foreach (var result in searchResults.Value.GetResultsAsync())
{
    var doc = result.Document;
    // Format each result as: HotelName:Description:Tags
    sources.Add($"{doc["HotelName"]}:{doc["Description"]}:{doc["Tags"]}");
}
string sourcesFormatted = string.Join("\n", sources);

// Format the prompt with the query and sources
string formattedPrompt = string.Format(GROUNDED_PROMPT, query, sourcesFormatted);

// Create a chat client for the specified deployment/model
ChatClient chatClient = openAIClient.GetChatClient(azureDeploymentModel);

// Send the prompt to the LLM and stream the response
var chatUpdates = chatClient.CompleteChatStreamingAsync(
    [ new UserChatMessage(formattedPrompt) ]
);

// Print the streaming response to the console
await foreach (var chatUpdate in chatUpdates)
{
    if (chatUpdate.Role.HasValue)
    {
        Console.Write($"{chatUpdate.Role} : ");
    }
    foreach (var contentPart in chatUpdate.ContentUpdate)
    {
        Console.Write(contentPart.Text);
    }
}
```

The output from Azure OpenAI consists of recommendations for several hotels, such as the following example:

```output
Sure! Here are a few hotels that offer complimentary breakfast:

- **Head Wind Resort**
- Complimentary continental breakfast in the lobby
- Free Wi-Fi throughout the hotel

- **Double Sanctuary Resort**
- Continental breakfast included

- **White Mountain Lodge & Suites**
- Continental breakfast available

- **Swan Bird Lake Inn**
- Continental-style breakfast each morning with a variety of food and drinks 
   such as caramel cinnamon rolls, coffee, orange juice, milk, cereal, 
   instant oatmeal, bagels, and muffins
```

If you get a **Forbidden** error message, check Azure AI Search configuration to make sure role-based access is enabled.

If you get an **Authorization failed** error message, wait a few minutes and try again. It can take several minutes for role assignments to become operational.

If you get a **Resource not found** error message, check the resource URIs and make sure the API version on the chat model is valid.

Otherwise, to experiment further, change the query and rerun the last step to better understand how the model works with the grounding data.

You can also modify the prompt to change the tone or structure of the output.

## Send a complex RAG query

Azure AI Search supports [complex types](../../search-howto-complex-data-types.md) for nested JSON structures. In the hotels-sample-index, `Address` is an example of a complex type, consisting of `Address.StreetAddress`, `Address.City`, `Address.StateProvince`, `Address.PostalCode`, and `Address.Country`. The index also has complex collection of `Rooms` for each hotel.

If your index has complex types, your query can provide those fields if you first convert the search results output to JSON, and then pass the JSON to the chat model.

The following example updates the user prompt and adds complex types to the request:

```csharp
// The user's query
var query = "Can you recommend a few hotels that offer complimentary breakfast? Tell me their description, address, tags, and the rate for one room that sleeps 4 people.";

// Define the fields to select from the search index
var selectedFields = new[] { "HotelName", "Description", "Address", "Rooms", "Tags" };

// Configure search options: top 5 results, select relevant fields
var options = new SearchOptions { Size = 5 };
foreach(var field in selectedFields)
{
    options.Select.Add(field);
}

// Execute the search
var searchResults = await searchClient.SearchAsync<SearchDocument>(query, options);

// Filter and format the sources
var sourcesFiltered = new List<Dictionary<string, object>>();
await foreach (var result in searchResults.Value.GetResultsAsync())
{
    var filtered = new Dictionary<string, object>();
    foreach (var field in selectedFields)
    {
        if (result.Document.TryGetValue(field, out var value))
        {
            filtered[field] = value;
        }
    }
    sourcesFiltered.Add(filtered);
}
var sourcesFormatted = string.Join("\n", sourcesFiltered.ConvertAll(source => JsonSerializer.Serialize(source)));

// Format the prompt with the query and sources
string formattedPrompt = string.Format(GROUNDED_PROMPT, query, sourcesFormatted);

// Create a chat client for the specified deployment/model
ChatClient chatClient = openAIClient.GetChatClient(azureDeploymentModel);

// Send the prompt to the LLM and stream the response
var chatUpdates = chatClient.CompleteChatStreamingAsync(
    [ new UserChatMessage(formattedPrompt) ]
);

// Print the streaming response to the console
await foreach (var chatUpdate in chatUpdates)
{
    if (chatUpdate.Role.HasValue)
    {
        Console.Write($"{chatUpdate.Role} : ");
    }
    foreach (var contentPart in chatUpdate.ContentUpdate)
    {
        Console.Write(contentPart.Text);
    }
}
```

The output from Azure OpenAI consists of recommendations for several hotels, such as the following example:

```output
1. **Double Sanctuary Resort**
   - **Description**: 5-star luxury hotel with the biggest rooms in the city. Recognized as the #1 hotel in the area by Traveler magazine. Features include free WiFi, flexible check-in/out, a fitness center, and in-room espresso.
   - **Address**: 2211 Elliott Ave, Seattle, WA, 98121, USA
   - **Tags**: view, pool, restaurant, bar, continental breakfast
   - **Room Rate for 4 People**: 
     - Suite, 2 Queen Beds: $254.99 per night

2. **Starlight Suites**
   - **Description**: Spacious all-suite hotel with complimentary airport shuttle and WiFi. Facilities include an indoor/outdoor pool, fitness center, and Florida Green certification. Complimentary coffee and HDTV are also available.
   - **Address**: 19575 Biscayne Blvd, Aventura, FL, 33180, USA
   - **Tags**: pool, coffee in lobby, free wifi
   - **Room Rate for 4 People**:
     - Suite, 2 Queen Beds (Cityside): $231.99 per night
     - Deluxe Room, 2 Queen Beds (Waterfront View): $148.99 per night

3. **Good Business Hotel**
   - **Description**: Located one mile from the airport with free WiFi, an outdoor pool, and a complimentary airport shuttle. Close proximity to Lake Lanier and downtown. The business center includes printers, a copy machine, fax, and a work area.
   - **Address**: 4400 Ashford Dunwoody Rd NE, Atlanta, GA, 30346, USA
   - **Tags**: pool, continental breakfast, free parking
   - **Room Rate for 4 People**:
     - Budget Room, 2 Queen Beds (Amenities): $60.99 per night
     - Deluxe Room, 2 Queen Beds (Amenities): $139.99 per night
```

## Troubleshooting errors

If you see output messages while debugging related to `ManagedIdentityCredential` and token acquisition failures, it could be that you have multiple tenants, and your Azure sign-in is using a tenant that doesn't have your search service. To get your tenant ID, search the Azure portal for "tenant properties" or run `az login tenant list`.

Once you have your tenant ID, run `az login --tenant <YOUR-TENANT-ID>` at a command prompt, and then rerun the script.

You can also log errors in your code by creating an instance of `ILogger`:

```csharp
using var loggerFactory = LoggerFactory.Create(builder =>
{
   builder.AddConsole();
});
ILogger logger = loggerFactory.CreateLogger<Program>();
```

## Clean up

When you're working in your own subscription, it's a good idea at the end of a project to identify whether you still need the resources you created. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

You can find and manage resources in the Azure portal by using the **All resources** or **Resource groups** link in the leftmost pane.

