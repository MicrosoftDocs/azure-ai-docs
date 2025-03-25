---
title: "Quickstart: Analyze image content with JavaScript"
description: In this quickstart, get started using the Azure AI Content Safety JavaScript SDK to analyze image content for objectionable material.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.custom:
ms.topic: include
ms.date: 03/07/2024
ms.author: pafarley
---

[Reference documentation](https://www.npmjs.com/package/@azure-rest/ai-content-safety/v/1.0.0) | [Library source code](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/contentsafety/ai-content-safety-rest) | [Package (npm)](https://www.npmjs.com/package/@azure-rest/ai-content-safety) | [Samples](https://github.com/Azure-Samples/AzureAIContentSafety/tree/main/js/1.0.0) |


## Prerequisites

* An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services/) 
* The current version of [Node.js](https://nodejs.org/)
* Once you have your Azure subscription, <a href="https://aka.ms/acs-create"  title="Create a Content Safety resource"  target="_blank">create a Content Safety resource </a> in the Azure portal to get your key and endpoint. Enter a unique name for your resource, select your subscription, and select a resource group, supported region (see [Region availability](/azure/ai-services/content-safety/overview#region-availability)), and supported pricing tier. Then select **Create**.
  * The resource takes a few minutes to deploy. After it finishes, Select **go to resource**. In the left pane, under **Resource Management**, select **Subscription Key and Endpoint**. The endpoint and either of the keys are used to call APIs.

## Set up application

Create a new Node.js application. In a console window (such as cmd, PowerShell, or Bash), create a new directory for your app, and navigate to it.

```console
mkdir myapp && cd myapp
```

Run the `npm init` command to create a node application with a `package.json` file.

```console
npm init
```

Also create a `/resources` folder at the root of your project, and add a sample image to it.


### Install the client SDK 

Install the `@azure-rest/ai-content-safety` npm package:

```console
npm install @azure-rest/ai-content-safety
```

Also install the `dotenv` module to use environment variables:

```console
npm install dotenv
```

Your app's `package.json` file will be updated with the dependencies.

[!INCLUDE [Create environment variables](../env-vars.md)]

## Analyze image content

Create a new file in your directory, *index.js*. Open it in your preferred editor or IDE and paste in the following code. Replace the `image_path` variable with the path to your sample image.

```JavaScript
const ContentSafetyClient = require("@azure-rest/ai-content-safety").default,
  { isUnexpected } = require("@azure-rest/ai-content-safety");
const { AzureKeyCredential } = require("@azure/core-auth");
const fs = require("fs");
const path = require("path");

// Load the .env file if it exists
require("dotenv").config();

async function main() {
    // get endpoint and key from environment variables
    const endpoint = process.env["CONTENT_SAFETY_ENDPOINT"];
    const key = process.env["CONTENT_SAFETY_KEY"];
    
    const credential = new AzureKeyCredential(key);
    const client = ContentSafetyClient(endpoint, credential);
    
    // replace with your own sample image file path 
    const image_path = path.resolve(__dirname, "./resources/image.jpg");
    
    const imageBuffer = fs.readFileSync(image_path);
    const base64Image = imageBuffer.toString("base64");
    const analyzeImageOption = { image: { content: base64Image } };
    const analyzeImageParameters = { body: analyzeImageOption };
    
    const result = await client.path("/image:analyze").post(analyzeImageParameters);
    
    if (isUnexpected(result)) {
        throw result;
    }
    for (let i = 0; i < result.body.categoriesAnalysis.length; i++) {
    const imageCategoriesAnalysisOutput = result.body.categoriesAnalysis[i];
    console.log(
      imageCategoriesAnalysisOutput.category,
      " severity: ",
      imageCategoriesAnalysisOutput.severity
    );
  }
}

main().catch((err) => {
    console.error("The sample encountered an error:", err);
});
```

Run the application with the `node` command on your quickstart file.

```console
node index.js
```

## Output

```console
Hate severity:  0
SelfHarm severity:  0
Sexual severity:  0
Violence severity:  0
```