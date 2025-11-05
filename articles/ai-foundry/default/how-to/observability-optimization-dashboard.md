---
title: Monitoring dashboard insights in Azure AI Foundry with Foundry Agent
titleSuffix: Azure AI Foundry 
description: Discover how to use Foundry Agent in Azure AI Foundry to interpret your monitoring dashboard and gain actionable insights for better decision-making.
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 11/18/2025
ms.reviewer: hanch
ms.author: lagayhar
author: lgayhardt
ai-usage: ai-assisted 
---
 

# Monitoring Dashboard Insights in Azure AI Foundry with Foundry Agent

Once your agent is in production, you can set up and view various metrics in the monitoring dashboard or control plane dashboard. You can use **Azure AI Foundry Agent** - the built-in chat assistant to get a summary on your dashboard data and recommend next steps without leaving the Foundry portal.

This article describes the integrated user experience and system behavior how you get a dashboard summary or insights through Foundry Agent.

## Prerequisites

Before you begin:

- You have access to the **Azure AI Foundry portal**.
- You have one or more published agents.
- You have access to **Foundry Agent** (the chat assistant).

## Start a chat with Foundry Agent

You can start a chat with Foundry Agent from any page in the Foundry portal.

1. Select the **Ask AI** icon at the top of the page.
1. Select one of the predefined prompts from the **Ask AI** banner under *Build/Model/Monitor* or *Build/Agent/Monitor* page.
1. Select one of the predefined prompts from the **Ask AI** banner under *Operate* page.

## Get a summary / insight of your dashboard

You can ask Foundry Agent questions like:

- “Give me a summary of the dashboard”
- “Analyze the performance trend of my dashboard”

Or you can select predefined prompt under *Ask AI* banner, and the question passes to the Foundry Agent.

Foundry Agent provides highlights and abnormal behavior insights on your dashboard with selected time period and provide annotated link to the chart it refers to. When you select any annotated link, it will scroll directly to the chart with a highlighted background for you to easily distinguish.

## Get recommended next steps

You can also ask any free form questions related to your dashboard and get recommended next steps. Some suggested action items include:

- Investigate what caused the latency increase on [the abnormal date] to ensure it isn't a recurring or growing issue.
- Monitor whether future requests show similar latency patterns when usage increases.
- Consider load testing or profiling to identify potential bottlenecks causing slower response times.
- Optimize prompt and completion token usage, if possible, to reduce load and costs as usage scales.
- Keep observing token consumption and request frequency trends for early signs of performance degradation.

## Related content

- [Evaluate your AI agents locally with the Azure AI Evaluation SDK](../..//how-to/develop/agent-evaluate-sdk.md)
- [Agent tracing overview](../concepts/trace-agent-concept.md)
