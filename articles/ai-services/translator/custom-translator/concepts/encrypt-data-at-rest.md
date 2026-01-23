---
title: Azure Translator in Foundry Tools encryption of data at rest
titleSuffix: Foundry Tools
description: Microsoft lets you manage your Foundry Tools subscriptions with your own keys, called customer-managed keys (CMK). This article covers data encryption at rest for Azure Translator in Foundry Tools, and how to enable and manage CMK. 
author: erindormier
manager: nitinme
ms.service: azure-ai-translator
ms.topic: concept-article
ms.date: 11/18/2025
ms.author: egeaney
#Customer intent: As a user of the Translator service, I want to learn how encryption at rest works.
---

# Foundry Tools encryption of data at rest

Translator automatically encrypts your cloud uploaded data to meet your organizational security and compliance goals.

## Foundry Tools encryption

Data is encrypted and decrypted using [`FIPS` 140-2](https://en.wikipedia.org/wiki/FIPS_140-2) compliant [256-bit `AES`](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) encryption. Encryption and decryption are transparent, meaning encryption and access are managed for you. Your data is secure by default and you don't need to modify your code or applications to take advantage of encryption.

## Encryption key management

By default, your subscription uses Microsoft-managed encryption keys. If you're using a pricing tier that supports Customer-managed keys, you can see the encryption settings for your resource in the **Encryption** section of the [Azure portal](https://portal.azure.com), as shown in the following image.

![View Encryption settings](../../../media/cognitive-services-encryption/encryptionblade.png)

For subscriptions that only support Microsoft-managed encryption keys, there isn't an **Encryption** section.

## Customer-managed keys with Azure Key Vault

By default, your subscription uses Microsoft-managed encryption keys. There's also the option to manage your subscription with your own keys called customer-managed keys (CMK). CMK offers greater flexibility to create, rotate, disable, and revoke access controls. You can also audit the encryption keys used to protect your data. If CMK is configured for your subscription, double encryption is provided, which offers a second layer of protection, while allowing you to control the encryption key through your Azure Key Vault.

Follow these steps to enable customer-managed keys for Translator:

1. Create your new regional Translator or regional Microsoft Foundry resource. Customer-managed keys don't work with a global resource.
2. Enabled Managed Identity in the Azure portal, and add your customer-managed key information.
3. Create a new workspace in Custom Translator and associate this subscription information.

### Enable customer-managed keys

You must use Azure Key Vault to store your customer-managed keys. You can either create your own keys and store them in a key vault, or you can use the Azure Key Vault APIs to generate keys. The Foundry resource and the key vault must be in the same region and in the same Microsoft Entra tenant, but they can be in different subscriptions. For more information about Azure Key Vault, see [What is Azure Key Vault?](/azure/key-vault/general/overview).

A new Foundry resource is always encrypted using Microsoft-managed keys. It's not possible to enable customer-managed keys at the time that the resource is created. Customer-managed keys are stored in Azure Key Vault. The key vault must be provisioned with access policies that grant key permissions to the managed identity associated with the Foundry resource. The managed identity is available as soon as the resource is created.

To learn how to use customer-managed keys with Azure Key Vault for Foundry Tools encryption, see:

- [Configure customer-managed keys with Key Vault for Foundry Tools encryption from the Azure portal](../../../Encryption/cognitive-services-encryption-keys-portal.md)

Enabling customer managed keys also enables a system assigned managed identity, a feature of Microsoft Entra ID. Once the system assigned managed identity is enabled, this resource is registered with Microsoft Entra ID. After being registered, the managed identity will be given access to the Key Vault selected during customer managed key setup. You can learn more about [Managed Identities](/azure/active-directory/managed-identities-azure-resources/overview).

> [!IMPORTANT]
> If you disable system assigned managed identities, access to the key vault is removed and any data encrypted with the customer keys are no longer be accessible. Any features that depend on this data stops working. Any models that you deployed are also undeployed. All uploaded data is deleted from Custom Translator. If the managed identities are re-enabled, we don't automatically redeploy the model for you.

> [!IMPORTANT]
> Managed identities don't currently support cross-directory scenarios. When you configure customer-managed keys in the Azure portal, a managed identity is automatically assigned under the covers. Your managed identity and customer-managed keys aren't transferred when you move a subscription, resource group, or resource from one Microsoft Entra directory to another. For more information, see **Transferring a subscription between Microsoft Entra directories** in [FAQs and known issues with managed identities for Azure resources](/azure/active-directory/managed-identities-azure-resources/known-issues#transferring-a-subscription-between-azure-ad-directories).  

### Store customer-managed keys in Azure Key Vault

To enable customer-managed keys, you must use an Azure Key Vault to store your keys. You must enable both the **Soft Delete** and **Do Not Purge** properties on the key vault.

Only `RSA` keys of size 2048 are supported with Foundry Tools encryption. For more information about keys, see **Key Vault keys** in [About Azure Key Vault keys, secrets, and certificates](/azure/key-vault/general/about-keys-secrets-certificates).

> [!NOTE]
> If the entire key vault is deleted, your data is no longer displayed and all your models are undeployed. All uploaded data is deleted from Custom Translator. 

### Revoke access to customer-managed keys

To revoke access to customer-managed keys, use PowerShell or Azure CLI. For more information, see [Azure Key Vault PowerShell](/powershell/module/az.keyvault//) or [Azure Key Vault CLI](/cli/azure/keyvault). Revoking access effectively blocks access to all data in the Foundry resource and your models are undeployed, as the encryption key is inaccessible by Foundry Tools. All uploaded data is also deleted from Azure Translator Custom Translator.

## Next steps

> [!div class="nextstepaction"]
> [Learn more about Azure Key Vault](/azure/key-vault/general/overview)
