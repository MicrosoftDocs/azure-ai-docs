---
title: Azure Speech in Foundry Tools known issues
titlesuffix: Foundry Tools
description: Known and common issues with Azure Speech in Foundry Tools.
manager: heikora
ms.service: azure-ai-speech
ms.topic: reference
ms.date: 10/31/2025
author: PatrickFarley
ms.author: pafarley
---

# Azure Speech in Foundry Tools known issues

Azure Speech is updated regularly and we're continually improving and enhancing its features and capabilities. This page details known issues related to Azure Speech and provides steps to resolve them. Before submitting a support request, review the following list to see if your problem is already being addressed and to find a possible solution.

* For more information regarding service-level outages, *see* the [Azure status page](https://azure.status.microsoft/en-us/status). 
* To set up outage notifications and alerts, *see* the [Azure Service Health Portal](/azure/service-health/service-health-portal-update).

## Active known issues speech to text (STT)

This table lists the current known issues for the Speech to text feature:

|Issue ID|Category|Tile|Description|Workaround|Issues publish date|
|--------|--------|----|-----------|----------|-------------------|
| 1001   | Content | STT transcriptions with pound units | In certain instances, the use of pound units can pose difficulties for transcription. When phrases are spoken in a UK dialect, they're often inaccurately converted during real-time transcription, leading to the term 'pounds' being automatically translated to 'lbs' irrespective of the language setting. | Users can use Custom Display Post Processing (DPP) to train a custom speech model to correct default DPP results (for example, Pounds {tab} Pounds). Refer to [Custom Rewrite Rules](/azure/ai-services/speech-service/how-to-custom-speech-display-text-format#custom-rewrite). | June 9, 2025 |
| 1002   | Content | STT transcriptions with cardinal directions | The speech recognition model 20241218 might inaccurately interpret audio inputs that include cardinal directions, resulting in unexpected transcription outcomes. For instance, an audio file containing "SW123456" might be transcribed as "Southwest 123456," and similar errors can occur with other cardinal directions. | Potential workaround is to use Custom Display formatting where "Southwest" is mapped to "SW" in a rewrite rule: [Custom Rewrite Rules](/azure/ai-services/speech-service/how-to-custom-speech-display-text-format#custom-rewrite). | June 9, 2025 |
| 1003   | Model | STT transcriptions might include unexpected internal system tags. | Unexpected tags like 'nsnoise' have been appearing in transcription results. Initially customers reported this issue for the Arabic model (ar-SA), this issue was also observed in English models (en-US and en-GB). These tags are causing intermittent problems in the transcription outputs. To address this issue, a filter will be added to remove 'nsnoise' from the training data in future model updates. | N/A | June 9, 2025 |
| 1004   | Model | STT transcriptions with inaccurate spellings of language specific names and words | Inaccurate transcription of language specific names due to lack of entity coverage in base model for tier 2 locales (scenario specific to when our base models didn't see a specific word before). | Customers can train [Custom Speech](/azure/ai-services/speech-service/custom-speech-overview) models to include unknown names and words as training data. As a second step, unknown words can be added as [Phrase List](/azure/ai-services/speech-service/improve-accuracy-phrase-list?tabs=terminal&pivots=programming-language-csharp) at runtime. Biasing phrase list to a word known in the training corpus can greatly improve recognition accuracy. | June 9, 2025 |
| 1005   | File types | Words out of context added in STT real time output occasionally | Audio files that consist solely of background noise can result in inaccurate transcriptions. Ideally, only spoken sentences should be transcribed, but this isn't occurring with the nl-NL model. | Audio files that consist of background noise, captured echo reflections from surfaces in an environment or audio playback from a device while device microphone is active can result in inaccurate transcriptions. Customers can use the Microsoft Audio Stack built into the Speech SDK for noise suppression of observed background noise and echo cancellation. This should help optimize the audio being fed to the STT service: [Use the Microsoft Audio Stack (MAS)](/azure/ai-services/speech-service/audio-processing-speech-sdk?tabs=java). | June 9, 2025 |
| 1006  | File types  | MP4 decoding failure due to 'moov atom' position | The decoding of MP4 container files might fail because the "moov atom" is located at the end of the file instead of the beginning. This structure makes the file unstreamable for the current service and the underlying Microsoft MTS service, especially for files larger than 10MB. Supporting such formats would require fundamental changes. | Preprocess the file using audio codec utilities to move the 'moov atom' to the beginning or convert to MP3. | August 8, 2025 |

## Active known issues text to speech (TTS)

This table lists the current known issues for the Text-to-Speech feature.

|Issue ID|Category|Tile|Description|Workaround|Issues publish date|
|--------|--------|----|-----------|----------|-------------------|
| 2001   | Service | Model copying via Rest API | The TTS service doesn't allow model copying via the REST API for disaster recovery purposes. | N/A | June 9, 2025 |
| 2002   | TTS Avatar | Missing parameters | TTS Avatar parameters "avatarPosition" and "avatarSize" not supported in Batch synthesis. | N/A | June 9, 2025 |
| 2003   | TTS Avatar | Missing Blob file names | The 'outputs': 'result' url of Batch avatar synthesis job doesn't have the blob file name. | Customers should use 'subtitleType = soft_embedded' as a temporary workaround. | June 9, 2025 |
| 2004   | TTS Avatar | Batch synthesis unsupported for TTS | Batch synthesis for avatar doesn't support bring your own storage (BYOS) and it requires the storage account to allow external traffic. | N/A | June 9, 2025 |
| 2005   | Service | DNS cache refresh before end of July 2025  | Due to compliance reasons, the legacy Speech TTS clusters in Asia are removed on July 31, 2025. All traffic is migrated from the old IPs to the new ones.<br>Some customers are still accessing the old clusters even after DNS redirection was completed. This indicates that some customers may have persistent local or secondary DNS caches. | To avoid service downtime, refresh the DNS cache before the end of July 2025. | July 24, 2025 |
| 2006  | TTS | Word boundary duplication in output | Azure TTS sometimes returns duplicated word boundary entries in the synthesis output, particularly when using certain SSML configurations. This can lead to inaccurate timing data and misalignment in downstream applications. | Post-process the output to filter out duplicate word boundaries based on timestamp and word content. | August 8, 2025 |
| 2007  | TTS | Partially generated words in Arabic voices | Arabic voice outputs only contain partially generated words in cases of unclear or incomplete pronunciation, especially for words ending with ة or ت. This problem is reproducible across multiple voices. The issue is acknowledged as a known problem without an immediate solution available. | To mitigate the issue consider re-phrasing the voice output, if the issue occurs. | September 16, 2025 |
| 2008  | Service | 503 errors for streaming requests (WebSocket) | When a user starts a text stream request but does not send any text for a long time (e.g., 30 seconds), TTS returns 503 errors. | To mitigate the issue, please start the text streaming call only after receiving the first text token from the LLM. If all text from the LLM has been received but the text streaming call fails, please build an SSML with all the text and send it to TTS with a non-streaming call. | November 10, 2025 |

## Active known issues speech SDK/Runtime

This table lists the current known issues for the Speech SDK/Runtime feature.

|Issue ID|Category|Tile|Description|Workaround|Issues publish date|
|--------|--------|----|-----------|----------|-------------------|
| 3001   | SDK/SR Runtime | Handling of the InitialSilenceTimeout parameter | The issue is related to the handling of the InitialSilenceTimeout parameter. When set to 0, it unexpectedly caused customers to encounter 400 errors. Additionally, the endSilenceTimeout parameter might lead to incorrect transcriptions. When the endSilenceTimeout is set to a value other than "0", the system disregards user input after the specified duration, even if the user continues speaking. Customers want all parts of the conversation to be transcribed, including segments after pauses, to ensure no user input is lost. | The 400 error is due to "InitialSilenceTimeout" parameter not being currently exposed directly in Real-time Speech Recognition endpoint resulting in a failed URL consistency check. To bypass this error, customers can perform the following steps: <br> Adjust their production code to use Region/Key instantiation of SpeechConfig object. <ul> <li>SpeechConfig = fromSubscription (String subscriptionKey, String region); where region is the Azure Region where the Speech resource is located. </li> <li>Set the parameter "InitialSilenceTimeoutMs" to 0, which in effect disables timeout due to initial silence in the recognition audio stream. </li> </ul> Note: For single shot recognition, the session will be terminated after 30 seconds of initial silence. For continuous recognition, the service will report empty phrase after 30 seconds and continue the recognition process. This issue is due to a second parameter "Speech_SegmentationMaximumTimeMs" which determines the maximum length of a phrase and has default value of 30,000 ms. | June 9, 2025 |
| 3002 | SDK/SR Runtime | Handling of SegmentationTimeout parameter | Customers experience random words being generated as part of Speech recognition results (hallucinations) when the SegmentationSilenceTimeout parameter is set to > 1,000 ms. | Customers should maintain the default "SegmentationTimeout" value of 650 ms. | June 9, 2025 |
| 3003   | SDK/SR Runtime | Handling of speaker duration during Real-time diarization in STT | Python SDK not showing duration of speakers when using Real-time diarization with STT. | Check offset and duration on the result following steps on the following Documentation: [Conversation Transcription Result Class](/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.transcription.conversationtranscriptionresult). | June 9, 2025 |
| 3004   | SDK/TTS Avatar | Frequent disconnections with JavaScript SDK | TTS Avatar isn't loading/Frequent disconnections and reconnections of a custom avatar using the JavaScript SDK. | Customers should open the UDP 3478 port. | June 9, 2025 |

## Recently closed known issues

Fixed known issues are organized in this section in descending order by fixed date. Fixed issues are retained for at least 60 days.

## Related content

* [Azure Service Health Portal](/azure/service-health/service-health-portal-update)
* [Azure Status overview](/azure/service-health/azure-status-overview)
* [What's new in Azure Translator in Foundry Tools?](./releasenotes.md)
