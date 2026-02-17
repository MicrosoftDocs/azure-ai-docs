---
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 02/17/2026
ai-usage: ai-assisted
---

## Feature availability

This table shows which transcription features are supported by the fast transcription API, with and without LLM speech (enhanced mode):

| Feature    | Fast Transcription (default) | LLM Speech (enhanced)        |
|----------------------|-------------------|--------------------|
| Transcription        | ✅ (transcription Speech models) | ✅ (multimodal model) |
| Translation          | ❌                 | ✅ (multimodal model) |
| Diarization          | ✅                 | ✅                 |
| Channel (stereo)     | ✅                 | ✅                 |
| Profanity filtering  | ✅                 | ✅                 |
| Specify locale               | ✅                 | ❌ (use prompting to implement)                |
| Custom prompting               | ❌                 | ✅                 |
| Phrase list          | ✅                 | ❌ (use prompting to implement)                |

For fast transcription mode, specify locale codes to improve accuracy. For LLM speech (enhanced mode), use prompting to guide the output style instead of using explicit locale or phrase lists.