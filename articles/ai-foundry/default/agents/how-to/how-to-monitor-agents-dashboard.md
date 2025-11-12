---
title: Monitor AI Agents with Microsoft Foundry Dashboard
description: Gain insights into your AI agents' performance with the Agent Monitoring Dashboard. Optimize operations, evaluate responses, and ensure compliance.
#customer intent: As an AI operations manager, I want to monitor the performance of my AI agents in real time so that I can ensure optimal functionality and compliance.
author: sonalim-0
ms.author: scottpolly
ms.reviewer: sonalimalik
ms.date: 10/27/2025
ms.topic: how-to
ms.service: azure-ai-foundry
ms.custom: dev-focus
ai-usage: ai-assisted
---

# Monitor AI Agents with the Agent Monitoring Dashboard

The Agent Monitoring Dashboard in Microsoft Foundry provides real-time insights into the operational health, performance, and compliance of your AI agents. Use this dashboard to track token usage, latency, evaluation metrics, and security posture across multi-agent systems.

## Prerequisites

- A Foundry project. For more information, see [Create a Foundry project](/azure/ai-foundry/how-to/create-projects).
- At least one deployed agent in your Foundry project.
- An Application Insights resource connected to your project.
- Azure role-based access control (RBAC): At minimum, "Reader" role on the Application Insights resource to view monitoring data.

## View agent metrics in the portal

To view metrics for your agent in the Foundry portal:

1. [!INCLUDE [foundry-sign-in](../../includes/foundry-sign-in.md)].

2. Navigate to the **Build** page using the top navigation and select the agent you'd like to view data for.

3. Select the **Monitor** tab to view operational, evaluation, and red-teaming data for your agent.

## View agent metrics

 :::image type="content" source="../media/how-to-monitor-agents-dashboard/foundry-metrics-dashboard.png" alt-text="Screenshot of the Agent Monitoring Dashboard in Foundry showing summary cards at the top with high-level metrics and charts below displaying evaluation scores, agent run success rates, and token usage over time.":::

The Agent Monitoring Dashboard in Foundry is designed for quick insights and deep analysis of your AI agents' performance. It consists of two main areas:

- Summary Cards at the top for high-level metrics. These cards provide an at-a-glance view of key metrics.

- Charts and graphs below for granular details. These visualizations reflect data for the selected time range. Use them to view key metrics including evaluation scores by day, agent run success rates, and token usage.

## Configure settings

The Monitor Settings panel allows you to enable and customize telemetry, evaluations, and security checks for your AI agents. These settings ensure that the dashboard displays accurate operational and quality metrics.

:::image type="content" source="../media/how-to-monitor-agents-dashboard/monitor-settings-panel.png" alt-text="Screenshot showing the Monitor Settings panel in Foundry with options for operational metrics, continuous evaluation, scheduled evaluations, red team scans, and alerts configuration.":::

The following table describes the monitoring features available in the Monitor Settings panel:

| Setting | Purpose | Configuration Options |
|---------|---------|----------------------|
| **Operational Metrics** | Tracks agent runs, token usage, latency, and error rates. | Enabled automatically after connecting Application Insights. |
| **Continuous Evaluation** | Runs real-time checks on agent responses for intent resolution, coherence, and reconciliation. | Enable/Disable toggle<br>Add evaluators by name or import from past evaluations<br>Set sample rate (for example, 10 runs/hour) |
| **Scheduled Evaluations** | Performs periodic evaluations to validate agent performance against benchmarks. | Enable/Disable toggle<br>Select evaluation template<br>Select evaluation run<br>Set schedule frequency (weekly recommended) |
| **Red Team Scans** | Executes adversarial tests to identify vulnerabilities such as sensitive data leakage or prohibited actions. | Enable/Disable toggle<br>Select evaluation template<br>Select evaluation run<br>Set schedule frequency (weekly recommended) |
| **Alerts** | Monitors for performance anomalies, evaluation failures, and security risks. Integrates with Azure Monitor for automated notifications. | Configure alerts for:<br>- Performance anomalies (latency spikes, token overuse)<br>- Evaluation failures (low coherence scores)<br>- Security risks detected during red-teaming |


## Next steps

- [Continuously evaluate your AI agents (preview)](/azure/ai-foundry/how-to/continuous-evaluation-agents)
- [Trace and observe AI agents in Foundry (preview)](/azure/ai-foundry/how-to/develop/trace-agents-sdk)
- [Monitor your generative AI applications (preview)](/azure/ai-foundry/how-to/monitor-applications)
