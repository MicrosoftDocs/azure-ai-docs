---
title: Azure OpenAI Service encryption of data at rest
description: Learn how Azure OpenAI encrypts your data when it's persisted to the cloud.
titleSuffix: Azure AI services
author: mrbullwinkle
manager: nitinme
ms.service: azure-ai-openai
ms.topic: conceptual
ms.date: 12/02/2024
ms.author: mbullwin
---

# Azure OpenAI Service encryption of data at rest

Azure OpenAI automatically encrypts your data when it's persisted to the cloud. The encryption protects your data and helps you meet your organizational security and compliance commitments. This article covers how Azure OpenAI handles encryption of data at rest, specifically training data and fine-tuned models. For information on how data provided by you to the service is processed, used, and stored, consult the [data, privacy, and security article](/legal/cognitive-services/openai/data-privacy?context=/azure/ai-services/openai/context/context).

## About Azure AI services encryption

Azure OpenAI is part of Azure AI services. Azure AI services data is encrypted and decrypted using [FIPS 140-2](https://en.wikipedia.org/wiki/FIPS_140-2) compliant [256-bit AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) encryption. Encryption and decryption are transparent, meaning encryption and access are managed for you. Your data is secure by default and you don't need to modify your code or applications to take advantage of encryption.

## About encryption key management

By default, your subscription uses Microsoft-managed encryption keys. There's also the option to manage your subscription with your own keys called customer-managed keys (CMK). CMK offers greater flexibility to create, rotate, disable, and revoke access controls. You can also audit the encryption keys used to protect your data.

## Use customer-managed keys with Azure Key Vault

Customer-managed keys (CMK), also known as Bring your own key (BYOK), offer greater flexibility to create, rotate, disable, and revoke access controls. You can also audit the encryption keys used to protect your data.

You must use Azure Key Vault to store your customer-managed keys. You can either create your own keys and store them in a key vault, or you can use the Azure Key Vault APIs to generate keys. The Azure AI services resource and the key vault must be in the same region and in the same Microsoft Entra tenant, but they can be in different subscriptions. For more information about Azure Key Vault, see [What is Azure Key Vault?](/azure/key-vault/general/overview).

To enable customer-managed keys, the key vault containing your keys must meet these requirements:

- You must enable both the **Soft Delete** and **Do Not Purge** properties on the key vault.
- If you use the [Key Vault firewall](/azure/key-vault/general/access-behind-firewall), you must allow trusted Microsoft services to access the key vault.
- The key vault must use [legacy access policies](/azure/key-vault/general/assign-access-policy).
- You must grant the Azure OpenAI resource's system-assigned managed identity the following permissions on your key vault: *get key*, *wrap key*, *unwrap key*.

Only RSA and RSA-HSM keys of size 2048 are supported with Azure AI services encryption. For more information about keys, see **Key Vault keys** in [About Azure Key Vault keys, secrets and certificates](/azure/key-vault/general/about-keys-secrets-certificates).

### Enable your Azure OpenAI resource's managed identity

1. Go to your Azure AI services resource.
1. On the left, under **Resource Management**, select **Identity**.
1. Switch the system-assigned managed identity status to **On**.
1. Save your changes, and confirm that you want to enable the system-assigned managed identity.

### Configure your key vault's access permissions

1. In the Azure portal, go to your key vault.
1. On the left, select **Access policies**.
   
   If you see a message advising you that access policies aren't available, [reconfigure your key vault to use legacy access policies](/azure/key-vault/general/assign-access-policy) before continuing.
1. Select **Create**.
1. Under **Key permissions**, select **Get**, **Wrap Key**, and **Unwrap Key**. Leave the remaining checkboxes unselected.

   :::image type="content" source="../media/cognitive-services-encryption/key-vault-access-policy.png" alt-text="Screenshot of the Azure portal page for a key vault access policy. The permissions selected are Get Key, Wrap Key, and Unwrap Key.":::

1. Select **Next**.
1. Search for the name of your Azure OpenAI resource and select its managed identity.
1. Select **Next**.
1. Select **Next** to skip configuring any application settings.
1. Select **Create**.

### Enable customer-managed keys on your Azure OpenAI resource

To enable customer-managed keys in the Azure portal, follow these steps:

1. Go to your Azure AI services resource.
1. On the left, under **Resource Management**, select **Encryption**.
1. Under **Encryption type**, select **Customer Managed Keys**, as shown in the following screenshot.

   > [!div class="mx-imgBorder"]
   > ![Screenshot of create a resource user experience.](./media/encryption/encryption.png)

### Specify a key

After you enable customer-managed keys, you can specify a key to associate with the Azure AI services resource.

#### Specify a key as a URI

To specify a key as a URI, follow these steps:

1. In the Azure portal, go to your key vault.
1. Under **Objects**, select **Keys**.
1. Select the desired key, and then select the key to view its versions. Select a key version to view the settings for that version.
1. Copy the **Key Identifier** value, which provides the URI.

   :::image type="content" source="../media/cognitive-services-encryption/key-uri-portal.png" alt-text="Screenshot of the Azure portal page for a key version. The Key Identifier box contains a placeholder for a key URI.":::

1. Go back to your Azure AI services resource, and then select **Encryption**.
1. Under **Encryption key**, select **Enter key URI**.
1. Paste the URI that you copied into the **Key URI** box.

   :::image type="content" source="../media/cognitive-services-encryption/ssecmk2.png" alt-text="Screenshot of the Encryption page for an Azure AI services resource. The Enter key URI option is selected, and the Key URI box contains a value.":::

1. Under **Subscription**, select the subscription that contains the key vault.
1. Save your changes.

#### Select a key from a key vault

To select a key from a key vault, first make sure that you have a key vault that contains a key. Then follow these steps:

1. Go to your Azure AI services resource, and then select **Encryption**.
1. Under **Encryption key**, select **Select from Key Vault**.
1. Select the key vault that contains the key that you want to use.
1. Select the key that you want to use.

   :::image type="content" source="../media/cognitive-services-encryption/ssecmk3.png" alt-text="Screenshot of the Select key from Azure Key Vault page in the Azure portal. The Subscription, Key vault, Key, and Version boxes contain values.":::

1. Save your changes.

## Update the key version

When you create a new version of a key, update the Azure AI services resource to use the new version. Follow these steps:

1. Go to your Azure AI services resource, and then select **Encryption**.
1. Enter the URI for the new key version. Alternately, you can select the key vault and then select the key again to update the version.
1. Save your changes.

## Use a different key

To change the key that you use for encryption, follow these steps:

1. Go to your Azure AI services resource, and then select **Encryption**.
1. Enter the URI for the new key. Alternately, you can select the key vault and then select a new key.
1. Save your changes.

## Rotate customer-managed keys

You can rotate a customer-managed key in Key Vault according to your compliance policies. When the key is rotated, you must update the Azure AI services resource to use the new key URI. To learn how to update the resource to use a new version of the key in the Azure portal, see [Update the key version](#update-the-key-version).

Rotating the key doesn't trigger re-encryption of data in the resource. No further action is required from the user.

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
> Revoking access to an active customer-managed key while CMK is still enabled will prevent downloading of training data and results files, fine-tuning new models, and deploying fine-tuned models. However, previously deployed fine-tuned models will continue to operate and serve traffic until those deployments are deleted.

### Delete training, validation, and training results data

 The Files API allows customers to upload their training data for the purpose of fine-tuning a model. This data is stored in Azure Storage, within the same region as the resource and logically isolated with their Azure subscription and API Credentials. Uploaded files can be deleted by the user via the [DELETE API operation](./how-to/fine-tuning.md?pivots=programming-language-python#delete-your-training-files).

### Delete fine-tuned models and deployments

The Fine-tunes API allows customers to create their own fine-tuned version of the OpenAI models based on the training data that you've uploaded to the service via the Files APIs. The trained fine-tuned models are stored in Azure Storage in the same region, encrypted at rest (either with Microsoft-managed keys or customer-managed keys) and logically isolated with their Azure subscription and API credentials. Fine-tuned models and deployments can be deleted by the user by calling the [DELETE API operation](./how-to/fine-tuning.md?pivots=programming-language-python#delete-your-model-deployment).

## Disable customer-managed keys

When you disable customer-managed keys, your Azure AI services resource is then encrypted with Microsoft-managed keys. To disable customer-managed keys, follow these steps:

1. Go to your Azure AI services resource, and then select **Encryption**.
1. Select **Microsoft Managed Keys** > **Save**.

When you previously enabled customer managed keys this also enabled a system assigned managed identity, a feature of Microsoft Entra ID. Once the system assigned managed identity is enabled, this resource will be registered with Microsoft Entra ID. After being registered, the managed identity will be given access to the Key Vault selected during customer managed key setup. You can learn more about [Managed Identities](/azure/active-directory/managed-identities-azure-resources/overview).

> [!IMPORTANT]
> If you disable system assigned managed identities, access to the key vault will be removed and any data encrypted with the customer keys will no longer be accessible. Any features depended on this data will stop working.

> [!IMPORTANT]
> Managed identities do not currently support cross-directory scenarios. When you configure customer-managed keys in the Azure portal, a managed identity is automatically assigned under the covers. If you subsequently move the subscription, resource group, or resource from one Microsoft Entra directory to another, the managed identity associated with the resource is not transferred to the new tenant, so customer-managed keys may no longer work. For more information, see **Transferring a subscription between Microsoft Entra directories** in [FAQs and known issues with managed identities for Azure resources](/azure/active-directory/managed-identities-azure-resources/known-issues#transferring-a-subscription-between-azure-ad-directories).  

## Next steps

* [Learn more about Azure Key Vault](/azure/key-vault/general/overview)
