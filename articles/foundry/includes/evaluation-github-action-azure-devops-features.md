---
title: Include file
description: Include file
author: lgayhardt
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 9/19/2025
ms.author: lagayhar
ms.custom: include file
---

## Features

- **Agent Evaluation**: Automate pre-production assessment of Microsoft Foundry agents in your CI/CD workflow.
- **Evaluators**: Use any evaluators from the Foundry evaluator catalog.
- **Statistical Analysis**: Evaluation results include confidence intervals and test for statistical significance to determine if changes are meaningful and not due to random variation.

## Evaluator categories

- [Agent evaluators](../concepts/evaluation-evaluators/agent-evaluators.md): Process and system-level evaluators for agent workflows.
- [RAG evaluators](../concepts/evaluation-evaluators/rag-evaluators.md): Evaluate end-to-end and retrieval processes in RAG systems.
- [Risk and safety evaluators](../concepts/evaluation-evaluators/risk-safety-evaluators.md): Assess risks and safety concerns in responses.
- [General purpose evaluators](../concepts/evaluation-evaluators/general-purpose-evaluators.md): Quality evaluation such as coherence and fluency.
- [OpenAI-based graders](../concepts/evaluation-evaluators/azure-openai-graders.md): Use OpenAI graders including string check, text similarity, score/label model.
- [Custom evaluators](../concepts/evaluation-evaluators/custom-evaluators.md): Define your own custom evaluators using Python code or LLM-as-a-judge patterns.

