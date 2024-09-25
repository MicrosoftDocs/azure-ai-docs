---
author: santiagxf
ms.service: azure-machine-learning
ms.topic: include
ms.date: 09/25/2024
ms.author: fasantia
---

- Install the MLflow SDK `mlflow` package and the Azure Machine Learning `azureml-mlflow` plugin for MLflow as follows:

  ```bash
  pip install mlflow azureml-mlflow
  ```

  > [!TIP]
  > You can use the [`mlflow-skinny`](https://github.com/mlflow/mlflow/blob/master/README_SKINNY.rst) package, which is a lightweight MLflow package without SQL storage, server, UI, or data science dependencies. This package is recommended for users who primarily need the MLflow tracking and logging capabilities without importing the full suite of features, including deployments.

- Create an Azure Machine Learning workspace. To create a workspace, see [Create resources you need to get started](../quickstart-create-resources.md). Review the [access permissions](../how-to-assign-roles.md#mlflow-operations) you need to perform your MLflow operations in your workspace.

- To do remote tracking, that is track experiments running outside Azure Machine Learning, configure MLflow to point to the tracking URI of your Azure Machine Learning workspace. For more information on how to connect MLflow to your workspace, see [Configure MLflow for Azure Machine Learning](../how-to-use-mlflow-configure-tracking.md).
