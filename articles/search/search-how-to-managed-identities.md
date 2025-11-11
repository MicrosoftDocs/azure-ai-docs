---
title: Configure a managed identity
titleSuffix: Azure AI Search
description: Create a managed identity for your search service, and use Microsoft Entra authentication and role-based-access controls for connections to other cloud services.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 08/27/2025
ms.update-cycle: 180-days
ms.custom:
  - ignite-2023
  - build-2024
  - sfi-ropc-nochange
---

# Configure a search service to connect using a managed identity

You can use Microsoft Entra ID security principals and role assignments for outbound connections from Azure AI Search to other Azure resources providing data, applied AI, or vectorization during indexing or queries.

To use roles on an outbound connection, first configure your search service to use either a [system-assigned or user-assigned managed identity](/azure/active-directory/managed-identities-azure-resources/overview) as the security principal for your search service in a Microsoft Entra tenant. Once you have a managed identity, you can assign roles for authorized access. Managed identities and role assignments eliminate the need for passing secrets and credentials in a connection string or code.

## Prerequisites

+ A search service at the [Basic tier or higher](search-sku-tier.md), any region.

+ An Azure resource that accepts incoming requests from a Microsoft Entra security principal that has a valid role assignment.

+ To create a managed identity, you must be an Owner or User Access Administrator roles. To assign roles, you must be an Owner, User Access Administrator, Role-based Access Control Administrator, or a member of a custom role with Microsoft.Authorization/roleAssignments/write permissions.

## Supported scenarios

You can use managed identities for these scenarios.

| Scenario | System  | User-assigned |
|----------|-------------------------|---------------------------------|
| [Connect to indexer data sources](search-indexer-overview.md) <sup>1</sup>| Yes | Yes <sup>2</sup>  |
| Connect to embedding and chat completion models in Azure OpenAI, Microsoft Foundry, and Azure Functions via skills/vectorizers <sup>3</sup> | Yes | Yes |
| [Connect to Azure Key Vault for customer-managed keys](search-security-manage-encryption-keys.md) | Yes | Yes |
| [Connect to Debug sessions (hosted in Azure Storage)](cognitive-search-debug-session.md)	<sup>1</sup> | Yes | No |
| [Connect to an enrichment cache (hosted in Azure Storage)](enrichment-cache-how-to-configure.md) <sup>1,</sup> <sup>4</sup> | Yes | Yes <sup>2</sup>|
| [Connect to a Knowledge Store (hosted in Azure Storage)](knowledge-store-create-rest.md) <sup>1</sup>| Yes | Yes <sup>2</sup>|

<sup>1</sup> For connectivity between search and storage, network security imposes constraints on which type of managed identity you can use. Only a system managed identity can be used for a same-region connection to Azure Storage, and that connection must be via the *trusted service exception* or resource instance rule. See [Access to a network-protected storage account](search-indexer-securing-resources.md#access-to-a-network-protected-storage-account) for details.

<sup>2</sup> User-assigned managed identities can be used in data source connection strings. However, only the newer preview REST APIs and preview packages support a user-assigned managed identity in a  connection string. Be sure to switch to a preview API if you set [SearchIndexerDataUserAssignedIdentity](/rest/api/searchservice/data-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true#searchindexerdatauserassignedidentity) as the `identity` in a data source connection.

<sup>3</sup> Connections to Azure OpenAI,  Foundry, and Azure Functions via skills/vectorizers include: [Custom skill](cognitive-search-custom-skill-interface.md), [Custom vectorizer](vector-search-vectorizer-custom-web-api.md), [Azure OpenAI embedding skill](cognitive-search-skill-azure-openai-embedding.md), [Azure OpenAI vectorizer](vector-search-how-to-configure-vectorizer.md), [AML skill](cognitive-search-aml-skill.md) and [Microsoft Foundry model catalog vectorizer](vector-search-vectorizer-azure-machine-learning-ai-studio-catalog.md).

<sup>4</sup> AI search service currently can't connect to tables on a storage account that has [shared key access turned off](/azure/storage/common/shared-key-authorization-prevent).

## Create a system managed identity

A system-assigned managed identity is a Microsoft Entra ID security principal that's automatically created and linked to an Azure resource, such as an Azure AI Search service.

You can have one system-assigned managed identity for each search service. It's unique to your search service and bound to the service for its lifetime. 

When you enable a system-assigned managed identity, Microsoft Entra ID creates a security principal for your search service that's used to authenticate to other Azure resources. You can then use this identity in role assignments for authorized access to data and operations.

### [**Azure portal**](#tab/portal-sys)

1. Sign in to the [Azure portal](https://portal.azure.com) and [find your search service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices).

1. From the left pane, select **Settings** > **Identity**.

1. On the **System assigned** tab, under **Status**, select **On**.

1. Select **Save**.

   :::image type="content" source="media/search-managed-identities/turn-on-system-assigned-identity.png" alt-text="Screenshot of the Identity page in Azure portal." border="true":::

   After you save the settings, the page updates to show an object identifier that's assigned to your search service.

   :::image type="content" source="media/search-managed-identities/system-assigned-identity-object-id.png" alt-text="Screenshot of a system identity object identifier." border="true":::

### [**Azure PowerShell**](#tab/ps-sys)

```azurepowershell
Set-AzSearchService `
  -Name YOUR-SEARCH-SERVICE-NAME `
  -ResourceGroupName YOUR-RESOURCE-GROUP-NAME `
  -IdentityType SystemAssigned
```

For more information, see [Create a search service with a system-assigned managed identity (Azure PowerShell](search-manage-powershell.md#create-a-service-with-a-system-assigned-managed-identity).

### [**Azure CLI**](#tab/cli-sys)

```azurecli
az search service update `
  --name YOUR-SEARCH-SERVICE-NAME `
  --resource-group YOUR-RESOURCE-GROUP-NAME `
  --identity-type SystemAssigned
```

For more information, see [Create a search service with a system-assigned managed identity (Azure CLI)](search-manage-azure-cli.md#create-a-service-with-a-system-assigned-managed-identity).

### [**REST API**](#tab/rest-sys)

Use [Services - Create Or Update (REST API)](/rest/api/searchmanagement/services/create-or-update#searchcreateorupdateservicewithidentity) to formulate the request.

```http
PUT https://management.azure.com/subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Search/searchServices/mysearchservice?api-version=2025-05-01  HTTP/1.1
{
  "location": "[region]",
  "sku": {
    "name": "[sku]"
  },
  "properties": {
    "replicaCount": [replica count],
    "partitionCount": [partition count],
    "hostingMode": "default"
  },
  "identity": {
    "type": "SystemAssigned"
  }
} 
```

The response includes a confirmation and an object identifier for the system-assigned managed identity.

---

## Create a user-assigned managed identity

A user-assigned managed identity is an Azure resource that can be scoped to subscriptions, resource groups, or resource types. 

You can create multiple user-assigned managed identities for more granularity in role assignments. For example, you might want separate identities for different applications and scenarios. As an independently created and managed resource, it's not bound to the service itself.

The steps for setting up a user-assigned managed identity are as follows:

+ In your Azure subscription, create a user-assigned managed identity.

+ On your search service, associate the user-assigned managed identity with your search service.

+ On other Azure services you want to connect to, create a role assignment for the identity.

Associating a user-assigned managed identity with an Azure AI Search service is supported in the Azure portal, Search Management REST APIs, and SDK packages that provide the feature.

### [**Azure portal**](#tab/portal-user)

1. Sign in to the [Azure portal](https://portal.azure.com).

1. In the upper-left corner of your dashboard, select **Create a resource**.

1. Use the search box to find **User Assigned Managed Identity**, and then select **Create**.

   :::image type="content" source="media/search-managed-identities/user-assigned-managed-identity.png" alt-text="Screenshot of the user assigned managed identity tile in Azure Marketplace.":::

1. Select the subscription, resource group, and region. Give the identity a descriptive name.

1. Select **Create** and wait for the resource to finish deploying.

   It takes several minutes before you can use the identity.

1. On your search service page, select **Settings** > **Identity**.

1. On the **User assigned** tab, select **Add**.

1. Select the subscription and the user-assigned managed identity you previously created.

### [**REST API**](#tab/rest-user)

Instead of the Azure portal, you can use the Search Management REST APIs to assign a user-assigned managed identity.

1. Use [Services - Update (REST API)](/rest/api/searchmanagement/services/update?view=rest-searchmanagement-2025-05-01&preserve-view=true#identity) to formulate the request.

    ```http
    PUT https://management.azure.com/subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Search/searchServices/mysearchservice?api-version=2025-05-01  HTTP/1.1
    {
      "location": "[region]",
      "sku": {
        "name": "[sku]"
      },
      "properties": {
        "replicaCount": [replica count],
        "partitionCount": [partition count],
        "hostingMode": "default"
      },
      "identity": {
        "type": "UserAssigned",
        "userAssignedIdentities": {
          "/subscriptions/[subscription ID]/resourcegroups/[name of resource group]/providers/Microsoft.ManagedIdentity/userAssignedIdentities/[name of managed identity]": {}
        }
      }
    } 
    ```

1. Set `identity.type` to the type of identity.

    + Valid values are `SystemAssigned`, `UserAssigned`, or `SystemAssigned, UserAssigned` for both.

    + A value of `None` clears any previously assigned identities from the search service.

1. Update `identity.userAssignedIdentities` to include the details of your user-assigned managed identity. This identity [must already exist](/azure/active-directory/managed-identities-azure-resources/how-manage-user-assigned-managed-identities) before you can specify it in the request.

---

## Assign a role

Once you have a managed identity, assign roles that determine search service permissions on the Azure resource. 

+ Read permissions are needed for indexer data connections and for accessing a customer-managed key in Azure Key Vault.

+ Write permissions are needed for AI enrichment features that use Azure Storage for hosting debug session data, enrichment caching, and long-term content storage in a knowledge store.

The following steps illustrate the role assignment workflow. This example is for Azure OpenAI. For other Azure resources, see [Connect to Azure Storage](search-howto-managed-identities-storage.md), [Connect to Azure Cosmos DB](search-howto-managed-identities-cosmos-db.md), or [Connect to  Azure SQL](search-howto-managed-identities-sql.md).

1. Sign in to the [Azure portal](https://portal.azure.com/) with your Azure account, and go to your Azure OpenAI resource.

1. Select **Access control** from the left menu.

1. Select **Add** and then select **Add role assignment**.

1. Under **Job function roles**, select [**Cognitive Services OpenAI User**](/azure/ai-services/openai/how-to/role-based-access-control#azure-openai-roles) and then select **Next**.

1. Under **Members**, select **Managed identity** and then select **Members**.

1. Filter by subscription and resource type (Search services), and then select the managed identity of your search service.

1. Select **Review + assign**.

## Connection string examples

Recall from the scenarios description that you can use managed identities in connection strings to other Azure resources. This section provides examples. You can use generally available REST API versions and Azure SDK packages for connections using a system-assigned managed identity.

> [!TIP]
> You can create most of these objects in the Azure portal, specifying either a system or user-assigned managed identity, and then view the JSON definition to get the connection string.

Here are some examples of connection strings for various scenarios.

[**Blob data source (system managed identity):**](search-howto-managed-identities-storage.md)

An indexer data source includes a `credentials` property that determines how the connection is made to the data source. The following example shows a connection string specifying the unique resource ID of a storage account. 

A system managed identity is indicated when a connection string is the unique resource ID of a Microsoft Entra ID-aware service or application. A user-assigned managed identity is specified through an `identity` property.

```json
"credentials": {
    "connectionString": "ResourceId=/subscriptions/{subscription-ID}/resourceGroups/{resource-group-name}/providers/Microsoft.Storage/storageAccounts/{storage-account-name};"
    }
```

[**Blob data source (user managed identity):**](search-howto-managed-identities-storage.md)

User-assigned managed identities can also be used in indexer data source connection strings. However, only the newer preview REST APIs and preview packages support a user-assigned managed identity in a data source connection string. Be sure to switch to a preview version if you set [SearchIndexerDataUserAssignedIdentity](/rest/api/searchservice/data-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true#searchindexerdatauserassignedidentity) as the identity in a data source connection.

A search service user identity is specified in the `identity `property.

```json
"credentials": {
    "connectionString": "ResourceId=/subscriptions/{subscription-ID}/resourceGroups/{resource-group-name}/providers/Microsoft.Storage/storageAccounts/{storage-account-name};"
    },
  . . .
"identity": {
    "@odata.type": "#Microsoft.Azure.Search.DataUserAssignedIdentity",
    "userAssignedIdentity": "/subscriptions/{subscription-ID}/resourceGroups/{resource-group-name}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{user-assigned-managed-identity-name}"
  }
```

[**Knowledge store:**](knowledge-store-create-rest.md)

A knowledge store definition includes a connection string to Azure Storage. The connection string is the unique resource ID of your storage account. Notice that the string doesn't include containers or tables in the path. These are defined in the embedded projection definition, not the connection string.

```json
"knowledgeStore": {
  "storageConnectionString": "ResourceId=/subscriptions/{subscription-ID}/resourceGroups/{resource-group-name}/providers/Microsoft.Storage/storageAccounts/storage-account-name};"
}
```

[**Enrichment cache:**](enrichment-cache-how-to-configure.md)

An indexer creates, uses, and remembers the container used for the cached enrichments. It's not necessary to include the container in the cache connection string. You can find the object ID on the **Identity** page of your search service in the Azure portal.

```json
"cache": {
  "enableReprocessing": true,
  "storageConnectionString": "ResourceId=/subscriptions/{subscription-ID}/resourceGroups/{resource-group-name}/providers/Microsoft.Storage/storageAccounts/{storage-account-name};"
}
```

[**Debug session:**](cognitive-search-debug-session.md)

A debug session runs in the Azure portal and takes a connection string when you start the session. You can paste a string similar to the following example.

```json
"ResourceId=/subscriptions/{subscription-ID}/resourceGroups/{resource-group-name}/providers/Microsoft.Storage/storageAccounts/{storage-account-name}/{container-name};",
```

[**Custom skill:**](cognitive-search-custom-skill-interface.md)

A [custom skill](cognitive-search-custom-skill-web-api.md) targets the endpoint of an Azure function or app hosting custom code. 

+ `uri` is the endpoint of the function or app. 

+ `authResourceId` tells the search service to connect using a managed identity, passing the application ID of the target function or app in the property.

```json
{
  "@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
  "description": "A custom skill that can identify positions of different phrases in the source text",
  "uri": "https://contoso.count-things.com",
  "authResourceId": "<Azure-AD-registered-application-ID>",
  "batchSize": 4,
  "context": "/document",
  "inputs": [ ... ],
  "outputs": [ ...]
}
```

## Connection examples for models

For connections made using managed identities, this section shows examples of connection information used by a search service to connect to a model on another resource. A connection through a system managed identity is transparent; the identity and roles are in place, and the connection succeeds if they are properly configured. In contrast, a user managed identity requires extra connection properties.

[**Azure OpenAI embedding skill**](cognitive-search-skill-azure-openai-embedding.md) and [**Azure OpenAI vectorizer:**](vector-search-how-to-configure-vectorizer.md)

 An Azure OpenAI embedding skill and vectorizer in AI Search target the endpoint of an Azure OpenAI hosting an embedding model. The endpoint is specified in the [Azure OpenAI embedding skill definition](cognitive-search-skill-azure-openai-embedding.md) and/or in the [Azure OpenAI vectorizer definition](vector-search-how-to-configure-vectorizer.md). 

The system-managed identity is used automatically if `"apikey"` and `"authIdentity"` are empty, as demonstrated in the following example. The `"authIdentity"` property is used for user-assigned managed identity only.

**System-managed identity example:**
 
```json
{
  "@odata.type": "#Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill",
  "description": "Connects a deployed embedding model.",
  "resourceUri": "https://url.openai.azure.com/",
  "deploymentId": "text-embedding-ada-002",
  "modelName": "text-embedding-ada-002",
  "inputs": [
    {
      "name": "text",
      "source": "/document/content"
    }
  ],
  "outputs": [
    {
      "name": "embedding"
    }
  ]
}
```

Here's a [vectorizer example](vector-search-how-to-configure-vectorizer.md) configured for a system-assigned managed identity. A vectorizer is specified in a search index.

```json
 "vectorizers": [
    {
      "name": "my_azure_open_ai_vectorizer",
      "kind": "azureOpenAI",
      "azureOpenAIParameters": {
        "resourceUri": "https://url.openai.azure.com",
        "deploymentId": "text-embedding-ada-002",
        "modelName": "text-embedding-ada-002"
      }
    }
  ]
```

**User-assigned managed identity example:**

A user-assigned managed identity is used if `"apiKey"` is empty and a valid `"authIdentity"` is provided.

```json
{
  "@odata.type": "#Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill",
  "description": "Connects a deployed embedding model.",
  "resourceUri": "https://url.openai.azure.com/",
  "deploymentId": "text-embedding-ada-002",
  "modelName": "text-embedding-ada-002",
  "inputs": [
    {
      "name": "text",
      "source": "/document/content"
    }
  ],
  "outputs": [
    {
      "name": "embedding"
    }
  ],
  "authIdentity": {
    "@odata.type": "#Microsoft.Azure.Search.DataUserAssignedIdentity",
    "userAssignedIdentity": "/subscriptions/<subscription_id>/resourcegroups/<resource_group>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<user-assigned-managed-identity-name>"
   }
}
```

Here's a [vectorizer example](vector-search-how-to-configure-vectorizer.md) configured for a user-assigned managed identity. A vectorizer is specified in a search index.

```json
 "vectorizers": [
    {
      "name": "my_azure_open_ai_vectorizer",
      "kind": "azureOpenAI",
      "azureOpenAIParameters": {
        "resourceUri": "https://url.openai.azure.com",
        "deploymentId": "text-embedding-ada-002",
        "modelName": "text-embedding-ada-002"
        "authIdentity": {
            "@odata.type": "#Microsoft.Azure.Search.DataUserAssignedIdentity",
            "userAssignedIdentity": "/subscriptions/<subscription_id>/resourcegroups/<resource_group>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<user-assigned-managed-identity-name>"
          }
      }
    }
  ]
```

## Check for firewall access

If your Azure resource is behind a firewall, make sure there's an inbound rule that admits requests from your search service and from the Azure portal.

+ For same-region connections to Azure Blob Storage or Azure Data Lake Storage Gen2, use a system managed identity and the [trusted service exception](search-indexer-howto-access-trusted-service-exception.md). Optionally, you can configure a [resource instance rule](/azure/storage/common/storage-network-security#grant-access-from-azure-resource-instances) to admit requests.

+ For all other resources and connections, [configure an IP firewall rule](search-indexer-howto-access-ip-restricted.md) that admits requests from Azure AI Search. See [Indexer access to content protected by Azure network security features](search-indexer-securing-resources.md) for details.

## See also

+ [Security overview](search-security-overview.md)
+ [AI enrichment overview](cognitive-search-concept-intro.md)
+ [Indexers overview](search-indexer-overview.md)
+ [Authenticate with Microsoft Entra ID](/azure/architecture/framework/security/design-identity-authentication)
+ [About managed identities (Microsoft Entra ID)](/azure/active-directory/managed-identities-azure-resources/overview)
