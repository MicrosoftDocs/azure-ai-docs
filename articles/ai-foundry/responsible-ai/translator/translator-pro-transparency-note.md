---
title: Microsoft Translator Pro Transparency Note
titleSuffix: Foundry Tools
description: Microsoft Translator Pro responsible AI Basics, use cases, terms
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-translator
ms.topic: concept-article
ms.date: 01/21/2024
---

# Microsoft Translator Pro Transparency Note

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

An AI system includes not only the technology, but also the people who will use it, the people who will be affected by it, and the environment in which it is deployed. Creating a system that is fit for its intended purpose requires an understanding of how the technology works, what its capabilities and limitations are, and how to achieve the best performance. Microsoft's Transparency Notes are intended to help you understand how our AI technology works, the choices system owners can make that influence system performance and behavior, and the importance of thinking about the whole system, including the technology, the people, and the environment. You can use Transparency Notes when developing or deploying your own system, or share them with the people who will use or be affected by your system.

Microsoft's Transparency Notes are part of a broader effort at Microsoft to put our AI Principles into practice. To find out more, *see* [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai).

## Introduction

Microsoft Translator Pro is a solution for enterprise organizations seeking to overcome language barriers at work during communication. This solution is currently available as mobile app available on the iOS platform.

Enterprise organizations can sign into the Microsoft Translator Pro with their organizational credentials to translate conversations between speech-to-speech conversations. Users can either read a translated message or hear it in their language of choice. The app also allows translation of common phrases using a phrasebook. Following the completion of a conversation, the history can be viewed and optionally exported to the enterprise organization storage account.

## Key terms

|Term|Definition|
|----|----------|
|Speech-to-speech translation| This is the process of converting a voice input into text, translating it to another language as text, and finally, transforming it into speech.|
|Automatic language mode| A microphone's ability to hear two languages, identify which one is being spoken and translate it into another language.|
|Voice input|The audio data of a person speaking into the application.|
|Phrasebook|A set of common phrases organized by categories.|
|Enterprise employee| An employee working in an enterprise organization.|
|External user| A person from outside of the enterprise whom the enterprise employee encounters or communicates with.|
|Text-to-speech| Converting digital text input to speech (spoken output).|
|Embedded languages|Languages that can be accessed offline.|
|Admin settings|Settings that can be accessed by an administrator to manage and configure in an application.|

## Capabilities

The following sections describe the application's general appearance and response in two areas:

* [**System behavior**](#system-behavior)

* [**Use cases**](#use-cases)

### System behavior

* **Speech-to-speech translation via automatic language mode**. In this mode, the app displays a single microphone button with 2 chosen languages, for example English and Spanish. When the microphone button is pressed, the app listens for voice input in both English and Spanish. If the enterprise employee speaks in English, the app will identify the spoken language as English and translate it to Spanish. When the app completes the translation of the voice input, the app will speak the translated message aloud. The external user can then reply to the enterprise employee after hearing the translation. When the user speaks in Spanish, the app will detect the spoken language as Spanish and translate it to English and play the output aloud in English.

* **Translating common phrases**. Users can access a phrasebook that contains categories of common phrases. When a phrase is chosen from the phrasebook, the app can translate the common phrase to the another selected language.

* **Text-to-speech.** The app can converts text into natural-sounding speech.

* **Managing Text-to-speech settings**. Users can choose to enable or disable text-to-speech for a particular language or for both languages if they don't want the app to read the translated messages aloud.

* **Language auto-detection**. The app allows users to identify the language that the other person speaks by requesting them to say a few sentences.

* **Embedded languages**. The app supports offline usage for enterprise users in areas without internet access, offering a limited number of languages (Chinese Mandarin, English, French, German, Italian, Japanese, Russian, Spanish, and Ukrainian).

* **Admin settings**. Administrator settings enable organization administrators to manage and grant permissions for employees to access the app, adjust app configurations, manage conversation history export, and audit logs in the organization storage account.

### Use cases

#### Intended use

Microsoft Translator Pro can be used in multiple scenarios. The system's intended uses include:

* **Speech-to-speech translation**. Use the app to communicate with someone speaking in a different language by seeing and hearing the translation.

* **Conversation history**. Administrators can adjust settings to manage conversation history (audio and transcript) for all employees, such as turning off history or setting it to automatically export to cloud storage. These options are not visible to employees or end users. When an administrator activates the history saving feature, users can then see their conversation history on their devices after a conversation session ends. When an administrator deactivates the history saving feature, then the app will not store any records of past conversations.

* **Communication within workforce**. Enterprise employees can use the app to communicate with external users.

#### Considerations when choosing other use cases

* **Avoid use in public spaces**. When using voice-enabled features in the app in a public spaces, you cannot stop others from speaking near the app. You should advise users to avoid using these features in a public or open place where the app might capture voices of people without their knowledge or consent.

* **Use the app only in scenarios that are within the reasonable expectations of your users**. Audio data that contains someone's voice is sensitive information. The app is not designed for illegal audio surveillance/tracking purposes or in a way that violates legal regulations including places where users might have privacy expectations. Use the app only to translate audio in ways that are consistent with users' expectations. This means making sure you obtain all necessary and appropriate permissions from individuals to collect, process, and store their recorded voice data.

* **Avoid scenarios where use of translation without human review could have consequential impact on life opportunities or legal status**. Before making a decision based on translated material, check with a qualified human reviewer if translation errors might affect someone's legal status, rights, or access to credit, education, work, healthcare, housing, insurance, or social welfare benefits.

* [!INCLUDE [regulatory-considerations](../includes/regulatory-considerations.md)]

#### Unsupported use

* **Translation with speaker recognition**. The app is not designed to provide speaker diarization or speaker recognition and cannot be used to identify individuals. The app does not create voiceprints.

* **Speech-to-speech translation using multiple languages**. The app is not designed to provide translation for more than two languages at a time. The app supports translation when one of the languages is English.

* **Same language transcription**. The app is not designed to provide transcription where both users are speaking the same language.

## Limitations

### Technical limitations, operational factors and ranges

#### Transcription and Translation accuracy

Certain factors may lead to a lower accuracy in transcription and translation:

* **Acoustic quality**: The quality of transcription maybe degraded by how a user speaks into a microphone. Even a mobile device that has a high-quality microphone can impact the quality of translation. For example, if a speaker is located far from the microphone, the input quality can be too low. A speaker who is very close to the microphone can also cause audio quality deterioration. Both cases can affect the accuracy of transcription and translation.

* **Non-speech noise**: If the voice input contains some amount of noise, the accuracy can be affected. Noise can come from the mobile device or the voice input may contain background or environmental noise.

* **Overlapped speech**: The accuracy may be affected if there are multiple speakers within a range of the mobile app and they are speaking in the background at the same time as the main speaker.

* **Domain terminologies**: The app runs on models that have been trained on a wide variety of words in many domains. However, when users speak organization-specific terms and jargon that aren't in a standard vocabulary and for which the model is not trained, there may be an error in transcribing the voice input and lead to a mistranslation.

* **Accents**: The app utilizes models that have been trained on a range of accents. However, the accuracy may be affected when a person speaks into the app with an accent that's not included in the model's training data.

* **Mismatched locales**: If you select English as a language in the app and the user speaks in French, it leads to mistranscription and mistranslation.

* **Biases in translation**:

  * **Gender bias**: When the app translates from a gender-neutral language to a strongly gendered language, accuracy may be affected.

  * **Political or religious bias**: Phrases or word choices with a political bias in one language don't necessarily translate with the same bias or connotation in the another language.

#### Text-to-speech accuracy

Technical limitations to consider when using text-to-speech include the accuracy of pronunciation and intonation. While text-to-speech is designed to generate natural-sounding speech, the app may encounter difficulties with certain words, names, or uncommon phrases. Users should be aware that there can be instances where the system may mispronounce or emphasize words incorrectly, especially when dealing with niche or domain-specific vocabulary.

It is important to note that certain populations may be more negatively impacted by these technical limitations. For example, individuals who are hard of hearing or rely heavily on synthesized speech may face challenges in understanding unclear or distorted speech output. Similarly, users with cognitive or language-related disabilities may find it difficult to comprehend speech with unnatural intonation or mispronounced words.

* **Linguistic limitations**: The app leverages text-to-speech models that have been carefully trained to minimize biases. While text-to-speech supports multiple languages and accents, there may be variations in the quality and availability of voices across different languages. Users should be aware of potential limitations in pronunciation accuracy, intonation, and linguistic nuances specific to certain languages or dialects.

* **Context or emotion**: Text-to-speech may have limitations in accurately conveying contextual information and emotions. Customers and users should be mindful of the system's inability to understand the emotional nuances or subtle cues present in the text. Considerations should be made to provide additional context or utilize other methods to convey emotions effectively.

## System performance

### Best practices for improving system performance

The Microsoft Translator Pro is an integrated end-to-end solution that leverages various services such as speech-to-text, translation, and text-to-speech. Please refer to [speech-to-text](/azure/ai-foundry/responsible-ai/speech-service/speech-to-text/transparency-note) and [text-to-speech](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/transparency-note) transparency notes for more details on the best practices for improving system performance.

## Evaluation of Microsoft Translator Pro

### Evaluation results

The Microsoft Translator Pro is an integrated end-to-end solution that leverages various services such as speech-to-text, translation, and text-to-speech. Please refer to [speech-to-text](/azure/ai-foundry/responsible-ai/speech-service/speech-to-text/transparency-note) and [text-to-speech](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/transparency-note) transparency notes transparency notes for more details on evaluation results.

### Fairness considerations

**At Microsoft, we strive to empower every person on the planet to achieve more**. An essential part of this goal is working to create technologies and products that are fair and inclusive. Fairness is a multidimensional, sociotechnical topic, and it affects many different aspects of our product development. To learn more, *see* [Microsoft approach to fairness](https://www.microsoft.com/ai/responsible-ai?activetab=pivot1%3Aprimaryr6).

One dimension to consider is how well the app performs for different groups of people. Research has shown that without conscious effort focused on improving performance for all groups, it is often possible for the performance of an AI application to vary across groups based on factors such as race, ethnicity, region, gender, and age.

## Learn more about responsible AI

[Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai)

[Microsoft responsible AI resources](https://www.microsoft.com/ai/tools-practices)

[Microsoft Azure Learning courses on responsible AI](/ai/)

About this document

&copy; **2024 Microsoft Corporation**. All rights reserved. This document is provided "as-is" and for informational purposes only. Information and views expressed in this document, including URL and other Internet Web site references, may change without notice. You bear the risk of using it. Some examples are for illustration only and are fictitious. No real association is intended or inferred.

This document is not intended to be, and should not be construed as providing. legal advice. The jurisdiction in which you're operating may have various regulatory or legal requirements that apply to your AI system. Consult a legal specialist if you are uncertain about laws or regulations that might apply to your system, especially if you think those might impact these recommendations. Be aware that not all of these recommendations and resources will be appropriate for every scenario, and conversely, these recommendations and resources may be insufficient for some scenarios.
