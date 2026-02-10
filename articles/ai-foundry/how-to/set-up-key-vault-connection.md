---
title: Set up an Azure Key Vault Connection
description: Learn how to securely connect your Azure Key Vault to Foundry. Follow step-by-step instructions to manage secrets and ensure seamless integration.
monikerRange: 'foundry-classic || foundry'
author: jonburchel
ms.author: jburchel
ms.reviewer: andyaviles
ms.date: 02/02/2026
ms.topic: how-to
ms.service: azure-ai-foundry
ms.custom: dev-focus
ai-usage: ai-assisted
# zone_pivot_groups: set-up-key-vault
---

# Set up an Azure Key Vault connection in Microsoft Foundry

[!INCLUDE [version-banner](../includes/version-banner.md)]

If you don't set up a Key Vault connection, Microsoft Foundry stores connection details in a Microsoft-managed Key Vault outside your subscription. To manage your own secrets, connect your Azure Key Vault to Foundry. Before you begin, review the [limitations](#limitations) for Key Vault connections.

Azure Key Vault is a cloud service for securely storing and accessing secrets. A secret is anything that you want to tightly control access to, such as API keys, passwords, certificates, or cryptographic keys. For more information, see [About Azure Key Vault](/azure/key-vault/general/overview).

## Prerequisites

- An Azure subscription.
- A Foundry resource with no existing connections at the resource or project level.
- An Azure Key Vault in your subscription, or permissions to create one.
- One of the following Azure RBAC roles on your Key Vault:
  - [Key Vault Secrets Officer](/azure/role-based-access-control/built-in-roles/security#key-vault-secrets-officer) (minimal permissions)
  - [Key Vault Contributor](/azure/role-based-access-control/built-in-roles/security#key-vault-contributor)
  - [Key Vault Administrator](/azure/role-based-access-control/built-in-roles/security#key-vault-administrator)

## Limitations

Create Azure Key Vault connections only when you need them.

If you bring your own Azure Key Vault, review these limitations:

- Limit Azure Key Vault connections to one per Foundry resource. Delete an Azure Key Vault connection only if no other connections exist at the Foundry resource or project level.

- Foundry doesn't support secret migration. Remove and recreate connections yourself.
- Deleting the underlying Azure Key Vault breaks the Foundry resource. Azure Key Vault stores secrets for connections that don't use Microsoft Entra ID. Any Foundry feature that depends on those connections stops working.
- Deleting connection secrets that your Foundry resource stores in your bring your own (BYO) Azure Key Vault can break connections to other services.

::: moniker range="foundry-classic"

<!-- ::: zone pivot="ai-foundry-portal" -->

## Use the Foundry (classic) portal

Create a connection to Azure Key Vault in the Foundry (classic) portal.

1. [!INCLUDE [classic-sign-in](../includes/classic-sign-in.md)]
1. Select or create your project. 
1. Select **Management center** in the lower left pane. You might need to scroll to find it.

1. Check that there are no connections in the **Resource** or **Project** sections. If connections exist, **Azure Key Vault** isn't available.

1. In the **Resource** section, select **Connected resources**.

1. In the **Connected resources** section, select **+ New connection**.

   :::image type="content" source="../media/setup-key-vault-connection/select-azure-key-vault.jpeg" alt-text="Screenshot of the Connected resources section with the + New connection button selected, showing Azure Key Vault as an available option.":::

1. Select **Azure Key Vault**.

   :::image type="content" source="../media/setup-key-vault-connection/azure-key-vault-connection.jpeg" alt-text="Screenshot of the Azure Key Vault selection dialog with Azure Key Vault selected.":::

1. Select your **Azure Key Vault**, and then select **Connect**.
1. It might take a few minutes after these steps are completed before you can use the connection.

### Verify the connection

After you create the connection, verify that the Key Vault appears in the **Connected resources** list. Select the connection to view its properties and confirm the Key Vault resource ID.

<!-- ::: zone-end -->
<!-- ::: zone pivot="bicep" -->
::: moniker-end

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

## Related content

- [Azure Key Vault documentation](/azure/key-vault/)
- [Foundry documentation](/azure/ai-foundry/)
