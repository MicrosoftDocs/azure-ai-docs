---
title: "Create and Use Memory"
description: "Learn how to create and manage memory in Foundry Agent Service to enable AI agents to retain context across sessions and personalize user interactions."
author: haileytap
ms.author: haileytapia
ms.reviewer: liulewis
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 04/03/2026
ms.custom: pilot-ai-workflow-jan-2026, doc-kit-assisted
ai-usage: ai-assisted
zone_pivot_groups: foundry-memory-store
#customer intent: As a developer, I want to attach a memory store to my AI agent so that it can access and update memories during interactions.
---

# Create and use memory in Foundry Agent Service (preview)

> [!IMPORTANT]
> Memory (preview) in Foundry Agent Service and the Memory Store API (preview) are licensed to you as part of your Azure subscription and are subject to terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/product/ForOnlineServices/all) and the [Microsoft Products and Services Data Protection Addendum](https://aka.ms/DPA), as well as the Microsoft Generative AI Services Previews terms in the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

Memory in Foundry Agent Service is a managed, long-term memory solution. It enables agent continuity across sessions, devices, and workflows. By creating and managing memory stores, you can build agents that retain user preferences, maintain conversation history, and deliver personalized experiences.

Memory stores act as persistent storage, defining which types of information are relevant to each agent. You control access using the `scope` parameter, which segments memory across users to ensure secure and isolated experiences.

This article explains how to create, manage, and use memory stores. For conceptual information, see [Memory in Foundry Agent Service](../concepts/what-is-memory.md).

### Usage support

| Capability | Python SDK | C# SDK | JavaScript SDK | REST API |
|---|---|---|---|---|
| Create, update, list, and delete memory stores | ✔️ | ✔️ | ✔️ | ✔️ |
| Update and search memories | ✔️ | ✔️ | ✔️ | ✔️ |
| Attach memory to a prompt agent | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A [Microsoft Foundry project](../../how-to/create-projects.md) with configured [authorization and permissions](#authorization-and-permissions).
- A [chat model deployment](../../foundry-models/how-to/create-model-deployments.md), such as `gpt-5.2`, in your project.
- An [embedding model deployment](../../openai/tutorials/embeddings.md), such as `text-embedding-3-small`, in your project.
- A [configured local environment](#set-up-your-environment) with required packages and environment variables.

### Authorization and permissions

We recommend [role-based access control](../../concepts/rbac-foundry.md) for production deployments. If roles aren't feasible, skip this section and use key-based authentication instead.

To configure role-based access:

1. Sign in to the [Azure portal](https://portal.azure.com/).

1. On your project:
    1. From the left pane, select **Resource Management** > **Identity**.
    1. Use the toggle to enable a system-assigned managed identity.

1. On the resource that contains your project:
    1. From the left pane, select **Access control (IAM)**.
    1. Select **Add** > **Add role assignment**.
    1. Assign **Azure AI User** to the managed identity of your project.

### Set up your environment

:::zone pivot="python"

Install the required packages:

```bash
pip install "azure-ai-projects>=2.0.0" azure-identity
```

:::zone-end

:::zone pivot="csharp"

Install the required packages:

```bash
dotnet add package Azure.AI.Projects --prerelease
dotnet add package Azure.AI.Projects.Agents --prerelease
dotnet add package Azure.AI.Extensions.OpenAI --prerelease
dotnet add package Azure.Identity
```

:::zone-end

:::zone pivot="typescript"

Install the required packages:

```bash
npm install @azure/ai-projects@2 @azure/identity
```

:::zone-end

:::zone pivot="python,csharp,typescript"

Set environment variables for your project endpoint and model deployment names:

```bash
export FOUNDRY_PROJECT_ENDPOINT="https://{your-ai-services-account}.services.ai.azure.com/api/projects/{project-name}"
export MEMORY_STORE_CHAT_MODEL_DEPLOYMENT_NAME="<chat-model-deployment-name>"
export MEMORY_STORE_EMBEDDING_MODEL_DEPLOYMENT_NAME="<embedding-model-deployment-name>"
```

:::zone-end

:::zone pivot="rest"

Set environment variables for your project endpoint, model deployments, API version, and access token:

```bash
FOUNDRY_PROJECT_ENDPOINT="https://{your-ai-services-account}.services.ai.azure.com/api/projects/{project-name}"
MEMORY_STORE_CHAT_MODEL_DEPLOYMENT_NAME="<chat-model-deployment-name>" # For example, gpt-5.2
MEMORY_STORE_EMBEDDING_MODEL_DEPLOYMENT_NAME="<embedding-model-deployment-name>" # For example, text-embedding-3-small
API_VERSION="2025-11-15-preview"

# Get a short-lived access token using Azure CLI
ACCESS_TOKEN="$(az account get-access-token --resource https://ai.azure.com/ --query accessToken -o tsv)"
```

:::zone-end

## Understand scope

The `scope` parameter controls how memory is partitioned. Each scope in the memory store keeps an isolated collection of memory items. For example, if you create a customer support agent with memory, each customer should have their own individual memory.

As a developer, you choose the key used to store and retrieve memory items. The right approach depends on how you access memory.

### Via the memory search tool

When you attach the [memory search tool](#use-memories-via-an-agent-tool) to an agent, set `scope` to `{{$userId}}` to enable per-user memory isolation without hard-coding identifiers. The system automatically resolves the end user's identity on each response call from one of two sources:

- **`x-memory-user-id` request header:** If present, the header value is used as the user ID. Use this in proxy or backend scenarios where your service calls the API on behalf of an end user.

- **Microsoft Entra authentication token:** If the header isn't set, the system falls back to the caller's tenant ID (TID) and object ID (OID). This is the default in frontend scenarios where users authenticate directly with Microsoft Entra.

If you don't need per-user isolation, use a static `scope` value instead.

### Via low-level memory APIs

When you call [memory APIs](#use-memories-via-apis) directly, specify `scope` explicitly in each request. You can pass a static value, such as a universally unique identifier (UUID) or another stable identifier from your system. Automatic identity extraction isn't supported for these operations.

## Create a memory store

Create a dedicated memory store for each agent to establish clear boundaries for memory access and optimization. When you create a memory store, specify the chat model and embedding model deployments that process your memory content.

:::zone pivot="python"

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
chat_model = os.environ["MEMORY_STORE_CHAT_MODEL_DEPLOYMENT_NAME"]
embedding_model = os.environ["MEMORY_STORE_EMBEDDING_MODEL_DEPLOYMENT_NAME"]

definition = MemoryStoreDefaultDefinition(
    chat_model=chat_model,
    embedding_model=embedding_model,
    options=options
)

memory_store = project_client.beta.memory_stores.create(
    name=memory_store_name,
    definition=definition,
    description="Memory store for customer support agent",
)

print(f"Created memory store: {memory_store.name}")
```

:::zone-end

:::zone pivot="csharp"

```csharp
using System;
using Azure.AI.Projects;
using Azure.AI.Projects.Memory;
using Azure.Identity;

#pragma warning disable AAIP001

var projectEndpoint = Environment.GetEnvironmentVariable(
    "FOUNDRY_PROJECT_ENDPOINT");
var chatModel = Environment.GetEnvironmentVariable(
    "MEMORY_STORE_CHAT_MODEL_DEPLOYMENT_NAME");
var embeddingModel = Environment.GetEnvironmentVariable(
    "MEMORY_STORE_EMBEDDING_MODEL_DEPLOYMENT_NAME");

AIProjectClient projectClient = new(
    new Uri(projectEndpoint),
    new DefaultAzureCredential());

var memoryStoreName = "my_memory_store";

// Specify memory store options
MemoryStoreDefaultDefinition memoryStoreDefinition = new(
    chatModel: chatModel,
    embeddingModel: embeddingModel
);
memoryStoreDefinition.Options = new(
    isUserProfileEnabled: true,
    isChatSummaryEnabled: true);
memoryStoreDefinition.Options.UserProfileDetails =
    "Avoid irrelevant or sensitive data, such as age, "
    + "financials, precise location, and credentials";

// Create memory store
MemoryStore memoryStore = projectClient.MemoryStores.CreateMemoryStore(
    name: memoryStoreName,
    definition: memoryStoreDefinition,
    description: "Memory store for customer support agent"
);

Console.WriteLine($"Created memory store: {memoryStore.Name}");
```

:::zone-end

:::zone pivot="typescript"

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import type {
  MemoryStoreDefaultDefinition,
  MemoryStoreDefaultOptions,
} from "@azure/ai-projects";
import { AIProjectClient } from "@azure/ai-projects";

const projectEndpoint =
  process.env["FOUNDRY_PROJECT_ENDPOINT"] ||
  "<project endpoint>";
const chatModelDeployment =
  process.env["MEMORY_STORE_CHAT_MODEL_DEPLOYMENT_NAME"] ||
  "<chat model deployment name>";
const embeddingModelDeployment =
  process.env["MEMORY_STORE_EMBEDDING_MODEL_DEPLOYMENT_NAME"] ||
  "<embedding model deployment name>";

const memoryStoreName = "my_memory_store";

const project = new AIProjectClient(
  projectEndpoint,
  new DefaultAzureCredential(),
);

const memoryOptions: MemoryStoreDefaultOptions = {
  user_profile_enabled: true,
  chat_summary_enabled: true,
  user_profile_details:
    "Avoid irrelevant or sensitive data, such as age, " +
    "financials, precise location, and credentials",
};

const definition: MemoryStoreDefaultDefinition = {
  kind: "default",
  chat_model: chatModelDeployment,
  embedding_model: embeddingModelDeployment,
  options: memoryOptions,
};

const memoryStore = await project.beta.memoryStores.create(
  memoryStoreName,
  definition,
  {
    description: "Memory store for customer support agent",
  },
);

console.log(
  `Created memory store: ${memoryStore.name} (${memoryStore.id})`,
);
```

:::zone-end

:::zone pivot="rest"

```bash
curl -X POST "${FOUNDRY_PROJECT_ENDPOINT}/memory_stores?api-version=${API_VERSION}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my_memory_store",
    "description": "Memory store for customer support agent",
    "definition": {
      "kind": "default",
      "chat_model": "'"${MEMORY_STORE_CHAT_MODEL_DEPLOYMENT_NAME}"'",
      "embedding_model": "'"${MEMORY_STORE_EMBEDDING_MODEL_DEPLOYMENT_NAME}"'",
      "options": {
        "chat_summary_enabled": true,
        "user_profile_enabled": true,
        "user_profile_details": "Avoid irrelevant or sensitive data, such as age, financials, precise location, and credentials"
      }
    }
  }'
```

:::zone-end

> [!TIP]
> + The remaining Python, C#, and TypeScript snippets build on the client and variables defined in [Create a memory store](#create-a-memory-store). If you run those code snippets independently, include the import and client initialization code from this section.
> + The C# snippets in this article use synchronous methods. For asynchronous usage, see the [memory search tool](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Extensions.OpenAI/samples/Sample5_MemorySearchTool.md) and [memory store](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Projects/samples/Sample20_MemoryStore.md) samples.

### Customize memory

Customize what information the agent stores to keep memory efficient, relevant, and privacy-respecting. Use the `user_profile_details` parameter to specify the types of data that are critical to the agent's function.

For example, set `user_profile_details` to prioritize "flight carrier preference and dietary restrictions" for a travel agent. This focused approach helps the memory system know which details to extract, summarize, and commit to long-term memory.

You can also use this parameter to exclude certain types of data, keeping memory lean and compliant with privacy requirements. For example, set `user_profile_details` to "avoid irrelevant or sensitive data, such as age, financials, precise location, and credentials."

## Update a memory store

Update memory store properties, such as `description` or `metadata`, to better manage memory stores.

:::zone pivot="python"

```python
# Update memory store properties
updated_store = project_client.beta.memory_stores.update(
    name=memory_store_name,
    description="Updated description"
)

print(f"Updated: {updated_store.description}")
```

:::zone-end

:::zone pivot="csharp"

```csharp
// Update memory store properties
MemoryStore updatedStore = projectClient.MemoryStores.UpdateMemoryStore(
    name: memoryStoreName,
    description: "Updated description"
);

Console.WriteLine($"Updated: {updatedStore.Description}");
```

:::zone-end

:::zone pivot="typescript"

```typescript
const updatedStore = await project.beta.memoryStores.update(
  memoryStoreName,
  {
    description: "Updated description",
  },
);

console.log(`Updated: ${updatedStore.description}`);
```

:::zone-end

:::zone pivot="rest"

```bash
MEMORY_STORE_NAME="my_memory_store"

curl -X POST "${FOUNDRY_PROJECT_ENDPOINT}/memory_stores/${MEMORY_STORE_NAME}?api-version=${API_VERSION}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Updated description"
  }'
```

:::zone-end

## List memory stores

Retrieve a list of memory stores in your project to manage and monitor your memory infrastructure.

:::zone pivot="python"

```python
# List all memory stores
stores_list = list(project_client.beta.memory_stores.list())

print(f"Found {len(stores_list)} memory stores")
for store in stores_list:
    print(f"- {store.name} ({store.description})")
```

:::zone-end

:::zone pivot="csharp"

```csharp
// List all memory stores
foreach (MemoryStore store in projectClient.MemoryStores.GetMemoryStores())
{
    Console.WriteLine(
        $"Memory store: {store.Name} ({store.Description})");
}
```

:::zone-end

:::zone pivot="typescript"

```typescript
const storeList = project.beta.memoryStores.list();

console.log("Listing all memory stores...");
for await (const store of storeList) {
  console.log(`  - Memory Store: ${store.name} (${store.id})`);
}
```

:::zone-end

:::zone pivot="rest"

```bash
curl -X GET "${FOUNDRY_PROJECT_ENDPOINT}/memory_stores?api-version=${API_VERSION}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

:::zone-end

## Use memories via an agent tool

After you create a memory store, you can attach the memory search tool to a prompt agent. This tool enables the agent to read from and write to your memory store during conversations. Configure the tool with the appropriate `scope` and `update_delay` to control how and when memories are updated.

> [!TIP]
> To scope memories to an individual end user, set `scope` to `"{{$userId}}"` in the tool definition and pass `x-memory-user-id: <user-id>` as a header on each response call. The system resolves the scope to that user's identity. Without the header, the scope falls back to the caller's Microsoft Entra identity (TID and OID). For more information, see [Understand scope](#understand-scope).

:::zone pivot="python"

```python
from azure.ai.projects.models import MemorySearchPreviewTool, PromptAgentDefinition

# Set scope to associate the memories with
scope = "user_123"

openai_client = project_client.get_openai_client()

# Create memory search tool
tool = MemorySearchPreviewTool(
    memory_store_name=memory_store_name,
    scope=scope,
    update_delay=1, # Wait 1 second of inactivity before updating memories
    # In a real application, set this to a higher value like 300 (5 minutes, default)
)

# Create a prompt agent with memory search tool
agent = project_client.agents.create_version(
    agent_name="MyAgent",
    definition=PromptAgentDefinition(
        model=os.environ["MEMORY_STORE_CHAT_MODEL_DEPLOYMENT_NAME"],
        instructions="You are a helpful assistant that answers general questions",
        tools=[tool],
    )
)

print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")
```

:::zone-end

:::zone pivot="csharp"

```csharp
using Azure.AI.Projects.Agents;
using Azure.AI.Extensions.OpenAI;
using OpenAI.Responses;

#pragma warning disable OPENAI001

// Set scope to associate the memories with
string scope = "user_123";

// Create a prompt agent with memory search tool
DeclarativeAgentDefinition agentDefinition = new(model: chatModel)
{
    Instructions = "You are a helpful assistant that answers "
        + "general questions",
};
agentDefinition.Tools.Add(new MemorySearchPreviewTool(
    memoryStoreName: memoryStore.Name,
    scope: scope)
{
    UpdateDelayInSecs = 1, // Wait 1 second of inactivity before updating memories
    // In a real application, set this to a higher value
    // like 300 (5 minutes, default)
});

ProjectsAgentVersion agent =
    projectClient.AgentAdministrationClient.CreateAgentVersion(
        agentName: "MyAgent",
        options: new(agentDefinition));

Console.WriteLine(
    $"Agent created (id: {agent.Id}, name: {agent.Name}, "
    + $"version: {agent.Version})");
```

:::zone-end

:::zone pivot="typescript"

```typescript
// Set scope to associate the memories with
const scope = "user_123";

const agent = await project.agents.createVersion(
  "memory-search-agent",
  {
    kind: "prompt",
    model: chatModelDeployment,
    instructions:
      "You are a helpful assistant that retrieves relevant " +
      "information from the user's memory store to answer their questions.",
    tools: [
      {
        type: "memory_search_preview",
        memory_store_name: memoryStoreName,
        scope: scope,
        update_delay: 1,
      },
    ],
  },
);

console.log(
  `Created agent with memory search tool, agent ID: ${agent.id}, ` +
    `name: ${agent.name}, version: ${agent.version}`,
);
```

:::zone-end

:::zone pivot="rest"

```bash
# The agents API uses api-version=v1, which differs from the memory store API version
curl -X POST "${FOUNDRY_PROJECT_ENDPOINT}/agents?api-version=v1" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MyAgent",
    "definition": {
        "kind": "prompt",
        "model": "gpt-5.2",
        "instructions": "You are a helpful assistant that answers general questions",
        "tools": [
            {
              "type": "memory_search_preview",
              "memory_store_name": "my_memory_store",
              "scope": "user_123",
              "update_delay": 1
            }
        ]
    }
}'
```

:::zone-end

### Create a conversation

You can now create conversations and request agent responses. At the start of each conversation, static memories are injected so the agent has immediate, persistent context. Contextual memories are retrieved per turn based on the latest messages to inform each response.

After each agent response, the service internally calls `update_memories`. However, actual writes to long‑term memory are debounced by the `update_delay` setting. The update is scheduled and only completes after the configured period of inactivity.

:::zone pivot="python"

```python
import time

# Create a conversation with the agent with memory tool enabled
conversation = openai_client.conversations.create()
print(f"Created conversation (id: {conversation.id})")

# Create an agent response to initial user message
response = openai_client.responses.create(
    input="I prefer dark roast coffee",
    conversation=conversation.id,
    extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
    # To scope memories to an end user, uncomment:
    # extra_headers={"x-memory-user-id": "<user-id>"},
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
    extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
)

print(f"Response output: {new_response.output_text}")
```

:::zone-end

:::zone pivot="csharp"

```csharp
using System.Threading;

#pragma warning disable OPENAI001

// Get a response client scoped to the agent
ProjectResponsesClient responseClient =
    projectClient.ProjectOpenAIClient
        .GetProjectResponsesClientForAgent(agent.Name);

// Create an agent response to initial user message
ResponseItem request = ResponseItem.CreateUserMessageItem(
    "I prefer dark roast coffee");
ResponseResult response = responseClient.CreateResponse([request]);
// To scope memories to an end user, uncomment:
// var options = new CreateResponseOptions();
// options.InputItems.Add(request);
// var requestOptions = new RequestOptions();
// requestOptions.AddHeader("x-memory-user-id", "<user-id>");
// ClientResult result = responseClient.CreateResponse(
//     BinaryContent.Create(options), requestOptions);
// ResponseResult response = ModelReaderWriter.Read<ResponseResult>(
//     result.GetRawResponse().Content);

Console.WriteLine($"Response output: {response.GetOutputText()}");

// After inactivity, memories are extracted and stored
Console.WriteLine("Waiting for memories to be stored...");
Thread.Sleep(65_000);

// Create a new response to demonstrate cross-session recall
ResponseItem newRequest = ResponseItem.CreateUserMessageItem(
    "Please order my usual coffee");
ResponseResult newResponse = responseClient.CreateResponse(
    [newRequest]);

Console.WriteLine(
    $"Response output: {newResponse.GetOutputText()}");
```

:::zone-end

:::zone pivot="typescript"

```typescript
import { setTimeout } from "timers/promises";

const openaiClient = project.getOpenAIClient();

// Create a conversation with the agent with memory tool enabled
const conversation = await openaiClient.conversations.create();
console.log(`Created conversation (id: ${conversation.id})`);

// Create an agent response to initial user message
const response = await openaiClient.responses.create(
  {
    conversation: conversation.id,
    input: "I prefer dark roast coffee",
  },
  {
    body: {
      agent: { name: agent.name, type: "agent_reference" },
    },
    // To scope memories to an end user, uncomment:
    // headers: { "x-memory-user-id": "<user-id>" },
  },
);

console.log(`Response output: ${response.output_text}`);

// After inactivity, memories are extracted and stored
console.log("Waiting for memories to be stored...");
await setTimeout(65_000);

// Create a new conversation to demonstrate cross-session recall
const newConversation = await openaiClient.conversations.create();
console.log(`Created new conversation (id: ${newConversation.id})`);

// Create an agent response with stored memories
const newResponse = await openaiClient.responses.create(
  {
    conversation: newConversation.id,
    input: "Please order my usual coffee",
  },
  {
    body: {
      agent: { name: agent.name, type: "agent_reference" },
    },
  },
);

console.log(`Response output: ${newResponse.output_text}`);
```

:::zone-end

:::zone pivot="rest"

```bash
curl -X POST "${FOUNDRY_PROJECT_ENDPOINT}/openai/v1/conversations" \
    -H "Authorization: Bearer ${ACCESS_TOKEN}" \
    -H "Content-Type: application/json" \
    -d '{}'

# Copy the "id" field from the previous response
# To scope memories to an end user, add -H "x-memory-user-id: <user-id>" to the following request
curl -X POST "${FOUNDRY_PROJECT_ENDPOINT}/openai/v1/responses" \
    -H "Authorization: Bearer ${ACCESS_TOKEN}" \
    -H "Content-Type: application/json" \
    -d '{
      "input": "I prefer dark roast coffee",
      "conversation": "{conversation-id}",
      "agent_reference": {
        "type": "agent_reference",
        "name": "MyAgent"
      }
    }'
```

:::zone-end

## Use memories via APIs

You can interact with a memory store directly using the memory store APIs. Start by adding memories from conversation content to the memory store, and then search for relevant memories to provide context for agent interactions.

### Add memories to a memory store

Add memories by providing conversation content to the memory store. The system preprocesses and postprocesses the data, including memory extraction and consolidation, to optimize the agent's memory. This long-running operation might take about one minute.

Decide how to segment memory across users by specifying the `scope` parameter. You can scope the memory to a specific end user, a team, or another identifier.

You can update a memory store with content from multiple conversation turns, or update after each turn and chain updates using the previous update operation ID.

:::zone pivot="python"

```python
# Set scope to associate the memories with
scope = "user_123"

user_message = {
  "role": "user",
  "content": "I prefer dark roast coffee and usually drink it in the morning",
   "type": "message"
}

update_poller = project_client.beta.memory_stores.begin_update_memories(
    name=memory_store_name,
    scope=scope,
    items=[user_message], # Pass conversation items that you want to add to memory
    update_delay=0, # Trigger update immediately without waiting for inactivity
)

# Wait for the update operation to complete, but can also fire and forget
update_result = update_poller.result()
print(f"Updated with {len(update_result.memory_operations)} memory operations")
for operation in update_result.memory_operations:
    print(
        f"  - Operation: {operation.kind}, Memory ID: {operation.memory_item.memory_id}, Content: {operation.memory_item.content}"
    )

# Extend the previous update with another update and more messages
new_message = {
    "role":"user", 
    "content":"I also like cappuccinos in the afternoon", 
    "type":"message"}

new_update_poller = project_client.beta.memory_stores.begin_update_memories(
    name=memory_store_name,
    scope=scope,
    items=[new_message],
    previous_update_id=update_poller.update_id, # Extend from previous update ID
    update_delay=0, # Trigger update immediately without waiting for inactivity
)
new_update_result = new_update_poller.result()
for operation in new_update_result.memory_operations:
    print(
        f"  - Operation: {operation.kind}, Memory ID: {operation.memory_item.memory_id}, Content: {operation.memory_item.content}"
    )
```

:::zone-end

:::zone pivot="csharp"

```csharp
#pragma warning disable OPENAI001

// Set scope to associate the memories with
string scope = "user_123";

MemoryUpdateOptions memoryOptions = new(scope)
{
    UpdateDelay = 0, // Trigger update immediately without waiting for inactivity
};
memoryOptions.Items.Add(ResponseItem.CreateUserMessageItem(
    "I prefer dark roast coffee and usually drink it "
    + "in the morning"));

// Wait for the update operation to complete
MemoryUpdateResult updateResult =
    projectClient.MemoryStores.WaitForMemoriesUpdate(
        memoryStoreName: memoryStore.Name,
        options: memoryOptions,
        pollingInterval: 500);

if (updateResult.Status == MemoryStoreUpdateStatus.Failed)
{
    throw new InvalidOperationException(
        updateResult.ErrorDetails);
}
Console.WriteLine(
    $"Updated with {updateResult.Details.MemoryOperations.Count} "
    + "memory operations");
foreach (var operation in updateResult.Details.MemoryOperations)
{
    Console.WriteLine(
        $"  - Operation: {operation.Kind}, "
        + $"Memory ID: {operation.MemoryItem.MemoryId}, "
        + $"Content: {operation.MemoryItem.Content}");
}

// Extend the previous update with another message
MemoryUpdateOptions newMemoryOptions = new(scope)
{
    PreviousUpdateId = updateResult.UpdateId,
    UpdateDelay = 0, // Trigger update immediately without waiting for inactivity
};
newMemoryOptions.Items.Add(ResponseItem.CreateUserMessageItem(
    "I also like cappuccinos in the afternoon"));

MemoryUpdateResult newUpdateResult =
    projectClient.MemoryStores.WaitForMemoriesUpdate(
        memoryStoreName: memoryStore.Name,
        options: newMemoryOptions,
        pollingInterval: 500);

if (newUpdateResult.Status == MemoryStoreUpdateStatus.Failed)
{
    throw new InvalidOperationException(
        newUpdateResult.ErrorDetails);
}
foreach (var operation in newUpdateResult.Details.MemoryOperations)
{
    Console.WriteLine(
        $"  - Operation: {operation.Kind}, "
        + $"Memory ID: {operation.MemoryItem.MemoryId}, "
        + $"Content: {operation.MemoryItem.Content}");
}
```

:::zone-end

:::zone pivot="typescript"

```typescript
const scope = "user_123";

const userMessage: Record<string, unknown> = {
  type: "message",
  role: "user",
  content: [
    {
      type: "input_text",
      text: "I prefer dark roast coffee and usually drink it in the morning",
    },
  ],
};

console.log("\nSubmitting memory update request...");
const updatePoller = project.beta.memoryStores.updateMemories(
  memoryStoreName,
  scope,
  {
    items: [userMessage],
    updateDelayInSecs: 0,
  },
);

const updateResult = await updatePoller.pollUntilDone();
console.log(
  `Updated with ${updateResult.memory_operations.length} ` +
    `memory operation(s)`,
);
for (const operation of updateResult.memory_operations) {
  console.log(
    `  - Operation: ${operation.kind}, ` +
      `Memory ID: ${operation.memory_item.memory_id}, ` +
      `Content: ${operation.memory_item.content}`,
  );
}

// Extend the previous update with another message
const newMessage = {
  role: "user",
  content: "I also like cappuccinos in the afternoon",
  type: "message",
};

const newUpdatePoller = project.beta.memoryStores.updateMemories(
  memoryStoreName,
  scope,
  {
    items: [newMessage],
    updateDelayInSecs: 0,
  },
);

const newUpdateResult = await newUpdatePoller.pollUntilDone();
console.log(
  `Updated with ${newUpdateResult.memory_operations.length} ` +
    `memory operation(s)`,
);
for (const operation of newUpdateResult.memory_operations) {
  console.log(
    `  - Operation: ${operation.kind}, ` +
      `Memory ID: ${operation.memory_item.memory_id}, ` +
      `Content: ${operation.memory_item.content}`,
  );
}
```

:::zone-end

:::zone pivot="rest"

```bash
curl -X POST "${FOUNDRY_PROJECT_ENDPOINT}/memory_stores/my_memory_store:update_memories?api-version=${API_VERSION}" \
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
curl -X GET "${FOUNDRY_PROJECT_ENDPOINT}/memory_stores/my_memory_store/updates/${UPDATE_ID}?api-version=${API_VERSION}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

:::zone-end

### Search for memories in a memory store

Search memories to retrieve relevant context for agent interactions. Specify the memory store name and scope to narrow the search.

:::zone pivot="python"

```python
from azure.ai.projects.models import MemorySearchOptions

# Search memories by a query
query_message = {"role": "user", "content": "What are my coffee preferences?", "type": "message"}

search_response = project_client.beta.memory_stores.search_memories(
    name=memory_store_name,
    scope=scope,
    items=[query_message],
    options=MemorySearchOptions(max_memories=5)
)
print(f"Found {len(search_response.memories)} memories")
for memory in search_response.memories:
    print(f"  - Memory ID: {memory.memory_item.memory_id}, Content: {memory.memory_item.content}")
```

:::zone-end

:::zone pivot="csharp"

```csharp
#pragma warning disable OPENAI001

// Search memories by a query
MemorySearchOptions searchOptions = new(scope)
{
    Items =
    {
        ResponseItem.CreateUserMessageItem(
            "What are my coffee preferences?")
    },
    ResultOptions = new() { MaxMemories = 5 },
};

MemoryStoreSearchResponse searchResponse =
    projectClient.MemoryStores.SearchMemories(
        memoryStoreName: memoryStore.Name,
        options: searchOptions);

Console.WriteLine(
    $"Found {searchResponse.Memories.Count} memories");
foreach (MemorySearchItem item in searchResponse.Memories)
{
    Console.WriteLine(
        $"  - Content: {item.MemoryItem.Content}");
}
```

:::zone-end

:::zone pivot="typescript"

```typescript
const queryMessage: Record<string, unknown> = {
  type: "message",
  role: "user",
  content: [
    { type: "input_text", text: "What are my coffee preferences?" },
  ],
};

console.log("\nSearching memories for stored preferences...");
const searchResponse =
  await project.beta.memoryStores.searchMemories(
    memoryStoreName,
    scope,
    {
      items: [queryMessage],
      options: { max_memories: 5 },
    },
  );

console.log(`Found ${searchResponse.memories.length} memory item(s)`);
for (const memory of searchResponse.memories) {
  console.log(
    `  - Memory ID: ${memory.memory_item.memory_id}, ` +
      `Content: ${memory.memory_item.content}`,
  );
}
```

:::zone-end

:::zone pivot="rest"

```bash
curl -X POST "${FOUNDRY_PROJECT_ENDPOINT}/memory_stores/my_memory_store:search_memories?api-version=${API_VERSION}" \
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

:::zone-end

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

:::zone pivot="python"

```python
# Delete memories for a specific scope
project_client.beta.memory_stores.delete_scope(
    name=memory_store_name,
    scope="user_123"
)

print(f"Deleted memories for scope: user_123")
```

:::zone-end

:::zone pivot="csharp"

```csharp
// Delete memories for a specific scope
MemoryStoreDeleteScopeResponse deleteScopeResponse =
    projectClient.MemoryStores.DeleteScope(
        name: memoryStore.Name,
        scope: "user_123");

Console.WriteLine(
    $"Deleted scope: {deleteScopeResponse.Name}, "
    + $"success: {deleteScopeResponse.IsDeleted}");
```

:::zone-end

:::zone pivot="typescript"

```typescript
console.log("\nDeleting memories for scope...");
await project.beta.memoryStores.deleteScope(memoryStoreName, scope);
```

:::zone-end

:::zone pivot="rest"

```bash
curl -X POST "${FOUNDRY_PROJECT_ENDPOINT}/memory_stores/my_memory_store:delete_scope?api-version=${API_VERSION}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "scope": "user_123"
  }'
```

:::zone-end

### Delete a memory store

Remove the entire memory store and all associated memories across all scopes. This operation is irreversible.

:::zone pivot="python"

```python
# Delete the entire memory store
delete_response = project_client.beta.memory_stores.delete(memory_store_name)
print(f"Deleted memory store: {delete_response.deleted}")
```

:::zone-end

:::zone pivot="csharp"

```csharp
// Delete the entire memory store
DeleteMemoryStoreResponse deleteResponse =
    projectClient.MemoryStores.DeleteMemoryStore(
        name: memoryStore.Name);

Console.WriteLine(
    $"Deleted memory store: {deleteResponse.Name}, "
    + $"success: {deleteResponse.IsDeleted}");
```

:::zone-end

:::zone pivot="typescript"

```typescript
console.log("Deleting memory store...");
await project.beta.memoryStores.delete(memoryStoreName);
```

:::zone-end

:::zone pivot="rest"

```bash
curl -X DELETE "${FOUNDRY_PROJECT_ENDPOINT}/memory_stores/my_memory_store?api-version=${API_VERSION}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

:::zone-end

## Best practices

- **Implement per-user access controls:** Avoid giving agents access to memories shared across all users. Use the `scope` property to partition the memory store by user. When you share `scope` across users, use `user_profile_details` to instruct the memory system not to store personal information.

- **Map scope to the end user:** When you use the [memory search tool](#use-memories-via-an-agent-tool), set `scope` to `{{$userId}}` in the tool definition. The system resolves the user identity from the `x-memory-user-id` request header, if present. Otherwise, it falls back to the caller's Microsoft Entra token (`{tid}_{oid}`).

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
| The agent response doesn’t use stored memory. | The agent isn’t configured with the memory search tool, or the memory store name is incorrect. | Confirm the agent definition includes the `memory_search_preview` tool and references the correct memory store name. |

## Related content

:::zone pivot="python"

- [Azure AI Projects client library for Python: Memory samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/memories)
- [Memory store REST API reference](../../reference/foundry-project-rest-preview.md)
- [Memory in Foundry Agent Service](../concepts/what-is-memory.md)
- [Foundry Agent Service quotas and limits](../concepts/limits-quotas-regions.md)
- [Build an agent with Microsoft Foundry](../../quickstarts/get-started-code.md)

:::zone-end

:::zone pivot="csharp"

- [Azure AI Extensions for OpenAI: Memory search tool sample](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Extensions.OpenAI/samples/Sample5_MemorySearchTool.md)
- [Azure AI Projects client library for .NET: Memory store sample](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Projects/samples/Sample20_MemoryStore.md)
- [Memory store REST API reference](../../reference/foundry-project-rest-preview.md)
- [Memory in Foundry Agent Service](../concepts/what-is-memory.md)
- [Foundry Agent Service quotas and limits](../concepts/limits-quotas-regions.md)
- [Build an agent with Microsoft Foundry](../../quickstarts/get-started-code.md)

:::zone-end

:::zone pivot="typescript"

- [Azure AI Projects client library for JavaScript: Memory samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-projects/samples/v2/javascript/memories)
- [Memory store REST API reference](../../reference/foundry-project-rest-preview.md)
- [Memory in Foundry Agent Service](../concepts/what-is-memory.md)
- [Foundry Agent Service quotas and limits](../concepts/limits-quotas-regions.md)
- [Build an agent with Microsoft Foundry](../../quickstarts/get-started-code.md)

:::zone-end

:::zone pivot="rest"

- [Memory store REST API reference](../../reference/foundry-project-rest-preview.md)
- [Memory in Foundry Agent Service](../concepts/what-is-memory.md)
- [Foundry Agent Service quotas and limits](../concepts/limits-quotas-regions.md)
- [Build an agent with Microsoft Foundry](../../quickstarts/get-started-code.md)

:::zone-end
