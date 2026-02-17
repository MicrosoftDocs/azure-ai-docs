---
title: Optimize Model Cost and Performance
titleSuffix: Foundry
description: Learn how to use the Ask AI agent to identify cost spikes and optimize model cost and performance in the Microsoft Foundry portal.
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 02/17/2026
ms.reviewer: hanch
ms.author: scottpolly
author: bhcglx
monikerRange: 'foundry'
ms.custom: dev-focus
ai-usage: ai-assisted
---

# Optimize model cost and performance

When your model or agent costs start increasing, use the *Ask AI agent* to quickly diagnose issues, take action, and verify improvements. The Ask AI agent is a built-in chat assistant that you can access from the toolbar in the Microsoft Foundry portal.

This article describes how to identify cost spikes, switch to a cost-efficient model, and validate performance improvements by using the Foundry portal.

## Prerequisites

[!INCLUDE [control-plane-prereqs](../includes/control-plane-prereqs.md)]

- The following permissions:
  - Read access to the project and subscription that you want to view data for.
  - [Log Analytics Reader](/azure/role-based-access-control/built-in-roles/monitor#log-analytics-reader) role or higher on the Application Insights resource that's associated with your agent.
  - [Cost Management Reader](/azure/role-based-access-control/built-in-roles/management-and-governance#cost-management-reader) role.

- Application Insights configured for your Foundry project. For more information, see [Configure monitoring](monitoring-across-fleet.md#configure-monitoring).

- At least one deployed or published agent with cost data. For meaningful trend analysis, you need a minimum of seven days of usage data.

- Access to the Ask AI agent.

- An evaluation dataset configured for your project. To configure an evaluation dataset, see [Evaluate your generative AI application locally with the Azure AI Evaluation SDK](../../how-to/develop/evaluate-sdk.md).

## Detect cost increases

Use the Ask AI agent or the prebuilt prompts on the **Overview** pane to identify cost spikes.

1. On the toolbar, select the **Ask AI agent**. Alternatively, go to **Operate** > **Overview** to use one of the prebuilt prompts that are specific to agent optimization and performance.

1. Enter a prompt such as "Summarize my recent cost trend" or "Which agents contributed most to my cost increase?"

1. Review the summary. The Ask AI agent highlights key cost drivers such as high token usage, longer completion length, or frequent evaluation runs. The summary includes annotated links to the dashboard charts for deeper inspection.

You should see a summary with cost drivers and links to dashboard charts.

> [!TIP]
> If the Ask AI agent is unavailable, go to **Operate** > **Overview** to view cost trend charts directly.

## Investigate high-cost agents

After you review the cost summary, explore detailed insights for specific agents.

1. In the Ask AI agent, enter a prompt such as "Show me cost and performance details for \[agent name\]" or "Break down cost by model or deployment for this agent."

1. Review the response to identify which model or deployment drives the highest cost for that agent.

Alternatively, you can investigate agents without the Ask AI agent:

1. On the left pane, select **Assets**.

1. Select **View Agent details** to open the **Assets** pane.

1. Compare your agents by cost and token usage to identify which agent costs the most.

The **Assets** pane displays agents sorted by cost and token usage.

## Switch to a cost-efficient model

When you identify a model as a cost driver, use the Ask AI agent to find a more cost-efficient alternative.

1. In the Ask AI agent, enter a prompt such as "Recommend a cheaper model with similar performance" or "Switch this agent's deployment to a more cost-efficient model."

1. Review the response. The Ask AI agent recommends alternative models available in the model catalog and provides performance and cost comparisons.

1. Confirm your selection. The Ask AI agent provides a link to the model deployment page.

1. Follow the instructions on the model deployment page to deploy the new model.

After deployment completes, confirm the new model appears in your agent's deployment list.

> [!TIP]
> If the Ask AI agent is unavailable, browse the [Foundry model catalog](../../concepts/foundry-models-overview.md) to compare models manually.

## Evaluate model differences

After you switch models, compare the old and new models by running an evaluation.

1. In the Ask AI agent, enter a prompt such as "How do I compare performance and cost between the old and new model?"

1. Follow the guidance that the Ask AI agent provides. The agent gives you a link to the evaluation creation wizard.

1. In the evaluation creation wizard, create two evaluation runs: one for the original model and one for the new model.

1. Wait for both evaluation runs to finish. Go to **Operate** > **Overview** or the evaluation history in your project to compare results side by side.

1. Look for differences in quality scores, latency, and cost per token.

Both evaluation runs appear in the evaluation history with comparative scores.

## Update your agent

When you confirm that the new model meets your cost and performance requirements, update the agent to use it.

1. In the Foundry portal, go to **Build** > **Agents**.

1. Select the agent that you want to update.

1. Change the model to the new deployment.

1. Test the agent to verify that it responds correctly with the new model.

1. Select **Save** to create a new version.

The updated agent version appears on the agent details page with the new model.

## Track improvements

To verify improvements after the model switch, check the latest cost data.

1. Open the Ask AI agent from the toolbar.

1. Enter a prompt such as "Show me the summary on the latest data for cost."

1. Review the summary. The Ask AI agent retrieves the latest metrics from your continuous evaluation and summarizes improvements in cost and performance trends.

The summary reflects lower cost trends compared to the previous period. Use this workflow regularly to monitor efficiency and return on investment.

## Troubleshoot common issues

| Issue | Cause | Resolution |
|-------|-------|------------|
| No cost data appears in the summary | Application Insights isn't configured for the project. | [Configure monitoring](monitoring-across-fleet.md#configure-monitoring) for your Foundry project. |
| Ask AI agent doesn't respond to prompts | The agent might be unavailable or the prompt might be too vague. | Try a more specific prompt or use the **Operate** > **Overview** pane directly. |
| No alternative models recommended | The current model might already be the most cost-efficient option, or the model catalog doesn't have comparable alternatives. | Browse the [Foundry model catalog](../../concepts/foundry-models-overview.md) manually. |
| Evaluation runs don't complete | The evaluation dataset might be misconfigured or too large. | Verify your evaluation dataset configuration. See [Evaluate with the Azure AI Evaluation SDK](../../how-to/develop/evaluate-sdk.md). |

## Related content

- [What is Foundry Control Plane?](overview.md)
- [Monitor agent health and performance across your fleet](monitoring-across-fleet.md)
- [Manage agents in Foundry Control Plane](how-to-manage-agents.md)
- [Enforce token limits on models](how-to-enforce-limits-models.md)
- [Evaluate your generative AI application locally with the Azure AI Evaluation SDK](../../how-to/develop/evaluate-sdk.md)
- [Explore Microsoft Foundry Models](../../concepts/foundry-models-overview.md)
