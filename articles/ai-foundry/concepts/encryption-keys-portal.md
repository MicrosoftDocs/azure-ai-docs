---
title: Customer-Managed Keys for Azure AI Foundry
titleSuffix: Azure AI Foundry
description: Learn about using customer-managed keys for encryption to improve data security with Azure AI Foundry.
ms.author: jburchel 
author: jonburchel 
ms.reviewer: deeikele
ms.date: 05/01/2025
ms.service: azure-ai-services
ms.topic: concept-article
ms.custom:
  - ignite-2023
  - build-aifnd
  - build-2025
zone_pivot_groups: project-type
# Customer intent: As an admin, I want to understand how I can use my own encryption keys with Azure AI Foundry.
---

# Customer-managed keys for encryption with Azure AI Foundry

Customer-managed key (CMK) encryption in [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs) provide enhanced control over the encryption of your data. By using CMK, you can manage your own encryption keys to add an extra layer of protection and meet compliance requirements more effectively.

## About encryption in Azure AI Foundry

Azure AI Foundry is a service in the Microsoft Azure cloud. By default, Azure services use Microsoft-managed encryption keys to encrypt data in transit and at rest.

::: zone pivot="hub-project"

When you use hub-based projects, the Azure AI hub resource acts as gateway to multiple Azure services including Azure AI Hub, Azure Storage account, and Azure AI Foundry resource. You must configure customer-managed key encryption on each of these services to use CMK encryption throughout with AI Foundry.

* AI Hub resources, and [!INCLUDE [hub](../includes/hub-project-name.md)] resources are implementations of the Azure Machine Learning workspace and encrypt data in transit and at rest. For details, see [Data encryption with Azure Machine Learning](../../machine-learning/concept-data-encryption.md). 

*  AI Foundry resources data is encrypted and decrypted using [FIPS 140-2](https://en.wikipedia.org/wiki/FIPS_140-2) compliant [256-bit AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) encryption. Encryption and decryption are transparent, meaning encryption and access are managed for you. Your data is secure by default and you don't need to modify your code or applications to take advantage of encryption.

* Azure Storage accounts are used to store data uploaded when using AI Foundry portal and when using Foundry tools. For details on how to set up CMK encryption, see [Customer-managed keys for Azure Storage encryption](/azure/storage/common/customer-managed-keys-overview). 

::: zone-end

::: zone pivot="fdp-project"

On your Azure AI Foundry resource data is encrypted and decrypted using [FIPS 140-2](https://en.wikipedia.org/wiki/FIPS_140-2) compliant [256-bit AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) encryption. Encryption and decryption are transparent, meaning encryption and access are managed for you. Your data is secure by default and you don't need to modify your code or applications to take advantage of encryption.

::: zone-end

> [!IMPORTANT]
> If you [connect AI Foundry with other Azure tools](../how-to/connections-add.md), CMK encryption is recommended to be configured on every other Azure resource to optimize security.

::: zone pivot="hub-project"
## Data storage options with Azure AI Hub CMK encryption

Two architecture options are available when using customer-managed keys with Azure AI Hubs:

* **(Recommended) Encrypted data is stored in Microsoft subscription**

  Data is stored service-side on Microsoft-managed resources instead of in managed resources in your subscription. Metadata is stored in multitenant resources using document-level CMK encryption. An Azure AI Search instance is hosted in the Microsoft-subscription per customer, for each hub, in order to provide data isolation of encrypted data. It's recommended to pick this option for any new deployments.

* **(Legacy) Encrypted data is stored in your subscription** 

  Traditionally in Azure Machine Learning platform (which AI Hub resource is built on), data is stored in your subscription using a Microsoft-managed resource group that includes an Azure Storage account, Azure Cosmos DB resource and Azure AI Search. The configuration of these resources can't be modified. Changes to its configurations aren't supported. 

  > [!IMPORTANT]
  > This option is available for backwards compatibility, and is not recommended for new workloads.

  All projects using the same hub store data on the resources in a managed resource group identified by the name `azureml-rg-hubworkspacename_GUID`. Projects use Microsoft Entra ID authentication when interacting with these resources. If your hub has a private link endpoint, network access to the managed resources is restricted. The managed resource group is deleted, when the hub is deleted. 

  The following data is stored on the managed resources.

  |Service|What it's used for|Example|
  |-----|-----|-----|
  |Azure Cosmos DB|Stores metadata for your Azure AI projects and tools|Index names, tags; Flow creation timestamps; deployment tags; evaluation metrics|
  |Azure AI Search|Stores indices that are used to help query your Azure AI Foundry content.|An index based off your model deployment names|
  |Azure Storage Account|Stores instructions for how customization tasks are orchestrated|JSON representation of flows you create in [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs)|

::: zone-end

## Use customer-managed keys with Azure Key Vault

You must use Azure Key Vault to store your customer-managed keys. You can either create your own keys and store them in a key vault, or you can use the Azure Key Vault APIs to generate keys. Your Azure resources and the Azure Key vault resources must be in the same region and in the same Microsoft Entra tenant, but they can be in different subscriptions. For more information about Azure Key Vault, see [What is Azure Key Vault?](/azure/key-vault/general/overview).

- You must enable both the **Soft Delete** and **Do Not Purge** properties on the key vault.
- If you use the [Key Vault firewall](/azure/key-vault/general/access-behind-firewall), you must allow trusted Microsoft services to access the key vault.
- You must grant your [!INCLUDE [fdp](../includes/fdp-project-name.md)] system-assigned managed identity the following permissions on your key vault: *get key*, *wrap key*, *unwrap key*.
- Only RSA and RSA-HSM keys of size 2048 are supported. For more information about keys, see **Key Vault keys** in [About Azure Key Vault keys, secrets, and certificates](/azure/key-vault/general/about-keys-secrets-certificates).

### Enable your Azure AI Foundry resource's managed identity

Managed identity must be enabled as a prerequisite for using customer-managed keys.

1. Go to your Azure AI Foundry resource in Azure portal.
1. On the left, under **Resource Management**, select **Identity**.
1. Switch the system-assigned managed identity status to **On**.
1. Save your changes, and confirm that you want to enable the system-assigned managed identity.

## Enable customer-managed keys

::: zone pivot="fdp-project"

Customer-managed key encryption is configured via Azure portal (or alternatively infrastructure-as-code options) in a similar way for each Azure resource:

> [!IMPORTANT]
> The Azure Key Vault used for encryption **must be in the same resource group** as the AI Foundry project. Key Vaults in other resource groups aren't currently supported by the deployment wizards or project configuration workflows.

1. Create a new Azure AI Foundry resource in the [Azure portal](https://portal.azure.com/).
1. Under the **Encryption** tab, select **Customer-managed key**, **Select vault and key**, and then select the key vault and key to use.

    :::image type="content" source="../media/portal/customer-managed-key.png" alt-text="Screenshot of the encryption tab for an AI Foundry project with the option for customer-managed key selected." lightbox="../media/portal/customer-managed-key.png":::

1. Continue creating your resource as normal.

::: zone-end

::: zone pivot="hub-project"

Customer-managed key encryption is configured via Azure portal (or alternatively infrastructure-as-code options) in a similar way for each Azure resource:

1. Create a new Azure resource in Azure portal.
1. Under the encryption tab, select your encryption key.
1. For Azure AI Hub, check or uncheck 'Service-side encryption' to select your preferred data storage option. Service-side encryption is recommended for any new workload.

   :::image type="content" source="../../machine-learning/media/concept-customer-managed-keys/cmk-service-side-encryption.png" alt-text="Screenshot of the encryption tab with the option for service side encryption selected." lightbox="../../machine-learning/media/concept-customer-managed-keys/cmk-service-side-encryption.png":::

::: zone-end

## Encryption Key Rotation

You can rotate a customer-managed key in Key Vault according to your compliance policies. When the key is rotated, you must update the Azure AI Foundry resource to use the new key URI. Rotating the key doesn't trigger re-encryption of data in the resource.

Rotation Limitations

* **Same Key Vault Requirement**

  You can only rotate encryption keys to another key within the same Azure Key Vault instance. Cross-vault key rotation isn't supported.

* **Scope of Rotation**

  The new key must be compatible with the existing encryption configuration. Ensure that the new key is properly configured with the necessary access policies and permissions.

* **Updating from customer-managed to Microsoft-managed**
  
  When an Azure AI Foundry resource or/and AI Hub is created, you can update from Microsoft-managed keys to customer-managed keys. However, you can't switch back from customer-managed keys to Microsoft-managed keys.

How to Rotate Encryption Keys

* In your Azure Key Vault, create or identify the new key you want to use for new data encryption.

* From Azure portal or template options, update the resource configuration to reference the new key within the same Key Vault.

* Your resource takes a few minutes to configure wrapping data using your new encryption key. During this period, certain service operations are available.

* The service begins using the new key for encryption of newly stored data. Existing data remains encrypted with the previous key unless reprocessed.

## Revoke a customer-managed key

You can revoke a customer-managed encryption key by changing the access policy, by changing the permissions on the key vault, or by deleting the key.

To change the access policy of the managed identity that your registry uses, run the [az-keyvault-delete-policy](/cli/azure/keyvault#az-keyvault-delete-policy) command:

```azurecli
az keyvault delete-policy \
  --resource-group <resource-group-name> \
  --name <key-vault-name> \
  --key_id <key-vault-key-id>
```

To delete the individual versions of a key, run the [az-keyvault-key-delete](/cli/azure/keyvault/key#az-keyvault-key-delete) command. This operation requires the *keys/delete* permission.

```azurecli
az keyvault key delete  \
  --vault-name <key-vault-name> \
  --id <key-ID>                     
```

> [!IMPORTANT]
> Revoking access to an active customer-managed key while CMK is still enabled will prevent downloading of training data and results files, fine-tuning new models, and deploying fine-tuned models. However, previously deployed fine-tuned models continue to operate and serve traffic until those deployments are deleted.

## Extra Azure cost when using customer-managed keys

When using customer-managed keys, generally your data is stored using document-level encryption in Microsoft-managed storage components. To ensure your data can be stored in isolation and encrypted using your keys, certain backend Azure services used by Azure AI Foundry must be hosted in a dedicated manner per AI Foundry resource in combination with CMK encryption. Additional charges apply when using CMK to accommodate this dedicated hosting model. These charges will show in Azure Cost management as sub line items under your Azure AI Foundry resource.

## Limitations

* AI Foundry resources may be updated from Microsoft-managed keys to customer-managed keys, but not from customer-managed keys to Microsoft-managed keys.
* AI Foundry hub resources can't be updated from Microsoft-managed keys to customer-managed keys, or vice versa, post-creation.
* The customer-managed key for encryption can only be updated to keys in the same Azure Key Vault instance.
* [Azure AI Foundry Customer-Managed Key Request Form](https://aka.ms/cogsvc-cmk) is required to use customer-managed keys in combination with Azure Speech and Content Moderator capabilities.
* [Azure AI Foundry Customer-Managed Key Request Form](https://aka.ms/cogsvc-cmk) is required for Speech and Content Moderator.
* If your AI Foundry resource is in a soft-deleted state, any storage-related charges for customer-managed key encryption will continue to accrue during the soft delete retention period.

## Next steps

Learn more:

* [Customer-managed key encryption](../concepts/encryption-keys-portal.md)
* [Disable local auth](../how-to/disable-local-auth.md)
* [What is Azure Key Vault](/azure/key-vault/general/overview)?

Reference infrastructure-as-code templates:

* [Bicep sample for CMK encryption for Azure AI Foundry resource](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup/30-customer-managed-keys)
* [Bicep sample for CMK encryption for Azure AI Foundry resource and Agent service standard setup](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup/31-customer-managed-keys-standard-agent)
* [Bicep sample for CMK encryption for Azure AI hub](https://github.com/azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.machinelearningservices/aistudio-cmk-service-side-encryption).
