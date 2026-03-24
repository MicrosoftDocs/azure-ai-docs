---
title: "Tutorial: Create a custom analyzer using the Content Understanding JavaScript SDK"
author: PatrickFarley
manager: nitinme
description: Learn to create a custom analyzer with Content Understanding using the JavaScript SDK.
ms.service: azure-ai-content-understanding
ms.topic: include
ms.date: 03/16/2026
ms.author: lahlouchu
ai-usage: ai-assisted
---

<!-- markdownlint-disable MD025 -->

[Client library](https://www.npmjs.com/package/@azure/ai-content-understanding) | [Samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/javascript) | [SDK source](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/contentunderstanding/ai-content-understanding)

This guide shows you how to use the Content Understanding JavaScript SDK to create a custom analyzer that extracts structured data from your content. Custom analyzers support document, image, audio, and video content types.

## Prerequisites

* An active Azure subscription. If you don't have an Azure account, [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) created in a [supported region](../../language-region-support.md).
* Your resource endpoint and API key (found under **Keys and Endpoint** in the Azure portal).
* Model deployment defaults configured for your resource. See [Models and deployments](../../concepts/models-deployments.md) or this one-time [configuration script](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/javascript/updateDefaults.js) for setup instructions.
* [Node.js](https://nodejs.org/) LTS version.

## Set up

1. Create a new Node.js project:

    ```console
    mkdir custom-analyzer-tutorial
    cd custom-analyzer-tutorial
    npm init -y
    ```

1. Install the Content Understanding client library:

    ```console
    npm install @azure/ai-content-understanding
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

```javascript
const { AzureKeyCredential } =
    require("@azure/core-auth");
const {
    ContentUnderstandingClient,
} = require("@azure/ai-content-understanding");

const endpoint =
    process.env["CONTENTUNDERSTANDING_ENDPOINT"];
const key =
    process.env["CONTENTUNDERSTANDING_KEY"];

const client = new ContentUnderstandingClient(
    endpoint,
    new AzureKeyCredential(key)
);
```

## Create a custom analyzer

# [Document](#tab/document)

The following example creates a custom document analyzer based on the [prebuilt document analyzer](../../concepts/prebuilt-analyzers.md). It defines fields using three extraction methods: `extract` for literal text, `generate` for AI-generated summaries, and `classify` for categorization.

```javascript
const analyzerId =
    `my_document_analyzer_${Math.floor(
        Date.now() / 1000
    )}`;

const analyzer = {
    baseAnalyzerId: "prebuilt-document",
    description:
        "Custom analyzer for extracting"
        + " company information",
    config: {
        enableFormula: true,
        enableLayout: true,
        enableOcr: true,
        estimateFieldSourceAndConfidence: true,
        returnDetails: true,
    },
    fieldSchema: {
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
                    "Total amount on the"
                    + " document",
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
    },
    models: {
        completion: "gpt-4.1",
        embedding: "text-embedding-3-large", // Required when using field_schema and prebuilt-document base analyzer
    },
};

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

if (result.description) {
    console.log(
        `  Description: ${result.description}`
    );
}

if (result.fieldSchema?.fields) {
    const fields = result.fieldSchema.fields;
    console.log(
        `  Fields`
        + ` (${Object.keys(fields).length}):`
    );
    for (const [name, fieldDef]
        of Object.entries(fields)) {
        const method =
            fieldDef.method ?? "auto";
        const fieldType =
            fieldDef.type ?? "unknown";
        console.log(
            `    - ${name}: `
            + `${fieldType} (${method})`
        );
    }
}
```

An example output looks like:

```text
Analyzer 'my_document_analyzer_ID' created successfully!
  Description: Custom analyzer for extracting company information
  Fields (4):
    - company_name: string (extract)
    - total_amount: number (extract)
    - document_summary: string (generate)
    - document_type: string (classify)
```

> [!TIP]
> This code is based on the [createAnalyzer.js](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/javascript/createAnalyzer.js) sample in the SDK repository.


Optionally, you can create a classifier analyzer to categorize documents and use its results to route documents to prebuilt or custom analyzers you created. Here is an example of creating a custom analyzer for classification workflows.

```javascript
const classifierId =
    `my_classifier_${Math.floor(
        Date.now() / 1000
    )}`;

console.log(
    `Creating classifier '${classifierId}'...`
);

const classifierAnalyzer = {
    baseAnalyzerId: "prebuilt-document",
    description:
        "Custom classifier for financial"
        + " document categorization",
    config: {
        returnDetails: true,
        enableSegment: true,
        contentCategories: {
            Loan_Application: {
                description:
                    "Documents submitted by"
                    + " individuals or"
                    + " businesses to request"
                    + " funding, typically"
                    + " including personal or"
                    + " business details,"
                    + " financial history,"
                    + " loan amount, purpose,"
                    + " and supporting"
                    + " documentation.",
            },
            Invoice: {
                description:
                    "Billing documents issued"
                    + " by sellers or service"
                    + " providers to request"
                    + " payment for goods or"
                    + " services, detailing"
                    + " items, prices, taxes,"
                    + " totals, and payment"
                    + " terms.",
            },
            Bank_Statement: {
                description:
                    "Official statements"
                    + " issued by banks that"
                    + " summarize account"
                    + " activity over a"
                    + " period, including"
                    + " deposits, withdrawals,"
                    + " fees, and balances.",
            },
        },
    },
    models: {
        completion: "gpt-4.1",
    },
};

const classifierPoller =
    client.createAnalyzer(
        classifierId, classifierAnalyzer
    );
await classifierPoller.pollUntilDone();

const classifierResult =
    await client.getAnalyzer(classifierId);

console.log(
    `Classifier '${classifierId}' created`
    + ` successfully!`
);

if (classifierResult.description) {
    console.log(
        `  Description: `
        + `${classifierResult.description}`
    );
}
```

> [!TIP]
> This code is based on the [createClassifier.js](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/javascript/createClassifier.js) sample for classification workflows.



# [Image](#tab/image)

The following example creates a custom image analyzer based on the [prebuilt image analyzer](../../concepts/prebuilt-analyzers.md) for processing charts and graphs.

```javascript
const analyzerId =
    `my_image_analyzer_${Math.floor(
        Date.now() / 1000
    )}`;

const analyzer = {
    baseAnalyzerId: "prebuilt-image",
    description:
        "Custom analyzer for charts and graphs",
    fieldSchema: {
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
    },
    models: {
        completion: "gpt-4.1",
    },
};

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

if (result.description) {
    console.log(
        `  Description: ${result.description}`
    );
}

if (result.fieldSchema?.fields) {
    const fields = result.fieldSchema.fields;
    console.log(
        `  Fields`
        + ` (${Object.keys(fields).length}):`
    );
    for (const [name, fieldDef]
        of Object.entries(fields)) {
        const method =
            fieldDef.method ?? "auto";
        const fieldType =
            fieldDef.type ?? "unknown";
        console.log(
            `    - ${name}: `
            + `${fieldType} (${method})`
        );
    }
}
```

An example output looks like:

```text
Analyzer 'my_image_analyzer_ID' created successfully!
  Description: Custom analyzer for charts and graphs
  Fields (2):
    - Title: string (auto)
    - ChartType: string (classify)
```

> [!TIP]
> This code adapts the [createAnalyzer.js](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/javascript/createAnalyzer.js) pattern for image content.

# [Audio](#tab/audio)

The following example creates a custom audio analyzer based on the [prebuilt audio analyzer](../../concepts/prebuilt-analyzers.md) for processing customer support call recordings.

```javascript
const analyzerId =
    `my_audio_analyzer_${Math.floor(
        Date.now() / 1000
    )}`;

const analyzer = {
    baseAnalyzerId: "prebuilt-audio",
    description:
        "Custom analyzer for customer"
        + " support calls",
    config: {
        locales: ["en-US", "fr-FR"],
        returnDetails: true,
    },
    fieldSchema: {
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
                itemDefinition: {
                    type: "object",
                    properties: {
                        Name: {
                            type: "string",
                        },
                        Role: {
                            type: "string",
                        },
                    },
                },
            },
        },
    },
    models: {
        completion: "gpt-4.1",
        embedding: "text-embedding-3-large",
    },
};

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

if (result.description) {
    console.log(
        `  Description: ${result.description}`
    );
}

if (result.fieldSchema?.fields) {
    const fields = result.fieldSchema.fields;
    console.log(
        `  Fields`
        + ` (${Object.keys(fields).length}):`
    );
    for (const [name, fieldDef]
        of Object.entries(fields)) {
        const method =
            fieldDef.method ?? "auto";
        const fieldType =
            fieldDef.type ?? "unknown";
        console.log(
            `    - ${name}: `
            + `${fieldType} (${method})`
        );
    }
}
```

An example output looks like:

```text
Analyzer 'my_audio_analyzer_ID' created successfully!
  Description: Custom analyzer for customer support calls
  Fields (3):
    - Summary: string (generate)
    - Sentiment: string (classify)
    - People: array (auto)
```

> [!TIP]
> This code adapts the [createAnalyzer.js](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/javascript/createAnalyzer.js) pattern for audio content.

# [Video](#tab/video)

The following example creates a custom video analyzer based on the [prebuilt video analyzer](../../concepts/prebuilt-analyzers.md) for processing product demos and reviews.

```javascript
const analyzerId =
    `my_video_analyzer_${Math.floor(
        Date.now() / 1000
    )}`;

const analyzer = {
    baseAnalyzerId: "prebuilt-video",
    description:
        "Custom analyzer for product"
        + " demo videos",
    config: {
        locales: ["en-US", "fr-FR"],
        returnDetails: true,
    },
    fieldSchema: {
        name: "video_schema",
        description:
            "Schema for analyzing product"
            + " demo videos",
        fields: {
            Segments: {
                type: "array",
                itemDefinition: {
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
    },
    models: {
        completion: "gpt-4.1",
    },
};

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

if (result.description) {
    console.log(
        `  Description: ${result.description}`
    );
}

if (result.fieldSchema?.fields) {
    const fields = result.fieldSchema.fields;
    console.log(
        `  Fields`
        + ` (${Object.keys(fields).length}):`
    );
    for (const [name, fieldDef]
        of Object.entries(fields)) {
        const method =
            fieldDef.method ?? "auto";
        const fieldType =
            fieldDef.type ?? "unknown";
        console.log(
            `    - ${name}: `
            + `${fieldType} (${method})`
        );
    }
}
```

An example output looks like:

```text
Analyzer 'my_video_analyzer_ID' created successfully!
  Description: Custom analyzer for product demo videos
  Fields (1):
    - Segments: array (auto)
```

> [!TIP]
> This code adapts the [createAnalyzer.js](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/javascript/createAnalyzer.js) pattern for video content.

---

## Use the custom analyzer

# [Document](#tab/document)

After creating the analyzer, use it to analyze a document and extract the custom fields. Delete the analyzer when you no longer need it.

```javascript
const documentUrl =
    "https://raw.githubusercontent.com/"
    + "Azure-Samples/"
    + "azure-ai-content-understanding-assets/"
    + "main/document/invoice.pdf";

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

        const total =
            content.fields["total_amount"];
        if (total) {
            console.log(
                `Total Amount: `
                + `${total.value}`
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

// --- Clean up ---
console.log(
    `\nCleaning up: deleting analyzer`
    + ` '${analyzerId}'...`
);
await client.deleteAnalyzer(analyzerId);
console.log(
    `Analyzer '${analyzerId}' deleted`
    + ` successfully.`
);
```

An example output looks like:

```text
Company Name: CONTOSO LTD.
  Confidence: 0.739
Total Amount: 610
Summary: This document is an invoice from CONTOSO LTD. to Microsoft Corporation for consulting, document, and printing services provided during the service period. It details line items, subtotal, sales tax, total, previous unpaid balance, and the final amount due.
Document Type: invoice

Cleaning up: deleting analyzer 'my_document_analyzer_ID'...
Analyzer 'my_document_analyzer_ID' deleted successfully.
```

> [!TIP]
> Check out more examples of running analyzers at [JavaScript SDK samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/javascript).

# [Image](#tab/image)

After creating the analyzer, use it to analyze an image and extract the custom fields. Delete the analyzer when you no longer need it.

```javascript
const imageUrl =
    "https://raw.githubusercontent.com/"
    + "Azure-Samples/"
    + "azure-ai-content-understanding-assets/"
    + "main/image/pieChart.jpg";

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

// --- Clean up ---
console.log(
    `\nCleaning up: deleting analyzer`
    + ` '${analyzerId}'...`
);
await client.deleteAnalyzer(analyzerId);
console.log(
    `Analyzer '${analyzerId}' deleted`
    + ` successfully.`
);
```

An example output looks like:

```text
Title: Distribution of Weekly Working Hours
Chart Type: pie

Cleaning up: deleting analyzer 'my_image_analyzer_ID'...
Analyzer 'my_image_analyzer_ID' deleted successfully.
```

> [!TIP]
> Check out more examples of running analyzers at [JavaScript SDK samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/javascript).

# [Audio](#tab/audio)

After creating the analyzer, use it to analyze an audio file and extract the custom fields. Delete the analyzer when you no longer need it.

```javascript
const audioUrl =
    "https://raw.githubusercontent.com/"
    + "Azure-Samples/"
    + "azure-ai-content-understanding-assets/"
    + "main/audio/callCenterRecording.mp3";

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

// --- Clean up ---
console.log(
    `\nCleaning up: deleting analyzer`
    + ` '${analyzerId}'...`
);
await client.deleteAnalyzer(analyzerId);
console.log(
    `Analyzer '${analyzerId}' deleted`
    + ` successfully.`
);
```

An example output looks like:

```text
Summary: Maria Smith contacted Contoso to inquire about her current point balance. John Doe, the representative, verified her identity by requesting her date of birth and then provided her with her point balance of 599 points. Maria confirmed she needed no further information and ended the call.
Sentiment: Positive

Cleaning up: deleting analyzer 'my_audio_analyzer_ID'...
Analyzer 'my_audio_analyzer_ID' deleted successfully.
```

> [!TIP]
> Check out more examples of running analyzers at [JavaScript SDK samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/javascript).

# [Video](#tab/video)

After creating the analyzer, use it to analyze a video and extract the custom fields. Delete the analyzer when you no longer need it.

```javascript
const videoUrl =
    "https://raw.githubusercontent.com/"
    + "Azure-Samples/"
    + "azure-ai-content-understanding-assets/"
    + "main/videos/sdk_samples/"
    + "FlightSimulator.mp4";

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
        if (segments && segments.value) {
            console.log(
                `Segments`
                + ` (${segments.value.length}):`
            );
            for (const segment
                of segments.value) {
                const segId =
                    segment.value
                        ?.SegmentId?.value
                    ?? "N/A";
                const desc =
                    segment.value
                        ?.Description?.value
                    ?? "N/A";
                const sent =
                    segment.value
                        ?.Sentiment?.value
                    ?? "N/A";
                console.log(
                    `  Segment: ${segId}`
                );
                console.log(
                    `    Description:`
                    + ` ${desc}`
                );
                console.log(
                    `    Sentiment:`
                    + ` ${sent}`
                );
            }
        }
    }
}

// --- Clean up ---
console.log(
    `\nCleaning up: deleting analyzer`
    + ` '${analyzerId}'...`
);
await client.deleteAnalyzer(analyzerId);
console.log(
    `Analyzer '${analyzerId}' deleted`
    + ` successfully.`
);
```

An example output looks like:

```text
Content kind: audioVisual
Segments (16):
  Segment: 00:00:00.000-00:00:01.467
    Description: The video opens with a scenic aerial view of an island surrounded by turquoise water. A small airplane is flying over the landscape. The screen displays the logos for 'Flight Simulator' and 'Microsoft Azure AI', indicating a collaboration or integration between the two.
    Sentiment: Positive
  Segment: 00:00:01.467-00:00:03.233
    Description: A man is shown sitting in a modern office setting, likely preparing to speak or introduce the topic. The background features geometric wall lights and a plant, giving a professional and contemporary atmosphere.
    Sentiment: Neutral
  Segment: 00:00:03.233-00:00:07.367
    Description: The screen displays a digital audio waveform, suggesting a focus on audio technology. The accompanying transcript discusses the importance of good data for neural TTS (Text-to-Speech) to achieve a high-quality voice.
    Sentiment: Neutral
  Segment: 00:00:07.367-00:00:08.200
    Description: Another man is shown in a similar office environment, possibly continuing the explanation or providing additional information about the product.
    Sentiment: Neutral
  Segment: 00:00:08.200-00:00:11.367
    Description: The video transitions to an outdoor scene showing a large facility with multiple buildings, set in a rural landscape. This likely represents the data centers or infrastructure supporting the technology.
    Sentiment: Neutral
  Segment: 00:00:11.367-00:00:13.567
    Description: The camera moves inside a data center, showing rows of servers and high-tech equipment. This emphasizes the scale and capability of the infrastructure used for the TTS model.
    Sentiment: Neutral
  Segment: 00:00:13.567-00:00:16.100
    Description: The man from earlier is shown again in the office, likely elaborating on the accumulation of data and the universal TTS model, as mentioned in the transcript.
    Sentiment: Neutral
  Segment: 00:00:16.100-00:00:19.433
    Description: A biplane is seen flying over a coastal city with clear blue water and lush green hills, highlighting the realism and immersive visuals of the Flight Simulator.
    Sentiment: Positive
  Segment: 00:00:19.433-00:00:23.967
    Description: The video shows a castle surrounded by mountains and clouds, with a small aircraft flying nearby. This further showcases the detailed environments possible in the Flight Simulator.
    Sentiment: Positive
  Segment: 00:00:23.967-00:00:30.033
    Description: A bald man is interviewed in a modern office setting. The transcript discusses the high fidelity and naturalness of voices generated by cognitive services, suggesting he is explaining the benefits of the technology.
    Sentiment: Positive
  Segment: 00:00:30.033-00:00:33.200
    Description: The bald man continues speaking, possibly providing more details about the product's capabilities and its impact on user experience.
    Sentiment: Positive
  Segment: 00:00:33.200-00:00:35.267
    Description: The video shifts to an overhead view of an airplane on the runway, preparing for movement. This scene likely relates to the realism of the simulator and the integration of AI-driven voice technology.
    Sentiment: Neutral
  Segment: 00:00:35.267-00:00:37.700
    Description: A ground crew member directs an Airbus aircraft, with pilots visible in the cockpit. This scene emphasizes the operational realism and communication aspects in the simulator.
    Sentiment: Neutral
  Segment: 00:00:37.700-00:00:39.200
    Description: Two ground crew members walk near an aircraft on the tarmac, with airport buildings and other planes in the background. The environment is realistic and detailed.
    Sentiment: Neutral
  Segment: 00:00:39.200-00:00:42.033
    Description: A close-up of an Airbus aircraft at the gate, with sunlight illuminating the scene. This further highlights the visual fidelity and immersive experience of the simulator.
    Sentiment: Positive
  Segment: 00:00:42.033-00:00:43.866
    Description: The video ends with the Microsoft logo and branding, signaling the conclusion of the product demo and reinforcing the partnership between Flight Simulator and Microsoft Azure AI.
    Sentiment: Positive

Cleaning up: deleting analyzer 'my_video_analyzer_ID'...
Analyzer 'my_video_analyzer_ID' deleted successfully.
```

> [!TIP]
> Check out more examples of running analyzers at [JavaScript SDK samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/javascript).

---



