---
title: Monitor AI Agent Fleets with Azure AI Foundry
description: Monitor and manage your AI agents at scale with Azure AI Foundry. Learn how to track health, compliance, and performance trends using a centralized dashboard.
#customer intent: As a system administrator, I want to access top-level metrics for all registered agents so that I can maintain an overview of the fleet.
author: sonalim-0
ms.author: scottpolly
ms.reviewer: sonalimalik
ms.date: 11/05/2025
ms.topic: how-to
ms.service: azure-ai-foundry
ms.custom: dev-focus
ai-usage: ai-assisted
---

# Monitor AI Agents Across Your Fleet

As organizations scale from isolated copilots to autonomous multi-agent fleets, maintaining visibility and control becomes critical. The Foundry Control Plane provides a unified command center where you can monitor all agents, models, and tools across your enterprise from build to production.

This article shows you how to use the Foundry Control Plane's capabilities to track agent health, performance, compliance, and cost efficiency at scale. With centralized monitoring, you can identify issues early, optimize resource consumption, and ensure your AI systems operate safely and reliably.

## What is fleet monitoring in the Control Plane?

Fleet monitoring in the Foundry Control Plane gives you real-time visibility into your entire AI estate. Instead of monitoring agents individually, you gain a unified view across all agents in your projects, whether they're Foundry-native, Microsoft services, or third-party integrations.

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

## Prerequisites

[!INCLUDE [control-plane-prereqs](../includes/control-plane-prereqs.md)]
- Read access to the project & subscription you'd like to view data for.

## View Metrics

You can view aggregated metrics for all agents within a selected project using Azure AI Foundry. The Overview pane provides insights into fleet health, compliance, and performance trends.

:::image type="content" source="media/monitoring-across-fleet/agent-metrics-overview-page.png" alt-text="Screenshot of the Overview page displaying aggregated metrics for all agents.":::

1. Go to **Azure AI Foundry Portal**.

1. Select **Operate** > **Overview**.

The Overview page displays common metrics and insights for all registered agents in your selected project:

- Monitor compliance alerts and track fleet health, including active versus inactive agents, success rates, and error trends.

- Analyze resource usage and performance trends, including budget consumption, token usage, and agent run volume.

## View all assets

:::image type="content" source="media/monitoring-across-fleet/agents-tab-overview-metrics.png" alt-text="Screenshot of the Agents tab showing all registered agents with top-level metrics.":::You can also view all your assets under a specific project along with top-level metrics from AI Foundry.

1. Select **Operate** > **Assets** > **Agents**.

1. Review the overview of common metrics.

The Agents tab displays all registered agents in your selected project. From here, you can:

- Filter by metrics including platform, status, and cost.

- Select **Include all agent types** to view every agent in your fleet.



## Related content
- [Register an agent]()
- [Configure agent policies]()
- [Troubleshoot agent issues]()
