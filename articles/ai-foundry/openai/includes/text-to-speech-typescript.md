---
ms.topic: include
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 09/12/2024
ms.author: pafarley
author: PatrickFarley
recommendations: false
---

[Source code](https://github.com/openai/openai-node) | [Package (npm)](https://www.npmjs.com/package/openai) | [Samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai/samples)

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

1. Create a new folder `assistants-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir assistants-quickstart && cd assistants-quickstart
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

## Create a speech file

#### [Microsoft Entra ID](#tab/typescript-keyless)

1. Create the `index.ts` file with the following code:

    ```typescript
    import { writeFile } from "fs/promises";
    import { AzureOpenAI } from "openai";
    import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";
    import type { SpeechCreateParams } from "openai/resources/audio/speech";
    import "openai/shims/node";
    
    // You will need to set these environment variables or edit the following values
    const endpoint = process.env.AZURE_OPENAI_ENDPOINT || "Your endpoint";
    const speechFilePath = "<path to save the speech file>";
    
    // Required Azure OpenAI deployment name and API version
    const deploymentName = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || "tts";
    const apiVersion = process.env.OPENAI_API_VERSION || "2025-04-01-preview";

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
    
    async function generateAudioStream(
      client: AzureOpenAI,
      params: SpeechCreateParams
    ): Promise<NodeJS.ReadableStream> {
      const response = await client.audio.speech.create(params);
      if (response.ok) return response.body;
      throw new Error(`Failed to generate audio stream: ${response.statusText}`);
    }
    export async function main() {
      console.log("== Text to Speech Sample ==");
    
      const client = getClient();
      const streamToRead = await generateAudioStream(client, {
        model: deploymentName,
        voice: "alloy",
        input: "the quick brown chicken jumped over the lazy dogs",
      });
    
      console.log(`Streaming response to ${speechFilePath}`);
      await writeFile(speechFilePath, streamToRead);
      console.log("Finished streaming");
    }
    
    main().catch((err) => {
      console.error("The sample encountered an error:", err);
    });
    
    ```
    
   The import of `"openai/shims/node"` is necessary when running the code in a Node.js environment. It ensures that the output type of the `client.audio.speech.create` method is correctly set to `NodeJS.ReadableStream`.

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

#### [API key](#tab/typescript-key)

1. Create the `index.ts` file with the following code:

    ```typescript
    import { writeFile } from "fs/promises";
    import { AzureOpenAI } from "openai";
    import type { SpeechCreateParams } from "openai/resources/audio/speech";
    import "openai/shims/node";
    
    // You will need to set these environment variables or edit the following values
    const endpoint = "Your endpoint";
    const apiKey = process.env.AZURE_OPENAI_API_KEY || "Your API key";
    const speechFilePath =
      process.env["SPEECH_FILE_PATH"] || "<path to save the speech file>";
    
    // Required Azure OpenAI deployment name and API version
    const deploymentName = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || "tts";
    const apiVersion = process.env.OPENAI_API_VERSION || "2025-04-01-preview";
    
    function getClient(): AzureOpenAI {
      return new AzureOpenAI({
        endpoint,
        apiKey,
        apiVersion,
        deployment: deploymentName,
      });
    }
    
    async function generateAudioStream(
      client: AzureOpenAI,
      params: SpeechCreateParams
    ): Promise<NodeJS.ReadableStream> {
      const response = await client.audio.speech.create(params);
      if (response.ok) return response.body;
      throw new Error(`Failed to generate audio stream: ${response.statusText}`);
    }
    export async function main() {
      console.log("== Text to Speech Sample ==");
    
      const client = getClient();
      const streamToRead = await generateAudioStream(client, {
        model: deploymentName,
        voice: "alloy",
        input: "the quick brown chicken jumped over the lazy dogs",
      });
    
      console.log(`Streaming response to ${speechFilePath}`);
      await writeFile(speechFilePath, streamToRead);
      console.log("Finished streaming");
    }
    
    main().catch((err) => {
      console.error("The sample encountered an error:", err);
    });
    
    ```
    
   The import of `"openai/shims/node"` is necessary when running the code in a Node.js environment. It ensures that the output type of the `client.audio.speech.create` method is correctly set to `NodeJS.ReadableStream`.

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