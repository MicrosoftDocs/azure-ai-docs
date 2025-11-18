---
title: Monitor AI Agent Fleets with Microsoft Foundry
description: "Monitor and manage AI agents at scale with Microsoft Foundry. Track health, compliance, and performance trends using a centralized dashboard. Get started today."
author: sonalim-0
ms.author: scottpolly
ms.reviewer: sonalimalik
ms.date: 11/05/2025
ms.topic: how-to
ms.service: azure-ai-foundry
ms.custom: dev-focus
ai-usage: ai-assisted
#customer intent: As a system administrator, I want to access top-level metrics for all registered agents so that I can maintain an overview of the fleet.
---

# Monitor agent health and performance across your fleet

As your organization scales from isolated copilots to autonomous multi-agent fleets, maintaining visibility and control becomes critical. The Foundry Control Plane provides a unified command center where you can monitor all agents, models, and tools across your enterprise from build to production.

This article shows you how to use the Foundry Control Plane's capabilities to track agent health, performance, compliance, and cost efficiency at scale. With centralized monitoring, you can identify issues early, optimize resource consumption, and ensure your AI systems operate safely and reliably.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

## Prerequisites

[!INCLUDE [control-plane-prereqs](../includes/control-plane-prereqs.md)]
- Read access to the project and subscription you want to view data for.

[!INCLUDE [capability-new-portal](../includes/capability-new-portal.md)]

## What is fleet monitoring in the Foundry Control Plane?

The Foundry Control Plane gives you real-time visibility into your entire AI estate. Instead of monitoring agents individually, you get a unified view across all agents in your projects, whether they're Foundry-native, Microsoft services, or third-party integrations.

Key monitoring capabilities include:

- **Fleet health metrics**: Track active agents, run completion rates, and error trends across your entire fleet
- **Compliance monitoring**: View compliance posture, policy adherence, and prevented behaviors in real time
- **Cost and performance tracking**: Monitor token usage, budget consumption, and resource efficiency across all agents
- **Anomaly detection**: Identify cost spikes, performance degradation, and emerging issues through trend analysis
- **Drill-down analysis**: Navigate from fleet-level metrics to individual agent traces and logs for detailed investigation

Fleet monitoring serves multiple roles:
- **Team managers** gain oversight of agent operations and team productivity
- **Administrators** enforce governance policies and track compliance posture
- **Cost managers** optimize spending and identify resource inefficiencies
- **Security teams** monitor for prohibited behaviors and policy violations

## View metrics

You can view aggregated metrics for all agents within a selected project by using Foundry. The **Overview** pane provides insights into fleet health, compliance, and performance trends.

:::image type="content" source="media/monitoring-across-fleet/agent-metrics-overview-page.png" alt-text="Screenshot of Foundry Overview page displaying aggregated metrics for all agents." lightbox="media/monitoring-across-fleet/agent-metrics-overview-page.png":::

1. [!INCLUDE [foundry-sign-in](../includes/foundry-sign-in.md)]

1. Select **Operate** from the upper-right navigation.

The **Overview** pane displays common metrics and insights for all registered agents in your selected project:

- Monitor alerts: View issues grouped by severity and category, such as alerts for evaluation scores and policy and security violations. 

- Track fleet health: See metrics to help you assess the performance of agents in the selected projects, including total number of running agents and overall agent run success rates. 

- Analyze resource usage: Review total cost and token usage while monitoring changes in these metrics over time. 

- Visualize performance trends: Explore charts for agent run volume and top increases or decreases in activity. 

## View all assets

You can view all your assets under a specific project along with top-level metrics from Foundry.

:::image type="content" source="media/monitoring-across-fleet/agents-tab-overview-metrics.png" alt-text="Screenshot of Foundry Agents tab showing all registered agents with top-level metrics." lightbox="media/monitoring-across-fleet/agents-tab-overview-metrics.png":::

1. [!INCLUDE [foundry-sign-in](../includes/foundry-sign-in.md)]

1. Select **Operate** from the upper-right navigation.

1. Select **Assets** in the left pane.

1. Select the **Agents** tab.

1. Review the overview of common metrics.

To view more granular information on the performance of an individual agent, the side panel provides quick insights into the selected agent's health and recent activity. You can use it to identify issues and take corrective actions.  

:::image type="content" source="media/monitoring-across-fleet/agent-details.png" alt-text="Screenshot of Foundry Control Plane agent details pane showing details of a selected agent." lightbox="media/monitoring-across-fleet/agent-details.png":::

In this section, you see: 

- Active alerts: View policy, security, and evaluation alerts grouped by severity and take action. 

- Activity: See key metrics such as error rate over time, total run information, and information on token usage. 


## Related content

- [Foundry Control Plane overview](overview.md)
- [Register an agent](register-custom-agent.md)

