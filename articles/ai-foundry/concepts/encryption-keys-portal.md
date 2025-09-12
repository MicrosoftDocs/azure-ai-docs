---
 title: Customer-Managed Keys for Azure AI Foundry
 titleSuffix: Azure AI Foundry
 description: Learn about using customer-managed keys for encryption to improve data security with Azure AI Foundry projects.
 ms.author: jburchel 
 author: jonburchel 
 ms.reviewer: deeikele
 ms.date: 09/12/2025
 ms.service: azure-ai-services
 ms.topic: concept-article
 ms.custom:
   - ignite-2023
   - build-aifnd
   - build-2025
 ai-usage: ai-assisted
---

# Customer-managed keys for encryption with Azure AI Foundry (Foundry projects)

> [!NOTE]
> An alternate hub-focused CMK article is available: [Customer-managed keys for hub projects](hub-encryption-keys-portal.md).

Customer-managed key (CMK) encryption in [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs) provides enhanced control over the encryption of your data. By using a CMK, you can manage your own encryption keys to add an extra layer of protection and meet compliance requirements more effectively.

## About encryption in Azure AI Foundry

On your Azure AI Foundry resource, data is encrypted and decrypted by using [FIPS 140-2](https://en.wikipedia.org/wiki/FIPS_140-2)-compliant [256-bit AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) encryption. Encryption and decryption are transparent, which means that encryption and access are managed for you. Your data is secure by default, and you don't need to modify your code or applications to take advantage of encryption.

> [!IMPORTANT]
> If you [connect Azure AI Foundry with other Azure tools](../how-to/connections-add.md), we recommend that you configure CMK encryption on every other Azure resource to optimize security.

## Use CMKs with Azure Key Vault

You must use Azure Key Vault to store your CMKs. You can either create your own keys and store them in a key vault or use the Key Vault APIs to generate keys. Your Azure resources and the Key Vault resources must be in the same region and in the same Microsoft Entra tenant. You can use different subscriptions for the resources. For more information about Key Vault, see [What is Azure Key Vault?](/azure/key-vault/general/overview).

- Enable both the **Soft-delete** and **Purge protection** properties on the key vault.
- Allow trusted Microsoft services to access the key vault if you use the [key vault firewall](/azure/key-vault/general/access-behind-firewall).
- Grant your project system-assigned managed identity the following permissions on your key vault: Get key, Wrap key, Unwrap key.
- Only RSA and RSA-HSM keys of size 2048 are supported. For more information about keys, see the "Key Vault keys" section in [About Azure Key Vault keys, secrets, and certificates](/azure/key-vault/general/about-keys-secrets-certificates).

### Enable the managed identity for your Azure AI Foundry resource

Managed identity must be enabled as a prerequisite for using CMKs.

1. Go to your Azure AI Foundry resource in the Azure portal.
1. On the left, under **Resource Management**, select **Identity**.
1. Switch the system-assigned managed identity status to **On**.
1. Save your changes, and confirm that you want to enable the system-assigned managed identity.

## Enable customer-managed keys

CMK encryption is configured via the Azure portal (or via infrastructure-as-code) similarly for each Azure resource.

> [!IMPORTANT]
> The key vault that you use for encryption must be in the same resource group as the Azure AI Foundry project. Deployment wizards or project configuration workflows don't currently support key vaults in other resource groups.

1. Create a new Azure AI Foundry resource in the [Azure portal](https://portal.azure.com/).
1. On the **Encryption** tab, select **Encrypt data using a customer-managed key** > **Select vault and key**. Then select the key vault and the key to use.

    :::image type="content" source="../media/portal/customer-managed-key.png" alt-text="Screenshot that shows the Encryption tab for an Azure AI Foundry project with the option for customer-managed key selected." lightbox="../media/portal/customer-managed-key.png":::

1. Continue creating your resource as normal.

## Encryption key rotation

Rotate a CMK in Key Vault according to your compliance policies. When the key is rotated, update the Azure AI Foundry resource to use the new key URI. Rotating the key doesn't trigger reencryption of existing data.

### Rotation limitations

* Same key vault only: rotate to another key within the same Key Vault instance.
* Scope: new key must have required access policies.
* Can't revert from CMKs to Microsoft-managed keys after switching.

### Rotate encryption keys

1. In your key vault, create or identify the new key.
2. Update the resource configuration to reference the new key within the same key vault.
3. The service begins using the new key for newly stored data; existing data remains under the previous key unless reprocessed.

## Revoke a customer-managed key

Change the access policy, update permissions, or delete the key.

Remove access policy:
```azurecli
az keyvault delete-policy \
  --resource-group <resource-group-name> \
  --name <key-vault-name> \
  --key_id <key-vault-key-id>
```

Delete key version:
```azurecli
az keyvault key delete  \
  --vault-name <key-vault-name> \
  --id <key-ID>
```

Revoking access to an active CMK while CMK encryption is still enabled prevents downloading training data, fine-tuning new models, and deploying fine-tuned models. Existing deployments continue until deleted.

## Added Azure cost when you use CMKs

Using CMKs may incur extra subline cost items due to dedicated hosting of certain encrypted back-end services.

## Limitations

* Projects can be updated from Microsoft-managed keys to CMKs but not reverted.
* Project CMK can be updated only to keys in the same Key Vault instance.
* Request form required for some services: [Azure AI Foundry Customer-Managed Key Request Form](https://aka.ms/cogsvc-cmk) for Speech and Content Safety.
* Storage-related charges for CMK encryption continue during soft-deleted retention.

## Related content

* [Disable local authorization](../how-to/disable-local-auth.md)
* [What is Azure Key Vault?](/azure/key-vault/general/overview)
