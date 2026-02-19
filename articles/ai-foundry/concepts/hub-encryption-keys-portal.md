---
title: Customer-managed keys for hub projects
titleSuffix: Microsoft Foundry
description: Use customer-managed keys (CMK) with hub-based projects in Microsoft Foundry.
ms.author: jburchel 
author: jonburchel 
ms.reviewer: deeikele
ms.date: 10/24/2025
ms.service: azure-ai-services
ms.topic: concept-article
ms.custom:
  - build-2025
  - hub-only
ai-usage: ai-assisted
---

# Customer-managed keys for hub projects

[!INCLUDE [uses-hub-only](../includes/uses-hub-only.md)]

> [!TIP]
> An alternate Foundry project article is available: [Customer-managed keys for encryption with Microsoft Foundry (Foundry projects)](encryption-keys-portal.md).

Hub-based projects require configuring CMK on each underlying service (Azure AI Hub, Storage) for end-to-end encryption control.

## Architecture

Azure AI Hub resource acts as a gateway to multiple Azure services. Configure CMK per service:
- Azure AI Hub / hub project (Machine Learning workspace) – see ML data encryption docs.
- Foundry resources – AES-256 FIPS 140-2 compliant.
- Azure Storage accounts – store uploaded data (configure CMK in Storage).

## Data storage options

Two options when using CMK with hubs:
1. Service-side encrypted data stored in Microsoft subscription (recommended). Document-level CMK, dedicated per-customer Azure AI Search instance for isolation.
2. Legacy managed resource group in your subscription (Cosmos DB, Storage, Azure AI Search). Backward compatibility only.

Managed resource group naming: `azureml-rg-hubworkspacename_GUID`. Deleted when hub deleted.

### Managed resource data
| Service | Use | Example |
|---------|-----|---------|
| Azure Cosmos DB | Metadata for projects/tools | Flow creation timestamps |
| Azure AI Search | Indices for querying content | Index of model deployment names |
| Azure Storage | Orchestration instructions | JSON flow representations |

## Key Vault usage

Store CMKs in Azure Key Vault (same region & tenant). Enable soft-delete & purge protection. Allow trusted services if firewalling.

Grant hub system-assigned managed identity: Get, Wrap, Unwrap permissions.

Supported keys: RSA / RSA-HSM 2048.

## Create a hub with customer-managed keys

For customers in highly regulated industries, creating a hub with customer-managed keys (CMK) is a critical requirement.  

### Prerequisites

Before creating your hub with CMK:

1. **Create and configure Azure Key Vault** in the same region and tenant as your planned hub:
   - Enable soft-delete
   - Enable purge protection
   - If using firewall, allow trusted Microsoft services
   - Prepare an RSA or RSA-HSM 2048-bit key

1. **Plan your data storage approach**:
   - Service-side encryption (recommended): Data stored in Microsoft subscription
   - Legacy approach: Managed resource group in your subscription

1. **Ensure proper permissions**: You need permissions to create the hub and assign Key Vault access policies

### Configure CMK during hub creation

To create a hub with CMK enabled, follow these steps in the Azure portal:

1. Start the **Create an Azure AI Hub** wizard.
1. On the **Basics** tab, fill in the required details.
1. Navigate to the **Encryption** tab.
1. Select **Customer-managed keys**.
1. Select **Select a key vault and key**.
1. Choose your existing Key Vault and the key you created in the prerequisites.
1. (Optional) Configure the **Service-side encryption** setting if needed.
1. Continue through the remaining tabs (Networking, Tags) and select **Review + create**.
1. Select **Create** to finish the hub creation.

After the hub is created, the system assigns a managed identity that receives Get, Wrap, and Unwrap permissions for the specified key.

## Customer-managed key constraints (permanent)

- CMK must be configured at hub creation time; you cannot add CMK to an existing hub.
- You cannot switch between customer-managed keys and Microsoft-managed keys after creation.
- Key rotation is supported only within the same Azure Key Vault; changing Key Vaults is not supported.  

## Rotation

Rotate within the same Key Vault by updating the hub to a new key URI. Existing data isn't re-encrypted; new data uses the new key.  

## Revocation

Remove access policy or delete key versions. Revocation halts new fine-tunes or downloads, but existing deployments continue to serve until deleted.

## Cost considerations

Dedicated hosting of certain back-end services under CMK results in extra subline items in Cost Management.

## Related content

* [Disable local authorization](../how-to/disable-local-auth.md)
* [What is Azure Key Vault?](/azure/key-vault/general/overview)