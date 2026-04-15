---
title: "Quickstart: Create a Foundry resource using Bicep (classic)"
description: "Learn how to use a Bicep file (template) to create a Microsoft Foundry resource in your Azure subscription. (classic)"
ms.author: sgilley
author: sdgilley
reviewer: deeikele
ms.date: 04/15/2026
ms.service: microsoft-foundry
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
    git clone https://github.com/microsoft-foundry/foundry-samples
    cd foundry-samples/infrastructure/infrastructure-setup-bicep/00-basic
    ```

    # [Azure PowerShell](#tab/powershell)

    ```azurepowershell
    git clone https://github.com/microsoft-foundry/foundry-samples
    cd foundry-samples/infrastructure/infrastructure-setup-bicep/00-basic
    ```

    ---

- The Bicep command-line tools. To install the Bicep CLI, see [Install the Bicep CLI](/azure/azure-resource-manager/bicep/install).
- [!INCLUDE [rbac-assign-roles](../../foundry/includes/rbac-assign-roles.md)]

## Deploy the Bicep file

Deploy the Bicep file by using either Azure CLI or Azure PowerShell.

[!INCLUDE [create-resource-template-deploy](../../foundry/includes/how-to-create-resource-template-deploy.md)]

[!INCLUDE [create-resource-template-export](../../foundry/includes/how-to-create-resource-template-export.md)]

### Related security configurations

When you customize your template, consider adding the following security configurations:

- [Configure network isolation with private endpoints](configure-private-link.md)
- [Set up customer-managed keys for encryption](../concepts/encryption-keys-portal.md)
- [Configure role-based access control for Foundry](../concepts/rbac-foundry.md)
- [Create custom Azure Policy definitions](custom-policy-definition.md)

[!INCLUDE [create-resource-template 1](../../foundry/includes/how-to-create-resource-template-1.md)]
