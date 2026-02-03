---
title: Capability hosts for Foundry Agent Service
titleSuffix: Microsoft Foundry
description: Learn how capability hosts route agent data to Microsoft-managed or your own Azure resources, and how to configure and troubleshoot them.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: concept-article
ms.date: 01/20/2026
author: aahill
ms.author: aahi
ms.reviewer: fosteramanda
monikerRange: 'foundry-classic || foundry'
ms.custom: pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
---

# Capability hosts

[!INCLUDE [version-banner](../../includes/version-banner.md)]

> [!NOTE]
> Updating capability hosts is not supported. To modify a capability host, you must delete the existing one and recreate it with the new configuration.

Capability hosts are sub-resources that you configure at both the Microsoft Foundry account and Foundry project scopes. They tell Foundry Agent Service where to store and process agent data, including:
- **Conversation history (threads)** 
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
- Thread storage (conversation history, agent definitions)
- File storage (uploaded documents) 
- Vector search (embeddings and retrieval)

### Bring-your-own resources
When you create capability hosts at both the account and project levels, your Azure resources store and process agent data. This is **standard agent setup**. For network-secured standard agent setup, deploy all related resources in the same region as your virtual network (VNet). For guidance, see [Create a new network-secured environment with user-managed identity](../how-to/virtual-networks.md).

To learn more about standard agent setup, see [Built-in enterprise readiness with standard agent setup](standard-agent-setup.md).

> [!NOTE]
> We recommend using separate Foundry accounts and projects for standard agent setup and basic agent setup. Avoid mixing setup types within the same Foundry account.

#### Configuration hierarchy

Capability hosts follow a hierarchy where more specific configurations override broader ones:

1. **Service defaults** (Microsoft-managed search and storage) - Used when no capability host is configured.
2. **Account-level capability host** - Provides shared defaults for all projects under the account.
3. **Project-level capability host** - Overrides account-level and service defaults for that specific project. 

## Understand capability host constraints

When creating capability hosts, be aware of these important constraints to avoid conflicts:

- **One capability host per scope**: Each account and each project can have only one active capability host. If you try to create a second capability host with a different name at the same scope, you get a 409 conflict.

- **You can't update configurations**: If you need to change configuration, delete the existing capability host and recreate it.

## Create connections for capability hosts

Capability hosts reference connection names that you create in your Foundry account and project. Before you configure a project capability host for standard agent setup, create connections for the resources that store agent data:

- **Thread storage**: Azure Cosmos DB connection
- **File storage**: Azure Storage connection
- **Vector store**: Azure AI Search connection

If you want to use model deployments from your own Azure OpenAI resource, also create an Azure OpenAI connection.

To add connections in the Foundry portal, see [Add a new connection to your project](../../how-to/connections-add.md).

## Configure capability hosts

Currently, you manage capability hosts using the REST API. SDK support for capability host management isn't available.

### Required properties (project capability host)

To use your own resources for agent data (standard agent setup), configure the project capability host with the following properties:

| Property | Purpose | Required Azure resource | Example connection name |
|----------|---------|------------------------|------------------------|
| `threadStorageConnections` | Stores agent definitions, conversation history and chat threads | Azure Cosmos DB | `"my-cosmosdb-connection"` |
| `vectorStoreConnections` | Handles vector storage for retrieval and search | Azure AI Search | `"my-ai-search-connection"` |
| `storageConnections` | Manages file uploads and blob storage | Azure Storage Account | `"my-storage-connection"` |

### Optional property

| Property | Purpose | Required Azure resource | When to use |
|----------|---------|------------------------|-------------|
| `aiServicesConnections` | Use your own model deployments | Azure OpenAI | When you want to use models from your existing Azure OpenAI resource instead of the built-in account level ones. |

**Account capability host**

Use an account capability host to enable Agent Service and (optionally) define defaults that projects can inherit.

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

This configuration overrides service defaults and any account-level settings. All agents in this project will use your specified resources:
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

Reference: [Project Capability Hosts - Create or update](/rest/api/aifoundry/accountmanagement/project-capability-hosts/create-or-update)

### Optional: account-level defaults with project overrides

Set shared defaults at the account level that apply to all projects:

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
> All Foundry projects will inherit these settings. Then override specific settings at the project level as needed.

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
   - Conversation threads appear in your Azure Cosmos DB
   - Uploaded files appear in your Azure Storage account
   - Vector data appears in your Azure AI Search index

4. If you update connections or want to change where data is stored, delete and recreate the capability hosts with the updated configuration.

## Delete capability hosts

> [!WARNING]
> Deleting a capability host will affect all agents that depend on it. Make sure you understand the impact before proceeding. For instance, if you delete the project and account capability host, agents in your project will no longer have access to the files, thread, and vector stores it previously did.

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
- **Shared resources across projects**: Configure account-level defaults, then override at the project level as needed.

## Next steps

- [Standard agent setup](standard-agent-setup.md)
- [Set up your environment](../environment-setup.md)
- [Add a new connection to your project](../../how-to/connections-add.md)
