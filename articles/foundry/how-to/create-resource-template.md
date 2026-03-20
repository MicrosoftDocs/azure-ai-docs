---
title: "Quickstart: Deploy a Foundry resource by using Bicep"
titleSuffix: Microsoft Foundry
description: Learn how to use a Bicep file (template) to create a Microsoft Foundry resource in your Azure subscription.
ms.author: sgilley
author: sdgilley
reviewer: deeikele
ms.date: 12/24/2025
ms.service: azure-ai-foundry
ms.topic: quickstart
ms.custom:
  - classic-and-new
  - "subject-bicepqs"
  - "build-aifnd"
  - "build-2025"
  - "dev-focus"
ai-usage: ai-assisted
# Customer intent: As a DevOps person, I need to automate or customize the creation of a Foundry resource by using templates.
---

# Quickstart: Deploy a Microsoft Foundry resource by using a Bicep file

In this quickstart, you deploy a [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs) resource and project by using a [Microsoft Bicep](/azure/azure-resource-manager/bicep/overview) template. Bicep helps you create related resources in one coordinated deployment and reuse the same configuration across environments.

> [!TIP]
> For production-ready Bicep templates that cover common Foundry deployment scenarios, see the [infrastructure-setup-bicep](https://github.com/azure-ai-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep) folder in the Foundry samples repository. Clone the repository and customize the templates instead of starting from scratch.

## Prerequisites

[!INCLUDE [azure-subscription](../includes/azure-subscription.md)]

- [!INCLUDE [rbac-assign-roles](../includes/rbac-assign-roles.md)]
- [Install the Bicep CLI](/azure/azure-resource-manager/bicep/install).

Get the sample files:

# [Azure CLI](#tab/cli)

```azurecli
git clone https://github.com/Azure-AI-Foundry/foundry-samples
cd foundry-samples/infrastructure/infrastructure-setup-bicep/00-basic
```

# [Azure PowerShell](#tab/powershell)

```azurepowershell
git clone https://github.com/Azure-AI-Foundry/foundry-samples
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

## Review the Bicep file (optional)

Optionally, review the Bicep template to understand the resource definitions. 

You can find the Bicep file used in this article at [https://github.com/azure-ai-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/00-basic](https://github.com/azure-ai-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/00-basic).

This template creates the following resources:

- [microsoft.cognitiveservices/accounts](/azure/templates/microsoft.cognitiveservices/accounts?pivots=deployment-language-bicep)
- [microsoft.cognitiveservices/accounts/projects](/azure/templates/microsoft.cognitiveservices/accounts/projects?pivots=deployment-language-bicep)

## Review deployed resources

Use the [Foundry portal](https://ai.azure.com/?cid=learnDocs) to view the created resources. You can also use Azure CLI or Azure PowerShell to list the resources.

# [Azure CLI](#tab/cli)

```azurecli
az resource list --resource-group exampleRG
```

# [Azure PowerShell](#tab/powershell)

```azurepowershell
Get-AzResource -ResourceGroupName exampleRG
```

---

## Clean up resources

If you plan to continue working with subsequent quickstarts and tutorials, you can keep the resources you created in this quickstart. If you want to remove the resources, use the following command.

# [Azure CLI](#tab/cli)

```azurecli
az group delete --name exampleRG
```

Reference: [az group delete](/cli/azure/group#az-group-delete)

# [Azure PowerShell](#tab/powershell)

```azurepowershell
Remove-AzResourceGroup -Name exampleRG
```

Reference: [Remove-AzResourceGroup](/powershell/module/az.resources/remove-azresourcegroup)

---

## Related content

- [Get started with the SDK](../quickstarts/get-started-code.md)
- [Security configurations samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples) — See example Bicep template configurations for enterprise security configurations, including network isolation, customer-managed key encryption, advanced identity options, and Agents standard setup.
