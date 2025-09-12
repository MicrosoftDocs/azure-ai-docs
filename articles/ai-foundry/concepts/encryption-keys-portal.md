---
title: Customer-Managed Keys for Azure AI Foundry
titleSuffix: Azure AI Foundry
description: Learn how to use customer-managed keys (CMK) for enhanced encryption and data security in Azure AI Foundry. Configure Azure Key Vault integration and meet compliance requirements.
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
ai-usage: ai-assisted
# Customer intent: As an admin, I want to understand how I can use my own encryption keys with Azure AI Foundry.
---

# Customer-managed keys for encryption with Azure AI Foundry

Customer-managed key (CMK) encryption in [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs) gives you control over encryption of your data. Use CMKs to add an extra protection layer and help meet compliance requirements with Azure Key Vault integration.

In this article, you learn how to:

- Understand Microsoft-managed encryption versus CMK.
- Identify data storage patterns for hub-based and project-based resources.
- Choose a data storage architecture option for hub projects.
- Configure required Key Vault settings and permissions.
- Plan rotation and revocation.

## About encryption in Azure AI Foundry

Azure AI Foundry is a service in the Azure cloud. By default, Azure services use Microsoft-managed encryption keys to encrypt data in transit and at rest. Your data is always encrypted; CMKs add customer ownership and rotation control.

::: zone pivot="hub-project"

When you use hub-based projects, the Azure AI Hub resource acts as a gateway to multiple Azure services, including Azure AI Hub, Azure Storage, and Azure AI Foundry resources. You must configure CMK encryption on each of these services for consistent CMK coverage.

* Azure AI Hub resources and [!INCLUDE [hub](../includes/hub-project-name.md)] resources are implementations of the Azure Machine Learning workspace and encrypt data in transit and at rest. For more information, see [Data encryption with Azure Machine Learning](../../machine-learning/concept-data-encryption.md).
* Azure AI Foundry resources data is encrypted and decrypted by using [FIPS 140-2](https://en.wikipedia.org/wiki/FIPS_140-2)-compliant [256-bit AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) encryption. Encryption and decryption are transparent, which means that encryption and access are managed for you. Your data is secure by default, and you don't need to modify your code or applications to take advantage of encryption.
* Azure Storage accounts are used to store uploaded data when you use the Azure AI Foundry portal and tools. For more information on how to set up CMK encryption, see [Customer-managed keys for Azure Storage encryption](/azure/storage/common/customer-managed-keys-overview).

::: zone-end

::: zone pivot="fdp-project"

On your Azure AI Foundry resource, data is encrypted and decrypted by using [FIPS 140-2](https://en.wikipedia.org/wiki/FIPS_140-2)-compliant [256-bit AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) encryption. Encryption and decryption are transparent, which means that encryption and access are managed for you. Your data is secure by default, and you don't need to modify your code or applications to take advantage of encryption.

::: zone-end

> [!IMPORTANT]
> If you [connect Azure AI Foundry with other Azure tools](../how-to/connections-add.md), we recommend that you configure CMK encryption on every other Azure resource to optimize security.

::: zone pivot="hub-project"
## Data storage options with Azure AI Hub CMK encryption

Two architecture options are available when you use CMKs with Azure AI Hub:

1. **(Recommended) Service-side encrypted data in a Microsoft subscription**  
  Data is stored service side on Microsoft-managed infrastructure. Metadata is stored in multitenant resources with document-level CMK encryption. An Azure AI Search instance is hosted per hub (isolation boundary) to isolate encrypted data. Choose this model for new deployments.
2. **(Legacy) Data stored in a managed resource group in your subscription**  
  Retained for backward compatibility. Not recommended for new workloads.

All projects that use the same hub store data on the managed resource group (`azureml-rg-hubworkspacename_GUID`). If your hub has a private link endpoint, network access to the managed resources is restricted. The managed resource group is deleted when the hub is deleted.

| Service | Purpose | Example |
|---------|---------|---------|
| Azure Cosmos DB | Metadata for Azure AI projects and tools | Index names, flow timestamps, deployment tags, evaluation metrics |
| Azure AI Search | Indices to query Azure AI Foundry content | Index based on model deployment names |
| Azure Storage account | Orchestration instructions and configuration assets | JSON representations of flows created in the portal |

::: zone-end

## Use CMKs with Azure Key Vault

You must use Azure Key Vault to store your CMKs. You can either create your own keys and store them in a key vault or use the Key Vault APIs to generate keys. Your Azure resources and the Key Vault resources must be in the same region and in the same Microsoft Entra tenant. You can use different subscriptions for the resources. For more information about Key Vault, see [What is Azure Key Vault?](/azure/key-vault/general/overview).

- Enable **Soft-delete** and **Purge protection** on the key vault.
- Allow trusted Microsoft services to access the key vault if you use the [Key Vault firewall](/azure/key-vault/general/access-behind-firewall).
- Grant your [!INCLUDE [fdp](../includes/fdp-project-name.md)] system-assigned managed identity these key permissions: **get**, **wrapKey**, **unwrapKey**.
- Use RSA or RSA-HSM keys of size 2048. Other key types/sizes aren't supported. See the "Key Vault keys" section in [About Azure Key Vault keys, secrets, and certificates](/azure/key-vault/general/about-keys-secrets-certificates).

## Next steps

- Review related: [Data encryption with Azure Machine Learning](../../machine-learning/concept-data-encryption.md)
- Plan key [rotation policies in Key Vault](/azure/key-vault/secrets/tutorial-rotation-dual).
- Assess migration from legacy storage architecture if applicable.

### Enable the managed identity for your Azure AI Foundry resource

Managed identity must be enabled as a prerequisite for using CMKs.

1. Go to your Azure AI Foundry resource in the Azure portal.
1. On the left, under **Resource Management**, select **Identity**.
1. Switch the system-assigned managed identity status to **On**.
1. Save your changes, and confirm that you want to enable the system-assigned managed identity.

## Enable customer-managed keys

::: zone pivot="fdp-project"

CMK encryption is configured via the Azure portal (or alternatively via infrastructure-as-code options) in a similar way for each Azure resource.

> [!IMPORTANT]
> The key vault that you use for encryption *must be in the same resource group* as the Azure AI Foundry project. Currently, deployment wizards or project configuration workflows don't support key vaults in other resource groups.

1. Create a new Azure AI Foundry resource in the [Azure portal](https://portal.azure.com/).
1. On the **Encryption** tab, select **Encrypt data using a customer-managed key** > **Select vault and key**. Then select the key vault and the key to use.

    :::image type="content" source="../media/portal/customer-managed-key.png" alt-text="Screenshot that shows the Encryption tab for an Azure AI Foundry project with the option for customer-managed key selected." lightbox="../media/portal/customer-managed-key.png":::

1. Continue creating your resource as normal.

::: zone-end

::: zone pivot="hub-project"

CMK encryption is configured via the Azure portal (or alternatively via infrastructure-as-code options) in a similar way for each Azure resource.

1. Create a new Azure resource in the Azure portal.
1. On the **Encryption** tab, select your encryption key.
1. For Azure AI Hub, select or clear **Use service-side encryption** to select your preferred data storage option. We recommend service-side encryption for any new workload.

   :::image type="content" source="../../machine-learning/media/concept-customer-managed-keys/cmk-service-side-encryption.png" alt-text="Screenshot that shows the Encryption tab with the option for service-side encryption selected." lightbox="../../machine-learning/media/concept-customer-managed-keys/cmk-service-side-encryption.png":::

::: zone-end

## Encryption key rotation

You can rotate a CMK in Key Vault according to your compliance policies. When the key is rotated, you must update the Azure AI Foundry resource to use the new key URI. Rotating the key doesn't trigger reencryption of data in the resource.

### Rotation limitations

* **Same key vault requirement**: You can rotate encryption keys only to another key within the same Key Vault instance. Cross-vault key rotation isn't supported.
* **Scope of rotation**: The new key must be compatible with the existing encryption configuration. Ensure that the new key is properly configured with the necessary access policies and permissions.
* **Update from customer managed to Microsoft managed**: When an Azure AI Foundry resource or an Azure AI hub is created, you can update from Microsoft-managed keys to CMKs. You can't switch back from CMKs to Microsoft-managed keys.

### Rotate encryption keys

* In your key vault, create or identify the new key that you want to use for new data encryption.
* From Azure portal or template options, update the resource configuration to reference the new key within the same key vault.
* Your resource takes a few minutes to configure wrapping data by using your new encryption key. During this period, certain service operations are available.
* The service begins using the new key for encryption of newly stored data. Existing data remains encrypted with the previous key unless reprocessed.

## Revoke a customer-managed key

To revoke a CMK, you can change the access policy, change the permissions on the key vault, or delete the key.

To change the access policy of the managed identity that your registry uses, run the [az-keyvault-delete-policy](/cli/azure/keyvault#az-keyvault-delete-policy) command:

```azurecli
az keyvault delete-policy \
  --resource-group <resource-group-name> \
  --name <key-vault-name> \
  --key_id <key-vault-key-id>
```

To delete the individual versions of a key, run the [az-keyvault-key-delete](/cli/azure/keyvault/key#az-keyvault-key-delete) command. This operation requires the Keys/Delete permission.

```azurecli
az keyvault key delete  \
  --vault-name <key-vault-name> \
  --id <key-ID>                     
```
Revoking access to an active CMK while CMK encryption is still enabled prevents downloading of training data and results files, fine-tuning new models, and deploying fine-tuned models. Previously deployed fine-tuned models continue to operate and serve traffic until those deployments are deleted.

## Added Azure cost when you use CMKs

When you use CMKs, generally your data is stored by using document-level encryption in Microsoft-managed storage components. To ensure that your data can be stored in isolation and encrypted by using your keys, certain back-end Azure services used by Azure AI Foundry must be hosted in a dedicated manner according to the Azure AI Foundry resource in combination with CMK encryption. More charges apply when you use CMKs to accommodate this dedicated hosting model. These charges show in Microsoft Cost Management as subline items under your Azure AI Foundry resource.

## Limitations

* Azure AI Foundry resources can be updated from Microsoft-managed keys to CMKs but not from CMKs to Microsoft-managed keys.
* Azure AI Foundry hub resources can't be updated from Microsoft-managed keys to CMKs, or vice versa, post-creation.
* CMK for encryption can be updated only to keys in the same Key Vault instance.
* [Azure AI Foundry Customer-Managed Key Request Form](https://aka.ms/cogsvc-cmk) is required to use CMKs in combination with Azure AI Speech and Azure AI Content Safety capabilities.
* [Azure AI Foundry Customer-Managed Key Request Form](https://aka.ms/cogsvc-cmk) is required for Azure AI Speech and Azure AI Content Safety.
* If your Azure AI Foundry resource is in a soft-deleted state, any storage-related charges for CMK encryption continue to accrue during the soft-deleted retention period.

## Related content

Learn more:

* [Customer-managed key encryption](../concepts/encryption-keys-portal.md)
* [Disable local authorization](../how-to/disable-local-auth.md)
* [What is Azure Key Vault?](/azure/key-vault/general/overview)

Reference infrastructure-as-code templates:

* [Bicep sample for CMK encryption for an Azure AI Foundry resource](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup/30-customer-managed-keys)
* [Bicep sample for CMK encryption for Azure an AI Foundry resource and agent service standard setup](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup/31-customer-managed-keys-standard-agent)
* [Bicep sample for CMK encryption for Azure AI Hub](https://github.com/azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.machinelearningservices/aistudio-cmk-service-side-encryption)
