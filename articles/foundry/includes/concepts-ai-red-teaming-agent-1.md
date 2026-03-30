---
title: Include file
description: Include file
author: lgayhardt
ms.reviewer: minthigpen
ms.author: lagayhar
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

[!INCLUDE [feature-preview](feature-preview.md)]

The AI Red Teaming Agent is a powerful tool designed to help organizations proactively find safety risks associated with generative AI systems during design and development of generative AI models and applications.

Traditional red teaming involves exploiting the cyber kill chain and describes the process by which a system is tested for security vulnerabilities. However, with the rise of generative AI, the term AI red teaming has been coined to describe probing for novel risks (both content and security related) that these systems present and refers to simulating the behavior of an adversarial user who is trying to cause your AI system to misbehave in a particular way.

The AI Red Teaming Agent leverages Microsoft's open-source framework for Python Risk Identification Tool's ([PyRIT](https://github.com/Azure/PyRIT)) AI red teaming capabilities along with Microsoft Foundry's [Risk and Safety Evaluations](../concepts/evaluation-evaluators/risk-safety-evaluators.md) to help you automatically assess safety issues in three ways:

- **Automated scans for content risks:** Firstly, you can automatically scan your model and application endpoints for safety risks by simulating adversarial probing.
- **Evaluate probing success:** Next, you can evaluate and score each attack-response pair to generate insightful metrics such as Attack Success Rate (ASR).
- **Reporting and logging** Finally, you can generate a score card of the attack probing techniques and risk categories to help you decide if the system is ready for deployment. Findings can be logged, monitored, and tracked over time directly in Foundry, ensuring compliance and continuous risk mitigation.

Together these components (scanning, evaluating, and reporting) help teams understand how AI systems respond to common attacks, ultimately guiding a comprehensive risk management strategy.
