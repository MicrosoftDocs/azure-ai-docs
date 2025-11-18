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
ms.date: 10/24/2025
ai-usage: ai-assisted
---

# Manage memory in Foundry Agent Service (preview)

> [!IMPORTANT]
> Memory (preview) in Foundry Agent Service and the Memory Store API (preview) are licensed to you as part of your Azure subscription and are subject to terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage) and the [Microsoft Products and Services Data Protection Addendum](https://aka.ms/DPA) ("DPA"), as well as the Microsoft Generative AI Services Previews terms in the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

Memory in Microsoft Foundry Agent Service (preview) is a managed, long-term memory solution that enables agent continuity across sessions, devices, and workflows. By creating memory stores and managing their content, you can build agents that retain user preferences, maintain conversation history, and deliver personalized experiences.

This article shows you how to create memory stores, attach them to agents, add and search memories, and implement best practices for security and privacy. With these capabilities, your agents can maintain context across multistep interactions and provide more reliable, personalized responses.

Memory stores act as persistent storage that define what types of information are relevant to each agent. You control access through the `scope` parameter, which ensures secure and isolated experiences by segmenting memory across users.

## Common memory use cases

The following examples illustrate how memory can enhance various types of agents.

**Conversational Agent**

- A customer support agent that remembers your name, previous issues and resolution, ticket numbers, and whether you prefer chat, email, or a call-back. This memory prevents the user from having to repeat themselves, ensuring continuity and increasing customer satisfaction.
- A personal shopping assistant that remembers your size in specific brands, preferred color, past returns, and recent purchases to offer highly relevant suggestions immediately upon starting a new session and avoid recommending items you already own.
 
**Planning Agent**
  
- A travel agent that knows your flight preference (window/aisle), seat selection, food preference, non-stop vs. connecting flights, loyalty programs, and past destination feedback to build an optimized itinerary quickly.
- An architectural design agent that remembers the local building codes, the material costs from past bids, and initial client feedback to iteratively refine design, ensuring the final plan is both feasible and meets all constraints. 
  
**Research Agent**

A medical research agent that remembers which compounds were previously tested (and failed), the key findings from different labs, and the complex relationships between various proteins to suggest a novel, untested research hypothesis.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/free/).
- Access to Microsoft Foundry with appropriate permissions to create and manage resources.
- A [Microsoft Foundry project](../../../how-to/create-projects.md).
- An [agent created in Microsoft Foundry](../../../agents/quickstart.md).
- [Chat model deployment](../../../foundry-models/how-to/create-model-deployments.md) (for example, `gpt-4.1`) in your project.
- [Embedding model deployment](../../../openai/tutorials/embeddings.md) (for example, `text-embedding-3-small`) in your project.
- Python 3.8 or later with the Foundry Agent SDK installed, or access to the REST API.

## Create a memory store

Create a dedicated memory store for each agent to establish clear boundaries for memory access and optimization. When you create a memory store, specify the chat model and embedding model deployments that process and store your memory content.

You must decide how to segment memory across users by specifying the `scope` parameter. By default, the system uses the end user's sign-in ID. To enable shared memory across users or groups, override this value with a team name, organization name, or other identifier that fits your use case.

# [Python](#tab/python)

```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MemoryStoreDefaultDefinition
from azure.identity import DefaultAzureCredential

# Initialize the client
client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential()
)

# Create memory store
definition = MemoryStoreDefaultDefinition(
    chat_model="gpt-4.1",  # Your chat model deployment name
    embedding_model="text-embedding-3-small"  # Your embedding model deployment name
)

memory_store = client.memory_stores.create_memory_store(
    name="my_memory_store",
    definition=definition,
    description="Memory store for customer support agent",
)

print(f"Created memory store: {memory_store.id}")
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
      "embedding_model": "text-embedding-3-small"
    }
  }'
```

---

The memory store creation returns an ID that you use in subsequent operations. Store this ID securely for reference.


## Add memories to a memory store

Add memories by providing conversation content to the memory store. The system performs preprocessing and postprocessing, including memory extraction and consolidation, to optimize the agent's memory. This long-running operation might take about one minute to complete.

You can update a memory store in three ways: add an array of conversation items, reference an existing conversation ID, or use a previous update ID for incremental updates.

# [Python](#tab/python)

```python
from azure.ai.projects.models import ResponsesUserMessageItemParam

user_message = ResponsesUserMessageItemParam(
    content="I prefer dark roast coffee and usually drink it in the morning"
)

# METHOD 1: Using items (conversation messages) directly

update_poller = client.memory_stores.begin_update_memories(
    name="my_memory_store",
    scope="user_123",
    items=[user_message],  # Pass conversation items that you want to add to memory
    update_delay=0  # Process immediately (default is 300 seconds)
)

result = update_poller.result()
print(f"✓ Updated with {len(result.memory_operations)} memory operations")

# METHOD 2: Using an existing conversation_id

update_poller = client.memory_stores.begin_update_memories(
    name="my_memory_store",
    scope="user_123",
    conversation_id="conv_id_456",  # Reference an existing conversation
    update_delay=60  # Wait 60 seconds before processing
)

result = update_poller.result()
print(f"✓ Updated from conversation: {result.conversation_id}")

# METHOD 3: Using previous_update_id for incremental updates

new_message = ResponsesUserMessageItemParam(
    content="I also like cappuccinos in the afternoon"
)

incremental_update = client.memory_stores.begin_update_memories(
    name="my_memory_store",
    scope="user_123",
    items=[new_message],
    previous_update_id=result.update_id,  # Continue from previous update
    update_delay=0
)

incremental_result = incremental_update.result()
print(f"✓ Incremental update completed")```
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
curl -X GET "${ENDPOINT}/memory_stores/my_memory_store/updates/${UPDATE_ID}?api-version=${API_VERSION}" -H "Authorization: Bearer ${ACCESS_TOKEN}"
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
    name=memory_store.name,
    scope="user_123",
    conversation_id="conv_id_456",  # Search based on a conversation
    options=MemorySearchOptions(max_memories=5)
)

# Search based on a specific query message
query_message = ResponsesUserMessageItemParam(
    content="What are my coffee preferences?"
)

search_response = client.memory_stores.search_memories(
    name=memory_store.name,
    scope="user_123",
    items=[query_message],  # Your search query as a message
    options=MemorySearchOptions(max_memories=10)
)
    
print(f"✓ Search completed (ID: {search_response.search_id})")
print(f"  Found {len(search_response.memories)} memories")
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
      "max_memories": 10
    }
  }'
```

---

Search operations return a search ID that you can use for incremental searches, allowing you to paginate through large result sets efficiently.

## Update a memory store

Update memory store properties, such as `name` or `description`, to reflect changes in your application or organizational requirements.

# [Python](#tab/python)

```python
# Update memory store properties
updated_store = client.memory_stores.update_memory_store(
    memory_store_id=memory_store.id,
    name="updated_memory_store",
    description="Updated description for production use"
)

print(f"Updated: {updated_store.name}")
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
    "description": "Updated: Memory store for customer interactions with enhanced tracking"
  }'
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

```bash
# Configuration
ENDPOINT="https://{your-ai-services-account}.services.ai.azure.com/api/projects/{project-name}"
API_VERSION="2025-11-15-preview"
ACCESS_TOKEN="your-access-token-here"

curl -X GET "${ENDPOINT}/memory_stores?api-version=${API_VERSION}&limit=10&order=desc" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

---

Use the `limit` parameter to control pagination and efficiently manage large numbers of memory stores.

## Delete memories

> [!WARNING]
> Before you delete a memory store, consider the impact on dependent agents. Agents with attached memory stores might lose access to historical context.

Memories are organized by scope within a memory store. You can delete memories for a specific scope to remove user-specific data, or delete the entire memory store to remove all memories across all scopes.

### Delete memories by scope

Remove all memories associated with a particular user or group scope while preserving the memory store structure. Use this operation to handle user data deletion requests or reset memory for specific users.

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
delete_response = client.memory_stores.delete_memory_store(memory_store.id)
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

## Use memory with prompt agent

Attach the memory store to your agent to enable memory capabilities. Start with one memory store per agent to maximize memory protection and ensure optimization for your specific use case.

# [Python](#tab/python)

```python
# Attach memory store to agent

agent = project_client.agents.create_version(
        agent_name="MyAgent",
        definition=PromptAgentDefinition(
            model=os.environ["AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME"],
            instructions="You are a helpful assistant that answers general questions",
        ),
        tools=[
            MemorySearchTool(
                memory_store_name=memory_store.name, 
                scope="{{$userId}}", 
                update_delay=10  # Wait 5 seconds of inactivity before updating memories
                                 # In a real application, set this to a higher value like 300 (5 minutes, default)
            )
        ]
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")
```

# [REST](#tab/rest)

```bash
# Configuration
ENDPOINT="https://{your-ai-services-account}.services.ai.azure.com/api/projects/{project-name}"
API_VERSION="2025-11-15-preview"
ACCESS_TOKEN="your-access-token-here"

curl -X POST "${ENDPOINT}/agents?api-version=${API_VERSION}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "customer-support-agent",
    "description": "Customer support agent with memory capabilities",
    "definition": {
      "kind": "prompt",
      "model": "gpt-4o",
      "instructions": "You are a helpful customer support agent. Use your memory to recall user preferences and past interactions.",
      "tools": [
        {
          "type": "memory_search",
          "memory_store_id": "user-conversation-memory",
          "scope": "user-123"
        }
      ]
    }
  }'

# Converse with the agent
curl --include -X POST "${ENDPOINT}/openai/responses?api-version=2025-11-15-preview" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -d '{
        "agent": {"type": "agent_reference", "name": "customer-support-agent", "version": "1"},
        "input": [ {"role": "user", "content": "Hello"} ]
  }'
```

---

## Understand memory types

Agent memory typically falls into two categories:

- **Short-term memory** tracks the current session's conversation, maintaining immediate context for ongoing interactions. Agent orchestration frameworks like [Microsoft Agent Framework](/agent-framework/overview/agent-framework-overview) typically manage this memory as part of the session context.

- **Long-term memory** retains distilled knowledge across sessions, enabling the model to recall and build on previous user interactions over time. This memory type requires integration with a persistent system that supports extraction, consolidation, and management of knowledge.

Microsoft Foundry memory is designed for long-term memory. It extracts meaningful information from conversations, consolidates it into durable knowledge, and makes it available across sessions and agents.
## Understand `Scope`
`Scope` defines how memory is partitioned. Each scope in the memory store maintains an isolated collection of memory items. For example, when you create a customer support agent with memory, you want each customer to have their own individual memory.

As a developer, you decide the key used to store and retrieve these memory items - such as a UUID or an email address (provided it is unique and permanent in your system).

The memory store supports the `{{$userId}}` variable, which is replaced at runtime with the actual user OID. This support allows you to leverage the memory store for scoping when using Microsoft Entra for authenticating your end users. If you manage your own user identities, you are responsible for setting this value for every end user interacting with your agent.

## Customize memory
To ensure an agent's memory is efficient, relevant, and privacy-respecting, you should actively customize what information is prioritized and stored. The `user_profile_details` parameter allows you to explicitly indicate the types of data that are critical to the agent's core function. 

For a planning agent, this parameter might include setting `user_profile_details` to prioritize "flight carrier preference and dietary restrictions". This focused approach ensures that when new information is encountered during an interaction, the memory system knows which details to extract, summarize, and commit to long-term memory.

You can also leverage the same parameter to inform the memory not to focus on certain type of data, ensuring the memory remains lean and compliant with privacy requirement. For example, you can set `user_profile_details` to "avoid irrelevant or sensitive data (age, financials, precise location, credentials etc.)"

## Pricing 

In this public preview, the use of memory features is free. However, you're billed for use of the chat completion model and embedding model. 

## Best practices

When you implement memory in your agents, consider the following practices:

- **Implement per-user access controls**: Avoid giving every agent access to all memory. Use the `Scope` parameter to restrict who can see and update memories. For shared memory across agents or users, use the scope to instruct the memory system not to store personal information.
- **Minimize and protect sensitive data**: Store only what's necessary for your use case. If you must store sensitive data, such as personal data, health data, or confidential business inputs, perform redaction and store only partial data.
- **Support privacy and compliance**: Implement mechanisms for users to access, export, correct, and delete their data. Support selective deletion of specific memory entries, not just full resets. Log deletions in a tamper-evident audit trail. Ensure your system supports CCPA, HIPAA, and other relevant frameworks.
- **Segment data and isolate memory**: In multitenant or multiagent systems, segment memory logically and operationally. Allow customers to define, isolate, inspect, and delete their own memory footprint.
- **Monitor memory usage**: Track token usage and memory operations to understand costs and optimize performance. Set appropriate limits for memory storage and retrieval.
- **Version your memory stores**: Use metadata to track versions and configurations of memory stores, making it easier to manage updates and troubleshoot issues.
## Security risks of prompt injection
 
When you work with memory in Foundry Agent Service, protect memory against threats like prompt injection and memory corruption. These risks arise when incorrect or harmful data is stored in the agent’s memory, potentially influencing future decisions and actions.
 
To strengthen memory security, consider the following actions:
 
- **Use [Foundry Content Safety](https://ai.azure.com/explore/contentsafety)**: Validate all prompts entering or leaving the memory system to prevent malicious content.
- **Perform attack and adversarial testing**: Regularly stress-test your agent for injection vulnerabilities through controlled adversarial exercises.

## Related content

- [Build an agent with Microsoft Foundry](../../../agents/quickstart.md)
- [Microsoft Agent Framework overview](/agent-framework/overview/agent-framework-overview)
- [Create a project in Microsoft Foundry](../../../how-to/create-projects.md)
