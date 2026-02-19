---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 7/16/2025
ms.author: pafarley
---

In this quickstart, you run an application for speech to text transcription with real-time diarization. Diarization distinguishes between the different speakers who participate in the conversation. The Speech service provides information about which speaker was speaking a particular part of transcribed speech. 

The speaker information is included in the result in the speaker ID field. The speaker ID is a generic identifier assigned to each conversation participant by the service during the recognition as different speakers are being identified from the provided audio content.

> [!TIP]
> For fast transcription of audio files, consider using the [fast transcription API.](/azure/ai-services/speech-service/fast-transcription-create) Fast transcription API supports features such as language identification and diarization. 
