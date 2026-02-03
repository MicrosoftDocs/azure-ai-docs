---
title: Connect Using API keys
titleSuffix: Azure AI Search
description: Learn how to use an admin or query API key for inbound access to an Azure AI Search service endpoint.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ai-usage: ai-assisted
ms.custom:
  - ignite-2023
  - dev-focus
ms.topic: how-to
ms.date: 01/20/2026
ms.update-cycle: 365-days
---

# Connect to Azure AI Search using keys

Azure AI Search supports both identity-based and key-based authentication (default) for connections to your search service.

A request made to a search service endpoint is accepted if both the request and the API key are valid and if the search service is configured to allow API keys on a request.

> [!IMPORTANT]
> When you create a search service, key-based authentication is the default, but it's not the most secure option. We recommend that you replace it with  [role-based access](search-security-enable-roles.md).

## Prerequisites

You must be an Owner, Contributor, or [Search Service Contributor](/azure/role-based-access-control/built-in-roles#search-service-contributor) to view or manage keys.

## Enabled by default

In the Azure portal, authentication is specified on the **Settings** > **Keys** page. Options set to either **API keys** (default) or **Both** allow API keys on a request.

:::image type="content" source="media/search-security-overview/api-keys-enabled.png" alt-text="Screenshot of the Keys page in the Azure portal.":::

## Types of keys

An API key is a unique string composed of 52 randomly generated numbers and letters. Visually, there's no distinction between an admin key or query key. If you lose track of what type of key is specified in your application, you can [check the key values in the Azure portal](#find-existing-keys).

There are two kinds of keys used for authenticating a request:

| Type | Permission level | How it's created | Maximum |
| ------ | ------------------ | --------- | --------- |
| Admin | Full access (read-write) for all data plane (content) operations | Two admin keys, *primary* and *secondary*, are generated when the service is created and can be individually regenerated on demand. Having two allows you to roll over one key while using the second key for continued access to the service. | 2 |
| Query | Read-only access, scoped to the documents collection of a search index | One query key is generated with the service. More can be created on demand by a search service administrator. | 50 |

## Find existing keys

You can view and manage API keys using the [Azure portal](https://portal.azure.com), [PowerShell](/powershell/module/az.search), [Azure CLI](/cli/azure/search), or [REST API](/rest/api/searchmanagement/).

### [**Portal**](#tab/portal-find)

1. Sign in to the [Azure portal](https://portal.azure.com) and [find your search service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices).

1. From the left pane, select **Settings** > **Keys** to view admin and query keys.

    :::image type="content" source="media/search-manage/azure-search-view-keys.png" alt-text="Screenshot of a portal page showing API keys." border="true":::

### [**REST API**](#tab/rest-find)

Run the following commands to return admin and query API keys, respectively. For help with REST, see [Manage your Azure AI Search service with REST APIs](search-manage-rest.md).

1. Return admin keys:

    ```rest
    POST https://management.azure.com/subscriptions/{{subscriptionId}}/resourceGroups/{{resource-group}}/providers//Microsoft.Search/searchServices/{{search-service-name}}/listAdminKeys?api-version=2025-05-01
    ```

1. Return query keys:

    ```rest
    POST https://management.azure.com/subscriptions/{{subscriptionId}}/resourceGroups/{{resource-group}}/providers//Microsoft.Search/searchServices/{{search-service-name}}/listAdminKeys?api-version=2025-05-01
    ```

**Reference:** [Admin Keys - Get](/rest/api/searchmanagement/admin-keys/get), [Query Keys - List By Search Service](/rest/api/searchmanagement/query-keys/list-by-search-service)

### [**Python**](#tab/python-find)

Use the Azure SDK for Python to retrieve API keys programmatically. Install the management SDK:

```bash
pip install azure-mgmt-search azure-identity
```

Run the following code to return admin and query API keys:

```python
import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.search import SearchManagementClient

# Set up variables
subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
resource_group = "your-resource-group"
search_service_name = "your-search-service"

# Create the management client
credential = DefaultAzureCredential()
client = SearchManagementClient(credential, subscription_id)

# Get admin keys
admin_keys = client.admin_keys.get(resource_group, search_service_name)
print(f"Primary admin key: {admin_keys.primary_key}")
print(f"Secondary admin key: {admin_keys.secondary_key}")

# Get query keys
query_keys = client.query_keys.list_by_search_service(resource_group, search_service_name)
for key in query_keys:
    print(f"Query key '{key.name}': {key.key}")
```

**Reference:** [SearchManagementClient](/python/api/azure-mgmt-search/azure.mgmt.search.searchmanagementclient) | [AdminKeys](/python/api/azure-mgmt-search/azure.mgmt.search.operations.adminkeysoperations) | [QueryKeys](/python/api/azure-mgmt-search/azure.mgmt.search.operations.querykeysoperations)

### [**PowerShell**](#tab/azure-ps-find)

Run the following commands to return admin and query API keys, respectively. For help with PowerShell, see [Manage your Azure AI Search service using PowerShell](search-manage-powershell.md).

1. Install the `Az.Search` module:

   ```azurepowershell
   Install-Module Az.Search
   ```

1. Return admin keys:

   ```azurepowershell
   Get-AzSearchAdminKeyPair -ResourceGroupName <resource-group-name> -ServiceName <search-service-name>
   ```

1. Return query keys:

   ```azurepowershell
   Get-AzSearchQueryKey -ResourceGroupName <resource-group-name> -ServiceName <search-service-name>
   ```


### [**Azure CLI**](#tab/azure-cli-find)

Run the following commands to return admin and query API keys, respectively. For help with the Azure CLI, see [Manage your Azure AI Search service using the Azure CLI](search-manage-azure-cli.md).

1. Return admin keys:

    ```azurecli
    az search admin-key show --resource-group <myresourcegroup> --service-name <myservice>
    ```

1. Return query keys:

    ```azurecli
    az search query-key list --resource-group <myresourcegroup> --service-name <myservice>
    ```
---

## Use keys on connections

Key-based authentication is used only for data plane (content) requests, such as creating or querying index and any other action that's performed using the [Search Service REST API](/rest/api/searchservice/operation-groups).

In your source code, you can directly specify the API key in a request header. Alternatively, you can store it as an [environment variable](/azure/ai-services/cognitive-services-environment-variables) or app setting in your project and then reference the variable in the request.

- Admin keys are used for creating, modifying, or deleting objects. 
- Admin keys are also used to GET object definitions and system information, such as [LIST Indexes](/rest/api/searchservice/indexes/list) or [GET Service Statistics](/rest/api/searchservice/get-service-statistics/get-service-statistics).
- Query keys are typically distributed to client applications that issue queries.

### [**Portal**](#tab/portal-use)

Recall that key authentication is enabled by default and supports data plane operations such as indexing and queries.

However, if you [disable API keys](search-security-enable-roles.md#disable-api-key-authentication) and set up role assignments, the Azure portal uses role assignments instead.

### [**REST API**](#tab/rest-use)

Set an admin key in the request header. You can't pass admin keys on the URI or in the body of the request.

Here's an example of admin API key usage on a create index request:

```http
@baseUrl=https://my-demo-search-service.search.windows.net
@adminApiKey=aaaabbbb-0000-cccc-1111-dddd2222eeee

### Create an index
POST {{baseUrl}}/indexes?api-version=2025-09-01  HTTP/1.1
  Content-Type: application/json
  api-key: {{adminApiKey}}

    {
        "name": "my-new-index",  
        "fields": [
            {"name": "docId", "type": "Edm.String", "key": true, "filterable": true},
            {"name": "Name", "type": "Edm.String", "searchable": true }
         ]
   }
```

Set a query key in a request header for POST, or on the URI for GET. Query keys are used for operations that target the `index/docs` collection: [Search Documents](/rest/api/searchservice/documents/search-get), [Autocomplete](/rest/api/searchservice/documents/autocomplete-get), [Suggest](/rest/api/searchservice/documents/suggest-get), or [GET Document](/rest/api/searchservice/documents/get).

Here's an example of query API key usage on a Search Documents (GET) request:

```http
### Query an index
GET /indexes/my-new-index/docs?search=*&api-version=2025-09-01&api-key={{queryApiKey}}
```

> [!NOTE]  
> It's considered a poor security practice to pass sensitive data such as an `api-key` in the request URI. For this reason, Azure AI Search only accepts a query key as an `api-key` in the query string. As a general rule, we recommend passing your `api-key` as a request header.

### [**Python**](#tab/python-use)

It's a best practice to set the API key as an environment variable, but for simplicity, this example shows it as a string. The example uses a query API key for a query operation.

```python
# Import libraries
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential, AzureAuthorityHosts

# Variables for endpoint, keys, index
search_endpoint: str = "https://<Put your search service NAME here>.search.windows.net/"
credential = AzureKeyCredential("Your search service query key")
index_name: str = "hotels-quickstart-python"

# Set up the client
search_client = SearchClient(endpoint=search_endpoint,
                      index_name=index_name,
                      credential=credential)

# Run the query
results =  search_client.search(query_type='simple',
    search_text="*" ,
    select='HotelName,Description,Tags',
    include_total_count=True)

print ('Total Documents Matching Query:', results.get_count())
for result in results:
    print(result["@search.score"])
    print(result["HotelName"])
    print(result["Tags"])
    print(f"Description: {result['Description']}")
```

### [**PowerShell**](#tab/azure-ps-use)

Set API keys in the request header using the following syntax:

```powershell
$headers = @{
'api-key' = '<YOUR-ADMIN-OR-QUERY-API-KEY>'
'Content-Type' = 'application/json' 
'Accept' = 'application/json' }
```

Use a variable to contain the fully qualified query:

```powershell
$url = '<YOUR-SEARCH-SERVICE>/indexes/hotels-quickstart/docs?api-version=2025-09-01&search=attached restaurant&searchFields=Description,Tags&$select=HotelId,HotelName,Tags,Description&$count=true'
```

Send the request to the search service:

```powershell
Invoke-RestMethod -Uri $url -Headers $headers | ConvertTo-Json
```

More script examples for other operations can be found at [Quickstart: Create an Azure AI Search index in PowerShell using REST APIs](search-get-started-text.md).

---

## Create query keys

Query keys are used for read-only access to documents within an index for operations targeting a documents collection. Search, filter, and suggestion queries are all operations that take a query key. Any read-only operation that returns system data or object definitions, such as an index definition or indexer status, requires an admin key.

Restricting access and operations in client apps is essential to safeguarding the search assets on your service. Always use a query key rather than an admin key for any query originating from a client app.

### [**Portal**](#tab/portal-query)

1. Sign in to the [Azure portal](https://portal.azure.com) and [find your search service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices).

1. From the left pane, select **Settings** > **Keys** to view API keys.

1. Under **Manage query keys**, use the query key already generated for your service, or create new query keys. The default query key isn't named, but other generated query keys can be named for manageability.

   :::image type="content" source="media/search-security-overview/create-query-key.png" alt-text="Screenshot of the query key management options." border="true":::

### [**REST API**](#tab/rest-query)

Use [Create Query Keys](/rest/api/searchmanagement/query-keys/create) in the Management REST API.

You must have a valid role assignment to create or manage API keys. See [Manage your Azure AI Search service with REST APIs](search-manage-rest.md) for guidance on meeting role requirements using the REST APIs.

```rest
POST https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Search/searchServices/{searchServiceName}/createQueryKey/{name}?api-version=2025-05-01
```

### [**PowerShell**](#tab/azure-ps-query)

A script example showing API key usage can be found at [Create or delete query keys](search-manage-powershell.md#create-or-delete-query-keys).

### [**Azure CLI**](#tab/azure-cli-query)

A script example showing query key usage can be found at [Create or delete query keys](search-manage-azure-cli.md#create-or-delete-query-keys).

---

<a name="regenerate-admin-keys"></a>

## Regenerate admin keys

Two admin keys are created for each service so that you can rotate a primary key while using the secondary key for business continuity.

1. Sign in to the [Azure portal](https://portal.azure.com) and [find your search service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices).

1. From the left pane, select **Settings** > **Keys**.

1. Copy the secondary key.

1. For all applications, update the API key settings to use the secondary key.

1. Regenerate the primary key.

1. Update all applications to use the new primary key.

If you inadvertently regenerate both keys at the same time, all client requests using those keys will fail with HTTP 403 Forbidden. However, content isn't deleted and you aren't locked out permanently.

You can still access the service through the Azure portal or programmatically. Management functions are operative through a subscription ID not a service API key, and are thus still available even if your API keys aren't.

After you create new keys via portal or management layer, access is restored to your content (indexes, indexers, data sources, synonym maps) once you provide those keys on requests.

## Migrate from keys to roles

If you want to transition to role-based access, it's helpful to understand how keys map to [built-in roles in Azure AI Search](search-security-rbac.md#built-in-roles-used-in-search):

+ An admin key corresponds to the **Search Service Contributor** and **Search Index Data Contributor** roles.
+ A query key corresponds to the **Search Index Data Reader** role.

## Secure keys

Use role assignments to restrict access to API keys.

It's not possible to use [customer-managed key encryption](search-security-manage-encryption-keys.md) to encrypt API keys. Only sensitive data within the search service itself (for example, index content or connection strings in data source object definitions) can be CMK-encrypted.

1. Sign in to the [Azure portal](https://portal.azure.com) and [find your search service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices).

1. From the left pane, select **Access control (IAM)**, and then select the **Role assignments** tab.

1. In the **Role** filter, select the roles that have permission to view or manage keys (Owner, Contributor, Search Service Contributor). The resulting security principals assigned to those roles have key permissions on your search service.

1. As a precaution, also check the **Classic administrators** tab to determine whether administrators and co-administrators have access.

## Best practices

+ For production workloads, switch to [Microsoft Entra ID and role-based access](search-security-rbac-client-code.md). Alternatively, if you want to continue using API keys, be sure to always monitor [who has access to your API keys](#secure-keys) and [regenerate API keys](#regenerate-admin-keys) on a regular cadence.

+ Only use API keys if data disclosure isn't a risk (for example, when using sample data) and if you're operating behind a firewall. Exposing API keys puts both your data and your search service at risk of unauthorized use.

+ If you use an API key, store it securely somewhere else, such as in [Azure Key Vault](/azure/key-vault/general/overview). Don't include the API key directly in your code, and never post it publicly.

+ Always check code, samples, and training material before publishing to make sure you don't inadvertently expose an API key.

## Related content

+ [Security in Azure AI Search](search-security-overview.md)
+ [Azure role-based access control in Azure AI Search](search-security-rbac.md)
+ [Manage using PowerShell](search-manage-powershell.md)
