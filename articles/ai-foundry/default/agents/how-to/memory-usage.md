---
title: Create and Use Memory
titleSuffix: Microsoft Foundry
description: Learn how to create and manage memory in Foundry Agent Service to enable AI agents to retain context across sessions and personalize user interactions.
author: haileytap
ms.author: haileytapia
ms.reviewer: liulewis
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 01/22/2026
ms.custom: pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
#customer intent: As a developer, I want to attach a memory store to my AI agent so that it can access and update memories during interactions.
---

# Create and use memory in Foundry Agent Service (preview)

> [!IMPORTANT]
> Memory (preview) in Foundry Agent Service and the Memory Store API (preview) are licensed to you as part of your Azure subscription and are subject to terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/product/ForOnlineServices/all) and the [Microsoft Products and Services Data Protection Addendum](https://aka.ms/DPA), as well as the Microsoft Generative AI Services Previews terms in the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

Memory in Foundry Agent Service is a managed, long-term memory solution. It enables agent continuity across sessions, devices, and workflows. By creating and managing memory stores, you can build agents that retain user preferences, maintain conversation history, and deliver personalized experiences.

Memory stores act as persistent storage, defining which types of information are relevant to each agent. You control access using the `scope` parameter, which segments memory across users to ensure secure and isolated experiences.

This article explains how to create, manage, and use memory stores. For conceptual information, see [Memory in Foundry Agent Service](../concepts/what-is-memory.md).

### Usage support

| Capability | Python SDK | REST API |
|---|---|---|
| Create, update, list, and delete memory stores | ✔️ | ✔️ |
| Update and search memories | ✔️ | ✔️ |
| Attach memory to a prompt agent | ✔️ | ✔️ |

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A [Microsoft Foundry project](../../../how-to/create-projects.md) with [authorization and permissions](#authorization-and-permissions) configured.
- [Chat model deployment](../../../foundry-models/how-to/create-model-deployments.md) (for example, `gpt-4.1`) in your project.
- [Embedding model deployment](../../../openai/tutorials/embeddings.md) (for example, `text-embedding-3-small`) in your project.
- For Python examples:
  - Python 3.8 or later with a [configured environment](../../../quickstarts/get-started-code.md?tabs=python&view=foundry&preserve-view=true)
  - Required packages: `pip install azure-ai-projects azure-identity`
- For REST API examples, Azure CLI authenticated to your subscription.

### Authorization and permissions

We recommend [role-based access control](../../../concepts/rbac-foundry.md) for production deployments. If roles aren't feasible, skip this section and use key-based authentication instead.

To configure role-based access:

1. Sign in to the [Azure portal](https://portal.azure.com/).
1. On your project:
    1. From the left pane, select **Resource Management** > **Identity**.
    1. Use the toggle to enable a system-assigned managed identity.
1. On the resource that contains your project:
    1. From the left pane, select **Access control (IAM)**.
    1. Select **Add** > **Add role assignment**.
    1. Assign **Azure AI User** to the managed identity of your project.

### Set project endpoint

For the Python examples in this article, set an environment variable for your project endpoint:

```bash
export FOUNDRY_PROJECT_ENDPOINT="https://{your-ai-services-account}.services.ai.azure.com/api/projects/{project-name}"
```

```powershell
$env:FOUNDRY_PROJECT_ENDPOINT = "https://{your-ai-services-account}.services.ai.azure.com/api/projects/{project-name}"
```

## Understand scope

The `scope` parameter controls how memory is partitioned. Each scope in the memory store keeps an isolated collection of memory items. For example, if you create a customer support agent with memory, each customer should have their own individual memory.

As a developer, you choose the key used to store and retrieve memory items, such as a UUID or a unique user ID in your system.

## Create a memory store

Create a dedicated memory store for each agent to establish clear boundaries for memory access and optimization. When you create a memory store, specify the chat model and embedding model deployments that process your memory content.

# [Python](#tab/python)

```python
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MemoryStoreDefaultDefinition, MemoryStoreDefaultOptions
from azure.identity import DefaultAzureCredential

project_client = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

memory_store_name = "my_memory_store"

# Specify memory store options
options = MemoryStoreDefaultOptions(
    chat_summary_enabled=True,
    user_profile_enabled=True,
    user_profile_details="Avoid irrelevant or sensitive data, such as age, financials, precise location, and credentials"
)

# Create memory store
definition = MemoryStoreDefaultDefinition(
    chat_model="gpt-4.1",  # Your chat model deployment name
    embedding_model="text-embedding-3-small",  # Your embedding model deployment name
    options=options
)

memory_store = project_client.memory_stores.create(
    name=memory_store_name,
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

# Get a short-lived access token using Azure CLI
ACCESS_TOKEN="$(az account get-access-token --resource https://ai.azure.com/ --query accessToken -o tsv)"

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
        "chat_summary_enabled": true,
        "user_profile_enabled": true,
        "user_profile_details": "Avoid irrelevant or sensitive data, such as age, financials, precise location, and credentials"
      }
    }
  }'
```

---

### Customize memory

Customize what information the agent stores to keep memory efficient, relevant, and privacy-respecting. Use the `user_profile_details` parameter to specify the types of data that are critical to the agent's function.

For example, set `user_profile_details` to prioritize "flight carrier preference and dietary restrictions" for a travel agent. This focused approach helps the memory system know which details to extract, summarize, and commit to long-term memory.

You can also use this parameter to exclude certain types of data, keeping memory lean and compliant with privacy requirements. For example, set `user_profile_details` to "avoid irrelevant or sensitive data, such as age, financials, precise location, and credentials."

## Update a memory store

Update memory store properties, such as `description` or `metadata`, to better manage memory stores.

# [Python](#tab/python)

```python
# Update memory store properties
updated_store = project_client.memory_stores.update(
    name=memory_store_name,
    description="Updated description"
)

print(f"Updated: {updated_store.description}")
```

# [REST API](#tab/rest)

```bash
# Configuration
ENDPOINT="https://{your-ai-services-account}.services.ai.azure.com/api/projects/{project-name}"
API_VERSION="2025-11-15-preview"
ACCESS_TOKEN="$(az account get-access-token --resource https://ai.azure.com/ --query accessToken -o tsv)"

MEMORY_STORE_NAME="my_memory_store"

curl -X POST "${ENDPOINT}/memory_stores/${MEMORY_STORE_NAME}?api-version=${API_VERSION}" \
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
stores_list = project_client.memory_stores.list()

print(f"Found {len(stores_list.data)} memory stores")
for store in stores_list.data:
    print(f"- {store.name} ({store.description})")
```

# [REST API](#tab/rest)

```bash
# Configuration
ENDPOINT="https://{your-ai-services-account}.services.ai.azure.com/api/projects/{project-name}"
API_VERSION="2025-11-15-preview"
ACCESS_TOKEN="$(az account get-access-token --resource https://ai.azure.com/ --query accessToken -o tsv)"

curl -X GET "${ENDPOINT}/memory_stores?api-version=${API_VERSION}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

---

## Use memories via an agent tool

After you create a memory store, you can attach the memory search tool to a prompt agent. This tool enables the agent to read from and write to your memory store during conversations. Configure the tool with the appropriate `scope` and `update_delay` to control how and when memories are updated.

# [Python](#tab/python)

```python
# Continue from the previous Python snippets.
from azure.ai.projects.models import MemorySearchTool, PromptAgentDefinition

# Set scope to associate the memories with
# You can also use "{{$userId}}" to take the oid of the request authentication header
scope = "user_123"

openai_client = project_client.get_openai_client()

# Create memory search tool
tool = MemorySearchTool(
    memory_store_name=memory_store_name,
    scope=scope,
    update_delay=1,  # Wait 1 second of inactivity before updating memories
    # In a real application, set this to a higher value like 300 (5 minutes, default)
)

# Create a prompt agent with memory search tool
agent = project_client.agents.create_version(
    agent_name="MyAgent",
    definition=PromptAgentDefinition(
        model="gpt-4.1",
        instructions="You are a helpful assistant that answers general questions",
        tools=[tool],
    )
)

print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")
```

# [REST API](#tab/rest)

```bash
# Configuration
ENDPOINT="https://{your-ai-services-account}.services.ai.azure.com/api/projects/{project-name}"
API_VERSION="2025-11-15-preview"
ACCESS_TOKEN="$(az account get-access-token --resource https://ai.azure.com/ --query accessToken -o tsv)"

curl -X POST "${ENDPOINT}/agents/MyAgent/versions?api-version=${API_VERSION}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "definition": {
        "kind": "prompt",
        "model": "gpt-4.1",
        "instructions": "You are a helpful assistant that answers general questions",
        "tools": [
            {
              "type": "memory_search",
              "memory_store_name": "my_memory_store",
              "scope": "user_123",
              "update_delay": 1
            }
        ]
    }
}'
```

---

### Create a conversation

You can now create conversations and request agent responses. At the start of each conversation, static memories are injected so the agent has immediate, persistent context. Contextual memories are retrieved per turn based on the latest messages to inform each response.

After each agent response, the service internally calls `update_memories`. However, actual writes to long‑term memory are debounced by the `update_delay` setting. The update is scheduled and only completes after the configured period of inactivity.

# [Python](#tab/python)

```python
import time

# Create a conversation with the agent with memory tool enabled
conversation = openai_client.conversations.create()
print(f"Created conversation (id: {conversation.id})")

# Create an agent response to initial user message
response = openai_client.responses.create(
    input="I prefer dark roast coffee",
    conversation=conversation.id,
    extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
)

print(f"Response output: {response.output_text}")

# After an inactivity in the conversation, memories will be extracted from the conversation and stored
print("Waiting for memories to be stored...")
time.sleep(65)

# Create a new conversation
new_conversation = openai_client.conversations.create()
print(f"Created new conversation (id: {new_conversation.id})")

# Create an agent response with stored memories
new_response = openai_client.responses.create(
    input="Please order my usual coffee",
    conversation=new_conversation.id,
    extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
)

print(f"Response output: {new_response.output_text}")
```

# [REST API](#tab/rest)

```bash
# Configuration
ENDPOINT="https://{your-ai-services-account}.services.ai.azure.com/api/projects/{project-name}"
API_VERSION="2025-11-15-preview"
ACCESS_TOKEN="$(az account get-access-token --resource https://ai.azure.com/ --query accessToken -o tsv)"

curl -X POST "${ENDPOINT}/openai/conversations?api-version=${API_VERSION}" \
    -H "Authorization: Bearer ${ACCESS_TOKEN}" \
    -H "Content-Type: application/json" \
    -d '{}'

# Copy the "id" field from the previous response.
curl -X POST "${ENDPOINT}/openai/responses?api-version=${API_VERSION}" \
    -H "Authorization: Bearer ${ACCESS_TOKEN}" \
    -H "Content-Type: application/json" \
    -d '{
      "input": "I prefer dark roast coffee",
      "conversation": "{conversation-id}",
      "agent": {
        "name": "MyAgent",
        "type": "agent_reference"
      }
    }'
```

---

## Use memories via APIs

You can interact with a memory store directly using the memory store APIs. Start by adding memories from conversation content to the memory store, and then search for relevant memories to provide context for agent interactions.

### Add memories to a memory store

Add memories by providing conversation content to the memory store. The system preprocesses and postprocesses the data, including memory extraction and consolidation, to optimize the agent's memory. This long-running operation might take about one minute.

Decide how to segment memory across users by specifying the `scope` parameter. You can scope the memory to a specific end user, a team, or another identifier.

You can update a memory store with content from multiple conversation turns, or update after each turn and chain updates using the previous update operation ID.

# [Python](#tab/python)

```python
# Continue from the previous Python snippets.
from azure.ai.projects.models import ResponsesUserMessageItemParam

# Set scope to associate the memories with
scope = "user_123"

user_message = ResponsesUserMessageItemParam(
    content="I prefer dark roast coffee and usually drink it in the morning"
)

update_poller = project_client.memory_stores.begin_update_memories(
    name=memory_store_name,
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
new_update_poller = project_client.memory_stores.begin_update_memories(
    name=memory_store_name,
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
ACCESS_TOKEN="$(az account get-access-token --resource https://ai.azure.com/ --query accessToken -o tsv)"

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

### Search for memories in a memory store

Search memories to retrieve relevant context for agent interactions. Specify the memory store name and scope to narrow the search.

# [Python](#tab/python)

```python
# Continue from the previous Python snippets.
from azure.ai.projects.models import MemorySearchOptions, ResponsesUserMessageItemParam

# Search memories by a query
query_message = ResponsesUserMessageItemParam(content="What are my coffee preferences?")

search_response = project_client.memory_stores.search_memories(
    name=memory_store_name,
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
ACCESS_TOKEN="$(az account get-access-token --resource https://ai.azure.com/ --query accessToken -o tsv)"

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

### Retrieve static or contextual memories

Often, user profile memories can't be retrieved based on semantic similarity to a user's message. We recommend that you inject static memories into the beginning of each conversation and use contextual memories to generate each agent response.

- To retrieve static memories, call `search_memories` with a `scope` but without `items` or `previous_search_id`. This returns user profile memories associated with the scope.

- To retrieve contextual memories, call `search_memories` with `items` set to the latest messages. This can return both user profile and chat summary memories most relevant to the given items.

For more information about user profile and chat summary memories, see [Memory types](../concepts/what-is-memory.md#memory-types).

## Delete memories

> [!WARNING]
> Before you delete a memory store, consider the impact on dependent agents. Agents with attached memory stores might lose access to historical context.

Memories are organized by scope within a memory store. You can delete memories for a specific scope to remove user-specific data, or you can delete the entire memory store to remove all memories across all scopes.

### Delete memories by scope

Remove all memories associated with a particular user or group scope while preserving the memory store structure. Use this operation to handle user data deletion requests or reset memory for specific users.

# [Python](#tab/python)

```python
# Delete memories for a specific scope
delete_scope_response = project_client.memory_stores.delete_scope(
    name=memory_store_name,
    scope="user_123"
)

print(f"Deleted memories for scope: user_123")
```

# [REST API](#tab/rest)

```bash
# Configuration
ENDPOINT="https://{your-ai-services-account}.services.ai.azure.com/api/projects/{project-name}"
API_VERSION="2025-11-15-preview"
ACCESS_TOKEN="$(az account get-access-token --resource https://ai.azure.com/ --query accessToken -o tsv)"

curl -X POST "${ENDPOINT}/memory_stores/my_memory_store:delete_scope?api-version=${API_VERSION}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "scope": "user_123"
  }'
```

---

### Delete a memory store

Remove the entire memory store and all associated memories across all scopes. This operation is irreversible.

# [Python](#tab/python)

```python
# Delete the entire memory store
delete_response = project_client.memory_stores.delete(memory_store_name)
print(f"Deleted memory store: {delete_response.deleted}")
```

# [REST API](#tab/rest)

```bash
# Configuration
ENDPOINT="https://{your-ai-services-account}.services.ai.azure.com/api/projects/{project-name}"
API_VERSION="2025-11-15-preview"
ACCESS_TOKEN="$(az account get-access-token --resource https://ai.azure.com/ --query accessToken -o tsv)"

curl -X DELETE "${ENDPOINT}/memory_stores/my_memory_store?api-version=${API_VERSION}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

---

## Best practices

- **Implement per-user access controls:** Avoid giving agents access to memories shared across all users. Use the `scope` property to partition the memory store by user. When you share `scope` across users, use `user_profile_details` to instruct the memory system not to store personal information.

- **Map scope to an authenticated user:** When you specify scope in the [memory search tool](#use-memories-via-an-agent-tool), set `scope={{$userId}}` to map to the user from the authentication token (`{tid}_{oid}`). This ensures that memory searches automatically target the correct user.

- **Minimize and protect sensitive data:** Store only what's necessary for your use case. If you must store sensitive data, such as personal data, health data, or confidential business inputs, redact or remove other content that could be used to trace back to an individual.

- **Support privacy and compliance:** Provide users with transparency, including options to access and delete their data. Record all deletions in a tamper-evident audit trail. Ensure the system adheres to local compliance requirements and regulatory standards.

- **Segment data and isolate memory:** In multi-agent systems, segment memory logically and operationally. Allow customers to define, isolate, inspect, and delete their own memory footprint.

- **Monitor memory usage:** Track token usage and memory operations to understand costs and optimize performance.

## Troubleshooting

| Issue | Cause | Resolution |
|---|---|---|
| Requests fail with an authentication or authorization error. | Your identity or the project managed identity doesn’t have the required roles. | Verify the roles in [Authorization and permissions](#authorization-and-permissions). For REST calls, generate a fresh access token and retry. |
| Memories don’t appear after a conversation. | Memory updates are debounced or still processing. | Increase the wait time or call the update API with `update_delay` set to `0` to trigger processing immediately. |
| Memory search returns no results. | The `scope` value doesn’t match the scope used when memories were stored. | Use the same scope for update and search. If you map scope to users, use a stable user identifier. |
| The agent response doesn’t use stored memory. | The agent isn’t configured with the memory search tool, or the memory store name is incorrect. | Confirm the agent definition includes the `memory_search` tool and references the correct memory store name. |

## Related content

- [Python code samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/memories)
- [Memory store REST API reference](../../../reference/foundry-project-rest-preview.md)
- [Memory in Foundry Agent Service](../concepts/what-is-memory.md)
- [Foundry Agent Service quotas and limits](../../../agents/quotas-limits.md)
- [Build an agent with Microsoft Foundry](../../../agents/quickstart.md)
