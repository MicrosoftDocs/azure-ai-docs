---
title: Add user consent to the personal voice project - Speech service
titleSuffix: Azure AI services
description: Learn about how to add user consent to the personal voice project.
author: eric-urban
manager: nitinme
ms.service: azure-ai-speech
ms.custom:
  - build-2024
ms.topic: how-to
ms.date: 9/20/2024
ms.author: eur
#Customer intent: As a developer, I want to learn how to add user consent to the personal voice project.
---

# Add user consent to the personal voice project

With the personal voice feature, it's required that every voice be created with explicit consent from the user. A recorded statement from the user is required acknowledging that the customer (Azure AI Speech resource owner) will create and use their voice.

To add user consent to the personal voice project, you provide the prerecorded consent audio file [from a publicly accessible URL](#add-consent-from-a-url) ([Consents_Create](/rest/api/aiservices/speechapi/consents/create)) or [upload the audio file](#add-consent-from-a-file) ([Consents_Post](/rest/api/aiservices/speechapi/consents/post)).  

## Consent statement

You need an audio recording of the user speaking the consent statement.

You can get the consent statement text for each locale from the text to speech GitHub repository. See [verbal-statement-all-locales.txt](https://github.com/Azure-Samples/Cognitive-Speech-TTS/blob/master/CustomVoice/script/verbal-statement-all-locales.txt) for the consent statement. Below is a sample for the `en-US` locale:

```
"I [state your first and last name] am aware that recordings of my voice will be used by [state the name of the company] to create and use a synthetic version of my voice."
```

### Supported audio formats for consent audio

See the table below for the supported formats for consent audio files:

| Format | Sample rate                  | Bit rate                    | Bit depth|
|------------|--------------------------|-------------------------|----------|
| mp3  | 16 kHz, 24 kHz, 44.1 kHz, 48 kHz       | 128 kbps, 192 kbps, 256 kbps, 320 kbps              | /                          |
| wav    | 16 kHz, 24 kHz, 44.1 kHz, 48 kHz       | /                                               | 16-bit, 24-bit, 32-bit      |

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
- Replace `YourResourceRegion` with your Speech resource region.
- Replace `JessicaConsentId` with a consent ID of your choice. The case sensitive ID will be used in the consent's URI and can't be changed later. 

```azurecli-interactive
curl -v -X POST -H "Ocp-Apim-Subscription-Key: YourResourceKey" -F 'description="Consent for Jessica voice"' -F 'projectId="ProjectId"' -F 'voiceTalentName="Jessica Smith"' -F 'companyName="Contoso"' -F 'audiodata=@"D:\PersonalVoiceTest\jessica-consent.wav"' -F 'locale="en-US"' "https://YourResourceRegion.api.cognitive.microsoft.com/customvoice/consents/JessicaConsentId?api-version=2024-02-01-preview"
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
Operation-Location: https://eastus.api.cognitive.microsoft.com/customvoice/operations/070f7986-ef17-41d0-ba2b-907f0f28e314?api-version=2024-02-01-preview
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
- Replace `YourResourceRegion` with your Speech resource region.
- Replace `JessicaConsentId` with a consent ID of your choice. The case sensitive ID will be used in the consent's URI and can't be changed later. 

```azurecli-interactive
curl -v -X PUT -H "Ocp-Apim-Subscription-Key: YourResourceKey" -H "Content-Type: application/json" -d '{
  "description": "Consent for Jessica voice",
  "projectId": "ProjectId",
  "voiceTalentName": "Jessica Smith",
  "companyName": "Contoso",
  "audioUrl": "https://contoso.blob.core.windows.net/public/jessica-consent.wav?mySasToken",
  "locale": "en-US"
} '  "https://YourResourceRegion.api.cognitive.microsoft.com/customvoice/consents/JessicaConsentId?api-version=2024-02-01-preview"
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
Operation-Location: https://eastus.api.cognitive.microsoft.com/customvoice/operations/070f7986-ef17-41d0-ba2b-907f0f28e314?api-version=2024-02-01-preview
Operation-Id: 070f7986-ef17-41d0-ba2b-907f0f28e314
```

## Next steps

> [!div class="nextstepaction"]
> [Create a personal voice.](./personal-voice-create-voice.md).
