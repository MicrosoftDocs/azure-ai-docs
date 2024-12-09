---
title: Use the fast transcription API - Speech service
titleSuffix: Azure AI services
description: Learn how to use Azure AI Speech for fast transcriptions, where you submit audio get the transcription results faster than real-time.
manager: nitinme
author: eric-urban
ms.author: eur
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 11/12/2024
# Customer intent: As a user who implements audio transcription, I want create transcriptions as quickly as possible.
---

# Use the fast transcription API with Azure AI Speech 

Fast transcription API is used to transcribe audio files with returning results synchronously and faster than real-time. Use fast transcription in the scenarios that you need the transcript of an audio recording as quickly as possible with predictable latency, such as: 

- Quick audio or video transcription, subtitles, and edit. 
- Video translation

Unlike the batch transcription API, fast transcription API only produces transcriptions in the display (not lexical) form. The display form is a more human-readable form of the transcription that includes punctuation and capitalization.

## Prerequisites

- An Azure AI Speech resource in one of the regions where the fast transcription API is available. The supported regions are: **Australia East**, **Brazil South**, **Central India**, **East US**, **East US 2**, **French Central**, **Japan East**, **North Central US**, **North Europe**, **South Central US**, **Southeast Asia**, **Sweden Central**, **West Europe**, **West US**, **West US 2**, **West US 3**. For more information about regions supported for other Speech service features, see [Speech service regions](./regions.md).
  
- An audio file (less than 2 hours long and less than 200 MB in size) in one of the formats and codecs supported by the batch transcription API. For more information about supported audio formats, see [supported audio formats](./batch-transcription-audio-data.md#supported-audio-formats-and-codecs).

## Use the fast transcription API

> [!TIP]
> Try out fast transcription in the [Azure AI Foundry portal](https://aka.ms/fasttranscription/studio).

We learn how to use the fast transcription API (via [Transcriptions - Transcribe](https://go.microsoft.com/fwlink/?linkid=2296107)) with the following scenarios:
- [Known locale specified](?tabs=locale-specified): Transcribe an audio file with a specified locale. If you know the locale of the audio file, you can specify it to improve transcription accuracy and minimize the latency.
- [Language identification on](?tabs=language-identification-on): Transcribe an audio file with language identification on. If you're not sure about the locale of the audio file, you can turn on language identification to let the Speech service identify the locale.
- [Diarization on](?tabs=diarization-on): Transcribe an audio file with diarization on. Diarization distinguishes between different speakers in the conversation. The Speech service provides information about which speaker was speaking a particular part of the transcribed speech.
- [Multi-channel on](?tabs=multi-channel-on): Transcribe an audio file that has one or two channels. Multi-channel transcriptions are useful for audio files with multiple channels, such as audio files with multiple speakers or audio files with background noise. By default, the fast transcription API merges all input channels into a single channel and then performs the transcription. If this isn't desirable, channels can be transcribed independently without merging.

# [Known locale specified](#tab/locale-specified)

Make a multipart/form-data POST request to the `transcriptions` endpoint with the audio file and the request body properties. 

The following example shows how to transcribe an audio file with a specified locale. If you know the locale of the audio file, you can specify it to improve transcription accuracy and minimize the latency.

- Replace `YourSubscriptionKey` with your Speech resource key.
- Replace `YourServiceRegion` with your Speech resource region.
- Replace `YourAudioFile` with the path to your audio file.

```azurecli-interactive
curl --location 'https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/transcriptions:transcribe?api-version=2024-11-15' \
--header 'Content-Type: multipart/form-data' \
--header 'Ocp-Apim-Subscription-Key: YourSubscriptionKey' \
--form 'audio=@"YourAudioFile"' \
--form 'definition="{
    "locales":["en-US"]}"'
```

Construct the form definition according to the following instructions:

- Set the optional (but recommended) `locales` property that should match the expected locale of the audio data to transcribe. In this example, the locale is set to `en-US`. The supported locales that you can specify are: de-DE, en-IN, en-US, es-ES, es-MX, fr-FR, hi-IN, it-IT, ja-JP, ko-KR, pt-BR, and zh-CN.

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
			"confidence": 0.93616915
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
			"confidence": 0.93616915
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
			"confidence": 0.93616915
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
			"confidence": 0.93616915
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
			"confidence": 0.93616915
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
			"confidence": 0.93616915
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
			"confidence": 0.9314801
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
			"confidence": 0.9314801
		}
	]
}
```

# [Language identification on](#tab/language-identification-on)

Make a multipart/form-data POST request to the `transcriptions` endpoint with the audio file and the request body properties. 

The following example shows how to transcribe an audio file with language identification on. If you're not sure about the locale, you can specify multiple locales. If you don't specify any locale, or if the locales that you specify aren't in the audio file, then the Speech service tries to identify the locale. 

- Replace `YourSubscriptionKey` with your Speech resource key.
- Replace `YourServiceRegion` with your Speech resource region.
- Replace `YourAudioFile` with the path to your audio file.

```azurecli-interactive
curl --location 'https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/transcriptions:transcribe?api-version=2024-11-15' \
--header 'Content-Type: multipart/form-data' \
--header 'Ocp-Apim-Subscription-Key: YourSubscriptionKey' \
--form 'audio=@"YourAudioFile"' \
--form 'definition="{
    "locales":["en-US","ja-JP"]}"'
```

Construct the form definition according to the following instructions:

- Set the optional (but recommended) `locales` property that should match the expected locale of the audio data to transcribe. In this example, the locales are set to `en-US` and `ja-JP`. The supported locales that you can specify are: de-DE, en-IN, en-US, es-ES, es-MX, fr-FR, hi-IN, it-IT, ja-JP, ko-KR, pt-BR, and zh-CN.

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

# [Diarization on](#tab/diarization-on)

Make a multipart/form-data POST request to the `transcriptions` endpoint with the audio file and the request body properties. 

The following example shows how to transcribe an audio file with diarization enabled. Diarization distinguishes between different speakers in the conversation. The Speech service provides information about which speaker was speaking a particular part of the transcribed speech.

- Replace `YourSubscriptionKey` with your Speech resource key.
- Replace `YourServiceRegion` with your Speech resource region.
- Replace `YourAudioFile` with the path to your audio file.

```azurecli-interactive
curl --location 'https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/transcriptions:transcribe?api-version=2024-11-15' \
--header 'Content-Type: multipart/form-data' \
--header 'Ocp-Apim-Subscription-Key: YourSubscriptionKey' \
--form 'audio=@"YourAudioFile"' \
--form 'definition="{
    "locales":["en-US"], 
    "diarization": {"maxSpeakers": 2,"enabled": true}}"'
```

Construct the form definition according to the following instructions:

1. Set the optional (but recommended) `locales` property that should match the expected locale of the audio data to transcribe. In this example, the locale is set to `en-US`. The supported locales that you can specify are: de-DE, en-IN, en-US, es-ES, es-MX, fr-FR, hi-IN, it-IT, ja-JP, ko-KR, pt-BR, and zh-CN.

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

- Replace `YourSubscriptionKey` with your Speech resource key.
- Replace `YourServiceRegion` with your Speech resource region.
- Replace `YourAudioFile` with the path to your audio file.

```azurecli-interactive
curl --location 'https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/transcriptions:transcribe?api-version=2024-11-15' \
--header 'Content-Type: multipart/form-data' \
--header 'Ocp-Apim-Subscription-Key: YourSubscriptionKey' \
--form 'audio=@"YourAudioFile"' \
--form 'definition="{
    "locales":["en-US"], 
    "channels": [0,1]}"'
```

Construct the form definition according to the following instructions:

1. Set the optional (but recommended) `locales` property that should match the expected locale of the audio data to transcribe. In this example, the locale is set to `en-US`. The supported locales that you can specify are: de-DE, en-IN, en-US, es-ES, es-MX, fr-FR, hi-IN, it-IT, ja-JP, ko-KR, pt-BR, and zh-CN.

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

## Request configuration options

Here are some property options to configure a transcription when you call the [Transcriptions - Transcribe](https://go.microsoft.com/fwlink/?linkid=2296107) operation.

| Property | Description | Required or optional |
|----------|-------------|----------------------|
| `channels` | The list of zero-based indices of the channels to be transcribed separately. Up to two channels are supported unless diarization is enabled. By default, the fast transcription API merges all input channels into a single channel and then performs the transcription. If this isn't desirable, channels can be transcribed independently without merging.<br/><br/>If you want to transcribe the channels from a stereo audio file separately, you need to specify `[0,1]`, `[0]`, or `[1]`. Otherwise, stereo audio is merged to mono and only a single channel is transcribed.<br/><br/>If the audio is stereo and diarization is enabled, then you can't set the `channels` property to `[0,1]`. The Speech service doesn't support diarization of multiple channels.<br/><br/>For mono audio, the `channels` property is ignored, and the audio is always transcribed as a single channel.| Optional |
| `diarization` | The diarization configuration. Diarization is the process of recognizing and separating multiple speakers in one audio channel. For example, specify `"diarization": {"maxSpeakers": 2, "enabled": true}`. Then the transcription file contains `speaker` entries (such as `"speaker": 0` or `"speaker": 1`) for each transcribed phrase. | Optional |
| `locales` | The list of locales that should match the expected locale of the audio data to transcribe.<br/><br/>If you know the locale of the audio file, you can specify it to improve transcription accuracy and minimize the latency. If a single locale is specified, that locale is used for transcription.<br/><br/>But if you're not sure about the locale, you can specify multiple locales. Language identification might be more accurate with a more precise list of candidate locales.<br/><br/>If you don't specify any locale, or if the locales that you specify aren't in the audio file, then the Speech service still tries to identify the language. If the language can't be identified, an error is returned.<br/><br/>The supported locales that you can specify are: de-DE, en-IN, en-US, es-ES, es-MX, fr-FR, hi-IN, it-IT, ja-JP, ko-KR, pt-BR, and zh-CN. You can get the latest supported languages via the [Transcriptions - List Supported Locales](/rest/api/speechtotext/transcriptions/list-supported-locales) REST API. For more information about locales, see the [Speech service language support](language-support.md?tabs=stt) documentation.| Optional but recommended if you know the expected locale. |
| `profanityFilterMode` |Specifies how to handle profanity in recognition results. Accepted values are `None` to disable profanity filtering, `Masked` to replace profanity with asterisks, `Removed` to remove all profanity from the result, or `Tags` to add profanity tags. The default value is `Masked`. | Optional |

## Related content

- [Fast transcription REST API reference](https://go.microsoft.com/fwlink/?linkid=2296107)
- [Speech to text supported languages](./language-support.md?tabs=stt)
- [Batch transcription](./batch-transcription.md)
