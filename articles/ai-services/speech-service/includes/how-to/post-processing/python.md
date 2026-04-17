---
author: emilyjiji
ms.service: azure-ai-speech
ms.topic: include
ms.date: 03/30/2026
ms.author: emilyjiji
---

## Change post-processing option

[!INCLUDE [intro](intro.md)]

**Example:** To enable TrueText post-processing:

```python
speech_config.set_property(property_id=speechsdk.PropertyId.SpeechServiceResponse_PostProcessingOption, value="TrueText")
```
