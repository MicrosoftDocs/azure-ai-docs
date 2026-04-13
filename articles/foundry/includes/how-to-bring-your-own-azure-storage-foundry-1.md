---
title: Include file
description: Include file
author: jonburchel
ms.reviewer: andyaviles
ms.author: jburchel
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

[!INCLUDE [feature-preview](feature-preview.md)]

Microsoft Foundry brings Agents, Azure OpenAI, Speech, and Language services together under one unified resource type. Bring-your-own-storage (BYOS) lets you route data produced by these capabilities to an Azure Storage account that you own and govern. The configuration patterns align with (and provide backwards compatibility to) earlier standalone Speech and Language resource types.

This article shows you how to connect your storage to Foundry by using two overarching approaches:

- Connections: recommended baseline for most features. Connections provide the shared data pointer.
- Capability hosts: optionally override/explicitly bind a specific feature (for example, Agents standard setup) to one connection among several.
- userOwnedStorage field: a resource-level binding used only by Speech and Language.

## Prerequisites

Before connecting your storage, ensure you have:

[!INCLUDE [azure-subscription](azure-subscription.md)]

1. An [Azure Storage account](/azure/storage/common/storage-account-create?tabs=azure-portal) in the same subscription (Blob Storage supported) with the following configuration:
   - `allowSharedKeyAccess` set to `true`
   - `minimumTlsVersion` set to `TLS1_2`
   - `allowBlobPublicAccess` set to `false`
   - `allowCrossTenantReplication` set to `false`
1. Contributor or Owner permissions on both the Foundry resource and the storage account.
1. Clarity on which features you plan to use (Agents, Evaluations, Datasets, Content Understanding, Speech, Language).
1. (Optional) A plan for customer-managed keys (CMK) encryption on the storage account.

> [!TIP]
> See [Azure Storage documentation](/azure/storage/) for guidance on security, networking, and encryption options.

## Understand storage connection approaches

| Approach | What it is | Features supported | Scope | When to use |
|----------|------------|--------------------|-------|-------------|
| Foundry connections (shared data pointer) | Sub-resource holding endpoint + auth; grants project users indirect access | Agents, Evaluations, Datasets, Content Understanding | Resource or project level | Default pattern for most scenarios |
| Capability hosts (feature override binding) | Explicit per-feature binding selecting which connection a feature uses | Agents (standard setup) | Resource and project level | When multiple connections exist and you must force one for Agents |
| userOwnedStorage field (resource storage binding) | Resource property assigning one storage account for Speech & Language (shared) | Speech, Language | Resource level only | To enable customer-managed storage for Speech & Language at creation time |

### Foundry connections

Foundry connections act as shared data pointers across Foundry capabilities (agents, evaluations, datasets, content understanding). Each connection wraps the target storage endpoint plus authentication so users with project access can use the data without direct storage account permissions. Use connections as the default pattern; create a capability host only when you need to explicitly bind (override) a single feature to one connection among several.

### Capability hosts

[Capability hosts](/azure/ai-foundry/agents/concepts/capability-hosts) bind specific features to designated connections when multiple storage connections exist. They define which storage connection a particular feature uses. Use capability hosts most commonly for agents standard setup. If you don't create capability hosts for agents, Foundry uses Microsoft-managed storage for that feature.

See [Capability hosts](../agents/concepts/capability-hosts.md) for conceptual details.

### userOwnedStorage (resource storage binding)

The `userOwnedStorage` field enables customer-managed storage for Speech and Language capabilities. Set this field during resource creation at the resource level, so all projects within the resource share the same storage account.

Speech and Language capabilities share the storage account but use different containers within it. The setting applies at the resource level and cannot be changed after creation without recreating the resource.

If strict data isolation is required between Speech and Language scenarios, create separate Foundry resources with different storage accounts.

> [!IMPORTANT]
> If you delete or move (change resource ID of) the storage account bound by `userOwnedStorage`, Speech and Language stop functioning. Consider attempting account recovery first: [Recover a storage account](/azure/storage/common/storage-account-recover). Otherwise you must recreate the Foundry resource.
