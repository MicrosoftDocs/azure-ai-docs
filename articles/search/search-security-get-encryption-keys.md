---
title: Find encryption key information
titleSuffix: Azure AI Search
description: Retrieve the encryption key name and version used in an index or synonym map so that you can manage the key in Azure Key Vault.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: conceptual
ms.date: 10/30/2024
---

# Find encrypted objects and information

In Azure AI Search, customer-managed encryption keys are created, stored, and managed in Azure Key Vault. If you need to determine whether an object is encrypted, or what key name or version is used in Azure Key Vault, use the REST API or an Azure SDK to retrieve the **encryptionKey** property from the object definition in your search service.

Objects that aren't encrypted with a customer-managed key have an empty **encryptionKey** property. Otherwise, you might see a definition similar to the following example.

```json
"encryptionKey":{
   "keyVaultUri":"https://demokeyvault.vault.azure.net",
   "keyVaultKeyName":"myEncryptionKey",
   "keyVaultKeyVersion":"eaab6a663d59439ebb95ce2fe7d5f660",
   "accessCredentials":{
      "applicationId":"00001111-aaaa-2222-bbbb-3333cccc4444",
      "applicationSecret":"myApplicationSecret"
   }
}
```

The **encryptionKey** construct is the same for all encrypted objects. It's a first-level property, on the same level as the object name and description.

## Permissions for retrieving object definitions

You must have [Search Service Contributor](search-security-rbac.md#built-in-roles-used-in-search) or equivalent permissions. To use [key-based authentication](search-security-api-keys.md) instead, provide an admin API key. Admin permissions are required on requests that return object definitions and metadata. The easiest way to get the admin API key is through the Azure portal.

1. Sign in to the [Azure portal](https://portal.azure.com/) and open the search service overview page.

1. On the left side, select **Keys** and copy an admin API. 

For the remaining steps, switch to PowerShell and the REST API. the Azure portal doesn't show encryption key information for any object.

## Retrieve object properties

Use PowerShell and REST to run the following commands to set up the variables and get object definitions. 

Alternatively, you can also use the Azure SDK for [.NET](/dotnet/api/azure.search.documents.indexes.searchindexclient.getindexes), [Python](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient), [JavaScript](/javascript/api/@azure/search-documents/searchindexclient), and [Java](/java/api/com.azure.search.documents.indexes.searchindexclient.getindex).

First, connect to your Azure account.

```powershell
Connect-AzAccount
```

If you have more than one active subscription in your tenant, specify the subscription containing your search service:

```powershell
 Set-AzContext -Subscription <your-subscription-ID>
```

Set up the headers used on each request in the current session. Provide the admin API key used for search service authentication.

```powershell
$headers = @{
'api-key' = '<YOUR-ADMIN-API-KEY>'
'Content-Type' = 'application/json'
'Accept' = 'application/json' }
```

To return a list of all search indexes, set the endpoint to the indexes collection.

```powershell
$uri= 'https://<YOUR-SEARCH-SERVICE>.search.windows.net/indexes?api-version=2024-07-01&$select=name'
Invoke-RestMethod -Uri $uri -Headers $headers | ConvertTo-Json
```

To return a specific index definition, provide its name in the path. The encryptionKey property is at the end.

```powershell
$uri= 'https://<YOUR-SEARCH-SERVICE>.search.windows.net/indexes/<YOUR-INDEX-NAME>?api-version=2024-07-01'
Invoke-RestMethod -Uri $uri -Headers $headers | ConvertTo-Json
```

To return synonym maps, set the endpoint to the synonyms collection and then send the request.

```powershell
$uri= 'https://<YOUR-SEARCH-SERVICE>.search.windows.net/synonyms?api-version=2024-07-01&$select=name'
Invoke-RestMethod -Uri $uri -Headers $headers | ConvertTo-Json
```

The following example returns a specific synonym map definition, including the encryptionKey property is towards the end of the definition.

```powershell
$uri= 'https://<YOUR-SEARCH-SERVICE>.search.windows.net/synonyms/<YOUR-SYNONYM-MAP-NAME>?api-version=2024-07-01'
Invoke-RestMethod -Uri $uri -Headers $headers | ConvertTo-Json
```

Use the same pattern to return the encryptionKey property for other top-level objects such as indexers, skillsets, data sources, and index aliases.

## Next steps

We recommend that you [enable logging](/azure/key-vault/general/logging) on Azure Key Vault so that you can monitor key usage.

For more information about using Azure Key or configuring customer managed encryption:

+ [Quickstart: Set and retrieve a secret from Azure Key Vault using PowerShell](/azure/key-vault/secrets/quick-create-powershell)

+ [Configure customer-managed keys for data encryption in Azure AI Search](search-security-manage-encryption-keys.md)
