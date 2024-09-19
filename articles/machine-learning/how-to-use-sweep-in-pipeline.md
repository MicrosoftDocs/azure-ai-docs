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

In this article, you learn how to do hyperparameter tuning in Azure Machine Learning pipelines by using Azure Machine Learning CLI v2 or Azure Machine Learning SDK for Python v2, and view results in Azure Machine Learning studio.

Hyperparameters are adjustable parameters that let you control the model training process. Hyperparameter tuning is the process of finding the configuration of hyperparameters that results in the best performance. Azure Machine Learning lets you automate hyperparameter tuning and run experiments in parallel to efficiently optimize hyperparameters.

## Prerequisites

- Understand the concepts of pipelines and hyperparameter tuning. For more information, see [Azure Machine Learning pipelines](concept-ml-pipelines.md) and [Hyperparameter tuning a model](how-to-tune-hyperparameters.md).
- Have an Azure Machine Learning pipeline with a command component that takes hyperparameters as inputs. For more information, see [Create and run machine learning pipelines using components with the Azure Machine Learning CLI](how-to-create-component-pipelines-cli.md) or [Create and run machine learning pipelines using components with the Azure Machine Learning SDK v2](how-to-create-component-pipeline-python.md)

## Create a pipeline with a hyperparameter sweep step

### CLI v2

The following examples come from [Run a pipeline job using sweep (hyperdrive) in pipeline](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/pipelines-with-components/pipeline_with_hyperparameter_sweep) in the [Azure Machine Learning examples](https://github.com/Azure/azureml-examples) repository.

Assume you already have a command component defined in *train.yml*. The following code shows the two-step `train` and `predict` *pipeline.yml* file, with the `sweep_step` for hyperparameter tuning highlighted.

In the `sweep_step` code, the step type must be `sweep`. The `search_space` field shows three hyperparameters, `c_value`, `kernel`, and `coef`, and `trial` refers to the command component defined in *train.yml*.

:::code language="yaml" source="~/azureml-examples-main/cli/jobs/pipelines-with-components/pipeline_with_hyperparameter_sweep/pipeline.yml" highlight="7-48":::

After you submit this pipeline job, Azure Machine Learning runs the trial component multiple times to sweep over hyperparameters, based on the search space and limits you defined in `sweep_step`. See [CLI (v2) sweep job YAML schema](reference-yaml-job-sweep.md) for the full sweep job schema.

The following code shows the `trial` component definition in the *train.yml* file. 

:::code language="yaml" source="~/azureml-examples-main/cli/jobs/pipelines-with-components/pipeline_with_hyperparameter_sweep/train.yml" highlight="11-16,23-25,60":::

The hyperparameters added to `search_space` in *pipeline.yml* must be inputs for the `trial` component. The source code of the trial component is under the *./train-src* folder. In this example, the code is a single *train.py* file. This code is executed in every trial of the sweep job.

Make sure to log the metrics in the trial component source code with exactly the same name as the `primary_metric` value in the *pipeline.yml* file. This example uses `mlflow.autolog()`, which is the recommended way to track machine learning experiments. For more information about MLflow, see [Track ML experiments and models with MLflow](./how-to-use-mlflow-cli-runs.md).
 
The following example shows the trial component source code.

:::code language="python" source="~/azureml-examples-main/cli/jobs/pipelines-with-components/pipeline_with_hyperparameter_sweep/train-src/train.py" highlight="15":::

### Python SDK

The following Python SDK example comes from [Build pipeline with sweep node](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/pipelines/1c_pipeline_with_hyperparameter_sweep/pipeline_with_hyperparameter_sweep.ipynb) in the [Azure Machine Learning examples](https://github.com/Azure/azureml-examples) repository.

In Azure Machine Learning Python SDK v2, you can enable hyperparameter tuning for any command component by the calling `.sweep()` method. The following code snippet shows how to enable sweep for `train_model`.

The example first loads the `train_component_func` defined in the *train.yml* file. To create the `train_model`, the code adds `c_value`, `kernel`, and `coef0` into the search space. The `sweep_step` defines the `primary_metric`, `sampling_algorithm`, and other parameters.

[!notebook-python[] (~/azureml-examples-main/sdk/python/jobs/pipelines/1c_pipeline_with_hyperparameter_sweep/pipeline_with_hyperparameter_sweep.ipynb?name=enable-sweep)]

## Check a pipeline job with sweep step in studio

After you submit a pipeline job, the SDK or CLI widget provides a web URL link to the Azure Machine Learning studio UI. The link takes you to the pipeline graph view by default.

To check details of the sweep step, double click the sweep step and navigate to the **Child jobs** tab in the detail panel.

:::image type="content" source="./media/how-to-use-sweep-in-pipeline/pipeline-view.png" alt-text="Screenshot of the pipeline with child job and the train_model node highlighted." lightbox= "./media/how-to-use-sweep-in-pipeline/pipeline-view.png":::

Select a child job to go to the job page, and then select the **Child runs** tab, 

:::image type="content" source="./media/how-to-use-sweep-in-pipeline/sweep-job.png" alt-text="Screenshot of the child job page with the child runs tab." lightbox= "./media/how-to-use-sweep-in-pipeline/sweep-job.png":::

If a child job failed, select the **Outputs + logs** tab on the child job page to see useful debug information.

:::image type="content" source="./media/how-to-use-sweep-in-pipeline/child-run.png" alt-text="Screenshot of the output + logs tab of a child run." lightbox= "./media/how-to-use-sweep-in-pipeline/child-run.png":::

## Other sample notebooks

- [Build pipeline with sweep node](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/pipelines/1c_pipeline_with_hyperparameter_sweep/pipeline_with_hyperparameter_sweep.ipynb)
- [Run hyperparameter sweep on a command job](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/single-step/lightgbm/iris/lightgbm-iris-sweep.ipynb)

## Related content

- [Track an experiment](how-to-log-view-metrics.md)
- [Deploy a trained model](how-to-deploy-online-endpoints.md)
