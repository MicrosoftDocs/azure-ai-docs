---
author: diberry
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
  - dev-focus
ms.topic: include
ms.date: 03/04/2026
ai-usage: ai-assisted
---

In this quickstart, you use the [Azure AI Search client library for JavaScript](/javascript/api/overview/azure/search-documents-readme) (compatible with TypeScript) to add [semantic ranking](../../semantic-search-overview.md) to an existing search index and query the index.

Semantic ranking is query-side functionality that uses machine reading comprehension to rescore search results, promoting the most semantically relevant matches to the top of the list. You can add a semantic configuration to an existing index with no rebuild requirement.  Semantic ranking is most effective for informational or descriptive text.

> [!TIP]
> Want to get started right away? Download the [source code](https://github.com/Azure-Samples/azure-search-javascript-samples/tree/main/quickstart-semantic-ranking-ts) on GitHub.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](../../search-create-service-portal.md) with [semantic ranker enabled](../../semantic-how-to-enable-disable.md).

+ An [index](../../search-how-to-create-search-index.md) with descriptive text fields attributed as `searchable` and `retrievable`.  This quickstart assumes the [hotels-sample](../../search-get-started-portal.md) index.

+ [Node.js 20 LTS](https://nodejs.org/en/download/) or later to run the compiled code.

+ [TypeScript](https://www.typescriptlang.org/download/) to compile TypeScript to JavaScript.

+ [Visual Studio Code](https://code.visualstudio.com/download).

+ [Git](https://git-scm.com/downloads) to clone the sample repository.

+ The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

## Configure access

[!INCLUDE [resource authentication](../resource-authentication-semantic.md)]

## Get endpoint

[!INCLUDE [resource endpoint](../resource-endpoint.md)]

## Start with an index

[!INCLUDE [start with an index](semantic-ranker-index.md)]

## Set up the environment

1. Use Git to clone the sample repository.

    ```bash
    git clone https://github.com/Azure-Samples/azure-search-javascript-samples
    ```

1. Navigate to the quickstart folder and open it in Visual Studio Code.

    ```bash
    cd azure-search-javascript-samples/quickstart-semantic-ranking-ts
    code .
    ```

1. In `sample.env`, replace the placeholder value for `AZURE_SEARCH_ENDPOINT` with the URL you obtained in [Get endpoint](#get-endpoint).

1. Rename `sample.env` to `.env`.

    ```bash
    mv sample.env .env
    ```

1. Install the dependencies.

    ```bash
    npm install
    ```

    When the installation completes, you should see a `node_modules` folder in the project directory.

1. Build the TypeScript files.

    ```bash
    npm run build
    ```

1. For keyless authentication with Microsoft Entra ID, sign in to your Azure account. If you have multiple subscriptions, select the one that contains your Azure AI Search service.

    ```azurecli
    az login
    ```

## Run the code

1. Get the existing index settings.

    ```bash
    node -r dotenv/config dist/getIndexSettings.js
    ```

1. Update the index with a semantic configuration.

    ```bash
    node -r dotenv/config dist/updateIndexSettings.js
    ```

1. Run a semantic query.

    ```bash
    node -r dotenv/config dist/semanticQuery.js
    ```

1. Run a semantic query with captions.

    ```bash
    node -r dotenv/config dist/semanticQueryReturnCaptions.js
    ```

1. Run a semantic query with answers.

    ```bash
    node -r dotenv/config dist/semanticAnswer.js
    ```

> [!NOTE]
> These commands run `.js` files from the `dist` folder because you previously transpiled from TypeScript to JavaScript with `npm run build`.

### Output

The `getIndexSettings.js` script returns the index name, field count, field details with type and searchable status, and any existing semantic configurations.

```output
Index name: hotels-sample
Number of fields: 23
Field: HotelId, Type: Edm.String, Searchable: true
Field: HotelName, Type: Edm.String, Searchable: true
Field: Description, Type: Edm.String, Searchable: true
// Trimmed for brevity
Semantic ranking configurations: 1
Configuration name: hotels-sample-semantic-configuration
Title field: undefined
```

The `updateIndexSettings.js` script returns all semantic configurations, including the one you added.

```output
Semantic configurations:
----------------------------------------
Configuration name: hotels-sample-semantic-configuration
Title field: undefined
Keywords fields:
Content fields: AzureSearch_DocumentKey
----------------------------------------
Configuration name: semantic-config
Title field: HotelName
Keywords fields: Tags
Content fields: Description
----------------------------------------
Semantic configuration updated successfully.
```

The `semanticQuery.js` script returns results ordered by the reranker score.

```output
Search result #1:
  Re-ranker Score: 2.613231658935547
  HotelId: 24
  HotelName: Uptown Chic Hotel
  Description: Chic hotel near the city. High-rise hotel in downtown,
  within walking distance to theaters, art galleries, restaurants and
  shops. Visit Seattle Art Museum by day, and then head over to
  Benaroya Hall to catch the evening's concert performance.

Search result #2:
  Re-ranker Score: 2.271434783935547
  HotelId: 2
  HotelName: Old Century Hotel
  Description: The hotel is situated in a nineteenth century plaza...
  // Trimmed for brevity
```

The `semanticQueryReturnCaptions.js` script returns extractive captions with hit highlighting. Captions are the most relevant passages in a result.

```output
Search result #1:
  Re-ranker Score: 2.613231658935547
  HotelName: Uptown Chic Hotel
  Description: Chic hotel near the city. High-rise hotel in downtown,
  within walking distance to theaters, art galleries, restaurants and
  shops. Visit Seattle Art Museum by day, and then head over to
  Benaroya Hall to catch the evening's concert performance.

  Caption with highlights: Chic hotel near the city. High-rise hotel
  in downtown, within walking distance to<em> theaters, </em>art
  galleries, restaurants and shops. Visit<em> Seattle Art Museum
  </em>by day, and then head over to<em> Benaroya Hall </em>to catch
  the evening's concert performance.
------------------------------------------------------------
Search result #2:
  Re-ranker Score: 2.271434783935547
  HotelName: Old Century Hotel
  // Trimmed for brevity
```

The `semanticAnswer.js` script returns a semantic answer (verbatim content) pulled from the result that best matches the question.

```output
Semantic answer result #1:
Semantic Answer: Nature is Home on the beach. Explore the shore by
day, and then come home to our shared living space to relax around
a stone fireplace, sip something warm, and explore the<em> library
</em>by night. Save up to 30 percent. Valid Now through the end of
the year. Restrictions and blackouts may apply.
Semantic Answer Score: 0.9829999804496765

Search Results:

Search result #1:
2.124817371368408
Stay-Kay City Hotel
This classic hotel is fully-refurbished and ideally located on the
main commercial artery of the city in the heart of New York...
Caption: This classic hotel is<em> fully-refurbished </em>and
ideally located on the main commercial artery of the city...
// Trimmed for brevity
```

## Understand the code

[!INCLUDE [understand code note](../understand-code-note.md)]

Now that you've run the code, let's break down the key steps:

1. [Configuration and authentication](#configuration-and-authentication)
1. [Update the index with a semantic configuration](#update-the-index-with-a-semantic-configuration)
1. [Query the index](#query-the-index)

### Configuration and authentication

The `config.ts` file loads environment variables, creates a `DefaultAzureCredential` for authentication, and defines a `HotelDocument` interface for type safety.

```typescript
import { DefaultAzureCredential }
    from "@azure/identity";

export const searchEndpoint =
    process.env.AZURE_SEARCH_ENDPOINT
    || "PUT-YOUR-SEARCH-SERVICE-ENDPOINT-HERE";
export const indexName =
    process.env.AZURE_SEARCH_INDEX_NAME
    || "hotels-sample";
export const semanticConfigurationName =
    process.env.SEMANTIC_CONFIGURATION_NAME
    || "semantic-config";

export const credential = new DefaultAzureCredential();

export interface HotelDocument {
    HotelId: string;
    HotelName: string;
    Description: string;
    Category: string;
    Tags: string[];
}
```

Key takeaways:

+ `DefaultAzureCredential` provides keyless authentication using Microsoft Entra ID. It chains multiple credential types, including the Azure CLI credential from `az login`.
+ The `HotelDocument` interface provides compile-time type checking for search results, ensuring type-safe access to document fields.
+ Environment variables are loaded from the `.env` file using `dotenv`.

### Update the index with a semantic configuration

The `updateIndexSettings.ts` file adds a semantic configuration to the existing `hotels-sample` index. This operation doesn't delete any search documents, and your index remains operational after the configuration is added. TypeScript type annotations ensure the configuration matches the expected schema.

```typescript
import {
    SearchIndexClient,
    SemanticConfiguration,
    SemanticPrioritizedFields,
    SemanticField
} from "@azure/search-documents";
import {
    searchEndpoint, indexName,
    credential, semanticConfigurationName
} from "./config.js";

const indexClient = new SearchIndexClient(
    searchEndpoint, credential
);
const existingIndex =
    await indexClient.getIndex(indexName);

const fields: SemanticPrioritizedFields = {
    titleField: { name: "HotelName" },
    keywordsFields: [
        { name: "Tags" }
    ] as SemanticField[],
    contentFields: [
        { name: "Description" }
    ] as SemanticField[]
};

const newSemanticConfiguration:
    SemanticConfiguration = {
    name: semanticConfigurationName,
    prioritizedFields: fields
};

if (existingIndex.semanticSearch
    && existingIndex.semanticSearch.configurations) {
    existingIndex.semanticSearch.configurations
        .push(newSemanticConfiguration);
} else {
    existingIndex.semanticSearch = {
        configurations: [newSemanticConfiguration]
    };
}

await indexClient.createOrUpdateIndex(existingIndex);
```

Key takeaways:

+ TypeScript types like `SemanticPrioritizedFields`, `SemanticConfiguration`, and `SemanticField` provide compile-time validation for the configuration structure.
+ `titleField` sets the document title, `contentFields` sets the main content, and `keywordsFields` sets the keyword or tag fields.
+ `createOrUpdateIndex` pushes the updated schema to the search service without rebuilding the index or deleting documents.

### Query the index

The query scripts run three queries in sequence, progressing from a basic semantic search to semantic ranking with captions and answers.

#### Semantic query (no captions, no answers)

The `semanticQuery.ts` script shows the minimum requirement for invoking semantic ranking with type-safe results.

```typescript
import { SearchClient }
    from "@azure/search-documents";
import {
    HotelDocument, credential,
    searchEndpoint, indexName,
    semanticConfigurationName
} from "./config.js";

const searchClient =
    new SearchClient<HotelDocument>(
        searchEndpoint, indexName, credential
    );

const results = await searchClient.search(
    "walking distance to live music",
    {
        queryType: "semantic",
        semanticSearchOptions: {
            configurationName:
                semanticConfigurationName
        },
        select: [
            "HotelId", "HotelName", "Description"
        ]
    }
);
```

Key takeaways:

+ `SearchClient<HotelDocument>` provides type-safe access to document fields in results, with autocomplete for field names in `select` and `result.document`.
+ `queryType: "semantic"` enables semantic ranking on the query.
+ `semanticSearchOptions.configurationName` specifies which semantic configuration to use.

#### Semantic query with captions

The `semanticQueryReturnCaptions.ts` script adds captions to extract the most relevant passages from each result, with hit highlighting applied to the important terms and phrases.

```typescript
const results = await searchClient.search(
    "walking distance to live music",
    {
        queryType: "semantic",
        semanticSearchOptions: {
            configurationName:
                semanticConfigurationName,
            captions: {
                captionType: "extractive",
                highlight: true
            }
        },
        select: [
            "HotelId", "HotelName", "Description"
        ]
    }
);

for await (const result of results.results) {
    const captions = result.captions;
    if (captions && captions.length > 0) {
        const caption = captions[0];
        if (caption.highlights) {
            console.log(
                `Caption: ${caption.highlights}`
            );
        }
    }
}
```

Key takeaways:

+ `captions.captionType: "extractive"` enables extractive captions from the content fields.
+ Captions surface the most relevant passages and add `<em>` tags around important terms.

#### Semantic query with answers

The `semanticAnswer.ts` script adds semantic answers. It uses a question as the search text because semantic answers work best when the query is phrased as a question. The answer is a verbatim passage extracted from your index, not a composed response from a chat completion model.

The query and the indexed content must be closely aligned for an answer to be returned. If no candidate meets the confidence threshold, the response doesn't include an answer. This example uses a question that's known to produce a result so that you can see the syntax. If answers aren't useful for your scenario, omit `answers` from your code. For composed answers, consider a [RAG pattern](../../retrieval-augmented-generation-overview.md) or [agentic retrieval](../../agentic-retrieval-overview.md).

```typescript
const results = await searchClient.search(
    "What's a good hotel for people who "
    + "like to read",
    {
        queryType: "semantic",
        semanticSearchOptions: {
            configurationName:
                semanticConfigurationName,
            captions: {
                captionType: "extractive"
            },
            answers: {
                answerType: "extractive"
            }
        },
        select: [
            "HotelName", "Description", "Category"
        ]
    }
);

const semanticAnswers = results.answers;
for (const answer of semanticAnswers || []) {
    if (answer.highlights) {
        console.log(
            `Semantic Answer: ${answer.highlights}`
        );
    } else {
        console.log(
            `Semantic Answer: ${answer.text}`
        );
    }
    console.log(
        `Semantic Answer Score: ${answer.score}`
    );
}
```

Key takeaways:

+ `answers.answerType: "extractive"` enables extractive answers for question-like queries.
+ Answers are verbatim content extracted from your index, not generated text.
+ `results.answers` retrieves the answer objects separately from the search results.
