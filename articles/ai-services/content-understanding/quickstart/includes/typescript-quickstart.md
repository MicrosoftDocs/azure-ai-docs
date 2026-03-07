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

This quickstart shows you how to use the Content Understanding TypeScript SDK to extract structured data using prebuilt analyzers from document, image, audio, and video files. To learn more about prebuilt analyzers and other features, see the documentation of [Prebuilt Analyzers](../concepts/prebuilt-analyzers.md).

## Prerequisites

* An active Azure subscription. If you don't have an Azure account, [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) created in a [supported region](https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/language-region-support).
* Your resource endpoint and API key (found under Keys and Endpoint in the Azure portal).
* Model deployment defaults configured for your resource. See [Models and deployments](../../concepts/models-deployments.md) for setup instructions.
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

1. Create a **tsconfig.json** file with the following content:

    ```json
    {
        "compilerOptions": {
            "target": "ES2020",
            "module": "commonjs",
            "strict": true,
            "esModuleInterop": true,
            "skipLibCheck": true
        }
    }
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

const endpoint = process.env["CONTENTUNDERSTANDING_ENDPOINT"]!;
const key = process.env["CONTENTUNDERSTANDING_KEY"]!;

const client = new ContentUnderstandingClient(
    endpoint,
    new AzureKeyCredential(key)
);
```

## Get started with a prebuilt analyzer

Analyzers define how your content is processed and the insights that are extracted. We offer [prebuilt analyzers](../concepts/prebuilt-analyzers.md) for common use cases. You can [customize prebuilt analyzers](../concepts/prebuilt-analyzers.md) to better fit your specific needs and use cases.
This quickstart uses prebuilt invoice, image, audio, and video analyzers to help you get started.


# [Document](#tab/document)

This example uses the `prebuilt-invoice` analyzer to extract structured data from an invoice document.

```typescript
// TODO: Document (prebuilt-invoice) code snippet
```

This will produce the following output:
```bash
<!-- TODO: Document output -->
```

> [!NOTE]
> This code is based on the [analyzeInvoice.ts](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/typescript/src/analyzeInvoice.ts) sample in the SDK repository.

# [Image](#tab/image)

This example uses the `prebuilt-imageSearch` analyzer to generate a description of the image.

```typescript
// TODO: Image code snippet
```

This will produce the following output:
```bash
<!-- TODO: Image output -->
```

# [Audio](#tab/audio)

This example uses the `prebuilt-audioSearch` analyzer to extract the audio transcript, generate a summary, and perform speaker labeling.

```typescript
// TODO: Audio code snippet
```

This will produce the following output:
```text
<!-- TODO: Audio output -->
```

# [Video](#tab/video)

This example uses the `prebuilt-videoSearch` analyzer to extract keyframes, transcript, and chapter segments from video.

```typescript
// TODO: Video code snippet
```

This will produce the following output:
```text
<!-- TODO: Video output -->
```


## Next steps

* Explore more [TypeScript SDK samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/typescript)
* [Create a custom analyzer](../../tutorial/create-custom-analyzer.md)
* [Prebuilt analyzers](../../concepts/prebuilt-analyzers.md)
* [Language and region support](../../language-region-support.md)
