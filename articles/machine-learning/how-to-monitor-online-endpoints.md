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

- Deploy an Azure Machine Learning online endpoint.
- You must have at least [Reader access](/azure/role-based-access-control/role-assignments-portal) on the endpoint.

## Metrics

You can view metrics pages for online endpoints or deployments in the Azure portal. An easy way to access these metrics pages is through links available in the Azure Machine Learning studio user interface—specifically in the **Details** tab of an endpoint's page. Following these links will take you to the exact metrics page in the Azure portal for the endpoint or deployment. Alternatively, you can also go into the Azure portal to search for the metrics page for the endpoint or deployment.

To access the metrics pages through links available in the studio:

1. In [Azure Machine Learning studio](https://ml.azure.com), go to your workspace.

1. Under **Assets**, select **Endpoints**.

1. Select the name of an endpoint.

1. Under **Endpoint attributes**, select **View metrics**.

   :::image type="content" source="media/how-to-monitor-online-endpoints/online-endpoints-access-metrics-studio.png" alt-text="A screenshot showing how to access the metrics of an endpoint and deployment from the studio UI." lightbox="media/how-to-monitor-online-endpoints/online-endpoints-access-metrics-studio.png":::

   The endpoint's metrics page opens in the Azure portal.

1. In Azure Machine Learning studio, go to the section for a deployment, and then select **View metrics**.

   :::image type="content" source="media/how-to-monitor-online-endpoints/deployment-metrics-studio.png" alt-text="A screenshot showing how to access the metrics of an endpoint and deployment from the studio UI." lightbox="media/how-to-monitor-online-endpoints/deployment-metrics-studio.png":::

   The deployment's metrics page opens in the Azure portal.

To access metrics directly from the Azure portal:

1. Go to the [Azure portal](https://portal.azure.com).

1. Go to the online endpoint or deployment resource.

   Online endpoints and deployments are Azure Resource Manager resources. You can find them by going to their resource group and then looking for the resource types **Machine Learning online endpoint** and **Machine Learning online deployment**.

1. Under **Monitoring**, select **Metrics**.

   :::image type="content" source="media/how-to-monitor-online-endpoints/endpoint-metrics-azure-portal.png" alt-text="A screenshot showing how to access the metrics of an endpoint and deployment from the studio UI." lightbox="media/how-to-monitor-online-endpoints/endpoint-metrics-azure-portal.png":::

### Available metrics

Depending on the resource that you select, the metrics that you see will be different. Metrics are scoped differently for online endpoints and online deployments.

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

You can also create custom alerts to notify you of important status updates to your online endpoint:

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

* **AmlOnlineEndpointTrafficLog**: This traffic log provides a way for you to check the information of a request to the endpoint. You can use this log in the following cases: 

    * If the request response isn't 200, check the value of the `ResponseCodeReason` column to see the reason. Also check the reason in [HTTPS status codes](how-to-troubleshoot-online-endpoints.md#http-status-codes), in the article about troubleshooting online endpoints.

    * You could check the response code and response reason of your model from the column "ModelStatusCode" and "ModelStatusReason". 

    * You want to check the duration of the request like total duration, the request/response duration, and the delay caused by the network throttling. You could check it from the logs to see the breakdown latency. 

    * If you want to check how many requests or failed requests recently. You could also enable the logs. 

* **AmlOnlineEndpointConsoleLog**: Contains logs that the containers output to the console. Below are some cases: 

    * If the container fails to start, the console log can be useful for debugging. 

    * Monitor container behavior and make sure that all requests are correctly handled. 

    * Write request IDs in the console log. Joining the request ID, the AmlOnlineEndpointConsoleLog, and AmlOnlineEndpointTrafficLog in the Log Analytics workspace, you can trace a request from the network entry point of an online endpoint to the container.  

    * You can also use this log for performance analysis in determining the time required by the model to process each request. 

* **AmlOnlineEndpointEventLog**: Contains event information regarding the container's life cycle. Currently, we provide information on the following types of events: 

    | Name | Message |
    | ----- | ----- | 
    | BackOff | Back-off restarting failed container 
    | Pulled | Container image "\<IMAGE\_NAME\>" already present on machine 
    | Killing | Container inference-server failed liveness probe, will be restarted 
    | Created | Created container image-fetcher 
    | Created | Created container inference-server 
    | Created | Created container model-mount 
    | LivenessProbeFailed | Liveness probe failed: \<FAILURE\_CONTENT\> 
    | ReadinessProbeFailed | Readiness probe failed: \<FAILURE\_CONTENT\> 
    | Started | Started container image-fetcher 
    | Started | Started container inference-server 
    | Started | Started container model-mount 
    | Killing | Stopping container inference-server 
    | Killing | Stopping container model-mount 

### Turn logs on or off

> [!IMPORTANT]
> Logging uses Azure Log Analytics. If you do not currently have a Log Analytics workspace, you can create one using the steps in [Create a Log Analytics workspace in the Azure portal](/azure/azure-monitor/logs/quick-create-workspace#create-a-workspace).

1. In the [Azure portal](https://portal.azure.com), go to the resource group that contains your endpoint and then select the endpoint.

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

1. From either the online endpoint properties or the Log Analytics workspace, select **Logs** from the left of the screen.

1. Close the **Queries** dialog that automatically opens, and then double-click the **AmlOnlineEndpointConsoleLog**. If you don't see it, use the **Search** field.

    :::image type="content" source="./media/how-to-monitor-online-endpoints/online-endpoints-log-queries.png" alt-text="Screenshot showing the log queries.":::

1. Select **Run**.

    :::image type="content" source="./media/how-to-monitor-online-endpoints/query-results.png" alt-text="Screenshots of the results after running a query.":::

### Example queries

You can find example queries on the __Queries__ tab while viewing logs. Search for __Online endpoint__ to find example queries.

:::image type="content" source="./media/how-to-monitor-online-endpoints/example-queries.png" alt-text="Screenshot of the example queries.":::

### Log column details 

The following tables provide details on the data stored in each log:

**AmlOnlineEndpointTrafficLog**

[!INCLUDE [endpoint-monitor-traffic-reference](includes/endpoint-monitor-traffic-reference.md)]

**AmlOnlineEndpointConsoleLog**

[!INCLUDE [endpoint-monitor-console-reference](includes/endpoint-monitor-console-reference.md)]

**AmlOnlineEndpointEventLog**

[!INCLUDE [endpoint-monitor-event-reference](includes/endpoint-monitor-event-reference.md)]


## Using Application Insights

Curated environments include integration with Application Insights, and you can enable or disable this integration when you create an online deployment. Built-in metrics and logs are sent to Application Insights, and you can use the built-in features of Application Insights (such as Live metrics, Transaction search, Failures, and Performance) for further analysis.

See [Application Insights overview](/azure/azure-monitor/app/app-insights-overview) for more.

In the studio, you can use the **Monitoring** tab on an online endpoint's page to see high-level activity monitor graphs for the managed online endpoint. To use the monitoring tab, you must select **Enable Application Insight diagnostic and data collection** when you create your endpoint.

:::image type="content" source="media/how-to-monitor-online-endpoints/monitor-endpoint.png" lightbox="media/how-to-monitor-online-endpoints/monitor-endpoint.png" alt-text="A screenshot of monitoring endpoint-level metrics in the studio.":::


## Related content

* Learn how to [view costs for your deployed endpoint](./how-to-view-online-endpoints-costs.md).
* Read more about [metrics explorer](/azure/azure-monitor/essentials/metrics-charts).
