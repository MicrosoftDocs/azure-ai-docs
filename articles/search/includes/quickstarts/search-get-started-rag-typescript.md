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
- [Visual Studio Code](https://code.visualstudio.com/download).
- [Node.JS with LTS](https://nodejs.org/en/download/).
- [TypeScript](https://www.typescriptlang.org/download). You can globally install TypeScript using npm:

   ```bash
   npm install -g typescript
   ```


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

## Set up environment variables for local development

1. Create a `.env` file.
1. Add the following environment variables to the `.env` file, replacing the values with your own service endpoints and keys.

   ```plaintext
   AZURE_SEARCH_ENDPOINT=<YOUR AZURE AI SEARCH ENDPOINT>
   AZURE_SEARCH_INDEX_NAME=hotels-sample-index

   AZURE_OPENAI_ENDPOINT=<YOUR AZURE OPENAI ENDPOINT>
   AZURE_OPENAI_VERSION=<YOUR AZURE OPENAI API VERSION>
   AZURE_DEPLOYMENT_MODEL=<YOUR DEPLOYMENT NAME>
   ```

## Set up the Node.JS project

Setup project with Visual Studio Code and TypeScript.

1. Start Visual Studio Code in a new directory.

   ```bash
   mkdir rag-quickstart && cd rag-quickstart
   code .
   ```
1. Create a new package for ESM modules in your project directory.

   ```bash
   npm init -y
   npm pkg set type=module
   ```

   This creates a `package.json` file with default values.

1. Install the following npm packages.

   ```bash
   npm install @azure/identity @azure/search-documents openai dotenv @types/node
   ``` 

1. Create a `src` directory in your project directory.

   ```bash
   mkdir src
   ```

1. Create a `tsconfig.json` file in the project directory for ESM with the following content.

    ```json
    {
      "compilerOptions": {
        "target": "esnext",
        "module": "NodeNext",
        "moduleResolution": "nodenext",
        "rootDir": "./src",
        "outDir": "./dist/",
        "esModuleInterop": true,
        "forceConsistentCasingInFileNames": true,
        "strict": true,
        "skipLibCheck": true,
        "declaration": true,
        "sourceMap": true,
        "resolveJsonModule": true,
        "moduleDetection": "force", // Add this for ESM
        "allowSyntheticDefaultImports": true // Helpful for ESM interop
      },
      "include": [
        "src/**/*.ts"
      ]
    }
   ```

## Sign in to Azure

You're using Microsoft Entra ID and role assignments for the connection. Make sure you're logged in to the same tenant and subscription as Azure AI Search and Azure OpenAI. You can use the Azure CLI on the command line to show current properties, change properties, and to sign in. For more information, see [Connect without keys](../../search-get-started-rbac.md). 

Run each of the following commands in sequence.

```azure-cli
az account show

az account set --subscription <PUT YOUR SUBSCRIPTION ID HERE>

az login --tenant <PUT YOUR TENANT ID HERE>
```

You should now be logged in to Azure from your local device.

## Set up query and chat thread

Create a query script that uses the Azure AI Search index and the chat model to generate responses based on grounding data. The following steps guide you through setting up the query script.


1. Create a `query.ts` file in the `src` directory with the following code.

    :::code language="typescript" source="~/azure-search-javascript-samples/quickstart-rag-ts/src/query.ts" :::



    The preceding code does the following:
    - Imports the necessary libraries for Azure AI Search and Azure OpenAI.
    - Uses environment variables to configure the Azure AI Search and Azure OpenAI clients.
    - Defines a function to get the clients for Azure AI Search and Azure OpenAI, using environment variables for configuration.
    - Defines a function to query Azure AI Search for sources based on the user query.
    - Defines a function to query Azure OpenAI for a response based on the user query and the sources retrieved from Azure AI Search.
    - The `main` function orchestrates the flow by calling the search and OpenAI functions, and then prints the response.    
    
1. Build the TypeScript code to JavaScript.

   ```bash
   tsc
   ```

   This command compiles the TypeScript code in the `src` directory and outputs the JavaScript files in the `dist` directory.

1. Run the following command in a terminal to execute the query script:

    ```bash
    node -r dotenv/config dist/query.js
    ```

    The `.env` is passed into the runtime using the `-r dotenv/config`. 

1. View the output consists of recommendations for several hotels. Here's an example of what the output might look like:

    ```
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

## Troubleshooting

If you get a **Forbidden** error message, check Azure AI Search configuration to make sure role-based access is enabled.

If you get an **Authorization failed** error message, wait a few minutes and try again. It can take several minutes for role assignments to become operational.

If you get a **Resource not found** error message, check the resource URIs and make sure the API version on the chat model is valid.

Otherwise, to experiment further, change the query and rerun the last step to better understand how the model works with the grounding data.

You can also modify the prompt to change the tone or structure of the output.

You might also try the query without semantic ranking by setting `use_semantic_reranker=False` in the query parameters step. Semantic ranking can noticably improve the relevance of query results and the ability of the LLM to return useful information. Experimentation can help you decide whether it makes a difference for your content.

## Send a complex RAG query

Azure AI Search supports [complex types](../../search-howto-complex-data-types.md) for nested JSON structures. In the hotels-sample-index, `Address` is an example of a complex type, consisting of `Address.StreetAddress`, `Address.City`, `Address.StateProvince`, `Address.PostalCode`, and `Address.Country`. The index also has complex collection of `Rooms` for each hotel.

If your index has complex types, change your prompt to include formatting instructions: 

```text
Can you recommend a few hotels that offer complimentary breakfast? 
Tell me their description, address, tags, and the rate for one room that sleeps 4 people.
```

1. Create a new file `queryComplex.ts` in the `src` directory.
1. Copy the following code to the file:

    :::code language="typescript" source="~/azure-search-javascript-samples/quickstart-rag-ts/src/queryComplex.ts" :::

1. Build the TypeScript code to JavaScript.

   ```bash
   tsc
   ```

   This command compiles the TypeScript code in the `src` directory and outputs the JavaScript files in the `dist` directory.

1. Run the following command in a terminal to execute the query script:

    ```bash
    node -r dotenv/config dist/queryComplex.js
    ```

    The `.env` is passed into the runtime using the `-r dotenv/config`. 


1. View the output from Azure OpenAI, and it adds content from complex types.

```
Here are a few hotels that offer complimentary breakfast and have rooms that sleep 4 people:

1. **Head Wind Resort**
   - **Description:** The best of old town hospitality combined with views of the river and 
   cool breezes off the prairie. Enjoy a complimentary continental breakfast in the lobby, 
   and free Wi-Fi throughout the hotel.
   - **Address:** 7633 E 63rd Pl, Tulsa, OK 74133, USA
   - **Tags:** Coffee in lobby, free Wi-Fi, view
   - **Room for 4:** Suite, 2 Queen Beds (Amenities) - $254.99

2. **Double Sanctuary Resort**
   - **Description:** 5-star Luxury Hotel - Biggest Rooms in the city. #1 Hotel in the area 
   listed by Traveler magazine. Free WiFi, Flexible check in/out, Fitness Center & espresso 
   in room. Offers continental breakfast.
   - **Address:** 2211 Elliott Ave, Seattle, WA 98121, USA
   - **Tags:** View, pool, restaurant, bar, continental breakfast
   - **Room for 4:** Suite, 2 Queen Beds (Amenities) - $254.99

3. **Swan Bird Lake Inn**
   - **Description:** Continental-style breakfast featuring a variety of food and drinks. 
   Locally made caramel cinnamon rolls are a favorite.
   - **Address:** 1 Memorial Dr, Cambridge, MA 02142, USA
   - **Tags:** Continental breakfast, free Wi-Fi, 24-hour front desk service
   - **Room for 4:** Budget Room, 2 Queen Beds (City View) - $85.99

4. **Gastronomic Landscape Hotel**
   - **Description:** Known for its culinary excellence under the management of William Dough, 
   offers continental breakfast.
   - **Address:** 3393 Peachtree Rd, Atlanta, GA 30326, USA
   - **Tags:** Restaurant, bar, continental breakfast
   - **Room for 4:** Budget Room, 2 Queen Beds (Amenities) - $66.99
...
   - **Tags:** Pool, continental breakfast, free parking
   - **Room for 4:** Budget Room, 2 Queen Beds (Amenities) - $60.99

Enjoy your stay! Let me know if you need any more information.
```

## Troubleshooting errors

To debug Azure SDK errors, set the environment variable `AZURE_LOG_LEVEL` to one of the following: `verbose`, `info`, `warning`, `error`. This will enable detailed logging for the Azure SDK, which can help identify [issues with authentication](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/identity/identity/TROUBLESHOOTING.md#enable-and-configure-logging), network connectivity, or other problems.

Rerun the query script. You should now get informational statements from the SDKs in the output that provide more detail about any issues.

If you see output messages related to ManagedIdentityCredential and token acquisition failures, it could be that you have multiple tenants, and your Azure sign-in is using a tenant that doesn't have your search service. To get your tenant ID, search the Azure portal for "tenant properties" or run `az login tenant list`.

Once you have your tenant ID, run `az login --tenant <YOUR-TENANT-ID>` at a command prompt, and then rerun the script.

## Clean up

When you're working in your own subscription, it's a good idea at the end of a project to identify whether you still need the resources you created. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

You can find and manage resources in the Azure portal by using the **All resources** or **Resource groups** link in the leftmost pane.
