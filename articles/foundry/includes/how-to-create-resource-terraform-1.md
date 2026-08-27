---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: deeikele
ms.author: sgilley
ms.service: microsoft-foundry
ms.topic: include
ms.date: 08/27/2026
ms.custom: include
ai-usage: ai-assisted
---

## Prerequisites

[!INCLUDE [azure-subscription](azure-subscription.md)]

- [!INCLUDE [rbac-create](rbac-create.md)]
- [Azure CLI](/cli/azure/install-azure-cli). Run `az login`, and then run `az account show` to verify your active subscription.
- [Install and configure Terraform](/azure/developer/terraform/quickstart-configure).

## Create a basic Foundry configuration

# [AzAPI Provider](#tab/azapi)

1. Create a directory to test and run the sample Terraform code. Make this directory your current directory.

1. Create a file named `versions.tf` and add the required provider sources.

        ```terraform
        terraform {
            required_providers {
                azapi = {
                    source  = "Azure/azapi"
                    version = "~> 2.5"
                }
                random = {
                    source  = "hashicorp/random"
                    version = "~> 3.6"
                }
            }
        }
        ```

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

Set the required variables in your current shell. Replace `eastus` if you want to deploy to another supported region.

```console
export TF_VAR_subscription_id=$(az account show --query id --output tsv)
export TF_VAR_location=eastus
```

Run `test -n "$TF_VAR_subscription_id" && echo "Subscription configured."` to verify that the subscription variable is set.

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
