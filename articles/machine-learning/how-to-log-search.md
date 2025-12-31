---
title: Send Distributed Training Logs to Azure Application Insights
description: Learn how to centralize distributed training logs in Azure Application Insights for faster debugging and error detection in Azure Machine Learning SDK v2.
#customer intent: As a data scientist, I want to centralize distributed training logs in Azure Application Insights so that I can quickly diagnose errors across multiple nodes.
author: s-polly
ms.author: scottpolly
ms.reviewer: sooryar
ms.date: 11/5/2025
ms.topic: how-to
ms.service: azure-machine-learning
ms.subservice: training
ms.collection: ce-skilling-ai-copilot
ms.custom: dev-focus
ai-usage: ai-assisted

---

# Send distributed training logs to Azure Application Insights

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

Azure Machine Learning simplifies debugging and observability in distributed training scenarios. Training jobs generate multiple log files - often one per worker - which makes error diagnosis cumbersome. For example, a 10-node cluster with eight GPUs per node can produce 80 separate log files. You can now send these logs to a central **Azure Application Insights AppTraces** table enabling fast query-based error and exception detection.

**Key benefits:**

- **Centralized log access**: Aggregates stdout and stderr from all workers into Application Insights.

- **Searchable logs**: Use Kusto queries to filter errors, warnings, or custom patterns.

- **Improved debuggability**: Reduces time spent manually inspecting multiple files.

- **Configurable retention and billing**: Logs are retained for **90 days** by default in an AppTraces Table with table type as Analytics; ingestion is billed by size of logs, retention beyond 90 days can be configured at additional cost. For more information, see [Manage data retention](/azure/azure-monitor/logs/data-retention-configure).

[!INCLUDE [machine-learning-preview-generic-disclaimer](includes/machine-learning-preview-generic-disclaimer.md)]

## Prerequisites

- An Azure subscription. If you don't have an Azure subscription, create a free account before you begin. Try the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

- An Azure Machine Learning workspace. For steps to create a workspace, see [Create workspace resources](quickstart-create-resources.md).

- Application Insights resource is configured to support [local authentication](/azure/azure-monitor/app/azure-ad-authentication?tabs=aspnetcore) for writing traces (Microsoft Entra ID based authentication isn't supported yet).

- Compute cluster running the job has network access to the linked Application Insights workspace.

- Your Azure Machine Learning workspace must not be a [Hub workspace](/azure/machine-learning/concept-hub-workspace).

- You must have the `Log Analytics Reader` role assigned in the Log Analytics workspace in order to query and search logs. For more information, see [Manage access to Log Analytics workspaces](/azure/azure-monitor/logs/manage-access?tabs=portal).

## Enable log forwarding to Application Insights

Set the `AZUREML_COMMON_RUNTIME_USE_APPINSIGHTS_CAPABILITY` environment variable in your training job configuration.

# [Studio](#tab/studio)

In Azure Machine Learning studio, add the environment variable when you configure your job:

1. Go to your job configuration.
1. In the **Environment variables** section, add the following values:
   - **Name**: `AZUREML_COMMON_RUNTIME_USE_APPINSIGHTS_CAPABILITY`
   - **Value**: `true`

:::image type="content" source="media/how-to-log-search/portal-configuration.png" alt-text="Screenshot of portal environment variable configuration." lightbox="media/how-to-log-search/portal-configuration.png":::

# [Python SDK](#tab/python)

Set the environment variable when you configure your training job:

```python
from azure.ai.ml import command, MLClient
from azure.identity import DefaultAzureCredential

# Connect to workspace
ml_client = MLClient.from_config(credential=DefaultAzureCredential())

# Configure job with Application Insights logging
job = command(
    code="./src",
    command="python healthcare-new-drugs.py",
    environment="azureml://registries/azureml/environments/mldesigner/versions/19",
    compute="gpu-compute",
    instance_count=1,
    experiment_name="healthcare-new-drugs",
    display_name="bisoprolol-c4ab99f",
    environment_variables={
        "AZUREML_COMMON_RUNTIME_USE_APPINSIGHTS_CAPABILITY": "true",
    }
)
train_job = ml_client.jobs.create_or_update(job)
```

**Reference**: 
- [command function](/python/api/azure-ai-ml/azure.ai.ml#azure-ai-ml-command)
- [MLClient.jobs.create_or_update](/python/api/azure-ai-ml/azure.ai.ml.operations.joboperations#azure-ai-ml-operations-joboperations-create-or-update)

# [Azure CLI](#tab/azurecli)

Create a job YAML file with the environment variable:

```yaml
$schema: https://azuremlschemas.azureedge.net/latest/commandJob.schema.json
code: ./src
command: python healthcare-new-drugs.py
environment: azureml://registries/azureml/environments/mldesigner/versions/19
compute: azureml:gpu-compute
experiment_name: healthcare-new-drugs
display_name: bisoprolol-c4ab99f
environment_variables:
  AZUREML_COMMON_RUNTIME_USE_APPINSIGHTS_CAPABILITY: 'true'
```

Submit the job using the Azure CLI:

```azurecli
az ml job create --file job.yml
```
---

## Query training job logs

After configuring log forwarding, you can query your training logs in Application Insights.

1. Go to the job overview page in Azure Machine Learning studio.
1. Select the **Job Logs** link.

   :::image type="content" source="media/how-to-log-search/job-overview.png" alt-text="Screenshot of job overview page with Job Logs link." lightbox="media/how-to-log-search/job-overview.png":::

1. You're taken to an Application Insights workspace with a default query filtered by the job ID.

   :::image type="content" source="media/how-to-log-search/app-insights.png" alt-text="Screenshot of application insights workspace with default query." lightbox="media/how-to-log-search/app-insights.png":::

1. Logs are written following the AppTraces [schema](/azure/azure-monitor/reference/tables/apptraces). Edit the query to search for errors, exceptions, or other points of interest across nodes.

   :::image type="content" source="media/how-to-log-search/query-editor.png" alt-text="Screenshot of query editor for searching logs." lightbox="media/how-to-log-search/query-editor.png":::

### Useful log fields

The most useful fields in the `AppTraces` table are:

- `timestamp` – Timestamp of the log message
- `message` – The log line from your training code
- `customDimensions` – JSON with useful fields like job ID, source file name, source node, and more

## Verify log ingestion

To verify that Application Insights receives your logs:

1. Submit a test training job with the environment variable configured.
1. Wait for the job to start running.
1. Go to the job overview page and select the **Job Logs** link.
1. Confirm that log traces appear in the Application Insights query results.

If you don't see logs, check the troubleshooting section.

## Troubleshooting

- If you look at the logs for an old job and you don't see any log messages, modify the default query. The default query only checks the last few days of logs in Application Insights.

- Verify that you set the environment variable in **Job Overview > Job Yaml**.

- Check Application Insights linkage in workspace settings by opening the workspace resource in the Azure portal and checking if the Application Insights link is populated.

- Ensure the compute cluster has network access to the default Application Insights workspace linked to the Azure Machine Learning workspace.

- Inspect **appinsights-capability.log** in system job logs for errors.

## Next steps

- [Monitor Azure Machine Learning](/azure/machine-learning/monitor-azure-machine-learning)
- [Query data in Azure Monitor Logs](/azure/azure-monitor/logs/log-query-overview)
- [Application Insights overview](/azure/azure-monitor/app/app-insights-overview)
