---
title: Asynchronous conversation transcription - Speech service
titleSuffix: Azure AI services
description: Learn how to use asynchronous conversation transcription using the Speech service. Available for Java and C# only.
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 9/9/2024
ms.devlang: csharp
ms.custom: cogserv-non-critical-speech, devx-track-csharp, devx-track-extended-java
zone_pivot_groups: programming-languages-set-twenty-one
---

# Asynchronous conversation transcription

> [!NOTE]
> This feature is currently in public preview. This preview is provided without a service-level agreement, and is not recommended for production workloads. Certain features might not be supported or might have constrained capabilities. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

In this article, asynchronous conversation transcription is demonstrated using the **RemoteMeetingTranscriptionClient** API. If you have configured conversation transcription to do asynchronous transcription and have a `meetingId`, you can obtain the transcription associated with that `meetingId` using the **RemoteMeetingTranscriptionClient** API.

> [!IMPORTANT]
> Conversation transcription multichannel diarization (preview) is retiring on March 28, 2025. For more information about migrating to other speech to text features, see [Migrate away from conversation transcription multichannel diarization](#migrate-away-from-conversation-transcription-multichannel-diarization).

## Asynchronous vs. real-time + asynchronous

With asynchronous transcription, you stream the meeting audio, but don't need a transcription returned in real-time. Instead, after the audio is sent, use the `meetingId` of `Meeting` to query for the status of the asynchronous transcription. When the asynchronous transcription is ready, you get a `RemoteMeetingTranscriptionResult`.

With real-time plus asynchronous, you get the transcription in real-time, but also get the transcription by querying with the `meetingId` (similar to asynchronous scenario).

Two steps are required to accomplish asynchronous transcription. The first step is to upload the audio, choosing either asynchronous only or real-time plus asynchronous. The second step is to get the transcription results.

::: zone pivot="programming-language-csharp"
[!INCLUDE [prerequisites](includes/how-to/remote-meeting/csharp/examples.md)]
::: zone-end

::: zone pivot="programming-language-java"
[!INCLUDE [prerequisites](includes/how-to/remote-meeting/java/examples.md)]
::: zone-end


## Related content

- [Try the real-time diarization quickstart](get-started-stt-diarization.md)
- [Try batch transcription with diarization](batch-transcription.md)
