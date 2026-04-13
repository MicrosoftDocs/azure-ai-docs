---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: deeikele
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Data storage

Foundry provides flexible and secure data storage options to support a wide range of AI workloads.

* **Managed storage for file upload**:
In the default setup, Foundry uses Microsoft-managed storage accounts that are logically separated and support direct file uploads for select use cases, such as OpenAI models, Assistants, and Agents, without requiring a customer-provided storage account.

* **Bring your own storage (optional)**:
Users can optionally connect their own Azure Storage accounts. Foundry tools can read inputs from and write outputs to these accounts, depending on the tool and use case.

* **Bring your own storage for storing Agent state**:

  * In the basic configuration, the Agent service stores threads, messages, and files in Microsoft-managed multitenant storage, with logical separation.
  * With the [Agent standard setup](../agents/how-to/use-your-own-resources.md), you can bring your own storage for thread and message data. In this configuration, data is isolated by project within the customer’s storage account.

* **Customer-managed key encryption**:
  By default, Azure services use Microsoft-managed encryption keys to encrypt data in transit and at rest. Data is encrypted and decrypted using FIPS 140-2 compliant 256-bit AES encryption. Encryption and decryption are transparent, meaning encryption and access are managed for you. Your data is secure by default and you don't need to modify your code or applications to take advantage of encryption.

  Before you enable customer-managed keys for Foundry, confirm these prerequisites:

  - Key Vault is deployed in the same Azure region as your Foundry resource.
  - Soft delete and purge protection are enabled on Key Vault.
  - Managed identities have required key permissions, such as the **Key Vault Crypto User** role when using Azure RBAC.

* **Bring your own Key Vault**:
  By default, Foundry stores all API key-based connection secrets in a managed Azure Key Vault. For users that prefer to manage this themselves, they can connect their key vault to the Foundry resource. One Azure Key Vault connection manages all project and resource level connection secrets. For more information, see [how to set up an Azure Key Vault connection to Foundry](../how-to/set-up-key-vault-connection.md).

  When you use customer-managed keys, your data on Microsoft-managed infrastructure is encrypted by using your keys.
  
  To learn more about data encryption, see [customer-managed keys for encryption with Foundry](../concepts/encryption-keys-portal.md).

## Validate architecture decisions

Before rollout, validate the following for your target environment:

1. Confirm that required models and features are available in your deployment regions. For details, see [Feature availability across cloud regions](../reference/region-support.md).
1. Confirm that role assignments are scoped correctly at both the Foundry resource and project levels. For details, see [Role-based access control for Microsoft Foundry](../concepts/rbac-foundry.md).
1. Confirm network isolation requirements and private access paths. For details, see [How to configure a private link for Foundry](../how-to/configure-private-link.md).
1. Confirm encryption and secret-management requirements, including customer-managed keys and Azure Key Vault integration. For details, see [Customer-managed keys for encryption with Foundry](../concepts/encryption-keys-portal.md) and [how to set up an Azure Key Vault connection to Foundry](../how-to/set-up-key-vault-connection.md).

## Related content

* [Foundry rollout across my organization](../concepts/planning.md)
* [Role-based access control for Microsoft Foundry](../concepts/rbac-foundry.md).
* [Customer-managed keys for encryption with Foundry](../concepts/encryption-keys-portal.md)
* [How to configure a private link for Foundry](../how-to/configure-private-link.md)
* [Bring-your-own resources with the Agent service](../agents/how-to/use-your-own-resources.md)
