---
title: include file
description: include file
ms.author: pafarley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 01/28/2025
ms.custom: include
---

## Understand harm categories

### Harm categories

| Category  | Description         |API term |
| --------- | ------------------- | --- |
| Hate and Fairness      | Hate and fairness harms refer to any content that attacks or uses discriminatory language with reference to a person or identity group based on certain differentiating attributes of these groups. <br><br>This includes, but isn't limited to:<ul><li>Race, ethnicity, nationality</li><li>Gender identity groups and expression</li><li>Sexual orientation</li><li>Religion</li><li>Personal appearance and body size</li><li>Disability status</li><li>Harassment and bullying</li></ul> | `Hate` |
| Sexual  | Sexual describes language related to anatomical organs and genitals, romantic relationships and sexual acts, acts portrayed in erotic or affectionate terms, including those portrayed as an assault or a forced sexual violent act against one's will. <br><br> This includes but isn't limited to:<ul><li>Vulgar content</li><li>Prostitution</li><li>Nudity and Pornography</li><li>Abuse</li><li>Child exploitation, child abuse, child grooming</li></ul>   | `Sexual` |
| Violence  | Violence describes language related to physical actions intended to hurt, injure, damage, or kill someone or something; describes weapons, guns, and related entities. <br><br>This includes, but isn't limited to:  <ul><li>Weapons</li><li>Bullying and intimidation</li><li>Terrorist and violent extremism</li><li>Stalking</li></ul>  | `Violence` |
| Self-Harm  | Self-harm describes language related to physical actions intended to purposely hurt, injure, damage one's body or kill oneself. <br><br> This includes, but isn't limited to: <ul><li>Eating Disorders</li><li>Bullying and intimidation</li></ul>  | `SelfHarm` |

### Severity levels 

| Level | Description |
| --- | ---|
|Safe |Content might be related to violence, self-harm, sexual, or hate categories. However, the terms are used in general, journalistic, scientific, medical, and similar professional contexts, which are appropriate for most audiences. |
|Low |Content that expresses prejudiced, judgmental, or opinionated views, includes offensive use of language, stereotyping, use-cases exploring a fictional world (for example, gaming, literature) and depictions at low intensity.| 
|Medium |Content that uses offensive, insulting, mocking, intimidating, or demeaning language towards specific identity groups, includes depictions of seeking and executing harmful instructions, fantasies, glorification, promotion of harm at medium intensity. |
|High |Content that displays explicit and severe harmful instructions, actions, damage, or abuse; includes endorsement, glorification, or promotion of severe harmful acts, extreme or illegal forms of harm, radicalization, or nonconsensual power exchange or abuse. |