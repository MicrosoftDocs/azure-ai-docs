---
title: AI Red Teaming Agent
titleSuffix: Azure AI Foundry
description: This article provides conceptual overview of the AI Red Teaming Agent.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 04/04/2025
ms.reviewer: minthigpen
ms.author: lagayhar
author: lgayhardt
---

# AI Red Teaming Agent (preview)

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

The AI Red Teaming Agent (preview) is a powerful tool designed to help organizations proactively find safety risks associated with generative AI systems during design and development of generative AI models and applications.

Traditional red teaming involves exploiting the cyber kill chain and describes the process by which a system is tested for security vulnerabilities. However, with the rise of generative AI, the term AI red teaming has been coined to describe probing for novel risks (both content safety and security related) that these systems present and refers to simulating the behavior of an adversarial user who is trying to cause your AI system to misbehave in a particular way.

The AI Red Teaming Agent leverages Microsoft's open-source framework for Python Risk Identification Tool's ([PyRIT](https://github.com/Azure/PyRIT)) AI red teaming capabilities along with Azure AI Foundry's [Risk and Safety Evaluations](./evaluation-metrics-built-in.md#risk-and-safety-evaluators) to help you automatically assess safety issues in three ways:

- **Automated scans for content safety risks:** Firstly, you can automatically scan your model and application endpoints for safety risks by simulating adversarial probing.
- **Evaluate probing success:** Next, you can evaluate and score each attack-response pair to generate insightful metrics such as Attack Success Rate (ASR).
- **Reporting and logging** Finally, you can generate a score card of the attack probing techniques and risk categories to help you decide if the system is ready for deployment. Findings can be logged, monitored, and tracked over time directly in Azure AI Foundry, ensuring compliance and continuous risk mitigation.

Together these components (scanning, evaluating, and reporting) help teams understand how AI systems respond to common attacks, ultimately guiding a comprehensive risk management strategy.

## When to use the AI Red Teaming Agent's scans

When thinking about AI-related safety risks developing trustworthy AI systems, Microsoft uses NIST's framework to mitigate risk effectively: Govern, Map, Measure, Manage. We'll focus on the last three parts in relation to the generative AI development lifecycle:

- Map: Identify relevant risks and define your use case.
- Measure: Evaluate risks at scale.
- Manage: Mitigate risks in production and monitor with a plan for incident response.

:::image type="content" source="../media/evaluations/red-teaming-agent/map-measure-mitigate-ai-red-teaming.png" alt-text="Diagram of how to use AI Red Teaming Agent showing proactive to reactive and less costly to more costly." lightbox="../media/evaluations/red-teaming-agent/map-measure-mitigate-ai-red-teaming.png":::

AI Red Teaming Agent can be used to run automated scans and simulate adversarial probing to help accelerate the identification and evaluation of known risks at scale. This helps teams "shift left" from costly reactive incidents to more proactive testing frameworks that can catch issues before deployment. Manual AI red teaming process is time and resource intensive. It relies on the creativity of safety and security expertise to simulate adversarial probing. This process can create a bottleneck for many organizations to accelerate AI adoption. With the AI Red Teaming Agent, organizations can now leverage Microsoft’s deep expertise to scale and accelerate their AI development with Trustworthy AI at the forefront.

We encourage teams to use the AI Red Teaming Agent to run automated scans throughout the design, development, and pre-deployment stage:

- Design: Picking out the safest foundational model on your use case.
- Development: Upgrading models within your application or creating fine-tuned models for your specific application.
- Pre-deployment: Before deploying GenAI applications to productions.

In production, we recommend implementing **safety mitigations** such as [Azure AI Content Safety filters](../../ai-services/content-safety/overview.md) or implementing safety system messages using our [templates](../../ai-services/openai/concepts/safety-system-message-templates.md).

## How AI Red Teaming works

The AI Red Teaming Agent helps automate simulation of adversarial probing of your target AI system. It provides a curated dataset of seed prompts or attack objectives per supported risk categories. These can be used to automate direct adversarial probing. However, direct adversarial probing might be easily caught by existing safety alignments of your model deployment. Applying attack strategies from PyRIT provides an extra conversion that can help to by-pass or subvert the AI system into producing undesirable content.

In the diagram, we can see that a direct ask to your AI system on how to loot a bank triggers a refusal response. However, applying an attack strategy such as flipping all the characters can help trick the model into answering the question.

:::image type="content" source="../media/evaluations/red-teaming-agent/how-ai-red-teaming-works.png" alt-text="Diagram of how AI Red Teaming Agent works." lightbox="../media/evaluations/red-teaming-agent/how-ai-red-teaming-works.png":::

Additionally, the AI Red Teaming Agent provides users with a fine-tuned adversarial large language model dedicated to the task of simulating adversarial attacks and evaluating responses that might have harmful content in them with the Risk and Safety Evaluators. The key metric to assess the risk posture of your AI system is Attack Success Rate (ASR) which calculates the percentage of successful attacks over the number of total attacks.

## Supported risk categories

The following risk categories are supported in the AI Red Teaming Agent from [Risk and Safety Evaluations](./evaluation-metrics-built-in.md#risk-and-safety-evaluators). Only text-based scenarios are supported.

| **Risk category** | **Description** |
|------------------|-----------------|
| **Hateful and Unfair Content** | Hateful and unfair content refers to any language or imagery pertaining to hate toward or unfair representations of individuals and social groups along factors including but not limited to race, ethnicity, nationality, gender, sexual orientation, religion, immigration status, ability, personal appearance, and body size. Unfairness occurs when AI systems treat or represent social groups inequitably, creating or contributing to societal inequities. |
| **Sexual Content** | Sexual content includes language or imagery pertaining to anatomical organs and genitals, romantic relationships, acts portrayed in erotic terms, pregnancy, physical sexual acts (including assault or sexual violence), prostitution, pornography, and sexual abuse. |
| **Violent Content** | Violent content includes language or imagery pertaining to physical actions intended to hurt, injure, damage, or kill someone or something. It also includes descriptions of weapons and guns (and related entities such as manufacturers and associations). |
| **Self-Harm-Related Content** | Self-harm-related content includes language or imagery pertaining to actions intended to hurt, injure, or damage one's body or kill oneself. |

## Supported attack strategies

The following attack strategies are supported in the AI Red Teaming Agent from [PyRIT](https://azure.github.io/PyRIT/index.html):

| **Attack Strategy** | **Description** |
|---------------------|-----------------|
| AnsiAttack | Utilizes ANSI escape sequences to manipulate text appearance and behavior. |
| AsciiArt | Generates visual art using ASCII characters, often used for creative or obfuscation purposes. |
| AsciiSmuggler | Conceals data within ASCII characters, making it harder to detect. |
| Atbash | Implements the Atbash cipher, a simple substitution cipher where each letter is mapped to its reverse. |
| Base64 | Encodes binary data into a text format using Base64, commonly used for data transmission. |
| Binary | Converts text into binary code, representing data in a series of 0s and 1s. |
| Caesar | Applies the Caesar cipher, a substitution cipher that shifts characters by a fixed number of positions. |
| CharacterSpace | Alters text by adding spaces between characters, often used for obfuscation. |
| CharSwap | Swaps characters within text to create variations or obfuscate the original content. |
| Diacritic | Adds diacritical marks to characters, changing their appearance and sometimes their meaning. |
| Flip | Flips characters from front to back, creating a mirrored effect. |
| Leetspeak | Transforms text into Leetspeak, a form of encoding that replaces letters with similar-looking numbers or symbols. |
| Morse | Encodes text into Morse code, using dots and dashes to represent characters. |
| ROT13 | Applies the ROT13 cipher, a simple substitution cipher that shifts characters by 13 positions. |
| SuffixAppend | Appends an adversarial suffix to the prompt |
| StringJoin | Joins multiple strings together, often used for concatenation or obfuscation. |
| UnicodeConfusable | Uses Unicode characters that look similar to standard characters, creating visual confusion. |
| UnicodeSubstitution | Substitutes standard characters with Unicode equivalents, often for obfuscation. |
| Url | Encodes text into URL format |
| Jailbreak | Injects specially crafted prompts to bypass AI safeguards, known as User Injected Prompt Attacks (UPIA). |
| Tense | Changes the tense of text, specifically converting it into past tense. |

## Learn more

Get started with our [documentation on how to run an automated scan for safety risks with the AI Red Teaming Agent](../how-to/develop/run-scans-ai-red-teaming-agent.md).

Learn more about the tools leveraged by the AI Red Teaming Agent.

- [Azure AI Risk and Safety Evaluations](./safety-evaluations-transparency-note.md)
- [PyRIT: Python Risk Identification Tool](https://github.com/Azure/PyRIT)

The most effective strategies for risk assessment we’ve seen leverage automated tools to surface potential risks, which are then analyzed by expert human teams for deeper insights. If your organization is just starting with AI red teaming, we encourage you to explore the resources created by our own AI red team at Microsoft to help you get started.

- [Planning red teaming for large language models (LLMs) and their applications](../../ai-services/openai/concepts/red-teaming.md)
- [Three takeaways from red teaming 100 generative AI products](https://www.microsoft.com/security/blog/2025/01/13/3-takeaways-from-red-teaming-100-generative-ai-products/)
- [Microsoft AI Red Team building future of safer AI](https://www.microsoft.com/security/blog/2023/08/07/microsoft-ai-red-team-building-future-of-safer-ai/)
