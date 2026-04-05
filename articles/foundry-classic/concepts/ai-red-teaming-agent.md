---
title: "AI Red Teaming Agent (classic)"
description: "This article provides conceptual overview of the AI Red Teaming Agent. (classic)"
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.date: 02/25/2026
ms.reviewer: minthigpen
ms.author: lagayhar
author: lgayhardt
ms.custom:
  - classic-and-new
ROBOTS: NOINDEX, NOFOLLOW
---

# AI Red Teaming Agent (preview) (classic)

**Currently viewing:** :::image type="icon" source="../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../foundry/concepts/ai-red-teaming-agent.md)

[!INCLUDE [ai-red-teaming-agent 1](../../foundry/includes/concepts-ai-red-teaming-agent-1.md)]

## When to use an AI red teaming run

When thinking about AI-related safety risks developing trustworthy AI systems, Microsoft uses NIST's framework to mitigate risk effectively: Govern, Map, Measure, Manage. We'll focus on the last three parts in relation to the generative AI development lifecycle:

- Map: Identify relevant risks and define your use case.
- Measure: Evaluate risks at scale.
- Manage: Mitigate risks in production and monitor with a plan for incident response.

:::image type="content" source="../../foundry/media/evaluations/red-teaming-agent/map-measure-mitigate-ai-red-teaming.png" alt-text="Diagram of how to use AI Red Teaming Agent showing proactive to reactive and less costly to more costly." lightbox="../../foundry/media/evaluations/red-teaming-agent/map-measure-mitigate-ai-red-teaming.png":::

AI Red Teaming Agent can be used to run automated scans and simulate adversarial probing to help accelerate the identification and evaluation of known risks at scale. This helps teams "shift left" from costly reactive incidents to more proactive testing frameworks that can catch issues before deployment. Manual AI red teaming process is time and resource intensive. It relies on the creativity of safety and security expertise to simulate adversarial probing. This process can create a bottleneck for many organizations to accelerate AI adoption. With the AI Red Teaming Agent, organizations can now leverage Microsoft's deep expertise to scale and accelerate their AI development with Trustworthy AI at the forefront.

We encourage teams to use the AI Red Teaming Agent to run automated scans throughout the design, development, and predeployment stage:

- Design: Picking out the safest foundational model on your use case.
- Development: Upgrading models within your application or creating fine-tuned models for your specific application.
- Predeployment: Before deploying GenAI applications to productions.

In production, we recommend implementing **safety mitigations** such as [Azure AI Content Safety filters](../../ai-services/content-safety/overview.md) or implementing safety system messages using our [templates](../openai/concepts/safety-system-message-templates.md).

[!INCLUDE [ai-red-teaming-agent 2](../../foundry/includes/concepts-ai-red-teaming-agent-2.md)]

## Supported risk categories

The following risk categories are supported in the AI Red Teaming Agent from [Risk and Safety Evaluations](./observability.md). Only text-based scenarios are supported.

| **Risk category** | **Description** |
|------------------|-----------------|
| **Hateful and Unfair Content** | Hateful and unfair content refers to any language or imagery pertaining to hate toward or unfair representations of individuals and social groups along factors including but not limited to race, ethnicity, nationality, gender, sexual orientation, religion, immigration status, ability, personal appearance, and body size. Unfairness occurs when AI systems treat or represent social groups inequitably, creating or contributing to societal inequities. |
| **Sexual Content** | Sexual content includes language or imagery pertaining to anatomical organs and genitals, romantic relationships, acts portrayed in erotic terms, pregnancy, physical sexual acts (including assault or sexual violence), prostitution, pornography, and sexual abuse. |
| **Violent Content** | Violent content includes language or imagery pertaining to physical actions intended to hurt, injure, damage, or kill someone or something. It also includes descriptions of weapons and guns (and related entities such as manufacturers and associations). |
| **Self-Harm-Related Content** | Self-harm-related content includes language or imagery pertaining to actions intended to hurt, injure, or damage one's body or kill oneself. |

[!INCLUDE [ai-red-teaming-agent 3](../../foundry/includes/concepts-ai-red-teaming-agent-3.md)]
