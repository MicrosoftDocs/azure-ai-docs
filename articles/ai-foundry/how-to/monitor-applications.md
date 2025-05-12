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

1. Navigate to **Monitoring** in the left navigation pane of the Azure AI Foundry portal.
2. Select the **Application analytics** tab.
3. Create a new Application Insights resource if you don't already have one.
4. Connect the resource to your AI Foundry project.

### Collecting production data for monitoring

From here, you want to begin collecting telemetry for your application that you can monitor in our built-in views. To do this, we recommend:

- Instrumenting traces allows you to capture detailed telemetry data from your application. This data provides insights into the performance, latency, and behavior of your application in production.

- [Continuous evaluations](./continuous-evaluation-agents.md) help monitor the quality and safety of your agent in production by assessing its outputs against predefined metrics and thresholds.

## Viewing monitoring results

In Azure AI Foundry portal, the **Application analytics** dashboard view uses signals from [Azure Monitor Application Insights](/azure/azure-monitor/app/overview-dashboard), querying it through [Azure Workbooks](/azure/azure-monitor/visualize/workbooks-overview) and creating visualizations.

These views are designed to bring key metrics - token consumption, latency, exceptions, response quality into a single pane of glass that provides transparency to teams to track operational health and quality, understand trends, and assess continuously to improve their application.

Follow these steps to access and utilize the built-in monitoring view in your AI Foundry Project:

1. Navigate to your AI Foundry Project in the Azure AI Foundry portal.
2. Select **Monitoring** from the left navigation pane.
3. Under the **Application analytics** tab, review the overview of your application's health.
4. Use filters to specify a time range, application, and/or model to extract detailed insights.
5. If you notice issues, such as declining quality metrics, go to **Tracing**  to [debug issues in your application](./develop/trace-application.md).
6. To further customize your monitoring experience and use advanced capabilities in Azure Monitor, scroll to the bottom and select **View in Azure Monitor Application Insights**.

> [!NOTE]
> When you're sharing this workbook with your team members, they must have at least 'Reader' role to the connected Application Insights resource to view the displayed information.

## Customize and share your dashboard

Application Insights is a powerful tool for application performance monitoring (APM) that provides insights into the health and performance of your applications.

You can open the **Application analytics** dashboard in Azure Monitor Application Insights workbooks gallery by selecting on **View in Azure Monitor Application Insights** link at the end of the page.

This dashboard is opened as an editable workbook where you can customize the workbook and save according to your needs.

1. Select **Edit** in the command bar.
    :::image type="content" source="../media/how-to/monitor-applications/customize-dashboard-2.png" alt-text="Screenshot of the workbooks tab under monitoring highlighting the edit button in the Azure portal." lightbox="../media/how-to/monitor-applications/customize-dashboard-2.png":::

2. Modify elements as needed per your use case. Select **...** on an element to edit, add, move/resize, clone, or remove. For example, you can add a tile using KQL to track a custom attribute you're collecting and not shown in our built-in view.
    :::image type="content" source="../media/how-to/monitor-applications/customize-dashboard-3.png" alt-text="Screenshot of workbooks tab under monitoring highlighting modify element buttons in Azure portal." lightbox="../media/how-to/monitor-applications/customize-dashboard-3.png":::

3. Save your latest changes and create different views as needed by selecting **Save**.
    :::image type="content" source="../media/how-to/monitor-applications/customize-dashboard-4.png" alt-text="Screenshot of workbooks tab under monitoring highlighting the save button and tab in Azure portal." lightbox="../media/how-to/monitor-applications/customize-dashboard-4.png":::

4. Share with your team by selecting "Share" icon in the command bar.
    :::image type="content" source="../media/how-to/monitor-applications/customize-dashboard-5.png" alt-text="Screenshot of workbooks tab under monitoring highlighting share workbook button and tab in Azure portal." lightbox="../media/how-to/monitor-applications/customize-dashboard-5.png":::

## Explore and analyze with Kusto Query Language (KQL)

[KQL (Kusto Query Language)](/kusto/query/) is a powerful query language used in Azure to explore, analyze, and visualize large volumes of telemetry and log data.

In the **Application analytics** dashboard view, you can **Open query link** by selecting on the icon in the top right for a particular tile or chart.

:::image type="content" source="../media/how-to/monitor-applications/kql-1.png" alt-text="Screenshot of application analytics dashboard view highlighting the open query link button in Azure portal." lightbox="../media/how-to/monitor-applications/kql-1.png":::

Once you select that, you can view and run the same KQL queries powering your monitoring view and deep dive into the related data.

:::image type="content" source="../media/how-to/monitor-applications/kql-2.png" alt-text="Screenshot of logs highlighting KQL mode and results in Azure portal. " lightbox="../media/how-to/monitor-applications/kql-2.png":::

## Set up Azure Alerts

You can define Azure Alert rules based on the previous KQL queries to proactively detect issues with your post-production operations in the future. Select **...** to view more options like **New alert rule**.

:::image type="content" source="../media/how-to/monitor-applications/create-new-alert-rule-1.png" alt-text="Screenshot of logs highlighting new alert rule button in Azure portal." lightbox="../media/how-to/monitor-applications/create-new-alert-rule-1.png":::

Selecting on the **New alert rule** button opens a wizard to create an alert rule on the related signal.

:::image type="content" source="../media/how-to/monitor-applications/create-new-alert-rule-2.png" alt-text="Screenshot of create an alert rule wizard in Azure portal." lightbox="../media/how-to/monitor-applications/create-new-alert-rule-2.png":::

To learn more about setting up and managing Azure Alerts to proactively address issues, see [Alerts in Azure Monitor](/azure/azure-monitor/alerts/alerts-overview).

## Related content

- [Monitor model deployments](../model-inference/how-to/monitor-models.md#metrics-explorer)
