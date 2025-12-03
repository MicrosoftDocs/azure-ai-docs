---
author: diberry
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: include
ms.date: 11/20/2025
---

[!INCLUDE [Semantic ranker introduction](semantic-ranker-intro.md)]

## Set up the client

In this quickstart, you use an IDE and the [**@azure/search-documents**](https://www.npmjs.com/package/@azure/search-documents) client library to add semantic ranking to an existing search index.

The quickstart assumes the following is available on your computer:
- [Visual Studio Code](https://code.visualstudio.com/) for this quickstart.
- [Node.js](https://nodejs.org/) (LTS) for running the sample.

> [!TIP]
> You can download the [source code](https://github.com/Azure-Samples/azure-search-javascript-samples/tree/main/quickstart-semantic-ranking-js) to start with a finished project or follow these steps to create your own.

### Set up local development environment

1. Start Visual Studio Code in a new directory.

   ```bash
   mkdir semantic-ranking-quickstart && cd semantic-ranking-quickstart
   code .
   ```

1. Create a new package for ESM modules in your project directory.

   ```bash
   npm init -y
   npm pkg set type=module
   ```

1. Install packages, including [azure-search-documents](/javascript/api/%40azure/search-documents).

    ```bash
   npm install @azure/identity @azure/search-documents dotenv
    ```

1. Create `.env`, and provide your search service endpoint. You can get the endpoint from the Azure portal on the search service **Overview** page.

    ```ini
    AZURE_SEARCH_ENDPOINT=YOUR-SEARCH-SERVICE-ENDPOINT
    AZURE_SEARCH_INDEX_NAME=hotels-sample-index
    SEMANTIC_CONFIGURATION_NAME=semantic-config
    ```

1. Create a `src` directory in your project directory.

   ```bash
   mkdir src
   ```

### Sign in to Azure

If you signed in to the [Azure portal](https://portal.azure.com), you're signed into Azure. If you aren't sure, use the Azure CLI or Azure PowerShell to log in: `az login` or `az connect`. If you have multiple tenants and subscriptions, see [Quickstart: Connect without keys](../../search-get-started-rbac.md) for help on how to connect.

## Create a common authentication file

Create a file in `./src` called `config.ts` to read the `.env` file and hold the environment variables and authentication credential. Copy in the following code; don't change it. This file will be used by all the other files in this quickstart.

```javascript
import { DefaultAzureCredential } from "@azure/identity";

// Configuration - use environment variables
export const searchEndpoint = process.env.AZURE_SEARCH_ENDPOINT || "PUT-YOUR-SEARCH-SERVICE-ENDPOINT-HERE";
export const indexName = process.env.AZURE_SEARCH_INDEX_NAME || "hotels-sample-index";
export const semanticConfigurationName = process.env.SEMANTIC_CONFIGURATION_NAME || "semantic-config";

// Create credential
export const credential = new DefaultAzureCredential();

console.log(`Using Azure Search endpoint: ${searchEndpoint}`);
console.log(`Using index name: ${indexName}\n\n`);
```

## Get the index schema

In this section, you get settings for the existing `hotels-sample-index` index on your search service.

1. Create a file in `./src` called `getIndexSettings.js` and copy in the following code.

    ```javascript
    import {
        SearchIndexClient
    } from "@azure/search-documents";
    import { searchEndpoint, indexName, credential } from "./config.js";
    
    const indexClient = new SearchIndexClient(searchEndpoint, credential);
    
    console.log('Getting semantic search index settings...');
    
    // Get the existing schema
    const index = await indexClient.getIndex(indexName);
    
    console.log(`Index name: ${index.name}`);
    console.log(`Number of fields: ${index.fields.length}`);
    
    for(const field of index.fields) {
        console.log(`Field: ${field.name}, Type: ${field.type}, Searchable: ${field.searchable}`);
    }
    
    if(index.semanticSearch && index.semanticSearch.configurations) {
        console.log(`Semantic search configurations: ${index.semanticSearch.configurations.length}`);
        for(const config of index.semanticSearch.configurations) {
            console.log(`Configuration name: ${config.name}`);
            console.log(`Title field: ${config.prioritizedFields.titleField?.name}`);
        }
    } else {
        console.log("No semantic configuration exists for this index.");
    }
    ```

1. Run the code.

    ```bash
    node -r dotenv/config src/getIndexSettings.js
    ```

1. Output is the name of the index, list of fields, and a statement indicating whether a semantic configuration exists. For the purposes of this quickstart, the message should say `No semantic configuration exists for this index`.

## Update the index with a semantic configuration

1. Create a file in `./src` called `updateIndexSettings.js` and copy in the following code to add a semantic configuration to the existing `hotels-sample-index` index on your search service. No search documents are deleted by this operation and your index is still operational after the configuration is added.

    ```javascript
    import {
        SearchIndexClient
    } from "@azure/search-documents";
    import { searchEndpoint, indexName, credential, semanticConfigurationName } from "./config.js";
    
    try {
    
        const indexClient = new SearchIndexClient(searchEndpoint, credential);
    
        const existingIndex = await indexClient.getIndex(indexName);
    
        const fields = {
            titleField: {
                name: "HotelName"
            },
            keywordsFields: [{
                name: "Tags"
            }],
            contentFields: [{
                name: "Description"
            }]
        };
    
        const newSemanticConfiguration = {
            name: semanticConfigurationName,
            prioritizedFields: fields
        };
    
        // Add the new semantic configuration to the existing index
        if (existingIndex.semanticSearch && existingIndex.semanticSearch.configurations) {
            existingIndex.semanticSearch.configurations.push(newSemanticConfiguration);
        } else {
            const configExists = existingIndex.semanticSearch?.configurations?.some(
                config => config.name === semanticConfigurationName
            );
            if (!configExists) {
                existingIndex.semanticSearch = {
                    configurations: [newSemanticConfiguration]
                };
            }
        }
    
        await indexClient.createOrUpdateIndex(existingIndex);
    
        const updatedIndex = await indexClient.getIndex(indexName);
    
        console.log(`Semantic configurations:`);
        console.log("-".repeat(40));
    
        if (updatedIndex.semanticSearch && updatedIndex.semanticSearch.configurations) {
            for (const config of updatedIndex.semanticSearch.configurations) {
                console.log(`Configuration name: ${config.name}`);
                console.log(`Title field: ${config.prioritizedFields.titleField?.name}`);
                console.log(`Keywords fields: ${config.prioritizedFields.keywordsFields?.map(f => f.name).join(", ")}`);
                console.log(`Content fields: ${config.prioritizedFields.contentFields?.map(f => f.name).join(", ")}`);
                console.log("-".repeat(40));
            }
        } else {
            console.log("No semantic configurations found.");
        }
    
        console.log("Semantic configuration updated successfully.");
    } catch (error) {
        console.error("Error updating semantic configuration:", error);
    }
    ```

1. Run the code.

    ```bash
    node -r dotenv/config src/updateIndexSettings.js
    ```

1. Output is the semantic configuration you just added, `Semantic configuration updated successfully.`.

## Run semantic queries

Once the `hotels-sample-index` index has a semantic configuration, you can run queries that include semantic parameters.

1. Create a file in `./src` called `semanticQuery.js` and copy in the following code to create a semantic query of the index. This is the minimum requirement for invoking semantic ranking.

    ```javascript
    import { SearchClient } from "@azure/search-documents";
    import { credential, searchEndpoint, indexName, semanticConfigurationName } from "./config.js";
    
    const searchClient = new SearchClient(
        searchEndpoint,
        indexName,
        credential
    );
    
    const results = await searchClient.search("walking distance to live music", {
        queryType: "semantic",
        semanticSearchOptions: {
            configurationName: semanticConfigurationName
        },
        select: ["HotelId", "HotelName", "Description"]
    });
    
    let rowNumber = 1;
    for await (const result of results.results) {
        // Log each result
        const doc = result.document;
        const score = result.score;
        const rerankerScoreDisplay = result.rerankerScore;
    
        console.log(`Search result #${rowNumber++}:`);
        console.log(`  Re-ranker Score: ${rerankerScoreDisplay}`);
        console.log(`  HotelId: ${doc.HotelId}`);
        console.log(`  HotelName: ${doc.HotelName}`);
        console.log(`  Description: ${doc.Description || 'N/A'}\n`);
    }
    ```

1. Run the code.

    ```bash
    node -r dotenv/config src/semanticQuery.js
    ```

1. Output should consist of 13 documents, ordered by the `rerankerScoreDisplay`.

### Return captions

Optionally, you can add captions to extract portions of the text and apply hit highlighting to the important terms and phrases. This query adds captions.

1. Create a file in `./src` called `semanticQueryReturnCaptions.js` and copy in the following code to add captions to the query.

    ```javascript
    import { SearchClient } from "@azure/search-documents";
    import { credential, searchEndpoint, indexName, semanticConfigurationName } from "./config.js";
    
    const searchClient = new SearchClient(
        searchEndpoint,
        indexName,
        credential
    );
    
    console.log(`Using semantic configuration: ${semanticConfigurationName}`);
    console.log("Search query: walking distance to live music");
    
    const results = await searchClient.search("walking distance to live music", {
        queryType: "semantic",
        semanticSearchOptions: {
            configurationName: semanticConfigurationName,
            captions: {
                captionType: "extractive",
                highlight: true
            }
        },
        select: ["HotelId", "HotelName", "Description"],
    });
    
    console.log(`Found ${results.count} results with semantic search\n`);
    let rowNumber = 1;
    
    for await (const result of results.results) {
        // Log each result
        const doc = result.document;
        const rerankerScoreDisplay = result.rerankerScore;
    
        console.log(`Search result #${rowNumber++}:`);
        console.log(`  Re-ranker Score: ${rerankerScoreDisplay}`);
        console.log(`  HotelName: ${doc.HotelName}`);
        console.log(`  Description: ${doc.Description || 'N/A'}\n`);
    
        // Caption handling with better debugging
        const captions = result.captions;
        
        if (captions && captions.length > 0) {
            const caption = captions[0];
            
            if (caption.highlights) {
                console.log(`  Caption with highlights: ${caption.highlights}`);
            } else if (caption.text) {
                console.log(`  Caption text: ${caption.text}`);
            } else {
                console.log(`  Caption exists but has no text or highlights content`);
            }
        } else {
            console.log("  No captions found for this result");
        }
        console.log("-".repeat(60));
    }
    ```

1. Run the code.

    ```bash
    node -r dotenv/config src/semanticQueryReturnCaptions.js
    ```

1. Output should include a new caption element alongside search field. Captions are the most relevant passages in a result. If your index includes larger chunks of text, a caption is helpful for extracting the most interesting sentences.

    ```console
    Search result #1:
      Re-ranker Score: 2.613231658935547
      HotelName: Uptown Chic Hotel
      Description: Chic hotel near the city. High-rise hotel in downtown, within walking distance to theaters, art galleries, restaurants and shops. Visit Seattle Art Museum by day, and then head over to Benaroya Hall to catch the evening's concert performance.
    
      Caption with highlights: Chic hotel near the city. High-rise hotel in downtown, within walking distance to<em> theaters, </em>art galleries, restaurants and shops. Visit<em> Seattle Art Museum </em>by day, and then head over to<em> Benaroya Hall </em>to catch the evening's concert performance.
    ```

### Return semantic answers

In this final query, return semantic answers.

Semantic ranker can produce an answer to a query string that has the characteristics of a question. The generated answer is extracted verbatim from your content so it won't include composed content like what you might expect from a chat completion model. If the semantic answer isn't useful for your scenario, you can omit `semantic_answers` from your code.

To produce a semantic answer, the question and answer must be closely aligned, and the model must find content that clearly answers the question. If potential answers fail to meet a confidence threshold, the model doesn't return an answer. For demonstration purposes, the question in this example is designed to get a response so that you can see the syntax.

1. Create a file in `./src` called `semanticAnswer.js` and copy in the following code to get semantic answers. 

    ```javascript
    import { SearchClient } from "@azure/search-documents";
    import { credential, searchEndpoint, indexName, semanticConfigurationName } from "./config.js";
    
    const searchClient = new SearchClient(
        searchEndpoint,
        indexName,
        credential
    );
    
    const results = await searchClient.search("What's a good hotel for people who like to read", {
        queryType: "semantic",
        semanticSearchOptions: {
            configurationName: semanticConfigurationName,
            captions: {
                captionType: "extractive"
            },
            answers: {
                answerType: "extractive"
            }
        },
        select: ["HotelName", "Description", "Category"]
    });
    
    console.log(`Answers:\n\n`);
    let rowNumber = 1; 
    
    // Extract semantic answers from the search results
    const semanticAnswers = results.answers;
    for (const answer of semanticAnswers || []) {
        console.log(`Semantic answer result #${rowNumber++}:`);
        if (answer.highlights) {
            console.log(`Semantic Answer: ${answer.highlights}`);
        } else {
            console.log(`Semantic Answer: ${answer.text}`);
        }
        console.log(`Semantic Answer Score: ${answer.score}\n\n`);
    }
    
    console.log(`Search Results:\n\n`);
    rowNumber = 1;
    
    // Iterate through the search results
    for await (const result of results.results) {
        // Log each result
        const doc = result.document;
        const rerankerScoreDisplay = result.rerankerScore;
    
        console.log(`Search result #${rowNumber++}:`);
        console.log(`${rerankerScoreDisplay}`);
        console.log(`${doc.HotelName}`);
        console.log(`${doc.Description || 'N/A'}`);
    
        const captions = result.captions;
    
        if (captions && captions.length > 0) {
            const caption = captions[0];
            if (caption.highlights) {
                console.log(`Caption: ${caption.highlights}\n`);
            } else {
                console.log(`Caption: ${caption.text}\n`);
            }
        }
    }
    ```

1. Run the code.

    ```bash
    node -r dotenv/config src/semanticAnswer.js
    ```

1. Output should look similar to the following example, where the best answer to question is pulled from one of the results.

    Recall that answers are *verbatim content* pulled from your index and might be missing phrases that a user would expect to see. To get *composed answers* as generated by a chat completion model, considering using a [RAG pattern](../../retrieval-augmented-generation-overview.md) or [agentic retrieval](../../agentic-retrieval-overview.md).

    ```console
    Semantic answer result #1:
    Semantic Answer: Nature is Home on the beach. Explore the shore by day, and then come home to our shared living space to relax around a stone fireplace, sip something warm, and explore the<em> library </em>by night. Save up to 30 percent. Valid Now through the end of the year. Restrictions and blackouts may apply.
    Semantic Answer Score: 0.9829999804496765
    ```
