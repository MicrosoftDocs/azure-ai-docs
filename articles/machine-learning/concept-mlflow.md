---
title: MLflow and Azure Machine Learning
titleSuffix: Azure Machine Learning
description: See how to use MLflow with Azure Machine Learning to log metrics, store artifacts, and deploy models to an endpoint.
services: machine-learning
author: s-polly
ms.author: scottpolly
ms.reviewer: jturuk
ms.service: azure-machine-learning
ms.subservice: mlops
ms.date: 10/6/2025
ms.topic: concept-article
ms.custom: cliv2, sdkv2, FY25Q1-Linter
#Customer intent: As a data scientist, I want to understand what MLflow is and does so that I can use MLflow with my models.
---

# MLflow and Azure Machine Learning

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

This article describes the capabilities of [MLflow](https://www.mlflow.org), an open-source framework that manages the complete machine learning lifecycle. MLflow uses a consistent set of tools to train and serve models on different platforms. Use MLflow whether your experiments run locally, on a remote compute target, a virtual machine, or an Azure Machine Learning compute instance.

Azure Machine Learning workspaces are MLflow-compatible, so you use an Azure Machine Learning workspace the same way you use an MLflow server. This compatibility offers these advantages:

- Azure Machine Learning doesn't host MLflow server instances, but uses the MLflow APIs directly.
- Use an Azure Machine Learning workspace as your tracking server for any MLflow code, whether or not it runs in Azure Machine Learning. Just configure MLflow to point to the workspace where tracking happens.
- Run any training routine that uses MLflow in Azure Machine Learning without making changes.

> [!TIP]
> Unlike the Azure Machine Learning SDK v1, the Azure Machine Learning v2 SDK doesn't include logging functionality. Use MLflow logging to keep your training routines cloud-agnostic, portable, and independent of Azure Machine Learning.

## What is tracking

When you work with jobs, Azure Machine Learning automatically tracks information about experiments, like code, environment, and input and output data. But models, parameters, and metrics are specific to each scenario, so model builders need to set up their tracking.

The saved tracking metadata varies by experiment and can include:

- Code
- Environment details like OS version and Python packages
- Input data
- Parameter configurations
- Models
- Evaluation metrics
- Evaluation visualizations like confusion matrices and importance plots
- Evaluation results, including some evaluation predictions

## Benefits of tracking experiments

Whether you train models with jobs in Azure Machine Learning or interactively in notebooks, experiment tracking helps you:

- Organize all your machine learning experiments in one place. Then search and filter experiments, and drill down to see details about previous experiments.
- Compare experiments, analyze results, and debug model training.
- Reproduce or rerun experiments to validate results.
- Collaborate more easily, because you see what other teammates are doing, share experiment results, and access experiment data programmatically.

## Tracking with MLflow

Azure Machine Learning workspaces are MLflow-compatible. This compatibility means you use MLflow to track runs, metrics, parameters, and artifacts in workspaces without changing your training routines or adding any cloud-specific syntax. To learn how to use MLflow for tracking experiments and runs in Azure Machine Learning workspaces, see [Track experiments and models with MLflow](how-to-use-mlflow-cli-runs.md).

Azure Machine Learning uses MLflow tracking to log metrics and store artifacts for your experiments. When you're connected to Azure Machine Learning, all MLflow tracking appears in the workspace you use.

To learn how to enable logging to monitor real-time run metrics with MLflow, see [Log metrics, parameters, and files with MLflow](how-to-log-view-metrics.md). You also [query and compare experiments and runs with MLflow](how-to-track-experiments-mlflow.md).

MLflow in Azure Machine Learning provides a way to centralize tracking. Connect MLflow to Azure Machine Learning workspaces even when you work locally or in a different cloud. The Azure Machine Learning workspace provides a centralized, secure, and scalable location to store training metrics and models.

MLflow in Azure Machine Learning lets you:

- [Track machine learning experiments and models running locally or in the cloud](how-to-use-mlflow-cli-runs.md).
- [Track Azure Databricks machine learning experiments](how-to-use-mlflow-azure-databricks.md).
- [Track Azure Synapse Analytics machine learning experiments](how-to-use-mlflow-azure-synapse.md).

### Tracking with MLflow in R

MLflow support in R has these limitations:

- MLflow tracking is limited to tracking experiment metrics, parameters, and models on Azure Machine Learning jobs.
- Interactive training on RStudio, Posit (formerly RStudio Workbench), or Jupyter notebooks with R kernels isn't supported.
- Model management and registration aren't supported. Use the Azure Machine Learning CLI or Azure Machine Learning studio for model registration and management.

For examples of using the MLflow tracking client with R models in Azure Machine Learning, see [Train R models using the Azure Machine Learning CLI (v2)](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/single-step/r).

### Tracking with MLflow in Java

MLflow support in Java has these limitations:

- MLflow tracking is limited to tracking experiment metrics and parameters on Azure Machine Learning jobs.
- Artifacts and models can't be tracked. Instead, use the `mlflow.save_model` method with the `outputs` folder in jobs to save models or artifacts that you want to capture.

For a Java example that uses the MLflow tracking client with the Azure Machine Learning tracking server, see [azuremlflow-java](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/single-step/java/iris).

### Example notebooks for MLflow tracking

- [Training and tracking an XGBoost classifier with MLflow](https://github.com/Azure/azureml-examples/blob/main/sdk/python/using-mlflow/train-and-log/xgboost_classification_mlflow.ipynb) shows how to use MLflow to track experiments, log models, and combine multiple flavors into pipelines.
- [Training and tracking an XGBoost classifier with MLflow using service principal authentication](https://github.com/Azure/azureml-examples/blob/main/sdk/python/using-mlflow/train-and-log/xgboost_service_principal.ipynb) shows how to use MLflow to track experiments from a compute that's running outside Azure Machine Learning. The example shows how to authenticate against Azure Machine Learning services by using a service principal.
- [Hyperparameter optimization using HyperOpt and nested runs in MLflow](https://github.com/Azure/azureml-examples/blob/main/sdk/python/using-mlflow/train-and-log/xgboost_nested_runs.ipynb) shows how to use child runs to do hyperparameter optimization for models by using the popular HyperOpt library. The example shows how to transfer metrics, parameters, and artifacts from child runs to parent runs.
- [Logging models with MLflow](https://github.com/Azure/azureml-examples/blob/main/sdk/python/using-mlflow/train-and-log/logging_and_customizing_models.ipynb) shows how to use the concept of models instead of artifacts with MLflow. The example also shows how to construct custom models.
- [Manage runs and experiments with MLflow](https://github.com/Azure/azureml-examples/blob/main/sdk/python/using-mlflow/runs-management/run_history.ipynb) shows how to use MLflow to query experiments, runs, metrics, parameters, and artifacts from Azure Machine Learning.

## Model registration with MLflow

Azure Machine Learning supports MLflow for model management. If you're familiar with the MLflow client, you can use it to manage the entire model lifecycle. To learn more about managing models with the MLflow API in Azure Machine Learning, see [Manage model registries in Azure Machine Learning with MLflow](how-to-manage-models-mlflow.md).

### Example notebook for MLflow model registration

[Model management with MLflow](https://github.com/Azure/azureml-examples/blob/main/sdk/python/using-mlflow/model-management/model_management.ipynb) shows how to manage models in registries.

## Model deployment with MLflow

Deploy MLflow models to Azure Machine Learning to get an improved experience. Azure Machine Learning supports deploying MLflow models to both real-time and batch endpoints without specifying an environment or a scoring script.

The MLflow SDK, Azure Machine Learning CLI, Azure Machine Learning SDK for Python, and Azure Machine Learning studio all support MLflow model deployment. For more information about deploying MLflow models to Azure Machine Learning for both real-time and batch inference, see [Guidelines for deploying MLflow models](how-to-deploy-mlflow-models.md).

### Example notebooks for MLflow model deployment

- [Deploy MLflow to online endpoints](https://github.com/Azure/azureml-examples/blob/main/sdk/python/using-mlflow/deploy/mlflow_sdk_online_endpoints.ipynb) shows how to deploy MLflow models to online endpoints using the MLflow SDK.
- [Progressive rollout of MLflow deployments](https://github.com/Azure/azureml-examples/blob/main/sdk/python/using-mlflow/deploy/mlflow_sdk_online_endpoints_progresive.ipynb) shows how to deploy MLflow models to online endpoints using the MLflow SDK with progressive model rollout. The example also shows how to deploy multiple versions of a model to the same endpoint.
- [Deploy MLflow models to legacy web services](https://github.com/Azure/azureml-examples/blob/main/sdk/python/using-mlflow/deploy/mlflow_sdk_web_service.ipynb) shows how to deploy MLflow models to legacy web services (Azure Container Instances or Azure Kubernetes Service v1) using the MLflow SDK.
- [Train models in Azure Databricks and deploy them on Azure Machine Learning](https://github.com/Azure/azureml-examples/blob/main/sdk/python/using-mlflow/deploy/track_with_databricks_deploy_aml.ipynb) shows how to train models in Azure Databricks and deploy them in Azure Machine Learning. The example also covers tracking experiments with the MLflow instance in Azure Databricks.

## Training with MLflow Projects (preview)

[!INCLUDE [machine-learning-mlflow-projects-deprecation](includes/machine-learning-mlflow-projects-deprecation.md)]

[!INCLUDE [machine-learning-preview-generic-disclaimer](includes/machine-learning-preview-generic-disclaimer.md)]

Submit training jobs to Azure Machine Learning by using [MLflow Projects](https://www.mlflow.org/docs/latest/projects.html). Submit jobs locally with Azure Machine Learning tracking, or migrate your jobs to the cloud by using [Azure Machine Learning compute](how-to-create-attach-compute-cluster.md).

Learn how to submit training jobs that use MLflow Projects to Azure Machine Learning workspaces for tracking in [Train with MLflow Projects in Azure Machine Learning (preview)](how-to-train-mlflow-projects.md).

### Example notebooks for MLflow projects

- [Train with MLflow Projects on local compute](https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/track-and-monitor-experiments/using-mlflow/train-projects-local/train-projects-local.ipynb)
- [Train with MLflow Projects on Azure Machine Learning compute](https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/track-and-monitor-experiments/using-mlflow/train-projects-remote/train-projects-remote.ipynb)

## MLflow vs Azure Machine Learning client tools capabilities

The following table shows machine learning lifecycle operations you can do with the MLflow SDK and Azure Machine Learning client tools.

| Feature | MLflow SDK | Azure Machine Learning CLI/SDK v2 | Azure Machine Learning studio |
|---|---|---|---|
| Track and log metrics, parameters, and models | **&check;** | | |
| Retrieve metrics, parameters, and models | **&check;** | You can download only artifacts and models. | **&check;** |
| Submit training jobs | You can use MLflow Projects (preview). | **&check;** | **&check;** |
| Submit training jobs with Azure Machine Learning data assets |  | **&check;** | **&check;** |
| Submit training jobs with machine learning pipelines | | **&check;** | **&check;** |
| Manage experiments and runs | **&check;** | **&check;** | **&check;** |
| Manage MLflow models | Some operations aren't supported.<sup>1</sup> | **&check;** | **&check;** |
| Manage non-MLflow models | | **&check;** | **&check;** |
| Deploy MLflow models to Azure Machine Learning (online and batch) | You can't deploy MLflow models for batch inference right now.<sup>2</sup> | **&check;** | **&check;** |
| Deploy non-MLflow models to Azure Machine Learning | | **&check;** | **&check;** |

<sup>1</sup> For more information, see [Manage model registries in Azure Machine Learning with MLflow](how-to-manage-models-mlflow.md).

<sup>2</sup> For an alternative, see [Deploy and run MLflow models in Spark jobs](how-to-deploy-mlflow-model-spark-jobs.md).

## Related content

- [Configure MLflow for Azure Machine Learning](how-to-use-mlflow-configure-tracking.md)
- [Track ML experiments and models with MLflow](how-to-use-mlflow-cli-runs.md)
- [Guidelines for deploying MLflow models](how-to-deploy-mlflow-models.md)
