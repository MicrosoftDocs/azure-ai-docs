---
title: 'Use Terraform to create a Microsoft Foundry hub'
description: In this article, you create a Microsoft Foundry hub, a Microsoft Foundry project, an AI services resource, and more resources.
ms.topic: how-to
ms.date: 12/22/2025
titleSuffix: Microsoft Foundry 
ms.service: azure-ai-foundry
ms.reviewer: andyaviles 
ms.author: sgilley
author: sdgilley
ms.custom: 
  - devx-track-terraform
  - hub-only
  - dev-focus
content_well_notification: 
  - AI-contribution
ai-usage: ai-assisted
#customer intent: As a Terraform user, I want to see how to create a Microsoft Foundry hub and its associated resources.
---

# Use Terraform to create a Microsoft Foundry hub

[!INCLUDE [hub-only-alt](../includes/uses-hub-only-alt.md)]

In this article, you use Terraform to create a [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs) hub, a project, and Foundry Tools connection. A hub is a central place for data scientists and developers to collaborate on machine learning projects. It provides a shared, collaborative space to build, train, and deploy machine learning models. The hub is integrated with Azure Machine Learning and other Azure services, making it a comprehensive solution for machine learning tasks. The hub also allows you to manage and monitor your AI deployments, ensuring they're performing as expected.

[!INCLUDE [About Terraform](~/azure-dev-docs-pr/articles/terraform/includes/abstract.md)]

> [!div class="checklist"]
> * Create a resource group
> * Set up a storage account
> * Establish a key vault
> * Configure Foundry Tools
> * Build a Foundry hub
> * Develop a hub-based project
> * Establish a Foundry Tools connection

## Prerequisites

- [!INCLUDE [azure-subscription](../includes/azure-subscription.md)]

- **Azure role:** Owner or Contributor on the Azure subscription. This role is required to create resource groups, storage accounts, key vaults, and Foundry resources.

- [Install and configure Terraform](/azure/developer/terraform/quickstart-configure)

## Create Terraform configuration files

You'll create four Terraform files to configure the Azure provider, define Foundry resources, declare input variables, and output deployment results.

> [!NOTE]
> The sample code for this article is located in the [Azure Terraform GitHub repo](https://github.com/Azure/terraform/tree/master/quickstart/101-azure-ai-foundry). You can view the log file containing the [test results from current and previous versions of Terraform](https://github.com/Azure/terraform/tree/master/quickstart/101-azure-ai-foundry/TestRecord.md). You might need to update the resource provider versions used in the template to use the latest available versions.
> 
> See more [articles and sample code showing how to use Terraform to manage Azure resources](/azure/terraform).

1. Create a directory to test and run the sample Terraform code. Make it the current directory.

1. Create a file named `providers.tf` and insert the following code.

    :::code language="Terraform" source="~/terraform_samples/quickstart/101-azure-ai-foundry/providers.tf":::

    This file configures the Azure Terraform provider, specifying the Azure subscription and required provider versions. It establishes the connection between Terraform and your Azure subscription.

    **Reference:** [Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)

1. Create a file named `main.tf` and insert the following code.

    :::code language="Terraform" source="~/terraform_samples/quickstart/101-azure-ai-foundry/main.tf":::

    This file defines the core Foundry resources: a resource group, storage account, key vault, Foundry hub, project, and Foundry Tools connection. These resources form the foundation for your AI development environment.

    **Reference:** [azurerm_machine_learning_workspace](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/machine_learning_workspace), [azurerm_storage_account](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/storage_account), [azurerm_key_vault](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/key_vault)

1. Create a file named `variables.tf` and insert the following code.

    :::code language="Terraform" source="~/terraform_samples/quickstart/101-azure-ai-foundry/variables.tf":::

    This file declares input variables for your Terraform configuration (such as location, environment, and resource naming). These variables allow you to customize the deployment without editing the main resource definitions.

    **Reference:** [Terraform Input Variables](https://registry.terraform.io/language/values/variables)

1. Create a file named `outputs.tf` and insert the following code.
    
    :::code language="Terraform" source="~/terraform_samples/quickstart/101-azure-ai-foundry/outputs.tf":::

    This file defines output values that display deployment results after Terraform apply completes. Outputs include the resource group name, workspace name, and other resource identifiers that you'll need to reference or manage your Foundry resources.

    **Reference:** [Terraform Output Values](https://registry.terraform.io/language/values/outputs)

## Authenticate to Azure

1. Run [az login](/cli/azure/account#az-login) without any parameters and follow the instructions to sign in to Azure.

    ```azurecli
    az login
    ```

    **Key points:**

    - Upon successful sign in, `az login` displays a list of the Azure subscriptions associated with the logged-in Microsoft account, including the default subscription.

1. To confirm the current Azure subscription, run [az account show](/cli/azure/account#az-account-show).

    ```azurecli
    az account show
    ```

## Initialize Terraform

[!INCLUDE [terraform-init.md](~/azure-dev-docs-pr/articles/terraform/includes/terraform-init.md)]

## Create a Terraform execution plan

[!INCLUDE [terraform-plan.md](~/azure-dev-docs-pr/articles/terraform/includes/terraform-plan.md)]

## Apply a Terraform execution plan

[!INCLUDE [terraform-apply-plan.md](~/azure-dev-docs-pr/articles/terraform/includes/terraform-apply-plan.md)]

## Verify the results

### [Azure CLI](#tab/azure-cli)

1. Get the Azure resource group name.

    ```console
    resource_group_name=$(terraform output -raw resource_group_name)
    ```

1. Get the workspace name.

    ```console
    workspace_name=$(terraform output -raw workspace_name)
    ```

1. Run [az ml workspace show](/cli/azure/ml/workspace#az-ml-workspace-show) to display information about the new workspace.

    ```azurecli
    az ml workspace show --resource-group $resource_group_name \
                         --name $workspace_name
    ```

### [Azure PowerShell](#tab/azure-powershell)

1. Get the Azure resource group name.

    ```console
    $resource_group_name=$(terraform output -raw resource_group_name)
    ```

1. Get the workspace name.

    ```console
    $workspace_name=$(terraform output -raw workspace_name)
    ```

1. Run [Get-AzMLWorkspace](/powershell/module/az.machinelearningservices/get-azmlworkspace) to display information about the new workspace.

    ```azurepowershell
    Get-AzMLWorkspace -ResourceGroupName $resource_group_name `
                      -Name $workspace_name
    ```

---

## Clean up resources

[!INCLUDE [terraform-plan-destroy.md](~/azure-dev-docs-pr/articles/terraform/includes/terraform-plan-destroy.md)]

## Troubleshoot Terraform on Azure

[Troubleshoot common problems when using Terraform on Azure](/azure/developer/terraform/troubleshoot).

## Next steps

> [!div class="nextstepaction"]
> [See more articles about Foundry hub](/search/?terms=Azure%20ai%20hub%20and%20terraform)

