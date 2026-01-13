---
title: Recover or purge deleted Microsoft Foundry resources
titleSuffix: Foundry Tools
description: This article provides instructions on how to recover or purge an already-deleted Microsoft Foundry resource.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-services
ms.topic: how-to
ms.date: 10/02/2025
ms.author: pafarley
ms.custom: sfi-image-nochange
---

# Recover or purge deleted Microsoft Foundry resources

This article provides instructions on how to recover or purge a Foundry resource that is already deleted. 

Once you delete a resource, you can't create another one with the same name for 48 hours. To create a resource with the same name, you need to purge the deleted resource.

> [!NOTE]
> * The instructions in this article are applicable to both a multi-service resource and a single-service resource. A multi-service resource enables access to multiple Foundry Tools using a single key and endpoint. On the other hand, a single-service resource enables access to just that specific Foundry Tools for which the resource was created.
>
> * Charges for provisioned deployments on a deleted resource continue until the resource is purged. To prevent unnecessary charges, delete a resource's deployment before deleting the resource.

## Recover a deleted resource

The following prerequisites must be met before you can recover a deleted resource:

* The resource to be recovered must be deleted within the past 48 hours.
* The resource to be recovered must not be purged already. A purged resource can't be recovered.
* Before you attempt to recover a deleted resource, make sure that the resource group for that account exists. If the resource group was deleted, you must recreate it. Recovering a resource group isn't possible. For more information, see [Manage resource groups](/azure/azure-resource-manager/management/manage-resource-groups-portal).
* If the deleted resource used customer-managed keys with Azure Key Vault and the key vault is also deleted, then you must restore the key vault before you restore the Foundry resource. For more information, see [Azure Key Vault recovery management](/azure/key-vault/general/key-vault-recovery).
* If the deleted resource used a customer-managed storage and storage account is also deleted, you must restore the storage account before you restore the Foundry resource. For instructions, see [Recover a deleted storage account](/azure/storage/common/storage-account-recover).

To recover a deleted Foundry resource, use the following commands. Where applicable, replace:

* `{subscriptionID}` with your Azure subscription ID
* `{resourceGroup}` with your resource group
* `{resourceName}` with your resource name
* `{location}` with the location of your resource


# [Azure portal](#tab/azure-portal)

If you need to recover a deleted resource, navigate to the hub of the Foundry Tools API type and select "Manage deleted resources" from the menu. For example, if you would like to recover an "Anomaly detector" resource, search for "Anomaly detector" in the search bar and select the service. Then select **Manage deleted resources**.

To locate the deleted resource you would like to recover, select the subscription in the dropdown list. Select one or more of the deleted resources and select **Recover**.

:::image type="content" source="media/managing-deleted-resource.png" alt-text="A screenshot showing deleted resources you can recover." lightbox="media/managing-deleted-resource.png":::

> [!NOTE] 
> It can take a couple of minutes for your deleted resource to recover and show up in the list of the resources. Select the **Refresh** button in the menu to update the list of resources.

# [Rest API](#tab/rest-api)

Use the following `PUT` command:

```rest-api
https://management.azure.com/subscriptions/{subscriptionID}/resourceGroups/{resourceGroup}/providers/Microsoft.CognitiveServices/accounts/{resourceName}?Api-Version=2021-04-30
```

In the request body, use the following JSON format:

```json
{ 
  "location": "{location}", 
   "properties": { 
        "restore": true 
    } 
} 
```

# [PowerShell](#tab/powershell)

Use the following command to restore the resource: 

```powershell
New-AzResource -Location {location} -Properties @{restore=$true} -ResourceId /subscriptions/{subscriptionID}/resourceGroups/{resourceGroup}/providers/Microsoft.CognitiveServices/accounts/{resourceName}   -ApiVersion 2021-04-30 
```

If you need to find the name of your deleted resources, you can get a list of deleted resource names with the following command: 

```powershell
Get-AzResource -ResourceId /subscriptions/{subscriptionId}/providers/Microsoft.CognitiveServices/deletedAccounts -ApiVersion 2021-04-30 
```

# [Azure CLI](#tab/azure-cli)

```azurecli-interactive
az resource create --subscription {subscriptionID} -g {resourceGroup} -n {resourceName} --location {location} --namespace Microsoft.CognitiveServices --resource-type accounts --properties "{\"restore\": true}"
```

---

## Purge a deleted resource 

Your subscription must have `Microsoft.CognitiveServices/locations/resourceGroups/deletedAccounts/delete` permissions to purge resources, such as [Cognitive Services Contributor](/azure/role-based-access-control/built-in-roles#cognitive-services-contributor) or [Contributor](/azure/role-based-access-control/built-in-roles#contributor). 

When using `Contributor` to purge a resource the role must be assigned at the subscription level. If the role assignment is only present at the resource or resource group level, you can't access the purge functionality.

To purge a deleted Foundry resource, use the following commands. Where applicable, replace:

* `{subscriptionID}` with your Azure subscription ID
* `{resourceGroup}` with your resource group
* `{resourceName}` with your resource name
* `{location}` with the location of your resource

> [!NOTE]
> Once a resource is purged, it's permanently deleted and can't be restored. You lose all data and keys associated with the resource.


# [Azure portal](#tab/azure-portal)

If you need to purge a deleted resource, the steps are similar to recovering a deleted resource.

1. Navigate to the hub of the Foundry Tools API type of your deleted resource. For example, if you would like to purge an "Anomaly detector" resource, search for "Anomaly detector" in the search bar and select the service. Then select **Manage deleted resources** from the menu.

1. To locate the deleted resource you would like to purge, select the subscription in the dropdown list. 

1. Select one or more deleted resources and select **Purge**. Purging permanently deletes a Foundry resource. 

    :::image type="content" source="media/managing-deleted-resource.png" alt-text="A screenshot showing a list of resources that can be purged." lightbox="media/managing-deleted-resource.png":::


# [Rest API](#tab/rest-api)

Use the following `DELETE` command:

```rest-api
https://management.azure.com/subscriptions/{subscriptionID}/providers/Microsoft.CognitiveServices/locations/{location}/resourceGroups/{resourceGroup}/deletedAccounts/{resourceName}?Api-Version=2021-04-30`
```

# [PowerShell](#tab/powershell)

```powershell
Remove-AzResource -ResourceId /subscriptions/{subscriptionID}/providers/Microsoft.CognitiveServices/locations/{location}/resourceGroups/{resourceGroup}/deletedAccounts/{resourceName}  -ApiVersion 2021-04-30
```

# [Azure CLI](#tab/azure-cli)

```azurecli-interactive
az resource delete --ids /subscriptions/{subscriptionId}/providers/Microsoft.CognitiveServices/locations/{location}/resourceGroups/{resourceGroup}/deletedAccounts/{resourceName}
```

---


## Related content
* [Create a Foundry resource](multi-service-resource.md)
* [Create a Foundry resource using an ARM template](create-account-resource-manager-template.md)