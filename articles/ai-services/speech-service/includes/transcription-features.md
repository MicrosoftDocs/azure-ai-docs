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

This table shows transcription features that the fast transcription API supports, with and without LLM Speech (enhanced mode):

| Feature             | Fast transcription (default)      | LLM Speech (enhanced)          |
|---------------------|-----------------------------------|--------------------------------|
| Transcription       | ✅ (transcription Speech models)  | ✅ (multimodal model)          |
| Translation         | ❌                                | ✅ (multimodal model)          |
| Diarization         | ✅                                | ✅                             |
| Channel (stereo)    | ✅                                | ✅                             |
| Profanity filtering | ✅                                | ✅                             |
| Specify locale      | ✅                                | ❌ (use prompting to implement)|
| Custom prompting    | ❌                                | ✅                             |
| Phrase list         | ✅                                | ❌ (use prompting to implement)|

For LLM Speech, use prompting to guide the output style instead of using explicit locale or phrase lists.
