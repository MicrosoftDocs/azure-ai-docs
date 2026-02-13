---
title: "Quickstart: Use a blocklist with TypeScript"
description: In this quickstart, get started using the Azure AI Content Safety TypeScript SDK to create and use a text blocklist.
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
* [TypeScript](https://www.typescriptlang.org/)
* [Visual Studio Code](https://code.visualstudio.com/)
* Once you have your Azure subscription, <a href="https://aka.ms/acs-create"  title="Create a Content Safety resource"  target="_blank">create a Content Safety resource </a> in the Azure portal to get your key and endpoint. Enter a unique name for your resource, select your subscription, and select a resource group, supported region (see [Region availability](/azure/ai-services/content-safety/overview#region-availability)), and supported pricing tier. Then select **Create**.
  * The resource takes a few minutes to deploy. After it finishes, Select **go to resource**. In the left pane, under **Resource Management**, select **Subscription Key and Endpoint**. The endpoint and either of the keys are used to call APIs.

## Set up local development environment

1. Create a new directory for your project and navigate to it:

   ```console
   mkdir content-safety-blocklist-analysis
   cd content-safety-blocklist-analysis
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

1. Create a `src` directory for your TypeScript code.

[!INCLUDE [Create environment variables](../env-vars.md)]

## Create and use a blocklist

Create a new file in your `src` directory, `index.ts` and paste in the following code.

> [!NOTE]
> After you edit a blocklist, it can take a few minutes before text analysis reflects the changes. If you don't see matches right away, retry the analyze call after a short delay.

```typescript
import ContentSafetyClient, { 
  isUnexpected,
  CreateOrUpdateTextBlocklistParameters,
  CreateOrUpdateTextBlocklist200Response,
  CreateOrUpdateTextBlocklist201Response,
  CreateOrUpdateTextBlocklistDefaultResponse,
  AddOrUpdateBlocklistItemsParameters,
  AddOrUpdateBlocklistItems200Response,
  AddOrUpdateBlocklistItemsDefaultResponse,
  AnalyzeTextParameters,
  AnalyzeText200Response,
  AnalyzeTextDefaultResponse,
  AnalyzeTextOptions,
  TextBlocklist,
  TextBlocklistItem
} from "@azure-rest/ai-content-safety";
import { AzureKeyCredential } from "@azure/core-auth";

// Get endpoint and key from environment variables
const key = process.env.CONTENT_SAFETY_KEY;
const endpoint = process.env.CONTENT_SAFETY_ENDPOINT;

if (!key || !endpoint) {
  throw new Error("Missing required environment variables: CONTENT_SAFETY_KEY or CONTENT_SAFETY_ENDPOINT");
}

// Define your blocklist information
// This creates a custom blocklist for words/phrases you want to specifically block
const blocklistName = "company-prohibited-terms";
const blocklistDescription = "Custom blocklist for company-specific prohibited terms and phrases";

// Define items to block - these are specific words or phrases you want to flag
// Even if Azure AI doesn't naturally flag them, these will be caught
const blocklistItemText1 = "confidential project alpha";
const blocklistItemText2 = "internal revenue data";

// Define sample text for analysis that contains one of our blocked terms
const inputText = "Please don't share the confidential project alpha details with external teams.";

/**
 * Step 1: Create or update a custom blocklist container
 */
async function createBlocklistContainer(
  client: ReturnType<typeof ContentSafetyClient>,
  name: string,
  description: string
): Promise<void> {

  const blocklistData: TextBlocklist = {
    blocklistName: name,
    description: description
  };
  
  const createBlocklistParams: CreateOrUpdateTextBlocklistParameters = {
    body: blocklistData,
    contentType: "application/merge-patch+json"
  };
  
  const blocklistResult: CreateOrUpdateTextBlocklist200Response | CreateOrUpdateTextBlocklist201Response | CreateOrUpdateTextBlocklistDefaultResponse = 
    await client.path("/text/blocklists/{blocklistName}", name).patch(createBlocklistParams);
  
  if (isUnexpected(blocklistResult)) {
    throw blocklistResult;
  }
  
  console.log("✅ Blocklist created successfully!");
  console.log(`   Name: ${blocklistResult.body.blocklistName}`);
  console.log(`   Description: ${blocklistResult.body.description || "No description"}\n`);
}

/**
 * Step 2: Add specific prohibited terms to the blocklist
 */
async function addProhibitedTerms(
  client: ReturnType<typeof ContentSafetyClient>,
  blocklistName: string,
  terms: string[]
): Promise<void> {
  
  const blocklistItems: TextBlocklistItem[] = terms.map(text => ({ text }));
  
  const addItemsParams: AddOrUpdateBlocklistItemsParameters = {
    body: { blocklistItems: blocklistItems }
  };
  
  const addItemsResult: AddOrUpdateBlocklistItems200Response | AddOrUpdateBlocklistItemsDefaultResponse = 
    await client.path("/text/blocklists/{blocklistName}:addOrUpdateBlocklistItems", blocklistName).post(addItemsParams);
  
  if (isUnexpected(addItemsResult)) {
    throw addItemsResult;
  }
  
  console.log("✅ Terms added to blocklist successfully!");
  for (const item of addItemsResult.body.blocklistItems) {
    console.log(`   BlocklistItemId: ${item.blocklistItemId}`);
    console.log(`   Text: "${item.text}"`);
    console.log(`   Description: ${item.description || "No description"}\n`);
  }
}

/**
 * Step 3: Wait for blocklist changes to propagate through Azure's system
 */
async function waitForBlocklistActivation(seconds: number = 5): Promise<void> {
  await new Promise(resolve => setTimeout(resolve, seconds * 1000));
}

/**
 * Step 4: Analyze text against the custom blocklist
 */
async function analyzeTextAgainstBlocklist(
  client: ReturnType<typeof ContentSafetyClient>,
  textToAnalyze: string,
  blocklistName: string
): Promise<AnalyzeText200Response | AnalyzeTextDefaultResponse> {
  
  const analyzeTextOption: AnalyzeTextOptions = {
    text: textToAnalyze,
    blocklistNames: [blocklistName], // Use our custom blocklist
    haltOnBlocklistHit: false // Continue analysis even if blocklist match found
  };
  
  const analyzeTextParams: AnalyzeTextParameters = { body: analyzeTextOption };
  
  const analysisResult: AnalyzeText200Response | AnalyzeTextDefaultResponse = 
    await client.path("/text:analyze").post(analyzeTextParams);
  
  if (isUnexpected(analysisResult)) {
    throw analysisResult;
  }
  
  return analysisResult;
}

/**
 * Step 5: Display analysis results and explain what they mean
 */
function displayAnalysisResults(analysisResult: AnalyzeText200Response): void {
  
  if (analysisResult.body.blocklistsMatch && analysisResult.body.blocklistsMatch.length > 0) {
    console.log("🚨 BLOCKED CONTENT DETECTED!");
    console.log("The following prohibited terms were found:\n");
    
    for (const match of analysisResult.body.blocklistsMatch) {
      console.log(`   Blocklist: ${match.blocklistName}`);
      console.log(`   Matched Term: "${match.blocklistItemText}"`);
      console.log(`   Item ID: ${match.blocklistItemId}\n`);
    }
    
  } else {
    console.log("✅ No blocked content found.");
    console.log("The text does not contain any terms from your custom blocklist.");
  }
}

try {
  const credential = new AzureKeyCredential(key);
  const client = ContentSafetyClient(endpoint, credential);
   
  // Execute the five main steps
  await createBlocklistContainer(client, blocklistName, blocklistDescription);
  await addProhibitedTerms(client, blocklistName, [blocklistItemText1, blocklistItemText2]);
  
  console.log("⏳ Waiting for blocklist changes to take effect...");
  await waitForBlocklistActivation();
  
  const analysisResult = await analyzeTextAgainstBlocklist(client, inputText, blocklistName);
  
  displayAnalysisResults(analysisResult as AnalyzeText200Response);

} catch (error: any) {
  console.error("❌ An error occurred:", error.message);
  if (error.code) {
    console.error(`Error code: ${error.code}`);
  }
  if (error.details) {
    console.error("Error details:", error.details);
  }
}
```

This code:

- Creates a custom blocklist.
- Adds prohibited terms to it.
- Analyzes text against the blocklist.


The TypeScript implementation provides strong typing for better development experience and error checking.

## Build and run the sample

1. Compile the TypeScript code:

   ```console
   npm run build
   ```

1. Run the compiled JavaScript:

   ```console
   npm start
   ```

## Output

When you run the application, you should see output similar to this:

```console
✅ Blocklist created successfully!
   Name: company-prohibited-terms
   Description: Custom blocklist for company-specific prohibited terms and phrases

✅ Terms added to blocklist successfully!
   BlocklistItemId: 6fe21688-f65d-4d0b-9ff5-c6e5859ea83a
   Text: "internal revenue data"
   Description: No description

   BlocklistItemId: b48f958b-a58b-4d49-9e33-8ece75fc6c3b
   Text: "confidential project alpha"
   Description: No description

🚨 BLOCKED CONTENT DETECTED!
The following prohibited terms were found:

   Blocklist: company-prohibited-terms
   Matched Term: "confidential project alpha"
   Item ID: b48f958b-a58b-4d49-9e33-8ece75fc6c3b
```
