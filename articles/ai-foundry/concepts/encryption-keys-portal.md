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
ai-usage: ai-assisted 
# Customer intent: As an admin, I want to understand how I can use my own encryption keys with Microsoft Foundry.
---

# Customer-managed keys (CMK) for Microsoft Foundry

Microsoft Foundry provides robust encryption capabilities, including the ability to use **customer-managed keys (CMKs)** stored in **Azure Key Vault** to secure your sensitive data. This article explains the concept of encryption with CMKs and provides step-by-step guidance for configuring CMK using Azure Key Vault. It also discusses encryption models and access control methods like **Azure Role-Based Access Control (RBAC)** and **Vault Access Policies**, ensuring compatibility with **system-assigned managed identities**. Support for **user-assigned managed identities (UAI)** is currently available only via Bicep templates.

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

    - Follow this guide to create a Key Vault: [Quickstart: Create a Key Vault using Azure Portal](Microsoft/azure/key-vault/general/quick-create-portal).

1.  **Managed Identity Configuration**:

    - **System-assigned managed identity**: Ensure your Microsoft Foundry resource has enabled a system-assigned managed identity.

    - **User-assigned managed identity**: **Support for UAI is currently available only via Bicep templates.** Refer to the Bicep template example: [GitHub Repository: Customer-Managed Keys with User-Assigned Identity](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup/32-customer-managed-keys-user-assigned-identity).

1.  **Key Vault Permissions**:

    - If you're using **Azure RBAC**, assign roles like Key Vault Crypto Officer or Key Vault Contributor to the managed identity.

    - If you're using **Vault Access Policies**, grant key-specific permissions to the managed identity, such as **unwrap key** and **wrap key**.

## Regional availability note (UAI for CMK)

Support for **Customer-Managed Keys (CMK) with User-Assigned Managed Identities (UAI)** is currently available in **all Azure regions** except for the following regions:

- **United States**:  
  westus, centralus, southcentralus, westus2

- **Europe**:  
  westeurope, ukwest, switzerlandwest, germanywestcentral, francecentral, denmarkeast, polandcentral, swedencentral, norwayeast

- **Asia-Pacific**:  
  taiwannorthwest, australasia (australiaeast, newzealandnorth), southeastasia, japaneast, koreacentral, indonesiacentral, malaysiawest, centralindia

- **Middle East**:  
  israelcentral, qatarcentral

- **Africa**:  
  southafricanorth

- **Canada**:  
  canadaeast

- **Latin America**:  
  mexicocentral

- **Azure China**:  
  China East, China East 2, China North, China North 2

- **Azure US Government**:  
  US Gov Virginia, US Gov Arizona, US Gov Texas, US Gov Iowa

Before configuring CMK with UAI, make sure you deploy your resources in a supported region.

## Steps to Configure CMK

### Step 1. Create or Import a Key in Azure Key Vault

You store Customer-Managed Keys (CMKs) in **Azure Key Vault**. You can either generate a new key within the Key Vault or import an existing key. Follow the steps in the following sections:

**Generate a Key**

1. Go to your Azure Key Vault in the Azure portal.
1. Under **Settings**, select **Keys**.
1. Select **+ Generate/Import**.
1. Enter a key name, choose the key type (such as RSA or HSM-backed), and configure key size and expiration details.
1. Select **Create** to save the new key.

   For more information, see [Create and Manage Keys in Azure Key Vault](Microsoft/azure/key-vault/keys/about-keys).

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
1. Assign the Key Vault Crypto Officer, Key Vault Contributor, or a similar role to the **system-assigned managed identity** of the Microsoft Foundry resource.

**User-assigned managed identity**

> [!NOTE]  
> [GitHub Repository: Customer-Managed Keys with User-Assigned Identity](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup/32-customer-managed-keys-user-assigned-identity).

1. Use the provided Bicep templates to deploy a user-assigned identity and configure Key Vault permissions.

1. After deployment, confirm the user-assigned identity has appropriate roles (such as Key Vault Crypto Officer) or permissions on the Key Vault.

### Step 3. Enable CMK in Microsoft Foundry

1. Open the Microsoft Foundry resource in the Azure portal.
1. Go to the **Encryption Settings** section.
1. Select **Customer-Managed Keys** as the encryption type.
1. Enter the **Key Vault URL** and the key name.
1. If you use **User-Assigned Managed Identity**, make sure the deployment through Bicep templates is complete, as the identity and associated permissions are already configured.

**Key Vault Access Design: Azure RBAC vs. Vault Access Policies**

Azure Key Vault supports two models for managing access permissions:

1.  **Azure RBAC (Recommended)**:
    - Provides centralized access control using Azure AD roles.
    - Simplifies permission management for resources across Azure.
    - Recommended roles include Key Vault Crypto Officer or Key Vault Contributor.
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
- [GitHub Bicep Example: Customer-Managed Keys with UAI](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup/32-customer-managed-keys-user-assigned-identity)
- [Azure Managed Identities Overview](/azure/active-directory/managed-identities-azure-resources/overview)
