---
title: Upgrade/Switch Models in Azure AI Foundry with Foundry Agent 
titleSuffix: Azure AI Foundry 
description: Learn how to use Foundry Agent for an easy and smooth model upgrade or switch for the agents.  
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 11/18/2025
ms.reviewer: hanch
ms.author: lagayhar
author: lgayhardt
ai-usage: ai-assisted 
---

# Upgrade/Switch Models in Azure AI Foundry with Foundry Agent

When new model versions are released or older versions are deprecated, you can use **Azure AI Foundry Agent** - the built-in chat assistant to detect, evaluate, and upgrade models without leaving the Foundry portal.

Foundry Agent provides conversational guidance, context-aware recommendations, and one-click actions for model upgrade, evaluation, and deployment.

This article describes the integrated user experience and system behavior when you initiate or manage model upgrades through Foundry Agent.

## Prerequisites

Before you begin:

- You have access to the **Azure AI Foundry portal**.
- You have one or more deployed models or agents.
- You have access to **Foundry Agent** (the chat assistant).
- You have at least one evaluation dataset in CSV or JSONL format.
- You have sufficient permission to deploy and evaluate.

## Start a chat with Foundry Agent

You can start a chat with Foundry Agent from any page in the Foundry portal.

1. Select the **Ask AI** icon at the top of the page.
1. Select one of the predefined prompts from the **Ask AI** banner under “Build/Model/Monitor” or “Build/Agent/Monitor” page.

## Get recommendation on model replacement or upgrade

You can ask Foundry Agent questions like:

- “Is any model I’m using deprecated?”
- “Should I upgrade my model?”
- “What’s new in the latest GPT-5 version?”

It gives responses and different options on what models are recommended. You can either select any of the models to view details in model catalog or go to model deployment page to deploy a model. To learn how to deploy a model, see [Add and configure models to Azure AI Foundry Models](../../foundry-models/how-to/create-model-deployments.md).

## Evaluate the new model and compare the performance

Once a new model is deployed, you can ask Foundry Agent to start an evaluation of the new model with the same agent instructions and configurations. You can either do it via the link provided by Foundry Agent and follow the steps of [creating a new evaluation](), or ask Foundry Agent to create it on your behalf.

Once the evaluation is complete, you can view the result in the evaluation group detail page and check if the new model is performing better than the current model. You can also use [compare]() or [cluster analysis](observability-optimization-cluster-analysis.md) to have a deeper understanding of the evaluation result.

If you aren't satisfied with the new model, you can test other models and repeat the previous steps to create new evaluation runs. The new run is added to the evaluation group when you create the evaluation for the first time.

## Update your agent with the new model

Once you decide to update your agent with the new model, you can either chat with Foundry Agent to kick off this process or go to Agent Playground page to manually update it. The new model is updated to the agent with a new version.

You can also chat with Foundry Agent to scan your project and find agents in similar situations and apply the change to them.

## Related content

-
