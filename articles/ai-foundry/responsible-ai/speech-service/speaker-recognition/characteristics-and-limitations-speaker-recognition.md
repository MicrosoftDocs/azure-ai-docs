---
title: Characteristics and limitations of Speaker Recognition
titleSuffix: Azure AI services
description: Speaker Recognition, also known as voice recognition, is used to verify a speaker's identity by comparing the voice characteristics of incoming speech with their registered voice signatures. This article discusses the characteristics and limitations of the Speaker Recognition service in Azure.
author: HeidiHanZhang
ms.author: heidizh
manager: nitinme
ms.service: azure-ai-speech
ms.topic: article
ms.date: 10/08/2021
---

# Characteristics and limitations of Speaker Recognition

[!INCLUDE [non-english-translation](/azure/ai-foundry/responsible-ai/includes/non-english-translation.md)]

In this section, we'll review what performance means for Speaker Recognition, best practices for improving performance, limitations, and fairness as it relates to the Speaker Recognition feature.

## General performance guidelines

Because Speaker Recognition serves various uses, there's no universally applicable estimate of accuracy for every system. In some cases, such as meeting transcription, Speaker Recognition is a building block that you can combine with other components to create an end-to-end solution. The performance of Speaker Recognition is therefore affected by these other components.

### Accuracy

The accuracy of both speaker verification and speaker identification can be measured by False Rejection Rate (FRR) and False Acceptance Rate (FAR). Developers must balance the trade-off between the rates of FRR and FAR in each specific scenario.

Let's take text-independent speaker verification as an example. The following table shows the possible outcomes where two individuals request access to a building or system that uses Speaker Recognition. These two individuals are *Speaker A* who is enrolled, and an imposter who is claiming to be *Speaker A*. Speaker Recognition tests the audio of speech input against the saved voice signature of *Speaker A*.

| Outcome | Details |
|----|--------|
| Correct accept or true positive| The system correctly accepts an access attempt by *Speaker A*. |
| Correct reject or true negative| The system correctly rejects an access attempt by the imposter. |
|False accept or false positive| The system incorrectly accepts an access attempt by the imposter.|
| False reject or false negative | The system incorrectly rejects an access attempt by *Speaker A*. |

The measurement for Speaker Identification API is similar, except that a speech input is tested against one of multiple known speakers.  

The consequences of a false positive or a false negative will vary depending upon the intended use of the speaker recognition system. The following examples illustrate this variation and the how choices you make in designing the system affect the people who are subject to it. The design of the whole system, including fallback mechanisms, determines the consequences for people when errors occur.

* **Signing into a banking app:** Speaker Recognition can provide an added layer of security in addition to a PIN. A false positive for this application reduces customer security because it results in an incorrect match, while a false negative could prevent the customer from accessing their account. Because the purpose of the banking system is security, system owners will likely want to ensure that false positives are minimized by requiring higher confidence level thresholds. This however, may also result in most errors being made as false negatives (account access fails). To address this limitation, system owners should provide an alternative mechanism for enabling its users to access their application, for example, offering alternative sign-in via an access code notification to the customer's phone. The customer's experience might be less convenient in this case, but account access isn't blocked while security is still prioritized.

* **Receiving personalized content on a smart device:** Personal devices can use Speaker Recognition to respond to the device owner's voice command for personalized content. A false positive increases unnecessary activation, while a false negative might result in no response to the user command. Here, if the purpose of the system is convenience and efficiency and not security, some false positives may be acceptable to the system provider. In this case, false negatives are usually minimized, while most errors will be the result of false positives. Conducting multiple enrollments of the device owner's voice can help Speaker Recognition perform more accurately for that voice over time.

#### Match scores, match thresholds, and matched conditions

System configuration influences system accuracy. By comparing the pre-enrolled speaker profile and input audio, Speaker Recognition outputs a match score to indicate the similarity of the comparison result and uses a threshold to decide whether to accept or reject the input as a match. It's important to understand the trade-off between the rates of false positives and false negatives. The table below gives more details description.

|Term|Definition|
|----|--------|
|Match score or similarity score| Match scores range from 0 to 1. High match scores indicate that it's more likely that the speech input comes from the same person with the enrolled voice signature.|
|Match threshold|A match threshold is a configurable value between 0 and 1 that determines the match score required to be considered a positive match. If the match threshold is set to 0, then the system will accept any match score and the false accept rate would be high; if the match threshold is set to 1, then it will only accept a voice input with a 1 (100%) match score and the false reject rate would be high. Speaker Recognition API has a default match threshold that you can change to suit your application.|

Because the optimal threshold varies highly with use cases or scenarios, the Speaker Verification API decides whether to accept or reject based on a default threshold of 0.5. The threshold is a compromise between the requirements of high security applications and high convenience applications. Adjust the threshold for each scenario and validate the results by testing with your data.

| Outcome | Details |
|----|--------|
| Correct accept or true positive| When the real *Speaker A* requests access as *Speaker A*, the system returns a match score of 0.8, which is above the default threshold of 0.5. The system correctly accepts the access attempt.|
| Correct reject or true negative| When an imposter requests access as *Speaker A*, the system returns 0.2, which is below the default threshold of 0.5. The system correctly rejects the access attempt. |
|False accept or false positive| When an imposter requests access as *Speaker A*, the system returns 0.6, which is above the threshold of 0.5. The system incorrectly accepts the access attempt.|
| False reject or false negative | When the real *Speaker A* requests access as *Speaker A*, the system returns 0.4, which is below the threshold of 0.5. The system incorrectly rejects the access attempt. |

#### How should a match threshold be selected?

The optimal threshold varies greatly according to different scenarios. If the accuracy of results isn't optimal for a particular scenario, you can adjust the default threshold and fine-tune it based on the results of testing on your own data. You can gather real-world data to evaluate if audio samples are labeled with the correct speaker identities. This type of dataset is known as a ground truth evaluation dataset.

You can then feed the evaluation data into Speaker Verification API and keep the returned match scores. Compare ground truth labels to the output of the system. With this evaluation of system performance, you can establish the overall FRR and FAR on the threshold of interest, and the distribution of errors between false positives and false negatives. Ground truth evaluation data should include adequate sampling of diverse people who will be subject to recognition, so that you can understand performance differences between groups of people and take corrective action.

With your evaluation results, you can adjust the threshold to better suit the scenario. For example, because the customer identity verification scenario usually prefers high security over convenience, you might set the threshold higher than the default threshold to reduce false accept errors. By contrast, because the personalization scenario might prefer high convenience over security, you might set the threshold lower than the default to reduce the false reject errors. Based on each evaluation result, you can iteratively adjust the match threshold until the trade-off between false positives and false negatives meets your objectives.

### Best practices to improve accuracy

Here are some specific actions you can take to ensure the best results from your speaker recognition system.

#### Plan for variations in subject and environment

You can improve system accuracy by having matching conditions between the enrollment audio and the recognition audio. Matching conditions means using the same device or microphone, or having a consistent acoustic environment, or a consistent speaking style of the speaker (for example, a reading style versus a conversational style).  

Achieving matching conditions can be difficult. Although Speaker Recognition has been trained with data of various acoustic conditions, it's still better to support multiple enrollments to accommodate varying conditions. The APIs support multiple enrollments, so you can enroll the speaker over time under the range of conditions you expect the system to be used in. Speaker Recognition can create a more robust audio signature with multiple enrollments.

For text-independent verification or identification, the duration of the enrollment or recognition audio input also affects accuracy. Effective speech length measures the total length of speech, excluding silence and non-speech segments. We use a speech detection module to count the total usable amount of audio. For example, a user might send 30 seconds of audio for text-independent enrollment, but the effective speech length might only be 15 seconds. In cases where the speech content of enrollment and recognition is different (text-independent systems), the longer the effective speech, the better the performance. When active enrollment is enabled, the length of the activation phrase at the beginning of the enrollment is counted in the total speech length of enrollment.

#### Meet specifications

The following specifications are important to be aware of:

- **Audio format:** The current system only supports mono channel 16 bit, 16 kHz PCM-encoded WAV. Any data in the 8-kHz sampling rate should be up sampled to 16kHz before being sent to the service.
- **Maximum number of enrolled voices to compare:**  In Speaker Identification API, the speech input is compared to a specified list of enrolled voices. The fewer candidates there are to compare with, the more accurate the result will be. In the current Speaker Identification API, the limit is 50 enrolled voices to compare.

#### Design the system to support human judgment

We recommend using Speaker Recognition capabilities to support people making accurate and efficient judgments, rather than fully automating a process. Meaningful human review is important to:

- Detect and resolve cases of misidentification or other failures.
- Provide support to people who believe their results were incorrect.

For example, in call center scenarios, a legitimate customer can be rejected due to having a sore throat. In this case, a human agent can intervene and help the customer verify their identity by asking security questions.

#### Use multiple factors for authentication

It's always recommended to build multifactor authentication for scenarios that require high security. Using another security factor can help mitigate spoofing attacks.

#### Mitigate the risk of replay (or spoofing) attacks

Speaker Recognition isn't intended to determine whether the audio is from a live person speaking or is an audio recording of an enrolled speaker. For verification scenarios requiring high security, in addition to using speech as a secondary authentication factor, consider mitigations such as generating random phrases for the speaker to read at runtime. This can mitigate the risk of replay attacks or attacks that use a non-parameter-based, synthesized voice.

Your application can send separate requests to the text-independent Speaker Verification API and the speech to text API. By combining these, the application can help confirm the speaker's identity.

## Fairness

At Microsoft, we strive to empower every person on the planet to achieve more. An essential part of this goal is working to create technologies and products that are fair and inclusive. Fairness is a multi-dimensional, sociotechnical topic and impacts many different aspects of our product development. You can learn more about our approach to fairness [here](https://www.microsoft.com/ai/responsible-ai?activetab=pivot1%3aprimaryr6).

One dimension of this goal is to consider how well the system performs for different groups of people. Research has shown that without conscious effort focused on improving performance for all groups, it is often possible for the performance of a system to vary across groups based on factors such as race, ethnicity, region, gender, and age.

We test our systems on various factors, including demographic factors such as gender, ethnicity, and age. Each application is different, and our testing might not perfectly match your context or cover all scenarios required for your use case. We encourage developers to thoroughly evaluate error rates for the service with real-world data that reflects your use case. This should include testing with users from different demographic groups and with different speech characteristics.

For Speaker Recognition, there are some observable differences in performance across languages on some specific datasets. We have tuned and evaluated on eight languages (English, French, Spanish, Chinese, German, Italian, Japanese, and Portuguese) for text-independent verification and identification APIs. You can see more details on Speaker Recognition's language and locale support [here](/azure/ai-services/speech-service/language-support). Speaker Recognition hasn't been tested with data representing minors under the age of 18 or people with speech disorders.

## Evaluating and integrating Speaker Recognition for your use

Before a large-scale deployment or rollout of any speaker recognition system, system owners should conduct an evaluation phase. Do this evaluation in the context where you'll use the system, and with people who will interact with the system. Work with your analytics and research teams to collect ground truth evaluation data to:

1. Establish baseline accuracy, false positive and false negative rates.
2. Choose an appropriate match threshold for your scenario.
3. Determine whether the error distribution is skewed towards specific groups of people.

Evaluation is likely to be an iterative process. For example, you can start with 50 speakers and 20 trials for each speaker. An evaluation should reflect your deployment environment and any variations in that environment, such as microphone channel and noise level. Use ground truth evaluation data that represents a diversity of people and speaker styles.

In addition to analyzing accuracy data, you can also analyze feedback from the people making judgments based on the system output. Further, you can analyze satisfaction data from the people who are subject to recognition, and feedback from existing customer voice channels, to help tune the system and ensure successful engagement.

## Next steps

* [Speaker Recognition overview](/azure/ai-services/speech-service/speaker-recognition-overview)
* [Limited access for Speaker Recognition](/azure/ai-foundry/responsible-ai/speech-service/speaker-recognition/limited-access-speaker-recognition?context=/azure/ai-services/speech-service/context/context)
* [Transparency Note for Speaker Recognition](/azure/ai-foundry/responsible-ai/speech-service/speaker-recognition/transparency-note-speaker-recognition?context=/azure/ai-services/speech-service/context/context)
