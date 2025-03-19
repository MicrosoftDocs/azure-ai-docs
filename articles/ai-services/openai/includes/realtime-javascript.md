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

1. Create a new folder `realtime-audio-quickstart` to contain the application and open Visual Studio Code in that folder with the following command:

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
    import { AzureOpenAI } from "openai/index.mjs";
    import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";
    async function main() {
        // You will need to set these environment variables or edit the following values
        const endpoint = process.env.AZURE_OPENAI_ENDPOINT || "AZURE_OPENAI_ENDPOINT";
        // Required Azure OpenAI deployment name and API version
        const deploymentName = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || "gpt-4o-mini-realtime-preview";
        const apiVersion = process.env.OPENAI_API_VERSION || "2024-10-01-preview";
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
    import { AzureOpenAI } from "openai/index.mjs";
    async function main() {
        // You will need to set these environment variables or edit the following values
        const endpoint = process.env.AZURE_OPENAI_ENDPOINT || "AZURE_OPENAI_ENDPOINT";
        const apiKey = process.env.AZURE_OPENAI_API_KEY || "Your API key";
        // Required Azure OpenAI deployment name and API version
        const deploymentName = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || "gpt-4o-mini-realtime-preview";
        const apiVersion = process.env.OPENAI_API_VERSION || "2024-10-01-preview";
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

## Web application sample

Our JavaScript web sample [on GitHub](https://github.com/azure-samples/aoai-realtime-audio-sdk) demonstrates how to use the GPT-4o Realtime API to interact with the model in real time. The sample code includes a simple web interface that captures audio from the user's microphone and sends it to the model for processing. The model responds with text and audio, which the sample code renders in the web interface.

You can run the sample code locally on your machine by following these steps. Refer to the [repository on GitHub](https://github.com/azure-samples/aoai-realtime-audio-sdk) for the most up-to-date instructions.
1. If you don't have Node.js installed, download and install the [LTS version of Node.js](https://nodejs.org/).

1. Clone the repository to your local machine:
    
    ```bash
    git clone https://github.com/Azure-Samples/aoai-realtime-audio-sdk.git
    ```

1. Go to the `javascript/samples/web` folder in your preferred code editor.

    ```bash
    cd ./javascript/samples
    ```

1. Run `download-pkg.ps1` or `download-pkg.sh` to download the required packages. 

1. Go to the `web` folder from the `./javascript/samples` folder.

    ```bash
    cd ./web
    ```

1. Run `npm install` to install package dependencies.

1. Run `npm run dev` to start the web server, navigating any firewall permissions prompts as needed.
1. Go to any of the provided URIs from the console output (such as `http://localhost:5173/`) in a browser.
1. Enter the following information in the web interface:
    - **Endpoint**: The resource endpoint of an Azure OpenAI resource. You don't need to append the `/realtime` path. An example structure might be `https://my-azure-openai-resource-from-portal.openai.azure.com`.
    - **API Key**: A corresponding API key for the Azure OpenAI resource.
    - **Deployment**: The name of the `gpt-4o-mini-realtime-preview` model that [you deployed in the previous section](#deploy-a-model-for-real-time-audio).
    - **System Message**: Optionally, you can provide a system message such as "You always talk like a friendly pirate."
    - **Temperature**: Optionally, you can provide a custom temperature.
    - **Voice**: Optionally, you can select a voice.
1. Select the **Record** button to start the session. Accept permissions to use your microphone if prompted.
1. You should see a `<< Session Started >>` message in the main output. Then you can speak into the microphone to start a chat.
1. You can interrupt the chat at any time by speaking. You can end the chat by selecting the **Stop** button.
