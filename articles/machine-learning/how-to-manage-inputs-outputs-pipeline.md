---
title: Manage component and pipeline inputs and outputs
titleSuffix: Azure Machine Learning
description: Learn how to manage inputs and outputs of components and pipelines in Azure Machine Learning.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.author: lagayhar
author: lgayhardt
ms.reviewer: zhanxia
ms.date:  09/11/2024
ms.topic: how-to
ms.custom: devplatv2, pipeline, devx-track-azurecli, update-code6
---
# Manage component and pipeline inputs and outputs

Azure Machine Learning pipelines support inputs and outputs at both the component and pipeline levels. This article describes pipeline and component inputs and outputs and how to manage them.

At the component level, the inputs and outputs define the interface of a component. You can use the output from one component as an input for another component in the same parent pipeline, allowing for data or models to be passed between components. This interconnectivity forms a graph that illustrates the data flow within the pipeline.

At the pipeline level, you can use inputs and outputs to submit pipeline jobs with varying data inputs or parameters that control training logic, such as `learning_rate`. When you invoke a pipeline via a REST endpoint, inputs and outputs are especially useful for assigning different values to the pipeline input or accessing the output of pipeline jobs. For more information, see [Create jobs and input data for batch endpoints](how-to-access-data-batch-endpoints-jobs.md).

## Input and output types

The following types are supported as **inputs** or **outputs** of a component or pipeline:
 
Data types. For more information, see [Data types](concept-data.md#data-types).
- `uri_file`
- `uri_folder`
- `mltable`

Model types.
- `mlflow_model`
- `custom_model`

Pipeline or component **inputs** can also be the following primitive types:
- `string`
- `number`
- `integer`
- `boolean`

Primitive types **output** isn't supported.

Using data or model output serializes the outputs and saves them as files in a storage location. Later steps can mount this storage location, or download or upload the files to the compute file system, allowing the steps to access the files during job execution.

This process requires the component source code to serialize the desired output object, usually stored in memory, into files. For example, you could serialize a pandas dataframe as a CSV file. Azure Machine Learning doesn't define any standardized methods for object serialization. Users have the flexibility to choose their preferred methods to serialize objects into files. In the downstream component, you can independently deserialize and read these files.

### Examples

The following example inputs and outputs are from the [NYC Taxi Data Regression](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/pipelines-with-components/nyc_taxi_data_regression) pipeline in the [Azure Machine Learning examples](https://github.com/Azure/azureml-examples) GitHub repository.

- The [train component](https://github.com/Azure/azureml-examples/blob/main/cli/jobs/pipelines-with-components/nyc_taxi_data_regression/train.yml) has a `number` input named `test_split_ratio`.
- The [prep component](https://github.com/Azure/azureml-examples/blob/main/cli/jobs/pipelines-with-components/nyc_taxi_data_regression/prep.yml) has  an`uri_folder` type output. The component source code reads the CSV files from the input folder, processes the files, and writes the processed CSV files to the output folder.
- The [train component](https://github.com/Azure/azureml-examples/blob/main/cli/jobs/pipelines-with-components/nyc_taxi_data_regression/train.yml) has a `mlflow_model` type output. The component source code saves the trained model using `mlflow.sklearn.save_model` method.

## Data type input and output paths and modes

For data asset inputs and outputs, you must specify a `path` parameter that points to the data location. The following table shows the different data locations that Azure Machine Learning pipelines support, with `path` parameter examples:

|Location  | Examples  | Input | Output|
|---------|---------|---------|---------|
|A path on your local computer     | `./home/username/data/my_data`         | ✓ | |
|A path on a public http(s) server    |  `https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv`    | ✓ | |
|A path on Azure Storage     |   `wasbs://<container_name>@<account_name>.blob.core.windows.net/<path>`<br>`abfss://<file_system>@<account_name>.dfs.core.windows.net/<path>`    | \* |  |
|A path on an Azure Machine Learning datastore   |   `azureml://datastores/<data_store_name>/paths/<path>`  | ✓ | ✓ |
|A path to a data asset  |  `azureml:<my_data>:<version>`  |✓ | ✓ |

\* Using Azure Storage directly isn't recommended for input/output, because it might need extra identity configuration to read the data. It's better to use an Azure Machine Learning datastore path instead of a direct Azure Storage path. Datastore paths are supported across various job types in pipelines.

For data input/output, you can choose from various download, upload, and mount modes to define how to access data in the compute target. The following table shows the possible modes for different types of inputs and outputs.

Type | `upload` | `download` | `ro_mount` | `rw_mount` | `direct` | `eval_download` | `eval_mount` 
------ | ------ | :---: | :---: | :---: | :---: | :---: | :---: | :---:
`uri_folder` input  |   | ✓  |  ✓  |   | ✓  |  | 
`uri_file` input |   | ✓  |  ✓  |   | ✓  |  | 
`mltable` input |   | ✓  |  ✓  |   | ✓  | ✓ | ✓
`uri_folder` output  | ✓  |   |    | ✓  |   |  | 
`uri_file` output | ✓  |   |    | ✓  |   |  | 
`mltable` output | ✓  |   |    | ✓  | ✓  |  | 

> [!NOTE]
> In most cases, `ro_mount` or `rw_mount` modes are suggested. For more information, see [Modes](how-to-read-write-data-v2.md#modes). 

## Inputs and outputs in the studio UI

The following screenshots show how the Azure Machine Learning studio UI displays inputs and outputs in the [NYC Taxi Data Regression](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/pipelines-with-components/nyc_taxi_data_regression) pipeline from the [Azure Machine Learning examples](https://github.com/Azure/azureml-examples) repository.

The studio pipeline job page shows data or model type inputs/outputs as small circles, called input/output ports, in the corresponding component. These ports represent the data flow in a pipeline. Pipeline level output is displayed as a purple box for easy identification.

:::image type="content" source="./media/how-to-manage-pipeline-input-output/input-output-port.png" lightbox="./media/how-to-manage-pipeline-input-output/input-output-port.png" alt-text="Screenshot highlighting the pipeline input and output ports.":::

When you hover over an input/output port, the type is displayed.

:::image type="content" source="./media/how-to-manage-pipeline-input-output/hover-port.png" alt-text="Screenshot that highlights the port type when hovering over the port.":::

Primitive type inputs aren't displayed on the graph. You can find these inputs on the **Settings** tab of the pipeline job overview panel for pipeline level inputs, or the component panel for component level inputs.

The following screenshot shows the **Settings** tab of a pipeline job, which you can open by selecting **Job Overview**. To check inputs for a component, double-click the component to open the component panel.

:::image type="content" source="./media/how-to-manage-pipeline-input-output/job-overview-setting.png" lightbox="./media/how-to-manage-pipeline-input-output/job-overview-setting.png" alt-text="Screenshot highlighting the job overview setting panel.":::

When you edit a pipeline in the Designer, the pipeline inputs and outputs are in the **Pipeline interface** panel, and the component inputs and outputs are in the component's panel. 

:::image type="content" source="./media/how-to-manage-pipeline-input-output/pipeline-interface.png" lightbox="./media/how-to-manage-pipeline-input-output/pipeline-interface.png" alt-text="Screenshot highlighting the pipeline interface in Designer.":::

## Promote component inputs/outputs to pipeline level

Promoting a component's input/output to the pipeline level lets you overwrite the component's input/output when you submit a pipeline job. Promoting to the pipeline level is also useful for triggering the pipeline by using the REST endpoint.

The following examples show how to promote component level inputs/outputs to pipeline level inputs/outputs.

# [Azure CLI](#tab/cli)

The following pipeline promotes three inputs and three outputs to the pipeline level. For example, `pipeline_job_training_max_epocs` is declared under the `inputs` section on the root level, which means it's pipeline level input.

Under `train_job` in the `jobs` section, the input named `max_epocs` is referenced as `${{parent.inputs.pipeline_job_training_max_epocs}}`, meaning that the `train_job`'s `max_epocs` input references the pipeline level `pipeline_job_training_max_epocs` input. You can promote pipeline output by using the same schema.

:::code language="yaml" source="~/azureml-examples-main/cli/jobs/pipelines-with-components/basics/1b_e2e_registered_components/pipeline.yml" range="1-65" highlight="6-17,30,34,52,57,63,65":::

You can find the full example at [train-score-eval pipeline with registered components](https://github.com/Azure/azureml-examples/blob/main/cli/jobs/pipelines-with-components/basics/1b_e2e_registered_components/pipeline.yml) in the [Azure Machine Learning examples](https://github.com/Azure/azureml-examples) repository.

# [Python SDK](#tab/python)

The following code example defines the `nyc_taxi_data_regression` pipeline. The pipeline takes one input, `pipeline_job_input`, and generates six outputs as defined in the `return` statement. The pipeline outputs are promoted from the child component using the schema `<step_name.outputs.output_name>`, for example `prepare_sample_data.outputs.prep_data`.

You can find the end-to-end notebook at [NYC taxi data regression](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/pipelines/2c_nyc_taxi_data_regression/nyc_taxi_data_regression.ipynb) in the [Azure Machine Learning examples](https://github.com/Azure/azureml-examples) repository.

```python
# import required libraries
from azure.identity import DefaultAzureCredential

from azure.ai.ml import MLClient, Input
from azure.ai.ml.dsl import pipeline
from azure.ai.ml import load_component

# Set your subscription, resource group and workspace name:
subscription_id = "<SUBSCRIPTION_ID>"
resource_group = "<RESOURCE_GROUP>"
workspace = "<AML_WORKSPACE_NAME>"

# connect to the AzureML workspace
ml_client = MLClient(
    DefaultAzureCredential(), subscription_id, resource_group, workspace
)

# define the directory that stores the input data 
parent_dir = ""

# Load components
prepare_data = load_component(source=parent_dir + "./prep.yml")
transform_data = load_component(source=parent_dir + "./transform.yml")
train_model = load_component(source=parent_dir + "./train.yml")
predict_result = load_component(source=parent_dir + "./predict.yml")
score_data = load_component(source=parent_dir + "./score.yml")

# Construct pipeline. 
@pipeline()
def nyc_taxi_data_regression(pipeline_job_input):
    """NYC taxi data regression example."""
    prepare_sample_data = prepare_data(raw_data=pipeline_job_input)
    transform_sample_data = transform_data(
        clean_data=prepare_sample_data.outputs.prep_data
    )
    train_with_sample_data = train_model(
        training_data=transform_sample_data.outputs.transformed_data
    )
    predict_with_sample_data = predict_result(
        model_input=train_with_sample_data.outputs.model_output,
        test_data=train_with_sample_data.outputs.test_data,
    )
    score_with_sample_data = score_data(
        predictions=predict_with_sample_data.outputs.predictions,
        model=train_with_sample_data.outputs.model_output,
    )
    return {
        "pipeline_job_prepped_data": prepare_sample_data.outputs.prep_data,
        "pipeline_job_transformed_data": transform_sample_data.outputs.transformed_data,
        "pipeline_job_trained_model": train_with_sample_data.outputs.model_output,
        "pipeline_job_test_data": train_with_sample_data.outputs.test_data,
        "pipeline_job_predictions": predict_with_sample_data.outputs.predictions,
        "pipeline_job_score_report": score_with_sample_data.outputs.score_report,
    }
# Build pipeline job
pipeline_job = nyc_taxi_data_regression(
    Input(type="uri_folder", path=parent_dir + "./data/")
)
# demo how to change pipeline output settings
pipeline_job.outputs.pipeline_job_prepped_data.mode = "rw_mount"

# set pipeline level compute
pipeline_job.settings.default_compute = "cpu-cluster"
# set pipeline level datastore
pipeline_job.settings.default_datastore = "workspaceblobstore"
```

---

### Studio UI

You can promote a component's input to pipeline level input in the studio Designer authoring page.

1. Open the component's settings panel by double clicking the component.
1. Find the input you want to promote and select the three dots on the right.
1. Select **Add to pipeline input**.

   :::image type="content" source="./media/how-to-manage-pipeline-input-output/promote-pipeline-input.png" lightbox="./media/how-to-manage-pipeline-input-output/promote-pipeline-input.png" alt-text="Screenshot highlighting how to promote to pipeline input in Designer.":::

## Define optional inputs

By default, all inputs are required and must be assigned a default value or a value each time you submit a pipeline job. However, you can define an optional input and not assign a value to the input when you submit a pipeline job.

> [!NOTE]
> Optional outputs aren't supported.

If you have an optional data/model type input and don't assign a value to it when submitting the pipeline job, a component in the pipeline lacks a preceding data dependency. The component's input port isn't linked to any component or data/model node. This situation causes the pipeline service to invoke the component directly, instead of waiting for the preceding dependency to be ready.

If you set `continue_on_step_failure = True` for the pipeline and a second node uses required output from the first node, the second node doesn't execute if the first node fails. But if the second node uses optional input from the first node, it executes even if the first node fails. The following screenshot illustrates this scenario:

:::image type="content" source="./media/how-to-manage-pipeline-input-output/continue-on-failure-optional-input.png" alt-text="Screenshot showing the orchestration logic of optional input and continue on failure.":::

The following YAML code example shows how to define optional input. When the input is set as `optional = true`, you need to use `$[[]]` to embrace the command line with inputs, as in the highlighted lines of the example.

:::code language="yaml" source="~/azureml-examples-main/cli/assets/component/train.yml" range="1-34" highlight="11-21,30-32":::

In a pipeline graph, optional inputs of data/model types are represented by dotted circles. Optional inputs of primitive types are in the **Settings** tab. Unlike required inputs, optional inputs don't have an asterisk next to them, showing that they aren't mandatory.

:::image type="content" source="./media/how-to-manage-pipeline-input-output/optional-input.png" lightbox="./media/how-to-manage-pipeline-input-output/optional-input.png" alt-text="Screenshot highlighting the optional input.":::

## Customize output paths

By default, component output is stored in `azureml://datastores/${{default_datastore}}/paths/${{name}}/${{output_name}}`, the `{default_datastore}` you set for the pipeline. If not set, the default is the workspace blob storage.

The job `{name}` is resolved at job execution time, and the `{output_name}` is the name you defined in the component YAML. But you can customize where to store the output by defining the path of an output, as in the following examples.

# [Azure CLI](#tab/cli)

The *pipeline.yml* file defines a pipeline that has three pipeline level outputs. You can use the following command to set custom output paths for the `pipeline_job_trained_model` output.

```azurecli
# define the custom output path using datastore uri
# add relative path to your blob container after "azureml://datastores/<datastore_name>/paths"
output_path="azureml://datastores/{datastore_name}/paths/{relative_path_of_container}"  

# create job and define path using --outputs.<outputname>
az ml job create -f ./pipeline.yml --set outputs.pipeline_job_trained_model.path=$output_path  
```

You can find the full YAML file at [train-score-eval pipeline with registered components example](https://github.com/Azure/azureml-examples/blob/main/cli/jobs/pipelines-with-components/basics/1b_e2e_registered_components/pipeline.yml).

# [Python SDK](#tab/python)

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/pipelines/1b_pipeline_with_python_function_components/pipeline_with_python_function_components.ipynb?name=custom-output-path)] 

You can find the end-to-end notebook at [Build pipeline with command_component decorated python function](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/pipelines/1b_pipeline_with_python_function_components/pipeline_with_python_function_components.ipynb).

---

## Download pipeline outputs

# [Azure CLI](#tab/cli)

```azurecli
# Download all the outputs of the job
az ml job download --all -n <JOB_NAME> -g <RESOURCE_GROUP_NAME> -w <WORKSPACE_NAME> --subscription <SUBSCRIPTION_ID>

# Download specific output
az ml job download --output-name <OUTPUT_PORT_NAME> -n <JOB_NAME> -g <RESOURCE_GROUP_NAME> -w <WORKSPACE_NAME> --subscription <SUBSCRIPTION_ID>
```

# [Python SDK](#tab/python)

First, create and initialize `ml_client` as a handle to reference your workspace. For more information, see [Create a handle to the workspace](tutorial-explore-data.md#create-a-handle-to-the-workspace).

```python
# Set your subscription, resource group and workspace name:
subscription_id = "<SUBSCRIPTION_ID>"
resource_group = "<RESOURCE_GROUP>"
workspace = "<AML_WORKSPACE_NAME>"

# connect to the AzureML workspace
ml_client = MLClient(
    DefaultAzureCredential(), subscription_id, resource_group, workspace
)
```

To download pipeline-level outputs:

```python
# Download all the outputs of the job
output = client.jobs.download(name=job.name, download_path=tmp_path, all=True)

# Download specific output
output = client.jobs.download(name=job.name, download_path=tmp_path, output_name=output_port_name)
```
---

### Download child job outputs

To download the output of a child component that isn't promoted to pipeline level, first list all child job entities of a pipeline job and then use similar code to download the output.

# [Azure CLI](#tab/cli)

```azurecli
# List all child jobs in the job and print job details in table format
az ml job list --parent-job-name <JOB_NAME> -g <RESOURCE_GROUP_NAME> -w <WORKSPACE_NAME> --subscription <SUBSCRIPTION_ID> -o table

# Select the desired child job name to download output
az ml job download --all -n <JOB_NAME> -g <RESOURCE_GROUP_NAME> -w <WORKSPACE_NAME> --subscription <SUBSCRIPTION_ID>
```

# [Python SDK](#tab/python)

First, create and initialize `ml_client` as a handle to reference your workspace. For more information, see [Create a handle to the workspace](tutorial-explore-data.md#create-a-handle-to-the-workspace).

```python
# Set your subscription, resource group and workspace name:
subscription_id = "<SUBSCRIPTION_ID>"
resource_group = "<RESOURCE_GROUP>"
workspace = "<AML_WORKSPACE_NAME>"

# connect to the AzureML workspace
ml_client = MLClient(
    DefaultAzureCredential(), subscription_id, resource_group, workspace
)
```

Download child job output:

```python
# List all child jobs in the job
child_jobs = client.jobs.list(parent_job_name=job.name)
# Traverse and download all the outputs of child job
for child_job in child_jobs:
    client.jobs.download(name=child_job.name, all=True)
```
---

## Register output as a named asset

You can register output of a component or pipeline as named asset by assigning `name` and `version` to the output. The registered asset can be listed in your workspace through the studio UI, CLI, or SDK and can be referenced in future workspace jobs.

### Register pipeline-level output

# [Azure CLI](#tab/cli)

```yaml
display_name: register_pipeline_output
type: pipeline
jobs:
  node:
    type: command
    inputs:
      component_in_path:
        type: uri_file
        path: https://dprepdata.blob.core.windows.net/demo/Titanic.csv
    component: ../components/helloworld_component.yml
    outputs:
      component_out_path: ${{parent.outputs.component_out_path}}
outputs:
  component_out_path:
    type: mltable
    name: pipeline_output  # Define name and version to register pipeline output
    version: '1'
settings:
  default_compute: azureml:cpu-cluster
```

# [Python SDK](#tab/python)

```python
from azure.ai.ml import dsl, Output

# Load component functions
components_dir = "./components/"
helloworld_component = load_component(source=f"{components_dir}/helloworld_component.yml")

@pipeline()
def register_pipeline_output():
  # Call component obj as function: apply given inputs & parameters to create a node in pipeline
  node = helloworld_component(component_in_path=Input(
    type='uri_file', path='https://dprepdata.blob.core.windows.net/demo/Titanic.csv'))

  return {
      'component_out_path': node.outputs.component_out_path
  }

pipeline = register_pipeline_output()
# Define name and version to register pipeline output
pipeline.settings.default_compute = "azureml:cpu-cluster"
pipeline.outputs.component_out_path.name = 'pipeline_output'
pipeline.outputs.component_out_path.version = '1'
```
---
 
### Register child job output

# [Azure CLI](#tab/cli)

```yaml
display_name: register_node_output
type: pipeline
jobs:
  node:
    type: command
    component: ../components/helloworld_component.yml
    inputs:
      component_in_path:
        type: uri_file
        path: 'https://dprepdata.blob.core.windows.net/demo/Titanic.csv'
    outputs:
      component_out_path:
        type: uri_folder
        name: 'node_output'  # Define name and version to register a child job's output
        version: '1'
settings:
  default_compute: azureml:cpu-cluster
```

# [Python SDK](#tab/python)

```python
from azure.ai.ml import dsl, Output

# Load component functions
components_dir = "./components/"
helloworld_component = load_component(source=f"{components_dir}/helloworld_component.yml")

@pipeline()
def register_node_output():
  # Call component obj as function: apply given inputs & parameters to create a node in pipeline
  node = helloworld_component(component_in_path=Input(
    type='uri_file', path='https://dprepdata.blob.core.windows.net/demo/Titanic.csv'))

  # Define name and version to register node output
  node.outputs.component_out_path.name = 'node_output'
  node.outputs.component_out_path.version = '1'

pipeline = register_node_output()
pipeline.settings.default_compute = "azureml:cpu-cluster"
```
---

## Related content

- [YAML reference for pipeline job](./reference-yaml-job-pipeline.md)
- [How to debug pipeline failure](./how-to-debug-pipeline-failure.md)
- [Schedule a pipeline job](./how-to-schedule-pipeline-job.md)
- [Deploy a pipeline with batch endpoints (preview)](./how-to-use-batch-pipeline-deployments.md)
