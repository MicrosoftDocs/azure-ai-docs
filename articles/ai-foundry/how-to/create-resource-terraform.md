---
title: 'Use Terraform to create Microsoft Foundry'
description: In this article, you create a Microsoft Foundry resource, a Microsoft Foundry project, using Terraform infrastructure as code templates.
ms.topic: how-to
ms.date: 10/27/2025
titleSuffix: Microsoft Foundry 
ms.service: azure-ai-foundry
ms.reviewer: deeikele 
ms.author: sgilley
author: sdgilley
ms.custom: 
  - devx-track-terraform
  - update-code
monikerRange: foundry-classic || foundry
content_well_notification: 
  - AI-contribution
ai-usage: ai-assisted
#customer intent: As a Terraform user, I want to see how to configure Microsoft Foundry using Terraform, so I can automate my setup.
---

# Use Terraform to manage Microsoft Foundry resources

In this article, you use Terraform to manage a [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs) resource. You learn how to use Terraform to manage Foundry management configurations including projects, deployments, and connections. 

You can use either the Terraform [AzAPI Provider](/azure/developer/terraform/overview-azapi-provider) or [AzureRM Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/cognitive_account) to manage Foundry resources. While the AzAPI provider lets you access all Foundry control plane configurations including preview features, the AzureRM variant is limited to core management capabilities:

|Action|AzAPI Provider|AzureRM Provider|
| --- | --- | --- |
| Create a resource group | ✅ | ✅ |
| Create a Foundry resource | ✅ | ✅ |
| Configure deployments | ✅ | ✅ |
| Configure projects | ✅ | - |
| Configure a connection to knowledge and tools | ✅ | - |
| Configure a capability host (for advanced tool configurations like [Agent standard setup](../agents/concepts/capability-hosts.md)) | ✅ | - |


[!INCLUDE [About Terraform](~/azure-dev-docs-pr/articles/terraform/includes/abstract.md)]

## Prerequisites

[!INCLUDE [azure-subscription](../includes/azure-subscription.md)]

- [Install and configure Terraform](/azure/developer/terraform/quickstart-configure).

## Implement a basic Foundry configuration using Terraform code

# [AzAPI Provider](#tab/azapi)

1. Create a directory in which to test and run the sample Terraform code and make it the current directory.

1. Create a file named `providers.tf` and insert the following code.

    :::code language="Terraform" source="~/foundry-samples-main/infrastructure/infrastructure-setup-terraform/00-basic/code/providers.tf":::

1. Create a file named `main.tf` and insert the following code.

    :::code language="Terraform" source="~/foundry-samples-main/infrastructure/infrastructure-setup-terraform/00-basic/code/main.tf":::

1. Create a file named `variables.tf` and insert the following code.

    :::code language="Terraform" source="~/foundry-samples-main/infrastructure/infrastructure-setup-terraform/00-basic/code/variables.tf"::: 

# [AzureRM Provider](#tab/azurerm)

1. Create a directory in which to test and run the sample Terraform code and make it the current directory.

1. Create a file named `providers.tf` and insert the following code.

    :::code language="Terraform" source="~/foundry-samples-main/infrastructure/infrastructure-setup-terraform/00-basic-azurerm/code/providers.tf":::

1. Create a file named `main.tf` and insert the following code.

    :::code language="Terraform" source="~/foundry-samples-main/infrastructure/infrastructure-setup-terraform/00-basic-azurerm/code/main.tf":::

1. Create a file named `variables.tf` and insert the following code.

    :::code language="Terraform" source="~/foundry-samples-main/infrastructure/infrastructure-setup-terraform/00-basic-azurerm/code/variables.tf"::: 

---

## Initialize Terraform

[!INCLUDE [terraform-init.md](~/azure-dev-docs-pr/articles/terraform/includes/terraform-init.md)]

## Create a Terraform execution plan

[!INCLUDE [terraform-plan.md](~/azure-dev-docs-pr/articles/terraform/includes/terraform-plan.md)]

## Apply a Terraform execution plan

[!INCLUDE [terraform-apply-plan.md](~/azure-dev-docs-pr/articles/terraform/includes/terraform-apply-plan.md)]

## Customize with security and compliance controls

To meet security and compliance requirements, you may customize Foundry with security configurations and by bringing your own storage resources. For example, when using the Agent service, you may opt to bring your own Azure CosmosDB database, Azure AI Search instance, and Azure Storage Account to store your threads and messages.

Refer to the below repositories for advanced setup samples:

- [Foundry Samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples) repository contains example Terraform configurations for the most common enterprise security configurations.
- [Terraform Azure Verified Module (Cognitive Services account)](https://registry.terraform.io/modules/Azure/avm-res-cognitiveservices-account/azurerm/latest) is a generic module set to manage the Azure resource type used by Foundry, Azure OpenAI, Azure Speech, Azure Language.
- [Terraform Azure Verified Pattern Module (Foundry)](https://registry.terraform.io/modules/Azure/avm-ptn-aiml-ai-foundry/azurerm/latest) is a reference implementation for Foundry.
- [Terraform Azure Verified Pattern Module (Azure AI and ML Landing Zone)](https://registry.terraform.io/modules/Azure/avm-ptn-aiml-landing-zone/azurerm/latest) provides a reference for the set of resources typically created alongside Foundry for an end-to-end sample.

## Clean up resources

[!INCLUDE [terraform-plan-destroy.md](~/azure-dev-docs-pr/articles/terraform/includes/terraform-plan-destroy.md)]

## Troubleshoot Terraform on Azure

[Troubleshoot common problems when using Terraform on Azure](/azure/developer/terraform/troubleshoot).

## Next steps

- [See AzureRM reference docs for Foundry](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/cognitive_account)
- [Learn more about AzAPI provider](/azure/developer/terraform/overview-azapi-provider)


