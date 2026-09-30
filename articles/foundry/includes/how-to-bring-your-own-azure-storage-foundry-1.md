---
title: Include file
description: Include file
author: s-polly
ms.reviewer: andyaviles
ms.author: scottpolly
ms.service: microsoft-foundry
ms.topic: include
ms.date: 08/18/2026
ms.custom: include
ai-usage: ai-assisted
---

[!INCLUDE [feature-preview](feature-preview.md)]

Microsoft Foundry brings Agents, Azure OpenAI, Speech, and Language services together under one unified resource type. Bring-your-own-storage (BYOS) lets you route data produced by these capabilities to an Azure Storage account that you own and govern. The configuration patterns align with (and provide backward compatibility to) earlier standalone Speech and Language resource types.

This article shows you how to connect your storage to Foundry by using two overarching approaches:

- **Connections**: recommended baseline for most features. Connections provide the shared data pointer.
- **Capability settings**: declare the storage account that Foundry Agent Service uses for agent files.
- **userOwnedStorage field:** a resource-level binding used only by Speech and Language.

## Prerequisites

Before connecting your storage, ensure you have:

[!INCLUDE [azure-subscription](azure-subscription.md)]

1. An [Azure Storage account](/azure/storage/common/storage-account-create?tabs=azure-portal) in the same subscription (Blob Storage supported) with the following configuration:
   - `allowSharedKeyAccess` set to `false`. Foundry uses identity-based (Microsoft Entra) access with the project managed identity and Azure RBAC, so shared key access isn't required.
   - `minimumTlsVersion` set to `TLS1_2`
   - `allowBlobPublicAccess` set to `false`
   - `allowCrossTenantReplication` set to `false` (recommended hardening)

1. Contributor or Owner permissions on both the Foundry resource and the storage account.
1. Clarity on which features you plan to use (Agents, Evaluations, Datasets, Content Understanding, Speech, Language).
1. (Optional) A plan for customer-managed keys (CMK) encryption on the storage account.

> [!TIP]
> See [Azure Storage documentation](/azure/storage/) for guidance on security, networking, and encryption options.

## Understand storage connection approaches

| Approach | What it is | Features supported | Scope | When to use |
| --- | --- | --- | --- | --- |
| Foundry connections (shared data pointer) | Sub-resource holding endpoint and authentication; grants project users indirect access | Agents, Evaluations, Datasets, Content Understanding | Resource or project level | Default pattern for most scenarios |
| Capability settings (agent storage declaration) | Account and project properties naming the storage account that holds agent files | Agents (standard setup) | Account and project level | When agents must store files in a storage account you own |
| userOwnedStorage field (resource storage binding) | Resource property assigning one storage account for Speech and Language (shared) | Speech, Language | Resource level only | To enable customer-managed storage for Speech and Language at creation time |

### Foundry connections

Foundry connections act as shared data pointers across Foundry capabilities (agents, evaluations, datasets, content understanding). Each connection wraps the target storage endpoint plus authentication so users with project access can use the data without direct storage account permissions. Use connections as the default pattern for evaluations, datasets, and content understanding.

### Capability settings

Capability settings are properties on the Foundry account and project that declare which Azure resources hold agent state, vector data, and files. Set `blobStore` to the resource ID of your storage account, and Agent Service provisions the required underlying infrastructure and the connection to that account. You don't create or bind the connection yourself.

If you don't set `blobStore`, Foundry uses Microsoft-managed storage for agent files. See [Configure agent capability settings](../how-to/configure-capability-settings.md) for settings, permissions, and Bicep examples.

### userOwnedStorage (resource storage binding)

The `userOwnedStorage` field enables customer-managed storage for Speech and Language capabilities. Set this field during resource creation at the resource level, so all projects within the resource share the same storage account.

Speech and Language capabilities share the storage account but use different containers within it. The setting applies at the resource level and can't be changed after creation without recreating the resource.

If strict data isolation is required between Speech and Language scenarios, create separate Foundry resources with different storage accounts.

> [!IMPORTANT]
> If you delete or move (change resource ID of) the storage account bound by `userOwnedStorage`, Speech and Language stop functioning. Consider attempting account recovery first: [Recover a storage account](/azure/storage/common/storage-account-recover). Otherwise you must recreate the Foundry resource.
