---
title: Customer-managed keys for hub projects
titleSuffix: Azure AI Foundry
description: Use customer-managed keys (CMK) with hub-based projects in Azure AI Foundry.
ms.author: jburchel 
author: jonburchel 
ms.reviewer: deeikele
ms.date: 09/12/2025
ms.service: azure-ai-services
ms.topic: concept-article
ms.custom:
  - build-2025
ai-usage: ai-assisted
---

# Customer-managed keys for hub projects

> [!NOTE]
> An alternate Foundry (fdp) project CMK article is available: [Customer-managed keys for encryption with Azure AI Foundry (Foundry projects)](encryption-keys-portal.md).

Hub-based projects require configuring CMK on each underlying service (Azure AI Hub, Storage) for end-to-end encryption control.

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

Portal steps during hub creation:
1. Encryption tab: choose key vault & key.
2. (Optional) Select service-side encryption setting.

## Rotation

Rotate within same Key Vault; update hub to new key URI. Existing data not re-encrypted; new data uses new key.

Limitations:
- Same Key Vault only.
- Cannot revert from CMK to Microsoft-managed.
- Hub resources cannot toggle post-creation between key types.

## Revocation

Remove access policy or delete key versions. Revocation halts new fine-tunes / downloads but existing deployments serve until deleted.

## Cost considerations

Dedicated hosting of certain back-end services under CMK results in extra subline items in Cost Management.

## Related content

- Hub creation
- Project encryption (see encryption-keys-portal.md)
- Key Vault overview
