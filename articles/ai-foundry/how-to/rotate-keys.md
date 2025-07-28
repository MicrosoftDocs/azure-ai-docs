---
title: Rotate keys in Azure AI Foundry
titleSuffix: Azure AI Foundry
description: "Learn how to rotate API keys and encryptions for better security, without interrupting service"
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-services
ms.custom:
  - ignite-2023
ms.topic: how-to
ms.date: 5/19/2025
ms.author: pafarley
---

# Rotate Keys in Azure AI Foundry

Azure AI Foundry supports key rotation for both API keys and encryption keys to help maintain strong security hygiene and reduce the risk of unauthorized access. The dual-key setup for API access is designed to enable rotation without interrupting current traffic, helping maintain service availability while enhancing security posture. 

## How to rotate API Keys

Follow these steps to rotate your API keys:

1. Ensure only one key is actively used in production.
  
   For example, if both keys are in use, update your application to use only Key 1. This is important because regenerating a key invalidates its previous version immediately, which would result in 401 Access Denied errors for clients still using the old key.

1. Regenerate the unused key.
   
   In the Azure portal, navigate to your Foundry resource, select the Keys and Endpoint tab, and click Regenerate Key 2.

1. Update your application to use the newly generated key.

   Monitor logs or availability to confirm that all clients have successfully switched to Key 2.

1. Regenerate the original key.
   Once all clients are using Key 2, repeat the process to regenerate Key 1.

1. Switch back to Key 1 if desired.
   Update your application to use the new Key 1.

## Encryption Key Rotation (Customer-Managed Keys)
If you're using [customer-managed key encryption](../concepts/encryption-keys-portal.md), Azure AI Foundry allows you to rotate the encryption key used to protect your data. This applies to data stored in Microsoft-managed infrastructure, encrypted using your Azure Key Vault key.

Rotation Limitations

* **Same Key Vault Requirement**

  You can only rotate encryption keys to another key within the same Azure Key Vault instance. Cross-vault key rotation is not supported.

* **Scope of Rotation**

  The new key must be compatible with the existing encryption configuration. Ensure that the new key is properly configured with the necessary access policies and permissions.

* **Updating from customer-managed to Microsoft-managed**

  When an Azure AI Foundry resource is created, you can update from Microsoft-managed keys to customer-managed keys. However, you may not switch back from customer-managed keys to Microsoft-managed keys.

How to Rotate Encryption Keys

* In your Azure Key Vault, create or identify the new key you want to use for encryption.

* From Azure Portal or template options, update the Foundry resource configuration to reference the new key within the same Key Vault.

* Your AI Foundry resource will take a few minutes to wrap data using your new encryption key. During this period, certain service operations are available.

* Azure AI Foundry will begin using the new key for encryption of newly stored data. Existing data remains encrypted with the previous key unless reprocessed.

## Learn more

* [Customer-managed key encryption](../concepts/encryption-keys-portal.md)
* [Disable local auth](disable-local-auth.md)
