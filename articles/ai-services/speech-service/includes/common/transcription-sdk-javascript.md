---
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 04/07/2026
ai-usage: ai-assisted
---

[Reference documentation](/javascript/api/overview/azure/ai-speech-transcription-readme) | [Package (npm)](https://www.npmjs.com/package/@azure/ai-speech-transcription) | [GitHub samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/transcription/ai-speech-transcription/samples)

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- [Node.js LTS](https://nodejs.org/).
- A [Microsoft Foundry resource](/azure/ai-services/multi-service-resource) created in one of the supported regions. For more information about region availability, see [Region support](/azure/ai-services/speech-service/regions?tabs=stt).
- A sample `.wav` audio file to transcribe.

### Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Sign in with Azure CLI by running `az login`.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Set up the project

1. Create a new folder and initialize a Node.js project:

    ```bash
    mkdir transcription-quickstart
    cd transcription-quickstart
    npm init -y
    ```

1. Install the required packages:

    ```bash
    npm install @azure/ai-speech-transcription @azure/identity
    ```

1. Configure the project to use ES modules by adding the module type to your `package.json`:

    ```bash
    npm pkg set type=module
    ```

    Or manually add `"type": "module"` to your `package.json` file. This is required for the `import` statements in the sample code to work.

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

    # [Linux](#tab/linux)

    ```bash
    export AZURE_SPEECH_ENDPOINT="<your-speech-endpoint>"
    ```

    # [macOS](#tab/macos)

    ```bash
    export AZURE_SPEECH_ENDPOINT="<your-speech-endpoint>"
    ```

    ---

## Transcribe audio

1. Create a file named `transcribe-audio-file.js` with the following code:

    ```javascript
    import { readFileSync } from "node:fs";
    import { DefaultAzureCredential } from "@azure/identity";
    import { TranscriptionClient } from "@azure/ai-speech-transcription";

    const endpoint = process.env.AZURE_SPEECH_ENDPOINT;
    if (!endpoint) {
      throw new Error("Set the AZURE_SPEECH_ENDPOINT environment variable.");
    }

    // Use DefaultAzureCredential for keyless authentication (recommended).
    const client = new TranscriptionClient(endpoint, new DefaultAzureCredential());

    const audioFile = readFileSync("<path-to-your-audio-file.wav>");

    const result = await client.transcribe(audioFile, {
      locales: ["en-US"],
    });

    console.log("Transcription:", result.combinedPhrases[0]?.text ?? "No text");
    ```

    Reference: [TranscriptionClient](/javascript/api/%40azure/ai-speech-transcription/transcriptionclient) | [DefaultAzureCredential](/javascript/api/%40azure/identity/defaultazurecredential)

1. Replace `<path-to-your-audio-file.wav>` with the path to your audio file.

1. Run the app:

    ```bash
    node transcribe-audio-file.js
    ```

## Output

The app prints the transcribed text to the console:

```output
Transcription: Hi there! This is a sample voice recording.
```

## Common request options

### Identify speakers with diarization

```javascript
const result = await client.transcribe(audioFile, {
  locales: ["en-US"],
  diarizationOptions: {
    maxSpeakers: 4,
  },
});

for (const phrase of result.phrases) {
  console.log(`Speaker ${phrase.speaker}: ${phrase.text}`);
}
```

Reference: [TranscriptionDiarizationOptions](/javascript/api/%40azure/ai-speech-transcription/transcriptiondiarizationoptions)

### Set profanity filtering

```javascript
import {
  KnownProfanityFilterModes,
} from "@azure/ai-speech-transcription";

const result = await client.transcribe(audioFile, {
  locales: ["en-US"],
  profanityFilterMode: KnownProfanityFilterModes.Masked,
});
```

Reference: [KnownProfanityFilterModes](/javascript/api/%40azure/ai-speech-transcription/knownprofanityfiltermodes)

### Add a phrase list

Use a phrase list to improve recognition for domain-specific terms, proper nouns, and acronyms:

```javascript
const result = await client.transcribe(audioFile, {
  locales: ["en-US"],
  phraseList: {
    phrases: ["Contoso", "Jessie", "Rehaan"],
  },
});

console.log("Transcription:", result.combinedPhrases[0]?.text ?? "No text");
```

Reference: [PhraseListProperties](/javascript/api/%40azure/ai-speech-transcription/phraselistproperties)

### Enable multi-language detection

When you're unsure which language is spoken, pass multiple locale candidates. The service detects the language and returns locale per phrase:

```javascript
const result = await client.transcribe(audioFile, {
  locales: ["en-US", "es-ES"],
});

for (const phrase of result.phrases) {
  console.log(`[${phrase.locale}] ${phrase.text}`);
}
```

Reference: [TranscribedPhrase](/javascript/api/%40azure/ai-speech-transcription/transcribedphrase)

