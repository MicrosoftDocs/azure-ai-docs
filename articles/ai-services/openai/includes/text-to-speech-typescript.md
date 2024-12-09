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
- [TypeScript](https://www.typescriptlang.org/download/)
- [Azure CLI](/cli/azure/install-azure-cli) used for passwordless authentication in a local development environment, create the necessary context by signing in with the Azure CLI.
- An Azure OpenAI resource created in a supported region (see [Region availability](/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability)). For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).


## Set up

### Retrieve key and endpoint

To successfully make a call against Azure OpenAI, you need an **endpoint** and a **key**.

|Variable name | Value |
|--------------------------|-------------|
| `AZURE_OPENAI_ENDPOINT`               | This value can be found in the **Keys & Endpoint** section when examining your resource from the Azure portal. Alternatively, you can find the value in the **Azure OpenAI Studio** > **Playground** > **Code View**. An example endpoint is: `https://aoai-docs.openai.azure.com/`.|
| `AZURE_OPENAI_API_KEY` | This value can be found in the **Keys & Endpoint** section when examining your resource from the Azure portal. You can use either `KEY1` or `KEY2`.|

Go to your resource in the Azure portal. The **Endpoint and Keys** can be found in the **Resource Management** section. Copy your endpoint and access key as you need both for authenticating your API calls. You can use either `KEY1` or `KEY2`. Always having two keys allows you to securely rotate and regenerate keys without causing a service disruption.

:::image type="content" source="../media/quickstarts/endpoint.png" alt-text="Screenshot of the overview UI for an Azure OpenAI resource in the Azure portal with the endpoint & access keys location highlighted." lightbox="../media/quickstarts/endpoint.png":::

### Environment variables

Create and assign persistent environment variables for your key and endpoint.

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

# [Command Line](#tab/command-line)

```CMD
setx AZURE_OPENAI_API_KEY "REPLACE_WITH_YOUR_KEY_VALUE_HERE" 
```

```CMD
setx AZURE_OPENAI_ENDPOINT "REPLACE_WITH_YOUR_ENDPOINT_HERE" 
```

# [PowerShell](#tab/powershell)

```powershell
[System.Environment]::SetEnvironmentVariable('AZURE_OPENAI_API_KEY', 'REPLACE_WITH_YOUR_KEY_VALUE_HERE', 'User')
```

```powershell
[System.Environment]::SetEnvironmentVariable('AZURE_OPENAI_ENDPOINT', 'REPLACE_WITH_YOUR_ENDPOINT_HERE', 'User')
```

# [Bash](#tab/bash)

```Bash
echo export AZURE_OPENAI_API_KEY="REPLACE_WITH_YOUR_KEY_VALUE_HERE" >> /etc/environment && source /etc/environment
```

```Bash
echo export AZURE_OPENAI_ENDPOINT="REPLACE_WITH_YOUR_ENDPOINT_HERE" >> /etc/environment && source /etc/environment
```
---

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

    

#### [Microsoft Entra ID](#tab/typescript-keyless)

1. Create a new file named _Text-to-speech.ts_ and open it in your preferred code editor. Copy the following code into the _Text-to-speech.ts_ file:

    ```typescript
    import { writeFile } from "fs/promises";
    import { AzureOpenAI } from "openai";
    import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";
    import type { SpeechCreateParams } from "openai/resources/audio/speech";
    import "openai/shims/node";
    
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

1. Build the application with the following command:

    ```console
    tsc
    ```

1. Run the application with the following command:

    ```console
    node Text-to-speech.js
    ```


#### [API key](#tab/typescript-key)

1. Create a new file named _Text-to-speech.ts_ and open it in your preferred code editor. Copy the following code into the _Text-to-speech.ts_ file:

    ```typescript
    import { writeFile } from "fs/promises";
    import { AzureOpenAI } from "openai";
    import type { SpeechCreateParams } from "openai/resources/audio/speech";
    import "openai/shims/node";
    
    // You will need to set these environment variables or edit the following values
    const endpoint = "<endpoint>";
    const apiKey = process.env["AZURE_OPENAI_API_KEY"] || "<api key>";
    const speechFilePath =
      process.env["SPEECH_FILE_PATH"] || "<path to save the speech file>";
    
    // Required Azure OpenAI deployment name and API version
    const deploymentName = "tts";
    const apiVersion = "2024-08-01-preview";
    
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

1. Build the application with the following command:

    ```console
    tsc
    ```

1. Run the application with the following command:

    ```console
    node Text-to-speech.js
    ```

---