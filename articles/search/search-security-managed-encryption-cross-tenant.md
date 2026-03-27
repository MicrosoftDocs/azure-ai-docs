---
title: Configure CMK across different tenants in Azure AI Search
description: Configure cross-tenant customer-managed key encryption in Azure AI Search using either a managed identity with federated identity credentials or client secrets.
author: mattwojo
ms.author: mattwoj
ms.reviewer: mcarter
ms.date: 03/26/2026
ms.topic: how-to
ms.service: azure-ai-search
ms.custom: doc-kit-assisted
---

# Configure customer-managed keys across different tenants

This article provides guidance for configuring cross-tenant [customer-managed key (CMK) encryption](search-security-manage-encryption-keys.md) when your Azure AI Search service and Azure Key Vault are in different Microsoft Entra tenants.

This scenario is common for SaaS providers that host Azure AI Search in their own tenant while allowing customers to encrypt data by using keys stored in the customer’s Key Vault.

There are two possible approaches to enable cross-tenant CMK encryption for Azure AI Search:

1. **Use a Microsoft Entra multitenant application with a federated identity credential (FIC)** (preview): This is the recommended approach, but currently requires use of a preview API (version `2026-03-01-preview` or later). This approach allows Azure AI Search to access encryption keys in another tenant without the need for client secrets, enhancing security and simplifying management.

1. **Use a Microsoft Entra multitenant application with client secrets**: This approach is less secure and more complex to manage, as it requires handling client secrets. It is not recommended unless the first approach is not feasible for your scenario.

## Option 1: Use a Microsoft Entra multitenant application with a federated identity credential (preview)

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

To configure cross-tenant CMK encryption using a Microsoft Entra multitenant application with a federated identity credential (FIC)  paired with a user-assigned managed identity, so Azure AI Search can access encryption keys in another tenant without client secrets, follow these steps.

### Prerequisites for option 1

- A tenant (Tenant A) that contains Azure AI Search. To configure customer-managed keys (CMK), the search service must be on a [billable tier](search-sku-tier.md#tier-descriptions) (Basic or higher) in any region and must be [enabled for role-based access control](search-security-enable-roles.md).

- A separate tenant (Tenant B) that contains Azure Key Vault. The key vault must have [soft delete](../key-vault/general/soft-delete-overview.md), [purge protection](../key-vault/general/soft-delete-overview.md#purge-protection), and [role-based access control](../key-vault/general/rbac-guide.md) enabled.

- The [Azure CLI](/cli/azure/install-azure-cli) installed and signed in.

- [Permissions in both tenants](#required-permissions) to create applications, assign roles, and manage key vaults (see below).

#### Required permissions

| Tenant | Role | Purpose |
| ------ | ---- | ------- |
| Tenant A (search service) | [Owner or Contributor on the search service](/azure/search/search-security-rbac#built-in-roles-used-in-search) | Configure encryption and assign identities |
| Tenant A (search service) | Application Developer or Application Administrator | [Create the multitenant app registration and federated identity credential](#create-a-multitenant-microsoft-entra-application-in-tenant-a) |
| Tenant B (key vault) | [Global Administrator or Privileged Role Administrator](/azure/role-based-access-control/built-in-roles#privileged) | Grant admin consent for the multitenant application |
| Tenant B (key vault) | [Key Vault Crypto Officer](/azure/role-based-access-control/built-in-roles/security#key-vault-crypto-officer) | Create keys in the key vault |
| Tenant B (key vault) | [User Access Administrator](/azure/role-based-access-control/built-in-roles/privileged#user-access-administrator) | Assign Key Vault roles to the service principal |

### Create a multitenant Microsoft Entra application in tenant A

A multitenant Microsoft Entra application enables the search service to authenticate to a key vault in a different tenant. You can reuse the same application for multiple key vault tenants. Each tenant gets its own service principal with a different object ID.

To create the multitenant Microsoft Entra application:

1. Sign in to Tenant A where you deployed your Azure AI Search service using [Azure CLI](/cli/azure/what-is-azure-cli?view=azure-cli-latest).

    ```azurecli
    az login --tenant "$TENANT_A_ID"
    az account set --subscription "$TENANT_A_SUBSCRIPTION_ID"
    ```

1. Create the multitenant application registration.

    ```azurecli
    APP_ID=$(az ad app create \
      --display-name "$APP_NAME" \
      --sign-in-audience "AzureADMultipleOrgs" \
      --query appId -o tsv)
    
    echo "APP_ID=$APP_ID"
    ```

    The output is a GUID in the format `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`. Save this value. You need it throughout the remaining steps.

1. Write down the application ID. You need it throughout the remaining steps, and you must provide it to Tenant B to create a service principal.

### Create a user-assigned managed identity

You will need to create a user-assigned managed identity (UAMI) and assign it to the Azure AI Search service. The managed identity acts as the workload identity for cross-tenant authentication.

You will also need to configure a multitenant Microsoft Entra application with a federated identity credential (FIC) that trusts the managed identity. At runtime, Azure AI Search uses the managed identity and federated identity flow to obtain access tokens and call the customer’s Azure Key Vault for customer-managed key (CMK) operations, without using client secrets.

To create the user-assigned managed identity and assign it to the search service:

1. Create the managed identity and capture its resource ID:

    ```azurecli
    az identity create -g "$TENANT_A_RG" -n "$UAMI_NAME"
    
    UAMI_ID=$(az identity show -g "$TENANT_A_RG" -n "$UAMI_NAME" --query id -o tsv)
    ```

    The `UAMI_ID` value is a full resource ID in the format `/subscriptions/<sub-id>/resourcegroups/<rg>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<name>`.

1. Assign the managed identity to the search service:

    ```azurecli
    az search service update \
      --name "$SEARCH_NAME" \
      --resource-group "$SEARCH_RG" \
      --identity-type "UserAssigned" \
      --user-assigned-identities "$UAMI_ID"
    ```

### Add a federated identity credential

You will also need to add a federated identity credential (FIC) on the multitenant Microsoft Entra application to allow Azure AI Search to exchange its UAMI token for an application access token, enabling access to Azure Key Vault without using a client secret.

> [!IMPORTANT]
> An application can have a maximum of 20 federated identity credentials. If you manage multiple Tenant B key vaults, you might need to share federated identities. For more information, see [Important considerations and restrictions](/entra/workload-id/workload-identity-federation-considerations).

To get the principal ID of the UAMI and create a FIC configuration file:

1. Retrieve the managed identity’s principal (object) ID:

    ```azurecli
    UAMI_PRINCIPAL_ID=$(az identity show -g "$TENANT_A_RG" -n "$UAMI_NAME" --query principalId -o tsv)
    ```

2. Create the federated identity credential JSON:

    ```azurecli
    cat > fic.json <<EOF
    {
      "name": "search-uami-fic",
      "issuer": "https://login.microsoftonline.com/$TENANT_A_ID/v2.0",
      "subject": "$UAMI_PRINCIPAL_ID",
      "audiences": ["api://AzureADTokenExchange"],
      "description": "Trust Azure AI Search UAMI to act as this app for Key Vault access"
    }
    EOF
    ```

3. Add the federated credential to the application:

    ```azurecli
    az ad app federated-credential create \
      --id "$APP_ID" \
      --parameters fic.json
    ```

### Grant consent for the application

Install the multitenant application in Tenant B so that you create a service principal. You need administrator-level permissions in Tenant B to perform these steps.

#### Consent Option A: Admin consent URL

Grant admin consent by opening the following URL in Tenant B. You need to be a Global Administrator or Privileged Role Administrator.

```html
https://login.microsoftonline.com/<TENANT_B_ID>/adminconsent?client_id=<APP_ID>
```

#### Consent Option B: Azure CLI

Sign in to Tenant B and create the service principal directly:

```azurecli
az login --tenant "$TENANT_B_ID"
az account set --subscription "$TENANT_B_SUBSCRIPTION_ID"

SP_OBJECT_ID=$(az ad sp create --id "$APP_ID" --query id -o tsv)

echo "Service Principal ObjectId: $SP_OBJECT_ID"
```

The output is the object ID of the service principal created in Tenant B.

### Grant key vault permissions

Assign the **Key Vault Crypto Service Encryption User** role to the service principal in Tenant B. By using this role, Azure AI Search can use the key for wrap and unwrap operations.

```azurecli
KV_ID=$(az keyvault show -n "$TENANT_B_KV_NAME" -g "$TENANT_B_KV_RG" --query id -o tsv)

SP_OBJECT_ID=$(az ad sp list --filter "appId eq '$APP_ID'" --query "[0].id" -o tsv)

az role assignment create \
  --assignee-object-id "$SP_OBJECT_ID" \
  --assignee-principal-type ServicePrincipal \
  --role "Key Vault Crypto Service Encryption User" \
  --scope "$KV_ID"
```

### Create an encryption key

Create an RSA key in the Tenant B key vault. Skip this section if Tenant B already has a key to use.

```azurecli
az keyvault key create \
  --vault-name "$TENANT_B_KV_NAME" \
  --name "$TENANT_B_KEY_NAME" \
  --kty RSA \
  --size 2048

TENANT_B_KEY_VERSION=$(az keyvault key show \
  --vault-name "$TENANT_B_KV_NAME" \
  --name "$TENANT_B_KEY_NAME" \
  --query "properties.version" -o tsv)

echo "TENANT_B_KEY_VERSION=$TENANT_B_KEY_VERSION"
```

The `TENANT_B_KEY_VERSION` value is a hex string that represents the key version (for example, `abc123def456ghi789`).

To complete this step, you need the key vault name, key name, and key version from Tenant B.

### Create an encrypted index

Create a search index in Tenant A with the `encryptionKey` property configured for cross-tenant access. The `identity` block specifies the user-assigned managed identity and the federated identity client ID, replacing the `accessCredentials` property.

Sign back in to Tenant A:

```azurecli
az login --tenant "$TENANT_A_ID"
az account set --subscription "$TENANT_A_SUBSCRIPTION_ID"
```

Send a request to create the index with cross-tenant CMK encryption:

```http
POST https://<search-service>.search.windows.net/indexes?api-version=2026-03-01-preview
Content-Type: application/json
api-key: <ADMIN-API-KEY>

{
  "name": "cmk-demo",
  "fields": [
    {
      "name": "id",
      "type": "Edm.String",
      "key": true,
      "filterable": false,
      "sortable": false,
      "facetable": false
    },
    {
      "name": "content",
      "type": "Edm.String",
      "searchable": true
    }
  ],
  "encryptionKey": {
    "keyVaultUri": "https://<TENANT_B_KV_NAME>.vault.azure.net/",
    "keyVaultKeyName": "<TENANT_B_KEY_NAME>",
    "keyVaultKeyVersion": "<TENANT_B_KEY_VERSION>",
    "identity": {
      "@odata.type": "#Microsoft.Azure.Search.DataUserAssignedIdentity",
      "userAssignedIdentity": "<UAMI-RESOURCE-ID>",
      "federatedIdentityClientId": "<APP_ID>"
    }
  }
}
```

The `identity` block contains these properties:

| Property | Description |
|----------|-------------|
| `@odata.type` | Must be `#Microsoft.Azure.Search.DataUserAssignedIdentity`. |
| `userAssignedIdentity` | The full resource ID of the user-assigned managed identity assigned to the search service. |
| `federatedIdentityClientId` | The application (client) ID of the multitenant Microsoft Entra application. |

### Validate the configuration

Verify that cross-tenant CMK encryption works correctly after you create the index.

Send a GET request to the index endpoint and verify the response includes the `encryptionKey` property:

```http
GET https://<search-service>.search.windows.net/indexes/cmk-demo?api-version=2026-03-01-preview
api-key: <ADMIN-API-KEY>
```

Upload a document to the index and run a search query to confirm the index is operational.

In the Tenant B key vault, review the audit logs to confirm that wrap and unwrap operations appear from the service principal associated with the multitenant application.

### Rotate or revoke encryption keys

For guidance on rotating keys, updating key versions, or revoking access, see [Rotate or update encryption keys](search-security-manage-encryption-keys.md#rotate-or-update-encryption-keys). The same key lifecycle guidance applies to cross-tenant configurations. Azure AI Search caches the key for up to 60 minutes, so allow time for changes to take effect.

### Summary of values exchanged between tenants

Tenant A and Tenant B need to exchange specific values during setup:

| From | To | Values |
| ---- | --- | ----- |
| Tenant A | Tenant B | Multitenant application ID |
| Tenant B | Tenant A | Key vault name, key name, key version |

## Option 2: Use a Microsoft Entra multitenant application with client secrets

To configure cross-tenant CMK encryption using a Microsoft Entra multitenant application that uses `accessCredentials` with an application ID and client secret, follow these steps. *This approach is less secure and more complex to manage, as it requires handling client secrets. It is not recommended unless the FIC approach (option 1) is not feasible for your scenario.*

### Prerequisites for option 2

- A tenant containing the search service that has content you want to encrypt. Azure AI Search must be [configured for role-based access](search-security-enable-roles.md). Support for CMK requires Basic pricing tier or higher.

- A separate tenant having the Azure Key Vault and the encryption keys you want to use. Azure Key Vault must be [configured for role-based access](/azure/key-vault/general/rbac-guide).

- The [Azure CLI](/cli/azure/install-azure-cli) installed and signed in.

### Create a multitenant Microsoft Entra application in tenant A

Use the Azure CLI to send requests. We refer to the tenant containing Azure AI Search as *tenant A*.

1. Get the tenant ID:

   `az account show --query tenantId --output tsv`

1. Make sure you're signed in to tenant A:

   `az login --tenant <tenant-A-id> `

1. Create the application registration:

   `az ad app create --display-name cross-tenant-auth --sign-in-audience AzureADMultipleOrgs `

1. Save the app ID output from this step.

### Add a client secret to the multitenant application

1. To add the client secret to the multitenant application in tenant A, run the following command:

   `az ad app credential reset --id <multitenant-app-id>`

1. Save the password output from this step. The password output is a required input for [setting up CMK](search-security-manage-encryption-keys.md) in Azure AI Search.

1. To specify when the client secret expires, you can specify an end-date parameter to this command.

   `az ad app credential reset --id <multitenant-app-id> --end-date <end-date>`

   The end-date parameter accepts a date in ISO 8601 format. For example: `az ad app credential reset --id <multitenant-app-id> --end-date 2026-12-31`.

### Create a service principal in tenant B for the multitenant application

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

### Test encryption

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

## Related content

- [Configure customer-managed keys for data encryption in Azure AI Search](search-security-manage-encryption-keys.md)
- [Configure cross-tenant customer-managed keys for a new storage account](/azure/storage/common/customer-managed-keys-configure-cross-tenant-new-account)
- [Configure cross-tenant customer-managed keys for an Azure Cosmos DB account](/azure/cosmos-db/how-to-setup-cross-tenant-customer-managed-keys)
- [Cross-tenant customer-managed keys with transparent data encryption](/azure/azure-sql/database/transparent-data-encryption-byok-cross-tenant)
- [What are managed identities for Azure resources?](/entra/identity/managed-identities-azure-resources/overview)
- [Workload identity federation](/entra/workload-id/workload-identity-federation)
