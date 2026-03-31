---
title: Configure CMK across different tenants in Azure AI Search
description: Configure cross-tenant customer-managed key encryption in Azure AI Search using either a managed identity with federated identity credentials or client secrets.
author: mattwojo
ms.author: mattwoj
ms.reviewer: mcarter
ms.date: 03/27/2026
ms.topic: how-to
ms.service: azure-ai-search
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# Configure customer-managed keys across different tenants

Azure AI Search automatically encrypts data at rest with Microsoft-managed keys. For additional control over encryption keys, you can manage your own keys. Customer-managed keys must be stored in an Azure Key Vault or in an Azure Key Vault Managed Hardware Security Model (HSM).

This article shows how to configure encryption with customer-managed keys when your Azure AI Search service and Azure Key Vault are in different Microsoft Entra tenants. In the cross-tenant scenario, the Azure AI Search service resides in a tenant managed by an ISV, while the key used for encryption of that search service resides in a key vault in a tenant that is managed by the customer.

To learn how to configure customer-managed keys for a new Azure AI Search service, see [Configure customer-managed keys for data encryption in Azure AI Search](search-security-manage-encryption-keys.md).

> [!NOTE]
> Azure Key Vault and Azure Key Vault Managed HSM support the same APIs and management interfaces for configuration of customer-managed keys. Any action that is supported for Azure Key Vault is also supported for Azure Key Vault Managed HSM.

There are two possible approaches to enable cross-tenant CMK encryption for Azure AI Search:

1. **Configure cross-tenant customer-managed keys with a federated identity credential (FIC)** (preview): 
a Microsoft Entra multitenant application with a federated identity credential (FIC)
This approach is recommended, but currently requires use of a preview API (version `2026-03-01-preview` or later). While each approach utilizes a Microsoft Entra multitenant application with Azure AI Search, this approach enhances security and simplifies management by avoiding reliance on client secrets.

1. **Configure cross-tenant customer-managed keys with client secrets**: This approach is less secure and more complex to manage, as it requires handling client secrets. Don't use this approach unless the first approach isn't feasible for your scenario.

[!INCLUDE [entra-msi-cross-tenant-cmk-overview](~/reusable-content/ce-skilling/azure/includes/entra-msi-cross-tenant-cmk-overview.md)]

[!INCLUDE [entra-msi-cross-tenant-cmk-create-identities-authorize-key-vault](~/reusable-content/ce-skilling/azure/includes/entra-msi-cross-tenant-cmk-create-identities-authorize-key-vault.md)]

## Configure cross-tenant customer-managed keys with a federated identity credential (FIC)

Up to this point, you've configured the multi-tenant application on the ISV's tenant (tenant 1), installed the application on the customer's tenant (tenant 2), and configured the key vault and key on the customer's tenant (tenant 2). Next you can configure customer-managed keys on an existing Azure AI Search service with the key from the customer's tenant. To configure customer-managed keys (CMK), the search service must be on a [billable tier](search-sku-tier.md#tier-descriptions) (Basic or higher).

The examples in this article show how to configure customer-managed keys on an existing Azure AI Search service by using a user-assigned managed identity to authorize access to the key vault. You can also use a system-assigned managed identity to configure customer-managed keys on the service. In either case, the managed identity must have appropriate permissions to access the key vault. For more information, see [Authenticate to Azure Key Vault](/azure/key-vault/general/authentication).

**TO-DO: CONFIRM THE FOLLOWING**

When you configure encryption with customer-managed keys for an Azure AI Search service, you can choose to automatically update the key version used for Azure AI Search encryption whenever a new version is available in the associated key vault. To do so, omit the key version from the key URI. Alternately, you can explicitly specify a key version to be used for encryption until the key version is manually updated. Including the key version on the key URI configures customer-managed keys for manual updating of the key version.

> [!IMPORTANT]
> To rotate a key, create a new version of the key in Azure Key Vault. Azure AI Search does not handle key rotation, so you will need to manage rotation of the key in the key vault. You can [configure key auto-rotation in Azure Key Vault](/azure/key-vault/keys/how-to-configure-key-rotation) or rotate your key manually.
>
> Azure AI Search checks the key vault for a new key version only once daily. When you rotate a key in Azure Key Vault, be sure to wait 24 hours before disabling the older version.


### [Azure portal](#tab/azure-portal)

To configure cross-tenant customer-managed keys for an existing Azure AI Search service in the Azure portal, follow these steps:

1. Navigate to your Azure AI Search service.
1. Under Search management, select Indexes, Indexers, or Data Sources.
1. Add the new object (Index, Indexer, or Data Source). When you create a new object in the Azure portal, you can specify a predefined customer-managed key in a key vault. Requirements for using the Azure portal are that the key vault and key must exist, and you completed the previous steps for authorized access to the key. The Azure portal lets you enable CMK encryption for:
    - Indexes
    - Data sources
    - Indexers
    - In the Azure portal, skillsets are defined in JSON view. Use the JSON shown in the REST API examples to provide a customer-managed key on a skillset.
1. In the object definition, select Encryption: Microsoft-managed keys.
1. Select Encryption type: Customer-managed keys and choose your subscription, key store type, vault, key, and version.
1. **TO-DO: Under Authentication, should they choose Entra ID credentials or Identity?** Choosing Entra ID credentials will ask for App ID and App secret -- guessing this is the old way. Choosing Identity will ask for the **Managed identity type** field, and give the options of system-assigned or user-assigned. Select **User-assigned**, then specify the managed identity with the federated identity credential that you created previously.
1. **TO-DO: I don't see the option to do this. Does is show up after the previous step is completed? Or not there yet?** Expand the **Advanced** section, and select the multi-tenant registered application that you previously created in the ISV's tenant.

    :::image type="content" source="media/customer-managed-keys-configure-cross-tenant-existing-account/portal-configure-cross-tenant-cmk.png" alt-text="Screenshot showing how to configure cross-tenant customer-managed keys for an existing storage account in Azure portal.":::

1. Save your changes.

After you've specified the key from the key vault in the customer's tenant, the Azure portal indicates that customer-managed keys are configured with that key. It also indicates that automatic updating of the key version is enabled, and displays the key version currently in use for encryption. The portal also displays the type of managed identity used to authorize access to the key vault, the principal ID for the managed identity, and the application ID of the multi-tenant application.

**TO-DO: Screenshots are for storage accounts right now. Need to update to show Azure AI Search or remove.**
:::image type="content" source="media/customer-managed-keys-configure-cross-tenant-existing-account/portal-cross-tenant-cmk-settings.png" alt-text="Screenshot showing cross-tenant customer-managed key configuration.":::

### [PowerShell](#tab/azure-powershell)

To configure cross-tenant customer-managed keys for a new Azure AI Search service with PowerShell, first install the [Az.Search PowerShell module](/powershell/module/az.search), **TO-DO: Confirm this** version 15.4.0 or later. This module is installed with the [Az PowerShell module](/powershell/azure/install-azps-windows), version 15.4.0 or later.

Next, call [Set-AzSearchService](/powershell/module/az.search/set-azsearchservice), providing the resource ID for the user-assigned managed identity that you configured previously in the ISV's subscription, and the application (client) ID for the multi-tenant application that you configured previously in the ISV's subscription. Provide the key vault URI and key name from the customer's key vault.

Remember to replace the placeholder values in brackets with your own values and to use the variables defined in the previous examples.

```azurepowershell
$accountName = "<search-service>"
$kvUri = "<key-vault-uri>"
$keyName = "<key-name>"
$multiTenantAppId = "<multi-tenant-app-id>"

Set-AzStorageAccount -ResourceGroupName $isvRgName `
    -Name $accountName `
    -KeyvaultEncryption `
    -UserAssignedIdentityId $userIdentity.Id `
    -IdentityType SystemAssignedUserAssigned `
    -KeyName $keyName `
    -KeyVaultUri $kvUri `
    -KeyVaultUserAssignedIdentityId $userIdentity.Id `
    -KeyVaultFederatedClientId $multiTenantAppId 
```

### [Azure CLI](#tab/azure-cli)

To configure cross-tenant customer-managed keys for an existing Azure AI Search service with Azure CLI, first install the Azure CLI, version 2.42.0 or later. For more information about installing Azure CLI, see [How to install the Azure CLI](/cli/azure/install-azure-cli).

Next, call [az resource update](/cli/azure/resource), providing the resource ID for the user-assigned managed identity that you configured previously in the ISV's subscription, and the application (client) ID for the multi-tenant application that you configured previously in the ISV's subscription. Provide the key vault URI and key name from the customer's key vault.

Remember to replace the placeholder values in brackets with your own values and to use the variables defined in the previous examples.

```azurecli
serviceName="<Azure AI Search service name>"
kvUri="<key-vault-uri>"
keyName="<key-name>"
multiTenantAppId="<multi-tenant-app-id>" # appId value from multi-tenant app

# Get the resource ID for the user-assigned managed identity.
identityResourceId=$(az identity show --name $userIdentityName \
    --resource-group $isvRgName \
    --query id \
    --output tsv)

az resource update --name $serviceName \
    --resource-group $isvRgName \
    --identity-type SystemAssigned,UserAssigned \
    --user-identity-id $identityResourceId \
    --encryption-key-vault $kvUri \
    --encryption-key-name $keyName \
    --encryption-key-source Microsoft.Keyvault \
    --key-vault-user-identity-id $identityResourceId \
    --key-vault-federated-client-id $multiTenantAppId
```
---

## Configure cross-tenant customer-managed keys with client secrets

If using a federated identity credential (FIC) isn't feasible for your scenario, you can instead configure cross-tenant customer-managed keys with client secrets. This approach is less secure and more complex to manage, but still allows you to configure cross-tenant customer-managed keys for Azure AI Search.

To use client secrets for cross-tenant customer-managed keys, you create a client secret for the multi-tenant application that you created in the ISV's tenant, and use that client secret to authenticate to the key vault in the customer's tenant when configuring customer-managed keys on the Azure AI Search service.


### [Azure portal](#tab/azure-portal)

To add a client secret to the multitenant application in the ISV's tenant (Tenant 1) that can be used by the customer's tenant (Tenant 2) for access to an Azure AI Search service using Azure Portal, follow these steps:

1. TO-DO


### [PowerShell](#tab/azure-powershell)

To add a client secret to the multitenant application in the ISV's tenant (Tenant 1) that can be used by the customer's tenant (Tenant 2) for access to an Azure AI Search service using Azure PowerShell, follow these steps:

1. TO-DO

### [Azure CLI](#tab/azure-cli)

To add a client secret to the multitenant application in the ISV's tenant (Tenant 1) that can be used by the customer's tenant (Tenant 2) for access to an Azure AI Search service using Azure PowerShell, follow these steps:

1. Get the tenant ID:

   `az account show --query tenantId --output tsv`

1. Make sure you're signed in to tenant A:

   `az login --tenant <tenant-A-id> `

1. Create the application registration:

   `az ad app create --display-name cross-tenant-auth --sign-in-audience AzureADMultipleOrgs `

1. Save the app ID output from this step.

1. Add the client secret to the multitenant application in tenant 1, by running this command:

   `az ad app credential reset --id <multitenant-app-id>`

1. Save the password output from this step. The password output is a required input for [setting up CMK](search-security-manage-encryption-keys.md) in Azure AI Search.

1. To specify when the client secret expires, you can specify an end-date parameter to this command.

   `az ad app credential reset --id <multitenant-app-id> --end-date <end-date>`

   The end-date parameter accepts a date in ISO 8601 format. For example: `az ad app credential reset --id <multitenant-app-id> --end-date 2026-12-31`.

1. Create a test index in the search service (tenant A) to validate the setup. Use the multitenant app ID and the credentials you added in the "access credentials" object to authenticate to the key vault in the other tenant.

You can use this sample index schema for testing. You can use the Azure portal to add an index and provide this JSON, or use a REST client to send a Create Index request.

```json
{
  "name": "cross-tenant-cmk-test", 
  "fields": [ 
        { 
            "name": "id", 
            "type": "Edm.String", 
            "key": true 
        } 
      ], 
  "encryptionKey": { 
    "keyVaultUri": "https://myCompanyKeyVault.vault.azure.net/", 
    "keyVaultKeyName": "search-encryption-key", 
    "keyVaultKeyVersion": "abc123def456ghi789", 
    "accessCredentials": { 
      "applicationId": "12345678-1234-1234-1234-123456789012", 
      "applicationSecret": "secretValueFromStep2" 
    } 
  } 
}
```

Verify the index was created successfully:

```http
GET https://<search-service>.search.windows.net/indexes/cross-tenant-cmk-test?api-version=2025-09-01
```

## Rotate or revoke encryption keys

For guidance on rotating keys, updating key versions, or revoking access, see [Rotate or update encryption keys](search-security-manage-encryption-keys.md#rotate-or-update-encryption-keys). The same key lifecycle guidance applies to cross-tenant configurations. Azure AI Search caches the key for up to 60 minutes, so allow time for changes to take effect.

## See also

- [Configure customer-managed keys for data encryption in Azure AI Search](search-security-manage-encryption-keys.md)
- [Find encrypted objects and information](search-security-get-encryption-keys.md)