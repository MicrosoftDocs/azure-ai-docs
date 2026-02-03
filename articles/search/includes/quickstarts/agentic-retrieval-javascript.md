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

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](../../search-create-service-portal.md) in any [region that provides agentic retrieval](../../search-region-support.md).

+ A [Microsoft Foundry project](/azure/ai-foundry/how-to/create-projects) and resource. When you create a project, the resource is automatically created.

+ The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

+ [Visual Studio Code](https://code.visualstudio.com/download) and the latest LTS version of [Node.js](https://nodejs.org/en/download/).

[!INCLUDE [Setup](./agentic-retrieval-setup.md)]

## Set up the environment

To set up the console application for this quickstart:

1. Create a folder named `quickstart-agentic-retrieval` to contain the application.

1. Open the folder in Visual Studio Code.

1. Select **Terminal** > **New Terminal**, and then run the following commands to initialize the `package.json` file.

    ```console
    npm init -y
    npm pkg set type=module
    ```

1. Install the [Azure AI Search client library for JavaScript](/javascript/api/overview/azure/search-documents-readme).

    ```console
    npm install @azure/search-documents@12.3.0-beta.1
    ```

1. For keyless authentication with Microsoft Entra ID, install the [Azure Identity client library for JavaScript](/javascript/api/overview/azure/identity-readme).

    ```console
    npm install @azure/identity
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
    AZURE_SEARCH_ENDPOINT = https://<your-search-service-name>.search.windows.net
    AZURE_OPENAI_ENDPOINT = https://<your-ai-foundry-resource-name>.openai.azure.com/
    AZURE_OPENAI_GPT_DEPLOYMENT = gpt-5-mini
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT = text-embedding-3-large
    ```

1. Set `AZURE_SEARCH_ENDPOINT` and `AZURE_OPENAI_ENDPOINT` to the values you obtained in [Get endpoints](#get-endpoints).

1. Create a file named `index.js`, and then paste the following code into the file.

    ```javascript
    import { DefaultAzureCredential } from '@azure/identity';
    import {
        SearchIndexClient,
        SearchClient,
        KnowledgeRetrievalClient,
        SearchIndexingBufferedSender
    } from '@azure/search-documents';
    
    export const documentKeyRetriever = (document) => {
      return document.id;
    };
    
    export const WAIT_TIME = 4000;
    export function delay(timeInMs) {
      return new Promise((resolve) => setTimeout(resolve, timeInMs));
    }
    
    const index = {
        name: 'earth_at_night',
        fields: [
            {
                name: "id",
                type: "Edm.String",
                key: true,
                filterable: true,
                sortable: true,
                facetable: true
            },
            {
                name: "page_chunk",
                type: "Edm.String",
                searchable: true,
                filterable: false,
                sortable: false,
                facetable: false
            },
            {
                name: "page_embedding_text_3_large",
                type: "Collection(Edm.Single)",
                searchable: true,
                filterable: false,
                sortable: false,
                facetable: false,
                vectorSearchDimensions: 3072,
                vectorSearchProfileName: "hnsw_text_3_large"
            },
            {
                name: "page_number",
                type: "Edm.Int32",
                filterable: true,
                sortable: true,
                facetable: true
            }
        ],
        vectorSearch: {
            profiles: [
                {
                    name: "hnsw_text_3_large",
                    algorithmConfigurationName: "alg",
                    vectorizerName: "azure_openai_text_3_large"
                }
            ],
            algorithms: [
                {
                    name: "alg",
                    kind: "hnsw"
                }
            ],
            vectorizers: [
                {
                    vectorizerName: "azure_openai_text_3_large",
                    kind: "azureOpenAI",
                    parameters: {
                        resourceUrl: process.env.AZURE_OPENAI_ENDPOINT,
                        deploymentId: process.env.AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
                        modelName: process.env.AZURE_OPENAI_EMBEDDING_DEPLOYMENT
                    }
                }
            ]
        },
        semanticSearch: {
            defaultConfigurationName: "semantic_config",
            configurations: [
                {
                    name: "semantic_config",
                    prioritizedFields: {
                        contentFields: [
                            { name: "page_chunk" }
                        ]
                    }
                }
            ]
        }
    };
    
    const credential = new DefaultAzureCredential();
    
    const searchIndexClient = new SearchIndexClient(process.env.AZURE_SEARCH_ENDPOINT, credential);
    const searchClient = new SearchClient(process.env.AZURE_SEARCH_ENDPOINT, 'earth_at_night', credential);
    
    await searchIndexClient.createOrUpdateIndex(index);
    
    // get Documents with vectors
    const response = await fetch("https://raw.githubusercontent.com/Azure-Samples/azure-search-sample-data/refs/heads/main/nasa-e-book/earth-at-night-json/documents.json");
    
    if (!response.ok) {
        throw new Error(`Failed to fetch documents: ${response.status} ${response.statusText}`);
    }
    const documents = await response.json();
    
    const bufferedClient = new SearchIndexingBufferedSender(
        searchClient,
        documentKeyRetriever,
        {
            autoFlush: true,
        },
    );
    
    await bufferedClient.uploadDocuments(documents);
    await bufferedClient.flush();
    await bufferedClient.dispose();
    
    console.log(`Waiting for indexing to complete...`);
    console.log(`Expected documents: ${documents.length}`);
    await delay(WAIT_TIME);
    
    let count = await searchClient.getDocumentsCount();
    console.log(`Current indexed count: ${count}`);
    
    while (count !== documents.length) {
        await delay(WAIT_TIME);
        count = await searchClient.getDocumentsCount();
        console.log(`Current indexed count: ${count}`);
    }
    
    console.log(`✓ All ${documents.length} documents indexed successfully!`);
    
    await searchIndexClient.createKnowledgeSource({
        name: 'earth-knowledge-source',
        description: "Knowledge source for Earth at Night e-book content",
        kind: "searchIndex",
        searchIndexParameters: {
            searchIndexName: 'earth_at_night',
            sourceDataFields: [
                { name: "id" },
                { name: "page_number" }
            ]
        }
    });
    
    console.log(`✅ Knowledge source 'earth-knowledge-source' created successfully.`);
    
    await searchIndexClient.createKnowledgeBase({
        name: 'earth-knowledge-base',
        knowledgeSources: [
            {
                name: 'earth-knowledge-source'
            }
        ],
        models: [
            {
                kind: "azureOpenAI",
                azureOpenAIParameters: {
                    resourceUrl: process.env.AZURE_OPENAI_ENDPOINT,
                    deploymentId: process.env.AZURE_OPENAI_GPT_DEPLOYMENT,
                    modelName: process.env.AZURE_OPENAI_GPT_DEPLOYMENT
                }
            }
        ],
        outputMode: "answerSynthesis",
        answerInstructions: "Provide a two sentence concise and informative answer based on the retrieved documents."
    });
    
    console.log(`✅ Knowledge base 'earth-knowledge-base' created successfully.`);
    
    const knowledgeRetrievalClient = new KnowledgeRetrievalClient(
        process.env.AZURE_SEARCH_ENDPOINT,
        'earth-knowledge-base',
        credential
    );
    
    const query1 = `Why do suburban belts display larger December brightening than urban cores even though absolute light levels are higher downtown? Why is the Phoenix nighttime street grid is so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?`;
    
    const retrievalRequest = {
        messages: [
            {
                role: "user",
                content: [
                    {
                        type: "text",
                        text: query1
                    }
                ]
            }
        ],
        knowledgeSourceParams: [
            {
                kind: "searchIndex",
                knowledgeSourceName: 'earth-knowledge-source',
                includeReferences: true,
                includeReferenceSourceData: true,
                alwaysQuerySource: true,
                rerankerThreshold: 2.5
            }
        ],
        includeActivity: true,
        retrievalReasoningEffort: { kind: "low" }
    };
    
    const result = await knowledgeRetrievalClient.retrieveKnowledge(retrievalRequest);
    
    console.log("\n📝 ANSWER:");
    console.log("─".repeat(80));
    if (result.response && result.response.length > 0) {
        result.response.forEach((msg) => {
            if (msg.content && msg.content.length > 0) {
                msg.content.forEach((content) => {
                    if (content.type === "text" && 'text' in content) {
                        console.log(content.text);
                    }
                });
            }
        });
    }
    console.log("─".repeat(80));
    
    if (result.activity) {
        console.log("\nActivities:");
        result.activity.forEach((activity) => {
            console.log(`Activity Type: ${activity.type}`);
            console.log(JSON.stringify(activity, null, 2));
        });
    }
    
    if (result.references) {
        console.log("\nReferences:");
        result.references.forEach((reference) => {
            console.log(`Reference Type: ${reference.type}`);
            console.log(JSON.stringify(reference, null, 2));
        });
    }
    
    // Follow-up query - to demonstrate conversational context
    const query2 = "How do I find lava at night?";
    console.log(`\n❓ Follow-up question: ${query2}`);
    
    const retrievalRequest2 = {
        messages: [
            {
                role: "user",
                content: [
                    {
                        type: "text",
                        text: query2
                    }
                ]
            }
        ],
        knowledgeSourceParams: [
            {
                kind: "searchIndex",
                knowledgeSourceName: 'earth-knowledge-source',
                includeReferences: true,
                includeReferenceSourceData: true,
                alwaysQuerySource: true,
                rerankerThreshold: 2.5
            }
        ],
        includeActivity: true,
        retrievalReasoningEffort: { kind: "low" }
    };
    
    const result2 = await knowledgeRetrievalClient.retrieveKnowledge(retrievalRequest2);
    
    console.log("\n📝 ANSWER:");
    console.log("─".repeat(80));
    if (result2.response && result2.response.length > 0) {
        result2.response.forEach((msg) => {
            if (msg.content && msg.content.length > 0) {
                msg.content.forEach((content) => {
                    if (content.type === "text" && 'text' in content) {
                        console.log(content.text);
                    }
                });
            }
        });
    }
    console.log("─".repeat(80));
    
    if (result2.activity) {
        console.log("\nActivities:");
        result2.activity.forEach((activity) => {
            console.log(`Activity Type: ${activity.type}`);
            console.log(JSON.stringify(activity, null, 2));
        });
    }
    
    if (result2.references) {
        console.log("\nReferences:");
        result2.references.forEach((reference) => {
            console.log(`Reference Type: ${reference.type}`);
            console.log(JSON.stringify(reference, null, 2));
        });
    }
    
    console.log("\n✅ Quickstart completed successfully!");
    
    // Clean up resources
    await searchIndexClient.deleteKnowledgeBase('earth-knowledge-base');
    await searchIndexClient.deleteKnowledgeSource('earth-knowledge-source');
    await searchIndexClient.deleteIndex('earth_at_night');
    
    console.log(`\n🗑️  Cleaned up resources.`);
    ```

1. Build and run the application.

    ```console
    node --env-file=.env index.js
    ```

### Output

The output of the application should be similar to the following:

```console
Waiting for indexing to complete...
Expected documents: 194
Current indexed count: 194
✓ All 194 documents indexed successfully!
✅ Knowledge source 'earth-knowledge-source' created successfully.
✅ Knowledge base 'earth-knowledge-base' created successfully.

📝 ANSWER:
────────────────────────────────────────────────────────────────────────────────
Suburban belts show larger December brightening (20–50% increases) because residential holiday lighting and seasonal decorations are concentrated there, so relative (fractional) increases over the baseline are bigger even though absolute downtown radiances remain higher; urban cores already emit strong baseline light while many suburbs add a large seasonal increment visible in VIIRS DNB observations [ref_id:0][ref_id:1]. The Phoenix street grid appears sharply from space because continuous, street‑oriented lighting with regular residential lot spacing and little vegetative masking produces strong, linear emissions, whereas long interstate stretches between Midwestern cities have sparser, access‑limited lighting, fewer adjacent developments and more shielded fixtures so they register comparatively dim on night‑light sensors like VIIRS/DNB [ref_id:0][ref_id:1].
────────────────────────────────────────────────────────────────────────────────

Activities:
Activity Type: modelQueryPlanning
{
  "id": 0,
  "type": "modelQueryPlanning",
  "elapsedMs": 5883,
  "inputTokens": 1489,
  "outputTokens": 326
}
Activity Type: searchIndex
{
  "id": 1,
  "type": "searchIndex",
  "elapsedMs": 527,
  "knowledgeSourceName": "earth-knowledge-source",
  "queryTime": "2025-12-19T15:38:23.462Z",
  "count": 1,
  "searchIndexArguments": {
    "search": "December brightening suburban belts vs urban cores light pollution causes December increase in night lights suburban vs urban",
    "filter": null,
    "sourceDataFields": [
      {
        "name": "page_chunk"
      },
      {
        "name": "id"
      },
      {
        "name": "page_number"
      }
    ],
    "searchFields": [],
    "semanticConfigurationName": "semantic_config"
  }
}
Activity Type: searchIndex
{
  "id": 2,
  "type": "searchIndex",
  "elapsedMs": 538,
  "knowledgeSourceName": "earth-knowledge-source",
  "queryTime": "2025-12-19T15:38:24.001Z",
  "count": 0,
  "searchIndexArguments": {
    "search": "factors that make Phoenix nighttime street grid highly visible from space reasons highway/interstate lighting visibility differences Midwestern interstates dim",
    "filter": null,
    "sourceDataFields": [
      {
        "name": "page_chunk"
      },
      {
        "name": "id"
      },
      {
        "name": "page_number"
      }
    ],
    "searchFields": [],
    "semanticConfigurationName": "semantic_config"
  }
}
Activity Type: searchIndex
{
  "id": 3,
  "type": "searchIndex",
  "elapsedMs": 465,
  "knowledgeSourceName": "earth-knowledge-source",
  "queryTime": "2025-12-19T15:38:24.467Z",
  "count": 2,
  "searchIndexArguments": {
    "search": "satellite nighttime lights seasonal variations suburban brightening studies December holiday lighting residential vs commercial lighting patterns",
    "filter": null,
    "sourceDataFields": [
      {
        "name": "page_chunk"
      },
      {
        "name": "id"
      },
      {
        "name": "page_number"
      }
    ],
    "searchFields": [],
    "semanticConfigurationName": "semantic_config"
  }
}
Activity Type: agenticReasoning
{
  "id": 4,
  "type": "agenticReasoning",
  "reasoningTokens": 70397,
  "retrievalReasoningEffort": {
    "kind": "low"
  }
}
Activity Type: modelAnswerSynthesis
{
  "id": 5,
  "type": "modelAnswerSynthesis",
  "elapsedMs": 4908,
  "inputTokens": 4013,
  "outputTokens": 187
}

References:
Reference Type: searchIndex
{
  "type": "searchIndex",
  "id": "0",
  "activitySource": 3,
  "sourceData": {
    "id": "earth_at_night_508_page_174_verbalized",
    "page_chunk": "<!-- PageHeader=\"Holiday Lights\" -->\n\n## Holiday Lights\n\n### Bursting with Holiday Energy-United States\n\nNASA researchers found that nighttime lights in the United States shine 20 to 50 percent brighter in December due to holiday light displays and other activities during Christmas and New Year's when compared to light output during the rest of the year.\n\nThe next five maps (see also pages 161-163), created using data from the VIIRS DNB on the Suomi NPP satellite, show changes in lighting intensity and location around many major cities, comparing the nighttime light signals from December 2012 and beyond.\n\n---\n\n#### Figure 1. Location Overview\n\nA map of the western hemisphere with a marker indicating the mid-Atlantic region of the eastern United States, where the study of holiday lighting intensity was focused.\n\n---\n\n#### Figure 2. Holiday Lighting Intensity: Mid-Atlantic United States (2012–2014)\n\nA map showing Maryland, New Jersey, Delaware, Virginia, West Virginia, Ohio, Kentucky, Tennessee, North Carolina, South Carolina, and surrounding areas. Major cities labeled include Washington, D.C., Richmond, Norfolk, and Raleigh.\n\nThe map uses colors to indicate changes in holiday nighttime lighting intensity between 2012 and 2014:\n\n- **Green/bright areas**: More holiday lighting (areas shining 20–50% brighter in December).\n- **Yellow areas**: No change in lighting.\n- **Dim/grey areas**: Less holiday lighting.\n\nKey observations from the map:\n\n- The Washington, D.C. metropolitan area shows significant increases in lighting during the holidays, extending into Maryland and Virginia.\n- Urban centers such as Richmond (Virginia), Norfolk (Virginia), Raleigh (North Carolina), and clusters in Tennessee and South Carolina also experience notable increases in light intensity during December.\n- Rural areas and the interiors of West Virginia, Kentucky, and North Carolina show little change or less holiday lighting, corresponding to population density and urbanization.\n\n**Legend:**\n\n| Holiday Lighting Change | Color on Map   |\n|------------------------|---------------|\n| More                   | Green/bright  |\n| No Change              | Yellow        |\n| Less                   | Dim/grey      |\n\n_The scale bar indicates a distance of 100 km for reference._\n\n---\n\n<!-- PageFooter=\"158 Earth at Night\" -->",
    "page_number": 174
  },
  "rerankerScore": 2.6692379,
  "docKey": "earth_at_night_508_page_174_verbalized"
}
... // Trimmed for brevity

❓ Follow-up question: How do I find lava at night?

📝 ANSWER:
────────────────────────────────────────────────────────────────────────────────
... // Trimmed for brevity
────────────────────────────────────────────────────────────────────────────────

Activities:
... // Trimmed for brevity

References:
... // Trimmed for brevity

✅ Quickstart completed successfully!

🗑️  Cleaned up resources.
```

## Understand the code

Now that you have the code, let's break down the key components:

1. [Create a search index](#create-a-search-index)
1. [Upload documents to the index](#upload-documents-to-the-index)
1. [Create a knowledge source](#create-a-knowledge-source)
1. [Create a knowledge base](#create-a-knowledge-base)
1. [Run the retrieval pipeline](#run-the-retrieval-pipeline)
1. [Review the response, activity, and references](#review-the-response-activity-and-results)
1. [Continue the conversation](#continue-the-conversation)

### Create a search index

In Azure AI Search, an index is a structured collection of data. The following code defines an index named `earth_at_night`.

The index schema contains fields for document identification and page content, embeddings, and numbers. The schema also includes configurations for semantic ranking and vector search, which uses your `text-embedding-3-large` deployment to vectorize text and match documents based on semantic similarity.

```javascript
const index: SearchIndex = {
    name: 'earth_at_night',
    fields: [
        {
            name: "id",
            type: "Edm.String",
            key: true,
            filterable: true,
            sortable: true,
            facetable: true
        } as SearchField,
        {
            name: "page_chunk",
            type: "Edm.String",
            searchable: true,
            filterable: false,
            sortable: false,
            facetable: false
        } as SearchField,
        {
            name: "page_embedding_text_3_large",
            type: "Collection(Edm.Single)",
            searchable: true,
            filterable: false,
            sortable: false,
            facetable: false,
            vectorSearchDimensions: 3072,
            vectorSearchProfileName: "hnsw_text_3_large"
        } as SearchField,
        {
            name: "page_number",
            type: "Edm.Int32",
            filterable: true,
            sortable: true,
            facetable: true
        } as SearchField
    ],
    vectorSearch: {
        profiles: [
            {
                name: "hnsw_text_3_large",
                algorithmConfigurationName: "alg",
                vectorizerName: "azure_openai_text_3_large"
            } as VectorSearchProfile
        ],
        algorithms: [
            {
                name: "alg",
                kind: "hnsw"
            } as HnswAlgorithmConfiguration
        ],
        vectorizers: [
            {
                vectorizerName: "azure_openai_text_3_large",
                kind: "azureOpenAI",
                parameters: {
                    resourceUrl: process.env.AZURE_OPENAI_ENDPOINT!,
                    deploymentId: process.env.AZURE_OPENAI_EMBEDDING_DEPLOYMENT!,
                    modelName: process.env.AZURE_OPENAI_EMBEDDING_DEPLOYMENT!
                } as AzureOpenAIParameters
            } as AzureOpenAIVectorizer
        ]
    } as VectorSearch,
    semanticSearch: {
        defaultConfigurationName: "semantic_config",
        configurations: [
            {
                name: "semantic_config",
                prioritizedFields: {
                    contentFields: [
                        { name: "page_chunk" } as SemanticField
                    ]
                } as SemanticPrioritizedFields
            } as SemanticConfiguration
        ]
    } as SemanticSearch
};

const credential = new DefaultAzureCredential();

const searchIndexClient = new SearchIndexClient(process.env.AZURE_SEARCH_ENDPOINT, credential);
const searchClient = new SearchClient(process.env.AZURE_SEARCH_ENDPOINT, 'earth_at_night', credential);

await searchIndexClient.createOrUpdateIndex(index);
```

**Reference:** [SearchField](/javascript/api/@azure/search-documents/searchfield), [VectorSearch](/javascript/api/@azure/search-documents/vectorsearch), [SemanticSearch](/javascript/api/@azure/search-documents/semanticsearch), [SearchIndex](/javascript/api/@azure/search-documents/searchindex), [SearchIndexClient](/javascript/api/@azure/search-documents/searchindexclient), [SearchClient](/javascript/api/@azure/search-documents/searchclient), [DefaultAzureCredential](/javascript/api/@azure/identity/defaultazurecredential)

### Upload documents to the index

Currently, the `earth-at-night` index is empty. The following code populates the index with JSON documents from [NASA's Earth at Night e-book](https://raw.githubusercontent.com/Azure-Samples/azure-search-sample-data/refs/heads/main/nasa-e-book/earth-at-night-json/documents.json). As required by Azure AI Search, each document conforms to the fields and data types defined in the index schema.

```javascript
const response = await fetch("https://raw.githubusercontent.com/Azure-Samples/azure-search-sample-data/refs/heads/main/nasa-e-book/earth-at-night-json/documents.json");

if (!response.ok) {
    throw new Error(`Failed to fetch documents: ${response.status} ${response.statusText}`);
}
const documents = await response.json();

const bufferedClient = new SearchIndexingBufferedSender(
    searchClient,
    documentKeyRetriever,
    {
        autoFlush: true,
    },
);

await bufferedClient.uploadDocuments(documents);
await bufferedClient.flush();
await bufferedClient.dispose();

console.log(`Waiting for indexing to complete...`);
console.log(`Expected documents: ${documents.length}`);
await delay(WAIT_TIME);

let count = await searchClient.getDocumentsCount();
console.log(`Current indexed count: ${count}`);

while (count !== documents.length) {
    await delay(WAIT_TIME);
    count = await searchClient.getDocumentsCount();
    console.log(`Current indexed count: ${count}`);
}

console.log(`✓ All ${documents.length} documents indexed successfully!`);
```

**Reference:** [SearchIndexingBufferedSender](/javascript/api/@azure/search-documents/searchindexingbufferedsender)

### Create a knowledge source

A knowledge source is a reusable reference to source data. The following code defines a knowledge source named `earth-knowledge-source` that targets the `earth-at-night` index.

`source_data_fields` specifies which index fields are included in citation references. This example includes only human-readable fields to avoid lengthy, uninterpretable embeddings in responses.

```javascript
await searchIndexClient.createKnowledgeSource({
    name: 'earth-knowledge-source',
    description: "Knowledge source for Earth at Night e-book content",
    kind: "searchIndex",
    searchIndexParameters: {
        searchIndexName: 'earth_at_night',
        sourceDataFields: [
            { name: "id" },
            { name: "page_number" }
        ]
    }
});

console.log(`✅ Knowledge source 'earth-knowledge-source' created successfully.`);
```

**Reference:** [SearchIndexKnowledgeSource](/javascript/api/@azure/search-documents/searchindexknowledgesource)

### Create a knowledge base

To target `earth-knowledge-source` and your `gpt-5-mini` deployment at query time, you need a knowledge base. The following code defines a knowledge base named `earth-knowledge-base`.

`outputMode` is set to `answerSynthesis`, enabling natural-language answers that cite the retrieved documents and follow the provided `answerInstructions`.

```javascript
await searchIndexClient.createKnowledgeBase({
    name: 'earth-knowledge-base',
    knowledgeSources: [
        {
            name: 'earth-knowledge-source'
        }
    ],
    models: [
        {
            kind: "azureOpenAI",
            azureOpenAIParameters: {
                resourceUrl: process.env.AZURE_OPENAI_ENDPOINT,
                deploymentId: process.env.AZURE_OPENAI_GPT_DEPLOYMENT,
                modelName: process.env.AZURE_OPENAI_GPT_DEPLOYMENT
            }
        }
    ],
    outputMode: "answerSynthesis",
    answerInstructions: "Provide a two sentence concise and informative answer based on the retrieved documents."
});

console.log(`✅ Knowledge base 'earth-knowledge-base' created successfully.`);
```

**Reference:** [KnowledgeBase](/javascript/api/@azure/search-documents/knowledgebase)

### Run the retrieval pipeline

You're ready to run agentic retrieval. The following code sends a two-part user query to `earth-knowledge-base`, which:

1. Analyzes the entire conversation to infer the user's information need.
1. Decomposes the compound query into focused subqueries.
1. Runs the subqueries concurrently against your knowledge source.
1. Uses semantic ranker to rerank and filter the results.
1. Synthesizes the top results into a natural-language answer.

```javascript
const knowledgeRetrievalClient = new KnowledgeRetrievalClient(
    process.env.AZURE_SEARCH_ENDPOINT,
    'earth-knowledge-base',
    credential
)

const query1 = `Why do suburban belts display larger December brightening than urban cores even though absolute light levels are higher downtown? Why is the Phoenix nighttime street grid is so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?`;

const retrievalRequest = {
    messages: [
        {
            role: "user",
            content: [
                {
                    type: "text",
                    text: query1
                }
            ]
        }
    ],
    knowledgeSourceParams: [
        {
            kind: "searchIndex",
            knowledgeSourceName: 'earth-knowledge-source',
            includeReferences: true,
            includeReferenceSourceData: true,
            alwaysQuerySource: true,
            rerankerThreshold: 2.5
        }
    ],
    includeActivity: true,
    retrievalReasoningEffort: { kind: "low" }
};

const result = await knowledgeRetrievalClient.retrieveKnowledge(retrievalRequest);
```

**Reference:** [KnowledgeRetrievalClient](/javascript/api/@azure/search-documents/knowledgeretrievalclient), [KnowledgeBaseRetrievalRequest](/javascript/api/@azure/search-documents/knowledgebaseretrievalrequest)

### Review the response, activity, and references

The following code displays the response, activity, and references from the retrieval pipeline, where:

+ `Answer` provides a synthesized, LLM-generated answer to the query that cites the retrieved documents. When answer synthesis isn't enabled, this section contains content extracted directly from the documents.

+ `Activities` tracks the steps that were taken during the retrieval process, including the subqueries generated by your `gpt-5-mini` deployment and the tokens used for semantic ranking, query planning, and answer synthesis.

+ `References` lists the documents that contributed to the response, each one identified by their `docKey`.

```javascript
console.log("\n📝 ANSWER:");
console.log("─".repeat(80));
if (result.response && result.response.length > 0) {
    result.response.forEach((msg) => {
        if (msg.content && msg.content.length > 0) {
            msg.content.forEach((content) => {
                if (content.type === "text" && 'text' in content) {
                    console.log(content.text);
                }
            });
        }
    });
}
console.log("─".repeat(80));

if (result.activity) {
    console.log("\nActivities:");
    result.activity.forEach((activity) => {
        console.log(`Activity Type: ${activity.type}`);
        console.log(JSON.stringify(activity, null, 2));
    });
}

if (result.references) {
    console.log("\nReferences:");
    result.references.forEach((reference) => {
        console.log(`Reference Type: ${reference.type}`);
        console.log(JSON.stringify(reference, null, 2));
    });
}
```

### Continue the conversation

The following code continues the conversation with `earth-knowledge-base`. After you send this user query, the knowledge base fetches relevant content from `earth-knowledge-source` and appends the response to the messages list.

```javascript
const query2 = "How do I find lava at night?";
console.log(`\n❓ Follow-up question: ${query2}`);

const retrievalRequest2 = {
    messages: [
        {
            role: "user",
            content: [
                {
                    type: "text",
                    text: query2
                }
            ]
        }
    ],
    knowledgeSourceParams: [
        {
            kind: "searchIndex",
            knowledgeSourceName: 'earth-knowledge-source',
            includeReferences: true,
            includeReferenceSourceData: true,
            alwaysQuerySource: true,
            rerankerThreshold: 2.5
        }
    ],
    includeActivity: true,
    retrievalReasoningEffort: { kind: "low" }
};

const result2 = await knowledgeRetrievalClient.retrieveKnowledge(retrievalRequest2);
```

#### Review the new response, activity, and references

The following code displays the new response, activity, and references from the retrieval pipeline.

```javascript
console.log("\n📝 ANSWER:");
console.log("─".repeat(80));
if (result2.response && result2.response.length > 0) {
    result2.response.forEach((msg) => {
        if (msg.content && msg.content.length > 0) {
            msg.content.forEach((content) => {
                if (content.type === "text" && 'text' in content) {
                    console.log(content.text);
                }
            });
        }
    });
}
console.log("─".repeat(80));

if (result2.activity) {
    console.log("\nActivities:");
    result2.activity.forEach((activity) => {
        console.log(`Activity Type: ${activity.type}`);
        console.log(JSON.stringify(activity, null, 2));
    });
}

if (result2.references) {
    console.log("\nReferences:");
    result2.references.forEach((reference) => {
        console.log(`Reference Type: ${reference.type}`);
        console.log(JSON.stringify(reference, null, 2));
    });
}
```

## Clean up resources

When you work in your own subscription, it's a good idea to finish a project by determining whether you still need the resources you created. Resources that are left running can cost you money.

In the [Azure portal](https://portal.azure.com/), you can manage your Azure AI Search and Microsoft Foundry resources by selecting **All resources** or **Resource groups** from the left pane.

Otherwise, the following code from `index.js` deleted the objects you created in this quickstart.

```javascript
await searchIndexClient.deleteKnowledgeBase('earth-knowledge-base');
await searchIndexClient.deleteKnowledgeSource('earth-knowledge-source');
await searchIndexClient.deleteIndex('earth_at_night');

console.log(`\n🗑️  Cleaned up resources.`);
```
