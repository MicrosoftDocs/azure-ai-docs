---
author: PatrickFarley
reviewer: patrickfarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 10/28/2025
ms.author: pafarley
ms.custom: references_regions
---

### December 2025 release

Speech to text 5.1.0
- General availability of real time diarization using the speech to text container.
- Resolved vulnerabilities

### November 2025 release

* LLM speech API is public preview now. It uses a large-language-model-enhanced speech model that delivers improved quality, deep contextual understanding, multilingual support, and prompt-tuning capabilities. It currently supports the following speech tasks:
   - `transcribe`: Convert pre-recorded audio into text.
   - `translate`: Convert pre-recorded audio into text in a specified target language.

  For more information, see [LLM speech](../../llm-speech.md). 
* Fast transcription is generally available. It can transcribe audio much faster than the actual audio duration. For more information, see the [fast transcription API guide](../../fast-transcription-create.md).
* To transcribe multi-lingual contents continuously and accurately in an audio file, you can now use the latest multi-lingual model without specifying the locale codes via fast transcription API. For more information, see [multi-lingual transcription in fast transcription](../../fast-transcription-create.md?tabs=multilingual-transcription-on).
* Video translation is now available in the Azure Speech service. For more information, see [What is video translation?](../../video-translation-overview.md)


### October 2025 release

#### Speech to text REST API version 2025-10-15

The speech to text REST API version 2025-10-15 is released for general availability. For more information, see the [speech to text REST API reference documentation](https://go.microsoft.com/fwlink/?linkid=2296107) and the [Speech to text REST API guide](../../rest-speech-to-text.md).


#### Phrase list weight control for Speech SDK

You can now control the influence of phrase lists on speech recognition results when using the Speech SDK with Real-time transcription. The new phrase list weight feature allows you to set a bias level between 0.0 (disabled) and 2.0 (maximum influence) to fine-tune how much priority phrase list terms receive over the default dictionary. For more information, see [Improve recognition accuracy with phrase list](../../improve-accuracy-phrase-list.md).

### September 2025 release

Speech to text 5.0.3-preview
- Fixed vulnerabilities
- Support user set redis endpoint for diarization.
- STT backend/frontend engine update
- Added coverage of locales previously supported in version 4.12.

### August 2025 release

#### New locales supported in Fast Transcription
Fast transcription now supports additional locales including a few `en-` variants (12 locales), `es-` variants (19 locales), and `ar-` variants (13 locales). For more information, see [speech to text supported languages](../../language-support.md?tabs=stt).

### July 2025 release

#### Improved speech to text models

The English models (all `en-*` models except for `en-IN`) were updated to incorporate a new VAD (voice activity detector) which helps reduce the latency by 100 ms or more. It can affect the accuracy and silence segmentation both positively and negatively, with the aim of reducing latency. Further language expansion is coming in the next few months.

### June 2025 release

#### Improved pronunciation assessment model

We rolled out significant upgrades to the pronunciation assessment models for `ta-IN` and `ms-MY`. You're seeing a noticeable jump in Pearson Correlation Coefficients (PCC), which means more precise and dependable evaluations.

These updated models are ready to use through the API and the Microsoft Foundry playground, just like before.

#### Improved speech to text models
Accuracy of speech to text models in [fast transcription](../../fast-transcription-create.md) for `de-DE`, `en-US`, `en-GB`, `es-ES`, `es-MX`,  `fr-FR`, `it-IT`, `ja-JP`, `ko-KR`, `pt-BR`, and `zh-CN` locales improving by 10%-25% percent respectively, particularly with improved readability and recognition on entities.

### May 2025 release

#### Improved speech to text models
Accuracy of speech to text models for `ta-IN`, `te-IN`, `en-IN`, and `hu-HU` locales improving by 5-10 percent respectively. We also approximate a 20x reduction in ghost words for the `ta-IN` and `te-IN` models.

#### Fast transcription API - Multi-lingual speech transcription

To transcribe multi-lingual contents continuously and accurately in an audio file, now you can use the latest multi-lingual model without specifying the locale codes via fast transcription API. For more information, see [multi-lingual transcription in fast transcription](../../fast-transcription-create.md?tabs=multilingual-transcription-on).

#### New locales supported in Fast Transcription
Fast transcription now supports additional locales including fi-FI, he-IL, id-ID, pl-PL, pt-PT, sv-SE, etc. For more information, see [speech to text supported languages](../../language-support.md?tabs=stt).

### April 2025 release

#### Pronunciation assessment

We are excited to announce substantial improvements to our pronunciation assessment models for these locales: `de-DE`, `es-MX`, `it-IT`, `ja-JP`, `ko-KR`, and `pt-BR`. These enhancements bring significant advancements in Pearson Correlation Coefficients (PCC), ensuring more accurate and reliable assessments.

As before, the models are available through the API and Microsoft Foundry playground.

### March 2025 release

#### Conversation transcription multichannel diarization (retired)

Conversation transcription multichannel diarization is retiring on March 28, 2025.

To continue using speech to text with diarization, use the following features instead:

- [Real-time speech to text with diarization](../../get-started-stt-diarization.md)
- [Fast transcription with diarization](../../fast-transcription-create.md)
- [Batch transcription with diarization](../../batch-transcription.md)

These speech to text features only support diarization for single-channel audio. Multichannel audio that you used with conversation transcription multichannel diarization isn't supported.

### January 2025 release

#### New Feature - Semantic Segmentation
Announcing the release of a new feature: Semantic Segmentation. This feature integrates a punctuation module inside decoder that segments audio based on semantic information, resulting in more logical and precise segmentation boundaries.
Key Benefits:
- Improved Segmentation Accuracy: By using semantic information, this feature significantly reduces instances of long segments caused by the absence of pauses in the input audio.
- Reduce latency caused by under-segmentation: The overall latency for speech recognition is reduced, with a 40%-60% reduction in the length of the longest 5% of segments.
- Over-Segmentation Mitigation: This feature also helps prevent over-segmentation by delaying segmentation when a better sentence can be formed.

Supported Locales:
- English (en-US, en-GB)
- Chinese (zh-CN, zh-HK)
- Japanese (ja-JP)
- Korean (ko-KR)
- German (de-DE)
- French (fr-FR)
- Italian (it-IT)
- Spanish (es-ES, es-MX)
- Hindi (hi-IN)
- Portuguese (pt-BR, pt-PT)
- Turkish (tr-TR)
- Russian (ru-RU)
- Thai (th-TH)
- Indonesian (id-ID)

For implementation details, please refer to the documentation: [How to Recognize Speech](/azure/ai-services/speech-service/how-to-recognize-speech?pivots=programming-language-csharp) in the "Semantic Segmentation" section.

#### Real-time speech to text - New English model release

Announcing the release of the latest English speech model (en-US, en-CA), which brings substantial improvements across various performance metrics. Below are the key highlights of this release:
- Accessibility Enhancements: Achieved a 36% reduction in Word Error Rate (WER) on Microsoft internal accessibility test sets, making speech recognition more accurate and reliable for recognizing speech from individuals with speech disabilities.
- Ghost Word Reduction: A remarkable 90% reduction in ghost words on the ghost word development set and reductions range from 63% to 100% across other ghost word datasets, significantly enhancing the clarity and accuracy of transcriptions.

The new model also improved the overall performance, including entity recognition and better recognition of spelled-out letters.

These advancements are expected to provide a more accurate, efficient, and satisfying experience for all users. The new model is available through the API and Microsoft Foundry playground. Feedback is encouraged to further refine its capabilities.

### November 2024 release

#### Speech to text REST API version 2024-11-15

The speech to text REST API version 2024-11-15 is released for general availability. For more information, see the [speech to text REST API reference documentation](https://go.microsoft.com/fwlink/?linkid=2296107) and the [Speech to text REST API guide](../../rest-speech-to-text.md).

> [!NOTE]
> The speech to text REST API version 2024-05-15-preview is deprecated.

#### Fast transcription (GA)

Fast transcription is now generally available via [speech to text REST API version 2024-11-15](https://go.microsoft.com/fwlink/?linkid=2296107). Fast transcription allows you to transcribe audio file to text accurately and synchronously, with a high speed factor. It can transcribe audio faster than the actual audio duration. For more information, see the [fast transcription API guide](../../fast-transcription-create.md).

### October 2024 release

#### Real-time speech to text (bilingual)

Significant improvements have been made the recognition quality of short Spanish terms via the `es-US` bilingual models. The model is bilingual and also supports English. The quality of English recognition is also improved.

#### Video translation (Preview)

The video translation API is now available in public preview. For more information, see the [How to use video translation](../../video-translation-get-started.md?pivots=rest-api).

### September 2024 release

#### Real-time speech to text

[Real-time speech to text](../../how-to-recognize-speech.md) has released new models, with better quality, for the following languages.

fi-FI/id-ID/zh-TW/pl-PL/pt-PT
es-SV/es-EC/es-BO/es-PY/es-AR/es-DO/es-UY/es-CR/es-VE/es-NI/es-HN/es-PR/es-CO/es-CL/es-CU/es-PE/es-PA/es-GT/es-GQ

#### Fast transcription (Preview)
Fast transcription now supports diarization to recognize and separate multiple speakers on mono channel audio file. For more information, see [fast transcription API guide](../../fast-transcription-create.md#use-the-fast-transcription-api).

### August 2024 release

#### Language learning (Preview)

Language learning is now available in public preview. Interactive language learning can make your learning experience more engaging and effective. For more information, see [Interactive language learning with pronunciation assessment](../../language-learning-with-pronunciation-assessment.md).

#### Pronunciation assessment

Speech [pronunciation assessment](../../how-to-pronunciation-assessment.md) now supports 33 languages generally available, and each language is available on all Speech to text [regions](../../regions.md#regions). For more information, see the full [language list for Pronunciation assessment](../../language-support.md?tabs=pronunciation-assessment).

| Language | Locale (BCP-47) |
|--|--|
|Arabic (Egypt)|`ar-EG` |
|Arabic (Saudi Arabia)|`ar-SA` |
|Catalan|`ca-ES`|
|Chinese (Cantonese, Traditional)|`zh-HK`|
|Chinese (Mandarin, Simplified)|`zh-CN`|
|Chinese (Taiwanese Mandarin, Traditional)|`zh-TW`|
|Danish (Denmark)|`da-DK`|
|Dutch (Netherlands)|`nl-NL`|
|English (Australia)|`en-AU`|
|English (Canada)|`en-CA` |
|English (India)|`en-IN` |
|English (United Kingdom)|`en-GB`|
|English (United States)|`en-US`|
|Finnish (Finland)|`fi-FI`|
|French (Canada)|`fr-CA`|
|French (France)|`fr-FR`|
|German (Germany)|`de-DE`|
|Hindi (India)|`hi-IN`|
|Italian (Italy)|`it-IT`|
|Japanese (Japan)|`ja-JP`|
|Korean (Korea)|`ko-KR`|
|Malay (Malaysia)|`ms-MY`|
|Norwegian Bokmål (Norway)|`nb-NO`|
|Polish (Poland)|`pl-PL`|
|Portuguese (Brazil)|`pt-BR`|
|Portuguese (Portugal)|`pt-PT`|
|Russian (Russia)|`ru-RU`|
|Spanish (Mexico)|`es-MX` |
|Spanish (Spain)|`es-ES` |
|Swedish (Sweden)|`sv-SE`|
|Tamil (India)|`ta-IN` |
|Thai (Thailand)|`th-TH` |
|Vietnamese (Vietnam)|`vi-VN` |


### July 2024 release

#### Fast Transcription API (Preview)

Fast transcription is now available in public preview. Fast transcription allows you to transcribe audio file to text accurately and synchronously, with a high speed factor. It can transcribe audio faster than the actual audio duration. For more information, see the [fast transcription API guide](../../fast-transcription-create.md).

> [!TIP]
> Try out fast transcription in the [Microsoft Foundry portal](https://aka.ms/fasttranscription/studio).

### June 2024 release

#### Speech to text REST API v3.2 general availability

The Speech to text REST API version 3.2 is now generally available. For more information about speech to text REST API v3.2, see the [Speech to text REST API v3.2 reference documentation](/rest/api/speechtotext/operation-groups?view=rest-speechtotext-v3.2&preserve-view=true) and the [Speech to text REST API guide](../../rest-speech-to-text.md).

> [!NOTE]
> Preview versions *3.2-preview.1* and *3.2-preview.2* are retired as of September 2024.

[Speech to text REST API](../../rest-speech-to-text.md) v3.1 will be retired on a date to be announced. Speech to text REST API v3.0 will be retired on March 31st, 2026. For more information about upgrading, see the Speech to text REST API [v3.0 to v3.1](../../migrate-v3-0-to-v3-1.md) and [v3.1 to v3.2](../../migrate-v3-1-to-v3-2.md) migration guides.


### May 2024 release

#### Video translation (Preview)

Video translation is now available in public preview. Video translation is a feature in Azure Speech in Foundry Tools that enables you to seamlessly translate and generate videos in multiple languages automatically. This feature is designed to help you localize your video content to cater to diverse audiences around the globe. You can efficiently create immersive, localized videos across various use cases such as vlogs, education, news, enterprise training, advertising, film, TV shows, and more. For more information, see the [video translation overview](../../video-translation-overview.md).

#### Pronunciation Assessment

Speech [Pronunciation Assessment](../../how-to-pronunciation-assessment.md) now supports 24 languages generally available (with one new language added), with 7 more languages available in public preview. For more information, see the full [language list for Pronunciation Assessment](../../language-support.md?tabs=pronunciation-assessment).

### April 2024 release

#### Automatic multi-lingual speech translation (Preview)

Automatic multi-lingual speech translation is available in public preview. This innovative feature revolutionizes the way language barriers are overcome, offering unparalleled capabilities for seamless communication across diverse linguistic landscapes.

##### Key Highlights

- Unspecified input language: Multi-lingual speech translation can receive audio in a wide range of languages, and there's no need to specify what the expected input language is. It makes it an invaluable feature to understand and collaborate across global contexts without the need for presetting.
- Language switching: Multi-lingual speech translation allows for multiple languages to be spoken during the same session, and have them all translated into the same target language. There's no need to restart a session when the input language changes or any other actions by you.

##### How it works

- Travel interpreter: multi-lingual speech translation can enhance the experience of tourists visiting foreign destinations by providing them with information and assistance in their preferred language. Hotel concierge services, guided tours, and visitor centers can utilize this technology to cater to diverse linguistic needs.
- International conferences: multi-lingual speech translation can facilitate communication among participants from different regions who might speak various languages using live translated caption. Attendees can speak in their native languages without needing to specify them, ensuring seamless understanding and collaboration.
- Educational meetings: In multi-cultural classrooms or online learning environments, multi-lingual speech translation can support language diversity among students and teachers. It allows for seamless communication and participation without the need to specify each student's or instructor's language.

##### How to access

For a detailed introduction, visit [Speech translation overview](../../speech-translation.md). Additionally, you can refer to the code samples at [how to translate speech](../../how-to-translate-speech.md). This new feature is fully supported by all SDK versions from 1.37.0 onwards.

#### Real-time speech to text with diariazation (GA)

Real-time speech to text with diariazation is now generally available.

You can create speech to text applications that use diarization to distinguish between the different speakers who participate in the conversation. For more information about real-time diarization, Check out the [real-time diarization quickstart](../../get-started-stt-diarization.md).

#### Speech to text model Update

[Real-time speech to text](../../how-to-recognize-speech.md) has released new models with bilingual capabilities. The `en-IN` model now supports both English and Hindi bilingual scenarios and offers improved accuracy. Arabic locales (`ar-AE`, `ar-BH`, `ar-DZ`, `ar-IL`, `ar-IQ`, `ar-KW`, `ar-LB`, `ar-LY`, `ar-MA`, `ar-OM`, `ar-PS`, `ar-QA`, `ar-SA`, `ar-SY`, `ar-TN`, `ar-YE`) are now equipped with bilingual support for English, enhanced accuracy and call center support.

[Batch transcription](../../batch-transcription.md) provides models with new architecture for these locales: `es-ES`, `es-MX`, `fr-FR`, `it-IT`, `ja-JP`, `ko-KR`, `pt-BR`, and `zh-CN`. These models significantly enhance readability and entity recognition.

### March 2024 release

#### Whisper general availability (GA)

The Whisper speech to text model with Azure Speech is now generally available.

Check out [What is the Whisper model?](../../whisper-overview.md) to learn more about when to use Azure Speech vs. Azure OpenAI in Microsoft Foundry Models.

### February 2024 release

#### Pronunciation Assessment

- Speech [Pronunciation Assessment](../../how-to-pronunciation-assessment.md) now supports 23 languages generally available (with 5 new languages added), with 3 more languages available in public preview. For more information, see the full [language list for Pronunciation Assessment](../../language-support.md?tabs=pronunciation-assessment).

#### Phrase list

Added phrase list support for the following locales: ar-SA, de-CH, en-IE, en-ZA, es-US, id-ID, nl-NL, pl-PL, pt-PT, ru-RU, sv-SE, th-TH, vi-VN, zh-HK, zh-TW.

### November 2023 release

#### Introducing Bilingual Speech Modeling!
We're thrilled to unveil a groundbreaking addition to our real-time speech modeling—Bilingual Speech Modeling. This significant enhancement allows our speech model to seamlessly support bilingual language pairs, such as English and Spanish, as well as English and French. This feature empowers users to effortlessly switch between languages during real-time interactions, marking a pivotal moment in our commitment to enhancing communication experiences.

Key Highlights:
- Bilingual Support: With our latest release, users can seamlessly switch between English and Spanish or between English and French during real-time speech interactions. This functionality is tailored to accommodate bilingual speakers who frequently transition between these two languages.
- Enhanced User Experience: Bilingual speakers, whether at work, home, or in various community settings, will find this feature immensely beneficial. The model's ability to comprehend and respond to both English and Spanish in real time opens up new possibilities for effective and fluid communication.

How to Use:

Choose es-US (Spanish and English) or fr-CA (French and English) when you call the Speech Service API or try it out on Speech Studio. Feel free to speak either language or mix them together—the model is designed to adapt dynamically, providing accurate and context-aware responses in both languages.

It's time to elevate your communication game with our latest feature release—seamless, multi-lingual communication at your fingertips!

#### Speech To text models update

We're excited to introduce a significant update to our speech models, promising enhanced accuracy, improved readability, and refined entity recognition. This upgrade comes with a robust new structure, bolstered by an expanded training dataset, ensuring a marked advancement in overall performance. It includes newly released models for en-US, zh-CN, ja-JP, it-IT, pt-BR, es-MX, es-ES, fr-FR, de-DE, ko-KR, tr-TR, sv-SE, and he-IL.

Highlights:
- Better accuracy with new model structure: The redefined model structure, coupled with a richer training dataset, elevates accuracy levels, promising more precise speech output.
- Readability improvement: Our latest model brings a substantial boost to readability, enhancing the coherence and clarity of spoken content.
- Advanced entity recognition: Entity recognition receives a substantial upgrade, resulting in more accurate and nuanced results.

Potential impacts: Despite these advancements, it's crucial to be mindful of potential impacts:
- Custom Silences Time-out Feature: Users employing custom silence time-out, especially with low settings, might encounter over-segmentation and potential omissions of single-word phrases.
- The new model might exhibit compatibility issues with the Keyword prefix feature, and users are advised to assess its performance in their specific applications.
- Reduced disfluency words or phrases: Users might notice a reduction in disfluency words or phrases like "um" or "uh" in the speech output.
- Inaccuracies in word timestamp duration: Some disfluency words might display inaccuracies in timestamp duration, requiring attention in applications dependent on precise timing.
- Confidence score distribution variance: Users relying on confidence scores and associated thresholds should be aware of potential variations in distribution, necessitating adjustments for optimal performance.
- The accuracy enhancement of the phrase list feature might be affected by the misrecognition of certain phrases.

We encourage you to explore these improvements and consider potential issues for a seamless transition, and as always, your feedback is instrumental in refining and advancing our services.

#### Pronunciation Assessment

- Speech [Pronunciation Assessment](../../how-to-pronunciation-assessment.md) now supports 18 languages generally available, with six more languages available in public preview. For more information, see the full [language list for Pronunciation Assessment](../../language-support.md?tabs=pronunciation-assessment).

- We're excited to announce that Pronunciation Assessment is introducing new features starting November 1, 2023: Prosody, Grammar, Vocabulary, and Topic. These enhancements aim to provide an even more comprehensive language learning experience for both reading and speaking assessments. Upgrade to SDK version 1.35.0 or later to explore further details in the [How to use pronunciation assessment](../../how-to-pronunciation-assessment.md) and [Pronunciation assessment in Speech Studio](../../pronunciation-assessment-tool.md).

### September 2023 release

#### Whisper public preview

Azure Speech now supports OpenAI's Whisper model via the batch transcription API. To learn more, check out the [Create a batch transcription](../../batch-transcription-create.md#use-a-whisper-model) guide.

> [!NOTE]
> Azure OpenAI also supports OpenAI's Whisper model for speech to text with a synchronous REST API. To learn more, check out the [quickstart](../../../../ai-foundry/openai/whisper-quickstart.md).

Check out [What is the Whisper model?](../../whisper-overview.md) to learn more about when to use Azure Speech vs. Azure OpenAI.

#### Speech to text REST API v3.2 public preview

Speech to text REST API v3.2 is available in preview. [Speech to text REST API](../../rest-speech-to-text.md) v3.1 is generally available. Speech to text REST API v3.0 will be retired on March 31st, 2026. For more information, see the Speech to text REST API [v3.0 to v3.1](../../migrate-v3-0-to-v3-1.md) and [v3.1 to v3.2](../../migrate-v3-1-to-v3-2.md) migration guides.

### August 2023 release

#### New Speech to text-locales:

Speech to text supports two new locales as shown in the following table. Refer to the complete language list [here](../../language-support.md?tabs=stt).

| Locale  | Language                          |
|---------|-----------------------------------|
| `pa-IN`         | Punjabi (India) |
| `ur-IN`        | Urdu (India)  |

#### Pronunciation Assessment

- Speech [Pronunciation Assessment](../../how-to-pronunciation-assessment.md) now supports 3 additional languages generally available in English (Canada), English (India), and French (Canada), with 3 additional languages available in preview. For more information, see the full [language list for Pronunciation Assessment](../../language-support.md?tabs=pronunciation-assessment).

### May 2023 release

#### Pronunciation Assessment

- Speech [Pronunciation Assessment](../../how-to-pronunciation-assessment.md) now supports 3 additional languages generally available in German (Germany), Japanese (Japan), and Spanish (Mexico), with 4 additional languages available in preview. For more information, see the full [language list for Pronunciation Assessment](../../language-support.md?tabs=pronunciation-assessment).
- You can now use the standard Speech to Text commitment tier for pronunciation assessment on all public regions. If you purchase a commitment tier for standard Speech to text, the spend for pronunciation assessment goes towards meeting the commitment. See [commitment tier pricing](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services).

### February 2023 release

#### Pronunciation Assessment

- Speech [Pronunciation Assessment](../../how-to-pronunciation-assessment.md) now supports 5 additional languages generally available in English (United Kingdom), English (Australia), French (France), Spanish (Spain), and Chinese (Mandarin, Simplified), with other languages available in preview.
- Added sample codes showing how to use Pronunciation Assessment in streaming mode in your own application.
  - **C#**: See [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/csharp/sharedcontent/console/speech_recognition_samples.cs#:~:text=PronunciationAssessmentWithStream).
  - **C++**: See [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/cpp/windows/console/samples/speech_recognition_samples.cpp#:~:text=PronunciationAssessmentWithStream).
  - **java**: See [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/java/android/sdkdemo/app/src/main/java/com/microsoft/cognitiveservices/speech/samples/sdkdemo/MainActivity.java#L548).
  - **javascript**: See [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/js/node).
  - **Objective-C**: See [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/objective-c/ios/speech-samples/speech-samples/ViewController.m#L831).
  - **Python**: See [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/python/console/speech_sample.py#L915).
  - **Swift**: See [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/swift/ios).

#### Custom speech

Support for audio + human-labeled transcript is added for the `de-AT` locales.

### January 2023 release

#### Custom speech

Support for audio + human-labeled transcript is added for additional locales: `ar-BH`, `ar-DZ`, `ar-EG`, `ar-MA`, `ar-SA`, `ar-TN`, `ar-YE`, and `ja-JP`.

Support for structured text adaptation is added for locale `de-AT`.

### December 2022 release

#### Speech to text REST API

The Speech to text REST API version 3.1 is generally available. Version 3.0 of the [Speech to text REST API](../../rest-speech-to-text.md) will be retired. For more information about how to migrate, see the [guide](../../migrate-v3-0-to-v3-1.md).

### October 2022 release

#### New speech to text locale

Added support for Malayalam (India) with the `ml-IN` locale. See the complete language list [here](../../language-support.md?tabs=stt).


### July 2022 release

#### New Speech to text-locales:

Added 7 new locales as shown in the following table. See the complete language list [here](../../language-support.md?tabs=stt).

| Locale  | Language                          |
|---------|-----------------------------------|
| `bs-BA`         | Bosnian (Bosnia and Herzegovina) |
| `yue-CN`        | Chinese (Cantonese, Simplified)  |
| `zh-CN-sichuan` | Chinese (Southwestern Mandarin, Simplified) |
| `wuu-CN`        | Chinese (Wu, Simplified)  |
| `ps-AF`         | Pashto (Afghanistan)      |
| `so-SO`         | Somali (Somalia)          |
| `cy-GB`         | Welsh (United Kingdom)    |


### June 2022 release

#### New Speech to text-locales:

Added 10 new locales as shown in the following table. See the complete language list [here](../../language-support.md?tabs=stt).

| Locale  | Language                          |
|---------|-----------------------------------|
| `sq-AL`         | Albanian (Albania)                |
|  `hy-AM`         | Armenian (Armenia)                |
|  `az-AZ`         | Azerbaijani (Azerbaijan)          |
|  `eu-ES`         | Basque                    |
|  `gl-ES`         | Galician                  |
| `ka-GE`         | Georgian (Georgia)                |
|  `it-CH`         | Italian (Switzerland)             |
|  `kk-KZ`         | Kazakh (Kazakhstan)               |
|  `mn-MN`         | Mongolian (Mongolia)              |
|  `ne-NP`         | Nepali (Nepal)                    |


### April 2022 release

#### New Speech to text-locales:

Below is a list of the new locales. See the complete language list [here](../../language-support.md?tabs=stt).

| Locale  | Language                          |
|---------|-----------------------------------|
| `bn-IN` | Bengali (India)                   |


### January 2022 release

#### New Speech to text-locales:

Below is a list of the new locales. See the complete language list [here](../../language-support.md?tabs=stt).

| Locale  | Language                          |
|---------|-----------------------------------|
| `af-ZA` | Afrikaans (South Africa)            |
| `am-ET` | Amharic (Ethiopia)            |
| `de-CH` | German (Switzerland)            |
| `fr-BE` | French (Belgium)            |
| `is-IS` | Icelandic (Iceland)            |
| `jv-ID` | Javanese (Indonesia)            |
| `km-KH` | Khmer (Cambodia)            |
| `kn-IN` | Kannada (India)            |
| `lo-LA` | Lao (Laos)            |
| `mk-MK` | Macedonian (North Macedonia)            |
| `my-MM` | Burmese (Myanmar)            |
| `nl-BE` | Dutch (Belgium)            |
| `si-LK` | Sinhala (Sri Lanka)            |
| `sr-RS` | Serbian (Serbia)            |
| `sw-TZ` | Swahili (Tanzania)            |
| `uk-UA` | Ukrainian (Ukraine)            |
| `uz-UZ` | Uzbek (Uzbekistan)            |
| `zu-ZA` | Zulu (South Africa)            |


### July 2021 release

#### New Speech to text-locales:

Below is a list of the new locales. See the complete language list [here](../../language-support.md?tabs=stt).

| Locale  | Language                          |
|---------|-----------------------------------|
| `ar-DZ` | Arabic (Algeria)            |
| `ar-LY` | Arabic (Libya)            |
| `ar-MA` | Arabic (Morocco)            |
| `ar-TN` | Arabic (Tunisia)            |
| `ar-YE` | Arabic (Yemen)            |
| `bg-BG` | Bulgarian (Bulgaria)            |
| `el-GR` | Greek (Greece)            |
| `et-EE` | Estonian (Estonia)            |
| `fa-IR` | Persian  (Iran)            |
| `ga-IE` | Irish (Ireland)            |
| `hr-HR` | Croatian (Croatia)            |
| `lt-LT` | Lithuanian (Lithuania)            |
| `lv-LV` | Latvian (Latvia)            |
| `mt-MT` | Maltese (Malta)            |
| `ro-RO` | Romanian (Romania)            |
| `sk-SK` | Slovak (Slovakia)            |
| `sl-SI` | Slovenian (Slovenia)            |
| `sw-KE` | Swahili  (Kenya)            |


### January 2021 release

#### New Speech to text-locales:

Below is a list of the new locales. See the complete language list [here](../../language-support.md?tabs=stt).

| Locale  | Language                          |
|---------|-----------------------------------|
| `ar-AE` | Arabic (United Arab Emirates)            |
| `ar-IL` | Arabic (Israel)            |
| `ar-IQ` | Arabic (Iraq)            |
| `ar-OM` | Arabic (Oman)            |
| `ar-PS` | Arabic (Palestinian Authority)            |
| `de-AT` | German (Austria)            |
| `en-GH` | English (Ghana)            |
| `en-KE` | English (Kenya)               |
| `en-NG` | English (Nigeria)            |
| `en-TZ` | English (Tanzania)            |
| `es-GQ` | Spanish (Equatorial Guinea)            |
| `fil-PH` | Filipino  (Philippines)            |
| `fr-CH` | French  (Switzerland)            |
| `he-IL` | Hebrew  (Israel)            |
| `id-ID` | Indonesian  (Indonesia)            |
| `ms-MY` | Malay  (Malaysia)            |
| `vi-VN` | Vietnamese  (Vietnam)            |

### August 2020 Release

#### New speech to text locales:
Speech to text released 26 new locales in August: 2 European languages `cs-CZ` and `hu-HU`, 5 English locales and 19 Spanish locales that cover most South American countries/regions. Below is a list of the new locales. See the complete language list [here](../../language-support.md?tabs=stt).

| Locale  | Language                          |
|---------|-----------------------------------|
| `cs-CZ` | Czech (Czech Republic)            |
| `en-HK` | English (Hong Kong Special Administrative Region)               |
| `en-IE` | English (Ireland)                 |
| `en-PH` | English (Philippines)             |
| `en-SG` | English (Singapore)               |
| `en-ZA` | English (South Africa)            |
| `es-AR` | Spanish (Argentina)               |
| `es-BO` | Spanish (Bolivia)                 |
| `es-CL` | Spanish (Chile)                   |
| `es-CO` | Spanish (Colombia)                |
| `es-CR` | Spanish (Costa Rica)              |
| `es-CU` | Spanish (Cuba)                    |
| `es-DO` | Spanish (Dominican Republic)      |
| `es-EC` | Spanish (Ecuador)                 |
| `es-GT` | Spanish (Guatemala)               |
| `es-HN` | Spanish (Honduras)                |
| `es-NI` | Spanish (Nicaragua)               |
| `es-PA` | Spanish (Panama)                  |
| `es-PE` | Spanish (Peru)                    |
| `es-PR` | Spanish (Puerto Rico)             |
| `es-PY` | Spanish (Paraguay)                |
| `es-SV` | Spanish (El Salvador)             |
| `es-US` | Spanish (USA)                     |
| `es-UY` | Spanish (Uruguay)                 |
| `es-VE` | Spanish (Venezuela)               |
| `hu-HU` | Hungarian (Hungary)               |
