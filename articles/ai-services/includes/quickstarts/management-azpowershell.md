---
title: Create a Foundry resource using Azure PowerShell
titleSuffix: Foundry Tools
description: Get started with Foundry Tools by using Azure PowerShell commands to create a Foundry resource.
manager: nitinme
ms.service: azure-ai-services
keywords: Foundry Tools, cognitive intelligence, cognitive solutions, ai services
ms.topic: include
ms.date: 8/1/2024
ms.custom:
  - mode-api
  - devx-track-azurepowershell
  - ignite-2023
ms.devlang: azurepowershell
---

Use this quickstart to create a Foundry resource using [Azure PowerShell](/powershell/azure/install-azure-powershell) commands. 

## Prerequisites

* A valid Azure subscription - [Create one](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) for free.
* [Azure PowerShell](/powershell/azure/install-azure-powershell) version 5.0 or later.
* Azure RBAC role to create resources. You need one of the following roles assigned on your Azure subscription or resource group:
  * Contributor
  * Owner
  * Custom role with `Microsoft.CognitiveServices/accounts/write` permission

## Install Azure PowerShell and sign in

Install [Azure PowerShell](/powershell/azure/install-azure-powershell). To sign in, run the [Connect-AzAccount](/powershell/module/az.accounts/connect-azaccount) command:

```azurepowershell
Connect-AzAccount
```

## Create a new Microsoft Foundry resource group

Before you create a Foundry resource, you must have an Azure resource group to contain the resource. When you create a new resource, you can either create a new resource group, or use an existing one. This article shows how to create a new resource group.

To create a resource, you'll need one of the Azure locations available for your subscription. You can retrieve a list of available locations with the [Get-AzLocation](/powershell/module/az.resources/get-azlocation) command. Most Foundry Tools can be accessed from several locations. Choose the one closest to you, or see which locations are available for the service.

> [!IMPORTANT]
> * Remember your Azure location, as you will need it when calling the Foundry resources.
> * The availability of some Foundry Tools can vary by region. For more information, see [Azure products by region](https://azure.microsoft.com/global-infrastructure/services/?products=cognitive-services).

```azurepowershell-interactive
Get-AzLocation | Select-Object -Property Location, DisplayName
```

After you have your Azure location, create a new resource group in Azure PowerShell using the [New-AzResourceGroup](/powershell/module/az.resources/new-azresourcegroup) command. In the example below, replace the Azure location `westus2` with one of the Azure locations available for your subscription.

```azurepowershell-interactive
New-AzResourceGroup -Name ai-services-resource-group -Location westus2
```

## Create a Foundry resource

To create and subscribe to a new Foundry resource, use the [New-AzCognitiveServicesAccount](/powershell/module/az.cognitiveservices/new-azcognitiveservicesaccount) command. This command adds a new billable resource to the resource group you created earlier. When you create your new resource, you'll need to know the "kind" of service you want to use, along with its pricing tier (or SKU) and an Azure location:

> [!IMPORTANT]
> Azure provides more than one resource kinds for Foundry Tools. Be sure to create one with the `Type` (kind) of `AIServices`.

You can create a Foundry resource named `foundry-multi-service-resource` with the command below.

```azurepowershell-interactive
New-AzCognitiveServicesAccount -ResourceGroupName ai-services-resource-group -Name foundry-multi-service-resource -Type AIServices -SkuName S0 -Location westus2
```

> [!TIP]
> If your subscription doesn't allow you to create a Foundry resource, you might need to enable the privilege of that [Azure resource provider](/azure/azure-resource-manager/management/resource-providers-and-types#register-resource-provider) using the [Azure portal](/azure/azure-resource-manager/management/resource-providers-and-types#azure-portal), [PowerShell command](/azure/azure-resource-manager/management/resource-providers-and-types#azure-powershell) or an [Azure CLI command](/azure/azure-resource-manager/management/resource-providers-and-types#azure-cli). If you are not the subscription owner, ask someone with the role of *Owner* or *Admin* to complete the registration for you or ask for the **/register/action** privileges to be granted to your account.

## Get current quota usage for your resource

Use the [Get-AzCognitiveServicesAccountUsage](/powershell/module/az.cognitiveservices/get-azcognitiveservicesaccountusage) command to get the usage for your resource.

```azurepowershell-interactive
Get-AzCognitiveServicesAccountUsage -ResourceGroupName ai-services-resource-group -Name foundry-multi-service-resource
```

## Clean up resources

If you want to clean up and remove a Foundry resource, you can delete it or the resource group. Deleting the resource group also deletes any other resources contained in the group.

To remove the resource group and its associated resources, use the [Remove-AzResourceGroup](/powershell/module/az.resources/remove-azresourcegroup) command.

```azurepowershell-interactive
Remove-AzResourceGroup -Name ai-services-resource-group
```
