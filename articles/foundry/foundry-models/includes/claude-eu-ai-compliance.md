---
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: include
ms.date: 09/01/2026
ms.author: mopeakande
author: msakande
---

> [!IMPORTANT]
> The following Claude models comply with the **EU watermarking** standard: `claude-mythos-5-1`, `claude-fable-5-1`, and `claude-fable-5`.
> While `claude-fable-5` uses single-key watermarking, `claude-mythos-5-1` and `claude-fable-5-1` use double key (interwoven 2-key and C2PA) as follows:
> 
> - **Interwoven text watermarking (second key)**: a second key is added for interwoven watermark detection per EU standards. Watermarking happens server-side at generation time; there is no change to request or response shapes. A separate watermark detection API is in early access and isn't part of the Foundry launch scope.
> - **C2PA watermarking**: C2PA content-provenance marking, handled server/client-side by Anthropic surfaces. No API shape change.