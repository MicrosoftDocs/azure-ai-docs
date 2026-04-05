---
title: "Quickstart: Create a Foundry resource using Bicep (classic)"
description: "Learn how to use a Bicep file (template) to create a Microsoft Foundry resource in your Azure subscription. (classic)"
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
ROBOTS: NOINDEX, NOFOLLOW
---

# Quickstart: Create a Microsoft Foundry resource using a Bicep file (classic)

**Currently viewing:** :::image type="icon" source="../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../foundry/how-to/create-resource-template.md)

Use a [Microsoft Bicep](/azure/azure-resource-manager/bicep/overview) file (template) to create a [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs) resource. A template makes it easy to create resources as a single, coordinated operation. A Bicep file is a text document that defines the resources that are needed for a deployment. It might also specify deployment parameters. You use parameters to provide input values when deploying resources by using the file.

## Prerequisites

[!INCLUDE [azure-subscription](../../foundry/includes/azure-subscription.md)]

- A copy of the files from the GitHub repo. To clone the GitHub repo to your local machine, you can use [Git](https://git-scm.com/). Use the following command to clone the quickstart repository to your local machine and navigate to the `aifoundry-basics` directory.

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

- The Bicep command-line tools. To install the Bicep CLI, see [Install the Bicep CLI](/azure/azure-resource-manager/bicep/install).
- [!INCLUDE [rbac-assign-roles](../../foundry/includes/rbac-assign-roles.md)]

## Deploy the Bicep file

Deploy the Bicep file by using either Azure CLI or Azure PowerShell.

# [Azure CLI](#tab/cli)

```azurecli
az group create --name exampleRG --location eastus
az deployment group create --resource-group exampleRG --template-file main.bicep --parameters aiFoundryName=myai aiProjectName=myai-proj 
```

Reference: [az group create](/cli/azure/group#az-group-create), [az deployment group create](/cli/azure/deployment/group#az-deployment-group-create)

# [Azure PowerShell](#tab/powershell)

```azurepowershell
New-AzResourceGroup -Name exampleRG -Location eastus
New-AzResourceGroupDeployment -ResourceGroupName exampleRG -TemplateFile main.bicep -aiFoundryName myai -aiProjectName myai-proj
```

Reference: [New-AzResourceGroup](/powershell/module/az.resources/new-azresourcegroup), [New-AzResourceGroupDeployment](/powershell/module/az.resources/new-azresourcegroupdeployment)

---

> [!NOTE]
> Replace `myai` with the name of your resource. `exampleRG` is the name of the resource group, and `eastus` is the Azure region where resources are deployed.

When the deployment finishes, you see a message indicating the deployment succeeded (output displays: `"provisioningState": "Succeeded"`). This confirms that your Foundry resource and project have been created.

[!INCLUDE [create-resource-template 1](../../foundry/includes/how-to-create-resource-template-1.md)]
