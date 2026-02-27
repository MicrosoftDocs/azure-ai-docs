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
- [Azure CLI](/cli/azure/install-azure-cli) used for passwordless authentication in a local development environment, create the necessary context by signing in with the Azure CLI.
- An Azure OpenAI resource created in a supported region (see [Region availability](/azure/ai-foundry/openai/concepts/models#model-summary-table-and-region-availability)). For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).

### Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Set up
 
1. Create a new folder `synthesis-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir synthesis-quickstart && cd synthesis-quickstart
    ```
    
1. Create the `package.json` with the following command:

    ```shell
    npm init -y
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

#### [Microsoft Entra ID](#tab/keyless)

1. Create the `index.js` file with the following code:

    ```javascript
    const { writeFile } = require("fs/promises");
    const { AzureOpenAI } = require("openai");
    const { DefaultAzureCredential, getBearerTokenProvider } = require("@azure/identity");
    require("openai/shims/node");
    
    // You will need to set these environment variables or edit the following values
    const endpoint = process.env.AZURE_OPENAI_ENDPOINT || "Your endpoint";
    const speechFilePath = "<path to save the speech file>";
    
    // Required Azure OpenAI deployment name and API version
    const deploymentName = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || "tts";
    const apiVersion = process.env.OPENAI_API_VERSION || "2024-08-01-preview";
    
    // keyless authentication    
    const credential = new DefaultAzureCredential();
    const scope = "https://cognitiveservices.azure.com/.default";
    const azureADTokenProvider = getBearerTokenProvider(credential, scope);

    function getClient() {
      return new AzureOpenAI({
        endpoint,
        azureADTokenProvider,
        apiVersion,
        deployment: deploymentName,
      });
    }
    
    async function generateAudioStream(
      client,
      params
    ) {
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

1. Sign in to Azure with the following command:

    ```shell
    az login
    ```

1. Run the JavaScript file.

    ```shell
    node index.js
    ```

## [API key](#tab/api-key)

1. Create the `index.js` file with the following code: 

    ```javascript
    const { writeFile } = require("fs/promises");
    const { AzureOpenAI } = require("openai");
    require("openai/shims/node");
    
    // You will need to set these environment variables or edit the following values
    const endpoint = process.env.AZURE_OPENAI_ENDPOINT || "Your endpoint";
    const apiKey = process.env.AZURE_OPENAI_API_KEY || "Your API key";
    const speechFilePath = "<path to save the speech file>";
    
    // Required Azure OpenAI deployment name and API version
    const deploymentName = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || "tts";
    const apiVersion = process.env.OPENAI_API_VERSION || "2024-08-01-preview";
    
    function getClient() {
      return new AzureOpenAI({
        endpoint,
        apiKey,
        apiVersion,
        deployment: deploymentName,
      });
    }
    
    async function generateAudioStream(
      client,
      params
    ) {
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

1. Run the JavaScript file.

    ```shell
    node index.js
    ```
    
---