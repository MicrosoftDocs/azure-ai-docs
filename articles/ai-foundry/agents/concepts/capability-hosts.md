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

### Common 409 conflict scenarios

#### 1. **Multiple capability hosts per scope** ?

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
- ? **Check existing capability hosts first** before creating new ones
- ? **Use consistent naming** across all requests for the same scope
- ? **Query existing resources** to understand current state

#### 2. **Concurrent operations** ?

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
- ? **Monitor operation status** before making new requests
- ? **Implement retry logic** with exponential backoff
- ? **Wait for operations to complete** before starting new ones

### Best practices to prevent conflicts

#### 1. **Pre-request validation**
Always check for existing capability hosts before attempting to create new ones:

**For account-level capability hosts:**
```http
GET https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/capabilityHosts?api-version=2025-06-01
```

**For project-level capability hosts:**
```http
GET https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/projects/{projectName}/capabilityHosts?api-version=2025-06-01
```

#### 2. **Implement proper retry logic**
For 409 conflicts due to concurrent operations, implement exponential backoff:

```python
import time
import random

def create_capability_host_with_retry(max_retries=3):
    for attempt in range(max_retries):
        try:
            return create_capability_host()
        except requests.HTTPError as e:
            if e.response.status_code == 409 and "currently in non creating" in e.response.text:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(wait_time)
                continue
            else:
                raise  # Different type of conflict, don't retry
    raise Exception("Max retries exceeded")
```

#### 3. **Monitor long-running operations**
Capability host operations are asynchronous. Always monitor operation status:

```http
GET https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.CognitiveServices/locations/{location}/operationResults/{operationId}?api-version=2025-06-01
```

#### 4. **Handle idempotent requests correctly**
The system supports idempotent create requests:
- ? **Same name + same configuration** = Returns existing resource (success)
- ? **Same name + different configuration** = Returns 400 Bad Request
- ? **Different name** = Returns 409 Conflict

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

## Next steps
- Learn more about the [Standard Agent Setup](standard-agent-setup.md) 
- Get started with [Agent Service](../environment-setup.md)
