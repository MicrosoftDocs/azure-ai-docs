---
title: "Tutorial: Create a custom analyzer using the Content Understanding TypeScript SDK"
author: PatrickFarley
manager: nitinme
description: Learn to create a custom analyzer with Content Understanding using the TypeScript SDK.
ms.service: azure-ai-content-understanding
ms.topic: include
ms.date: 03/16/2026
ms.author: lahlouchu
ai-usage: ai-assisted
---

<!-- markdownlint-disable MD025 -->

[Client library](https://www.npmjs.com/package/@azure/ai-content-understanding) | [Samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/typescript) | [SDK source](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/contentunderstanding/ai-content-understanding)

This guide shows you how to use the Content Understanding TypeScript SDK to create a custom analyzer that extracts structured data from your content. Custom analyzers support document, image, audio, and video content types.

## Prerequisites

* An active Azure subscription. If you don't have an Azure account, [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) created in a [supported region](../../language-region-support.md).
* Your resource endpoint and API key (found under **Keys and Endpoint** in the Azure portal).
* Model deployment defaults configured for your resource. See [Models and deployments](../../concepts/models-deployments.md) or this one-time [configuration script](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/typescript/src/updateDefaults.ts) for setup instructions.
* [Node.js](https://nodejs.org/) LTS version.
* [TypeScript](https://www.typescriptlang.org/) 5.x or later.

## Set up

1. Create a new Node.js project:

    ```console
    mkdir custom-analyzer-tutorial
    cd custom-analyzer-tutorial
    npm init -y
    ```

1. Install TypeScript and the Content Understanding client library:

    ```console
    npm install typescript ts-node @azure/ai-content-understanding
    ```

1. Optionally, install the Azure Identity library for Microsoft Entra authentication:

    ```console
    npm install @azure/identity
    ```

## Set up environment variables

To authenticate with the Content Understanding service, set the environment variables with your own values before running the sample:
1) `CONTENTUNDERSTANDING_ENDPOINT` - the endpoint to your Content Understanding resource.
2) `CONTENTUNDERSTANDING_KEY` - your Content Understanding API key (optional if using [Microsoft Entra ID](../../concepts/secure-communications.md) DefaultAzureCredential).

### Windows

```cmd
setx CONTENTUNDERSTANDING_ENDPOINT "your-endpoint"
setx CONTENTUNDERSTANDING_KEY "your-key"
```

### Linux / macOS

```bash
export CONTENTUNDERSTANDING_ENDPOINT="your-endpoint"
export CONTENTUNDERSTANDING_KEY="your-key"
```

## Create the client

```typescript
import { AzureKeyCredential } from "@azure/core-auth";
import {
    ContentUnderstandingClient,
} from "@azure/ai-content-understanding";
import type {
    ContentAnalyzer,
    ContentAnalyzerConfig,
    ContentFieldSchema,
} from "@azure/ai-content-understanding";

const endpoint =
    process.env["CONTENTUNDERSTANDING_ENDPOINT"]!;
const key =
    process.env["CONTENTUNDERSTANDING_KEY"]!;

const client = new ContentUnderstandingClient(
    endpoint,
    new AzureKeyCredential(key)
);
```

## Create a custom analyzer

# [Document](#tab/document)

The following example creates a custom document analyzer based on the [prebuilt document analyzer](../../concepts/prebuilt-analyzers.md). It defines fields using three extraction methods: `extract` for literal text, `generate` for AI-generated summaries, and `classify` for categorization.

```typescript
const analyzerId =
    `my_document_analyzer_${Math.floor(
        Date.now() / 1000
    )}`;

const fieldSchema: ContentFieldSchema = {
    name: "company_schema",
    description:
        "Schema for extracting company"
        + " information",
    fields: {
        company_name: {
            type: "string",
            method: "extract",
            description:
                "Name of the company",
        },
        total_amount: {
            type: "number",
            method: "extract",
            description:
                "Total amount on the document",
        },
        document_summary: {
            type: "string",
            method: "generate",
            description:
                "A brief summary of the"
                + " document content",
        },
        document_type: {
            type: "string",
            method: "classify",
            description: "Type of document",
            enum: [
                "invoice", "receipt",
                "contract", "report", "other",
            ],
        },
    },
};

const config: ContentAnalyzerConfig = {
    enableFormula: true,
    enableLayout: true,
    enableOcr: true,
    estimateFieldSourceAndConfidence: true,
    returnDetails: true,
};

const analyzer: ContentAnalyzer = {
    baseAnalyzerId: "prebuilt-document",
    description:
        "Custom analyzer for extracting"
        + " company information",
    config,
    fieldSchema,
    models: {
        completion: "gpt-4.1",
        embedding: "text-embedding-3-large",
    },
} as unknown as ContentAnalyzer;

const poller = client.createAnalyzer(
    analyzerId, analyzer
);
await poller.pollUntilDone();

const result = await client.getAnalyzer(
    analyzerId
);
console.log(
    `Analyzer '${analyzerId}' created`
    + ` successfully!`
);
```

> [!TIP]
> This code is based on the [createAnalyzer.ts](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/typescript/src/createAnalyzer.ts) sample in the SDK repository.

# [Image](#tab/image)

The following example creates a custom image analyzer based on the [prebuilt image analyzer](../../concepts/prebuilt-analyzers.md) for processing charts and graphs.

```typescript
const analyzerId =
    `my_image_analyzer_${Math.floor(
        Date.now() / 1000
    )}`;

const fieldSchema: ContentFieldSchema = {
    name: "chart_schema",
    description:
        "Schema for extracting chart"
        + " information",
    fields: {
        Title: {
            type: "string",
            description:
                "Title of the chart",
        },
        ChartType: {
            type: "string",
            method: "classify",
            description: "Type of chart",
            enum: ["bar", "line", "pie"],
        },
    },
};

const analyzer: ContentAnalyzer = {
    baseAnalyzerId: "prebuilt-image",
    description:
        "Custom analyzer for charts"
        + " and graphs",
    fieldSchema,
    models: {
        completion: "gpt-4.1",
    },
} as unknown as ContentAnalyzer;

const poller = client.createAnalyzer(
    analyzerId, analyzer
);
await poller.pollUntilDone();

console.log(
    `Analyzer '${analyzerId}' created`
    + ` successfully!`
);
```

> [!TIP]
> This code adapts the [createAnalyzer.ts](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/typescript/src/createAnalyzer.ts) pattern for image content.

# [Audio](#tab/audio)

The following example creates a custom audio analyzer based on the [prebuilt audio analyzer](../../concepts/prebuilt-analyzers.md) for processing customer support call recordings.

```typescript
const analyzerId =
    `my_audio_analyzer_${Math.floor(
        Date.now() / 1000
    )}`;

const fieldSchema: ContentFieldSchema = {
    name: "call_center_schema",
    description:
        "Schema for analyzing customer"
        + " support calls",
    fields: {
        Summary: {
            type: "string",
            method: "generate",
            description:
                "Summary of the call",
        },
        Sentiment: {
            type: "string",
            method: "classify",
            description:
                "Overall sentiment of"
                + " the call",
            enum: [
                "Positive", "Neutral",
                "Negative",
            ],
        },
        People: {
            type: "array",
            description:
                "List of people mentioned",
            items: {
                type: "object",
                properties: {
                    Name: { type: "string" },
                    Role: { type: "string" },
                },
            },
        },
    },
};

const config: ContentAnalyzerConfig = {
    locales: ["en-US", "fr-FR"],
    returnDetails: true,
};

const analyzer: ContentAnalyzer = {
    baseAnalyzerId: "prebuilt-audio",
    description:
        "Custom analyzer for customer"
        + " support calls",
    config,
    fieldSchema,
} as unknown as ContentAnalyzer;

const poller = client.createAnalyzer(
    analyzerId, analyzer
);
await poller.pollUntilDone();

console.log(
    `Analyzer '${analyzerId}' created`
    + ` successfully!`
);
```

> [!TIP]
> This code adapts the [createAnalyzer.ts](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/typescript/src/createAnalyzer.ts) pattern for audio content.

# [Video](#tab/video)

The following example creates a custom video analyzer based on the [prebuilt video analyzer](../../concepts/prebuilt-analyzers.md) for processing product demos and reviews.

```typescript
const analyzerId =
    `my_video_analyzer_${Math.floor(
        Date.now() / 1000
    )}`;

const fieldSchema: ContentFieldSchema = {
    name: "video_schema",
    description:
        "Schema for analyzing product"
        + " demo videos",
    fields: {
        Segments: {
            type: "array",
            items: {
                type: "object",
                properties: {
                    SegmentId: {
                        type: "string",
                    },
                    Description: {
                        type: "string",
                        method: "generate",
                        description:
                            "Detailed summary"
                            + " of the video"
                            + " segment",
                    },
                    Sentiment: {
                        type: "string",
                        method: "classify",
                        enum: [
                            "Positive",
                            "Neutral",
                            "Negative",
                        ],
                    },
                },
            },
        },
    },
};

const config: ContentAnalyzerConfig = {
    locales: ["en-US", "fr-FR"],
    returnDetails: true,
    segmentationMode: "auto",
};

const analyzer: ContentAnalyzer = {
    baseAnalyzerId: "prebuilt-video",
    description:
        "Custom analyzer for product"
        + " demo videos",
    config,
    fieldSchema,
    models: {
        completion: "gpt-4.1",
    },
} as unknown as ContentAnalyzer;

const poller = client.createAnalyzer(
    analyzerId, analyzer
);
await poller.pollUntilDone();

console.log(
    `Analyzer '${analyzerId}' created`
    + ` successfully!`
);
```

> [!TIP]
> This code adapts the [createAnalyzer.ts](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/typescript/src/createAnalyzer.ts) pattern for video content.

---

## Use the custom analyzer

# [Document](#tab/document)

After creating the analyzer, use it to analyze a document and extract the custom fields.

```typescript
const documentUrl =
    "https://raw.githubusercontent.com/"
    + "Azure-Samples/"
    + "azure-ai-content-understanding-python/"
    + "main/data/receipt.png";

const analyzePoller = client.analyze(
    analyzerId, [{ url: documentUrl }]
);
const analyzeResult =
    await analyzePoller.pollUntilDone();

if (analyzeResult.contents
    && analyzeResult.contents.length > 0) {
    const content = analyzeResult.contents[0];
    if (content.fields) {
        const company =
            content.fields["company_name"];
        if (company) {
            console.log(
                `Company Name: `
                + `${company.value}`
            );
            console.log(
                `  Confidence: `
                + `${company.confidence}`
            );
        }

        const summary =
            content.fields["document_summary"];
        if (summary) {
            console.log(
                `Summary: ${summary.value}`
            );
        }

        const docType =
            content.fields["document_type"];
        if (docType) {
            console.log(
                `Document Type: `
                + `${docType.value}`
            );
        }
    }
}
```

> [!TIP]
> This code adapts the [createAnalyzer.ts](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/typescript/src/createAnalyzer.ts) pattern for document content.

# [Image](#tab/image)

After creating the analyzer, use it to analyze an image and extract the custom fields.

```typescript
const imageUrl =
    "https://raw.githubusercontent.com/"
    + "Azure-Samples/"
    + "azure-ai-content-understanding-python/"
    + "main/data/pieChart.jpg";

const analyzePoller = client.analyze(
    analyzerId, [{ url: imageUrl }]
);
const analyzeResult =
    await analyzePoller.pollUntilDone();

if (analyzeResult.contents
    && analyzeResult.contents.length > 0) {
    const content = analyzeResult.contents[0];
    if (content.fields) {
        const title =
            content.fields["Title"];
        if (title) {
            console.log(
                `Title: ${title.value}`
            );
        }

        const chartType =
            content.fields["ChartType"];
        if (chartType) {
            console.log(
                `Chart Type: `
                + `${chartType.value}`
            );
        }
    }
}
```

> [!TIP]
> This code adapts the [createAnalyzer.ts](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/typescript/src/createAnalyzer.ts) pattern for image content.

# [Audio](#tab/audio)

After creating the analyzer, use it to analyze an audio file and extract the custom fields.

```typescript
const audioUrl =
    "https://raw.githubusercontent.com/"
    + "Azure-Samples/"
    + "azure-ai-content-understanding-python/"
    + "main/data/audio.wav";

const analyzePoller = client.analyze(
    analyzerId, [{ url: audioUrl }]
);
const analyzeResult =
    await analyzePoller.pollUntilDone();

if (analyzeResult.contents
    && analyzeResult.contents.length > 0) {
    const content = analyzeResult.contents[0];
    if (content.fields) {
        const summary =
            content.fields["Summary"];
        if (summary) {
            console.log(
                `Summary: ${summary.value}`
            );
        }

        const sentiment =
            content.fields["Sentiment"];
        if (sentiment) {
            console.log(
                `Sentiment: `
                + `${sentiment.value}`
            );
        }
    }
}
```

> [!TIP]
> This code adapts the [createAnalyzer.ts](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/typescript/src/createAnalyzer.ts) pattern for audio content.

# [Video](#tab/video)

After creating the analyzer, use it to analyze a video and extract the custom fields.

```typescript
const videoUrl =
    "https://raw.githubusercontent.com/"
    + "Azure-Samples/"
    + "azure-ai-content-understanding-python/"
    + "main/data/FlightSimulator.mp4";

const analyzePoller = client.analyze(
    analyzerId, [{ url: videoUrl }]
);
const analyzeResult =
    await analyzePoller.pollUntilDone();

if (analyzeResult.contents
    && analyzeResult.contents.length > 0) {
    const content = analyzeResult.contents[0];
    console.log(
        `Content kind: ${content.kind}`
    );
    if (content.fields) {
        const segments =
            content.fields["Segments"];
        if (segments) {
            console.log(
                `Segments: `
                + JSON.stringify(
                    segments, null, 2
                )
            );
        }
    }
}
```

> [!TIP]
> This code adapts the [createAnalyzer.ts](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/typescript/src/createAnalyzer.ts) pattern for video content.

---

## Clean up resources

Delete the analyzer when you no longer need it.

```typescript
await client.deleteAnalyzer(analyzerId);
console.log(
    `Analyzer '${analyzerId}' deleted`
    + ` successfully.`
);
```

> [!NOTE]
> The document example is based on the [createAnalyzer.ts](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/typescript/src/createAnalyzer.ts) sample. Custom analyzers support the same field schema concepts across all content types. For the complete set of samples, see [TypeScript SDK samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/typescript).