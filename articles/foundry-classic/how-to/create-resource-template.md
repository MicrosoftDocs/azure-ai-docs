---
title: "Quickstart: Create a Foundry resource using Bicep (classic)"
description: "Learn how to use a Bicep file (template) to create a Microsoft Foundry resource in your Azure subscription. (classic)"
ms.author: sgilley
author: sdgilley
reviewer: deeikele
ms.date: 04/08/2026
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

If you already configured a Foundry resource in the Azure portal, you can [export that configuration as a Bicep file](#export-an-existing-resource-to-a-bicep-file) instead of authoring a template from scratch.

> [!TIP]
> For production-ready Bicep templates that cover common Foundry deployment scenarios, see the [infrastructure-setup-bicep](https://github.com/azure-ai-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep) folder in the Foundry samples repository. Clone the repository and customize the templates instead of starting from scratch.

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

[!INCLUDE [create-resource-template 1](../../foundry/includes/how-to-create-resource-template-1.md)]
