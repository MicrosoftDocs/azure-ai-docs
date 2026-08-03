---
author: emilyjiji
ms.service: azure-speech-foundry-tools
ms.topic: include
ms.date: 07/22/2026
ms.author: emilyjiji
ai-usage: ai-assisted
---

The Speech service can apply post-processing to recognition results before they're returned. You can control which post-processing option is used by setting the `SpeechServiceResponse_PostProcessingOption` property on the `SpeechConfig` instance used to create a `SpeechRecognizer`.

The following values are supported:

| Value | Description |
|-------|-------------|
| `TrueText` | Applies display formatting to recognition results, including punctuation and capitalization, to produce more readable output. |
| `PostRefinement` | Gives you more accurate final transcription results with no impact to first-token latency. A second recognition pass runs in parallel with real-time streaming. Intermediate results stay low-latency. Only the final result for each segment is replaced with a more accurate version. Monolingual post-stream refinement is generally available. Multilingual post-stream refinement is in public preview. Region availability differs between the two modes. For more information, see [Speech service regions](../../../regions.md?tabs=stt). |
