---
title: Monitor your Generative AI Applications
titleSuffix: Microsoft Foundry
description: This article provides instructions on how to continuously monitor Generative AI Applications.
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 01/30/2026
ms.reviewer: amibp
ms.author: lagayhar  
author: lgayhardt
ai-usage: ai-assisted
---

# Monitor your generative AI applications (preview)

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Monitoring your generative AI applications is important because of the complexity and rapid evolution of the AI industry. By using observability integrated with Azure Monitor Application Insights, you can continuously monitor your deployed AI applications to ensure that they're performant, safe, and produce high-quality results in production. In addition to the continuous monitoring capabilities, the Foundry Observability dashboard also provides [continuous evaluation capabilities for Agents](./continuous-evaluation-agents.md) with visibility into critical quality and safety metrics.

[!INCLUDE [uses-fdp-only](../includes/uses-fdp-only.md)]

## How to enable monitoring

To use monitoring capabilities in Microsoft Foundry, connect an Application Insights resource to your Foundry project.

1. Navigate to **Monitoring** in the left navigation pane of the Foundry portal.
1. Select the **Application analytics** tab.
1. Create a new Application Insights resource if you don't already have one.
1. Connect the resource to your Foundry project.

### Collect production data for monitoring

Start collecting telemetry for your application that you can monitor in the built-in views. To do this, follow these recommendations:

- Instrument traces to capture detailed telemetry data from your application. This data provides insights into the performance, latency, and behavior of your application in production.

- Use [continuous evaluations](./continuous-evaluation-agents.md) to help monitor the quality and safety of your agent in production by assessing its outputs against predefined metrics and thresholds.

## Viewing monitoring results

In Foundry portal, the **Application analytics** dashboard view uses signals from [Azure Monitor Application Insights](/azure/azure-monitor/app/overview-dashboard), querying it through [Azure Workbooks](/azure/azure-monitor/visualize/workbooks-overview) and creating visualizations.

These views bring key metrics - token consumption, latency, exceptions, response quality - into a single pane that provides transparency to teams. They help teams track operational health and quality, understand trends, and continuously assess to improve their application.

Follow these steps to access and utilize the built-in monitoring view in your Foundry Project:

1. Go to your Foundry Project in the Foundry portal.
1. Select **Monitoring** from the left navigation pane.
1. Under the **Application analytics** tab, review the overview of your application's health.
1. Use filters to specify a time range, application, and model to extract detailed insights.
1. If you notice problems, such as declining quality metrics, go to **Tracing** to [debug problems in your application](./develop/trace-application.md).
1. To further customize your monitoring experience and use advanced capabilities in Azure Monitor, select **View in Azure Monitor Application Insights**.

> [!NOTE]
> When you share this workbook with your team members, they must have at least the **Reader** role to the connected Application Insights resource to view the displayed information.

## Customize and share your dashboard

Application Insights is a powerful tool for application performance monitoring (APM) that provides insights into the health and performance of your applications.

You can open the **Application analytics** dashboard in Azure Monitor Application Insights workbooks gallery by selecting the **View in Azure Monitor Application Insights** link at the end of the page.

This dashboard is opened as an editable workbook where you can customize the workbook and save according to your needs.

1. Select **Edit** in the command bar.
    :::image type="content" source="../media/how-to/monitor-applications/customize-dashboard-2.png" alt-text="Screenshot of the workbooks tab under monitoring highlighting the edit button in the Azure portal." lightbox="../media/how-to/monitor-applications/customize-dashboard-2.png":::

1. Modify elements as needed for your use case. Select **...** on an element to edit, add, move, resize, clone, or remove. For example, you can add a tile by using KQL to track a custom attribute you're collecting and that isn't shown in the built-in view.
    :::image type="content" source="../media/how-to/monitor-applications/customize-dashboard-3.png" alt-text="Screenshot of workbooks tab under monitoring highlighting modify element buttons in Azure portal." lightbox="../media/how-to/monitor-applications/customize-dashboard-3.png":::

1. Save your latest changes and create different views as needed by selecting **Save**.
    :::image type="content" source="../media/how-to/monitor-applications/customize-dashboard-4.png" alt-text="Screenshot of workbooks tab under monitoring highlighting the save button and tab in Azure portal." lightbox="../media/how-to/monitor-applications/customize-dashboard-4.png":::

1. Share by selecting the **Share** icon in the command bar.
    :::image type="content" source="../media/how-to/monitor-applications/customize-dashboard-5.png" alt-text="Screenshot of workbooks tab under monitoring highlighting share workbook button and tab in Azure portal." lightbox="../media/how-to/monitor-applications/customize-dashboard-5.png":::

## Explore and analyze with Kusto Query Language (KQL)

[KQL (Kusto Query Language)](/kusto/query/) is a powerful query language you can use in Azure to explore, analyze, and visualize large volumes of telemetry and log data.

In the **Application analytics** dashboard view, you can **Open query link** by selecting the icon in the upper right for a particular tile or chart.

:::image type="content" source="../media/how-to/monitor-applications/query-link.png" alt-text="Screenshot of application analytics dashboard view highlighting the open query link button in Azure portal." lightbox="../media/how-to/monitor-applications/query-link.png":::

When you select that icon, you can view and run the same KQL queries that power your monitoring view. You can also deep dive into the related data.

:::image type="content" source="../media/how-to/monitor-applications/kql-mode.png" alt-text="Screenshot of logs highlighting KQL mode and results in Azure portal. " lightbox="../media/how-to/monitor-applications/kql-mode.png":::

## Set up Azure Alerts

You can define Azure Alert rules based on the previous KQL queries to proactively detect problems with your post-production operations. Select **...** to view more options like **New alert rule**.

:::image type="content" source="../media/how-to/monitor-applications/create-new-alert-rule-1.png" alt-text="Screenshot of logs highlighting new alert rule button in Azure portal." lightbox="../media/how-to/monitor-applications/create-new-alert-rule-1.png":::

Selecting the **New alert rule** button opens a wizard to create an alert rule on the related signal.

:::image type="content" source="../media/how-to/monitor-applications/create-new-alert-rule-2.png" alt-text="Screenshot of create an alert rule wizard in Azure portal." lightbox="../media/how-to/monitor-applications/create-new-alert-rule-2.png":::

To learn more about setting up and managing Azure Alerts to proactively address problems, see [Alerts in Azure Monitor](/azure/azure-monitor/alerts/alerts-overview).

## Related content

- [Monitor model deployments](../foundry-models/how-to/monitor-models.md#metrics-explorer)
