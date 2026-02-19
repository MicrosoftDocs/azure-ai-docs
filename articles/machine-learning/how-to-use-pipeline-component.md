---
title: How to use pipeline components in pipeline jobs
titleSuffix: Azure Machine Learning
description: Learn how to nest multistep pipeline components in Azure Machine Learning pipeline jobs by using CLI v2, Python SDK v2, or the studio UI.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mlops
ms.topic: how-to
author: lgayhardt
ms.author: scottpolly
ms.reviewer: jturuk
ms.date: 09/13/2024
ms.custom:
  - sdkv2
  - cliv2
  - devx-track-python
  - ignite-2023
---

# Use multistep pipeline components in pipeline jobs

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

It's common to use pipeline components to develop complex machine learning pipelines. You can group multiple steps into a pipeline component that you use as a single step to do tasks like data preprocessing or model training.

This article shows you how to nest multiple steps in components that you use to build complex Azure Machine Learning pipeline jobs. You can develop and test these multistep components standalone, which helps you share your work and collaborate better with team members.

By using multistep pipeline components, you can focus on developing subtasks and easily integrate them with the entire pipeline job. A pipeline component has a well-defined input and output interface, so multistep pipeline component users don't need to know the implementation details of the component.

Both pipeline components and pipeline jobs contain groups of steps or components, but defining a pipeline component differs from defining a pipeline job in the following ways:

- Pipeline components define only the interfaces of inputs and outputs. In a pipeline component, you explicitly set the input and output types, but you don't directly assign values to them.
- Pipeline components don't have runtime settings, so you can't hardcode a compute or data node in a pipeline component. Instead you must promote these nodes as pipeline level inputs and assign values during runtime.
- Pipeline level settings such as `default_datastore` and `default_compute` are also runtime settings that aren't part of pipeline component definitions.

## Prerequisites

- Have an Azure Machine Learning workspace. For more information, see [Create workspace resources](quickstart-create-resources.md).
- Understand the concepts of Azure Machine Learning [pipelines](concept-ml-pipelines.md) and [components](concept-component.md), and know how to use components in Azure Machine Learning pipelines.

# [Azure CLI](#tab/cliv2)

- Install the Azure CLI and the `ml` extension. For more information, see [Install, set up, and use the CLI (v2)](how-to-configure-cli.md). The `ml` extension automatically installs the first time you run an `az ml` command.
- Understand how to [create and run Azure Machine Learning pipelines and components with the CLI v2](how-to-create-component-pipelines-cli.md).

# [Python SDK](#tab/python)

- Install the [Azure Machine Learning SDK v2 for Python](/python/api/overview/azure/ai-ml-readme).
- Understand how to [create and run Azure Machine Learning pipelines and components with the Python SDK v2](how-to-create-component-pipeline-python.md).

# [Studio UI](#tab/ui)

- Understand how to [create and run pipelines and components with the Azure Machine Learning studio UI](how-to-create-component-pipelines-ui.md).

---

## Build pipeline jobs with pipeline components

You can define multiple steps as a pipeline component, and then use the multistep component like any other component to build a pipeline job.

### Define pipeline components

# [Azure CLI](#tab/cliv2)

You can use multiple components to build a pipeline component, similar to how you build pipeline jobs with components.

The following example comes from the [pipeline_with_train_eval_pipeline_component](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/pipelines-with-components/pipeline_with_pipeline_component/pipeline_with_train_eval_pipeline_component) example pipeline in the [Azure Machine Learning examples](https://github.com/Azure/azureml-examples) GitHub repository.

The example component defines a three-node pipeline job. The two nodes in the example pipeline job each use the locally defined components `train`, `score`, and `eval`. The following code defines the pipeline component:

:::code language="yaml" source="~/azureml-examples-main/cli/jobs/pipelines-with-components/pipeline_with_pipeline_component/pipeline_with_train_eval_pipeline_component/components/train_pipeline_component.yml" highlight="8,20,23,30,43,53":::

# [Python SDK](#tab/python)

You can define a pipeline component using a Python function, which is similar to defining a pipeline job using a function. You can also promote the compute of some steps to use as inputs for the pipeline component.

The following Python SDK examples are from the [Build pipeline with subpipeline (pipeline component)](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/pipelines/1j_pipeline_with_pipeline_component/pipeline_with_train_eval_pipeline_component/pipeline_with_train_eval_pipeline_component.ipynb) Azure Machine Learning notebook. Run this notebook to build the example pipeline.

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/pipelines/1j_pipeline_with_pipeline_component/pipeline_with_train_eval_pipeline_component/pipeline_with_train_eval_pipeline_component.ipynb?name=pipeline-component)]

# [Studio UI](#tab/ui)

To access components in Azure Machine Learning studio, you need to register the components. To register pipeline components, follow the instructions at [Register component in your workspace](how-to-create-component-pipelines-ui.md#register-a-component-in-your-workspace). After that, you can view and use the components in the studio asset library and components list page.

---

### Use components in pipelines

# [Azure CLI](#tab/cliv2)

You reference pipeline components as child jobs in a pipeline job just like you reference other types of components. You can provide runtime settings like `default_datastore` and `default_compute` at the pipeline job level.

You need to promote any parameters you want to change during runtime as pipeline job inputs. Otherwise, they're hard-coded in the pipeline component. Promoting compute definition to a pipeline level input supports heterogeneous pipelines that can use different compute targets in different steps.

To submit the pipeline job, edit the `cpu-cluster` in the `default_compute` section before you run the `az ml job create -f pipeline.yml` command.

:::code language="yaml" source="~/azureml-examples-main/cli/jobs/pipelines-with-components/pipeline_with_pipeline_component/pipeline_with_train_eval_pipeline_component/pipeline.yml" highlight="17,18,27,28,40,50,55":::

>[!NOTE]
>To share or reuse components across jobs in the workspace, you need to register the components. You can use [`az ml component create`](/cli/azure/ml/component#az-ml-component-create) to register pipeline components.

You can find other Azure CLI pipeline component-related examples and information at [pipelines-with-components](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/pipelines-with-components) in the [Azure Machine Learning examples repository](https://github.com/Azure/azureml-examples).

# [Python SDK](#tab/python)

You can use the pipeline component as a step like other components in the pipeline job.

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/pipelines/1j_pipeline_with_pipeline_component/pipeline_with_train_eval_pipeline_component/pipeline_with_train_eval_pipeline_component.ipynb?name=pipeline-component-pipeline-job)]

>[!NOTE]
>To share or reuse components across jobs in the workspace, you need to register the components. You can use [`ml_client.components.create_or_update`](/python/api/azure-ai-ml/azure.ai.ml.mlclient#azure-ai-ml-mlclient-create-or-update) to register pipeline components.

You can find other Python SDK v2 pipeline component-related notebooks and information at [Pipeline component](https://github.com/Azure/azureml-examples/tree/main/sdk/python/jobs/pipelines/1j_pipeline_with_pipeline_component) in the [Azure Machine Learning examples](https://github.com/Azure/azureml-examples) GitHub repository.

# [Studio UI](#tab/ui)

After you register a pipeline component, you can drag and drop the component into the studio Designer canvas and use the UI to build a pipeline job. For detailed instructions, see [Create pipelines using registered components](how-to-create-component-pipelines-ui.md#create-pipeline-by-using-registered-component).

The following screenshots are from the [nyc_taxi_data_regression_with_pipeline_component](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/pipelines/1j_pipeline_with_pipeline_component/nyc_taxi_data_regression_with_pipeline_component/nyc_taxi_data_regression_with_pipeline_component.ipynb) notebook in the [Azure Machine Learning examples](https://github.com/Azure/azureml-examples) GitHub repository.

:::image type="content" source="./media/how-to-use-pipeline-component/pipeline-component-authoring.png" alt-text="Screenshot of the Designer canvas page to build a pipeline job with a pipeline component." lightbox= "./media/how-to-use-pipeline-component/pipeline-component-authoring.png":::

After you submit a pipeline job, you can go to the pipeline job detail page to change pipeline component status. You can also drill down to child components in the pipeline component to debug the components.

:::image type="content" source="./media/how-to-use-pipeline-component/pipeline-component-right-panel.png" alt-text="Screenshot of View pipeline component on the pipeline job detail page." lightbox= "./media/how-to-use-pipeline-component/pipeline-component-right-panel.png":::

---

## Related content

- [YAML reference for pipeline component](reference-yaml-component-pipeline.md)
- [Manage inputs and outputs of components and pipelines](how-to-manage-inputs-outputs-pipeline.md)
- [Deploy your pipeline as batch endpoint](how-to-deploy-pipeline-component-as-batch-endpoint.md)
