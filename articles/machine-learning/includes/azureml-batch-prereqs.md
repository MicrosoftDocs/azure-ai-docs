---
ms.service: azure-machine-learning
ms.topic: include
ms.date: 11/20/2024
author: ccrestana
ms.author: cacrest
---

- An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- An Azure Machine Learning workspace. To create a workspace, see [Manage Azure Machine Learning workspaces](../how-to-manage-workspace.md).
- The following permissions in the Azure Machine Learning workspace:
  - For creating or managing batch endpoints and deployments: Use an Owner, Contributor, or custom role that has the `Microsoft.MachineLearningServices/workspaces/batchEndpoints/*` permissions.
  - For creating Azure Resource Manager deployments in the workspace resource group: Use an Owner, Contributor, or custom role that has the `Microsoft.Resources/deployments/write` permission in the resource group where the workspace is deployed.
- The Azure Machine Learning CLI or the Azure Machine Learning SDK for Python:

  # [Azure CLI](#tab/cli)

  Run the following command to install the [Azure CLI](/cli/azure/install-azure-cli) and the `ml` [extension for Azure Machine Learning](../how-to-configure-cli.md):

  ```azurecli
  az extension add -n ml
  ```

  Pipeline component deployments for batch endpoints require version 2.7 or later of the `ml` extension for the Azure CLI (current version: 2.37.0). Use the `az extension update --name ml` command to get the latest version.

  # [Python](#tab/python)

  Run the following command to install the [Azure Machine Learning SDK for Python](https://aka.ms/sdk-v2-install):

  ```python
  pip install azure-ai-ml
  ```

  The `ModelBatchDeployment` and `PipelineComponentBatchDeployment` classes require version 1.7.0 or later of the SDK (current version: 1.31.0). Use the `pip install -U azure-ai-ml` command to get the latest version.

  ---

### Connect to your workspace

The workspace is the top-level resource for Azure Machine Learning. It provides a centralized place to work with all artifacts you create when you use Azure Machine Learning. In this section, you connect to the workspace where you perform your deployment tasks.

# [Azure CLI](#tab/cli)

In the following command, enter your subscription ID, workspace name, resource group name, and location:

```azurecli
az account set --subscription <subscription>
az configure --defaults workspace=<workspace> group=<resource-group> location=<location>
```

# [Python](#tab/python)

1. Import the required libraries:

   ```python
   from azure.ai.ml import MLClient, Input, load_component
   from azure.ai.ml.entities import BatchEndpoint, ModelBatchDeployment, ModelBatchDeploymentSettings, PipelineComponentBatchDeployment, Model, AmlCompute, Data, BatchRetrySettings, CodeConfiguration, Environment, Data
   from azure.ai.ml.constants import AssetTypes, BatchDeploymentOutputAction
   from azure.ai.ml.dsl import pipeline
   from azure.identity import DefaultAzureCredential
   ```

1. Configure the workspace details and get a handle to the workspace:

   In the following command, enter your subscription ID, resource group name, and workspace name:

   ```python
   subscription_id = "<subscription>"
   resource_group = "<resource-group>"
   workspace = "<workspace>"
   
   ml_client = MLClient(DefaultAzureCredential(), subscription_id, resource_group, workspace)
   ```

---
