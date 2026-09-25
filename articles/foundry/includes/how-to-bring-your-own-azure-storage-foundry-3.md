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

## End-to-end customer-managed storage checklist

1. Create resource with `userOwnedStorage` (if Speech or Language features are needed).
2. Create storage connection.
3. Set `blobStore` in the account capability settings so agents use your storage account.
4. Override `blobStore` on a project only if that project needs a different storage account.
5. Bind Content Understanding to the storage connection.

After these steps, all features (Agents, Evaluations, Datasets, Content Understanding, Speech, Language) route to customer-managed storage.

## Troubleshooting

### Agents still use Microsoft-managed storage

If agents continue to write data to Microsoft-managed storage instead of your storage account:

- Verify that a GET on the project returns the `blobStore` value you expect, either set on the project or inherited from the account.
- Confirm the resource ID in `blobStore` points to the expected storage account.
- Confirm the deployment that set the capability settings succeeded. A caller missing **Storage Blob Data Contributor** fails provisioning before the setting takes effect.
- Review role assignments on the storage account. Standard agent setup requires **Storage Account Contributor** on the account, **Storage Blob Data Contributor** on the `<workspaceId>-azureml-blobstore` container, and **Storage Blob Data Owner** on the `<workspaceId>-agents-blobstore` container.

### Permission errors when accessing storage

If you get authorization or permission errors:

- Confirm that the project managed identity (not the resource identity) has the required storage roles on the storage account and containers.
- Confirm the storage account permits the authentication method your connection uses. 
- Check that network rules on the storage account allow traffic from Microsoft Foundry. If the storage account uses a firewall, add the appropriate exceptions.

### Speech or Language stops working after storage changes

If Speech or Language capabilities stop functioning after changes to your storage account:

- Don't delete or move (change the resource ID of) the storage account bound by `userOwnedStorage`.
- If the storage account was deleted, attempt recovery first: [Recover a storage account](/azure/storage/common/storage-account-recover).
- If recovery isn't possible, recreate the Foundry resource with a new storage account. You can't change the `userOwnedStorage` field after resource creation.

## Related content

- [Configure agent capability settings](../how-to/configure-capability-settings.md)
- [Understanding Agents standard setup](../agents/concepts/standard-agent-setup.md)
- [Add connections to your project](../how-to/connections-add.md)
- [Recover a storage account](/azure/storage/common/storage-account-recover).
- [Azure Storage documentation](/azure/storage/).
- [Infrastructure setup samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples).
- [Connect storage for Speech/Language](../../ai-services/speech-service/bring-your-own-storage-speech-resource.md?tabs=portal).
