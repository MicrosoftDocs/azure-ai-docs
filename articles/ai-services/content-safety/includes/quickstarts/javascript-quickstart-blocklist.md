---
title: "Quickstart: Use a blocklist with JavaScript"
description: In this quickstart, get started using the Azure AI Content Safety JavaScript SDK to create and use a text blocklist.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.custom:
ms.topic: include
ms.date: 07/16/2025
ms.author: pafarley
ai-usage: ai-assisted
---

[Reference documentation](https://learn.microsoft.com/javascript/api/@azure-rest/ai-content-safety?view=azure-node-latest) | [Library source code](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/contentsafety/ai-content-safety-rest) | [Package (npm)](https://www.npmjs.com/package/@azure-rest/ai-content-safety) | [Samples](https://github.com/Azure-Samples/AzureAIContentSafety/tree/main/js/1.0.0) |

## Prerequisites

* An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) 
* [Node.js LTS](https://nodejs.org/)
* [Visual Studio Code](https://code.visualstudio.com/)
* Once you have your Azure subscription, <a href="https://aka.ms/acs-create"  title="Create a Content Safety resource"  target="_blank">create a Content Safety resource </a> in the Azure portal to get your key and endpoint. Enter a unique name for your resource, select your subscription, and select a resource group, supported region (see [Region availability](/azure/ai-services/content-safety/overview#region-availability)), and supported pricing tier. Then select **Create**.
  * The resource takes a few minutes to deploy. After it finishes, select **Go to resource**. In the left pane, under **Resource Management**, select **Subscription Key and Endpoint**. The endpoint and either of the keys are used to call APIs.

## Set up application

Create a new Node.js application. In a console window (such as cmd, PowerShell, or Bash), create a new directory for your app, and navigate to it.

```console
mkdir myapp && cd myapp
```

Run the `npm init` command to create a node application with a `package.json` file.

```console
npm init
```

### Install the client SDK 

Install the required npm packages:

```console
npm install @azure-rest/ai-content-safety
```

Also install the `dotenv` module to use environment variables:

```console
npm install dotenv
```

Your app's `package.json` file will be updated with the dependencies.

[!INCLUDE [Create environment variables](../env-vars.md)]

## Create and use a blocklist

Create a new file in your directory, *index.js*. Open it in your preferred editor or IDE and paste in the following code. This code creates a new blocklist, adds items to it, and then analyzes a text string against the blocklist.

> [!NOTE]
> After you edit a blocklist, it can take a few minutes before text analysis reflects the changes. If you don't see matches right away, retry the analyze call after a short delay.

```javascript
const ContentSafetyClient = require("@azure-rest/ai-content-safety").default;
const { AzureKeyCredential } = require("@azure/core-auth");
require("dotenv").config();


async function useBlocklist() {
    const endpoint = process.env["CONTENT_SAFETY_ENDPOINT"];
    const key = process.env["CONTENT_SAFETY_KEY"];
    const credential = new AzureKeyCredential(key);
    const client = ContentSafetyClient(endpoint, credential);

    const blocklistName = "ProductSaleBlocklist-Node";
    const blocklistDescription = "Contains terms related to the sale of a product.";

    // Create or update blocklist
    const createBlocklistResponse = await client
        .path("/text/blocklists/{blocklistName}", blocklistName)
        .patch({
            body: { description: blocklistDescription },
            contentType: "application/merge-patch+json"
        });
    
    // Wait for the blocklist to be available
    await new Promise(resolve => setTimeout(resolve, 5000)); // 5 seconds

    if (createBlocklistResponse.status === '201' || createBlocklistResponse.status === '200') {
        console.log(`Blocklist ${blocklistName} created or updated.`);
        console.log(`Blocklist name: ${createBlocklistResponse.body.blocklistName}`);
    } else {
        console.error("Failed to create or update blocklist. ", createBlocklistResponse);
        return;
    }

    // Add blocklist items
    const blocklistItems = [
        { text: "price" },
        { text: "offer" }
    ];

    const addItemsResponse = await client
        .path("/text/blocklists/{blocklistName}:addOrUpdateBlocklistItems", blocklistName)
        .post({ body: { blocklistItems }, contentType: "application/json" });

    // Wait for the add operation
    await new Promise(resolve => setTimeout(resolve, 5000)); // 5 seconds

    if (addItemsResponse.status === '200') {
        console.log("Blocklist items added:");
        for (const item of addItemsResponse.body.blocklistItems) {
            console.log(`BlocklistItemId: ${item.blocklistItemId}, Text: ${item.text}, Description: ${item.description}`);
        }
    } else {
        console.error("Failed to add blocklist items. ", addItemsResponse);
    }


    // Analyze text
    const analyzeTextOption = {
        text: "You can order a copy now for the low price of $19.99.",
        blocklistNames: [blocklistName],
        haltOnBlocklistHit: true
    };

    const analyzeResponse = await client
        .path("/text:analyze")
        .post({ body: analyzeTextOption, contentType: "application/json" });

    if (analyzeResponse.body.blocklistsMatch) {
        console.log("Blocklist match result:");
        for (const match of analyzeResponse.body.blocklistsMatch) {
            console.log(`BlocklistName: ${match.blocklistName}, BlocklistItemId: ${match.blocklistItemId}, BlocklistText: ${match.blocklistItemText}`);
        }
    }
}

useBlocklist().catch((err) => {
    console.error("The sample encountered an error:", err);
});
```

Optionally replace the blocklist name and items with your own.

## Run the application

Run the application with the `node` command on your quickstart file.

```console
node index.js
```

