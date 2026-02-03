---
title: "Quickstart: Analyze text content with TypeScript"
description: In this quickstart, get started using the Azure AI Content Safety TypeScript SDK to analyze text content for objectionable material.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.custom:
ms.topic: include
ms.date: 07/11/2025
ms.author: pafarley
---

[Reference documentation](https://www.npmjs.com/package/@azure-rest/ai-content-safety) | [Library source code](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/contentsafety/ai-content-safety-rest) | [Package (npm)](https://www.npmjs.com/package/@azure-rest/ai-content-safety) | [Samples](https://github.com/Azure-Samples/AzureAIContentSafety/tree/main/js/1.0.0) |


## Prerequisites

* An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) 
* [Node.js LTS](https://nodejs.org/)
* [TypeScript](https://www.typescriptlang.org/)
* [Visual Studio Code](https://code.visualstudio.com/)
* Once you have your Azure subscription, <a href="https://aka.ms/acs-create"  title="Create a Content Safety resource"  target="_blank">create a Content Safety resource </a> in the Azure portal to get your key and endpoint. Enter a unique name for your resource, select your subscription, and select a resource group, supported region (see [Region availability](/azure/ai-services/content-safety/overview#region-availability)), and supported pricing tier. Then select **Create**.
  * The resource takes a few minutes to deploy. After it finishes, Select **go to resource**. In the left pane, under **Resource Management**, select **Subscription Key and Endpoint**. The endpoint and either of the keys are used to call APIs.
* **Cognitive Services User** role or higher on the Content Safety resource

## Set up application

1. Create a new TypeScript application. In a console window (such as cmd, PowerShell, or Bash), create a new directory for your app, and navigate to it.

    ```console
    mkdir content-safety-typescript && cd content-safety-typescript
    code .
    ```
    
1. Initialize a new Node.js project with TypeScript:

    ```console
    npm init -y
    npm pkg set type=module
    ```

1. Install the required packages:

   ```console
   npm install @azure-rest/ai-content-safety @azure/core-auth
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

1. Create a `src` directory for your TypeScript code.

[!INCLUDE [Create environment variables](../env-vars.md)]

## Analyze text content

Create a file in the `src` directory named `index.ts`. Open it in your preferred editor or IDE and paste in the following code. Replace `<your text sample>` with the text content you'd like to analyze.

> [!TIP]
> Text size and granularity
>
> See [Input requirements](../../overview.md#input-requirements) for maximum text length limitations.

```typescript
import ContentSafetyClient, { 
  isUnexpected, 
  AnalyzeTextParameters,
  AnalyzeText200Response,
  AnalyzeTextDefaultResponse,
  AnalyzeTextOptions,
  TextCategoriesAnalysisOutput 
} from "@azure-rest/ai-content-safety";
import { AzureKeyCredential } from "@azure/core-auth";

// Get endpoint and key from environment variables
const endpoint = process.env.CONTENT_SAFETY_ENDPOINT;
const key = process.env.CONTENT_SAFETY_KEY;

if (!endpoint || !key) {
  throw new Error("Missing required environment variables: CONTENT_SAFETY_ENDPOINT or CONTENT_SAFETY_KEY");
}

try {
  // Create client with Azure Key Credential
  const credential = new AzureKeyCredential(key);
  const client = ContentSafetyClient(endpoint, credential);
  
  // Replace with your own sample text string
  const text = "Replace with your text sample";
  const analyzeTextOption: AnalyzeTextOptions = { text };
  const analyzeTextParameters: AnalyzeTextParameters = { body: analyzeTextOption };
  
  // Call the Content Safety API to analyze the text
  const result: AnalyzeText200Response | AnalyzeTextDefaultResponse = await client.path("/text:analyze").post(analyzeTextParameters);
  
  if (isUnexpected(result)) {
    throw result;
  }
  
  // Process and display the analysis results
  console.log("Text analysis results:");
  
  const categoriesAnalysis = result.body.categoriesAnalysis as TextCategoriesAnalysisOutput[];
  
  for (const analysis of categoriesAnalysis) {
    console.log(`${analysis.category} severity: ${analysis.severity}`);
  }
} catch (error: any) {
  console.error("The sample encountered an error:", error.message);
}
```

## Build and run the application

1. Build the TypeScript code:

```console
npm run build
```

1. Run the application:

```console
npm start
```

## Output

The application outputs severity scores for each content category:

```console
Text analysis results:
Hate severity: 0
SelfHarm severity: 0
Sexual severity: 0
Violence severity: 0
```

Severity levels range from 0 (safe) to 6 (high risk).

**References**: [Content Safety REST Client](https://www.npmjs.com/package/@azure-rest/ai-content-safety), [AzureKeyCredential](/javascript/api/@azure/core-auth/azurekeycredential)
