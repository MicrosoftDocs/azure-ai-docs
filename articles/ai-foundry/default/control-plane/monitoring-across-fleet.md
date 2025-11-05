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

Managing and monitoring a large fleet of AI agents is critical for ensuring reliability, compliance, and cost efficiency. Azure AI Foundry provides a centralized dashboard to track agent health, performance, and policy adherence. This guide walks you through the key steps and best practices for monitoring agents at scale.

## Prerequisites

[!INCLUDE [control-plane-prereqs](../includes/control-plane-prereqs.md)]
- Read access to the project & subscription you'd like to view data for.

## View Metrics

You can view aggregated metrics for all agents within a selected project using Azure AI Foundry. The Overview page provides insights into fleet health, compliance, and performance trends.

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

## Next steps

> [!div class="nextstepaction"]
> [Register an agent](../register-agent.md)

## Related content

- [Configure agent policies](../configure-policies.md)
- [Troubleshoot agent issues](../troubleshoot-agents.md)
