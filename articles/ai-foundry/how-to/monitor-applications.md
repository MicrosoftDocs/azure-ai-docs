---
title: Monitor your Generative AI Applications
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to continuously monitor Generative AI Applications.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 05/19/2025
ms.reviewer: amibp
ms.author: lagayhar  
author: lgayhardt
---

# Monitor your generative AI applications (preview)

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Monitoring your generative AI applications has never been more important, due to the complexity and rapid evolvement of the AI industry. Azure AI Foundry Observability, integrated with Azure Monitor Application Insights, enables you to continuously monitor your deployed AI applications to ensure that they're performant, safe, and produce high-quality results in production. In addition to the continuous monitoring capabilities, we also provide [continuous evaluation capabilities for Agents](./continuous-evaluation-agents.md) to add further enhance the Foundry Observability dashboard with visibility into additional critical quality and safety metrics.

## How to enable monitoring

To use monitoring capabilities in Azure AI Foundry, you need to connect an Application Insights resource to your Azure AI Foundry project.

1. Navigate to *Monitoring* in the left navigation pane of the Azure AI Foundry portal.
2. Select the **Application analytics** tab.
3. Create a new Application Insights resource if you don't already have one.
4. Connect the resource to your AI Foundry project.

### Collecting production data for monitoring

From here, you want to begin collecting telemetry for your application that you can monitor in our built-in views. To do this, we recommend:

- Instrumenting traces allows you to capture detailed telemetry data from your application. This data provides insights into the performance, latency, and behavior of your application in production.

- [Continuous evaluations](./continuous-evaluation-agents.md) help monitor the quality and safety of your agent in production by assessing its outputs against predefined metrics and thresholds.

## Viewing monitoring results

These views are designed to bring key metrics - token consumption, latency, exceptions, response quality into a single pane of glass that provides transparency to teams to track operational health and quality, understand trends, and assess continuously to improve their application.

> [!NOTE]
> When you're sharing this workbook with your team members, they must have at least 'Reader' role to the connected Application Insights resource to view the displayed information.

### AI Foundry Portal

Follow these steps to access and utilize the built-in monitoring views in your AI Foundry Project:

1. Navigate to your AI Foundry Project in the Azure AI Foundry portal.
2. Select *Monitoring* from the left navigation pane.
3. Under the **Application analytics** tab, review the overview of your application's health.
4. Use filters to specify a time range, application, and/or model to extract detailed insights.
5. If you notice issues, such as declining quality metrics, go to **Tracing**  to [debug issues in your application](./develop/trace-application.md).
6. To further customize your monitoring experience and use advanced capabilities in Azure Monitor, scroll to the bottom and select **View in Azure Monitor Application Insights**.

## Related content

- [Monitor model deployments](../model-inference/how-to/monitor-models.md#metrics-explorer)