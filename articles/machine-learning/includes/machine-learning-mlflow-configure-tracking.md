---
author: santiagxf
ms.service: azure-machine-learning
ms.topic: include
ms.date: 11/20/2024
ms.author: fasantia
---

1. Get the tracking URI for your workspace:

    # [Azure CLI](#tab/cli)
    
    [!INCLUDE [cli v2](machine-learning-cli-v2.md)]
    
    1. Sign in and configure your workspace:
    
        ```bash
        az account set --subscription <subscription-ID>
        az configure --defaults workspace=<workspace-name> group=<resource-group-name> location=<location> 
        ```
    
    1. Get the tracking URI by using the `az ml workspace` command:
    
        ```bash
        az ml workspace show --query mlflow_tracking_uri
        ```
        
    # [Python SDK](#tab/python)
    
    [!INCLUDE [sdk v2](machine-learning-sdk-v2.md)]
    
    You can use the [Azure Machine Learning SDK v2 for Python](../concept-v2.md) to get the Azure Machine Learning MLflow tracking URI. Ensure that the `azure-ai-ml` library is installed in your compute instance. Then use the following code to get the unique MLFLow tracking URI that's associated with your workspace.
    
    1. Use an instance of `MLClient` to sign in to your workspace. There are two options for signing in:
    
        - The easiest way is to use the workspace configuration file:
    
          ```python
          from azure.ai.ml import MLClient
          from azure.identity import DefaultAzureCredential
    
          ml_client = MLClient.from_config(credential=DefaultAzureCredential())
          ```
    
          > [!TIP]
          >
          > You can download the workspace configuration file by taking the following steps:
          >
          > 1. In the Azure portal, go to your workspace.
          > 1. On the workspace page, select **Download config.json**.
          > 1. Move the config.json file to the directory that you're working in.
    
       - Alternatively, you can use your subscription ID, resource group name, and workspace name to sign in:
    
          ```python
          from azure.ai.ml import MLClient
          from azure.identity import DefaultAzureCredential
    
          # Enter information about your Azure Machine Learning workspace.
          subscription_id = "<subscription-ID>"
          resource_group = "<resource-group-name>"
          workspace_name = "<workspace-name>"
    
          ml_client = MLClient(credential=DefaultAzureCredential(),
                                  subscription_id=subscription_id, 
                                  resource_group_name=resource_group,
                                  workspace_name=workspace_name)
          ```
    
          > [!IMPORTANT]
          > The `DefaultAzureCredential` method tries to pull credentials from the available context. But you might want to specify credentials in a different way, for instance by using the web browser in an interactive way. In these cases, you can use `InteractiveBrowserCredential` or any other method available in the [`azure.identity`](https://pypi.org/project/azure-identity/) package.
    
    1. Get the Azure Machine Learning tracking URI:
    
        ```python
        mlflow_tracking_uri = ml_client.workspaces.get(ml_client.workspace_name).mlflow_tracking_uri
        ```
    
    # [Azure portal](#tab/studio)
    
    Use the Azure portal to get the tracking URI:
    
    1. In the Azure portal, go to the workspace.

    1. In the upper right corner, select the name of your workspace.

    1. Under __Essentials__, copy the __MLflow tracking URI__ value.    
    
    # [Manually](#tab/manual)
    
    You can construct the Azure Machine Learning tracking URI manually. You need your subscription ID, the region your workspace is deployed in, your resource group name, and your workspace name. To get the URI, enter those values into the following code:
    
    > [!WARNING]
    > If you use a private link-enabled workspace, the MLflow endpoint also uses a private link to communicate with Azure Machine Learning. As a result, the tracking URI uses a format that's different from the one in this article. In this case, you need to use the Azure Machine Learning SDK for Python or the Azure Machine Learning CLI v2 to get the tracking URI.
    
    ```python
    region = "<region>"
    subscription_id = "<subscription-ID>"
    resource_group = "<resource-group-name>"
    workspace_name = "<workspace-name>"
    
    mlflow_tracking_uri = f"azureml://{region}.api.azureml.ms/mlflow/v1.0/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.MachineLearningServices/workspaces/{workspace_name}"
    ```

    ---

1. Configure the tracking URI:

    # [MLflow SDK](#tab/mlflow)
    
    Use the [`set_tracking_uri()`](https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.set_tracking_uri) method to set the MLflow tracking URI to the tracking URI of your workspace.
    
    ```python
    import mlflow
    
    mlflow.set_tracking_uri(mlflow_tracking_uri)
    ```
    
    # [Environment variables](#tab/environ)
    
    In your compute instance, use the following code to set the `MLFLOW_TRACKING_URI` MLflow environment variable to the tracking URI of your workspace. This assignment makes all interactions with MLflow in that compute instance point to Azure Machine Learning by default. For more information, see [Logging functions](https://mlflow.org/docs/latest/tracking/tracking-api.html#logging-functions).
    
    ```bash
    MLFLOW_TRACKING_URI=$(az ml workspace show --query mlflow_tracking_uri | sed 's/"//g') 
    ```

    ---

    > [!TIP]
    >
    > Some scenarios involve working in a shared environment like an Azure Databricks cluster or an Azure Synapse Analytics cluster. In these cases, it's useful to set the `MLFLOW_TRACKING_URI` environment variable at the cluster level rather than for each session. Setting the variable at the cluster level automatically configures the MLflow tracking URI to point to Azure Machine Learning for all sessions in the cluster.
