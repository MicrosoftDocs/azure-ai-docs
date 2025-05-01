---
title: Customer-Managed Keys for Azure AI Foundry
titleSuffix: Azure AI Foundry
description: Learn about using customer-managed keys for encryption to improve data security with Azure AI Foundry.
author: Blackmist
ms.author: larryfr
ms.service: azure-ai-services
ms.custom:
  - ignite-2023
ms.topic: concept-article
ms.date: 05/01/2025
ms.reviewer: deeikele
zone_pivot_groups: project-type
# Customer intent: As an admin, I want to understand how I can use my own encryption keys with Azure AI Foundry.
---

# Customer-managed keys for encryption with Azure AI Foundry

Customer-managed keys (CMKs) in [Azure AI Foundry portal](https://ai.azure.com/) provide enhanced control over the encryption of your data. By using CMKs, you can manage your own encryption keys to add an extra layer of protection and meet compliance requirements more effectively.

## About encryption in Azure AI Foundry portal

Azure AI Foundry is a service in the Microsoft Azure cloud, and it also relies on other Azure services. By default, these services use Microsoft-managed encryption keys to encrypt data in transit and at rest.

::: zone pivot="hub-project"

Hub and [!INCLUDE [hub](../includes/hub-project-name.md)] resources are implementations of the Azure Machine Learning workspace and encrypt data in transit and at rest. For details, see [Data encryption with Azure Machine Learning](../../machine-learning/concept-data-encryption.md).

::: zone-end

Azure AI services data is encrypted and decrypted using [FIPS 140-2](https://en.wikipedia.org/wiki/FIPS_140-2) compliant [256-bit AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) encryption. Encryption and decryption are transparent, meaning encryption and access are managed for you. Your data is secure by default and you don't need to modify your code or applications to take advantage of encryption.

::: zone pivot="fdp-project"

## Service-side storage of encrypted data when using customer-managed keys

Customer-managed key encryption can be enabled during project creation through the Azure portal or Bicep template. The encrypted data is stored service-side on Microsoft-managed resources. Metadata is stored in multitenant resources using document-level CMK encryption. Due to its dedicated resource model, its Azure cost is charged in your subscription.

> [!NOTE]
> When you use server-side encryption, Azure charges will continue to accrue during the soft delete retention period.

::: zone-end

::: zone pivot="hub-project"

## Data storage in your subscription when using customer-managed keys

Hub resources store metadata in your Azure subscription when using customer-managed keys. Data is stored in a Microsoft-managed resource group that includes an Azure Storage account, Azure Cosmos DB resource and Azure AI Search. 

> [!IMPORTANT]
> When using a customer-managed key, the costs for your subscription will be higher because encrypted data is stored in your subscription. To estimate the cost, use the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/).

The encryption key you provide when creating a hub is used to encrypt data that is stored on Microsoft-managed resources. All projects using the same hub store data on the resources in a managed resource group identified by the name `azureml-rg-hubworkspacename_GUID`. Projects use Microsoft Entra ID authentication when interacting with these resources. If your hub has a private link endpoint, network access to the managed resources is restricted. The managed resource group is deleted, when the hub is deleted. 

The following data is stored on the managed resources.

|Service|What it's used for|Example|
|-----|-----|-----|
|Azure Cosmos DB|Stores metadata for your Azure AI projects and tools|Index names, tags; Flow creation timestamps; deployment tags; evaluation metrics|
|Azure AI Search|Stores indices that are used to help query your Azure AI Foundry content.|An index based off your model deployment names|
|Azure Storage Account|Stores instructions for how customization tasks are orchestrated|JSON representation of flows you create in [Azure AI Foundry portal](https://ai.azure.com/)|

>[!IMPORTANT]
> Azure AI Foundry uses Azure compute that is managed in the Microsoft subscription, for example when you fine-tune models or or build flows. Its disks are encrypted with Microsoft-managed keys. Compute is ephemeral, meaning after a task is completed the virtual machine is deprovisioned, and the OS disk is deleted. Compute instance machines used for 'Code' experiences are persistant. Azure Disk Encryption isn't supported for the OS disk. 

## (Preview) Service-side storage of encrypted data when using customer-managed keys

A new architecture for customer-managed key encryption with hubs is available in preview, which resolves the dependency on the managed resource group. In this new model, encrypted data is stored service-side on Microsoft-managed resources instead of in managed resources in your subscription. Metadata is stored in multitenant resources using document-level CMK encryption. An Azure AI Search instance is hosted on the Microsoft-side per customer, and for each hub. Due to its dedicated resource model, its Azure cost is charged in your subscription via the hub resource.

> [!NOTE]
> - During this preview key rotation and user-assigned identity capabilities are not supported. Service-side encryption is currently not supported in reference to an Azure Key Vault for storing your encryption key that has public network access disabled.
> - If you are using the preview server-side storage, Azure charges will continue to accrue during the soft delete retention period.

::: zone-end

## Use customer-managed keys with Azure Key Vault

You must use Azure Key Vault to store your customer-managed keys. You can either create your own keys and store them in a key vault, or you can use the Azure Key Vault APIs to generate keys. The Azure AI services resource and the key vault must be in the same region and in the same Microsoft Entra tenant, but they can be in different subscriptions. For more information about Azure Key Vault, see [What is Azure Key Vault?](/azure/key-vault/general/overview).

To enable customer-managed keys, the key vault containing your keys must meet these requirements:

::: zone pivot="fdp-project"

- You must enable both the **Soft Delete** and **Do Not Purge** properties on the key vault.
- If you use the [Key Vault firewall](/azure/key-vault/general/access-behind-firewall), you must allow trusted Microsoft services to access the key vault.
- You must grant your [!INCLUDE [fdp](../includes/fdp-project-name.md)] and Azure AI Services resource's system-assigned managed identity the following permissions on your key vault: *get key*, *wrap key*, *unwrap key*.

::: zone-end

::: zone pivot="hub-project"

- You must enable both the **Soft Delete** and **Do Not Purge** properties on the key vault.
- If you use the [Key Vault firewall](/azure/key-vault/general/access-behind-firewall), you must allow trusted Microsoft services to access the key vault.
- You must grant your hub and Azure AI Services resource's system-assigned managed identity the following permissions on your key vault: *get key*, *wrap key*, *unwrap key*.

::: zone-end

The following limitations hold for Azure AI Services:
- Only Azure Key Vault with [legacy access policies](/azure/key-vault/general/assign-access-policy) are supported.
- Only RSA and RSA-HSM keys of size 2048 are supported with Azure AI services encryption. For more information about keys, see **Key Vault keys** in [About Azure Key Vault keys, secrets, and certificates](/azure/key-vault/general/about-keys-secrets-certificates).

### Enable your Azure AI Services resource's managed identity

If connecting with Azure AI Services, or variants of Azure AI Services such as Azure OpenAI, you need to enable managed identity as a prerequisite for using customer-managed keys.

1. Go to your Azure AI services resource.
1. On the left, under **Resource Management**, select **Identity**.
1. Switch the system-assigned managed identity status to **On**.
1. Save your changes, and confirm that you want to enable the system-assigned managed identity.

## Enable customer-managed keys

::: zone pivot="fdp-project"

Customer-managed key encryption is configured via Azure portal in a similar way for each Azure resource:

1. Create a new Azure AI Foundry resource in the [Azure portal](https://portal.azure.com/).
1. Under the **Encryption** tab, select **Customer-managed key**, **Select vault and key**, and then select the key vault and key to use.

    :::image type="content" source="../../machine-learning/media/portal/customer-managed-key.png" alt-text="Screenshot of the encryption tab for an AI Foundry project with the option for customer-managed key selected." lightbox="../../machine-learning/media/portal/customer-managed-key.png":::

1. Continue creating your resource as normal.

## Limitations

* The customer-managed key for encryption can only be updated to keys in the same Azure Key Vault instance.
* After deployment, your [!INCLUDE [fdp](../includes/fdp-project-name.md)] can't switch from Microsoft-managed keys to customer-managed keys or vice versa.
* [Azure AI services Customer-Managed Key Request Form](https://aka.ms/cogsvc-cmk) is required to use customer-managed keys in combination with Azure Speech and Content Moderator capabilities.
* Azure charges will continue to accrue during the soft delete retention period.

::: zone-end

::: zone pivot="hub-project"

Azure AI Foundry builds on hub as implementation of Azure Machine Learning workspace, Azure AI Services, and lets you connect with other resources in Azure. You must set encryption specifically on each resource.

Customer-managed key encryption is configured via Azure portal in a similar way for each Azure resource:
1. Create a new Azure resource in Azure portal.
1. Under the encryption tab, select your encryption key.

    :::image type="content" source="../../machine-learning/media/concept-customer-managed-keys/cmk-service-side-encryption.png" alt-text="Screenshot of the encryption tab with the option for service side encryption selected." lightbox="../../machine-learning/media/concept-customer-managed-keys/cmk-service-side-encryption.png":::

Alternatively, use infrastructure-as-code options for automation. Example Bicep templates for Azure AI Foundry are available on the Azure Quickstart repo:
1. [CMK encryption for hub](https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.machinelearningservices/aifoundry-cmk).
1. [Service-side CMK encryption preview for hub](https://github.com/azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.machinelearningservices/aistudio-cmk-service-side-encryption).

## Limitations

* The customer-managed key for encryption can only be updated to keys in the same Azure Key Vault instance.
* After deployment, hubs can't switch from Microsoft-managed keys to Customer-managed keys or vice versa.
* [Azure AI services Customer-Managed Key Request Form](https://aka.ms/cogsvc-cmk) is required to use customer-managed keys in combination with Azure Speech and Content Moderator capabilities.
* At the time of creation, you can't provide or modify resources that are created in the Microsoft-managed Azure resource group in your subscription.
* You can't delete Microsoft-managed resources used for customer-managed keys without also deleting your hub.
* [Azure AI services Customer-Managed Key Request Form](https://aka.ms/cogsvc-cmk) is still required for Speech and Content Moderator.
* If you are using the [server-side preview](#preview-service-side-storage-of-encrypted-data-when-using-customer-managed-keys), Azure charges will continue to accrue during the soft delete retention period.

::: zone-end

## Related content

* [What is Azure Key Vault](/azure/key-vault/general/overview)?
