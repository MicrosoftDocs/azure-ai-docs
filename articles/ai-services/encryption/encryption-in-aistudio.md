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

Hub and project resources are implementations of the Azure Machine Learning workspace and encrypt data in transit and at rest. For details, see [Data encryption with Azure Machine Learning](../machine-learning/concept-data-encryption?view=azureml-api-2).

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

>[!IMPORTANT]
> Azure AI Studio uses Azure compute that is managed in the Microsoft subscription, for example when you fine-tune models or or build flows. Its disks are encrypted with Microsoft-managed keys. Compute is ephemeral, meaning after a task is completed the virtual machine is deprovisioned, and the OS disk is deleted. Compute instance machines used for 'Code' experiences are persistant. Azure Disk Encryption isn't supported for the OS disk. 

## (Preview) Service-side storage of encrypted data when using customer-managed keys

A new architecture for customer-managed key encryption with hubs is available in preview, which resolves the dependency on the managed resource group. In this new model, encrypted data is stored service-side on Microsoft-managed resources instead of in managed resources in your subscription. Metadata is stored in multi-tenant resources using document-level CMK encryption. An Azure AI Search instance is hosted on the Microsoft-side per customer, and for each hub. Due to its dedicated resource model, its Azure cost is charged in your subscription via the hub resource.

> [!NOTE]
> During this preview key rotation and user-assigned identity capabilities are not supported. Server-side encryption is currently not supported in reference to an Azure Key Vault for storing your encryption key that has public network access disabled.

## Use customer-managed keys with Azure Key Vault

You must use Azure Key Vault to store your customer-managed keys. You can either create your own keys and store them in a key vault, or you can use the Azure Key Vault APIs to generate keys. The Azure AI services resource and the key vault must be in the same region and in the same Microsoft Entra tenant, but they can be in different subscriptions. For more information about Azure Key Vault, see [What is Azure Key Vault?](/azure/key-vault/general/overview).

To enable customer-managed keys, the key vault containing your keys must meet these requirements:

- You must enable both the **Soft Delete** and **Do Not Purge** properties on the key vault.
- If you use the [Key Vault firewall](/azure/key-vault/general/access-behind-firewall), you must allow trusted Microsoft services to access the key vault.
- You must grant your hub's and Azure AI Services resource's system-assigned managed identity the following permissions on your key vault: *get key*, *wrap key*, *unwrap key*.

The following limitations hold for Azure AI Services:
- Only Azure Key Vault with [legacy access policies](/azure/key-vault/general/assign-access-policy) are supported.
- Only RSA and RSA-HSM keys of size 2048 are supported with Azure AI services encryption. For more information about keys, see **Key Vault keys** in [About Azure Key Vault keys, secrets and certificates](/azure/key-vault/general/about-keys-secrets-certificates).

### Enable your Azure AI Services resource's managed identity

If connecting with Azure AI Services, or variants of Azure AI Services such as Azure OpenAI, you need to enable managed identity as a prerequisite for using customer-managed keys.

1. Go to your Azure AI services resource.
1. On the left, under **Resource Management**, select **Identity**.
1. Switch the system-assigned managed identity status to **On**.
1. Save your changes, and confirm that you want to enable the system-assigned managed identity.

## Enable customer-managed keys

Azure AI studio builds on hub as implementation of Azure Machine Learning workspace, Azure AI Services, and lets you connect with additional resources in Azure. You must set encryption specifically on each resource.

Customer-managed key encryption is configured via Azure Portal in a similar way for each Azure resource:
1. Create a new Azure resource in Azure portal.
1. Under the encryption tab, select your encryption key.

:::image type="content" source="../machine-learning/media/concept-customer-managed-keys/cmk-service-side-encryption.png" alt-text="Screenshot of the encryption tab with the option for server side encryption selected." lightbox="./media/concept-customer-managed-keys/cmk-service-side-encryption.png":::

Alternatively, use infrastructure-as-code options for automation. Example Bicep templates for Azure AI Studio are available on the Azure Quickstart repo:
1. [CMK encryption for hub](https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.machinelearningservices/aistudio-cmk).
1. [Service-side CMK encryption preview for hub](https://github.com/azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.machinelearningservices/machine-learning-workspace-cmk-service-side-encryption).

## Limitations

* The customer-managed key for encryption can only be updated to keys in the same Azure Key Vault instance.
* After deployment, hubs cannot switch from Microsoft-managed keys to Customer-managed keys or vice versa.
* [Azure AI services Customer-Managed Key Request Form](https://aka.ms/cogsvc-cmk) is required to use customer-managed keys in combination with Azure Speech and Content Moderator capabilities.
* Resources that are created in the Microsoft-managed Azure resource group in your subscription can't be modified by you or be provided by you at the time of creation as existing resources.
* You can't delete Microsoft-managed resources used for customer-managed keys without also deleting your hub.
* [Azure AI services Customer-Managed Key Request Form](https://aka.ms/cogsvc-cmk) is still required for Speech and Content Moderator.

## Next steps
* [What is Azure Key Vault](/azure/key-vault/general/overview)?
