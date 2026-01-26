---
title: Language service encryption of data at rest
description: Learn how Azure Language service encrypts your data when persisted to the cloud.
titleSuffix: Foundry Tools
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 11/18/2025
ms.author: lajanuar
#Customer intent: As a user of Azure Language service, I want to learn how encryption at rest works.
---
# Language encryption of data at rest

The Language automatically encrypts your data when persisted to the cloud. The Language encryption protects your data and helps you meet your organizational security and compliance commitments.

## Foundry Tools encryption

Data is encrypted and decrypted using [`FIPS` 140-2](https://en.wikipedia.org/wiki/FIPS_140-2) compliant [256-bit `AES`](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) encryption. Encryption and decryption are transparent, meaning encryption and access are managed for you. Your data is secure by default and you don't need to modify your code or applications to take advantage of encryption.

## About encryption key management

By default, your subscription uses Microsoft-managed encryption keys. There's also the option to manage your subscription with your own keys called customer-managed keys (CMK). CMK offers greater flexibility to create, rotate, disable, and revoke access controls. You can also audit the encryption keys used to protect your data.

## Customer-managed keys with Azure Key Vault

There's also an option to manage your subscription with your own keys. Customer-managed keys (CMK), also known as Bring your own key (BYOK), offer greater flexibility to create, rotate, disable, and revoke access controls. You can also audit the encryption keys used to protect your data.

You must use Azure Key Vault to store your customer-managed keys. You can either create your own keys and store them in a key vault, or you can use the Azure Key Vault APIs to generate keys. The Microsoft Foundry resource and the key vault must be in the same region and in the same Microsoft Entra tenant, but they can be in different subscriptions. For more information about Azure Key Vault, see [What is Azure Key Vault?](/azure/key-vault/general/overview).


### Enable customer-managed keys

A new Foundry resource is always encrypted using Microsoft-managed keys. It's not possible to enable customer-managed keys at the time that the resource is created. Customer-managed keys are stored in Azure Key Vault. The key vault must be provisioned with access policies that grant key permissions to the managed identity that is associated with the Foundry resource. The managed identity is available only after the resource is created using the Pricing Tier for CMK.

To learn how to use customer-managed keys with Azure Key Vault for Foundry Tools encryption, see:

- [Configure customer-managed keys with Key Vault for Foundry Tools encryption from the Azure portal](../../encryption/cognitive-services-encryption-keys-portal.md)

Enabling customer managed keys also enable a system assigned managed identity, a feature of Microsoft Entra ID. Once the system assigned managed identity is enabled, this resource is registered with Microsoft Entra ID. After being registered, the managed identity is given access to the Key Vault selected during customer managed key setup. You can learn more about [Managed Identities](/azure/active-directory/managed-identities-azure-resources/overview).

> [!IMPORTANT]
> If you disable system assigned managed identities, access to the key vault is removed and any data encrypted with the customer keys are no longer accessible. Any features dependent on this data stop working.

> [!IMPORTANT]
> Managed identities don't currently support cross-directory scenarios. When you configure customer-managed keys in the Azure portal, a managed identity is automatically assigned under the covers. If you move a subscription, resource group, or resource to another Microsoft Entra directory, the managed identity doesn't transfer to the new tenant. Thus, the customer-managed keys may no longer work. For more information, see **Transferring a subscription between Microsoft Entra directories** in [FAQs and known issues with managed identities for Azure resources](/azure/active-directory/managed-identities-azure-resources/known-issues#transferring-a-subscription-between-azure-ad-directories).  

### Store customer-managed keys in Azure Key Vault

To enable customer-managed keys, you must use an Azure Key Vault to store your keys. You must enable both the **Soft Delete** and **Do Not Purge** properties on the key vault.

Only `RSA` keys of size 2048 are supported with Foundry Tools encryption. For more information about keys, see **Key Vault keys** in [About Azure Key Vault keys, secrets, and certificates](/azure/key-vault/general/about-keys-secrets-certificates).

### Rotate customer-managed keys

You can rotate a customer-managed key in Azure Key Vault according to your compliance policies. When the key is rotated, you must update the Foundry resource to use the new key URI. To learn how to update the resource to use a new version of the key in the Azure portal, see the section titled **Update the key version** in [Configure customer-managed keys for Foundry Tools by using the Azure portal](../../encryption/cognitive-services-encryption-keys-portal.md).

Rotating the key doesn't trigger re-encryption of data in the resource. There's no further action required from the user.

### Revoke access to customer-managed keys

To revoke access to customer-managed keys, use PowerShell or Azure CLI. For more information, see [Azure Key Vault PowerShell](/powershell/module/az.keyvault//) or [Azure Key Vault CLI](/cli/azure/keyvault). Revoking access effectively blocks access to all data in the Foundry resource, as the encryption key is inaccessible by Foundry Tools.

## Next steps

* [Learn more about Azure Key Vault](/azure/key-vault/general/overview)
