---
title: "Quickstart: Deploy a Foundry resource by using Bicep"
titleSuffix: Microsoft Foundry
description: Learn how to use a Bicep file (template) to create a Microsoft Foundry resource in your Azure subscription.
ms.author: sgilley
author: sdgilley
ms.reviewer: deeikele
ms.date: 03/31/2026
ms.service: azure-ai-foundry
ms.topic: quickstart
ms.custom:
  - classic-and-new
  - "subject-bicepqs"
  - "build-aifnd"
  - "build-2025"
  - "dev-focus"
  - doc-kit-assisted
ai-usage: ai-assisted
# Customer intent: As a DevOps person, I need to automate or customize the creation of a Foundry resource by using templates.
---

# Quickstart: Deploy a Microsoft Foundry resource by using a Bicep file

In this quickstart, you deploy a [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs) resource and project by using a [Microsoft Bicep](/azure/azure-resource-manager/bicep/overview) template. Bicep helps you create related resources in one coordinated deployment and reuse the same configuration across environments.

If you already configured a Foundry resource in the Azure portal, you can [export that configuration as a Bicep file](#export-an-existing-resource-to-a-bicep-file) instead of authoring a template from scratch.

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

## Export an existing resource to a Bicep file

If you already configured a Foundry resource in the Azure portal, you can export that configuration as a Bicep file. The exported file captures your current resource settings, including network rules, identity configuration, and project associations. Use it as a starting point for repeatable deployments across environments.

1. In the [Azure portal](https://portal.azure.com), go to your Foundry resource.
1. In the left menu under **Automation**, select **Export template**.
1. Select the **Bicep** tab to view the generated Bicep code.
1. Select **Download** to save the file locally, or **Copy** to copy the code to your clipboard.

> [!NOTE]
> The export might complete with warnings if some resource types don't support full export. Review the output and fill in any missing properties manually.

### Customize the exported template

The exported Bicep file contains hardcoded values specific to your subscription and resource group. Before you reuse the template, review and update the following:

- Replace hardcoded subscription IDs, resource group names, and resource IDs with [Bicep parameters](/azure/azure-resource-manager/bicep/parameters).
- Remove any properties you don't need or that reference resources outside the deployment scope.
- Add or adjust security configurations to match your organization's requirements.

For production-ready Bicep templates with enterprise security configurations already built in, see the [infrastructure-setup-bicep](https://github.com/azure-ai-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep) folder in the Foundry samples repository.

### Related security configurations

When you customize your template, consider adding the following security configurations:

- [Configure network isolation with private endpoints](configure-private-link.md)
- [Set up customer-managed keys for encryption](../concepts/encryption-keys-portal.md)
- [Configure role-based access control for Foundry](../concepts/rbac-foundry.md)
- [Create custom Azure Policy definitions](custom-policy-definition.md)

[!INCLUDE [create-resource-template 1](../includes/how-to-create-resource-template-1.md)]
