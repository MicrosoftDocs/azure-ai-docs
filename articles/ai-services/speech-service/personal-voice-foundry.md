---
title: Create personal voice in Microsoft Foundry
titleSuffix: Azure AI Speech
description: Learn how to create a personal voice in Microsoft Foundry, including setting up fine-tuning, adding voice talent consent, adding a training dataset, and testing your voice.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 05/19/2026
ms.author: pafarley
ai-usage: ai-assisted
---

# Create personal voice in Microsoft Foundry

This article walks through the end-to-end process for creating a personal voice in Microsoft Foundry. You create a fine-tuning project, register voice talent consent, add a training dataset to get a speaker profile ID, and then test and use the voice in your application.

## Create a personal voice project

### Start fine-tuning

1. Go to your Foundry project.
1. Select **Fine-tuning**.
1. Select the **AI Service** tab, then select **Fine-tune**.
1. In the wizard, select **Azure Speech – Text to Speech**.
1. Select **Personal voice** as the type.
1. Follow the wizard to complete the setup.

## Add voice talent consent

A *voice talent* is the individual whose voice is being recorded. Before fine-tuning, you must submit a consent statement recording from the voice talent.

> [!TIP]
> Define a voice persona and choose the right voice talent before you start. See [Choose your voice talent](./record-custom-voice-samples.md#choose-your-voice-talent).

You can get the consent statement text for each locale from the GitHub repository: [verbal-statement-all-locales.txt](https://github.com/Azure-Samples/Cognitive-Speech-TTS/blob/master/CustomVoice/script/verbal-statement-all-locales.txt). The following example shows the `en-US` statement:

```
"I [state your first and last name] am aware that recordings of my voice will be used by [state the name of the company] to create and use a synthetic version of my voice."
```

For disclosure requirements, see [Disclosure for voice talent](/legal/cognitive-services/speech-service/disclosure-voice-talent).

> [!TIP]
> Sample consent audio and training data are available on GitHub: [CustomVoice/Sample Data](https://github.com/Azure-Samples/Cognitive-Speech-TTS/tree/master/CustomVoice/Sample%20Data).

### Add voice talent

1. Sign in to the [Microsoft Foundry portal](https://ai.azure.com).
1. Select **Fine-tuning**, then select the **AI Service** tab.
1. Select your personal voice fine-tuning job.
1. Go to **Register voice talent**. Select an existing voice talent entry, or select **+ New data** to add one.
1. On the **Upload verbal statement** page, follow the instructions:
   - Enter the voice talent name and the company name. The company name must match the name spoken in the recorded statement.
   - Ensure the company name is entered in the same language as the recorded statement.
   - Select the language that matches the recording.
1. Select **Done**.

After the voice talent status shows *Succeeded*, you can add fine-tuning data.

## Add a voice training dataset

To use personal voice in your application, you need a speaker profile ID. You create the speaker profile ID from the voice talent's verbal consent statement and an audio prompt — a clean human voice sample between 5 and 90 seconds. The user's voice characteristics are encoded in the `speakerProfileId` property that's used for text to speech. For more information, see [Use personal voice in your application](./personal-voice-how-to-use.md).

You provide the audio by uploading a file or recording directly in the portal.

### Prompt audio format

The supported formats for prompt audio files are:

| Format | Sample rate | Bit rate | Bit depth |
|--------|-------------|----------|-----------|
| mp3 | 16 kHz, 24 kHz, 44.1 kHz, 48 kHz | 128 kbps, 192 kbps, 256 kbps, 320 kbps | / |
| wav | 16 kHz, 24 kHz, 44.1 kHz, 48 kHz | / | 16-bit, 24-bit, 32-bit |

### Record audio data

1. Select **Record data**.
1. Read and follow the **Recording tips**:
   - **Avoid background noise**: Record in a quiet environment to minimize background noise for better audio quality.
   - **Stay relaxed**: Speak naturally and at a comfortable pace. Avoid rushing or over-enunciating.
   - **Use a quality microphone**: Use a headset or external microphone for best results. Avoid built-in laptop microphones.
   - **Review quality metrics**: After recording, review the quality scores to ensure your audio meets the required standards.
1. Press the microphone button to start recording 5–90 seconds of audio, then select **Next** and submit.

## Use personal voice in your application

### Try out in the TTS playground

1. Select **Fine-tuning** from the left pane, then select the **AI Service** tab.
1. Select the personal voice fine-tuning job you submitted.
1. Select **Open in Playground** in the upper right.
1. Enter plain text or SSML to try out the voice.

### Use in Voice Live Agent

[TO VERIFY] Documentation for using personal voice in Voice Live Agent is pending portal availability. In the meantime, see [Integrate personal voice in your application](./personal-voice-how-to-use.md).
