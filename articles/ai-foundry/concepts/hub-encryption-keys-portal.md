---
title: Customer-managed keys for hub projects
titleSuffix: Azure AI Foundry
description: Use customer-managed keys (CMK) with hub-based projects in Azure AI Foundry.
ms.author: jburchel 
author: jonburchel 
ms.reviewer: deeikele
ms.date: 10/24/2025
ms.service: azure-ai-services
ms.topic: concept-article
ms.custom:
  - build-2025
ai-usage: ai-assisted
---

# Customer-managed keys for hub projects

> [!NOTE]
> An alternate Foundry project article is available: [Customer-managed keys for encryption with Azure AI Foundry (Foundry projects)](encryption-keys-portal.md).

Hub-based projects require configuring CMK on each underlying service (Azure AI Hub, Storage) for end-to-end encryption control.

> [!IMPORTANT]
> For organizations in highly regulated industries or with strict compliance requirements, you **must** configure customer-managed keys during the initial hub creation. CMK cannot be added to an existing hub after creation. Plan your encryption strategy before creating your hub resource.

## Architecture

Azure AI Hub resource acts as a gateway to multiple Azure services. Configure CMK per service:
- Azure AI Hub / hub project (Machine Learning workspace) – see ML data encryption docs.
- Azure AI Foundry resources – AES-256 FIPS 140-2 compliant.
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

## Enable CMK (hub)

Customer-managed keys must be configured during hub creation. You cannot add CMK to an existing hub or convert a hub from Microsoft-managed keys to customer-managed keys after creation.

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

In the Azure portal during hub creation:

1. Navigate to the **Encryption** tab
1. Select **Customer-managed keys**
1. Choose your Key Vault and key
1. (Optional) Select service-side encryption setting
1. Complete the hub creation process

After the hub is created, the system assigns a managed identity that receives Get, Wrap, and Unwrap permissions for the specified key.

> [!WARNING]
> This encryption configuration is permanent. You cannot switch from customer-managed keys to Microsoft-managed keys after hub creation.

## Rotation

Rotate within same Key Vault; update hub to new key URI. Existing data not re-encrypted; new data uses new key.

Limitations:
- **CMK must be configured during hub creation** - You cannot add CMK to an existing hub or convert from Microsoft-managed keys to CMK after creation.
- Key rotation must use the same Key Vault - You cannot change to a different Key Vault.
- Cannot revert from CMK to Microsoft-managed keys.

## Revocation

Remove access policy or delete key versions. Revocation halts new fine-tunes / downloads but existing deployments serve until deleted.

## Cost considerations

Dedicated hosting of certain back-end services under CMK results in extra subline items in Cost Management.

## Related content

* [Disable local authorization](../how-to/disable-local-auth.md)
* [What is Azure Key Vault?](/azure/key-vault/general/overview)
