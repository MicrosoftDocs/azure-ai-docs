---
title: MLflow and Azure Machine Learning
titleSuffix: Azure Machine Learning
description: See how to use MLflow with Azure Machine Learning to log metrics, store artifacts, and deploy models to an endpoint.
services: machine-learning
author: msakande
ms.author: mopeakande
ms.reviewer: cacrest
ms.service: azure-machine-learning
ms.subservice: mlops
ms.date: 09/30/2024
ms.topic: concept-article
ms.custom: cliv2, sdkv2, FY25Q1-Linter
#Customer intent: As a data scientist, I want to understand what MLflow is and does so that I can use MLflow with my models.
---

# MLflow and Azure Machine Learning

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

This article describes the capabilities of [MLflow](https://www.mlflow.org), an open-source framework designed to manage the complete machine learning lifecycle. MLflow uses a consistent set of tools to train and serve models on different platforms. You can use MLflow whether your experiments are running locally or on a remote compute target, virtual machine, or Azure Machine Learning compute instance.

Azure Machine Learning workspaces are MLflow-compatible, which means that you can use an Azure Machine Learning workspace the same way you use an MLflow server. This compatibility has the following advantages:

- Azure Machine Learning doesn't host MLflow server instances, but can use the MLflow APIs directly.
- You can use an Azure Machine Learning workspace as your tracking server for any MLflow code, whether or not it runs in Azure Machine Learning. You only need to configure MLflow to point to the workspace where the tracking should occur.
- You can run any training routine that uses MLflow in Azure Machine Learning without making any changes.

> [!TIP]
> Unlike the Azure Machine Learning SDK v1, there's no logging functionality in the Azure Machine Learning v2 SDK. You can use MLflow logging to ensure that your training routines are cloud-agnostic, portable, and have no dependency on Azure Machine Learning.

## What is tracking

When you work with jobs, Azure Machine Learning automatically tracks some information about experiments, such as code, environment, and input and output data. However, models, parameters, and metrics are specific to the scenario, so model builders must configure their tracking.

The saved tracking metadata varies by experiment, and can include:

- Code
- Environment details such as OS version and Python packages
- Input data
- Parameter configurations
- Models
- Evaluation metrics 
- Evaluation visualizations such as confusion matrices and importance plots
- Evaluation results, including some evaluation predictions

## Benefits of tracking experiments

Whether you train models with jobs in Azure Machine Learning or interactively in notebooks, experiment tracking helps you:

- Organize all of your machine learning experiments in a single place. You can then search and filter experiments and drill down to see details about previous experiments.
- Easily compare experiments, analyze results, and debug model training.
- Reproduce or rerun experiments to validate results.
- Improve collaboration, because you can see what other teammates are doing, share experiment results, and access experiment data programmatically.

## Tracking with MLflow

Azure Machine Learning workspaces are MLflow-compatible. This compatibility means you can use MLflow to track runs, metrics, parameters, and artifacts in workspaces without needing to change your training routines or inject any cloud-specific syntax. To learn how to use MLflow for tracking experiments and runs in Azure Machine Learning workspaces, see [Track experiments and models with MLflow](how-to-use-mlflow-cli-runs.md).

Azure Machine Learning uses MLflow tracking to log metrics and store artifacts for your experiments. When you're connected to Azure Machine Learning, all MLflow tracking materializes in the workspace you're working in.

To learn how to enable logging to monitor real-time run metrics with MLflow, see [Log metrics, parameters, and files with MLflow](how-to-log-view-metrics.md). You can also [query and compare experiments and runs with MLflow](how-to-track-experiments-mlflow.md).

MLflow in Azure Machine Learning provides a way to centralize tracking. You can connect MLflow to Azure Machine Learning workspaces even when you're working locally or in a different cloud. The Azure Machine Learning workspace provides a centralized, secure, and scalable location to store training metrics and models.

MLflow in Azure Machine Learning can:

- [Track machine learning experiments and models running locally or in the cloud](how-to-use-mlflow-cli-runs.md).
- [Track Azure Databricks machine learning experiments](how-to-use-mlflow-azure-databricks.md).
- [Track Azure Synapse Analytics machine learning experiments](how-to-use-mlflow-azure-synapse.md).

### Tracking with MLflow in R

MLflow support in R has the following limitations:

- MLflow tracking is limited to tracking experiment metrics, parameters, and models on Azure Machine Learning jobs.
- Interactive training on RStudio, Posit (formerly RStudio Workbench), or Jupyter notebooks with R kernels isn't supported.
- Model management and registration aren't supported. Use the Azure Machine Learning CLI or Azure Machine Learning studio for model registration and management.

For examples of using the MLflow tracking client with R models in Azure Machine Learning, see [Train R models using the Azure Machine Learning CLI (v2)](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/single-step/r).

### Tracking with MLflow in Java

MLflow support in Java has the following limitations:

- MLflow tracking is limited to tracking experiment metrics and parameters on Azure Machine Learning jobs.
- Artifacts and models can't be tracked. Instead, use the `mlflow.save_model` method with the `outputs` folder in jobs to save models or artifacts that you want to capture.

For a Java example that uses the MLflow tracking client with the Azure Machine Learning tracking server, see [azuremlflow-java](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/single-step/java/iris).

### Example notebooks for MLflow tracking

- [Training and tracking an XGBoost classifier with MLflow](https://github.com/Azure/azureml-examples/blob/main/sdk/python/using-mlflow/train-and-log/xgboost_classification_mlflow.ipynb) demonstrates how to use MLflow to track experiments, log models, and combine multiple flavors into pipelines.
- [Training and tracking an XGBoost classifier with MLflow using service principal authentication](https://github.com/Azure/azureml-examples/blob/main/sdk/python/using-mlflow/train-and-log/xgboost_service_principal.ipynb) demonstrates how to use MLflow to track experiments from a compute that's running outside Azure Machine Learning. The example shows how to authenticate against Azure Machine Learning services by using a service principal.
- [Hyperparameter optimization using HyperOpt and nested runs in MLflow](https://github.com/Azure/azureml-examples/blob/main/sdk/python/using-mlflow/train-and-log/xgboost_nested_runs.ipynb) demonstrates how to use child runs to do hyperparameter optimization for models by using the popular HyperOpt library. The example shows how to transfer metrics, parameters, and artifacts from child runs to parent runs.
- [Logging models with MLflow](https://github.com/Azure/azureml-examples/blob/main/sdk/python/using-mlflow/train-and-log/logging_and_customizing_models.ipynb) demonstrates how to use the concept of models instead of artifacts with MLflow. The example also shows how to construct custom models.
- [Manage runs and experiments with MLflow](https://github.com/Azure/azureml-examples/blob/main/sdk/python/using-mlflow/runs-management/run_history.ipynb) demonstrates how to use MLflow to query experiments, runs, metrics, parameters, and artifacts from Azure Machine Learning.

## Model registration with MLflow

Azure Machine Learning supports MLflow for model management. This support is a convenient way for users who are familiar with the MLflow client to manage the entire model lifecycle. For more information about how to manage models by using the MLflow API in Azure Machine Learning, see [Manage model registries in Azure Machine Learning with MLflow](how-to-manage-models-mlflow.md).

### Example notebook for MLflow model registration

[Model management with MLflow](https://github.com/Azure/azureml-examples/blob/main/sdk/python/using-mlflow/model-management/model_management.ipynb) demonstrates how to manage models in registries.

## Model deployment with MLflow

You can deploy MLflow models to Azure Machine Learning to take advantage of an improved experience. Azure Machine Learning supports deployment of MLflow models to both real-time and batch endpoints without having to specify an environment or a scoring script.

The MLflow SDK, Azure Machine Learning CLI, Azure Machine Learning SDK for Python, and Azure Machine Learning studio all support MLflow model deployment. For more information about deploying MLflow models to Azure Machine Learning for both real-time and batch inferencing, see [Guidelines for deploying MLflow models](how-to-deploy-mlflow-models.md).

### Example notebooks for MLflow model deployment

- [Deploy MLflow to online endpoints](https://github.com/Azure/azureml-examples/blob/main/sdk/python/using-mlflow/deploy/mlflow_sdk_online_endpoints.ipynb) demonstrates how to deploy MLflow models to online endpoints using the MLflow SDK.
- [Progressive rollout of MLflow deployments](https://github.com/Azure/azureml-examples/blob/main/sdk/python/using-mlflow/deploy/mlflow_sdk_online_endpoints_progresive.ipynb) demonstrates how to deploy MLflow models to online endpoints using the MLflow SDK with progressive model rollout. The example also shows deployment of multiple versions of a model to the same endpoint.
- [Deploy MLflow models to legacy web services](https://github.com/Azure/azureml-examples/blob/main/sdk/python/using-mlflow/deploy/mlflow_sdk_web_service.ipynb) demonstrates how to deploy MLflow models to legacy web services (Azure Container Instances or Azure Kubernetes Service v1) using the MLflow SDK.
- [Train models in Azure Databricks and deploy them on Azure Machine Learning](https://github.com/Azure/azureml-examples/blob/main/sdk/python/using-mlflow/deploy/track_with_databricks_deploy_aml.ipynb) demonstrates how to train models in Azure Databricks and deploy them in Azure Machine Learning. The example also covers tracking experiments with the MLflow instance in Azure Databricks.

## Training with MLflow Projects (preview)

[!INCLUDE [machine-learning-mlflow-projects-deprecation](includes/machine-learning-mlflow-projects-deprecation.md)]

[!INCLUDE [machine-learning-preview-generic-disclaimer](includes/machine-learning-preview-generic-disclaimer.md)]

You can submit training jobs to Azure Machine Learning by using [MLflow Projects](https://www.mlflow.org/docs/latest/projects.html). You can submit jobs locally with Azure Machine Learning tracking or migrate your jobs to the cloud via [Azure Machine Learning compute](how-to-create-attach-compute-cluster.md).

To learn how to submit training jobs that use MLflow Projects to Azure Machine Learning workspaces for tracking, see [Train with MLflow Projects in Azure Machine Learning (preview)](how-to-train-mlflow-projects.md).

### Example notebooks for MLflow Projects

- [Train with MLflow Projects on local compute](https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/track-and-monitor-experiments/using-mlflow/train-projects-local/train-projects-local.ipynb).
- [Train with MLflow Projects on Azure Machine Learning compute](https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/track-and-monitor-experiments/using-mlflow/train-projects-remote/train-projects-remote.ipynb).

## MLflow vs Azure Machine Learning client tools capabilities

The following table shows machine learning lifecycle operations that are possible with the MLflow SDK and the Azure Machine Learning client tools.

| Feature | MLflow SDK | Azure Machine Learning CLI/SDK v2 | Azure Machine Learning studio |
|---|---|---|---|
| Track and log metrics, parameters, and models | **&check;** | | |
| Retrieve metrics, parameters, and models | **&check;** | Only artifacts and models can be downloaded. | **&check;** |
| Submit training jobs | Possible by using MLflow Projects (preview). | **&check;** | **&check;** |
| Submit training jobs with Azure Machine Learning data assets |  | **&check;** | **&check;** |
| Submit training jobs with machine learning pipelines | | **&check;** | **&check;** |
| Manage experiments and runs | **&check;** | **&check;** | **&check;** |
| Manage MLflow models | Some operations might not be supported.<sup>1</sup> | **&check;** | **&check;** |
| Manage non-MLflow models | | **&check;** | **&check;** |
| Deploy MLflow models to Azure Machine Learning (online and batch) | Deploying MLflow models for batch inference isn't currently supported.<sup>2</sup> | **&check;** | **&check;** |
| Deploy non-MLflow models to Azure Machine Learning | | **&check;** | **&check;** |

<sup>1</sup> For more information, see [Manage model registries in Azure Machine Learning with MLflow](how-to-manage-models-mlflow.md).

<sup>2</sup> For an alternative, see [Deploy and run MLflow models in Spark jobs](how-to-deploy-mlflow-model-spark-jobs.md).

## Related content

- [Configure MLflow for Azure Machine Learning](how-to-use-mlflow-configure-tracking.md)
- [Track ML experiments and models with MLflow](how-to-use-mlflow-cli-runs.md)
- [Guidelines for deploying MLflow models](how-to-deploy-mlflow-models.md)
