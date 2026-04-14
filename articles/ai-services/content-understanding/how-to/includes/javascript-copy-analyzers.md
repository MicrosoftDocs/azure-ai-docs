---
title: "How-to: Copy custom analyzers using the Content Understanding JavaScript SDK"
author: PatrickFarley
manager: nitinme
description: Learn to copy custom analyzers with Content Understanding using the JavaScript SDK.
ms.service: azure-ai-content-understanding
ms.topic: include
ms.date: 04/14/2026
ms.author: lahlouchu
ai-usage: ai-assisted
---

<!-- markdownlint-disable MD025 -->

This guide shows you how to use the Content Understanding JavaScript SDK to copy custom analyzers within a resource and across Foundry resources.

## Prerequisites

* An active Azure subscription. If you don't have an Azure account, [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) created in a [supported region](../../language-region-support.md).
* Your resource endpoint and API key.
* [Node.js](https://nodejs.org/) LTS version.
* An existing custom analyzer in your resource. See [Create a custom analyzer](../../tutorial/create-custom-analyzer.md) if you need to create one.

## Set up

1. Create a new Node.js project:

    ```console
    mkdir copy-analyzer-example
    cd copy-analyzer-example
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
- `CONTENTUNDERSTANDING_ENDPOINT` - the endpoint to your Content Understanding resource.
- `CONTENTUNDERSTANDING_KEY` - your Content Understanding API key (optional if using [Microsoft Entra ID](../../concepts/secure-communications.md) DefaultAzureCredential).

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

## Copy within a Foundry resource

To copy an analyzer within the same resource, call the `copyAnalyzer` method with the target and source analyzer IDs.

```javascript
const sourceAnalyzerId = "my-source-analyzer";
const targetAnalyzerId = "my-target-analyzer";

const copyPoller = client.copyAnalyzer(
    targetAnalyzerId, sourceAnalyzerId
);
await copyPoller.pollUntilDone();

console.log("Analyzer copied successfully!");
```

> [!TIP]
> This code is based on the [copy analyzer sample](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/javascript/copyAnalyzer.js) in the SDK repository.

## Copy across Foundry resources

Copying an analyzer across Foundry resources is a multi-step process:

1. Grant copy authorization on the source resource.
1. Use the authorization to call the copy API on the target resource.

> [!IMPORTANT]
> Both the source and target resources require the **Cognitive Services User** role to be granted to the credential used to run the code. This role is required for cross-resource copying operations.

For cross-resource copying, set the following additional environment variables:
- `CONTENTUNDERSTANDING_SOURCE_RESOURCE_ID` - Full Azure Resource Manager resource ID of the source resource.
- `CONTENTUNDERSTANDING_SOURCE_REGION` - Azure region of the source resource.
- `CONTENTUNDERSTANDING_TARGET_ENDPOINT` - Target resource endpoint.
- `CONTENTUNDERSTANDING_TARGET_RESOURCE_ID` - Full Azure Resource Manager resource ID of the target resource.
- `CONTENTUNDERSTANDING_TARGET_REGION` - Azure region of the target resource.
- `CONTENTUNDERSTANDING_TARGET_KEY` - Target API key (optional if using DefaultAzureCredential).

Example resource ID format:
`/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{name}`

```javascript
const sourceEndpoint =
    process.env["CONTENTUNDERSTANDING_ENDPOINT"];
const sourceKey =
    process.env["CONTENTUNDERSTANDING_KEY"];

const sourceResourceId =
    process.env[
        "CONTENTUNDERSTANDING_SOURCE_RESOURCE_ID"
    ];
const sourceRegion =
    process.env["CONTENTUNDERSTANDING_SOURCE_REGION"];

const targetEndpoint =
    process.env[
        "CONTENTUNDERSTANDING_TARGET_ENDPOINT"
    ];
const targetKey =
    process.env["CONTENTUNDERSTANDING_TARGET_KEY"];

const targetResourceId =
    process.env[
        "CONTENTUNDERSTANDING_TARGET_RESOURCE_ID"
    ];
const targetRegion =
    process.env[
        "CONTENTUNDERSTANDING_TARGET_REGION"
    ];

const sourceAnalyzerId = "my-source-analyzer";
const targetAnalyzerId = "my-target-analyzer";

// Create clients for source and target resources
const sourceClient = new ContentUnderstandingClient(
    sourceEndpoint,
    new AzureKeyCredential(sourceKey)
);
const targetClient = new ContentUnderstandingClient(
    targetEndpoint,
    new AzureKeyCredential(targetKey)
);

// Step 1: Grant copy authorization on the source
const copyAuth =
    await sourceClient.grantCopyAuthorization(
        sourceAnalyzerId,
        targetResourceId,
        { targetRegion: targetRegion }
    );

console.log("Copy authorization granted!");
console.log(
    `  Target resource: `
    + `${copyAuth.targetAzureResourceId}`
);
console.log(
    `  Expires at: ${copyAuth.expiresAt}`
);

// Step 2: Copy the analyzer from source to target
const copyPoller = targetClient.copyAnalyzer(
    targetAnalyzerId,
    sourceAnalyzerId,
    {
        sourceAzureResourceId: sourceResourceId,
        sourceRegion: sourceRegion,
    }
);
await copyPoller.pollUntilDone();

console.log("Analyzer copied successfully!");

// Verify the copy
const targetInfo = await targetClient.getAnalyzer(
    targetAnalyzerId
);
console.log(
    `Target analyzer '${targetAnalyzerId}':`
);
console.log(
    `  Description: ${targetInfo.description}`
);
console.log(
    `  Status: ${targetInfo.status}`
);
```

> [!TIP]
> This code is based on the [grant copy auth sample](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/javascript/grantCopyAuth.js) in the SDK repository.

> [!NOTE]
>
> Analyzers now support classification/segmentation and analysis of each of the identified classes and segments in a single request. When copying an analyzer that uses this feature, you need to copy any referenced analyzers as well.

## Verify the copy

Validate that the analyzer was copied by retrieving it from the target resource.

```javascript
const analyzer = await client.getAnalyzer(
    targetAnalyzerId
);
console.log(
    `Analyzer '${targetAnalyzerId}' found.`
);
if (analyzer.description) {
    console.log(
        `  Description: ${analyzer.description}`
    );
}
```
