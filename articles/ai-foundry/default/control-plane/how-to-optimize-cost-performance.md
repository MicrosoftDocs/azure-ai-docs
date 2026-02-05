---
title: Optimize Cost and Performance in Microsoft Foundry
titleSuffix: Foundry
description: Learn how to use the Ask AI agent to analyze and optimize model cost and performance directly from Microsoft Foundry.
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 02/04/2026
ms.reviewer: hanch
ms.author: scottpolly
author: bhcglx
monikerRange: 'foundry'
ms.custom: dev-focus
ai-usage: ai-assisted
---

# Optimize model cost and performance

When your model or agent costs start increasing, use the *Ask AI agent* to quickly diagnose issues, take action, and verify improvements. The Ask AI agent is a built-in chat assistant. You can access it from the toolbar in the Microsoft Foundry portal.

This article walks you through a recommended workflow, from identifying cost spikes to switching models and validating performance improvements. All these activities happen within the Foundry portal.

## Prerequisites

[!INCLUDE [control-plane-prereqs](../includes/control-plane-prereqs.md)]

- At least one deployed or published agent with cost data. For meaningful trend analysis, you need a minimum of seven days of usage data.

- Access to the Ask AI agent.

- An evaluation dataset configured for your project. To set one up, see [Evaluate your generative AI application locally with the Azure AI Evaluation SDK](../../how-to/develop/evaluate-sdk.md).

## Detect cost increases

Start by opening the Ask AI agent from the toolbar. Or, go to **Operate** > **Overview** to use one of the prebuilt prompts that are specific to agent optimization and performance.

Ask the assistant to provide a summary of your metrics and cost data from the Foundry Control Plane dashboard. You can select a predefined prompt on the **Overview** pane or type your own question, such as:

- "Summarize my recent cost trend."

- "Which agents contributed most to my cost increase?"

The Ask AI agent generates a summary that highlights key cost drivers, such as high token usage, longer completion length, or frequent evaluation runs. The summary includes annotated links to the dashboard charts for deeper inspection.

## Investigate high-cost agents

After you review the summary, you can explore detailed insights for specific agents by asking:

- "Show me cost and performance details for [agent name]."

- "Break down cost by model or deployment for this agent."

You can also select **Assets** on the left pane. Then, select **View Agent details** to view the **Assets** pane. There, you can compare your agents with cost and token usage, and see which agent costs the most.

## Switch to a cost-efficient model

When you identify a model as a cost driver, ask the Ask AI agent:

- "Recommend a cheaper model with similar performance."

- "Switch this agent's deployment to a more cost-efficient model."

The Ask AI agent:

- Recommends alternative models available in the model catalog.

- Provides performance and cost comparisons.

- Upon confirmation, provides a link to the model deployment page.

Follow the instructions in the model deployment page, or continue to chat with the Ask AI agent to complete the model deployment step.

## Evaluate model differences

After you switch models, you can ask the Ask AI agent to run an evaluation that compares the old and new models:

- "Evaluate performance and cost difference between the old and new model."

The Ask AI agent provides guidance on how to create an evaluation and gives you a link to the evaluation creation wizard. You can follow the instructions step by step to create two evaluation runs on the two models.

View the results after both evaluation runs finish.

## Update your agent

When you confirm that the new model performs better than the current model, go to **Agent Playground** to update the model and save a new version.

## Track improvements

Later, return to the Ask AI agent and ask:

- "Show me the summary on the latest data for cost."

The Ask AI agent retrieves the latest metrics from your continuous evaluation and summarizes improvements in cost and performance trends. This feature helps you continuously monitor efficiency and return on investment.

## Related content

- [Evaluate your generative AI application locally with the Azure AI Evaluation SDK](../../how-to/develop/evaluate-sdk.md)
- [Explore Microsoft Foundry Models](../../concepts/foundry-models-overview.md)
