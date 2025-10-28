---
title: "Quickstart: Analyze image content with TypeScript"
description: In this quickstart, get started using the Azure AI Content Safety TypeScript SDK to analyze image content for objectionable material.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.custom:
ms.topic: include
ms.date: 07/11/2025
ms.author: pafarley
---

[Reference documentation](https://www.npmjs.com/package/@azure-rest/ai-content-safety/v/1.0.0) | [Library source code](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/contentsafety/ai-content-safety-rest) | [Package (npm)](https://www.npmjs.com/package/@azure-rest/ai-content-safety) | [Samples](https://github.com/Azure-Samples/AzureAIContentSafety/tree/main/js/1.0.0) |


## Prerequisites

* An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) 
* [Node.js LTS](https://nodejs.org/)
* [TypeScript](https://www.typescriptlang.org/)
* [Visual Studio Code](https://code.visualstudio.com/)
* Once you have your Azure subscription, <a href="https://aka.ms/acs-create"  title="Create a Content Safety resource"  target="_blank">create a Content Safety resource </a> in the Azure portal to get your key and endpoint. Enter a unique name for your resource, select your subscription, and select a resource group, supported region (see [Region availability](/azure/ai-services/content-safety/overview#region-availability)), and supported pricing tier. Then select **Create**.
  * The resource takes a few minutes to deploy. After it finishes, Select **go to resource**. In the left pane, under **Resource Management**, select **Subscription Key and Endpoint**. The endpoint and either of the keys are used to call APIs.

## Set up local development environment

1. Create a new directory for your project and navigate to it:

   ```console
   mkdir content-safety-image-analysis
   cd content-safety-image-analysis
   code .
   ```

1. Create a new package for ESM modules in your project directory:

   ```console
   npm init -y
   npm pkg set type=module
   ```

1. Install the required packages:

   ```console
   npm install @azure-rest/ai-content-safety
   ```

1. Install development dependencies:

   ```console
   npm install typescript @types/node --save-dev
   ```

1. Create a `tsconfig.json` file in your project directory:

   ```json
   {
     "compilerOptions": {
       "target": "es2022",
       "module": "esnext",
       "moduleResolution": "bundler",
       "rootDir": "./src",
       "outDir": "./dist/",
       "esModuleInterop": true,
       "forceConsistentCasingInFileNames": true,
       "strict": true,
       "skipLibCheck": true,
       "declaration": true,
       "sourceMap": true,
       "resolveJsonModule": true,
       "moduleDetection": "force",
       "allowSyntheticDefaultImports": true,
       "verbatimModuleSyntax": false
     },
     "include": [
       "src/**/*.ts"
     ],
     "exclude": [
       "node_modules/**/*",
       "**/*.spec.ts"
     ]
   }
   ```

1. Update `package.json` to include a script for building TypeScript files:

   ```json
   "scripts": {
     "build": "tsc",
     "start": "node dist/index.js"
   }
   ```

1. Create a `resources` folder and add a sample image to it.

1. Create a `src` directory for your TypeScript code.

[!INCLUDE [Create environment variables](../env-vars.md)]

## Analyze image content

Create a new file in your `src` directory, `index.ts` and paste in the following code. Replace the string used to create the `imagePath` variable with the path to your sample image.

```typescript
import ContentSafetyClient, {
    isUnexpected,
    AnalyzeImageParameters,
    AnalyzeImage200Response,
    AnalyzeImageDefaultResponse,
    AnalyzeImageOptions,
    ImageCategoriesAnalysisOutput
} from "@azure-rest/ai-content-safety";
import { AzureKeyCredential } from "@azure/core-auth";
import * as fs from "fs";
import * as path from "path";
import { fileURLToPath } from "url";

// Create __dirname equivalent for ESM modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Get endpoint and key from environment variables
const endpoint = process.env.CONTENT_SAFETY_ENDPOINT;
const key = process.env.CONTENT_SAFETY_KEY;

if (!endpoint || !key) {
    throw new Error("Missing required environment variables CONTENT_SAFETY_ENDPOINT or CONTENT_SAFETY_KEY");
}

try {

    const credential = new AzureKeyCredential(key);
    const client = ContentSafetyClient(endpoint, credential);

    const imagePath = path.join(__dirname, '../resources/image.jpg');

    const imageBuffer = fs.readFileSync(imagePath);
    const base64Image = imageBuffer.toString("base64");
    const analyzeImageOption: AnalyzeImageOptions = { image: { content: base64Image } };
    const analyzeImageParameters: AnalyzeImageParameters = { body: analyzeImageOption };

    const result: AnalyzeImage200Response | AnalyzeImageDefaultResponse = await client.path("/image:analyze").post(analyzeImageParameters);

    if (isUnexpected(result)) {
        throw result;
    }

    const categoriesAnalysis = result.body.categoriesAnalysis as ImageCategoriesAnalysisOutput[];

    for (const analysis of categoriesAnalysis) {
        console.log(`${analysis.category} severity: ${analysis.severity}`);
    }
} catch (error) {
    console.error("Error analyzing image:", error);
}
```

## Build and run the sample

1. Compile the TypeScript code:

   ```console
   npm run build
   ```

1. Run the compiled JavaScript:

   ```console
   node dist/index.js
   ```

## Output

```console
Hate severity:  0
SelfHarm severity:  0
Sexual severity:  0
Violence severity:  0
```