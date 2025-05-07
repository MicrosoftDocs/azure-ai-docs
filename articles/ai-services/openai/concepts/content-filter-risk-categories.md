---
title: Content Filter Risk Categories
description: Overview of risk categories for content filtering in Azure OpenAI, including hate, fairness, sexual, violence, and more.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-services
ms.topic: conceptual
ms.date: 05/07/2025
ms.author: pafarley
---

# Content filtering risk categories

<!--
Text and image models support Drugs as an additional classification. This category covers advice related to Drugs and depictions of recreational and non-recreational drugs.
-->


|Category|Description|
|--------|-----------|
| Hate and Fairness      | Hate and fairness-related harms refer to any content that attacks or uses discriminatory language with reference to a person or Identity group based on certain differentiating attributes of these groups. <br><br>This includes, but is not limited to:<ul><li>Race, ethnicity, nationality</li><li>Gender identity groups and expression</li><li>Sexual orientation</li><li>Religion</li><li>Personal appearance and body size</li><li>Disability status</li><li>Harassment and bullying</li></ul> |
| Sexual  | Sexual describes language related to anatomical organs and genitals, romantic relationships and sexual acts, acts portrayed in erotic or affectionate terms, including those portrayed as an assault or a forced sexual violent act against one’s will. <br><br> This includes but is not limited to:<ul><li>Vulgar content</li><li>Prostitution</li><li>Nudity and Pornography</li><li>Abuse</li><li>Child exploitation, child abuse, child grooming</li></ul>   |
| Violence  | Violence describes language related to physical actions intended to hurt, injure, damage, or kill someone or something; describes weapons, guns and related entities. <br><br>This includes, but isn't limited to:  <ul><li>Weapons</li><li>Bullying and intimidation</li><li>Terrorist and violent extremism</li><li>Stalking</li></ul>  |
| Self-Harm  | Self-harm describes language related to physical actions intended to purposely hurt, injure, damage one’s body or kill oneself. <br><br> This includes, but isn't limited to: <ul><li>Eating Disorders</li><li>Bullying and intimidation</li></ul>  |
| Protected Material for Text<sup>1</sup> | Protected material text describes known text content (for example, song lyrics, articles, recipes, and selected web content) that can be outputted by large language models.
| Protected Material for Code | Protected material code describes source code that matches a set of source code from public repositories, which can be outputted by large language models without proper citation of source repositories.
|User Prompt Attacks |User prompt attacks are User Prompts designed to provoke the Generative AI model into exhibiting behaviors it was trained to avoid or to break the rules set in the System Message. Such attacks can vary from intricate roleplay to subtle subversion of the safety objective. |
|Indirect Attacks |Indirect Attacks, also referred to as Indirect Prompt Attacks or Cross-Domain Prompt Injection Attacks, are a potential vulnerability where third parties place malicious instructions inside of documents that the Generative AI system can access and process. Requires [document embedding and formatting](#embedding-documents-in-your-prompt). |
| Groundedness<sup>2</sup> | Groundedness detection flags whether the text responses of large language models (LLMs) are grounded in the source materials provided by the users. Ungrounded material refers to instances where the LLMs produce information that is non-factual or inaccurate from what was present in the source materials. Requires [document embedding and formatting](#embedding-documents-in-your-prompt). |

<sup>1</sup> If you're an owner of text material and want to submit text content for protection, [file a request](https://aka.ms/protectedmaterialsform).

<sup>2</sup> Not available in non-streaming scenarios; only available for streaming scenarios. The following regions support Groundedness Detection: Central US, East US, France Central, and Canada East 

[!INCLUDE [severity-levels text, four-level](../../content-safety/includes/severity-levels-text-four.md)]

[!INCLUDE [severity-levels image](../../content-safety/includes/severity-levels-image.md)]