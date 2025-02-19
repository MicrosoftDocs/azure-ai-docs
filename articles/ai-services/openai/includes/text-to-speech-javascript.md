---
ms.topic: include
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.date: 09/12/2024
ms.reviewer: v-baolianzou
ms.author: eur
author: eric-urban
recommendations: false
---

[Source code](https://github.com/openai/openai-node) | [Package (npm)](https://www.npmjs.com/package/openai) | [Samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai/samples)

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services?azure-portal=true)
- [LTS versions of Node.js](https://github.com/nodejs/release#release-schedule)
- [Azure CLI](/cli/azure/install-azure-cli) used for passwordless authentication in a local development environment, create the necessary context by signing in with the Azure CLI.
- An Azure OpenAI resource created in a supported region (see [Region availability](/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability)). For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).

### Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Retrieve resource information

[!INCLUDE [resource authentication](resource-authentication.md)]

> [!CAUTION]
> To use the recommended keyless authentication with the SDK, make sure that the `AZURE_OPENAI_API_KEY` environment variable isn't set. 

## Create a Node application

In a console window (such as cmd, PowerShell, or Bash), create a new directory for your app, and navigate to it. Then run the `npm init` command to create a node application with a _package.json_ file.

```console
npm init
```

## Install the client library

Install the client libraries with:

```console
npm install openai @azure/identity
```

Your app's _package.json_ file will be updated with the dependencies.

## Create a speech file

    

#### [Microsoft Entra ID](#tab/keyless)

1. Create a new file named _Text-to-speech.js_ and open it in your preferred code editor. Copy the following code into the _Text-to-speech.js_ file:

    ```javascript
    const { writeFile } = require("fs/promises");
    const { AzureOpenAI } = require("openai");
    const { DefaultAzureCredential, getBearerTokenProvider } = require("@azure/identity");
    require("openai/shims/node");
    
    // You will need to set these environment variables or edit the following values
    const endpoint = process.env["AZURE_OPENAI_ENDPOINT"] || "<endpoint>";
    const speechFilePath = "<path to save the speech file>";
    
    // Required Azure OpenAI deployment name and API version
    const deploymentName = "tts";
    const apiVersion = "2024-08-01-preview";
    
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

1. Run the script with the following command:

    ```console
    node Text-to-speech.js
    ```

#### [API key](#tab/api-key)

1. Create a new file named _Text-to-speech.js_ and open it in your preferred code editor. Copy the following code into the _Text-to-speech.js_ file:

    ```javascript
    const { writeFile } = require("fs/promises");
    const { AzureOpenAI } = require("openai");
    require("openai/shims/node");
    
    // You will need to set these environment variables or edit the following values
    const endpoint = process.env["AZURE_OPENAI_ENDPOINT"] || "<endpoint>";
    const apiKey = process.env["AZURE_OPENAI_API_KEY"] || "<api key>";
    const speechFilePath = "<path to save the speech file>";
    
    // Required Azure OpenAI deployment name and API version
    const deploymentName = "tts";
    const apiVersion = "2024-08-01-preview";
    
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
[!INCLUDE [Azure Key Vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

1. Run the script with the following command:

    ```console
    node Text-to-speech.js
    ```
    

---