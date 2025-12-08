---
title: Create and manage memory in Foundry Agent Service (preview)
ms.reviewer: liulewis
titleSuffix: Microsoft Foundry
description: Learn how to create and manage memory (preview) in Foundry Agent Service to enable AI agents to retain context across sessions and personalize user interactions.
#customer intent: As a developer, I want to attach a memory store to my AI agent so that it can access and update memories during interactions.
author: jonburchel
ms.author: jburchel
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 11/20/2025
ai-usage: ai-assisted
---

# Manage memory in Foundry Agent Service (preview)

> [!IMPORTANT]
> Memory (preview) in Foundry Agent Service and the Memory Store API (preview) are licensed to you as part of your Azure subscription and are subject to terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/product/ForOnlineServices/all) and the [Microsoft Products and Services Data Protection Addendum](https://aka.ms/DPA), as well as the Microsoft Generative AI Services Previews terms in the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

Memory in Foundry Agent Service (preview) is a managed, long-term memory solution. It enables agent continuity across sessions, devices, and workflows. By creating and managing memory stores, you can build agents that retain user preferences, maintain conversation history, and deliver personalized experiences.

This article explains how to create memory stores, add and search memories, and follow best practices for security and privacy. Memory stores act as persistent storage, defining which types of information are relevant to each agent. You control access using the `scope` parameter, which segments memory across users to ensure secure and isolated experiences.

## Common memory use cases

The following examples illustrate how memory can enhance various types of agents.

**Conversational agent**

- A customer support agent that remembers your name, previous issues and resolutions, ticket numbers, and your preferred contact method (chat, email, or call back). This memory lets you avoid repeating information, so conversations are more efficient and satisfying.
- A personal shopping assistant that remembers your size in specific brands, preferred colors, past returns, and recent purchases. The agent can suggest relevant items as soon as you start a session and avoids recommending products you already own.

**Planning agent**

- A travel agent that knows your flight preferences (window or aisle), seat selections, food choices, nonstop versus connecting flights, loyalty programs, and feedback from past trips. The agent uses this information to quickly build an optimized itinerary.
- An architectural design agent that remembers local building codes, material costs from previous bids, and initial client feedback. The agent refines designs iteratively, ensuring the final plan is feasible and meets all requirements.

**Research agent**

- A medical research agent that remembers which compounds were previously tested and failed, key findings from different labs, and complex relationships between proteins. The agent uses this knowledge to suggest new, untested research hypotheses.

## Understand memory types

Agent memory falls into two categories:

- **Short-term memory** tracks the current session's conversation and maintains immediate context for ongoing interactions. Agent orchestration frameworks, like [Microsoft Agent Framework](/agent-framework/overview/agent-framework-overview), typically manage this memory as part of the session context.

- **Long-term memory** retains distilled knowledge across sessions. The model can recall and build on previous user interactions over time. Long-term memory requires a persistent system that extracts, consolidates, and manages knowledge.

Foundry memory is designed for long-term memory. It extracts meaningful information from conversations, consolidates it into durable knowledge, and makes it available across sessions.

## Understand scope

The `scope` parameter controls how memory is partitioned. Each scope in the memory store keeps an isolated collection of memory items. For example, if you create a customer support agent with memory, each customer should have their own individual memory.

As a developer, you choose the key used to store and retrieve memory items, such as a UUID or a unique user ID in your system.

## Customize memory

Customize what information the agent stores to keep memory efficient, relevant, and privacy-respecting. Use the `user_profile_details` parameter to specify the types of data that are critical to the agent's function.

For example, set `user_profile_details` to prioritize "flight carrier preference and dietary restrictions" for a travel agent. This focused approach helps the memory system know which details to extract, summarize, and commit to long-term memory.

You can also use this parameter to exclude certain types of data, keeping memory lean and compliant with privacy requirements. For example, set `user_profile_details` to "avoid irrelevant or sensitive data (age, financials, precise location, credentials, etc.)."

## Current limitations and quotas

- Memory works only with Azure OpenAI models.
- You must set the `scope` value explicitly. Currently, the value can't be populated from the user identity specified in the request header isn't supported yet.
- In this preview, the following limits apply:
  - Maximum scopes per memory store: 100
  - Maximum memories per scope: 10,000
  - Search memories: 1,000 requests per minute
  - Update memories: 1,000 requests per minute

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- Access to Microsoft Foundry with appropriate permissions to create and manage resources.
- A [Microsoft Foundry project](../../../how-to/create-projects.md). Ensure your project's managed identity has the **Azure AI User** role on its parent resource, which allows the memory runtime to invoke your model deployments for memory-related operations.
- [Chat model deployment](../../../foundry-models/how-to/create-model-deployments.md) (for example, `gpt-4.1`) in your project.
- [Embedding model deployment](../../../openai/tutorials/embeddings.md) (for example, `text-embedding-3-small`) in your project.
- Python 3.8 or later with [configured environment](../../../quickstarts/get-started-code.md?tabs=python), or access to the REST API.

## Create a memory store

Create a dedicated memory store for each agent to establish clear boundaries for memory access and optimization. When you create a memory store, specify the chat model and embedding model deployments that process your memory content.

# [Python](#tab/python)

```python
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MemoryStoreDefaultDefinition, MemoryStoreDefaultOptions
from azure.identity import DefaultAzureCredential

# Initialize the client
client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential()
)

# Create memory store
definition = MemoryStoreDefaultDefinition(
    chat_model="gpt-4.1",  # Your chat model deployment name
    embedding_model="text-embedding-3-small",  # Your embedding model deployment name
    options=MemoryStoreDefaultOptions(user_profile_enabled=True, chat_summary_enabled=True)
)

memory_store = client.memory_stores.create(
    name="my_memory_store",
    definition=definition,
    description="Memory store for customer support agent",
)

print(f"Created memory store: {memory_store.name}")
```

# [REST API](#tab/rest)

```bash
# Configuration
ENDPOINT="https://{your-ai-services-account}.services.ai.azure.com/api/projects/{project-name}"
API_VERSION="2025-11-15-preview"
ACCESS_TOKEN="your-access-token-here"

curl -X POST "${ENDPOINT}/memory_stores?api-version=${API_VERSION}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my_memory_store",
    "description": "Memory store for customer support agent",
    "definition": {
      "kind": "default",
      "chat_model": "gpt-4.1",
      "embedding_model": "text-embedding-3-small",
      "options": {
        "user_profile_enabled": true,
        "chat_summary_enabled": true
      }
    }
  }'
```

---

## Add memories to a memory store

Add memories by providing conversation content to the memory store. The system preprocesses and postprocesses the data, including memory extraction and consolidation, to optimize the agent's memory. This long-running operation might take about one minute.

Decide how to segment memory across users by specifying the `scope` parameter. You can scope the memory to a specific end user, a team, or another identifier.

You can update a memory store with content from multiple conversation turns, or update after each turn and chain updates using the previous update operation ID.

# [Python](#tab/python)

```python
from azure.ai.projects.models import ResponsesUserMessageItemParam

# Set scope to associate the memories with
scope = "user_123"

user_message = ResponsesUserMessageItemParam(
    content="I prefer dark roast coffee and usually drink it in the morning"
)

update_poller = client.memory_stores.begin_update_memories(
    name="my_memory_store",
    scope=scope,
    items=[user_message],  # Pass conversation items that you want to add to memory
    update_delay=0,  # Trigger update immediately without waiting for inactivity
)

# Wait for the update operation to complete, but can also fire and forget
update_result = update_poller.result()
print(f"Updated with {len(update_result.memory_operations)} memory operations")
for operation in update_result.memory_operations:
    print(
        f"  - Operation: {operation.kind}, Memory ID: {operation.memory_item.memory_id}, Content: {operation.memory_item.content}"
    )

# Extend the previous update with another update and more messages
new_message = ResponsesUserMessageItemParam(content="I also like cappuccinos in the afternoon")
new_update_poller = client.memory_stores.begin_update_memories(
    name="my_memory_store",
    scope=scope,
    items=[new_message],
    previous_update_id=update_poller.update_id,  # Extend from previous update ID
    update_delay=0,  # Trigger update immediately without waiting for inactivity
)
new_update_result = new_update_poller.result()
for operation in new_update_result.memory_operations:
    print(
        f"  - Operation: {operation.kind}, Memory ID: {operation.memory_item.memory_id}, Content: {operation.memory_item.content}"
    )
```

# [REST API](#tab/rest)

```bash
# Configuration
ENDPOINT="https://{your-ai-services-account}.services.ai.azure.com/api/projects/{project-name}"
API_VERSION="2025-11-15-preview"
ACCESS_TOKEN="your-access-token-here"

curl -X POST "${ENDPOINT}/memory_stores/my_memory_store:update_memories?api-version=${API_VERSION}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "scope": "user_123",
    "items": [
      {
        "type": "message",
        "role": "user",
        "content": [
          {
            "type": "input_text",
            "text": "I prefer dark roast coffee and usually drink it in the morning"
          }
        ]
      }
    ],
    "update_delay": 0
  }'

# Get add memory status by polling the update_id
# Use the "update_id" from previous response
UPDATE_ID=<your_update_id>
curl -X GET "${ENDPOINT}/memory_stores/my_memory_store/updates/${UPDATE_ID}?api-version=${API_VERSION}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

---

## Search for memories in a memory store

Search memories to retrieve relevant context for agent interactions. Specify the memory store name and scope to narrow the search.

# [Python](#tab/python)

```python
from azure.ai.projects.models import MemorySearchOptions

# Search memories by a query
query_message = ResponsesUserMessageItemParam(content="What are my coffee preferences?")

search_response = client.memory_stores.search_memories(
    name="my_memory_store",
    scope=scope,
    items=[query_message],
    options=MemorySearchOptions(max_memories=5)
)
print(f"Found {len(search_response.memories)} memories")
for memory in search_response.memories:
    print(f"  - Memory ID: {memory.memory_item.memory_id}, Content: {memory.memory_item.content}")
```

# [REST API](#tab/rest)

```bash
# Configuration
ENDPOINT="https://{your-ai-services-account}.services.ai.azure.com/api/projects/{project-name}"
API_VERSION="2025-11-15-preview"
ACCESS_TOKEN="your-access-token-here"

curl -X POST "${ENDPOINT}/memory_stores/my_memory_store:search_memories?api-version=${API_VERSION}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "scope": "user_123",
    "items": [
      {
        "type": "message",
        "role": "user",
        "content": [
          {
            "type": "input_text",
            "text": "What are my coffee preferences?"
          }
        ]
      }
    ],
    "options": {
      "max_memories": 5
    }
  }'
```

---

## Update a memory store

Update memory store properties, such as `description` or `metadata`, to better manage memory stores.

# [Python](#tab/python)

```python
# Update memory store properties
updated_store = client.memory_stores.update(
    name="my_memory_store",
    description="Updated description"
)

print(f"Updated: {updated_store.description}")
```

# [REST API](#tab/rest)

```bash
# Configuration
ENDPOINT="https://{your-ai-services-account}.services.ai.azure.com/api/projects/{project-name}"
API_VERSION="2025-11-15-preview"
ACCESS_TOKEN="your-access-token-here"

curl -X POST "${ENDPOINT}/memory_stores/my_memory_store?api-version=${API_VERSION}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Updated description"
  }'
```

---

## List memory stores

Retrieve a list of memory stores in your project to manage and monitor your memory infrastructure.

# [Python](#tab/python)

```python
# List all memory stores
stores_list = client.memory_stores.list()

print(f"Found {len(stores_list.data)} memory stores")
for store in stores_list.data:
    print(f"- {store.name} ({store.description})")
```

# [REST API](#tab/rest)

```bash
# Configuration
ENDPOINT="https://{your-ai-services-account}.services.ai.azure.com/api/projects/{project-name}"
API_VERSION="2025-11-15-preview"
ACCESS_TOKEN="your-access-token-here"

curl -X GET "${ENDPOINT}/memory_stores?api-version=${API_VERSION}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

---

## Delete memories

> [!WARNING]
> Before you delete a memory store, consider the impact on dependent agents. Agents with attached memory stores might lose access to historical context.

Memories are organized by scope within a memory store. You can delete memories for a specific scope to remove user-specific data, or delete the entire memory store to remove all memories across all scopes.

### Delete memories by scope

Remove all memories associated with a particular user or group scope while preserving the memory store structure. Use this operation to handle user data deletion requests or reset memory for specific users.

# [Python](#tab/python)

```python
# Delete memories for a specific scope
delete_scope_response = client.memory_stores.delete_scope(
    name="my_memory_store",
    scope="user_123"
)

print(f"Deleted memories for scope: user_123")
```

# [REST API](#tab/rest)

```bash
# Configuration
ENDPOINT="https://{your-ai-services-account}.services.ai.azure.com/api/projects/{project-name}"
API_VERSION="2025-11-15-preview"
ACCESS_TOKEN="your-access-token-here"

curl -X POST "${ENDPOINT}/memory_stores/my_memory_store:delete_scope?api-version=${API_VERSION}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "scope": "user-123"
  }'
```

---

### Delete a memory store

Remove the entire memory store and all associated memories across all scopes. This operation is irreversible.

# [Python](#tab/python)

```python
# Delete the entire memory store
delete_response = client.memory_stores.delete("my_memory_store")
print(f"Deleted memory store: {delete_response.deleted}")
```

# [REST API](#tab/rest)

```bash
# Configuration
ENDPOINT="https://{your-ai-services-account}.services.ai.azure.com/api/projects/{project-name}"
API_VERSION="2025-11-15-preview"
ACCESS_TOKEN="your-access-token-here"

curl -X DELETE "${ENDPOINT}/memory_stores/my_memory_store?api-version=${API_VERSION}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

---


## Pricing

In this public preview, memory features are free. You're only billed for use of the chat completion model and embedding model.

## Best practices

When you implement memory in your agents, follow these practices:

- **Implement per-user access controls**. Avoid giving agents access to memories shared across all users. Use the `scope` property to partition the memory store by user. When sharing `scope` across users, use `user_profile_details` to instruct the memory system not to store personal information.
- **Minimize and protect sensitive data**. Store only what's necessary for your use case. If you must store sensitive data, such as personal data, health data, or confidential business inputs, redact or remove other content that could be used to trace back to an individual.
- **Support privacy and compliance**. Provide users with transparency, including options to access and delete their data. Record all deletions in a tamper-evident audit trail. Ensure the system adheres to local compliance requirements and regulatory standards.
- **Segment data and isolate memory**. In multi-agent systems, segment memory logically and operationally. Allow customers to define, isolate, inspect, and delete their own memory footprint.
- **Monitor memory usage**. Track token usage and memory operations to understand costs and optimize performance.

## Security risks of prompt injection

When working with memory in Foundry Agent Service, the LLM extracts and consolidates memories based on conversations. Protect memory against threats like prompt injection and memory corruption. These risks arise when incorrect or harmful data is stored in the agent’s memory, potentially influencing agent responses and actions.

Perform input validation to prevent prompt injection. Consider these actions:

- **Use [Azure AI Content Safety](https://ai.azure.com/explore/contentsafety) and its [prompt injection detection](../../../../ai-services/content-safety/concepts/jailbreak-detection.md)**. Validate all prompts entering or leaving the memory system to prevent malicious content.
- **Perform attack and adversarial testing**. Regularly stress-test your agent for injection vulnerabilities through controlled adversarial exercises.

## Related content

- [Build an agent with Microsoft Foundry](../../../agents/quickstart.md)
- [Microsoft Agent Framework overview](/agent-framework/overview/agent-framework-overview)
- [Create a project in Microsoft Foundry](../../../how-to/create-projects.md)
- [Python code samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/memories)
