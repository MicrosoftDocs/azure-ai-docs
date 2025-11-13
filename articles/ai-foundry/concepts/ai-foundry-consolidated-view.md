---
title: Consolidated View for AI Services in the Azure portal
description: Discover how the Foundry consolidated view in the Azure portal simplifies AI workload management with cost, usage, and quota insights in one place.
#customer intent: As an Azure user managing AI workloads, I want to monitor costs and resource usage in a single view so that I can optimize spending and performance.
author: jonburchel
ms.author: jburchel
ms.reviewer: aashishb
ms.date: 09/29/2025
ms.topic: concept-article
ms.service: azure-ai-foundry
---

# Consolidated view for AI services in the Azure portal

The [Foundry consolidated view](https://portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/overview) shows key insights about your AI workloads in the Azure portal. Instead of switching between tools, you see in one place how your AI resources perform, what they cost, and whether you’re nearing usage limits.

## Why use the consolidated view?

- **Faster visibility**: Check cost, quota, and resource usage at a glance.
- **Built-in governance**: Spot early warning signs like quota thresholds and cost spikes before they become blockers.
- **Lightweight experience**: No new resource types or complex setup required. It surfaces what you already use.

## Key features

- **Alerts and service health**

  View key alerts for your AI resources so you can investigate and fix issues without leaving the dashboard.

- **Accumulated costs**

   View your costs over time by subscription or resource type. Identify trends, track experiments, and drill into **Cost management** for deeper analysis.

- **Active resources by cost**

  You can see which active resources are driving the most spend to help you optimize usage and clean up idle resources quickly.

- **Model utilization**

  Track AI model usage over time. Spot peaks, dips, and usage patterns across your projects to make better scaling decisions.

- **Resource breakdown by type**

  Understand which AI services you use most (for example, Azure OpenAI, Speech, Language). This helps with cost allocation and planning for future workloads.

- **Quota utilization**

  Monitor quota usage by model and region. Stay ahead of capacity issues with quick links to **Quota management** for requesting increases.

## Visual layout of the consolidated view

The dashboard shows tiles for each visibility area:

- **Top row**: Alerts, active resources by cost, and accumulated costs
- **Middle row**: Model utilization over time
- **Bottom row**: Resource breakdown by type and quota utilization

:::image type="content" source="../media/ai-foundry-consolidated-view/consolidated-view-dashboard.png" alt-text="Screenshot of a dashboard with tiles for alerts, resource costs, model utilization, resource breakdown, and quota utilization." lightbox="../media/ai-foundry-consolidated-view/consolidated-view-dashboard.png":::

## What you can do next

- Open **Cost analysis** from the dashboard to analyze costs.
- Request quota increases in **Quota management** when you reach limits.
- Use utilization insights to decide where to scale, pause, or reallocate resources.
- Keep AI projects running smoothly by acting on alerts.

## Related content

- [Microsoft Foundry management center](management-center.md)
- [Foundry status dashboard](../azure-ai-foundry-status-dashboard-documentation.md)
