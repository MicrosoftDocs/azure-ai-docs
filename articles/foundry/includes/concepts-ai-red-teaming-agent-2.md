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

## How AI Red Teaming works

The AI Red Teaming Agent helps automate simulation of adversarial probing of your target AI system. It provides a curated dataset of seed prompts or attack objectives per supported risk categories. These can be used to automate direct adversarial probing. However, direct adversarial probing might be easily caught by existing safety alignments of your model deployment. Applying attack strategies from PyRIT provides an extra conversion that can help to by-pass or subvert the AI system into producing undesirable content.

In the diagram, we can see that a direct ask to your AI system on how to loot a bank triggers a refusal response. However, applying an attack strategy such as flipping all the characters can help trick the model into answering the question.

:::image type="content" source="../media/evaluations/red-teaming-agent/how-ai-red-teaming-works.png" alt-text="Diagram of how AI Red Teaming Agent works." lightbox="../media/evaluations/red-teaming-agent/how-ai-red-teaming-works.png":::

Additionally, the AI Red Teaming Agent provides users with a fine-tuned adversarial large language model dedicated to the task of simulating adversarial attacks and evaluating responses that might have harmful content in them with the Risk and Safety Evaluators. The key metric to assess the risk posture of your AI system is Attack Success Rate (ASR) which calculates the percentage of successful attacks over the number of total attacks.
