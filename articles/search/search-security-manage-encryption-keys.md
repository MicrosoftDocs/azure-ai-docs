---
title: Encrypt data using customer-managed keys
titleSuffix: Azure AI Search
description: Supplement server-side encryption in Azure AI Search using customer managed keys (CMK) or bring your own keys (BYOK) that you create and manage in Azure Key Vault.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 09/18/2025
ms.update-cycle: 365-days
ms.custom:
  - references_regions
  - ignite-2023
  - sfi-image-nochange
---

# Configure customer-managed keys for data encryption in Azure AI Search

Azure AI Search automatically encrypts data at rest with [Microsoft-managed keys](/azure/security/fundamentals/encryption-atrest#azure-encryption-at-rest-components). If you need another layer of encryption or the ability to revoke keys and shut down access to content, you can use keys that you create and manage in Azure Key Vault. This article explains how to set up customer-managed key (CMK) encryption.

You can store keys using either:

+ Azure Key Vault

+ Azure Key Vault Managed HSM (Hardware Security Module). An Azure Key Vault Managed HSM is an FIPS 140-2 Level 3 validated HSM. HSM support is new in Azure AI Search. To migrate from Azure Key Vault to HSM, [rotate your keys](#rotate-or-update-encryption-keys) and choose Managed HSM for storage.

> [!IMPORTANT]
> + CMK provides encryption for data at rest. If you need to protect data in use, consider using [confidential computing](search-security-overview.md#data-in-use).
>
> + CMK encryption is irreversible. You can rotate keys and change CMK configuration, but index encryption lasts for the lifetime of the index. Post-CMK encryption, an index is only accessible if the search service has access to the key. If you revoke access to the key by deleting or changing role assignment, the index is unusable and the service can't be scaled until the index is deleted or access to the key is restored. If you delete or rotate keys, the most recent key is cached for up to 60 minutes.

## CMK encrypted objects

CMK encryption applies to individual objects when they're created. This means you can't encrypt objects that already exist. CMK encryption occurs each time an object is saved to disk, for both data at rest (long-term storage) or temporary cached data (short-term storage). With CMK, the disk never sees unencrypted data.

Objects that can be encrypted include indexes, synonym lists, indexers, data sources, and skillsets. Encryption is computationally expensive to decrypt so only sensitive content is encrypted.

Encryption is performed over the following content:

+ All content within indexes and synonym lists.

+ Sensitive content in indexers, data sources, skillsets, and vectorizers. Sensitive content refers to connection strings, descriptions, identities, keys, and user inputs. For example, skillsets have Foundry Tools keys, and some skills accept user inputs, such as custom entities. In both cases, keys and user inputs are encrypted. Any references to external resources (such as Azure data sources or Azure OpenAI models) are also encrypted.

If you require CMK across your search service, [set an enforcement policy](#set-up-a-policy-to-enforce-cmk-compliance).

Although you can't add encryption to an existing object, once an object is configured for encryption, you can change all parts of its encryption definition, including switching to a different key vault or HMS storage as long as the resource is in the same tenant.

## Prerequisites

+ [Azure AI Search](search-create-service-portal.md) on a [billable tier](search-sku-tier.md#tier-descriptions) (Basic or higher, in any region).

+ [Azure Key Vault](/azure/key-vault/general/overview) and a key vault with **soft-delete** and **purge protection** enabled. Or, [Azure Key Vault Managed HSM](/azure/key-vault/managed-hsm/overview). This resource can be in any subscription and in a different tenant. These instructions assume a single tenant. For cross-tenant configuration, see [Configure customer-managed keys across different tenants](search-security-managed-encryption-cross-tenant.md).

+ Ability to set up permissions for key access and to assign roles. To create keys, you must be **Key Vault Crypto Officer** in Azure Key Vault or **Managed HSM Crypto Officer** in Azure Key Vault Managed HSM.

  To assign roles, you must be subscription **Owner**, **User Access Administrator**, **Role-based Access Control Administrator**, or be assigned to a custom role with **Microsoft.Authorization/roleAssignments/write** permissions.

## Step 1: Create an encryption key

Use either Azure Key Vault or Azure Key Vault Managed HSM to create a key. Azure AI Search encryption supports RSA keys of sizes 2048, 3072 and 4096. For more information about supported key types, see [About keys](/azure/key-vault/keys/about-keys).

We recommend reviewing [these tips](#key-vault-tips) before you start.

Required operations are **Wrap**, **Unwrap**, **Encrypt**, and **Decrypt**.

### [**Azure Key Vault**](#tab/azure-key-vault)

You can [create a key vault using the Azure portal](/azure/key-vault/general/quick-create-portal), [Azure CLI](/azure/key-vault/general/quick-create-cli), or [Azure PowerShell](/azure/key-vault/general/quick-create-powershell).

1. Sign in to the [Azure portal](https://portal.azure.com) and open your key vault overview page.

1. Select **Objects** > **Keys** on the left, and then select **Generate/Import**.

1. In the **Create a key** pane, from the list of **Options**, choose **Generate** to create a new key.

1. Enter a **Name** for your key, and accept the defaults for other key properties.

1. Optionally, set a key rotation policy to [enable auto rotation](/azure/key-vault/keys/how-to-configure-key-rotation).

1. Select **Create** to start the deployment.

1. After the key is created, get its key identifier. Select the key, select the current version, and then copy the key identifier. It's composed of the **key value Uri**, the **key name**, and the **key version**. You need the identifier to define an encrypted index in Azure AI Search. Recall that required operations are **Wrap**, **Unwrap**, **Encrypt**, and **Decrypt**.

   :::image type="content" source="media/search-manage-encryption-keys/cmk-key-identifier.png" alt-text="Create a new key vault key" border="true":::

### [**Managed HSM**](#tab/managed-hsm)

You can create and activate a Managed HSM in the Azure portal, [Azure CLI](/azure/key-vault/managed-hsm/quick-create-cli), or [Azure PowerShell](/azure/key-vault/managed-hsm/quick-create-powershell).

To generate or import a key, use the [Azure CLI](/azure/key-vault/managed-hsm/key-management).

---

## Step 2: Create a security principal

Create a security principal that your search service uses to access to the encryption key. You can use a managed identity and role assignment, or you can register an application and have the search service provide the application ID on requests.

We recommend using a managed identity and roles. You can use either a system-managed identity or user-managed identity. A managed identity enables your search service to authenticate through Microsoft Entra ID, without storing credentials (ApplicationID or ApplicationSecret) in code. The lifecycle of this type of managed identity is tied to the lifecycle of your search service, which can only have one system assigned managed identity. For more information about how managed identities work, see [What are managed identities for Azure resources](/azure/active-directory/managed-identities-azure-resources/overview).

### [**System-managed identity**](#tab/managed-id-sys)

Enable the system-assigned managed identity for your search service. It's a two-click operation: enable and save.

![Screenshot of turn on system assigned managed identity.](media/search-managed-identities/turn-on-system-assigned-identity.png "Screenshot showing how to turn on the system-assigned managed identity.")

### [**User-managed identity**](#tab/managed-id-user)

You can use the Azure portal or Search Management REST APIs to create a user-assigned managed identity and assign the identity to your search service. For more information, see [Create a user-assigned managed identity](search-how-to-managed-identities.md#create-a-user-assigned-managed-identity).

### [**Register an app**](#tab/register-app)

Follow these instructions if you can't use role assignments for search service access to encryption keys.

1. In the [Azure portal](https://portal.azure.com), find the Microsoft Entra resource for your subscription.

1. On the left, under **Manage**, select **App registrations**, and then select **New registration**.

1. Give the registration a name, perhaps a name that is similar to the search application name. Select **Register**.

1. Once the app registration is created, copy the Application ID. You need to provide this string to your application. 

   If you're stepping through the [DotNetHowToEncryptionUsingCMK](https://github.com/Azure-Samples/search-dotnet-getting-started/tree/master/DotNetHowToEncryptionUsingCMK), paste this value into the **appsettings.json** file.

   :::image type="content" source="media/search-manage-encryption-keys/cmk-application-id.png" alt-text="Application ID in the Essentials section":::

1. Next, select **Certificates & secrets**.

1. Select **New client secret**. Give the secret a display name and select **Add**.

1. Copy the application secret. If you're stepping through the sample, paste this value into the **appsettings.json** file.

   :::image type="content" source="media/search-manage-encryption-keys/cmk-application-secret.png" alt-text="Application secret":::

---

## Step 3: Grant permissions

If you configured your search service to use a managed identity, assign roles that give it access to the encryption key.

Role-based access control is recommended over the Access Policy permission model. For more information or migration steps, start with [Azure role-based access control (Azure RBAC) vs. access policies (legacy)](/azure/key-vault/general/rbac-access-policy).

1. Sign in to the [Azure portal](https://portal.azure.com) and find your key vault.

1. Select **Access control (IAM)** and select **Add role assignment**.

1. Select a role:

   + On Azure Key Vault, select **Key Vault Crypto Service Encryption User**.
   + On Managed HSM, select **Managed HSM Crypto Service Encryption User**.

1. Select managed identities, select members, and then select the managed identity of your search service. If you're testing locally, assign this role to yourself as well.

1. Select **Review + Assign**.

Wait a few minutes for the role assignment to become operational.

## Step 4: Encrypt content

Encryption occurs when you create or update an object. You can use the Azure portal for select objects. For all objects, use the [Search Service REST APIs](/rest/api/searchservice/) or an Azure SDK.

### [**Azure portal**](#tab/portal)

When you create a new object in the Azure portal, you can specify a predefined customer-managed key in a key vault. The Azure portal lets you enable CMK encryption for:

+ Indexes
+ Data sources
+ Indexers

Requirements for using the Azure portal are that the key vault and key must exist, and you completed the previous steps for authorized access to the key.

In the Azure portal, skillsets are defined in JSON view. Use the JSON shown in the REST API examples to provide a customer-managed key on a skillset.

1. Sign in to the [Azure portal](https://portal.azure.com) and open your search service page.

1. Under **Search management**, select **Indexes**, **Indexers**, or **Data Sources**.

1. Add a new object. In the object definition, select **Microsoft-managed encryption**.

1. Select **Customer-managed keys** and choose your subscription, vault, key, and version.

:::image type="content" source="media/search-security-manage-encryption-keys/assign-key-vault.png" alt-text="Screenshot of the encryption key page in the Azure portal.":::

### [**REST APIs**](#tab/rest)

1. Call the creation APIs to specify the **encryptionKey** property:

   + [Create Index](/rest/api/searchservice/indexes/create)
   + [Create Synonym Map](/rest/api/searchservice/synonym-maps/create)
   + [Create Indexer](/rest/api/searchservice/indexers/create)
   + [Create Data Source](/rest/api/searchservice/data-sources/create)
   + [Create Skillset](/rest/api/searchservice/skillsets/create)

1. Insert the encryptionKey construct into the object definition. This property is a first-level property, on the same level as name and description. If you're using the same vault, key, and version, you can paste in the same encryptionKey construct into each object definition. 

   If your key identifier is `https://contoso-keyvault.vault.azure.net/keys/contoso-cmk/aaaaaaaa-0b0b-1c1c-2d2d-333333333333`, then the URI is `https://contoso-keyvault.vault.azure.net`, the key name is `contoso-cmk`, and the version is `aaaaaaaa-0b0b-1c1c-2d2d-333333333333`.

    ```json
    {
      "encryptionKey": {
        "keyVaultUri": "<YOUR-KEY-VAULT-URI>",
        "keyVaultKeyName": "<YOUR-ENCRYPTION-KEY-NAME>",
        "keyVaultKeyVersion": "<YOUR-ENCRYPTION-KEY-VERSION>",
        "identity" : { 
            "@odata.type": "#Microsoft.Azure.Search.DataUserAssignedIdentity",
            "userAssignedIdentity" : "/subscriptions/<your-subscription-ID>/resourceGroups/<your-resource-group-name>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<your-managed-identity-name>"
        }
      }
    }
    ```

   The first example shows an encryptionKey for a search service that connects using a managed identity:

    ```json
    {
      "encryptionKey": {
        "keyVaultUri": "<YOUR-KEY-VAULT-URI>",
        "keyVaultKeyName": "<YOUR-ENCRYPTION-KEY-NAME>",
        "keyVaultKeyVersion": "<YOUR-ENCRYPTION-KEY-VERSION>"
      }
    }
    ```

    The second example includes accessCredentials, necessary if you registered an application in Microsoft Entra ID:

    ```json
    {
      "encryptionKey": {
        "keyVaultUri": "<YOUR-KEY-VAULT-URI>",
        "keyVaultKeyName": "<YOUR-ENCRYPTION-KEY-NAME>",
        "keyVaultKeyVersion": "<YOUR-ENCRYPTION-KEY-VERSION>",
        "accessCredentials": {
          "applicationId": "<YOUR-APPLICATION-ID>",
          "applicationSecret": "<YOUR-APPLICATION-SECRET>"
        }
      }
    }
    ```

1. Verify the encryption key exists by issuing a GET on the object.

   + [GET Index](/rest/api/searchservice/indexes/get)
   + [GET Synonym Map](/rest/api/searchservice/synonym-maps/get)
   + [GET Indexer](/rest/api/searchservice/indexers/get)
   + [GET Data Source](/rest/api/searchservice/data-sources/get)
   + [GET Skillset](/rest/api/searchservice/skillsets/get)

1. Verify the object is operational by performing a task, such as query an index that's encrypted.

After you create the encrypted object on the search service, you can use it as you would any other object of its type. Encryption is transparent to the user and developer.

None of these key vault details are considered secret and could be easily retrieved by browsing to the relevant Azure Key Vault page in Azure portal.

### [**Python**](#tab/python)

This example shows the Python representation of an `encryptionKey` in an object definition. The same definition applies to indexes, data sources, skillets, indexers, and synonym maps. To try this example on your search service and key vault, download the notebook from [azure-search-python-samples](https://github.com/Azure-Samples/azure-search-python-samples).

1. Install some packages.

    ```python
    ! pip install python-dotenv
    ! pip install azure-core
    ! pip install azure-search-documents==11.5.1
    ! pip install azure-identity
    ```

1. Create an index that has an encryption key.

    ```python
    from azure.search.documents.indexes import SearchIndexClient
    from azure.search.documents.indexes.models import (
    SimpleField,
    SearchFieldDataType,
    SearchableField,
    SearchIndex,
    SearchResourceEncryptionKey
    )
    from azure.identity import DefaultAzureCredential

    endpoint="<PUT YOUR AZURE SEARCH SERVICE ENDPOINT HERE>"
    credential = DefaultAzureCredential()

    index_name = "test-cmk-index"
    index_client = SearchIndexClient(endpoint=endpoint, credential=credential)
    fields = [
    SimpleField(name="Id", type=SearchFieldDataType.String, key=True),
    SearchableField(name="Description", type=SearchFieldDataType.String)
    ]

    scoring_profiles = []
    suggester = []
    encryption_key = SearchResourceEncryptionKey(
    key_name="<PUT YOUR KEY VAULT NAME HERE>",
    key_version="<PUT YOUR ALPHANUMERIC KEY VERSION HERE>",
    vault_uri
    )
    
    index = SearchIndex(name=index_name, fields=fields, encryption_key=encryption_key)
    result = index_client.create_or_update_index(index)
    print(f' {result.name} created')
    ```

1. Get the index definition to verify encryption key configuration exists.

    ```python
    index_name = "test-cmk-index-qs"
    index_client = SearchIndexClient(endpoint=AZURE_SEARCH_SERVICE, credential=credential)  
        
    result = index_client.get_index(index_name)  
    print(f"{result}")  
    ```

1. Load the index with a few documents. All field content is considered sensitive and is encrypted on disk using your customer managed key.

    ```python
    from azure.search.documents import SearchClient
    
    # Create a documents payload
    documents = [
        {
        "@search.action": "upload",
        "Id": "1",
        "Description": "The hotel is ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Time's Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities."
        },
        {
        "@search.action": "upload",
        "Id": "2",
        "Description": "The hotel is situated in a  nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts."
        },
        {
        "@search.action": "upload",
        "Id": "3",
        "Description": "The hotel stands out for its gastronomic excellence under the management of William Dough, who advises on and oversees all of the Hotel's restaurant services."
        },
        {
        "@search.action": "upload",
        "Id": "4",
        "Description": "The hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Palace is part of a lovingly restored 1800 palace."
        }
    ]
    
    search_client = SearchClient(endpoint=AZURE_SEARCH_SERVICE, index_name=index_name, credential=credential)
    try:
        result = search_client.upload_documents(documents=documents)
        print("Upload of new document succeeded: {}".format(result[0].succeeded))
    except Exception as ex:
        print (ex.message)
    
        index_client = SearchClient(endpoint=AZURE_SEARCH_SERVICE, credential=credential)
    ```

1. Run a query to confirm the index is operational.

    ```python
    from azure.search.documents import SearchClient
    
    query = "historic"  
    
    search_client = SearchClient(endpoint=AZURE_SEARCH_SERVICE, credential=credential, index_name=index_name)
      
    results = search_client.search(  
        query_type='simple',
        search_text=query, 
        select=["Id", "Description"],
        include_total_count=True
        )
      
    for result in results:  
        print(f"Score: {result['@search.score']}")
        print(f"Id: {result['Id']}")
        print(f"Description: {result['Description']}")
    ```

    Output from the query should produce results similar to the following example.

    ```
    Score: 0.6130029
    Id: 4
    Description: The hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Palace is part of a lovingly restored 1800 palace.
    Score: 0.26286605
    Id: 1
    Description: The hotel is ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Time's Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.
    ```

    Since encrypted content is decrypted prior to data refresh or queries, you won't see visual evidence of encryption. To verify encryption is working, check the resource logs.

---

> [!Important]
> Encrypted content in Azure AI Search is configured to use a specific key with a specific *version*. If you change the key or version, the object must be updated to use it **before** you delete the previous one. Failing to do so renders the object unusable. You won't be able to decrypt the content if the key is lost.

## Step 5: Test encryption

To verify encryption is working, revoke the encryption key, query the index (it should be unusable), and then reinstate the encryption key.

Use the Azure portal for this task. Make sure you have a role assignment that grants read access to the key.

1. On the Azure Key Vault page, select **Objects** > **Keys**.

1. Select the key you created, and then select **Delete**.

1. On the Azure AI Search page, select **Search management** > **Indexes**.

1. Select your index and use Search Explorer to run a query. You should get an error.

1. Return to the Azure Key Vault **Objects** > **Keys** page.

1. Select **Manage deleted keys**.

1. Select your key, and then select **Recover**. 

1. Return to your index in Azure AI Search and rerun the query. You should see search results. If you don't see immediate results, wait a minute and try again.

## Set up a policy to enforce CMK compliance

Azure policies help to enforce organizational standards and to assess compliance at-scale. Azure AI Search has two optional built-in policies related to CMK. These policies apply to new and existing search services.

| Effect | Effect if enabled|
|--------|------------------|
| [**AuditIfNotExists**](/azure/governance/policy/concepts/effect-audit-if-not-exists) | Checks for policy compliance: do objects have a customer-managed key defined, and is the content encrypted. This effect applies to existing services with content. It's evaluated each time an object is created or updated, or [per the evaluation schedule](/azure/governance/policy/overview#understand-evaluation-outcomes). [Learn more...](https://portal.azure.com/#view/Microsoft_Azure_Policy/PolicyDetailBlade/definitionId/%2Fproviders%2FMicrosoft.Authorization%2FpolicyDefinitions%2F356da939-f20a-4bb9-86f8-5db445b0e354) |
| [**Deny**](/azure/governance/policy/concepts/effect-deny) | Checks for policy enforcement: does the search service have [SearchEncryptionWithCmk](/rest/api/searchmanagement/services/create-or-update?view=rest-searchmanagement-2025-05-01&tabs=HTTP&preserve-view=true#searchencryptionwithcmk) set to `Enabled`. This effect applies to new services only, which must be created with encryption enabled. Existing services remain operational but you can't update them unless you patch the service. None of the tools used for provisioning services expose this property, so be aware that setting the policy limits you to [programmatic set up](#enable-cmk-policy-enforcement).|

### Assign a policy

1. In the Azure portal, navigate to a built-in policy and then select **Assign**.

   + [AuditIfExists](https://portal.azure.com/#view/Microsoft_Azure_Policy/PolicyDetailBlade/definitionId/%2Fproviders%2FMicrosoft.Authorization%2FpolicyDefinitions%2F76a56461-9dc0-40f0-82f5-2453283afa2f)

   + [Deny](https://portal.azure.com/#view/Microsoft_Azure_Policy/PolicyDetailBlade/definitionId/%2Fproviders%2FMicrosoft.Authorization%2FpolicyDefinitions%2F356da939-f20a-4bb9-86f8-5db445b0e354)

   Here's an example of the **AuditIfExists** policy in the Azure portal:

   :::image type="content" source="media/search-security-manage-encryption-keys/assign-policy.png" alt-text="Screenshot of assigning built-in CMK policy." border="true":::

1. Set [policy scope](/azure/governance/policy/concepts/scope) by selecting the subscription and resource group. Exclude any search services for which the policy shouldn't apply.

1. Accept or modify the defaults. Select **Review +create**, followed by **Create**.

### Enable CMK policy enforcement

A policy that's assigned to a resource group in your subscription is effective immediately. Audit policies flag non-compliant resources, but Deny policies prevent the creation and update of non-compliant search services. This section explains how to create a compliant search service or update a service to make it compliant. To bring objects into compliance, start at [step one](#step-1-create-an-encryption-key) of this article.

#### Create a compliant search service

For new search services, create them with [SearchEncryptionWithCmk](/rest/api/searchmanagement/services/create-or-update?view=rest-searchmanagement-2025-05-01&tabs=HTTP&preserve-view=true#searchencryptionwithcmk) set to `Enabled`.

Neither the Azure portal nor the command line tools (the Azure CLI and Azure PowerShell) provide this property natively, but you can use [Management REST API](/rest/api/searchmanagement/services/create-or-update) to provision a search service with a CMK policy definition.

### [**Management REST API**](#tab/mgmt-rest-create)

This example is from [Manage your Azure AI Search service with REST APIs](search-manage-rest.md), modified to include the [SearchEncryptionWithCmk](/rest/api/searchmanagement/services/create-or-update?view=rest-searchmanagement-2025-05-01&tabs=HTTP&preserve-view=true#searchencryptionwithcmk) property.

```rest
### Create a search service (provide an existing resource group)
@resource-group = my-rg
@search-service-name = my-search
PUT https://management.azure.com/subscriptions/{{subscriptionId}}/resourceGroups/{{resource-group}}/providers/Microsoft.Search/searchServices/{{search-service-name}}?api-version=2025-05-01 HTTP/1.1
     Content-type: application/json
     Authorization: Bearer {{token}}

    {
        "location": "North Central US",
        "sku": {
            "name": "basic"
        },
        "properties": {
            "replicaCount": 1,
            "partitionCount": 1,
            "hostingMode": "default",
            "encryptionWithCmk": {
                "enforcement": "Enabled"
        }
      }
    }
```
<!-- 
### [**Azure CLI**](#tab/azure-cli-create)

These instructions assume you have a Deny policy defined for the resource group into which you're deploying a new search service.

Run the following [`az resource`](/cli/azure/resource) command to create a new search service with CMK enforcement enabled. Substitute valid values for the name of the new search service and name of the existing resource group. The command includes eastus for a region so that you can see how regions are specified (lower case, no spaces).

```azurecli
az resource create --name SEARCH-SERVICE-PLACEHOLDER --location eastus --resource-group RESOURCE-GROUP-PLACEHOLDER --resource-type searchServices --namespace Microsoft.Search --set properties.encryptionWithCmk.enforcement=Enabled
``` -->

---

#### Update an existing search service

For existing search services that are now non-compliant, patch them using [Services - Update API](/rest/api/searchmanagement/services/update) or the Azure CLI [az resource update](/cli/azure/resource?view=azure-cli-latest#az-resource-update&preserve-view=true) command. Patching the services restores the ability to update search service properties.

### [**Management REST API**](#tab/mgmt-rest-update)

```http
PATCH https://management.azure.com/subscriptions/<your-subscription-Id>/resourceGroups/<your-resource-group-name>/providers/Microsoft.Search/searchServices/<your-search-service-name>?api-version=2025-05-01

{
  "properties": {
      "encryptionWithCmk": {
          "enforcement": "Enabled"
      }
  }
}
```

### [**Azure CLI**](#tab/azure-cli-update)

Run the following command, substituting valid values for the search service and resource group.

```azurecli
az resource update --name SEARCH-SERVICE-PLACEHOLDER --resource-group RESOURCE-GROUP-PLACEHOLDER --resource-type searchServices --namespace Microsoft.Search --set properties.encryptionWithCmk.enforcement=Enabled
```

The response should include the following statement:

```bash
"encryptionWithCmk": {
      "encryptionComplianceStatus": "NonCompliant",
      "enforcement": "Enabled"
    }
...
```

"Non-compliant" means the search service has existing objects that aren't CMK encrypted. To achieve compliance, recreate each object, specifying an encryption key.

---

## Rotate or update encryption keys

Use the following instructions to rotate keys or to migrate from Azure Key Vault to the Hardware Security Model (HSM). 

For key rotation, we recommend using the [autorotation capabilities of Azure Key Vault](/azure/key-vault/keys/how-to-configure-key-rotation). If you use autorotation, omit the key version in object definitions. The latest key is used, rather than a specific version.

When you change a key or its version, any object that uses the key must first be updated to use the new values **before** you delete the old values. Otherwise, the object becomes unusable because it can't be decrypted. 

Recall that keys are cached for 60 minutes. Remember this when testing and rotating keys.

1. [Determine the key used by an index or synonym map](search-security-get-encryption-keys.md).

1. [Create a new key in key vault](/azure/key-vault/keys/quick-create-portal), but leave the original key available. In this step, you can switch from key vault to HSM.

1. [Update the encryptionKey properties](/rest/api/searchservice/indexes/create-or-update) on an index or synonym map to use the new values. Only objects that were originally created with this property can be updated to use a different value.

1. Disable or delete the previous key in the key vault. Monitor key access to verify the new key is being used.

For performance reasons, the search service caches the key for up to several hours. If you disable or delete the key without providing a new one, queries continue to work on a temporary basis until the cache expires. However, once the search service can no longer decrypt content, you get this message: `"Access forbidden. The query key used might have been revoked - please retry."` 

## Key Vault tips

+ If you're new to Azure Key Vault, review this quickstart to learn about basic tasks: [Set and retrieve a secret from Azure Key Vault using PowerShell](/azure/key-vault/secrets/quick-create-powershell). 

+ Use as many key vaults as you need. Managed keys can be in different key vaults. A search service can have multiple encrypted objects, each one encrypted with a different customer-managed encryption key, stored in different key vaults.

+ Use the same [Azure tenant](/entra/fundamentals/create-new-tenant) so that you can retrieve your managed key through role assignments and by connecting through a system or user-managed identity. For more information about creating a tenant, see [Set up a new tenant](/azure/active-directory/develop/quickstart-create-new-tenant).

+ [Enable purge protection](/azure/key-vault/general/soft-delete-overview#purge-protection) and [soft-delete](/azure/key-vault/general/soft-delete-overview) on a key vault. Due to the nature of encryption with customer-managed keys, no one can retrieve your data if your Azure Key Vault key is deleted. To prevent data loss caused by accidental Key Vault key deletions, soft-delete and purge protection must be enabled on the key vault. Soft-delete is enabled by default, so you'll only encounter issues if you purposely disable it. Purge protection isn't enabled by default, but it's required for CMK encryption in Azure AI Search.

+ [Enable logging](/azure/key-vault/general/logging) on the key vault so that you can monitor key usage.

+ [Enable autorotation of keys](/azure/key-vault/keys/how-to-configure-key-rotation) or follow strict procedures during routine rotation of key vault keys and application secrets and registration. Always update all [encrypted content](search-security-get-encryption-keys.md) to use new secrets and keys before deleting the old ones. If you miss this step, your content can't be decrypted.

## Work with encrypted content

With CMK encryption, you might notice latency for both indexing and queries due to the extra encrypt/decrypt work. Azure AI Search doesn't log encryption activity, but you can monitor key access through key vault logging.

We recommend that you [enable logging](/azure/key-vault/general/logging) as part of key vault configuration.

1. [Create a log analytics workspace](/azure/azure-monitor/logs/quick-create-workspace).

1. [Add a diagnostic setting in key vault](/azure/key-vault/general/howto-logging) that uses the workspace for data retention.

1. Select **audit** or **allLogs** for the category, give the diagnostic setting a name, and then save it.

## Next steps

If you're unfamiliar with Azure security architecture, review the [Azure Security documentation](/azure/security/), and in particular, this article:

> [!div class="nextstepaction"]
> [Data encryption-at-rest](/azure/security/fundamentals/encryption-atrest)
