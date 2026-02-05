---
title: Upgrade/Switch Models in Microsoft Foundry with Ask AI 
titleSuffix: Microsoft Foundry 
description: Learn how to use Ask AI for an easy and smooth model upgrade or switch for the agents.  
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 11/18/2025
ms.reviewer: hanch
ms.author: lagayhar
author: lgayhardt
ai-usage: ai-assisted 
---

# Upgrade/switch models in Microsoft Foundry with Ask AI (preview)

[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

When new model versions are released or older versions are deprecated, use Ask AI—the built-in chat assistant—to detect, evaluate, and upgrade models without leaving the Foundry portal.

Ask AI provides conversational guidance, context-aware recommendations, and one-click actions for upgrading, evaluating, and deploying models.

This article describes the integrated user experience and system behavior when you initiate or manage model upgrades through Ask AI.

## Prerequisites

- A [Foundry project](../../../how-to/create-projects.md) with one or more deployed models or [agents](../../../agents/overview.md).
- Access to **Ask AI** (the chat assistant) in the Foundry portal.
- At least one [evaluation dataset](../../../how-to/develop/cloud-evaluation.md) in CSV or JSONL format.
- Sufficient permission to deploy and evaluate.

## Start a chat with Ask AI

You can start a chat with Ask AI from any page in the Foundry portal.

1. Select the **Ask AI** icon at the top of the page.
1. Select one of the predefined prompts from the **Ask AI** banner under *Build/Model/Monitor* or *Build/Agent/Monitor* page, or in Ask AI.
    :::image type="content" source="../../media/observability/model-upgrade-predefined-prompts.png" alt-text="Screenshot of Ask AI with predefined prompts." lightbox="../../media/observability/model-upgrade-predefined-prompts.png":::

## Get recommendations on model replacement or upgrade

Ask AI questions like:

- "Is any model I’m using deprecated?"
- "Should I upgrade my model?"
- "What’s new in the latest GPT-5 version?"

:::image type="content" source="../../media/observability/model-upgrade-ask-ai.png" alt-text="Screenshot of Ask AI answering a question." lightbox="../../media/observability/model-upgrade-ask-ai.png":::

It gives responses and options for recommended models. Select a model to view details in the model catalog, or go to the model deployment page to deploy a model. To learn how to deploy a model, see [Add and configure models to Foundry Models](../../../foundry-models/how-to/create-model-deployments.md).

:::image type="content" source="../../media/observability/model-upgrade-selected-model.png" alt-text="Screenshot of a selected model page with Ask AI offering other detailed model links to view next." lightbox="../../media/observability/model-upgrade-selected-model.png":::

## Evaluate the new model and compare the performance

After deploying a new model, ask Ask AI to start an evaluation of the model using the same agent instructions and configurations. Either use the link provided by Ask AI and follow the steps in [creating a new evaluation](../../../how-to/evaluate-generative-ai-app.md?view=foundry&preserve-view=true), or ask Ask AI to create it for you.

:::image type="content" source="../../media/observability/model-upgrade-evaluations.png" alt-text="Screenshot of submit a new evaluation page with Ask AI showing a workflow and a creation wizard option." lightbox="../../media/observability/model-upgrade-evaluations.png":::

After the evaluation is complete, view the result on the evaluation detail page to check if the new model performs better than the current model. Use [compare](../../../how-to/evaluate-results.md?view=foundry&preserve-view=true#compare-the-evaluation-results) or [cluster analysis](cluster-analysis.md) to gain deeper insights into the evaluation result.

If the new model isn't satisfactory, test other models and repeat the steps to create new evaluation runs. The new run is added to the evaluation when you create the first evaluation.

## Update your agent with the new model

To update your agent with the new model, chat with Ask AI to start the process or go to the Agent Playground page to update it manually. The new model updates the agent with a new version.

Chat with Ask AI to scan your project, find agents in similar situations, and apply the change to them.

## Related content

- [Model versions in Foundry Models](../../../foundry-models/concepts/model-versions.md?view=foundry&preserve-view=true)
