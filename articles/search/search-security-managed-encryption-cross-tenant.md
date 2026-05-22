---
title: Cross-Tenant CMKs
description: Set up CMK encryption in Azure AI Search that uses a key from an Azure Key Vault in another tenant.
ms.reviewer: magottei
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 06/02/2026
ms.update-cycle: 180-days
ai-usage: ai-assisted
---

# Configure customer-managed keys across different tenants

This article describes a cross-tenant scenario where a service provider hosts Azure AI Search in their own tenant and enables [customer-managed key (CMK) encryption](search-security-manage-encryption-keys.md) using a multitenant Microsoft Entra application. 

In this configuration, the customer uses Azure Key Vault in their own tenant to manage their encryption key. The service provider has no access to this key.

## Prerequisites

- **Tenant A**: A tenant and the necessary permissions to create the Azure AI Search service and associated objects (indexes, synonym lists, indexers, data sources, vectorizers, skillsets). Support for customer-managed keys (CMK) requires Basic pricing tier or higher.

- The search service must be [configured for role-based access](/azure/search/search-security-enable-roles).

- **Tenant B:** A separate customer tenant with an Azure Key Vault and the necessary permissions on that tenant:
  - **[Key Vault Contributor](/azure/role-based-access-control/built-in-roles#key-vault-contributor)**: This role is required if you need to create a new key vault.
  - **Permission to register applications in Microsoft Entra ID**: To install the multitenant app configured by the service provider for cross-tenant CMK, you must have permission to create app registrations in Microsoft Entra ID. This typically requires the [Application Developer role](/entra/identity/role-based-access-control/permissions-reference#application-developer) or a higher administrative role, such as Application Administrator or Global Administrator.
  - [Key Vault Crypto Officer](/azure/role-based-access-control/built-in-roles#key-vault-crypto-officer): This role is required to add a new key to the key vault.
  - [Key Vault Crypto Service Encryption User](/azure/role-based-access-control/built-in-roles#key-vault-crypto-service-encryption-user): This role must be assigned to the service principal created for the installed multitenant application in order to grant the service principal access to the customer-managed key in the key vault. You must have [User Access Administrator permission](/azure/role-based-access-control/rbac-and-directory-admin-roles#azure-roles) to do this. You can view the service principal GUID (aka Object ID) under: `Enterprise applications\<installed multitenant application>\Manage\Properties\Object ID`.

- The Azure Key Vault must also be [configured for role-based access](/azure/key-vault/general/rbac-guide).

- [Azure CLI](/cli/azure/install-azure-cli) for sending requests.

## Choose an authentication approach

You can configure a multitenant Microsoft Entra application to use customer-managed keys in a cross-tenant scenario by using one of the following approaches:

1. **Federated identity support (recommended)**: Configure Microsoft Entra federated identity credentials (FIC) with a user-assigned managed identity (UAMI). This approach uses managed identity tokens and exchanges them for access tokens, eliminating the need for long-lived secrets and aligning with workload identity federation principles. This approach requires the preview `federatedIdentityClientId` property, introduced in API version `2026-05-01-preview`.

1. **Client secrets**: Configure a client secret using the `accessCredentials` property. This approach is less secure and requires additional management to rotate and protect the secret.

> [!NOTE]
> Azure Key Vault and Azure Key Vault Managed HSM use the same APIs and management interfaces for customer-managed keys. Any supported operation in Azure Key Vault is also supported in Azure Key Vault Managed HSM.

## Create a multitenant Microsoft Entra application in tenant A

Use the Azure CLI to send requests. The service provider’s tenant that contains Azure AI Search will be referred to as *tenant A*.

1. Get the tenant ID: `az account show --query tenantId --output tsv`

1. Make sure you're signed in to tenant A: `az login --tenant \<tenant-A-id\>`

1. Create the application registration: `az ad app create --display-name cross-tenant-auth --sign-in-audience AzureADMultipleOrgs`

1. Save the app ID output from this step.

## Use federated identity support (preview)

> [!IMPORTANT]
> These features and functionality are part of the 2026-05-01-preview REST API. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

To use federated identity to support a cross-tenant CMK scenario:

1. The service provider configures the AI Search service in their tenant (Tenant A). For guidance on how to do this, see [Create a Search Service (in the Azure portal)](/azure/search/search-create-service-portal) or use the [az search service create](/cli/azure/search/service#az-search-service-create) command in Azure CLI.

1. The service provider creates a multitenant Microsoft Entra app registration. For guidance on how to do this, see [How to register an app in Microsoft Entra ID](/entra/identity-platform/quickstart-register-app), or use the Azure CLI command: [az ad app create](/cli/azure/ad/app#az-ad-app-create). Record the Application (client) ID once you complete the app registration.

1. The service provider sets up a user-assigned managed identity. For guidance on how to do this, see [Manage user-assigned managed identities using Azure portal](/entra/identity/managed-identities-azure-resources/manage-user-assigned-managed-identities-azure-portal?pivots=identity-mi-methods-azp&preserve-view=true) or [Manage user-assigned managed identities using the Azure CLI](/entra/identity/managed-identities-azure-resources/manage-user-assigned-managed-identities-azure-cli).

1. The service provider configures the user-assigned managed identities as a federated identity credential on the app. For guidance on how to do this, see [Configure an app to trust an external identity provider](/entra/workload-id/workload-identity-federation-create-trust?pivots=identity-wif-apps-methods-azp)*.*

1. Once the service provider shares the multitenant app ID, the customer grants the service provider’s app access to the Key Vault in their tenant (Tenant B). To install the app in Tenant B, a service principal must be created with the multitenant app ID. To create the service principal, construct an [admin-consent URL](/azure/active-directory/manage-apps/grant-admin-consent#construct-the-url-for-granting-tenant-wide-admin-consent) and grant tenant-wide consent or use the [az ad sp](/cli/azure/ad/sp#az-ad-sp-create) command in Azure CLI.

1. If the customer doesn’t already have a key vault to use, see [Quickstart - Create an Azure Key Vault with the Azure portal](/azure/key-vault/general/quick-create-portal) or [Quickstart - Create an Azure Key Vault with the Azure CLI](/azure/key-vault/general/quick-create-cli). The Key Vault will need the permission model set to “Azure role-based access control (RBAC)” with the service provider’s multitenant application granted permission by assigning it the [Key Vault Crypto Service Encryption User role](/azure/key-vault/general/rbac-guide?preserve-view=true&tabs=azure-cli#azure-built-in-roles-for-key-vault-data-plane-operations). The customer can then create an encryption key. For guidance on how to do this, see [Grant permission to applications to access an Azure key vault using Azure RBAC](/azure/key-vault/general/rbac-guide?tabs=azure-cli).

Once these steps are completed, the service provider now has:

- An application ID for a multitenant application installed in the customer's tenant, which has been granted access to the customer-managed key.

- A managed identity configured as the federated credential on the multitenant application.

- The location of the key in the customer's key vault.

With these three parameters, the service provider can now create Azure AI Search objects in *Tenant A* that can be encrypted with the customer-managed key stored in *Tenant B*. For guidance on how to configure customer-managed keys on new search objects, see [Configure customer-managed keys for Azure AI Search encrypted data](/azure/search/search-security-manage-encryption-keys?tabs=azure-key-vault%2Cmanaged-id-sys%2Cportal%2Cmgmt-rest-create%2Cmgmt-rest-update).


### Validate the federated identity cross-tenant CMK configuration

After you configure the multitenant Microsoft Entra application and connect it to the customer's Key Vault, verify the setup by creating a test object in your search service (tenant A). This example creates an index to confirm that the search service can access the customer-managed key using federated identity authentication.

1. See [Configure customer-managed keys for Azure AI Search encrypted data](search-security-manage-encryption-keys.md) for guidance on how to create a search service and a new index object with a customer-managed key.

1. Once the index object is created, you will need to fill in the following:

    - `keyVaultUri`: The URI address from the customer.
    - `keyVaultKeyName`: The key name from the customer.
    - `keyVaultKeyVersion`: The key version from the customer.
    - `userAssignedIdentity`: The `<subscription-id>` and `<resource-group>` from your tenant, and the `<identity-name>` is the user-assigned managed identity name.
    - `federatedIdentityClientId`: This property value, `<application-client-id>`, will be the multitenant application (client) ID. 

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
        "keyVaultUri": "https://<key-vault-name>.vault.azure.net/",
        "keyVaultKeyName": "<key-name>",
        "keyVaultKeyVersion": "<key-version>",
        "identity": {
          "@odata.type": "#Microsoft.Azure.Search.DataUserAssignedIdentity",
          "userAssignedIdentity": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<identity-name>",
          "federatedIdentityClientId": "<application-client-id>"
        }
      }
    }
    ```

1. Verify the index by sending a `GET` request: `GET https://<search-service>.search.windows.net/indexes/cross-tenant-cmk-test?api-version=2026-05-01-preview`

If the request succeeds, the cross-tenant CMK configuration is working correctly.

If index creation fails with a key access error, verify that:

- The user-assigned managed identity is configured correctly
- The federated identity credential is set on the app
- The Key Vault access policy or RBAC role assignments are correct


## Use a client secret (if using federated identity is not an option)

If federated identity isn't an option, you can add a client secret to the multitenant application to support a cross-tenant CMK scenario:

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

### Validate the client secret cross-tenant CMK configuration

After you configure the multitenant Microsoft Entra application and connect it to the customer's Key Vault, verify the setup by creating a test object in your search service (tenant A). This example creates an index to confirm that the search service can access the customer-managed key using the client secret.

1. See [Configure customer-managed keys for Azure AI Search encrypted data](search-security-manage-encryption-keys.md) for guidance on how to create a search service and a new index object with a customer-managed key.

1. You can use the Azure portal to add an index and provide this JSON, or use a [REST client](search-get-started-text.md) to send a `Create Index` request. Once the index object is created, you will need to fill in the following:

    - `keyVaultUri`: The URI address from the customer.
    - `keyVaultKeyName`: The key name from the customer.
    - `keyVaultKeyVersion`: The key version from the customer.
    - `accessCredentials`: The `applicationId` will look something like "12345678-1234-1234-1234-123456789012" and the `applicationSecret` that was just created.

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
        "keyVaultUri": "https://<key-vault-name>.vault.azure.net/",
        "keyVaultKeyName": "<key-name>",
        "keyVaultKeyVersion": "<key-version>",
    "accessCredentials": { 
      "applicationId": "<application-client-id>", 
      "applicationSecret": "<application-client-secret>" 
    } 
  } 
}
```

Verify the index was created successfully:

```http
GET https://<search-service>.search.windows.net/indexes/cross-tenant-cmk-test?api-version=2026-04-01
```

For more information about how to rotate or manage keys, see [Configure customer-managed keys for data encryption](search-security-manage-encryption-keys.md).
