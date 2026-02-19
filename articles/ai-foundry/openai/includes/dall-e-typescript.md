---
title: 'Quickstart: Use Azure OpenAI in Microsoft Foundry Models with the JavaScript SDK to generate images'
titleSuffix: Azure OpenAI
description: Walkthrough on how to get started with Azure OpenAI and make your first image generation call with the JavaScript SDK. 
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
author: PatrickFarley
ms.author: pafarley
ms.date: 10/23/2024
---

Use this guide to get started generating images with the Azure OpenAI SDK for JavaScript.

[Reference documentation](https://platform.openai.com/docs/api-reference/images/create) | [Source code](https://github.com/openai/openai-node) | [Package (npm)](https://www.npmjs.com/package/openai) | [Samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai/samples)

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)
- [LTS versions of Node.js](https://github.com/nodejs/release#release-schedule)
- [TypeScript](https://www.typescriptlang.org/download/)
- [Azure CLI](/cli/azure/install-azure-cli) used for passwordless authentication in a local development environment, create the necessary context by signing in with the Azure CLI.
- An Azure OpenAI resource created in a supported region (see [Region availability](/azure/ai-foundry/openai/concepts/models#model-summary-table-and-region-availability)). For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).

### Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Set up

1. Create a new folder `image-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir image-quickstart && cd image-quickstart
    ```
    
1. Create the `package.json` with the following command:

    ```shell
    npm init -y
    ```

1. Update the `package.json` to ECMAScript with the following command: 

    ```shell
    npm pkg set type=module
    ```
    

1. Install the OpenAI client library for JavaScript with:

    ```console
    npm install openai
    ```

1. For the **recommended** passwordless authentication:

    ```console
    npm install @azure/identity
    ```

## Retrieve resource information

[!INCLUDE [resource authentication](resource-authentication.md)]

> [!CAUTION]
> To use the recommended keyless authentication with the SDK, make sure that the `AZURE_OPENAI_API_KEY` environment variable isn't set. 

## Generate images with DALL-E

#### [Microsoft Entra ID](#tab/typescript-keyless)

1. Create the `index.ts` file with the following code:

    ```typescript
    import { AzureOpenAI } from "openai";
    import { 
        DefaultAzureCredential, 
        getBearerTokenProvider 
    } from "@azure/identity";
    
    // You will need to set these environment variables or edit the following values
    const endpoint = process.env.AZURE_OPENAI_ENDPOINT || "Your endpoint";
    
    // Required Azure OpenAI deployment name and API version
    const apiVersion = process.env.OPENAI_API_VERSION || "2024-07-01";
    const deploymentName = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || "dall-e-3";
    
    // keyless authentication    
    const credential = new DefaultAzureCredential();
    const scope = "https://cognitiveservices.azure.com/.default";
    const azureADTokenProvider = getBearerTokenProvider(credential, scope);
    
    function getClient(): AzureOpenAI {
      return new AzureOpenAI({
        endpoint,
        azureADTokenProvider,
        apiVersion,
        deployment: deploymentName,
      });
    }
    async function main() {
      console.log("== Image Generation ==");
    
      const client = getClient();
    
      const results = await client.images.generate({
        prompt,
        size: "1024x1024",
        n: numberOfImagesToGenerate,
        model: "",
        style: "vivid", // or "natural"
      });
    
      for (const image of results.data) {
        console.log(`Image generation result URL: ${image.url}`);
      }
    }
    
    main().catch((err) => {
      console.error("The sample encountered an error:", err);
    });
    ```

1. Create the `tsconfig.json` file to transpile the TypeScript code and copy the following code for ECMAScript.

    ```json
    {
        "compilerOptions": {
          "module": "NodeNext",
          "target": "ES2022", // Supports top-level await
          "moduleResolution": "NodeNext",
          "skipLibCheck": true, // Avoid type errors from node_modules
          "strict": true // Enable strict type-checking options
        },
        "include": ["*.ts"]
    }
    ```

1. Transpile from TypeScript to JavaScript.

    ```shell
    tsc
    ```
    
1. Sign in to Azure with the following command:

    ```shell
    az login
    ```

1. Run the code with the following command:

    ```shell
    node index.js
    ```

## [API key](#tab/typescript-key)

1. Create the `index.ts` file with the following code:

    ```typescript
    import { AzureOpenAI } from "openai";
    
    // You will need to set these environment variables or edit the following values
    const endpoint = process.env.AZURE_OPENAI_ENDPOINT || "Your endpoint";
    const apiKey = process.env.AZURE_OPENAI_API_KEY || "Your API key";
    
    // Required Azure OpenAI deployment name and API version
    const apiVersion = process.env.OPENAI_API_VERSION || "2024-07-01";
    const deploymentName = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || "dall-e-3";
    
    // The prompt to generate images from
    const prompt = "a monkey eating a banana";
    const numberOfImagesToGenerate = 1;
    
    function getClient(): AzureOpenAI {
      return new AzureOpenAI({
        endpoint,
        apiKey,
        apiVersion,
        deployment: deploymentName,
      });
    }
    async function main() {
      console.log("== Image Generation ==");
    
      const client = getClient();
    
      const results = await client.images.generate({
        prompt,
        size: "1024x1024",
        n: numberOfImagesToGenerate,
        model: "",
        style: "vivid", // or "natural"
      });
    
      for (const image of results.data) {
        console.log(`Image generation result URL: ${image.url}`);
      }
    }
    
    main().catch((err) => {
      console.error("The sample encountered an error:", err);
    });
    ```


1. Create the `tsconfig.json` file to transpile the TypeScript code and copy the following code for ECMAScript.

    ```json
    {
        "compilerOptions": {
          "module": "NodeNext",
          "target": "ES2022", // Supports top-level await
          "moduleResolution": "NodeNext",
          "skipLibCheck": true, // Avoid type errors from node_modules
          "strict": true // Enable strict type-checking options
        },
        "include": ["*.ts"]
    }
    ```

1. Transpile from TypeScript to JavaScript.

    ```shell
    tsc
    ```
    
1. Run the code with the following command:

    ```shell
    node index.js
    ```

---

## Output

The URL of the generated image is printed to the console.

```console
== Batch Image Generation ==
Image generation result URL: <SAS URL>
Image generation result URL: <SAS URL>
```

> [!NOTE]
> The Image APIs come with a content moderation filter. If the service recognizes your prompt as harmful content, it won't return a generated image. For more information, see the [content filter](../concepts/content-filter.md) article.

## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource. Before deleting the resource, you must first delete any deployed models.

- [Azure portal](../../../ai-services/multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../../ai-services/multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

* Explore the Image APIs in more depth with the [Image API how-to guide](../how-to/dall-e.md).
* For more examples check out the [Azure OpenAI Samples GitHub repository](https://github.com/Azure/azure-openai-samples).
