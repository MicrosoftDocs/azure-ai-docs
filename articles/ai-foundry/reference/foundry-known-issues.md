---
title: Known issues - Microsoft Foundry
titleSuffix: Microsoft Foundry
description: Find known issues, workarounds, and solutions for Microsoft Foundry, including Speech, Translator, and portal services. Review before submitting a support request.
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
ms.service: azure-ai-foundry
ms.topic: troubleshooting-known-issue
ms.date: 02/19/2026
author: s-polly
ms.author: scottpolly
ms.reviewer: bgilmore
---

# Known issues - Microsoft Foundry

[!INCLUDE [version-banner](../includes/version-banner.md)]

This article lists known issues and workarounds for Foundry. Review these issues before you submit a support request.

* Check the [Azure status page](https://status.azure.com/status) for service-level outages.
* Set up outage notifications in the [Azure Service Health portal](/azure/service-health/service-health-portal-update).

:::moniker range="foundry"

## General Foundry known issues 

| Issue ID | Category | Title | Description | Workaround | Issue publish date |
|--------|--------|----|-----------|----------|-------------------|
| 0001   | Foundry portal | Network isolation in new Foundry  | The new Foundry portal experience doesn't support end-to-end network isolation. | When you configure network isolation (disable public network access, enable private endpoints, and use virtual network-injected Agents), you must use the classic Foundry portal experience, the SDK, or CLI to securely access your Foundry projects.  | December 5, 2025 |
| 0002   | Foundry portal | Multiple projects per Foundry resource  | The new Foundry portal experience doesn't support multiple projects per Foundry resource. Each Foundry resource supports only one default project. | None  | December 5, 2025 |

:::moniker-end

## Agent Service

No currently active known issues.

## Foundry Tools

<!-- ### Azure Content Safety in Foundry Tools

No currently active known issues. -->

<!-- ### Azure Content Understanding in Foundry Tools

No currently active known issues. -->

<!-- ### Azure Document Intelligence in Foundry Tools

No currently active known issues. -->

<!-- ### Azure Language in Foundry Tools

No currently active known issues. -->

### Azure Speech in Foundry Tools

The following tables describe the current known issues for Speech, including Speech to Text (STT), Text to Speech (TTS), and Speech SDK/Runtime.

#### Speech to Text (STT) active known issues
The following table lists the current known issues for Speech to Text:

| Issue ID | Category | Title | Description | Workaround | Issue publish date |
|--------|--------|----|-----------|----------|-------------------|
| 1001   | Content | STT transcriptions with pound units | Real-time transcription often converts "pounds" to "lbs" incorrectly when phrases are spoken in a UK dialect, regardless of the language setting. | Use Custom Display Post Processing (DPP) to train a custom speech model to correct default DPP results (for example, Pounds {tab} Pounds). For more information, see [Custom rewrite rules](/azure/ai-services/speech-service/custom-speech-display-text-format). | June 9, 2025 |
| 1002   | Content | STT transcriptions with cardinal directions | The speech recognition model 20241218 might inaccurately interpret audio inputs that include cardinal directions. For example, "SW123456" might be transcribed as "Southwest 123456." Similar errors can occur with other cardinal directions. | Use Custom Display formatting to map "Southwest" to "SW" in a rewrite rule. For more information, see [Custom rewrite rules](/azure/ai-services/speech-service/custom-speech-display-text-format). | June 9, 2025 |
| 1003   | Model | STT transcriptions might include unexpected internal system tags | Unexpected tags like "nsnoise" appear in transcription results. This issue was initially reported for the Arabic model (ar-SA) but also occurs in English models (en-US and en-GB). A future model update adds a filter to remove "nsnoise" from training data. | No workaround is available. A fix is planned in a future model update. | June 9, 2025 |
| 1004   | Model | STT transcriptions with inaccurate spellings of language-specific names and words | Inaccurate transcription of language-specific names due to lack of entity coverage in the base model for tier 2 locales. This issue occurs when base models haven't encountered a specific word before. | Train Custom Speech models to include unknown names and words as training data. You can also add unknown words as a [phrase list](/azure/ai-services/speech-service/improve-accuracy-phrase-list) at runtime to improve recognition accuracy. | June 9, 2025 |
| 1005   | File types | Words out of context added in STT real-time output occasionally | Audio files that consist solely of background noise can result in inaccurate transcriptions. Ideally, only spoken sentences should be transcribed, but this isn't occurring with the nl-NL model. | Use the [Microsoft Audio Stack (MAS)](/azure/ai-services/speech-service/audio-processing-overview) built into the Speech SDK for noise suppression and echo cancellation. This optimization helps improve the audio quality before it reaches the STT service. | June 9, 2025 |
| 1006   | File types | MP4 decoding failure due to 'moov atom' position | Decoding of MP4 container files might fail because the "moov atom" is located at the end of the file instead of the beginning. This structure makes the file unstreamable for the current service, especially for files larger than 10 MB. | Preprocess the file by using audio codec utilities to move the "moov atom" to the beginning, or convert the file to MP3. | August 8, 2025 |

#### Text to Speech (TTS) active known issues

The following table lists the current known issues for Text to Speech:

| Issue ID | Category | Title | Description | Workaround | Issue publish date |
|--------|--------|----|-----------|----------|-------------------|
| 2001   | Service | Model copying via REST API | The TTS service doesn't allow model copying via the REST API for disaster recovery purposes. | No workaround is available. This is a current limitation. | June 9, 2025 |
| 2002   | TTS avatar | Missing parameters | TTS avatar parameters `avatarPosition` and `avatarSize` aren't supported in Batch synthesis. | No workaround is available. This is a current limitation. | June 9, 2025 |
| 2003   | TTS avatar | Missing blob file names | The `outputs: result` URL of Batch avatar synthesis job doesn't include the blob file name. | Use `subtitleType = soft_embedded` as a temporary workaround. | June 9, 2025 |
| 2004   | TTS avatar | Batch synthesis unsupported for TTS avatar | Batch synthesis for avatar doesn't support bring-your-own-storage (BYOS) and requires the storage account to allow external traffic. | No workaround is available. This is a current limitation. | June 9, 2025 |
| 2005   | Service | DNS cache refresh after July 2025 migration | The legacy Speech TTS clusters in Asia were removed on July 31, 2025 for compliance reasons. All traffic migrated to new IPs. Some customers might still experience issues due to persistent local or secondary DNS caches that haven't refreshed. | Clear local and secondary DNS caches to resolve connectivity issues with the new TTS cluster IPs. | July 24, 2025 |
| 2006   | TTS | Word boundary duplication in output | Azure TTS sometimes returns duplicated word boundary entries in the synthesis output, particularly when using certain SSML configurations. This duplication can lead to inaccurate timing data and misalignment in downstream applications. | Post-process the output to filter out duplicate word boundaries based on timestamp and word content. | August 8, 2025 |
| 2007   | TTS | Partially generated words in Arabic voices | Arabic voice outputs contain partially generated words in cases of unclear or incomplete pronunciation, especially for words ending with ة or ت. This problem is reproducible across multiple voices. | To mitigate this problem, consider rephrasing the voice output text. | September 16, 2025 |


#### Speech SDK/Runtime active known issues  

The following table lists the current known issues for Speech SDK/Runtime:

| Issue ID | Category | Title | Description | Workaround | Issue publish date |
|--------|--------|----|-----------|----------|-------------------|
| 3001   | SDK/Runtime | InitialSilenceTimeout parameter causes 400 errors | Setting `InitialSilenceTimeout` to 0 causes 400 errors. The `endSilenceTimeout` parameter might also lead to incorrect transcriptions — when set to a value other than 0, the system disregards user input after the specified duration. | Set `InitialSilenceTimeoutMs` to 0 by using `SpeechConfig.fromSubscription(subscriptionKey, region)` to disable the timeout due to initial silence. For single-shot recognition, the session terminates after 30 seconds of initial silence. For continuous recognition, the service reports an empty phrase after 30 seconds and continues. The `Speech_SegmentationMaximumTimeMs` parameter determines the maximum phrase length (default: 30,000 ms). | June 9, 2025 |
| 3002   | SDK/Runtime | SegmentationTimeout parameter causes false words | Random words appear in Speech recognition results when `SegmentationSilenceTimeout` is set to more than 1,000 ms. | Maintain the default `SegmentationTimeout` value of 650 ms. | June 9, 2025 |
| 3003   | SDK/Runtime | Speaker duration missing during real-time diarization in STT | The Python SDK doesn't show speaker duration when using real-time diarization with STT. | Check offset and duration on the result by following the [Conversation transcription result class](/azure/ai-services/speech-service/how-to-use-conversation-transcription) documentation. | June 9, 2025 |
| 3004   | SDK/TTS avatar | Frequent disconnections with JavaScript SDK | TTS avatar doesn't load or frequently disconnects and reconnects when using a custom avatar with the JavaScript SDK. | Open UDP port 3478. | June 9, 2025 |

### Azure Translator in Foundry Tools

The following tables describe the current known issues for Translator.

#### Text Translation active known issues

| Issue ID | Category | Title | Description | Workaround | Issue publish date |
|--------|--------|----|-----------|----------|-------------------|
| 4001   | Model | Preserving context and pronouns | Some translation models don't handle pronouns well, especially third-person pronouns. This problem occurs because sentence-level training and inference don't preserve context. The product team is actively working to shift all models to document-level training and inference. | No direct workaround is available. Manually review and adjust pronoun usage as needed. | February 5, 2025 |
| 4002   | Content | Translating sentences with mixed-language text | The Text Translation API doesn't support translating sentences that contain mixed-language input. Translations can be incorrect or incomplete when a single sentence includes multiple languages. | Specify the intended source language, remove the mixed-language sentence, or split the text into single-language segments. | February 5, 2025 |

#### Document Translation active known issues

| Issue ID | Category | Title | Description | Workaround | Issue publish date |
|--------|--------|----|-----------|----------|-------------------|
| 5001   | Formatting | Formatting of mathematical expressions | Translated documents might not fully retain the formatting of mathematical expressions. Superscript and subscript numbers can be reformatted incorrectly. | No direct workaround is available. Manually adjust the formatting of mathematical expressions as needed. | February 5, 2025 |
| 5002   | Content | Translating documents with mixed source languages | Document translation might not translate source documents with multiple languages, leading to incorrect or incomplete results. | Specify the intended source language. Alternatively, remove the mixed-language sentence or split the text into segments that contain only one language. | February 5, 2025 |
| 5003   | File types | Translating complex documents | Documents with thousands of intricate pages can encounter failures during the extraction, translation, and reassembly processes. These documents often include images, embedded text within images, and manually typed text. | Split the large document into smaller sections (for example, divide a 1,000-page file into approximately 10 files of 100 pages each) and submit them individually. | February 5, 2025 |
| 5004   | Formatting | Translating documents containing borderless charts and tables | Charts and tables with mixed horizontal and vertical text, varying cell sizes, or borderless grid structures are difficult to format accurately during translation. | Recreate documents by using bordered tables and charts rather than borderless ones to improve translation output quality. | April 1, 2025 |
| 5005   | Content | Translating documents containing visible watermarks or seals | Visible watermarks or seals can overlap with text, making it difficult for the models to accurately recognize and process the content. Documents might remain untranslated or only partially translated. | Use clean, watermark-free documents for optimal translation results. | May 21, 2025 |


<!-- ### Azure Vision in Foundry Tools

No currently active known issues. -->

<!-- ## AI Search

No currently active known issues. -->

<!-- ## Azure OpenAI (Foundry Models)

No currently active known issues. -->

<!-- ## Observability

No currently active known issues. -->

## Azure Machine Learning

For known problems related to Azure Machine Learning, see [Azure Machine Learning known problems](../../machine-learning/known-issues/azure-machine-learning-known-issues.md).


## Related content

* [Azure Service Health portal](/azure/service-health/service-health-portal-update)
* [Azure status overview](/azure/service-health/azure-status-overview)
