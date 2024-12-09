---
title: Connect using Azure roles
titleSuffix: Azure AI Search
description: Use Azure role-based access control for granular permissions on service administration and content tasks.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 10/30/2024
ms.custom: subject-rbac-steps, devx-track-azurepowershell
---

# Connect to Azure AI Search using roles

Azure provides a global authentication and [role-based access control](/azure/role-based-access-control/role-assignments-portal) through Microsoft Entra ID for all services running on the platform. In this article, learn which roles provide access to search content and administration on Azure AI Search.

In Azure AI Search, you can assign Azure roles for:

+ [Service administration](#assign-roles-for-service-administration)
+ [Development or write-access to a search service](#assign-roles-for-development)
+ [Read-only access for queries](#assign-roles-for-read-only-queries)
+ [Scoped access to a single index](#grant-access-to-a-single-index)

Per-user access over search results (sometimes referred to as *row-level security* or *document-level security*) isn't supported through role assignments. As a workaround, [create security filters](search-security-trimming-for-azure-search.md) that trim results by user identity, removing documents for which the requestor shouldn't have access. See this [Enterprise chat sample using RAG](/azure/developer/python/get-started-app-chat-template) for a demonstration.

Role assignments are cumulative and pervasive across all tools and client libraries. You can assign roles using any of the [supported approaches](/azure/role-based-access-control/role-assignments-steps) described in Azure role-based access control documentation.

Role-based access is optional, but recommended. The alternative is [key-based authentication](search-security-api-keys.md), which is the default.

## Prerequisites

+ A search service in any region, on any tier, [enabled for role-based access](search-security-enable-roles.md).

+ Owner, User Access Administrator, Role-based Access Control Administrator, or a custom role with [Microsoft.Authorization/roleAssignments/write](/azure/templates/microsoft.authorization/roleassignments) permissions.

## How to assign roles in the Azure portal

The following steps work for all role assignments.

1. Sign in to the [Azure portal](https://portal.azure.com).

1. Navigate to your search service.

1. [Enable role-based access](search-security-enable-roles.md).

1. Select **Access Control (IAM)** in the left navigation pane.

1. Select **+ Add** > **Add role assignment** to start the **Add role assignment** wizard.

   :::image type="content" source="media/search-security-rbac/portal-access-control.png" alt-text="Screenshot of the access control page in the Azure portal.":::

1. Select a role. You can assign multiple security principals, whether users or managed identities to a role in one pass through the wizard, but you have to repeat these steps for each role you define.

1. On the **Members** tab, select the Microsoft Entra user or group identity. If you're setting up permissions for another Azure service, select a system or user-managed identity.

1. On the **Review + assign** tab, select **Review + assign** to assign the role.

## Built-in roles used in search

*Data plane* refers to operations against the search service endpoint, such as indexing or queries, or any other operation specified in the [Search Service REST APIs](/rest/api/searchservice/) or equivalent Azure SDK client libraries. 

*Control plane* refers to Azure resource management, such as creating or configuring a search service.

The following roles are built in. If these roles are insufficient, [create a custom role](#create-a-custom-role). 

| Role | Plane | Description  |
| ---- | ------|--------------------- |
| [Owner](/azure/role-based-access-control/built-in-roles#owner) | Control & Data | Full access to the control plane of the search resource, including the ability to assign Azure roles. Only the Owner role can enable or disable authentication options or manage roles for other users. Subscription administrators are members by default. </br></br>On the data plane, this role has the same access as the Search Service Contributor role. It includes access to all data plane actions except the ability to query or index documents.|
| [Contributor](/azure/role-based-access-control/built-in-roles#contributor) | Control & Data |  Same level of control plane access as Owner, minus the ability to assign roles or change authentication options. </br></br>On the data plane, this role has the same access as the Search Service Contributor role. It includes access to all data plane actions except the ability to query or index documents.|
| [Reader](/azure/role-based-access-control/built-in-roles#reader) | Control & Data | Read access across the entire service, including search metrics, content metrics (storage consumed, number of objects), and the object definitions of data plane resources (indexes, indexers, and so on). However, it can't read API keys or read content within indexes. |
| [Search Service Contributor](/azure/role-based-access-control/built-in-roles#search-service-contributor) | Control & Data | Read-write access to object definitions (indexes, aliases, synonym maps, indexers, data sources, and skillsets). This role is for developers who create objects, and for administrators who manage a search service and its objects, but without access to index content. Use this role to create, delete, and list indexes, get index definitions, get service information (statistics and quotas), test analyzers, create and manage synonym maps, indexers, data sources, and skillsets. See [`Microsoft.Search/searchServices/*`](/azure/role-based-access-control/resource-provider-operations#microsoftsearch) for the permissions list. |
| [Search Index Data Contributor](/azure/role-based-access-control/built-in-roles#search-index-data-contributor) | Data | Read-write access to content in indexes. This role is for developers or index owners who need to import, refresh, or query the documents collection of an index. This role doesn't support index creation or management. By default, this role is for all indexes on a search service. See [Grant access to a single index](#grant-access-to-a-single-index) to narrow the scope.  |
| [Search Index Data Reader](/azure/role-based-access-control/built-in-roles#search-index-data-reader) | Data |  Read-only access for querying search indexes. This role is for apps and users who run queries. This role doesn't support read access to object definitions. For example, you can't read a search index definition or get search service statistics. By default, this role is for all indexes on a search service. See [Grant access to a single index](#grant-access-to-a-single-index) to narrow the scope.  |

Combine these roles to get sufficient permissions for your use case.

> [!NOTE]
> If you disable Azure role-based access, built-in roles for the control plane (Owner, Contributor, Reader) continue to be available. Disabling role-based access removes just the data-related permissions associated with those roles. If data plane roles are disabled, Search Service Contributor is equivalent to control-plane Contributor.

## Summary

| Permissions | Search Index Data Reader | Search Index Data Contributor | Search Service Contributor | Owner/Contributor | Reader |
|-------------|--------------------------|-------------------------------|----------------------------|-------------------|--------|
|View the resource in Azure portal |❌|❌|✅|✅|✅|
|View resource properties/metrics/endpoint |❌|❌|✅|✅|✅|
|List all objects on the resource |❌|❌|✅|✅|✅|
|Access quotas and service statistics |❌|❌|✅|✅|❌|
|Read/query an index |✅|❌|❌|❌|❌|
|Upload data for indexing |❌|✅|❌|❌|❌|
|Create or edit indexes/aliases |❌|❌|✅|✅|❌|
|Create, edit and run indexers/data sources/skillsets |❌|❌|✅|✅|❌|
|Create or edit synonym maps |❌|❌|✅|✅|❌|
|Create or edit debug sessions |❌|❌|✅|✅|❌|
|Create or manage deployments |❌|❌|✅|✅|❌|
|Create or configure Azure AI Search resources |❌|❌|✅|✅|❌|
|View/Copy/Regenerate keys under Keys |❌|❌|✅|✅|❌|
|View roles/policies/definitions |❌|❌|✅|✅|❌|
|Set authentication options |❌|❌|✅|✅|❌|
|Configure private connections |❌|❌|✅|✅|❌|
|Configure network security |❌|❌|✅|✅|❌|

Owners and Contributors grant the same permissions, except that only Owners can assign roles.

Owners and Contributors can create, read, update, and delete objects in the Azure portal *if API keys are enabled*. the Azure portal uses keys on internal calls to data plane APIs. In you subsequently configure Azure AI Search to use "roles only", then Owner and Contributor won't be able to manage objects in the Azure portal using just those role assignments. The solution is to assign more roles, such as Search Index Data Reader, Search Index Data Contributor, and Search Service Contributor.

## Assign roles

In this section, assign roles for:

+ Service administration
+ Development or write-access to a search service
+ Read-only access for queries

<!-- + [Service administration](#assign-roles-for-service-administration)

    | Role | ID|
    | --- | --- |
    |`Owner`|8e3af657-a8ff-443c-a75c-2fe8c4bcb635|
    |`Contributor`|b24988ac-6180-42a0-ab88-20f7382dd24c|
    |`Reader`|acdd72a7-3385-48ef-bd42-f606fba81ae7|

+ [Development or write-access to a search service](#assign-roles-for-development)

    | Task | Role | ID|
    | --- | --- | --- |
    | CRUD operations | `Search Service Contributor`|7ca78c08-252a-4471-8644-bb5ff32d4ba0|
    | Load documents, run indexing jobs | `Search Index Data Contributor`|8ebe5a00-799e-43f5-93ac-243d3dce84a7|
    | Query an index | `Search Index Data Reader`|1407120a-92aa-4202-b7e9-c0e197c71c8f|

+ [Read-only access for queries](#assign-roles-for-read-only-queries)

    | Role | ID|
    | --- | --- |
    | `Search Index Data Reader` [with PowerShell](search-security-rbac.md?tabs=roles-portal-admin%2Croles-portal%2Croles-portal-query%2Ctest-portal%2Ccustom-role-portal#grant-access-to-a-single-index)|1407120a-92aa-4202-b7e9-c0e197c71c8f| -->

### Assign roles for service administration

As a service administrator, you can create and configure a search service, and perform all control plane operations described in the [Management REST API](/rest/api/searchmanagement/) or equivalent client libraries. If you're an Owner or Contributor, you can also perform most data plane [Search REST API](/rest/api/searchservice/) tasks in the Azure portal.

| Role | ID|
| --- | --- |
|[`Owner`](/azure/role-based-access-control/built-in-roles#owner) |8e3af657-a8ff-443c-a75c-2fe8c4bcb635|
|[`Contributor`](/azure/role-based-access-control/built-in-roles#contributor)|b24988ac-6180-42a0-ab88-20f7382dd24c|
|[`Reader`](/azure/role-based-access-control/built-in-roles#reader)|acdd72a7-3385-48ef-bd42-f606fba81ae7|

#### [**Azure portal**](#tab/roles-portal-admin)

1. Sign in to the [Azure portal](https://portal.azure.com).

1. Assign these roles:

   + Owner (full access to all data plane and control plane operations, except for query permissions)
   + Contributor (same as Owner, except for permissions to assign roles)
   + Reader (acceptable for monitoring and viewing metrics)

#### [**PowerShell**](#tab/roles-powershell-admin)

When you [use PowerShell to assign roles](/azure/role-based-access-control/role-assignments-powershell), call [New-AzRoleAssignment](/powershell/module/az.resources/new-azroleassignment), providing the Azure user or group name, and the scope of the assignment.

This example creates a role assignment scoped to a search service:

```powershell
New-AzRoleAssignment -SignInName <email> `
    -RoleDefinitionName "Reader" `
    -Scope  "/subscriptions/<subscription>/resourceGroups/<resource-group>/providers/Microsoft.Search/searchServices/<search-service>"
```

---

### Assign roles for development

Role assignments are global across the search service. To [scope permissions to a single index](#rbac-single-index), use PowerShell or the Azure CLI to create a custom role.

| Task | Role | ID|
| --- | --- | --- |
| CRUD operations | [`Search Service Contributor`](/azure/role-based-access-control/built-in-roles#search-service-contributor)|7ca78c08-252a-4471-8644-bb5ff32d4ba0|
| Load documents, run indexing jobs | [`Search Index Data Contributor`](/azure/role-based-access-control/built-in-roles#search-index-data-contributor)|8ebe5a00-799e-43f5-93ac-243d3dce84a7|
| Query an index | [`Search Index Data Reader`](/azure/role-based-access-control/built-in-roles#search-index-data-reader)|1407120a-92aa-4202-b7e9-c0e197c71c8f|

Another combination of roles that provides full access is Contributor or Owner, plus Search Index Data Reader.

> [!IMPORTANT]
> If you configure role-based access for a service or index and you also provide an API key on the request, the search service uses the API key to authenticate.

#### [**Azure portal**](#tab/roles-portal)

1. Sign in to the [Azure portal](https://portal.azure.com).

1. Assign these roles:

   + Search Service Contributor (create-read-update-delete operations on indexes, indexers, skillsets, and other top-level objects)
   + Search Index Data Contributor (load documents and run indexing jobs)
   + Search Index Data Reader (query an index)

#### [**PowerShell**](#tab/roles-powershell)

When you [use PowerShell to assign roles](/azure/role-based-access-control/role-assignments-powershell), call [New-AzRoleAssignment](/powershell/module/az.resources/new-azroleassignment), providing the Azure user or group name, and the scope of the assignment.

This example creates a role assignment scoped to a search service:

```powershell
New-AzRoleAssignment -SignInName <email> `
    -RoleDefinitionName "Search Index Data Contributor" `
    -Scope  "/subscriptions/<subscription>/resourceGroups/<resource-group>/providers/Microsoft.Search/searchServices/<search-service>"
```

This example creates a role assignment scoped to a specific index:

```powershell
New-AzRoleAssignment -SignInName <email> `
    -RoleDefinitionName "Search Index Data Contributor" `
    -Scope  "/subscriptions/<subscription>/resourceGroups/<resource-group>/providers/Microsoft.Search/searchServices/<search-service>/indexes/<index-name>"
```

---

### Assign roles for read-only queries

Use the Search Index Data Reader role for apps and processes that only need read-access to an index.

| Role | ID|
| --- | --- |
| [`Search Index Data Reader`](/azure/role-based-access-control/built-in-roles#search-index-data-reader) [with PowerShell](search-security-rbac.md#grant-access-to-a-single-index)|1407120a-92aa-4202-b7e9-c0e197c71c8f|

This is a very specific role. It grants [GET or POST access](/rest/api/searchservice/documents) to the *documents collection of a search index* for search, autocomplete, and suggestions. It doesn't support GET or LIST operations on an index or other top-level objects, or GET service statistics.

This section provides basic steps for setting up the role assignment and is here for completeness, but we recommend [Use Azure AI Search without keys ](keyless-connections.md) for comprehensive instructions on configuring your app for role-based access.

#### [**Azure portal**](#tab/roles-portal-query)

1. Sign in to the [Azure portal](https://portal.azure.com).

1. Assign the **Search Index Data Reader** role.

#### [**PowerShell**](#tab/roles-powershell-query)

When [using PowerShell to assign roles](/azure/role-based-access-control/role-assignments-powershell), call [New-AzRoleAssignment](/powershell/module/az.resources/new-azroleassignment), providing the Azure user or group name, and the scope of the assignment.

1. Get your subscription ID, search service resource group, and search service name.

1. Get the object identifier of your Azure service, such as Azure OpenAI.

   ```azurepowershell
    Get-AzADServicePrincipal -SearchString <YOUR AZURE OPENAI RESOURCE NAME>
   ```

1. Get the role definition and review the permissions to make sure this is the role you want.

   ```azurepowershell
   Get-AzRoleDefinition -Name "Search Index Data Reader"
   ```

1. Create the role assignment, substituting valid values for the placeholders.

   ```azurepowershell
   New-AzRoleAssignment -ObjectId YOUR-AZURE-OPENAI-OBJECT-ID -RoleDefinitionName "Search Index Data Reader" -Scope /subscriptions/YOUR-SUBSCRIPTION-ID/resourcegroups/YOUR-RESOURCE-GROUP/providers/Microsoft.Search/searchServices/YOUR-SEARCH-SERVICE-NAME
   ```

1. Here's an example of a role assignment scoped to a specific index:

    ```powershell
    New-AzRoleAssignment -ObjectId YOUR-AZURE-OPENAI-OBJECT-ID `
        -RoleDefinitionName "Search Index Data Reader" `
        -Scope /subscriptions/YOUR-SUBSCRIPTION-ID/resourcegroups/YOUR-RESOURCE-GROUP/providers/Microsoft.Search/searchServices/YOUR-SEARCH-SERVICE-NAME/indexes/YOUR-INDEX-NAME
    ```

---

## Test role assignments

Use a client to test role assignments. Remember that roles are cumulative and inherited roles that are scoped to the subscription or resource group level can't be deleted or denied at the resource (search service) level. 

[Configure your application for keyless connections](keyless-connections.md) and have role assignments in place before testing. 

### [**Azure portal**](#tab/test-portal)

1. Sign in to the [Azure portal](https://portal.azure.com).

1. Navigate to your search service.

1. On the Overview page, select the **Indexes** tab:

   + Search Service Contributors can view and create any object, but can't load documents or query an index. To verify permissions, [create a search index](search-how-to-create-search-index.md#create-an-index).

   + Search Index Data Contributors can load documents. There's no load documents option in the Azure portal outside of Import data wizard, but you can [reset and run an indexer](search-howto-run-reset-indexers.md) to confirm document load permissions.

   + Search Index Data Readers can query the index. To verify permissions, use [Search explorer](search-explorer.md). You should be able to send queries and view results, but you shouldn't be able to view the index definition or create one.

### [**REST API**](#tab/test-rest)

This approach assumes Visual Studio Code with a REST client extension.

1. Open a command shell for Azure CLI and sign in to your Azure subscription.

   ```azurecli
   az login
   ```

1. Get your tenant ID and subscription ID. The ID is used as a variable in a future step. 

   ```azurecli
   az account show
   ```

1. Get an access token.

   ```azurecli
   az account get-access-token --query accessToken --output tsv
   ```

1. Paste these variables in a new text file in Visual Studio Code.

   ```http
   @baseUrl = PASTE-YOUR-SEARCH-SERVICE-URL-HERE
   @index-name = PASTE-YOUR-INDEX-NAME-HERE
   @token = PASTE-YOUR-TOKEN-HERE
   ```

1. Paste and then send a request that uses the variables you've specified. For the "Search Index Data Reader" role, you can send a query. You can use any [supported API version](/rest/api/searchservice/search-service-api-versions).

   ```http
   POST https://{{baseUrl}}/indexes/{{index-name}}/docs/search?api-version=2024-07-01 HTTP/1.1
     Content-type: application/json
     Authorization: Bearer {{token}}

       {
            "queryType": "simple",
            "search": "motel",
            "filter": "",
            "select": "HotelName,Description,Category,Tags",
            "count": true
        }
   ```

For more information on how to acquire a token for a specific environment, see [Manage a Azure AI Search service with REST APIs](search-manage-rest.md) and [Microsoft identity platform authentication libraries](/azure/active-directory/develop/reference-v2-libraries).

### [**.NET**](#tab/test-csharp)

1. Use the [Azure.Search.Documents](https://www.nuget.org/packages/Azure.Search.Documents) package.

1. Use [Azure.Identity for .NET](/dotnet/api/overview/azure/identity-readme) for token authentication. Microsoft recommends [`DefaultAzureCredential()`](/dotnet/api/azure.identity.defaultazurecredential) for most scenarios.

1. Here's an example of a client connection using `DefaultAzureCredential()`.

    ```csharp
    // Create a SearchIndexClient to send create/delete index commands
    SearchIndexClient adminClient = new SearchIndexClient(serviceEndpoint, new DefaultAzureCredential());

    // Create a SearchClient to load and query documents
    SearchClient srchclient = new SearchClient(serviceEndpoint, indexName, new DefaultAzureCredential());
    ```

1. Here's another example of using [client secret credential](/dotnet/api/azure.core.tokencredential):

    ```csharp
    var tokenCredential =  new ClientSecretCredential(aadTenantId, aadClientId, aadSecret);
    SearchClient srchclient = new SearchClient(serviceEndpoint, indexName, tokenCredential);
    ```

### [**Python**](#tab/test-python)

1. Use [azure.search.documents (Azure SDK for Python)](https://pypi.org/project/azure-search-documents/).

1. Use [Azure.Identity for Python](/python/api/overview/azure/identity-readme) for token authentication.

1. Use [DefaultAzureCredential](/python/api/overview/azure/identity-readme?view=azure-python#authenticate-with-defaultazurecredential&preserve-view=true) if the Python client is an application that executes server-side. Enable [interactive authentication](/python/api/overview/azure/identity-readme?view=azure-python#enable-interactive-authentication-with-defaultazurecredential&preserve-view=true) if the app runs in a browser.

1. Here's an example:

    ```python
    from azure.search.documents import SearchClient
    from azure.identity import DefaultAzureCredential
    
    credential = DefaultAzureCredential()
    endpoint = "https://<mysearch>.search.windows.net"
    index_name = "myindex"
    client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)
    ```

### [**JavaScript**](#tab/test-javascript)

1. Use [@azure/search-documents (Azure SDK for JavaScript), version 11.3](https://www.npmjs.com/package/@azure/search-documents).

1. Use [Azure.Identity for JavaScript](/javascript/api/overview/azure/identity-readme) for token authentication.

1. If you're using React, use `InteractiveBrowserCredential` for Microsoft Entra authentication to Search. See [When to use `@azure/identity`](/javascript/api/overview/azure/identity-readme?view=azure-node-latest#when-to-use&preserve-view=true) for details.

### [**Java**](#tab/test-java)

1. Use [azure-search-documents (Azure SDK for Java)](https://central.sonatype.com/artifact/com.azure/azure-search-documents).

1. Use [Azure.Identity for Java](/java/api/overview/azure/identity-readme?view=azure-java-stable&preserve-view=true) for token authentication.

1. Microsoft recommends [DefaultAzureCredential](/java/api/overview/azure/identity-readme?view=azure-java-stable#defaultazurecredential&preserve-view=true) for apps that run on Azure.

---

## Test as current user

If you're already a Contributor or Owner of your search service, you can present a bearer token for your user identity for authentication to Azure AI Search. 

1. Get a bearer token for the current user using the Azure CLI:

    ```azurecli
    az account get-access-token --scope https://search.azure.com/.default
    ```

   Or by using PowerShell:

   ```powershell
   Get-AzAccessToken -ResourceUrl https://search.azure.com
   ```

1. Paste these variables into a new text file in Visual Studio Code.

   ```http
   @baseUrl = PASTE-YOUR-SEARCH-SERVICE-URL-HERE
   @index-name = PASTE-YOUR-INDEX-NAME-HERE
   @token = PASTE-YOUR-TOKEN-HERE
   ```

1. Paste in and then send a request to confirm access. Here's one that queries the hotels-quickstart index

   ```http
   POST https://{{baseUrl}}/indexes/{{index-name}}/docs/search?api-version=2024-07-01 HTTP/1.1
     Content-type: application/json
     Authorization: Bearer {{token}}

       {
            "queryType": "simple",
            "search": "motel",
            "filter": "",
            "select": "HotelName,Description,Category,Tags",
            "count": true
        }
   ```

<a name="rbac-single-index"></a>

## Grant access to a single index

In some scenarios, you might want to limit an application's access to a single resource, such as an index.

the Azure portal doesn't currently support role assignments at this level of granularity, but it can be done with [PowerShell](/azure/role-based-access-control/role-assignments-powershell) or the [Azure CLI](/azure/role-based-access-control/role-assignments-cli).

In PowerShell, use [New-AzRoleAssignment](/powershell/module/az.resources/new-azroleassignment), providing the Azure user or group name, and the scope of the assignment.

1. Load the `Azure` and `AzureAD` modules and connect to your Azure account:

   ```powershell
   Import-Module -Name Az
   Import-Module -Name AzureAD
   Connect-AzAccount
   ```

1. Add a role assignment scoped to an individual index:

   ```powershell
   New-AzRoleAssignment -ObjectId <objectId> `
       -RoleDefinitionName "Search Index Data Contributor" `
       -Scope  "/subscriptions/<subscription>/resourceGroups/<resource-group>/providers/Microsoft.Search/searchServices/<search-service>/indexes/<index-name>"
   ```

## Create a custom role

If [built-in roles](#built-in-roles-used-in-search) don't provide the right combination of permissions, you can create a [custom role](/azure/role-based-access-control/custom-roles) to support the operations you require.

This example clones **Search Index Data Reader** and then adds the ability to list indexes by name. Normally, listing the indexes on a search service is considered an administrative right.

### [**Azure portal**](#tab/custom-role-portal)

These steps are derived from [Create or update Azure custom roles using the Azure portal](/azure/role-based-access-control/custom-roles-portal). Cloning from an existing role is supported in a search service page.

These steps create a custom role that augments search query rights to include listing indexes by name. Typically, listing indexes is considered an admin function.

1. In the Azure portal, navigate to your search service.

1. In the left-navigation pane, select **Access Control (IAM)**.

1. In the action bar, select **Roles**.

1. Right-click **Search Index Data Reader** (or another role) and select **Clone** to open the **Create a custom role** wizard.

1. On the Basics tab, provide a name for the custom role, such as "Search Index Data Explorer", and then select **Next**.

1. On the Permissions tab, select **Add permission**.

1. On the Add permissions tab, search for and then select the **Microsoft Search** tile.

1. Set the permissions for your custom role. At the top of the page, using the default **Actions** selection:

   + Under Microsoft.Search/operations, select **Read : List all available operations**. 
   + Under Microsoft.Search/searchServices/indexes, select **Read : Read Index**.

1. On the same page, switch to **Data actions** and under Microsoft.Search/searchServices/indexes/documents, select **Read : Read Documents**.

   The JSON definition looks like the following example:

   ```json
   {
    "properties": {
        "roleName": "search index data explorer",
        "description": "",
        "assignableScopes": [
            "/subscriptions/0000000000000000000000000000000/resourceGroups/free-search-svc/providers/Microsoft.Search/searchServices/demo-search-svc"
        ],
        "permissions": [
            {
                "actions": [
                    "Microsoft.Search/operations/read",
                    "Microsoft.Search/searchServices/indexes/read"
                ],
                "notActions": [],
                "dataActions": [
                    "Microsoft.Search/searchServices/indexes/documents/read"
                ],
                "notDataActions": []
            }
        ]
      }
    }
    ```

1. Select **Review + create** to create the role. You can now assign users and groups to the role.

### [**Azure PowerShell**](#tab/custom-role-ps)

The PowerShell example shows the JSON syntax for creating a custom role that's a clone of **Search Index Data Reader**, but withe ability to list all indexes by name.

1. Review the [list of atomic permissions](/azure/role-based-access-control/resource-provider-operations#microsoftsearch) to determine which ones you need. For this example, you'll need the following:

   ```json
   "Microsoft.Search/operations/read",
   "Microsoft.Search/searchServices/read",
   "Microsoft.Search/searchServices/indexes/read"
   ```

1. Set up a PowerShell session to create the custom role. For detailed instructions, see [Azure PowerShell](/azure/role-based-access-control/custom-roles-powershell)

1. Provide the role definition as a JSON document. The following example shows the syntax for creating a custom role with PowerShell.

```json
{
  "Name": "Search Index Data Explorer",
  "Id": "88888888-8888-8888-8888-888888888888",
  "IsCustom": true,
  "Description": "List all indexes on the service and query them.",
  "Actions": [
      "Microsoft.Search/operations/read",
      "Microsoft.Search/searchServices/read"
  ],
  "NotActions": [],
  "DataActions": [
      "Microsoft.Search/searchServices/indexes/read"
  ],
  "NotDataActions": [],
  "AssignableScopes": [
    "/subscriptions/{subscriptionId1}"
  ]
}
```

> [!NOTE]
> If the assignable scope is at the index level, the data action should be `"Microsoft.Search/searchServices/indexes/documents/read"`.

### [**REST API**](#tab/custom-role-rest)

1. Review the [list of atomic permissions](/azure/role-based-access-control/resource-provider-operations#microsoftsearch) to determine which ones you need.

1. See [Create or update Azure custom roles using the REST API](/azure/role-based-access-control/custom-roles-rest) for steps.

1. Copy or create a role, or use JSON to specify the custom role (see the PowerShell tab for JSON syntax).

### [**Azure CLI**](#tab/custom-role-cli)

1. Review the [list of atomic permissions](/azure/role-based-access-control/resource-provider-operations#microsoftsearch) to determine which ones you need.

1. See [Create or update Azure custom roles using Azure CLI](/azure/role-based-access-control/custom-roles-cli) for steps.

1. See the PowerShell tab for JSON syntax.

---

## Conditional Access

We recommend [Microsoft Entra Conditional Access](/entra/identity/conditional-access/overview) if you need to enforce organizational policies, such as multifactor authentication.

To enable a Conditional Access policy for Azure AI Search, follow these steps:

1. [Sign in](https://portal.azure.com) to the Azure portal.

1. Search for **Microsoft Entra Conditional Access**.

1. Select **Policies**.

1. Select **New policy**.

1. In the **Cloud apps or actions** section of the policy, add **Azure AI Search** as a cloud app depending on how you want to set up your policy.

1. Update the remaining parameters of the policy. For example, specify which users and groups this policy applies to. 

1. Save the policy.

> [!IMPORTANT]
> If your search service has a managed identity assigned to it, the specific search service will show up as a cloud app that can be included or excluded as part of the Conditional Access policy. Conditional Access policies can't be enforced on a specific search service. Instead make sure you select the general **Azure AI Search** cloud app.

## Limitations

+ Role-based access control can increase the latency of some requests. Each unique combination of service resource (index, indexer, etc.) and service principal triggers an authorization check. These authorization checks can add up to 200 milliseconds of latency per request. 

+ In rare cases where requests originate from a high number of different service principals, all targeting different service resources (indexes, indexers, etc.), it's possible for the authorization checks to result in throttling. Throttling would only happen if hundreds of unique combinations of search service resource and service principal were used within a second.

## Troubleshooting role-based access control issues

When developing applications that use role-based access control for authentication, some common issues might occur:

+ If the authorization token came from a [managed identity](/entra/identity/managed-identities-azure-resources/overview) and the appropriate permissions were recently assigned, it [might take several hours](/entra/identity/managed-identities-azure-resources/managed-identity-best-practice-recommendations#limitation-of-using-managed-identities-for-authorization) for these permissions assignments to take effect.

+ The default configuration for a search service is [key-based authentication](search-security-api-keys.md). If you didn't change the default key setting to **Both** or **Role-based access control**, then all requests using role-based authentication are automatically denied regardless of the underlying permissions.
