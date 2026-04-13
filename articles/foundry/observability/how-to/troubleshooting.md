---
title: Troubleshoot evaluation and observability issues - Microsoft Foundry
description: Learn how to troubleshoot common issues with evaluations and observability in Microsoft Foundry, including storage account access, RBAC, and network configuration.
author: naposani
ms.author: naposani
ms.service: azure-ai-foundry
ms.topic: troubleshooting
ms.date: 04/13/2026
ai-usage: ai-assisted
#CustomerIntent: As a developer, I want to troubleshoot common evaluation and observability issues in Microsoft Foundry so that I can resolve problems quickly.
---

# Troubleshoot evaluation and observability issues

This article provides information to help you solve common issues you might encounter when you use evaluation and observability features in Microsoft Foundry. Issues often relate to storage account configuration, role-based access control (RBAC), or network settings for the Foundry project.

## Storage account not linked to the Foundry project

Evaluation features require a storage account linked to your Foundry project through a connection. If the storage account isn't connected, evaluations fail because the service can't read or write evaluation data.

### Symptoms

- Evaluations fail with errors related to storage access or missing storage configuration.
- The evaluation service can't upload evaluation results or download datasets.

### Solution

Connect your storage account to the Foundry project by creating an Azure Blob Storage connection. For step-by-step instructions, see [Add a new connection to your project](../../how-to/connections-add.md).

You can authenticate the connection by using either an **account key** or **Microsoft Entra ID** (recommended). If you use Entra ID, see [Missing RBAC role assignment for Entra ID authentication](#missing-rbac-role-assignment-for-entra-id-authentication) to configure the required permissions.

For more details on bringing your own storage for evaluations, see [Rate limits, region support, and enterprise features for evaluation](../../concepts/evaluation-regions-limits-virtual-network.md#bring-your-own-storage).

## Missing RBAC role assignment for Entra ID authentication

If you connect your storage account by using Microsoft Entra ID authentication, the Foundry project's managed identity must have the **Storage Blob Data Contributor** role on the storage account. Without this role, the service can't read or write blob data and evaluations fail.

### Symptoms

- Evaluations fail with `403 Forbidden` or `AuthorizationPermissionMismatch` errors.
- You see errors indicating insufficient permissions to access the storage account.
- Storage operations time out or are denied.

### Verify the managed identity role assignment

Use the following Azure CLI commands to check whether the correct RBAC role is assigned to the Foundry project's managed identity on the storage account.

First, retrieve the managed identity principal ID for your Foundry project:

```azurecli
az resource show \
  --resource-group <your-resource-group> \
  --name <your-foundry-account-name> \
  --resource-type "Microsoft.CognitiveServices/accounts" \
  --query "identity.principalId" \
  --output tsv
```

Then, list the role assignments on the storage account and filter for the managed identity:

```azurecli
az role assignment list \
  --scope "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.Storage/storageAccounts/<storage-account-name>" \
  --assignee <principal-id> \
  --output table
```

Verify that the output includes a role assignment with `RoleDefinitionName` set to **Storage Blob Data Contributor** (or **Storage Blob Data Owner**).

### Solution

If the role assignment is missing, assign the **Storage Blob Data Contributor** role to the Foundry project's managed identity:

```azurecli
az role assignment create \
  --assignee <principal-id> \
  --role "Storage Blob Data Contributor" \
  --scope "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.Storage/storageAccounts/<storage-account-name>"
```

> [!NOTE]
> Role assignments can take up to 10 minutes to propagate. Wait a few minutes after assigning the role before retrying the evaluation.

## Storage account network access restrictions

When you use Microsoft Entra ID authentication, the storage account must have public network access enabled. If network access is restricted, the Foundry evaluation service might not be able to reach the storage account.

### Symptoms

- Evaluations fail with network-related errors or timeouts.
- You see `403 Forbidden` errors even though RBAC roles are correctly assigned.
- Connections to the storage account are refused.

### Verify the storage account network configuration

Use the following Azure CLI command to check the network access settings of your storage account:

```azurecli
az storage account show \
  --resource-group <resource-group> \
  --name <storage-account-name> \
  --query "{publicNetworkAccess: publicNetworkAccess, defaultAction: networkRuleSet.defaultAction, virtualNetworkRules: networkRuleSet.virtualNetworkRules, ipRules: networkRuleSet.ipRules}" \
  --output json
```

Check the output for the following values:

| Property | Expected value | Description |
|---|---|---|
| `publicNetworkAccess` | `Enabled` | Public network access must be enabled. |
| `defaultAction` | `Allow` | The default network rule should allow access. |

If `publicNetworkAccess` is set to `Disabled` or `defaultAction` is set to `Deny`, the evaluation service can't reach the storage account.

### Solution

Enable public network access on the storage account:

```azurecli
az storage account update \
  --resource-group <resource-group> \
  --name <storage-account-name> \
  --public-network-access Enabled
```

If you need to keep the firewall enabled but allow access, set the default action to **Allow**:

```azurecli
az storage account update \
  --resource-group <resource-group> \
  --name <storage-account-name> \
  --default-action Allow
```

> [!IMPORTANT]
> Enabling public network access or setting the default action to **Allow** makes the storage account accessible from all networks. Evaluate this change against your organization's security requirements.

## Troubleshooting checklist

Use this checklist to quickly verify your evaluation setup:

1. **Storage connection exists**: Confirm that an Azure Blob Storage connection is configured in your Foundry project. Navigate to **Build** > **Tools** in the Foundry portal to check.

1. **Authentication type**: Identify whether the connection uses an account key or Microsoft Entra ID. If Entra ID, complete the remaining checks.

1. **RBAC role assigned**: Verify that the Foundry project's managed identity has the **Storage Blob Data Contributor** role on the storage account.

   ```azurecli
   az role assignment list \
     --scope "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.Storage/storageAccounts/<storage-account-name>" \
     --assignee <principal-id> \
     --query "[].{Role:roleDefinitionName, Principal:principalId}" \
     --output table
   ```

1. **Network access**: Verify that the storage account has public network access enabled.

   ```azurecli
   az storage account show \
     --resource-group <resource-group> \
     --name <storage-account-name> \
     --query "publicNetworkAccess" \
     --output tsv
   ```

1. **Propagation delay**: If you recently made RBAC or network changes, wait at least 10 minutes before retrying.

## Related content

- [Add a new connection to your project](../../how-to/connections-add.md)
- [Connect to your own storage](../../how-to/bring-your-own-azure-storage-foundry.md)
- [Rate limits, region support, and enterprise features for evaluation](../../concepts/evaluation-regions-limits-virtual-network.md)
- [Evaluate your AI agents](evaluate-agent.md)
