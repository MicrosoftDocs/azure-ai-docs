---
manager: mcleans
author: PatrickFarley
ms.author: pafarley
ms.service: azure-speech-foundry-tools
ms.topic: include
ms.date: 09/09/2026
ai-usage: ai-assisted
---

## Feature availability

This table shows transcription features that the fast transcription API supports, with and without LLM Speech, and with MAI-Transcribe-2:

The MAI-Transcribe-2 column shows only MAI-Transcribe-2 capabilities. For supported model versions and model-specific configuration options, see [MAI-Transcribe in Azure Speech](../mai-transcribe.md).

| Feature                  | Fast transcription (default)     | LLM Speech (enhanced) | MAI-Transcribe-2          |
|--------------------------|----------------------------------|-----------------------|---------------------------|
| Transcription            | ✅ (transcription Speech models) | ✅ (multimodal model) | ✅ (speech-to-text model) |
| Translation              | ❌                               | ✅ (multimodal model) | ❌                        |
| Diarization              | ✅                               | ✅                    | ✅                        |
| Channel (stereo)         | ✅                               | ✅                    | ❌                        |
| Profanity filtering      | ✅                               | ✅                    | ✅                        |
| Specify locale           | ✅                               | ✅                    | ✅                        |
| Custom prompting         | ❌                               | ✅                    | ❌                        |
| Phrase list              | ✅                               | ✅                    | ✅                        |
| Segment-level timestamps | ✅                               | ✅                    | ✅                        |
| Word-level timestamps    | ✅                               | ✅                    | ✅                        |


