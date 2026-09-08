---
title: 'CLI (v2) parallel job YAML schema'
titleSuffix: Azure Machine Learning
description: Reference documentation for the CLI (v2) parallel job YAML schema.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.topic: reference
ms.custom: cliv2
author: lgayhardt
ms.author: lagayhar
ms.reviewer: alainli
ms.date: 09/27/2022
---

# CLI (v2) parallel job YAML schema

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]


> [!IMPORTANT]
> You can use a parallel job only as a single step inside an Azure Machine Learning pipeline job. Therefore, there's no source JSON schema for parallel job. This article lists the valid keys and their values when creating a parallel job in a pipeline.

[!INCLUDE [schema note](includes/machine-learning-preview-old-json-schema-note.md)]

## YAML syntax

| Key | Type | Description | Allowed values | Default value |
| --- | ---- | ----------- | -------------- | ------------- |
| `type` | const | **Required.** The type of job. | `parallel` | |
| `inputs` | object | Dictionary of inputs to the parallel job. The key is a name for the input within the context of the job and the value is the input value. <br><br> You can reference inputs in the `program_arguments` by using the `${{ inputs.<input_name> }}` expression. <br><br> Pipeline inputs can reference parallel job inputs by using the `${{ parent.inputs.<input_name> }}` expression. For information about how to bind the inputs of a parallel step to the pipeline inputs, see the [Expression syntax for binding inputs and outputs between steps in a pipeline job](reference-yaml-core-syntax.md#binding-inputs-and-outputs-between-steps-in-a-pipeline-job). | | |
| `inputs.<input_name>` | number, integer, boolean, string, or object | One of a literal value (of type number, integer, boolean, or string) or an object containing a [job input data specification](#job-inputs). | | |
| `outputs` | object | Dictionary of output configurations of the parallel job. The key is a name for the output within the context of the job and the value is the output configuration. <br><br> Pipeline outputs can reference parallel job outputs by using the `${{ parents.outputs.<output_name> }}` expression. For information about how to bind the outputs of a parallel step to the pipeline outputs, see the [Expression syntax for binding inputs and outputs between steps in a pipeline job](reference-yaml-core-syntax.md#binding-inputs-and-outputs-between-steps-in-a-pipeline-job). | |
| `outputs.<output_name>` | object | You can leave the object empty. By default, the output is of type `uri_folder` and Azure Machine Learning system-generates an output location for the output based on the following templatized path: `{settings.datastore}/azureml/{job-name}/{output-name}/`. The job writes files to the output directory through a read-write mount. If you want to specify a different mode for the output, provide an object containing the [job output specification](#job-outputs). | |
| `compute` | string | Name of the compute target to execute the job on. The value can be either a reference to an existing compute in the workspace (using the `azureml:<compute_name>` syntax) or `local` to designate local execution. <br><br> When using parallel job in pipeline, you can leave this setting empty. The `default_compute` of pipeline auto-selects the compute.| | `local` |
| `task` | object | **Required.** The template for defining the distributed tasks for parallel job. See [Attributes of the `task` key](#attributes-of-the-task-key).|||
|`input_data`| object | **Required.**  Define which input data is split into mini-batches to run the parallel job. Only applicable for referencing one of the parallel job `inputs` by using the `${{ inputs.<input_name> }}` expression.|||
| `mini_batch_size` | string | Define the size of each mini-batch to split the input.<br><br> If the `input_data` is a folder or set of files, this number defines the **file count** for each mini-batch. For example, 10, 100.<br>If the `input_data` is a tabular data from `mltable`, this number defines the approximate physical size for each mini-batch. For example, 100 kb, 100 mb. ||1|
| `partition_keys` | list | The keys used to partition dataset into mini-batches.<br><br>If specified, the data with the same key is partitioned into the same mini-batch. If both `partition_keys` and `mini_batch_size` are specified, the partition keys take effect. |||
| `mini_batch_error_threshold` | integer | Define the number of failed mini batches that the job can ignore. If the count of failed mini-batch is higher than this threshold, the parallel job fails.<br><br>Mini-batch is marked as failed if:<br> - the count of return from run() is less than mini-batch input count. <br> - catch exceptions in custom run() code.<br><br> "-1" is the default number, which means to ignore all failed mini-batch during parallel job.|[-1, int.max]|-1|
| `logging_level` | string | Define which level of logs are sent to user log files. |INFO, WARNING, DEBUG|INFO|
| `resources.instance_count` | integer | The number of nodes to use for the job. | | 1 |
| `max_concurrency_per_instance` | integer| Define the number of processes on each node of compute.<br><br>For a GPU compute, the default value is 1.<br>For a CPU compute, the default value is the number of cores.|||
| `retry_settings.max_retries` | integer | Define the number of retries when mini-batch fails or times out. If all retries fail, the mini-batch is marked as failed to be counted by `mini_batch_error_threshold` calculation. ||2|
| `retry_settings.timeout` | integer | Define the timeout in seconds for executing custom run() function. If the execution time is higher than this threshold, the mini-batch is aborted, and marked as a failed mini-batch to trigger retry.|(0, 259200]|60|
| `environment_variables` | object | Dictionary of environment variable key-value pairs to set on the process where the command is executed. |||


### Attributes of the `task` key

| Key | Type | Description | Allowed values | Default value |
| --- | ---- | ----------- | -------------- | ------------- |
| `type` | const | **Required.** The type of task. Only applicable for `run_function` by now.<br><br> In `run_function` mode, you're required to provide `code`, `entry_script`, and `program_arguments` to define Python script with executable functions and arguments. Note: Parallel job only supports Python script in this mode. | run_function | run_function |
| `code` | string | Local path to the source code directory to upload and use for the job. |||
| `entry_script` | string | The Python file that contains the implementation of pre-defined parallel functions. For more information, see [Prepare entry script to parallel job](how-to-use-parallel-job-in-pipeline.md#prepare-for-parallelization). |||
| `environment` | string or object | **Required** The environment to use for running the task. The value can be either a reference to an existing versioned environment in the workspace or an inline environment specification. <br><br> To reference an existing environment, use the `azureml:<environment_name>:<environment_version>` syntax or `azureml:<environment_name>@latest` (to reference the latest version of an environment). <br><br> To define an inline environment, follow the [Environment schema](reference-yaml-environment.md#yaml-syntax). Exclude the `name` and `version` properties as they aren't supported for inline environments.|||
| `program_arguments` | string | The arguments to pass to the entry script. May contain  "--\<arg_name\> ${{inputs.\<intput_name\>}}" reference to inputs or outputs.<br><br> Parallel job provides a list of predefined arguments to set configuration of parallel run. For more information, see [predefined arguments for parallel job](#predefined-arguments-for-parallel-job). |||
| `append_row_to` | string | Aggregate all returns from each run of mini-batch and output it into this file. May reference to one of the outputs of parallel job by using the expression \${{outputs.<output_name>}} |||

### Job inputs

| Key | Type | Description | Allowed values | Default value |
| --- | ---- | ----------- | -------------- | ------------- |
| `type` | string | The type of job input. Specify `mltable` for input data that points to a location where has the mltable meta file, or `uri_folder` for input data that points to a folder source. | `mltable`, `uri_folder` | `uri_folder` |
| `path` | string | The path to the data to use as input. Specify the value in one of the following ways: <br><br> - A local path to the data source file or folder, for example, `path: ./iris.csv`. The data is uploaded during job submission. <br><br> - A URI of a cloud path to the file or folder to use as the input. Supported URI types are `azureml`, `https`, `wasbs`, `abfss`, `adl`. For more information, see [Core yaml syntax](reference-yaml-core-syntax.md) on how to use the `azureml://` URI format. <br><br> - An existing registered Azure Machine Learning data asset to use as the input. To reference a registered data asset, use the `azureml:<data_name>:<data_version>` syntax or `azureml:<data_name>@latest` (to reference the latest version of that data asset), for example, `path: azureml:cifar10-data:1` or `path: azureml:cifar10-data@latest`. | | |
| `mode` | string | Mode of how the data should be delivered to the compute target. <br><br> For read-only mount (`ro_mount`), the data is consumed as a mount path. A folder is mounted as a folder and a file is mounted as a file. Azure Machine Learning resolves the input to the mount path. <br><br> For `download` mode the data is downloaded to the compute target. Azure Machine Learning resolves the input to the downloaded path. <br><br> If you only want the URL of the storage location of the data artifacts rather than mounting or downloading the data itself, use the `direct` mode. It passes in the URL of the storage location as the job input. In this case, you're fully responsible for handling credentials to access the storage. | `ro_mount`, `download`, `direct` | `ro_mount` |

### Job outputs

| Key | Type | Description | Allowed values | Default value |
| --- | ---- | ----------- | -------------- | ------------- |
| `type` | string | The type of job output. For the default `uri_folder` type, the output corresponds to a folder. | `uri_folder` | `uri_folder` |
| `mode` | string | Mode of how output files get delivered to the destination storage. For read-write mount mode (`rw_mount`) the output directory is a mounted directory. For upload mode the files written get uploaded at the end of the job. | `rw_mount`, `upload` | `rw_mount` |

### Predefined arguments for parallel job
| Key  | Description | Allowed values | Default value |
| ---  | ----------- | -------------- | ------------- |
| `--error_threshold`  | The threshold of **failed items**. The system counts failed items by the number gap between inputs and returns from each mini-batch. If the sum of failed items is higher than this threshold, the parallel job fails.<br><br>Note: "-1" is the default number, which means the system ignores all failures during the parallel job.| [-1, int.max] | -1 |
| `--allowed_failed_percent`  | Similar to `mini_batch_error_threshold` but uses the percent of failed mini-batches instead of the count. | [0, 100] | 100 |
| `--task_overhead_timeout`  | The timeout in seconds for initialization of each mini-batch. For example, load mini-batch data and pass it to run() function. | (0, 259200] | 30 |
| `--progress_update_timeout`  | The timeout in seconds for monitoring the progress of mini-batch execution. If no progress updates receive within this timeout setting, the parallel job fails. | (0, 259200] | Dynamically calculated by other settings. |
| `--first_task_creation_timeout`  | The timeout in seconds for monitoring the time between the job start to the run of first mini-batch. | (0, 259200] | 600 |
| `--copy_logs_to_parent`  | Boolean option to whether copy the job progress, overview, and logs to the parent pipeline job. | True, False | False |
| `--metrics_name_prefix`  | Provide the custom prefix of your metrics in this parallel job. |  |  |
| `--push_metrics_to_parent`  | Boolean option to whether push metrics to the parent pipeline job. | True, False | False |
| `--resource_monitor_interval`  | The time interval in seconds to dump node resource usage (for example, CPU, memory) to log folder under "logs/sys/perf" path. <br><br> Note: Frequent dump resource logs slightly slows down the execution speed of your mini-batch. Set this value to "0" to stop dumping resource usage. | [0, int.max] | 600 |

## Remarks

Use the `az ml job` commands to manage Azure Machine Learning jobs.

## Examples

Examples are available in the [examples GitHub repository](https://github.com/Azure/azureml-examples/tree/main/cli/jobs). Several are shown in the following section.

## YAML: Using parallel job in pipeline

:::code language="yaml" source="~/azureml-examples-main/cli/jobs/pipelines/iris-batch-prediction-using-parallel/pipeline.yml":::

## Next steps

- [Install and use the CLI (v2)](how-to-configure-cli.md)
