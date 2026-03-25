---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: deeikele
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Prerequisites

[!INCLUDE [azure-subscription](azure-subscription.md)]

- [!INCLUDE [rbac-create](rbac-create.md)]
- [Install and configure Terraform](/azure/developer/terraform/quickstart-configure).

## Create a basic Foundry configuration

# [AzAPI Provider](#tab/azapi)

1. Create a directory to test and run the sample Terraform code. Make this directory your current directory.

1. Create a file named `providers.tf` and add the following code.

    :::code language="Terraform" source="~/foundry-samples-main/infrastructure/infrastructure-setup-terraform/00-basic/code/providers.tf":::

1. Create a file named `main.tf` and add the following code.

    :::code language="Terraform" source="~/foundry-samples-main/infrastructure/infrastructure-setup-terraform/00-basic/code/main.tf":::

1. Create a file named `variables.tf` and add the following code.

    :::code language="Terraform" source="~/foundry-samples-main/infrastructure/infrastructure-setup-terraform/00-basic/code/variables.tf"::: 

# [AzureRM Provider](#tab/azurerm)

1. Create a directory to test and run the sample Terraform code. Make this directory your current directory.

1. Create a file named `providers.tf` and add the following code.

    :::code language="Terraform" source="~/foundry-samples-main/infrastructure/infrastructure-setup-terraform/00-basic-azurerm/code/providers.tf":::

1. Create a file named `main.tf` and add the following code.

    :::code language="Terraform" source="~/foundry-samples-main/infrastructure/infrastructure-setup-terraform/00-basic-azurerm/code/main.tf":::

1. Create a file named `variables.tf` and add the following code.

    :::code language="Terraform" source="~/foundry-samples-main/infrastructure/infrastructure-setup-terraform/00-basic-azurerm/code/variables.tf"::: 

---

**References:**
- [AzAPI provider documentation](/azure/developer/terraform/overview-azapi-provider)
- [AzureRM cognitive_account resource](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/cognitive_account)
- [Foundry Terraform samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-terraform)

## Initialize Terraform

[!INCLUDE [terraform-init.md](~/azure-dev-docs-pr/articles/terraform/includes/terraform-init.md)]

## Create a Terraform execution plan

[!INCLUDE [terraform-plan.md](~/azure-dev-docs-pr/articles/terraform/includes/terraform-plan.md)]

## Apply a Terraform execution plan

[!INCLUDE [terraform-apply-plan.md](~/azure-dev-docs-pr/articles/terraform/includes/terraform-apply-plan.md)]
