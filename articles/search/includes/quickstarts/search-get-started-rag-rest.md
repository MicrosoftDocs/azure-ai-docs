---
manager: nitinme
author: heidisteen
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 08/27/2025
---

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

- An [Azure OpenAI resource](/azure/ai-services/openai/how-to/create-resource).
  - [Choose a region](/azure/ai-services/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions#global-standard-model-availability) that supports the chat completion model you want to use (gpt-4o, gpt-4o-mini, or an equivalent model).
  - [Deploy the chat completion model](/azure/ai-foundry/how-to/deploy-models-openai) in Microsoft Foundry or [use another approach](/azure/ai-services/openai/how-to/working-with-models).
- An [Azure AI Search resource](../../search-create-service-portal.md).
  - We recommend using the Basic tier or higher.
  - [Enable semantic ranking](../../semantic-how-to-enable-disable.md).

- A [new or existing index](../../search-how-to-create-search-index.md) with descriptive or verbose text fields, attributed as retrievable in your index. This quickstart assumes the [hotels-sample-index](../../search-get-started-portal.md).

- The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

- [Visual Studio Code](https://code.visualstudio.com/download) with the [REST client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) .

## Download file

[Download a .rest file](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/Quickstart-RAG) from GitHub to send the requests in this quickstart. For more information, see [Downloading files from GitHub](https://docs.github.com/get-started/start-your-journey/downloading-files-from-github).

You can also start a new file on your local system and create requests manually by using the instructions in this article.

## Configure access

Requests to the search endpoint must be authenticated and authorized. You can use [API keys](../../search-security-api-keys.md) or roles for this task. Keys are easier to start with, but roles are more secure. This quickstart assumes roles.

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

## Get service endpoints and tokens

In the remaining sections, you set up API calls to Azure OpenAI and Azure AI Search. Get the service endpoints and tokens so that you can provide them as variables in your code.

1. Sign in to the [Azure portal](https://portal.azure.com).

1. [Find your search service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices).

1. On the **Overview** home page, copy the URL. An example endpoint might look like `https://example.search.windows.net`. 

1. [Find your Azure OpenAI service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.CognitiveServices%2Faccounts).

1. On the **Overview** home page, select the link to view the endpoints. Copy the URL. An example endpoint might look like `https://example.openai.azure.com/`.

1. Get personal access tokens from the Azure CLI on a command prompt. Here are the commands for each resource:

   - `az account get-access-token --resource https://search.azure.com --query "accessToken" -o tsv`
   - `az account get-access-token --resource https://cognitiveservices.azure.com --query "accessToken" -o tsv`

## Set up the client

In this quickstart, you use a REST client and the [Azure AI Search REST APIs](/rest/api/searchservice) to implement the RAG pattern.

We recommend [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for this quickstart.

> [!TIP]
> You can [download the source code](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/Quickstart-rag) to start with a finished project or follow these steps to create your own. 

1. Start Visual Studio Code and open the [quickstart-rag.rest](https://github.com/Azure-Samples/azure-search-rest-samples/blob/main/Quickstart-RAG/rag.rest) file or create a new file.

1. At the top, set environment variables for your search service, authorization, and index name.

   - For @searchUrl, paste in the search endpoint.
   - For @aoaiUrl, paste in the Azure OpenAI endpoint.
   - For @searchAccessToken, paste in the access token scoped to `https://search.azure.com`.
   - For @aoaiAccessToken, paste in the access token scoped to `https://cognitiveservices.azure.com`.

1. To test the connection, send your first request.

   ```http
   ### List existing indexes by name (verify the connection)
    GET  {{searchUrl}}/indexes?api-version=2025-11-01-preview&$select=name  HTTP/1.1
    Authorization: Bearer {{personalAccessToken}}
   ```

1. Select **Sent request**.

   :::image type="content" source="../../media/search-get-started-semantic/visual-studio-code-send-request.png" alt-text="Screenshot of the REST client send request link.":::

1. Output for this GET request should be a list of indexes. You should see the **hotels-sample-index** among them.

## Set up the query and chat thread

This section uses Visual Studio Code and REST to call the chat completion APIs on Azure OpenAI.

1. Set up a query request on the phrase *"Can you recommend a few hotels with complimentary breakfast?"*. This query uses semantic ranking to return relevant matches, even if the verbatim text isn't an exact match. Results are held in the **searchRequest** variable for reuse on the next request.

   ```http
   # @name searchRequest
    POST {{searchUrl}}/indexes/{{index-name}}/docs/search?api-version={{api-version}} HTTP/1.1
    Content-Type: application/json
    Authorization: Bearer {{searchAccessToken}}
    
    {
      "search": "Can you recommend a few hotels with complimentary breakfast?",
      "queryType": "semantic",
      "semanticConfiguration": "semantic-config",
      "select": "Description,HotelName,Tags",
      "top": 5
    }
    
    ### 3 - Use search results in Azure OpenAI call to a chat completion model
    POST {{aoaiUrl}}/openai/deployments/{{aoaiGptDeployment}}/chat/completions?api-version=2024-08-01-preview HTTP/1.1
    Content-Type: application/json
    Authorization: Bearer {{aoaiAccessToken}}
    
    {
      "messages": [
        {
          "role": "system", 
          "content": "You recommend hotels based on activities and amenities. Answer the query using only the search result. Answer in a friendly and concise manner. Answer ONLY with the facts provided. If there isn't enough information below, say you don't know."
        },
        {
          "role": "user",
          "content": "Based on the hotel search results, can you recommend hotels with breakfast? Here are all the hotels I found:\n\nHotel 1: {{searchRequest.response.body.value[0].HotelName}}\nDescription: {{searchRequest.response.body.value[0].Description}}\n\nHotel 2: {{searchRequest.response.body.value[1].HotelName}}\nDescription: {{searchRequest.response.body.value[1].Description}}\n\nHotel 3: {{searchRequest.response.body.value[2].HotelName}}\nDescription: {{searchRequest.response.body.value[2].Description}}\n\nHotel 4: {{searchRequest.response.body.value[3].HotelName}}\nDescription: {{searchRequest.response.body.value[3].Description}}\n\nHotel 5: {{searchRequest.response.body.value[4].HotelName}}\nDescription: {{searchRequest.response.body.value[4].Description}}\n\nPlease recommend which hotels offer breakfast based on their descriptions."
        }
      ],
      "max_tokens": 1000,
      "temperature": 0.7
    }`
    ```

1. **Send** the request.

1. Output should look similar to the following example:

   ```json
      "value": [
        {
          "@search.score": 3.9269178,
          "@search.rerankerScore": 2.380699872970581,
          "HotelName": "Head Wind Resort",
          "Description": "The best of old town hospitality combined with views of the river and cool breezes off the prairie. Our penthouse suites offer views for miles and the rooftop plaza is open to all guests from sunset to 10 p.m. Enjoy a complimentary continental breakfast in the lobby, and free Wi-Fi throughout the hotel.",
          "Tags": [
            "coffee in lobby",
            "free wifi",
            "view"
          ]
        },
        {
          "@search.score": 1.5450059,
          "@search.rerankerScore": 2.1258809566497803,
          "HotelName": "Thunderbird Motel",
          "Description": "Book Now & Save. Clean, Comfortable rooms at the lowest price. Enjoy complimentary coffee and tea in common areas.",
          "Tags": [
            "coffee in lobby",
            "free parking",
            "free wifi"
          ]
        },
        {
          "@search.score": 2.2158256,
          "@search.rerankerScore": 2.121671438217163,
          "HotelName": "Swan Bird Lake Inn",
          "Description": "We serve a continental-style breakfast each morning, featuring a variety of food and drinks. Our locally made, oh-so-soft, caramel cinnamon rolls are a favorite with our guests. Other breakfast items include coffee, orange juice, milk, cereal, instant oatmeal, bagels, and muffins.",
          "Tags": [
            "continental breakfast",
            "free wifi",
            "24-hour front desk service"
          ]
        },
        {
          "@search.score": 0.6395861,
          "@search.rerankerScore": 2.116753339767456,
          "HotelName": "Waterfront Scottish Inn",
          "Description": "Newly Redesigned Rooms & airport shuttle. Minutes from the airport, enjoy lakeside amenities, a resort-style pool & stylish new guestrooms with Internet TVs.",
          "Tags": [
            "24-hour front desk service",
            "continental breakfast",
            "free wifi"
          ]
        },
        {
          "@search.score": 4.885111,
          "@search.rerankerScore": 2.0008862018585205,
          "HotelName": "Double Sanctuary Resort",
          "Description": "5 star Luxury Hotel - Biggest Rooms in the city. #1 Hotel in the area listed by Traveler magazine. Free WiFi, Flexible check in/out, Fitness Center & espresso in room.",
          "Tags": [
            "view",
            "pool",
            "restaurant",
            "bar",
            "continental breakfast"
          ]
        }
      ]
    ```

1. Set up a conversation turn with a chat completion model. This request includes a prompt that provides instructions for the response. The `max_tokens` value is large enough to accommodate the search results from the previous query.

   ```http
    POST {{aoaiUrl}}/openai/deployments/{{aoaiGptDeployment}}/chat/completions?api-version=2024-08-01-preview HTTP/1.1
    Content-Type: application/json
    Authorization: Bearer {{aoaiAccessToken}}
    
    {
    "messages": [
    {
      "role": "system", 
      "content": "You  are a friendly assistant that recommends hotels based on activities and amenities. Answer the query using only the search result. Answer in a friendly and concise manner. Answer ONLY with the facts provided. If there isn't enough information below, say you don't know."
        },
    {
      "role": "user",
      "content": "Based on the hotel search results, can you recommend hotels with breakfast? Here are all the hotels I found:\n\nHotel 1: {{searchRequest.response.body.value[0].HotelName}}\nDescription: {{searchRequest.response.body.value[0].Description}}\n\nHotel 2: {{searchRequest.response.body.value[1].HotelName}}\nDescription: {{searchRequest.response.body.value[1].Description}}\n\nHotel 3: {{searchRequest.response.body.value[2].HotelName}}\nDescription: {{searchRequest.response.body.value[2].Description}}\n\nHotel 4: {{searchRequest.response.body.value[3].HotelName}}\nDescription: {{searchRequest.response.body.value[3].Description}}\n\nHotel 5: {{searchRequest.response.body.value[4].HotelName}}\nDescription: {{searchRequest.response.body.value[4].Description}}\n\nPlease recommend which hotels offer breakfast based on their descriptions."
    }
    ],
    "max_tokens": 1000,
    "temperature": 0.7
    }
    ```

1. **Send** the request.

1. Output should be an HTTP 200 Success status message. Included in the output is content that answers the question:

   ```json
    "message": {
      "annotations": [],
      "content": "I recommend the following hotels that offer breakfast:\n\n1. **Head Wind Resort** - Offers a complimentary continental breakfast in the lobby.\n2. **Swan Bird Lake Inn** - Serves a continental-style breakfast each morning, including a variety of food and drinks. \n\nEnjoy your stay!",
      "refusal": null,
      "role": "assistant"
    }
    ```

Notice that the output is missing several hotels that mention breakfast in the Tags field. The Tags field is an array, and including this field breaks the JSON structure in the results. Because there are no string conversion capabilities in the REST client, extra code for manually converting the JSON to a string is required if arrays are to be included. We omit this step for this quickstart.

## Clean up

When you're working in your own subscription, it's a good idea at the end of a project to identify whether you still need the resources you created. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

You can find and manage resources in the Azure portal by using the **All resources** or **Resource groups** link in the leftmost pane.
