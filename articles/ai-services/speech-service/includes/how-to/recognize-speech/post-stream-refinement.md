---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 03/30/2026
ms.author: pafarley
---

## Post-stream refinement (preview)

Post-stream refinement improves final transcript accuracy by running a second recognition pass in parallel with real-time streaming. Intermediate and partial results remain low-latency. Only the final result is replaced with a more accurate version that uses broader audio context.

To enable post-stream refinement, set the `SpeechServiceResponse_PostProcessingOption` property on the `SpeechConfig` instance:

::: zone pivot="programming-language-cpp"

```cpp
speechConfig->SetProperty(PropertyId::SpeechServiceResponse_PostProcessingOption, "PostRefinement");
```

::: zone-end

::: zone pivot="programming-language-csharp"

```csharp
speechConfig.SetProperty(PropertyId.SpeechServiceResponse_PostProcessingOption, "PostRefinement");
```

::: zone-end

::: zone pivot="programming-language-java"

```java
speechConfig.setProperty(PropertyId.SpeechServiceResponse_PostProcessingOption, "PostRefinement");
```

::: zone-end

::: zone pivot="programming-language-python"

```python
speech_config.set_property(
    speechsdk.PropertyId.SpeechServiceResponse_PostProcessingOption,
    "PostRefinement"
)
```

::: zone-end

Some important considerations for post-stream refinement:

- Post-stream refinement works best for longer utterances such as conversations, meetings, and dictation. For very short phrases, the refined result might be identical to the standard result.
- Post-stream refinement and semantic segmentation can't be used together.
- Post-stream refinement and TrueText are separate values of the same `SpeechServiceResponse_PostProcessingOption` property. Only one value can be set at a time.

For more information about post-processing options, see [How to use post-processing](../../../how-to-post-processing.md).

> [!IMPORTANT]
> Post-stream refinement is currently in public preview. Accuracy improvements vary by language and locale. Some locales might not show significant quality gains, and results can differ from what you observe with standard recognition. Only monolingual recognition is supported during preview. Multilingual and automatic language identification aren't available with post-stream refinement.
