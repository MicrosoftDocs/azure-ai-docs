---
title: include file
description: include file
author: eric-urban
ms.author: eur
ms.service: azure-ai-speech
ms.topic: include
ms.date: 12/1/2023
ms.custom: include
---

With the professional voice feature, it's required that every voice be created with explicit consent from the user. A recorded statement from the user is required acknowledging that the customer (Azure AI Speech resource owner) will create and use their voice.

To add voice talent consent to the professional voice project, you get the prerecorded consent audio file from a publicly accessible URL ([Consents_Create](/rest/api/aiservices/speechapi/consents/create)) or upload the audio file ([Consents_Post](/rest/api/aiservices/speechapi/consents/post)). In this article, you add consent from a URL. 

## Consent statement

You need an audio recording of the user speaking the consent statement.

You can get the consent statement text for each locale from the text to speech GitHub repository. See [SpeakerAuthorization.txt](https://github.com/Azure-Samples/Cognitive-Speech-TTS/blob/master/CustomVoice/script/English%20(United%20States)_en-US/SpeakerAuthorization.txt) for the consent statement for the `en-US` locale:

```
"I  [state your first and last name] am aware that recordings of my voice will be used by [state the name of the company] to create and use a synthetic version of my voice."
```

## Add consent from a URL

To add consent to a professional voice project from the URL of an audio file, use the [Consents_Create](/rest/api/aiservices/speechapi/consents/create) operation of the custom voice API. Construct the request body according to the following instructions:

- Set the required `projectId` property. See [create a project](../../../../professional-voice-create-project.md).
- Set the required `voiceTalentName` property. The voice talent name must be the name of the person who recorded the consent statement. Enter the name in the same language used in the recorded statement. The voice talent name can't be changed later.
- Set the required `companyName` property. The company name must match the company name spoken in the recorded statement. Ensure the company name is entered in the same language as the recorded statement. The company name can't be changed later. 
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
  "createdDateTime": "2023-04-01T05:30:00.000Z",
  "lastActionDateTime": "2023-04-02T10:15:30.000Z"
}
```

The response header contains the `Operation-Location` property. Use this URI to get details about the [Consents_Create](/rest/api/aiservices/speechapi/consents/create) operation. Here's an example of the response header:

```HTTP 201
Operation-Location: https://eastus.api.cognitive.microsoft.com/customvoice/operations/070f7986-ef17-41d0-ba2b-907f0f28e314?api-version=2024-02-01-preview
Operation-Id: 070f7986-ef17-41d0-ba2b-907f0f28e314
```


## Next steps

> [!div class="nextstepaction"]
> [Add training data to the professional voice project](../../../../professional-voice-create-training-set.md)

