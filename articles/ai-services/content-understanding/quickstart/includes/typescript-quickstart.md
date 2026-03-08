---
title: "Quickstart: Use the Content Understanding TypeScript SDK"
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: include
ms.date: 03/06/2026
ms.author: lahlouchu
ai-usage: ai-assisted
---

<!-- markdownlint-disable MD025 -->

[Client library](https://www.npmjs.com/package/@azure/ai-content-understanding) | [Samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/typescript) | [SDK source](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/contentunderstanding/ai-content-understanding)

This quickstart shows you how to use the Content Understanding TypeScript SDK to extract structured data using prebuilt analyzers from document, image, audio, and video files. To learn more about prebuilt analyzers and other features, see the documentation of [Prebuilt Analyzers](../../concepts/prebuilt-analyzers.md).

## Prerequisites

* An active Azure subscription. If you don't have an Azure account, [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) created in a [supported region](https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/language-region-support).
* Your resource endpoint and API key (found under Keys and Endpoint in the Azure portal).
* Model deployment defaults configured for your resource. See [Models and deployments](../../concepts/models-deployments.md) or this one-time [configuration script](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/typescript/src/updateDefaults.ts) for setup instructions.
* [Node.js](https://nodejs.org/) LTS version.
* [TypeScript](https://www.typescriptlang.org/) 5.x or later.

## Set up

1. Create a new Node.js project:

    ```console
    mkdir content-understanding-quickstart
    cd content-understanding-quickstart
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


# [Windows](#tab/windows)

```cmd
setx CONTENTUNDERSTANDING_ENDPOINT "your-endpoint"
setx CONTENTUNDERSTANDING_KEY "your-key"
```

# [Linux / macOS](#tab/linux)

```bash
export CONTENTUNDERSTANDING_ENDPOINT="your-endpoint"
export CONTENTUNDERSTANDING_KEY="your-key"
```

## Create a client

The `ContentUnderstandingClient` is the main entry point for interacting with the service. Create an instance by providing your endpoint and credential.

```typescript
import { AzureKeyCredential } from "@azure/core-auth";
import {
    ContentUnderstandingClient,
} from "@azure/ai-content-understanding";

const endpoint = process.env["CONTENTUNDERSTANDING_ENDPOINT"];
const key = process.env["CONTENTUNDERSTANDING_KEY"];

const client = new ContentUnderstandingClient(
    endpoint,
    new AzureKeyCredential(key)
);
```

## Get started with a prebuilt analyzer

Analyzers define how your content is processed and the insights that are extracted. We offer [prebuilt analyzers](../../concepts/prebuilt-analyzers.md) for common use cases. You can [customize prebuilt analyzers](../../concepts/prebuilt-analyzers.md) to better fit your specific needs and use cases.
This quickstart uses prebuilt invoice, image, audio, and video analyzers to help you get started.


# [Document](#tab/document)

This example uses the `prebuilt-invoice` analyzer to extract structured data from an invoice document.

```typescript
import {
    type DocumentContent,
    type ArrayField,
    type ObjectField,
} from "@azure/ai-content-understanding";

async function main(): Promise<void> {
    const client = new ContentUnderstandingClient(
        endpoint,
        new AzureKeyCredential(key)
    );

    // Sample invoice
    const invoiceUrl =
        "https://raw.githubusercontent.com/"
        + "Azure-Samples/"
        + "azure-ai-content-understanding-assets/"
        + "main/document/invoice.pdf";

    const poller = client.analyze(
        "prebuilt-invoice",
        [{ url: invoiceUrl }]
    );
    const result = await poller.pollUntilDone();

    if (
        !result.contents
        || result.contents.length === 0
    ) {
        console.log(
            "No content found in the analysis result."
        );
        return;
    }

    const content = result.contents[0];

    // Get the document content
    if (content.kind === "document") {
        const documentContent =
            content as DocumentContent;

        console.log(
            `Document unit: `
            + `${documentContent.unit ?? "unknown"}`
        );
        console.log(
            `Pages: ${documentContent.startPageNumber}`
            + ` to ${documentContent.endPageNumber}`
        );

        if (!documentContent.fields) {
            console.log("No fields found.");
            return;
        }

        // Extract simple string fields
        const customerNameField =
            documentContent.fields["CustomerName"];
        if (customerNameField) {
            console.log(
                `Customer Name: `
                + `${customerNameField.value ?? "(None)"}`
            );
            if (
                customerNameField.confidence !== undefined
            ) {
                console.log(
                    `  Confidence: `
                    + `${customerNameField.confidence
                        .toFixed(2)}`
                );
            }
        }

        // Extract date fields
        const invoiceDateField =
            documentContent.fields["InvoiceDate"];
        if (invoiceDateField) {
            console.log(
                `Invoice Date: `
                + `${invoiceDateField.value ?? "(None)"}`
            );
            if (
                invoiceDateField.confidence !== undefined
            ) {
                console.log(
                    `  Confidence: `
                    + `${invoiceDateField.confidence
                        .toFixed(2)}`
                );
            }
        }

        // Extract object fields (nested structures)
        const totalAmountField =
            documentContent.fields["TotalAmount"];
        if (
            totalAmountField
            && totalAmountField.type === "object"
        ) {
            const objField =
                totalAmountField as ObjectField;
            if (objField.value) {
                const amountField =
                    objField.value["Amount"];
                const currencyField =
                    objField.value["CurrencyCode"];

                const amount =
                    amountField?.value ?? "(None)";
                const currency =
                    currencyField?.value ?? "";

                console.log(
                    `\nTotal: ${currency}${amount}`
                );
            }
        }

        // Extract array fields (line items)
        const lineItemsField =
            documentContent.fields["LineItems"];
        if (
            lineItemsField
            && lineItemsField.type === "array"
        ) {
            const arrField =
                lineItemsField as ArrayField;
            if (
                arrField.value
                && arrField.value.length > 0
            ) {
                console.log(
                    `\nLine Items `
                    + `(${arrField.value.length}):`
                );
                arrField.value.forEach(
                    (item, index) => {
                        if (item.type === "object") {
                            const itemObj =
                                item as ObjectField;
                            if (itemObj.value) {
                                const descField =
                                    itemObj.value[
                                        "Description"
                                    ];
                                const qtyField =
                                    itemObj.value[
                                        "Quantity"
                                    ];

                                const description =
                                    descField?.value
                                    ?? "N/A";
                                const quantity =
                                    qtyField?.value
                                    ?? "N/A";

                                console.log(
                                    `  Item `
                                    + `${index + 1}: `
                                    + `${description}`
                                );
                                console.log(
                                    `    Quantity: `
                                    + `${quantity}`
                                );
                            }
                        }
                    }
                );
            }
        }
    }
}

main().catch((err) => {
    console.error("The sample encountered an error:", err);
});
```

This will produce the following output:
```text
Document unit: inch
Pages: 1 to 1
Customer Name: MICROSOFT CORPORATION
  Confidence: 0.39
Invoice Date: Thu Nov 14 2019 19:00:00 GMT-0500 (Eastern Standard Time)
  Confidence: 0.94

Total: USD110

Line Items (3):
  Item 1: Consulting Services
    Quantity: 2
  Item 2: Document Fee
    Quantity: 3
  Item 3: Printing Fee
    Quantity: 10
```

> [!NOTE]
> This code is based on the [analyzeInvoice.ts](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/typescript/src/analyzeInvoice.ts) sample in the SDK repository.

# [Image](#tab/image)

This example uses the `prebuilt-imageSearch` analyzer to generate a description of the image.

```typescript
async function main(): Promise<void> {
    const client = new ContentUnderstandingClient(
        endpoint,
        new AzureKeyCredential(key)
    );

    const poller = client.analyze("prebuilt-imageSearch", [
        { url: "https://raw.githubusercontent.com/Azure-Samples/azure-ai-content-understanding-assets/main/image/pieChart.jpg" },
    ]);
    const result = await poller.pollUntilDone();

    const content = result.contents![0];
    console.log(content.markdown);
    console.log("Summary:",
        content.fields?.["Summary"]?.value ?? "");
}

main().catch((err) => {
    console.error("The sample encountered an error:", err);
});
```

This will produce an output like the following:
```text
The pie chart displays the distribution of hours spent in four categories: 1-39 hours (6.7%), 40-50 hours (18.9%), 50-60 hours (36.6%), and 60+ hours (37.8%). The largest segment is 60+ hours, followed closely by 50-60 hours, then 40-50 hours, and the smallest segment is 1-39 hours.
```
> [!NOTE]
> This code is based on the [analyzeUrl.ts](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/typescript/src/analyzeUrl.ts) sample in the SDK repository.

# [Audio](#tab/audio)

This example uses the `prebuilt-audioSearch` analyzer to extract the audio transcript, generate a summary, and perform speaker labeling.

```typescript
import {
    type AudioVisualContent,
} from "@azure/ai-content-understanding";

async function main(): Promise<void> {
    const client = new ContentUnderstandingClient(
        endpoint,
        new AzureKeyCredential(key)
    );

    const poller = client.analyze("prebuilt-audioSearch", [
        { url: "https://raw.githubusercontent.com/Azure-Samples/azure-ai-content-understanding-assets/main/audio/callCenterRecording.mp3" },
    ]);
    const result = await poller.pollUntilDone();

    if (result.contents && result.contents.length > 0
        && result.contents[0].kind === "audioVisual") {
        const audioContent =
            result.contents[0] as AudioVisualContent;
        console.log(audioContent.markdown);
        console.log("Summary:",
            audioContent.fields?.["Summary"]?.value ?? "");

        if (audioContent.transcriptPhrases
            && audioContent.transcriptPhrases.length > 0) {
            console.log("Transcript (first two phrases):");
            for (const phrase
                of audioContent.transcriptPhrases.slice(0, 2)) {
                console.log(
                    `  [${phrase.speaker}] `
                    + `${phrase.startTimeMs} ms: `
                    + `${phrase.text}`
                );
            }
        }
    }
}

main().catch((err) => {
    console.error("The sample encountered an error:", err);
});
```

This will produce an output like the following:
```text
# Audio: 00:00.000 => 00:32.183

Transcript

WEBVTT

00:00.080 --> 00:00.640
<v Speaker 1>Good day.

00:00.880 --> 00:02.240
<v Speaker 1>Welcome to Contoso.

00:02.560 --> 00:03.760
<v Speaker 1>My name is John Doe.

00:03.920 --> 00:05.120
<v Speaker 1>How can I help you today?

00:05.440 --> 00:06.320
<v Speaker 2>Yes, good day.

00:06.640 --> 00:08.160
<v Speaker 2>My name is Maria Smith.

00:08.560 --> 00:11.360
<v Speaker 2>I would like to inquire about my current point balance.

00:11.680 --> 00:12.560
<v Speaker 1>No problem.

00:12.880 --> 00:13.920
<v Speaker 1>I am happy to help.

00:14.240 --> 00:16.720
<v Speaker 1>I need your date of birth to confirm your identity.

00:17.120 --> 00:19.600
<v Speaker 2>It is April 19th, 1988.

00:20.000 --> 00:20.480
<v Speaker 1>Great.

00:20.800 --> 00:24.160
<v Speaker 1>Your current point balance is 599 points.

00:24.560 --> 00:26.160
<v Speaker 1>Do you need any more information?

00:26.480 --> 00:27.200
<v Speaker 2>No, thank you.

00:27.600 --> 00:28.320
<v Speaker 2>That was all.

00:28.720 --> 00:29.360
<v Speaker 2>Goodbye.

00:29.680 --> 00:31.920
<v Speaker 1>You're welcome, goodbye a Cantoso.

Summary: The conversation is a customer service interaction where Maria Smith contacts Contoso to inquire about her current point balance. The agent, John Doe, verifies her identity by asking for her date of birth and then informs her that her current point balance is 599 points. Maria confirms she does not need further information and ends the call politely.   
Transcript (first two phrases):
  [Speaker 1] 80 ms: Good day.
  [Speaker 1] 880 ms: Welcome to Contoso.
```
> [!NOTE]
> This code is based on the [analyzeUrl.ts](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/typescript/src/analyzeUrl.ts) sample in the SDK repository.

# [Video](#tab/video)

This example uses the `prebuilt-videoSearch` analyzer to extract keyframes, transcript, and chapter segments from video.

```typescript
import {
    type AudioVisualContent,
} from "@azure/ai-content-understanding";

async function main(): Promise<void> {
    const client = new ContentUnderstandingClient(
        endpoint,
        new AzureKeyCredential(key)
    );

    const poller = client.analyze("prebuilt-videoSearch", [
        { url: "https://raw.githubusercontent.com/Azure-Samples/azure-ai-content-understanding-assets/main/videos/sdk_samples/FlightSimulator.mp4" },
    ]);
    const result = await poller.pollUntilDone();

    if (result.contents) {
        let segmentIndex = 1;
        for (const content of result.contents) {
            if (content.kind === "audioVisual") {
                const videoContent =
                    content as AudioVisualContent;
                console.log(
                    `--- Segment ${segmentIndex} ---`
                );
                console.log("Markdown:");
                console.log(videoContent.markdown);
                console.log("Summary:",
                    videoContent.fields?.["Summary"]?.value
                    ?? "");
                console.log(
                    `Start: ${videoContent.startTimeMs} ms, `
                    + `End: ${videoContent.endTimeMs} ms`
                );
                console.log(
                    `Frame size: ${videoContent.width} `
                    + `x ${videoContent.height}`
                );
                console.log("---------------------");
                segmentIndex++;
            }
        }
    }
}

main().catch((err) => {
    console.error("The sample encountered an error:", err);
});
```

This will produce an output like the following:
```text
--- Segment 1 ---
Markdown:
# Video: 00:00.733 => 00:43.233
Width: 1080
Height: 608

Transcript

WEBVTT

00:01.360 --> 00:06.640
<Speaker 1>When it comes to the neural TTS, in order to get a good voice, it's better to have good data.

00:07.120 --> 00:13.320
<Speaker 2>To achieve that, we build a universal TTS model based on 3,000 hours of data.

00:13.440 --> 00:23.680
<Speaker 1>We actually accumulated tons of the data so that this universal model is able to capture the nuance of the audio and generate a more natural voice for the algorithm.

00:24.040 --> 00:29.120
<Speaker 3>What we liked about cognitive services offerings were that they had a much higher fidelity.

00:29.600 --> 00:32.880
<Speaker 3>And they sounded a lot more like an actual human voice.

00:33.680 --> 00:37.200
<Speaker 4>Orlando ground 9555 requesting the end of pushback.

00:38.680 --> 00:41.280
<Speaker 4>9555 request to end pushback received.


Key Frames
- 00:00.733 ![](keyFrame.733.jpg)
- 00:02.067 ![](keyFrame.2067.jpg)
- 00:02.667 ![](keyFrame.2667.jpg)
- 00:04.067 ![](keyFrame.4067.jpg)
- 00:04.900 ![](keyFrame.4900.jpg)
- 00:05.733 ![](keyFrame.5733.jpg)
- 00:06.567 ![](keyFrame.6567.jpg)
- 00:07.800 ![](keyFrame.7800.jpg)
- 00:09.000 ![](keyFrame.9000.jpg)
- 00:09.800 ![](keyFrame.9800.jpg)
- 00:10.600 ![](keyFrame.10600.jpg)
- 00:12.100 ![](keyFrame.12100.jpg)
- 00:12.833 ![](keyFrame.12833.jpg)
- 00:14.200 ![](keyFrame.14200.jpg)
- 00:14.833 ![](keyFrame.14833.jpg)
- 00:15.467 ![](keyFrame.15467.jpg)
- 00:16.933 ![](keyFrame.16933.jpg)
- 00:17.767 ![](keyFrame.17767.jpg)
- 00:18.600 ![](keyFrame.18600.jpg)
- 00:20.167 ![](keyFrame.20167.jpg)
- 00:20.900 ![](keyFrame.20900.jpg)
- 00:21.633 ![](keyFrame.21633.jpg)
- 00:22.367 ![](keyFrame.22367.jpg)
- 00:23.100 ![](keyFrame.23100.jpg)
- 00:24.833 ![](keyFrame.24833.jpg)
- 00:25.700 ![](keyFrame.25700.jpg)
- 00:26.567 ![](keyFrame.26567.jpg)
- 00:27.433 ![](keyFrame.27433.jpg)
- 00:28.300 ![](keyFrame.28300.jpg)
- 00:29.167 ![](keyFrame.29167.jpg)
- 00:30.833 ![](keyFrame.30833.jpg)
- 00:31.633 ![](keyFrame.31633.jpg)
- 00:32.433 ![](keyFrame.32433.jpg)
- 00:33.900 ![](keyFrame.33900.jpg)
- 00:34.600 ![](keyFrame.34600.jpg)
- 00:36.067 ![](keyFrame.36067.jpg)
- 00:36.867 ![](keyFrame.36867.jpg)
- 00:38.200 ![](keyFrame.38200.jpg)
- 00:38.700 ![](keyFrame.38700.jpg)
- 00:39.900 ![](keyFrame.39900.jpg)
- 00:40.600 ![](keyFrame.40600.jpg)
- 00:41.300 ![](keyFrame.41300.jpg)
- 00:42.633 ![](keyFrame.42633.jpg)
- 00:43.233 ![](keyFrame.43233.jpg)
Summary: The video opens with a scenic aerial view of an island and a small plane flying, accompanied by the Flight Simulator and Microsoft Azure AI logos. It then transitions to a person speaking about the importance of good data for neural text-to-speech (TTS) technology, mentioning the creation of a universal TTS model trained on 3,000 hours of data to capture audio nuances and generate natural voices. Visuals include audio waveform displays and shots of data centers, emphasizing the technology's backend. The speaker praises the high fidelity and human-like quality of cognitive services' voice offerings. The segment concludes with realistic flight simulation visuals showing planes on the runway and ground crew, alongside simulated air traffic control communications.
Start: 733 ms, End: 43233 ms
Frame size: 1080 x 608
```
> [!NOTE]
> This code is based on the [analyzeUrl.ts](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/typescript/src/analyzeUrl.ts) sample in the SDK repository.

## Next steps

* Explore more [TypeScript SDK samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/typescript)
* [Create a custom analyzer](../../tutorial/create-custom-analyzer.md)
* [Prebuilt analyzers](../../concepts/prebuilt-analyzers.md)
* [Language and region support](../../language-region-support.md)
