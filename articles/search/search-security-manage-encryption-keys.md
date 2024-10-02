---
title:  Encrypt data using customer-managed keys
titleSuffix: Azure AI Search
description: Supplement server-side encryption in Azure AI Search using customer managed keys (CMK) or bring your own keys (BYOK) that you create and manage in Azure Key Vault.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: cognitive-search
ms.topic: how-to
ms.date: 10/02/2024
ms.custom:
  - references_regions
  - ignite-2023
---

# Configure customer-managed keys for data encryption in Azure AI Search

Azure AI Search automatically encrypts data at rest with [service-managed keys](/azure/security/fundamentals/encryption-atrest#azure-encryption-at-rest-components). If more protection is needed, you can supplement default encryption with another encryption layer using keys that you create and manage in Azure Key Vault. 

This article walks you through the steps of setting up customer-managed key (CMK) or "bring-your-own-key" (BYOK) encryption.

> [!NOTE]
> If an index is CMK encrypted, it is only accessible if the search service has access to the key. If access is revoked, the index is unusable and the service cannot be scaled until the index is deleted or access to the key is restored.

## CMK encrypted objects

CMK encryption is enacted on individual objects. If you require CMK across your search service, [set an enforcement policy](#set-up-a-policy-to-enforce-cmk-compliance).

CMK encryption becomes operational when an object is created. You can't encrypt objects that already exist. CMK encryption occurs whenever an object is saved to disk, either data at rest for long-term storage or temporary data for short-term storage. With CMK, the disk never sees unencrypted data.

Objects that can be encrypted include indexes, synonym lists, indexers, data sources, and skillsets. Encryption is computationally expensive to decrypt so only sensitive content is encrypted.

Encryption is performed over the following content:

+ All content within indexes and synonym lists.

+ Sensitive content in indexers, data sources, skillsets, and vectorizers. This content consists of only those fields that store connection strings, descriptions, identities, keys, and user inputs. For example, skillsets have Azure AI services keys, and some skills accept user inputs, such as custom entities. In both cases, keys and user inputs into skills are encrypted. Any references to external resources (such as Azure data sources or Azure OpenAI models) are also encrypted.

## Full double encryption

When you introduce CMK encryption, you're encrypting content twice. For the objects and fields noted in the previous section, content is first encrypted with your CMK, and secondly with the Microsoft-managed key. Content is doubly encrypted on data disks for long-term storage, and on temporary disks used for short-term storage.

Enabling CMK encryption increases index size and degrades query performance. Based on observations to date, you can expect to see an increase of 30-60 percent in query times, although actual performance varies depending on the index definition and types of queries. Because performance is diminished, we recommend that you only enable this feature on objects that really require it.

Although double encryption is now available in all regions, support was rolled out in two phases:

+ The first rollout was on August 1, 2020 and included the five regions listed below. Search services created in the following regions supported CMK for data disks, but not temporary disks:

  + West US 2
  + East US
  + South Central US
  + US Gov Virginia
  + US Gov Arizona

+ The second rollout on May 13, 2021 added encryption for temporary disks and extended CMK encryption to [all supported regions](search-region-support.md).

  If you're using CMK from a service created during the first rollout and you also want CMK encryption over temporary disks, you need to create a new search service in your region of choice and redeploy your content. To determine your service creation date, see [How to check service creation date](vector-search-index-size.md#how-to-check-service-creation-date).

## Prerequisites

+ [Azure AI Search](search-create-service-portal.md) on a [billable tier](search-sku-tier.md#tier-descriptions) (Basic or above, in any region).

+ [Azure Key Vault](/azure/key-vault/general/overview) in the same subscription as Azure AI Search. You can [create a key vault using the Azure portal](/azure/key-vault/general/quick-create-portal), [Azure CLI](/azure/key-vault/general/quick-create-cli), or [Azure PowerShell](/azure/key-vault/general/quick-create-powershell). The key vault must have **soft-delete** and **purge protection** enabled. 

+ A search client that can create an encrypted object, such as a [REST client](search-get-started-rest.md), [Azure PowerShell](search-get-started-powershell.md), or an Azure SDK (Python, .NET, Java, JavaScript). 

## Limitations

+ No support for Azure Key Vault Managed Hardware Security Model (HSM).

+ No support for adding encryption keys in the Azure portal.

+ No cross-subscription support. Azure Key Vault and Azure AI Search must be in the same subscription.

## Key Vault tips

If you're new to Azure Key Vault, review this quickstart to learn about basic tasks: [Set and retrieve a secret from Azure Key Vault using PowerShell](/azure/key-vault/secrets/quick-create-powershell). 

Here are some tips for using Key Vault:

+ Use as many key vaults as you need. Managed keys can be in different key vaults. A search service can have multiple encrypted objects, each one encrypted with a different customer-managed encryption key, stored in different key vaults.

+ Use the same tenant so that you can retrieve your managed key by connecting through a system or user-managed identity. This behavior requires both services to share the same tenant. For more information about creating a tenant, see [Set up a new tenant](/azure/active-directory/develop/quickstart-create-new-tenant).

+ [Enable purge protection](/azure/key-vault/general/soft-delete-overview#purge-protection) and [soft-delete](/azure/key-vault/general/soft-delete-overview). Due to the nature of encryption with customer-managed keys, no one can retrieve your data if your Azure Key Vault key is deleted. To prevent data loss caused by accidental Key Vault key deletions, soft-delete and purge protection must be enabled on the key vault. Soft-delete is enabled by default, so you'll only encounter issues if you purposely disable it. Purge protection isn't enabled by default, but it's required for customer-managed key encryption in Azure AI Search.

+ [Enable logging](/azure/key-vault/general/logging) on the key vault so that you can monitor key usage.

+ [Enable autorotation of keys](/azure/key-vault/keys/how-to-configure-key-rotation) or follow strict procedures during routine rotation of key vault keys and application secrets and registration. Always update all [encrypted content](search-security-get-encryption-keys.md) to use new secrets and keys before deleting the old ones. If you miss this step, your content can't be decrypted.

## Step 1: Create a key in Key Vault

Skip key generation if you already have a key in Azure Key Vault that you want to use, but collect the key identifier. You need this information when creating an encrypted object.

Before you add the key, make sure that you have assigned to yourself the **Key Vault Crypto Officer** role.

Azure AI Search encryption supports RSA keys of sizes 2048, 3072 and 4096. For more information about supported key types, see [About keys](/azure/key-vault/keys/about-keys).

1. Sign in to the [Azure portal](https://portal.azure.com) and open your key vault overview page.

1. Select **Objects** > **Keys** on the left, and then select **Generate/Import**.

1. In the **Create a key** pane, from the list of **Options**, choose **Generate** to create a new key.

1. Enter a **Name** for your key, and accept the defaults for other key properties.

1. Optionally, set a key rotation policy to [enable auto rotation](/azure/key-vault/keys/how-to-configure-key-rotation).

1. Select **Create** to start the deployment.

1. Select the key, select the current version, and then make a note of the key identifier. It's composed of the **key value Uri**, the **key name**, and the **key version**. You need the identifier to define an encrypted index in Azure AI Search.

   :::image type="content" source="media/search-manage-encryption-keys/cmk-key-identifier.png" alt-text="Create a new key vault key" border="true":::

## Step 2: Create a security principal

You have several options for setting up Azure AI Search access to the encryption key at run time. The simplest approach is to retrieve the key using the managed identity of your search service. You can use either a system or user-managed identity. Doing so allows you to omit the steps for application registration and application secrets. Alternatively, you can create and register a Microsoft Entra application and have the search service provides the application ID on requests.

We recommend using a managed identity. A managed identity enables your search service to authenticate to Azure Key Vault without storing credentials (ApplicationID or ApplicationSecret) in code. The lifecycle of this type of managed identity is tied to the lifecycle of your search service, which can only have one system assigned managed identity. For more information about how managed identities work, see [What are managed identities for Azure resources](/azure/active-directory/managed-identities-azure-resources/overview).

### [**System-managed identity**](#tab/managed-id-sys)

Enable the system assigned managed identity for your search service.

![Turn on system assigned managed identity](./media/search-managed-identities/turn-on-system-assigned-identity.png "Turn on system assigned managed identity")

### [**User-managed identity (preview)**](#tab/managed-id-user)

> [!IMPORTANT] 
> User-managed identity support for CMK is in public preview under [supplemental terms of use](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
> 
> 2021-04-01-Preview of the [Management REST API](/rest/api/searchmanagement/) introduced this feature.

1. Sign in to the [Azure portal](https://portal.azure.com).

1. Select **Create a new resource**.

1. In the "Search services and marketplace" search bar, search for "User Assigned Managed Identity" and then select **Create**.

1. Give the identity a descriptive name.

1. Next, assign the user-managed identity to the search service. This can be done using the latest preview [2024-06-01-preview](/rest/api/searchmanagement/management-api-versions) management API or the previous preview.

    The identity property takes a type and one or more fully qualified user-assigned identities:
  
    * **type** is the type of identity used for the resource. The type 'SystemAssigned, UserAssigned' includes both an identity created by the system and a set of user assigned identities. The type 'None' removes all identities from the service.
    * **userAssignedIdentities** includes the details of the user-managed identity.
        * User-managed identity format: 
            * /subscriptions/**subscription ID**/resourcegroups/**resource group name**/providers/Microsoft.ManagedIdentity/userAssignedIdentities/**managed identity name**
  
    Example of how to assign a user-managed identity to a search service:
  
    ```http
    PUT https://management.azure.com/subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Search/searchServices/[search service name]?api-version=2024-06-01-preview
    Content-Type: application/json

    {
      "location": "<your-region>",
      "sku": {
        "name": "<your-sku>"
      },
      "properties": {
        "replicaCount": <your-replica-count>,
        "partitionCount": <your-partition count>,
        "hostingMode": "default"
      },
      "identity": {
        "type": "UserAssigned",
        "userAssignedIdentities": {
          "/subscriptions/<your-subscription-ID>/resourcegroups/<your-resource-group-name>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<your-managed-identity-name>": {}
        }
      }
    } 
    ```

1. Update the `"encryptionKey"` section to use an identity property. Make sure to use preview REST API version when sending this request to your search service.

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

### [**Register an app**](#tab/register-app)

1. In the [Azure portal](https://portal.azure.com), find the Microsoft Entra resource for your subscription.

1. On the left, under **Manage**, select **App registrations**, and then select **New registration**.

1. Give the registration a name, perhaps a name that is similar to the search application name. Select **Register**.

1. Once the app registration is created, copy the Application ID. You need to provide this string to your application. 

   If you're stepping through the [DotNetHowToEncryptionUsingCMK](https://github.com/Azure-Samples/search-dotnet-getting-started/tree/master/DotNetHowToEncryptionUsingCMK), paste this value into the **appsettings.json** file.

   :::image type="content" source="media/search-manage-encryption-keys/cmk-application-id.png" alt-text="Application ID in the Essentials section":::

1. Next, select **Certificates & secrets** on the left.

1. Select **New client secret**. Give the secret a display name and select **Add**.

1. Copy the application secret. If you're stepping through the sample, paste this value into the **appsettings.json** file.

   :::image type="content" source="media/search-manage-encryption-keys/cmk-application-secret.png" alt-text="Application secret":::

---

## Step 3: Grant permissions

Azure Key Vault supports authorization using role-based access controls. We recommend this approach over key vault access policies. For more information, see [Provide access to Key Vault keys, certificates, and secrets using Azure roles](/azure/key-vault/general/rbac-guide).

In this step, assign the **Key Vault Crypto Service Encryption User** role to your search service. If you're testing locally, assign this role to yourself as well.

1. Sign in to the [Azure portal](https://portal.azure.com) and find your key vault.

1. Select **Access control (IAM)** and select **Add role assignment**.

1. Select **Key Vault Crypto Service Encryption User** and then select **Next**.

1. Select managed identities, select members, and then select the managed identity of your search service.

1. Select **Review + Assign**.

Wait a few minutes for the role assignment to become operational.

## Step 4: Encrypt content

Encryption keys are added when you create an object. To add a customer-managed key on an index, synonym map, indexer, data source, or skillset, use the [Search REST API](/rest/api/searchservice/) or an Azure SDK to create an object that has encryption enabled. To add encryption using the Azure SDK, see the [Python example](#python-example-of-an-encryption-key-configuration) in this article.

1. Call the creation APIs to specify the **encryptionKey** property:

   + [Create Index](/rest/api/searchservice/indexes/create)
   + [Create Synonym Map](/rest/api/searchservice/synonym-maps/create)
   + [Create Indexer](/rest/api/searchservice/indexers/create)
   + [Create Data Source](/rest/api/searchservice/data-sources/create)
   + [Create Skillset](/rest/api/searchservice/skillsets/create)

1. Insert the encryptionKey construct into the object definition. This property is a first-level property, on the same level as name and description. If you're using the same vault, key, and version, you can paste in the same encryptionKey construct into each object definition.

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

1. Verify the object is operational by performing a task, such as query an index that's been encrypted.

Once you create the encrypted object on the search service, you can use it as you would any other object of its type. Encryption is transparent to the user and developer.

None of these key vault details are considered secret and could be easily retrieved by browsing to the relevant Azure Key Vault page in Azure portal.

> [!Important]
> Encrypted content in Azure AI Search is configured to use a specific Azure Key Vault key with a specific *version*. If you change the key or version, the object must be updated to use it **before** you delete the previous one. Failing to do so renders the object unusable. You won't be able to decrypt the content if the key is lost.

## Step 5: Test encryption

To verify encryption is working, revoke the encryption key, query the index (it should be unusable), and then reinstate the encryption key.

Use the Azure portal for this task.

1. On the Azure Key Vault page, select **Objects** > **Keys**.

1. Select the key you just created, and then select **Delete**.

1. On the Azure AI Search page, select **Search management** > **Indexes**.

1. Select your index and use Search Explorer to run a query. You should get an error.

1. Return to the Azure Key Vault **Objects** > **Keys** page.

1. Select **Manage deleted keys**.

1. Select your key, and then select **Recover**. 

1. Return to your index in Azure AI Search and rerun the query. You should see search results.

## Set up a policy to enforce CMK compliance

Azure policies help to enforce organizational standards and to assess compliance at-scale. Azure AI Search has an optional [built-in policy for service-wide CMK enforcement](https://portal.azure.com/#view/Microsoft_Azure_Policy/PolicyDetailBlade/definitionId/%2Fproviders%2FMicrosoft.Authorization%2FpolicyDefinitions%2F76a56461-9dc0-40f0-82f5-2453283afa2f).

In this section, you set the policy that defines a CMK standard for your search service. Then, you set up your search service to enforce this policy.

1. Navigate to the [built-in policy](https://portal.azure.com/#view/Microsoft_Azure_Policy/PolicyDetailBlade/definitionId/%2Fproviders%2FMicrosoft.Authorization%2FpolicyDefinitions%2F76a56461-9dc0-40f0-82f5-2453283afa2f) in your web browser. Select **Assign**

   :::image type="content" source="media/search-security-manage-encryption-keys/assign-policy.png" alt-text="Screenshot of assigning built-in CMK policy." border="true":::

1. Set up the [policy scope](/azure/governance/policy/concepts/scope). In the **Parameters** section, uncheck **Only show parameters...** and set **Effect** to [**Deny**](/azure/governance/policy/concepts/effects#deny). 

   During evaluation of the request, a request that matches a deny policy definition is marked as noncompliant. Assuming the standard for your service is CMK encryption, "deny" means that requests that *don't* specify CMK encryption are noncompliant.

   :::image type="content" source="media/search-security-manage-encryption-keys/effect-deny.png" alt-text="Screenshot of changing built-in CMK policy effect to deny." border="true":::

1. Finish creating the policy.

1. Call the [Services - Update API](/rest/api/searchmanagement/services/update) to enable CMK policy enforcement at the service level.

```http
PATCH https://management.azure.com/subscriptions/<your-subscription-Id>/resourceGroups/<your-resource-group-name>/providers/Microsoft.Search/searchServices/<your-search-service-name>?api-version=2023-11-01

{
    "properties": {
        "encryptionWithCmk": {
            "enforcement": "Enabled"
        }
    }
}
```

## Rotate or update encryption keys

We recommend using the [autorotation capabilities of Azure Key Vault](/azure/key-vault/keys/how-to-configure-key-rotation), but you can also rotate keys manually.

When you change a key or its version, any object that uses the key must first be updated to use the new key\version **before** deleting the previous key\version. Failing to do so will render the object unusable, as it won't be able to decrypt the content once key access is lost. Although restoring key vault access permissions at a later time will restore content access.

1. [Determine the key used by an index or synonym map](search-security-get-encryption-keys.md).

1. [Create a new key in key vault](/azure/key-vault/keys/quick-create-portal), but leave the original key available.

1. [Update the encryptionKey properties](/rest/api/searchservice/indexes/create-or-update) on an index or synonym map to use the new values. Only objects that were originally created with this property can be updated to use a different value.

1. Disable or delete the previous key in the key vault. Monitor key access to verify the new key is being used.

For performance reasons, the search service caches the key for up to several hours. If you disable or delete the key without providing a new one, queries continue to work on a temporary basis until the cache expires. However, once the search service can no longer decrypt content, you get this message: "Access forbidden. The query key used might have been revoked - please retry." 

## Work with encrypted content

With customer-managed key encryption, you might notice latency for both indexing and queries due to the extra encrypt/decrypt work. Azure AI Search doesn't log encryption activity, but you can monitor key access through key vault logging. 

We reommend that you [enable logging](/azure/key-vault/general/logging) as part of key vault configuration.

1. [Create a log analytics workspace](/azure/azure-monitor/logs/quick-create-workspace).

1. [Add a diagnostic setting in key vault](/azure/key-vault/general/howto-logging) that uses the workspace for data retention. 

1. Select **audit** or **allLogs** for the category, give the diagnostic setting a name, and then save it.

## Python example of an encryption key configuration

This section shows the Python representation of an `encryptionKey` in an object definition. The same definition applies to indexes, data sources, skillets, indexers, and synonym maps. To try this example on your search service and key vault, download the notebook from [azure-search-python-samples](https://github.com/Azure-Samples/azure-search-python-samples).

Install some packages.

```python
! pip install python-dotenv
! pip install azure-core
! pip install azure-search-documents==11.5.1
! pip install azure-identity
```

Create an index that has an encryption key.

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
    vault_uri="<PUT YOUR KEY VAULT ENDPOINT HERE>"
)

index = SearchIndex(name=index_name, fields=fields, encryption_key=encryption_key)
result = index_client.create_or_update_index(index)
print(f' {result.name} created')
```

Get the index definition to verify encryption key configuration exists.

```python
index_name = "test-cmk-index-qs"
index_client = SearchIndexClient(endpoint=AZURE_SEARCH_SERVICE, credential=credential)  

result = index_client.get_index(index_name)  
print(f"{result}")  
```

Load the index with a few documents. All field content is considered sensitive and is encrypted on disk using your customer managed key.

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
    "Description": "The hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Cliff is part of a lovingly restored 1800 palace."
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

Run a query to confirm the index is operational.

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
Description: The hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Cliff is part of a lovingly restored 1800 palace.
Score: 0.26286605
Id: 1
Description: The hotel is ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Time's Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.
```

Since encrypted content is decrypted prior to data refresh or queries, you won't see visual evidence of encryption. To verify encryption is working, check the resource logs.

## Next steps

If you're unfamiliar with Azure security architecture, review the [Azure Security documentation](/azure/security/), and in particular, this article:

> [!div class="nextstepaction"]
> [Data encryption-at-rest](/azure/security/fundamentals/encryption-atrest)
