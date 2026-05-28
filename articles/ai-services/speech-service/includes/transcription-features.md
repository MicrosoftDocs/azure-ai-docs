---
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 02/16/2026
ai-usage: ai-assisted
---

## Feature availability

This table shows transcription features that the fast transcription API supports, with and without LLM Speech:

| Feature             | Fast transcription (default)      | LLM Speech (enhanced)           | MAI-transcribe         |
|---------------------|-----------------------------------|---------------------------------|-------------------------|
| Transcription       | ✅ (transcription Speech models)  | ✅ (multimodal model)           | ✅ (multimodal model)  |
| Translation         | ❌                                | ✅ (multimodal model)           | ❌                     |
| Diarization         | ✅                                | ✅                              | ❌                     |
| Channel (stereo)    | ✅                                | ✅                              | ❌                     |
| Profanity filtering | ✅                                | ✅                              | ✅                     |
| Specify locale      | ✅                                | ✅                              | ✅                     |
| Custom prompting    | ❌                                | ✅                              | ❌                     |
| Phrase list         | ✅                                | ❌<sup>1</sup>                  | ❌                     |
| Segment-level timestamps         | ✅                                | ✅                 | ✅                     |
| Word-level timestamps         | ✅                                | ✅                 | ❌                     |

<sup>1</sup>For LLM Speech, use prompting to guide the output style instead of using explicit phrase list.
