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

- An Azure subscription. If you don't have one, create a free account before you begin. Try the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

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

In the `cli/jobs/pipelines-with-components/basics` directory of the [`azureml-examples` repository](https://github.com/Azure/azureml-examples), go to the `3b_pipeline_with_data` subdirectory. There are three types of files in this directory. These are the files that you need to create when you build your own pipeline.

- **pipeline.yml**. This YAML file defines the machine learning pipeline. It describes how to break a full machine learning task into a multistep workflow. For example, consider the simple machine learning task of using historical data to train a sales forecasting model. You might want to build a sequential workflow that contains data processing, model training, and model evaluation steps. Each step is a component that has a well-defined interface and can be developed, tested, and optimized independently. The pipeline YAML also defines how the child steps connect to other steps in the pipeline. For example, the model training step generates a model file and the model file is passed to a model evaluation step.

- **component.yml**. These YAML files define the components. They contain the following information:
  - Metadata: Name, display name, version, description, type, and so on. The metadata helps to describe and manage the component.
  - Interface: Inputs and outputs. For example, a model training component takes training data and number of epochs as input and generates a trained model file as output. After the interface is defined, different teams can develop and test the component independently.
  - Command, code, and environment: The command, code, and environment to run the component. The command is the shell command to run the component. The code usually refers to a source code directory. The environment can be an Azure Machine Learning environment (curated or customer created), Docker image, or conda environment.  

- **component_src**. These are the source code directories for specific components. They contain the source code that's run in the component. You can use your preferred language, including Python, R, and others. The code must be run by a shell command. The source code can take a few inputs from the shell command line to control how this step is run. For example, a training step might take training data, learning rate, and the number of epochs to control the training process. The argument of a shell command is used to pass inputs and outputs to the code.

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

Go to the `services.Studio.endpoint` URL to see a visualization of the pipeline:

:::image type="content" source="./media/how-to-create-component-pipelines-cli/pipeline-graph-dependencies.png" alt-text="Screenshot of a visualization of the pipeline.":::

## Understand the pipeline definition YAML

You'll now look at the pipeline definition in the *3b_pipeline_with_data/pipeline.yml* file.  

> [!NOTE]
> To use [serverless compute](how-to-use-serverless-compute.md), replace `default_compute: azureml:cpu-cluster` with `default_compute: azureml:serverless` in this file.

:::code language="yaml" source="~/azureml-examples-main/cli/jobs/pipelines-with-components/basics/3b_pipeline_with_data/pipeline.yml":::

The following table describes the most commonly used fields of the pipeline YAML schema. To learn more, see the [full pipeline YAML schema](reference-yaml-job-pipeline.md).  

|Key|Description|
|------|------|
|`type`|**Required**. The job type. It must be `pipeline` for pipeline jobs.|
|`display_name`|The display name of the pipeline job in the studio UI. Editable in the studio UI. It doesn't have to be unique across all jobs in the workspace.|
|`jobs`|**Required**. A dictionary of the set of individual jobs to run as steps within the pipeline. These jobs are considered child jobs of the parent pipeline job. In the current release, supported job types in pipeline are `command` and `sweep`.|
|`inputs`|A dictionary of inputs to the pipeline job. The key is a name for the input within the context of the job, and the value is the input value. You can reference these pipeline inputs by the inputs of an individual step job in the pipeline by using the `${{ parent.inputs.<input_name> }}` expression.|
|`outputs`|A dictionary of output configurations of the pipeline job. The key is a name for the output in the context of the job, and the value is the output configuration. You can reference these pipeline outputs by the outputs of an individual step job in the pipeline by using the `${{ parents.outputs.<output_name> }}` expression. |

The *3b_pipeline_with_data* example contains a three-step pipeline.

- The three steps are defined under `jobs`. All three steps are of type `command`. Each step's definition is in a corresponding `component*.yml` file. You can see the component YAML files in the *3b_pipeline_with_data* directory. `componentA.yml` is described in the next section.
- This pipeline has data dependency, which is common in real-world pipelines. Component A takes data input from a local folder under `./data` (lines 18-21) and passes its output to component B (line 29). Component A's output can be referenced as `${{parent.jobs.component_a.outputs.component_a_output}}`.
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

In the example in *3b_pipeline_with_data/componentA.yml*, component A has one data input and one data output, which can be connected to other steps in the parent pipeline. All the files in the `code` section in the component YAML will be uploaded to Azure Machine Learning when the pipeline job is submitted. In this example, files under `./componentA_src` will be uploaded. (Line 16 in *componentA.yml*.) You can see the uploaded source code in the studio UI: double-click the **componentA** step in the graph and go to the **Code** tab, as shown in the following screenshot. You can see that it's a hello-world script doing some simple printing, and that it writes the current date and time to the `componentA_output` path. The component takes input and provides output via the command line. It's handled in *hello.py* via `argparse`.
  
:::image type="content" source="./media/how-to-create-component-pipelines-cli/component-snapshot.png" alt-text="Screenshot of the pipeline with data example. It shows component A." lightbox="./media/how-to-create-component-pipelines-cli/component-snapshot.png":::

### Input and output

Input and output define the interface of a component. Input and output can be literal values (of type `string`, `number`, `integer`, or `boolean`) or an object that contains an input schema.

**Object input** (of type `uri_file`, `uri_folder`, `mltable`, `mlflow_model`, or `custom_model`) can connect to other steps in the parent pipeline job to pass data/models to other steps. In the pipeline graph, the object type input renders as a connection dot.

**Literal value inputs** (`string`, `number`, `integer`, `boolean`) are the parameters you can pass to the component at runtime. You can add a default value of literal inputs in the `default` field. For `number` and `integer` types, you can also add minimum and maximum values by using the `min` and `max` fields. If the input value is less than the minimum or more than the maximum, the pipeline fails at validation. Validation occurs before you submit a pipeline job, which can save time. Validation works for the CLI, the Python SDK, and the Designer UI. The following screenshot shows a validation example in the Designer UI. Similarly, you can define allowed values in `enum` fields.

:::image type="content" source="./media/how-to-create-component-pipelines-cli/component-input-output.png" alt-text="Screenshot of the input and output of the train linear regression model component." lightbox= "./media/how-to-create-component-pipelines-cli/component-input-output.png":::

If you want to add an input to a component, you need to make edits in three places:

- The `inputs` field in the component YAML.
- The `command` field in the component YAML.
- In component source code to handle the command-line input. 

These locations are marked with green boxes in the preceding screenshot.  

To learn more about inputs and outputs, see [Manage inputs and outputs for components and pipelines](./how-to-manage-inputs-outputs-pipeline.md).

### Environments

The environment is the environment in which the component runs. It could be an Azure Machine Learning environment (curated or custom registered), a Docker image, or a conda environment. See the following examples:

- [Registered Azure Machine Learning environment asset](https://github.com/Azure/azureml-examples/tree/sdk-preview/cli/jobs/pipelines-with-components/basics/5b_env_registered). The environment is referenced in the component with `azureml:<environment-name>:<environment-version>` syntax.
- [Public docker image](https://github.com/Azure/azureml-examples/tree/sdk-preview/cli/jobs/pipelines-with-components/basics/5a_env_public_docker_image).
- [Conda file](https://github.com/Azure/azureml-examples/tree/sdk-preview/cli/jobs/pipelines-with-components/basics/5c_env_conda_file). The conda file needs to be used together with a base image.

## Register a component for reuse and sharing

Although some components are specific to a particular pipeline, the real benefit of components comes from reuse and sharing. You can register a component in your Machine Learning workspace to make it available for reuse. Registered components support automatic versioning so you can update the component but ensure that pipelines that require an older version will continue to work.  

In the azureml-examples repository, go to the `cli/jobs/pipelines-with-components/basics/1b_e2e_registered_components` directory. 

To register a component, use the `az ml component create` command:

```azurecli
az ml component create --file train.yml
az ml component create --file score.yml
az ml component create --file eval.yml
```

After these commands run to completion, you can see the components in studio, under **Assets** > **Components**:

:::image type="content" source="./media/how-to-create-component-pipelines-cli/registered-components.png" alt-text="Screenshot of studio. It shows the registered components." lightbox ="./media/how-to-create-component-pipelines-cli/registered-components.png":::

Select a component. You see detailed information for each version of the component.

The **Details** tab shows basic information like the component name, who created it, and the version. There are editable fields for **Tags** and **Description**. You can use tags to add search keywords. The description field supports Markdown formatting. You should use it to describe your component's functionality and basic use.

On the **Jobs** tab, you see the history of all jobs that use the component.

### Use registered components in a pipeline job YAML file

You'll now use `1b_e2e_registered_components` as an example of how to use registered component in pipeline YAML. Go to the `1b_e2e_registered_components` directory and open the `pipeline.yml` file. The keys and values in the `inputs` and `outputs` fields are similar to those already discussed. The only significant difference is the value of the `component` field in the `jobs.<job_name>.component` entries. The `component` value is in the form `azureml:<component_name>:<component_version>`. The `train-job` definition, for example, specifies that the latest version of the registered component `my_train` should be used:

:::code language="yaml" source="~/azureml-examples-main/cli/jobs/pipelines-with-components/basics/1b_e2e_registered_components/pipeline.yml" range="24-36" highlight="2":::

### Manage components

You can check component details and manage components by using CLI v2. Use `az ml component -h` to get detailed instructions on component commands. The following table lists all available commands. See more examples in [Azure CLI reference](/cli/azure/ml/component?view=azure-cli-latest&preserve-view=true).

|Command|Description|
|------|------|
|`az ml component create`|Create a component.|
|`az ml component list`|List the components in a workspace.|
|`az ml component show`|Show a component's details.|
|`az ml component update`|Update a component. Only a few fields (description,  display_name) support update.|
|`az ml component archive`|Archive a component container.|
|`az ml component restore`|Restore an archived component.|

## Next step

- Try the [CLI v2 component example](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/pipelines-with-components)
