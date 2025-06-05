---
title: Create and Run Component-Based ML Pipelines (CLI)
titleSuffix: Azure Machine Learning
description: Create and run machine learning pipelines by using the Azure Machine Learning CLI.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
author: lgayhardt
ms.author: lagayhar
ms.reviewer: zhanxia
ms.date: 06/11/2025
ms.topic: how-to
ms.custom:
  - devplatv2
  - devx-track-azurecli
  - build-2023
  - ignite-2023
ms.devlang: azurecli
# ms.devlang: azurecli, cliv2

#customer intent: As a machine learning engineer, I want to create a component-based machine learning pipeline so that I can take advantage of the flexibility and reuse provided by components.
---

# Create and run machine learning pipelines using components with the Azure Machine Learning CLI

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

In this article, you learn how to create and run [machine learning pipelines](concept-ml-pipelines.md) by using Azure CLI and [components](concept-component.md). You can create pipelines without using components, but components provide flexibility and enable reuse. Azure Machine Learning pipelines can be defined in YAML and run from the CLI, authored in Python, or composed in the Azure Machine Learning studio Designer via a drag-and-drop UI. This article focuses on the CLI.

## Prerequisites

- An Azure subscription. If you don't have one, create a free account before you begin. Try the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/free/).

- An [Azure Machine Learning workspace](quickstart-create-resources.md).

- [The Azure CLI extension for Machine Learning](how-to-configure-cli.md), installed and set up.

- A clone of the examples repository. You can use these commands to clone the repo:

    ```azurecli-interactive
    git clone https://github.com/Azure/azureml-examples --depth 1
    cd azureml-examples/cli/jobs/pipelines-with-components/basics
    ```

### Suggested prereading

- [What are Azure Machine Learning pipelines?](./concept-ml-pipelines.md)
- [What is an Azure Machine Learning component?](./concept-component.md)

## Create your first pipeline with components

First, you'll create a pipeline with components by using an example. Doing so gives you an initial impression of what a pipeline and component look like in Azure Machine Learning.

From the `cli/jobs/pipelines-with-components/basics` directory of the [`azureml-examples` repository](https://github.com/Azure/azureml-examples), go to the `3b_pipeline_with_data` subdirector. There are three types of files in this directory. These are the files that you need to create when you build your own pipeline.

- **pipeline.yml**. This YAML file defines the machine learning pipeline. It describes how to break a full machine learning task into a multistep workflow. For example, consider the simple machine learning task of using historical data to train a sales forecasting model. You might want to build a sequential workflow that contains data processing, model training, and model evaluation steps.  Each step is a component that has a well-defined interface and can be developed, tested, and optimized independently. The pipeline YAML also defines how the child steps connect to other steps in the pipeline. For example, the model training step generates a model file and the model file is passed to a model evaluation step.

- **component.yml**.  This YAML file defines the component. It packages the following information:
  - Metadata: Name, display name, version, description, type, and so on. The metadata helps to describe and manage the component.
  - Interface: Inputs and outputs. For example, a model training component takes training data and number of epochs as input and generates a trained model file as output. After the interface is defined, different teams can develop and test the component independently.
  - Command, code, and environment: The command, code, and environment to run the component. The command is the shell command to run the component. The code usually refers to a source code directory. The environment can be an Azure Machine Learning environment (curated or customer created), Docker image, or conda environment.  

- **component_src**. This is the source code directory for a specific component. It contains the source code that's executed in the component. You can use your preferred language, including Python, R, and others. The code must be run by a shell command. The source code can take a few inputs from the shell command line to control how this step is run. For example, a training step might take training data, learning rate, and the number of epochs to control the training process. The argument of a shell command is used to pass inputs and outputs to the code.

 You'll now create a pipeline by using the `3b_pipeline_with_data` example. Each file is explained further in the following sections.

 First, list your available compute resources by using the following command:

```azurecli
az ml compute list
```

If you don't have it, create a cluster called `cpu-cluster` by running this command:

> [!NOTE]
> Skip this step to use [serverless compute](./how-to-use-serverless-compute.md).

```azurecli
az ml compute create -n cpu-cluster --type amlcompute --min-instances 0 --max-instances 10
```

Now create a pipeline job that's defined in the pipeline.yml file by running the following command. The compute target is referenced in the pipeline.yml file as `azureml:cpu-cluster`. If your compute target uses a different name, remember to update it in the pipeline.yml file.

```azurecli
az ml job create --file pipeline.yml
```

You should receive a JSON dictionary with information about the pipeline job, including:

| Key  | Description           |
|----------------|----------------------------------------|
| `name`                     | The GUID-based name of the job.                   |
| `experiment_name`          | The name under which jobs will be organized in studio.         |
| `services.Studio.endpoint` | A URL for monitoring and reviewing the pipeline job.         |
| `status`             | The status of the job. It will probably be `Preparing` at this point. |

Open the `services.Studio.endpoint` URL to see a visualization of the pipeline:

:::image type="content" source="./media/how-to-create-component-pipelines-cli/pipeline-graph-dependencies.png" alt-text="Screenshot of a visualization of the pipeline.":::

## Understand the pipeline definition YAML

You'll now look at the pipeline definition in the *3b_pipeline_with_data/pipeline.yml* file.  

> [!NOTE]
> To use [serverless compute](how-to-use-serverless-compute.md), replace `default_compute: azureml:cpu-cluster` with `default_compute: azureml:serverless` in this file.

:::code language="yaml" source="~/azureml-examples-main/cli/jobs/pipelines-with-components/basics/3b_pipeline_with_data/pipeline.yml":::

The table describes the most commonly used fields of the pipeline YAML schema. To learn more, see the [full pipeline YAML schema](reference-yaml-job-pipeline.md).  

|Key|Description|
|------|------|
|`type`|**Required**. The job type. It must be `pipeline` for pipeline jobs.|
|`display_name`|The display name of the pipeline job in the studio UI. Editable in the studio UI. It doesn't have to be unique across all jobs in the workspace.|
|`jobs`|**Required**. A dictionary of the set of individual jobs to run as steps within the pipeline. These jobs are considered child jobs of the parent pipeline job. In the current release, supported job types in pipeline are `command` and `sweep`|
|`inputs`|A dictionary of inputs to the pipeline job. The key is a name for the input within the context of the job, and the value is the input value. You can reference these pipeline inputs by the inputs of an individual step job in the pipeline by using the `${{ parent.inputs.<input_name> }}` expression.|
|`outputs`|A dictionary of output configurations of the pipeline job. The key is a name for the output in the context of the job, and the value is the output configuration. You can reference these pipeline outputs by the outputs of an individual step job in the pipeline by using the `${{ parents.outputs.<output_name> }}` expression. |

The *3b_pipeline_with_data* example, contains a three-step pipeline.

- The three steps are defined under `jobs`. All three steps are of type `command`. Each step's definition is in a corresponding `component*.yml` file. You can see the component YAML files in the *3b_pipeline_with_data* directory. `componentA.yml` is described in the next section.
- This pipeline has data dependency, which is common in real-world pipelines. Component A takes data input from a local folder under `./data` (lines 17-20) and passes its output to component B (line 29). Component A's output can be referenced as `${{parent.jobs.component_a.outputs.component_a_output}}`.
- `default_compute` defines the default compute for the pipeline. If a component under `jobs` defines a different compute, component-specific settings are respected.

:::image type="content" source="./media/how-to-create-component-pipelines-cli/pipeline-inputs-and-outputs.png" alt-text="Screenshot of the pipeline with data example." lightbox ="./media/how-to-create-component-pipelines-cli/pipeline-inputs-and-outputs.png":::

### Read and write data in a pipeline

One common scenario is to read and write data in a pipeline. In Azure Machine Learning, you use the same schema to [read and write data](how-to-read-write-data-v2.md) for all types of jobs (pipeline jobs, command jobs, and sweep jobs). Following are examples of using data in pipelines for common scenarios:

- [Local data](https://github.com/Azure/azureml-examples/tree/sdk-preview/cli/jobs/pipelines-with-components/basics/4a_local_data_input)
- [Web file with a public URL](https://github.com/Azure/azureml-examples/blob/sdk-preview/cli/jobs/pipelines-with-components/basics/4c_web_url_input/pipeline.yml)
- [Azure Machine Learning datastore and path](https://github.com/Azure/azureml-examples/tree/sdk-preview/cli/jobs/pipelines-with-components/basics/4b_datastore_datapath_uri)
- [Azure Machine Learning data asset](https://github.com/Azure/azureml-examples/tree/sdk-preview/cli/jobs/pipelines-with-components/basics/4d_data_input)

## Understand the component definition YAML

Here's the *componentA.yml* file, an example of YAML that defines a component:

:::code language="yaml" source="~/azureml-examples-main/cli/jobs/pipelines-with-components/basics/3b_pipeline_with_data/componentA.yml":::

This table defines the most commonly used fields of component YAML. To learn more, see the [full component YAML schema](reference-yaml-component-command.md).

|Key|Description|
|------|------|
|`name`|**Required**. The name of the component. It must be unique across the Azure Machine Learning workspace. It must start with a lowercase letter. Lowercase letters, numbers, and underscores (_) are allowed. Maximum length is 255 characters.|
|`display_name`|The display name of the component in the studio UI. It doesn't have to be unique within the workspace.|
|`command`|**Required**. The command to run.|
|`code`|The local path to the source code directory to be uploaded and used for the component.|
|`environment`|**Required**. The environment that's used to run the component.|
|`inputs`|A dictionary of component inputs. The key is a name for the input within the context of the component, and the value is the component input definition. You can reference inputs in the command by using the `${{ inputs.<input_name> }}` expression.|
|`outputs`|A dictionary of component outputs. The key is a name for the output within the context of the component, and the value is the component output definition. You can reference outputs in the command by using the `${{ outputs.<output_name> }}` expression.|
|`is_deterministic`|Whether to reuse the previous job's result if the component inputs don't change. The default value is `true`. This setting is also known as *reuse by default*. The common scenario when set to `false` is to force reload data from cloud storage or a URL.|

In the example in *3b_pipeline_with_data/componentA.yml*, component A has one data input and one data output. The output can be connected to other steps in the parent pipeline. All the files in the `code` section in the component YAML will be uploaded to Azure Machine Learning when the pipeline job is submitted. In this example, files under `./componentA_src` will be uploaded (line 16 in *componentA.yml*). You can see the uploaded source code in the studio UI: double-click the **componentA** step in the graph and go to the **Snapshot** tab, as shown in the following screenshot. We can see it's a hello-world script just doing some simple printing, and write current datetime to the `componentA_output` path. The component takes input and output through command line argument, and it's handled in the *hello.py* using `argparse`.
  
:::image type="content" source="./media/how-to-create-component-pipelines-cli/component-snapshot.png" alt-text="Screenshot of pipeline with data example showing componentA." lightbox="./media/how-to-create-component-pipelines-cli/component-snapshot.png":::

### Input and output
Input and output define the interface of a component. Input and output could be either of a literal value(of type `string`,`number`,`integer`, or `boolean`) or an object containing input schema.

**Object input** (of type `uri_file`, `uri_folder`,`mltable`,`mlflow_model`,`custom_model`) can connect to other steps in the parent pipeline job and hence pass data/model to other steps. In pipeline graph, the object type input renders as a connection dot.

**Literal value inputs** (`string`,`number`,`integer`,`boolean`) are the parameters you can pass to the component at run time. You can add default value of literal inputs under `default` field. For `number` and `integer` type, you can also add minimum and maximum value of the accepted value using `min` and `max` fields. If the input value exceeds the min and max, pipeline fails at validation. Validation happens before you submit a pipeline job to save your time. Validation works for CLI, Python SDK and designer UI. The following screenshot shows a validation example in designer UI. Similarly, you can define allowed values in `enum` field.

:::image type="content" source="./media/how-to-create-component-pipelines-cli/component-input-output.png" alt-text="Screenshot of the input and output of the train linear regression model component." lightbox= "./media/how-to-create-component-pipelines-cli/component-input-output.png":::

If you want to add an input to a component, remember to edit three places:

- `inputs` field in component YAML
- `command` field in component YAML.
- Component source code to handle the command line input. It's marked in green box in the previous screenshot.  

To learn more about inputs and outputs, see [Manage inputs and outputs of component and pipeline](./how-to-manage-inputs-outputs-pipeline.md).

### Environment

Environment defines the environment to execute the component. It could be an Azure Machine Learning environment(curated or custom registered), docker image or conda environment. See the following examples.

- [Azure Machine Learning registered environment asset](https://github.com/Azure/azureml-examples/tree/sdk-preview/cli/jobs/pipelines-with-components/basics/5b_env_registered). It's referenced in component following `azureml:<environment-name>:<environment-version>` syntax.
- [public docker image](https://github.com/Azure/azureml-examples/tree/sdk-preview/cli/jobs/pipelines-with-components/basics/5a_env_public_docker_image)
- [conda file](https://github.com/Azure/azureml-examples/tree/sdk-preview/cli/jobs/pipelines-with-components/basics/5c_env_conda_file) Conda file needs to be used together with a base image.

## Register component for reuse and sharing

While some components are specific to a particular pipeline, the real benefit of components comes from reuse and sharing. Register a component in your Machine Learning workspace to make it available for reuse. Registered components support automatic versioning so you can update the component but assure that pipelines that require an older version will continue to work.  

In the azureml-examples repository, navigate to the `cli/jobs/pipelines-with-components/basics/1b_e2e_registered_components` directory. 

To register a component, use the `az ml component create` command:

```azurecli
az ml component create --file train.yml
az ml component create --file score.yml
az ml component create --file eval.yml
```

After these commands run to completion, you can see the components in Studio, under Asset -> Components:

:::image type="content" source="./media/how-to-create-component-pipelines-cli/registered-components.png" alt-text="Screenshot of Studio showing the components that were just registered." lightbox ="./media/how-to-create-component-pipelines-cli/registered-components.png":::

Select a component. You see detailed information for each version of the component.

Under **Details** tab, you see basic information of the component like name, created by, version etc. You see editable fields for Tags and Description. The tags can be used for adding rapidly searched keywords. The description field supports Markdown formatting and should be used to describe your component's functionality and basic use.

Under **Jobs** tab, you see the history of all jobs that use this component.

### Use registered components in a pipeline job YAML file

Let's use `1b_e2e_registered_components` to demo how to use registered component in pipeline YAML. Navigate to `1b_e2e_registered_components` directory, open the `pipeline.yml` file. The keys and values in the `inputs` and `outputs` fields are similar to those already discussed. The only significant difference is the value of the `component` field in the `jobs.<JOB_NAME>.component` entries. The `component` value is of the form `azureml:<COMPONENT_NAME>:<COMPONENT_VERSION>`. The `train-job` definition, for instance, specifies the latest version of the registered component `my_train` should be used:

:::code language="yaml" source="~/azureml-examples-main/cli/jobs/pipelines-with-components/basics/1b_e2e_registered_components/pipeline.yml" range="24-36" highlight="4":::

### Manage components

You can check component details and manage the component using CLI (v2). Use `az ml component -h` to get detailed instructions on component command. The following table lists all available commands. See more examples in [Azure CLI reference](/cli/azure/ml/component?view=azure-cli-latest&preserve-view=true).

|commands|description|
|------|------|
|`az ml component create`|Create a component|
|`az ml component list`|List components in a workspace|
|`az ml component show`|Show details of a component|
|`az ml component update`|Update a component. Only a few fields(description, display_name) support update|
|`az ml component archive`|Archive a component container|
|`az ml component restore`|Restore an archived component|

## Next steps

- Try out [CLI v2 component example](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/pipelines-with-components)
