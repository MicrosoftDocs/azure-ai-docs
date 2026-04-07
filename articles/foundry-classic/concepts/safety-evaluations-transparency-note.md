---
title:  "Microsoft Foundry risk and safety evaluations (preview) Transparency Note (classic)"
description: "Microsoft Foundry safety evaluations intended purpose, capabilities, limitations and how to achieve the best performance. (classic)"
ms.service: azure-ai-foundry
ms.custom:
  - classic-and-new
  - build-2024
ms.topic: concept-article
ms.date: 12/23/2025
ms.reviewer: mithigpe
ms.author: lagayhar
author: lgayhardt
ai-usage: ai-assisted
# customer intent: As a developer, I want to understand the capabilities, limitations, and best practices for Microsoft Foundry safety evaluations so I can responsibly evaluate and deploy my generative AI applications.
ROBOTS: NOINDEX, NOFOLLOW
---

# Microsoft Foundry risk and safety evaluations (preview) Transparency Note (classic)

**Currently viewing:** :::image type="icon" source="../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../foundry/concepts/safety-evaluations-transparency-note.md)

[!INCLUDE [feature-preview](../../foundry/includes/feature-preview.md)]

[!INCLUDE [safety-evaluations-transparency-note 1](../../foundry/includes/concepts-safety-evaluations-transparency-note-1.md)]

## The basics of Microsoft Foundry risk and safety evaluations (preview)

### Introduction

The Foundry risk and safety evaluations let users evaluate the output of their generative AI application for textual content risks: hateful and unfair content, sexual content, violent content, self-harm-related content, direct and indirect jailbreak vulnerability, and protected material in content. Safety evaluations can also help generate adversarial datasets to help you accelerate and augment the red-teaming operation. Foundry safety evaluations reflect Microsoft's commitments to ensure AI systems are built safely and responsibly, operationalizing our Responsible AI principles.

### Key terms

- **Hateful and unfair content (for text and images)** refers to any language or imagery pertaining to hate toward or unfair representations of individuals and social groups along factors including but not limited to race, ethnicity, nationality, gender, sexual orientation, religion, immigration status, ability, personal appearance, and body size. Unfairness occurs when AI systems treat or represent social groups inequitably, creating or contributing to societal inequities.
- **Sexual content (for text and images)** includes language or imagery pertaining to anatomical organs and genitals, romantic relationships, acts portrayed in erotic terms, pregnancy, physical sexual acts (including assault or sexual violence), prostitution, pornography, and sexual abuse.
- **Violent content (for text and images)** includes language or imagery  pertaining to physical actions intended to hurt, injure, damage, or kill someone or something. It also includes descriptions of weapons and guns (and related entities such as manufacturers and associations).
- **Self-harm-related content (for text and images)** includes language or imagery pertaining to actions intended to hurt, injure, or damage one's body or kill oneself.
- **Protected material content (for text)** known textual content, for example, song lyrics, articles, recipes, and selected web content, that might be output by large language models. By detecting and preventing the display of protected material, organizations can maintain compliance with intellectual property rights and preserve content originality.
- **Protected material content (for images)** refers to certain protected visual content, that is protected by copyright such as logos and brands, artworks, or fictional characters. The system uses an image-to-text foundation model to identify whether such content is present.
- **Direct jailbreak**, direct prompt attacks, or user prompt injection attacks, refer to users manipulating prompts to inject harmful inputs into LLMs to distort actions and outputs. An example of a jailbreak command is a 'DAN' (Do Anything Now) attack, which can trick the LLM into inappropriate content generation or ignoring system-imposed restrictions.  
- **Indirect jailbreak** indirect prompt attacks or cross-domain prompt injection attacks, refers to when malicious instructions are hidden within data that an AI system processes or generates grounded content from. This data can include emails, documents, websites, or other sources not directly authored by the developer or user and can lead to inappropriate content generation or ignoring system-imposed restrictions.
- **Defect rate (content risk)** is defined as the percentage of instances in your test dataset that surpass a threshold on the severity scale over the whole dataset size.
- **Red-teaming** has historically described systematic adversarial attacks for testing security vulnerabilities. With the rise of Large Language Models (LLM), the term has extended beyond traditional cybersecurity and evolved in common usage to describe many kinds of probing, testing, and attacking of AI systems. With LLMs, both benign and adversarial usage can produce potentially harmful outputs, which can take many forms, including harmful content such as hateful speech, incitement or glorification of violence, reference to self-harm-related content or sexual content.

[!INCLUDE [safety-evaluations-transparency-note 2](../../foundry/includes/concepts-safety-evaluations-transparency-note-2.md)]
