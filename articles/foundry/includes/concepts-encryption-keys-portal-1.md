---
title: Include file
description: Include file
author: jonburchel
ms.reviewer: deeikele
ms.author: jburchel
ms.service: microsoft-foundry
ms.topic: include
ms.date: 05/04/2026
ms.custom: include
---

## Benefits of CMKs

- The ability to use your own keys to encrypt data at rest.
- Integration with organizational security and compliance policies.
- The ability to rotate or revoke keys for enhanced control over access to encrypted data.

## Prerequisites

To configure a CMK for Foundry, you need:

- An active Azure subscription to create and manage Azure resources.

- An existing key vault or Managed HSM to store your keys. These requirements also apply:
  - Deploy the key store and the Foundry resource in the same Azure region.
  - Enable soft delete and purge protection on the key store to help safeguard customer-managed keys from accidental or malicious deletion (required by Azure).
  
  To create a key vault, see [Quickstart: Create a key vault by using the Azure portal](/azure/key-vault/general/quick-create-portal). To create a Managed HSM, see [Quickstart: Provision and activate a Managed HSM by using the Azure portal](/azure/key-vault/managed-hsm/quick-create-portal).

- A managed identity configuration:

  - A system-assigned managed identity enabled for your Foundry resource.
  - A user-assigned managed identity. See [Create a user-assigned managed identity](/entra/identity/managed-identities-azure-resources/manage-user-assigned-managed-identities-azure-portal?pivots=identity-mi-methods-azp#create-a-user-assigned-managed-identity).

- Key store permissions:

  - For Key Vault with Azure RBAC, assign the Key Vault Crypto User role to the managed identity.
  - For Key Vault with vault access policies, grant key-specific permissions to the managed identity, such as `unwrapKey` and `wrapKey`.
  - For Managed HSM, assign the Managed HSM Crypto User role to the managed identity at the appropriate scope. For more information, see [Managed HSM local RBAC built-in roles](/azure/key-vault/managed-hsm/built-in-roles).

- Sufficient Azure permissions:

  - Owner or User Access Administrator role on the key vault to assign RBAC roles. For Managed HSM, Managed HSM Administrator role to assign local RBAC role assignments.
  - Contributor or Owner role on the Foundry resource to configure encryption settings.

Before you configure a CMK, be sure to deploy your resources in a supported region. For more information on regional support for Foundry features, see [Microsoft Foundry feature availability across cloud regions](../reference/region-support.md).

## Key store networking configurations

When you use private networking with your Foundry resource, the customer-provided Azure Key Vault or Managed HSM that hosts the CMK supports the following configurations:

- **Private link endpoint with "Allow trusted Microsoft services" enabled**: The key store uses a private endpoint for connectivity and also permits access from trusted Microsoft services. This is the recommended configuration for environments that require private connectivity.
- **"Allow trusted Microsoft services" enabled (without a private endpoint)**: The key store allows access from trusted Microsoft services over the public endpoint. Enable this setting to ensure that the Foundry resource can access the key store for encryption operations.

To configure trusted services access, see [Configure Azure Key Vault firewalls and virtual networks](/azure/key-vault/general/network-security) or [Managed HSM network security](/azure/key-vault/managed-hsm/secure-your-managed-hsm).

## Steps to configure a CMK

### Step 1: Create or import a key in the key store

To generate a key in Azure Key Vault:

1. In the Azure portal, go to your key vault.

1. Under **Settings**, select **Keys**.

1. Select **+ Generate/Import**.

1. Enter a key name, choose the key type (such as RSA or HSM-backed), and configure key size (2048-bit minimum) and expiration details.

1. Select **Create** to save the new key.

   The new key appears in the **Keys** list.

To generate a key in Azure Managed HSM, see [Create an HSM key](/azure/key-vault/managed-hsm/key-management).

Keep these considerations in mind:

- Projects can be updated from Microsoft-managed keys to CMKs but not reverted.
- Project CMKs can be updated only to keys in the same key store.
- Storage-related charges for CMK encryption continue during soft-deleted retention.

For more information, see [About keys](/azure/key-vault/keys/about-keys).

To import a key into Key Vault:

1. In your key vault, go to the **Keys** section.

1. Select **+ Generate/Import**, and then choose the **Import** option.

1. Upload the key material and provide the necessary details for key configuration.

1. Follow the prompts to complete the import process.

To import a key into Managed HSM, see [Import HSM-protected keys to Managed HSM](/azure/key-vault/managed-hsm/hsm-protected-keys-byok).

### Step 2: Grant key store permissions to managed identities

Configure appropriate permissions for the system-assigned or user-assigned managed identity to access the key store:

#### Key Vault

1. In the Azure portal, go to your key vault.

1. Select **Access Control (IAM)**.

1. Select **+ Add role assignment**.

1. Assign the Key Vault Crypto User role to the system-assigned managed identity of the Foundry resource or to the user-assigned managed identity.

   The managed identity appears in the role assignments list for the key vault.

#### Managed HSM

Managed HSM uses a separate, local RBAC system from Azure RBAC. Assign roles by using `az keyvault role assignment create` or the Managed HSM data plane:

1. As a Managed HSM Administrator, assign the **Managed HSM Crypto User** role to the system-assigned or user-assigned managed identity of the Foundry resource. Scope the assignment to the key or to the appropriate scope for your scenario.

1. Verify the assignment with `az keyvault role assignment list`.

For more information, see [Managed HSM access control](/azure/key-vault/managed-hsm/access-control).

### Step 3: Enable the CMK in Foundry

You can enable CMKs either during the creation of a Foundry resource or by updating an existing resource. During resource creation, the wizard guides you to use a user-assigned or system-assigned managed identity. It also guides you to select a key vault or Managed HSM where your key is stored.

If you're updating an existing Foundry resource, use these steps to enable a CMK:

1. In the Azure portal, open the Foundry resource.

1. Go to **Resource Management** > **Encryption**.

1. Select **Customer-Managed Keys** as the encryption type.

1. Enter the key store URL (key vault URL or Managed HSM URL) and the key name.

1. Select **Save**.

To verify the configuration, go to **Resource Management** > **Encryption** and confirm that **Customer-Managed Keys** shows as the active encryption type with your key store and key name displayed.

## Vault access: Azure RBAC vs. vault access policies

Azure Key Vault supports two models for managing access permissions:

- Azure RBAC (recommended):
  - Provides centralized access control by using Microsoft Entra roles.
  - Simplifies permission management for resources across Azure.
  - Requires the Key Vault Crypto User role.

- Vault access policies:
  - Allow granular access control specific to Key Vault resources.
  - Are suitable for configurations where legacy or isolated permission settings are necessary.

Choose the model that aligns with your organizational requirements. For new deployments, use Azure RBAC. Use vault access policies only when existing organizational requirements mandate them.

Azure Managed HSM uses its own local RBAC system separate from Azure RBAC. For Managed HSM, assign the Managed HSM Crypto User role to the managed identity. For more information, see [Managed HSM local RBAC built-in roles](/azure/key-vault/managed-hsm/built-in-roles).

## Monitoring and rotating keys

To maintain optimal security and compliance, implement the following practices:

- **Enable diagnostics**: Monitor key usage and access activity by enabling diagnostic logging in Azure Monitor or Log Analytics for your key vault or Managed HSM.
- **Rotate keys regularly**: Periodically create a new version of your key in your key store. Update the Foundry resource to reference the latest key version in its encryption settings.
- **Understand key revocation impact**: If you revoke or delete a CMK, data encrypted with that key becomes inaccessible until the key is restored. Don't purge the key store or key version without first verifying that the data is no longer needed.

## Troubleshooting

| Issue | Resolution |
| ----- | ---------- |
| **403 Forbidden** when enabling CMK | For Key Vault, verify the managed identity has the Key Vault Crypto User role (RBAC) or `unwrapKey` and `wrapKey` permissions (vault access policies). For Managed HSM, verify the managed identity has the Managed HSM Crypto User role at the appropriate scope. |
| **Key store not found** | Confirm the key vault or Managed HSM is in the same Azure region as the Foundry resource. |
| **Key version not supported** | Use an RSA key with a minimum size of 2048 bits. |
| **Data inaccessible after key revocation** | Restore the key version in your key store. Data remains inaccessible until the key is restored. Contact Azure support if the key store was purged. |

## Related content

- [Azure Key Vault documentation](/azure/key-vault/)
- [Azure Managed HSM documentation](/azure/key-vault/managed-hsm/)
- [GitHub Bicep example: Customer-managed keys with a user-assigned identity](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/32-customer-managed-keys-user-assigned-identity)
- [Overview of Azure managed identities](/entra/identity/managed-identities-azure-resources/overview)
