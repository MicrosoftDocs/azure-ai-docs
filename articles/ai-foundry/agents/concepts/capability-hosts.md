---
title: 'Learn what is a capability host'
titleSuffix: Azure AI Foundry
description: Learn how to create and delete capability hosts
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: conceptual
ms.date: 07/07/2025
author: fosteramanda
ms.author: fosteramanda
---

# Capability hosts

> [!NOTE]
> Updating capability hosts is not supported. To modify a capability host, you must delete the existing one and recreate it with the new configuration.

Capability hosts are sub-resources that you define at both the Azure AI Foundry Account and Foundry project scopes. They specify where the Azure AI Foundry Agent Service should store and process your agent data, including:
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
If you don't create an account-level and project-level capability host, the Azure AI Foundry Agent Service automatically uses Microsoft-managed Azure resources for:
- Thread storage (conversation history)
- File storage (uploaded documents) 
- Vector search (embeddings and retrieval)

### Bring-your-own resources
When you create capability hosts at both the account and project levels, all agent data is stored and processed using your own Azure resources within your subscription. This configuration is called a **standard agent setup**.

#### Configuration hierarchy

Capability hosts follow a hierarchy where more specific configurations override broader ones:

1. **Service defaults** (Microsoft-managed search and storage) - Used when no capability host is configured.
2. **Account-level capability host** - Provides shared defaults for all projects under the account.
3. **Project-level capability host** - Overrides account-level and service defaults for that specific project. 

## Avoiding HTTP 409 (Conflict) errors

### Understanding capability host constraints

When creating capability hosts, be aware of these important constraints to avoid conflicts:

> [!IMPORTANT]
> **One capability host per scope**: Each account and each project can only have one active capability host. Attempting to create a second capability host with a different name at the same scope will result in a 409 conflict.

### Best practices to prevent conflicts

#### 1. **Pre-request validation**
Always check for existing capability hosts before attempting to create new ones:

**For account-level capability hosts:**
```http
GET https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/capabilityHosts?api-version=2025-06-01
```

#### 2. **Monitor long-running operations**
Capability host operations are asynchronous. Always monitor operation status:

```http
GET https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.CognitiveServices/locations/{location}/operationResults/{operationId}?api-version=2025-06-01
```

#### 4. **Handle idempotent requests correctly**
The system supports idempotent create requests:
- **Same name + same configuration** = Returns existing resource (success)
- **Same name + different configuration** = Returns 400 Bad Request
- **Different name** = Returns 409 Conflict

### Configuration update limitations

> [!WARNING]
> Configuration updates are not supported. If you need to change configuration, you must delete the existing capability host and recreate it.

**Error example:**
```json
{
  "error": {
    "code": "InvalidData",
    "message": "Update of capability is not currently supported. Please delete and recreate with the new configuration."
  }
}
```

**Recommended approach for configuration changes:**
1. Delete the existing capability host
2. Wait for deletion to complete
3. Create a new capability host with the desired configuration

## Recommended setup 

### Required properties

A capability host must be configured with the following three properties at either the account or project level:

| Property | Purpose | Required Azure resource | Example connection name |
|----------|---------|------------------------|------------------------|
| `threadStorageConnections` | Stores conversation history and chat threads | Azure Cosmos DB | `"my-cosmosdb-connection"` |
| `vectorStoreConnections` | Handles vector storage for retrieval and search | Azure AI Search | `"my-ai-search-connection"` |
| `storageConnections` | Manages file uploads and blob storage | Azure Storage Account | `"my-storage-connection"` |

### Optional property

| Property | Purpose | Required Azure resource | When to use |
|----------|---------|------------------------|-------------|
| `aiServicesConnections` | Use your own model deployments | Azure OpenAI | When you want to use models from your existing Azure OpenAI resource instead of the built-in account level ones. |

### Account capability host
Create an account-level capability host that provides shared defaults:

```http
PUT https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/capabilityHosts/{name}?api-version=2025-06-01

{
  "properties": {
    "capabilityHostKind": "Agents"
  }
}
```

### Project capability host
Create a project-level capability host that overrides service defaults and any account-level settings:

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

### Example URLs from your environment:

**Account-level capability host:**
```
https://management.azure.com/subscriptions/b17253fa-f327-42d6-9686-f3e553e24763/resourceGroups/howie-cap-1/providers/Microsoft.CognitiveServices/accounts/foundyav3b/capabilityHosts/caphostaccount?api-version=2025-06-01
```

**Project-level capability host:**
```
https://management.azure.com/subscriptions/b17253fa-f327-42d6-9686-f3e553e24763/resourceGroups/howie-cap-1/providers/Microsoft.CognitiveServices/accounts/foundyav3b/projects/projectav3b/capabilityHosts/caphostproj?api-version=2025-06-01
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
> All Azure AI Foundry projects will inherit these settings. Then override specific settings at the project level as needed.

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

### Common 409 conflict scenarios

#### 1. **Multiple capability hosts per scope**

**What happens:** You try to create a capability host with a different name when one already exists at the same scope (account or project level).

**Error example:**
```json
{
  "error": {
    "code": "Conflict",
    "message": "There is an existing Capability Host with name: existing-host, provisioning state: Succeeded for workspace: /subscriptions/.../workspaces/my-workspace, cannot create a new Capability Host with name: new-host for the same ClientId."
  }
}
```

**How to avoid:**
- **Check existing capability hosts first** before creating new ones
- **Use consistent naming** across all requests for the same scope
- **Query existing resources** to understand current state

#### 2. **Concurrent operations** 

**What happens:** You try to create a capability host while another operation (update, delete, modify) is in progress at the same scope.

**Error example:**
```json
{
  "error": {
    "code": "Conflict", 
    "message": "Create: Capability Host my-host is currently in non creating, retry after its complete: /subscriptions/.../workspaces/my-workspace"
  }
}
```

**How to avoid:**
- **Monitor operation status** before making new requests
- **Wait for operations to complete** before starting new ones

### Error handling patterns

#### For Application Developers:

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
        // Different name conflict - check if existing resource meets your needs
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
        // Resource busy - implement retry
        await Task.Delay(TimeSpan.FromSeconds(30));
        return await CreateCapabilityHostAsync(request); // Retry
    }
}
```

#### For CLI/PowerShell Users:

```bash
# Check for existing account-level capability hosts first
az cognitiveservices account capability-host list \
  --account-name myaccount \
  --resource-group myrg

# Check for existing project-level capability hosts
az cognitiveservices account project capability-host list \
  --account-name myaccount \
  --project-name myproject \
  --resource-group myrg

# If none exist, create new one at account level
az cognitiveservices account capability-host create \
  --account-name myaccount \
  --resource-group myrg \
  --capability-host-name myhost \
  --kind Agents

# If creation fails with 409, check operation status
az cognitiveservices account capability-host show \
  --account-name myaccount \
  --resource-group myrg \
  --capability-host-name myhost
```

### Troubleshooting

To minimize 409 conflicts when creating capability hosts:

- **Check existing capability hosts** at both account and project levels before creating new ones
- **Use consistent naming** within the same scope (account or project)
- **Implement exponential backoff retry logic** for busy resources
- **Monitor long-running operations** before making new requests
- **Leverage idempotent behavior** for identical requests
- **Don't attempt configuration updates** - delete and recreate instead
- **Monitor operation status** using the operations API
- **Handle error responses** appropriately based on conflict type
- **Understand the scope** - account vs project level capability hosts serve different purposes

Following these practices will significantly reduce 409 conflicts and provide a better experience for your users.

## Next steps
- Learn more about the [Standard Agent Setup](standard-agent-setup.md) 
- Get started with [Agent Service](../environment-setup.md)
