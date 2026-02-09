---
title: Autoscale online endpoints
titleSuffix: Azure Machine Learning
description: Learn how to scale Azure Machine Learning online endpoints based on metrics and schedules.
ms.service: azure-machine-learning
ms.subservice: inferencing
ms.topic: how-to
author: s-polly
ms.author: scottpolly
ms.reviewer: jturuk
ms.custom: devplatv2, cliv2, update-code
ms.date: 02/09/2026

#customer intent: As a developer, I want to autoscale online endpoints in Azure Machine Learning so I can control resource usage in my deployment based on metrics or schedules.
---

# Autoscale online endpoints in Azure Machine Learning

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

In this article, you learn to manage resource usage in a deployment by configuring autoscaling based on metrics and schedules. The autoscale process lets you automatically run the right amount of resources to handle the load on your application.

[Online endpoints](concept-endpoints.md) in Azure Machine Learning support autoscaling through integration with the autoscale feature in Azure Monitor. For more information on autoscale settings from Azure Monitor, see [Microsoft.Insights autoscalesettings](/azure/templates/microsoft.insights/autoscalesettings).

Azure Monitor autoscale allows you to set rules that trigger one or more autoscale actions when conditions of the rules are met. You can base scaling on metrics such as CPU utilization, schedule such as peak business hours, or a combination of the two. For more information, see [Overview of autoscale in Microsoft Azure](/azure/azure-monitor/autoscale/autoscale-overview).

:::image type="content" source="media/how-to-autoscale-endpoints/concept-autoscale.png" border="false" alt-text="Diagram that shows how autoscale adds and removes instances as needed.":::

You can manage autoscaling by using REST APIs, Azure Resource Manager, Azure Machine Learning CLI v2, Azure Machine Learning Python SDK v2, or Machine Learning studio and the Azure portal.

## Prerequisites

- An Azure Machine Learning workspace with a deployed endpoint. For more information, see [Deploy and score a machine learning model by using an online endpoint](how-to-deploy-online-endpoints.md). 
- To use the Azure Monitor service, the Python SDK `azure-mgmt-monitor` package installed by using `pip install azure-mgmt-monitor`.
- The `microsoft.insights/autoscalesettings/write` permission assigned to the identity that manages autoscale, through any built-in or custom role that allow this action. For more information, see [Manage users and roles](how-to-assign-roles.md).

## Define an autoscale profile

To enable autoscale for an online endpoint, you first define an autoscale profile. The profile specifies the default, minimum, and maximum scale set capacity. The following example shows how to set the number of virtual machine (VM) instances for the default, minimum, and maximum scale capacity.

# [Azure CLI](#tab/cli)

If you haven't already set the defaults for Azure CLI, run the following code to avoid repeatedly specifying values for your subscription, workspace, and resource group.

```azurecli
az account set --subscription <subscription ID>
az configure --defaults workspace=<Azure Machine Learning workspace name> group=<resource group>
```

To define an autoscale profile:

1. Set the endpoint and deployment names:

   :::code language="azurecli" source="~/azureml-examples-main/cli/deploy-moe-autoscale.sh" ID="set_endpoint_deployment_name" :::

1. Get the Azure Resource Manager ID of the deployment and endpoint:

   :::code language="azurecli" source="~/azureml-examples-main/cli/deploy-moe-autoscale.sh" ID="set_other_env_variables" :::

1. Create the autoscale profile:

   :::code language="azurecli" source="~/azureml-examples-main/cli/deploy-moe-autoscale.sh" ID="create_autoscale_profile" :::

For more information, see the [az monitor autoscale](/cli/azure/monitor/autoscale) reference.

# [Python SDK](#tab/python)

To define an autoscale profile:

1. Import the necessary modules:

   ```python
   from azure.ai.ml import MLClient
   from azure.identity import DefaultAzureCredential
   from azure.mgmt.monitor import MonitorManagementClient
   from azure.mgmt.monitor.models import AutoscaleProfile, ScaleRule, MetricTrigger, ScaleAction, Recurrence, RecurrentSchedule
   import random 
   import datetime 
   ``` 

1. Define variables for the workspace, endpoint, and deployment:

   ```python
   subscription_id = "<YOUR-SUBSCRIPTION-ID>"
   resource_group = "<YOUR-RESOURCE-GROUP>"
   workspace = "<YOUR-WORKSPACE>"

   endpoint_name = "<YOUR-ENDPOINT-NAME>"
   deployment_name = "blue"
   ``` 

1. Get Azure Machine Learning and Azure Monitor clients:

   ```python
   credential = DefaultAzureCredential()
   ml_client = MLClient(
       credential, subscription_id, resource_group, workspace
   )

   mon_client = MonitorManagementClient(
       credential, subscription_id
   )
   ```

1. Get the endpoint and deployment objects: 

   ```python 
   deployment = ml_client.online_deployments.get(
       deployment_name, endpoint_name
   )

   endpoint = ml_client.online_endpoints.get(
       endpoint_name
   )
   ```

1. Create an autoscale profile: 

   ```python
   # Set a unique name for autoscale settings for this deployment. The following code appends a random number to create a unique name.
   autoscale_settings_name = f"autoscale-{endpoint_name}-{deployment_name}-{random.randint(0,1000)}"

   mon_client.autoscale_settings.create_or_update(
       resource_group, 
       autoscale_settings_name, 
       parameters = {
           "location" : endpoint.location,
           "target_resource_uri" : deployment.id,
           "profiles" : [
               AutoscaleProfile(
                   name="my-scale-settings",
                   capacity={
                       "minimum" : 2, 
                       "maximum" : 5,
                       "default" : 2
                   },
                   rules = []
               )
           ]
       }
   )
   ```

# [Studio](#tab/azure-studio)

1. In your workspace in [Azure Machine Learning studio](https://ml.azure.com), select **Endpoints** from the left menu.

1. Select the endpoint to configure from the list of available endpoints.

   :::image type="content" source="media/how-to-autoscale-endpoints/select-endpoint.png" alt-text="Screenshot that shows how to select an endpoint deployment entry for a Machine Learning workspace in the studio." lightbox="media/how-to-autoscale-endpoints/select-endpoint.png":::

1. On the **Details** tab for the selected endpoint, scroll down and select the **Configure auto scaling** link under **Scaling**.

   :::image type="content" source="media/how-to-autoscale-endpoints/configure-auto-scaling.png" alt-text="Screenshot that shows how to select the option to configure autoscaling for an endpoint." lightbox="media/how-to-autoscale-endpoints/configure-auto-scaling.png":::

1. On the Azure portal **Scaling** page for the deployment, select **Custom autoscale** under **Choose how to scale your resources**.

   :::image type="content" source="media/how-to-autoscale-endpoints/choose-custom-autoscale.png" alt-text="Screenshot that shows how to configure the autoscale settings in the studio." lightbox="media/how-to-autoscale-endpoints/choose-custom-autoscale.png":::

1. In the **Default** pane, select **Scale based on a metric**.

1. Under **Instance limits**, set **Minimum** to *2*, **Maximum** to *5*, and **Default** to *2*.

1. Under **Rules**, select the **Add a rule** link.

---

## Create a scale-out rule based on deployment metrics

A common scale-out rule increases the number of VM instances when the average CPU load is high. The following example shows how to allocate two more nodes, up to the maximum, if the CPU average load is greater than 70% for five minutes.

# [Azure CLI](#tab/cli)

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-moe-autoscale.sh" ID="scale_out_on_cpu_util" :::

The rule is part of the `my-scale-settings` profile, where `autoscale-name` matches the `name` portion of the profile. The value of the `condition` argument indicates that the rule triggers when the average CPU consumption among the VM instances exceeds 70% for five minutes. Autoscaling allocates two more VM instances when the condition is satisfied.

For more information, see the [az monitor autoscale](/cli/azure/monitor/autoscale) Azure CLI syntax reference.

# [Python SDK](#tab/python)

1. Create the rule definition:

   ```python
   rule_scale_out = ScaleRule(
       metric_trigger = MetricTrigger(
           metric_name="CpuUtilizationPercentage",
           metric_resource_uri = deployment.id, 
           time_grain = datetime.timedelta(minutes = 1),
           statistic = "Average",
           operator = "GreaterThan", 
           time_aggregation = "Last",
           time_window = datetime.timedelta(minutes = 5), 
           threshold = 70
       ), 
       scale_action = ScaleAction(
           direction = "Increase", 
           type = "ChangeCount", 
           value = 2, 
           cooldown = datetime.timedelta(hours = 1)
       )
   )
   ```

   This rule refers to the last 5-minute average of the `CPUUtilizationpercentage` value from the arguments `metric_name`, `time_window`, and `time_aggregation`. When the value of the metric is greater than the `threshold` of 70, the deployment allocates two more VM instances. 

1. Update the `my-scale-settings` profile to include this rule.

   ```python 
   mon_client.autoscale_settings.create_or_update(
       resource_group, 
       autoscale_settings_name, 
       parameters = {
           "location" : endpoint.location,
           "target_resource_uri" : deployment.id,
           "profiles" : [
               AutoscaleProfile(
                   name="my-scale-settings",
                   capacity={
                       "minimum" : 2, 
                       "maximum" : 5,
                       "default" : 2
                   },
                   rules = [
                       rule_scale_out
                   ]
               )
           ]
       }
   )
   ```

# [Studio](#tab/azure-studio)

1. On the **Scale rule** page, configure the following values:

   - **Metric name**: Select **CPU Utilization Percentage**.
   - **Operator**: Select **Greater than**.
   - **Metric threshold**: Set to *70*.
   - **Duration (minutes)**: Set to *5*.
   - **Time grain statistic**: Select **Average**.
   - **Operation**: Select **Increase count by**.
   - **Instance count**: Set to *2*.

1. Select **Add**.

   :::image type="content" source="media/how-to-autoscale-endpoints/scale-out-rule.png" alt-text="Screenshot that shows how to configure the scale-out rule for greater than 70% CPU for 5 minutes.":::

1. On the **Scaling** page, select **Save**.

---

## Create a scale-in rule based on deployment metrics

A scale-in rule can reduce the number of VM instances when the average CPU load is light. The following example shows how to release a single node, down to a minimum of two, if the CPU load is less than 30% for five minutes.

# [Azure CLI](#tab/cli)

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-moe-autoscale.sh" ID="scale_in_on_cpu_util" :::

# [Python SDK](#tab/python)

1. Create the rule definition.

   ```python 
   rule_scale_in = ScaleRule(
       metric_trigger = MetricTrigger(
           metric_name="CpuUtilizationPercentage",
           metric_resource_uri = deployment.id, 
           time_grain = datetime.timedelta(minutes = 1),
           statistic = "Average",
           operator = "LessThan", 
           time_aggregation = "Last",
           time_window = datetime.timedelta(minutes = 5), 
           threshold = 30
       ), 
       scale_action = ScaleAction(
           direction = "Increase", 
           type = "ChangeCount", 
           value = 1, 
           cooldown = datetime.timedelta(hours = 1)
       )
   )
   ``` 

1. Update the `my-scale-settings` profile to include this rule.

   ```python 
   mon_client.autoscale_settings.create_or_update(
       resource_group, 
       autoscale_settings_name, 
       parameters = {
           "location" : endpoint.location,
           "target_resource_uri" : deployment.id,
           "profiles" : [
               AutoscaleProfile(
                   name="my-scale-settings",
                   capacity={
                       "minimum" : 2, 
                       "maximum" : 5,
                       "default" : 2
                   },
                   rules = [
                       rule_scale_out, 
                       rule_scale_in
                   ]
               )
           ]
       }
   )
   ```
 
# [Studio](#tab/azure-studio)

The following steps adjust the **Rules** configuration to support a scale in rule.

1. On the Azure portal **Scaling** page with **Custom autoscale** selected, select **Scale based on a metric**, and then select the **Add a rule** link.

1. On the **Scale rule** page, configure the following values:

   - **Metric name**: Select **CPU Utilization Percentage**.
   - **Operator**: Set to **Less than**.
   - **Metric threshold**: Set to *30*.
   - **Duration (minutes)**: Set to *5*.
   - **Time grain statistic**: Select **Average**.
   - **Operation**: Select **Decrease count by**.
   - **Instance count**: Set to *1*.

1. Select **Add**.

   :::image type="content" source="media/how-to-autoscale-endpoints/scale-in-rule.png" alt-text="Screenshot that shows how to configure the scale in rule for less than 30% CPU for 5 minutes.":::

1. On the **Scaling** page, select **Save**.

If you configure both scale-out and scale-in rules, the **Rules** section of the **Scaling** page looks similar to the following screenshot. The rules specify that if average CPU load exceeds 70% for 5 minutes, two more nodes should be allocated, up to the limit of five. If CPU load is less than 30% for 5 minutes, a single node should be released, down to the minimum of two. 

:::image type="content" source="media/how-to-autoscale-endpoints/autoscale-rules-final.png" lightbox="media/how-to-autoscale-endpoints/autoscale-rules-final.png" alt-text="Screenshot that shows the autoscale settings including the scale in and scale-out rules.":::

---

## Create a scale rule based on endpoint metrics

In the preceding sections, you created rules to scale in or out based on deployment metrics. You can also create a rule that applies to the deployment endpoint. In this section, you learn how to allocate another node when the request latency is greater than an average of 70 milliseconds for five minutes.

# [Azure CLI](#tab/cli)

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-moe-autoscale.sh" ID="scale_up_on_request_latency" :::

# [Python SDK](#tab/python)

1. Create the rule definition: 

   ```python
   rule_scale_out_endpoint = ScaleRule(
       metric_trigger = MetricTrigger(
           metric_name="RequestLatency",
           metric_resource_uri = endpoint.id, 
           time_grain = datetime.timedelta(minutes = 1),
           statistic = "Average",
           operator = "GreaterThan", 
           time_aggregation = "Last",
           time_window = datetime.timedelta(minutes = 5), 
           threshold = 70
       ), 
       scale_action = ScaleAction(
           direction = "Increase", 
           type = "ChangeCount", 
           value = 1, 
           cooldown = datetime.timedelta(hours = 1)
       )
   )
   ```

   This rule's `metric_resource_uri` field now refers to the endpoint rather than the deployment.

1. Update the `my-scale-settings` profile to include this rule.

   ```python 
   mon_client.autoscale_settings.create_or_update(
       resource_group, 
       autoscale_settings_name, 
       parameters = {
           "location" : endpoint.location,
           "target_resource_uri" : deployment.id,
           "profiles" : [
               AutoscaleProfile(
                   name="my-scale-settings",
                   capacity={
                       "minimum" : 2, 
                       "maximum" : 5,
                       "default" : 2
                   },
                   rules = [
                       rule_scale_out, 
                       rule_scale_in,
                       rule_scale_out_endpoint
                   ]
               )
           ]
       }
   )
   ```

# [Studio](#tab/azure-studio)

1. At the bottom of the Azure portal **Scaling** page with **Custom autoscale** selected, select the **Add a scale condition* link.

1. In the **Profile** section, select **Scale based on a metric** and then select the **Add a rule** link.

1. On the **Scale rule** page, configure the following values:

   - **Metric source**: Select **Other resource**.
   - **Resource type**: Select **Machine Learning online endpoints**.
   - **Resource**: Select your endpoint.
   - **Metric name**: Select **Request latency**.
   - **Operator**: Set to **Greater than**.
   - **Metric threshold**: Set to 70.
   - **Duration (minutes)**: Set to 5.
   - **Time grain statistic**: Select **Average**.
   - **Operation**: Select **Increase count by**.
   - **Instance count**: Set to 1.

1. Select **Add**.

   :::image type="content" source="media/how-to-autoscale-endpoints/endpoint-rule.png" lightbox="media/how-to-autoscale-endpoints/endpoint-rule.png" alt-text="Screenshot that shows how to configure a scale rule by using endpoint metrics.":::

1. On the **Scaling** page, select **Save**.

---

## Find other supported metrics

You can use other metrics when you set up autoscale rules.

- For the names of endpoint metrics to use in code, see the values in the **Name in REST API** column in the table in [Supported metrics for Microsoft.MachineLearningServices/workspaces/onlineEndpoints](monitor-azure-machine-learning-reference.md#supported-metrics-for-microsoftmachinelearningservicesworkspacesonlineendpoints).

- For the names of deployment metrics to use in code, see the values in the **Name in REST API** column in the tables in [Supported metrics for Microsoft.MachineLearningServices/workspaces/onlineEndpoints/deployments](monitor-azure-machine-learning-reference.md#supported-metrics-for-microsoftmachinelearningservicesworkspacesonlineendpointsdeployments).

- To select other metrics on the Azure portal **Scale rule** page, select the metric source under **Metric source**, and then select from the available metrics under **Metric name**.

## Create a scale rule based on schedule

You can also create rules that apply only on certain days or at certain times. In this section, you create a rule that sets the node count to two on weekends.

# [Azure CLI](#tab/cli)

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-moe-autoscale.sh" ID="weekend_profile" :::

# [Python SDK](#tab/python)

```python 
mon_client.autoscale_settings.create_or_update(
    resource_group, 
    autoscale_settings_name, 
    parameters = {
        "location" : endpoint.location,
        "target_resource_uri" : deployment.id,
        "profiles" : [
            AutoscaleProfile(
                name="Default",
                capacity={
                    "minimum" : 2, 
                    "maximum" : 2,
                    "default" : 2
                },
                rules=[],
                recurrence = Recurrence(
                    frequency = "Week", 
                    schedule = RecurrentSchedule(
                        time_zone = "Pacific Standard Time", 
                        days = ["Saturday", "Sunday"], 
                        hours = ["0"], 
                        minutes = ["0"]
                    )
                )
            )
        ]
    }
)
``` 

# [Studio](#tab/azure-studio)

1. At the bottom of the Azure portal **Scaling** page with **Custom autoscale** selected, select **Add a scale condition**.

1. In the **Profile** section, select **Scale to a specific instance count**.

1. Set **Instance count** to *2*.

1. For **Schedule**, select **Repeat specific days**.

1. For **Repeat every**, select **Saturday** and **Sunday**.

1. Select **Add**.

   :::image type="content" source="media/how-to-autoscale-endpoints/schedule-rules.png" lightbox="media/how-to-autoscale-endpoints/schedule-rules.png" alt-text="Screenshot that shows how to create a rule based on a schedule.":::

1. Select **Save** at the top of the page.

---

## Enable or disable autoscale

You can enable or disable a specific autoscale profile.

# [Azure CLI](#tab/cli)

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-moe-autoscale.sh" ID="disable_profile" :::

# [Python SDK](#tab/python)

```python
mon_client.autoscale_settings.create_or_update(
    resource_group, 
    autoscale_settings_name, 
    parameters = {
        "location" : endpoint.location,
        "target_resource_uri" : deployment.id,
        "enabled" : False
    }
)
```

# [Studio](#tab/azure-studio)

On the Azure portal **Scaling** page:

- To disable autoscale profiles in use, select **Manual scale**, and then select **Save**.
- To reenable the autoscale profiles, select **Custom autoscale**, and then select **Save**

---

## Delete resources

If you're not going to use your deployments, you can delete the resources.

# [Azure CLI](#tab/cli)

Run the following code:

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-moe-autoscale.sh" ID="delete_endpoint" :::

# [Python SDK](#tab/python)

Run the following code:

```python
mon_client.autoscale_settings.delete(
    resource_group, 
    autoscale_settings_name
)

ml_client.online_endpoints.begin_delete(endpoint_name)
```

# [Studio](#tab/azure-studio)

1. In your workspace in [Azure Machine Learning studio](https://ml.azure.com), select **Endpoints** from the left menu.
1. Select the endpoint to delete by selecting the circle next to the endpoint name.
1. Select **Delete**.

You can also delete a managed online endpoint from the [endpoint details page](how-to-use-managed-online-endpoint-studio.md#view-managed-online-endpoints). 

---

## Related content

- [Understand autoscale settings](/azure/azure-monitor/autoscale/autoscale-understanding-settings)
- [Review common autoscale patterns](/azure/azure-monitor/autoscale/autoscale-common-scale-patterns)
- [Explore best practices for autoscale](/azure/azure-monitor/autoscale/autoscale-best-practices)
