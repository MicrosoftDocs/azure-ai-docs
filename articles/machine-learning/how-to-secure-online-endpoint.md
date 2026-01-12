---
title: Secure managed online endpoints
titleSuffix: Azure Machine Learning
description: See how to use private endpoints to provide network isolation for Azure Machine Learning managed online endpoints.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: enterprise-readiness
ms.topic: how-to
ms.reviewer: shshubhe
author: s-polly
ms.author: scottpolly
ms.date: 03/31/2025
ms.custom: devx-track-azurecli, moe-wsvnet, update-code6
# customer intent: As a developer, I want to see how to use private endpoints to provide network isolation so that I can improve the security of my Azure Machine Learning managed online endpoints.
---

# Secure managed online endpoints by using network isolation

[!INCLUDE [machine-learning-dev-v2](includes/machine-learning-dev-v2.md)]

This article shows you how to use network isolation to improve the security of an Azure Machine Learning managed online endpoint. Network isolation helps secure the inbound and outbound communication to and from your endpoint.

To help secure inbound communication, you can create a managed online endpoint that uses the private endpoint of an Azure Machine Learning workspace. To allow only approved outbound communication for deployments, you can configure the workspace with a managed virtual network. This article shows you how to take these steps to improve endpoint security. It also shows you how to create a deployment that uses the private endpoints of the workspace's managed virtual network for outbound communication.

If you prefer to use the legacy method for network isolation, see the following deployment file examples in the [azureml-examples](https://github.com/Azure/azureml-examples) GitHub repository:

- For a deployment that uses a generic model: [deploy-moe-vnet-legacy.sh](https://github.com/Azure/azureml-examples/blob/main/cli/deploy-moe-vnet-legacy.sh)
- For a deployment that uses an MLflow model: [deploy-moe-vnet-mlflow-legacy.sh](https://github.com/Azure/azureml-examples/blob/main/cli/deploy-moe-vnet-mlflow-legacy.sh)

## Prerequisites

* An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.

* The [Azure CLI](/cli/azure/install-azure-cli) and the Azure CLI `ml` extension, installed and configured. For more information, see [Install and set up the CLI (v2)](how-to-configure-cli.md).

  >[!TIP]
  > The Azure Machine Learning managed virtual network feature was introduced on May 23, 2023. If you have an older version of the `ml` extension, you might need to update it for the examples in this article to work. To update the extension, use the following Azure CLI command:
  >
  > ```azurecli
  > az extension update -n ml
  > ```

* A Bash shell or a compatible shell, for example, a shell on a Linux system or [Windows Subsystem for Linux](/windows/wsl/about). The Azure CLI examples in this article assume that you use this type of shell.

* An Azure resource group in which you or the service principal that you use have Contributor access. For instructions for creating a resource group, see [Set up](how-to-configure-cli.md?#set-up).

* A [user-assigned managed identity](/azure/active-directory/managed-identities-azure-resources/how-manage-user-assigned-managed-identities?pivots=identity-mi-methods-azp) with appropriate permissions, if you want to use a managed identity to create and manage online endpoints and online deployments. For detailed information about required permissions, see [Set up authentication between Azure Machine Learning and other services](./how-to-identity-based-service-authentication.md#workspace). For example, you need to grant your managed identity specific Azure role-based access control (Azure RBAC) permissions for Azure Key Vault.

### Migrate from the legacy network isolation method to a workspace managed virtual network

If you use the [legacy method](concept-secure-online-endpoint.md#secure-outbound-access-with-legacy-network-isolation-method) for network isolation of managed online endpoints and you want to migrate to a managed virtual network to secure your endpoints, follow these steps:

1. Create a new workspace and enable a managed virtual network. For more information about how to configure a managed network for your workspace, see [Workspace managed virtual network isolation](how-to-managed-network.md).
1. (Optional) If your deployments access private resources other than Azure Storage, Key Vault, and Azure Container Registry, add outbound rules to the network settings of your workspace. Specifically, the network is configured with rules for Azure Storage, Key Vault, and Container Registry by default. Add rules with private endpoints for any other private resources that you use. 
1. (Optional) If you intend to use an Azure Machine Learning registry, configure private endpoints for outbound communication to your registry, its storage account, and its instance of Container Registry.
1. Create online endpoints and deployments in the new workspace. If you use Azure Machine Learning registries, you can directly deploy components from them. For more information, see [Deploy model from registry to online endpoint in workspace](how-to-share-models-pipelines-across-workspaces-with-registries.md#deploy-model-from-registry-to-online-endpoint-in-workspace).
1. Update applications that invoke endpoints so that the applications use the scoring URIs of the new online endpoints.
1. After you validate your new endpoints, delete the online endpoints in your old workspace.

If you don't need to avoid downtime during migration, you can take a more straightforward approach. If you don't need to maintain compute instances, online endpoints, and deployments in your old workspace, you can delete the compute instances and then update the workspace to enable a managed virtual network.

## Limitations

[!INCLUDE [machine-learning-managed-vnet-online-endpoint-limitations](includes/machine-learning-managed-vnet-online-endpoint-limitations.md)]

## Prepare your system

1. Create environment variables by running the following commands. Replace `<resource-group-name>` with the resource group for your workspace. Replace `<workspace-name>` with the name of your workspace.

   ```azurecli
   export RESOURCEGROUP_NAME="<resource-group-name>"
   export WORKSPACE_NAME="<workspace-name>"
   ```

1. Create your workspace. The `-m allow_only_approved_outbound` parameter configures a managed virtual network for the workspace and blocks outbound traffic except to approved destinations.

   :::code language="azurecli" source="~/azureml-examples-main/cli/deploy-managed-online-endpoint-workspacevnet.sh" ID="create_workspace_allow_only_approved_outbound" :::

   Alternatively, if you'd like to allow the deployment to send outbound traffic to the internet, uncomment the following code and run it instead.

   :::code language="azurecli" source="~/azureml-examples-main/cli/deploy-managed-online-endpoint-workspacevnet.sh" ID="create_workspace_internet_outbound" :::

   For more information about how to create a new workspace or upgrade your existing workspace to use a managed virtual network, see [Configure a managed virtual network to allow internet outbound](how-to-managed-network.md#configure-a-managed-virtual-network-to-allow-internet-outbound).

1. Provision the managed virtual network. For instructions and more information, see [Manually provision a managed VNet](how-to-managed-network.md#manually-provision-a-managed-vnet).

   > [!IMPORTANT]
   > When you set up a managed virtual network for a workspace for the first time, the network isn't provisioned. You can't create online deployments until you provision the managed network.

1. Configure the container registry that's associated with the workspace to use a premium pricing plan. This setting is needed to provide access to the registry via a private endpoint. For more information, see [Azure Container Registry service tiers](/azure/container-registry/container-registry-skus).

1. Configure your workspace to use a compute cluster or compute instance to build images. You can use the `image_build_compute` property for this purpose. For more information and instructions, see [Configure image builds](how-to-managed-network.md#configure-image-builds).

1. Configure default values for the Azure CLI so that you can avoid passing in the values for your workspace and resource group multiple times.

   ```azurecli
   az configure --defaults workspace=$WORKSPACE_NAME group=$RESOURCEGROUP_NAME
   ```

1. Clone the examples repository to get the example files for the endpoint and deployment, and then go to the repository's cli directory.

   ```azurecli
   git clone --depth 1 https://github.com/Azure/azureml-examples
   cd azureml-examples/cli
   ```

The commands in this article are in the deploy-managed-online-endpoint-workspacevnet.sh file in the cli directory. The YAML configuration files are in the endpoints/online/managed/sample/ subdirectory.

## Create a secured managed online endpoint

To create a secured managed online endpoint, you create the endpoint in your workspace. Then you set the endpoint's `public_network_access` value to `disabled` to control inbound communication.

This setting forces the online endpoint to use the workspace's private endpoint for inbound communication. The only way to invoke the online endpoint is by using a private endpoint that can access the workspace in your virtual network. For more information, see [Secure inbound scoring requests](concept-secure-online-endpoint.md#secure-inbound-scoring-requests) and [Configure a private endpoint for an Azure Machine Learning workspace](how-to-configure-private-link.md).

Because the workspace is configured to have a managed virtual network, any endpoint deployments use the private endpoints of the managed virtual network for outbound communication.

1. Set the endpoint's name:

   :::code language="azurecli" source="~/azureml-examples-main/cli/deploy-managed-online-endpoint-workspacevnet.sh" ID="set_endpoint_name" :::

1. Create an endpoint with `public_network_access` set to `disabled` to block inbound traffic:

   > [!NOTE]
   > The referenced script uses YAML configuration files from the cloned repository. Ensure you're in the correct directory (cli) after cloning the repository, or provide the full path to your YAML files. In Azure Cloud Shell, verify the files are accessible in your cloud storage before running the commands.

   :::code language="azurecli" source="~/azureml-examples-main/cli/deploy-managed-online-endpoint-workspacevnet.sh" ID="create_endpoint_inbound_blocked" :::

   Alternatively, if you want to allow the endpoint to receive scoring requests from the internet, uncomment the following code and run it instead:

   :::code language="azurecli" source="~/azureml-examples-main/cli/deploy-managed-online-endpoint-workspacevnet.sh" ID="create_endpoint_inbound_allowed" :::

## Test the endpoint

1. Create a deployment in the managed virtual network of the workspace:

   :::code language="azurecli" source="~/azureml-examples-main/cli/deploy-managed-online-endpoint-workspacevnet.sh" ID="create_deployment" :::

   If you get an error about an authorization failure, check the networking configuration for the workspace storage account. You might have to adjust the public network access settings to give the workspace access to the storage account.

1. Get the status of the deployment:

   :::code language="azurecli" source="~/azureml-examples-main/cli/deploy-managed-online-endpoint-workspacevnet.sh" ID="get_status" :::

1. Test the endpoint by issuing a scoring request:

   :::code language="azurecli" source="~/azureml-examples-main/cli/deploy-managed-online-endpoint-workspacevnet.sh" ID="test_endpoint" :::

1. Get the deployment logs:

   :::code language="azurecli" source="~/azureml-examples-main/cli/deploy-managed-online-endpoint-workspacevnet.sh" ID="get_logs" :::

## Clean up resources

1. If you no longer need the endpoint, run the following command to delete it.

   :::code language="azurecli" source="~/azureml-examples-main/cli/deploy-managed-online-endpoint-workspacevnet.sh" ID="delete_endpoint" :::

1. If you no longer need the workspace, its associated resources, and the other resources in your resource group, delete them. Replace `<resource-group-name>` with the name of the resource group that contains your workspace.

   ```azurecli
   az group delete --resource-group <resource-group-name>
   ```

## Troubleshooting

[!INCLUDE [network isolation issues](includes/machine-learning-online-endpoint-troubleshooting.md)]

## Related content

- [Network isolation with managed online endpoints](concept-secure-online-endpoint.md)
- [Workspace managed network isolation](how-to-managed-network.md)
- [Troubleshoot online endpoint deployment and scoring](how-to-troubleshoot-online-endpoints.md)
