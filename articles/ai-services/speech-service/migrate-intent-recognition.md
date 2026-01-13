---
title: Migrate from retired intent recognition in Azure Speech in Foundry Tools
description: Learn about the retirement of intent recognition in Azure Speech in Foundry Tools and how to migrate to Azure Language in Foundry Tools Service or Azure OpenAI.
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 10/31/2025
ai-usage: ai-assisted
author: PatrickFarley
ms.author: pafarley
#Customer intent: As a developer, I want to migrate from Speech IntentRecognizer to an alternative.
---

# Migrate from retired intent recognition

Intent recognition in Azure Speech in Foundry Tools was retired on September 30, 2025. Applications can no longer use intent recognition via Speech. However, you can still perform intent recognition using Azure Language in Foundry Tools Service or Azure OpenAI.

This change doesn't affect other Speech capabilities such as [speech to text](./speech-to-text.md) (including no change to speaker diarization), [text to speech](./text-to-speech.md), and [speech translation](./speech-translation.md).

Speech previously exposed the `IntentRecognizer` object family in the Speech SDK. These APIs depended on a Language Understanding Intelligent Service (LUIS) application or simple pattern matching constructs. With the retirement:

* `IntentRecognizer`, pattern matching intents/entities, and related parameters are no longer available.
* Existing applications must remove direct Speech SDK intent logic and adopt a two-step approach (speech to text, then intent classification) or a single prompt-based approach.

## Choose an alternative

| Requirement | Recommended service | Why |
|-------------|---------------------|-----|
| Structured intent and entity extraction with labeled training data | Language Service Conversational Language Understanding (CLU) | Purpose-built for multi-intent classification and entity extraction; supports versions, testing, and analytics. |
| Few-shot or zero-shot dynamic intent determination | Azure OpenAI | Use GPT models with example prompts; rapidly adapt without schema changes. |
| Combine transcription with generative reasoning (summaries + intents) | Azure OpenAI + Speech | Transcribe audio then enrich with GPT outputs for complex reasoning. |
| Multilingual speech input flowed into consistent intent schema | Speech (STT) + CLU | Speech handles transcription; CLU handles normalization and classification. |

## Migration steps

1. Replace any Speech SDK `IntentRecognizer` usage with `SpeechRecognizer` or `ConversationTranscriber` to obtain text.
2. For structured intent/entity needs, create a CLU project and deploy a model. Send transcribed utterances to the CLU prediction API.
3. For flexible or rapid scenarios, craft a prompt for an Azure OpenAI model including representative user utterances and expected JSON intent output.
4. Remove dependencies on `LanguageUnderstandingModel` and any LUIS application IDs or endpoints from configuration.
5. Eliminate pattern matching code referencing `PatternMatchingIntent` or `PatternMatchingEntity` types.
6. Validate accuracy by comparing historic `IntentRecognizer` outputs to CLU classification results or OpenAI completions, adjusting training data or prompts as needed.
7. Update monitoring: shift any existing intent latency/accuracy dashboards to new sources (CLU evaluation logs or OpenAI prompt result tracking).

## Sample architecture

1. Speech to text transcribes audio into text with real-time or batch mode.
2. Text is sent to CLU or Azure OpenAI depending on your intent strategy.
3. Response is normalized into a common JSON shape (for example: `{ "intent": "BookFlight", "entities": { "Destination": "Seattle" } }`).
4. Business logic routes the normalized output to downstream services (booking, knowledge base, workflow engine).

## Result format considerations

| Aspect | CLU | Azure OpenAI |
|--------|-----|--------------|
| Schema stability | High (defined intents/entities) | Flexible (prompt-defined) |
| Versioning | Built-in model versions | Manual prompt versioning |
| Training effort | Requires labeled dataset | Few-shot examples in prompt |
| Edge cases | Requires more labeled data | Add examples or instructions |
| Latency | Prediction API call | Completion API call (similar) |

## Frequently asked questions

**Do I need to re-label data?** If you used LUIS, you need to export and reimport data into CLU, then retrain. Mapping is often direct (intents, entities). Pattern matching intents might require manual conversion to examples.

**Can I combine CLU and Azure OpenAI?** Yes. Use CLU for deterministic classification and OpenAI for summarization or fallback classification when confidence is low.

**Is speaker diarization affected?** No. Diarization features continue; you just process each speaker segment through CLU or OpenAI after transcription.

## Related links

- [Speech to text](./speech-to-text.md)
- [Conversational Language Understanding overview](../language-service/conversational-language-understanding/overview.md)
- [Azure OpenAI overview](../../ai-foundry/openai/overview.md)
