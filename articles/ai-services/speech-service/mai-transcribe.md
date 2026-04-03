---
title: MAI-Transcribe-1 in LLM Speech API - Speech service
titleSuffix: Foundry Tools
description: Learn how to use MAI-Transcribe-1 model in Azure Speech LLM Speech API
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 04/01/2026
# Customer intent: As a user who implements audio transcription, I want create transcriptions with MAI's latest mai-transcribe-1 model.
---

# MAI-Transcribe-1 in Azure Speech (preview)

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

MAI‑Transcribe‑1 is a speech recognition model developed by the Microsoft AI (MAI) Superintelligence team with a dual focus: high accuracy and high efficiency. You can use the MAI‑Transcribe‑1 model with the LLM Speech API.

## Prerequisites

> [!div class="checklist"]
> - An Azure subscription. You can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
> - [Create a Foundry resource for Speech](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) in the Azure portal.
> - Get the Speech resource key and region. After your Speech resource is deployed, select **Go to resource** to view and manage keys. For the current list of supported regions, see [Speech service regions](regions.md?tabs=llmspeech).
> - An audio file (less than 300 MB in size) in one of the formats: WAV, MP3, and FLAC.

## Use the MAI-Transcribe-1 model


The following languages are currently supported for mai-transcribe-1 model:
 - `Arabic`, `Chinese`, `Czech`, `Danish`, `Dutch`, `English`, `Finnish`, `French`, `German`, `Hindi`, `Hungarian`, `Indonesian`, `Italian`, `Japanese`, `Korean`, `Norwegian Bokmål`, `Polish`, `Portuguese`, `Romanian`, `Russian`, `Spanish`, `Swedish`, `Thai`, `Turkish`, and `Vietnamese`.


### Upload audio

You can provide audio data in the following ways:

- Pass inline audio data.

```
  --form 'audio=@"YourAudioFile"'
```

- Upload audio file from a public `audioUrl`.

```
  --form 'definition": "{\"audioUrl\": \"https://crbn.us/hello.wav"}"'
```

In the sections below, inline audio upload is used as an example.


### Create transcription

To use the MAI-Transcribe-1 model, set the `model` property accordingly in the request.
```azurecli-interactive
curl --location 'https://<YourServiceRegion>.api.cognitive.microsoft.com/speechtotext/transcriptions:transcribe?api-version=2025-10-15' \
--header 'Content-Type: multipart/form-data' \
--header 'Ocp-Apim-Subscription-Key: <YourSpeechResourceKey>' \
--form 'audio=@"YourAudioFile.wav"' \
--form 'definition={
  "enhancedMode": {
    "enabled": true,
    "model":"mai-transcribe-1"
  }
}'
```
Note the following limitations using the MAI-Transcribe-1 model:
- Diarization isn't supported.

> [!TIP]
> For more information about using LLM Speech API, see [LLM Speech API](llm-speech.md)

## Related content

- [MAI-Voice-1 in Azure Speech](mai-voices.md)
