---
title: 'Use Terraform to create Azure AI Foundry'
description: In this article, you create an Azure AI Foundry resource, an Azure AI Foundry project, using Terraform infrastructure as code templates.
ms.topic: how-to
ms.date: 07/22/2025
titleSuffix: Azure AI Foundry 
ms.service: azure-ai-foundry
ms.reviewer: deeikele 
ms.author: sgilley
author: sdgilley
ms.custom: devx-track-terraform
content_well_notification: 
  - AI-contribution
ai-usage: ai-assisted
#customer intent: As a Terraform user, I want to see how to configure Azure AI Foundry using Terraform, so I can automate my setup.
---

# Use Terraform to manage Azure AI Foundry resources

In this article, you use Terraform to manage an [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs) resource. You learn how to use Terraform to manage AI Foundry management configurations including projects, deployments, and connections. 

You can use either the [AzAPI](/azure/developer/terraform/overview-azapi-provider) or [AzureRM](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/cognitive_account) Terraform provider to manage Azure AI Foundry resources. While the AzAPI provider lets you access to all Foundry control plane configurations including preview features, the AzureRM variant is limited to core management capabilities. 

[!INCLUDE [About Terraform](~/azure-dev-docs-pr/articles/terraform/includes/abstract.md)]

> [!div class="checklist"]
> * Create a resource group
> * Create an AI Foundry resource.
> * Configure projects.
> * Configure deployments.
> * Configure a connection to other resources.
> * Configure capability host to bring your own storage with Agent service.

## Prerequisites

[!INCLUDE [azure-subscription](../includes/azure-subscription.md)]

- [Install and configure Terraform](/azure/developer/terraform/quickstart-configure).

## Implement a basic AI Foundry configuration using Terraform code

# [AzAPI](#tab/azapi)

1. Create a directory in which to test and run the sample Terraform code and make it the current directory.

1. Create a file named `providers.tf` and insert the following code.

    :::code language="Terraform" source="~/foundry-samples-main/samples/microsoft/infrastructure-setup-terraform/00-basic/code/providers.tf":::

1. Create a file named `main.tf` and insert the following code.

    :::code language="Terraform" source="~/foundry-samples-main/samples/microsoft/infrastructure-setup-terraform/00-basic/code/main.tf":::

1. Create a file named `variables.tf` and insert the following code.

    :::code language="Terraform" source="~/foundry-samples-main/samples/microsoft/infrastructure-setup-terraform/00-basic/code/variables.tf"::: 

# [AzureRM](#tab/azurerm)

1. Create a directory in which to test and run the sample Terraform code and make it the current directory.

1. Create a file named `providers.tf` and insert the following code.

    :::code language="Terraform" source="~/foundry-samples-main/samples/microsoft/infrastructure-setup-terraform/00-basic-azurerm/code/providers.tf":::

1. Create a file named `main.tf` and insert the following code.

    :::code language="Terraform" source="~/foundry-samples-main/samples/microsoft/infrastructure-setup-terraform/00-basic-azurerm/code/main.tf":::

1. Create a file named `variables.tf` and insert the following code.

    :::code language="Terraform" source="~/foundry-samples-main/samples/microsoft/infrastructure-setup-terraform/00-basic-azurerm/code/variables.tf"::: 

---

## Initialize Terraform

[!INCLUDE [terraform-init.md](~/azure-dev-docs-pr/articles/terraform/includes/terraform-init.md)]

## Create a Terraform execution plan

[!INCLUDE [terraform-plan.md](~/azure-dev-docs-pr/articles/terraform/includes/terraform-plan.md)]

## Apply a Terraform execution plan

[!INCLUDE [terraform-apply-plan.md](~/azure-dev-docs-pr/articles/terraform/includes/terraform-apply-plan.md)]

## Customize AI Foundry using Terraform with custom storage and security

To help meet security and compliance requirements, AI Foundry lets you customize security configurations and bring your own storage resources. For example, when using the Agent service, you may opt to bring your own Azure CosmosDB database, Azure AI Search instance, and Azure Storage Account to store your threads and messages.

See the [Azure AI Foundry Samples](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup-terraform) repository with example Terraform configurations for the most common enterprise security configurations.

## Clean up resources

[!INCLUDE [terraform-plan-destroy.md](~/azure-dev-docs-pr/articles/terraform/includes/terraform-plan-destroy.md)]

## Troubleshoot Terraform on Azure

[Troubleshoot common problems when using Terraform on Azure](/azure/developer/terraform/troubleshoot).

## Next steps

> [!div class="nextstepaction"]
> [See AzureRM reference docs for Azure AI Foundry](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/cognitive_account)
> [Learn more about AzAPI provider](/azure/developer/terraform/overview-azapi-provider)
> [See more articles about Azure AI Foundry hub](/search/?terms=Azure%20ai%20hub%20and%20terraform)

