---
title: Include file
description: Include file
author: ssalgadodev
ms.reviewer: sgilley
ms.author: ssalgado
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Spotlighting (preview)

Spotlighting provides enhanced protection against indirect attacks when your application processes third-party documents that might contain embedded malicious instructions. Use Spotlighting when you need an additional defense layer beyond standard document attack detection, especially for applications that handle user-uploaded files or external web content.

### How it works

Spotlighting tags input documents with special formatting to indicate lower trust to the model. The service transforms document content using base-64 encoding so the model treats it as less trustworthy than direct user and system prompts. This helps prevent the model from executing unintended commands found in third-party documents.

### Cost and limitations

There's no direct cost for spotlighting, but it increases document tokens due to base-64 encoding, which can increase total costs. Spotlighting can also cause large documents to exceed input size limits. Spotlighting is only available for models used via the Chat Completions API.

### Enable Spotlighting

Spotlighting is turned off by default. You can enable it when [configuring guardrail controls](../../guardrails/how-to-create-guardrails.md) in the Foundry portal or through the REST API by enabling the **Spotlighting** toggle when configuring document attack controls.

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

For detailed configuration steps, see [Configure guardrails and controls](../../guardrails/how-to-create-guardrails.md).

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

- [Guardrails and controls overview](../../guardrails/guardrails-overview.md)
- [Configure guardrails and controls](../../guardrails/how-to-create-guardrails.md)
- [Guardrail annotations](../../../foundry-classic/openai/concepts/content-filter-annotations.md)
- [Harm categories and severity levels](../concepts/content-filter-severity-levels.md)
- [Content filtering](../../../foundry-classic/foundry-models/concepts/content-filter.md)
