---
title: Known issue for reasoning tokens
description: Include file
author: msakande
ms.author: mopeakande
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: include
ms.date: 06/04/2026
ms.custom: include
ai-usage: ai-assisted
---
> [!NOTE]
> **Known issue:** For Foundry Models (non-Azure OpenAI models), such as DeepSeek-R1-0528, the reasoning summary text on each `reasoning` output item is populated reliably, but the reasoning token count in the response usage details (`reasoning_tokens` on the wire) currently reports `0` even when summary text is present. Don't rely on the reasoning token count for billing or quota accounting when using Foundry models. This caveat *doesn't apply to Azure OpenAI in Foundry Models*.