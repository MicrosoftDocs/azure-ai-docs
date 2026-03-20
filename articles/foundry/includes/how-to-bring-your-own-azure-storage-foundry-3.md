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

## End-to-end customer-managed storage checklist

1. Create resource with `userOwnedStorage` (if Speech/Language needed).
2. Create storage connection (connections).
3. Create resource-level capability host (Agents override when needed).
4. Create project-level capability host (Agents override at project).
5. Bind Content Understanding to the storage connection.

After these steps all features (Agents, Evaluations, Datasets, Content Understanding, Speech, Language) route to customer-managed storage.

## Troubleshooting

### Agents still use Microsoft-managed storage

If agents continue to write data to Microsoft-managed storage instead of your storage account:

- Verify that both resource-level and project-level capability hosts exist. Both levels are required for the binding chain to work.
- Check that each capability host references the correct connection ID.
- Confirm the storage connection points to the expected storage account.
- Review role assignments on the storage account to ensure the project managed identity has `Storage Blob Data Contributor`.

### Permission errors when accessing storage

If you get authorization or permission errors:

- Confirm that the project managed identity (not the resource identity) has the `Storage Blob Data Contributor` role on the storage account.
- Verify the storage account has `allowSharedKeyAccess` set to `true`.
- Check that network rules on the storage account allow traffic from Microsoft Foundry. If the storage account uses a firewall, add the appropriate exceptions.

### Speech or Language stops working after storage changes

If Speech or Language capabilities stop functioning after changes to your storage account:

- Don't delete or move (change the resource ID of) the storage account bound by `userOwnedStorage`.
- If the storage account was deleted, attempt recovery first: [Recover a storage account](/azure/storage/common/storage-account-recover).
- If recovery isn't possible, recreate the Foundry resource with a new storage account. The `userOwnedStorage` field can't be changed after resource creation.

## Related content

- [Capability hosts for Agents](../agents/concepts/capability-hosts.md)
- [Understanding Agents standard setup](../agents/concepts/standard-agent-setup.md)
- [Add connections to your project](../how-to/connections-add.md)
- [Recover a storage account](/azure/storage/common/storage-account-recover)
- [Azure Storage documentation](/azure/storage/)
- [Infrastructure setup samples](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples)
- [Connect storage for Speech/Language](../../ai-services/speech-service/bring-your-own-storage-speech-resource.md?tabs=portal)
