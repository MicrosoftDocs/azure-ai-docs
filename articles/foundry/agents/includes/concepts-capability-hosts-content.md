---
title: include file
description: include file
author: aahill
ms.author: aahi
ms.reviewer: fosteramanda
ms.service: microsoft-foundry
ms.topic: include
ms.date: 06/23/2026
ms.custom: include, classic-and-new
ai-usage: ai-assisted
---

> [!NOTE]
> Updating capability hosts is not supported. To modify a capability host, you must delete the existing one and recreate it with the new configuration.

Capability hosts are sub-resources that you configure at both the Microsoft Foundry account and Foundry project scopes. They tell Foundry Agent Service where to store and process agent data, including:
- **Conversation history** 
- **File uploads** 
- **Vector stores** 

## Prerequisites

- A [Microsoft Foundry project](../../how-to/create-projects.md)
- If you use your own resources for agent data (standard agent setup), create the required Azure resources and connections:
  - [Use your own resources](../how-to/use-your-own-resources.md)
  - [Add a new connection to your project](../../how-to/connections-add.md)
- Required permissions:
  - **Contributor** role on the Foundry account to create capability hosts
  - **User Access Administrator** or **Owner** role to assign access to Azure resources (for standard agent setup)
  - For details, see [Required permissions](../environment-setup.md#required-permissions) and [Role-based access control (RBAC) in Microsoft Foundry](../../concepts/rbac-foundry.md).

## Why use capability hosts?

Capability hosts let you **bring your own Azure resources** instead of using the default Microsoft-managed platform resources. This gives you:

- **Data sovereignty** - Keep all agent data within your Azure subscription.
- **Security control** - Use your own storage accounts, databases, and search services.
- **Compliance** - Meet specific regulatory or organizational requirements.

## How do capability hosts work?

Creating capability hosts isn't required. If you want agents to use your own Azure resources, create capability hosts at both the account and project scopes.

### Default behavior (Microsoft-managed resources)
If you don't create capability hosts, Agent Service automatically uses Microsoft-managed Azure resources for:
- Conversation storage (conversation history, agent definitions)
- File storage (uploaded documents) 
- Vector search (embeddings and retrieval)

### Bring-your-own resources
When you create capability hosts at both the account and project levels, your Azure resources store and process agent data. This is **standard agent setup**. For securing your agent service, see [Set up private networking for Foundry Agent Service](../how-to/virtual-networks.md).

To learn more about standard agent setup, see [Built-in enterprise readiness with standard agent setup](../concepts/standard-agent-setup.md).

> [!NOTE]
> We recommend using separate Foundry accounts and projects for standard agent setup and basic agent setup. Avoid mixing setup types within the same Foundry account.

#### Configuration hierarchy

Capability hosts operate at two distinct scopes:

1. **Service defaults** (Microsoft-managed search and storage) - Used when no capability host is configured.
2. **Account-level capability host** - Enables Agent Service at the account level.
3. **Project-level capability host** - Defines which BYO resources Agent Service uses for that specific project.

> [!IMPORTANT]
> The project-level capability host is what Agent Service reads to determine which storage, conversation, and vector store resources to use for a project. There's no automatic inheritance of BYO resource configuration from the account capability host to the project. Even if the account capability host references connections, Agent Service doesn't use them for a project unless those connections are explicitly referenced in a project capability host.

## Understand capability host constraints

When creating capability hosts, be aware of these important constraints to avoid conflicts:

- **One capability host per scope**: Each account and each project can have only one active capability host. If you try to create a second capability host with a different name at the same scope, you'll receive a 409 error.

- **You can't update configurations**: If you need to change configuration, delete the existing capability host and recreate it.

- **Account capability host prerequisite**: You can't create a project capability host unless an account-level capability host already exists.

## Create connections for capability hosts

Capability hosts reference connection names that you create in your Foundry account and project. Before you configure a project capability host for standard agent setup, create connections for resources that store agent data:

- **Conversation storage**: Azure Cosmos DB connection
- **File storage**: Azure Storage connection
- **Vector store**: Azure AI Search connection

If you want to use model deployments from your own Azure OpenAI resource, also create an Azure OpenAI connection.

To add connections in the Foundry portal, see [Add a new connection to your project](../../how-to/connections-add.md).

### Required connection properties

For Agent Service to correctly resolve and use your resources at runtime, each connection referenced by a capability host must have the following properties populated:

| Property | Description |
|----------|-------------|
| `authType` | The authentication type for the connection (for example, `AAD`) |
| `category` | The Azure resource type (for example, `AzureStorageAccount`, `AzureCosmosDb`, `CognitiveSearch`) |
| `target` | The service endpoint URL for the resource (not the resource ID) |
| `metadata.ResourceId` | The full Azure resource ID for the resource |

> [!IMPORTANT]
> The `metadata.ResourceId` field is required for Agent Service to correctly resolve your resources at runtime. This applies to both project-level and account-level connections referenced by a capability host.

The following example shows a correctly configured Azure Storage connection:

```json
{
  "properties": {
    "authType": "AAD",
    "category": "AzureStorageAccount",
    "target": "https://{storageAccountName}.blob.core.windows.net/",
    "metadata": {
      "ResourceId": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Storage/storageAccounts/{storageAccountName}"
    }
  }
}
```

> [!NOTE]
> While connection templates may include additional metadata fields, the functional requirements for correct resolution and runtime behavior are a valid `metadata.ResourceId` and the correctly populated `authType`, `category`, and `target` properties.

## Configure capability hosts

Currently, you manage capability hosts using the REST API. SDK support for capability host management isn't available.

### Required properties (project capability host)

To use your own resources for agent data (standard agent setup), configure the project capability host with the following properties:

| Property | Purpose | Required Azure resource | Example connection name |
|----------|---------|------------------------|------------------------|
| `threadStorageConnections` | Stores agent definitions and conversation history | Azure Cosmos DB | `"my-cosmosdb-connection"` |
| `vectorStoreConnections` | Handles vector storage for retrieval and search | Azure AI Search | `"my-ai-search-connection"` |
| `storageConnections` | Manages file uploads and blob storage | Azure Storage Account | `"my-storage-connection"` |

### Optional property

| Property | Purpose | Required Azure resource | When to use |
|----------|---------|------------------------|-------------|
| `aiServicesConnections` | Use your own model deployments | Azure OpenAI | When you want to use models from your existing Azure OpenAI resource instead of the built-in account level ones. |

**Account capability host**

Use an account capability host to enable Agent Service at the account level.

```http
PUT https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/capabilityHosts/{name}?api-version=2025-06-01

{
  "properties": {
    "capabilityHostKind": "Agents"
  }
}
```

Reference: [Foundry account management REST API](/rest/api/aifoundry/accountmanagement/operation-groups)

**Project capability host**

The project capability host is what Agent Service reads to determine which BYO resources to use for a project. All agents in this project will use the resources referenced here:

```http
PUT https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/projects/{projectName}/capabilityHosts/{name}?api-version=2025-06-01

{
  "properties": {
    "capabilityHostKind": "Agents",
    "threadStorageConnections": ["my-cosmos-db-connection"],
    "vectorStoreConnections": ["my-ai-search-connection"],
    "storageConnections": ["my-storage-account-connection"],
    "aiServicesConnections": ["my-azure-openai-connection"]
  }
}
```

Reference: [Project Capability Hosts - Create or update](/rest/api/aifoundry/accountmanagement/operation-groups)

### Optional: account-level connections with project capability hosts

You can also define connections at the account level. When a new project is created under that account, those connections are inherited by the project. However, the project capability host configuration is not inherited — you must still create a project capability host explicitly and reference the connections you want Agent Service to use for that project.

```http
PUT https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/capabilityHosts/{name}?api-version=2025-06-01

{
  "properties": {
    "capabilityHostKind": "Agents",
    "threadStorageConnections": ["shared-cosmosdb-connection"],
    "vectorStoreConnections": ["shared-ai-search-connection"],
    "storageConnections": ["shared-storage-connection"]
  }
}
```

> [!NOTE]
> Connections defined at the account level are inherited by new projects. However, the project capability host configuration is not inherited. To use those connections with Agent Service, you must create a project capability host that explicitly references the project-level connections.

## Verify your configuration

Use these steps to confirm that capability hosts are configured correctly:

1. Get the account capability host and confirm it exists.

   ```http
   GET https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/capabilityHosts?api-version=2025-06-01
   ```

2. Get the project capability host and confirm it references the expected connection names.

   ```http
   GET https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/projects/{projectName}/capabilityHosts?api-version=2025-06-01
   ```

3. Test your configuration by creating a test agent and running a conversation. Confirm that:
   - Conversations appear in your Azure Cosmos DB.
   - Uploaded files appear in your Azure Storage account
   - Vector data appears in your Azure AI Search index

4. If you update connections or want to change where data is stored, delete and recreate the capability hosts with the updated configuration.

## Delete capability hosts

> [!WARNING]
> Deleting a capability host affects all agents that depend on it. Make sure you understand the impact before proceeding. For example, if you delete the project and account capability host, agents in your project no longer have access to the files, conversations, and vector stores they previously accessed.

### Delete an account-level capability host

```http
DELETE https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/capabilityHosts/{name}?api-version=2025-06-01
```

### Delete a project-level capability host

```http
DELETE https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/projects/{projectName}/capabilityHosts/{name}?api-version=2025-06-01
```

## Troubleshooting

If you're experiencing issues when creating capability hosts, this section provides solutions to the most common problems and errors.

### HTTP 409 Conflict errors

#### Problem: Multiple capability hosts per scope

**Symptoms:** You receive a 409 Conflict error when trying to create a capability host, even though you believe the scope is empty.

**Error message:**
```json
{
  "error": {
    "code": "Conflict",
    "message": "There is an existing Capability Host with name: existing-host, provisioning state: Succeeded for workspace: /subscriptions/.../workspaces/my-workspace, cannot create a new Capability Host with name: new-host for the same ClientId."
  }
}
```

**Root cause:** Each account and each project can only have one active capability host. You're trying to create a capability host with a different name when one already exists at the same scope.

**Solution:**
1. **Check existing capability hosts** - Query the scope to see what already exists
2. **Use consistent naming** - Ensure you're using the same name across all requests for the same scope
3. **Review your requirements** - Determine if the existing capability host meets your needs

**Validation steps:**
Use the GET requests in [Verify your configuration](#verify-your-configuration) to confirm whether a capability host already exists at the target scope.

#### Problem: Concurrent operations in progress

**Symptoms:** You receive a 409 Conflict error indicating that another operation is currently running.

**Error message:**
```json
{
  "error": {
    "code": "Conflict", 
    "message": "Create: Capability Host my-host is currently in non creating, retry after its complete: /subscriptions/.../workspaces/my-workspace"
  }
}
```

**Root cause:** You're trying to create a capability host while another operation (update, delete, modify) is in progress at the same scope.

**Solution:**
1. **Wait for current operation to complete** - Check the status of ongoing operations
2. **Monitor operation progress** - Use the operations API to track completion
3. **Implement retry logic** - Use exponential backoff for temporary conflicts

**Operation monitoring:**
```http
GET https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.CognitiveServices/locations/{location}/operationResults/{operationId}?api-version=2025-06-01
```

### Best practices for conflict prevention

#### 1. Pre-request validation
Always verify the current state before making changes:
- Query existing capability hosts in the target scope
- Check for any ongoing operations
- Understand the current configuration

#### 2. Implement retry logic with exponential backoff
```csharp
try 
{
    var response = await CreateCapabilityHostAsync(request);
    return response;
}
catch (HttpRequestException ex) when (ex.Message.Contains("409"))
{
    if (ex.Message.Contains("existing Capability Host with name"))
    {
        // Handle name conflict - check if existing resource is acceptable
        var existing = await GetExistingCapabilityHostAsync();
        if (IsAcceptable(existing))
        {
            return existing; // Use existing resource
        }
        else
        {
            throw new InvalidOperationException("Scope already has a capability host with different name");
        }
    }
    else if (ex.Message.Contains("currently in non creating"))
    {
        // Handle concurrent operation - implement retry with backoff
        await Task.Delay(TimeSpan.FromSeconds(30));
        return await CreateCapabilityHostAsync(request); // Retry once
    }
}
```

#### 3. Understand idempotent behavior
The system supports idempotent create requests:
- **Same name + same configuration** → Returns existing resource (200 OK)
- **Same name + different configuration** → Returns 400 Bad Request  
- **Different name** → Returns 409 Conflict

#### 4. Configuration change workflow
Since updates aren't supported, follow this sequence for configuration changes:
1. Delete the existing capability host
2. Wait for deletion to complete  
3. Create a new capability host with the desired configuration

## Common scenarios

- **Development and testing**: Use Microsoft-managed resources. No capability host configuration needed.
- **Production with compliance requirements**: Create capability hosts with your own Azure Cosmos DB, Storage, and AI Search.
- **Shared resources across projects**: Configure account-level connections, then create a project capability host for each project that explicitly references those connections.

## Next steps

- [Standard agent setup](../concepts/standard-agent-setup.md)
- [Set up your environment](../environment-setup.md)
- [Add a new connection to your project](../../how-to/connections-add.md)
