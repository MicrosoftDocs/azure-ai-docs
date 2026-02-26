---
title: Monitor AI agent fleet health and performance - Microsoft Foundry
description: Track agent health, compliance, performance trends, and cost efficiency across your AI fleet by using Microsoft Foundry Control Plane monitoring.
author: sonalim-0
ms.author: scottpolly
ms.reviewer: sonalimalik
ms.date: 02/13/2026
ms.topic: how-to
ms.service: azure-ai-foundry
ms.custom: dev-focus
ai-usage: ai-assisted
#CustomerIntent: As a system administrator, I want to access top-level metrics for all registered agents so that I can maintain an overview of the fleet.
---

# Monitor agent health and performance across your fleet

As your organization scales from isolated copilots to autonomous multi-agent fleets, maintaining visibility and control becomes critical. Microsoft Foundry Control Plane provides a unified command center where you can monitor all agents, models, and tools across your enterprise from build to production.

Fleet monitoring serves multiple roles:

- *Team managers* gain oversight of agent operations and team productivity.
- *Administrators* enforce governance policies and track compliance posture.
- *Cost managers* optimize spending and identify resource inefficiencies.
- *Security teams* monitor for prohibited behaviors and policy violations.

This article shows you how to use Foundry Control Plane capabilities to track agent health, performance, compliance, and cost efficiency at scale. By using centralized monitoring, you can identify problems early, optimize resource consumption, and help ensure that your AI systems operate safely and reliably.

## Prerequisites

[!INCLUDE [control-plane-prereqs](../includes/control-plane-prereqs.md)]

- The following permissions:
  - Read access to the project and subscription that you want to view data for
  - [Log Analytics Reader](/azure/role-based-access-control/built-in-roles/monitor#log-analytics-reader) role or higher on the Application Insights resource that's associated with your agent
  - [Cost Management Reader](/azure/role-based-access-control/built-in-roles/management-and-governance#cost-management-reader) role

[!INCLUDE [capability-new-portal](../includes/capability-new-portal.md)]

## How monitoring works

Foundry Control Plane discovers all the agents that you can access. It uses the Application Insights resources that host your agents to help you monitor and diagnose those agents.

Foundry Control Plane supports:

> [!div class="checklist"]
>
> - Foundry agents, including [prompt-based agents](../../agents/overview.md), [workflows](../agents/concepts/workflow.md), and [hosted agents](../agents/concepts/hosted-agents.md).
> - [Azure SRE Agent](/azure/sre-agent/).
> - [Azure Logic Apps agent loops](/azure/logic-apps/agent-workflows-concepts).
> - [Custom agents](register-custom-agent.md) registered manually.

Because Foundry Control Plane aggregates information across resources within the subscription, different users might see different agents listed, depending on their access.

Foundry Control Plane aggregates logs and metrics available across each Application Insights resource that's connected to each agent.

:::image type="content" source="media/monitoring-across-fleet/observability-app-insights-architecture.png" alt-text="Architecture diagram that shows how Foundry Control Plane uses Application Insights to collect logs and metrics across resources." lightbox="media/monitoring-across-fleet/observability-app-insights-architecture.png":::

Foundry Control Plane requires agents to log diagnostic information by following OpenTelemetry standards with [semantic conventions for Generative AI](https://opentelemetry.io/docs/specs/semconv/gen-ai/) applications. You don't need to configure Application Insights on each resource, but doing so is strongly recommended. When Control Plane has this data, it can provide:

- **Fleet health metrics**: Track active agents, run completion rates, and error trends across your entire fleet.
- **Cost and performance tracking**: Monitor token usage, budget consumption, and resource efficiency across all agents.
- **Anomaly detection**: Identify cost spikes, performance degradation, and emerging issues through trend analysis.
- **Drill-down analysis**: Move from fleet-level metrics to individual agent traces and logs for detailed investigation.

> [!IMPORTANT]
> Agents running on resources without Application Insights don't have health metrics, cost tracking, or drill-down traces.

## Configure monitoring

Follow these steps for each project where you want to configure monitoring:

1. On the toolbar, select **Operate**.

1. On the left pane, select **Admin**.

1. Under **All projects**, use the search box to look for your project.

1. Select the project.

1. Select the **Connected resources** tab.

1. Ensure that there's an associated resource for the category **AppInsights**.

    :::image type="content" source="media/register-custom-agent/verify-app-insights.png" alt-text="Screenshot of the administration portal that shows how to verify if a project has an associated Application Insights resource." lightbox="media/register-custom-agent/verify-app-insights.png":::

1. If there's no associated resource, add one by selecting **Add connection** and then selecting **Application Insights**.

    > [!TIP]
    > You can send traces to either different Application Insights resources or to the same resource, depending on your governance and security requirements.

Your project is now configured for observability and tracing. To verify that monitoring is active, go to **Operate** > **Overview** in the Foundry portal, select your project from the dropdown list, and confirm that agent metrics appear in the dashboard. Metrics might take a few minutes to populate after initial configuration.

## View metrics

You can view aggregated metrics for all agents within a selected project by using Foundry. The **Overview** pane provides insights into fleet health, compliance, and performance trends.

1. [!INCLUDE [foundry-sign-in](../includes/foundry-sign-in.md)]

1. On the toolbar, select **Operate**.

1. The **Overview** pane displays common metrics and insights for all discovered agents within the subscription by default.

    :::image type="content" source="media/overview/control-plane-overview.gif" alt-text="Animation of the Overview pane that displays trend-based health scores, alert summaries, and aggregated compliance metrics for a fleet." lightbox="media/overview/control-plane-overview.gif":::

1. Use the project dropdown list to scope down the metrics to specific projects, if necessary.

1. Configure the date range by using the date selectors in the upper-right corner.

The **Overview** pane shows fleet-level health scores, alert summaries, active agent counts, error rates, and compliance metrics for the selected time range. Use this view to quickly assess the operational state of your fleet and identify areas that need attention.

## View individual agent metrics

You can view all your assets under a specific project, along with top-level metrics, from Foundry.

1. [!INCLUDE [foundry-sign-in](../includes/foundry-sign-in.md)]

1. On the toolbar, select **Operate**.

1. On the left pane, select **Assets**.

1. Select the **Agents** tab.

    :::image type="content" source="media/monitoring-across-fleet/agents-tab-overview-metrics.png" alt-text="Screenshot of the Agents tab that shows all registered agents with top-level metrics." lightbox="media/monitoring-across-fleet/agents-tab-overview-metrics.png":::

   The tab shows the details of agents discovered within the subscription. To learn about these details, see [Agent inventory](how-to-manage-agents.md#agent-inventory).

1. To view more granular information on the performance of an individual agent, select an agent. The pane that appears provides quick insights into the selected agent's health and recent activity. Use it to identify problems and take corrective actions.  

    :::image type="content" source="media/monitoring-across-fleet/agent-details.png" alt-text="Screenshot of the Foundry pane that shows details of a selected agent." lightbox="media/monitoring-across-fleet/agent-details.png":::

    The pane contains these sections:

    - **Active alerts**: View policy, security, and evaluation alerts grouped by severity and take action.
    - **Activity**: See key metrics such as error rate over time, total run information, and information on token usage.

To learn more about how to manage individual agents, see [Manage agents at scale](how-to-manage-agents.md).

## Troubleshoot monitoring

If you don't see expected metrics or agents in the dashboard, check the following common causes:

- **Agents don't appear in the Assets pane**: Verify that you have read access to the subscription and project where the agents are deployed. Different users see different agents depending on their access level.
- **Metrics are empty or missing**: Confirm that the Application Insights resource is connected to the project (see [Configure monitoring](#configure-monitoring)). Metrics can take several minutes to populate after the initial connection.
- **Health metrics or traces aren't available for a specific agent**: The agent might be running on a resource without Application Insights configured. Connect an Application Insights resource to the agent's project to enable health data and drill-down traces.
- **Cost data doesn't appear**: Verify that you have the [Cost Management Reader](/azure/role-based-access-control/built-in-roles/management-and-governance#cost-management-reader) role on the subscription.

## Related content

- [What is Microsoft Foundry Control Plane?](overview.md)
- [Manage agents at scale](how-to-manage-agents.md)
- [Register and manage custom agents](register-custom-agent.md)
