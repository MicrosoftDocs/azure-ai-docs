---
manager: nitinme
author: goergenj
ms.author: jagoerge
ms.service: azure-ai-speech
ms.topic: include
ms.date: 01/31/2026
---

## Prerequisites

- An Azure Speech resource in one of the regions where the fast transcription API is available. For the current list of supported regions, see the [Speech service regions table](../../regions.md?tabs=stt).
  
- An audio file (less than 2 hours long and less than 300 MB in size) in one of the formats and codecs supported by the batch transcription API: WAV, MP3, OPUS/OGG, FLAC, WMA, AAC, ALAW in WAV container, MULAW in WAV container, AMR, WebM, and SPEEX. For more information about supported audio formats, see [supported audio formats](../../batch-transcription-audio-data.md#supported-input-formats-and-codecs).


## Upload audio

You can provide audio data to fast transcription in the following ways:

- Inline audio upload
  
```
--form 'audio=@"YourAudioFile"'
```

- Audio from a public URL
  
```
--form 'definition="{"audioUrl": "https://crbn.us/hello.wav"}"'
```
In the sections below, inline audio upload is used as an example.

## Use the fast transcription API

> [!TIP]
> Try out fast transcription in the [Microsoft Foundry portal](https://aka.ms/fasttranscription/studio).

We learn how to use the fast transcription API (via [Transcriptions - Transcribe](/rest/api/speechtotext/transcriptions/transcribe)) with the following scenarios:
- [Known locale specified](?tabs=locale-specified): Transcribe an audio file with a specified locale. If you know the locale of the audio file, you can specify it to improve transcription accuracy and minimize the latency.
- [Language identification on](?tabs=language-identification-on): Transcribe an audio file with language identification on. If you're not sure about the locale of the audio file, you can turn on language identification to let the Speech service identify the locale (one locale per audio).
- [Multi-lingual transcription (preview)](?tabs=multilingual-transcription-on): Transcribe an audio file with the latest multi-lingual speech transcription model. If your audio contains multi-lingual contents that you want to transcribe continuously and accurately, you can use the latest multi-lingual speech transcription model without specifying the locale codes.
- [Diarization on](?tabs=diarization-on): Transcribe an audio file with diarization on. Diarization distinguishes between different speakers in the conversation. The Speech service provides information about which speaker was speaking a particular part of the transcribed speech.
- [Multi-channel on](?tabs=multi-channel-on): Transcribe an audio file that has one or two channels. Multi-channel transcriptions are useful for audio files with multiple channels, such as audio files with multiple speakers or audio files with background noise. By default, the fast transcription API merges all input channels into a single channel and then performs the transcription. If this isn't desirable, channels can be transcribed independently without merging.

# [Known locale specified](#tab/locale-specified)

Make a multipart/form-data POST request to the `transcriptions` endpoint with the audio file and the request body properties. 

The following example shows how to transcribe an audio file with a specified locale. If you know the locale of the audio file, you can specify it to improve transcription accuracy and minimize the latency.

- Replace `YourSpeechResourceKey` with your Speech resource key.
- Replace `YourServiceRegion` with your Speech resource region.
- Replace `YourAudioFile` with the path to your audio file.

> [!IMPORTANT]
> For the recommended keyless authentication with Microsoft Entra ID, replace `--header 'Ocp-Apim-Subscription-Key: YourSpeechResourceKey'` with `--header "Authorization: Bearer YourAccessToken"`. For more information about keyless authentication, see the [role-based access control](../../role-based-access-control.md#authentication-with-keys-and-tokens) how-to guide.

```azurecli-interactive
curl --location 'https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/transcriptions:transcribe?api-version=2025-10-15' \
--header 'Content-Type: multipart/form-data' \
--header 'Ocp-Apim-Subscription-Key: YourSpeechResourceKey' \
--form 'audio=@"YourAudioFile"' \
--form 'definition="{
    "locales":["en-US"]}"'
```

Construct the form definition according to the following instructions:

- Set the optional (but recommended) `locales` property that should match the expected locale of the audio data to transcribe. In this example, the locale is set to `en-US`. For more information about the supported locales, see [speech to text supported languages](../../language-support.md?tabs=stt).

For more information about `locales` and other properties for the fast transcription API, see the [request configuration options](#request-configuration-options) section later in this guide.

The response includes `durationMilliseconds`, `offsetMilliseconds`, and more. The `combinedPhrases` property contains the full transcriptions for all speakers. 

```json
{
    "durationMilliseconds": 182439,
    "combinedPhrases": [
        {
            "text": "Good afternoon. This is Sam. Thank you for calling Contoso. How can I help? Hi there. My name is Mary. I'm currently living in Los Angeles, but I'm planning to move to Las Vegas. I would like to apply for a loan. Okay. I see you're currently living in California. Let me make sure I understand you correctly. Uh You'd like to apply for a loan even though you'll be moving soon. Is that right? Yes, exactly. So I'm planning to relocate soon, but I would like to apply for the loan first so that I can purchase a new home once I move there. And are you planning to sell your current home? Yes, I will be listing it on the market soon and hopefully it'll sell quickly. That's why I'm applying for a loan now, so that I can purchase a new house in Nevada and close on it quickly as well once my current home sells. I see. Would you mind holding for a moment while I take your information down? Yeah, no problem. Thank you for your help. Mm-hmm. Just one moment. All right. Thank you for your patience, ma'am. May I have your first and last name, please? Yes, my name is Mary Smith. Thank you, Ms. Smith. May I have your current address, please? Yes. So my address is 123 Main Street in Los Angeles, California, and the zip code is 90923. Sorry, that was a 90 what? 90923. 90923 on Main Street. Got it. Thank you. May I have your phone number as well, please? Uh Yes, my phone number is 504-529-2351 and then yeah. 2351. Got it. And do you have an e-mail address we I can associate with this application? uh Yes, so my e-mail address is mary.a.sm78@gmail.com. Mary.a, was that a S-N as in November or M as in Mike? M as in Mike. Mike78, got it. Thank you. Ms. Smith, do you currently have any other loans? Uh Yes, so I currently have two other loans through Contoso. So my first one is my car loan and then my other is my student loan. They total about 1400 per month combined and my interest rate is 8%. I see. And you're currently paying those loans off monthly, is that right? Yes, of course I do. OK, thank you. Here's what I suggest we do. Let me place you on a brief hold again so that I can talk with one of our loan officers and get this started for you immediately. In the meantime, it would be great if you could take a few minutes and complete the remainder of the secure application online at www.contosoloans.com. Yeah, that sounds good. I can go ahead and get started. Thank you for your help. Thank you."
        }
    ],
    "phrases": [
        {
            "offsetMilliseconds": 960,
            "durationMilliseconds": 640,
            "text": "Good afternoon.",
            "words": [
                {
                    "text": "Good",
                    "offsetMilliseconds": 960,
                    "durationMilliseconds": 240
                },
                {
                    "text": "afternoon.",
                    "offsetMilliseconds": 1200,
                    "durationMilliseconds": 400
                }
            ],
            "locale": "en-US",
            "confidence": 0.93554276
        },
        {
            "offsetMilliseconds": 1600,
            "durationMilliseconds": 640,
            "text": "This is Sam.",
            "words": [
                {
                    "text": "This",
                    "offsetMilliseconds": 1600,
                    "durationMilliseconds": 240
                },
                {
                    "text": "is",
                    "offsetMilliseconds": 1840,
                    "durationMilliseconds": 120
                },
                {
                    "text": "Sam.",
                    "offsetMilliseconds": 1960,
                    "durationMilliseconds": 280
                }
            ],
            "locale": "en-US",
            "confidence": 0.93554276
        },
        {
            "offsetMilliseconds": 2240,
            "durationMilliseconds": 1040,
            "text": "Thank you for calling Contoso.",
            "words": [
                {
                    "text": "Thank",
                    "offsetMilliseconds": 2240,
                    "durationMilliseconds": 200
                },
                {
                    "text": "you",
                    "offsetMilliseconds": 2440,
                    "durationMilliseconds": 80
                },
                {
                    "text": "for",
                    "offsetMilliseconds": 2520,
                    "durationMilliseconds": 120
                },
                {
                    "text": "calling",
                    "offsetMilliseconds": 2640,
                    "durationMilliseconds": 200
                },
                {
                    "text": "Contoso.",
                    "offsetMilliseconds": 2840,
                    "durationMilliseconds": 440
                }
            ],
            "locale": "en-US",
            "confidence": 0.93554276
        },
        {
            "offsetMilliseconds": 3280,
            "durationMilliseconds": 640,
            "text": "How can I help?",
            "words": [
                {
                    "text": "How",
                    "offsetMilliseconds": 3280,
                    "durationMilliseconds": 120
                },
                {
                    "text": "can",
                    "offsetMilliseconds": 3440,
                    "durationMilliseconds": 120
                },
                {
                    "text": "I",
                    "offsetMilliseconds": 3560,
                    "durationMilliseconds": 40
                },
                {
                    "text": "help?",
                    "offsetMilliseconds": 3600,
                    "durationMilliseconds": 320
                }
            ],
            "locale": "en-US",
            "confidence": 0.93554276
        },
        {
            "offsetMilliseconds": 5040,
            "durationMilliseconds": 400,
            "text": "Hi there.",
            "words": [
                {
                    "text": "Hi",
                    "offsetMilliseconds": 5040,
                    "durationMilliseconds": 240
                },
                {
                    "text": "there.",
                    "offsetMilliseconds": 5280,
                    "durationMilliseconds": 160
                }
            ],
            "locale": "en-US",
            "confidence": 0.93554276
        },
        {
            "offsetMilliseconds": 5440,
            "durationMilliseconds": 800,
            "text": "My name is Mary.",
            "words": [
                {
                    "text": "My",
                    "offsetMilliseconds": 5440,
                    "durationMilliseconds": 80
                },
                {
                    "text": "name",
                    "offsetMilliseconds": 5520,
                    "durationMilliseconds": 120
                },
                {
                    "text": "is",
                    "offsetMilliseconds": 5640,
                    "durationMilliseconds": 80
                },
                {
                    "text": "Mary.",
                    "offsetMilliseconds": 5720,
                    "durationMilliseconds": 520
                }
            ],
            "locale": "en-US",
            "confidence": 0.93554276
        },
        // More transcription results...
        // Redacted for brevity
        {
            "offsetMilliseconds": 180320,
            "durationMilliseconds": 680,
            "text": "Thank you for your help.",
            "words": [
                {
                    "text": "Thank",
                    "offsetMilliseconds": 180320,
                    "durationMilliseconds": 160
                },
                {
                    "text": "you",
                    "offsetMilliseconds": 180480,
                    "durationMilliseconds": 80
                },
                {
                    "text": "for",
                    "offsetMilliseconds": 180560,
                    "durationMilliseconds": 120
                },
                {
                    "text": "your",
                    "offsetMilliseconds": 180680,
                    "durationMilliseconds": 120
                },
                {
                    "text": "help.",
                    "offsetMilliseconds": 180800,
                    "durationMilliseconds": 200
                }
            ],
            "locale": "en-US",
            "confidence": 0.92022026
        },
        {
            "offsetMilliseconds": 181960,
            "durationMilliseconds": 280,
            "text": "Thank you.",
            "words": [
                {
                    "text": "Thank",
                    "offsetMilliseconds": 181960,
                    "durationMilliseconds": 200
                },
                {
                    "text": "you.",
                    "offsetMilliseconds": 182160,
                    "durationMilliseconds": 80
                }
            ],
            "locale": "en-US",
            "confidence": 0.92022026
        }
    ]
}
```

# [Language identification on](#tab/language-identification-on)

Make a multipart/form-data POST request to the `transcriptions` endpoint with the audio file and the request body properties. 

The following example shows how to transcribe an audio file with language identification on. If you're not sure about the locale, you can specify multiple locales. If you don't specify any locale, or if the locales that you specify aren't in the audio file, then the Speech service tries to identify the locale. 
> [!NOTE]
> The language identification in fast transcription is designed to identify one main language locale per audio file. If you need to transcribe multi-lingual contents in the audio, please consider [multi-lingual transcription (preview)](?tabs=multilingual-transcription-on).

- Replace `YourSpeechResoureKey` with your Speech resource key.
- Replace `YourServiceRegion` with your Speech resource region.
- Replace `YourAudioFile` with the path to your audio file.

> [!IMPORTANT]
> For the recommended keyless authentication with Microsoft Entra ID, replace `--header 'Ocp-Apim-Subscription-Key: YourSpeechResoureKey'` with `--header "Authorization: Bearer YourAccessToken"`. For more information about keyless authentication, see the [role-based access control](../../role-based-access-control.md#authentication-with-keys-and-tokens) how-to guide.

```azurecli-interactive
curl --location 'https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/transcriptions:transcribe?api-version=2025-10-15' \
--header 'Content-Type: multipart/form-data' \
--header 'Ocp-Apim-Subscription-Key: YourSpeechResoureKey' \
--form 'audio=@"YourAudioFile"' \
--form 'definition="{
    "locales":["en-US","ja-JP"]}"'
```

Construct the form definition according to the following instructions:

- Set the optional (but recommended) `locales` property that should match the expected locale of the audio data to transcribe. In this example, the locales are set to `en-US` and `ja-JP`. The supported locales that you can specify are within all the supported languages.

For more information about `locales` and other properties for the fast transcription API, see the [request configuration options](#request-configuration-options) section later in this guide.

The response includes `durationMilliseconds`, `offsetMilliseconds`, and more. The `combinedPhrases` property contains the full transcriptions for all speakers. 

```json
{
    "durationMilliseconds": 185079,
    "combinedPhrases": [
        {
            "text": "Hello, thank you for calling Contoso. Who am I speaking with today? Hi, my name is Mary Rondo. I'm trying to enroll myself with Contoso. Hi, Mary. Are you calling because you need health insurance? Yes. Yeah, I'm calling to sign up for insurance. Great. Uh If you can answer a few questions, we can get you signed up in a Jiffy. Okay. So what's your full name? uh So Mary Beth Rondo, last name is R like Romeo, O like Ocean, N like Nancy D, D like Dog, and O like Ocean again. Rondo. Got it. And what's the best callback number in case we get disconnected? I only have a cell phone, so I can give you that. Yep, that'll be fine. Sure. So it's 234-554 and then 9312. Got it. So to confirm, it's 234-554-9312. Yep, that's right. Excellent. Let's get some additional information for your application. Do you have a job? Uh Yes, I am self-employed. Okay, so then you have a social security number as well? Uh Yes, I do. Okay, and what is your social security number, please? Uh Sure, so it's 412-253-4931. 6789. Sorry, was that a 25 or a 225? You cut out for a bit. It's double two, so 412, then another two, then five. Thank you so much. And could I have your e-mail address, please? Yeah, it's maryrondo@gmail.com. So my first and last name at gmail.com. No periods, no dashes. Great. Uh That is the last question. So let me take your information and I'll be able to get you signed up right away. Thank you for calling Contoso and I'll be able to get you signed up immediately. One of our agents will call you back in about 24 hours or so to confirm your application. That sounds good. Thank you. Absolutely. If you need anything else, please give us a call at 1-800-555-5564, extension 123. Thank you very much for calling Contoso. Actually, so I have one more question. Yes, of course. I'm curious, will I be getting a physical card as proof of coverage? So the default is a digital membership card, but we can send you a physical card if you prefer. Uh Yes. Could you please mail it to me when it's ready? I'd like to have it shipped to, are you ready for my address? Uh Yeah. uh So it's 2660 Unit A on Maple Avenue, Southeast Lansing, and then zip code is 48823. Absolutely. I've made a note on your file. Awesome. Thanks so much. You're very welcome. Thank you for calling Contoso and have a great day."
        }
    ],
    "phrases": [
        {
            "offsetMilliseconds": 720,
            "durationMilliseconds": 1600,
            "text": "Hello, thank you for calling Contoso.",
            "words": [
                {
                    "text": "Hello,",
                    "offsetMilliseconds": 720,
                    "durationMilliseconds": 480
                },
                {
                    "text": "thank",
                    "offsetMilliseconds": 1200,
                    "durationMilliseconds": 200
                },
                {
                    "text": "you",
                    "offsetMilliseconds": 1400,
                    "durationMilliseconds": 80
                },
                {
                    "text": "for",
                    "offsetMilliseconds": 1480,
                    "durationMilliseconds": 120
                },
                {
                    "text": "calling",
                    "offsetMilliseconds": 1600,
                    "durationMilliseconds": 240
                },
                {
                    "text": "Contoso.",
                    "offsetMilliseconds": 1840,
                    "durationMilliseconds": 480
                }
            ],
            "locale": "en-US",
            "confidence": 0.93265927
        },
        {
            "offsetMilliseconds": 2320,
            "durationMilliseconds": 1120,
            "text": "Who am I speaking with today?",
            "words": [
                {
                    "text": "Who",
                    "offsetMilliseconds": 2320,
                    "durationMilliseconds": 160
                },
                {
                    "text": "am",
                    "offsetMilliseconds": 2480,
                    "durationMilliseconds": 80
                },
                {
                    "text": "I",
                    "offsetMilliseconds": 2560,
                    "durationMilliseconds": 80
                },
                {
                    "text": "speaking",
                    "offsetMilliseconds": 2640,
                    "durationMilliseconds": 320
                },
                {
                    "text": "with",
                    "offsetMilliseconds": 2960,
                    "durationMilliseconds": 160
                },
                {
                    "text": "today?",
                    "offsetMilliseconds": 3120,
                    "durationMilliseconds": 320
                }
            ],
            "locale": "en-US",
            "confidence": 0.93265927
        },
        {
            "offsetMilliseconds": 4480,
            "durationMilliseconds": 1600,
            "text": "Hi, my name is Mary Rondo.",
            "words": [
                {
                    "text": "Hi,",
                    "offsetMilliseconds": 4480,
                    "durationMilliseconds": 400
                },
                {
                    "text": "my",
                    "offsetMilliseconds": 4880,
                    "durationMilliseconds": 120
                },
                {
                    "text": "name",
                    "offsetMilliseconds": 5000,
                    "durationMilliseconds": 120
                },
                {
                    "text": "is",
                    "offsetMilliseconds": 5120,
                    "durationMilliseconds": 160
                },
                {
                    "text": "Mary",
                    "offsetMilliseconds": 5280,
                    "durationMilliseconds": 240
                },
                {
                    "text": "Rondo.",
                    "offsetMilliseconds": 5520,
                    "durationMilliseconds": 560
                }
            ],
            "locale": "en-US",
            "confidence": 0.93265927
        },
        {
            "offsetMilliseconds": 6120,
            "durationMilliseconds": 1800,
            "text": "I'm trying to enroll myself with Contoso.",
            "words": [
                {
                    "text": "I'm",
                    "offsetMilliseconds": 6120,
                    "durationMilliseconds": 120
                },
                {
                    "text": "trying",
                    "offsetMilliseconds": 6240,
                    "durationMilliseconds": 200
                },
                {
                    "text": "to",
                    "offsetMilliseconds": 6440,
                    "durationMilliseconds": 80
                },
                {
                    "text": "enroll",
                    "offsetMilliseconds": 6520,
                    "durationMilliseconds": 200
                },
                {
                    "text": "myself",
                    "offsetMilliseconds": 6720,
                    "durationMilliseconds": 360
                },
                {
                    "text": "with",
                    "offsetMilliseconds": 7080,
                    "durationMilliseconds": 120
                },
                {
                    "text": "Contoso.",
                    "offsetMilliseconds": 7200,
                    "durationMilliseconds": 720
                }
            ],
            "locale": "en-US",
            "confidence": 0.93265927
        },
        // More transcription results...
        // Redacted for brevity
        {
            "offsetMilliseconds": 181520,
            "durationMilliseconds": 720,
            "text": "You're very welcome.",
            "words": [
                {
                    "text": "You're",
                    "offsetMilliseconds": 181520,
                    "durationMilliseconds": 160
                },
                {
                    "text": "very",
                    "offsetMilliseconds": 181680,
                    "durationMilliseconds": 200
                },
                {
                    "text": "welcome.",
                    "offsetMilliseconds": 181880,
                    "durationMilliseconds": 360
                }
            ],
            "locale": "en-US",
            "confidence": 0.90571773
        },
        {
            "offsetMilliseconds": 182320,
            "durationMilliseconds": 1840,
            "text": "Thank you for calling Contoso and have a great day.",
            "words": [
                {
                    "text": "Thank",
                    "offsetMilliseconds": 182320,
                    "durationMilliseconds": 200
                },
                {
                    "text": "you",
                    "offsetMilliseconds": 182520,
                    "durationMilliseconds": 80
                },
                {
                    "text": "for",
                    "offsetMilliseconds": 182600,
                    "durationMilliseconds": 120
                },
                {
                    "text": "calling",
                    "offsetMilliseconds": 182720,
                    "durationMilliseconds": 280
                },
                {
                    "text": "Contoso",
                    "offsetMilliseconds": 183000,
                    "durationMilliseconds": 520
                },
                {
                    "text": "and",
                    "offsetMilliseconds": 183520,
                    "durationMilliseconds": 160
                },
                {
                    "text": "have",
                    "offsetMilliseconds": 183680,
                    "durationMilliseconds": 120
                },
                {
                    "text": "a",
                    "offsetMilliseconds": 183800,
                    "durationMilliseconds": 40
                },
                {
                    "text": "great",
                    "offsetMilliseconds": 183840,
                    "durationMilliseconds": 200
                },
                {
                    "text": "day.",
                    "offsetMilliseconds": 184040,
                    "durationMilliseconds": 120
                }
            ],
            "locale": "en-US",
            "confidence": 0.90571773
        }
    ]
}
```

# [Multi-lingual transcription](#tab/multilingual-transcription-on)

Make a multipart/form-data POST request to the `transcriptions` endpoint with the audio file and the request body properties. 

The following example shows how to transcribe an audio file with the latest multi-lingual speech transcription model. If your audio contains multi-lingual contents that you want to transcribe continuously and accurately, you can use the latest multi-lingual speech transcription model without specifying the locale codes.

- Replace `YourSpeechResoureKey` with your Speech resource key.
- Replace `YourServiceRegion` with your Speech resource region.
- Replace `YourAudioFile` with the path to your audio file.

> [!IMPORTANT]
> For the recommended keyless authentication with Microsoft Entra ID, replace `--header 'Ocp-Apim-Subscription-Key: YourSpeechResoureKey'` with `--header "Authorization: Bearer YourAccessToken"`. For more information about keyless authentication, see the [role-based access control](../../role-based-access-control.md#authentication-with-keys-and-tokens) how-to guide.

```azurecli-interactive
curl --location 'https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/transcriptions:transcribe?api-version=2025-10-15' \
--header 'Content-Type: multipart/form-data' \
--header 'Ocp-Apim-Subscription-Key: YourSpeechResoureKey' \
--form 'audio=@"YourAudioFile"' \
--form 'definition="{
    "locales":[]}"'
```

Construct the form definition according to the following instructions:

- You can either leave the `locales` property empty (as shown in the previous example) or omit it.

- The supported audio input locales with current multi-lingual model are: **de-DE**, **en-AU**, **en-CA**, **en-GB**, **en-IN**, **en-US**, **es-ES**, **es-MX**, **fr-CA**, **fr-FR**, **it-IT**, **ja-JP**, **ko-KR**, and **zh-CN**.

- The transcription result is distinguished at the language level and will follow the "major locale of this language" (e.g., it will always output "en-US" locale code even if the audio has a British English or Indian English accent).

For more information about `locales` and other properties for the fast transcription API, see the [request configuration options](#request-configuration-options) section later in this guide.

The response includes `durationMilliseconds`, `offsetMilliseconds`, and more. The `combinedPhrases` property contains the full transcriptions for all speakers. 

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
                },
                {
                    "text": ",",
                    "offsetMilliseconds": 1080,
                    "durationMilliseconds": 10
                },
                {
                    "text": "you",
                    "offsetMilliseconds": 1200,
                    "durationMilliseconds": 240
                },
                {
                    "text": "can",
                    "offsetMilliseconds": 1440,
                    "durationMilliseconds": 160
                },
                {
                    "text": "evaluate",
                    "offsetMilliseconds": 1600,
                    "durationMilliseconds": 640
                },
                {
                    "text": "and",
                    "offsetMilliseconds": 2240,
                    "durationMilliseconds": 200
                },
                {
                    "text": "improve",
                    "offsetMilliseconds": 2440,
                    "durationMilliseconds": 280
                },
                {
                    "text": "the",
                    "offsetMilliseconds": 2720,
                    "durationMilliseconds": 160
                },
                {
                    "text": "microsoft",
                    "offsetMilliseconds": 2880,
                    "durationMilliseconds": 640
                },
                {
                    "text": "speech",
                    "offsetMilliseconds": 3520,
                    "durationMilliseconds": 320
                },
                {
                    "text": "to",
                    "offsetMilliseconds": 3840,
                    "durationMilliseconds": 200
                },
                {
                    "text": "text",
                    "offsetMilliseconds": 4040,
                    "durationMilliseconds": 360
                },
                {
                    "text": "accuracy",
                    "offsetMilliseconds": 4400,
                    "durationMilliseconds": 560
                },
                {
                    "text": "for",
                    "offsetMilliseconds": 4960,
                    "durationMilliseconds": 160
                },
                {
                    "text": "your",
                    "offsetMilliseconds": 5120,
                    "durationMilliseconds": 200
                },
                {
                    "text": "applications",
                    "offsetMilliseconds": 5320,
                    "durationMilliseconds": 760
                },
                {
                    "text": "and",
                    "offsetMilliseconds": 6080,
                    "durationMilliseconds": 200
                },
                {
                    "text": "products",
                    "offsetMilliseconds": 6280,
                    "durationMilliseconds": 680
                },
            ],
            "locale": "en-us",
            "confidence": 0.9539559
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
                {
                    "text": "的",
                    "offsetMilliseconds": 8160,
                    "durationMilliseconds": 40
                },
                {
                    "text": "语",
                    "offsetMilliseconds": 8200,
                    "durationMilliseconds": 40
                },
                {
                    "text": "音",
                    "offsetMilliseconds": 8240,
                    "durationMilliseconds": 40
                },
                {
                    "text": "转",
                    "offsetMilliseconds": 8280,
                    "durationMilliseconds": 40
                },
                {
                    "text": "文",
                    "offsetMilliseconds": 8320,
                    "durationMilliseconds": 40
                },
                {
                    "text": "本,",
                    "offsetMilliseconds": 8360,
                    "durationMilliseconds": 40
                },
                {
                    "text": "利",
                    "offsetMilliseconds": 8400,
                    "durationMilliseconds": 40
                },
                {
                    "text": "用",
                    "offsetMilliseconds": 8440,
                    "durationMilliseconds": 40
                },
                {
                    "text": "通",
                    "offsetMilliseconds": 8480,
                    "durationMilliseconds": 40
                },
                {
                    "text": "用",
                    "offsetMilliseconds": 8520,
                    "durationMilliseconds": 40
                },
                {
                    "text": "语",
                    "offsetMilliseconds": 8560,
                    "durationMilliseconds": 40
                },
                {
                    "text": "言",
                    "offsetMilliseconds": 8600,
                    "durationMilliseconds": 40
                },
                {
                    "text": "模",
                    "offsetMilliseconds": 8640,
                    "durationMilliseconds": 40
                },
                {
                    "text": "型",
                    "offsetMilliseconds": 8680,
                    "durationMilliseconds": 40
                },
                {
                    "text": "作",
                    "offsetMilliseconds": 8800,
                    "durationMilliseconds": 40
                },
                {
                    "text": "为",
                    "offsetMilliseconds": 8840,
                    "durationMilliseconds": 40
                },
                {
                    "text": "一",
                    "offsetMilliseconds": 9520,
                    "durationMilliseconds": 40
                },
                {
                    "text": "个",
                    "offsetMilliseconds": 9560,
                    "durationMilliseconds": 40
                },
                {
                    "text": "基",
                    "offsetMilliseconds": 9600,
                    "durationMilliseconds": 40
                },
                {
                    "text": "本",
                    "offsetMilliseconds": 9640,
                    "durationMilliseconds": 40
                },
                {
                    "text": "模",
                    "offsetMilliseconds": 9680,
                    "durationMilliseconds": 40
                },
                {
                    "text": "型,",
                    "offsetMilliseconds": 9720,
                    "durationMilliseconds": 40
                },
                {
                    "text": "使",
                    "offsetMilliseconds": 9760,
                    "durationMilliseconds": 40
                },
                {
                    "text": "用",
                    "offsetMilliseconds": 10080,
                    "durationMilliseconds": 320
                },
                {
                    "text": "microsoft",
                    "offsetMilliseconds": 10400,
                    "durationMilliseconds": 3600
                },
                {
                    "text": "自",
                    "offsetMilliseconds": 14000,
                    "durationMilliseconds": 40
                },
                {
                    "text": "有",
                    "offsetMilliseconds": 14040,
                    "durationMilliseconds": 40
                },
                {
                    "text": "数",
                    "offsetMilliseconds": 14160,
                    "durationMilliseconds": 40
                },
                {
                    "text": "据",
                    "offsetMilliseconds": 14200,
                    "durationMilliseconds": 40
                },
                {
                    "text": "进",
                    "offsetMilliseconds": 14320,
                    "durationMilliseconds": 40
                },
                {
                    "text": "行",
                    "offsetMilliseconds": 14360,
                    "durationMilliseconds": 40
                },
                {
                    "text": "训",
                    "offsetMilliseconds": 14400,
                    "durationMilliseconds": 40
                },
                {
                    "text": "练,",
                    "offsetMilliseconds": 14440,
                    "durationMilliseconds": 40
                },
                {
                    "text": "并",
                    "offsetMilliseconds": 14480,
                    "durationMilliseconds": 40
                },
                {
                    "text": "反",
                    "offsetMilliseconds": 14520,
                    "durationMilliseconds": 40
                },
                {
                    "text": "映",
                    "offsetMilliseconds": 14560,
                    "durationMilliseconds": 40
                },
                {
                    "text": "常",
                    "offsetMilliseconds": 14600,
                    "durationMilliseconds": 40
                },
                {
                    "text": "用",
                    "offsetMilliseconds": 14640,
                    "durationMilliseconds": 40
                },
                {
                    "text": "的",
                    "offsetMilliseconds": 14680,
                    "durationMilliseconds": 40
                },
                {
                    "text": "口",
                    "offsetMilliseconds": 14720,
                    "durationMilliseconds": 40
                },
                {
                    "text": "语",
                    "offsetMilliseconds": 14760,
                    "durationMilliseconds": 40
                },
                {
                    "text": "。",
                    "offsetMilliseconds": 14800,
                    "durationMilliseconds": 40
                },
                {
                    "text": "此",
                    "offsetMilliseconds": 14840,
                    "durationMilliseconds": 40
                },
                {
                    "text": "基",
                    "offsetMilliseconds": 14880,
                    "durationMilliseconds": 40
                },
                {
                    "text": "础",
                    "offsetMilliseconds": 14920,
                    "durationMilliseconds": 40
                },
                {
                    "text": "模",
                    "offsetMilliseconds": 14960,
                    "durationMilliseconds": 40
                },
                {
                    "text": "型",
                    "offsetMilliseconds": 15000,
                    "durationMilliseconds": 40
                },
                {
                    "text": "使",
                    "offsetMilliseconds": 15040,
                    "durationMilliseconds": 40
                },
                {
                    "text": "用",
                    "offsetMilliseconds": 15080,
                    "durationMilliseconds": 40
                },
                {
                    "text": "那",
                    "offsetMilliseconds": 15120,
                    "durationMilliseconds": 40
                },
                {
                    "text": "些",
                    "offsetMilliseconds": 15160,
                    "durationMilliseconds": 40
                },
                {
                    "text": "代",
                    "offsetMilliseconds": 15200,
                    "durationMilliseconds": 40
                },
                {
                    "text": "表",
                    "offsetMilliseconds": 15240,
                    "durationMilliseconds": 40
                },
                {
                    "text": "各",
                    "offsetMilliseconds": 15280,
                    "durationMilliseconds": 40
                },
                {
                    "text": "常",
                    "offsetMilliseconds": 15320,
                    "durationMilliseconds": 40
                },
                {
                    "text": "见",
                    "offsetMilliseconds": 15360,
                    "durationMilliseconds": 40
                },
                {
                    "text": "领",
                    "offsetMilliseconds": 15400,
                    "durationMilliseconds": 40
                },
                {
                    "text": "域",
                    "offsetMilliseconds": 15760,
                    "durationMilliseconds": 40
                },
                {
                    "text": "的",
                    "offsetMilliseconds": 15800,
                    "durationMilliseconds": 40
                },
                {
                    "text": "方",
                    "offsetMilliseconds": 15920,
                    "durationMilliseconds": 40
                },
                {
                    "text": "言",
                    "offsetMilliseconds": 15960,
                    "durationMilliseconds": 40
                },
                {
                    "text": "和",
                    "offsetMilliseconds": 16000,
                    "durationMilliseconds": 40
                },
                {
                    "text": "发",
                    "offsetMilliseconds": 16040,
                    "durationMilliseconds": 40
                },
                {
                    "text": "音",
                    "offsetMilliseconds": 16080,
                    "durationMilliseconds": 40
                },
                {
                    "text": "进",
                    "offsetMilliseconds": 16120,
                    "durationMilliseconds": 40
                },
                {
                    "text": "行",
                    "offsetMilliseconds": 16160,
                    "durationMilliseconds": 40
                },
                {
                    "text": "了",
                    "offsetMilliseconds": 16200,
                    "durationMilliseconds": 40
                },
                {
                    "text": "预",
                    "offsetMilliseconds": 16320,
                    "durationMilliseconds": 40
                },
                {
                    "text": "先",
                    "offsetMilliseconds": 16360,
                    "durationMilliseconds": 40
                },
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
            "confidence": 0.9241725
        },
        {
            "offsetMilliseconds": 24320,
            "durationMilliseconds": 6640,
            "text": "Quand vous effectuez une demande de reconnaissance vocale, le modèle de base le plus récent pour chaque langue prise en charge est utilisé par défaut.",
            "words": [
                {
                    "text": "Quand",
                    "offsetMilliseconds": 24320,
                    "durationMilliseconds": 160
                },
                {
                    "text": "vous",
                    "offsetMilliseconds": 24480,
                    "durationMilliseconds": 80
                },
        // More transcription results...
        // Redacted for brevity
                {
                    "text": "scénarios",
                    "offsetMilliseconds": 34200,
                    "durationMilliseconds": 400
                },
                {
                    "text": "de",
                    "offsetMilliseconds": 34600,
                    "durationMilliseconds": 120
                },
                {
                    "text": "reconnaissance",
                    "offsetMilliseconds": 34720,
                    "durationMilliseconds": 640
                },
                {
                    "text": "vocale.",
                    "offsetMilliseconds": 35360,
                    "durationMilliseconds": 480
                }
            ],
            "locale": "fr-fr",
            "confidence": 0.9308314
        },
        {
            "offsetMilliseconds": 36720,
            "durationMilliseconds": 10320,
            "text": "A custom model can be used to augment the base model to improve recognition of domain specific vocabulary spécifique to the application by providing text data to train the model.",
            "words": [
                {
                    "text": "A",
                    "offsetMilliseconds": 36720,
                    "durationMilliseconds": 80
                },
                {
                    "text": "custom",
                    "offsetMilliseconds": 36880,
                    "durationMilliseconds": 400
                },
                {
                    "text": "model",
                    "offsetMilliseconds": 37280,
                    "durationMilliseconds": 480
                },

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
            "confidence": 0.92155737
        }
    ]
}
```



# [Diarization on](#tab/diarization-on)

Make a multipart/form-data POST request to the `transcriptions` endpoint with the audio file and the request body properties. 

The following example shows how to transcribe an audio file with diarization enabled. Diarization distinguishes between different speakers in the conversation. The Speech service provides information about which speaker was speaking a particular part of the transcribed speech.

- Replace `YourSpeechResoureKey` with your Speech resource key.
- Replace `YourServiceRegion` with your Speech resource region.
- Replace `YourAudioFile` with the path to your audio file.

> [!IMPORTANT]
> For the recommended keyless authentication with Microsoft Entra ID, replace `--header 'Ocp-Apim-Subscription-Key: YourSpeechResoureKey'` with `--header "Authorization: Bearer YourAccessToken"`. For more information about keyless authentication, see the [role-based access control](../../role-based-access-control.md#authentication-with-keys-and-tokens) how-to guide.

```azurecli-interactive
curl --location 'https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/transcriptions:transcribe?api-version=2025-10-15' \
--header 'Content-Type: multipart/form-data' \
--header 'Ocp-Apim-Subscription-Key: YourSpeechResoureKey' \
--form 'audio=@"YourAudioFile"' \
--form 'definition="{
    "locales":["en-US"], 
    "diarization": {"maxSpeakers": 2,"enabled": true}}"'
```

Construct the form definition according to the following instructions:

1. Set the optional (but recommended) `locales` property that should match the expected locale of the audio data to transcribe. In this example, the locale is set to `en-US`.

1. Set the `diarization` property to recognize and separate multiple speakers in one audio channel. For example, specify `"diarization": {"maxSpeakers": 2, "enabled": true}`. Then the transcription file contains `speaker` entries for each transcribed phrase.

For more information about `locales`, `diarization`, and other properties for the fast transcription API, see the [request configuration options](#request-configuration-options) section later in this guide.

The response includes `durationMilliseconds`, `offsetMilliseconds`, and more. In this example, diarization is enabled, so the response includes `speaker` information for each transcribed phrase. The `combinedPhrases` property contains the full transcriptions for all speakers in a single channel. 

```json
{
    "durationMilliseconds": 182439,
    "combinedPhrases": [
        {
            "channel": 0,
            "text": "Good afternoon. This is Sam. Thank you for calling Contoso. How can I help? Hi there. My name is Mary. I'm currently living in Los Angeles, but I'm planning to move to Las Vegas. I would like to apply for a loan. Okay. I see you're currently living in California. Let me make sure I understand you correctly. Uh You'd like to apply for a loan even though you'll be moving soon. Is that right? Yes, exactly. So I'm planning to relocate soon, but I would like to apply for the loan first so that I can purchase a new home once I move there. And are you planning to sell your current home? Yes, I will be listing it on the market soon and hopefully it'll sell quickly. That's why I'm applying for a loan now, so that I can purchase a new house in Nevada and close on it quickly as well once my current home sells. I see. Would you mind holding for a moment while I take your information down? Yeah, no problem. Thank you for your help. Mm-hmm. Just one moment. All right. Thank you for your patience, ma'am. May I have your first and last name, please? Yes, my name is Mary Smith. Thank you, Ms. Smith. May I have your current address, please? Yes. So my address is 123 Main Street in Los Angeles, California, and the zip code is 90923. Sorry, that was a 90 what? 90923. 90923 on Main Street. Got it. Thank you. May I have your phone number as well, please? Uh. Yes, my phone number is 504-529-2351 and then yeah. 2351. Got it. And do you have an e-mail address we I can associate with this application? Uh Yes, so my e-mail address is mary.a.sm78@gmail.com. Mary.a, was that a S-N as in November or M as in Mike? M as in Mike. Mike78, got it. Thank you. Ms. Smith, do you currently have any other loans? Uh Yes, so I currently have two other loans through Contoso. So my first one is my car loan and then my other is my student loan. They total about 1400 per month combined and my interest rate is 8%. I see. And. You're currently paying those loans off monthly, is that right? Yes, of course I do. OK, thank you. Here's what I suggest we do. Let me place you on a brief hold again so that I can talk with one of our loan officers and get this started for you immediately. In the meantime, it would be great if you could take a few minutes and complete the remainder of the secure application online at www.contosoloans.com. Yeah, that sounds good. I can go ahead and get started. Thank you for your help. Thank you."
        }
    ],
    "phrases": [
        {
            "channel": 0,
            "speaker": 1,
            "offsetMilliseconds": 960,
            "durationMilliseconds": 640,
            "text": "Good afternoon.",
            "words": [
                {
                    "text": "Good",
                    "offsetMilliseconds": 960,
                    "durationMilliseconds": 240
                },
                {
                    "text": "afternoon.",
                    "offsetMilliseconds": 1200,
                    "durationMilliseconds": 400
                }
            ],
            "locale": "en-US",
            "confidence": 0.93616915
        },
        {
            "channel": 0,
            "speaker": 1,
            "offsetMilliseconds": 1600,
            "durationMilliseconds": 640,
            "text": "This is Sam.",
            "words": [
                {
                    "text": "This",
                    "offsetMilliseconds": 1600,
                    "durationMilliseconds": 240
                },
                {
                    "text": "is",
                    "offsetMilliseconds": 1840,
                    "durationMilliseconds": 120
                },
                {
                    "text": "Sam.",
                    "offsetMilliseconds": 1960,
                    "durationMilliseconds": 280
                }
            ],
            "locale": "en-US",
            "confidence": 0.93616915
        },
        {
            "channel": 0,
            "speaker": 1,
            "offsetMilliseconds": 2240,
            "durationMilliseconds": 1040,
            "text": "Thank you for calling Contoso.",
            "words": [
                {
                    "text": "Thank",
                    "offsetMilliseconds": 2240,
                    "durationMilliseconds": 200
                },
                {
                    "text": "you",
                    "offsetMilliseconds": 2440,
                    "durationMilliseconds": 80
                },
                {
                    "text": "for",
                    "offsetMilliseconds": 2520,
                    "durationMilliseconds": 120
                },
                {
                    "text": "calling",
                    "offsetMilliseconds": 2640,
                    "durationMilliseconds": 200
                },
                {
                    "text": "Contoso.",
                    "offsetMilliseconds": 2840,
                    "durationMilliseconds": 440
                }
            ],
            "locale": "en-US",
            "confidence": 0.93616915
        },
        {
            "channel": 0,
            "speaker": 1,
            "offsetMilliseconds": 3280,
            "durationMilliseconds": 640,
            "text": "How can I help?",
            "words": [
                {
                    "text": "How",
                    "offsetMilliseconds": 3280,
                    "durationMilliseconds": 120
                },
                {
                    "text": "can",
                    "offsetMilliseconds": 3440,
                    "durationMilliseconds": 120
                },
                {
                    "text": "I",
                    "offsetMilliseconds": 3560,
                    "durationMilliseconds": 40
                },
                {
                    "text": "help?",
                    "offsetMilliseconds": 3600,
                    "durationMilliseconds": 320
                }
            ],
            "locale": "en-US",
            "confidence": 0.93616915
        },
        {
            "channel": 0,
            "speaker": 0,
            "offsetMilliseconds": 5040,
            "durationMilliseconds": 400,
            "text": "Hi there.",
            "words": [
                {
                    "text": "Hi",
                    "offsetMilliseconds": 5040,
                    "durationMilliseconds": 240
                },
                {
                    "text": "there.",
                    "offsetMilliseconds": 5280,
                    "durationMilliseconds": 160
                }
            ],
            "locale": "en-US",
            "confidence": 0.93616915
        },
        {
            "channel": 0,
            "speaker": 0,
            "offsetMilliseconds": 5440,
            "durationMilliseconds": 800,
            "text": "My name is Mary.",
            "words": [
                {
                    "text": "My",
                    "offsetMilliseconds": 5440,
                    "durationMilliseconds": 80
                },
                {
                    "text": "name",
                    "offsetMilliseconds": 5520,
                    "durationMilliseconds": 120
                },
                {
                    "text": "is",
                    "offsetMilliseconds": 5640,
                    "durationMilliseconds": 80
                },
                {
                    "text": "Mary.",
                    "offsetMilliseconds": 5720,
                    "durationMilliseconds": 520
                }
            ],
            "locale": "en-US",
            "confidence": 0.93616915
        },
        // More transcription results...
        // Redacted for brevity
        {
            "channel": 0,
            "speaker": 0,
            "offsetMilliseconds": 180320,
            "durationMilliseconds": 680,
            "text": "Thank you for your help.",
            "words": [
                {
                    "text": "Thank",
                    "offsetMilliseconds": 180320,
                    "durationMilliseconds": 160
                },
                {
                    "text": "you",
                    "offsetMilliseconds": 180480,
                    "durationMilliseconds": 80
                },
                {
                    "text": "for",
                    "offsetMilliseconds": 180560,
                    "durationMilliseconds": 120
                },
                {
                    "text": "your",
                    "offsetMilliseconds": 180680,
                    "durationMilliseconds": 120
                },
                {
                    "text": "help.",
                    "offsetMilliseconds": 180800,
                    "durationMilliseconds": 200
                }
            ],
            "locale": "en-US",
            "confidence": 0.9314801
        },
        {
            "channel": 0,
            "speaker": 1,
            "offsetMilliseconds": 181960,
            "durationMilliseconds": 280,
            "text": "Thank you.",
            "words": [
                {
                    "text": "Thank",
                    "offsetMilliseconds": 181960,
                    "durationMilliseconds": 200
                },
                {
                    "text": "you.",
                    "offsetMilliseconds": 182160,
                    "durationMilliseconds": 80
                }
            ],
            "locale": "en-US",
            "confidence": 0.9314801
        }
    ]
}
```

# [Multi-channel on](#tab/multi-channel)

Make a multipart/form-data POST request to the `transcriptions` endpoint with the audio file and the request body properties. 

The following example shows how to transcribe an audio file that has one or two channels. Multi-channel transcriptions are useful for audio files with multiple channels, such as audio files with multiple speakers or audio files with background noise. By default, the fast transcription API merges all input channels into a single channel and then performs the transcription. If this isn't desirable, channels can be transcribed independently without merging.

- Replace `YourSpeechResoureKey` with your Speech resource key.
- Replace `YourServiceRegion` with your Speech resource region.
- Replace `YourAudioFile` with the path to your audio file.

> [!IMPORTANT]
> For the recommended keyless authentication with Microsoft Entra ID, replace `--header 'Ocp-Apim-Subscription-Key: YourSpeechResoureKey'` with `--header "Authorization: Bearer YourAccessToken"`. For more information about keyless authentication, see the [role-based access control](../../role-based-access-control.md#authentication-with-keys-and-tokens) how-to guide.

```azurecli-interactive
curl --location 'https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/transcriptions:transcribe?api-version=2025-10-15' \
--header 'Content-Type: multipart/form-data' \
--header 'Ocp-Apim-Subscription-Key: YourSpeechResoureKey' \
--form 'audio=@"YourAudioFile"' \
--form 'definition="{
    "locales":["en-US"], 
    "channels": [0,1]}"'
```

Construct the form definition according to the following instructions:

1. Set the optional (but recommended) `locales` property that should match the expected locale of the audio data to transcribe. In this example, the locale is set to `en-US`. The supported locales that you can specify are: de-DE, en-GB, en-IN, en-US, es-ES, es-MX, fr-FR, hi-IN, it-IT, ja-JP, ko-KR, pt-BR, and zh-CN.

1. Set the `channels` property to specify the zero-based indices of the channels to be transcribed separately. Up to two channels are supported unless diarization is enabled. In this example, channels 0 and 1 are specified.

For more information about `locales`, `channels`, and other properties for the fast transcription API, see the [request configuration options](#request-configuration-options) section later in this guide.

The response includes `durationMilliseconds`, `offsetMilliseconds`, and more. The `channel` property identifies the channel if the audio file contains multiple channels. The `combinedPhrases` property contains full transcriptions separate per audio channel. Look for `"channel": 0,"text"` and `"channel": 1,"text"` to identify the full transcriptions for each channel.

```json
{
    "durationMilliseconds": 185079,
    "combinedPhrases": [
        {
            "channel": 0,
            "text": "Hello. Thank you for calling Contoso. Who am I speaking with today? Hi, Mary. Are you calling because you need health insurance? Great. If you can answer a few questions, we can get you signed up in the Jiffy. So what's your full name? Got it. And what's the best callback number in case we get disconnected? Yep, that'll be fine. Got it. So to confirm, it's 234-554-9312. Excellent. Let's get some additional information for your application. Do you have a job? OK, so then you have a Social Security number as well. OK, and what is your Social Security number please? Sorry, what was that, a 25 or a 225? You cut out for a bit. Alright, thank you so much. And could I have your e-mail address please? Great. Uh That is the last question. So let me take your information and I'll be able to get you signed up right away. Thank you for calling Contoso and I'll be able to get you signed up immediately. One of our agents will call you back in about 24 hours or so to confirm your application. Absolutely. If you need anything else, please give us a call at 1-800-555-5564, extension 123. Thank you very much for calling Contoso. Uh Yes, of course. So the default is a digital membership card, but we can send you a physical card if you prefer. Uh, yeah. Absolutely. I've made a note on your file. You're very welcome. Thank you for calling Contoso and have a great day."
        },
        {
            "channel": 1,
            "text": "Hi, my name is Mary Rondo. I'm trying to enroll myself with Contuso. Yes, yeah, I'm calling to sign up for insurance. Okay. So Mary Beth Rondo, last name is R like Romeo, O like Ocean, N like Nancy D, D like Dog, and O like Ocean again. Rondo. I only have a cell phone so I can give you that. Sure, so it's 234-554 and then 9312. Yep, that's right. Uh Yes, I am self-employed. Yes, I do. Uh Sure, so it's 412256789. It's double two, so 412, then another two, then five. Yeah, it's maryrondo@gmail.com. So my first and last name at gmail.com. No periods, no dashes. That was quick. Thank you. Actually, so I have one more question. I'm curious, will I be getting a physical card as proof of coverage? uh Yes. Could you please mail it to me when it's ready? I'd like to have it shipped to, are you ready for my address? So it's 2660 Unit A on Maple Avenue SE, Lansing, and then zip code is 48823. Awesome. Thanks so much."
        }
    ],
    "phrases": [
        {
            "channel": 0,
            "offsetMilliseconds": 720,
            "durationMilliseconds": 480,
            "text": "Hello.",
            "words": [
                {
                    "text": "Hello.",
                    "offsetMilliseconds": 720,
                    "durationMilliseconds": 480
                }
            ],
            "locale": "en-US",
            "confidence": 0.9177142
        },
        {
            "channel": 0,
            "offsetMilliseconds": 1200,
            "durationMilliseconds": 1120,
            "text": "Thank you for calling Contoso.",
            "words": [
                {
                    "text": "Thank",
                    "offsetMilliseconds": 1200,
                    "durationMilliseconds": 200
                },
                {
                    "text": "you",
                    "offsetMilliseconds": 1400,
                    "durationMilliseconds": 80
                },
                {
                    "text": "for",
                    "offsetMilliseconds": 1480,
                    "durationMilliseconds": 120
                },
                {
                    "text": "calling",
                    "offsetMilliseconds": 1600,
                    "durationMilliseconds": 240
                },
                {
                    "text": "Contoso.",
                    "offsetMilliseconds": 1840,
                    "durationMilliseconds": 480
                }
            ],
            "locale": "en-US",
            "confidence": 0.9177142
        },
        {
            "channel": 0,
            "offsetMilliseconds": 2320,
            "durationMilliseconds": 1120,
            "text": "Who am I speaking with today?",
            "words": [
                {
                    "text": "Who",
                    "offsetMilliseconds": 2320,
                    "durationMilliseconds": 160
                },
                {
                    "text": "am",
                    "offsetMilliseconds": 2480,
                    "durationMilliseconds": 80
                },
                {
                    "text": "I",
                    "offsetMilliseconds": 2560,
                    "durationMilliseconds": 80
                },
                {
                    "text": "speaking",
                    "offsetMilliseconds": 2640,
                    "durationMilliseconds": 320
                },
                {
                    "text": "with",
                    "offsetMilliseconds": 2960,
                    "durationMilliseconds": 160
                },
                {
                    "text": "today?",
                    "offsetMilliseconds": 3120,
                    "durationMilliseconds": 320
                }
            ],
            "locale": "en-US",
            "confidence": 0.9177142
        },
        {
            "channel": 0,
            "offsetMilliseconds": 9520,
            "durationMilliseconds": 400,
            "text": "Hi, Mary.",
            "words": [
                {
                    "text": "Hi,",
                    "offsetMilliseconds": 9520,
                    "durationMilliseconds": 80
                },
                {
                    "text": "Mary.",
                    "offsetMilliseconds": 9600,
                    "durationMilliseconds": 320
                }
            ],
            "locale": "en-US",
            "confidence": 0.9177142
        },
        // More transcription results...
        // Redacted for brevity
        {
            "channel": 1,
            "offsetMilliseconds": 4480,
            "durationMilliseconds": 1600,
            "text": "Hi, my name is Mary Rondo.",
            "words": [
                {
                    "text": "Hi,",
                    "offsetMilliseconds": 4480,
                    "durationMilliseconds": 400
                },
                {
                    "text": "my",
                    "offsetMilliseconds": 4880,
                    "durationMilliseconds": 120
                },
                {
                    "text": "name",
                    "offsetMilliseconds": 5000,
                    "durationMilliseconds": 120
                },
                {
                    "text": "is",
                    "offsetMilliseconds": 5120,
                    "durationMilliseconds": 160
                },
                {
                    "text": "Mary",
                    "offsetMilliseconds": 5280,
                    "durationMilliseconds": 240
                },
                {
                    "text": "Rondo.",
                    "offsetMilliseconds": 5520,
                    "durationMilliseconds": 560
                }
            ],
            "locale": "en-US",
            "confidence": 0.8989456
        },
        {
            "channel": 1,
            "offsetMilliseconds": 6080,
            "durationMilliseconds": 1920,
            "text": "I'm trying to enroll myself with Contuso.",
            "words": [
                {
                    "text": "I'm",
                    "offsetMilliseconds": 6080,
                    "durationMilliseconds": 160
                },
                {
                    "text": "trying",
                    "offsetMilliseconds": 6240,
                    "durationMilliseconds": 200
                },
                {
                    "text": "to",
                    "offsetMilliseconds": 6440,
                    "durationMilliseconds": 80
                },
                {
                    "text": "enroll",
                    "offsetMilliseconds": 6520,
                    "durationMilliseconds": 200
                },
                {
                    "text": "myself",
                    "offsetMilliseconds": 6720,
                    "durationMilliseconds": 360
                },
                {
                    "text": "with",
                    "offsetMilliseconds": 7080,
                    "durationMilliseconds": 120
                },
                {
                    "text": "Contuso.",
                    "offsetMilliseconds": 7200,
                    "durationMilliseconds": 800
                }
            ],
            "locale": "en-US",
            "confidence": 0.8989456
        },
        // More transcription results...
        // Redacted for brevity
    ]
}
```
---

> [!NOTE]
> Speech service is an elastic service. If you receive 429 error code (too many requests), please follow the [best practices to mitigate throttling during autoscaling](../../speech-services-quotas-and-limits.md#general-best-practices-to-mitigate-throttling-during-autoscaling).

## Request configuration options

Here are some property options to configure a transcription when you call the [Transcriptions - Transcribe](/rest/api/speechtotext/transcriptions/transcribe) operation.

| Property | Description | Required or optional |
|----------|-------------|----------------------|
| `channels` | The list of zero-based indices of the channels to be transcribed separately. Up to two channels are supported unless diarization is enabled. By default, the fast transcription API merges all input channels into a single channel and then performs the transcription. If this isn't desirable, channels can be transcribed independently without merging.<br/><br/>If you want to transcribe the channels from a stereo audio file separately, you need to specify `[0,1]`, `[0]`, or `[1]`. Otherwise, stereo audio is merged to mono and only a single channel is transcribed.<br/><br/>If the audio is stereo and diarization is enabled, then you can't set the `channels` property to `[0,1]`. The Speech service doesn't support diarization of multiple channels.<br/><br/>For mono audio, the `channels` property is ignored, and the audio is always transcribed as a single channel.| Optional |
| `diarization` | The diarization configuration. Diarization is the process of recognizing and separating multiple speakers in one audio channel. For example, specify `"diarization": {"maxSpeakers": 2, "enabled": true}`. Then the transcription file contains `speaker` entries (such as `"speaker": 0` or `"speaker": 1`) for each transcribed phrase. | Optional |
| `locales` | The list of locales that should match the expected locale of the audio data to transcribe.<br/><br/>If you know the locale of the audio file, you can specify it to improve transcription accuracy and minimize the latency. If a single locale is specified, that locale is used for transcription.<br/><br/>But if you're not sure about the locale, you can specify multiple locales to use language identification. Language identification might be more accurate with a more precise list of candidate locales.<br/><br/>If you don't specify any locale, then the Speech service will use the latest multi-lingual model to identify the locale and transcribe continuously.<br/><br/> You can get the latest supported languages via the [Transcriptions - List Supported Locales](/rest/api/speechtotext/transcriptions/list-supported-locales) REST API (API version 2024-11-15 or later). For more information about locales, see the [Speech service language support](../../language-support.md?tabs=stt) documentation.| Optional but recommended if you know the expected locale. |
| `phraseList` |Phrase list is a list of words or phrases provided ahead of time to help improve their recognition. Adding a phrase to a phrase list increases its importance, thus making it more likely to be recognized. For example, specify `phraseList":{"phrases":["Contoso","Jessie","Rehaan"]}`. Phrase List is supported via API version 2025-10-15. For more information, see [Improve recognition accuracy with phrase list](../../improve-accuracy-phrase-list.md#implement-phrase-list-in-fast-transcription). | Optional |
| `profanityFilterMode` |Specifies how to handle profanity in recognition results. Accepted values are `None` to disable profanity filtering, `Masked` to replace profanity with asterisks, `Removed` to remove all profanity from the result, or `Tags` to add profanity tags. The default value is `Masked`. | Optional |