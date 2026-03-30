---
title: "Prompt Shields in Microsoft Foundry"
description: "Learn how Prompt Shields in Microsoft Foundry detect and block user prompt attacks and document attacks on your model deployments and agents."
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
  - doc-kit-assisted
---

# Prompt Shields in Microsoft Foundry

Prompt Shields detect and prevent attempts to manipulate your model's behavior through adversarial inputs. The feature protects against two types of attacks:

- **User prompt attacks** — Malicious prompts that attempt to bypass system instructions or safety training. Scanned at the **user input** intervention point.
- **Document attacks** — Hidden instructions embedded in third-party content (documents, emails, web pages) that try to hijack the model session. Scanned at the **user input** and **tool response** intervention points.

Prompt Shields are part of the [Foundry guardrails and controls system](../../guardrails/guardrails-overview.md). You can enable them when [configuring guardrail controls](../../guardrails/how-to-create-guardrails.md) for your model deployments or agents. When enabled, each request returns annotation results with `detected` (true/false) and `filtered` (true/false) values.

Example response structure:

```json
{
  "choices": [...],
  "prompt_filter_results": [{
    "prompt_index": 0,
    "content_filter_results": {
      "jailbreak": {
        "filtered": false,
        "detected": true
      }
    }
  }]
}
```

[!INCLUDE [prompt-shield-attack-info](../../../ai-services/content-safety/includes/prompt-shield-attack-info.md)]

[!INCLUDE [content-filter-prompt-shields 1](../includes/concepts-content-filter-prompt-shields-1.md)]
