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

::: moniker-end

::: moniker range="foundry-classic"

Prompt Shields detect and prevent attempts to manipulate your model's behavior through adversarial inputs. The feature protects against two types of attacks:

- **User prompt attacks** — Malicious prompts that attempt to bypass system instructions or safety training.
- **Document attacks** — Hidden instructions embedded in third-party content (documents, emails, web pages) that try to hijack the model session.

Prompt Shields are part of the Azure OpenAI content filtering system. You can enable them when [configuring content filters](../../openai/how-to/content-filters.md) for your deployments. When enabled, each request returns annotation results with `detected` (true/false) and `filtered` (true/false) values.

[!INCLUDE [prompt-shield-attack-info](../../../ai-services/content-safety/includes/prompt-shield-attack-info.md)]

::: moniker-end

## Spotlighting (preview)

Spotlighting provides enhanced protection when your application processes untrusted third-party documents that might contain embedded malicious instructions. Use Spotlighting when you need an additional defense layer beyond standard document attack detection, especially for applications that handle user-uploaded files or external web content.

### How it works

Spotlighting tags input documents with special formatting to indicate lower trust to the model. The service transforms document content using base-64 encoding so the model treats it as less trustworthy than direct user and system prompts. This helps prevent the model from executing unintended commands found in third-party documents.

### Cost and limitations

There's no direct cost for spotlighting, but it increases document tokens by approximately 30-40% due to base-64 encoding, which can increase total costs. Spotlighting can also cause large documents to exceed input size limits. Spotlighting is only available for models used via the Chat Completions API.

### Enable Spotlighting

Spotlighting is turned off by default. You can enable it when [configuring guardrail controls](../../default/guardrails/how-to-create-guardrails.md) in the Foundry portal or through the REST API by enabling the **Spotlighting** toggle when configuring document attack controls.

> [!NOTE]
> An occasional known side effect of spotlighting is the model response mentioning that the document content was base-64 encoded, even when neither the user nor the system prompt asked about encodings.

## Configure Prompt Shields

### Using the Foundry portal

1. In the Foundry portal, navigate to your project.
2. Select **Guardrails** from the left navigation.
3. Select **Create guardrail**.
4. Choose **User prompt attack** or **Document attack** from the risk dropdown.
5. Select intervention points (user input, tool response) and action (annotate or block).
6. For Spotlighting, enable the **Spotlighting** toggle when configuring document attack controls.
7. Assign the guardrail to your model deployments or agents.

For detailed configuration steps, see [Configure guardrails and controls](../../default/guardrails/how-to-create-guardrails.md).

### Using the REST API

```http
POST https://{endpoint}/openai/deployments/{deployment-id}/chat/completions?api-version=2024-10-01-preview
Content-Type: application/json
api-key: {key}

{
  "messages": [{"role": "user", "content": "Hello"}],
  "data_sources": [{...}],
  "prompt_shield": {
    "user_prompt": {
      "enabled": true,
      "action": "annotate"
    },
    "documents": {
      "enabled": true,
      "action": "block",
      "spotlighting_enabled": true
    }
  }
}
```

## Troubleshooting

### Prompt Shields not detecting expected attacks

- Verify the guardrail is assigned to your deployment or agent
- Check intervention points match where attacks occur (user input vs tool response)
- Review annotation results to see detected vs filtered status

### False positives

- Adjust from "block" to "annotate" mode to log without filtering
- Review specific attack subtypes triggering false positives
- Consider exempting trusted input sources from document attack scanning

### Spotlighting causing encoding references in responses

- This is a known side effect when Spotlighting is enabled
- Consider disabling Spotlighting if encoding mentions disrupt user experience
- Use system prompts to instruct the model to avoid mentioning encodings

## Related guardrail resources

- [Guardrails and controls overview](../../default/guardrails/guardrails-overview.md)
- [Configure guardrails and controls](../../default/guardrails/how-to-create-guardrails.md)
- [Guardrail annotations](content-filter-annotations.md)
- [Harm categories and severity levels](content-filter-severity-levels.md)
- [Content filtering](../../foundry-models/concepts/content-filter.md)
