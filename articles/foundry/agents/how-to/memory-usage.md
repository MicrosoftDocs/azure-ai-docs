---
title: Create and Use Memory
description: Learn how to create and manage memory in Foundry Agent Service to enable AI agents to retain context across sessions and personalize user interactions
author: haileytap
ms.author: haileytapia
ms.reviewer: liulewis
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 06/08/2026
ms.custom: pilot-ai-workflow-jan-2026, doc-kit-assisted
ai-usage: ai-assisted
zone_pivot_groups: foundry-memory-store
#customer intent: As a developer, I want to attach a memory store to my AI agent so that it can access and update memories during interactions.
---

# Create and use memory in Foundry Agent Service (preview)

> [!IMPORTANT]
> Memory (preview) in Foundry Agent Service and the Memory Store API (preview) are licensed to you as part of your Azure subscription and are subject to terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/product/ForOnlineServices/all), the [Microsoft Products and Services Data Protection Addendum](https://aka.ms/DPA), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> The latest preview offers new capabilities and enhancements, including:
>
> - Memory item operations to create, read, update, list, and delete individual memory records.
> - Store-level default retention controls, including default TTL for newly created memory stores.
> - Direct remember-or-forget synchronized memory command behavior.

Memory in Foundry Agent Service is a managed, long-term memory solution. It enables agent continuity across sessions, devices, and workflows. By creating and managing memory stores, you can build agents that retain user preferences, maintain conversation history, and deliver personalized experiences.

Memory stores act as persistent storage, defining which types of information are relevant to each agent. You control access using the `scope` parameter, which segments memory across users to ensure secure and isolated experiences.

This article explains how to create, manage, and use memory stores. For conceptual information, see [Memory in Foundry Agent Service](../concepts/what-is-memory.md).

### Usage support

| Capability | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API |
| --- | --- | --- | --- | --- | --- |
| Create, update, list, and delete memory stores | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| Attach memory to a prompt agent | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| Update and search memories | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| Create, read, update, list, and delete memory items | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

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
    1. Assign **Foundry User** to the managed identity of your project.

       [!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]

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
dotnet add package Azure.AI.Projects
dotnet add package Azure.AI.Projects.Agents
dotnet add package Azure.AI.Extensions.OpenAI
dotnet add package Azure.Identity
```

:::zone-end

:::zone pivot="typescript"

Install the required packages:

```bash
npm install @azure/ai-projects@2 @azure/identity
```

:::zone-end

:::zone pivot="java"

Install the required packages:

```xml
<dependency>
  <groupId>com.azure</groupId>
  <artifactId>azure-ai-agents</artifactId>
</dependency>
<dependency>
  <groupId>com.azure</groupId>
  <artifactId>azure-identity</artifactId>
</dependency>
```

:::zone-end

:::zone pivot="python,csharp,typescript,java"

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

Use memory store options to control extraction behavior and retention defaults. In the latest preview, you can enable procedural memory and set a default TTL (seconds) for newly created memory entries.

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
    procedural_memory_enabled=True,
    default_ttl_seconds=30 * 24 * 60 * 60,
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
    description="Memory store with procedural memory and 30-day default TTL",
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
  procedural_memory_enabled: true,
  default_ttl_seconds: 30 * 24 * 60 * 60,
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
    description: "Memory store with procedural memory and 30-day default TTL",
  },
);

console.log(
  `Created memory store: ${memoryStore.name} (${memoryStore.id})`,
);
```

:::zone-end

:::zone pivot="java"

```java
import com.azure.ai.agents.AgentsClientBuilder;
import com.azure.ai.agents.MemoryStoresClient;
import com.azure.ai.agents.models.MemoryStoreDefaultDefinition;
import com.azure.ai.agents.models.MemoryStoreDefaultOptions;
import com.azure.ai.agents.models.MemoryStoreDetails;
import com.azure.identity.DefaultAzureCredentialBuilder;

String projectEndpoint = System.getenv("FOUNDRY_PROJECT_ENDPOINT");
String chatModel = System.getenv("MEMORY_STORE_CHAT_MODEL_DEPLOYMENT_NAME");
String embeddingModel =
  System.getenv("MEMORY_STORE_EMBEDDING_MODEL_DEPLOYMENT_NAME");

MemoryStoresClient memoryStoresClient = new AgentsClientBuilder()
  .credential(new DefaultAzureCredentialBuilder().build())
  .endpoint(projectEndpoint)
  .buildMemoryStoresClient();

String memoryStoreName = "my_memory_store";

MemoryStoreDefaultDefinition definition =
  new MemoryStoreDefaultDefinition(chatModel, embeddingModel)
    .setOptions(new MemoryStoreDefaultOptions(true, true));

MemoryStoreDetails memoryStore = memoryStoresClient.createMemoryStore(
  memoryStoreName,
  definition,
  "Memory store for customer support agent",
  null);

System.out.println("Created memory store: " + memoryStore.getName());
```

:::zone-end

:::zone pivot="rest"

```bash
curl -X POST "${FOUNDRY_PROJECT_ENDPOINT}/memory_stores?api-version=${API_VERSION}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my_memory_store",
    "description": "Memory store with procedural memory and 30-day default TTL",
    "definition": {
      "kind": "default",
      "chat_model": "'"${MEMORY_STORE_CHAT_MODEL_DEPLOYMENT_NAME}"'",
      "embedding_model": "'"${MEMORY_STORE_EMBEDDING_MODEL_DEPLOYMENT_NAME}"'",
      "options": {
        "chat_summary_enabled": true,
        "user_profile_enabled": true,
        "procedural_memory_enabled": true,
        "default_ttl_seconds": 2592000,
        "user_profile_details": "Avoid irrelevant or sensitive data, such as age, financials, precise location, and credentials"
      }
    }
  }'
```

:::zone-end

> [!TIP]
> - The remaining Python, C#, TypeScript, and Java snippets build on the client and variables defined in [Create a memory store](#create-a-memory-store). If you run those code snippets independently, include the import and client initialization code from this section.
>
> - The C# snippets in this article use synchronous methods. For asynchronous usage, see the [memory search tool](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Extensions.OpenAI/samples/Sample5_MemorySearchTool.md) and [memory store](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Projects/samples/Sample20_MemoryStore.md) samples.

### Customize memory

Customize what information the agent stores to keep memory efficient, relevant, and privacy-respecting. Use the `user_profile_details` parameter to specify the types of data that are critical to the agent's function.

For example, set `user_profile_details` to prioritize "flight carrier preference and dietary restrictions" for a travel agent. This focused approach helps the memory system know which details to extract, summarize, and commit to long-term memory.

You can also use this parameter to exclude certain types of data, keeping memory lean and compliant with privacy requirements. For example, set `user_profile_details` to "avoid irrelevant or sensitive data, such as age, financials, precise location, and credentials."

### Configure TTL and retention policies

TTL applies to all memories, whether from direct memory commands, extraction and consolidation, or item-level CRUD operations. If a memory is updated and consolidated, the service resets its last-updated time.

TTL applies only to memory stores created after TTL support was introduced. It doesn't affect existing memory stores.

A `default_ttl_seconds` value of `0` indicates no expiration. Choose a retention period that matches your compliance and user-data lifecycle requirements.

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

:::zone pivot="java"

```java
import com.azure.ai.agents.models.MemoryStoreDetails;

MemoryStoreDetails updatedStore = memoryStoresClient.updateMemoryStore(
  memoryStoreName,
  "Updated description",
  null);

System.out.println("Updated: " + updatedStore.getDescription());
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

:::zone pivot="java"

```java
import com.azure.ai.agents.models.MemoryStoreDetails;

System.out.println("Listing all memory stores...");
for (MemoryStoreDetails store : memoryStoresClient.listMemoryStores()) {
    System.out.println(
        "  - Memory Store: " + store.getName() + " (" + store.getId() + ")");
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

:::zone pivot="java"

```java
import com.azure.ai.agents.AgentsClient;
import com.azure.ai.agents.AgentsClientBuilder;
import com.azure.ai.agents.models.AgentVersionDetails;
import com.azure.ai.agents.models.MemorySearchPreviewTool;
import com.azure.ai.agents.models.PromptAgentDefinition;
import com.azure.identity.DefaultAzureCredentialBuilder;

String scope = "user_123";

AgentsClient agentsClient = new AgentsClientBuilder()
  .credential(new DefaultAzureCredentialBuilder().build())
  .endpoint(projectEndpoint)
  .buildAgentsClient();

MemorySearchPreviewTool memoryTool = new MemorySearchPreviewTool(
  memoryStoreName,
  scope).setUpdateDelaySeconds(1);

PromptAgentDefinition agentDefinition = new PromptAgentDefinition(chatModel)
  .setInstructions("You are a helpful assistant that answers general questions")
  .setTools(java.util.Collections.singletonList(memoryTool));

AgentVersionDetails agent =
  agentsClient.createAgentVersion("MyAgent", agentDefinition);

System.out.println(
  "Agent created (id: " + agent.getId() + ", name: " + agent.getName()
    + ", version: " + agent.getVersion() + ")");
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

> [!NOTE]
> In the updated preview schema, the memory search tool output uses a `memories` collection instead of the legacy `results` field. If you process raw output payloads, update your parsers accordingly.

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

:::zone pivot="java"

```java
import com.azure.ai.agents.ResponsesClient;
import com.azure.ai.agents.AgentsClientBuilder;
import com.azure.ai.agents.models.AgentReference;
import com.azure.ai.agents.models.AzureCreateResponseOptions;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

ResponsesClient responsesClient = new AgentsClientBuilder()
  .credential(new DefaultAzureCredentialBuilder().build())
  .endpoint(projectEndpoint)
  .buildResponsesClient();

AgentReference agentReference = new AgentReference(agent.getName())
  .setVersion(agent.getVersion());

Response response = responsesClient.createAzureResponse(
  new AzureCreateResponseOptions().setAgentReference(agentReference),
  ResponseCreateParams.builder()
    .input("I prefer dark roast coffee"));

System.out.println("Response output: " + response.output());

System.out.println("Waiting for memories to be stored...");
Thread.sleep(65_000);

Response newResponse = responsesClient.createAzureResponse(
  new AzureCreateResponseOptions().setAgentReference(agentReference),
  ResponseCreateParams.builder()
    .input("Please order my usual coffee"));

System.out.println("Response output: " + newResponse.output());
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

### Apply direct remember-or-forget behavior

When a user explicitly asks the agent to remember or forget information, the memory search tool in the `tools` array applies the operation immediately and returns the result as memory command items in the response output. No additional tool configuration is required.

> [!NOTE]
> Direct memory commands don't override memory TTL. If a memory store has TTL configured, memory items can still expire, even if they were added by a remember command.

:::zone pivot="python"

```python
openai_client = project_client.get_openai_client()

# Configure the memory search tool
tools = [
    {
        "type": "memory_search_preview",
        "memory_store_name": memory_store_name,
        "scope": scope,
    }
]

# Ask the agent to remember information
remember_response = openai_client.responses.create(
    model=os.environ["MEMORY_STORE_CHAT_MODEL_DEPLOYMENT_NAME"],
    tools=tools,
    input="Remember that my preferred seat is aisle.",
)

for item in remember_response.output:
    if getattr(item, "type", None) == "memory_command_call":
        print(item.type)       # memory_command_call
        print(item.arguments)  # {"action": "remember", "content": "..."}
        print(item.status)     # completed

# Ask the agent to forget information
forget_response = openai_client.responses.create(
    model=os.environ["MEMORY_STORE_CHAT_MODEL_DEPLOYMENT_NAME"],
    tools=tools,
    input="Forget my preferred seat.",
)

for item in forget_response.output:
    if getattr(item, "type", None) == "memory_command_call":
        print(item.type)
        print(item.arguments)  # {"action": "forget", "content": "..."}
        print(item.status)
```

:::zone-end

:::zone pivot="csharp"

```csharp
// This code snippet is currently unavailable.
```

:::zone-end

:::zone pivot="typescript"

```typescript
const openaiClient = project.getOpenAIClient();

// Configure the memory search tool
const tools = [
  {
    type: "memory_search_preview",
    memory_store_name: memoryStoreName,
    scope: scope,
  },
];

// Ask the agent to remember information
const rememberResponse = await openaiClient.responses.create({
  model: chatModelDeployment,
  input: "Remember that my preferred seat is aisle.",
  tools: tools as any,
});

for (const item of rememberResponse.output) {
  const outputItem = item as Record<string, unknown>;
  if (outputItem["type"] === "memory_command_call") {
    console.log(outputItem["type"]);       // memory_command_call
    console.log(outputItem["arguments"]);
    // {"action": "remember", "content": "..."}
    console.log(outputItem["status"]);     // completed
  }
}

// Ask the agent to forget information
const forgetResponse = await openaiClient.responses.create({
  model: chatModelDeployment,
  input: "Forget my preferred seat.",
  tools: tools as any,
});

for (const item of forgetResponse.output) {
  const outputItem = item as Record<string, unknown>;
  if (outputItem["type"] === "memory_command_call") {
    console.log(outputItem["type"]);
    console.log(outputItem["arguments"]);
    // {"action": "forget", "content": "..."}
    console.log(outputItem["status"]);
  }
}
```

:::zone-end

:::zone pivot="java"

```java
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

Response rememberResponse = responsesClient.createAzureResponse(
  new AzureCreateResponseOptions().setAgentReference(agentReference),
  ResponseCreateParams.builder()
    .input("Remember that my preferred seat is aisle."));

System.out.println(rememberResponse.output());

Response forgetResponse = responsesClient.createAzureResponse(
  new AzureCreateResponseOptions().setAgentReference(agentReference),
  ResponseCreateParams.builder()
    .input("Forget my preferred seat."));

System.out.println(forgetResponse.output());
```

:::zone-end

:::zone pivot="rest"

```bash
# Reuse the {conversation-id} from the previous section
# To scope memories to an end user, set x-memory-user-id in each request
curl -X POST "${FOUNDRY_PROJECT_ENDPOINT}/openai/v1/responses" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -H "x-memory-user-id: <user-id>" \
  -d '{
    "input": "Remember that my preferred seat is aisle.",
    "conversation": "{conversation-id}",
    "agent_reference": {
      "type": "agent_reference",
      "name": "MyAgent"
    }
  }'

curl -X POST "${FOUNDRY_PROJECT_ENDPOINT}/openai/v1/responses" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -H "x-memory-user-id: <user-id>" \
  -d '{
    "input": "Forget my preferred seat.",
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

:::zone pivot="java"

```java
import com.azure.ai.agents.models.MemoryStoreUpdateCompletedResult;
import com.azure.ai.agents.models.MemoryStoreUpdateResponse;
import com.azure.core.util.polling.SyncPoller;
import com.openai.models.responses.EasyInputMessage;
import com.openai.models.responses.ResponseInputItem;
import java.util.Arrays;

ResponseInputItem userMessage = ResponseInputItem.ofEasyInputMessage(
  EasyInputMessage.builder()
    .role(EasyInputMessage.Role.USER)
    .content("I prefer dark roast coffee and usually drink it in the morning")
    .build());

SyncPoller<MemoryStoreUpdateResponse, MemoryStoreUpdateCompletedResult> updatePoller =
  memoryStoresClient.beginUpdateMemories(
    memoryStoreName,
    scope,
    Arrays.asList(userMessage),
    null,
    0);

updatePoller.waitForCompletion();
MemoryStoreUpdateCompletedResult updateResult = updatePoller.getFinalResult();
System.out.println(
  "Updated with " + updateResult.getMemoryOperations().size()
    + " memory operation(s)");
for (var operation : updateResult.getMemoryOperations()) {
  System.out.println(
    "  - Operation: " + operation.getKind() + ", Memory ID: "
      + operation.getMemoryItem().getMemoryId() + ", Content: "
      + operation.getMemoryItem().getContent());
}

ResponseInputItem newMessage = ResponseInputItem.ofEasyInputMessage(
  EasyInputMessage.builder()
    .role(EasyInputMessage.Role.USER)
    .content("I also like cappuccinos in the afternoon")
    .build());

// Pass null for previousUpdateId to start a fresh independent update.
// To chain from the previous update, pass the update ID from the
// intermediate poller response instead.
SyncPoller<MemoryStoreUpdateResponse, MemoryStoreUpdateCompletedResult> newUpdatePoller =
  memoryStoresClient.beginUpdateMemories(
    memoryStoreName,
    scope,
    Arrays.asList(newMessage),
    null,
    0);

newUpdatePoller.waitForCompletion();
MemoryStoreUpdateCompletedResult newUpdateResult = newUpdatePoller.getFinalResult();
for (var newOperation : newUpdateResult.getMemoryOperations()) {
  System.out.println(
    "  - Operation: " + newOperation.getKind() + ", Memory ID: "
      + newOperation.getMemoryItem().getMemoryId() + ", Content: "
      + newOperation.getMemoryItem().getContent());
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

:::zone pivot="java"

```java
import com.azure.ai.agents.models.MemorySearchItem;
import com.azure.ai.agents.models.MemorySearchOptions;
import com.azure.ai.agents.models.MemoryStoreSearchResponse;
import com.openai.models.responses.EasyInputMessage;
import com.openai.models.responses.ResponseInputItem;
import java.util.Arrays;

ResponseInputItem queryMessage = ResponseInputItem.ofEasyInputMessage(
  EasyInputMessage.builder()
    .role(EasyInputMessage.Role.USER)
    .content("What are my coffee preferences?")
    .build());

MemorySearchOptions searchOptions = new MemorySearchOptions()
  .setMaxMemories(5);

MemoryStoreSearchResponse searchResponse = memoryStoresClient.searchMemories(
  memoryStoreName,
  scope,
  Arrays.asList(queryMessage),
  null,
  searchOptions);

System.out.println("Found " + searchResponse.getMemories().size() + " memories");
for (MemorySearchItem item : searchResponse.getMemories()) {
  System.out.println(
    "  - Memory ID: " + item.getMemoryItem().getMemoryId() + ", Content: "
      + item.getMemoryItem().getContent());
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

## Manage memory items

Use item-level operations to directly create, inspect, update, and delete individual memory records. For scope-level or store-level deletion, see [Delete memories](#delete-memories).

:::zone pivot="rest"

:::zone-end

### Create a memory item

:::zone pivot="python"

```python
# Create a memory item directly
created = project_client.beta.memory_stores.create_memory(
    name=memory_store_name,
    scope="defaultUser",
    content="User prefers concise changelogs with impact-first summaries.",
    kind="user_profile",
)

print(f"Memory ID: {created.memory_id}")
print(f"Content: {created.content}")
print(f"Kind: {created.kind}")
```

:::zone-end

:::zone pivot="csharp"

```csharp
// This code snippet is currently unavailable.
```

:::zone-end

:::zone pivot="typescript"

```typescript
// Create a memory item directly
const created = await project.beta.memoryStores.createMemory(
  memoryStoreName,
  "defaultUser",
  "User prefers concise changelogs with impact-first summaries.",
  "user_profile",
);

console.log(`Memory ID: ${created.memory_id}`);
console.log(`Content: ${created.content}`);
console.log(`Kind: ${created.kind}`);
```

:::zone-end

:::zone pivot="java"

```java
import com.azure.ai.agents.models.MemoryItem;
import com.azure.ai.agents.models.MemoryItemKind;

MemoryItem created = memoryStoresClient.createMemory(
  memoryStoreName,
  "defaultUser",
  "User prefers concise changelogs with impact-first summaries.",
  MemoryItemKind.USER_PROFILE);

System.out.println("Memory ID: " + created.getMemoryId());
System.out.println("Content: " + created.getContent());
System.out.println("Kind: " + created.getKind());
```

:::zone-end

:::zone pivot="rest"

```bash
curl -X POST "${FOUNDRY_PROJECT_ENDPOINT}/memory_stores/my_memory_store/items?api-version=${API_VERSION}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "scope": "defaultUser",
    "content": "User prefers concise changelogs with impact-first summaries.",
    "kind": "user_profile"
  }'
```

:::zone-end

### Get a memory item

:::zone pivot="python"

```python
# Retrieve a memory item by ID
item = project_client.beta.memory_stores.get_memory(
    name=memory_store_name,
    memory_id="<memory-item-id>",
)

print(f"Memory ID: {item.memory_id}")
print(f"Content: {item.content}")
print(f"Kind: {item.kind}")
```

:::zone-end

:::zone pivot="csharp"

```csharp
// This code snippet is currently unavailable.
```

:::zone-end

:::zone pivot="typescript"

```typescript
// Retrieve a memory item by ID
const item = await project.beta.memoryStores.getMemory(
  memoryStoreName,
  "<memory-item-id>",
);

console.log(`Memory ID: ${item.memory_id}`);
console.log(`Content: ${item.content}`);
console.log(`Kind: ${item.kind}`);
```

:::zone-end

:::zone pivot="java"

```java
import com.azure.ai.agents.models.MemoryItem;

MemoryItem memItem = memoryStoresClient.getMemory(
  memoryStoreName,
  "<memory-item-id>");

System.out.println("Memory ID: " + memItem.getMemoryId());
System.out.println("Content: " + memItem.getContent());
System.out.println("Kind: " + memItem.getKind());
```

:::zone-end

:::zone pivot="rest"

```bash
curl -X GET "${FOUNDRY_PROJECT_ENDPOINT}/memory_stores/my_memory_store/items/<memory-item-id>?api-version=${API_VERSION}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

:::zone-end

### List memory items

:::zone pivot="python"

```python
# List all memory items in the store
memories = project_client.beta.memory_stores.list_memories(
    name=memory_store_name,
    scope="defaultUser",
)

count = 0
for item in memories:
    count += 1
    print(f"- {item.memory_id} [{item.kind}]: {item.content}")

print(f"Total memories: {count}")
```

:::zone-end

:::zone pivot="csharp"

```csharp
// This code snippet is currently unavailable.
```

:::zone-end

:::zone pivot="typescript"

```typescript
// List all memory items in the store
const memoriesList = project.beta.memoryStores.listMemories(
  memoryStoreName,
  "defaultUser",
);

let count = 0;
for await (const item of memoriesList) {
  count += 1;
  console.log(`- ${item.memory_id} [${item.kind}]: ${item.content}`);
}
console.log(`Total memories: ${count}`);
```

:::zone-end

:::zone pivot="java"

```java
import com.azure.ai.agents.models.ListMemoriesOptions;
import com.azure.ai.agents.models.MemoryItem;

ListMemoriesOptions options = new ListMemoriesOptions(
  memoryStoreName,
  "defaultUser");

int count = 0;
for (MemoryItem memoryEntry : memoryStoresClient.listMemories(options)) {
  count++;
  System.out.println(
    "- " + memoryEntry.getMemoryId() + " [" + memoryEntry.getKind() + "]: "
      + memoryEntry.getContent());
}

System.out.println("Total memories: " + count);
```

:::zone-end

:::zone pivot="rest"

```bash
curl -X GET "${FOUNDRY_PROJECT_ENDPOINT}/memory_stores/my_memory_store/items:list?scope=user_123&api-version=${API_VERSION}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

:::zone-end

### Update a memory item

:::zone pivot="python"

```python
# Update a memory item by ID
updated = project_client.beta.memory_stores.update_memory(
    name=memory_store_name,
    memory_id="<memory-item-id>",
    content="User prefers detailed technical explanations with examples.",
)

print(f"Updated: {updated.content}")
```

:::zone-end

:::zone pivot="csharp"

```csharp
// This code snippet is currently unavailable.
```

:::zone-end

:::zone pivot="typescript"

```typescript
// Update a memory item by ID
const updated = await project.beta.memoryStores.updateMemory(
  memoryStoreName,
  "<memory-item-id>",
  "User prefers detailed technical explanations with examples.",
);

console.log(`Updated: ${updated.content}`);
```

:::zone-end

:::zone pivot="java"

```java
import com.azure.ai.agents.models.MemoryItem;

MemoryItem updated = memoryStoresClient.updateMemory(
  memoryStoreName,
  "<memory-item-id>",
  "User prefers detailed technical explanations with examples.");

System.out.println("Updated: " + updated.getContent());
```

:::zone-end

:::zone pivot="rest"

```bash
curl -X POST "${FOUNDRY_PROJECT_ENDPOINT}/memory_stores/my_memory_store/items/<memory-item-id>?api-version=${API_VERSION}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"content": "User prefers detailed technical explanations with examples."}'
```

:::zone-end

### Delete a memory item

:::zone pivot="python"

```python
# Delete a memory item by ID
project_client.beta.memory_stores.delete_memory(
    name=memory_store_name,
    memory_id="<memory-item-id>",
)

print("Memory item deleted successfully")
```

:::zone-end

:::zone pivot="csharp"

```csharp
// This code snippet is currently unavailable.
```

:::zone-end

:::zone pivot="typescript"

```typescript
// Delete a memory item by ID
await project.beta.memoryStores.deleteMemory(
  memoryStoreName,
  "<memory-item-id>",
);

console.log("Memory item deleted successfully");
```

:::zone-end

:::zone pivot="java"

```java
memoryStoresClient.deleteMemory(memoryStoreName, "<memory-item-id>");

System.out.println("Memory item deleted successfully");
```

:::zone-end

:::zone pivot="rest"

```bash
curl -X DELETE "${FOUNDRY_PROJECT_ENDPOINT}/memory_stores/my_memory_store/items/<memory-item-id>?api-version=${API_VERSION}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

:::zone-end

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

:::zone pivot="java"

```java
memoryStoresClient.deleteScope(memoryStoreName, "user_123");

System.out.println("Deleted memories for scope: user_123");
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

:::zone pivot="java"

```java
memoryStoresClient.deleteMemoryStore(memoryStoreName);

System.out.println("Deleted memory store: " + memoryStoreName);
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

- **Expose user-facing memory controls:** Provide item-level edit and delete actions to support trust and data rights workflows.

- **Set explicit retention defaults:** Use TTL settings that match policy requirements. Document retention behavior in your product UX.

## Troubleshooting

| Issue | Cause | Resolution |
| --- | --- | --- |
| Requests fail with an authentication or authorization error. | Your identity or the project managed identity doesn’t have the required roles. | Verify the roles in [Authorization and permissions](#authorization-and-permissions). For REST calls, generate a fresh access token and retry. |
| Memories don’t appear after a conversation. | Memory updates are debounced or still processing. | Increase the wait time or call the update API with `update_delay` set to `0` to trigger processing immediately. |
| Memory search returns no results. | The `scope` value doesn’t match the scope used when memories were stored. | Use the same scope for update and search. If you map scope to users, use a stable user identifier. |
| The agent response doesn’t use stored memory. | The agent isn’t configured with the memory search tool, or the memory store name is incorrect. | Confirm the agent definition includes the `memory_search_preview` tool and references the correct memory store name. |
| Procedural memory or default TTL setting didn't take effect after an update. | In the latest preview, you can only set default options at memory store creation time. | Recreate the memory store with the desired defaults or check whether your API version supports post-create option updates. |
| An explicit remember-or-forget request didn't return memory command items in the response. | Memory tooling isn't configured correctly, or the input wasn't recognized as a remember-or-forget command. | Confirm the memory tool configuration and test with direct remember-or-forget phrasing. |

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

:::zone pivot="java"

- [Azure AI Agents client library for Java: Memory samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/ai/azure-ai-agents/src/samples/java/com/azure/ai/agents/memory)
- [Azure AI Agents client library for Java: Memory search agent sample](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/ai/azure-ai-agents/src/samples/java/com/azure/ai/agents/MemorySearchAgent.java)
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
