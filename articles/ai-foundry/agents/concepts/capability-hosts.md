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

Capability hosts are sub-resources that you define at both the Microsoft Foundry account and Foundry project scopes. They specify where the Foundry Agent Service stores and processes your agent data, including:
<!-- Tightened wording to reduce low-signal phrasing and improve readability. -->
- **Conversation history (threads)** 
- **File uploads** 
- **Vector stores** 

## Why use capability hosts?

Capability hosts allow you to **bring your own Azure resources** instead of using the default Microsoft-managed platform resources. This gives you:

- **Data sovereignty** - Keep all agent data within your Azure subscription.
- **Security control** - Use your own storage accounts, databases, and search services.
- **Compliance** - Meet specific regulatory or organizational requirements.

## How do capability hosts work?

Creating capability hosts is optional. To use your own resources, you must create a capability host at both the account and project levels.
<!-- Combined and tightened the conditional explanation into a single, clearer sentence. -->

### Default behavior (Microsoft-managed resources)
If you don't create an account-level and project-level capability host, the Agent Service automatically uses Microsoft-managed Azure resources for:
- Thread storage (conversation history, agent definitions)
- File storage (uploaded documents) 
- Vector search (embeddings and retrieval)

### Bring-your-own resources
When you create capability hosts at both the account and project levels, all agent data is stored and processed using your own Azure resources within your subscription. This configuration is called a **standard agent setup**.

All Foundry workspace resources should be in the same region as the VNet, including Cosmos DB, Storage accounts, Azure AI Search, Foundry accounts, projects, and managed identities.
<!-- Tightened list formatting and terminology for consistency with Microsoft style. -->

#### Configuration hierarchy

Capability hosts follow a hierarchy where more specific configurations override broader ones:

1. **Service defaults** (Microsoft-managed search and storage) - Used when no capability host is configured.
2. **Account-level capability host** - Provides shared defaults for all projects under the account.
3. **Project-level capability host** - Overrides account-level and service defaults for that specific project. 

## Understand capability host constraints

When creating capability hosts, be aware of these constraints to avoid conflicts:

- **One capability host per scope**: Each account and each project can have only one active capability host. Creating a second capability host with a different name at the same scope results in a 409 Conflict.

- **Configuration updates aren't supported**: To change the configuration, delete the existing capability host and recreate it.
<!-- Removed the earlier standalone note and consolidated this guidance here to eliminate duplicate note blocks. -->


## Recommended setup 

### Required properties

A capability host must be configured with the following three properties at either the account or project level:

| Property | Purpose | Required Azure resource | Example connection name |
|----------|---------|------------------------|------------------------|
| `threadStorageConnections` | Stores agent definitions, conversation history, and chat threads | Azure Cosmos DB | `"my-cosmosdb-connection"` |
| `vectorStoreConnections` | Handles vector storage for retrieval and search | Azure AI Search | `"my-ai-search-connection"` |
| `storageConnections` | Manages file uploads and blob storage | Azure Storage account | `"my-storage-connection"` |
<!-- Minor punctuation and capitalization adjustments for Microsoft style consistency. -->

### Optional property

| Property | Purpose | Required Azure resource | When to use |
|----------|---------|------------------------|-------------|
| `aiServicesConnections` | Use your own model deployments | Azure OpenAI | When you want to use models from your existing Azure OpenAI resource instead of the built-in account-level ones. |

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

This configuration overrides service defaults and any account-level settings. All agents in this project use your specified resources:
<!-- Tightened phrasing to remove low-signal future tense. -->
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

    // Optional: define shared BYO resources for every project. All Foundry projects under this account use these Azure resources  
    "threadStorageConnections": ["shared-cosmosdb-connection"],
    "vectorStoreConnections": ["shared-ai-search-connection"],
    "storageConnections": ["shared-storage-connection"]
  }
}
```
> [!NOTE]
> All Foundry projects inherit these settings. Override specific settings at the project level as needed.
<!-- Tightened inheritance explanation and removed redundant phrasing. -->

## Delete capability hosts

> [!WARNING]
> Deleting a capability host affects all agents that depend on it. Make sure you understand the impact before proceeding. For example, if you delete both the project-level and account-level capability hosts, agents in the project lose access to the files, threads, and vector stores they previously used.
<!-- Tightened warning language while preserving intent. -->

### Delete an account-level capability host

```http
DELETE https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/capabilityHosts/{name}?api-version=2025-06-01
```

### Delete a project-level capability host

```http
DELETE https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/projects/{projectName}/capabilityHosts/{name}?api-version=2025-06-01
```

## Troubleshooting

If you experience issues when creating capability hosts, this section provides solutions to common problems and errors.
<!-- Minor tightening for concision. -->

### HTTP 409 Conflict errors

#### Problem: Multiple capability hosts per scope

**Symptoms:** You receive a 409 Conflict error when you try to create a capability host, even though you believe the scope is empty.

**Error message:**
```json
{
  "error": {
    "code": "Conflict",
    "message": "There is an existing Capability Host with name: existing-host, provisioning state: Succeeded for workspace: /subscriptions/.../workspaces/my-workspace, cannot create a new Capability Host with name: new-host for the same ClientId."
  }
}
```

**Root cause:** Each account and project can have only one active capability host. You're trying to create a capability host with a different name when one already exists at the same scope.

**Solution:**
1. **Check existing capability hosts** - Query the scope to see what already exists.
2. **Use consistent naming** - Use the same name for all requests at the same scope.
3. **Review requirements** - Determine whether the existing capability host meets your needs.
<!-- Tightened list items for clarity and parallelism. -->

**Validation steps:**
```http
# For account-level capability hosts
GET https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/capabilityHosts?api-version=2025-06-01

# For project-level capability hosts  
GET https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/projects/{projectName}/capabilityHosts?api-version=2025-06-01
```

#### Problem: Concurrent operations in progress

**Symptoms:** You receive a 409 Conflict error indicating that another operation is running.

**Error message:**
```json
{
  "error": {
    "code": "Conflict", 
    "message": "Create: Capability Host my-host is currently in non creating, retry after its complete: /subscriptions/.../workspaces/my-workspace"
  }
}
```

**Root cause:** You're trying to create a capability host while another operation (create, delete, or modify) is in progress at the same scope.

**Solution:**
1. **Wait for the operation to complete** - Check the status of ongoing operations.
2. **Monitor progress** - Use the operations API to track completion.
3. **Implement retry logic** - Add exponential backoff for temporary conflicts.
<!-- Clarified operation types and tightened phrasing. -->

**Operation monitoring:**
```http
GET https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.CognitiveServices/locations/{location}/operationResults/{operationId}?api-version=2025-06-01
```

### Best practices for conflict prevention

#### 1. Pre-request validation
Verify the current state before making changes:
- Query existing capability hosts in the target scope.
- Check for ongoing operations.
- Understand the current configuration.
<!-- Tightened imperative phrasing. -->

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
        // Handle name conflict - check whether the existing resource is acceptable
        var existing = await GetExistingCapabilityHostAsync();
        if (IsAcceptable(existing))
        {
            return existing; // Use the existing resource
        }
        else
        {
            throw new InvalidOperationException("The scope already has a capability host with a different name.");
        }
    }
    else if (ex.Message.Contains("currently in non creating"))
    {
        // Handle concurrent operation - retry with backoff
        await Task.Delay(TimeSpan.FromSeconds(30));
        return await CreateCapabilityHostAsync(request); // Retry once
    }
}
```
<!-- Minor comment and punctuation adjustments for clarity. -->

#### 3. Understand idempotent behavior
The system supports idempotent create requests:
- **Same name + same configuration** → Returns the existing resource (200 OK).
- **Same name + different configuration** → Returns 400 Bad Request.  
- **Different name** → Returns 409 Conflict.
<!-- Added consistent punctuation. -->

#### 4. Configuration change workflow
Because updates aren't supported, use this sequence for configuration changes:
1. Delete the existing capability host.
2. Wait for deletion to complete.  
3. Create a new capability host with the desired configuration.
<!-- Tightened introductory clause. -->


## Next steps
- Learn more about the [Standard Agent Setup](standard-agent-setup.md) 
- Get started with [Agent Service](../environment-setup.md)