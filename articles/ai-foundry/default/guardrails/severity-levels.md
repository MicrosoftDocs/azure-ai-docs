---
title: 'Harm categories and severity levels in Microsoft Foundry'
titleSuffix: Microsoft Foundry
description: Learn about the harm categories and severity levels used by the content safety system in Microsoft Foundry to detect and filter harmful content.
manager: nitinme
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.date: 10/30/2025
author: ssalgadodev
ms.author: ssalgado
recommendations: false
ms.custom: azure-ai-content-safety
# customer intent: As a developer, I want to understand the harm categories and severity levels in Microsoft Foundry so that I can properly handle content filtering in my applications.
---

# Harm categories and severity levels in Microsoft Foundry

Content filtering in Microsoft Foundry ensures that AI-generated outputs align with ethical guidelines and safety standards. Azure OpenAI provides content filtering capabilities to help identify and mitigate risks associated with various categories of harmful or inappropriate content.

The content safety system contains neural multiclass classification models aimed at detecting and filtering harmful content. The models cover four categories (hate, sexual, violence, and self-harm) across four severity levels (safe, low, medium, and high) for both text and image content. Content detected at the 'safe' severity level is labeled in annotations but isn't subject to filtering and isn't configurable.

> [!NOTE]
> The text content safety models for the hate, sexual, violence, and self-harm categories are specifically trained and tested on the following languages: English, German, Japanese, Spanish, French, Italian, Portuguese, and Chinese. However, the service can work in many other languages, but the quality might vary. In all cases, you should do your own testing to ensure that it works for your application.

## Harm category descriptions

The following table summarizes the harm categories supported by Foundry guardrails:

| Category | Description |
|----------|-------------|
| **Hate and Fairness** | Hate and fairness-related harms refer to any content that attacks or uses discriminatory language with reference to a person or identity group based on certain differentiating attributes of these groups.<br><br>This includes, but is not limited to:<br>• Race, ethnicity, nationality<br>• Gender identity groups and expression<br>• Sexual orientation<br>• Religion<br>• Personal appearance and body size<br>• Disability status<br>• Harassment and bullying |
| **Sexual** | Sexual describes language related to anatomical organs and genitals, romantic relationships and sexual acts, acts portrayed in erotic or affectionate terms, including those portrayed as an assault or a forced sexual violent act against one's will.<br><br>This includes but is not limited to:<br>• Vulgar content<br>• Prostitution<br>• Nudity and pornography<br>• Abuse<br>• Child exploitation, child abuse, child grooming |
| **Violence** | Violence describes language related to physical actions intended to hurt, injure, damage, or kill someone or something; describes weapons, guns and related entities.<br><br>This includes, but isn't limited to:<br>• Weapons<br>• Bullying and intimidation<br>• Terrorist and violent extremism<br>• Stalking |
| **Self-Harm** | Self-harm describes language related to physical actions intended to purposely hurt, injure, damage one's body or kill oneself.<br><br>This includes, but isn't limited to:<br>• Eating disorders<br>• Bullying and intimidation |

## Severity levels

Guardrails ensure that AI-generated outputs align with ethical guidelines and safety standards. The content safety system uses four severity levels to classify harmful content:

- **Safe**: Content that doesn't contain harmful material
- **Low**: Content that contains mild harmful material
- **Medium**: Content that contains moderate harmful material  
- **High**: Content that contains severe harmful material

> [!NOTE]
> Content detected at the 'safe' severity level is labeled in annotations but isn't subject to filtering and isn't configurable.

[!INCLUDE [severity-levels-text-four](../../../ai-services/content-safety/includes/severity-levels-text-four.md)]

[!INCLUDE [severity-levels-image](../../../ai-services/content-safety/includes/severity-levels-image.md)]



## Next steps

- [Guardrails and controls overview](how-to-create-guardrails.md)
- [Understanding guardrail annotations](../../openai/concepts/content-filter-annotations.md)
- [Learn about content filtering in Azure OpenAI](../../openai/concepts/content-filter.md)
