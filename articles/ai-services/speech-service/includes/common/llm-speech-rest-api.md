---
manager: nitinme
author: goergenj
ms.author: jagoerge
ms.service: azure-ai-speech
ms.topic: include
ms.date: 01/31/2026
---

## Prerequisites

- An Azure Speech in Foundry Tools resource in one of the regions where the LLM speech API is available. For the current list of supported regions, see [Speech service regions](../../regions.md?tabs=llmspeech).
  
- An audio file (less than 2 hours long and less than 300 MB in size) in one of the formats and codecs supported by the batch transcription API: WAV, MP3, OPUS/OGG, FLAC, WMA, AAC, ALAW in WAV container, MULAW in WAV container, AMR, WebM, and SPEEX. For more information about supported audio formats, see [supported audio formats](../../batch-transcription-audio-data.md#supported-input-formats-and-codecs).
  

## Use the LLM speech API


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


### Call the LLM speech API
Make a multipart/form-data POST request to the `transcriptions` endpoint with the audio file and the request body properties. 

The following example shows how to transcribe an audio file with a specified locale. If you know the locale of the audio file, you can specify it to improve transcription accuracy and minimize the latency.

- Replace `YourSpeechResoureKey` with your Speech resource key.
- Replace `YourServiceRegion` with your Speech resource region.
- Replace `YourAudioFile` with the path to your audio file.

> [!IMPORTANT]
> For the recommended keyless authentication with Microsoft Entra ID, replace `--header 'Ocp-Apim-Subscription-Key: YourSpeechResoureKey'` with `--header "Authorization: Bearer YourAccessToken"`. For more information about keyless authentication, see the [role-based access control](../../role-based-access-control.md#authentication-with-keys-and-tokens) how-to guide.

#### Use LLM speech to transcribe an audio

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

#### Use LLM speech to translate an audio file

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

#### Use prompt-tuning to alter performance

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


Here are some best practices for prompts:
- Prompts are subject to a maximum length of 4,096 characters.
- Prompts should preferably be written in English.
- Prompts can guide output formatting. By default, responses use a display format optimized for readability. To enforce lexical formatting, include: `Output must be in lexical format.`
- Prompts can amplify the salience of specific phrases or acronyms, improving recognition likelihood. Use: `Pay attention to *phrase1*, *phrase2*, …`. For best results, limit the number of phrases per prompt.
- Prompts that aren’t related to speech tasks (e.g., `Tell me a story.`) are typically disregarded.


#### More configuration options

You can combine additional configuration options with [fast transcription](../../fast-transcription-create.md) to enable enhanced features such as `diarization`, `profanityFilterMode`, and `channels`.

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

Some configuration options, such as `locales` and `phraseLists`, are either not required or not applicable with LLM speech, and can be omitted from the request. Learn more from [configuration options of fast transcription](../../fast-transcription-create.md#request-configuration-options). 


#### Sample response

In the JSON response, the `combinedPhrases` property contains the full transcribed or translated text, and the `phrases` property contains segment-level and word-level details.

```json
{
    "durationMilliseconds": 57187,
    "combinedPhrases": [
        {
            "text": "With custom speech,you can evaluate and improve the microsoft speech to text accuracy for your applications and products 现成的语音转文本,利用通用语言模型作为一个基本模型,使用microsoft自有数据进行训练,并反映常用的口语。此基础模型使用那些代表各常见领域的方言和发音进行了预先训练。 Quand vous effectuez une demande de reconnaissance vocale, le modèle de base le plus récent pour chaque langue prise en charge est utilisé par défaut. Le modèle de base fonctionne très bien dans la plupart des scénarios de reconnaissance vocale. A custom model can be used to augment the base model to improve recognition of domain specific vocabulary specified to the application by providing text data to train the model. It can also be used to improve recognition based for the specific audio conditions of the application by providing audio data with reference transcriptions."
        }
    ],
    "phrases": [
        {
            "offsetMilliseconds": 80,
            "durationMilliseconds": 6960,
            "text": "With custom speech,you can evaluate and improve the microsoft speech to text accuracy for your applications and products.",
            "words": [
                {
                    "text": "with",
                    "offsetMilliseconds": 80,
                    "durationMilliseconds": 160
                },
                {
                    "text": "custom",
                    "offsetMilliseconds": 240,
                    "durationMilliseconds": 480
                },

                {
                    "text": "speech",
                    "offsetMilliseconds": 720,
                    "durationMilliseconds": 360
                },,
        // More transcription results...
        // Redacted for brevity
            ],
            "locale": "en-us",
            "confidence": 0
        },
        {
            "offsetMilliseconds": 8000,
            "durationMilliseconds": 8600,
            "text": "现成的语音转文本,利用通用语言模型作为一个基本模型,使用microsoft自有数据进行训练,并反映常用的口语。此基础模型使用那些代表各常见领域的方言和发音进行了预先训练。",
            "words": [
                {
                    "text": "现",
                    "offsetMilliseconds": 8000,
                    "durationMilliseconds": 40
                },
                {
                    "text": "成",
                    "offsetMilliseconds": 8040,
                    "durationMilliseconds": 40
                },
        // More transcription results...
        // Redacted for brevity
                {
                    "text": "训",
                    "offsetMilliseconds": 16400,
                    "durationMilliseconds": 40
                },
                {
                    "text": "练",
                    "offsetMilliseconds": 16560,
                    "durationMilliseconds": 40
                },
            ],
            "locale": "zh-cn",
            "confidence": 0
        // More transcription results...
        // Redacted for brevity
                {
                    "text": "with",
                    "offsetMilliseconds": 54720,
                    "durationMilliseconds": 200
                },
                {
                    "text": "reference",
                    "offsetMilliseconds": 54920,
                    "durationMilliseconds": 360
                },
                {
                    "text": "transcriptions.",
                    "offsetMilliseconds": 55280,
                    "durationMilliseconds": 1200
                }
            ],
            "locale": "en-us",
            "confidence": 0
        }
    ]
}
```

The response format is consistent with other existing speech-to-text outputs, such as fast transcription and batch transcription. Key differences include: 
- Word-level `durationMilliseconds` and `offsetMilliseconds` are not supported for `translate` task.
- Diarization is not supported for `translate` task, only the `speaker1` label is returned.
- `confidence` is not available and always `0`.
