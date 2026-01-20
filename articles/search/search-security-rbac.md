---
title: Connect using Azure roles
titleSuffix: Azure AI Search
description: Use Azure role-based access control for granular permissions on service administration and content tasks.
author: HeidiSteen
ms.author: heidist
manager: nitinme
ms.date: 01/20/2026
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.topic: how-to
ms.custom:
  - subject-rbac-steps
  - devx-track-azurepowershell
  - build-2025
  - dev-focus
ai-usage: ai-assisted
---

# Connect to Azure AI Search using roles

Azure provides global authentication and [role-based access control](/azure/role-based-access-control/role-assignments-portal) through Microsoft Entra ID for all services running on the platform. In this article, learn which roles provide access to search content and administration on Azure AI Search.

In Azure AI Search, you can assign Azure roles for:

+ [Service administration](#assign-roles-for-service-administration)
+ [Development or write-access to a search service](#assign-roles-for-development)
+ [Read-only access for queries](#assign-roles-for-read-only-queries)
+ [Scoped access to a single index](#grant-access-to-a-single-index)

Per-user access over search results (sometimes referred to as *row-level security* or *document-level access*) is supported through permission inheritance for Azure Data Lake Storage (ADLS) Gen2 and Azure blob indexes and through security filters for all other platforms (see [Document-level access control](search-document-level-access-overview.md)).

Role assignments are cumulative and pervasive across all tools and client libraries. You can assign roles by using any of the [supported approaches](/azure/role-based-access-control/role-assignments-steps) described in Azure role-based access control documentation.

Role-based access is optional, but recommended. The alternative is [key-based authentication](search-security-api-keys.md), which is the default.

### Quick reference: Roles by task

| Task | Required role(s) |
| ---- | ---------------- |
| Create or manage indexes, indexers, skillsets | Search Service Contributor |
| Load documents into an index | Search Index Data Contributor |
| Query an index | Search Index Data Reader |
| Full development access | Search Service Contributor + Search Index Data Contributor + Search Index Data Reader |
| Service administration | Owner or Contributor |

## Prerequisites

+ A search service in any region, on any tier, [enabled for role-based access](search-security-enable-roles.md).

+ Owner, User Access Administrator, Role-based Access Control Administrator, or a custom role with [Microsoft.Authorization/roleAssignments/write](/azure/templates/microsoft.authorization/roleassignments) permissions.

## Built-in roles used in search

Roles are a collection of permissions on specific operations that affect either data plane or control plane layers.

*Data plane* refers to operations against the search service endpoint, such as indexing or queries, or any other operation specified in the [Search Service REST APIs](/rest/api/searchservice/) or equivalent Azure SDK client libraries. 

*Control plane* refers to Azure resource management, such as creating or configuring a search service.

The following roles are built in. If these roles don't meet your needs, [create a custom role](#create-a-custom-role). 

| Role | Plane | Description  |
| ---- | ------|--------------------- |
| [Owner](/azure/role-based-access-control/built-in-roles#owner) | Control & Data | Full access to the control plane of the search resource, including the ability to assign Azure roles. Only the Owner role can enable or disable authentication options or manage roles for other users. Subscription administrators are members by default. </br></br>On the data plane, this role has the same access as the Search Service Contributor role. It includes access to all data plane actions except the ability to query documents.|
| [Contributor](/azure/role-based-access-control/built-in-roles#contributor) | Control & Data |  Same level of control plane access as Owner, minus the ability to assign roles or change authentication options. </br></br>On the data plane, this role has the same access as the Search Service Contributor role. It includes access to all data plane actions except the ability to query or index documents.|
| [Reader](/azure/role-based-access-control/built-in-roles#reader) | Control & Data | Read access across the entire service, including search metrics, content metrics (storage consumed, number of objects), and the object definitions of data plane resources (indexes, indexers, and so on). However, it can't read API keys or read content within indexes. |
| [Search Service Contributor](/azure/role-based-access-control/built-in-roles#search-service-contributor) | Control & Data | Read-write access to object definitions (indexes, aliases, synonym maps, indexers, data sources, and skillsets). This role is for developers who create objects, and for administrators who manage a search service and its objects, but without access to index content. Use this role to create, delete, and list indexes, get index definitions, get service information (statistics and quotas), test analyzers, create and manage synonym maps, indexers, data sources, and skillsets. See [`Microsoft.Search/searchServices/*`](/azure/role-based-access-control/resource-provider-operations#microsoftsearch) for the permissions list. |
| [Search Index Data Contributor](/azure/role-based-access-control/built-in-roles#search-index-data-contributor) | Data | Read-write access to content in indexes. This role is for developers or index owners who need to import, refresh, or query the documents collection of an index. This role doesn't support index creation, updates, or deletion. By default, this role applies to all indexes on a search service. See [Grant access to a single index](#grant-access-to-a-single-index) to narrow the scope.  |
| [Search Index Data Reader](/azure/role-based-access-control/built-in-roles#search-index-data-reader) | Data |  Read-only access for querying search indexes. This role is for apps and users who run queries. This role doesn't support read access to object definitions. For example, you can't read a search index definition or get search service statistics. By default, this role is for all indexes on a search service. See [Grant access to a single index](#grant-access-to-a-single-index) to narrow the scope.  |

Combine these roles to get sufficient permissions for your use case.

> [!NOTE]
> If you disable Azure role-based access, built-in roles for the control plane (Owner, Contributor, Reader) continue to be available. Disabling role-based access removes just the data-related permissions associated with those roles. If you disable data plane roles, Search Service Contributor is equivalent to control-plane Contributor.

## Summary of permissions

| Permissions | Search Index Data Reader | Search Index Data Contributor | Search Service Contributor | Owner/Contributor | Reader |
|-------------|--------------------------|-------------------------------|----------------------------|-------------------|--------|
|View the resource in Azure portal |❌|❌|✅|✅|✅|
|View resource properties, metrics, and endpoint |❌|❌|✅|✅|✅|
|List all objects on the resource |❌|❌|✅|✅|✅|
|Access quotas and service statistics |❌|❌|✅|✅|❌|
|Read and query an index |✅|✅|❌|❌|❌|
|Upload data for indexing <sup>1</sup>|❌|✅|❌|❌|❌|
|Elevated read regardless of permission filters <sup>2</sup>|❌|✅|❌|❌|❌|
|Create or edit indexes and aliases |❌|❌|✅|✅|❌|
|Create, edit, and run indexers, data sources, and skillsets |❌|❌|✅|✅|❌|
|Create or edit synonym maps |❌|❌|✅|✅|❌|
|Create or edit debug sessions |❌|❌|✅|✅|❌|
|Create or manage deployments |❌|❌|✅|✅|❌|
|Create or configure Azure AI Search resources |❌|❌|✅|✅|❌|
|View, copy, and regenerate keys under Keys |❌|❌|✅|✅|❌|
|View roles, policies, and definitions |❌|❌|✅|✅|❌|
|Set authentication options |❌|❌|✅|✅|❌|
|Configure private connections |❌|❌|✅|✅|❌|
|Configure network security |❌|❌|✅|✅|❌|

<sup>1</sup> In the Azure portal, an Owner or Contributor can run the Import data wizards that create and load indexes, even though they can't upload documents in other clients. The search service itself, not individual users, makes data connections in the wizard. The wizards have the `Microsoft.Search/searchServices/indexes/documents/*` permission necessary for completing this task.

<sup>2</sup> Use elevated read for debugging queries that obtain results by using the identity of the called. For more information, see [Investigate incorrect query results](search-query-access-control-rbac-enforcement.md#elevated-permissions-for-investigating-incorrect-results).

Owners and Contributors grant the same permissions, except that only Owners can assign roles.

## Assign roles

In this section, assign roles for:

+ Service administration
+ Development or write access to a search service
+ Read-only access for queries

### Assign roles for service administration

As a service administrator, you can create and configure a search service, and perform all control plane operations described in the [Management REST API](/rest/api/searchmanagement/) or equivalent client libraries. If you're an Owner or Contributor, you can also perform most data plane [Search REST API](/rest/api/searchservice/) tasks in the Azure portal.

| Role | ID|
| --- | --- |
|[`Owner`](/azure/role-based-access-control/built-in-roles#owner) |8e3af657-a8ff-443c-a75c-2fe8c4bcb635|
|[`Contributor`](/azure/role-based-access-control/built-in-roles#contributor)|b24988ac-6180-42a0-ab88-20f7382dd24c|
|[`Reader`](/azure/role-based-access-control/built-in-roles#reader)|acdd72a7-3385-48ef-bd42-f606fba81ae7|

#### [**Azure portal**](#tab/roles-portal-admin)

1. Sign in to the [Azure portal](https://portal.azure.com).

1. Select **Access Control (IAM)** in the left pane.

1. Select **+ Add** > **Add role assignment** to start the **Add role assignment** wizard.

   :::image type="content" source="media/search-security-rbac/portal-access-control.png" alt-text="Screenshot of the access control page in the Azure portal.":::

1. Select a role.

   + Owner (full access to all data plane and control plane operations, except for query permissions)
   + Contributor (same as Owner, except for permissions to assign roles)
   + Reader (acceptable for monitoring and viewing metrics)

1. On the **Members** tab, select the Microsoft Entra user or group identity. If you're setting up permissions for another Azure service, select a system or user-managed identity.

1. On the **Review + assign** tab, select **Review + assign** to assign the role.

#### [**PowerShell**](#tab/roles-powershell-admin)

When you [use PowerShell to assign roles](/azure/role-based-access-control/role-assignments-powershell), call [New-AzRoleAssignment](/powershell/module/az.resources/new-azroleassignment), providing the Azure user or group name, and the scope of the assignment.

This example creates a role assignment scoped to a search service:

```powershell
New-AzRoleAssignment -SignInName <email> `
    -RoleDefinitionName "Reader" `
    -Scope  "/subscriptions/<subscription>/resourceGroups/<resource-group>/providers/Microsoft.Search/searchServices/<search-service>"
```

**Reference:** [New-AzRoleAssignment](/powershell/module/az.resources/new-azroleassignment)

---

### Assign roles for development

Role assignments apply globally across the search service. To [scope permissions to a single index](#rbac-single-index), use PowerShell or the Azure CLI to create a custom role.

| Task | Role | ID |
| --- | --- | --- |
| Create or manage objects | [`Search Service Contributor`](/azure/role-based-access-control/built-in-roles#search-service-contributor) | 7ca78c08-252a-4471-8644-bb5ff32d4ba0 |
| Load documents, run indexing jobs | [`Search Index Data Contributor`](/azure/role-based-access-control/built-in-roles#search-index-data-contributor) | 8ebe5a00-799e-43f5-93ac-243d3dce84a7 |
| Query an index | [`Search Index Data Reader`](/azure/role-based-access-control/built-in-roles#search-index-data-reader) | 1407120a-92aa-4202-b7e9-c0e197c71c8f |

Another combination of roles that provides full access is Contributor or Owner, plus Search Index Data Reader.

> [!IMPORTANT]
> If you configure role-based access for a service or index and you also provide an API key on the request, the search service uses the API key to authenticate.

#### [**Azure portal**](#tab/roles-portal)

1. Sign in to the [Azure portal](https://portal.azure.com).

1. Select **Access Control (IAM)** in the left pane.

1. Select **+ Add** > **Add role assignment** to start the **Add role assignment** wizard.

   :::image type="content" source="media/search-security-rbac/portal-access-control.png" alt-text="Screenshot of the access control page in the Azure portal.":::

1. Select a role.

   + Search Service Contributor (create, read, update, and delete operations on indexes, indexers, skillsets, and other top-level objects)
   + Search Index Data Contributor (load documents and run indexing jobs)
   + Search Index Data Reader (query an index)

1. On the **Members** tab, select the Microsoft Entra user or group identity. If you're setting up permissions for another Azure service, select a system or user-managed identity.

1. On the **Review + assign** tab, select **Review + assign** to assign the role.

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

**Reference:** [New-AzRoleAssignment](/powershell/module/az.resources/new-azroleassignment)

---

### Assign roles for read-only queries

Use the Search Index Data Reader role for apps and processes that only need read access to an index.

| Role | ID|
| --- | --- |
| [`Search Index Data Reader`](/azure/role-based-access-control/built-in-roles#search-index-data-reader) [with PowerShell](search-security-rbac.md#grant-access-to-a-single-index)|1407120a-92aa-4202-b7e9-c0e197c71c8f|

This role is very specific. It grants [GET or POST access](/rest/api/searchservice/documents) to the *documents collection of a search index* for search, autocomplete, and suggestions. It doesn't support GET or LIST operations on an index or other top-level objects, or GET service statistics.

This section provides basic steps for setting up the role assignment and is here for completeness, but for comprehensive instructions on configuring your app for role-based access, see [Use Azure AI Search without keys](search-security-rbac-client-code.md).

> [!NOTE]
> As a developer, if you need to debug queries that are predicated on a Microsoft identity, use Search Index Data Contributor or create a custom role that gives you [elevated permissions for debug purposes](search-query-access-control-rbac-enforcement.md#elevated-permissions-for-investigating-incorrect-results).

#### [**Azure portal**](#tab/roles-portal-query)

1. Sign in to the [Azure portal](https://portal.azure.com).

1. Select **Access Control (IAM)** in the left pane.

1. Select **+ Add** > **Add role assignment** to start the **Add role assignment** wizard.

   :::image type="content" source="media/search-security-rbac/portal-access-control.png" alt-text="Screenshot of the access control page in the Azure portal.":::

1. Select the **Search Index Data Reader** role.

1. On the **Members** tab, select the Microsoft Entra user or group identity. If you're setting up permissions for another Azure service, select a system or user-managed identity.

1. On the **Review + assign** tab, select **Review + assign** to assign the role.

#### [**PowerShell**](#tab/roles-powershell-query)

When [using PowerShell to assign roles](/azure/role-based-access-control/role-assignments-powershell), call [New-AzRoleAssignment](/powershell/module/az.resources/new-azroleassignment), providing the Azure user or group name, and the scope of the assignment.

1. Get your subscription ID, search service resource group, and search service name.

1. Get the object identifier of your Azure service, such as Azure OpenAI.

   ```azurepowershell
    Get-AzADServicePrincipal -SearchString <your-azure-openai-resource-name>
   ```

   The output includes an `Id` property containing the object ID you need for the role assignment.

1. Get the role definition and review the permissions to make sure this is the role you want.

   ```azurepowershell
   Get-AzRoleDefinition -Name "Search Index Data Reader"
   ```

1. Create the role assignment, substituting valid values for the placeholders.

   ```azurepowershell
   New-AzRoleAssignment -ObjectId <your-azure-openai-object-id> -RoleDefinitionName "Search Index Data Reader" -Scope /subscriptions/<your-subscription-id>/resourcegroups/<your-resource-group>/providers/Microsoft.Search/searchServices/<your-search-service-name>
   ```

   A successful assignment returns the role assignment details including `RoleAssignmentId`.

1. Here's an example of a role assignment scoped to a specific index:

    ```powershell
    New-AzRoleAssignment -ObjectId <your-azure-openai-object-id> `
        -RoleDefinitionName "Search Index Data Reader" `
        -Scope /subscriptions/<your-subscription-id>/resourcegroups/<your-resource-group>/providers/Microsoft.Search/searchServices/<your-search-service-name>/indexes/<your-index-name>
    ```

    **Reference:** [New-AzRoleAssignment](/powershell/module/az.resources/new-azroleassignment)

---

## Test role assignments

Use a client to test role assignments. Remember that roles are cumulative. You can't delete or deny inherited roles that are scoped to the subscription or resource group level at the resource (search service) level. 

[Configure your application for keyless connections](search-security-rbac-client-code.md) and have role assignments in place before testing. 

### [**Azure portal**](#tab/test-portal)

1. Sign in to the [Azure portal](https://portal.azure.com).

1. Navigate to your search service.

1. On the Overview page, select the **Indexes** tab:

   + Search Service Contributors can view and create any object, but can't load documents or query an index. To verify permissions, [create a search index](search-how-to-create-search-index.md#create-an-index).

   + Search Index Data Contributors can load documents. There's no load documents option in the Azure portal outside of Import data wizard, but you can [reset and run an indexer](search-howto-run-reset-indexers.md) to confirm document load permissions.

   + Search Index Data Readers can query the index. To verify permissions, use [Search explorer](search-explorer.md). You should be able to send queries and view results, but you shouldn't be able to view the index definition or create one.

### [**REST API**](#tab/test-rest)

This approach assumes Visual Studio Code with a [REST client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client).

1. Open a command shell for Azure CLI and sign in to your Azure subscription.

   ```azurecli
   az login
   ```

1. Get your tenant ID and subscription ID. Use the ID as a variable in a future step. 

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

1. Paste and then send a request that uses the variables you specify. For the "Search Index Data Reader" role, you can send a query. You can use any [supported API version](/rest/api/searchservice/search-service-api-versions).

   ```http
   POST https://{{baseUrl}}/indexes/{{index-name}}/docs/search?api-version=2025-09-01 HTTP/1.1
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

   A successful query returns search results with matching documents. If the index is empty or has no matches, `value` contains an empty array.

   **Reference:** [Search Documents](/rest/api/searchservice/documents/search-post)

> [!TIP]
> For more information on how to acquire a token for a specific environment, see [Manage a Azure AI Search service with REST APIs](search-manage-rest.md) and [Microsoft identity platform authentication libraries](/azure/active-directory/develop/reference-v2-libraries).

### [**.NET**](#tab/test-csharp)

1. Install the required packages:

   ```dotnetcli
   dotnet add package Azure.Search.Documents
   dotnet add package Azure.Identity
   ```

1. Use [Azure.Identity for .NET](/dotnet/api/overview/azure/identity-readme) for token authentication. Microsoft recommends [`DefaultAzureCredential()`](/dotnet/api/azure.identity.defaultazurecredential) for most scenarios.

1. Here's an example of a client connection using `DefaultAzureCredential()`:

    ```csharp
    // Create a SearchIndexClient to send create/delete index commands
    // Requires Search Service Contributor role
    SearchIndexClient adminClient = new SearchIndexClient(serviceEndpoint, new DefaultAzureCredential());

    // Create a SearchClient to load and query documents
    // Requires Search Index Data Contributor (load) or Search Index Data Reader (query)
    SearchClient srchclient = new SearchClient(serviceEndpoint, indexName, new DefaultAzureCredential());
    ```

    **Reference:** [SearchClient](/dotnet/api/azure.search.documents.searchclient), [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient), [DefaultAzureCredential](/dotnet/api/azure.identity.defaultazurecredential)

1. Here's another example of using [client secret credential](/dotnet/api/azure.core.tokencredential):

    ```csharp
    var tokenCredential =  new ClientSecretCredential(aadTenantId, aadClientId, aadSecret);
    SearchClient srchclient = new SearchClient(serviceEndpoint, indexName, tokenCredential);
    ```

1. Here's an example of running a query:

    ```csharp
    SearchResults<SearchDocument> response = srchclient.Search<SearchDocument>("motel");
    foreach (SearchResult<SearchDocument> result in response.GetResults())
    {
        Console.WriteLine(result.Document["HotelName"]);
    }
    ```

    A successful query returns search results. If no documents match, the results collection is empty.

### [**Python**](#tab/test-python)

1. Install the required packages:

   ```bash
   pip install azure-search-documents azure-identity
   ```

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

    **Reference:** [SearchClient](/python/api/azure-search-documents/azure.search.documents.searchclient), [DefaultAzureCredential](/python/api/azure-identity/azure.identity.defaultazurecredential)

### [**JavaScript**](#tab/test-javascript)

1. Install the required packages:

   ```bash
   npm install @azure/search-documents @azure/identity
   ```

1. Use [Azure.Identity for JavaScript](/javascript/api/overview/azure/identity-readme) for token authentication.

1. If you're using React, use `InteractiveBrowserCredential` for Microsoft Entra authentication to Search. See [When to use `@azure/identity`](/javascript/api/overview/azure/identity-readme?view=azure-node-latest#when-to-use&preserve-view=true) for details.

### [**Java**](#tab/test-java)

1. Add the required dependencies to your `pom.xml`:

   ```xml
   <dependency>
     <groupId>com.azure</groupId>
     <artifactId>azure-search-documents</artifactId>
     <version>11.6.0</version>
   </dependency>
   <dependency>
     <groupId>com.azure</groupId>
     <artifactId>azure-identity</artifactId>
     <version>1.10.0</version>
   </dependency>
   ```

1. Use [Azure.Identity for Java](/java/api/overview/azure/identity-readme?view=azure-java-stable&preserve-view=true) for token authentication.

1. Use [DefaultAzureCredential](/java/api/overview/azure/identity-readme?view=azure-java-stable#defaultazurecredential&preserve-view=true) for apps that run on Azure.

---

## Test as current user

If you're already a Contributor or Owner of your search service, you can use a bearer token for your user identity to authenticate to Azure AI Search.

1. Get a bearer token for the current user by using the Azure CLI:

    ```azurecli
    az account get-access-token --scope https://search.azure.com/.default
    ```

   Or use PowerShell:

   ```powershell
   Get-AzAccessToken -ResourceUrl https://search.azure.com
   ```

1. Paste these variables into a new text file in Visual Studio Code.

   ```http
   @baseUrl = PASTE-YOUR-SEARCH-SERVICE-URL-HERE
   @index-name = PASTE-YOUR-INDEX-NAME-HERE
   @token = PASTE-YOUR-TOKEN-HERE
   ```

1. Paste in and then send a request to confirm access. Here's one that queries the hotels-quickstart index.

   ```http
   POST https://{{baseUrl}}/indexes/{{index-name}}/docs/search?api-version=2025-09-01 HTTP/1.1
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

The Azure portal doesn't currently support role assignments at this level of granularity, but you can assign roles using [PowerShell](/azure/role-based-access-control/role-assignments-powershell) or the [Azure CLI](/azure/role-based-access-control/role-assignments-cli).

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

These steps are derived from [Create or update Azure custom roles using the Azure portal](/azure/role-based-access-control/custom-roles-portal). A search service page supports cloning from an existing role.

These steps create a custom role that augments search query rights to include listing indexes by name. Typically, listing indexes is considered an admin function.

1. In the Azure portal, go to your search service.

1. In the left-navigation pane, select **Access Control (IAM)**.

1. In the action bar, select **Roles**.

1. Right-click **Search Index Data Reader** (or another role) and select **Clone** to open the **Create a custom role** wizard.

1. On the Basics tab, provide a name for the custom role, such as "Search Index Data Explorer", and then select **Next**.

1. On the Permissions tab, select **Add permission**.

1. On the Add permissions tab, search for and then select the **Microsoft Search** tile.

1. Set the permissions for your custom role. At the top of the page, use the default **Actions** selection:

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

The PowerShell example shows the JSON syntax for creating a custom role that's a clone of **Search Index Data Reader**, but with the ability to list all indexes by name.

1. Review the [list of atomic permissions](/azure/role-based-access-control/resource-provider-operations#microsoftsearch) to determine which ones you need. For this example, you need the following permissions:

   ```json
   "Microsoft.Search/operations/read",
   "Microsoft.Search/searchServices/read",
   "Microsoft.Search/searchServices/indexes/read"
   ```

1. Set up a PowerShell session to create the custom role. For detailed instructions, see [Azure PowerShell](/azure/role-based-access-control/custom-roles-powershell).

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
> If you assign the scope at the index level, use the data action `"Microsoft.Search/searchServices/indexes/documents/read"`.

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

If you need to enforce organizational policies, such as multifactor authentication, use [Microsoft Entra Conditional Access](/entra/identity/conditional-access/overview).

To enable a Conditional Access policy for Azure AI Search, follow these steps:

1. [Sign in](https://portal.azure.com) to the Azure portal.

1. Search for **Microsoft Entra Conditional Access**.

1. Select **Policies**.

1. Select **New policy**.

1. In the **Cloud apps or actions** section of the policy, add **Azure AI Search** as a cloud app depending on how you want to set up your policy.

1. Update the remaining parameters of the policy. For example, specify which users and groups this policy applies to. 

1. Save the policy.

> [!IMPORTANT]
> If your search service has a managed identity assigned to it, the specific search service shows up as a cloud app that you can include or exclude as part of the Conditional Access policy. You can't enforce Conditional Access policies on a specific search service. Instead, make sure you select the general **Azure AI Search** cloud app.

## Troubleshooting role-based access control issues

When you develop applications that use role-based access control for authentication, you might encounter some common problems:

+ If the authorization token comes from a [managed identity](/entra/identity/managed-identities-azure-resources/overview) and you recently assigned the appropriate permissions, it [might take several hours](/entra/identity/managed-identities-azure-resources/managed-identity-best-practice-recommendations#limitation-of-using-managed-identities-for-authorization) for these permissions assignments to take effect.

+ The default configuration for a search service is [key-based authentication](search-security-api-keys.md). If you don't change the default key setting to **Both** or **Role-based access control**, then all requests by using role-based authentication are automatically denied regardless of the underlying permissions.
