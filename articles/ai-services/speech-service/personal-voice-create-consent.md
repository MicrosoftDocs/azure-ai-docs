---
title: Add user consent to the personal voice project - Speech service
titleSuffix: Foundry Tools
description: Learn about how to add user consent to the personal voice project.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-speech
ms.custom:
  - build-2024
ms.topic: how-to
ms.date: 05/22/2026
ms.author: pafarley
zone_pivot_groups: foundry-portal-rest
#Customer intent: As a developer, I want to learn how to add user consent to the personal voice project.
ai-usage: ai-assisted
---

# Add user consent to the personal voice project

A voice talent is the individual or target speaker whose voice is recorded and used to create personal voice profiles. With the personal voice feature, every voice must be created with explicit consent from the voice talent. A recorded statement from the voice talent is required acknowledging that the customer (Azure Speech in Foundry Tools resource owner) creates and uses their voice. The consent statement is also used to verify that the voice talent is the same person as the speaker in the fine-tuning data.

> [!TIP]
> Before you get started, learn how to [define and record your voice samples](./record-custom-voice-samples.md). See also the [responsible AI disclosure for voice talent](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/disclosure-voice-talent).

## Consent statement

You need an audio recording of the voice talent speaking the consent statement. The language of the verbal statement must match the language of your training data.

You can get the consent statement text for each locale from the text to speech GitHub repository. See [verbal-statement-all-locales.txt](https://github.com/Azure-Samples/Cognitive-Speech-TTS/blob/master/CustomVoice/script/verbal-statement-all-locales.txt) for the consent statement. The following example is for the `en-US` locale:

```
"I [state your first and last name] am aware that recordings of my voice will be used by [state the name of the company] to create and use a synthetic version of my voice."
```

> [!TIP]
> For a sample consent statement and training data, see the [Custom Voice sample data](https://github.com/Azure-Samples/Cognitive-Speech-TTS/tree/master/CustomVoice/Sample%20Data) on GitHub.

### Supported audio formats for consent audio

See the following table for the supported formats for consent audio files:

| Format | Sample rate                  | Bit rate                    | Bit depth|
|------------|--------------------------|-------------------------|----------|
| mp3  | 16 kHz, 24 kHz, 44.1 kHz, 48 kHz       | 128 kbps, 192 kbps, 256 kbps, 320 kbps              | /                          |
| wav    | 16 kHz, 24 kHz, 44.1 kHz, 48 kHz       | /                                               | 16-bit, 24-bit, 32-bit      |

::: zone pivot="ai-foundry-portal"

## Add voice talent consent

These steps continue from the **Fine-tune a model** wizard you opened in [Create a personal voice project](./personal-voice-create-project.md).

1. On the **Register voice talent** pane of the wizard, select an existing voice talent, or select **+ New data** to add a new one. When you add new data, select one of the following options:

   - **Upload data** to upload a prerecorded consent statement audio file.
   - **Record data** to record the consent statement directly in the portal.

### Upload a prerecorded consent statement

1. In the **Upload data** pane, provide the verbal consent statement:

   - Select the **Language** of the recorded statement.
   - Enter the **Voice talent name**. The name must match the person who recorded the consent statement, in the same language used in the recording.
   - Enter the **Company name**. The company name must match what was spoken in the recording, in the same language.
   - Drag and drop the audio file into the upload area, or select **Browse for a file** to select it.

1. Select **Upload**.

### Record a consent statement in the portal

1. In the **Record data** pane, provide the voice talent details:

   - Select the **Language** of the consent statement.
   - Enter the **Voice talent name** and **Company name** as the voice talent says them in the recording.

1. Read and follow the recording tips:

   - **Avoid background noise**: Record in a quiet environment to minimize background noise for better audio quality.
   - **Stay relaxed**: Speak naturally and at a comfortable pace. Avoid rushing or over-enunciating.
   - **Use a quality microphone**: Use a headset or external microphone for best results. Avoid built-in laptop microphones.

1. Have the voice talent read the on-screen consent statement aloud.
1. Press the microphone button to start recording. Have the voice talent read the consent statement, then stop the recording.
1. Review the recording and submit it.

After you add the voice talent and the status is **Succeeded**, select them on the **Register voice talent** pane, and then select **Next** to continue to the **Training data** step in [Get a speaker profile ID](./personal-voice-create-voice.md).

::: zone-end

::: zone pivot="rest-api"

To add user consent to the personal voice project, you provide the prerecorded consent audio file [from a publicly accessible URL](#add-consent-from-a-url) ([Consents_Create](/rest/api/aiservices/speechapi/consents/create)) or [upload the audio file](#add-consent-from-a-file) ([Consents_Post](/rest/api/aiservices/speechapi/consents/post)).

## Add consent from a file

In this scenario, the audio files must be available locally. 

To add consent to a personal voice project from a local audio file, use the `Consents_Post` operation of the custom voice API. Construct the request body according to the following instructions:

- Set the required `projectId` property. See [create a project](./personal-voice-create-project.md).
- Set the required `voiceTalentName` property. The voice talent name can't be changed later.
- Set the required `companyName` property. The company name can't be changed later.
- Set the required `audiodata` property with the consent audio file. 
- Set the required `locale` property. This should be the locale of the consent. The locale can't be changed later. You can find the text to speech locale list [here](/azure/ai-services/speech-service/language-support?tabs=tts).

Make an HTTP POST request using the URI as shown in the following `Consents_Post` example. 
- Replace `YourResourceKey` with your Speech resource key.
- Replace `YourResourceName` with your Speech resource name.
- Replace `JessicaConsentId` with a consent ID of your choice. The case sensitive ID will be used in the consent's URI and can't be changed later. 

```azurecli-interactive
curl -v -X POST -H "Ocp-Apim-Subscription-Key: YourResourceKey" -F 'description="Consent for Jessica voice"' -F 'projectId="ProjectId"' -F 'voiceTalentName="Jessica Smith"' -F 'companyName="Contoso"' -F 'audiodata=@"D:\PersonalVoiceTest\jessica-consent.wav"' -F 'locale="en-US"' "https://YourResourceName.cognitiveservices.azure.com/customvoice/consents/JessicaConsentId?api-version=2026-01-01"
```

You should receive a response body in the following format:

```json
{
  "id": "JessicaConsentId",
  "description": "Consent for Jessica voice",
  "projectId": "ProjectId",
  "voiceTalentName": "Jessica Smith",
  "companyName": "Contoso",
  "locale": "en-US",
  "status": "NotStarted",
  "createdDateTime": "2024-09-01T05:30:00.000Z",
  "lastActionDateTime": "2024-09-02T10:15:30.000Z"
}
```

The response header contains the `Operation-Location` property. Use this URI to get details about the `Consents_Post` operation. Here's an example of the response header:

```HTTP 201
Operation-Location: https://YourResourceName.cognitiveservices.azure.com/customvoice/operations/070f7986-ef17-41d0-ba2b-907f0f28e314?api-version=2026-01-01
Operation-Id: 070f7986-ef17-41d0-ba2b-907f0f28e314
```

## Add consent from a URL

In this scenario, the audio files must already be stored in an Azure Blob Storage container. 

To add consent to a personal voice project from the URL of an audio file, use the [Consents_Create](/rest/api/aiservices/speechapi/consents/create) operation of the custom voice API. Construct the request body according to the following instructions:

- Set the required `projectId` property. See [create a project](./personal-voice-create-project.md).
- Set the required `voiceTalentName` property. The voice talent name can't be changed later.
- Set the required `companyName` property. The company name can't be changed later.
- Set the required `audioUrl` property. The URL of the voice talent consent audio file. Use a URI with the [shared access signatures (SAS)](/azure/storage/common/storage-sas-overview) token.
- Set the required `locale` property. This should be the locale of the consent. The locale can't be changed later. You can find the text to speech locale list [here](/azure/ai-services/speech-service/language-support?tabs=tts).

Make an HTTP PUT request using the URI as shown in the following [Consents_Create](/rest/api/aiservices/speechapi/consents/create) example. 
- Replace `YourResourceKey` with your Speech resource key.
- Replace `YourResourceName` with your Speech resource name.
- Replace `JessicaConsentId` with a consent ID of your choice. The case sensitive ID will be used in the consent's URI and can't be changed later. 

```azurecli-interactive
curl -v -X PUT -H "Ocp-Apim-Subscription-Key: YourResourceKey" -H "Content-Type: application/json" -d '{
  "description": "Consent for Jessica voice",
  "projectId": "ProjectId",
  "voiceTalentName": "Jessica Smith",
  "companyName": "Contoso",
  "audioUrl": "https://contoso.blob.core.windows.net/public/jessica-consent.wav?mySasToken",
  "locale": "en-US"
} '  "https://YourResourceName.cognitiveservices.azure.com/customvoice/consents/JessicaConsentId?api-version=2026-01-01"
```

You should receive a response body in the following format:

```json
{
  "id": "JessicaConsentId",
  "description": "Consent for Jessica voice",
  "projectId": "ProjectId",
  "voiceTalentName": "Jessica Smith",
  "companyName": "Contoso",
  "locale": "en-US",
  "status": "NotStarted",
  "createdDateTime": "2024-09-01T05:30:00.000Z",
  "lastActionDateTime": "2024-09-02T10:15:30.000Z"
}
```

The response header contains the `Operation-Location` property. Use this URI to get details about the [Consents_Create](/rest/api/aiservices/speechapi/consents/create) operation. Here's an example of the response header:

```HTTP 201
Operation-Location: https://YourResourceName.cognitiveservices.azure.com/customvoice/operations/070f7986-ef17-41d0-ba2b-907f0f28e314?api-version=2026-01-01
Operation-Id: 070f7986-ef17-41d0-ba2b-907f0f28e314
```

::: zone-end

## Next steps

> [!div class="nextstepaction"]
> [Create a personal voice.](./personal-voice-create-voice.md).
