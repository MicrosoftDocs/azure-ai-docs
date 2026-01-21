---
title: 'Learn what is a capability host'
titleSuffix: Microsoft Foundry
description: Learn how to create and delete capability hosts
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: conceptual
ms.date: 12/04/2025
author: aahill
ms.author: aahi
ms.reviewer: fosteramanda
monikerRange: 'foundry-classic || foundry'
---

# Capability hosts

[!INCLUDE [version-banner](../../includes/version-banner.md)]

> [!NOTE]
> Updating capability hosts is not supported. To modify a capability host, you must delete the existing one and recreate it with the new configuration.

Capability hosts are sub-resources that you define at both the Microsoft Foundry Account and Foundry project scopes. They specify where the Foundry Agent Service should store and process your agent data, including:
- **Conversation history (threads)** 
- **File uploads** 
- **Vector stores** 

## Why use capability hosts?

Capability hosts allow you to **bring your own Azure resources** instead of using the default Microsoft-managed platform resources. This gives you:

- **Data sovereignty** - Keep all agent data within your Azure subscription.
- **Security control** - Use your own storage accounts, databases, and search services.
- **Compliance** - Meet specific regulatory or organizational requirements.

## How do capability hosts work?

Creating capability hosts is not required. However if you do want agents to use your own resources, you must create a capability host on both the account and project. 

### Default behavior (Microsoft-managed resources)
If you don't create an account-level and project-level capability host, the Agent Service automatically uses Microsoft-managed Azure resources for:
- Thread storage (conversation history, agent definitions)
- File storage (uploaded documents) 
- Vector search (embeddings and retrieval)

### Bring-your-own resources
When you create capability hosts at both the account and project levels, all agent data is stored and processed using your own Azure resources within your subscription. This configuration is called a **standard agent setup**. For this set-up, all Foundry workspace resources should be in the same region as the VNet, including CosmosDB, Storage Account, AI Search, Foundry Account, Project, and Managed Identity.

> [!NOTE]
> When it comes to **standard agent set-up** versus the **basic agent set-up** with managed agent data resources, we recommend creating different Foundry resources for each set-up. If you want to create **standard agents** in Foundry, create your account and project capability host with the bring-your-own resources defined. If you want to create **basic agents** in Foundry, create your account and project capability host without bring-your-own resources defined. We do not recommend mixing both agent set-ups within one Foundry account. 

#### Configuration hierarchy

Capability hosts follow a hierarchy where more specific configurations override broader ones:

1. **Service defaults** (Microsoft-managed search and storage) - Used when no capability host is configured.
2. **Account-level capability host** - Provides shared defaults for all projects under the account.
3. **Project-level capability host** - Overrides account-level and service defaults for that specific project. 

## Understand capability host constraints

When creating capability hosts, be aware of these important constraints to avoid conflicts:

- **One capability host per scope**: Each account and each project can only have one active capability host. Attempting to create a second capability host with a different name at the same scope will result in a 409 conflict.

- **Configuration updates are not supported**: If you need to change configuration, you must delete the existing capability host and recreate it.

## Recommended setup 

### Required properties

A capability host must be configured with the following three properties at either the account or project level:

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
```http
PUT https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/capabilityHosts/{name}?api-version=2025-06-01

{
  "properties": {
    "capabilityHostKind": "Agents"
  }
}
```

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
    "aiServicesConnections": ["my-azure-openai-connection"]  // Optional
  }
}
```

### Optional: account-level defaults with project overrides

Set shared defaults at the account level that apply to all projects:

```http
PUT https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/capabilityHosts/{name}?api-version=2025-06-01

{
  "properties": {
    "capabilityHostKind": "Agents",

    // Optional: define shared BYO resources for every project. All foundry projects under this account will uses these Azure resources  
    "threadStorageConnections": ["shared-cosmosdb-connection"],
    "vectorStoreConnections": ["shared-ai-search-connection"],
    "storageConnections": ["shared-storage-connection"]
  }
}
```
> [!NOTE]
> All Foundry projects will inherit these settings. Then override specific settings at the project level as needed.

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
```http
# For account-level capability hosts
GET https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/capabilityHosts?api-version=2025-06-01

# For project-level capability hosts  
GET https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/projects/{projectName}/capabilityHosts?api-version=2025-06-01
```

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
3. **Implement retry logic** - Add exponential backoff for temporary conflicts

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


## Next steps
- Learn more about the [Standard Agent Setup](standard-agent-setup.md) 
- Get started with [Agent Service](../environment-setup.md)
