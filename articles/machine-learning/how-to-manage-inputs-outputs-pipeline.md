---
title: Manage inputs and outputs for components and pipelines
titleSuffix: Azure Machine Learning
description: Understand and manage inputs and outputs of pipeline components and pipeline jobs in Azure Machine Learning.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.author: lagayhar
author: lgayhardt
ms.reviewer: zhanxia
ms.date: 09/18/2025
ms.topic: how-to
ms.custom: devplatv2, pipeline, devx-track-azurecli, update-code6
---
# Manage inputs and outputs for components and pipelines

Azure Machine Learning pipelines support inputs and outputs at both the component and pipeline levels. This article describes pipeline and component inputs and outputs and how to manage them.

At the component level, the inputs and outputs define the component interface. You can use the output from one component as an input for another component in the same parent pipeline, allowing for data or models to be passed between components. This interconnectivity represents the data flow within the pipeline.

At the pipeline level, you can use inputs and outputs to submit pipeline jobs with varying data inputs or parameters, such as `learning_rate`. Inputs and outputs are especially useful when you invoke a pipeline via a REST endpoint. You can assign different values to the pipeline input or access the output of different pipeline jobs. For more information, see [Create jobs and input data for batch endpoints](how-to-access-data-batch-endpoints-jobs.md).

## Input and output types

The following types are supported as both inputs and outputs of components or pipelines:
 
- Data types. For more information, see [Data types](concept-data.md#data-types).
  - `uri_file`
  - `uri_folder`
  - `mltable`

- Model types.
  - `mlflow_model`
  - `custom_model`

The following primitive types are also supported for inputs only:

- Primitive types
  - `string`
  - `number`
  - `integer`
  - `boolean`

Primitive type output isn't supported.

### Example inputs and outputs

These examples are from the [NYC Taxi Data Regression](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/pipelines-with-components/nyc_taxi_data_regression) pipeline in the [Azure Machine Learning examples](https://github.com/Azure/azureml-examples) GitHub repository:

- The [train component](https://github.com/Azure/azureml-examples/blob/main/cli/jobs/pipelines-with-components/nyc_taxi_data_regression/train.yml) has a `number` input named `test_split_ratio`.
- The [prep component](https://github.com/Azure/azureml-examples/blob/main/cli/jobs/pipelines-with-components/nyc_taxi_data_regression/prep.yml) has a `uri_folder` type output. The component source code reads the CSV files from the input folder, processes the files, and writes the processed CSV files to the output folder.
- The [train component](https://github.com/Azure/azureml-examples/blob/main/cli/jobs/pipelines-with-components/nyc_taxi_data_regression/train.yml) has a `mlflow_model` type output. The component source code saves the trained model using the `mlflow.sklearn.save_model` method.

## Output serialization

Using data or model outputs serializes the outputs and saves them as files in a storage location. Later steps can access the files during job execution by mounting this storage location or by downloading or uploading the files to the compute file system.

The component source code must serialize the output object, which is usually stored in memory, into files. For example, you could serialize a pandas dataframe into a CSV file. Azure Machine Learning doesn't define any standardized methods for object serialization. You have the flexibility to choose your preferred methods to serialize objects into files. In the downstream component, you can choose how to deserialize and read these files.

## Data type input and output paths

For data asset inputs and outputs, you must specify a path parameter that points to the data location. The following table shows the supported data locations for Azure Machine Learning pipeline inputs and outputs, with `path` parameter examples:

|Location | Input | Output | Example |
|---------|---------|---------|---------|
|A path on your local computer | ✓ | | `./home/<username>/data/my_data` |
|A path on a public http/s server | ✓ | | `https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv` |
|A path on Azure Storage | \* | | `wasbs://<container_name>@<account_name>.blob.core.windows.net/<path>`<br>or<br>`abfss://<file_system>@<account_name>.dfs.core.windows.net/<path>` |
|A path on an Azure Machine Learning datastore | ✓ | ✓ | `azureml://datastores/<data_store_name>/paths/<path>` |
|A path to a data asset |✓ | ✓ | `azureml:my_data:<version>` |

 > [!TIP]
> Using Azure Storage directly isn't recommended for input, because it can need extra identity configuration to read the data. It's better to use Azure Machine Learning datastore paths, which are supported across various pipeline job types.

## Data type input and output modes

For data type inputs and outputs, you can choose from several download, upload, and mount modes to define how the compute target accesses data. The following table shows the supported modes for different types of inputs and outputs.

Type | `upload` | `download` | `ro_mount` | `rw_mount` | `direct` | `eval_download` | `eval_mount` 
------ | ------ | :---: | :---: | :---: | :---: | :---: | :---: | :---:
`uri_folder` input  |   | ✓  |  ✓  |   | ✓  |  | 
`uri_file` input |   | ✓  |  ✓  |   | ✓  |  | 
`mltable` input |   | ✓  |  ✓  |   | ✓  | ✓ | ✓
`uri_folder` output  | ✓  |   |    | ✓  |   |  | 
`uri_file` output | ✓  |   |    | ✓  |   |  | 
`mltable` output | ✓  |   |    | ✓  | ✓  |  | 

We recommend the `ro_mount` or `rw_mount` modes for most cases. For more information, see [Modes](how-to-read-write-data-v2.md#modes). 

## Inputs and outputs in pipeline graphs

On the pipeline job page in Azure Machine Learning studio, component inputs and outputs appear as small circles called input/output ports. These ports represent the data flow in the pipeline. Pipeline level output is displayed in purple boxes for easy identification.

The following screenshot from the [NYC Taxi Data Regression](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/pipelines-with-components/nyc_taxi_data_regression) pipeline graph shows many component and pipeline inputs and outputs.

:::image type="content" source="./media/how-to-manage-pipeline-input-output/input-output-port.png" lightbox="./media/how-to-manage-pipeline-input-output/input-output-port.png" alt-text="Screenshot highlighting the pipeline input and output ports.":::

When you hover over an input/output port, the type is displayed.

:::image type="content" source="./media/how-to-manage-pipeline-input-output/hover-port.png" alt-text="Screenshot that highlights the port type when hovering over the port.":::

The pipeline graph doesn't display primitive type inputs. These inputs appear on the **Settings** tab of the pipeline **Job overview** panel for pipeline level inputs, or the component panel for component level inputs. To open the component panel, double-click the component in the graph.

:::image type="content" source="./media/how-to-manage-pipeline-input-output/job-overview-setting.png" lightbox="./media/how-to-manage-pipeline-input-output/job-overview-setting.png" alt-text="Screenshot highlighting the job overview setting panel.":::

When you edit a pipeline in the studio Designer, pipeline inputs and outputs are in the **Pipeline interface** panel, and component inputs and outputs are in the component panel.

:::image type="content" source="./media/how-to-manage-pipeline-input-output/pipeline-interface.png" alt-text="Screenshot highlighting the pipeline interface in Designer.":::

## Promote component inputs/outputs to pipeline level

Promoting a component's input/output to the pipeline level lets you overwrite the component's input/output when you submit a pipeline job. This ability is especially useful for triggering pipelines by using REST endpoints.

The following examples show how to promote component level inputs/outputs to pipeline level inputs/outputs.

# [Azure CLI](#tab/cli)

The following pipeline promotes three inputs and three outputs to the pipeline level. For example, `pipeline_job_training_max_epocs` is pipeline level input because it's declared under the `inputs` section on the root level.

Under `train_job` in the `jobs` section, the input named `max_epocs` is referenced as `${{parent.inputs.pipeline_job_training_max_epocs}}`, meaning that the `train_job`'s `max_epocs` input references the pipeline level `pipeline_job_training_max_epocs` input. Pipeline output is promoted by using the same schema.

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

# set subscription, resource group, and workspace name:
subscription_id = "<SUBSCRIPTION_ID>"
resource_group = "<RESOURCE_GROUP>"
workspace = "<AML_WORKSPACE_NAME>"

# connect to the AzureML workspace
ml_client = MLClient(
    DefaultAzureCredential(), subscription_id, resource_group, workspace
)

# define the directory that stores the input data 
parent_dir = ""

# load components
prepare_data = load_component(source=parent_dir + "./prep.yml")
transform_data = load_component(source=parent_dir + "./transform.yml")
train_model = load_component(source=parent_dir + "./train.yml")
predict_result = load_component(source=parent_dir + "./predict.yml")
score_data = load_component(source=parent_dir + "./score.yml")

# construct pipeline
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
# define pipeline job
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

# [Studio UI](#tab/ui)

You can promote a component's input to pipeline level input on the studio Designer authoring page.

1. Open the component's settings panel by double-clicking the component.
1. Select **...** next to the input you want to promote.
1. Select **Add to pipeline input**.

   :::image type="content" source="./media/how-to-manage-pipeline-input-output/promote-pipeline-input.png" alt-text="Screenshot highlighting how to promote to pipeline input in Designer.":::

---

## Define optional inputs

By default, all inputs are required and must either have a default value or be assigned a value each time you submit a pipeline job. However, you can define an optional input.

> [!NOTE]
> Optional outputs aren't supported.

Setting optional inputs can be useful in two scenarios:

- If you define an optional data/model type input and don't assign a value to it when you submit the pipeline job, the pipeline component lacks that data dependency. If the component's input port isn't linked to any component or data/model node, the pipeline invokes the component directly instead of waiting for a preceding dependency.

- If you set `continue_on_step_failure = True` for the pipeline but `node2` uses required input from `node1`, `node2` doesn't execute if `node1` fails. If `node1` input is optional, `node2` executes even if `node1` fails. The following graph demonstrates this scenario.

  :::image type="content" source="./media/how-to-manage-pipeline-input-output/continue-on-failure-optional-input.png" alt-text="Screenshot showing the orchestration logic of optional input and continue on failure.":::

# [Azure CLI / Python SDK](#tab/cli+python)

The following code example shows how to define optional input. When the input is set as `optional = true`, you must use `$[[]]` to embrace the command line inputs, as in the highlighted lines of the example.

:::code language="yaml" source="~/azureml-examples-main/cli/assets/component/train.yml" range="1-34" highlight="11-21,30-32":::

# [Studio UI](#tab/ui)

In a pipeline graph, dotted circles represent optional inputs of data or model types. Optional inputs of primitive types are in the **Settings** tab. Unlike required inputs, optional inputs don't have an asterisk next to them, indicating that they aren't mandatory.

:::image type="content" source="./media/how-to-manage-pipeline-input-output/optional-input.png" lightbox="./media/how-to-manage-pipeline-input-output/optional-input.png" alt-text="Screenshot highlighting the optional input.":::

---

## Customize output paths

By default, component output is stored in the `{default_datastore}` you set for the pipeline, `azureml://datastores/${{default_datastore}}/paths/${{name}}/${{output_name}}`. If not set, the default is the workspace blob storage.

Job `{name}` is resolved at job execution time, and `{output_name}` is the name you defined in the component YAML. You can customize where to store the output by defining an output path.

# [Azure CLI](#tab/cli)

The [pipeline.yml](https://github.com/Azure/azureml-examples/blob/main/cli/jobs/pipelines-with-components/basics/1b_e2e_registered_components/pipeline.yml) file at [train-score-eval pipeline with registered components example](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/pipelines-with-components/basics/1b_e2e_registered_components) defines a pipeline that has three pipeline level outputs. Use the following command to set custom output paths for the `pipeline_job_trained_model` output:

```azurecli
# define the custom output path using datastore uri
# add relative path to your blob container after "azureml://datastores/<datastore_name>/paths"
output_path="azureml://datastores/{datastore_name}/paths/{relative_path_of_container}"  

# create job and define path using --outputs.<outputname>
az ml job create -f ./pipeline.yml --set outputs.pipeline_job_trained_model.path=$output_path  
```

# [Python SDK](#tab/python)

The following code demonstrates how to customize output paths and is from the [Build pipeline with command_component decorated python function](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/pipelines/1b_pipeline_with_python_function_components/pipeline_with_python_function_components.ipynb) notebook:

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

# [Studio UI](#tab/ui)

In the Designer **Pipeline interface** for a pipeline, or the component panel for a component, expand **Outputs** in the **Settings** tab to specify a custom **Path**.

:::image type="content" source="./media/how-to-manage-pipeline-input-output/custom-output.png" lightbox="./media/how-to-manage-pipeline-input-output/custom-output.png" alt-text="Screenshot showing custom output.":::

---

## Download outputs

You can download outputs at the pipeline or component level.

### Download pipeline level outputs

# [Azure CLI](#tab/cli)

You can download all the outputs of a job or download a specific output.

```azurecli
# Download all the outputs of the job
az ml job download --all -n <JOB_NAME> -g <RESOURCE_GROUP_NAME> -w <WORKSPACE_NAME> --subscription <SUBSCRIPTION_ID>

# Download a specific output
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

Download all the outputs of a job or download a specific output.

```python
# Download all the outputs of the job
output = client.jobs.download(name=job.name, download_path=tmp_path, all=True)

# Download specific output
output = client.jobs.download(name=job.name, download_path=tmp_path, output_name=output_port_name)
```

# [Studio UI](#tab/ui)

On the **Outputs + logs** tab of the job details page:

- To download all outputs, select **Download all** in the top menu.
- To download a specific output, select **...** next to a file and select **Download** from the context menu.

:::image type="content" source="./media/how-to-manage-pipeline-input-output/download.png" lightbox="./media/how-to-manage-pipeline-input-output/download.png" alt-text="Screenshot showing how to download an output file or all outputs from a pipeline job.":::

---

### Download component outputs

# [Azure CLI](#tab/cli)

To download the outputs of a child component, first list all child jobs of a pipeline job and then use similar code to download the outputs.

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

To download the outputs of a child component, first list all child jobs of a pipeline job and then use similar code to download the outputs.

```python
# List all child jobs in the job
child_jobs = client.jobs.list(parent_job_name=job.name)

# Traverse and download all the outputs of child job
for child_job in child_jobs:
    client.jobs.download(name=child_job.name, all=True)
```

# [Studio UI](#tab/ui)

On the **Outputs + logs** tab of the component panel for a component, select **Download all**.

:::image type="content" source="./media/how-to-manage-pipeline-input-output/download-component.png" alt-text="Screenshot showing how to download outputs from a pipeline component.":::

---

## Register output as a named asset

You can register output of a component or pipeline as a named asset by assigning a `name` and `version` to the output. The registered asset can be listed in your workspace through the studio UI, CLI, or SDK and can be referenced in future workspace jobs.

### Register pipeline level output

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

yamle = register_pipeline_output()
display_name: register_node_outputter pipeline output
type: pipelinengs.default_compute = "azureml:cpu-cluster"
jobs:ine.outputs.component_out_path.name = 'pipeline_output'
  node:e.outputs.component_out_path.version = '1'
    type: command
    component: ../components/helloworld_component.yml
    inputs:I](#tab/ui)
      component_in_path:
        type: uri_fileb for a pipeline job, select a **Data asset** link under **Inputs** or **Outputs**. On the data asset page, select **Register**.
        path: 'https://dprepdata.blob.core.windows.net/demo/Titanic.csv'
    outputs:e="content" source="./media/how-to-manage-pipeline-input-output/register-output.png" alt-text="Screenshot showing how to register output from a pipeline job.":::
      component_out_path:
        type: uri_folder
        name: 'node_output'  # Define name and version to register a child job's output
        version: '1'nt output
settings:
  default_compute: azureml:cpu-cluster
```
```yaml
# [Python SDK](#tab/python)_output
type: pipeline
```python
from azure.ai.ml import dsl, Output
    type: command
# Load component functionsts/helloworld_component.yml
components_dir = "./components/"
helloworld_component = load_component(source=f"{components_dir}/helloworld_component.yml")
        type: uri_file
@pipeline()h: 'https://dprepdata.blob.core.windows.net/demo/Titanic.csv'
def register_node_output():
  # Call component obj as function: apply given inputs & parameters to create a node in pipeline
  node = helloworld_component(component_in_path=Input(
    type='uri_file', path='https://dprepdata.blob.core.windows.net/demo/Titanic.csv'))t
        version: '1'
  # Define name and version to register node output
  node.outputs.component_out_path.name = 'node_output'
  node.outputs.component_out_path.version = '1'

pipeline = register_node_output()
pipeline.settings.default_compute = "azureml:cpu-cluster"
```python
from azure.ai.ml import dsl, Output
# [Studio UI](#tab/ui)
# Load component functions
On the **Overview** tab for a component, select a **Data asset** link under **Inputs** or **Outputs**. On the data asset page, select **Register**.
helloworld_component = load_component(source=f"{components_dir}/helloworld_component.yml")
---
@pipeline()
## Related contentoutput():
  # Call component obj as function: apply given inputs & parameters to create a node in pipeline
- [YAML reference for pipeline job](./reference-yaml-job-pipeline.md)
- [How to debug pipeline failure](./how-to-debug-pipeline-failure.md)mo/Titanic.csv'))
- [Schedule a pipeline job](./how-to-schedule-pipeline-job.md)
- [Deploy a pipeline with batch endpoints (preview)](./how-to-use-batch-pipeline-deployments.md)
  node.outputs.component_out_path.name = 'node_output'
  node.outputs.component_out_path.version = '1'

pipeline = register_node_output()
pipeline.settings.default_compute = "azureml:cpu-cluster"
```

# [Studio UI](#tab/ui)

On the **Overview** tab for a component, select a **Data asset** link under **Inputs** or **Outputs**. On the data asset page, select **Register**.

---

## Related content

- [YAML reference for pipeline job](./reference-yaml-job-pipeline.md)
- [How to debug pipeline failure](./how-to-debug-pipeline-failure.md)
- [Schedule a pipeline job](./how-to-schedule-pipeline-job.md)
- [Deploy a pipeline with batch endpoints (preview)](./how-to-use-batch-pipeline-deployments.md)
