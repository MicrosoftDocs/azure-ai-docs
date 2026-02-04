---
title: Monitor AI Agent Fleets with Microsoft Foundry
description: "Monitor and manage AI agents at scale with Microsoft Foundry. Track health, compliance, and performance trends using a centralized dashboard. Get started today."
author: sonalim-0
ms.author: scottpolly
ms.reviewer: sonalimalik
ms.date: 02/04/2026
ms.topic: how-to
ms.service: azure-ai-foundry
ms.custom: dev-focus
ai-usage: ai-assisted
#customer intent: As a system administrator, I want to access top-level metrics for all registered agents so that I can maintain an overview of the fleet.
---

# Monitor agent health and performance across your fleet

As your organization scales from isolated copilots to autonomous multi-agent fleets, maintaining visibility and control becomes critical. The Foundry Control Plane provides a unified command center where you can monitor all agents, models, and tools across your enterprise from build to production. Fleet monitoring serves multiple roles:

- **Team managers** gain oversight of agent operations and team productivity.
- **Administrators** enforce governance policies and track compliance posture.
- **Cost managers** optimize spending and identify resource inefficiencies.
- **Security teams** monitor for prohibited behaviors and policy violations.

This article shows you how to use the Foundry Control Plane's capabilities to track agent health, performance, compliance, and cost efficiency at scale. By using centralized monitoring, you can identify problems early, optimize resource consumption, and ensure your AI systems operate safely and reliably.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

## Prerequisites

[!INCLUDE [control-plane-prereqs](../includes/control-plane-prereqs.md)]

- You need the following permissions:
    - Read access to the project and subscription you want to view data for.
    - [Log Analytics Reader](/azure/role-based-access-control/built-in-roles/monitor#log-analytics-reader) role or higher on the Azure Application Insights resource associated with your agent. 
    - [Cost Management reader](https://go.microsoft.com/fwlink/?linkid=2345241) role.

[!INCLUDE [capability-new-portal](../includes/capability-new-portal.md)]

## How monitoring works

Control Plane discovers all the agents you can access. It uses the Azure Application Insights associated with the resources that host your agent to help you monitor and diagnose your agents. 

Control Plane supports:

> [!div class="checklist"]
> * Foundry agents, including [prompt-based agents](../../agents/overview.md), [workflows](../agents/concepts/workflow.md), and [hosted-agents](../agents/concepts/hosted-agents.md). 
> * [Azure SRE Agent](/azure/sre-agent/)
> * [Azure Logic App agent loops](/azure/logic-apps/agent-workflows-concepts)
> * [Custom agents](register-custom-agent.md) registered manually

Because Control Plane aggregates information across resources within the subscription, different users see different agents listed depending on their access. 

Control Plane **aggregates logs and metrics available across each of the Azure Application Insights** connected to each of the agents:

:::image type="content" source="media/monitoring-across-fleet/observability-app-insights-architecture.png" alt-text="An architecture diagram about how Foundry Control Plane uses Azure Application Insights to collect logs and metrics across resources." lightbox="media/monitoring-across-fleet/observability-app-insights-architecture.png":::

Control Plane requires agents to log diagnostic information following OpenTelemetry standard with [semantic conventions for Generative AI](https://opentelemetry.io/docs/specs/semconv/gen-ai/) applications. You don't need to configure Azure Application Insights on each resource but **it's strongly advisable**. When Control Plane has this telemetry, it can:

- **Fleet health metrics**: Track active agents, run completion rates, and error trends across your entire fleet.
- **Cost and performance tracking**: Monitor token usage, budget consumption, and resource efficiency across all agents.
- **Anomaly detection**: Identify cost spikes, performance degradation, and emerging issues through trend analysis.
- **Drill-down analysis**: Navigate from fleet-level metrics to individual agent traces and logs for detailed investigation.

> [!IMPORTANT]
> Agents running on resources without Azure Application Insights don't have health metrics, cost tracking, or drill-down traces. 

## Configure monitoring

Follow these steps for each project where you want to configure monitoring:

1. Select **Operate** > **Admin console**.

1. Under **All projects**, use the search box to look for your project.

1. Select the project.

1. Select the tab **Connected resources**.

1. Ensure there's a resource associated under the category **Application Insights**.

    :::image type="content" source="media/register-custom-agent/verify-app-insights.png" alt-text="Screenshot of the administration portal showing how to verify if your project has an Azure Application Insights associated." lightbox="media/register-custom-agent/verify-app-insights.png":::

1. If there's no resource associated, add one by selecting **Add connection** and select **Application Insights**.

    > [!TIP]
    > You can sink traces to either different Azure Application Insights resources or to the same one depending on your governance and security requirements.

1. Your project is configured for observability and tracing.

### Permissions

After you configure observability, make sure you have the following permissions:
    
- [Log Analytics Reader](/azure/role-based-access-control/built-in-roles/monitor#log-analytics-reader) role (or higher) on the Azure Application Insights resource. 

- [Cost Management reader](https://go.microsoft.com/fwlink/?linkid=2345241) role.


## View metrics

You can view aggregated metrics for all agents within a selected project by using Foundry. The **Overview** pane provides insights into fleet health, compliance, and performance trends.

1. [!INCLUDE [foundry-sign-in](../includes/foundry-sign-in.md)]

1. Select **Operate** from the upper-right navigation.

1. The **Overview** pane displays common metrics and insights for all discovered agents within the subscription by default:

    :::image type="content" source="media/overview/control-plane-overview.gif" alt-text="Animation of the Fleet Overview page displaying trend-based health scores, alert summaries, and aggregated compliance metrics." lightbox="media/overview/control-plane-overview.gif":::

1. Use the project drop-down to scope down the metrics to specific projects if needed.

1. Configure the dates range you are seeing by using the date selectors located in the upper right corner.


## View agents' metrics

You can view all your assets under a specific project along with top-level metrics from Foundry.

1. [!INCLUDE [foundry-sign-in](../includes/foundry-sign-in.md)]

1. Select **Operate** from the upper-right navigation.

1. Select **Assets** in the left pane.

1. Select the **Agents** tab.

    :::image type="content" source="media/monitoring-across-fleet/agents-tab-overview-metrics.png" alt-text="Screenshot of Foundry Agents tab showing all registered agents with top-level metrics." lightbox="media/monitoring-across-fleet/agents-tab-overview-metrics.png":::

1. You see the details of agents discovered within the subscription. See [agent inventory](how-to-manage-agents.md#agents-inventory) to learn about the details of this page.

1. To view more granular information on the performance of an individual agent, the side panel provides quick insights into the selected agent's health and recent activity. Use it to identify problems and take corrective actions.  

    :::image type="content" source="media/monitoring-across-fleet/agent-details.png" alt-text="Screenshot of Foundry Control Plane agent details pane showing details of a selected agent." lightbox="media/monitoring-across-fleet/agent-details.png":::

1. In this section, you see: 

    - Active alerts: View policy, security, and evaluation alerts grouped by severity and take action. 
    
    - Activity: See key metrics such as error rate over time, total run information, and information on token usage. 

1. To learn more about how to manage individual agents see [Manage agents at scale](how-to-manage-agents.md).

## Related content

- [Foundry Control Plane overview](overview.md)
- [Register an agent](register-custom-agent.md)

