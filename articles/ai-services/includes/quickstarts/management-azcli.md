---
title: Create a Foundry resource using the Azure CLI
titleSuffix: Foundry Tools
description: Get started with Foundry Tools by using Azure CLI commands to create a Foundry resource.
manager: nitinme
ms.service: azure-ai-services
keywords: Foundry Tools, cognitive intelligence, cognitive solutions, ai services
ms.topic: quickstart
ms.date: 8/1/2024
ms.custom:
  - mode-api
  - devx-track-azurecli
  - ignite-2023
ms.devlang: azurecli
---

Use this quickstart to create a Foundry resource using [Azure Command-Line Interface (CLI)](/cli/azure/install-azure-cli) commands. 

## Prerequisites

* A valid Azure subscription - [Create one](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) for free.
* The [Azure CLI](/cli/azure/install-azure-cli) version 2.0 or later.
* Azure RBAC role to create resources. You need one of the following roles assigned on your Azure subscription or resource group:
  * Contributor
  * Owner
  * Custom role with `Microsoft.CognitiveServices/accounts/write` permission

## Install the Azure CLI and sign in

Install the [Azure CLI](/cli/azure/install-azure-cli). To sign into your local installation of the CLI, run the [az login](/cli/azure/reference-index#az-login) command:

```azurecli-interactive
az login
```

## Create a new resource group

Before you create a Foundry resource, you must have an Azure resource group to contain the resource. When you create a new resource, you can either create a new resource group, or use an existing one. This article shows how to create a new resource group.

To create a resource, you'll need one of the Azure locations available for your subscription. You can retrieve a list of available locations with the [az account list-locations](/cli/azure/account#az-account-list-locations) command. Most Foundry Tools can be accessed from several locations. Choose the one closest to you, or see which locations are available for the service.

> [!IMPORTANT]
> * Remember your Azure location, as you will need it when calling the Microsoft Foundry resources.
> * The availability of some Foundry Tools can vary by region. For more information, see [Azure products by region](https://azure.microsoft.com/global-infrastructure/services/?products=cognitive-services).

```azurecli-interactive
az account list-locations --query "[].{Region:name}" --out table
```

After you have your Azure location, create a new resource group in the Azure CLI using the [az group create](/cli/azure/group#az-group-create) command. In the example below, replace the Azure location `westus2` with one of the Azure locations available for your subscription.

```azurecli-interactive
az group create --name ai-services-resource-group --location westus2
```

## Create a Foundry resource

To create and subscribe to a new Foundry resource, use the [az cognitiveservices account create](/cli/azure/cognitiveservices/account#az-cognitiveservices-account-create) command. This command adds a new billable resource to the resource group you created earlier. When you create your new resource, you'll need to know the kind of service you want to use, along with its pricing tier (or SKU) and an Azure location.

> [!IMPORTANT]
> Azure provides more than one resource kinds for Foundry Tools. Be sure to create one with the `kind` of `AIServices`.

You can create a Foundry resource named `foundry-multi-service-resource` with the command below.

```azurecli-interactive
az cognitiveservices account create --name foundry-multi-service-resource --resource-group ai-services-resource-group  --kind AIServices --sku S0 --location westus2 --yes
```

> [!TIP]
> If your subscription doesn't allow you to create a Foundry resource, you might need to enable the privilege of that [Azure resource provider](/azure/azure-resource-manager/management/resource-providers-and-types#register-resource-provider) using the [Azure portal](/azure/azure-resource-manager/management/resource-providers-and-types#azure-portal), [PowerShell command](/azure/azure-resource-manager/management/resource-providers-and-types#azure-powershell) or an [Azure CLI command](/azure/azure-resource-manager/management/resource-providers-and-types#azure-cli). If you are not the subscription owner, ask someone with the role of *Owner* or *Admin* to complete the registration for you or ask for the **/register/action** privileges to be granted to your account.

## Get current quota usage for your resource

Use the [az cognitiveservices account list-usage](/cli/azure/cognitiveservices/account#az-cognitiveservices-account-list-usage) command to get the usage for your resource.

```azurecli-interactive
az cognitiveservices account list-usage --name foundry-multi-service-resource --resource-group ai-services-resource-group --subscription subscription-name
```

## Clean up resources

If you want to clean up and remove a Foundry resource, you can delete it or the resource group. Deleting the resource group also deletes any other resources contained in the group.

To remove the resource group and its associated resources, use the `az group delete command`.

```azurecli-interactive
az group delete --name ai-services-resource-group
```
