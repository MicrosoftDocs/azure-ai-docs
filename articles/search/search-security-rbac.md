---
title: Connect Using Azure Roles
description: Learn how to assign Azure roles in Azure AI Search to manage permissions for service administration, development, and query access with Microsoft Entra ID.
ms.date: 03/24/2026
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

Azure AI Search supports [role-based access control](/azure/role-based-access-control/role-assignments-portal) through Microsoft Entra ID. Role-based access is optional but recommended. The alternative is [key-based authentication](search-security-api-keys.md), which is the default.

If you assign multiple roles to a security principal, permissions are combined. Role assignments apply across all tools and client libraries. You can assign roles using any [supported approach](/azure/role-based-access-control/role-assignments-steps).

This article explains how to assign built-in roles for service administration, development, and read-only query and retrieval access. It also provides steps for creating custom roles and testing role assignments.

> [!TIP]
> + Want a quick overview of built-in roles? See [Summary of permissions](#summary-of-permissions).
> + For per-user access over search results, also known as row-level security or document-level access, see [Document-level access control in Azure AI Search](search-document-level-access-overview.md).

## Prerequisites

+ An Azure AI Search service (any region and any tier) with [role-based access enabled](search-security-enable-roles.md).

+ Permission to assign Azure roles. Any of the following roles work:
  + Owner
  + User Access Administrator
  + Role Based Access Control Administrator
  + A custom role with [Microsoft.Authorization/roleAssignments/write](/azure/templates/microsoft.authorization/roleassignments) permissions

## Built-in roles

Roles are a collection of permissions that affect the control plane or data plane:

+ **Control plane:** Operations that create, configure, and manage the search service and its object definitions. Available through the [Search Management REST APIs](/rest/api/searchmanagement/) for service provisioning and configuration, [Search Service REST APIs](/rest/api/searchservice/) for object definitions, and [Azure RBAC REST APIs](/rest/api/authorization/) for role assignments. Equivalent Azure SDK client libraries are also available.

+ **Data plane:** Operations that target content hosted on a search service, such as loading documents, querying indexes, and retrieving from knowledge bases. Available through the [Search Service REST APIs](/rest/api/searchservice/) or an equivalent Azure SDK client library.

### Role descriptions

The following built-in roles grant permissions to Azure AI Search. Control plane roles are always available, while data plane roles require role-based access to be enabled on your search service.

| Role | Plane | Description |
| -- | -- | -- |
| [Owner](/azure/role-based-access-control/built-in-roles#owner) | Control | Full control plane access, including the ability to assign roles and change authentication settings. Subscription administrators are members by default. Can manage object definitions and retrieve admin keys. Can't load documents, query indexes, or retrieve from knowledge bases. |
| [Contributor](/azure/role-based-access-control/built-in-roles#contributor) | Control | Same level of control plane access as Owner, minus the ability to assign roles. Can't load documents, query indexes, or retrieve from knowledge bases. |
| [Reader](/azure/role-based-access-control/built-in-roles#reader) | Control | Read-only control plane access to service metrics, object definitions, and quotas. Can't retrieve API keys, load documents, query indexes, or retrieve from knowledge bases. |
| [Search Service Contributor](/azure/role-based-access-control/built-in-roles#search-service-contributor) | Control | Create and manage object definitions, including indexes, indexers, data sources, skillsets, knowledge bases, and knowledge sources. Can retrieve admin keys. Can't load documents, query indexes, or retrieve from knowledge bases. For the full permissions list, see [`Microsoft.Search/searchServices/*`](/azure/role-based-access-control/permissions/ai-machine-learning#microsoftsearch). |
| [Search Index Data Contributor](/azure/role-based-access-control/built-in-roles#search-index-data-contributor) | Data | Read-write data access. Can load documents, query indexes, and retrieve from knowledge bases. Can't modify object definitions or retrieve admin keys. To scope to specific indexes, see [Grant access to a single index](#grant-access-to-a-single-index). |
| [Search Index Data Reader](/azure/role-based-access-control/built-in-roles#search-index-data-reader) | Data | Read-only data access. Can query indexes and retrieve from knowledge bases. Can't load documents, modify object definitions, or retrieve admin keys. To scope to specific indexes, see [Grant access to a single index](#grant-access-to-a-single-index). |

> [!NOTE]
> Combine the built-in roles to get sufficient permissions for your use case. If these roles don't meet your needs, [create a custom role](#create-a-custom-role).

### Summary of permissions

Use the following table to quickly find which role provides the permissions you need:

| Permissions | Owner/Contributor | Reader | Search Service Contributor | Search Index Data Contributor | Search Index Data Reader |
| -- | -- | -- | -- | -- | -- |
| Create and configure Azure AI Search services | ✅ | ❌ | ✅ | ❌ | ❌ |
| Access service in the Azure portal | ✅ | ✅ | ✅ | ❌ | ❌ |
| View service properties, metrics, and endpoint | ✅ | ✅ | ✅ | ❌ | ❌ |
| List all objects on the service | ✅ | ✅ | ✅ | ❌ | ❌ |
| Access quotas and service statistics | ✅ | ❌ | ✅ | ❌ | ❌ |
| View, copy, and regenerate keys | ✅ | ❌ | ✅ | ❌ | ❌ |
| Set authentication options | ✅ | ❌ | ✅ | ❌ | ❌ |
| View roles, policies, and definitions | ✅ | ❌ | ✅ | ❌ | ❌ |
| Configure network security and private connections | ✅ | ❌ | ✅ | ❌ | ❌ |
| Create, run, and manage search objects <sup>1</sup> | ✅ | ❌ | ✅ | ❌ | ❌ |
| Upload data for indexing <sup>2</sup> | ❌ | ❌ | ❌ | ✅ | ❌ |
| Query an index | ❌ | ❌ | ❌ | ✅ | ✅ |
| Retrieve from a knowledge base | ❌ | ❌ | ❌ | ✅ | ✅ |
| Elevated read, regardless of permission filters <sup>3</sup> | ❌ | ❌ | ❌ | ✅ | ❌ |

<sup>1</sup> Includes creating, updating, and deleting indexes, indexers, 
data sources, skillsets, aliases, synonym maps, debug sessions, knowledge bases, and knowledge sources. 
Indexers also support run and reset operations.

<sup>2</sup> An Owner or Contributor can run the [**Import data** wizard](search-import-data-portal.md) to create and load indexes, even though they can't upload documents in other clients. The search service itself, not individual users, makes data connections in the wizard. The wizard has the necessary `Microsoft.Search/searchServices/indexes/documents/*` permissions for this task.

<sup>3</sup> [Elevated read](search-query-access-control-rbac-enforcement.md#elevated-permissions-for-investigating-incorrect-results) bypasses permission metadata on documents, allowing you to see all results and investigate why specific users can't see expected content.

## Assign built-in roles

In this section, you assign roles for:

+ [Service administration](#assign-roles-for-service-administration)
+ [Development](#assign-roles-for-development)
+ [Read-only access](#assign-roles-for-read-only-access)

### Assign roles for service administration

The following roles let you create, configure, and manage a search service. These roles are hierarchical, so select one based on the access level you need.

| Role | ID |
| -- | -- |
| [Owner](#role-descriptions) | 8e3af657-a8ff-443c-a75c-2fe8c4bcb635 |
| [Contributor](#role-descriptions) | b24988ac-6180-42a0-ab88-20f7382dd24c |
| [Reader](#role-descriptions) | acdd72a7-3385-48ef-bd42-f606fba81ae7 |

#### [**Azure portal**](#tab/roles-portal-admin)

1. Sign in to the [Azure portal](https://portal.azure.com) and navigate to your search service.

1. From the left pane, select **Access control (IAM)**.

1. Select **+ Add** > **Add role assignment**.

   :::image type="content" source="media/search-security-rbac/portal-access-control.png" alt-text="Screenshot of the Access control (IAM) page for assigning service administration roles.":::

1. Select a role: **Owner**, **Contributor**, or **Reader**.

1. On the **Members** tab, select the Microsoft Entra user or group identity. If you're setting up permissions for another Azure service, select a system-assigned or user-assigned managed identity.

1. On the **Review + assign** tab, select **Review + assign** to assign the role.

#### [**PowerShell**](#tab/roles-powershell-admin)

When you [assign roles using PowerShell](/azure/role-based-access-control/role-assignments-powershell), call `New-AzRoleAssignment`, providing the Azure user or group name and the scope of the assignment.

This example creates a role assignment scoped to a search service:

```powershell
New-AzRoleAssignment -SignInName <email> `
    -RoleDefinitionName "Reader" `
    -Scope  "/subscriptions/<subscription>/resourceGroups/<resource-group>/providers/Microsoft.Search/searchServices/<search-service>"
```

**Reference:** [New-AzRoleAssignment](/powershell/module/az.resources/new-azroleassignment)

---

### Assign roles for development

The following roles let you create search objects, load documents, query indexes, and retrieve from knowledge bases. Assign all three roles to cover the full range of development tasks.

| Role | ID |
| -- | -- |
| [Search Service Contributor](#role-descriptions) | 7ca78c08-252a-4471-8644-bb5ff32d4ba0 |
| [Search Index Data Contributor](#role-descriptions) | 8ebe5a00-799e-43f5-93ac-243d3dce84a7 |
| [Search Index Data Reader](#role-descriptions) | 1407120a-92aa-4202-b7e9-c0e197c71c8f |

#### [**Azure portal**](#tab/roles-portal)

1. Sign in to the [Azure portal](https://portal.azure.com) and navigate to your search service.

1. From the left pane, select **Access control (IAM)**.

1. Select **+ Add** > **Add role assignment**.

   :::image type="content" source="media/search-security-rbac/portal-access-control.png" alt-text="Screenshot of the Access control (IAM) page for assigning development roles.":::

1. Select **Search Service Contributor**.

1. On the **Members** tab, select the Microsoft Entra user or group identity. If you're setting up permissions for another Azure service, select a system-assigned or user-assigned managed identity.

1. On the **Review + assign** tab, select **Review + assign** to assign the role.

1. Repeat these steps to assign **Search Index Data Contributor** and **Search Index Data Reader**.

#### [**PowerShell**](#tab/roles-powershell)

When you [assign roles using PowerShell](/azure/role-based-access-control/role-assignments-powershell), call `New-AzRoleAssignment`, providing the Azure user or group name and the scope of the assignment.

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

### Assign roles for read-only access

Use the following role for apps and processes that only need read access to indexes and knowledge bases. Supported operations include [search](/rest/api/searchservice/documents/search-post), [autocomplete](/rest/api/searchservice/documents/autocomplete-post), and [suggestions](/rest/api/searchservice/documents/suggest-post) for indexes and [retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve) for knowledge bases.

| Role | ID |
| -- | -- |
| [Search Index Data Reader](#role-descriptions) | 1407120a-92aa-4202-b7e9-c0e197c71c8f |

#### [**Azure portal**](#tab/roles-portal-query)

1. Sign in to the [Azure portal](https://portal.azure.com) and navigate to your search service.

1. From the left pane, select **Access control (IAM)**.

1. Select **+ Add** > **Add role assignment**.

   :::image type="content" source="media/search-security-rbac/portal-access-control.png" alt-text="Screenshot of the Access control (IAM) page for assigning read-only data access roles.":::

1. Select the **Search Index Data Reader** role.

1. On the **Members** tab, select the Microsoft Entra user or group identity. If you're setting up permissions for another Azure service, select a system-assigned or user-assigned managed identity.

1. On the **Review + assign** tab, select **Review + assign** to assign the role.

#### [**PowerShell**](#tab/roles-powershell-query)

When you [assign roles using PowerShell](/azure/role-based-access-control/role-assignments-powershell), call `New-AzRoleAssignment`, providing the Azure user or group name and the scope of the assignment.

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

Before you proceed, [configure your application for keyless connections](search-security-rbac-client-code.md) and have role assignments in place.

### [**Azure portal**](#tab/test-portal)

1. Sign in to the [Azure portal](https://portal.azure.com) and navigate to your search service.

1. From the left pane, select **Search management** > **Indexes** to test index-related permissions:

   + Search Service Contributors can create, modify, and delete search objects but can't load documents or run queries. To verify permissions, [create a search index](search-how-to-create-search-index.md#create-an-index).

   + Search Index Data Contributors can load documents. There's no load documents option in the Azure portal outside of the [**Import data** wizard](search-import-data-portal.md), but you can [reset and run an indexer](search-howto-run-reset-indexers.md) to confirm document load permissions.

   + Search Index Data Readers can query indexes. To verify permissions, use [Search explorer](search-explorer.md). You should be able to send queries and view results, but you shouldn't be able to view index definitions or create indexes.

### [**REST API**](#tab/test-rest)

This approach assumes Visual Studio Code with the [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client).

1. Open a command shell for Azure CLI and sign in to your Azure subscription.

   ```azurecli
   az login
   ```

1. Get your tenant ID and subscription ID. Use the ID as a variable in a future step. 

   ```azurecli
   az account show
   ```

1. Get an access token for the Azure AI Search data plane.

   ```azurecli
   az account get-access-token --scope https://search.azure.com/.default --query accessToken --output tsv
   ```

1. Paste these variables in a new text file in Visual Studio Code.

   ```http
   @baseUrl = PASTE-YOUR-SEARCH-SERVICE-URL-HERE
   @index-name = PASTE-YOUR-INDEX-NAME-HERE
   @token = PASTE-YOUR-TOKEN-HERE
   ```

1. Send a request that uses the variables you specify. For the Search Index Data Reader role, you can send a query using any [supported API version](/rest/api/searchservice/search-service-api-versions).

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

   **Reference:** [Search Documents](/rest/api/searchservice/documents/search-post)

   A successful query returns search results with matching documents. If the index is empty or has no matches, `value` contains an empty array.

    > [!TIP]
    > For more information on how to acquire a token for a specific environment, see [Manage an Azure AI Search service with REST APIs](search-manage-rest.md) and [Microsoft identity platform authentication libraries](/azure/active-directory/develop/reference-v2-libraries).
    
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

1. If you're using React, use `InteractiveBrowserCredential` for Microsoft Entra authentication to Azure AI Search. For more information, see [When to use `@azure/identity`](/javascript/api/overview/azure/identity-readme?view=azure-node-latest#when-to-use&preserve-view=true).

    **Reference:** [SearchClient](/javascript/api/@azure/search-documents/searchclient), [DefaultAzureCredential](/javascript/api/@azure/identity/defaultazurecredential)

### [**Java**](#tab/test-java)

1. Add the required dependencies to your `pom.xml`:

   ```xml
   <dependency>
     <groupId>com.azure</groupId>
     <artifactId>azure-search-documents</artifactId>
     <version>11.7.4</version>
   </dependency>
   <dependency>
     <groupId>com.azure</groupId>
     <artifactId>azure-identity</artifactId>
     <version>1.15.0</version>
   </dependency>
   ```

1. Use [Azure.Identity for Java](/java/api/overview/azure/identity-readme?view=azure-java-stable&preserve-view=true) for token authentication.

1. Use [DefaultAzureCredential](/java/api/overview/azure/identity-readme?view=azure-java-stable#defaultazurecredential&preserve-view=true) for apps that run on Azure.

---

<a name="rbac-single-index"></a>

## Grant access to a single index

In some scenarios, you might want to limit an application's access to a single resource, such as an index.

The Azure portal doesn't currently support role assignments at this level of granularity, but you can assign roles using [PowerShell](/azure/role-based-access-control/role-assignments-powershell) or the [Azure CLI](/azure/role-based-access-control/role-assignments-cli).

In PowerShell, use `New-AzRoleAssignment`, providing the Azure user or group name and the scope of the assignment.

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

   **Reference:** [New-AzRoleAssignment](/powershell/module/az.resources/new-azroleassignment)

## Create a custom role

If built-in roles don't provide the right combination of permissions, you can create a [custom role](/azure/role-based-access-control/custom-roles) to support the operations you require.

The following examples clone **Search Index Data Reader** and then add the ability to list indexes by name. Normally, listing the indexes on a search service is considered an administrative right.

### [**Azure portal**](#tab/custom-role-portal)

1. Sign in to the [Azure portal](https://portal.azure.com) and navigate to your search service.

1. From the left pane, select **Access control (IAM)**.

1. On the **Roles** tab, find **Search Index Data Reader** or another role, select the ellipsis (...), and then select **Clone**.

1. On the **Basics** tab, enter a name for the custom role, such as "Search Index Data Explorer", and then select **Next**.

1. On the **Permissions** tab, select **Add permissions**.

1. In the **Add permissions** pane, select the **Microsoft Search** tile.

1. With **Actions** selected at the top, set the following permissions:

   + Under `Microsoft.Search/operations`, select **Read : List all available operations**. 
   + Under `Microsoft.Search/searchServices/indexes`, select **Read : Read Index**.

1. Switch to **Data Actions** at the top, and under `Microsoft.Search/searchServices/indexes/documents`, select **Read : Read Documents**.

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

1. Select **Add** to close the pane.

1. Select **Review + create** to create the role.

   You can now assign users and groups to the role. For more information about these steps, see [Create or update Azure custom roles using the Azure portal](/azure/role-based-access-control/custom-roles-portal).

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

## Create a Conditional Access policy

If you need to enforce organizational policies, such as multifactor authentication, use [Microsoft Entra Conditional Access](/entra/identity/conditional-access/overview).

To create a Conditional Access policy for Azure AI Search:

1. Sign in to the [Azure portal](https://portal.azure.com).

1. Search for **Microsoft Entra Conditional Access**.

1. On the **Overview** page, select **Create new policy**.

1. Under **Cloud apps or actions**, add **Azure AI Search** as a cloud app, depending on how you want to set up your policy.

1. Update the remaining parameters of your policy. For example, specify which users and groups to which the policy applies. 

1. Save the policy.

> [!IMPORTANT]
> If your search service has a managed identity assigned to it, the specific search service appears as a cloud app. However, selecting that specific search service doesn't enforce the policy. Instead, select the general **Azure AI Search** cloud app to apply Conditional Access policies to your search service.

## Troubleshooting

When you develop applications that use role-based access control for authentication, you might encounter some common problems:

+ The default configuration for a search service is [key-based authentication](search-security-api-keys.md). If you don't change this setting to **Both** or **Role-based access control**, all requests that use role-based authentication are automatically denied, regardless of the underlying permissions.

+ If your request includes an API key alongside role-based credentials, the service authenticates using the key. Remove the API key from your request headers to use role-based authentication.

+ If the authorization token comes from a [managed identity](/entra/identity/managed-identities-azure-resources/overview) and you recently assigned the appropriate permissions, it [might take several hours](/entra/identity/managed-identities-azure-resources/managed-identity-best-practice-recommendations#limitation-of-using-managed-identities-for-authorization) for the permissions assignments to take effect.

+ If queries with document-level permissions don't return expected results, use Search Index Data Contributor or [create a custom role](#create-a-custom-role) with [elevated permissions](search-query-access-control-rbac-enforcement.md#elevated-permissions-for-investigating-incorrect-results) to investigate.

## Next step

This article explains how to assign roles for control and data plane operations on Azure AI Search. For comprehensive instructions on adding role-based access to your application code:

> [!div class="nextstepaction"]
> [Connect your app to Azure AI Search using identities](search-security-rbac-client-code.md)
