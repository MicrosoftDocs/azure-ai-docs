---
title: Monitor online endpoints
titleSuffix: Azure Machine Learning
description: Monitor online endpoints and create alerts with Application Insights.
services: machine-learning
ms.service: azure-machine-learning
ms.reviewer: None
author: msakande
ms.author: mopeakande
ms.subservice: mlops
ms.date: 10/24/2023
ms.topic: conceptual
ms.custom: how-to, devplatv2
---

# Monitor online endpoints

Azure Machine Learning uses integration with Azure Monitor to track and monitor metrics and logs for [online endpoints](concept-endpoints.md). You can view metrics in charts, compare between endpoints and deployments, pin to Azure portal dashboards, configure alerts, query from log tables, and push logs to supported targets. You can also use Application Insights to analyze events from user containers.

* **Metrics**: For endpoint-level metrics such as request latency, requests per minute, new connections per second, and network bytes, you can drill down to see details at the deployment level or status level. Deployment-level metrics such as CPU/GPU utilization and memory or disk utilization can also be drilled down to instance level. Azure Monitor allows tracking these metrics in charts and setting up dashboards and alerts for further analysis.

* **Logs**: You can send metrics to the Log Analytics workspace where you can query the logs using Kusto query syntax. You can also send metrics to Azure Storage accounts and/or Event Hubs for further processing. In addition, you can use dedicated log tables for online endpoint related events, traffic, and console (container) logs. Kusto query allows complex analysis and joining of multiple tables.

* **Application insights**: Curated environments include integration with Application Insights, and you can enable or disable this integration when you create an online deployment. Built-in metrics and logs are sent to Application Insights, and you can use the built-in features of Application Insights (such as Live metrics, Transaction search, Failures, and Performance) for further analysis. 

In this article you learn how to:

> [!div class="checklist"]
> * Choose the right method to view and track metrics and logs
> * View metrics for your online endpoint
> * Create a dashboard for your metrics
> * Create a metric alert
> * View logs for your online endpoint
> * Use Application Insights to track metrics and logs 

## Prerequisites

- An Azure Machine Learning online endpoint.
- At least [Reader access](/azure/role-based-access-control/role-assignments-portal) on the endpoint.

## Metrics

In the Azure portal, you can view metrics pages for online endpoints or deployments. An easy way to access these metrics pages is through links that are available in the Azure Machine Learning studio user interface. You can find these links in the **Details** tab of an endpoint's page. These links lead to the metrics page in the Azure portal for the endpoint or deployment. Alternatively, you can also go to the Azure portal and search for the metrics page for the endpoint or deployment.

To access the metrics pages through links that are available in the studio, take the following steps:

1. In [Azure Machine Learning studio](https://ml.azure.com), go to your workspace.

1. Under **Assets**, select **Endpoints**.

1. Select the name of an endpoint.

1. Under **Endpoint attributes**, select **View metrics**.

   :::image type="content" source="media/how-to-monitor-online-endpoints/online-endpoints-access-metrics-studio.png" alt-text="A screenshot showing how to access the metrics of an endpoint and deployment from the studio UI." lightbox="media/how-to-monitor-online-endpoints/online-endpoints-access-metrics-studio.png":::

   The endpoint's metrics page opens in the Azure portal.

1. In Azure Machine Learning studio, go to the section for a deployment, and then select **View metrics**.

   :::image type="content" source="media/how-to-monitor-online-endpoints/deployment-metrics-studio.png" alt-text="A screenshot showing how to access the metrics of an endpoint and deployment from the studio UI." lightbox="media/how-to-monitor-online-endpoints/deployment-metrics-studio.png":::

   The deployment's metrics page opens in the Azure portal.

To access metrics directly from the Azure portal, take the following steps:

1. Go to the [Azure portal](https://portal.azure.com).

1. Go to the online endpoint or deployment resource.

   Online endpoints and deployments are Azure Resource Manager resources. You can find them by going to their resource group and then looking for the resource types **Machine Learning online endpoint** and **Machine Learning online deployment**.

1. Under **Monitoring**, select **Metrics**.

   :::image type="content" source="media/how-to-monitor-online-endpoints/endpoint-metrics-azure-portal.png" alt-text="A screenshot showing how to access the metrics of an endpoint and deployment from the studio UI." lightbox="media/how-to-monitor-online-endpoints/endpoint-metrics-azure-portal.png":::

### Available metrics

The metrics that you see depend on the resource that you select. Metrics are scoped differently for online endpoints and online deployments.

#### Metrics at endpoint scope

[!INCLUDE [Microsoft.MachineLearningServices/workspaces](~/reusable-content/ce-skilling/azure/includes/azure-monitor/reference/metrics/microsoft-machinelearningservices-workspaces-onlineendpoints-metrics-include.md)]

**Bandwidth throttling**

Bandwidth will be throttled if the quota limits are exceeded for _managed_ online endpoints. For more information on limits, see the article on [limits for online endpoints](how-to-manage-quotas.md#azure-machine-learning-online-endpoints-and-batch-endpoints). To determine if requests are throttled:
- Monitor the "Network bytes" metric
- The response trailers will have the fields: `ms-azureml-bandwidth-request-delay-ms` and `ms-azureml-bandwidth-response-delay-ms`. The values of the fields are the delays, in milliseconds, of the bandwidth throttling.

For more information, see [Bandwidth limit issues](how-to-troubleshoot-online-endpoints.md#bandwidth-limit-issues).

#### Metrics at deployment scope

[!INCLUDE [Microsoft.MachineLearningServices/workspaces/onlineEndpoints/deployments](~/reusable-content/ce-skilling/azure/includes/azure-monitor/reference/metrics/microsoft-machinelearningservices-workspaces-onlineendpoints-deployments-metrics-include.md)]

### Create dashboards and alerts

Azure Monitor allows you to create dashboards and alerts that are based on metrics.

#### Create dashboards and visualize queries

You can create custom dashboards and visualize metrics from multiple sources in the Azure portal, including the metrics for your online endpoint. For more information on creating dashboards and visualizing queries, see [Dashboards using log data](/azure/azure-monitor/visualize/tutorial-logs-dashboards) and [Dashboards using application data](/azure/azure-monitor/app/overview-dashboard#create-custom-kpi-dashboards-using-application-insights).
    
#### Create alerts

You can also create custom alerts so you can receive notifications about important status updates to your online endpoint:

1. In the Azure portal, go to a metrics page, and then select **New alert rule**.

   :::image type="content" source="./media/how-to-monitor-online-endpoints/online-endpoints-new-alert-rule.png" alt-text="Screenshot showing 'New alert rule' button surrounded by a red box."  lightbox="./media/how-to-monitor-online-endpoints/online-endpoints-new-alert-rule.png" :::

1. In the Select a signal window, select the signal that you want to create an alert for, and then select **Apply**.

1. In the Create an alert rule page, enter a threshold, and edit any other settings that you want to adjust. For more information about alert rule settings, see [Configure the alert rule conditions](/azure/azure-monitor/alerts/alerts-create-metric-alert-rule#configure-the-alert-rule-conditions). Then select **Next: Actions**.

   :::image type="content" source="./media/how-to-monitor-online-endpoints/configure-alert-rule.png" alt-text="Screenshot showing 'New alert rule' button surrounded by a red box."  lightbox="./media/how-to-monitor-online-endpoints/configure-alert-rule.png" :::

1. In the Select action groups window, create or select an action group to specify what happens when your alert is triggered. For more information, see [Configure the alert rule details](/azure/azure-monitor/alerts/alerts-create-metric-alert-rule#configure-the-alert-rule-details).

1. Choose **Review + Create** to finish creating your alert.

### Scale automatically based on metrics

You can configure deployments to scale automatically based on metrics. To turn on the autoscale feature, you can use the UI or code. The options for code are the Azure Machine Learning CLI and the Azure Machine Learning SDK for Python. When you use code, you provide the IDs of metrics in the conditions for triggering automatic scaling. For those IDs, you can use the metrics that the table lists in the [Available metrics](#available-metrics) section. For more information, see [Autoscaling online endpoints](how-to-autoscale-endpoints.md).

## Logs

There are three logs that you can turn on for online endpoints:

* **AmlOnlineEndpointTrafficLog**: This traffic log provides a way for you to check the information of requests to the endpoint. This log is useful in the following cases:
  * A request response isn't 200, and you want more information. The `ResponseCodeReason` column in the log lists the reason. For a description of status codes and reasons, you can also see [HTTPS status codes](how-to-troubleshoot-online-endpoints.md#http-status-codes) in the article about troubleshooting online endpoints.
  * You want to look up the response code and response reason of your model for a request. The `ModelStatusCode` and `ModelStatusReason` columns provide this information.
  * You want to know the duration of a request. The logs provide a breakdown of the latency that shows the total duration, the request duration, the response duration, and the delay caused by network throttling.
  * You want to check how many recent requests succeeded and failed. The logs provide this information.
* **AmlOnlineEndpointConsoleLog**: This log contains statements that the containers write as output to the console. This log is useful in the following cases:
  * A container fails to start. The console log can be useful for debugging.
  * You want to monitor container behavior and make sure that all requests are correctly handled.
  * You want to write request IDs in the console log. Joining the request ID, the AmlOnlineEndpointConsoleLog, and AmlOnlineEndpointTrafficLog in the Log Analytics workspace, you can trace a request from the network entry point of an online endpoint to the container.
  * You want to run a performance analysis. For instance, you want to determine the time the model needs to process each request.
* **AmlOnlineEndpointEventLog**: This log contains event information about the container life cycle. Currently, the log provides information about the following types of events:

  | Name | Message |
  | ----- | ----- | 
  | BackOff | Back-off restarting failed container |
  | Pulled | Container image "\<IMAGE\_NAME\>" already present on machine |
  | Killing | Container inference-server failed liveness probe, will be restarted |
  | Created | Created container image-fetcher |
  | Created | Created container inference-server |
  | Created | Created container model-mount |
  | LivenessProbeFailed | Liveness probe failed: \<FAILURE\_CONTENT\> |
  | ReadinessProbeFailed | Readiness probe failed: \<FAILURE\_CONTENT\> |
  | Started | Started container image-fetcher |
  | Started | Started container inference-server |
  | Started | Started container model-mount |
  | Killing | Stopping container inference-server |
  | Killing | Stopping container model-mount |

### Turn logs on or off

> [!IMPORTANT]
> Logging uses Azure Log Analytics. If you don't currently have a Log Analytics workspace, you can create one by using the steps in [Create a Log Analytics workspace in the Azure portal](/azure/azure-monitor/logs/quick-create-workspace#create-a-workspace).

1. In the [Azure portal](https://portal.azure.com), go to the resource group that contains your endpoint, and then select the endpoint.

1. Under **Monitoring**, select **Diagnostic settings**, and then select **Add diagnostic setting**.

1. In the Diagnostic setting window, enter the following information:
   - Next to **Diagnostic setting name**, enter a name for your setting.
   - Select the log categories that you want to turn on.
   - Select **Send to Log Analytics workspace**, and then select the subscription and the Log Analytics workspace to use.

   :::image type="content" source="./media/how-to-monitor-online-endpoints/diagnostic-settings.png" alt-text="Screenshot of the diagnostic settings dialog.":::

1. Select **Save**.

    > [!IMPORTANT]
    > It may take up to an hour for the connection to the Log Analytics workspace to be enabled. Wait an hour before continuing with the steps in the next section.

### View logs

1. Submit scoring requests to the endpoint to create entries in the logs.

1. Go to the Azure portal, and then use one of the following options to open the logs:
   - Go to the properties page for your online endpoint. Under **Monitoring**, select **Logs**.
   - Go to your Log Analytics workspace. On the left, select **Logs**.

1. Close the **Queries hub** window that automatically opens.

1. Under **Other**, double-click **AmlOnlineEndpointConsoleLog**. If you don't see **AmlOnlineEndpointConsoleLog**, enter that value into the search field.

    :::image type="content" source="./media/how-to-monitor-online-endpoints/online-endpoints-log-queries.png" alt-text="Screenshot showing the log queries.":::

1. Select **Run**.

    :::image type="content" source="./media/how-to-monitor-online-endpoints/query-results.png" alt-text="Screenshots of the results after running a query.":::

### Example queries

Example queries are available for you to use. Take the following steps to view them:

1. On the Logs page, select **Queries**.

1. In the search box, enter **Online endpoint**.

:::image type="content" source="./media/how-to-monitor-online-endpoints/example-queries.png" alt-text="Screenshot of the Queries tab of the Azure portal Logs page. Two example queries are visible, and the Queries tab and the search box are highlighted.":::

### Log column details 

The following tables provide detailed information about the data that's stored in each log:

**AmlOnlineEndpointTrafficLog**

[!INCLUDE [endpoint-monitor-traffic-reference](includes/endpoint-monitor-traffic-reference.md)]

**AmlOnlineEndpointConsoleLog**

[!INCLUDE [endpoint-monitor-console-reference](includes/endpoint-monitor-console-reference.md)]

**AmlOnlineEndpointEventLog**

[!INCLUDE [endpoint-monitor-event-reference](includes/endpoint-monitor-event-reference.md)]

## Use Application Insights

Curated environments include integration with Application Insights. Through this integration, built-in metrics and logs are sent to Application Insights. You can then use Application Insights built-in features, such as live metrics, transaction search, failures, and performance, for further analysis.

For more information, see [Application Insights overview](/azure/azure-monitor/app/app-insights-overview).

You can turn on integration with Application Insights when you create an online deployment in the studio. On the Deployment page, under **Application Insights diagnostics**, select **Enabled**.

:::image type="content" source="media/how-to-monitor-online-endpoints/turn-on-application-insights-diagnostics.png" lightbox="media/how-to-monitor-online-endpoints/turn-on-application-insights-diagnostics.png" alt-text="Screenshot of the studio Deployment page when a user creates an online endpoint. The Application Insights diagnostics setting is highlighted.":::

When you turn on Application Insights, you can see high-level activity monitor graphs for a managed online endpoint. In the studio, go to the endpoint's page, and then select the **Monitoring** tab. 

:::image type="content" source="media/how-to-monitor-online-endpoints/monitor-endpoint.png" lightbox="media/how-to-monitor-online-endpoints/monitor-endpoint.png" alt-text="Screenshot of the Monitoring tab on a studio endpoint page. The Monitoring tab is highlighted. A chart shows requests per minute to the endpoint.":::

## Related content

* Learn how to [view costs for your deployed endpoint](./how-to-view-online-endpoints-costs.md).
* Read more about [metrics explorer](/azure/azure-monitor/essentials/metrics-charts).
