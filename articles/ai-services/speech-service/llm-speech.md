---
title: Use the llm-speech API - Speech service
titleSuffix: Azure AI services
description: Learn how to use Azure AI Speech for llm-speech, where you can leverage the latest llm-powered speech model for transcription and translation
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 10/15/2025
# Customer intent: As a user who implements audio transcription, I want create transcriptions as quickly as possible.
---

# LLM-Speech for speech transcription and translation (Preview)
[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

LLM-Speech is powered by a large-language-model-enhanced speech model that delivers improved quality, deep contextual understanding, multilingual support, and prompt-tuning capabilities. It uses GPU acceleration for ultra-fast inference, making it ideal for a wide range of scenarios including generating captions and subtitles from audio files, summarizing meeting notes, assisting call center agents, transcribing voicemails, and more.

The LLM-speech API currently supports the following speech tasks:
- `transcribe`
- `translate`


## Prerequisites

- An Azure AI Speech resource in one of the regions where the fast transcription API is available. The supported regions are: **East US**, **North Europe**, **Central India**, **Southeast Asia**, **West US**. For more information about regions supported for other Speech service features, see [Speech service regions](./regions.md).
  
- An audio file (less than 2 hours long and less than 300 MB in size) in one of the formats and codecs supported by the batch transcription API: WAV, MP3, OPUS/OGG, FLAC, WMA, AAC, ALAW in WAV container, MULAW in WAV container, AMR, WebM, and SPEEX. For more information about supported audio formats, see [supported audio formats](./batch-transcription-audio-data.md#supported-audio-formats-and-codecs).
  

## Use the llm-speech API

> [!TIP]
> Try out llm-speech in the [Azure AI Foundry](https://aka.ms/llm-speech-playground).

### Supported languages

The following languages are currently supported for both `transcribe` and `translate` tasks:

 - `English`, `Chinese`, `German`, `French`, `Italian`, `Japanese`, `Spanish`, `Portuguese`, and `Korean`.


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


### Quickstart
Make a multipart/form-data POST request to the `transcriptions` endpoint with the audio file and the request body properties. 

The following example shows how to transcribe an audio file with a specified locale. If you know the locale of the audio file, you can specify it to improve transcription accuracy and minimize the latency.

- Replace `YourSpeechResoureKey` with your Speech resource key.
- Replace `YourServiceRegion` with your Speech resource region.
- Replace `YourAudioFile` with the path to your audio file.

> [!IMPORTANT]
> For the recommended keyless authentication with Microsoft Entra ID, replace `--header 'Ocp-Apim-Subscription-Key: YourSpeechResoureKey'` with `--header "Authorization: Bearer YourAccessToken"`. For more information about keyless authentication, see the [role-based access control](./role-based-access-control.md#authentication-with-keys-and-tokens) how-to guide.

#### Use llm-speech to transcribe an audio

You can transcribe audio in the input language without specifying a locale code. The model automatically detects and selects the appropriate language based on the audio content.

```azurecli-interactive
curl --location 'https://<YourServiceRegion>.api.cognitive.microsoft.com/speechtotext/transcriptions:transcribe?api-version=2025-10-15' \
--header 'Content-Type: multipart/form-data' \
--header 'Ocp-Apim-Subscription-Key: <YourSpeechResourceKey>' \
--form 'audio=@"YourAudioFile.wav"' \
--form 'definition={
  "enhancedMode": {
    "enabled": true,
    "task": "transcribe"
  }
}'
```

#### Use llm-speech to transcribe an audio

You can translate audio into a specified target language. To enable translation, you must provide the target language code in the request.

```azurecli-interactive
curl --location 'https://<YourServiceRegion>.api.cognitive.microsoft.com/speechtotext/transcriptions:transcribe?api-version=2025-10-15' \
--header 'Content-Type: multipart/form-data' \
--header 'Ocp-Apim-Subscription-Key: <YourSpeechResourceKey>' \
--form 'audio=@"YourAudioFile.wav"' \
--form 'definition={
  "enhancedMode": {
    "enabled": true,
    "task": "translate",
    "targetLanguage": "ko"
  }
}'
```

#### Prompt tuning

You can provide an optional text to guide the output style for `transcribe` or `translate` task.

```azurecli-interactive
curl --location 'https://<YourServiceRegion>.api.cognitive.microsoft.com/speechtotext/transcriptions:transcribe?api-version=2025-10-15' \
--header 'Content-Type: multipart/form-data' \
--header 'Ocp-Apim-Subscription-Key: <YourSpeechResourceKey>' \
--form 'audio=@"YourAudioFile.wav"' \
--form 'definition={
  "enhancedMode": {
    "enabled": true,
    "task": "transcribe",
    "prompt": ["Output must be in lexical format."]
  }
}'
```


Here are some examples and practices of how prompts can help:
- Prompts are subject to a maximum length of 4,096 characters.
- The prompt should match the audio language.
- Prompts can guide output formatting. By default, responses use a display format optimized for readability. To enforce lexical formatting, include: `Output must be in lexical format.`
- Prompts can amplify the salience of specific phrases or acronyms, improving recognition likelihood. Use: `Pay attention to *phrase1*, *phrase2*, …`. For best results, limit the number of phrases per prompt.
- Prompts that aren’t related to speech tasks (e.g., `Tell me a story.`) are typically disregarded.


#### More audio configs

You can combine additional configuration options with [fast transcription](fast-transcription-create.md) to enable enhanced features such as `diarization`, `profanityFilterMode`, and `channels`.

```azurecli-interactive
curl --location 'https://<YourServiceRegion>.api.cognitive.microsoft.com/speechtotext/transcriptions:transcribe?api-version=2025-10-15' \
--header 'Content-Type: multipart/form-data' \
--header 'Ocp-Apim-Subscription-Key: <YourSpeechResourceKey>' \
--form 'audio=@"YourAudioFile.wav"' \
--form 'definition={
  "enhancedMode": {
    "enabled": true,
    "task": "transcribe",
    "prompt": ["Output must be in lexical format."]
  },
  "diarization": {
    "maxSpeakers": 2,
    "enabled": true
  },
  "profanityFilterMode": "Masked"
}'
```

Some configuration options, such as `locales` and `phraseLists`, are either not required or not applicable with llm-speech, and can be omitted from the request. Learn more from [configuration options of Fast Transcription](fast-transcription-create.md#request-configuration-options). 

---

> [!NOTE]
> Speech service is an elastic service. If you receive 429 error code (too many requests), please follow the [best practices to mitigate throttling during autoscaling](speech-services-quotas-and-limits.md#general-best-practices-to-mitigate-throttling-during-autoscaling).

## Related content

- [Speech to text REST API reference](/rest/api/speechtotext/transcriptions/transcribe)
- [Speech to text supported languages](./language-support.md?tabs=stt)
- [Fast transcription](fast-transcription-create.md)
