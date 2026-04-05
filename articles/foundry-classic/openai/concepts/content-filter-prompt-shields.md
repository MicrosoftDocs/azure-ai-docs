---
title: "Prompt Shields in Microsoft Foundry (classic)"
description: "Learn how Prompt Shields in Microsoft Foundry detect and block user prompt attacks and document attacks on your model deployments and agents. (classic)"
author: ssalgadodev
ms.author: ssalgado
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: concept-article
ms.date: 02/13/2026
ai-usage: ai-assisted
ms.custom:
  - classic-and-new
ROBOTS: NOINDEX, NOFOLLOW
---

# Prompt Shields in Microsoft Foundry (classic)

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../../foundry/openai/concepts/content-filter-prompt-shields.md)

Prompt Shields detect and prevent attempts to manipulate your model's behavior through adversarial inputs. The feature protects against two types of attacks:

- **User prompt attacks** — Malicious prompts that attempt to bypass system instructions or safety training.
- **Document attacks** — Hidden instructions embedded in third-party content (documents, emails, web pages) that try to hijack the model session.

Prompt Shields are part of the Azure OpenAI content filtering system. You can enable them when [configuring content filters](../../openai/how-to/content-filters.md) for your deployments. When enabled, each request returns annotation results with `detected` (true/false) and `filtered` (true/false) values.

[!INCLUDE [prompt-shield-attack-info](../../../ai-services/content-safety/includes/prompt-shield-attack-info.md)]

[!INCLUDE [content-filter-prompt-shields 1](../../../foundry/openai/includes/concepts-content-filter-prompt-shields-1.md)]
