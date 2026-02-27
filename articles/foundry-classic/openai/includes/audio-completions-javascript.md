---
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 1/21/2025
---

[Reference documentation](https://platform.openai.com/docs/api-reference/chat) | [Library source code](https://github.com/openai/openai-node?azure-portal=true) | [Package (npm)](https://www.npmjs.com/package/openai) | [Samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai/samples)

[!INCLUDE [Audio completions introduction](audio-completions-intro.md)]

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)
- <a href="https://nodejs.org/" target="_blank">Node.js LTS or ESM support.</a>
- An Azure OpenAI resource created in one of the supported regions. For more information about region availability, see the [models and versions documentation](../../foundry-models/concepts/models-sold-directly-by-azure.md#global-standard-model-availability).
- Then, you need to deploy a `gpt-4o-mini-audio-preview` model with your Azure OpenAI resource. For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md). 

## Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Set up

1. Create a new folder `audio-completions-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir audio-completions-quickstart && cd audio-completions-quickstart
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

## Generate audio from text input

#### [Microsoft Entra ID](#tab/keyless)

1. Create the `to-audio.js` file with the following code:

    ```javascript
    require("dotenv").config();
    const { AzureOpenAI } = require("openai");
    const { DefaultAzureCredential, getBearerTokenProvider } = require("@azure/identity");
    const { writeFileSync } = require("node:fs");
    
    // Keyless authentication    
    const credential = new DefaultAzureCredential();
    const scope = "https://cognitiveservices.azure.com/.default";
    const azureADTokenProvider = getBearerTokenProvider(credential, scope);
    
    // Set environment variables or edit the corresponding values here.
    const endpoint = process.env.AZURE_OPENAI_ENDPOINT || "AZURE_OPENAI_ENDPOINT";
    const deployment = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || "gpt-4o-mini-audio-preview"; 
    const apiVersion = process.env.OPENAI_API_VERSION || "2025-01-01-preview"; 
    
    const client = new AzureOpenAI({ 
        endpoint, 
        azureADTokenProvider, 
        apiVersion, 
        deployment 
    }); 
    
    async function main() {
    
        // Make the audio chat completions request
        const response = await client.chat.completions.create({ 
            model: "gpt-4o-mini-audio-preview", 
            modalities: ["text", "audio"], 
            audio: { voice: "alloy", format: "wav" }, 
            messages: [ 
            { 
                role: "user", 
                content: "Is a golden retriever a good family dog?" 
            } 
            ] 
        }); 
      
    // Inspect returned data 
    console.log(response.choices[0]); 
    
    // Write the output audio data to a file
    writeFileSync( 
        "dog.wav", 
        Buffer.from(response.choices[0].message.audio.data, 'base64'), 
        { encoding: "utf-8" } 
    ); 
    }
    
    main().catch((err) => {
      console.error("Error occurred:", err);
    });
    
    module.exports = { main };
    ```

1. Sign in to Azure with the following command:

    ```shell
    az login
    ```

1. Run the JavaScript file.

    ```shell
    node to-audio.js
    ```


#### [API key](#tab/api-key)

1. Create the `to-audio.js` file with the following code:

    ```javascript
    require("dotenv").config();
    const { AzureOpenAI } = require("openai");
    const { writeFileSync } = require("node:fs");
    
    // Set environment variables or edit the corresponding values here.
    const endpoint = process.env.AZURE_OPENAI_ENDPOINT || "AZURE_OPENAI_ENDPOINT";
    const apiKey = process.env.AZURE_OPENAI_API_KEY || "AZURE_OPENAI_API_KEY";
    const apiVersion = "2025-01-01-preview"; 
    const deployment = "gpt-4o-mini-audio-preview"; 
    
    const client = new AzureOpenAI({ 
        endpoint, 
        apiKey, 
        apiVersion, 
        deployment 
    });  
    
    async function main() {
    
        // Make the audio chat completions request
        const response = await client.chat.completions.create({ 
            model: "gpt-4o-mini-audio-preview", 
            modalities: ["text", "audio"], 
            audio: { voice: "alloy", format: "wav" }, 
            messages: [ 
            { 
                role: "user", 
                content: "Is a golden retriever a good family dog?" 
            } 
            ] 
        }); 
      
    // Inspect returned data 
    console.log(response.choices[0]); 
    
    // Write the output audio data to a file
    writeFileSync( 
        "dog.wav", 
        Buffer.from(response.choices[0].message.audio.data, 'base64'), 
        { encoding: "utf-8" } 
    ); 
    }
    
    main().catch((err) => {
      console.error("Error occurred:", err);
    });
    
    module.exports = { main };
    ```

1. Run the JavaScript file.

    ```shell
    node to-audio.js
    ```

---

Wait a few moments to get the response.

### Output for audio generation from text input

The script generates an audio file named _dog.wav_ in the same directory as the script. The audio file contains the spoken response to the prompt, "Is a golden retriever a good family dog?"


## Generate audio and text from audio input

#### [Microsoft Entra ID](#tab/keyless)

1. Create the `from-audio.js` file with the following code:

    ```javascript
    require("dotenv").config();
    const { AzureOpenAI } = require("openai");
    const { DefaultAzureCredential, getBearerTokenProvider } = require("@azure/identity");
    const fs = require('fs').promises;
    const { writeFileSync } = require("node:fs");
    
    // Keyless authentication    
    const credential = new DefaultAzureCredential();
    const scope = "https://cognitiveservices.azure.com/.default";
    const azureADTokenProvider = getBearerTokenProvider(credential, scope);
    
    // Set environment variables or edit the corresponding values here.
    const endpoint = process.env.AZURE_OPENAI_ENDPOINT || "AZURE_OPENAI_ENDPOINT";
    const apiVersion = "2025-01-01-preview"; 
    const deployment = "gpt-4o-mini-audio-preview"; 
    
    const client = new AzureOpenAI({ 
        endpoint, 
        azureADTokenProvider, 
        apiVersion, 
        deployment 
    });    
    
    async function main() {
        
        // Buffer the audio for input to the chat completion
        const wavBuffer = await fs.readFile("dog.wav"); 
        const base64str = Buffer.from(wavBuffer).toString("base64"); 
        
        // Make the audio chat completions request
        const response = await client.chat.completions.create({
            model: "gpt-4o-mini-audio-preview",
            modalities: ["text", "audio"],
            audio: { voice: "alloy", format: "wav" }, 
            messages: [
                {
                    role: "user",
                    content: [
                        { 
                            type: "text", 
                            text: "Describe in detail the spoken audio input." 
                        },
                        { 
                            type: "input_audio", 
                            input_audio: { 
                                data: base64str, 
                                format: "wav" 
                            } 
                        }
                    ]
                }
            ]
        });
        
        console.log(response.choices[0]); 
      
        // Write the output audio data to a file
        writeFileSync( 
            "analysis.wav", 
            Buffer.from(response.choices[0].message.audio.data, 'base64'), 
            { encoding: "utf-8" } 
        ); 
    }
    
    main().catch((err) => {
        console.error("Error occurred:", err);
    });
    
    module.exports = { main };
    ```

1. Sign in to Azure with the following command:

    ```shell
    az login
    ```

1. Run the JavaScript file.

    ```shell
    node from-audio.js
    ```


#### [API key](#tab/api-key)

1. Create the `from-audio.js` file with the following code:

    ```javascript 
    require("dotenv").config();
    const { AzureOpenAI } = require("openai");
    const fs = require('fs').promises;
    const { writeFileSync } = require("node:fs");
    
    // Set environment variables or edit the corresponding values here.
    const endpoint = process.env.AZURE_OPENAI_ENDPOINT || "AZURE_OPENAI_ENDPOINT";
    const apiKey = process.env.AZURE_OPENAI_API_KEY || "AZURE_OPENAI_API_KEY";
    const apiVersion = "2025-01-01-preview"; 
    const deployment = "gpt-4o-mini-audio-preview"; 
    
    const client = new AzureOpenAI({ 
        endpoint, 
        apiKey, 
        apiVersion, 
        deployment 
    });  
    
    async function main() {
        
        // Buffer the audio for input to the chat completion
        const wavBuffer = await fs.readFile("dog.wav"); 
        const base64str = Buffer.from(wavBuffer).toString("base64"); 
        
        // Make the audio chat completions request
        const response = await client.chat.completions.create({
            model: "gpt-4o-mini-audio-preview",
            modalities: ["text", "audio"],
            audio: { voice: "alloy", format: "wav" }, 
            messages: [
                {
                    role: "user",
                    content: [
                        { 
                            type: "text", 
                            text: "Describe in detail the spoken audio input." 
                        },
                        { 
                            type: "input_audio", 
                            input_audio: { 
                                data: base64str, 
                                format: "wav" 
                            } 
                        }
                    ]
                }
            ]
        });
        
        console.log(response.choices[0]); 
      
        // Write the output audio data to a file
        writeFileSync( 
            "analysis.wav", 
            Buffer.from(response.choices[0].message.audio.data, 'base64'), 
            { encoding: "utf-8" } 
        ); 
    }
    
    main().catch((err) => {
        console.error("Error occurred:", err);
    });
    
    module.exports = { main };
    ```

1. Run the JavaScript file.

    ```shell
    node from-audio.js
    ```

---

Wait a few moments to get the response.

### Output for audio and text generation from audio input

The script generates a transcript of the summary of the spoken audio input. It also generates an audio file named _analysis.wav_ in the same directory as the script. The audio file contains the spoken response to the prompt.

## Generate audio and use multi-turn chat completions

#### [Microsoft Entra ID](#tab/keyless)

1. Create the `multi-turn.js` file with the following code:

    ```javascript 
    require("dotenv").config();
    const { AzureOpenAI } = require("openai");
    const { DefaultAzureCredential, getBearerTokenProvider } = require("@azure/identity");
    const fs = require('fs').promises;
    
    // Keyless authentication    
    const credential = new DefaultAzureCredential();
    const scope = "https://cognitiveservices.azure.com/.default";
    const azureADTokenProvider = getBearerTokenProvider(credential, scope);
    
    // Set environment variables or edit the corresponding values here.
    const endpoint = process.env.AZURE_OPENAI_ENDPOINT || "AZURE_OPENAI_ENDPOINT";
    const apiVersion = "2025-01-01-preview"; 
    const deployment = "gpt-4o-mini-audio-preview"; 
    
    const client = new AzureOpenAI({ 
        endpoint, 
        azureADTokenProvider, 
        apiVersion, 
        deployment 
    }); 
    
    async function main() {
        
        // Buffer the audio for input to the chat completion
        const wavBuffer = await fs.readFile("dog.wav"); 
        const base64str = Buffer.from(wavBuffer).toString("base64"); 
        
        // Initialize messages with the first turn's user input 
        const messages = [
            {
                role: "user",
                content: [
                    { 
                        type: "text", 
                        text: "Describe in detail the spoken audio input." 
                    },
                    { 
                        type: "input_audio", 
                        input_audio: { 
                            data: base64str, 
                            format: "wav" 
                        } 
                    }
                ]
            }
        ];
        
        // Get the first turn's response 
    
        const response = await client.chat.completions.create({ 
            model: "gpt-4o-mini-audio-preview",
            modalities: ["text", "audio"], 
            audio: { voice: "alloy", format: "wav" }, 
            messages: messages
        }); 
        
        console.log(response.choices[0]); 
        
        // Add a history message referencing the previous turn's audio by ID 
        messages.push({ 
            role: "assistant", 
            audio: { id: response.choices[0].message.audio.id }
        });
    
        // Add a new user message for the second turn
        messages.push({ 
            role: "user", 
            content: [ 
                { 
                    type: "text", 
                    text: "Very concisely summarize the favorability." 
                } 
            ] 
        }); 
    
        // Send the follow-up request with the accumulated messages
        const followResponse = await client.chat.completions.create({ 
            model: "gpt-4o-mini-audio-preview",
            messages: messages
        });
    
        console.log(followResponse.choices[0].message.content); 
    }
    
    main().catch((err) => {
        console.error("Error occurred:", err);
    });
    
    module.exports = { main };
    ```

1. Sign in to Azure with the following command:

    ```shell
    az login
    ```

1. Run the JavaScript file.

    ```shell
    node multi-turn.js
    ```


#### [API key](#tab/api-key)

1. Create the `multi-turn.js` file with the following code:

    ```javascript 
    require("dotenv").config();
    const { AzureOpenAI } = require("openai");
    const fs = require('fs').promises;
    
    // Set environment variables or edit the corresponding values here.
    const endpoint = process.env.AZURE_OPENAI_ENDPOINT || "AZURE_OPENAI_ENDPOINT";
    const apiKey = process.env.AZURE_OPENAI_API_KEY || "AZURE_OPENAI_API_KEY";
    const apiVersion = "2025-01-01-preview"; 
    const deployment = "gpt-4o-mini-audio-preview"; 
    
    const client = new AzureOpenAI({ 
        endpoint, 
        apiKey, 
        apiVersion, 
        deployment 
    });  
    
    async function main() {
        
        // Buffer the audio for input to the chat completion
        const wavBuffer = await fs.readFile("dog.wav"); 
        const base64str = Buffer.from(wavBuffer).toString("base64"); 
        
        // Initialize messages with the first turn's user input 
        const messages = [
            {
                role: "user",
                content: [
                    { 
                        type: "text", 
                        text: "Describe in detail the spoken audio input." 
                    },
                    { 
                        type: "input_audio", 
                        input_audio: { 
                            data: base64str, 
                            format: "wav" 
                        } 
                    }
                ]
            }
        ];
        
        // Get the first turn's response 
    
        const response = await client.chat.completions.create({ 
            model: "gpt-4o-mini-audio-preview",
            modalities: ["text", "audio"], 
            audio: { voice: "alloy", format: "wav" }, 
            messages: messages
        }); 
        
        console.log(response.choices[0]); 
        
        // Add a history message referencing the previous turn's audio by ID 
        messages.push({ 
            role: "assistant", 
            audio: { id: response.choices[0].message.audio.id }
        });
    
        // Add a new user message for the second turn
        messages.push({ 
            role: "user", 
            content: [ 
                { 
                    type: "text", 
                    text: "Very concisely summarize the favorability." 
                } 
            ] 
        }); 
    
        // Send the follow-up request with the accumulated messages
        const followResponse = await client.chat.completions.create({ 
            model: "gpt-4o-mini-audio-preview",
            messages: messages
        });
    
        console.log(followResponse.choices[0].message.content); 
    }
    
    main().catch((err) => {
        console.error("Error occurred:", err);
    });
    
    module.exports = { main };
    ```

1. Run the JavaScript file.

    ```shell
    node multi-turn.js
    ```

---

Wait a few moments to get the response.

### Output for multi-turn chat completions

The script generates a transcript of the summary of the spoken audio input. Then, it makes a multi-turn chat completion to briefly summarize the spoken audio input. 