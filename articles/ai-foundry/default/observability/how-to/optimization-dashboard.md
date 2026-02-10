---
title: Monitoring dashboard insights in Microsoft Foundry with Ask AI
titleSuffix: Microsoft Foundry 
description: Discover how to use Ask AI in Microsoft Foundry to interpret your monitoring dashboard and gain actionable insights for better decision-making.
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 11/18/2025
ms.reviewer: hanch
ms.author: lagayhar
author: lgayhardt
ai-usage: ai-assisted 
---
 

# Monitoring dashboard insights in Microsoft Foundry with Ask AI (preview)

[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

After your agent is in production, set up and view various metrics in the monitoring dashboard or control plane dashboard. Use Ask AI—the built-in chat assistant—to get a summary of your dashboard data and recommendations for next steps without leaving the Foundry portal.

This article describes the integrated user experience and system behavior for getting a dashboard summary or insights through Ask AI.

## Prerequisites

- A [Foundry project](../../../how-to/create-projects.md) with one or more [published agents](../../../agents/overview.md).
- Access to **Ask AI** (the chat assistant) in the Foundry portal.

## Start a chat with Ask AI

You can start a chat with Ask AI from any page in the Foundry portal.

1. Select the **Ask AI** icon at the top of the page.
1. Select one of the predefined prompts from the *Ask AI* banner under *Build/Model/Monitor*, *Build/Agent/Monitor*, or overview page.

    :::image type="content" source="../../media/observability/monitor-dashboard.png" alt-text="Screenshot of the monitor dashboard with the Ask AI banner at the top." lightbox="../../media/observability/monitor-dashboard.png":::

    :::image type="content" source="../../media/observability/monitor-dashboard-overview.png" alt-text="Screenshot of the monitor dashboard overview page." lightbox="../../media/observability/monitor-dashboard-overview.png":::

## Get a summary or insight of your dashboard

You can ask questions like:

- "Give me a summary of the dashboard"
- "Analyze the performance trend of my dashboard"

Or you can select a predefined prompt under the *Ask AI* banner, and the question is passed to Ask AI.

Ask AI provides highlights and abnormal behavior insights on your dashboard for the selected time period and provides an annotated link to the chart it refers to. When you select an annotated link, it scrolls directly to the chart with a highlighted background, making it easy to distinguish.

:::image type="content" source="../../media/observability/monitor-dashboard-overview.png" alt-text="Screenshot showing a monitor dashboard summary from Ask AI." lightbox="../../media/observability/monitor-dashboard-summary.png":::

## Get recommended next steps

Ask any free-form questions related to your dashboard to get recommended next steps. Suggested action items include:

- "Investigate the cause of the latency increase on [the abnormal date] to ensure it isn't a recurring or growing issue."
- "Monitor whether future requests show similar latency patterns when usage increases."
- "Consider load testing or profiling to identify potential bottlenecks causing slower response times."
- "Optimize prompt and completion token usage to reduce load and costs as usage scales."
- "Monitor token consumption and request frequency trends for early signs of performance degradation."

## Related content

- [Run evaluations in the cloud](../../../how-to/develop/cloud-evaluation.md?view=foundry&preserve-view=true)
- [Agent tracing overview](../concepts/trace-agent-concept.md)
