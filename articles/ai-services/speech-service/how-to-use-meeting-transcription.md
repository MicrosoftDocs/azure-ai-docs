---
title: Real-time conversation transcription multichannel diarization quickstart - Speech service
titleSuffix: Azure AI services
description: In this quickstart, learn how to transcribe meetings. You can add, remove, and identify multiple participants by streaming audio to the Speech service.
author: eric-urban
manager: nitinme
ms.service: azure-ai-speech
ms.topic: quickstart
ms.date: 9/9/2024
ms.author: eur
zone_pivot_groups: acs-js-csharp-python
ms.custom: cogserv-non-critical-speech, references_regions, devx-track-extended-java, devx-track-js, devx-track-python
---

# Quickstart: Real-time conversation transcription multichannel diarization (preview)

> [!NOTE]
> This feature is currently in public preview. This preview is provided without a service-level agreement, and is not recommended for production workloads. Certain features might not be supported or might have constrained capabilities. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

With conversation transcription multichannel diarization, you can transcribe meetings with the ability to add, remove, and identify multiple participants by streaming audio to the Speech service. You first create voice signatures for each participant using the REST API, and then use the voice signatures with the Speech SDK to transcribe meetings. See the conversation transcription [overview](meeting-transcription.md) for more information.

> [!IMPORTANT]
> Conversation transcription multichannel diarization (preview) is retiring on March 28, 2025. For more information about migrating to other speech to text features, see [Migrate away from conversation transcription multichannel diarization](meeting-transcription.md#migrate-away-from-conversation-transcription-multichannel-diarization).

## Limitations

* Only available in the following subscription regions: `centralus`, `eastasia`, `eastus`, `westeurope`
* Requires a 7-mic circular multi-microphone array. The microphone array should meet [our specification](./speech-sdk-microphone.md).

> [!NOTE]
> For the conversation transcription multichannel diarization feature, use `MeetingTranscriber` instead of `ConversationTranscriber`, and use `CreateMeetingAsync` instead of `CreateConversationAsync`. 

::: zone pivot="programming-language-javascript"
[!INCLUDE [JavaScript Basics include](includes/how-to/meeting-transcription/real-time-javascript.md)]
::: zone-end

::: zone pivot="programming-language-csharp"
[!INCLUDE [C# Basics include](includes/how-to/meeting-transcription/real-time-csharp.md)]
::: zone-end

::: zone pivot="programming-language-python"
[!INCLUDE [Python Basics include](includes/how-to/meeting-transcription/real-time-python.md)]
::: zone-end

## Related content

- [Try the real-time diarization quickstart](get-started-stt-diarization.md)
- [Try batch transcription with diarization](batch-transcription.md)