---
title: Transparency note and use cases for Pronunciation Assessment
titleSuffix: Foundry Tools
description: This Transparency Note discusses Pronunciation Assessment and the key considerations for making use of this technology responsibly.
author: PatrickFarley
ms.author: pafarley 
manager: nitinme
ms.service: azure-ai-speech
ms.topic: concept-article
ms.date: 05/17/2021
---

# Transparency Note

[!INCLUDE [non-english-translation](../../includes/non-english-translation.md)]

An AI system includes not only the technology, but also the people who will use it, the people who will be affected by it, and the environment in which it is deployed. Creating a system that is fit for its intended purpose requires an understanding of how the technology works, its capabilities and limitations, and how to achieve the best performance.

Microsoft provides *Transparency Notes* to help you understand how our AI technology works. This includes the choices system owners can make that influence system performance and behavior, and the importance of thinking about the whole system, including the technology, the people, and the environment. You can use Transparency Notes when developing or deploying your own system, or share them with the people who will use or be affected by your system.

Transparency Notes are part of a broader effort at Microsoft to put our AI principles into practice. To find out more, see [Microsoft's AI principles](https://www.microsoft.com/ai/responsible-ai).

## Introduction to Pronunciation Assessment

The [Pronunciation Assessment](/azure/ai-services/speech-service/speech-to-text) API takes audio inputs to evaluate speech pronunciation and gives speakers feedback on accuracy, fluency, and completeness of spoken audio. Pronunciation Assessment feature also includes more comprehensive feedback on various aspects of speech prosody, vocabulary usage, grammar correctness, and topic understanding, providing you with a detailed evaluation of your language skills. Both scripted and unscripted assessments are supported, making it easier for you to assess your pronunciation and language proficiency. Pronunciation Assessment supports a broad range of [languages](/azure/ai-services/speech-service/language-support?tabs=pronunciation-assessment#pronunciation-assessment).

With Pronunciation Assessment, language learners can practice, get instant feedback, and improve their pronunciation so that they can speak and present with confidence. Educators can use Pronunciation Assessment to evaluate the pronunciation of multiple speakers in real time.

## The basics of Pronunciation Assessment

The Pronunciation Assessment API offers speech evaluation results using a machine learning-based approach that closely aligns with speech assessments conducted by native experts. It provides valuable feedback on pronunciation, fluency, prosody, vocabulary usage, grammar correctness, and topic understanding, helping you enhance their language skills and confidently communicate in a new language. The Pronunciation Assessment model was trained with 100,000+ hours of speech data from native speakers. It can provide accurate results when people miss, repeat, or add phrases compared to the reference text. It also enables rich configuration parameters to support flexibility in using the API, such as setting **Granularity** to change information granularity in evaluation. (For more information, see more in [sample code](/azure/ai-services/speech-service/rest-speech-to-text#pronunciation-assessment-parameters).)

Pronunciation Assessment evaluates multiple aspects of pronunciation and content: accuracy, fluency, completeness, prosody, vocabulary usage, grammar correctness, and topic understanding. It also provides evaluations at multiple levels of granularity and returns accuracy scores for specific phonemes, syllables, words, sentences, or even whole articles. For more information, see [how to use Speech SDK for Pronunciation Assessment features](/azure/ai-services/speech-service/how-to-pronunciation-assessment?pivots=programming-language-csharp).

The following table describes the key results. For more information, see the full [response parameters](/azure/ai-services/speech-service/rest-speech-to-text#response-parameters). By using [natural language processing (NLP)](https://en.wikipedia.org/wiki/Natural_language_processing) techniques and the **EnableMiscue** settings, Pronunciation Assessment can detect errors such as extra, missing, or repeated words when compared to the reference text. This information helps obtain more accurate scoring to be used as diagnosis information. This capability is useful for longer paragraphs of text.

|     Parameter             |   Description                |
|---------------------------|----------------------------------------------------|
| `AccuracyScore`     | Pronunciation accuracy of the speech. Accuracy indicates how closely the phonemes match a native speaker's pronunciation. Syllable, word, and full text accuracy scores are aggregated from phoneme-level accuracy score, and refined with assessment objectives. |
| `FluencyScore`       | Fluency of the given speech. Fluency indicates how closely the speech matches a native speaker's use of silent breaks between words. |
| `CompletenessScore`  | Completeness of the speech, calculated by the ratio of pronounced words to the input reference text. |
| `ProsodyScore`       | Prosody of the given speech. Prosody indicates how natural the given speech is, including stress, intonation, speaking speed, and rhythm. |
| `PronScore`          | Overall score indicating the pronunciation quality of the given speech. This is aggregated from AccuracyScore, FluencyScore, and CompletenessScore with weight. |
| `ErrorType`          | This value indicates whether a word is omitted, inserted, badly pronounced, improperly inserted with a break, missing a break at punctuation, or monotonically rising, falling, or flat on the utterance, compared to ReferenceText. Possible values are `None` (meaning no error on this word), `Omission`, `Insertion`, `Mispronunciation`, `UnexpectedBreak`, `MissingBreak`, and `Monotone`. |

Another set of parameters returned by Pronunciation Assessment are Offset and Duration (referred to together as the “timestamp”) The timestamp of speech is returned in structured JSON format. Pronunciation Assessment can calculate pronunciation errors on each phoneme. Pronunciation Assessment can also flag the errors to specific timestamps in the input audio. Customers developing applications can use the signal to offer a learning path to help students focus on the error in multiple ways. For example, the application can highlight the original speech, reply to the audio to compare it with standard pronunciation, or recommend similar words to practice with.

|     Parameter     |     Description                                                                                           |
|-------------------|-----------------------------------------------------------------------------------------------------------|
|     Offset        |     The time   (in 100-nanosecond units) at which the recognized speech begins in the audio   stream.     |
|     Duration      |     The duration (in 100-nanosecond units) of the recognized speech in the audio stream.                |

## Example use cases

Pronunciation Assessment can be used for [remote learning](https://techcommunity.microsoft.com/t5/azure-ai/improve-remote-learning-with-speech-enabled-apps-powered-by/ba-p/1612807), exam practice, or other scenarios that demand pronunciation feedback. The following examples are use cases that are deployed or that we've designed for customers using pronunciation Assessment:
- **Educational service provider**: Providers can build applications with the use of Pronunciation Assessment to help students practice language learning remotely with real-time feedback. This use case is typical when an application needs to support real-time feedback. We support [streaming upload](/azure/ai-services/speech-service/how-to-pronunciation-assessment#pronunciation-assessment-in-streaming-mode) on audio files for immediate feedback.
- **Education in a game**:  App developers, for example, can build a language learning app by combining comprehensive lessons in games with state-of-the-art speech technology to help children learn English. The program can cover a wide range of English skills, such as speaking, reading, and listening, and also train children on grammar and vocabulary, with Pronunciation Assessment used to support children as they learn to speak English. These multiple learning formats ensure that children learn English with ease based on a fun learning style.
- **Education in a communication app**: Microsoft Teams Reading Progress assists the teacher in evaluating a student's speaking assignment with autodetection assistance for omission, insertion, and mispronunciation. It also enables students to practice pronunciation more conveniently before they submit their homework. Microsoft Teams Speaker Progress as a Learning Accelerator cab can also help support students in developing presentation and public speaking skills.

## Considerations when choosing other use cases

Online learning has grown rapidly as schools and organizations adapt to new ways of connecting and methods of education. Speech technology can play a significant role in making distance learning more engaging and accessible to students of all backgrounds. With Foundry Tools, developers can quickly add speech capabilities to applications, bringing online learning to life.

One key element in language learning is improving pronunciation skills. For new language learners, practicing pronunciation and getting timely feedback are essential to becoming a more fluent speaker. For the solution provider that seeks to support learners or students in language learning, the ability to practice anytime, anywhere by using Pronunciation Assessment would be a good fit for this scenario. It can also be integrated as a virtual assistant for teachers and help to improve their efficiency.

The following recommendations pertain to use cases where Pronunciation Assessment should be used carefully:
- **Include a human-in-the-loop for any formal examination scenarios**: Pronunciation Assessment system is powered by AI systems, and external factors like voice quality and background noise may impact the accuracy. A human-in-the-loop in formal examinations ensures the assessment results are as expected.
- **Consider using different thresholds per scenario**: Currently, the Pronunciation Assessment score only represents the similarity distance to the native speakers used to train the model. Such similarity distance can be mapped toward different scenarios with rule-based conditions or weighted counting to help provide pronunciation feedback. For example, the grading method for children's learning might not be as strict as that for adult learning. Consider setting a higher mispronunciation detection threshold for adult learning. 
- **Consider the ability to account for miscues**:  When the scenario involves reading long paragraphs, users are likely to find it hard to follow the reference text without making mistakes. These mistakes, including omission, insertion, and repetition, are counted as miscues. With **EnableMiscue** enabled, the pronounced words will be compared to the reference text, and will be marked with Omission, Insertion, Repetition based on the comparison.

[!INCLUDE [regulatory-considerations](../../includes/regulatory-considerations.md)]

