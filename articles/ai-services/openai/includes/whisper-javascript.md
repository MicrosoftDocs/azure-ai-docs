---
ms.topic: include
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.date: 10/22/2024
ms.reviewer: v-baolianzou
ms.author: eur
author: eric-urban
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

---
Your app's _package.json_ file will be updated with the dependencies.

## Create a sample application

#### [Microsoft Entra ID](#tab/keyless)

1. Create a new file named _Whisper.js_ and open it in your preferred code editor. Copy the following code into the _Whisper.js_ file:

    ```javascript
    const { createReadStream } = require("fs");
    const { AzureOpenAI } = require("openai");
    const { DefaultAzureCredential, getBearerTokenProvider } = require("@azure/identity");
    
    // You will need to set these environment variables or edit the following values
    const audioFilePath = "<audio file path>";
    const endpoint = process.env.AZURE_OPENAI_ENDPOINT || "Your endpoint";
    
    // Required Azure OpenAI deployment name and API version
    const apiVersion = process.env.OPENAI_API_VERSION || "2024-08-01-preview";
    const deploymentName = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || "whisper";
    
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
    
    export async function main() {
      console.log("== Transcribe Audio Sample ==");
    
      const client = getClient();
      const result = await client.audio.transcriptions.create({
        model: "",
        file: createReadStream(audioFilePath),
      });
    
      console.log(`Transcription: ${result.text}`);
    }
    
    main().catch((err) => {
      console.error("The sample encountered an error:", err);
    });
    ```

1. Run the script with the following command:

    ```console
    node Whisper.js
    ```



#### [API key](#tab/typescript-key)

1. Create a new file named _Whisper.js_ and open it in your preferred code editor. Copy the following code into the _Whisper.js_ file:
    
    ```javascript
    import { createReadStream } from "fs";
    import { AzureOpenAI } from "openai";
    
    // You will need to set these environment variables or edit the following values
    const audioFilePath = "<audio file path>";
    const endpoint = process.env.AZURE_OPENAI_ENDPOINT || "Your endpoint";
    const apiKey = process.env.AZURE_OPENAI_API_KEY || "Your API key";
    
    // Required Azure OpenAI deployment name and API version
    const apiVersion = "2024-08-01-preview";
    const deploymentName = "whisper";
    
    function getClient(): AzureOpenAI {
      return new AzureOpenAI({
        endpoint,
        apiKey,
        apiVersion,
        deployment: deploymentName,
      });
    }
    
    export async function main() {
      console.log("== Transcribe Audio Sample ==");
    
      const client = getClient();
      const result = await client.audio.transcriptions.create({
        model: "",
        file: createReadStream(audioFilePath),
      });
    
      console.log(`Transcription: ${result.text}`);
    }
    
    main().catch((err) => {
      console.error("The sample encountered an error:", err);
    });
    ```

1. Build the application with the following command:

    ```console
    tsc
    ```

1. Run the application with the following command:

    ```console
    node Whisper.js
    ```

---

You can get sample audio files, such as *wikipediaOcelot.wav*, from the [Azure AI Speech SDK repository at GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/sampledata/audiofiles).

[!INCLUDE [Azure Key Vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

## Output

```json
{"text":"The ocelot, Lepardus paradalis, is a small wild cat native to the southwestern United States, Mexico, and Central and South America. This medium-sized cat is characterized by solid black spots and streaks on its coat, round ears, and white neck and undersides. It weighs between 8 and 15.5 kilograms, 18 and 34 pounds, and reaches 40 to 50 centimeters 16 to 20 inches at the shoulders. It was first described by Carl Linnaeus in 1758. Two subspecies are recognized, L. p. paradalis and L. p. mitis. Typically active during twilight and at night, the ocelot tends to be solitary and territorial. It is efficient at climbing, leaping, and swimming. It preys on small terrestrial mammals such as armadillo, opossum, and lagomorphs."}
```
