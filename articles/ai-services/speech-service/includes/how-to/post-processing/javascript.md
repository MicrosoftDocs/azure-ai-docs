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

```javascript
speechConfig.setProperty(sdk.PropertyId.SpeechServiceResponse_PostProcessingOption, "TrueText");
```
