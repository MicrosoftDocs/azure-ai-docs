---
author: emilyjiji
ms.service: azure-ai-speech
ms.topic: include
ms.date: 03/30/2026
ms.author: emilyjiji
---

The Speech service can apply post-processing to recognition results before they're returned. You can control which post-processing option is used by setting the `SpeechServiceResponse_PostProcessingOption` property on the `SpeechConfig` instance used to create a `SpeechRecognizer`.

The following values are supported:

| Value | Description |
|-------|-------------|
| `TrueText` | Applies display formatting to recognition results, including punctuation and capitalization, to produce more readable output. |
| `PostRefinement` | Improves final transcript accuracy by running a second recognition pass in parallel with real-time streaming. Intermediate results remain low-latency; only the final result for each segment is replaced with a more accurate version. This option is currently in public preview. |
