---
title: "Quickstart: Deploy a Foundry resource by using Bicep"
titleSuffix: Microsoft Foundry
description: Learn how to use a Bicep file (template) to create a Microsoft Foundry resource in your Azure subscription.
ms.author: sgilley
author: sdgilley
ms.reviewer: deeikele
ms.date: 04/15/2026
ms.service: microsoft-foundry
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

[!INCLUDE [create-resource-template-deploy](../includes/how-to-create-resource-template-deploy.md)]

[!INCLUDE [create-resource-template-export](../includes/how-to-create-resource-template-export.md)]

### Related security configurations

When you customize your template, consider adding the following security configurations:

- [Configure network isolation with private endpoints](configure-private-link.md)
- [Set up customer-managed keys for encryption](../concepts/encryption-keys-portal.md)
- [Configure role-based access control for Foundry](../concepts/rbac-foundry.md)
- [Create custom Azure Policy definitions](custom-policy-definition.md)

[!INCLUDE [create-resource-template 1](../includes/how-to-create-resource-template-1.md)]
