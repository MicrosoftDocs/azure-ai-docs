---
title: Customer-Managed Keys (CMKs) for Microsoft Foundry
titleSuffix: Microsoft Foundry
description: Learn how to use CMKs for enhanced encryption and data security in Microsoft Foundry. Configure Azure Key Vault integration and meet compliance requirements.
monikerRange: 'foundry-classic || foundry'
ms.author: jburchel 
author: jonburchel 
ms.reviewer: deeikele
ms.date: 09/29/2025
ms.service: azure-ai-services
ms.topic: concept-article
ms.custom:
  - ignite-2023
  - build-aifnd
  - build-2025
  - references-regions
ai-usage: ai-assisted 
# Customer intent: As an admin, I want to understand how I can use my own encryption keys with Microsoft Foundry.
---

# Customer-managed keys (CMKs) for Microsoft Foundry

[!INCLUDE [version-banner](../includes/version-banner.md)]

::: moniker range="foundry-classic"

> [!TIP]
> An alternate hub-focused article is available: [Customer-managed keys for hub projects](hub-encryption-keys-portal.md).

Customer-managed key (CMK) encryption in [!INCLUDE [classic-link](../includes/classic-link.md)] gives you control over encryption of your data. Use CMKs to add an extra protection layer and help meet compliance requirements with Azure Key Vault integration.

::: moniker-end

::: moniker range="foundry"

Customer-managed key (CMK) encryption in [!INCLUDE [foundry-link](../default/includes/foundry-link.md)] gives you control over encryption of your data. Use CMKs to add an extra protection layer and help meet compliance requirements with Azure Key Vault integration.

::: moniker-end

Microsoft Foundry provides robust encryption capabilities, including the ability to use CMKs stored in Key Vault to help secure your sensitive data.

This article explains the concept of encryption with CMKs and provides step-by-step guidance for configuring CMKs by using Key Vault. It also discusses:

- Encryption models and access control methods like Azure role-based access control (RBAC) and vault access policies.
- Ensuring compatibility with system-assigned managed identities and user-assigned managed identities.

## Benefits of CMKs

- The ability to use your own keys to encrypt data at rest.
- Integration with organizational security and compliance policies.
- The ability to rotate or revoke keys for enhanced control over access to encrypted data.

## Prerequisites

To configure a CMK for Foundry, you need:

- An active Azure subscription to create and manage Azure resources.

- An existing key vault to store your keys. These requirements also apply:
  - Deploy the key vault and the Foundry resource in the same Azure region.
  - Enable soft delete and purge protection on the key vault to help safeguard customer-managed keys from accidental or malicious deletion (required by Azure).
  
  To create a key vault, see [Quickstart: Create a key vault by using the Azure portal](/azure/key-vault/general/quick-create-portal).

- A managed identity configuration:

  - A system-assigned managed identity enabled for your Foundry resource.
  - A user-assigned managed identity. See [Create a user-assigned managed identity](/entra/identity/managed-identities-azure-resources/manage-user-assigned-managed-identities-azure-portal?pivots=identity-mi-methods-azp#create-a-user-assigned-managed-identity).

- Key Vault permissions:

  - If you're using Azure RBAC, assign the Key Vault Crypto User role to the managed identity.
  - If you're using vault access policies, grant key-specific permissions to the managed identity, such as `unwrapKey` and `wrapKey`.

Before you configure a CMK, be sure to deploy your resources in a supported region. For more information on regional support for Foundry features, see [Microsoft Foundry feature availability across cloud regions](../reference/region-support.md).

## Steps to configure a CMK

### Step 1: Create or import a key in the key vault

To generate a key:

1. In the Azure portal, go to your key vault.

1. Under **Settings**, select **Keys**.

1. Select **+ Generate/Import**.

1. Enter a key name, choose the key type (such as RSA or HSM-backed), and configure key size and expiration details.

1. Select **Create** to save the new key.

Keep these considerations in mind:

- Projects can be updated from Microsoft-managed keys to CMKs but not reverted.
- Project CMKs can be updated only to keys in the same key vault.
- Storage-related charges for CMK encryption continue during soft-deleted retention.

For more information, see [About keys](/azure/key-vault/keys/about-keys).

To import a key:

1. In your key vault, go to the **Keys** section.

1. Select **+ Generate/Import**, and then choose the **Import** option.

1. Upload the key material and provide the necessary details for key configuration.

1. Follow the prompts to complete the import process.

### Step 2: Grant key vault permissions to managed identities

Configure appropriate permissions for the system-assigned or user-assigned managed identity to access the key vault:

1. In the Azure portal, go to your key vault.

1. Select **Access Control (IAM)**.

1. Select **+ Add role assignment**.

1. Assign the Key Vault Crypto User role to the system-assigned managed identity of the Foundry resource or to the user-assigned managed identity.

### Step 3: Enable the CMK in Foundry

You can enable CMKs either during the creation of a Foundry resource or by updating an existing resource. During resource creation, the wizard guides you to use a user-assigned or system-assigned managed identity. It also guides you to select a key vault where your key is stored.

If you're updating an existing Foundry resource, use these steps to enable a CMK:

1. In the Azure portal, open the Foundry resource.

1. Go to **Resource Management** > **Encryption**.

1. Select **Customer-Managed Keys** as the encryption type.

1. Enter the key vault URL and the key name.

## Vault access: Azure RBAC vs. vault access policies

Azure Key Vault supports two models for managing access permissions:

- Azure RBAC (recommended):
  - Provides centralized access control by using Microsoft Entra roles.
  - Simplifies permission management for resources across Azure.
  - Requires the Key Vault Crypto User role.

- Vault access policies:
  - Allow granular access control specific to Key Vault resources.
  - Are suitable for configurations where legacy or isolated permission settings are necessary.

Choose the model that aligns with your organizational requirements.

## Monitoring and rotating keys

To maintain optimal security and compliance, implement the following practices:

- **Enable Key Vault diagnostics**: Monitor key usage and access activity by enabling diagnostic logging in Azure Monitor or Log Analytics.
- **Rotate keys regularly**: Periodically create a new version of your key in Key Vault. Update the Foundry resource to reference the latest key version in its encryption settings.

## Related content

- [Azure Key Vault documentation](/azure/key-vault/)
- [GitHub Bicep example: Customer-managed keys with a user-assigned identity](https://github.com/azure-ai-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/32-customer-managed-keys-user-assigned-identity)
- [Overview of Azure managed identities](/azure/active-directory/managed-identities-azure-resources/overview)
