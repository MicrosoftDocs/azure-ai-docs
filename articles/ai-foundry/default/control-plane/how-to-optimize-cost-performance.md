---
title: Optimize model cost and performance
titleSuffix: Foundry
description: Use Ask AI in Microsoft Foundry to detect cost spikes, switch to cost-efficient models, evaluate quality, and track performance improvements.
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

When your model or agent costs start increasing, use **Ask AI** (preview) to quickly diagnose issues, take action, and verify improvements. Ask AI is a built-in chat assistant that you can access from the toolbar in the Microsoft Foundry portal. For more information about Ask AI capabilities and limitations, see [Ask AI for help (preview)](../../concepts/ask-ai.md).

In this article, you identify cost spikes, switch to a cost-efficient model, and validate performance improvements by using the Foundry portal.

> [!NOTE]
> When you ask Ask AI to perform tasks that modify your Azure resources, such as deploying a model or changing a deployment, Ask AI proposes actions for you to review and approve before it runs them. You can configure approval settings by selecting the settings icon in the Ask AI prompt chat. For more information, see [Ask AI for help (preview)](../../concepts/ask-ai.md).

## Prerequisites

[!INCLUDE [control-plane-prereqs](../includes/control-plane-prereqs.md)]

- The following permissions:
  - Read access to the project and subscription that you want to view data for.
  - [Log Analytics Reader](/azure/role-based-access-control/built-in-roles/monitor#log-analytics-reader) role or higher on the Application Insights resource that's associated with your agent.
  - [Cost Management Reader](/azure/role-based-access-control/built-in-roles/management-and-governance#cost-management-reader) role.

- Application Insights configured for your Foundry project. For more information, see [Configure monitoring](monitoring-across-fleet.md#configure-monitoring).
- At least one deployed or published agent with cost data. For meaningful trend analysis, you need a minimum of seven days of usage data.

- The Ask AI agent enabled in your Foundry project. The Ask AI agent is available in preview on the toolbar of the Foundry portal. If you don't see it, verify that your project is in a [supported region](overview.md) and that your administrator hasn't disabled the feature.

- An evaluation dataset that represents your agent's typical workload. Use this dataset to compare model performance after switching models. To create an evaluation dataset, see [Evaluate your generative AI application with the Azure AI Evaluation SDK](../../how-to/develop/evaluate-sdk.md).

## Detect cost increases

Use Ask AI or the cost trend charts on the **Overview** pane to identify cost spikes.

1. On the toolbar, select **Ask AI**. Alternatively, go to **Operate** > **Overview** to review the cost trend charts.

1. Enter a prompt such as "Summarize my recent cost trend" or "Which agents contributed most to my cost increase?"

1. Review the summary. Ask AI highlights key cost drivers such as high token usage, longer completion length, or frequent evaluation runs. You should see a summary listing specific agents, models, and token-usage metrics that contribute to cost increases. To inspect specific trends, go to **Operate** > **Overview** and review the cost trend charts.

> [!TIP]
> If Ask AI is unavailable, go to **Operate** > **Overview** to view cost trend charts directly.

## Investigate high-cost agents

After you review the cost summary, explore detailed insights for specific agents.

1. In Ask AI, enter a prompt such as "Show me cost and performance details for \[agent name\]" or "Break down cost by model or deployment for this agent."

1. Review the response to identify which model or deployment drives the highest cost for that agent.

> [!TIP]
> If Ask AI is unavailable, go to **Operate** > **Assets**, select the **Agents** tab, and then select an agent to view its cost and token usage details.

## Switch to a cost-efficient model

When you identify a model as a cost driver, use Ask AI to find a more cost-efficient alternative.

1. In Ask AI, enter a prompt such as "Recommend a cheaper model with similar performance" or "Compare cost and quality for models similar to \[current model\]."

1. Review the response. Ask AI recommends alternative models from the model catalog with performance and cost comparisons. Review the recommendations and select a model that meets your requirements.

1. Deploy the new model. For detailed deployment steps, see [Deploy models as serverless API deployments](../../how-to/deploy-models-serverless.md) or [Deploy models with managed compute](../../how-to/deploy-models-managed.md).

1. After deployment completes, verify that the new model appears in your agent's deployment list with a **Succeeded** status.

> [!TIP]
> If Ask AI is unavailable, browse the [Foundry model catalog](../../concepts/foundry-models-overview.md) to compare models manually.

## Evaluate model cost and quality differences

After you switch models, compare the old and new models by running an evaluation.

1. In Ask AI, enter a prompt such as "How do I compare performance and cost between the old and new model?"

1. Follow the guidance that Ask AI provides. To create evaluation runs, go to the evaluation section of your project.

1. Create two evaluation runs: one for the original model and one for the new model.

1. Wait for both evaluation runs to finish. Go to **Operate** > **Overview** or the evaluation history in your project to compare results side by side.

1. Look for differences in quality scores, latency, and cost per token. In the evaluation history, verify that both runs show a completed status with scores for each metric.

   Key metrics to compare:

   - **Groundedness** — how well responses are grounded in source data
   - **Relevance** — how relevant responses are to the query
   - **Coherence** — how logically consistent responses are
   - **Latency** — response time for the model
   - **Cost per token** — the cost efficiency of the model

   Focus on metrics that align with your agent's quality requirements.

## Update your agent's model deployment

When you confirm that the new model meets your cost and performance requirements, update the agent to use it.

1. In the Foundry portal, go to **Build** > **Agents**.

1. Select the agent that you want to update.

1. Change the model to the new deployment.

1. Test the agent to verify that it responds correctly with the new model.

1. On the agent details page, select **Save** to create a new version. Verify that the version number incremented and the model name reflects the new deployment.

After you verify that the new model works correctly, consider deleting the old model deployment to avoid ongoing costs. For more information, see [Deploy models as serverless API deployments](../../how-to/deploy-models-serverless.md).

## Track cost and performance improvements

To verify improvements after the model switch, check the latest cost data.

1. Open Ask AI from the toolbar.

1. Enter a prompt such as "Show me the summary on the latest data for cost."

1. Review the summary. Ask AI retrieves the latest metrics from your [continuous evaluation](../../concepts/observability.md) and summarizes improvements in cost and performance trends. The summary reflects lower cost trends compared to the previous period.

Use this workflow regularly to monitor efficiency and return on investment.

## Troubleshoot common issues

| Issue | Cause | Resolution |
|-------|-------|------------|
| No cost data appears in the summary | Application Insights isn't configured for the project. | [Configure monitoring](monitoring-across-fleet.md#configure-monitoring) for your Foundry project. |
| Ask AI doesn't respond to prompts | The feature might be temporarily unavailable, or the prompt might be too vague. | Try a more specific prompt or use the **Operate** > **Overview** pane directly. |
| Ask AI asks for approval before acting | Ask AI proposes actions for review before modifying Azure resources. | Review the proposed action and select **Approve** to proceed. To configure pre-approval settings, select the settings icon in the Ask AI prompt chat. |
| No alternative models recommended | The current model might already be the most cost-efficient option, or the model catalog doesn't have comparable alternatives. | Browse the [Foundry model catalog](../../concepts/foundry-models-overview.md) manually. |
| Evaluation runs don't complete | The evaluation dataset might be misconfigured or too large. | Verify your evaluation dataset configuration. See [Evaluate your generative AI application with the Azure AI Evaluation SDK](../../how-to/develop/evaluate-sdk.md). |
| Cost data appears stale or delayed | Azure billing data can take up to 24-48 hours to update. Application Insights telemetry might also have a short delay. | Wait for the billing cycle to complete and check again. For near real-time data, rely on Application Insights metrics in the **Operate** > **Overview** pane. |
| Model switch causes quality regression | The new model might not perform as well on your specific workload. | Roll back to the previous model deployment and run more targeted evaluations before switching again. |

## Related content

- [Ask AI for help (preview)](../../concepts/ask-ai.md)
- [Monitor agent health and performance across your fleet](monitoring-across-fleet.md)
- [Manage agents in Foundry Control Plane](how-to-manage-agents.md)
- [Enforce token limits on models](how-to-enforce-limits-models.md)
- [What is Foundry Control Plane?](overview.md)
- [Evaluate your generative AI application with the Azure AI Evaluation SDK](../../how-to/develop/evaluate-sdk.md)
- [Explore Microsoft Foundry Models](../../concepts/foundry-models-overview.md)
