---
title: Cross-Tenant CMKs
description: Set up CMK encryption in Azure AI Search that uses a key from an Azure Key Vault in another tenant using federated identity credentials.
ms.reviewer: magottei
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 03/19/2026
ms.update-cycle: 180-days
ai-usage: ai-assisted
---

# Configure customer-managed keys across different tenants (legacy approach)

When Azure Key Vault and Azure AI Search are in different Azure tenants, you can set up [customer-managed key (CMK) encryption](search-security-manage-encryption-keys.md) using a key from another tenant. This configuration is common when a SaaS provider hosts Azure AI Search in its own tenant but needs each customer to encrypt data with a key stored in the customer's Key Vault.

The recommended approach uses a **federated identity credential (FIC)** on a multitenant Microsoft Entra application, paired with a managed identity on the search service. This secretless flow eliminates the need to share or rotate client secrets across tenants and aligns with the cross-tenant CMK patterns used by [Azure Storage](/azure/storage/common/customer-managed-keys-overview#cross-tenant-customer-managed-keys), [Azure Cosmos DB](/azure/cosmos-db/how-to-setup-cross-tenant-customer-managed-keys), and [Azure SQL](/azure/azure-sql/database/transparent-data-encryption-byok-cross-tenant).

> [!TIP]
> A legacy approach that uses a client secret instead of a federated identity credential is still supported but not recommended. See [Legacy approach: Configure cross-tenant CMK with a client secret](#legacy-approach-configure-cross-tenant-cmk-with-a-client-secret) later in this article.

## Scenario

This article uses a two-company example:

+ **Contoso** (Tenant A) is a SaaS provider that hosts an Azure AI Search service.
+ **Fabrikam** (Tenant B) is a customer that owns a Key Vault and the encryption key.

Contoso needs to encrypt search indexes with a key stored in Fabrikam's Key Vault, without exchanging secrets.

## Prerequisites

+ An Azure AI Search service (Contoso, Tenant A) on a [billable tier](search-sku-tier.md#tier-descriptions) (Basic or higher), [configured for role-based access](search-security-enable-roles.md).

+ An Azure Key Vault (Fabrikam, Tenant B) with **soft-delete** and **purge protection** enabled, [configured for role-based access](/azure/key-vault/general/rbac-guide), and containing an RSA key (2048, 3072, or 4096 bits).

+ A user-assigned managed identity (UAMI) or system-assigned managed identity (SAMI) on the search service.

+ Azure CLI for sending requests.

+ API version **2026-03-01-preview** or later (required for the `federatedIdentityClientId` property).

## Assign a managed identity to the search service

If the search service doesn't already have a user-assigned managed identity, create and assign one. A user-assigned managed identity (UAMI) is recommended because it can be reused across resources.

1. Sign in to Contoso's tenant (Tenant A):

   ```azurecli
   az login --tenant <tenant-A-id>
   ```

1. Create a user-assigned managed identity (skip this step if one already exists):

   ```azurecli
   az identity create --name search-cmk-identity --resource-group <resource-group>
   ```

1. Save the `principalId` and `id` (resource ID) values from the output.

1. Assign the UAMI to the search service:

   ```azurecli
   az search service update --name <search-service-name> \
     --resource-group <resource-group> \
     --identity-type UserAssigned \
     --user-assigned-identity <uami-resource-id>
   ```

## Create a multitenant application with a federated identity credential

In Contoso's tenant (Tenant A), register a multitenant Microsoft Entra application and add a federated identity credential that trusts the managed identity.

1. Create the multitenant application registration:

   ```azurecli
   az ad app create --display-name cross-tenant-cmk --sign-in-audience AzureADMultipleOrgs
   ```

1. Save the `appId` value from the output.

1. Create a service principal for the app in Tenant A:

   ```azurecli
   az ad sp create --id <app-id>
   ```

1. Add a federated identity credential that trusts the managed identity. Replace `<uami-principal-id>` with the `principalId` saved earlier and `<tenant-A-id>` with the Contoso tenant ID:

   ```azurecli
   az ad app federated-credential create --id <app-id> --parameters '{
     "name": "search-cmk-fic",
     "issuer": "https://login.microsoftonline.com/<tenant-A-id>/v2.0",
     "subject": "<uami-principal-id>",
     "audiences": ["api://AzureADTokenExchange"],
     "description": "FIC for cross-tenant CMK with Azure AI Search"
   }'
   ```

   At runtime, Azure AI Search uses the managed identity to obtain a token, then exchanges it through the federated identity credential to access Fabrikam's Key Vault—no client secrets required.

## Grant Key Vault permissions in the customer tenant

In Fabrikam's tenant (Tenant B), create a service principal for Contoso's multitenant app and assign Key Vault permissions.

1. Sign in to Fabrikam's tenant (Tenant B):

   ```azurecli
   az login --tenant <tenant-B-id>
   ```

1. Create a service principal for the multitenant app:

   ```azurecli
   az ad sp create --id <app-id>
   ```

   This service principal is an instance of Contoso's multitenant application in Fabrikam's tenant. Roles assigned to this service principal in Tenant B are also assigned to the multitenant application in Tenant A.

1. Verify the link between tenants by confirming that `appOwnerOrganizationId` matches Contoso's tenant ID:

   ```azurecli
   az ad sp show --id <app-id> --query appOwnerOrganizationId --output tsv
   ```

1. Get the resource ID for the Key Vault:

   ```azurecli
   az keyvault show --name <key-vault-name> --query id --output tsv
   ```

1. Assign the **Key Vault Crypto User** role on the Key Vault to the service principal:

   ```azurecli
   az role assignment create \
     --assignee-object-id $(az ad sp show --id <app-id> --query id --output tsv) \
     --assignee-principal-type ServicePrincipal \
     --role "Key Vault Crypto User" \
     --scope <key-vault-resource-id>
   ```

## Configure the index encryption key

Create an index in the search service (Contoso, Tenant A) that references Fabrikam's Key Vault key. Use the `identity` and `federatedIdentityClientId` properties instead of `accessCredentials`.

Send a Create Index request using API version `2026-03-01-preview` or later:

```json
PUT https://<search-service>.search.windows.net/indexes/cross-tenant-cmk-test?api-version=2026-03-01-preview
Content-Type: application/json
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
    "keyVaultUri": "https://<key-vault-name>.vault.azure.net",
    "keyVaultKeyName": "<key-name>",
    "keyVaultKeyVersion": "<key-version>",
    "identity": {
      "@odata.type": "#Microsoft.Azure.Search.DataUserAssignedIdentity",
      "userAssignedIdentity": "<uami-resource-id>"
    },
    "federatedIdentityClientId": "<app-id>"
  }
}
```

| Property | Description |
| --- | --- |
| `keyVaultUri` | The URI of Fabrikam's Key Vault. |
| `keyVaultKeyName` | The name of the encryption key in the Key Vault. |
| `keyVaultKeyVersion` | The version of the encryption key. |
| `identity` | The user-assigned managed identity on the search service that was configured with the federated identity credential. |
| `federatedIdentityClientId` | The `appId` (client ID) of the multitenant Microsoft Entra application. The search service uses this value with the managed identity to obtain a cross-tenant token for Key Vault access. |

Verify the index was created successfully:

```http
GET https://<search-service>.search.windows.net/indexes/cross-tenant-cmk-test?api-version=2026-03-01-preview
```

For more information about key rotation and management, see [Configure customer-managed keys for data encryption](search-security-manage-encryption-keys.md).

## Legacy approach: Configure cross-tenant CMK with a client secret

This section describes the original approach that uses a client secret on a multitenant application to authenticate to the customer's Key Vault. This method is still supported but is **not recommended** because it requires storing and rotating a shared secret.

> [!IMPORTANT]
> The federated identity credential approach described earlier in this article is the recommended path. It eliminates secrets and reduces operational overhead.

### Create a multitenant application in Tenant A

1. Sign in to Contoso's tenant (Tenant A):

   ```azurecli
   az login --tenant <tenant-A-id>
   ```

1. Create the application registration:

   ```azurecli
   az ad app create --display-name cross-tenant-auth --sign-in-audience AzureADMultipleOrgs
   ```

1. Save the `appId` from the output.

### Add a client secret

1. Add a client secret to the multitenant application:

   ```azurecli
   az ad app credential reset --id <app-id>
   ```

1. Save the `password` value. This value is required when configuring the CMK encryption key.

1. Optionally, set an expiration date:

   ```azurecli
   az ad app credential reset --id <app-id> --end-date 2027-12-31
   ```

### Create a service principal in Tenant B

1. Sign in to Fabrikam's tenant (Tenant B):

   ```azurecli
   az login --tenant <tenant-B-id>
   ```

1. Create the service principal:

   ```azurecli
   az ad sp create --id <app-id>
   ```

1. Verify `appOwnerOrganizationId` matches Contoso's tenant ID:

   ```azurecli
   az ad sp show --id <app-id> --query appOwnerOrganizationId --output tsv
   ```

1. Assign the **Key Vault Crypto Service Encryption User** role on the Key Vault:

   ```azurecli
   az role assignment create \
     --assignee-object-id $(az ad sp show --id <app-id> --query id --output tsv) \
     --assignee-principal-type ServicePrincipal \
     --role "Key Vault Crypto Service Encryption User" \
     --scope <key-vault-resource-id>
   ```

### Configure the index with access credentials

Create the index using `accessCredentials` with the app ID and client secret:

```json
PUT https://<search-service>.search.windows.net/indexes/cross-tenant-cmk-test?api-version=2025-09-01
Content-Type: application/json
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
    "keyVaultUri": "https://<key-vault-name>.vault.azure.net",
    "keyVaultKeyName": "<key-name>",
    "keyVaultKeyVersion": "<key-version>",
    "accessCredentials": {
      "applicationId": "<app-id>",
      "applicationSecret": "<client-secret>"
    }
  }
}
```

## Related content

+ [Configure customer-managed keys for data encryption](search-security-manage-encryption-keys.md)
+ [Azure Storage cross-tenant CMK](/azure/storage/common/customer-managed-keys-overview#cross-tenant-customer-managed-keys)
+ [Azure Cosmos DB cross-tenant CMK](/azure/cosmos-db/how-to-setup-cross-tenant-customer-managed-keys)
+ [Azure SQL cross-tenant CMK](/azure/azure-sql/database/transparent-data-encryption-byok-cross-tenant)