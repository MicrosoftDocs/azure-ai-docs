---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: deeikele
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/31/2026
ms.custom: include
---

## Customize security and compliance

To meet security and compliance requirements, customize Foundry with security configurations and by bringing your own storage resources. For example, when using the Agent service, you can opt to bring your own Azure Cosmos DB database, Azure AI Search instance, and Azure Storage Account to store your threads and messages.

For advanced setup samples, see the following repositories:

- [Foundry Samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-terraform) repository contains example Terraform configurations for the most common enterprise security configurations.
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
