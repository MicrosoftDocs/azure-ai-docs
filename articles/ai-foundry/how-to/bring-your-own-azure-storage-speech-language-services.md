---
title: Connect your own storage to Speech/Language
titleSuffix: Azure AI Foundry
description: Learn how to bring your own storage account to Azure AI Foundry for Speech and Language services during resource creation.
#customer intent: As a developer, I want to use my own storage account for Speech and Language services so that I can apply my security customizations and meet compliance requirements.
author: jonburchel
ms.author: jburchel
ms.reviewer: andyaviles
ms.service: azure-ai-foundry
ms.custom: ignite-2024, build-2025
ms.topic: how-to
ms.date: 10/24/2025
ai-usage: ai-assisted
---

# Connect to your own storage for Speech and Language services

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

When you bring your own storage, you get enhanced control by allowing Azure AI Foundry to integrate with and manage data outputs on storage accounts that you own. This approach provides flexibility to apply your own security customizations, including customer-managed key encryption. It also enables seamless integration with your existing storage accounts, data, and governance policies, ensuring that your organization's compliance and security requirements are met.

Azure AI Foundry resources act as an aggregator service, bringing together agents, speech, and language capabilities into a unified platform. This integration allows organizations to manage and deploy advanced AI services efficiently. Both Speech and Language services existed before their integration with Azure AI Foundry, each with its own methods for configuring storage and managing data. As a result, the interface and setup process for these services within Azure AI Foundry resources differ from what you might have experienced before.

This article shows you how to connect your storage account to your Azure AI Foundry resource for Speech and Language services. The limitations and instructions in this article apply only to Speech and Language services. To learn more about Azure AI Foundry's bring-your-own storage solutions for other features, see [Connect to your own storage](bring-your-own-azure-storage-foundry.md).

## Prerequisites

Before setting up your storage account with your Azure AI Foundry resource for Speech and Language services, ensure you have:

- An Azure subscription
- A storage account
- Contributor or Owner permissions on both the Azure AI Foundry resource and storage account
- Understanding of the [restrictions](#understand-restrictions) for Speech and Language storage configuration

## Understand restrictions

Consider the following restrictions before configuring your storage account:

- You can set only one storage account for Speech and Language capabilities.
- You must set the storage account during Azure AI Foundry resource creation. You can't set it after resource creation.
- You can't remove the storage account after you set it on the Azure AI Foundry resource.
- If you delete the storage account, Speech and Language services can't function. You need to create a new Azure AI Foundry resource if this issue occurs. This restriction also applies when you move the storage account to another Azure subscription. Changing the storage account's resource ID results in access issues.
- The storage account is shared by both Speech and Language capabilities in the Azure AI Foundry resource. While Speech and Language capabilities write to different Azure storage containers, if your scenario requires strict data isolation, create separate Azure AI Foundry resources and storage accounts.

## Configure authentication

After setting up the storage account, grant the Azure AI Foundry resource proper permissions on the storage account so the service can access your data. The service supports only Azure role-based access control (RBAC) authentication.

Assign the storage _Blob Data Contributor_ role on the storage account for the Azure AI Foundry resource's managed identity. Set the role assignment at the Azure AI Foundry resource level, not for individual projects.

API key-based authentication isn't supported.

## Create resource with storage account

You can associate storage accounts with your Azure AI Foundry resource for Speech and Language services by using infrastructure templates during resource creation.

### Use Bicep template

1. Access the Bicep template from the [Azure AI Foundry samples repository](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples/microsoft/infrastructure-setup/02-storage-speech-language/main.bicep).

1. Create an Azure AI Foundry resource with the `userOwnedStorage` field containing the storage account's resource ID.

1. Assign Storage Blob Data Contributor role for the Azure AI Foundry resource on the storage account.

### Use Terraform template

When you create an Azure AI Foundry resource with Terraform AzureRM, use the storage block to pass in the storage account's resource ID.

1. Review the [Terraform AzureRM cognitive account documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/cognitive_account) to understand how to define the storage block.

1. Define the storage block in your `kind=AIServices` cognitive account, which represents the Azure AI Foundry resource.

1. Reference the [basic Terraform template](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup-terraform/00-basic-azurerm) and include the `storage` block.

## Understand Speech integration

Speech services in an Azure AI Foundry resource generally follow the guidelines in [Bring your own storage (BYOS) Speech resource](../../ai-services/speech-service/bring-your-own-storage-speech-resource.md?tabs=portal). This guidance applies to key Speech scenarios, including Speech-to-Text (batch and real-time), Custom Speech, Text-to-Speech, and Custom Voice. For specific features under Speech, see that documentation.

### Configure customer-managed keys for Speech

When you attach your storage account, you can set your customer-managed keys for encryption of Speech data. If you don't associate your storage account, Speech services don't use the customer-managed keys set at the Azure AI Foundry resource level. All other services available through your Azure AI Foundry resource use the customer-managed key for encryption.

## Understand Language integration

The `userOwnedStorage` field in Azure AI Foundry resources acts similarly to Language resources with one key difference: you can't update the storage account even if the storage account is deleted. In standalone Language resources, you can update the storage account after deletion, but this capability isn't available in Azure AI Foundry resources.

## Understand shared storage configuration

Speech and Language services share the same storage account that you set on the Azure AI Foundry resource. You can't separate the data between users at the resource level. If a user has access to the Azure AI Foundry resource, they can access data from both Speech and Language scenarios. Both services use their own container naming conventions that keep each service separate on the storage account.

## Related content

- [Connect your own storage to AI Foundry](bring-your-own-azure-storage-foundry.md)
- [Connect your own storage to Speech/Language](../../ai-services/speech-service/bring-your-own-storage-speech-language-services.md)
- [Azure AI Foundry samples repository](https://github.com/azure-ai-foundry/foundry-samples)
