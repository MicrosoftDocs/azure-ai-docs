---
title: Schedule pipeline jobs
titleSuffix: Azure Machine Learning
description: Learn how to schedule pipeline jobs that allow you to automate routine, time-consuming tasks such as data processing, training, and monitoring.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mlops
ms.author: scottpolly
author: lgayhardt
ms.reviewer: jturuk
ms.date: 09/11/2025
ms.topic: how-to
---

# Schedule machine learning pipeline jobs

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

In this article, you learn how to schedule machine learning pipelines to run on Azure. You can schedule routine tasks like retraining models or regularly updating batch predictions based on elapsed time.

This article shows you how to create, retrieve, update, and deactivate schedules by using the Azure Machine Learning CLI, Azure Machine Learning SDK v2 for Python, or Azure Machine Learning studio UI.

> [!TIP]
> To schedule jobs by using an external orchestrator, like Azure Data Factory or Microsoft Fabric, consider deploying your pipeline jobs under a batch endpoint. For more information, see [Deploy existing pipeline jobs to batch endpoints](how-to-use-batch-pipeline-from-job.md) and [Run Azure Machine Learning models from Fabric by using batch endpoints (preview)](how-to-use-batch-fabric.md).

## Prerequisites

- An Azure subscription. If you don't have one, [create a free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin. 
- An Azure Machine Learning workspace. To create a workspace, see [Create workspace resources](quickstart-create-resources.md).
- An understanding of Azure Machine Learning pipelines. For information, see [What are machine learning pipelines](concept-ml-pipelines.md).

# [Azure CLI](#tab/cliv2)

- The Azure CLI and `ml` extension installed by following the instructions in [Install, set up, and use the CLI (v2)](how-to-configure-cli.md).
- Knowledge of how to create Azure Machine Learning YAML pipelines. For information, see [Create and run machine learning pipelines using components with the Azure Machine Learning CLI](how-to-create-component-pipelines-cli.md).

# [Python SDK](#tab/python)

- The [Azure Machine Learning SDK v2 for Python](/python/api/overview/azure/ai-ml-readme) installed.
- Knowledge of how to create Python pipelines for Azure Machine Learning. For information, see [Create and run machine learning pipelines using components with the Azure Machine Learning SDK](how-to-create-component-pipeline-python.md).

# [Studio UI](#tab/ui)

- Knowledge of how to create pipelines in Azure Machine Learning studio. For information, see [Create and run machine learning pipelines using components with the Azure Machine Learning studio](how-to-create-component-pipelines-ui.md).

---

## Limitations

- Azure Machine Learning v2 schedules don't support event-based triggers.
- CLI and SDK v2 schedules support specifying complex recurrence patterns that contain multiple trigger timestamps. The studio UI displays the complex patterns but doesn't support editing them.
- The studio UI supports only v2 schedules, and can't list or access v1 schedules that are based on published pipelines or pipeline endpoints. You can create a schedule for an unpublished pipeline.
- If recurrence is set as the 31st or 30th day of every month, the schedule doesn't trigger jobs in months that have fewer days.
- `DAYS` and `MONTHS` values aren't supported in cron schedule expressions. Values passed for these parameters are ignored and treated as `*`.
- Even after assigning a managed identity to a schedule, the author must retain their job run permissions for the schedule to function.

## Create a schedule

When you have a pipeline job with satisfying performance and outputs, you can set up a schedule to automatically trigger the job regularly. To do so, you must create a schedule that associates the job with a trigger. The trigger can be either a `recurrence` pattern or a `cron` expression that specifies the interval and frequency to run the job.

In both cases, you need to define a pipeline job first, either inline or by specifying an existing pipeline job. You can define pipelines in YAML and run them from the CLI, author pipelines inline in Python, or compose pipelines in Azure Machine Learning studio. You can create pipeline jobs locally or from existing jobs in the workspace.

You can create v2 schedules for v2 or v1 pipeline jobs by using the studio UI, SDK v2, or CLI v2. You don't have to publish existing pipelines first to set up schedules for pipeline jobs.

# [Azure CLI](#tab/cliv2)

The code examples in this article are from [Working with Schedule in Azure Machine Learning CLI 2.0](https://github.com/Azure/azureml-examples/tree/main/cli/schedules).

# [Python SDK](#tab/python)

The code examples in this article are excerpts from the [Working with Schedule](https://github.com/Azure/azureml-examples/blob/main/sdk/python/schedules/job-schedule.ipynb) Azure Machine Learning notebook. Run the notebook to create and manage the schedules as described.

# [Studio UI](#tab/ui)

To create a schedule for an Azure Machine Learning pipeline job in the studio UI, open the pipeline job detail page.

---

### Define a time-based schedule with a recurrence pattern

# [Azure CLI](#tab/cliv2)

The following YAML code defines a recurring schedule for a pipeline job. The required `type` parameter specifies that the `trigger` type is `recurrence`.

:::code language="yaml"source="~/azureml-examples-main/cli/schedules/recurrence-job-schedule.yml":::

You must or can provide the following schedule parameters:

# [Python SDK](#tab/python)

The following code uses `RecurrenceTrigger` to provide a better coding experience.

[!Notebook-python[] (~/azureml-examples-main/sdk/python/schedules/job-schedule.ipynb?name=create_schedule_recurrence)]

You must or can provide the following schedule parameters:

# [Studio UI](#tab/ui)

To open the schedule creation wizard, select **Schedule** > **Create new schedule** at the top of the page.

:::image type="content" source="./media/how-to-schedule-pipeline-job/schedule-entry-button.png" alt-text="Screenshot of the jobs tab showing the Create new schedule button selected." lightbox= "./media/how-to-schedule-pipeline-job/schedule-entry-button.png":::

---

# [Azure CLI / Python SDK](#tab/cliv2+python)

#### Parameters

- `frequency` **(required)** is the time unit on which basis the schedule fires. Can be `minutes`, `hours`, `days`, `weeks`, or `months`.
- `interval` **(required)** is the number of time units between schedule recurrences.
- `schedule` (optional) defines the recurrence pattern, which can contain `hours`, `minutes`, and `weekdays`. If omitted, jobs trigger according to the logic of `start_time`, `frequency`, and `interval`.
  - When `frequency` is `day`, the pattern can specify `hours` and `minutes`.
  - When `frequency` is `week` or `month`, the pattern can specify `hours`, `minutes`, and `weekdays`.
    - `hours` is an integer or list from 0 to 23.
    - `minutes` is an integer or list from 0 to 59.
    - `weekdays` is a string or list from `monday` to `sunday`.
- `start_time` (optional) is the start date and time with timezone. If omitted, the default is equal to schedule creation time. If the start time is in the past, the first job runs at the next calculated run time.
- `end_time` (optional) is the end date and time with timezone. If omitted, the schedule remains active until manually disabled.
- `time_zone` (optional) specifies the time zone of the recurrence schedule. If omitted, the default is Coordinated Universal Time (UTC). For more information about timezone values, see the [appendix for timezone values](reference-yaml-schedule.md#appendix).

# [Studio UI](#tab/ui)

To define a recurrence-based schedule, on the **Basic settings** screen, define the following properties. Only the **Name** property requires you to enter a value. If you don't specify values for the other properties, the default schedule is a **Recurrence** pattern that starts at schedule creation and runs every Monday through Friday at 4:00 PM UTC.

- **Name**: Unique identifier of the schedule within the workspace.
- **Description**: Schedule description.
- **Trigger**: Recurrence pattern of the schedule, including the following properties:
  - **Time zone**: Time zone to use for the trigger time, UTC by default.
  - Select **Recurrence** and specify a recurring pattern of minutes, hours, days, weeks, or months.
  - **Start**: Date the schedule becomes active, by default the date created.
  - **End**: Date when the schedule becomes inactive. By default the value is none, and the schedule remains active until manually disabled.
  - **Tags**: Tags on the schedule.

:::image type="content" source="./media/how-to-schedule-pipeline-job/create-schedule-basic-settings.png" alt-text="Screenshot of schedule creation wizard showing the basic settings." lightbox= "./media/how-to-schedule-pipeline-job/create-schedule-basic-settings.png":::

---

# [Azure CLI](#tab/cliv2)

After you create the schedule YAML, use the following command to create the schedule via CLI:

```azurecli
# This action creates related resources for a schedule. It takes dozens of seconds to complete.
az ml schedule create --file simple-pipeline-job.yml --no-wait
```

# [Python SDK](#tab/python)

The following Python code creates the schedule you defined:

[!Notebook-python[] (~/azureml-examples-main/sdk/python/schedules/job-schedule.ipynb?name=create_schedule)]

# [Studio UI](#tab/ui)

After you configure the basic settings, select **Review + Create**, review the settings, and then select **Review + Create** again to create the schedule.

---

### Define a time-based schedule with a cron expression

A cron expression can specify a flexible and customized recurrence pattern for a schedule. A standard crontab expression is composed of the space-delimited fields `MINUTES HOURS DAYS MONTHS DAYS-OF-WEEK`. A wildcard `*` means all values for a field.

In an Azure Machine Language schedule cron expression:

- `MINUTES` is an integer or list from 0 to 59.
- `HOURS` is an integer or list from 0 to 23.
- `DAYS` values aren't supported, and are always treated as `*`. The `*` value in `DAYS` means all days in a month, which varies with month and year. 
- `MONTHS` values aren't supported, and are always treated as `*`.
- `DAYS-OF-WEEK` is an integer or list from 0 to 6, where 0 = Sunday. Names of days are also accepted.

For example, the expression `15 16 * * 1` means 4:15 PM UTC every Monday. For more information about crontab expressions, see the [Crontab Expression wiki on GitHub](https://github.com/atifaziz/NCrontab/wiki/Crontab-Expression).

# [Azure CLI](#tab/cliv2)

The following YAML code defines a recurring schedule for a pipeline job. The required `type` parameter specifies that the `trigger` type is `cron`.

:::code language="yaml" source="~/azureml-examples-main/cli/schedules/cron-job-schedule.yml":::

You must or can provide the following schedule parameters:

# [Python SDK](#tab/python)

The following code uses `CronTrigger` to provide a better coding experience.

[!Notebook-python[] (~/azureml-examples-main/sdk/python/schedules/job-schedule.ipynb?name=create_schedule_cron)]

You must or can provide the following schedule parameters:

# [Studio UI](#tab/ui)

To define a cron-based schedule, select **Cron expression** instead of **Recurrence** on the **Basic settings** screen for the schedule.

---

# [Azure CLI / Python SDK](#tab/cliv2+python)

#### Parameters

- `expression` **(required)** is a standard crontab expression that expresses a recurring schedule.
- `start_time` (optional) is the schedule start date and time with timezone. For example, `start_time: "2022-05-10T10:15:00-04:00"` means the schedule starts from 10:15:00 AM on May 10, 2022 in UTC-4 timezone. If omitted, the default is equal to schedule creation time. If the start time is in the past, the first job runs at the next calculated run time.
- `end_time` (optional) is the end date and time with timezone. If omitted, the schedule remains active until manually disabled.
- `time_zone` (optional) specifies the time zone of the recurrence schedule. If omitted, the default is UTC.

# [Studio UI](#tab/ui)

Only the **Name** property requires you to enter a value. If you don't specify a cron expression, the default cron expression creates a schedule that runs daily at 4:00 PM UTC.

- **Name**: Unique identifier of the schedule within the workspace.
- **Description**: Description of the schedule.
- **Trigger**: Recurrence pattern of the schedule, including the following properties:
  - **Time zone**: Time zone to use for the trigger time, Coordinated Universal Time (UTC) by default.
  - Select **Cron expression** and provide a standard crontab expression that expresses a recurring schedule.
  - **Start**: Date the schedule becomes active, by default the date created.
  - **End**: Date the schedule becomes inactive. By default the value is none, and a schedule remains active until you manually disable it.
  - **Tags**: Tags on the schedule.

:::image type="content" source="./media/how-to-schedule-pipeline-job/create-schedule-basic-settings-cron.png" alt-text="Screenshot of schedule creation wizard showing the basic settings for cron." lightbox= "./media/how-to-schedule-pipeline-job/create-schedule-basic-settings-cron.png":::

---

# [Azure CLI](#tab/cliv2)

After you create the schedule YAML, use the following command to create the schedule via CLI:

```azurecli
# This action creates related resources for a schedule. It takes dozens of seconds to complete.
az ml schedule create --file simple-pipeline-job.yml --no-wait
```

# [Python SDK](#tab/python)

The following Python code creates the schedule you defined:

[!Notebook-python[] (~/azureml-examples-main/sdk/python/schedules/job-schedule.ipynb?name=create_schedule)]

# [Studio UI](#tab/ui)

After you configure the basic settings, select **Review + Create**, review the settings, and then select **Review + Create** again to create the schedule.

---

### Change job settings when you define schedules

Sometimes you might want the jobs triggered by schedules to have different configurations from the test jobs. When you define a schedule by using an existing job, you can change the job settings. This approach lets you define multiple schedules that use the same job with different inputs.

# [Azure CLI](#tab/cliv2)

When you define a schedule, you can change the `settings`, `inputs`, or `outputs` to use when running the pipeline job. You can also change the `experiment_name` of the triggered job.

The following schedule definition changes the settings of an existing job.

:::code language="yaml" source="~/azureml-examples-main/cli/schedules/cron-with-settings-job-schedule.yml":::

# [Python SDK](#tab/python)

When you define a schedule, you can change the `settings`, `inputs`, or `outputs` to use when running the pipeline job. You can also change the `experiment_name` of the triggered job.

The following schedule definition changes the settings of a pipeline per job.

[!Notebook-python[] (~/azureml-examples-main/sdk/python/schedules/job-schedule.ipynb?name=change_run_settings)]

# [Studio UI](#tab/ui)

In the studio UI, you can use **Advanced settings** in the schedule creation wizard to modify `inputs`, `outputs`, and runtime `settings` for a pipeline job. You can't change the `experiment_name` in the studio UI.

1. In **Job inputs & outputs**, you can modify inputs and outputs for future jobs triggered by the schedule. You can use macro expressions for the inputs and outputs paths.

   :::image type="content" source="./media/how-to-schedule-pipeline-job/create-schedule-advanced-settings-inputs-outputs.png" alt-text="Screenshot of create new schedule on the advanced settings job inputs and outputs tab." lightbox= "./media/how-to-schedule-pipeline-job/create-schedule-advanced-settings-inputs-outputs.png":::

1. In **Job runtime settings**, you can modify compute and other runtime settings for jobs triggered by the schedule.

   :::image type="content" source="./media/how-to-schedule-pipeline-job/create-schedule-advanced-settings-runtime.png" alt-text="Screenshot of schedule creation wizard showing the job runtime settings." lightbox= "./media/how-to-schedule-pipeline-job/create-schedule-advanced-settings-runtime.png":::

1. Select **Review + Create** to review the schedule settings you configured, and then select **Review + Create** again to create the schedule.

   :::image type="content" source="./media/how-to-schedule-pipeline-job/create-schedule-review.png" alt-text="Screenshot of schedule creation wizard showing the review of the schedule settings." lightbox= "./media/how-to-schedule-pipeline-job/create-schedule-review.png":::

---

#### Use supported expressions in schedules

When you define a schedule, you can use the following macro expressions to define dynamic parameter values that resolve to actual values during job runtime.

| Expression | Description |Supported properties|
|----------------|----------------|-------------|
|`${{name}}`|Name of the job|`outputs` path of the pipeline job|
|`${{creation_context.trigger_time}}`|Trigger time of the job | String type `inputs` of the pipeline job|

## Manage schedule

You can list, view details, update, disable, enable, and delete schedules in a workspace.

### List schedules

# [Azure CLI](#tab/cliv2)

:::code language="azurecli" source="~/azureml-examples-main/cli/schedules/schedule.sh" ID="list_schedule":::

# [Python SDK](#tab/python)

[!Notebook-python[] (~/azureml-examples-main/sdk/python/schedules/job-schedule.ipynb?name=list_schedule)]

# [Studio UI](#tab/ui)

Under **Jobs** in the studio, select the **All schedules** tab to see a list of all the v2 job schedules created by SDK, CLI, or studio UI in this workspace.

:::image type="content" source="./media/how-to-schedule-pipeline-job/schedule-list.png" alt-text="Screenshot of the all schedule tabs showing the list of schedule in this workspace." lightbox= "./media/how-to-schedule-pipeline-job/schedule-list.png":::

---

### View schedule details

# [Azure CLI](#tab/cliv2)

:::code language="azurecli" source="~/azureml-examples-main/cli/schedules/schedule.sh" ID="show_schedule":::

# [Python SDK](#tab/python)

[!Notebook-python[] (~/azureml-examples-main/sdk/python/schedules/job-schedule.ipynb?name=show_schedule)]

# [Studio UI](#tab/ui)

Select a schedule name to show the schedule detail page, which contains the following tabs:

- **Overview** provides basic information about the schedule.

  :::image type="content" source="./media/how-to-schedule-pipeline-job/schedule-detail-overview.png" alt-text="Screenshot of the overview tab in the schedule detail page." lightbox= "./media/how-to-schedule-pipeline-job/schedule-detail-overview.png":::

- **Job definition** defines the job triggered by the schedule.

  :::image type="content" source="./media/how-to-schedule-pipeline-job/schedule-detail-job-definition.png" alt-text="Screenshot of the job definition tab in the schedule detail page." lightbox= "./media/how-to-schedule-pipeline-job/schedule-detail-job-definition.png":::

- **Jobs history** provides a list of all jobs triggered by the schedule.

  :::image type="content" source="./media/how-to-schedule-pipeline-job/schedule-detail-jobs-history.png" alt-text="Screenshot of the jobs history tab in the schedule detail page." lightbox= "./media/how-to-schedule-pipeline-job/schedule-detail-jobs-history.png":::

---

### Update a schedule

# [Azure CLI](#tab/cliv2)

:::code language="azurecli" source="~/azureml-examples-main/cli/schedules/schedule.sh" ID="update_schedule":::

> [!NOTE]
> To update more than just tags and description, consider using `az ml schedule create --file update_schedule.yml`.

# [Python SDK](#tab/python)

[!Notebook-python[] (~/azureml-examples-main/sdk/python/schedules/job-schedule.ipynb?name=enable_schedule)]

# [Studio UI](#tab/ui)

In the schedule detail page, you can select **Update settings** to update the schedule settings, including job input/output and runtime settings.

:::image type="content" source="./media/how-to-schedule-pipeline-job/schedule-update-settings.png" alt-text="Screenshot of update settings showing the basic settings tab." lightbox= "./media/how-to-schedule-pipeline-job/schedule-update-settings.png":::

#### Update a new version pipeline to an existing schedule

Once you set up a schedule to do regular retraining or batch inference on production, you might continue fine tuning or optimizing the model. When you have a new version pipeline job with optimized performance, you can update the new version pipeline to run on an existing schedule.

1. In the new version pipeline job detail page, select **Schedule** > **Update to existing schedule**.

   :::image type="content" source="./media/how-to-schedule-pipeline-job/update-to-existing-schedule.png" alt-text="Screenshot of the jobs tab with schedule button selected showing update to existing schedule button." lightbox= "./media/how-to-schedule-pipeline-job/update-to-existing-schedule.png":::

1. Select an existing schedule to update its job definition.

   :::image type="content" source="./media/how-to-schedule-pipeline-job/update-select-schedule.png" alt-text="Screenshot of update select schedule showing the select schedule tab." lightbox= "./media/how-to-schedule-pipeline-job/update-select-schedule.png":::

   > [!IMPORTANT]
   > Make sure you select the correct schedule you want to update.

1. Optionally, select **Next** to modify the job inputs/outputs and runtime settings for the future jobs triggered by the schedule.

1. Select **Review + Update** to review the schedule settings, and then select **Review + Update** again to finish the update.

After the update completes, you can view the new job definition in the schedule detail page. The schedule now triggers the new job.

---

### Disable a schedule

# [Azure CLI](#tab/cliv2)

:::code language="azurecli" source="~/azureml-examples-main/cli/schedules/schedule.sh" ID="disable_schedule":::

# [Python SDK](#tab/python)

The following code returns `False`:

[!Notebook-python[] (~/azureml-examples-main/sdk/python/schedules/job-schedule.ipynb?name=disable_schedule)]

# [Studio UI](#tab/ui)

You can disable schedules from the **All schedules** tab or disable the current schedule from the schedule detail page.

---

### Enable a schedule

# [Azure CLI](#tab/cliv2)

:::code language="azurecli" source="~/azureml-examples-main/cli/schedules/schedule.sh" ID="enable_schedule":::

# [Python SDK](#tab/python)

The following code returns `True`:

```python
job_schedule = ml_client.schedules.begin_enable(name=schedule_name).result()
job_schedule.is_enabled
```

# [Studio UI](#tab/ui)

You can enable schedules from the **All schedules** tab or enable the current schedule from the schedule detail page.

---

### Delete a schedule

> [!IMPORTANT]
> You must first disable a schedule to delete it. Deletion is permanent and unrecoverable.

# [Azure CLI](#tab/cliv2)

:::code language="azurecli" source="~/azureml-examples-main/cli/schedules/schedule.sh" ID="delete_schedule":::  

# [Python SDK](#tab/python)

[!Notebook-python[] (~/azureml-examples-main/sdk/python/schedules/job-schedule.ipynb?name=delete_schedule)]

# [Studio UI](#tab/ui)

You can delete schedules from the **All schedules** tab or delete the current schedule from the schedule detail page.

---
## Query triggered jobs from a schedule

Jobs triggered by a specific schedule all have the display name `<schedule_name>-YYYYMMDDThhmmssZ`. For example, if a schedule named `named-schedule` runs every 12 hours starting at 6 AM on January 1, 2021, the display names of the jobs created are as follows:

- named-schedule-20210101T060000Z
- named-schedule-20210101T180000Z
- named-schedule-20210102T060000Z
- named-schedule-20210102T180000Z, and so on

:::image type="content" source="media/how-to-schedule-pipeline-job/schedule-triggered-pipeline-jobs.png" alt-text="Screenshot of the jobs tab in the Azure Machine Learning studio filtering by job display name." lightbox= "media/how-to-schedule-pipeline-job/schedule-triggered-pipeline-jobs.png":::

You can also apply [Azure CLI JMESPath query](/cli/azure/query-azure-cli) to query the jobs triggered by a schedule name.

:::code language="azurecli" source="~/azureml-examples-main/cli/schedules/schedule.sh" ID="query_triggered_jobs":::  

> [!TIP]
> The **Jobs history** tab on the schedule detail page in the studio provides a simple way to find all jobs triggered by a schedule.

---

## Role-based access controls (RBAC) support

Because schedules are used for production, it's important to reduce the possibility and impact of misoperation. Workspace admins can restrict access to schedule creation and management in a workspace.

Admins can configure the following action rules related to schedules in the Azure portal. For more information, see [Manage access to Azure Machine Learning workspaces](how-to-assign-roles.md).

| Action | Description                                                                | Rule                                                          |
|--------|----------------------------------------------------------------------------|---------------------------------------------------------------|
| Read   | Get and list schedules                       | Microsoft.MachineLearningServices/workspaces/schedules/read   |
| Write  | Create, update, disable, and enable schedules | Microsoft.MachineLearningServices/workspaces/schedules/write  |
| Delete | Delete schedules                             | Microsoft.MachineLearningServices/workspaces/schedules/delete |

## Cost considerations

Schedules are billed based on the number of schedules. Each schedule creates a logic app that Azure Machine Learning hosts on behalf of (HOBO) the user.
Therefore the logic app can't be shown as a resource under the user's subscription in Azure portal. 

On the other hand, the logic app charges back to the user's Azure subscription. HOBO resource costs are billed using the same meter emitted by the original resource provider. Charges appear under the host resource, which is the Azure Machine Learning workspace.

## Related content

- [CLI (v2) job schedule YAML schema](./reference-yaml-schedule.md)
- [CLI (v2) core YAML syntax](reference-yaml-core-syntax.md)
- [What are machine learning pipelines?](concept-ml-pipelines.md)
- [What is an Azure Machine Learning component?](concept-component.md)
