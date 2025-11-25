---
title: How to Optimize Cost and Performance in Microsoft Foundry
titleSuffix: Foundry
description: Learn how to use Foundry Agent to analyze and optimize model cost and performance directly from Microsoft Foundry.
ms.service: azure-ai-foundry
ms.custom:
ms.topic: how-to
ms.date: 11/18/2025
ms.reviewer: hanch
ms.author: scottpolly
author: bhcglx
monikerRange: 'foundry'
ai-usage: ai-assisted
---

# Optimize model cost and performance

When your model or agent costs start increasing, use the **Foundry Agent** — the built-in chat assistant — to quickly diagnose issues, take action, and verify improvements.

This article walks you through a recommended workflow, from identifying cost spikes to switching models and validating performance improvements — all within the Foundry portal.


## Prerequisites

[!INCLUDE [control-plane-prereqs](../includes/control-plane-prereqs.md)]

- At least one deployed or published agent with cost data. For meaningful trend analysis, you need a minimum of 7 days of usage data.

- You have access to the **Foundry Agent** (the chat assistant).

- An evaluation dataset configured for your project. To set one up, see [Create and manage evaluation datasets](../../how-to/develop/evaluate-sdk.md).

## Detect cost increases

A typical flow starts by asking **Ask AI** to provide a summary on the metrics and cost from the **Foundry Control Plane** dashboard.

You can use predefined prompts in the **Operate** overview page, or type your own question, such as:

- "Summarize my recent cost trend."

- "Which agents contributed most to my cost increase?"

The Foundry Agent generates a summary that highlights key cost drivers, such as high token usage, longer completion length, or frequent evaluation runs. The summary includes annotated links to the dashboard charts for deeper inspection.

## Investigate high-cost agents

After reviewing the summary, you can explore detailed insights for specific agents by asking:

- "Show me cost and performance details for [agent name]."

- "Break down cost by model or deployment for this agent."

You can also select **Assets** in the left pane. Select **View Agent details** to view the **Assets** page, where you can compare your agents with cost and token usage, and see which agent costs the most.


## Switch to a cost-efficient model

When you identify a model as a cost driver, ask the Foundry Agent:

- "Recommend a cheaper model with similar performance."

- "Switch this agent's deployment to a more cost-efficient model."

The Foundry Agent:

1. Recommends alternative models available in the **Model Catalog**.

1. Provides performance and cost comparisons.

1. Upon confirmation, provides a link to the model deployment page.

Follow the instructions in the model deployment page, or continue to chat with the Foundry Agent to complete the model deployment step.

## Evaluate model differences

After switching models, you can ask the Foundry Agent to run an evaluation that compares the old and new models:

- "Evaluate performance and cost difference between the old and new model."

The Foundry Agent provides guidance on how to create an evaluation and gives you a link to the evaluation creation wizard. You can follow the instructions step by step to create two evaluation runs on the two models.

View the results after both evaluation runs complete.


## Update your agent

When you confirm the new model performs better than the current model, go to **Agent Playground** to update the model and save a new version.

## Track improvements

Later, return to the Foundry Agent and ask:

- "Show me the summary on the latest data for cost."

The Foundry Agent retrieves the latest metrics from your continuous evaluation and summarizes improvements in cost and performance trends. This feature helps you continuously monitor ROI and efficiency.

## Related content

- [Evaluate model performance](../../how-to/develop/evaluate-sdk.md)
- [Explore models in the Model Catalog](../../how-to/model-catalog-overview.md)