---
manager: nitinme
author: eric-urban
ms.author: eur
ms.service: azure-ai-openai
ms.topic: include
ms.date: 1/21/2025
---

## Prerequisites

- An Azure subscription - <a href="https://azure.microsoft.com/free/cognitive-services" target="_blank">Create one for free</a>
- <a href="https://nodejs.org/" target="_blank">Node.js LTS or ESM support.</a>
- [TypeScript](https://www.typescriptlang.org/download/) installed globally.
- An Azure OpenAI resource created in one of the supported regions. For more information about region availability, see the [models and versions documentation](../concepts/models.md#global-standard-model-availability).
- Then, you need to deploy a `gpt-4o-mini-realtime-preview` model with your Azure OpenAI resource. For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md). 

### Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Deploy a model for real-time audio

[!INCLUDE [Deploy model](realtime-deploy-model.md)]

## Set up

1. Create a new folder `realtime-audio-quickstart` to contain the application and open Visual Studio Code in that folder with the following command:

    ```shell
    mkdir realtime-audio-quickstart && cd realtime-audio-quickstart
    ```
    

1. Create the `package.json` with the following command:

    ```shell
    npm init -y
    ```

1. Update the `package.json` to ECMAScript with the following command: 

    ```shell
    npm pkg set type=module
    ```
    
1. Install the real-time audio client library for JavaScript with:

    ```console
    npm install https://github.com/Azure-Samples/aoai-realtime-audio-sdk/releases/download/js/v0.5.2/rt-client-0.5.2.tgz
    ```

1. For the **recommended** keyless authentication with Microsoft Entra ID, install the `@azure/identity` package with:

    ```console
    npm install @azure/identity
    ```

## Retrieve resource information

[!INCLUDE [resource authentication](resource-authentication.md)]

> [!CAUTION]
> To use the recommended keyless authentication with the SDK, make sure that the `AZURE_OPENAI_API_KEY` environment variable isn't set. 

## Text in audio out

#### [Microsoft Entra ID](#tab/keyless)

1. Create the `text-in-audio-out.ts` file with the following code:

    ```typescript
    import { DefaultAzureCredential } from "@azure/identity";
    import { LowLevelRTClient } from "rt-client";
    import dotenv from "dotenv";
    dotenv.config();
    
    async function text_in_audio_out() {
        // Set environment variables or edit the corresponding values here.
        const endpoint: string = process.env.AZURE_OPENAI_ENDPOINT || "Your endpoint";
        const deployment = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || "gpt-4o-mini-realtime-preview";
        if (!endpoint || !deployment) {
            throw new Error("You didn't set the environment variables.");
        }
        const client = new LowLevelRTClient(
            new URL(endpoint), 
            new DefaultAzureCredential(), 
            {deployment: deployment}
        );
        try {
            await client.send({
                type: "response.create",
                response: {
                    modalities: ["audio", "text"],
                    instructions: "Please assist the user."
                }
            });
    
            for await (const message of client.messages()) {
                switch (message.type) {
                    case "response.done": {
                        break;
                    }
                    case "error": {
                        console.error(message.error);
                        break;
                    }
                    case "response.audio_transcript.delta": {
                        console.log(`Received text delta: ${message.delta}`);
                        break;
                    }
                    case "response.audio.delta": {
                        const buffer = Buffer.from(message.delta, "base64");
                        console.log(`Received ${buffer.length} bytes of audio data.`);
                        break;
                    }
                }
                if (message.type === "response.done" || message.type === "error") {
                    break;
                }
            }
        } finally {
            client.close();
        }
    }
    
    await text_in_audio_out();
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
    node text-in-audio-out.js
    ```

#### [API key](#tab/api-key)

1. Create the `text-in-audio-out.ts` file with the following code:

    ```typescript
    import { AzureKeyCredential } from "@azure/core-auth";
    import { LowLevelRTClient } from "rt-client";
    import dotenv from "dotenv";
    dotenv.config();
    
    async function text_in_audio_out() {
        // Set environment variables or edit the corresponding values here.
        const apiKey: string = process.env.AZURE_OPENAI_API_KEY || "Your API key";
        const endpoint: string = process.env.AZURE_OPENAI_ENDPOINT || "Your endpoint";
        const deployment = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || "gpt-4o-mini-realtime-preview";
        if (!endpoint || !deployment) {
            throw new Error("You didn't set the environment variables.");
        }
        const client = new LowLevelRTClient(
            new URL(endpoint), 
            new AzureKeyCredential(apiKey),
            {deployment: deployment}
        );
        try {
            await client.send({
                type: "response.create",
                response: {
                    modalities: ["audio", "text"],
                    instructions: "Please assist the user."
                }
            });
    
            for await (const message of client.messages()) {
                switch (message.type) {
                    case "response.done": {
                        break;
                    }
                    case "error": {
                        console.error(message.error);
                        break;
                    }
                    case "response.audio_transcript.delta": {
                        console.log(`Received text delta: ${message.delta}`);
                        break;
                    }
                    case "response.audio.delta": {
                        const buffer = Buffer.from(message.delta, "base64");
                        console.log(`Received ${buffer.length} bytes of audio data.`);
                        break;
                    }
                }
                if (message.type === "response.done" || message.type === "error") {
                    break;
                }
            }
        } finally {
            client.close();
        }
    }
    
    await text_in_audio_out();
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
    node text-in-audio-out.js
    ```

---

Wait a few moments to get the response.

## Output

The script gets a response from the model and prints the transcript and audio data received.

The output will look similar to the following:

```console
Received text delta: Hello
Received text delta: !
Received text delta:  How
Received text delta:  can
Received text delta:  I
Received 4800 bytes of audio data.
Received 7200 bytes of audio data.
Received text delta:  help
Received 12000 bytes of audio data.
Received text delta:  you
Received text delta:  today
Received text delta: ?
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received 24000 bytes of audio data.
```
