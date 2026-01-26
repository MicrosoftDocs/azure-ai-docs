---
title: 'Create and run machine learning pipelines using components with the Machine Learning SDK v2'
titleSuffix: Azure Machine Learning
description: Build a machine learning pipeline for image classification. Focus on machine learning instead of infrastructure and automation.
ms.service: azure-machine-learning
ms.subservice: mlops
ms.topic: how-to
author: lgayhardt
ms.author: scottpolly
ms.reviewer: jturuk
ms.date: 01/09/2026
ms.custom:
  - devx-track-python
  - sdkv2
  - build-2023
  - ignite-2023
  - update-code

#customer intent: As a machine learning engineer, I want to create a component-based machine learning pipeline so that I can take advantage of the flexibility and reuse provided by components.
---

# Create and run machine learning pipelines by using components with the Azure Machine Learning SDK v2

[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

In this article, you learn how to build an [Azure Machine Learning pipeline](concept-ml-pipelines.md) to complete an image classification task. This example uses the Azure Machine Learning Python SDK v2. Machine Learning pipelines optimize your workflow with speed, portability, and reuse, so you can focus on machine learning instead of infrastructure and automation.  

The pipeline contains three steps: prepare data, train an image classification model, and score the model. The example pipeline trains a small [Keras](https://keras.io/) convolutional neural network to classify images in the [Fashion MNIST](https://github.com/zalandoresearch/fashion-mnist) dataset. The pipeline looks like this:

:::image type="content" source="./media/how-to-create-component-pipeline-python/pipeline-graph.png" alt-text="Screenshot showing a pipeline graph of the image classification example." lightbox ="./media/how-to-create-component-pipeline-python/pipeline-graph.png":::

In this article, you complete the following tasks:

> [!div class="checklist"]
> - Prepare input data for the pipeline job
> - Create three components to prepare data, train a model, and score the model
> - Build a pipeline from the components
> - Get access to a workspace that has compute
> - Submit the pipeline job
> - Review the output of the components and the trained neural network
> - (Optional) Register the component for further reuse and sharing in the workspace

If you don't have an Azure subscription, create a free account before you begin. Try the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) today.

## Prerequisites

- An Azure Machine Learning workspace. If you don't have one, complete the [Create resources tutorial](quickstart-create-resources.md).
- A Python environment with Azure Machine Learning Python SDK v2 installed. For installation instructions, see [Getting started](https://github.com/Azure/azureml-examples/tree/sdk-preview/sdk#getting-started). This environment is for defining and controlling your Azure Machine Learning resources. It's separate from the environment used at runtime for training.
- A clone of the examples repository.

To run the training examples, first clone the examples repository and navigate to the `sdk` directory:

```bash
git clone --depth 1 https://github.com/Azure/azureml-examples
cd azureml-examples/sdk
```

## Start an interactive Python session

This article uses the Azure Machine Learning Python SDK to create and control an Azure Machine Learning pipeline. The article assumes you're running the code snippets interactively in either a Python REPL environment or a Jupyter notebook.

This article is based on the [image_classification_keras_minist_convnet.ipynb](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/pipelines/2e_image_classification_keras_minist_convnet/image_classification_keras_minist_convnet.ipynb) notebook in the `sdk/python/jobs/pipelines/2e_image_classification_keras_minist_convnet` directory of the [Azure Machine Learning examples](https://github.com/azure/azureml-examples) repository.

## Import required libraries

Import all the Azure Machine Learning libraries that you need for this article:

[!notebook-python[] (~/azureml-examples-main/sdk/python/jobs/pipelines/2e_image_classification_keras_minist_convnet/image_classification_keras_minist_convnet.ipynb?name=required-library)]

## Prepare input data for your pipeline job

You need to prepare the input data for the image classification pipeline.

Fashion MNIST is a dataset of fashion images divided into 10 classes. Each image is a 28 x 28 grayscale image. There are 60,000 training images and 10,000 test images.

[!notebook-python[] (~/azureml-examples-main/sdk/python/jobs/pipelines/2e_image_classification_keras_minist_convnet/image_classification_keras_minist_convnet.ipynb?name=define-input)]

By defining an `Input`, you create a reference to the data source location. The data remains in its existing location, so no extra storage cost is incurred.

## Create components for building the pipeline

The image classification task can be split into three steps: *prepare data*, *train the model*, and *score the model*.

An [Azure Machine Learning component](concept-component.md) is a self-contained piece of code that completes one step in a machine learning pipeline. In this article, you create three components for the image classification task:

- Prepare data for training and testing
- Train a neural network for image classification using training data
- Score the model using test data

For each component, you complete these steps:

1. Prepare the Python script that contains the execution logic.
1. Define the interface of the component.
1. Add other metadata of the component, including the runtime environment and the command to run the component.

The next sections show how to create the components in two ways. For the first two components, you use a Python function. For the third component, you use YAML definition.

### Create the data preparation component

The first component in this pipeline converts the compressed data files of `fashion_ds` into two .csv files, one for training and the other for scoring. You use a Python function to define this component.

If you're following along with the example in the [Azure Machine Learning examples repo](https://github.com/Azure/azureml-examples/tree/main/sdk/python/jobs/pipelines/2e_image_classification_keras_minist_convnet), the source files are already available in the `prep` folder. This folder contains two files to construct the component: `prep_component.py`, which defines the component, and `conda.yaml`, which defines the runtime environment of the component.

#### Define component using a Python function

In this section, you prepare all source files for the `Prep Data` component.

Using the `command_component()` function as a decorator, you can define the component's interface, its metadata, and the code to run from a Python function. Each decorated Python function is transformed into a single static specification (YAML) that the pipeline service can process.

:::code language="python" source="~/azureml-examples-main/sdk/python/jobs/pipelines/2e_image_classification_keras_minist_convnet/prep/prep_component.py":::

The preceding code defines a component with display name `Prep Data` using the `@command_component` decorator:

- `name` is the unique identifier of the component
- `version` is the current version of the component; a component can have multiple versions
- `display_name` is a friendly display name of the component for the UI
- `description` describes the task the component can complete
- `environment` specifies the runtime environment for the component using a `conda.yaml` file

The `conda.yaml` file contains all packages used for the component:

:::code language="python" source="~/azureml-examples-v2samplesreorg/sdk/python/jobs/pipelines/2e_image_classification_keras_minist_convnet/prep/conda.yaml":::

- The `prepare_data_component` function defines one input for `input_data` and two outputs for `training_data` and `test_data`

  - `input_data` is the input data path
  - `training_data` and `test_data` are output data paths for training data and test data

- The component converts the data from `input_data` into a `training_data` .csv file for training data and a `test_data` .csv file for test data

In the studio UI, a component appears as:

- A block in a pipeline graph
- `input_data`, `training_data`, and `test_data` are ports of the component, which connect to other components for data streaming

:::image type="content" source="./media/how-to-create-component-pipeline-python/prep-data-component.png" alt-text="Screenshot of the Prep Data component in the UI and code." lightbox ="./media/how-to-create-component-pipeline-python/prep-data-component.png":::

### Create the model training component

In this section, you create a component for training the image classification model using a Python function, as you did with the `Prep Data` component.

Because the training logic is more complex, put the training code in a separate Python file.

The source files for this component are in the `train` folder in the [Azure Machine Learning examples repo](https://github.com/Azure/azureml-examples/tree/main/sdk/python/jobs/pipelines/2e_image_classification_keras_minist_convnet). This folder contains three files to construct the component:

- `train.py` contains the logic to train the model
- `train_component.py` defines the interface of the component and imports the function from `train.py`
- `conda.yaml` defines the runtime environment of the component

#### Get a script that contains the logic

In this section, you prepare all the source files for the `Train Image Classification Keras` component.

The `train.py` file contains a normal Python function that performs the logic for training a Keras neural network for image classification. To view the code, see the [train.py file on GitHub](https://github.com/Azure/azureml-examples/tree/main/sdk/python/jobs/pipelines/2e_image_classification_keras_minist_convnet/train/train.py).

#### Define the component using a Python function

After you define the training function, you can use `@command_component` in the Azure Machine Learning SDK v2 to wrap your function as a component for use in Azure Machine Learning pipelines:

:::code language="python" source="~/azureml-examples-main/sdk/python/jobs/pipelines/2e_image_classification_keras_minist_convnet/train/train_component.py":::

The preceding code defines a component with display name `Train Image Classification Keras` using `@command_component`.

The `keras_train_component` function defines:

- One input, `input_data`, for source training data
- One input, `epochs`, which specifies the number of epochs to use during training
- One output, `output_model`, which specifies the output path for the model file

The default value of `epochs` is 10. The logic of this component comes from the `train()` function in [train.py](https://github.com/Azure/azureml-examples/tree/main/sdk/python/jobs/pipelines/2e_image_classification_keras_minist_convnet/train/train.py).

The train model component has a more complex configuration than the prepare data component. The `conda.yaml` looks like this:

:::code language="yaml" source="~/azureml-examples-main/sdk/python/jobs/pipelines/2e_image_classification_keras_minist_convnet/train/conda.yaml":::

### Create the model scoring component

In this section, you create a component to score the trained model using YAML specification and script.

If you're following along with the example in the [Azure Machine Learning examples repo](https://github.com/Azure/azureml-examples/tree/main/sdk/python/jobs/pipelines/2e_image_classification_keras_minist_convnet), the source files are already available in the `score` folder. This folder contains three files to construct the component:

- `score.py` contains the source code of the component
- `score.yaml` defines the interface and other details of the component
- `conda.yaml` defines the runtime environment of the component

#### Get a script that contains the logic

The `score.py` file contains a normal Python function that performs the model scoring logic:

:::code language="python" source="~/azureml-examples-main/sdk/python/jobs/pipelines/2e_image_classification_keras_minist_convnet/score/score.py":::

The code in `score.py` takes three command-line arguments: `input_data`, `input_model`, and `output_result`. The program scores the input model using input data and then outputs the result.

#### Define the component using YAML

In this section, you learn how to create a component specification in the valid YAML component specification format. This file specifies the following information:

- Metadata: Name, display name, version, type, and so on
- Interface: Inputs and outputs
- Command, code, and environment: The command, code, and environment used to run the component

:::code language="python" source="~/azureml-examples-main/sdk/python/jobs/pipelines/2e_image_classification_keras_minist_convnet/score/score.yaml":::

- `name` is the unique identifier of the component. Its display name is `Score Image Classification Keras`
- This component has two inputs and one output
- The source code path is defined in the `code` section. When the component runs in the cloud, all files from that path are uploaded as the snapshot of the component
- The `command` section specifies the command to run when the component runs
- The `environment` section contains a Docker image and a conda YAML file. The source file is in the [sample repository](https://github.com/Azure/azureml-examples/blob/v2samplesreorg/sdk/python/jobs/pipelines/2e_image_classification_keras_minist_convnet/score/conda.yaml)

You now have all the source files for the model scoring component.

## Load the components to build a pipeline

You can import the data preparation component and the model training component, which are defined by Python functions, just like other Python functions. 

The following code imports the `prepare_data_component()` and `keras_train_component()` functions from the `prep_component.py` file in the `prep` folder and the `train_component` file in the `train` folder, respectively.

[!notebook-python[] (~/azureml-examples-main/sdk/python/jobs/pipelines/2e_image_classification_keras_minist_convnet/image_classification_keras_minist_convnet.ipynb?name=load-from-dsl-component)]

You can use the `load_component()` function to load the score component. It loads a YAML file that defines the component.

[!notebook-python[] (~/azureml-examples-main/sdk/python/jobs/pipelines/2e_image_classification_keras_minist_convnet/image_classification_keras_minist_convnet.ipynb?name=load-from-yaml)]

### Load registered components from the workspace

> [!NOTE]
> To load registered components from your workspace, first configure your workspace connection as described in the [Get access to your workspace](#get-access-to-your-workspace) section. The `ml_client` object is required for the following operations.

If you have components that are already registered in your workspace, you can load them directly using the `ml_client.components.get()` method. This approach is useful when you want to reuse components that you previously registered or that other team members shared.

```python
# Load a registered component by name and version
registered_component = ml_client.components.get(
    name="my_registered_component", 
    version="1.0.0"
)

# Load the latest version of a registered component
latest_component = ml_client.components.get(
    name="my_registered_component"
)
```

You can list all available components in your workspace to find the ones you need:

```python
# List all components in the workspace
components = ml_client.components.list()
for component in components:
    print(f"Name: {component.name}, Version: {component.version}")
```

After you load them, you can use registered components in your pipeline exactly like components loaded from local files or Python functions.

## Build your pipeline

You created and loaded all the components and input data to build the pipeline. You can now compose them into a pipeline:

> [!NOTE]
> To use [serverless compute](how-to-use-serverless-compute.md), add `from azure.ai.ml.entities import ResourceConfiguration` to the top of the file. Then replace:
>
> - `default_compute=cpu_compute_target` with `default_compute="serverless"`
> - `train_node.compute = gpu_compute_target` with `train_node.resources = ResourceConfiguration(instance_type="Standard_NC6s_v3", instance_count=2)`

[!notebook-python[] (~/azureml-examples-main/sdk/python/jobs/pipelines/2e_image_classification_keras_minist_convnet/image_classification_keras_minist_convnet.ipynb?name=build-pipeline)]

The pipeline has a default compute `cpu_compute_target`. If you don't specify compute for a specific node, that node runs on the default compute.

The pipeline has a pipeline-level input, `pipeline_input_data`. You can assign a value to pipeline input when you submit a pipeline job.

The pipeline contains three nodes: `prepare_data_node`, `train_node`, and `score_node`:

- The `input_data` of `prepare_data_node` uses the value of `pipeline_input_data`
- The `input_data` of `train_node` is the `training_data` output of `prepare_data_node`
- The `input_data` of `score_node` is the `test_data` output of `prepare_data_node`, and the `input_model` is the `output_model` of `train_node`
- Because `train_node` trains a CNN model, you can specify its compute as the `gpu_compute_target` to improve training performance

## Submit your pipeline job

After you construct the pipeline, you can submit the job to your workspace. To submit a job, you first need to connect to a workspace.

### Get access to your workspace

#### Configure credentials

You use `DefaultAzureCredential` to get access to the workspace. `DefaultAzureCredential` should be capable of handling most Azure SDK authentication scenarios.

If `DefaultAzureCredential` doesn't work for you, see [the configure credential example](https://github.com/Azure/MachineLearningNotebooks/blob/master/configuration.ipynb) and [identity Package](/python/api/azure-identity/azure.identity?view=azure-python&preserve-view=true).

[!notebook-python[] (~/azureml-examples-main/sdk/python/jobs/pipelines/2e_image_classification_keras_minist_convnet/image_classification_keras_minist_convnet.ipynb?name=credential)]

#### Get a handle to a workspace that has compute

Create an `MLClient` object to manage Azure Machine Learning services. If you use [serverless compute](how-to-use-serverless-compute.md?view=azureml-api-2&preserve-view=true&tabs=python), you don't need to create these computes.

[!notebook-python[] (~/azureml-examples-main/sdk/python/jobs/pipelines/2e_image_classification_keras_minist_convnet/image_classification_keras_minist_convnet.ipynb?name=workspace)]

> [!IMPORTANT]
> This code snippet expects the workspace configuration JSON file to be saved in the current directory or its parent. For more information on creating a workspace, see [Create workspace resources](quickstart-create-resources.md). For more information on saving the configuration to a file, see [Create a workspace configuration file](how-to-configure-environment.md#local-and-dsvm-only-create-a-workspace-configuration-file).

#### Submit the pipeline job to the workspace

Now that you have a handle to your workspace, you can submit your pipeline job:

[!notebook-python[] (~/azureml-examples-main/sdk/python/jobs/pipelines/2e_image_classification_keras_minist_convnet/image_classification_keras_minist_convnet.ipynb?name=submit-pipeline)]

The preceding code submits this image classification pipeline job to an experiment called `pipeline_samples`. It automatically creates the experiment if it doesn't exist. `pipeline_input_data` uses `fashion_ds`.

The call to submit the experiment completes quickly and produces output similar to this example:

| Experiment | Name | Type | Status | Details page |
| --- | ---- | ----------- | -------------- | ------------- |
| `pipeline_samples` | sharp_pipe_4gvqx6h1fb | pipeline | Preparing | Link to Azure Machine Learning studio |

You can monitor the pipeline run by selecting the link. Or you can wait for it to complete by running this code:

[!notebook-python[] (~/azureml-examples-main/sdk/python/jobs/pipelines/2e_image_classification_keras_minist_convnet/image_classification_keras_minist_convnet.ipynb?name=stream-pipeline)]

> [!IMPORTANT]
> The first pipeline run takes about 15 minutes. All dependencies are downloaded, a Docker image is created, and the Python environment is provisioned and created. Running the pipeline again takes less time because those resources are reused instead of created. However, total runtime for the pipeline depends on the workload of your scripts and the processes that run in each pipeline step.

### Check outputs and debug your pipeline in the UI

You can select the `Link to Azure Machine Learning studio`, which is the job detail page of your pipeline. You see the pipeline graph:

:::image type="content" source="./media/how-to-create-component-pipeline-python/pipeline-ui.png" alt-text="Screenshot of the pipeline job detail page." lightbox ="./media/how-to-create-component-pipeline-python/pipeline-ui.png":::

You can check the logs and outputs of each component by right-clicking the component, or select the component to open its detail pane. To learn more about how to debug your pipeline in the UI, see [Use Azure Machine Learning studio to debug pipeline failures](how-to-debug-pipeline-failure.md).

## (Optional) Register components to the workspace

In the previous sections, you built a pipeline using three components to complete an image classification task. You can also register components to your workspace so they can be shared and reused in the workspace. The following example shows how to register the data preparation component:

[!notebook-python[] (~/azureml-examples-main/sdk/python/jobs/pipelines/2e_image_classification_keras_minist_convnet/image_classification_keras_minist_convnet.ipynb?name=register-component)]

You can use `ml_client.components.get()` to get a registered component by name and version. You can use `ml_client.components.create_or_update()` to register a component that was previously loaded from a Python function or YAML.

## Related content

- For more examples of how to build pipelines using the machine learning SDK, see the [example repository](https://github.com/Azure/azureml-examples/tree/main/sdk/python/jobs/pipelines).
- For information about using the studio UI to submit and debug a pipeline, see [Create and run machine learning pipelines using components with the Azure Machine Learning studio](how-to-create-component-pipelines-ui.md).
- For information about using the Azure Machine Learning CLI to create components and pipelines, see [Create and run machine learning pipelines using components with the Azure Machine Learning CLI](how-to-create-component-pipelines-cli.md).
- For information about deploying pipelines into production using batch endpoints, see [How to deploy pipelines with batch endpoints](how-to-use-batch-pipeline-deployments.md).
