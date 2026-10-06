---
title: Create a personal voice - Speech service
titleSuffix: Foundry Tools
description: Learn how to create a personal voice and get the speaker profile ID used for text to speech.
author: PatrickFarley
manager: mcleans
ms.service: azure-speech-foundry-tools
ms.custom:
  - build-2024
ms.topic: how-to
ms.date: 09/04/2026
ms.author: pafarley
zone_pivot_groups: foundry-portal-rest
#Customer intent: As a developer, I want to create a personal voice for use in my application.
ai-usage: ai-assisted
---

# Create a personal voice

Create a personal voice from the voice talent's consent and a short audio prompt.

The speaker profile ID is based on the speaker's verbal consent statement and an audio prompt, which is a clean human voice sample between 5 and 90 seconds. The speaker's voice characteristics are encoded in the `speakerProfileId` property that's used for text to speech. For more information, see [Use personal voice in your application](./personal-voice-how-to-use.md).

## Prerequisites

- Add a voice talent whose consent has the **Succeeded** status.
- Prepare a clean audio sample of the same voice talent speaking naturally for 5–90 seconds.

## Prompt audio format

The supported formats for prompt audio files are:

| Format | Sample rate                  | Bit rate                    | Bit depth|
|------------|--------------------------|-------------------------|----------|
| mp3  | 16 kHz, 24 kHz, 44.1 kHz, 48 kHz       | 128 kbps, 192 kbps, 256 kbps, 320 kbps              | /                          |
| wav    | 16 kHz, 24 kHz, 44.1 kHz, 48 kHz       | /                                               | 16-bit, 24-bit, 32-bit      |

::: zone pivot="ai-foundry-portal"

# [Foundry (new)](#tab/foundry-new)

In Foundry (new), complete the personal voice customization and test the voice in the playground.

## Add personal voice training data

These steps continue from the **Customize a model** page you opened in [Set up a personal voice](./personal-voice-create-project.md?pivots=ai-foundry-portal&tabs=foundry-new) and continued in [Add user consent](./personal-voice-create-consent.md?pivots=ai-foundry-portal&tabs=foundry-new).

1. On the **Training data** step, select **New data**, and then select one of the following options:

   - **Upload data** to upload a prerecorded audio prompt.
   - **Record data** to record the audio prompt directly in the portal.

### Upload a prerecorded audio prompt

1. Select the audio file. The file must be a clean human voice sample between 5 and 90 seconds. The file appears in the **Data preview** section.

### Record an audio prompt in the portal

1. Read and follow the **Recording tips**:

   - **Avoid background noise**: Record in a quiet environment to minimize background noise for better audio quality.
   - **Stay relaxed**: Speak naturally and at a comfortable pace. Avoid rushing or over-enunciating.
   - **Use a quality microphone**: Use a headset or external microphone for best results. Avoid built-in laptop microphones.
   - **Review quality metrics**: After recording, review the quality scores to ensure your audio meets the required standards.

1. Select **Got it, start recording**.
1. Select **Start recording**, and record 5–90 seconds of natural speech in the style you want the voice to use.
1. Stop and review the recording, and then select **Done**. The recording appears in the **Data preview** section.

### Review and submit

After you upload or record an audio prompt, complete the customization steps:

1. Select **Next**.
1. On the **Review** step, review the basic details, voice talent, and training data.

   :::image type="content" source="./media/personal-voice/foundry-new-personal-voice-review.png" alt-text="Screenshot of the Personal Voice Review step in Foundry with the usage and terms acknowledgments outlined and customization details in Data preview." lightbox="./media/personal-voice/foundry-new-personal-voice-review.png":::

1. Select the acknowledgment that training incurs account usage.
1. Select the acknowledgment to agree to the terms of use.
1. Select **Submit**.

## Test your personal voice

After the customization succeeds, you can try your personal voice in the text-to-speech playground. You don't need a separate deployment.

1. Select **Build** from the upper-right menu.
1. In the left pane, select **Services**, and then select the **Customizations** tab.
1. After the personal voice customization task has the **Succeeded** status, select its name.
1. Select **Open in Playground** > **Text to Speech** in the upper right.
1. Confirm that your personal voice is selected under **Voice**, and wait for the **Base model** to load.
1. Enter text, and then select **Play** to synthesize speech with the personal voice.
1. Optionally, select **Download** to save the generated audio.

:::image type="content" source="./media/personal-voice/foundry-new-personal-voice-playground.png" alt-text="Screenshot of the Foundry text to speech playground with Voice, Base model, Play, and Download outlined." lightbox="./media/personal-voice/foundry-new-personal-voice-playground.png":::

To work with SSML, select **Input mode** > **SSML**. The generated SSML uses a base model name in the `voice` element and your speaker profile ID in the `mstts:ttsembedding` element.

### Use the voice in your application

The customization details page shows **Profile ID** under **Model attributes**. Use this value as `speakerProfileId` in SSML. The **Voice name** you entered during setup identifies your customization; don't substitute it for the base model name in the SSML `voice` element.

:::image type="content" source="./media/personal-voice/foundry-new-personal-voice-details.png" alt-text="Screenshot of succeeded Personal Voice details in Foundry with Profile ID and deployment readiness outlined." lightbox="./media/personal-voice/foundry-new-personal-voice-details.png":::

Select **Call service** in the playground to view sample code for the current configuration. For Speech SDK and REST integration, see [Use personal voice in your application](./personal-voice-how-to-use.md).

# [Foundry (classic)](#tab/foundry-classic)

## Add a voice training dataset

These steps continue from the **Fine-tune a model** wizard you opened in [Create a personal voice project](./personal-voice-create-project.md?pivots=ai-foundry-portal&tabs=foundry-classic) and continued in [Add user consent](./personal-voice-create-consent.md?pivots=ai-foundry-portal&tabs=foundry-classic).

1. On the **Training data** pane of the wizard, select one of the following options:

   - **Upload data** to upload a prerecorded audio prompt.
   - **Record data** to record the audio prompt directly in the portal.

### Upload a prerecorded audio prompt

1. In the **Upload data** pane, drag and drop the audio file into the upload area, or select **Browse for a file** to select it. The file must be a clean human voice sample between 5 and 90 seconds.
1. Select **Upload**.

### Record an audio prompt in the portal

1. In the **Record data** pane, read and follow the recording tips:

   - **Avoid background noise**: Record in a quiet environment to minimize background noise for better audio quality.
   - **Stay relaxed**: Speak naturally and at a comfortable pace. Avoid rushing or over-enunciating.
   - **Use a quality microphone**: Use a headset or external microphone for best results. Avoid built-in laptop microphones.
   - **Review quality metrics**: After recording, review the quality scores to ensure your audio meets the required standards.

1. Press the microphone button to start recording 5–90 seconds of audio.
1. Stop the recording, review it, and then select **Next** to submit.

## Test your personal voice

After the training data is processed, you can try out your personal voice in the **Playground**:

1. Select **Fine-tuning** from the left pane, and then select the **AI Service** tab.
1. Select the personal voice fine-tuning task you submitted.
1. Select **Open in Playground** in the upper right.
1. Enter plain text or SSML to synthesize speech with the personal voice.

To integrate personal voice in your application by using the `speakerProfileId`, see [Use personal voice in your application](./personal-voice-how-to-use.md).

---

::: zone-end

::: zone pivot="rest-api"

The custom voice REST API returns the `speakerProfileId` that you use to synthesize speech in an application.

> [!NOTE]
> The personal voice ID and speaker profile ID aren't the same. You choose the personal voice ID, but the service generates the speaker profile ID. Use the personal voice ID to manage the personal voice. Use the speaker profile ID for text to speech.

You provide the audio files [from a publicly accessible URL](#create-personal-voice-from-a-url) ([PersonalVoices_Create](/rest/api/aiservices/speechapi/personal-voices/create)) or [upload the audio files](#create-personal-voice-from-a-file) ([PersonalVoices_Post](/rest/api/aiservices/speechapi/personal-voices/post)).  

## Create personal voice from a file

In this scenario, the audio files must be available locally. 

To create a personal voice and get the speaker profile ID, use the [PersonalVoices_Post](/rest/api/aiservices/speechapi/personal-voices/post) operation of the custom voice API. Construct the request body according to the following instructions:

- Set the required `projectId` property. See [create a project](./personal-voice-create-project.md?pivots=rest-api).
- Set the required `consentId` property. See [add user consent](./personal-voice-create-consent.md?pivots=rest-api).
- Set the required `audiodata` property. You can specify one or more audio files in the same request. The maximum file size is 30 MB.

Make an HTTP POST request using the URI as shown in the following [PersonalVoices_Post](/rest/api/aiservices/speechapi/personal-voices/post) example. 
- Replace `YourResourceKey` with your Speech resource key.
- Replace `YourResourceName` with your Speech resource name. 
- Replace `JessicaPersonalVoiceId` with a personal voice ID of your choice. The case sensitive ID will be used in the personal voice's URI and can't be changed later. 

```azurecli-interactive
curl -v -X POST -H "Ocp-Apim-Subscription-Key: YourResourceKey" -F 'projectId="ProjectId"' -F 'consentId="JessicaConsentId"' -F 'audiodata=@"D:\PersonalVoiceTest\CNVSample001.wav"' -F 'audiodata=@"D:\PersonalVoiceTest\CNVSample002.wav"' "https://YourResourceName.cognitiveservices.azure.com/customvoice/personalvoices/JessicaPersonalVoiceId?api-version=2026-01-01"
```

You should receive a response body in the following format:

```json
{
  "id": "JessicaPersonalVoiceId",
  "speakerProfileId": "3059912f-a3dc-49e3-bdd0-02e449df1fe3",
  "projectId": "ProjectId",
  "consentId": "JessicaConsentId",
  "status": "NotStarted",
  "createdDateTime": "2024-09-01T05:30:00.000Z",
  "lastActionDateTime": "2024-09-02T10:15:30.000Z"
}
```

Use the `speakerProfileId` property to integrate personal voice in your text to speech application. For more information, see [use personal voice in your application](./personal-voice-how-to-use.md).

The response header contains the `Operation-Location` property. Use this URI to get details about the [PersonalVoices_Post](/rest/api/aiservices/speechapi/personal-voices/post) operation. Here's an example of the response header:

```HTTP 201
Operation-Location: https://YourResourceName.cognitiveservices.azure.com/customvoice/operations/1321a2c0-9be4-471d-83bb-bc3be4f96a6f?api-version=2026-01-01
Operation-Id: 1321a2c0-9be4-471d-83bb-bc3be4f96a6f
```

## Create personal voice from a URL

In this scenario, the audio files must already be stored in an Azure Blob Storage container. 

To create a personal voice and get the speaker profile ID, use the [PersonalVoices_Create](/rest/api/aiservices/speechapi/personal-voices/create) operation of the custom voice API. Construct the request body according to the following instructions:

- Set the required `projectId` property. See [create a project](./personal-voice-create-project.md?pivots=rest-api).
- Set the required `consentId` property. See [add user consent](./personal-voice-create-consent.md?pivots=rest-api).
- Set the required `audios` property. Within the `audios` property, set the following properties:
  - Set the required `containerUrl` property to the URL of the Azure Blob Storage container that contains the audio files. Use [shared access signatures (SAS) for a container](/azure/storage/blobs/sas-service-create-dotnet-container#create-a-service-sas-for-a-container) with both read and list permissions. 
  - Set the required `extensions` property to the extensions of the audio files. 
  - Optionally, set the `prefix` property to set a prefix for the blob name.

Make an HTTP PUT request using the URI as shown in the following [PersonalVoices_Create](/rest/api/aiservices/speechapi/personal-voices/create) example. 
- Replace `YourResourceKey` with your Speech resource key.
- Replace `YourResourceName` with your Speech resource name. 
- Replace `JessicaPersonalVoiceId` with a personal voice ID of your choice. The case sensitive ID will be used in the personal voice's URI and can't be changed later. 

```azurecli-interactive
curl -v -X PUT -H "Ocp-Apim-Subscription-Key: YourResourceKey" -H "Content-Type: application/json" -d '{
  "projectId": "ProjectId",
  "consentId": "JessicaConsentId",
  "audios": {
    "containerUrl": "https://contoso.blob.core.windows.net/voicecontainer?mySasToken",
    "prefix": "jessica/", 
    "extensions": [
      ".wav"
    ]
  }
} '  "https://YourResourceName.cognitiveservices.azure.com/customvoice/personalvoices/JessicaPersonalVoiceId?api-version=2026-01-01"

# Ensure the `containerUrl` has both read and list permissions. 
# Ensure the `.wav` files are located in the "jessica" folder within the container. The `prefix` matches all `.wav` files in the "jessica" folder. If there is no such folder, the prefix will match `.wav` files with names starting with "jessica". 
```

You should receive a response body in the following format:

```json
{
  "id": "JessicaPersonalVoiceId",
  "speakerProfileId": "3059912f-a3dc-49e3-bdd0-02e449df1fe3",
  "projectId": "ProjectId",
  "consentId": "JessicaConsentId",
  "status": "NotStarted",
  "createdDateTime": "2024-09-01T05:30:00.000Z",
  "lastActionDateTime": "2024-09-02T10:15:30.000Z"
}
```

Use the `speakerProfileId` property to integrate personal voice in your text to speech application. For more information, see [use personal voice in your application](./personal-voice-how-to-use.md).

The response header contains the `Operation-Location` property. Use this URI to get details about the [PersonalVoices_Create](/rest/api/aiservices/speechapi/personal-voices/create) operation. Here's an example of the response header:

```HTTP 201
Operation-Location: https://YourResourceName.cognitiveservices.azure.com/customvoice/operations/1321a2c0-9be4-471d-83bb-bc3be4f96a6f?api-version=2026-01-01
Operation-Id: 1321a2c0-9be4-471d-83bb-bc3be4f96a6f
```

::: zone-end

## Next steps

> [!div class="nextstepaction"]
> [Use personal voice in your application.](./personal-voice-how-to-use.md).
