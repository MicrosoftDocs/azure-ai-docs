---
title: Consolidated view in the AI Foundry portal
description: Discover how the AI Foundry consolidated view in the Azure portal simplifies AI workload management with cost, usage, and quota insights in one place.
#customer intent: As an Azure user managing AI workloads, I want to monitor costs and resource usage in a single view so that I can optimize spending and performance.
author: jonburchel
ms.author: jburchel
ms.reviewer: aashishb
ms.date: 09/26/2025
ms.topic: concept-article
ms.service: azure-ai-foundry
---

# Consolidated view in the Azure AI Foundry portal

The **AI Foundry consolidate view** brings the most important insights about your AI workloads directly into the Azure Portal. Instead of jumping between multiple tools, you now have a single place to see how your AI resources are performing, what they’re costing, and whether you’re approaching your usage limits.

## Why use the consolidated view?

- **Faster visibility**: Check cost, quota, and resource usage at a glance.
- **Built-in governance**: Spot early warning signs like quota thresholds and cost spikes before they become blockers.
- **Seamless integration**: Deep-link into familiar Azure blades like **Cost management** and **Quota management** without losing context.
- **Lightweight experience**: No new resource types or complex setup required. Everything is surfaced from what you already use.

# Key Features

- **Accumulated costs**

   Visualize spend over time, broken down by subscription or resource type. Identify trends, track experiments, and drill down into **Cost management** for detailed analysis.

- **Active resources by cost**

  See which active resources are driving the most spend. This helps you optimize usage and clean up idle resources quickly.

- **Model utilization**

  Track how your AI models are being used over time. Spot peaks, dips, and usage patterns across your projects to make better scaling decisions.

- **Resource breakdown by type**

  Understand which AI services you’re consuming most (for example, Azure OpenAI, Speech, Language). This helps with cost allocation and planning for future workloads.

- **Quota utilization**

  Monitor quota usage by model and region. Stay ahead of capacity issues with quick links to **Quota management** for requesting increases.

- **Alerts and service health**

  Surface key alerts tied to your AI resources, so you can investigate and resolve issues without leaving the dashboard.

## Visual layout of the consolidated view

The view's dashboard is organized into tiles, each dedicated to a specific area of visibility:

- **Top row**: Alerts, active resources by cost, accumulated costs
- **Middle row**: Model utilization over time
- **Bottom row**: Resource breakdown by type, quota utilization

## What you can do next

- Open **Cost analysis** directly from the dashboard to drill deeper into spend.
- Request quota increases via **Quota management** when you hit thresholds.
- Use utilization insights to guide where to scale, pause, or reallocate resources.
- Keep AI projects running smoothly by acting on surfaced alerts.

## Related content

- [Azure AI Foundry Management center](management-center.md)
- [Azure AI Foundry status dashboard](../azure-ai-foundry-status-dashboard-documentation.md)
