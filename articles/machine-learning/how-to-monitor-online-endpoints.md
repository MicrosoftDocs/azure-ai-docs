---
title: Monitor online endpoints
titleSuffix: Azure Machine Learning
description: See how to monitor Azure Machine Learning online endpoints. Find out how to use available metrics, logs, and the integration with Application Insights.
services: machine-learning
ms.service: azure-machine-learning
ms.reviewer: jturuk
reviewer: Jagatjeet
author: s-polly
ms.author: scottpolly
ms.subservice: mlops
ms.date: 02/05/2026
ms.topic: how-to
ms.custom: how-to, devplatv2
# customer intent: As a developer, I want to see how to use metrics, logs, and Application Insights to monitor my Azure Machine Learning online endpoints so that I can track and analyze endpoint behavior.
---

# Monitor online endpoints

Azure Machine Learning uses integration with Azure Monitor to track and monitor metrics and logs for [online endpoints](concept-endpoints.md). You can view metrics in charts, compare metrics among endpoints and deployments, pin metrics to Azure portal dashboards, configure alerts, query log tables, and push logs to supported targets. You can also use Application Insights to analyze events from user containers.

* **Metrics**: For endpoint-level metrics such as request latency, requests per minute, new connections per second, and network bytes, you can drill down to see detailed information at the deployment level or status level. You can also drill down deployment-level metrics such as CPU/GPU usage and memory or disk usage to the instance level. In Monitor, you can track these metrics in charts, and you can set up dashboards and alerts for further analysis.

* **Logs**: You can send metrics to a Log Analytics workspace, where you can use Kusto query syntax to query the logs. You can also send metrics to Azure Storage accounts or Azure Event Hubs for further processing. For traffic, console (container) logs, and events related to online endpoints, you can use dedicated log tables. Kusto queries support complex analysis capabilities and the joining of multiple tables.

* **Application Insights**: Curated environments include integration with Application Insights. You can turn this integration on or off when you create an online deployment. When you turn it on, built-in metrics and logs are sent to Application Insights. You can then use the built-in features of Application Insights for further analysis. Examples of those features include live metrics, the transaction search, the failures view, and the performance view.

In this article, you learn how to:

* Choose the right method to view and track metrics and logs.
* View metrics for your online endpoint.
* Create a dashboard for your metrics.
* Create a metric alert.
* View logs for your online endpoint.
* Use Application Insights to track metrics and logs.

## Prerequisites

- An Azure Machine Learning online endpoint
- At least [Reader access](/azure/role-based-access-control/role-assignments-portal) on the endpoint

## Use metrics

In the Azure portal, you can view metrics pages for online endpoints and deployments.

### Access metrics from Azure Machine Learning studio

An easy way to access metrics pages is through links that are available in the Azure Machine Learning studio user interface. You can find these links in the **Details** tab of an endpoint's page. These links lead to the metrics page in the Azure portal for the endpoint or deployment.

To access the metrics pages through links that are available in the studio, take the following steps:

1. In [Azure Machine Learning studio](https://ml.azure.com), go to your workspace.

1. Under **Assets**, select **Endpoints**.

1. Select the name of an endpoint.

1. Under **Endpoint attributes**, select **View metrics**.

   :::image type="content" source="media/how-to-monitor-online-endpoints/online-endpoints-access-metrics-studio.png" alt-text="Screenshot of an endpoint page in the studio that shows endpoint attributes. Assets, Endpoints, Endpoint attributes, and View metrics are highlighted." lightbox="media/how-to-monitor-online-endpoints/online-endpoints-access-metrics-studio.png":::

   The portal opens to the endpoint's metrics page.

1. In Azure Machine Learning studio, on an endpoint page, go to the section for a deployment, and then select **View metrics**.

   :::image type="content" source="media/how-to-monitor-online-endpoints/deployment-metrics-studio.png" alt-text="Screenshot of an endpoint page in the studio that shows deployment information. Deployment blue and View metrics are highlighted." lightbox="media/how-to-monitor-online-endpoints/deployment-metrics-studio.png":::

   The portal opens to the deployment's metrics page.

### Access metrics from the Azure portal

You can view the metrics for an endpoint or deployment in the Azure portal. Follow these steps:

1. Go to the [Azure portal](https://portal.azure.com).

1. Go to the online endpoint or deployment resource.

   Online endpoints and deployments are Azure Resource Manager resources. You can find them by going to their resource group and then looking for the resource types **Machine Learning online endpoint** and **Machine Learning online deployment**.

1. On the resource page, under **Monitoring**, select **Metrics**.

   :::image type="content" source="media/how-to-monitor-online-endpoints/endpoint-metrics-azure-portal.png" alt-text="Screenshot of the Azure portal that shows the Metrics page for a deployment. Monitoring and Metrics are highlighted." lightbox="media/how-to-monitor-online-endpoints/endpoint-metrics-azure-portal.png":::

### Available metrics

The metrics that you see depend on the resource that you select. Metrics for online endpoints and online deployments are scoped differently.

#### Metrics at the endpoint scope

For information about metrics that are available at the online endpoint scope, see [Supported metrics for Microsoft.MachineLearningServices/workspaces/onlineEndpoints](monitor-azure-machine-learning-reference.md#supported-metrics-for-microsoftmachinelearningservicesworkspacesonlineendpoints).

##### Bandwidth throttling

Bandwidth is throttled if quota limits are exceeded for _managed_ online endpoints. For more information about limits for online endpoints, see [Azure Machine Learning online endpoints and batch endpoints](how-to-manage-quotas.md#azure-machine-learning-online-endpoints-and-batch-endpoints) in the article about quotas and limits in Azure Machine Learning. To determine whether requests are throttled:

- Monitor the Network bytes metric.
- Check for the following fields in the response trailers: `ms-azureml-bandwidth-request-delay-ms` and `ms-azureml-bandwidth-response-delay-ms`. The values of the fields are the delays, in milliseconds, of the bandwidth throttling.

For more information, see [Bandwidth limit issues](how-to-troubleshoot-online-endpoints.md#bandwidth-limit-issues).

#### Metrics at the deployment scope

For information about metrics that are available at the deployment scope, see [Supported metrics for Microsoft.MachineLearningServices/workspaces/onlineEndpoints/deployments](monitor-azure-machine-learning-reference.md#supported-metrics-for-microsoftmachinelearningservicesworkspacesonlineendpointsdeployments).

### Create dashboards and alerts

In Monitor, you can create dashboards and alerts that are based on metrics.

#### Create dashboards and visualize queries

You can create custom dashboards so that you can visualize metrics from multiple sources in the Azure portal, including the metrics for your online endpoint. For more information about creating dashboards and visualizing queries, see [Create and share dashboards of Log Analytics data](/azure/azure-monitor/visualize/tutorial-logs-dashboards) and [Create custom KPI dashboards using Application Insights](/azure/azure-monitor/app/overview-dashboard#create-custom-kpi-dashboards-using-application-insights).
    
#### Create alerts

You can also create custom alerts so that you receive notifications about important status updates to your online endpoint:

1. In the Azure portal, go to a metrics page, and then select **New alert rule**.

   :::image type="content" source="media/how-to-monitor-online-endpoints/online-endpoints-new-alert-rule.png" alt-text="Screenshot of the Azure portal that shows the Metrics page for a deployment. New alert rule is highlighted."  lightbox="media/how-to-monitor-online-endpoints/online-endpoints-new-alert-rule.png" :::

1. In the **Select a signal** window, select the signal that you want to create an alert for, and then select **Apply**.

1. In the **Create an alert rule** page, enter a threshold, and edit any other settings that you want to adjust. For more information about alert rule settings, see [Configure the alert rule conditions](/azure/azure-monitor/alerts/alerts-create-metric-alert-rule#configure-the-alert-rule-conditions). Then select **Next: Actions**.

   :::image type="content" source="media/how-to-monitor-online-endpoints/configure-alert-rule.png" alt-text="Screenshot of the Create an alert rule page in the Azure portal. The Threshold box and Next Actions are highlighted."  lightbox="media/how-to-monitor-online-endpoints/configure-alert-rule.png" :::

1. In the **Select action groups** window, create or select an action group to specify what happens when your alert is triggered. For more information, see [Configure the alert rule details](/azure/azure-monitor/alerts/alerts-create-metric-alert-rule#configure-the-alert-rule-details).

1. Select **Review + Create** to finish creating your alert.

### Scale automatically based on metrics

You can configure deployments to scale automatically based on metrics. To turn on the autoscale feature, use the UI or code.

The options for code are the Azure Machine Learning CLI and the Azure Machine Learning SDK for Python. When you use code, you configure the conditions for triggering automatic scaling by providing the REST API name of metrics.

- For the names of endpoint metrics to use in code, see the values in the **Name in REST API** column in the table in [Supported metrics for Microsoft.MachineLearningServices/workspaces/onlineEndpoints](monitor-azure-machine-learning-reference.md#supported-metrics-for-microsoftmachinelearningservicesworkspacesonlineendpoints).
- For the names of deployment metrics to use in code, see the values in the **Name in REST API** column in the tables in [Supported metrics for Microsoft.MachineLearningServices/workspaces/onlineEndpoints/deployments](monitor-azure-machine-learning-reference.md#supported-metrics-for-microsoftmachinelearningservicesworkspacesonlineendpointsdeployments).

For more information, see [Autoscale online endpoints in Azure Machine Learning](how-to-autoscale-endpoints.md).

## Use logs

Turn on three logs for online endpoints:

* **AmlOnlineEndpointTrafficLog**: This traffic log provides a way for you to check the information of requests to the endpoint. This log is useful in the following cases:
  * A request response isn't 200, and you want more information. The `ResponseCodeReason` column in the log lists the reason. For descriptions of status codes and reasons, see [HTTPS status codes](how-to-troubleshoot-online-endpoints.md#http-status-codes) in the article about troubleshooting online endpoints.
  * You want to look up the response code and response reason of your model for a request. The `ModelStatusCode` and `ModelStatusReason` columns provide this information.
  * You want to know the duration of a request. The logs provide a breakdown of the latency. That breakdown shows the total duration, the request duration, the response duration, and the delay that's caused by network throttling.
  * You want to check the number of recent requests that succeed and fail. The logs provide this information.
* **AmlOnlineEndpointConsoleLog**: This log contains statements that the containers write as output to the console. This log is useful in the following cases:
  * A container fails to start. The console log can be useful for debugging.
  * You want to monitor container behavior and make sure that all requests are correctly handled.
  * You want to trace a request from the network entry point of an online endpoint to the container. You can use a Log Analytics query that joins the request ID with information from the AmlOnlineEndpointConsoleLog and AmlOnlineEndpointTrafficLog logs.
  * You want to run a performance analysis, for instance, to determine the time the model takes to process each request.
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

### Turn on logs

> [!IMPORTANT]
> Logging uses the Log Analytics feature of Monitor. If you don't currently have a Log Analytics workspace, you can create one by following the steps in [Create a workspace](/azure/azure-monitor/logs/quick-create-workspace#create-a-workspace).

1. In the [Azure portal](https://portal.azure.com), go to the resource group that contains your endpoint, and then select the endpoint.

1. Under **Monitoring**, select **Diagnostic settings**, and then select **Add diagnostic setting**.

1. In the Diagnostic setting window, enter the following information:
   - Next to **Diagnostic setting name**, enter a name for your setting.
   - Under **Logs**, select the log categories that you want to turn on.
   - Under **Destination details**, select **Send to Log Analytics workspace**, and then select the subscription and the Log Analytics workspace to use.

   :::image type="content" source="media/how-to-monitor-online-endpoints/diagnostic-settings.png" alt-text="Screenshot of the Diagnostic setting window. All logs and Send to Log Analytics workspace are selected. A subscription and workspace are visible." lightbox="media/how-to-monitor-online-endpoints/diagnostic-settings.png":::

1. Select **Save**.

   > [!IMPORTANT]
   > It can take up to an hour for the connection to the Log Analytics workspace to be available. Wait an hour before continuing with the steps in the next section.

### Query logs

1. Submit scoring requests to the endpoint to create entries in the logs.

1. Go to the Azure portal. To open the logs, use one of the following options:
   - Go to the properties page for your online endpoint. Under **Monitoring**, select **Logs**.
   - Go to your Log Analytics workspace. On the left, select **Logs**.

1. Close the **Queries hub** window that opens by default.

1. Under **Other**, double-click **AmlOnlineEndpointConsoleLog**. If you don't see **AmlOnlineEndpointConsoleLog**, enter that value into the search field.

   :::image type="content" source="media/how-to-monitor-online-endpoints/online-endpoints-log-queries.png" alt-text="Screenshot of the Azure portal Logs page for an endpoint. AmlOnlineEndpointConsoleLog is highlighted in the search box and the results." lightbox="media/how-to-monitor-online-endpoints/online-endpoints-log-queries.png":::

1. Select **Run**.

   :::image type="content" source="media/how-to-monitor-online-endpoints/query-results.png" alt-text="Screenshot of the Azure portal Logs page for an endpoint. Run is highlighted, and AmlOnlineEndpointConsoleLog query results are visible." lightbox="media/how-to-monitor-online-endpoints/query-results.png":::

### Example queries

You can use the following example queries. To view the queries, take the following steps:

1. On the **Logs** page, select **Queries**.

1. In the search box, enter **Online endpoint**.

   :::image type="content" source="media/how-to-monitor-online-endpoints/example-queries.png" alt-text="Screenshot of the Queries tab of the Azure portal Logs page. Two example queries are visible, and the Queries tab and the search box are highlighted." lightbox="media/how-to-monitor-online-endpoints/example-queries.png":::

### Log column details

The following tables provide detailed information about the data that's stored in each log:

#### AmlOnlineEndpointTrafficLog

[!INCLUDE [endpoint-monitor-traffic-reference](includes/endpoint-monitor-traffic-reference.md)]

#### AmlOnlineEndpointConsoleLog

[!INCLUDE [endpoint-monitor-console-reference](includes/endpoint-monitor-console-reference.md)]

#### AmlOnlineEndpointEventLog

[!INCLUDE [endpoint-monitor-event-reference](includes/endpoint-monitor-event-reference.md)]

## Use Application Insights

Curated environments include integration with Application Insights. Through this integration, built-in metrics and logs are sent to Application Insights. As a result, you can use Application Insights built-in features for further analysis. Examples of those features include live metrics, the transaction search, the failures view, and the performance view.

For more information, see [Application Insights overview](/azure/azure-monitor/app/app-insights-overview).

You can turn on integration with Application Insights when you create an online deployment in the studio. On the Deployment page, under **Application Insights diagnostics**, select **Enabled**.

:::image type="content" source="media/how-to-monitor-online-endpoints/turn-on-application-insights-diagnostics.png" lightbox="media/how-to-monitor-online-endpoints/turn-on-application-insights-diagnostics.png" alt-text="Screenshot of the studio Deployment page when a user creates an online endpoint. The Application Insights diagnostics setting is highlighted.":::

When you turn on Application Insights, you can see high-level activity monitor graphs for a managed online endpoint. In the studio, go to the endpoint's page, and then select the **Monitoring** tab. 

:::image type="content" source="media/how-to-monitor-online-endpoints/monitor-endpoint.png" lightbox="media/how-to-monitor-online-endpoints/monitor-endpoint.png" alt-text="Screenshot of the Monitoring tab on a studio endpoint page. The Monitoring tab is highlighted. A chart shows requests per minute to the endpoint.":::

## Related content

* [View costs for an Azure Machine Learning managed online endpoint](how-to-view-online-endpoints-costs.md)
* [Analyze metrics with Azure Monitor metrics explorer](/azure/azure-monitor/essentials/analyze-metrics)
