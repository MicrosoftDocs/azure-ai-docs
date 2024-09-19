---
title: How to do hyperparameter sweep in pipelines
titleSuffix: Azure Machine Learning
description: Learn how to use sweep to do hyperparameter tuning in Azure Machine Learning pipeline using CLI v2 and Python SDK.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mlops
ms.topic: how-to
author: lgayhardt
ms.author: lagayhar
ms.reviewer: zhanxia
ms.date: 09/18/2024
ms.custom: devx-track-python, sdkv2, cliv2, update-code2
---

# How to do hyperparameter tuning in pipelines

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

In this article, you learn how to do hyperparameter tuning in Azure Machine Learning pipelines by using Azure Machine Learning CLI v2 or Azure Machine Learning SDK for Python v2.

Hyperparameters are adjustable parameters that let you control the model training process. Hyperparameter tuning is the process of finding the configuration of hyperparameters that results in the best performance. Azure Machine Learning lets you automate hyperparameter tuning and run experiments in parallel to efficiently optimize hyperparameters.

## Prerequisites

- Have an Azure Machine Learning account and workspace.
- Understand [Azure Machine Learning pipelines](concept-ml-pipelines.md) and [hyperparameter tuning a model](how-to-tune-hyperparameters.md).

## Create a pipeline with a hyperparameter sweep step

# [Azure CLI](#tab/cli)

The following Azure CLI examples come from [Run a pipeline job using sweep (hyperdrive) in pipeline](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/pipelines-with-components/pipeline_with_hyperparameter_sweep) in the [Azure Machine Learning examples](https://github.com/Azure/azureml-examples) repository. For more information about creating pipelines with components, see [Create and run machine learning pipelines using components with the Azure Machine Learning CLI](how-to-create-component-pipelines-cli.md).

# [Python SDK](#tab/python)

The following Python SDK examples come from [Build pipeline with sweep node](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/pipelines/1c_pipeline_with_hyperparameter_sweep/pipeline_with_hyperparameter_sweep.ipynb) in the [Azure Machine Learning examples](https://github.com/Azure/azureml-examples) repository. For more information about creating pipelines with components, see [Create and run machine learning pipelines using components with the Azure Machine Learning SDK v2](how-to-create-component-pipeline-python.md).

---

### Create a command component with hyperparameter inputs

The Azure Machine Learning pipeline must have a command component with hyperparameter inputs. The following *train.yml* file defines a `trial` component that has the `c_value`, `kernel`, and `coef` hyperparameter inputs and runs the source code that's located in the *./train-src* folder.

:::code language="yaml" source="~/azureml-examples-main/cli/jobs/pipelines-with-components/pipeline_with_hyperparameter_sweep/train.yml" highlight="11-16,23-25,60":::

### Create the trial component source code

The example source code for this example is a single *train.py* file. This code executes in every trial of the sweep job. The following code shows the trial component source code:

:::code language="python" source="~/azureml-examples-main/cli/jobs/pipelines-with-components/pipeline_with_hyperparameter_sweep/train-src/train.py" highlight="15":::

>[!NOTE]
>Make sure to log the metrics in the trial component source code with exactly the same name as the `primary_metric` value in the pipeline file. This example uses `mlflow.autolog()`, which is the recommended way to track machine learning experiments. For more information about MLflow, see [Track ML experiments and models with MLflow](./how-to-use-mlflow-cli-runs.md).

### Create the pipeline job with hyperparameter sweep step

# [Azure CLI](#tab/cli)

Given the command component defined in *train.yml*, the following code creates a two-step `train` and `predict` pipeline definition file. In the `sweep_step`, the required step type is `sweep`, and the `c_value`, `kernel`, and `coef` hyperparameter inputs for the `trial` component are added to the `search_space`. The following example highlights the hyperparameter tuning `sweep_step`.

:::code language="yaml" source="~/azureml-examples-main/cli/jobs/pipelines-with-components/pipeline_with_hyperparameter_sweep/pipeline.yml" highlight="8-48":::

# [Python SDK](#tab/python)

In the v2 SDK, you can enable hyperparameter tuning for any command component by calling the `.sweep()` method. The following pipeline definition shows how to enable sweep for `train_model`.

The example first loads the `train_component_func` defined in the *train.yml* file. To create the `train_model`, the code adds the `c_value`, `kernel`, and `coef0` hyperparameters into the search space. The `sweep_step` defines the `primary_metric`, `sampling_algorithm`, and other parameters.

[!Notebook-python[] (~/azureml-examples-main/sdk/python/jobs/pipelines/1c_pipeline_with_hyperparameter_sweep/pipeline_with_hyperparameter_sweep.ipynb?name=enable-sweep)]

---

After you submit this pipeline job, Azure Machine Learning runs the `trial` component multiple times to sweep over hyperparameters, based on the search space and limits you defined in the `sweep_step`. For the full sweep job schema, see [CLI (v2) sweep job YAML schema](reference-yaml-job-sweep.md).

## Check a pipeline job with sweep step in studio

After you submit a pipeline job, the SDK or CLI widget gives you a web URL link to the pipeline graph in the Azure Machine Learning studio UI.

To details of the sweep step, double click the sweep step in the pipeline graph, select the **Child jobs** tab in the details panel, and then select the child job.

:::image type="content" source="./media/how-to-use-sweep-in-pipeline/pipeline-view.png" alt-text="Screenshot of the pipeline with child job and the train_model node highlighted." lightbox= "./media/how-to-use-sweep-in-pipeline/pipeline-view.png":::

On the child job page, select the **Trials** tab to see and compare metrics for all the child runs. Select any of the child runs to see the details for that run.

:::image type="content" source="./media/how-to-use-sweep-in-pipeline/sweep-job.png" alt-text="Screenshot of the child job page with the Trials tab." lightbox= "./media/how-to-use-sweep-in-pipeline/sweep-job.png":::

If a child run failed, select the **Outputs + logs** tab on the child run page to see useful debug information.

:::image type="content" source="./media/how-to-use-sweep-in-pipeline/child-run.png" alt-text="Screenshot of the output and logs tab of a child run." lightbox= "./media/how-to-use-sweep-in-pipeline/child-run.png":::

## Other example notebooks

- [Build pipeline with sweep node](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/pipelines/1c_pipeline_with_hyperparameter_sweep/pipeline_with_hyperparameter_sweep.ipynb)
- [Run hyperparameter sweep on a command job](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/single-step/lightgbm/iris/lightgbm-iris-sweep.ipynb)

## Related content

- [Track an experiment](how-to-log-view-metrics.md)
- [Deploy a trained model](how-to-deploy-online-endpoints.md)
