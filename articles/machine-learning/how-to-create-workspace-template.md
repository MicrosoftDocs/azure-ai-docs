---
title: Create a Workspace by Using an Azure Resource Manager Template
titleSuffix: Azure Machine Learning
description: Learn how to use an Azure Resource Manager template to create a new Azure Machine Learning workspace.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: enterprise-readiness
ms.topic: how-to
ms.custom: devx-track-azurepowershell, devx-track-arm-template, devx-track-azurecli, dev-focus
ms.author: scottpolly
author: s-polly
ms.reviewer: shshubhe
ms.date: 12/22/2025
ai-usage: ai-assisted
#Customer intent: As a DevOps deployment manager, I want to automate or customize the creation of Azure Machine Learning by using templates.
---

# Use an Azure Resource Manager template to create a workspace for Azure Machine Learning

In this article, you learn several ways to create an Azure Machine Learning workspace by using Azure Resource Manager templates. A Resource Manager template makes it easy to create resources in a single, coordinated operation. A template is a JSON document that defines the resources that are needed for a deployment. It might also specify deployment parameters. Parameters are used to provide input values during deployment.

For more information, see [Deploy an application with an Azure Resource Manager template](/azure/azure-resource-manager/templates/deploy-powershell).

## Prerequisites

* An Azure subscription. If you don't have one, try the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

* To use a template from a CLI, you need either [Azure PowerShell](/powershell/azure/) or the [Azure CLI](/cli/azure/install-azure-cli).


## Limitations

[!INCLUDE [register-namespace](includes/machine-learning-register-namespace.md)]

* The example template might not always use the latest API version for Azure Machine Learning. We recommend that you modify the template to use the latest API versions before you use it. For information on the latest API versions for Azure Machine Learning, see the pages for specific operation groups in the [Azure Machine Learning REST API](/rest/api/azureml/) documentation.

    > [!TIP]
    > Each Azure service has its own set of API versions. For information on the API for a specific service, check the service information in the [Azure REST API reference](/rest/api/azure/).

    To update the API version, find the `"apiVersion": "YYYY-MM-DD"` entry for the resource type and update it to the latest version. The following example is an entry for Azure Machine Learning:

    ```json
    "type": "Microsoft.MachineLearningServices/workspaces",
    "apiVersion": "2023-10-01",
    ```

### Multiple workspaces in the same virtual network

The template doesn't support deploying multiple Azure Machine Learning workspaces in the same virtual network. This is because the template creates new DNS zones during deployment.

If you want to create a template that deploys multiple workspaces in the same virtual network, set it up manually (by using the Azure portal or CLI). Then [use the Azure portal to generate a template](/azure/azure-resource-manager/templates/export-template-portal).

## About the Resource Manager template

You can get the Resource Manager template used throughout this document from the [microsoft.machinelearningservices/machine-learning-workspace-vnet](https://github.com/Azure/azure-quickstart-templates/blob/master/quickstarts/microsoft.machinelearningservices/machine-learning-workspace-vnet/azuredeploy.json) directory of the Azure Quickstart Templates GitHub repository.

This template creates the following Azure services:

* An Azure Storage account
* Azure Key Vault
* Application Insights
* Azure Container Registry
* An Azure Machine Learning workspace

 The Azure Machine Learning workspace uses these services for functionality like logging and storing data, secrets, and Docker images. The template also creates a resource group that contains the services.

The example template has two required parameters:

* The `location`, which specifies where to create the resources.

    The template uses the location you select for most resources. The exception is Application Insights, which isn't available in all of the locations that the other services are. If you select a location where it isn't available, the service is created in the South Central US location.

* The `workspaceName`, which is the friendly name of the Azure Machine Learning workspace.

    > [!NOTE]
    > The workspace name is case-insensitive.

    The names of the other services are generated randomly.

> [!TIP]
> Although the template associated with this document creates a container registry, you can also create a new workspace without creating a container registry. One will be created when you perform an operation that requires a container registry. For example, training or deploying a model.
>
> You can also reference an existing container registry or storage account in the Azure Resource Manager template, instead of creating a new one. If you do, you must either [use a managed identity](how-to-identity-based-service-authentication.md) or [enable the admin account](/azure/container-registry/container-registry-authentication#admin-account) for the container registry.

[!INCLUDE [machine-learning-delete-acr](includes/machine-learning-delete-acr.md)]

## Deploy the template

To deploy your template, you need to create a resource group.

See the [Azure portal](#use-the-azure-portal) section if you prefer to use the graphical user interface.

# [Azure CLI](#tab/azcli)


```azurecli
az group create --name "examplegroup" --location "eastus"
```

# [Azure PowerShell](#tab/azpowershell)

```azurepowershell
New-AzResourceGroup -Name "examplegroup" -Location "eastus"
```

---

After your resource group is created, deploy the template by using the following command:

# [Azure CLI](#tab/azcli)

```azurecli
az deployment group create \
    --name "exampledeployment" \
    --resource-group "examplegroup" \
    --template-uri "https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/quickstarts/microsoft.machinelearningservices/machine-learning-workspace-vnet/azuredeploy.json" \
    --parameters workspaceName="exampleworkspace" location="eastus"
```

# [Azure PowerShell](#tab/azpowershell)

```azurepowershell
New-AzResourceGroupDeployment `
  -Name "exampledeployment" `
  -ResourceGroupName "examplegroup" `
  -TemplateUri "https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/quickstarts/microsoft.machinelearningservices/machine-learning-workspace-vnet/azuredeploy.json" `
  -workspaceName "exampleworkspace" `
  -location "eastus"
```

---

After the deployment completes, verify that the workspace exists by using the Azure CLI. The `az ml workspace show` command requires the Azure Machine Learning extension (`az extension add --name ml`) and returns a `provisioningState` of `Succeeded` when the deployment finishes.

```azurecli
az ml workspace show \
  --name "exampleworkspace" \
  --resource-group "examplegroup" \
  --output table
```

By default, all resources created by the template are new. However, you can also use existing resources by including different parameters in the template. Key parameters you'll reuse across scenarios include:

* `workspaceName`: Sets the friendly name for the Azure Machine Learning workspace.
* `location`: Specifies the region for the workspace metadata and dependent services.
* `storageAccountOption`: Choose `new` or `existing` to control whether the template provisions storage.
* `storageAccountName`: Provide the name when you reference an existing storage account.
* `privateEndpointType`: Set to `AutoApproval` or `ManualApproval` when you deploy with private endpoints.
* `vnetOption`: Choose `new` or `existing` to decide how the workspace connects to a virtual network.
* `vnetName`: Supply the virtual network name whenever you integrate with a virtual network.

For example, if you want to use an existing storage account, set the `storageAccountOption` value to `existing`, and provide the name of your storage account in the `storageAccountName` parameter, as shown in the following command.

> [!IMPORTANT]
> If you want to use an existing Azure Storage account, it can't be a premium account (Premium_LRS or Premium_GRS). It also can't have a hierarchical namespace (which is used with Azure Data Lake Storage Gen2). Neither premium storage nor hierarchical namespaces are supported with the default storage account of the workspace. You can use premium storage or hierarchical namespace with non-default storage accounts.

# [Azure CLI](#tab/azcli)

```azurecli
az deployment group create \
    --name "exampledeployment" \
    --resource-group "examplegroup" \
    --template-uri "https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/quickstarts/microsoft.machinelearningservices/machine-learning-workspace-vnet/azuredeploy.json" \
    --parameters workspaceName="exampleworkspace" \
      location="eastus" \
      storageAccountOption="existing" \
      storageAccountName="existingstorageaccountname"
```

# [Azure PowerShell](#tab/azpowershell)

```azurepowershell
New-AzResourceGroupDeployment `
  -Name "exampledeployment" `
  -ResourceGroupName "examplegroup" `
  -TemplateUri "https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/quickstarts/microsoft.machinelearningservices/machine-learning-workspace-vnet/azuredeploy.json" `
  -workspaceName "exampleworkspace" `
  -location "eastus" `
  -storageAccountOption "existing" `
  -storageAccountName "existingstorageaccountname"
```

---

## Deploy an encrypted workspace

The following example template demonstrates how to create a workspace that has three settings:

* Enable high confidentiality settings for the workspace. This configuration creates a new Azure Cosmos DB instance.
* Enable encryption for the workspace.
* Use an existing Azure key vault to retrieve customer-managed keys. Customer-managed keys are used to create a new Azure Cosmos DB instance for the workspace.

> [!IMPORTANT]
> After a workspace is created, you can't change the settings for confidential data, encryption, key vault ID, or key identifiers. To change these values, you must create a new workspace that uses the new values.

For more information, see [Customer-managed keys](concept-customer-managed-keys.md).

> [!IMPORTANT]
> Your subscription must meet these requirements before you use this template:
> * You must have an existing Azure key vault that contains an encryption key.
> * The key vault must be in the same region where you plan to create the Azure Machine Learning workspace.
> * You must specify the ID of the key vault and the URI of the encryption key.
> * The key vault must have both soft delete and purge protection enabled.
> 
> For information about creating the vault and key, see [Configure customer-managed keys](how-to-setup-customer-managed-keys.md).

To get the values for the `cmk_keyvault` (the ID of the key vault) and the `resource_cmk_uri` (the key URI) parameters needed by this template, take the following steps:    

1. To get the key vault ID, use the following command:    

    # [Azure CLI](#tab/azcli)    
    
    ```azurecli    
    az keyvault show --name <keyvault-name> --query 'id' --output tsv    
    ```    
    
    # [Azure PowerShell](#tab/azpowershell)    
    
    ```azurepowershell    
    Get-AzKeyVault -VaultName '<keyvault-name>'    
    ```    
    ---    

    This command returns a value similar to `/subscriptions/{subscription-guid}/resourceGroups/<resource-group-name>/providers/Microsoft.KeyVault/vaults/<keyvault-name>`.    

1. To get the value for the URI for the customer-managed key, use the following command:    

    # [Azure CLI](#tab/azcli)    
    
    ```azurecli    
    az keyvault key show --vault-name <keyvault-name> --name <key-name> --query 'key.kid' --output tsv    
    ```    
    
    # [Azure PowerShell](#tab/azpowershell)    
    
    ```azurepowershell    
    Get-AzKeyVaultKey -VaultName '<keyvault-name>' -KeyName '<key-name>'    
    ```    
    ---    

  This command returns a value similar to `https://mykeyvault.vault.azure.net/keys/mykey/{guid}`.    

> [!IMPORTANT]    
> After a workspace is created, you can't change the settings for confidential data, encryption, key vault ID, or key identifiers. To change these values, you must create a new workspace that uses the new values.

To enable the use of customer-managed keys, set the following parameters when deploying the template:

* Set `encryption_status` to `Enabled`.
* Set `cmk_keyvault` to the `cmk_keyvault` value obtained in the preceding steps.
* Set `resource_cmk_uri` to the `resource_cmk_uri` value obtained in the preceding steps.

# [Azure CLI](#tab/azcli)

```azurecli
az deployment group create \
    --name "exampledeployment" \
    --resource-group "examplegroup" \
    --template-uri "https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/quickstarts/microsoft.machinelearningservices/machine-learning-workspace-vnet/azuredeploy.json" \
    --parameters workspaceName="exampleworkspace" \
      location="eastus" \
      encryption_status="Enabled" \
      cmk_keyvault="/subscriptions/{subscription-guid}/resourceGroups/<resource-group-name>/providers/Microsoft.KeyVault/vaults/<keyvault-name>" \
      resource_cmk_uri="https://mykeyvault.vault.azure.net/keys/mykey/{guid}"
```

# [Azure PowerShell](#tab/azpowershell)

```azurepowershell
New-AzResourceGroupDeployment `
  -Name "exampledeployment" `
  -ResourceGroupName "examplegroup" `
  -TemplateUri "https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/quickstarts/microsoft.machinelearningservices/machine-learning-workspace-vnet/azuredeploy.json" `
  -workspaceName "exampleworkspace" `
  -location "eastus" `
  -encryption_status "Enabled" `
  -cmk_keyvault "/subscriptions/{subscription-guid}/resourceGroups/<resource-group-name>/providers/Microsoft.KeyVault/vaults/<keyvault-name>" `
  -resource_cmk_uri "https://mykeyvault.vault.azure.net/keys/mykey/{guid}"
```
---

When you use a customer-managed key, Azure Machine Learning creates a secondary resource group that contains the Azure Cosmos DB instance. For more information, see [Encryption at rest in Azure Cosmos DB](concept-data-encryption.md#encryption-at-rest).

You can optionally set the `confidential_data` parameter to `true`. Doing so enables the following behavior:

* Starts encrypting the local scratch disk for Azure Machine Learning compute clusters, if you haven't created any clusters in your subscription. If you have previously created a cluster in the subscription, open a support ticket to have encryption of the scratch disk enabled for your compute clusters.
* Cleans up the local scratch disk between jobs.
* Securely passes credentials for the storage account, container registry, and SSH account from the execution layer to your compute clusters by using Key Vault.
* Enables IP filtering to ensure that no external services other than AzureMachineLearningService can call the underlying batch pools.

  For more information, see [Encryption at rest](concept-data-encryption.md#encryption-at-rest).

## Deploy a workspace behind a virtual network

By setting the `vnetOption` parameter value to either `new` or `existing`, you can create the resources used by a workspace behind a virtual network.

> [!IMPORTANT]
> For Container Registry, only the Premium SKU is supported.

> [!IMPORTANT]
> Application Insights doesn't support deployment behind a virtual network.

### Only deploy the workspace behind a private endpoint

If your associated resources aren't behind a virtual network, you can set the `privateEndpointType` parameter to `AutoApproval` or `ManualApproval` to deploy the workspace behind a private endpoint. This setting can be used for both new and existing workspaces. When updating an existing workspace, configure the template parameters with the information from the existing workspace.

# [Azure CLI](#tab/azcli)

```azurecli
az deployment group create \
    --name "exampledeployment" \
    --resource-group "examplegroup" \
    --template-uri "https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/quickstarts/microsoft.machinelearningservices/machine-learning-workspace-vnet/azuredeploy.json" \
    --parameters workspaceName="exampleworkspace" \
      location="eastus" \
      privateEndpointType="AutoApproval"
```

# [Azure PowerShell](#tab/azpowershell)

```azurepowershell
New-AzResourceGroupDeployment `
  -Name "exampledeployment" `
  -ResourceGroupName "examplegroup" `
  -TemplateUri "https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/quickstarts/microsoft.machinelearningservices/machine-learning-workspace-vnet/azuredeploy.json" `
  -workspaceName "exampleworkspace" `
  -location "eastus" `
  -privateEndpointType "AutoApproval"
```

---

### Use a new virtual network

To deploy a resource behind a new virtual network, set the `vnetOption` to `new` and provide the virtual network settings for the resource. The following example shows how to deploy a workspace and deploy the storage account resource behind a new virtual network.

# [Azure CLI](#tab/azcli)

```azurecli
az deployment group create \
    --name "exampledeployment" \
    --resource-group "examplegroup" \
    --template-uri "https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/quickstarts/microsoft.machinelearningservices/machine-learning-workspace-vnet/azuredeploy.json" \
    --parameters workspaceName="exampleworkspace" \
      location="eastus" \
      vnetOption="new" \
      vnetName="examplevnet" \
      storageAccountBehindVNet="true" \
      privateEndpointType="AutoApproval"
```

# [Azure PowerShell](#tab/azpowershell)

```azurepowershell
New-AzResourceGroupDeployment `
  -Name "exampledeployment" `
  -ResourceGroupName "examplegroup" `
  -TemplateUri "https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/quickstarts/microsoft.machinelearningservices/machine-learning-workspace-vnet/azuredeploy.json" `
  -workspaceName "exampleworkspace" `
  -location "eastus" `
  -vnetOption "new" `
  -vnetName "examplevnet" `
  -storageAccountBehindVNet "true" `
  -privateEndpointType "AutoApproval"
```

---

Alternatively, you can deploy multiple or all dependent resources behind a virtual network:

# [Azure CLI](#tab/azcli)

```azurecli
az deployment group create \
    --name "exampledeployment" \
    --resource-group "examplegroup" \
    --template-uri "https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/quickstarts/microsoft.machinelearningservices/machine-learning-workspace-vnet/azuredeploy.json" \
    --parameters workspaceName="exampleworkspace" \
      location="eastus" \
      vnetOption="new" \
      vnetName="examplevnet" \
      storageAccountBehindVNet="true" \
      keyVaultBehindVNet="true" \
      containerRegistryBehindVNet="true" \
      containerRegistryOption="new" \
      containerRegistrySku="Premium" \
      privateEndpointType="AutoApproval"
```

# [Azure PowerShell](#tab/azpowershell)

```azurepowershell
New-AzResourceGroupDeployment `
  -Name "exampledeployment" `
  -ResourceGroupName "examplegroup" `
  -TemplateUri "https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/quickstarts/microsoft.machinelearningservices/machine-learning-workspace-vnet/azuredeploy.json" `
  -workspaceName "exampleworkspace" `
  -location "eastus" `
  -vnetOption "new" `
  -vnetName "examplevnet" `
  -storageAccountBehindVNet "true" `
  -keyVaultBehindVNet "true" `
  -containerRegistryBehindVNet "true" `
  -containerRegistryOption "new" `
  -containerRegistrySku "Premium" `
  -privateEndpointType "AutoApproval"
```

---

### Use an existing virtual network and existing resources

To deploy a workspace with existing resources, you have to set the `vnetOption` parameter and subnet parameters to `existing`. However, you need to create service endpoints in the virtual network for each of the resources before deployment. As with new virtual network deployments, you can place one or all of your resources behind a virtual network.

> [!IMPORTANT]
> Subnets should have a `Microsoft.Storage` service endpoint.

> [!IMPORTANT]
> Subnets don't support private endpoints. Disable private endpoints to enable subnets.

1. Enable service endpoints for the resources:

    # [Azure CLI](#tab/azcli)
      
    ```azurecli
    az network vnet subnet update --resource-group "examplegroup" --vnet-name "examplevnet" --name "examplesubnet" --service-endpoints "Microsoft.Storage"
    az network vnet subnet update --resource-group "examplegroup" --vnet-name "examplevnet" --name "examplesubnet" --service-endpoints "Microsoft.KeyVault"
    az network vnet subnet update --resource-group "examplegroup" --vnet-name "examplevnet" --name "examplesubnet" --service-endpoints "Microsoft.ContainerRegistry"
    ```
        
    # [Azure PowerShell](#tab/azpowershell)
      
    ```azurepowershell
    Get-AzVirtualNetwork -ResourceGroupName "examplegroup" -Name "examplevnet" | Set-AzVirtualNetworkSubnetConfig -Name "examplesubnet" -AddressPrefix "<subnet prefix>" -ServiceEndpoint "Microsoft.Storage" | Set-AzVirtualNetwork
    Get-AzVirtualNetwork -ResourceGroupName "examplegroup" -Name "examplevnet" | Set-AzVirtualNetworkSubnetConfig -Name "examplesubnet" -AddressPrefix "<subnet prefix>" -ServiceEndpoint "Microsoft.KeyVault" | Set-AzVirtualNetwork
    Get-AzVirtualNetwork -ResourceGroupName "examplegroup" -Name "examplevnet" | Set-AzVirtualNetworkSubnetConfig -Name "examplesubnet" -AddressPrefix "<subnet prefix>" -ServiceEndpoint "Microsoft.ContainerRegistry" | Set-AzVirtualNetwork
    ```
    
    ---

1. Deploy the workspace:

    # [Azure CLI](#tab/azcli)
    
    ```azurecli
    az deployment group create \
    --name "exampledeployment" \
    --resource-group "examplegroup" \
    --template-uri "https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/quickstarts/microsoft.machinelearningservices/machine-learning-workspace-vnet/azuredeploy.json" \
    --parameters workspaceName="exampleworkspace" \
      location="eastus" \
      vnetOption="existing" \
      vnetName="examplevnet" \
      vnetResourceGroupName="examplegroup" \
      storageAccountBehindVNet="true" \
      keyVaultBehindVNet="true" \
      containerRegistryBehindVNet="true" \
      containerRegistryOption="new" \
      containerRegistrySku="Premium" \
      subnetName="examplesubnet" \
      subnetOption="existing" \
      privateEndpointType="AutoApproval"
    ```
    
    # [Azure PowerShell](#tab/azpowershell)
    
    ```azurepowershell
    New-AzResourceGroupDeployment `
      -Name "exampledeployment" `
      -ResourceGroupName "examplegroup" `
      -TemplateUri "https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/quickstarts/microsoft.machinelearningservices/machine-learning-workspace-vnet/azuredeploy.json" `
      -workspaceName "exampleworkspace" `
      -location "eastus" `
      -vnetOption "existing" `
      -vnetName "examplevnet" `
      -vnetResourceGroupName "examplegroup" `
      -storageAccountBehindVNet "true"
      -keyVaultBehindVNet "true" `
      -containerRegistryBehindVNet "true" `
      -containerRegistryOption "new" `
      -containerRegistrySku "Premium" `
      -subnetName "examplesubnet" `
      -subnetOption "existing"
      -privateEndpointType "AutoApproval"
    ```
    ---

## Use the Azure portal

1. Complete the steps in [Deploy resources from custom template](/azure/azure-resource-manager/templates/deploy-portal#deploy-resources-from-custom-template). When you get to the __Custom deployment__ pane, select __Quickstart template__.
1. In the __Quickstart template__ list, select **quickstarts/microsoft.machinelearningservices/machine-learning-workspace-vnet**. Finally, select **Select template**.
1. On the **Custom deployment** page, provide the following required information and any other parameters required by your deployment scenario.

   * Subscription: Select the Azure subscription to use for the resources.
   * Resource group: Select or create the resource group to contain the services.
   * Region: Select the Azure region to create the resources in.
   * Workspace name: Enter a name for the Azure Machine Learning workspace. The workspace name must be between 3 and 33 characters. It can contain only alphanumeric characters and the `-` character.
   * Location: Select the location for the deployment metadata. This location can be the same as the region location, or it can be different. 
  * VNet name: Enter a virtual network name. 
1. Select __Review + create__.
1. Select __Create__.

For more information, see [Deploy resources from custom template](/azure/azure-resource-manager/templates/deploy-portal#deploy-resources-from-custom-template).

## Troubleshooting

### Resource provider errors

[!INCLUDE [machine-learning-resource-provider](includes/machine-learning-resource-provider.md)]

### Key Vault access policy and Resource Manager templates

You might encounter failures if you use a Resource Manager template to create a workspace and associated resources (including Key Vault), multiple times. For example, using a template multiple times with the same parameters as part of a continuous integration and deployment pipeline can lead to failures.

Most resource creation operations that run via templates are idempotent, but Key Vault clears the access policies each time the template is used. Clearing the access policies creates problems with accessing the key vault for any workspace that's using it. For example, stop and create operations of Azure notebook VMs might fail.  

To avoid this problem, we recommend one of the following approaches:

* Don't deploy a template more than once with the same parameters. Or delete existing resources before using the template to re-create them.

* Examine the Key Vault access policies and use these policies to set the `accessPolicies` property of the template. To view the access policies, use the following Azure CLI command:

    ```azurecli
    az keyvault show --name mykeyvault --resource-group myresourcegroup --query properties.accessPolicies
    ```

    For more information on using the `accessPolicies` section of the template, see the [AccessPolicyEntry object reference](/azure/templates/Microsoft.KeyVault/2018-02-14/vaults#AccessPolicyEntry).

* Check whether the Key Vault resource already exists. If it does, don't re-create it by using the template. For example, to use the existing Key Vault instead of creating a new one, make the following changes in the template:

    * Add a parameter that accepts the ID of an existing Key Vault resource:

        ```json
        "keyVaultId":{
          "type": "string",
          "metadata": {
            "description": "Specify the existing Key Vault ID."
          }
        }
      ```

    * Remove the section that creates a Key Vault resource:

        ```json
        {
          "type": "Microsoft.KeyVault/vaults",
          "apiVersion": "2018-02-14",
          "name": "[variables('keyVaultName')]",
          "location": "[parameters('location')]",
          "properties": {
            "tenantId": "[variables('tenantId')]",
            "sku": {
              "name": "standard",
              "family": "A"
            },
            "accessPolicies": [
            ]
          }
        },
        ```

    * Remove the `"[resourceId('Microsoft.KeyVault/vaults', variables('keyVaultName'))]",` line from the `dependsOn` section of the workspace. Also change the `keyVault` entry in the `properties` section of the workspace to reference the `keyVaultId` parameter:

        ```json
        {
          "type": "Microsoft.MachineLearningServices/workspaces",
          "apiVersion": "2019-11-01",
          "name": "[parameters('workspaceName')]",
          "location": "[parameters('location')]",
          "dependsOn": [
            "[resourceId('Microsoft.Storage/storageAccounts', variables('storageAccountName'))]",
            "[resourceId('Microsoft.Insights/components', variables('applicationInsightsName'))]"
          ],
          "identity": {
            "type": "systemAssigned"
          },
          "sku": {
            "tier": "[parameters('sku')]",
            "name": "[parameters('sku')]"
          },
          "properties": {
            "friendlyName": "[parameters('workspaceName')]",
            "keyVault": "[parameters('keyVaultId')]",
            "applicationInsights": "[resourceId('Microsoft.Insights/components',variables('applicationInsightsName'))]",
            "storageAccount": "[resourceId('Microsoft.Storage/storageAccounts/',variables('storageAccountName'))]"
          }
        }
        ```

    After you make these changes, you can specify the ID of the existing Key Vault resource when running the template. The template then reuses the key vault by setting the `keyVault` property of the workspace to its ID.

    To get the ID of the key vault, you can reference the output of the original template job or use the Azure CLI. The following command shows how to use the Azure CLI to get the key vault resource ID:

    ```azurecli
    az keyvault show --name mykeyvault --resource-group myresourcegroup --query id
    ```

    This command returns a value similar to this:

    ```text
    /subscriptions/{subscription-guid}/resourceGroups/myresourcegroup/providers/Microsoft.KeyVault/vaults/mykeyvault
    ```

## Related content

* [Deploy resources with Resource Manager templates and Resource Manager REST API](/azure/azure-resource-manager/templates/deploy-rest)
* [Creating and deploying Azure resource groups through Visual Studio](/azure/azure-resource-manager/templates/create-visual-studio-deployment-project)
* [Write Azure Resource Manager templates](/azure/azure-resource-manager/templates/syntax)
* [Deploy an application with Azure Resource Manager templates](/azure/azure-resource-manager/templates/deploy-powershell)
* [Microsoft.MachineLearningServices resource types](/azure/templates/microsoft.machinelearningservices/allversions)
* [Get other templates related to Azure Machine Learning](https://github.com/Azure/azure-quickstart-templates)
* [How to use workspace diagnostics](how-to-workspace-diagnostic-api.md)
* [Move an Azure Machine Learning workspace to another subscription](how-to-move-workspace.md)
