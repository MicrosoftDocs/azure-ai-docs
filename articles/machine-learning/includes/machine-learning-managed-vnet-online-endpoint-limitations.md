---
author: s-polly
ms.service: azure-machine-learning
ms.topic: include
ms.date: 12/02/2024
ms.author: scottpolly
---

- The `v1_legacy_mode` flag must be set to `false` to turn off v1 legacy mode on your Azure Machine Learning workspace. If this setting is turned on, you can't create a managed online endpoint. For more information, see [Network isolation change with our new API platform on Azure Resource Manager](../how-to-configure-network-isolation-with-v2.md).

- If your Azure Machine Learning workspace has a private endpoint that was created before May 24, 2022, you must re-create that private endpoint before you configure your online endpoints to use private endpoints. For more information about creating a private endpoint for your workspace, see [Configure a private endpoint for an Azure Machine Learning workspace](../how-to-configure-private-link.md).

  > [!TIP]
  > To see the creation date of a workspace, you can check the workspace properties.
  >
  > 1. In Azure Machine Learning studio, go to the upper-right corner and select the name of your workspace.
  > 1. In the Directory + Subscription + Workspace window, select **View all properties in Azure portal**.
  > 1. In the Azure portal Overview page, go to the upper-right corner and select **JSON View**.
  > 1. In the Resource JSON window, under **API Versions**, select the latest API version.
  > 1. In the `properties` section of the JSON code, check the `creationTime` value.
  >
  > Alternatively, use one of the following methods:
  >
  > - [Python SDK](/python/api/azureml-core/azureml.core.workspace.workspace): `Workspace.get(name=<workspace-name>, subscription_id=<subscription-ID>, resource_group=<resource-group-name>).get_details()`
  > - [REST API](../how-to-manage-rest.md#drill-down-into-workspaces-and-their-resources): `curl https://management.azure.com/subscriptions/<subscription-ID>/resourceGroups/<resource-group-name>/providers/Microsoft.MachineLearningServices/workspaces/?api-version=2023-10-01 -H "Authorization:Bearer <access-token>"`
  > - [PowerShell](/powershell/module/az.machinelearningservices/get-azmlworkspace): `Get-AzMLWorkspace -Name <workspace-name> -ResourceGroupName <resource-group-name>`

- When you use network isolation to help secure online endpoints, you can use workspace-associated resources from a different resource group than your workspace resource group. However, these resources must belong to the same subscription and tenant as your workspace. Resources that are associated with a workspace include Azure Container Registry, Azure Storage, Azure Key Vault, and Application Insights.

> [!NOTE]
> This article describes network isolation that applies to data plane operations. These operations result from scoring requests, or model serving. Control plane operations, such as requests to create, update, delete, or retrieve authentication keys, are sent to Azure Resource Manager over the public network.
