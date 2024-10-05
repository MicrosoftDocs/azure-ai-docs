---
title: Customer-Managed Keys for Azure AI Studio
titleSuffix: Azure AI Studio
description: Learn about using customer-managed keys to improve data security with Azure AI Studio.
author: deeikele
ms.service: azure-ai-services
ms.custom:
  - ignite-2023
ms.topic: conceptual
ms.date: 11/15/2023
ms.author: deeikele
---

# Customer-managed keys for encryption

Customer-managed keys (CMKs) in Azure AI Studio provide enhanced control over the encryption of your data. By using CMKs, you can manage your own encryption keys to add an additional layer of protection and meet compliance requirements more effectively.

## About encryption in Azure AI Studio

Azure AI Studio layers on top of Azure Machine Learning and Azure AI services. By default, these services use Microsoft-managed encryption keys. 

Hub and project resources are implementations of the Azure Machine Learning workspace and encrypt data in transit and at rest. For details, see [Data encryption with Azure Machine Learning](../machine-learning/concept-data-encryption?view=azureml-api-2)

Azure AI services data is encrypted and decrypted using [FIPS 140-2](https://en.wikipedia.org/wiki/FIPS_140-2) compliant [256-bit AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) encryption. Encryption and decryption are transparent, meaning encryption and access are managed for you. Your data is secure by default and you don't need to modify your code or applications to take advantage of encryption.

## Data storage in your subscription when using customer-managed keys

Hub resources store metadata in your Azure subscription when using customer-managed keys. Data is stored in a Microsoft-managed resource group that includes an Azure Storage account, Azure CosmosDB resource and Azure AI Search. 

> [!IMPORTANT]
> When using a customer-managed key, the costs for your subscription will be higher because encrypted data is stored in your subscription. To estimate the cost, use the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/).

The encryption key you provide when creating a hub is used to encrypt data that is stored on Microsoft-managed resources. All projects using the same hub store data on the resources in a managed resource group identified by the name `azureml-rg-hubworkspacename_GUID`. Projects use EntraID authentication when interacting with these resources. If your hub has a private link endpoint, network access to the managed resources is restricted. The managed resource group is deleted, when the hub is deleted. 

The following data is stored on the managed resources.

|Service|What it's used for|Example|
|-----|-----|-----|
|Azure Cosmos DB|Stores metadata for your Azure AI projects and tools|Index names, tags; Flow creation timestamps; deployment tags; evaluation metrics|
|Azure AI Search|Stores indices that are used to help query your AI studio content.|An index based off your model deployment names|
|Azure Storage Account|Stores instructions for how customization tasks are orchestrated|JSON representation of flows you create in AI Studio|

## (Preview) Service-side storage of encrypted data when using customer-managed keys

A new architecture for the customer-managed key encryption workspace is available in preview, which resolves the dependency on the managed resource group. In this new model, encrypted data is stored service-side on Microsoft-managed resources instead of in your subscription. Metadata is stored in multi-tenant resources using document-level CMK encryption. An Azure AI Search instance is hosted on the Microsoft-side for each hub. Due to its dedicated resource model, its Azure cost is charged in your subscription.

## Prerequisites

* An Azure subscription.
* An Azure Key Vault instance. The key vault contains the key(s) used to encrypt your services.

    * The key vault instance must enable soft delete and purge protection.
    * The managed identity for the services secured by a customer-managed key must have the following permissions in key vault:

        * wrap key
        * unwrap key
        * get

## How compute data is stored

Azure AI uses compute resources for compute instance and serverless compute when you fine-tune models or build flows. The following table describes the compute options and how data is encrypted by each one:

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

* Encryption keys don't pass down from the Azure AI resource to dependent resources including Azure AI Services and Azure Storage when configured on the Azure AI resource. You must set encryption specifically on each resource.
* The customer-managed key for encryption can only be updated to keys in the same Azure Key Vault instance.
* After deployment, you can't switch from Microsoft-managed keys to Customer-managed keys or vice versa.
* Resources that are created in the Microsoft-managed Azure resource group in your subscription can't be modified by you or be provided by you at the time of creation as existing resources.
* You can't delete Microsoft-managed resources used for customer-managed keys without also deleting your project.

## Next steps

* [Azure AI services Customer-Managed Key Request Form](https://aka.ms/cogsvc-cmk) is still required for Speech and Content Moderator.
* [What is Azure Key Vault](/azure/key-vault/general/overview)?
