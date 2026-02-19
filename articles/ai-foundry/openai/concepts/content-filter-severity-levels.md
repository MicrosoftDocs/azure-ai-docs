---
title: 'Harm categories and severity levels in Microsoft Foundry'
titleSuffix: Microsoft Foundry
description: Learn about the harm categories and severity levels used by the content safety system in Microsoft Foundry to detect and filter harmful content.
manager: nitinme
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.date: 02/05/2026
author: ssalgadodev
ms.author: ssalgado
recommendations: false
ms.custom: azure-ai-content-safety
monikerRange: 'foundry-classic || foundry'

# customer intent: As a developer, I want to understand the harm categories and severity levels in Microsoft Foundry so that I can properly handle content filtering in my applications.
---

# Harm categories and severity levels in Microsoft Foundry

[!INCLUDE [version-banner](../../includes/version-banner.md)]

Microsoft Foundry guardrails ensure that AI-generated outputs align with ethical guidelines and safety standards. The content filtering system classifies harmful content into four categories — hate, sexual, violence, and self-harm — each graded at four severity levels (safe, low, medium, and high) for both text and image content. Use these categories and levels to configure guardrail controls that detect and mitigate risks associated with harmful content in your model deployments and agents.

For an overview of how guardrails work, see [Guardrails and controls overview](../../default/guardrails/guardrails-overview.md).

The content safety system uses neural multiclass classification models to detect and filter harmful content for both text and image. Content detected at the "safe" severity level is labeled in annotations but isn't subject to filtering and isn't configurable.

> [!NOTE]
> The text content safety models for the hate, sexual, violence, and self-harm categories are trained and tested on the following languages: English, German, Japanese, Spanish, French, Italian, Portuguese, and Chinese. The service can work in many other languages, but detection accuracy and false positive rates may vary. For production use in other languages, conduct thorough testing to validate performance meets your requirements.

## Harm category descriptions

The following table summarizes the harm categories supported by Foundry guardrails:

| Category | Description |
|----------|-------------|
| **Hate and Fairness** | Hate and fairness-related harms refer to any content that attacks or uses discriminatory language with reference to a person or identity group based on certain differentiating attributes of these groups.<br><br>This category includes, but isn't limited to:<br>• Race, ethnicity, nationality<br>• Gender identity groups and expression<br>• Sexual orientation<br>• Religion<br>• Personal appearance and body size<br>• Disability status<br>• Harassment and bullying |
| **Sexual** | Sexual describes language related to anatomical organs and genitals, romantic relationships and sexual acts, acts portrayed in erotic or affectionate terms, including those portrayed as an assault or a forced sexual violent act against one's will.<br><br>This category includes but isn't limited to:<br>• Vulgar content<br>• Prostitution<br>• Nudity and pornography<br>• Abuse<br>• Child exploitation, child abuse, child grooming |
| **Violence** | Violence describes language related to physical actions intended to hurt, injure, damage, or kill someone or something; describes weapons, guns, and related entities.<br><br>This category includes, but isn't limited to:<br>• Weapons<br>• Bullying and intimidation<br>• Terrorist and violent extremism<br>• Stalking |
| **Self-Harm** | Self-harm describes language related to physical actions intended to purposely hurt, injure, damage one's body or kill oneself.<br><br>This category includes, but isn't limited to:<br>• Eating disorders<br>• Bullying and intimidation |

## Severity levels

The content safety system classifies harmful content at four severity levels:

| Severity level | Description |
|---------------|-------------|
| **Safe** | No harmful material detected. Annotated but never filtered. |
| **Low** | Mild harmful material. Includes prejudiced views, mild depictions in fictional contexts, or personal experiences. |
| **Medium** | Moderate harmful material. Includes graphic depictions, bullying, or content that promotes harmful acts. |
| **High** | Severe harmful material. Includes extremist content, explicit depictions, or content that endorses serious harm. |

### How severity levels map to guardrail configuration

When you configure a guardrail control for a harm category, you set a severity threshold that determines which content is flagged:

| Threshold setting | Behavior |
|-------------------|----------|
| **Off** | Detection is disabled for this category. No content is flagged or blocked. |
| **Low** | Flags content at low severity and higher. Least restrictive setting. |
| **Medium** | Flags content at medium severity and higher. |
| **High** | Flags only the most severe content. Most restrictive setting. |

Content at the "safe" level is always annotated but never blocked, regardless of threshold setting. To configure these thresholds, see [How to configure guardrails and controls](../../default/guardrails/how-to-create-guardrails.md).

### Detailed severity definitions for text

The following tables provide detailed descriptions and examples for each severity level within each harm category for text content. Select the **Severity definitions** tab to view examples.

[!INCLUDE [severity-levels-text-four](../../../ai-services/content-safety/includes/severity-levels-text-four.md)]

### Detailed severity definitions for images

The following tables provide detailed descriptions and examples for each severity level within each harm category for image content. Select the **Severity definitions** tab to view examples.

[!INCLUDE [severity-levels-image](../../../ai-services/content-safety/includes/severity-levels-image.md)]

## Troubleshooting

### Understanding severity classifications

If content is classified at an unexpected severity level:

- Review the detailed severity definitions to understand the classification criteria
- Check if context is missing that would change the interpretation (educational, historical, fictional)
- Verify the content language is in the supported list for best accuracy
- Use annotations to see all detected categories, not just filtered ones

### Adjusting sensitivity

If you're seeing too many false positives or negatives:

- Review your threshold settings in the guardrail configuration
- Consider whether the content type (educational, medical, creative) requires a custom content policy
- For supported use cases, request a custom content filter configuration

For more information, see [Configure guardrails and controls](../../default/guardrails/how-to-create-guardrails.md).

## Next steps

- [Guardrails and controls overview](../../default/guardrails/guardrails-overview.md)
- [Configure guardrails and controls](../../default/guardrails/how-to-create-guardrails.md)
- [Guardrail annotations](content-filter-annotations.md)
- [Content filtering](../../foundry-models/concepts/content-filter.md)
