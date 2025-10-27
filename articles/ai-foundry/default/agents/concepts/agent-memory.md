---
title: Create and Manage Memory for AI Agents
ms.reviewer: liulewis
titleSuffix: Azure AI Foundry
description: Learn how to create and manage memory stores to enable AI agents to retain context across sessions and personalize user interactions.
#customer intent: As a developer, I want to attach a memory store to my AI agent so that it can access and update memories during interactions.
author: jonburchel
ms.author: jburchel
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 10/24/2025
ai-usage: ai-assisted
---

# Manage memory for AI agents

[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

Memory in Azure AI Foundry Agent Service is a managed, long-term memory solution that enables agent continuity across sessions, devices, and workflows. By creating memory stores and managing their content, you can build agents that retain user preferences, maintain conversation history, and deliver personalized experiences.

This article shows you how to create memory stores, attach them to agents, add and search memories, and implement best practices for security and privacy. With these capabilities, your agents can maintain context across multistep interactions and provide more reliable, personalized responses.

Memory stores act as persistent storage boundaries that define what types of information are relevant to each agent. You control access through scope parameters that segment memory across users, ensuring secure, isolated experiences.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/free/).
- Access to Azure AI Foundry with appropriate permissions to create and manage resources.
- An [Azure AI Foundry project](../../../how-to/create-projects.md).
- An [agent created in Azure AI Foundry](../../../agents/quickstart.md).
- Chat model deployment (for example, GPT-4) in your project.
- Embedding model deployment (for example, text-embedding-ada-002) in your project.
- Python 3.8 or later with the Azure AI Agent SDK installed, or access to the REST API.

## Understand memory types

Agent memory typically falls into two categories:

- **Short-term memory** tracks the current session's conversation, maintaining immediate context for ongoing interactions. Agent orchestration frameworks like [Microsoft Agent Framework](/agent-framework/overview/agent-framework-overview) typically manage this memory as part of the session context.

- **Long-term memory** retains distilled knowledge across sessions, enabling the model to recall and build on previous user interactions over time. This memory type requires integration with a persistent system that supports extraction, consolidation, and management of knowledge.

Azure AI Foundry memory is designed as a long-term memory solution. It extracts meaningful information from conversations, consolidates it into durable knowledge, and makes it available across sessions and agents.

## Create a memory store

Create a dedicated memory store for each agent to establish clear boundaries for memory access and optimization. When you create a memory store, specify the chat model and embedding model deployments that process and store memory content.

You must decide how to segment memory across users by specifying the `scope` parameter. By default, the system uses the end user's sign-in ID. To enable shared memory across users or groups, override this value with a team name, organization name, or other identifier that fits your use case.

# [Python](#tab/python)

```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MemoryStoreDefaultDefinition
from azure.identity import DefaultAzureCredential

# Initialize the client
client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str="<your-connection-string>"
)

# Create memory store
definition = MemoryStoreDefaultDefinition(
    chat_model="gpt-4",  # Your chat model deployment name
    embedding_model="text-embedding-ada-002"  # Your embedding model deployment name
)

memory_store = client.memory_stores.create_memory_store(
    name="my_memory_store",
    definition=definition,
    description="Memory store for customer support agent",
    metadata={"project": "customer-service", "environment": "production"}
)

print(f"Created memory store: {memory_store.id}")
```

# [REST API](#tab/rest)

```http
POST https://<your-resource>.api.azureml.ms/agents/v1.0/memoryStores
Content-Type: application/json
Authorization: Bearer <your-token>

{
  "name": "my_memory_store",
  "description": "Memory store for customer support agent",
  "definition": {
    "type": "default",
    "chatModel": "gpt-4",
    "embeddingModel": "text-embedding-ada-002"
  },
  "metadata": {
    "project": "customer-service",
    "environment": "production"
  }
}
```

---

The memory store creation returns an ID that you use in subsequent operations. Store this ID securely for reference.

## Attach a memory store to an agent

Attach the memory store to your agent to enable memory capabilities. Start with one memory store per agent to maximize memory protection and ensure optimization for your specific use case.

# [Python](#tab/python)

```python
# Attach memory store to agent
agent = client.agents.update_agent(
    agent_id="<your-agent-id>",
    memory_store_id=memory_store.id
)

print(f"Attached memory store to agent: {agent.id}")
```

# [REST API](#tab/rest)

```http
PATCH https://<your-resource>.api.azureml.ms/agents/v1.0/agents/<agent-id>
Content-Type: application/json
Authorization: Bearer <your-token>

{
  "memoryStoreId": "<memory-store-id>"
}
```

---

Once attached, the agent can access and update memories within the memory store according to the scope permissions you configure.

## Add memories to a memory store

Add memories by providing conversation content to the memory store. The system performs preprocessing and postprocessing, including memory extraction and consolidation, to optimize the agent's memory. This long-running operation might take about one minute to complete.

# [Python](#tab/python)

```python
from azure.ai.projects.models import ResponsesUserMessageItemParam

# Create conversation content
user_message = ResponsesUserMessageItemParam(
    content="I prefer dark roast coffee and usually drink it in the morning"
)

# Add memories (this is a long-running operation)
update_poller = client.memory_stores.begin_update_memories(
    memory_store_id=memory_store.id,
    scope="user_123",  # User identifier for memory isolation
    items=[user_message],
    update_delay=0  # Process immediately
)

# Wait for completion
update_result = update_poller.result()
print(f"Memory update completed")
print(f"Operations performed: {len(update_result.memory_operations)}")
print(f"Token usage: {update_result.usage}")
```

# [REST API](#tab/rest)

```http
POST https://<your-resource>.api.azureml.ms/agents/v1.0/memoryStores/<memory-store-id>/memories
Content-Type: application/json
Authorization: Bearer <your-token>

{
  "scope": "user_123",
  "items": [
    {
      "type": "userMessage",
      "content": "I prefer dark roast coffee and usually drink it in the morning"
    }
  ],
  "updateDelay": 0
}
```

---

The system extracts relevant information from the conversation items and consolidates it into durable memories. You can check the operation status by using the returned operation ID if needed.

## Search for memories in a memory store

Search memories to retrieve relevant context for agent interactions. Specify the memory store ID and scope to narrow down the search to specific users or groups. You can search within a particular conversation or across all memories for a scope.

# [Python](#tab/python)

```python
from azure.ai.projects.models import MemorySearchOptions

# Search memories by conversation
search_response = client.memory_stores.search_memories(
    memory_store_id=memory_store.id,
    scope="user_123",  # User namespace
    conversation_id="conv_456",  # Specific conversation to search
    options=MemorySearchOptions(limit=5)
)

print(f"Search completed (ID: {search_response.search_id})")
print(f"Found {len(search_response.memories)} memories")

for memory in search_response.memories:
    print(f"- {memory.content}")

# Perform incremental search using previous search ID
if search_response.search_id:
    incremental_search = client.memory_stores.search_memories(
        memory_store_id=memory_store.id,
        scope="user_123",
        previous_search_id=search_response.search_id,
        options=MemorySearchOptions(limit=3)
    )
    print(f"Incremental search: {len(incremental_search.memories)} more memories")
```

# [REST API](#tab/rest)

```http
POST https://<your-resource>.api.azureml.ms/agents/v1.0/memoryStores/<memory-store-id>/search
Content-Type: application/json
Authorization: Bearer <your-token>

{
  "scope": "user_123",
  "conversationId": "conv_456",
  "options": {
    "limit": 5
  }
}
```

---

Search operations return a search ID that you can use for incremental searches, allowing you to paginate through large result sets efficiently.

## Update a memory store

Update memory store properties, such as `name`, `description`, or `metadata`, to reflect changes in your application or organizational requirements.

# [Python](#tab/python)

```python
# Update memory store properties
updated_store = client.memory_stores.update_memory_store(
    memory_store_id=memory_store.id,
    name="updated_memory_store",
    description="Updated description for production use",
    metadata={
        "project": "customer-service",
        "environment": "production",
        "version": "2.0"
    }
)

print(f"Updated: {updated_store.name}")
```

# [REST API](#tab/rest)

```http
PATCH https://<your-resource>.api.azureml.ms/agents/v1.0/memoryStores/<memory-store-id>
Content-Type: application/json
Authorization: Bearer <your-token>

{
  "name": "updated_memory_store",
  "description": "Updated description for production use",
  "metadata": {
    "project": "customer-service",
    "environment": "production",
    "version": "2.0"
  }
}
```

---

Updates to the memory store don't affect existing memories but help you maintain clear organization and tracking across your application.

## List memory stores

Retrieve a list of memory stores in your project to manage and monitor your memory infrastructure.

# [Python](#tab/python)

```python
# List all memory stores
stores_list = client.memory_stores.list_memory_stores(limit=10)

print(f"Found {len(stores_list.data)} memory stores")
for store in stores_list.data:
    print(f"- {store.name} ({store.id})")
```

# [REST API](#tab/rest)

```http
GET https://<your-resource>.api.azureml.ms/agents/v1.0/memoryStores?limit=10
Authorization: Bearer <your-token>
```

---

Use the `limit` parameter to control pagination and efficiently manage large numbers of memory stores.

## Delete memories

Memories are organized by scope within a memory store. You can delete memories for a specific scope to remove user-specific data, or delete the entire memory store to remove all memories across all scopes.

### Delete memories by scope

Remove all memories associated with a particular user or group scope while preserving the memory store structure.

# [Python](#tab/python)

```python
# Delete memories for a specific scope
delete_scope_response = client.memory_stores.delete_memories(
    memory_store_id=memory_store.id,
    scope="user_123"
)

print(f"Deleted memories for scope: user_123")
```

# [REST API](#tab/rest)

```http
DELETE https://<your-resource>.api.azureml.ms/agents/v1.0/memoryStores/<memory-store-id>/scopes/user_123
Authorization: Bearer <your-token>
```

---

Use this operation to handle user data deletion requests or reset memory for specific users.

### Delete a memory store

Remove the entire memory store and all associated memories across all scopes. This operation is irreversible.

# [Python](#tab/python)

```python
# Delete the entire memory store
delete_response = client.memory_stores.delete_memory_store(memory_store.id)
print(f"Deleted memory store: {delete_response.deleted}")
```

# [REST API](#tab/rest)

```http
DELETE https://<your-resource>.api.azureml.ms/agents/v1.0/memoryStores/<memory-store-id>
Authorization: Bearer <your-token>
```

---

Before you delete a memory store, consider the impact on dependent agents. Agents with attached memory stores might lose access to historical context.

## Best practices

When you implement memory in your agents, consider the following practices:

- **Implement per-user access controls**: Avoid giving every agent access to all memory. Use the `scope` parameter to restrict who can see and update memories. For shared memory across agents or users, use the scope to instruct the memory system not to store personal information.
- **Minimize and protect sensitive data**: Store only what's necessary for your use case. If you must store sensitive data, such as personally identifiable information (PII), health data, or confidential business inputs, perform redaction and store only partial data.
- **Support privacy and compliance**: Implement mechanisms for users to access, export, correct, and delete their data. Support selective deletion of specific memory entries, not just full resets. Log deletions in a tamper-evident audit trail. Ensure your system supports GDPR, CCPA, HIPAA, and other relevant frameworks.
- **Segment data and isolate memory**: In multitenant or multiagent systems, segment memory logically and operationally. Allow customers to define, isolate, inspect, and delete their own memory footprint.
- **Monitor memory usage**: Track token usage and memory operations to understand costs and optimize performance. Set appropriate limits for memory storage and retrieval.
- **Version your memory stores**: Use metadata to track versions and configurations of memory stores, making it easier to manage updates and troubleshoot issues.

## Related content

- [Build an agent with Azure AI Foundry](../../../agents/quickstart.md)
- [Microsoft Agent Framework overview](/agent-framework/overview/agent-framework-overview)
- [Create a project in Azure AI Foundry](../../../how-to/create-projects.md)
