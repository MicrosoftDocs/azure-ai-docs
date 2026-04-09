---
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 04/09/2026
ai-usage: ai-assisted
---

[Reference documentation](/javascript/api/@azure/ai-speech-transcription?view=azure-node-preview) | [Package (npm)](https://www.npmjs.com/package/@azure/ai-speech-transcription) | [GitHub samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/transcription/ai-speech-transcription/samples)

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- [Node.js LTS](https://nodejs.org/) installed.
- A [Microsoft Foundry resource](/azure/ai-services/multi-service-resource) created in one of the supported regions. For more information about region availability, see [Region support](/azure/ai-services/speech-service/regions?tabs=stt).
- A sample `.wav` audio file to transcribe.

### Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Sign in with the Azure CLI by running `az login`.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Set up the project

1. Create a new folder named `llm-speech-quickstart` and go to the folder:

    ```shell
    mkdir llm-speech-quickstart && cd llm-speech-quickstart
    ```

1. Initialize a Node.js project and install the required packages:

    ```shell
    npm init -y
    npm install @azure/ai-speech-transcription @azure/identity
    ```

## Retrieve resource information

You need to retrieve your resource endpoint for authentication.

1. Sign in to [Foundry portal](https://ai.azure.com).
1. Select **Management center** from the left menu. Under **Connected resources**, select your Speech or multi-service resource.
1. Select **Keys and Endpoint**.
1. Copy the **Endpoint** value and set it as an environment variable:

    # [Windows](#tab/windows)

    ```powershell
    $env:AZURE_SPEECH_ENDPOINT="<your-speech-endpoint>"
    ```

    # [Linux/macOS](#tab/linux-macos)

    ```bash
    export AZURE_SPEECH_ENDPOINT="<your-speech-endpoint>"
    ```

    ---

## Transcribe audio with LLM speech

LLM speech uses the `enhancedMode` option to enable large-language-model-enhanced transcription. The model automatically detects the language in your audio.

Create a file named `index.js` with the following code:

```javascript
const {
  TranscriptionClient,
} = require("@azure/ai-speech-transcription");
const { DefaultAzureCredential } = require("@azure/identity");
const fs = require("fs");

async function main() {
  const endpoint = process.env.AZURE_SPEECH_ENDPOINT;
  if (!endpoint) {
    throw new Error(
      "Set the AZURE_SPEECH_ENDPOINT environment variable."
    );
  }

  // Use DefaultAzureCredential for keyless authentication
  // (recommended). To use an API key instead, replace with:
  // const { AzureKeyCredential } = require("@azure/core-auth");
  // const credential = new AzureKeyCredential("<your-api-key>");
  const credential = new DefaultAzureCredential();
  const client = new TranscriptionClient(endpoint, credential);

  const audioFilePath = "<path-to-your-audio-file.wav>";
  const audioFile = fs.readFileSync(audioFilePath);

  // Use enhancedMode for LLM speech transcription
  const result = await client.transcribe(audioFile, {
    enhancedMode: {
      task: "transcribe",
    },
  });

  // Print the combined transcription text
  console.log("Transcription:", result.combinedPhrases[0]?.text);

  // Print detailed phrase information
  for (const phrase of result.phrases) {
    console.log(
      `  [${phrase.offsetMilliseconds}ms]`
        + ` (${phrase.locale}): ${phrase.text}`
    );
  }
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
  process.exit(1);
});
```

Replace `<path-to-your-audio-file.wav>` with the path to your audio file. The service supports WAV, MP3, FLAC, OGG, and other common audio formats.

Run the application:

```shell
node index.js
```

Reference: [`TranscriptionClient`](/javascript/api/@azure/ai-speech-transcription/transcriptionclient?view=azure-node-preview)

### Output

The application prints the transcription result to the console:

```console
Transcription: Hi there. This is a sample voice recording created for speech synthesis testing. The quick brown fox jumps over the lazy dog. Just a fun way to include every letter of the alphabet. Numbers, like one, two, three, are spoken clearly. Let's see how well this voice captures tone, timing, and natural rhythm. This audio is provided by samplefiles.com.
  [40ms] (en-US): Hi there.
  [800ms] (en-US): This is a sample voice recording created for speech synthesis testing.
  [5440ms] (en-US): The quick brown fox jumps over the lazy dog.
  [9040ms] (en-US): Just a fun way to include every letter of the alphabet.
  [12720ms] (en-US): Numbers, like one, two, three, are spoken clearly.
  [17200ms] (en-US): Let's see how well this voice captures tone, timing, and natural rhythm.
  [22480ms] (en-US): This audio is provided by samplefiles.com.
```

## Translate audio with LLM speech

You can also use LLM speech to translate audio to a target language. Set `task` to `translate` and specify the `targetLanguage`:

```javascript
const {
  TranscriptionClient,
} = require("@azure/ai-speech-transcription");
const { DefaultAzureCredential } = require("@azure/identity");
const fs = require("fs");

async function main() {
  const endpoint = process.env.AZURE_SPEECH_ENDPOINT;
  if (!endpoint) {
    throw new Error(
      "Set the AZURE_SPEECH_ENDPOINT environment variable."
    );
  }

  const credential = new DefaultAzureCredential();
  const client = new TranscriptionClient(endpoint, credential);

  const audioFilePath = "<path-to-your-audio-file.wav>";
  const audioFile = fs.readFileSync(audioFilePath);

  // Translate audio using enhanced mode
  const result = await client.transcribe(audioFile, {
    enhancedMode: {
      task: "translate",
      targetLanguage: "de", // Translate to German
    },
  });

  console.log("Translation:", result.combinedPhrases[0]?.text);
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
  process.exit(1);
});
```

Replace `<path-to-your-audio-file.wav>` with the path to your audio file.

Reference: [`TranscriptionClient`](/javascript/api/@azure/ai-speech-transcription/transcriptionclient?view=azure-node-preview)

## Use prompt-tuning

You can provide an optional prompt to guide the output style for transcription or translation tasks:

```javascript
const result = await client.transcribe(audioFile, {
  enhancedMode: {
    task: "transcribe",
    prompt: ["Output must be in lexical format."],
  },
});

console.log("Transcription:", result.combinedPhrases[0]?.text);
```

### Best practices for prompts

### Output

The application prints the transcription result to the console:

```console
Transcription: Hello this is a test of the LLM speech transcription service.
```

- Prompts are subject to a maximum length of 4,096 characters.
- Prompts should preferably be written in English.
- Use `Output must be in lexical format.` to enforce lexical formatting instead of the default display format.
- Use `Pay attention to *phrase1*, *phrase2*, …` to improve recognition of specific phrases or acronyms.

Reference: [`TranscriptionClient`](/javascript/api/@azure/ai-speech-transcription/transcriptionclient?view=azure-node-preview)

## Clean up resources

When you finish the quickstart, delete the project folder:

```shell
rm -rf llm-speech-quickstart
```
