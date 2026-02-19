---
title: Prompt Shields in Microsoft Foundry
description: Learn how Prompt Shields in Microsoft Foundry detect and block user prompt attacks and document attacks on your model deployments and agents.
author: ssalgadodev
ms.author: ssalgado
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: concept-article
ms.date: 02/13/2026
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

# Prompt Shields in Microsoft Foundry

::: moniker range="foundry"

Prompt Shields detect and prevent attempts to manipulate your model's behavior through adversarial inputs. The feature protects against two types of attacks:

- **User prompt attacks** — Malicious prompts that attempt to bypass system instructions or safety training. Scanned at the **user input** intervention point.
- **Document attacks** — Hidden instructions embedded in third-party content (documents, emails, web pages) that try to hijack the model session. Scanned at the **user input** and **tool response** intervention points.

Prompt Shields are part of the [Foundry guardrails and controls system](../../default/guardrails/guardrails-overview.md). You can enable them when [configuring guardrail controls](../../default/guardrails/how-to-create-guardrails.md) for your model deployments or agents. When enabled, each request returns annotation results with `detected` (true/false) and `filtered` (true/false) values.

[!INCLUDE [prompt-shield-attack-info](../../../ai-services/content-safety/includes/prompt-shield-attack-info.md)]

::: moniker-end

::: moniker range="foundry-classic"

Prompt Shields detect and prevent attempts to manipulate your model's behavior through adversarial inputs. The feature protects against two types of attacks:

- **User prompt attacks** — Malicious prompts that attempt to bypass system instructions or safety training.
- **Document attacks** — Hidden instructions embedded in third-party content (documents, emails, web pages) that try to hijack the model session.

Prompt Shields are part of the Azure OpenAI content filtering system. You can enable them when [configuring content filters](../../openai/how-to/content-filters.md) for your deployments. When enabled, each request returns annotation results with `detected` (true/false) and `filtered` (true/false) values.

[!INCLUDE [prompt-shield-attack-info](../../../ai-services/content-safety/includes/prompt-shield-attack-info.md)]

::: moniker-end

## Spotlighting (preview)

Spotlighting enhances protection against indirect attacks by tagging the input documents with special formatting to indicate lower trust to the model. When enabled, the service transforms document content using base-64 encoding so the model treats it as less trustworthy than direct user and system prompts. This helps prevent the model from executing unintended commands found in third-party documents.

Spotlighting is turned off by default. You can enable it when [configuring guardrail controls](../../default/guardrails/how-to-create-guardrails.md) in the Foundry portal or through the REST API. Once enabled, it transforms document content using base-64 encoding so the model treats it as less trustworthy than direct user and system prompts. Spotlighting is only available for models used via the Chat Completions API.

There's no direct cost for spotlighting, but it adds tokens to user and system prompts, which can increase total costs. Spotlighting can also cause large documents to exceed input size limits.

> [!NOTE]
> An occasional known side effect of spotlighting is the model response mentioning that the document content was base-64 encoded, even when neither the user nor the system prompt asked about encodings.

## Next steps

- [Guardrails and controls overview](../../default/guardrails/guardrails-overview.md)
- [Configure guardrails and controls](../../default/guardrails/how-to-create-guardrails.md)
- [Guardrail annotations](content-filter-annotations.md)
- [Harm categories and severity levels](content-filter-severity-levels.md)
- [Content filtering](../../foundry-models/concepts/content-filter.md)
