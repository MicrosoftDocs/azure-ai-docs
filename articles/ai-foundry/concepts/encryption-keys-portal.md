---
title: Customer-managed keys (CMK) for Microsoft Foundry
titleSuffix: Microsoft Foundry
description: Learn how to use customer-managed keys (CMK) for enhanced encryption and data security in Microsoft Foundry. Configure Azure Key Vault integration and meet compliance requirements.
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

# Customer-managed keys (CMK) for Microsoft Foundry

[!INCLUDE [version-banner](../includes/version-banner.md)]

::: moniker range="foundry-classic"

> [!TIP]
> An alternate hub-focused CMK article is available: [Customer-managed keys for hub projects](hub-encryption-keys-portal.md).


Customer-managed key (CMK) encryption in [!INCLUDE [classic-link](../includes/classic-link.md)] gives you control over encryption of your data. Use CMKs to add an extra protection layer and help meet compliance requirements with Azure Key Vault integration.

::: moniker-end

::: moniker range="foundry"

Customer-managed key (CMK) encryption in [!INCLUDE [foundry-link](../default/includes/foundry-link.md)] gives you control over encryption of your data. Use CMKs to add an extra protection layer and help meet compliance requirements with Azure Key Vault integration.

::: moniker-end

Microsoft Foundry provides robust encryption capabilities, including the ability to use **customer-managed keys (CMKs)** stored in **Azure Key Vault** to secure your sensitive data. This article explains the concept of encryption with CMKs and provides step-by-step guidance for configuring CMK using Azure Key Vault. It also discusses encryption models and access control methods like **Azure Role-Based Access Control (RBAC)** and **Vault Access Policies** and ensuring compatibility with **system-assigned managed identities** and **user-assigned managed identities (UAI)**.

## Why use customer-managed keys?

With CMK, you gain full control over encryption keys, providing enhanced protection for sensitive data and helping meet compliance requirements. The key benefits of using CMKs include:

- Using your own keys to encrypt data at rest.

- Integration with organizational security and compliance policies.

- The ability to rotate or revoke keys for enhanced control over access to encrypted data.

Microsoft Foundry supports encryption with your CMKs stored in **Azure Key Vault**, leveraging industry-leading security features.

## Prerequisites

To configure CMK for Microsoft Foundry, ensure the following prerequisites are met:

1.  **Azure Subscription**:  
    You need an active Azure subscription to create and manage Azure resources.

1.  **Azure Key Vault**:

    - You need an existing Azure Key Vault to store your keys.
    - You must deploy the Key Vault and the Microsoft Foundry resource in the same Azure region.
    - Enable Soft Delete and Purge Protection on Key Vault to safeguard customer-managed keys from accidental or malicious deletion (required by Azure)
    - Follow this guide to create a Key Vault: [Quickstart: Create a Key Vault using Azure portal](/azure/key-vault/general/quick-create-portal).

1.  **Managed Identity Configuration**:

    - **System-assigned managed identity**: Ensure your Microsoft Foundry resource has enabled a system-assigned managed identity.
    - **User-assigned managed identity**: You can use the following link to create a [User-Assigned Managed Identity](/entra/identity/managed-identities-azure-resources/manage-user-assigned-managed-identities-azure-portal?pivots=identity-mi-methods-azp#create-a-user-assigned-managed-identity)


1.  **Key Vault Permissions**:

    - If you're using **Azure RBAC**, assign Key Vault Crypto User role to the managed identity.
    - If you're using **Vault Access Policies**, grant key-specific permissions to the managed identity, such as **unwrap key** and **wrap key**.

Before configuring CMK, make sure you deploy your resources in a supported region. Refer to [Microsoft Foundry feature availability across cloud regions](../reference/region-support.md) for more details on regional support for Microsoft Foundry features.


## Steps to Configure CMK

### Step 1. Create or Import a Key in Azure Key Vault

You store Customer-Managed Keys (CMKs) in **Azure Key Vault**. You can either generate a new key within the Key Vault or import an existing key. Follow the steps in the following sections:

**Generate a Key**

1. Go to your Azure Key Vault in the Azure portal.
1. Under **Settings**, select **Keys**.
1. Select **+ Generate/Import**.
1. Enter a key name, choose the key type (such as RSA or HSM-backed), and configure key size and expiration details.
1. Select **Create** to save the new key.

* Projects can be updated from Microsoft-managed keys to CMKs but not reverted.
* Project CMK can be updated only to keys in the same Key Vault instance.
* Storage-related charges for CMK encryption continue during soft-deleted retention.
   For more information, see [Create and Manage Keys in Azure Key Vault](/azure/key-vault/keys/about-keys).

**Import a Key**

1. Go to the **Keys** section in your Key Vault.
1. Select **+ Generate/Import** and choose the **Import** option.
1. Upload the key material and provide the necessary key configuration details.
1. Follow the prompts to complete the import process.

### Step 2. Grant Key Vault permissions to managed identities

Configure appropriate permissions for the **system-assigned** or **user-assigned managed identity** to access the Key Vault.

**System-assigned managed identity**

1. Go to the Key Vault in the Azure portal.
1. Select **Access Control (IAM)**.
1. Select **+ Add role assignment**.
1. Assign the Key Vault Crypto User role to the **system-assigned managed identity** of the Microsoft Foundry resource or the **User-assigned managed identity**


### Step 3. Enable CMK in Microsoft Foundry

You can enable Customer-Managed Keys (CMK) either during the creation of a Microsoft Foundry resource or by updating an existing resource. During resource creation, the wizard will guide you to use either user-assigned or system-assigned managed identity, select a user-assigned managed identity, and select a key vault where your key is stored.

You can follow the steps below if you're updating an existing Microsoft Foundry resource to enable CMK:

1. Open the Microsoft Foundry resource in the Azure portal.
1. Go to the **Encryption** under **Resource Management** section.
1. Select **Customer-Managed Keys** as the encryption type.
1. Enter the **Key Vault URL** and the key name.


**Key Vault Access Design: Azure RBAC vs. Vault Access Policies**

Azure Key Vault supports two models for managing access permissions:

1.  **Azure RBAC (Recommended)**:
    - Provides centralized access control using Azure AD roles.
    - Simplifies permission management for resources across Azure.
    - Use Key Vault Crypto User role.
1.  **Vault Access Policies**:
    - Allows granular access control specific to Key Vault resources.
    - Suitable for configurations where legacy or isolated permission settings are necessary.

Choose the model that aligns with your organizational requirements.

**Monitoring and Rotating Keys**

To maintain optimal security and compliance, implement the following practices:

1.  **Enable Key Vault Diagnostics**:  
    Monitor key usage and access activity by enabling diagnostic logging in Azure Monitor or Log Analytics.
1.  **Rotate Keys Regularly**:  
    Periodically create a new version of your key in Azure Key Vault.  
    Update the Microsoft Foundry resource to reference the latest key version in its **Encryption Settings**.

## Related content

- [Azure Key Vault Documentation](/azure/key-vault/)
- [GitHub Bicep Example: Customer-Managed Keys with UAI](https://github.com/azure-ai-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/32-customer-managed-keys-user-assigned-identity)
- [Azure Managed Identities Overview](/azure/active-directory/managed-identities-azure-resources/overview)
