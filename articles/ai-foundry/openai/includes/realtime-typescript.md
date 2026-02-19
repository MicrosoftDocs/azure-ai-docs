---
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 3/20/2025
---

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)
- <a href="https://nodejs.org/" target="_blank">Node.js LTS or ESM support.</a>
- [TypeScript](https://www.typescriptlang.org/download/) installed globally.
- An Azure OpenAI resource created in one of the supported regions. For more information about region availability, see the [models and versions documentation](../../foundry-models/concepts/models-sold-directly-by-azure.md#global-standard-model-availability).
- Then, you need to deploy a `gpt-realtime` model with your Azure OpenAI resource. For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md). 

### Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services OpenAI User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Deploy a model for real-time audio

[!INCLUDE [Deploy model](realtime-deploy-model.md)]

## Set up

1. Create a new folder `realtime-audio-quickstart-ts` and go to the quickstart folder with the following command:

    ```bash
    mkdir realtime-audio-quickstart-ts && cd realtime-audio-quickstart-ts
    ```
    
1. Create the `package.json` with the following command:

    ```bash    
    npm init -y
    ```

1. Update the `package.json` to ECMAScript with the following command: 

    ```bash
    npm pkg set type=module
    ```
    
1. Install the OpenAI client library for JavaScript with:

    ```bash
    npm install openai
    ```

1. Install the dependent packages used by the OpenAI client library for JavaScript with:

    ```bash
    npm install ws
    ```

1. For the **recommended** keyless authentication with Microsoft Entra ID, install the `@azure/identity` package with:

    ```bash
    npm install @azure/identity
    ```

## Retrieve resource information

[!INCLUDE [resource authentication](resource-authentication.md)]

> [!CAUTION]
> To use the recommended keyless authentication with the SDK, make sure that the `AZURE_OPENAI_API_KEY` environment variable isn't set. 

## Send text, receive audio response

#### [Microsoft Entra ID](#tab/keyless)

1. Create the `index.ts` file with the following code:

    ```typescript
    import OpenAI from 'openai';
    import { OpenAIRealtimeWS } from 'openai/realtime/ws';
    import { OpenAIRealtimeError } from 'openai/realtime/internal-base';
    import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";
    import { RealtimeSessionCreateRequest } from 'openai/resources/realtime/realtime';
    
    let isCreated = false;
    let isConfigured = false;
    let responseDone = false;
    
    // Set this to false, if you want to continue receiving events after an error is received.
    const throwOnError = true;
    
    async function main(): Promise<void> {
        // The endpoint of your Azure OpenAI resource is required. You can set it in the AZURE_OPENAI_ENDPOINT
        // environment variable or replace the default value below.
        // You can find it in the Microsoft Foundry portal in the Overview page of your Azure OpenAI resource.
        // Example: https://{your-resource}.openai.azure.com
        const endpoint = process.env.AZURE_OPENAI_ENDPOINT || 'AZURE_OPENAI_ENDPOINT';
        const baseUrl = endpoint.replace(/\/$/, "") + '/openai/v1';
    
        // The deployment name of your Azure OpenAI model is required. You can set it in the AZURE_OPENAI_DEPLOYMENT_NAME
        // environment variable or replace the default value below.
        // You can find it in the Foundry portal in the "Models + endpoints" page of your Azure OpenAI resource.
        // Example: gpt-realtime
        const deploymentName = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || 'gpt-realtime';
    
        // Keyless authentication
        const credential = new DefaultAzureCredential();
        const scope = "https://cognitiveservices.azure.com/.default";
        const azureADTokenProvider = getBearerTokenProvider(credential, scope);
        const token = await azureADTokenProvider();
    
        // The APIs are compatible with the OpenAI client library.
        // You can use the OpenAI client library to access the Azure OpenAI APIs.
        // Make sure to set the baseURL and apiKey to use the Azure OpenAI endpoint and token.
        const openAIClient = new OpenAI({
            baseURL: baseUrl,
            apiKey: token,
        });
        const realtimeClient = await OpenAIRealtimeWS.create(openAIClient, { model: deploymentName });
    
        realtimeClient.on('error', (receivedError) => receiveError(receivedError));
        realtimeClient.on('session.created', (receivedEvent) => receiveEvent(receivedEvent));
        realtimeClient.on('session.updated', (receivedEvent) => receiveEvent(receivedEvent));
        realtimeClient.on('response.output_audio.delta', (receivedEvent) => receiveEvent(receivedEvent));
        realtimeClient.on('response.output_audio_transcript.delta', (receivedEvent) => receiveEvent(receivedEvent));
        realtimeClient.on('response.done', (receivedEvent) => receiveEvent(receivedEvent));
    
        console.log('Waiting for events...');
        while (!isCreated) {
            console.log('Waiting for session.created event...');
            await new Promise((resolve) => setTimeout(resolve, 100));
        }
    
        // After the session is created, configure it to enable audio input and output.
        const sessionConfig: RealtimeSessionCreateRequest = {
            'type': 'realtime',
            'instructions': 'You are a helpful assistant. You respond by voice and text.',
            'output_modalities': ['audio'],
            'audio': {
                'input': {
                    'transcription': {
                        'model': 'whisper-1'
                    },
                    'format': {
                        'type': 'audio/pcm',
                        'rate': 24000,
                    },
                    'turn_detection': {
                        'type': 'server_vad',
                        'threshold': 0.5,
                        'prefix_padding_ms': 300,
                        'silence_duration_ms': 200,
                        'create_response': true
                    }
                },
                'output': {
                    'voice': 'alloy',
                    'format': {
                        'type': 'audio/pcm',
                        'rate': 24000,
                    }
                }
            }
        };
    
        realtimeClient.send({ 'type': 'session.update', 'session': sessionConfig });
    
        while (!isConfigured) {
            console.log('Waiting for session.updated event...');
            await new Promise((resolve) => setTimeout(resolve, 100));
        }
    
        // After the session is configured, data can be sent to the session.
        realtimeClient.send({
            'type': 'conversation.item.create',
            'item': {
                'type': 'message',
                'role': 'user',
                'content': [{ type: 'input_text', text: 'Please assist the user.' }]
            }
        });
    
        realtimeClient.send({ type: 'response.create' });
    
        // While waiting for the session to finish, the events can be handled in the event handlers.
        // In this example, we just wait for the first response.done event. 
        while (!responseDone) {
            console.log('Waiting for response.done event...');
            await new Promise((resolve) => setTimeout(resolve, 100));
        }
    
        console.log('The sample completed successfully.');
        realtimeClient.close();
    }
    
    function receiveError(errorEvent: OpenAIRealtimeError): void {
        if (errorEvent instanceof OpenAIRealtimeError) {
            console.error('Received an error event.');
            console.error(`Message: ${errorEvent.message}`);
            console.error(`Stack: ${errorEvent.stack}`); errorEvent
        }
    
        if (throwOnError) {
            throw errorEvent;
        }
    }
    
    function receiveEvent(event: any): void {
        console.log(`Received an event: ${event.type}`);
    
        switch (event.type) {
            case 'session.created':
                console.log(`Session ID: ${event.session.id}`);
                isCreated = true;
                break;
            case 'session.updated':
                console.log(`Session ID: ${event.session.id}`);
                isConfigured = true;
                break;
            case 'response.output_audio_transcript.delta':
                console.log(`Transcript delta: ${event.delta}`);
                break;
            case 'response.output_audio.delta':
                let audioBuffer = Buffer.from(event.delta, 'base64');
                console.log(`Audio delta length: ${audioBuffer.length} bytes`);
                break;
            case 'response.done':
                console.log(`Response ID: ${event.response.id}`);
                console.log(`The final response is: ${event.response.output[0].content[0].transcript}`);
                responseDone = true;
                break;
            default:
                console.warn(`Unhandled event type: ${event.type}`);
        }
    }
    
    main().catch((err) => {
        console.error("The sample encountered an error:", err);
    });
    
    export { main };    
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
1. Install type definitions for Node

    ```bash
    npm i --save-dev @types/node
    ```
    
1. Transpile from TypeScript to JavaScript.

    ```bash
    tsc
    ```
    
1. Sign in to Azure with the following command:

    ```bash
    az login
    ```

1. Run the code with the following command:

    ```bash
    node index.js
    ```

#### [API key](#tab/api-key)

1. Create the `index.ts` file with the following code:

    ```typescript
    import OpenAI from 'openai';
    import { OpenAIRealtimeWS } from 'openai/realtime/ws';
    import { OpenAIRealtimeError } from 'openai/realtime/internal-base';
    import { RealtimeSessionCreateRequest } from 'openai/resources/realtime/realtime';
    
    let isCreated = false;
    let isConfigured = false;
    let responseDone = false;
    
    // Set this to false, if you want to continue receiving events after an error is received.
    const throwOnError = true;
    
    async function main(): Promise<void> {
        // The endpoint of your Azure OpenAI resource is required. You can set it in the AZURE_OPENAI_ENDPOINT
        // environment variable or replace the default value below.
        // You can find it in the Foundry portal in the Overview page of your Azure OpenAI resource.
        // Example: https://{your-resource}.openai.azure.com
        const endpoint = process.env.AZURE_OPENAI_ENDPOINT || 'AZURE_OPENAI_ENDPOINT';
        const baseUrl = endpoint.replace(/\/$/, "") + '/openai/v1';
    
        // The deployment name of your Azure OpenAI model is required. You can set it in the AZURE_OPENAI_DEPLOYMENT_NAME
        // environment variable or replace the default value below.
        // You can find it in the Foundry portal in the "Models + endpoints" page of your Azure OpenAI resource.
        // Example: gpt-realtime
        const deploymentName = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || 'gpt-realtime';
    
        // API Key of your Azure OpenAI resource is required. You can set it in the AZURE_OPENAI_API_KEY
        // environment variable or replace the default value below.
        // You can find it in the Foundry portal in the Overview page of your Azure OpenAI resource.
        const token = process.env.AZURE_OPENAI_API_KEY || '<Your API Key>';
    
        // The APIs are compatible with the OpenAI client library.
        // You can use the OpenAI client library to access the Azure OpenAI APIs.
        // Make sure to set the baseURL and apiKey to use the Azure OpenAI endpoint and token.
        const openAIClient = new OpenAI({
            baseURL: baseUrl,
            apiKey: token,
        });
    
        // Due to the current SDK limitation we need to explicitly
        // pass API key as Header
        const realtimeClient = await OpenAIRealtimeWS.create(
            openAIClient, {
            model: deploymentName,
            options: {
                headers: {
                    "api-key": token
                }
            }
        });
    
        realtimeClient.on('error', (receivedError) => receiveError(receivedError));
        realtimeClient.on('session.created', (receivedEvent) => receiveEvent(receivedEvent));
        realtimeClient.on('session.updated', (receivedEvent) => receiveEvent(receivedEvent));
        realtimeClient.on('response.output_audio.delta', (receivedEvent) => receiveEvent(receivedEvent));
        realtimeClient.on('response.output_audio_transcript.delta', (receivedEvent) => receiveEvent(receivedEvent));
        realtimeClient.on('response.done', (receivedEvent) => receiveEvent(receivedEvent));
    
        console.log('Waiting for events...');
        while (!isCreated) {
            console.log('Waiting for session.created event...');
            await new Promise((resolve) => setTimeout(resolve, 100));
        }
    
        // After the session is created, configure it to enable audio input and output.
        const sessionConfig: RealtimeSessionCreateRequest = {
            'type': 'realtime',
            'instructions': 'You are a helpful assistant. You respond by voice and text.',
            'output_modalities': ['audio'],
            'audio': {
                'input': {
                    'transcription': {
                        'model': 'whisper-1'
                    },
                    'format': {
                        'type': 'audio/pcm',
                        'rate': 24000,
                    },
                    'turn_detection': {
                        'type': 'server_vad',
                        'threshold': 0.5,
                        'prefix_padding_ms': 300,
                        'silence_duration_ms': 200,
                        'create_response': true
                    }
                },
                'output': {
                    'voice': 'alloy',
                    'format': {
                        'type': 'audio/pcm',
                        'rate': 24000,
                    }
                }
            }
        };
    
        realtimeClient.send({
            'type': 'session.update',
            'session': sessionConfig
        });
        while (!isConfigured) {
            console.log('Waiting for session.updated event...');
            await new Promise((resolve) => setTimeout(resolve, 100));
        }
    
        // After the session is configured, data can be sent to the session.    
        realtimeClient.send({
            'type': 'conversation.item.create',
            'item': {
                'type': 'message',
                'role': 'user',
                'content': [{
                    type: 'input_text',
                    text: 'Please assist the user.'
                }
                ]
            }
        });
    
        realtimeClient.send({
            type: 'response.create'
        });
    
        // While waiting for the session to finish, the events can be handled in the event handlers.
        // In this example, we just wait for the first response.done event.
        while (!responseDone) {
            console.log('Waiting for response.done event...');
            await new Promise((resolve) => setTimeout(resolve, 100));
        }
    
        console.log('The sample completed successfully.');
        realtimeClient.close();
    }
    
    function receiveError(errorEvent: OpenAIRealtimeError): void {
        if (errorEvent instanceof OpenAIRealtimeError) {
            console.error('Received an error event.');
            console.error(`Message: ${errorEvent.message}`);
            console.error(`Stack: ${errorEvent.stack}`);
            errorEvent
        }
    
        if (throwOnError) {
            throw errorEvent;
        }
    }
    
    function receiveEvent(event: any): void {
        console.log(`Received an event: ${event.type}`);
    
        switch (event.type) {
            case 'session.created':
                console.log(`Session ID: ${event.session.id}`);
                isCreated = true;
                break;
            case 'session.updated':
                console.log(`Session ID: ${event.session.id}`);
                isConfigured = true;
                break;
            case 'response.output_audio_transcript.delta':
                console.log(`Transcript delta: ${event.delta}`);
                break;
            case 'response.output_audio.delta':
                let audioBuffer = Buffer.from(event.delta, 'base64');
                console.log(`Audio delta length: ${audioBuffer.length} bytes`);
                break;
            case 'response.done':
                console.log(`Response ID: ${event.response.id}`);
                console.log(`The final response is: ${event.response.output[0].content[0].transcript}`);
                responseDone = true;
                break;
            default:
                console.warn(`Unhandled event type: ${event.type}`);
        }
    }
    
    main().catch((err) => {
        console.error("The sample encountered an error:", err);
    });
    
    export {
        main
    };
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

1. Install type definitions for Node

    ```bash
    npm i --save-dev @types/node
    ```

1. Transpile from TypeScript to JavaScript.

    ```bash
    tsc
    ```

1. Run the code with the following command:

    ```bash
    node index.js
    ```

---

Wait a few moments to get the response.

## Output

The script gets a response from the model and prints the transcript and audio data received.

The output will look similar to the following:

```console
Waiting for events...
Waiting for session.created event...
Waiting for session.created event...
Waiting for session.created event...
Waiting for session.created event...
Waiting for session.created event...
Waiting for session.created event...
Waiting for session.created event...
Waiting for session.created event...
Waiting for session.created event...
Waiting for session.created event...
Received an event: session.created
Session ID: sess_CWQkREiv3jlU3gk48bm0a
Waiting for session.updated event...
Waiting for session.updated event...
Received an event: session.updated
Session ID: sess_CWQkREiv3jlU3gk48bm0a
Waiting for response.done event...
Waiting for response.done event...
Waiting for response.done event...
Waiting for response.done event...
Waiting for response.done event...
Received an event: response.output_audio_transcript.delta
Transcript delta: Sure
Received an event: response.output_audio_transcript.delta
Transcript delta: ,
Received an event: response.output_audio_transcript.delta
Transcript delta:  I'm
Received an event: response.output_audio_transcript.delta
Transcript delta:  here
Waiting for response.done event...
Received an event: response.output_audio.delta
Audio delta length: 4800 bytes
Waiting for response.done event...
Received an event: response.output_audio.delta
Audio delta length: 7200 bytes
Waiting for response.done event...
Received an event: response.output_audio.delta
Audio delta length: 12000 bytes
Received an event: response.output_audio_transcript.delta
Transcript delta:  to
Received an event: response.output_audio_transcript.delta
Transcript delta:  help
Received an event: response.output_audio_transcript.delta
Transcript delta: .
Waiting for response.done event...
Received an event: response.output_audio.delta
Audio delta length: 12000 bytes
Received an event: response.output_audio.delta
Audio delta length: 12000 bytes
Received an event: response.output_audio_transcript.delta
Transcript delta:  What
Received an event: response.output_audio_transcript.delta
Transcript delta:  would
Received an event: response.output_audio_transcript.delta
Transcript delta:  you
Received an event: response.output_audio_transcript.delta
Transcript delta:  like
Waiting for response.done event...
Received an event: response.output_audio.delta
Audio delta length: 12000 bytes
Received an event: response.output_audio.delta
Audio delta length: 12000 bytes
Received an event: response.output_audio.delta
Audio delta length: 12000 bytes
Received an event: response.output_audio_transcript.delta
Transcript delta:  to
Received an event: response.output_audio_transcript.delta
Transcript delta:  do
Received an event: response.output_audio_transcript.delta
Transcript delta:  or
Received an event: response.output_audio_transcript.delta
Transcript delta:  know
Received an event: response.output_audio_transcript.delta
Transcript delta:  about
Received an event: response.output_audio_transcript.delta
Transcript delta: ?
Waiting for response.done event...
Received an event: response.output_audio.delta
Audio delta length: 12000 bytes
Received an event: response.output_audio.delta
Audio delta length: 12000 bytes
Received an event: response.output_audio.delta
Audio delta length: 12000 bytes
Waiting for response.done event...
Received an event: response.output_audio.delta
Audio delta length: 12000 bytes
Received an event: response.output_audio.delta
Audio delta length: 12000 bytes
Waiting for response.done event...
Received an event: response.output_audio.delta
Audio delta length: 12000 bytes
Received an event: response.output_audio.delta
Audio delta length: 12000 bytes
Received an event: response.output_audio.delta
Audio delta length: 24000 bytes
Received an event: response.done
Response ID: resp_CWQkRBrCcCjtHgIEapA92
The final response is: Sure, I'm here to help. What would you like to do or know about?
The sample completed successfully.
```
