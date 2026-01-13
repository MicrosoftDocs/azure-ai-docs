---
title: Configure MLflow for Azure Machine Learning
titleSuffix: Azure Machine Learning
description: Find out how to connect MLflow to an Azure Machine Learning workspace to log metrics, track artifacts, and deploy models.
services: machine-learning
author: s-polly
ms.author: scottpolly
ms.reviewer: jturuk
ms.service: azure-machine-learning
ms.subservice: mlops
ms.date: 12/29/2025
ms.topic: how-to
ms.custom: mlflow, cliv2, devplatv2
ms.devlang: azurecli
# customer intent: As a developer, I want to see how to configure MLflow so that I can run MLflow training routines in Azure Machine Learning.
---

# Configure MLflow for Azure Machine Learning

This article explains how to configure MLflow to connect to an Azure Machine Learning workspace for tracking, registry management, and deployment.

Azure Machine Learning workspaces are MLflow-compatible, which means they can act as MLflow servers without any extra configuration. Each workspace has an MLflow tracking URI that MLflow can use to connect to the workspace. Azure Machine Learning workspaces **are already configured to work with MLflow**, so no extra configuration is required.

However, if you work outside Azure Machine Learning, you need to configure MLflow to point to the workspace. Affected environments include your local machine, Azure Synapse Analytics, and Azure Databricks.

> [!IMPORTANT]
> When you use Azure compute infrastructure, you don't have to configure the tracking URI. It's automatically configured for you. Environments that have automatic configuration include Azure Machine Learning notebooks, Jupyter notebooks that are hosted on Azure Machine Learning compute instances, and jobs that run on Azure Machine Learning compute clusters.

## Prerequisites

- The MLflow SDK `mlflow` package and the Azure Machine Learning `azureml-mlflow` plugin for MLflow. You can use the following command to install this software:

  ```bash
  pip install mlflow azureml-mlflow
  ```

  > [!TIP]
  > Instead of `mlflow`, consider using [`mlflow-skinny`](https://github.com/mlflow/mlflow/blob/master/libs/skinny/README_SKINNY.md). This package is a lightweight MLflow package without SQL storage, server, UI, or data science dependencies. It's recommended for users who primarily need MLflow tracking and logging capabilities but don't want to import the full suite of features, including deployments.

- An Azure Machine Learning workspace. To create a workspace, see [Create resources you need to get started](quickstart-create-resources.md).

- Access permissions for performing MLflow operations in your workspace. For a list of operations and required permissions, see [MLflow operations](how-to-assign-roles.md#mlflow-operations).

## Configure the MLflow tracking URI

To do remote tracking, or track experiments running outside Azure Machine Learning, configure MLflow to point to the tracking URI of your Azure Machine Learning workspace.

To connect MLflow to an Azure Machine Learning workspace, you need the tracking URI of the workspace. Each workspace has its own tracking URI that starts with the protocol `azureml://`.

[!INCLUDE [mlflow-configure-tracking](includes/machine-learning-mlflow-configure-tracking.md)]

## Configure authentication

After you set up tracking, you also need to configure the authentication method for the associated workspace.

By default, the Azure Machine Learning plugin for MLflow performs interactive authentication by opening the default browser to prompt for credentials. But the plugin also supports several other authentication mechanisms. The `azure-identity` package provides this support. This package is installed as a dependency of the `azureml-mlflow` plugin.

The authentication process tries the following methods, one after another, until one succeeds:

1. **Environment**: Account information that's specified via environment variables is read and used for authentication.
1. **Managed identity**: If the application is deployed to an Azure host with a managed identity enabled, the managed identity is used for authentication.
1. **Azure CLI**: If you use the Azure CLI `az login` command to sign in, your credentials are used for authentication.
1. **Azure PowerShell**: If you use the Azure PowerShell `Connect-AzAccount` command to sign in, your credentials are used for authentication.
1. **Interactive browser**: The user is interactively authenticated via the default browser.

[!INCLUDE [mlflow-configure-auth](includes/machine-learning-mlflow-configure-auth.md)]

If you'd rather use a certificate than a secret, you can configure the following environment variables:

- Set `AZURE_CLIENT_CERTIFICATE_PATH` to the path of a file that contains the certificate and private key pair in Privacy-Enhanced Mail (PEM) or Public-Key Cryptography Standards 12 (PKCS #12) format.
- Set `AZURE_CLIENT_CERTIFICATE_PASSWORD` to the password of the certificate file, if it uses a password.

### Configure authorization and permission levels

Some [default roles](how-to-assign-roles.md#default-roles) like AzureML Data Scientist and Contributor are already configured to perform MLflow operations in an Azure Machine Learning workspace. If you use a custom role, you need the following permissions:

- **To use MLflow tracking:**
  - `Microsoft.MachineLearningServices/workspaces/experiments/*`
  - `Microsoft.MachineLearningServices/workspaces/jobs/*`

- **To use the MLflow model registry:**
  - `Microsoft.MachineLearningServices/workspaces/models/*/*`

To see how to grant access to your workspace to a service principal that you create or to your user account, see [Grant access](/azure/role-based-access-control/quickstart-assign-role-user-portal#grant-access).

### Troubleshoot authentication issues

MLflow tries to authenticate to Azure Machine Learning on the first operation that interacts with the service, like `mlflow.set_experiment()` or `mlflow.start_run()`. If you experience issues or unexpected authentication prompts during the process, you can increase the logging level to get more details about the error:

```python
import logging

logging.getLogger("azure").setLevel(logging.DEBUG)
```

## Set experiment name (optional)

All MLflow runs are logged to the active experiment. By default, runs are logged to an experiment named `Default` that's automatically created. You can configure the experiment that's used for tracking.

> [!TIP]
>
> When you use the Azure Machine Learning CLI v2 to submit jobs, you can set the experiment name by using the `experiment_name` property in the YAML definition of the job. You don't have to configure it in your training script. For more information, see [YAML: display name, experiment name, description, and tags](reference-yaml-job-command.md#yaml-display-name-experiment-name-description-and-tags).


# [MLflow SDK](#tab/mlflow)

Use the MLflow [`mlflow.set_experiment()`](https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.set_experiment) command to configure your experiment.
    
```python
experiment_name = "experiment_with_mlflow"
mlflow.set_experiment(experiment_name)
```

# [Environment variables](#tab/environ)

Use the MLflow `MLFLOW_EXPERIMENT_NAME` or `MLFLOW_EXPERIMENT_ID` environment variable to configure your experiment. For more information, see [Command-Line Interface](https://mlflow.org/docs/latest/cli.html) or [mlflow.start_run](https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.start_run).

```bash
export MLFLOW_EXPERIMENT_NAME="experiment_with_mlflow"
```

---

## Configure support for a nonpublic Azure cloud

The Azure Machine Learning plugin for MLflow is configured by default to work with the global Azure cloud. However, you can configure the Azure cloud you're using by setting the `AZUREML_CURRENT_CLOUD` environment variable:

# [MLflow SDK](#tab/mlflow)

```python
import os

os.environ["AZUREML_CURRENT_CLOUD"] = "AzureChinaCloud"
```

# [Environment variables](#tab/environ)

```bash
export AZUREML_CURRENT_CLOUD="AzureChinaCloud"
```

---

You can identify the cloud you're using with the following Azure CLI command:

```bash
az cloud list
```

The current cloud has the value `IsActive` set to `True`.

## Related content

Now that your environment is connected to your workspace in Azure Machine Learning, you can start to work with it.

- [Track experiments and models with MLflow](how-to-use-mlflow-cli-runs.md)
- [Manage models registry in Azure Machine Learning with MLflow](how-to-manage-models-mlflow.md)
- [Train with MLflow Projects in Azure Machine Learning (preview)](how-to-train-mlflow-projects.md)
- [Guidelines for deploying MLflow models](how-to-deploy-mlflow-models.md)
