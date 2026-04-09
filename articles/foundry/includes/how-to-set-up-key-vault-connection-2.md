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

## Use a Bicep template

Deploy a Key Vault connection by using Azure Bicep. The following template creates a connection between your Foundry resource and an existing Azure Key Vault, and assigns the Key Vault Secrets Officer role to the Foundry resource's managed identity.

:::code language="bicep" source="~/foundry-samples-main/infrastructure/infrastructure-setup-bicep/01-connections/connection-key-vault.bicep"

### Parameters

| Parameter        | Description                                 |
|------------------|---------------------------------------------|
| `aiFoundryName`  | The name of your Foundry resource.          |
| `keyVaultName`   | The name of your existing Azure Key Vault.  |

### Deploy the template

Run the following command to deploy the template:

```azurecli
az deployment group create \
  --name AzDeploy \
  --resource-group <resource-group-name> \
  --template-file connection-key-vault.bicep \
  --parameters aiFoundryName=<foundry-resource-name> keyVaultName=<keyvault-name>
```

### Verify the deployment

After deployment completes:

1. Navigate to your Foundry resource in the Azure portal.
1. Select **Management center** in the lower left pane.
1. Select **Connected resources** and confirm the Azure Key Vault connection appears in the list.
1. Select the connection to view its properties and verify the Key Vault resource ID.

To verify that the RBAC role assignment is in effect, run the following command:

```azurecli
az role assignment list \
  --scope /subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.KeyVault/vaults/<keyvault-name> \
  --query "[?roleDefinitionName=='Key Vault Secrets Officer']" \
  --output table
```

### Reference

- [Microsoft.CognitiveServices/accounts/connections](/azure/templates/microsoft.cognitiveservices/accounts/connections)
- [Microsoft.Authorization/roleAssignments](/azure/templates/microsoft.authorization/roleassignments)
- [Key Vault Secrets Officer role](/azure/role-based-access-control/built-in-roles/security#key-vault-secrets-officer)

<!-- ::: zone-end -->

## Key Vault connection management

### Creation

Make sure no other connections exist at the Foundry resource or project level.
The service blocks Key Vault connection creation if other connections exist.
If the UI doesn't show a Key Vault connection category when you choose a connection,
this problem might be the reason. Delete other connections, and then try again.

When you create a Key Vault connection, the service doesn't use the managed Key Vault in Azure.

### Deletion

Before you delete an Azure Key Vault connection from Foundry, remove all other connections.
After you remove all other connections at the Foundry resource and project levels,
delete the Key Vault connection. Foundry doesn't support secret migration.

### Update or change

To switch from Azure Key Vault 1 to Azure Key Vault 2, delete the Azure Key Vault 1 connection, and then create the Azure Key Vault 2 connection. Follow the deletion and creation steps, and manually recreate any connection secrets.

### Key Vault secret lifecycle

When you delete connections from your managed Key Vault, the corresponding secrets are deleted.
Deleting a Key Vault connection also deletes its secrets.

### Granting Foundry access to your key vault

Depending on how your key vault is provisioned, you might need to apply additional permissions.
Check whether your Azure Key Vault uses role-based access control (RBAC) or access policies, and then continue.

#### Role-based access control (RBAC)

After you create the Key Vault connection, assign an appropriate RBAC role in the Azure portal. Key Vault Contributor and Key Vault Administrator are two roles that work. For minimal permissions, use the [Key Vault Secrets
Officer](/azure/role-based-access-control/built-in-roles/security#key-vault-secrets-officer).

#### Access policies

Similar to RBAC roles, assign the appropriate key vault access policy (if applicable) to the Foundry resource's managed identity.

## Infrastructure as code templates

As a best practice, when setting up ARM, Bicep, or Terraform templates to create resources, make sure the Azure Key Vault connection is the first connection you create, and make all other connections depend on the Key Vault connection succeeding. This order helps reduce Key Vault connection failures. If you don't follow this best practice, your templates can encounter race conditions across your connections. As a result, deployments can work sometimes and fail at other times because Foundry doesn't support secret migration.

After you create the Foundry resource and the Key Vault connection, assign the appropriate RBAC roles to the Foundry resource. Make all other connections depend on this role assignment succeeding. The same applies if your Key Vault uses access policies instead of RBAC.

### Follow this order in your infrastructure as code templates

1. Create the Foundry resource.
1. Create a Foundry project.
1. Create the Azure Key Vault connection.
1. Assign the appropriate RBAC role on the Key Vault for the Foundry resource.
1. (Optional) Validate that the RBAC role takes effect.
1. Create any other connections at the resource or project level, and set the `dependsOn` field for steps 3 and 4.

#### Deletion

For cleanup, if you automate resource deletion by using templates, follow the creation steps in reverse order:

1. Delete all connections at the Foundry resource or project level.
1. Delete the Azure Key Vault connection.
1. Delete all Foundry projects.
1. Delete the Foundry resource.

## Troubleshooting

### RBAC role assignment delays

After you assign the Key Vault Secrets Officer role, it can take up to 30 minutes for permissions to propagate. If you get permission errors immediately after role assignment, wait and retry.

### Connection not appearing

If the Key Vault connection doesn't appear in **Connected resources**:

1. Verify the deployment completed successfully.
1. Refresh the portal page.
1. Check that no other connections exist at the resource or project level. The service blocks Key Vault connection creation when other connections exist.

### Deployment errors

If deployment fails:

- Confirm you have Contributor or Owner role on the resource group.
- Verify the Key Vault name is correct and the vault exists in your subscription.
- Check that the Foundry resource name matches exactly.

## Next steps

- Create other connections (storage, endpoints, AI services) that use this Key Vault for secret storage
- [Add connections to your project](../how-to/connections-add.md)
- [Azure Key Vault best practices](/azure/key-vault/general/best-practices)
- [Azure Key Vault documentation](/azure/key-vault/)
- [Foundry documentation](/azure/ai-foundry/)
