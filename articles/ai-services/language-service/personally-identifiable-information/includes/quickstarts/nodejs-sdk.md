---
author: laujan
ms.author: lajanuar
manager: nitinme
ms.date: 01/07/2026
ms.service: azure-ai-language
ms.topic: include
ms.custom:
  - devx-track-js
  - ignite-2024
  - build-2025
ai-usage: ai-assisted
---
<!-- markdownlint-disable MD041 -->
[Reference documentation](/javascript/api/overview/azure/ai-text-analytics-readme?view=azure-node-latest&preserve-view=true) | [More samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/textanalytics/ai-text-analytics/samples) | [Package (npm)](https://www.npmjs.com/package/@azure/ai-text-analytics) | [Library source code](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/textanalytics/ai-text-analytics)

Use this quickstart to create a Personally Identifiable Information (PII) detection application with the client library for Node.js. In the following example, you create a JavaScript application that can identify [recognized sensitive information](../../concepts/entity-categories.md) in text.

## Prerequisites

* Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)
* Once you have your Azure subscription, [create a Foundry resource](../../../../../ai-services/multi-service-resource.md?pivots=azportal).
* [Node.js](https://nodejs.org/) v14 `LTS` or later

## Setting up

[!INCLUDE [Create an Azure resource](../../../includes/create-resource.md)]

[!INCLUDE [Get your key and endpoint](../../../includes/get-key-endpoint.md)]

[!INCLUDE [Create environment variables](../../../includes/environment-variables.md)]

### Create a new Node.js application

In a console window (such as cmd, PowerShell, or Bash), create a new directory for your app, and navigate to it.

```console
mkdir myapp

cd myapp
```

Run the `npm init` command to create a node application with a `package.json` file.

```console
npm init
```

### Install the client library

Install the npm package:

```console
npm install @azure/ai-text-analytics
```

## Code example

Open the file and copy the following sample and run the code.

```javascript
"use strict";

const { TextAnalyticsClient, AzureKeyCredential } = require("@azure/ai-text-analytics");

// This example requires environment variables named "LANGUAGE_KEY" and "LANGUAGE_ENDPOINT"
const key = process.env.LANGUAGE_KEY;
const endpoint = process.env.LANGUAGE_ENDPOINT;

if (!key || !endpoint) {
  throw new Error("Missing LANGUAGE_KEY or LANGUAGE_ENDPOINT environment variables.");
}

async function main() {
    console.log(`PII recognition sample`);

  const client = new TextAnalyticsClient(endpoint, new AzureKeyCredential(key));

  const documents = ["My phone number is 555-555-5555"];

    const results = await client.recognizePiiEntities(documents, "en");

    for (const result of results) {
      if (result.error) {
        console.error("Encountered an error:", result.error);
        continue;
      }

      console.log(`Redacted text: "${result.redactedText}"`);
      console.log("PII entities:");
      for (const entity of result.entities) {
        console.log(`\t- "${entity.text}" of type ${entity.category}`);
      }
    }
}

main().catch((err) => {
console.error("The sample encountered an error:", err);
});
```

## Output

```console
PII recognition sample
Redacted text: "My phone number is ************"
PII entities:
        - "555-555-5555" of type PhoneNumber
```
