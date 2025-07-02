---
manager: nitinme
author: eric-urban
ms.author: eur
ms.service: azure-ai-openai
ms.topic: include
ms.date: 3/20/2025
---

## Prerequisites

- An Azure subscription - <a href="https://azure.microsoft.com/free/cognitive-services" target="_blank">Create one for free</a>
- <a href="https://nodejs.org/" target="_blank">Node.js LTS or ESM support.</a>
- An Azure OpenAI resource created in one of the supported regions. For more information about region availability, see the [models and versions documentation](../concepts/models.md#global-standard-model-availability).
- Then, you need to deploy a `gpt-4o-mini-realtime-preview` model with your Azure OpenAI resource. For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md). 

### Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Deploy a model for real-time audio

[!INCLUDE [Deploy model](realtime-deploy-model.md)]

## Set up

1. Create a new folder `realtime-audio-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir realtime-audio-quickstart && cd realtime-audio-quickstart
    ```
    
1. Create the `package.json` with the following command:

    ```shell
    npm init -y
    ```

1. Install the OpenAI client library for JavaScript with:

    ```console
    npm install openai
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

1. Create the `index.js` file with the following code:

    ```javascript 
    import { OpenAIRealtimeWS } from "openai/beta/realtime/ws";
    import { AzureOpenAI } from "openai";
    import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";
    async function main() {
        // You will need to set these environment variables or edit the following values
        const endpoint = process.env.AZURE_OPENAI_ENDPOINT || "AZURE_OPENAI_ENDPOINT";
        // Required Azure OpenAI deployment name and API version
        const deploymentName = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || "gpt-4o-mini-realtime-preview";
        const apiVersion = process.env.OPENAI_API_VERSION || "2025-04-01-preview";
        // Keyless authentication 
        const credential = new DefaultAzureCredential();
        const scope = "https://cognitiveservices.azure.com/.default";
        const azureADTokenProvider = getBearerTokenProvider(credential, scope);
        const azureOpenAIClient = new AzureOpenAI({
            azureADTokenProvider,
            apiVersion: apiVersion,
            deployment: deploymentName,
            endpoint: endpoint,
        });
        const realtimeClient = await OpenAIRealtimeWS.azure(azureOpenAIClient);
        realtimeClient.socket.on("open", () => {
            console.log("Connection opened!");
            realtimeClient.send({
                type: "session.update",
                session: {
                    modalities: ["text", "audio"],
                    model: "gpt-4o-mini-realtime-preview",
                },
            });
            realtimeClient.send({
                type: "conversation.item.create",
                item: {
                    type: "message",
                    role: "user",
                    content: [{ type: "input_text", text: "Please assist the user" }],
                },
            });
            realtimeClient.send({ type: "response.create" });
        });
        realtimeClient.on("error", (err) => {
            // Instead of throwing the error, you can log it
            // and continue processing events.
            throw err;
        });
        realtimeClient.on("session.created", (event) => {
            console.log("session created!", event.session);
            console.log();
        });
        realtimeClient.on("response.text.delta", (event) => process.stdout.write(event.delta));
        realtimeClient.on("response.audio.delta", (event) => {
            const buffer = Buffer.from(event.delta, "base64");
            console.log(`Received ${buffer.length} bytes of audio data.`);
        });
        realtimeClient.on("response.audio_transcript.delta", (event) => {
            console.log(`Received text delta:${event.delta}.`);
        });
        realtimeClient.on("response.text.done", () => console.log());
        realtimeClient.on("response.done", () => realtimeClient.close());
        realtimeClient.socket.on("close", () => console.log("\nConnection closed!"));
    }
    main().catch((err) => {
        console.error("The sample encountered an error:", err);
    });
    export { main };
    ```

1. Sign in to Azure with the following command:

    ```shell
    az login
    ```

1. Run the JavaScript file.

    ```shell
    node index.js
    ```

#### [API key](#tab/api-key)

1. Create the `index.js` file with the following code:

    ```javascript 
    import { OpenAIRealtimeWS } from "openai/beta/realtime/ws";
    import { AzureOpenAI } from "openai";
    async function main() {
        // You will need to set these environment variables or edit the following values
        const endpoint = process.env.AZURE_OPENAI_ENDPOINT || "AZURE_OPENAI_ENDPOINT";
        const apiKey = process.env.AZURE_OPENAI_API_KEY || "Your API key";
        // Required Azure OpenAI deployment name and API version
        const deploymentName = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || "gpt-4o-mini-realtime-preview";
        const apiVersion = process.env.OPENAI_API_VERSION || "2025-04-01-preview";
        const azureOpenAIClient = new AzureOpenAI({
            apiKey: apiKey,
            apiVersion: apiVersion,
            deployment: deploymentName,
            endpoint: endpoint,
        });
        const realtimeClient = await OpenAIRealtimeWS.azure(azureOpenAIClient);
        realtimeClient.socket.on("open", () => {
            console.log("Connection opened!");
            realtimeClient.send({
                type: "session.update",
                session: {
                    modalities: ["text", "audio"],
                    model: "gpt-4o-mini-realtime-preview",
                },
            });
            realtimeClient.send({
                type: "conversation.item.create",
                item: {
                    type: "message",
                    role: "user",
                    content: [{ type: "input_text", text: "Please assist the user" }],
                },
            });
            realtimeClient.send({ type: "response.create" });
        });
        realtimeClient.on("error", (err) => {
            // Instead of throwing the error, you can log it
            // and continue processing events.
            throw err;
        });
        realtimeClient.on("session.created", (event) => {
            console.log("session created!", event.session);
            console.log();
        });
        realtimeClient.on("response.text.delta", (event) => process.stdout.write(event.delta));
        realtimeClient.on("response.audio.delta", (event) => {
            const buffer = Buffer.from(event.delta, "base64");
            console.log(`Received ${buffer.length} bytes of audio data.`);
        });
        realtimeClient.on("response.audio_transcript.delta", (event) => {
            console.log(`Received text delta:${event.delta}.`);
        });
        realtimeClient.on("response.text.done", () => console.log());
        realtimeClient.on("response.done", () => realtimeClient.close());
        realtimeClient.socket.on("close", () => console.log("\nConnection closed!"));
    }
    main().catch((err) => {
        console.error("The sample encountered an error:", err);
    });
    export { main };
    ```

1. Run the JavaScript file.

    ```shell
    node index.js
    ```

---

Wait a few moments to get the response.

## Output

The script gets a response from the model and prints the transcript and audio data received.

The output will look similar to the following:

```console
Received text delta:Of.
Received text delta: course.
Received text delta:!.
Received text delta: How.
Received text delta: can.
Received 4800 bytes of audio data.
Received 7200 bytes of audio data.
Received text delta: I.
Received 12000 bytes of audio data.
Received text delta: help.
Received text delta: you.
Received text delta: today.
Received text delta:?.
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received 26400 bytes of audio data.

Connection closed!
```
