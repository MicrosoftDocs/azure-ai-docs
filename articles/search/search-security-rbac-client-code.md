---
title: Configure apps for role-based security
description: Use keyless connections with an Azure Identity library for Microsoft Entra ID authentication and authorization with Azure AI Search.
ms.topic: how-to
ms.date: 01/20/2026
ms.service: azure-ai-search
ms.update-cycle: 180-days
author: HeidiSteen
ms.author: heidist
ms.custom: devx-track-dotnet, devx-track-extended-java, devx-track-js, devx-track-python, Keyless-dotnet, Keyless-java, Keyless-js, Keyless-python, build-2024-intelligent-apps, dev-focus
ai-usage: ai-assisted
#customer intent: As a developer, I want to use keyless connections so that I don't leak secrets.
---

# Connect your app to Azure AI Search using identities

In your application code, you can set up a keyless connection to Azure AI Search that uses Microsoft Entra ID and roles for authentication and authorization. Application requests to most Azure services must be authenticated with keys or keyless connections. Developers must be diligent to never expose the keys in an unsecure location. Anyone who gains access to the key is able to authenticate to the service. Keyless authentication offers improved management and security benefits over the account key because there's no key (or connection string) to store.

This article explains how to use `DefaultAzureCredential` in your application code.

To implement keyless connections in your code, follow these steps: 

* Enable role-based access on your search service
* Set environment variables, as needed. 
* Use an Azure Identity library credential type to create an Azure AI Search client object.

## Prerequisites

+ [Azure AI Search](search-create-service-portal.md), any region but it must be a billable tier (basic or higher).

+ [Role-based access enabled](search-security-enable-roles.md) on your search service.

+ Role assignments on Azure AI Search. Assign these roles to your identity:
  + **Search Service Contributor** and **Search Index Data Contributor** for local development (full access)
  + **Search Index Data Reader** for production read-only queries

  For step-by-step instructions, see [Assign roles for development](search-security-rbac.md#assign-roles-for-development).

## Install Azure Identity client library

To use a keyless approach, update your AI Search enabled code with the Azure Identity client library.

### [.NET](#tab/csharp)

Install the [Azure Identity client library for .NET](https://www.nuget.org/packages/Azure.Identity) and the [Azure Search Documents client library](https://www.nuget.org/packages/Azure.Search.Documents):

```dotnetcli
dotnet add package Azure.Identity
dotnet add package Azure.Search.Documents
```

### [Java](#tab/java)

Install the [Azure Identity client library for Java](https://mvnrepository.com/artifact/com.azure/azure-identity) and the [Azure Search Documents client library](https://mvnrepository.com/artifact/com.azure/azure-search-documents) with the following POM file:

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>com.azure</groupId>
            <artifactId>azure-identity</artifactId>
            <version>1.15.1</version>
        </dependency>
        <dependency>
            <groupId>com.azure</groupId>
            <artifactId>azure-search-documents</artifactId>
            <version>11.7.0</version>
        </dependency>
    </dependencies>
</dependencyManagement>
```

### [JavaScript](#tab/javascript)

Install the [Azure Identity client library for JavaScript](https://www.npmjs.com/package/@azure/identity) and the [Azure Search Documents client library](https://www.npmjs.com/package/@azure/search-documents):

```console
npm install --save @azure/identity @azure/search-documents
```

### [Python](#tab/python)

Install the [Azure Identity client library for Python](https://pypi.org/project/azure-identity/) and the [Azure Search Documents client library](https://pypi.org/project/azure-search-documents/):

```console
pip install azure-identity azure-search-documents
```

---

## Update source code to use DefaultAzureCredential

The Azure Identity library's `DefaultAzureCredential` allows you to run the same code in the local development environment and in the Azure cloud. Create a single credential and reuse the credential instance as needed to take advantage of token caching.

### [.NET](#tab/csharp)

For more information on `DefaultAzureCredential` for .NET, see [Azure Identity client library for .NET](/dotnet/api/overview/azure/identity-readme#defaultazurecredential). 

```csharp
using Azure;
using Azure.Search.Documents;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;
using Azure.Search.Documents.Models;
using Azure.Identity;
using System;
using static System.Environment;

string endpoint = GetEnvironmentVariable("AZURE_SEARCH_ENDPOINT");
string indexName = "my-search-index";

DefaultAzureCredential credential = new();
SearchClient searchClient = new(new Uri(endpoint), indexName, credential);
SearchIndexClient searchIndexClient = new(endpoint, credential);
```

**Reference:** [SearchClient](/dotnet/api/azure.search.documents.searchclient), [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient), [DefaultAzureCredential](/dotnet/api/azure.identity.defaultazurecredential)

### [Java](#tab/java)

For more information on `DefaultAzureCredential` for Java, see [Azure Identity client library for Java](/java/api/overview/azure/identity-readme#defaultazurecredential).

```java
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.search.documents.SearchAsyncClient;
import com.azure.search.documents.SearchClientBuilder;
import com.azure.search.documents.SearchDocument;
import com.azure.search.documents.indexes.SearchIndexAsyncClient;
import com.azure.search.documents.indexes.SearchIndexClientBuilder;

String ENDPOINT = System.getenv("AZURE_SEARCH_ENDPOINT");
String INDEX_NAME = "my-index";

DefaultAzureCredential credential = new DefaultAzureCredentialBuilder().build();

// Sync SearchClient
SearchClient searchClient = new SearchClientBuilder()
    .endpoint(ENDPOINT)
    .credential(credential)
    .indexName(INDEX_NAME)
    .buildClient();

// Sync IndexClient
SearchIndexClient searchIndexClient = new SearchIndexClientBuilder()
    .endpoint(ENDPOINT)
    .credential(credential)
    .buildClient();

// Async SearchClient
SearchAsyncClient searchAsyncClient = new SearchClientBuilder()
    .endpoint(ENDPOINT)
    .credential(credential)
    .indexName(INDEX_NAME)
    .buildAsyncClient();

// Async IndexClient
SearchIndexAsyncClient searchIndexAsyncClient = new SearchIndexClientBuilder()
    .endpoint(ENDPOINT)
    .credential(credential)
    .buildAsyncClient();
```

**Reference:** [SearchClient](/java/api/com.azure.search.documents.searchclient), [SearchIndexClient](/java/api/com.azure.search.documents.indexes.searchindexclient), [DefaultAzureCredential](/java/api/com.azure.identity.defaultazurecredential)

### [JavaScript](#tab/javascript)

For more information on `DefaultAzureCredential` for JavaScript, see [Azure Identity client library for JavaScript](/javascript/api/overview/azure/identity-readme#defaultazurecredential).


```javascript
import { DefaultAzureCredential } from "@azure/identity";
import {
  SearchClient,
  SearchIndexClient
} from "@azure/search-documents";

const AZURE_SEARCH_ENDPOINT = process.env.AZURE_SEARCH_ENDPOINT;
const index = "my-index";
const credential = new DefaultAzureCredential();

// To query and manipulate documents
const searchClient = new SearchClient(
  AZURE_SEARCH_ENDPOINT,
  index,
  credential
);

// To manage indexes and synonymmaps
const indexClient = new SearchIndexClient(
  AZURE_SEARCH_ENDPOINT, 
  credential
);
```

**Reference:** [SearchClient](/javascript/api/@azure/search-documents/searchclient), [SearchIndexClient](/javascript/api/@azure/search-documents/searchindexclient), [DefaultAzureCredential](/javascript/api/@azure/identity/defaultazurecredential)

### [Python](#tab/python)

For more information on `DefaultAzureCredential` for Python, see [Azure Identity client library for Python](/python/api/overview/azure/identity-readme#defaultazurecredential).

```python
import os
from azure.search.documents import SearchClient
from azure.identity import DefaultAzureCredential, AzureAuthorityHosts

# Azure Public Cloud
audience = "https://search.azure.com"
authority = AzureAuthorityHosts.AZURE_PUBLIC_CLOUD

service_endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]
credential = DefaultAzureCredential(authority=authority)

search_client = SearchClient(
    endpoint=service_endpoint, 
    index_name=index_name, 
    credential=credential, 
    audience=audience)

search_index_client = SearchIndexClient(
    endpoint=service_endpoint, 
    credential=credential, 
    audience=audience)
```

**Reference:** [SearchClient](/python/api/azure-search-documents/azure.search.documents.searchclient), [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient), [DefaultAzureCredential](/python/api/azure-identity/azure.identity.defaultazurecredential)

---

## Verify your connection

After setting up the client, verify your connection by running a simple operation. The following example lists indexes on your search service:

### [.NET](#tab/csharp)

```csharp
// List indexes to verify connection
var indexes = searchIndexClient.GetIndexNames();
foreach (var name in indexes)
{
    Console.WriteLine(name);
}
```

### [Java](#tab/java)

```java
// List indexes to verify connection
searchIndexClient.listIndexNames().forEach(System.out::println);
```

### [JavaScript](#tab/javascript)

```javascript
// List indexes to verify connection
for await (const name of indexClient.listIndexesNames()) {
  console.log(name);
}
```

### [Python](#tab/python)

```python
# List indexes to verify connection
for index in search_index_client.list_index_names():
    print(index)
```

---

A successful connection prints the names of your indexes (or an empty list if no indexes exist). If you receive an authentication error, verify that role-based access is enabled and your identity has the required role assignments.

The default authority is Azure public cloud. Custom `audience` values for sovereign or specialized clouds include:

* `https://search.azure.us` for Azure Government
* `https://search.azure.cn` for Azure operated by 21Vianet
* `https://search.microsoftazure.de` for Azure Germany

---

## Local development

Local development using roles includes these steps:

- Assign your personal identity to RBAC roles on the specific resource.
- Use a tool like the Azure CLI or Azure PowerShell to authenticate with Azure.
- Establish environment variables for your resource.

### Roles for local development

As a local developer, your Azure identity needs full control over data plane operations. These are the suggested roles:

- Search Service Contributor, create and manage objects
- Search Index Data Contributor, load and query an index

Find your personal identity with one of the following tools. Use that identity as the `<identity-id>` value.

#### [Azure CLI](#tab/azure-cli)

Replace placeholders `<role-name>`, `<identity-id>`, `<subscription-id>`, and `<resource-group-name>` with your actual values in the following commands.

1. Sign in to Azure CLI.

    ```azurecli
    az login
    ```

    A browser window opens for authentication. After successful sign-in, the terminal displays your subscription information.

2. Get your personal identity.

    ```azurecli
    az ad signed-in-user show \
        --query id -o tsv
    ```

    The command returns your user object ID (a GUID). Save this value for the next step.

3. Assign the role-based access control (RBAC) role to the identity for the resource group.  

    ```azurecli
    az role assignment create \
        --role "<role-name>" \
        --assignee "<identity-id>" \
        --scope "/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>"
    ```

    A successful assignment returns a JSON object with the role assignment details.

#### [Azure PowerShell](#tab/azure-powershell)

Replace placeholders `<role-name>`, `<identity-id>`, `<subscription-id>`, and `<resource-group-name>` with your actual values in the following commands.

1. Sign in with PowerShell.

    ```azurepowershell
    Connect-AzAccount
    ```

    A browser window opens for authentication. After successful sign-in, the terminal displays your account and subscription information.

2. Get your personal identity.

    ```azurepowershell
    (Get-AzContext).Account.ExtendedProperties.HomeAccountId.Split('.')[0]
    ```

    The command returns your user object ID (a GUID). Save this value for the next step.

3. Assign the role-based access control (RBAC) role to the identity for the resource group.  

    ```azurepowershell
    New-AzRoleAssignment -ObjectId "<identity-id>" -RoleDefinitionName "<role-name>" -Scope "/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>"
    ```

    A successful assignment returns the role assignment object with details including the `RoleAssignmentId`.

#### [Azure portal](#tab/portal)

1. Use the steps found here: [find the user object ID](/partner-center/find-ids-and-domain-names#find-the-user-object-id) in the Azure portal.

1. Use the steps found at [open the Add role assignment page](search-security-rbac.md) in the Azure portal.

---

### Authentication for local development

Use a tool in your local development environment to authentication to Azure identity. Once you're authenticated, the `DefaultAzureCredential` instance in your source code finds and uses your identity for authentication purposes.

Select a tool for [authentication during local development](/python/api/overview/azure/identity-readme#authenticate-during-local-development).

### Configure environment variables for local development

To connect to Azure AI Search, your code needs to know your resource endpoint. 

Create an environment variable named `AZURE_SEARCH_ENDPOINT` for your Azure AI Search endpoint. This URL generally has the format `https://<YOUR-RESOURCE-NAME>.search.windows.net/`.

## Production workloads

Deploy production workloads includes these steps:

- Choose RBAC roles that adhere to the principle of least privilege.
- Assign RBAC roles to your production identity on the specific resource.
- Set up environment variables for your resource.

### Roles for production workloads

To create your production resources, you need to create a [user-assigned managed identity](/entra/identity/managed-identities-azure-resources/how-manage-user-assigned-managed-identities?pivots=identity-mi-methods-azp#create-a-user-assigned-managed-identity) then assign that identity to your resources with the correct roles. 

The following role is suggested for a production application:

|Role name|Id|
|--|--|
|Search Index Data Reader|1407120a-92aa-4202-b7e9-c0e197c71c8f|

### Authentication for production workloads

Use the following Azure AI Search **Bicep template** to create the resource and set the authentication for the `identityId`. Bicep requires the role ID. The `name` shown in this Bicep snippet isn't the Azure role; it's specific to the Bicep deployment. 

```bicep
// main.bicep
param environment string = 'production'
param roleGuid string = ''

module aiSearchRoleUser 'core/security/role.bicep' = {
    scope: aiSearchResourceGroup
    name: 'aiSearch-role-user'
    params: {
        principalId: (environment == 'development') ? principalId : userAssignedManagedIdentity.properties.principalId 
        principalType: (environment == 'development') ? 'User' : 'ServicePrincipal'
        roleDefinitionId: roleGuid
    }
}
```

The `main.bicep` file calls the following generic Bicep code to create any role. You have the option to create multiple RBAC roles, such as one for the user and another for production. This allows you to enable both development and production environments within the same Bicep deployment.

```bicep
// core/security/role.bicep
metadata description = 'Creates a role assignment for an identity.'
param principalId string // passed in from main.bicep

@allowed([
    'Device'
    'ForeignGroup'
    'Group'
    'ServicePrincipal'
    'User'
])
param principalType string = 'ServicePrincipal'
param roleDefinitionId string // Role ID

resource role 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
    name: guid(subscription().id, resourceGroup().id, principalId, roleDefinitionId)
    properties: {
        principalId: principalId
        principalType: principalType
        roleDefinitionId: resourceId('Microsoft.Authorization/roleDefinitions', roleDefinitionId)
    }
}
```

### Configure environment variables for production workloads

To connect to Azure AI Search, your code needs to know your resource endpoint, and the ID of the managed identity. 

Create environment variables for your deployed and keyless Azure AI Search resource:

- `AZURE_SEARCH_ENDPOINT`: This URL is the access point for your Azure AI Search resource. This URL generally has the format `https://<YOUR-RESOURCE-NAME>.search.windows.net/`.   
- `AZURE_CLIENT_ID`: This is the identity to authenticate as.

## Troubleshoot common errors

| Error | Cause | Solution |
| ----- | ----- | -------- |
| `AuthenticationFailedException` | Missing or invalid credentials | Ensure you're signed in with `az login` (CLI) or `Connect-AzAccount` (PowerShell). Verify your Azure account has access to the subscription. |
| `403 Forbidden` | Identity lacks required role | Assign the appropriate role (Search Index Data Reader for queries, Search Index Data Contributor for indexing). Role assignments can take up to 10 minutes to propagate. |
| `401 Unauthorized` | RBAC not enabled on search service | Enable role-based access in the Azure portal under **Settings** > **Keys** > **Role-based access control**. |
| `ResourceNotFoundException` | Invalid endpoint or index name | Verify the `AZURE_SEARCH_ENDPOINT` environment variable matches your search service URL (format: `https://<service-name>.search.windows.net`). |
| `CredentialUnavailableException` | No valid credential found | `DefaultAzureCredential` tries multiple authentication methods. Ensure at least one is configured (Azure CLI, Visual Studio, environment variables). |

## Related content

* [Keyless connections developer guide](/azure/developer/intro/passwordless-overview)
* [Azure built-in roles](/azure/role-based-access-control/built-in-roles)
* [Set environment variables](/azure/ai-services/cognitive-services-environment-variables)
