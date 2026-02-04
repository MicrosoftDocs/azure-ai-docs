---
title: Microsoft Foundry known issues
titlesuffix: Microsoft Foundry
description: Known and common issues with Microsoft Foundry.
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
ms.service: azure-ai-foundry
ms.topic: troubleshooting-known-issue
ms.date: 02/04/2026
author: s-polly
ms.author: scottpolly
ms.reviewer: bgilmore
---

# Microsoft Foundry known issues

[!INCLUDE [version-banner](../includes/version-banner.md)]

Microsoft Foundry is updated regularly and the product team is continually improving and enhancing its features and capabilities. This article lists known issues related to Foundry and provides steps to resolve them. Before submitting a support request, review the following list to see if your problem is already being addressed and to find a possible solution.

* For more information about service-level outages, *see* the [Azure status page](https://azure.status.microsoft.com/en-us/status). 
* To set up outage notifications and alerts, *see* the [Azure Service Health Portal](/azure/service-health/service-health-portal-update).

:::moniker range="foundry"

## General Foundry known issues 

| Issue ID | Category | Title | Description | Workaround | Issues publish date |
|--------|--------|----|-----------|----------|-------------------|
| 0001   | Foundry Portal |Network isolation in new Foundry  | The new Foundry portal experience doesn't support end-to-end network isolation. | When you configure network isolation (disable public network access, enable private endpoints, and use virtual network-injected Agents), you must use the classic Foundry portal experience, the SDK, or CLI to securely access your Foundry projects.  | December 5, 2025 |
| 0002   | Foundry Portal | Multiple projects per Foundry resource  | The new Foundry portal experience doesn't support multiple projects per Foundry resource. Each Foundry resource supports only one default project. | None  | December 5, 2025 |

:::moniker-end

<!---
## Agent Service

No current active known issues

## Foundry Tools

### AI Content Safety

No current active known issues

### AI Content Understanding

No current active known issues

### AI Document Intelligence

No current active known issues

### AI Language

No current active known issues
--->

### AI Speech

The following tables describe the current known issues for the Speech services, including Speech to Text (STT), Text to Speech (TTS), and Speech SDK/Runtime.

#### Speech to Text (STT) active known issues
This table lists the current known issues for the Speech to text feature:

|Issue ID|Category|Title|Description|Workaround|Issues publish date|
|--------|--------|----|-----------|----------|-------------------|
| 1001   | Content | STT transcriptions with pound units | In certain instances, the use of pounds units can pose difficulties for transcription. When phrases are spoken in a UK dialect, they're often inaccurately converted during real-time transcription, leading to the term "pounds" being automatically translated to "lbs" irrespective of the language setting. | Users can use Custom Display Post Processing (DPP) to train a custom speech model to correct default DPP results (for example, Pounds {tab} Pounds). Refer to Custom Rewrite Rules. | June 9, 2025 |
| 1002   | Content | STT transcriptions with cardinal directions | The speech recognition model 20241218 might inaccurately interpret audio inputs that include cardinal directions, resulting in unexpected transcription outcomes. For instance, an audio file containing "SW123456" might be transcribed as "Southwest 123456", and similar errors can occur with other cardinal directions. | Potential workaround is to use Custom Display formatting where "Southwest" is mapped to "SW" in a rewrite rule: Custom Rewrite Rules. | June 9, 2025 |
| 1003   | Model | STT transcriptions might include unexpected internal system tags. | Unexpected tags like "nsnoise" appear in transcription results. Customers initially reported this issue for the Arabic model (ar-SA), but it's also observed in English models (en-US and en-GB). These tags cause intermittent problems in the transcription outputs. To address this problem, a filter will be added to remove "nsnoise" from the training data in future model updates. | N/A | June 9, 2025 |
| 1004   | Model | STT Transcriptions with inaccurate spellings of language specific names and words | Inaccurate transcription of language specific names due to lack of entity coverage in base model for tier 2 locales (scenario specific to when base models didn't see a specific word before). | Customers can train Custom Speech models to include unknown names and words as training data. As a second step, unknown words can be added as Phrase List at runtime. Biasing phrase list to a word known in the training corpus can greatly improve recognition accuracy. | June 9, 2025 |
| 1005   | File Types | Words out of context added in STT real time output occasionally | Audio files that consist solely of background noise can result in inaccurate transcriptions. Ideally, only spoken sentences should be transcribed, but this isn't occurring with the nl-NL model. | Audio files that consist of background noise, captured echo reflections from surfaces in an environment, or audio playback from a device while device microphone is active can result in inaccurate transcriptions. Customers can use the Microsoft Audio Stack built into the Speech SDK for noise suppression of observed background noise and echo cancellation. This should help optimize the audio being fed to the STT service: Use the Microsoft Audio Stack (MAS). | June 9, 2025 |
| 1006   | Filetypes | MP4 decoding failure due to 'moov atom' position | The decoding of MP4 container files might fail because the "moov atom" is located at the end of the file instead of the beginning. This structure makes the file unstreamable for the current service and the underlying Microsoft MTS service, especially for files larger than 10 MB. Supporting such formats would require fundamental changes. | Preprocess the file using audio codec utilities to move the "moov atom" to the beginning or convert to MP3. | August 8, 2025 |

#### Text to Speech (TTS) active known issues

This table lists the current known issues for the Text-to-Speech feature.

|Issue ID|Category|Title|Description|Workaround|Issues publish date|
|--------|--------|----|-----------|----------|-------------------|
| 2001   | Service | Model copying via Rest API | The TTS service doesn't allow model copying via the REST API for disaster recovery purposes. | N/A | June 9, 2025 |
| 2002   | TTS Avatar | Missing parameters | TTS Avatar parameters "avatarPosition" and "avatarSize" not supported in Batch synthesis. | N/A | June 9, 2025 |
| 2003   | TTS Avatar | Missing Blob file names | The 'outputs': 'result' URL of Batch avatar synthesis job doesn't have the blob file name. | Customers should use 'subtitleType = soft_embedded' as a temporary workaround. | June 9, 2025 |
| 2004   | TTS Avatar | Batch synthesis unsupported for TTS | Batch synthesis for avatar doesn't support bring-your-own-storage (BYOS) and it requires the storage account to allow external traffic. | N/A | June 9, 2025 |
| 2005   | Service | DNS cache refresh before end of July 2025 | Due to compliance reasons, the legacy Speech TTS clusters in Asia are removed on July 31, 2025. All traffic is migrated from the old IPs to the new ones. | Some customers still access the old clusters even after DNS redirection is completed. This behavior indicates that some customers might have persistent local or secondary DNS caches. | July 24, 2025 |
| 2006   | TTS | Word boundary duplication in output | Azure TTS sometimes returns duplicated word boundary entries in the synthesis output, particularly when using certain SSML configurations. This duplication can lead to inaccurate timing data and misalignment in downstream applications. | Post-process the output to filter out duplicate word boundaries based on timestamp and word content. | August 8, 2025 |
| 2007   | TTS | Partially generated words in Arabic voices | Arabic voice outputs only contain partially generated words in cases of unclear or incomplete pronunciation, especially for words ending with  ة or ت. This problem is reproducible across multiple voices. This problem is acknowledged as a known problem without an immediate solution available. | To mitigate the problem, consider rephrasing the voice output, if the problem occurs. | September 16, 2025 |


#### Speech SDK/Runtime active known issues  

This table lists the current known issues for the Speech SDK/Runtime feature.

|Issue ID|Category|Title|Description|Workaround|Issues publish date|
|--------|--------|----|-----------|----------|-------------------|
| 3001   | SDK/SR runtime | Handling of the InitialSilence Timeout parameter | The problem is related to the handling of the InitialSilenceTimeout parameter. When set to 0, it unexpectedly causes customers to encounter 400 errors. Additionally, the endSilenceTimeout parameter might lead to incorrect transcriptions. When the endSilenceTimeout is set to a value other than "0," the system disregards user input after the specified duration, even if the user continues speaking. Customers want all the parts of the conversation to be transcribed, including segments after pauses, to ensure no user input is lost. | The 400 error occurs because the "InitialSilenceTimeout" parameter isn't currently exposed directly in Real-time Speech Recognition endpoint resulting in a failed URL consistency check. To bypass this error, customers can perform the following steps: SpeechConfig = fromSubscription (String subscriptionKey, String region); where region is the Azure Region where the Speech resource is located. Set the parameter "InitialSilenceTimeoutMs" to 0, which in effect disables timeout due to initial silence in the recognition audio stream. Note: For single shot recognition, the session terminates after 30 seconds of initial silence. For continuous recognition, the service reports empty phrase after 30 seconds and continues to recognition process. This problem is due to a second parameter `Speech_Segmentation MaximumTimeMs`, which determines the maximum length of a phrase and has default value of 30,000 ms. | June 9, 2025 |
| 3002   | SDK/SR Runtime | Handling of SegmentationTimeout parameter | Customers experience random words being generated as part of Speech recognition results (incorrect information) when the SegmentationSilenceTimeout parameter is set to > 1,000 ms. | Customers should maintain the default "SegmentationTimeout" value of 650 ms. | June 9, 2025 |
| 3003   | SDK/SR Runtime | Handling of speaker duration during Real-time diarization in STT | Python SDK not showing duration of speakers when using Real-time diarization with STT. | Check offset and duration on the result following steps on the following documentation: Conversation Transcription Result Class. | June 9, 2025 |
| 3004   | SDK/TTS Avatar | Frequent disconnections with JavaScript SDK | TTS Avatar isn't loading/frequent disconnections and reconnection of a custom avatar using the JavaScript SDK. | Customers should open the UDP 3478 port. | June 9, 2025 |

### AI Translator

The following tables describe the current known issues for Azure Translator in Foundry Tools. 

#### Text Translation active known issues

|Issue ID|Category|Title|Description|Workaround|Issues publish date|
|--------|--------|----|-----------|----------|-------------------|
| 1004   | Model | Preserving context and pronouns | Some translation models don't handle pronouns well, especially third-person pronouns. This problem occurs because sentence-level training and inference don't preserve context. The product team is actively working to shift all models to document-level training and inference to preserve the context. | Currently, there's no direct workaround. Manually review and adjust pronoun usage as needed. | February 5, 2025 |
| 1006   | Content | Translating sentences with mixed language text | The Text translation API doesn't support translating sentences that contain mixed language input. As a result, translations can be incorrect or incomplete when a single sentence includes multiple languages. | Specify the intended source language, remove the mixed-language sentence, or split the text into single-language segments. | February 5, 2025 |

#### Document Translation active known issues

|Issue ID|Category|Title|Description|Workaround|Issues publish date|
|--------|--------|----|-----------|----------|-------------------|
| 3001   | Formatting | Formatting of mathematical expressions | In some cases, translated documents don't fully retain the formatting of mathematical expressions. Superscript and subscript numbers can be reformatted incorrectly, leading to discrepancies between expected and actual output. | Currently, there's no direct workaround. Manually adjust the formatting of mathematical expressions as needed. | February 5, 2025 |
| 3007   | Content | Translating documents with mixed source languages | In some cases, document translation doesn't translate source documents with multiple languages leading to incorrect or incomplete results. For example, a sentence that contains more than one language. | To ensure that the desired language is translated to the target language, specify the intended source language. Alternatively, remove the mixed-language sentence, or split the text into segments containing only one language. | February 5, 2025 |
| 3008   | File types | Translating complex documents | Translating documents with thousands of intricate pages can be challenging. These documents often include images, embedded text within images, and manually typed text. As a result, the batch translation request can encounter failures during the extraction, translation, and reassembly processes. | Split the large document into smaller sections (for example, divide a 1,000-page file into approximately 10 files of 100 pages each) and submit them individually for the best results. | February 5, 2025 |
| 3009   | Formatting | Translating documents containing borderless charts and tables | Complex tables and charts can present significant challenges during translation, especially when they're large and intricate. Charts and tables with mixed horizontal and vertical text, varying cell sizes, or grid structures that are borderless, are difficult to format accurately. These types of tables might require added processing to ensure precision without compromising overall performance. | To improve the quality of translation output, consider recreating documents using bordered tables and charts rather than borderless ones. | April 1, 2025 |
| 3010   | Content | Translating documents containing visible watermarks or seals | Documents with visible watermarks or seals can significantly hinder the translation process, as the watermarks might overlap with the text, making it difficult for the models to accurately recognize and process the content. This problem can result in the document remaining untranslated or only partially translated. | For optimal translation results, use clean, watermark-free documents. Files without visible watermarks or seals translate accurately and as expected. | May 21, 2025 |


### AI Vision

No currently active known issues.

## AI Search

No currently active known issues.


## Azure OpenAI (Foundry Models)

No currently active known issues.

## Observability

No currently active known issues.

## Azure Machine Learning

For known problems related to Azure Machine Learning, see [Azure Machine Learning known problems](../../machine-learning/known-issues/azure-machine-learning-known-issues.md).


## Related content

* [Azure Service Health Portal](/azure/service-health/service-health-portal-update)
* [Azure Status overview](/azure/service-health/azure-status-overview)
