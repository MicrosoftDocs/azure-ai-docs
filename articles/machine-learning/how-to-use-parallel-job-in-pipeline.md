---
title: How to use parallel jobs in pipelines
titleSuffix: Azure Machine Learning
description: Learn how to configure and run parallel jobs in Azure Machine Learning pipelines by using the CLI v2 and Python SDK v2.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mlops
ms.topic: how-to
author: lgayhardt
ms.author: scottpolly
ms.reviewer: jturuk
ms.date: 01/12/2026
ms.custom:
  - devx-track-python
  - sdkv2
  - cliv2
  - update-code1
  - sfi-image-nochange
#customer intent: As a machine learning engineer, I need to learn how to run parallel jobs in Azure Machine Learning to distribute repeated tasks on multinode clusters.
---

# Use parallel jobs in pipelines

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

This article explains how to use the CLI v2 and Python SDK v2 to run parallel jobs in Azure Machine Learning pipelines. Parallel jobs accelerate job execution by distributing repeated tasks on powerful multinode compute clusters.

Machine learning engineers always have scale requirements on their training or inferencing tasks. For example, when a data scientist provides a single script to train a sales prediction model, machine learning engineers need to apply this training task to each individual data store. Challenges of this scale-out process include long execution times that cause delays, and unexpected issues that require manual intervention to keep the task running.

The core job of Azure Machine Learning parallelization is to split a single serial task into mini-batches. Then dispatch those mini-batches to multiple computes to run in parallel. Parallel jobs significantly reduce end-to-end execution time and also handle errors automatically. Consider using Azure Machine Learning Parallel jobs to train many models on top of your partitioned data or to accelerate your large-scale batch inferencing tasks.

For example, in a scenario where you run an object detection model on a large set of images, Azure Machine Learning parallel jobs let you distribute your images to run custom code in parallel on a specific compute cluster. Parallelization can significantly reduce time cost. Azure Machine Learning parallel jobs can also simplify and automate your process to make it more efficient.

## Prerequisites

- Have an Azure Machine Learning account and workspace.
- Understand [Azure Machine Learning pipelines](concept-ml-pipelines.md).

# [Azure CLI](#tab/cliv2)

- Install the Azure CLI and the `ml` extension. For more information, see [Install and set up the CLI](how-to-configure-cli.md). The `ml` extension automatically installs the first time you run an `az ml` command.
- Understand how to [create and run Azure Machine Learning pipelines and components with the CLI v2](how-to-create-component-pipelines-cli.md).

# [Python SDK](#tab/python)

- Install the [Azure Machine Learning SDK v2 for Python](/python/api/overview/azure/ai-ml-readme).
- Understand how to [create and run Azure Machine Learning pipelines and components with the Python SDK v2](how-to-create-component-pipeline-python.md).

---

## Create and run a pipeline with a parallel job step

An Azure Machine Learning parallel job can be used only as a step in a pipeline job.

# [Azure CLI](#tab/cliv2)

The following examples come from [Run a pipeline job using parallel job in pipeline](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/pipelines/iris-batch-prediction-using-parallel/) in the [Azure Machine Learning examples](https://github.com/Azure/azureml-examples) repository.

# [Python SDK](#tab/python)

The following examples come from the [Build a simple machine learning pipeline with parallel component](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/pipelines/1g_pipeline_with_parallel_nodes/pipeline_with_parallel_nodes.ipynb) notebook in the [Azure Machine Learning examples](https://github.com/Azure/azureml-examples) repository.

---

### Prepare for parallelization

This parallel job step requires preparation. You need an entry script that implements the predefined functions. You also need to set attributes in your parallel job definition that:

- Define and bind your input data.
- Set the data division method.
- Configure your compute resources.
- Call the entry script.

The following sections describe how to prepare the parallel job.

#### Declare the inputs and data division setting

A parallel job requires one major input to be split and processed in parallel. The major input data format can be either tabular data or a list of files.

Different data formats have different input types, input modes, and data division methods. The following table describes the options:

| Data format | Input type | Input mode | Data division method |
|: ---------- |: ------------- |: ------------- |: --------------- |
| File list | `mltable` or `uri_folder` | `ro_mount` or `download` | By size (number of files) or by partition |
| Tabular data | `mltable` | `direct` | By size (estimated physical size) or by partition |

> [!NOTE]
> If you use tabular `mltable` as your major input data, you need to:
>
> - Install the `mltable` library in your environment, as in line 9 of this [conda file](https://github.com/Azure/azureml-examples/blob/main/cli/jobs/parallel/1a_oj_sales_prediction/src/parallel_train/conda.yaml).
> - Have a *MLTable* specification file under your specified path with the `transformations: - read_delimited:` section filled out. For examples, see [Create and manage data assets](how-to-create-data-assets.md).

You can declare your major input data with the `input_data` attribute in the parallel job YAML or Python. Bind the data with the defined `input` of your parallel job by using `${{inputs.<input name>}}`. Then you define the data division attribute for your major input depending on your data division method.

| Data division method | Attribute name | Attribute type | Job example |
|: ---------- |: ------------- |: ------------- |: --------------- |
| By size | `mini_batch_size` | string | [Iris batch prediction](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/parallel/2a_iris_batch_prediction) |
| By partition | `partition_keys` | list of strings | [Orange juice sales prediction](https://github.com/Azure/azureml-examples/blob/main/cli/jobs/parallel/1a_oj_sales_prediction) |

#### Configure the compute resources for parallelization

After you define the data division attribute, configure the compute resources for your parallelization by setting the `instance_count` and `max_concurrency_per_instance` attributes.

| Attribute name | Type | Description | Default value |
|:-|--|:-|--|
| `instance_count` | integer | The number of nodes to use for the job. | 1 |
| `max_concurrency_per_instance` | integer | The number of processors on each node. | For a GPU compute: 1. For a CPU compute: number of cores. |

These attributes work together with your specified compute cluster, as shown in the following diagram:

:::image type="content" source="./media/how-to-use-parallel-job-in-pipeline/how-distributed-data-works-in-parallel-job.png" alt-text="Diagram showing how distributed data works in parallel job." border="false":::

#### Call the entry script

The entry script is a single Python file that implements the following three predefined functions with custom code.

| Function name | Required | Description | Input | Return |
| :------------ | -------- | :---------- | :---- | :----- |
| `Init()` | Y | Common preparation before starting to run mini-batches. For example, use this function to load the model into a global object. | -- | -- |
| `Run(mini_batch)` | Y | Implements main execution logic for mini-batches. | `mini_batch` is pandas dataframe if input data is a tabular data, or file path list if input data is a directory. | Dataframe, list, or tuple. |
| `Shutdown()` | N | Optional function to do custom cleanups before returning the compute to the pool. | -- | -- |

> [!IMPORTANT]
> To avoid exceptions when parsing arguments in `Init()` or `Run(mini_batch)` functions, use `parse_known_args` instead of `parse_args`. For an example of an entry script with argument parser, see the [iris_score](https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/machine-learning-pipelines/parallel-run/Code/iris_score.py).

> [!IMPORTANT]
> The `Run(mini_batch)` function requires a return of a dataframe, list, or tuple item. The parallel job uses the count of that return to measure the success items under that mini-batch. If the job processes all the items, the mini-batch count should be equal to the return list count.

The parallel job runs the functions in each processor, as shown in the following diagram.

:::image type="content" source="./media/how-to-use-parallel-job-in-pipeline/how-entry-script-works-in-parallel-job.png" alt-text="Diagram showing how entry script works in parallel job." border="false":::

See the following entry script examples:

- [Image identification for a list of image files](https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/machine-learning-pipelines/parallel-run/Code/digit_identification.py)
- [Iris classification for a tabular iris data](https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/machine-learning-pipelines/parallel-run/Code/iris_score.py)

To call the entry script, set the following two attributes in your parallel job definition:

| Attribute name | Type | Description |
|: ------------- | ---- |: ---------- |
| `code` | string | Local path to the source code directory to upload and use for the job. |
| `entry_script` | string | The Python file that contains the implementation of predefined parallel functions. |

#### Parallel job step example

# [Azure CLI](#tab/cliv2)

The following parallel job step declares the input type, mode, and data division method, binds the input, configures the compute, and calls the entry script.
:::code language="yaml" source="~/azureml-examples-main/cli/jobs/pipelines/iris-batch-prediction-using-parallel/pipeline.yml" range="14-51" highlight="5-8,18-22,32-33":::

# [Python](#tab/python)

The following code declares the `job_data_path` as input, binds it to the `input_data` attribute, sets the `mini_batch_size` data division attribute, and calls the entry script.

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/pipelines/1g_pipeline_with_parallel_nodes/pipeline_with_parallel_nodes.ipynb?name=parallel-job-for-file-data)]

---

#### Consider automation settings

Azure Machine Learning parallel job exposes many optional settings that can control the job without manual intervention. The following table describes these settings.

| Key | Type | Description | Allowed values | Default value | Set in attribute or program argument |
|--|--|--|--|--|--|
| `mini_batch_error_threshold` | integer | Number of failed mini-batches to ignore in this parallel job. If the count of failed mini-batches is higher than this threshold, the parallel job is marked as failed.<br><br>The mini-batch is marked as failed if:<br>- The count of return from `run()` is less than the mini-batch input count.<br>- Exceptions are caught in custom `run()` code. | `[-1, int.max]` | `-1`, meaning ignore all failed mini-batches | Attribute `mini_batch_error_threshold` |
| `mini_batch_max_retries` | integer | Number of retries when the mini-batch fails or times out. If all retries fail, the mini-batch is marked as failed per the `mini_batch_error_threshold` calculation. | `[0, int.max]` | `2` | Attribute `retry_settings.max_retries` |
| `mini_batch_timeout` | integer | Timeout in seconds for executing the custom `run()` function. If execution time is higher than this threshold, the mini-batch is aborted and marked as failed to trigger retry. | `(0, 259200]` | `60` | Attribute `retry_settings.timeout` |
| `item_error_threshold` | integer | The threshold of failed items. Failed items are counted by the number gap between inputs and returns from each mini-batch. If the sum of failed items is higher than this threshold, the parallel job is marked as failed. | `[-1, int.max]` | `-1`, meaning ignore all failures during parallel job | Program argument<br>`--error_threshold` |
| `allowed_failed_percent` | integer | Similar to `mini_batch_error_threshold`, but uses the percent of failed mini-batches instead of the count. | `[0, 100]` | `100` | Program argument<br>`--allowed_failed_percent` |
| `overhead_timeout` | integer | Timeout in seconds for initialization of each mini-batch. For example, load mini-batch data and pass it to the `run()` function. | `(0, 259200]` | `600` | Program argument<br>`--task_overhead_timeout` |
| `progress_update_timeout` | integer | Timeout in seconds for monitoring the progress of mini-batch execution. If no progress updates are received within this timeout setting, the parallel job is marked as failed. | `(0, 259200]` | Dynamically calculated by other settings | Program argument<br>`--progress_update_timeout` |
| `first_task_creation_timeout` | integer | Timeout in seconds for monitoring the time between the job start and the run of the first mini-batch. | `(0, 259200]` | `600` | Program argument<br>`--first_task_creation_timeout` |
| `logging_level` | string | The level of logs to dump to user log files. | `INFO`, `WARNING`, or `DEBUG` | `INFO` | Attribute `logging_level` |
| `append_row_to` | string | Aggregate all returns from each run of the mini-batch and output it into this file. Might refer to one of the outputs of the parallel job by using the expression `${{outputs.<output_name>}}`. |  |  | Attribute `task.append_row_to` |
| `copy_logs_to_parent` | string | Boolean option whether to copy the job progress, overview, and logs to the parent pipeline job. | `True` or `False` | `False` | Program argument<br>`--copy_logs_to_parent` |
| `resource_monitor_interval` | integer | Time interval in seconds to dump node resource usage (for example cpu or memory) to log folder under the *logs/sys/perf* path.<br><br>**Note:** Frequent dump resource logs slightly slow execution speed. Set this value to `0` to stop dumping resource usage. | `[0, int.max]` | `600` | Program argument<br>`--resource_monitor_interval` |

The following sample code updates these settings:

# [Azure CLI](#tab/cliv2)

:::code language="yaml" source="~/azureml-examples-main/cli/jobs/pipelines/iris-batch-prediction-using-parallel/pipeline.yml" range="14-61" highlight="24-28,39-48":::

# [Python](#tab/python)

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/pipelines/1g_pipeline_with_parallel_nodes/pipeline_with_parallel_nodes.ipynb?name=parallel-job-for-tabular-data)]

---

### Create the pipeline with parallel job step

# [Azure CLI](#tab/cliv2)

The following example shows the complete pipeline job with the parallel job step inline:

:::code language="yaml" source="~/azureml-examples-main/cli/jobs/pipelines/iris-batch-prediction-using-parallel/pipeline.yml" highlight="14-61":::

# [Python](#tab/python)

First, import the required libraries, initiate the `ml_client` with proper credentials, and create or retrieve your computes:

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/pipelines/1g_pipeline_with_parallel_nodes/pipeline_with_parallel_nodes.ipynb?name=required-library)]

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/pipelines/1g_pipeline_with_parallel_nodes/pipeline_with_parallel_nodes.ipynb?name=credential)]

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/pipelines/1g_pipeline_with_parallel_nodes/pipeline_with_parallel_nodes.ipynb?name=workspace)]

Then, implement the parallel job by completing the `parallel_run_function`:

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/pipelines/1g_pipeline_with_parallel_nodes/pipeline_with_parallel_nodes.ipynb?name=parallel-job-for-tabular-data)]

Finally, use your parallel job as a step in your pipeline and bind its inputs and outputs with other steps:

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/pipelines/1g_pipeline_with_parallel_nodes/pipeline_with_parallel_nodes.ipynb?name=build-pipeline)]

---

## Submit the pipeline job

# [Azure CLI](#tab/cliv2)

Submit your pipeline job with parallel step by using the `az ml job create` CLI command:

```azurecli
az ml job create --file pipeline.yml
```

# [Python](#tab/python)

Submit your pipeline job with parallel step by using the `jobs.create_or_update` function of `ml_client`:

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/pipelines/1g_pipeline_with_parallel_nodes/pipeline_with_parallel_nodes.ipynb?name=submit-pipeline)]

---

## Check parallel step in studio UI

After you submit a pipeline job, the SDK or CLI widget gives you a web URL link to the pipeline graph in the Azure Machine Learning studio UI.

To view parallel job results, double-click the parallel step in the pipeline graph, select the **Settings** tab in the details panel, expand **Run settings**, and then expand the **Parallel** section.

:::image type="content" source="./media/how-to-use-parallel-job-in-pipeline/screenshot-for-parallel-job-settings.png" alt-text="Screenshot of Azure Machine Learning studio showing the parallel job settings." lightbox ="./media/how-to-use-parallel-job-in-pipeline/screenshot-for-parallel-job-settings.png":::

To debug parallel job failure, select the **Outputs + logs** tab, expand the *logs* folder, and check *job_result.txt* to understand why the parallel job failed. For information about the logging structure of parallel jobs, see *readme.txt* in the same folder.

:::image type="content" source="./media/how-to-use-parallel-job-in-pipeline/screenshot-for-parallel-job-result.png" alt-text="Screenshot of Azure Machine Learning studio on the jobs tab showing the parallel job results." lightbox ="./media/how-to-use-parallel-job-in-pipeline/screenshot-for-parallel-job-result.png":::

## Related content

- [CLI (v2) parallel job YAML schema](reference-yaml-job-parallel.md)
- [Create and manage data assets](how-to-create-data-assets.md)
- [Schedule machine learning pipeline jobs](how-to-schedule-pipeline-job.md)
