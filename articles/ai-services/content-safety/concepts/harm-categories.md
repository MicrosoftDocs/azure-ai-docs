---
title: "Harm categories in Azure AI Content Safety"
titleSuffix: Azure AI services
description: Learn about the different content moderation flags and severity levels that the Azure AI Content Safety service returns.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.custom: build-2023
ms.topic: concept-article
ms.date: 11/21/2025
ms.author: pafarley
---


# Harm categories in Azure AI Content Safety

Azure AI Content Safety uses harm categories to flag and rate objectionable content in both text and images. This guide describes all of the harm categories and ratings that Azure AI Content Safety uses. Understanding these categories helps you configure moderation and compliance for your use cases. Both text and image content use the same set of flags.

## Harm categories

Content Safety recognizes four distinct categories of objectionable content.

| Category  | Description         |API term |
| --------- | ------------------- | --- |
| Hate and Fairness      | Hate and fairness harms refer to any content that attacks or uses discriminatory language with reference to a person or identity group based on certain differentiating attributes of these groups. <br><br>This includes, but is not limited to:<ul><li>Race, ethnicity, nationality</li><li>Gender identity groups and expression</li><li>Sexual orientation</li><li>Religion</li><li>Personal appearance and body size</li><li>Disability status</li><li>Harassment and bullying</li></ul> | `Hate` |
| Sexual  | Sexual describes language related to anatomical organs and genitals, romantic relationships and sexual acts, acts portrayed in erotic or affectionate terms, including those portrayed as an assault or a forced sexual violent act against one’s will. <br><br> This includes but is not limited to:<ul><li>Vulgar content</li><li>Prostitution</li><li>Nudity and Pornography</li><li>Abuse</li><li>Child exploitation, child abuse, child grooming</li></ul>   | `Sexual` |
| Violence  | Violence describes language related to physical actions intended to hurt, injure, damage, or kill someone or something; describes weapons, guns, and related entities. <br><br>This includes, but isn't limited to:  <ul><li>Weapons</li><li>Bullying and intimidation</li><li>Terrorist and violent extremism</li><li>Stalking</li></ul>  | `Violence` |
| Self-Harm  | Self-harm describes language related to physical actions intended to purposely hurt, injure, damage one’s body or kill oneself. <br><br> This includes, but isn't limited to: <ul><li>Eating Disorders</li><li>Bullying and intimidation</li></ul>  | `SelfHarm` |

Classification can be multi-labeled. For example, when a text sample goes through the text moderation model, it could be classified as both Sexual content and Violence.

## Severity levels

Every harm category the service applies also comes with a severity level rating. The severity level is meant to indicate the severity of the consequences of showing the flagged content.

**Text**: The current version of the text model supports the full 0-7 severity scale. The classifier detects among all severities along this scale. If the user specifies, it can return severities in the trimmed scale of 0, 2, 4, and 6; each two adjacent levels are mapped to a single level.
- `[0,1]` -> `0`
- `[2,3]` -> `2`
- `[4,5]` -> `4`
- `[6,7]` -> `6`

**Image**: The current version of the image model supports the trimmed version of the full 0-7 severity scale. The classifier only returns severities 0, 2, 4, and 6.
- `0`
- `2`
- `4`
- `6`

**Image with text**: The current version of the multimodal model supports the full 0-7 severity scale. The classifier detects among all severities along this scale. If the user specifies, it can return severities in the trimmed scale of 0, 2, 4, and 6; each two adjacent levels are mapped to a single level.
- `[0,1]` -> `0`
- `[2,3]` -> `2`
- `[4,5]` -> `4`
- `[6,7]` -> `6`

[!INCLUDE [severity-levels text](../includes/severity-levels-text.md)]

[!INCLUDE [severity-levels image](../includes/severity-levels-image.md)]

[!INCLUDE [severity-levels multimodal](../includes/severity-levels-multimodal.md)]


## Next step

Follow a quickstart to get started using Azure AI Content Safety in your application.

> [!div class="nextstepaction"]
> [Content Safety quickstart](../quickstart-text.md)
