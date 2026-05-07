---
title: Include file
description: Include file
author: alvinashcraft
ms.reviewer: shiyingfu
ms.author: aashcraft
ms.service: microsoft-foundry
ms.topic: include
ms.date: 05/07/2026
ms.custom: include, classic-and-new
ai-usage: ai-assisted
---

This article contains brief example templates to help get you started programmatically creating Azure OpenAI deployments that use quota to set TPM rate limits. With the introduction of quota you must use API version `2023-05-01` for resource management related activities. This API version is only for managing your resources, and doesn't impact the API version used for inferencing calls like completions, chat completions, embedding, image generation, etc.

# [REST](#tab/rest)

### Deployment

```http
PUT https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/deployments/{deploymentName}?api-version=2023-05-01
```

**Path parameters**

| Parameter | Type | Required? |  Description |
|--|--|--|--|
| ```accountName``` | string |  Required | The name of your Azure OpenAI Resource. |
| ```deploymentName``` | string | Required | The deployment name you chose when you deployed an existing model or the name you would like a new model deployment to have.   |
| ```resourceGroupName``` | string |  Required | The name of the associated resource group for this model deployment. |
| ```subscriptionId``` | string |  Required | Subscription ID for the associated subscription. |
| ```api-version``` | string | Required |The API version to use for this operation. This follows the YYYY-MM-DD format. |

**Supported versions**

- `2023-05-01` [Swagger spec](https://github.com/Azure/azure-rest-api-specs/blob/1e71ad94aeb8843559d59d863c895770560d7c93/specification/cognitiveservices/resource-manager/Microsoft.CognitiveServices/stable/2023-05-01/cognitiveservices.json)

**Request body**

This is only a subset of the available request body parameters. For the full list of the parameters, you can refer to the [REST API reference documentation](/rest/api/aiservices/accountmanagement/deployments/create-or-update?tabs=HTTP).

|Parameter|Type| Description |
|--|--|--|
|sku | Sku | The resource model definition representing SKU.|
|capacity|integer|This represents the amount of quota you're assigning to this deployment. A value of 1 equals 1,000 Tokens per Minute (TPM). A value of 10 equals 10k Tokens per Minute (TPM).|

#### Example request

```Bash
curl -X PUT https://management.azure.com/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resource-group-temp/providers/Microsoft.CognitiveServices/accounts/docs-openai-test-001/deployments/gpt-4o-test-deployment?api-version=2023-05-01 \
  -H "Content-Type: application/json" \
  -H 'Authorization: Bearer YOUR_AUTH_TOKEN' \
  -d '{"sku":{"name":"Standard","capacity":10},"properties": {"model": {"format": "OpenAI","name": "gpt-4o","version": "2024-11-20"}}}'
```

> [!NOTE]
> There are multiple ways to generate an authorization token. The easiest method for initial testing is to launch the Cloud Shell from the [Azure portal](https://portal.azure.com). Then run [`az account get-access-token`](/cli/azure/account?view=azure-cli-latest&preserve-view=true#az-account-get-access-token). You can use this token as your temporary authorization token for API testing.

For more information, see the REST API reference documentation for [usages](/rest/api/aiservices/accountmanagement/usages/list?branch=main&tabs=HTTP) and [deployment](/rest/api/aiservices/accountmanagement/deployments/create-or-update).

### Usage

To query your quota usage in a given region, for a specific subscription

```html
GET https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.CognitiveServices/locations/{location}/usages?api-version=2023-05-01
```
**Path parameters**

| Parameter | Type | Required? |  Description |
|--|--|--|--|
| ```subscriptionId``` | string |  Required | Subscription ID for the associated subscription. |
|```location```        | string | Required | Location to view usage for ex: `eastus` |
| ```api-version``` | string | Required |The API version to use for this operation. This follows the YYYY-MM-DD format. |

**Supported versions**

- `2023-05-01` [Swagger spec](https://github.com/Azure/azure-rest-api-specs/blob/1e71ad94aeb8843559d59d863c895770560d7c93/specification/cognitiveservices/resource-manager/Microsoft.CognitiveServices/stable/2023-05-01/cognitiveservices.json)

#### Example request

```Bash
curl -X GET https://management.azure.com/subscriptions/00000000-0000-0000-0000-000000000000/providers/Microsoft.CognitiveServices/locations/eastus/usages?api-version=2023-05-01 \
  -H "Content-Type: application/json" \
  -H 'Authorization: Bearer YOUR_AUTH_TOKEN' 
```

# [Azure CLI](#tab/cli)

Install the [Azure CLI](/cli/azure/install-azure-cli). Quota requires `Azure CLI version 2.51.0`. If you already have Azure CLI installed locally run `az upgrade` to update to the latest version.

To check which version of Azure CLI you're running use `az version`. Azure Cloud Shell is currently still running 2.50.0 so in the interim local installation of Azure CLI is required to take advantage of the latest Azure OpenAI features.

### Deployment

```azurecli
az cognitiveservices account deployment create --model-format
                                               --model-name
                                               --model-version
                                               --name
                                               --resource-group
                                               [--capacity]
                                               [--deployment-name]
                                               [--scale-capacity]
                                               [--scale-settings-scale-type {Manual, Standard}]
                                               [--sku]
```

To sign into your local installation of the CLI, run the [`az login`](/cli/azure/reference-index#az-login) command:

```azurecli
az login
```

<!--TODO:You can also use the green **Try It** button to run these commands in your browser in the Azure Cloud Shell.-->

By setting sku-capacity to 10 in the command below this deployment will be set with a 10K TPM limit.

```azurecli
az cognitiveservices account deployment create -g test-resource-group -n test-resource-name --deployment-name test-deployment-name --model-name gpt-4o --model-version "2024-11-20" --model-format OpenAI --sku-capacity 10 --sku-name "Standard"
```

### Usage

To [query your quota usage](/cli/azure/cognitiveservices/usage?view=azure-cli-latest&preserve-view=true) in a given region, for a specific subscription

```azurecli
az cognitiveservices usage list --location
```

### Example

```azurecli
az cognitiveservices usage list -l eastus
```

This command runs in the context of the currently active subscription for Azure CLI. Use `az-account-set --subscription` to [modify the active subscription](/cli/azure/manage-azure-subscriptions-azure-cli#change-the-active-subscription).

For more information, see the [Azure CLI reference documentation](/cli/azure/cognitiveservices/account/deployment?view=azure-cli-latest&preserve-view=true)

# [Azure PowerShell](#tab/powershell)

Install the latest version of the [Az PowerShell module](/powershell/azure/install-azure-powershell). If you already have the Az PowerShell module installed locally, run `Update-Module -Name Az` to update to the latest version.

To check which version of the Az PowerShell module you're running, use `Get-InstalledModule -Name Az`. Azure Cloud Shell is currently running a version of Azure PowerShell that can take advantage of the latest Azure OpenAI features.

### Deployment

```azurepowershell
New-AzCognitiveServicesAccountDeployment
   [-ResourceGroupName] <String>
   [-AccountName] <String>
   [-Name] <String>
   [-Properties] <DeploymentProperties>
   [-Sku] <Sku>
   [-DefaultProfile <IAzureContextContainer>]
   [-WhatIf]
   [-Confirm]
   [<CommonParameters>]
```

To sign into your local installation of Azure PowerShell, run the [Connect-AzAccount](/powershell/module/az.accounts/connect-azaccount) command:

```azurepowershell
Connect-AzAccount
```

By setting Sku Capacity to 10 in the command below, this deployment is set to a 10K TPM limit.

```azurepowershell-interactive
$cognitiveServicesDeploymentParams = @{
    ResourceGroupName = 'test-resource-group'
    AccountName = 'test-resource-name'
    Name = 'test-deployment-name'
    Properties = @{
        Model = @{
            Name = 'gpt-4o'
            Version = '2024-11-20'
            Format  = 'OpenAI'
        }
    }
    Sku = @{
        Name = 'Standard'
        Capacity = '10'
    }
}
New-AzCognitiveServicesAccountDeployment @cognitiveServicesDeploymentParams
```

### Usage

To [query your quota usage](/powershell/module/az.cognitiveservices/get-azcognitiveservicesusage) in a given region for a specific subscription:

```azurepowershell
Get-AzCognitiveServicesUsage -Location <location>
```

### Example

```azurepowershell-interactive
Get-AzCognitiveServicesUsage -Location eastus
```

This command runs in the context of the currently active subscription for Azure PowerShell. Use `Set-AzContext` to [modify the active subscription](/powershell/azure/manage-subscriptions-azureps#change-the-active-subscription).

For more information on `New-AzCognitiveServicesAccountDeployment` and `Get-AzCognitiveServicesUsage`, see [Azure PowerShell reference documentation](/powershell/module/az.cognitiveservices/).

# [Azure Resource Manager](#tab/arm)

```json
//
// This Azure Resource Manager template shows how to use the new schema introduced in the 2023-05-01 API version to 
// create deployments that set the model version and the TPM limits for standard deployments.
//
{
    "type": "Microsoft.CognitiveServices/accounts/deployments",
    "apiVersion": "2023-05-01",
    "name": "arm-je-aoai-test-resource/arm-je-std-deployment",    // Update reference to parent Azure OpenAI resource
    "dependsOn": [
        "[resourceId('Microsoft.CognitiveServices/accounts', 'arm-je-aoai-test-resource')]"  // Update reference to parent Azure OpenAI resource
    ],
    "sku": {
        "name": "Standard",      
        "capacity": 10            // The deployment will be created with a 10K TPM limit
    },
    "properties": {
        "model": {
            "format": "OpenAI",
            "name": "gpt-4o",
            "version": "2024-11-20"       
        }
    }
}
```

For more information, see the [full Azure Resource Manager reference documentation](/azure/templates/microsoft.cognitiveservices/accounts/deployments?pivots=deployment-language-arm-template).

# [Bicep](#tab/bicep)

```bicep
//
// This Bicep template shows how to use the new schema introduced in the 2023-05-01 API version to 
// create deployments that set the model version and the TPM limits for standard deployments.
//
resource arm_je_std_deployment 'Microsoft.CognitiveServices/accounts/deployments@2023-05-01' = {
  parent: arm_je_aoai_resource   // Replace this with a reference to the parent Azure OpenAI resource
  name: 'arm-je-std-deployment'
  sku: {
    name: 'Standard'            
    capacity: 10                 // The deployment will be created with a 10K TPM limit
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: 'gpt-4o'
      version: '2024-11-20'          
    }
  }
}
```

For more information, see the [full Bicep reference documentation](/azure/templates/microsoft.cognitiveservices/accounts/deployments?pivots=deployment-language-bicep).

# [Terraform](#tab/terraform)

```terraform
# This Terraform template shows how to use the new schema introduced in the 2023-05-01 API version to 
# create deployments that set the model version and the TPM limits for standard deployments.
# 
# The new schema is not yet available in the AzureRM provider (target v4.0), so this template uses the AzAPI
# provider, which provides a Terraform-compatible interface to the underlying ARM structures.
# 
# For more details on these providers:
#     AzureRM: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs
#     AzAPI: https://registry.terraform.io/providers/azure/azapi/latest/docs
#

# 
terraform {
  required_providers {
    azapi   = { source  = "Azure/azapi" }
    azurerm = { source  = "hashicorp/azurerm" }
  }
}

provider "azapi" {
  # Insert auth info here as necessary
}

provider "azurerm" {
    # Insert auth info here as necessary  
    features {
    }
}

# 
# To create a complete example, AzureRM is used to create a new resource group and Azure OpenAI Resource
# 
resource "azurerm_resource_group" "TERRAFORM-AOAI-TEST-GROUP" {
  name     = "TERRAFORM-AOAI-TEST-GROUP"
  location = "canadaeast"
}

resource "azurerm_cognitive_account" "TERRAFORM-AOAI-TEST-ACCOUNT" {
  name                  = "terraform-aoai-test-account"
  location              = "canadaeast"
  resource_group_name   = azurerm_resource_group.TERRAFORM-AOAI-TEST-GROUP.name
  kind                  = "OpenAI"
  sku_name              = "S0"
  custom_subdomain_name = "terraform-test-account-"
  }

# 
# AzAPI is used to create the deployment so that the TPM limit and model versions can be set
#
resource "azapi_resource" "TERRAFORM-AOAI-STD-DEPLOYMENT" {
  type      = "Microsoft.CognitiveServices/accounts/deployments@2023-05-01"
  name      = "TERRAFORM-AOAI-STD-DEPLOYMENT"
  parent_id = azurerm_cognitive_account.TERRAFORM-AOAI-TEST-ACCOUNT.id

  body = jsonencode({
    sku = {                            # The sku object specifies the deployment type and limit in 2023-05-01
        name = "Standard",             
        capacity = 10                  # This deployment will be set with a 10K TPM limit
    },
    properties = {
        model = {
            format = "OpenAI",
            name = "gpt-4o",
            version = "2024-11-20"           
        }
    }
  })
}
```

For more information, see the [full Terraform reference documentation](/azure/templates/microsoft.cognitiveservices/accounts/deployments?pivots=deployment-language-terraform).

---

## Related content

- [Manage Azure OpenAI in Microsoft Foundry Models quota](../how-to/quota.md)
- [Azure OpenAI quotas and limits](../quotas-limits.md)
