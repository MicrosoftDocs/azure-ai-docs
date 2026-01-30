---
title: Customer-Managed Keys for Foundry Tools
titleSuffix: Foundry Tools
description: Learn about using customer-managed keys to improve data security with Foundry Tools.
author: PatrickFarley
ms.service: azure-ai-services
ms.custom:
  - ignite-2023
ms.topic: concept-article
ms.date: 10/02/2025
ms.author: pafarley
---

# Customer-managed keys for encryption

Azure AI is built on top of multiple Azure services. While customer data is stored securely using encryption keys that Microsoft provides by default, you can enhance your security by providing your own (customer-managed) keys. The keys you provide are stored securely in Azure Key Vault.

## Prerequisites

* An Azure subscription.
* An Azure Key Vault instance. The key vault contains the keys used to encrypt your services.
    * The key vault instance must enable soft delete and purge protection.
    * The managed identity for the services secured by a customer-managed key must have the following permissions in key vault:
        * wrap key
        * unwrap key
        * get

## What are customer-managed keys?

By default, Microsoft creates and manages your resources in a Microsoft-owned Azure subscription and uses a Microsoft-managed key to encrypt the data. 

When you use a customer-managed key, these resources live in _your_ Azure subscription and are encrypted with your own key. While they exist in your subscription, these resources are still managed by Microsoft. They're automatically created and configured when you create your Azure AI resource. 

These Microsoft-managed resources are located in a new Azure resource group is created in your subscription. This resource group exists in addition to the resource group for your project. It contains the Microsoft-managed resources that your key is used with. The resource group is named using the formula of `<Azure AI resource group name><GUID>`. It isn't possible to change the naming of the resources in this managed resource group.

> [!TIP]
> If your AI resource uses a private endpoint, this resource group will also contain a Microsoft-managed Azure Virtual Network. This VNet is used to secure communications between the managed services and the project. You cannot provide your own VNet for use with the Microsoft-managed resources. You also cannot modify the virtual network. For example, you cannot change the IP address range that it uses.

> [!IMPORTANT]
> If your subscription does not have enough quota for these services, a failure will occur.

> [!IMPORTANT]
> When using a customer-managed key, the costs for your subscription will be higher because these resources are in your subscription. To estimate the cost, use the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/).

> [!WARNING]
> Don't delete the managed resource group any of the resources automatically created in this group. If you need to delete the resource group or Microsoft-managed services in it, you must delete the Azure AI resources that use it. The resource group resources are deleted when the associated AI resource is deleted.

## Enable customer-managed keys

The process to enable customer-managed keys with Azure Key Vault for Foundry Tools varies by product. Use these links for service-specific instructions:

* [Azure OpenAI](../../ai-foundry/openai/encrypt-data-at-rest.md)
* [Azure Custom Vision ](../custom-vision-service/encrypt-data-at-rest.md)
* [Azure AI Content Safety ](../content-safety/how-to/encrypt-data-at-rest.md)
* [Azure AI Face ](../computer-vision/identity-encrypt-data-at-rest.md)
* [Azure Document Intelligence ](../../ai-services/document-intelligence/authentication/encrypt-data-at-rest.md)
* [Azure Translator](../translator/encrypt-data-at-rest.md)
* [Azure Language](../language-service/concepts/encryption-data-at-rest.md)
* [Azure Speech](../speech-service/speech-encryption-of-data-at-rest.md)
* [Azure Content Moderator ](../Content-Moderator/encrypt-data-at-rest.md)
* [Azure Personalizer ](../personalizer/encrypt-data-at-rest.md)

## How compute data is stored

Azure AI uses resources for compute instance and serverless compute when you fine-tune models or build flows. The following table describes the compute options and how data is encrypted by each one:

| Compute | Encryption |
| ----- | ----- |
| Compute instance | Local scratch disk is encrypted. |
| Serverless compute | OS disk encrypted in Azure Storage with Microsoft-managed keys. Temporary disk is encrypted. |

**Compute instance**
The OS disk for compute instance is encrypted with Microsoft-managed keys in Microsoft-managed storage accounts. If the project was created with the `hbi_workspace` parameter set to `TRUE`, the local temporary disk on compute instance is encrypted with Microsoft managed keys. Customer managed key encryption isn't supported for OS and temp disk.

**Serverless compute**
The OS disk for each compute node stored in Azure Storage is encrypted with Microsoft-managed keys. This compute target is ephemeral, and clusters are typically scaled down when no jobs are queued. The underlying virtual machine is de-provisioned, and the OS disk is deleted. Azure Disk Encryption isn't supported for the OS disk. 

Each virtual machine also has a local temporary disk for OS operations. If you want, you can use the disk to stage training data. This environment is short-lived (only during your job) and encryption support is limited to system-managed keys only.

## Limitations

* Encryption keys don't pass down from the Azure AI resource to dependent resources including Foundry Tools and Azure Storage when configured on the Azure AI resource. You must set encryption specifically on each resource.
* The customer-managed key for encryption can only be updated to keys in the same Azure Key Vault instance.
* After deployment, you can't switch from Microsoft-managed keys to Customer-managed keys or vice versa.
* Resources that are created in the Microsoft-managed Azure resource group in your subscription can't be modified by you or be provided by you at the time of creation as existing resources.
* You can't delete Microsoft-managed resources used for customer-managed keys without also deleting your project.

## Related content

* [What is Azure Key Vault](/azure/key-vault/general/overview)?
