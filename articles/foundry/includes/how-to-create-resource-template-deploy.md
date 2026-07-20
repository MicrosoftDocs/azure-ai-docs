---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.topic: include
ms.date: 04/15/2026
ms.custom: include
---

In this quickstart, you deploy a [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs) resource and project by using a [Microsoft Bicep](/azure/azure-resource-manager/bicep/overview) template. Bicep helps you create related resources in one coordinated deployment and reuse the same configuration across environments.

If you already configured a Foundry resource in the Azure portal, you can [export that configuration as a Bicep file](#export-an-existing-resource-to-a-bicep-file) instead of authoring a template from scratch.

> [!TIP]
> For production-ready Bicep templates that cover common Foundry deployment scenarios, see the [infrastructure-setup-bicep](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep) folder in the Foundry samples repository. Clone the repository and customize the templates instead of starting from scratch.

## Prerequisites

[!INCLUDE [azure-subscription](../includes/azure-subscription.md)]

- [!INCLUDE [rbac-assign-roles](../includes/rbac-assign-roles.md)]
- [Install the Bicep CLI](/azure/azure-resource-manager/bicep/install).

Get the sample files:

# [Azure CLI](#tab/cli)

```azurecli
git clone https://github.com/microsoft-foundry/foundry-samples
cd foundry-samples/infrastructure/infrastructure-setup-bicep/00-basic
```

# [Azure PowerShell](#tab/powershell)

```azurepowershell
git clone https://github.com/microsoft-foundry/foundry-samples
cd foundry-samples/infrastructure/infrastructure-setup-bicep/00-basic
```

---

## Deploy the Bicep file

Deploy the Bicep file by using either Azure CLI or Azure PowerShell:

# [Azure CLI](#tab/cli)

```azurecli
az group create --name exampleRG --location eastus
az deployment group create --resource-group exampleRG --template-file main.bicep --parameters aiFoundryName=myai aiProjectName=myai-proj 
```

Reference: [az group create](/cli/azure/group#az-group-create), [az deployment group create](/cli/azure/deployment/group#az-deployment-group-create).

# [Azure PowerShell](#tab/powershell)

```azurepowershell
New-AzResourceGroup -Name exampleRG -Location eastus
New-AzResourceGroupDeployment -ResourceGroupName exampleRG -TemplateFile main.bicep -aiFoundryName myai -aiProjectName myai-proj
```

Reference: [New-AzResourceGroup](/powershell/module/az.resources/new-azresourcegroup), [New-AzResourceGroupDeployment](/powershell/module/az.resources/new-azresourcegroupdeployment).

---

> [!NOTE]
> Replace `myai` with the name of your resource. `exampleRG` is the name of the resource group, and `eastus` is the Azure region where resources are deployed.

When the deployment finishes, you see a message indicating the deployment succeeded (output displays: `"provisioningState": "Succeeded"`). This confirms that your Foundry resource and project have been created.
