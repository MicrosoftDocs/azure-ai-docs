---
title: 'Learn what is a capability host'
titleSuffix: Azure AI Foundry
description: Learn how to create and delete capability hosts
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: conceptual
ms.date: 07/7/2025
author: fosteramanda
ms.author: fosteramanda
---

# Capability Hosts

> [!NOTE]
> Updating capability hosts is not supported. To modify a capability host, you must delete the existing one and recreate it with the new configuration.

Capability hosts are configuration sub-resources that you define at both the Azure AI Foundry Account and Foundry project scopes. They specify where the Azure AI Foundry Agent Service should store and process your agent data, including:
- **Conversation history (threads)** 
- **File uploads** 
- **Vector stores** 

## Why use capability hosts?

Capability hosts allow you to **bring your own Azure resources** instead of using the default on Microsoft-managed platform resources. This gives you:

- **Data sovereignty** - Keep all agent data within your Azure subscription
- **Security control** - Use your own storage accounts, databases, and search services
- **Compliance** - Meet specific regulatory or organizational requirements

## How capability hosts work

### Default behavior (Microsoft-managed resources)
If you don't create an account-level and project-level capability host, the Agent Service automatically uses Microsoft-managed Azure resources for:
- Thread storage (conversation history)
- File storage (uploaded documents) 
- Vector search (embeddings and retrieval)

### Bring-your-own resources
When you create capability hosts at both the Account and Project levels, all agent data is stored and processed using your own Azure resources within your subscription. This configuration is called the **Standard Agent Setup**.

## Configuration hierarchy

Capability hosts follow a hierarchy where more specific configurations override broader ones:

1. **Service defaults** (Microsoft-managed search and storage) - Used when no capability host is configured
2. **Account-level capability host** - Provides shared defaults for all projects under the account
3. **Project-level capability host** - Overrides account-level and service defaults for that specific project 

## Required properties

A capability host must be configured with the following three properties at either the account or project level:

| Property | Purpose | Required Azure Resource | Example Connection Name |
|----------|---------|------------------------|------------------------|
| `threadStorageConnections` | Stores conversation history and chat threads | Azure Cosmos DB | `"my-cosmosdb-connection"` |
| `vectorStoreConnections` | Handles vector storage for retrieval and search | Azure AI Search | `"my-ai-search-connection"` |
| `storageConnections` | Manages file uploads and blob storage | Azure Storage Account | `"my-storage-connection"` |

### Optional property

| Property | Purpose | Required Azure Resource | When to use |
|----------|---------|------------------------|-------------|
| `aiServicesConnections` | Use your own model deployments | Azure OpenAI | When you want to use models from your existing Azure OpenAI resource instead of shared ones |

## Recommended Setup 

**Account Capability Host**
```http
PUT https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/capabilityHosts/{name}?api-version=2025-06-01

{
  "properties": {
    "capabilityHostKind": "Agents"
  }
}
```
**Project Capability Host**

This configuration overrides service defaults and any account-level settings. All agents in this project will use your specified resources:
```http
PUT https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/projects/{projectName}/capabilityHosts/{name}?api-version=2025-06-01

{
  "properties": {
    "capabilityHostKind": "Agents",
    "threadStorageConnections": ["my-cosmos-db-connection"],
    "vectorStoreConnections": ["my-ai-search-connection"],
    "storageConnections": ["my-storage-account-connection"],
    "aiServicesConnections": ["my-aoai-connection"]  // Optional
  }
}
```

### Optional: Account-level defaults with project overrides

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
Note: all Foundry projects will inherit these setting. Then override specific settings at the project level as needed.

## Deleting capability hosts

> [!WARNING]
> Deleting a capability host will affect all agents that depend on it. Make sure you understand the impact before proceeding. For instance, if you delete a capability host, agents in your project will no longer have access to the files, thread, and vector stores it previously did.

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
- Get started wth [Agent Service](../environment-setup.md)