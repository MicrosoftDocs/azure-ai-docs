---
title: Cross-tenant CMKs
titleSuffix: Azure AI Search
description: Set up CMK encryption in Azure AI Search that uses a key from an Azure Key Vault in another tenant.
manager: vinodva
author: mattgotteiner
ms.author: magottei
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 10/13/2025
ms.update-cycle: 180-days
---

# Configure customer-managed keys across different tenants

When Azure Key Vault and Azure AI Search are in different Azure tenants, use a Microsoft Entra multitenant app to enable [customer-managed key (CMK) encryption](search-security-manage-encryption-keys.md) using a key from another tenant.

## Prerequisites 

+ A tenant containing the search service that has content you want to encrypt. Azure AI Search must be [configured for role-based access](search-security-enable-roles.md). Support for CMK requires Basic pricing tier or higher.

+ A separate tenant having the Azure Key Vault and the encryption keys you want to use. Azure Key Vault must be [configured for role-based access](/azure/key-vault/general/rbac-guide).

+ Azure CLI for sending requests.

## Create a multitenant Microsoft Entra application in tenant A

Use the Azure CLI to send requests. We refer to the tenant containing Azure AI Search as *tenant A*.

1. Get the tenant ID:

   `az account show --query tenantId --output tsv`

1. Make sure you're signed in to tenant A:

   `az login --tenant <tenant-A-id> `

1. Create the application registration:

   `az ad app create --display-name cross-tenant-auth --sign-in-audience AzureADMultipleOrgs `

1. Save the app ID output from this step.

## Add a client secret to the multitenant application

1. To add the client secret to the multitenant application in tenant A, run the following command:

   `az ad app credential reset --id <multitenant-app-id>`

1. Save the password output from this step. The password output is a required input for [setting up CMK](search-security-manage-encryption-keys.md) in Azure AI Search.

1. To specify when the client secret expires, you can specify an end-date parameter to this command.

   `az ad app credential reset --id <multitenant-app-id> --end-date <end-date>`

   The end-date parameter accepts a date in ISO 8601 format. For example: `az ad app credential reset --id <multitenant-app-id> --end-date 2026-12-31`.

## Create a service principal in tenant B for the multitenant application

We refer to the tenant containing Azure Key Vault as *tenant B*. In tenant B, create a service principal for the multitenant application in tenant A.

1. Sign in to tenant B:

   `az login --tenant <tenant-B-id>`

1. Create the service principal using the multitenant app ID output from the first step:

   `az ad sp create --id <multitenant-app-id>` 

   This service principal is an instance of the multitenant application in tenant A. Roles assigned to this service principal in tenant B are also assigned to the multitenant application in tenant A.

1. Verify the link between tenant A and B by reviewing the "appOwnerOrganizationId" in the following command:

   `az ad sp show --id <multitenant-app-id>`

   This command displays the service principal details in JSON. Look for the "appOwnerOrganizationId" field in the output to confirm it matches tenant A's ID.

1. Save the object ID of the service principal (from the `"id"` field) from this step. The object ID is a required input for setting up CMK in Azure AI Search.

1. Get the resource ID for Azure Key Vault:

   `az keyvault show --name <key-vault-name> --query id --output tsv`

1. Assign the **Key Vault Crypto Service Encryption User** role on the key vault in tenant B to the new service principal.

   `az role assignment create --assignee <service-principal-object-id> --role "Key Vault Crypto Service Encryption User" --scope <key-vault-resource-id>`

   An example of this assignment might look like this:

   `az role assignment create --assignee 12345678-1234-1234-1234-123456789012 --role "Key Vault Crypto Service Encryption User" --scope /subscriptions/87654321-4321-4321-4321-210987654321/resourceGroups/myKeyVaultRG/providers/Microsoft.KeyVault/vaults/myCompanyKeyVault`

## Test encryption

Create a test index in the search service (tenant A) to validate the setup. Use the multitenant app ID and the credentials you added in the "access credentials" object to authenticate to the key vault in the other tenant. 

You can use this sample index schema for testing. You can use the Azure portal to add an index and provide this JSON, or use a [REST client](search-get-started-text.md) to send a Create Index request.

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

For more information about how to rotate or manage keys, see [Configure customer-managed keys for data encryption](search-security-manage-encryption-keys.md).