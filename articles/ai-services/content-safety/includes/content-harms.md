---
title: "Content harms include"
description: Content safety content harms
author: ssalgadodev
manager: mcleans
ms.service: azure-ai-content-safety
ms.topic: include
ms.date: 09/08/2026
ms.author: ssalgado
---
Guardrails, powered by Azure AI Content Safety, ensure that AI-generated outputs align with ethical guidelines and safety standards. The content filtering system classifies harmful content into four categories — hate, sexual, violence, and self-harm - for both text and image content. Use these categories to configure levels for guardrail controls that detect and mitigate risks associated with harmful content in your model deployments and agents.

The content safety system uses neural multiclass classification models to detect and filter harmful content for both text and image. Content detected at the "safe" severity level is labeled in annotations but isn't subject to filtering and isn't configurable.

> [!NOTE]
> The text content safety models for the hate, sexual, violence, and self-harm categories are trained and tested on the following languages: English, German, Japanese, Spanish, French, Italian, Portuguese, and Chinese. The service can work in many other languages, but detection accuracy and false positive rates may vary. In call cases, conduct thorough testing to validate performance meets your requirements.

## Harm category descriptions

The following table summarizes the harm categories supported:

| Category | Description |
|----------|-------------|
| **Hate and Fairness** | Hate and fairness-related harms refer to any content that attacks or uses discriminatory language with reference to a person or identity group based on certain differentiating attributes of these groups.<br><br>This category includes, but isn't limited to:<br>• Race, ethnicity, nationality<br>• Gender identity groups and expression<br>• Sexual orientation<br>• Religion<br>• Personal appearance and body size<br>• Disability status<br>• Harassment and bullying |
| **Sexual** | Sexual describes language related to anatomical organs and genitals, romantic relationships and sexual acts, acts portrayed in erotic or affectionate terms, including those portrayed as an assault or a forced sexual violent act against one's will.<br><br>This category includes but isn't limited to:<br>• Vulgar content<br>• Prostitution<br>• Nudity and pornography<br>• Abuse<br>• Child exploitation, child abuse, child grooming |
| **Violence** | Violence describes language related to physical actions intended to hurt, injure, damage, or kill someone or something; describes weapons, guns, and related entities.<br><br>This category includes, but isn't limited to:<br>• Weapons<br>• Bullying and intimidation<br>• Terrorist and violent extremism<br>• Stalking |
| **Self-Harm** | Self-harm describes language related to physical actions intended to purposely hurt, injure, damage one's body or kill oneself.<br><br>This category includes, but isn't limited to:<br>• Eating disorders<br>• Bullying and intimidation |
| **Task Adherence** | Helps ensure AI Agents consistently behave in alignment with user instructions and task objectives. It identifies discrepancies, such as misaligned tool invocations, improper tool input or output relative to user intent, and inconsistencies between responses and customer input.  |

## Severity levels for guardrails

Guardrails classifies harmful content into four severity levels:

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

Content at the **Safe** level is always annotated but never blocked, regardless of threshold setting.

## Severity levels for Azure AI Content Safety

Every harm category the service applies also comes with a severity level rating. The severity level indicates the severity of the consequences of showing the flagged content.

**Text**: The current version of the text model supports the full 0-7 severity scale. The classifier detects among all severities along this scale. If you specify, it can return severities in the trimmed scale of 0, 2, 4, and 6; each two adjacent levels are mapped to a single level.
- `[0,1]` -> `0`
- `[2,3]` -> `2`
- `[4,5]` -> `4`
- `[6,7]` -> `6`

**Image**: The current version of the image model supports the trimmed version of the full 0-7 severity scale. The classifier only returns severities 0, 2, 4, and 6.
- `0`
- `2`
- `4`
- `6`

**Image with text**: The current version of the multimodal model supports the full 0-7 severity scale. The classifier detects among all severities along this scale. If you specify, it can return severities in the trimmed scale of 0, 2, 4, and 6; each two adjacent levels are mapped to a single level.
- `[0,1]` -> `0`
- `[2,3]` -> `2`
- `[4,5]` -> `4`
- `[6,7]` -> `6`

## Severity definitions

### Detailed severity definitions for text in Guardrails

The following tables provide detailed descriptions and examples for each severity level within each harm category for text content in Guardrails. Select the **Severity definitions** tab to view examples.

[!INCLUDE [severity-levels-text-four](./severity-levels-text-four.md)]

### Detailed severity definitions for text in Azure AI Content Safety

The following tables provide detailed descriptions and examples for each severity level within each harm category for text content in Azure AI Content Safety. Select the **Severity definitions** tab to view examples.

[!INCLUDE [severity-levels text](../includes/severity-levels-text.md)]


### Detailed severity definitions for images in Guardrails and Azure AI Content Safety

The following tables provide detailed descriptions and examples for each severity level within each harm category for image content. Select the **Severity definitions** tab to view examples.

[!INCLUDE [severity-levels-image](./severity-levels-image.md)]

### Detailed severity definitions for multimodal in Azure AI Content Safety

The following tables provide detailed descriptions and examples for each severity level within each harm category for multimodal content. Select the **Severity definitions** tab to view examples.

[!INCLUDE [severity-levels multimodal](../includes/severity-levels-multimodal.md)]

## Troubleshooting

### Understanding severity classifications

If content is classified at an unexpected severity level:

- Review the detailed severity definitions to understand the classification criteria.
- Check if context is missing that would change the interpretation (educational, historical, fictional).
- Verify the content language is in the supported list for best accuracy.
- In Guardrails, use annotations to see all detected categories, not just filtered ones.

### Adjusting sensitivity

If you see too many false positives or negatives:

- Review your threshold settings.
- Consider whether the content type (educational, medical, creative) requires a custom content policy.
- For Guardrails supported use cases, request a custom content filter configuration.
