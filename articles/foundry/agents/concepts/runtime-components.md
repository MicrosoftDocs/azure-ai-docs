---
title: "Build with agents, conversations, and responses in Foundry Agent Service"
description: "Learn how to create agents, manage conversations, and generate responses in Microsoft Foundry Agent Service with code examples in Python, C#, JavaScript, Java, and REST API."
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: concept-article
ms.date: 03/11/2026
author: aahill
ms.author: aahi
ms.custom: pilot-ai-workflow-jan-2026, doc-kit-assisted
ai-usage: ai-assisted
---

# Build with agents, conversations, and responses

Microsoft Foundry Agent Service uses three core runtime components—**agents**, **conversations**, and **responses**—to power stateful, multi-turn interactions. An agent defines what model, instructions, and tools to use. A conversation persists history across turns. A response is the output the agent produces when it processes input.

This article walks through each component and shows how to use them together in code. You'll learn how to create an agent, start a conversation, generate responses (with or without an agent), add follow-up messages, and stream results—with examples in Python, C#, JavaScript, Java, and REST API.


## How runtime components work together

When you work with an agent, you follow a consistent pattern:

- **Create an agent**: Define an agent to start sending messages and receiving responses.
- **Create a conversation (optional)**: Use a conversation to maintain history across turns. If you don't use a conversation, carry forward context by using the output from a previous response.
- **Generate a response**: The agent processes input items in the conversation and any instructions provided in the request. The agent might append items to the conversation.
- **Check response status**: Monitor the response until it finishes (especially in streaming or background mode).
- **Retrieve the response**: Display the generated response to the user.

The following diagram illustrates how these components interact in a typical agent loop.

:::image type="content" source="../media/runtime-components.png" alt-text="Diagram that shows the agent runtime loop: an agent definition and optional conversation history feed response generation, which can call tools, append items back into the conversation, and produce output items you display to the user.":::

You provide user input (and optionally conversation history), the service generates a response (including tool calls when configured), and the resulting items can be reused as context for the next turn.


## Prerequisites

To run the samples in this article, you need:

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?icid=azurefreeaccount).
- A [Microsoft Foundry project](../../how-to/create-projects.md).
- The Foundry Agent Service SDK for your language:

# [Python](#tab/python)

```bash
pip install "azure-ai-projects>=2.0.0"
pip install azure-identity
```

# [C#](#tab/csharp)

```bash
dotnet add package Azure.AI.Projects --prerelease
dotnet add package Azure.AI.Projects.OpenAI --prerelease
dotnet add package Azure.Identity
```

# [JavaScript](#tab/javascript)

```bash
npm install @azure/ai-projects@2.0.0
npm install @azure/identity
```

# [Java](#tab/java)

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-agents</artifactId>
    <version>2.0.0-beta.2</version>
</dependency>
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-identity</artifactId>
    <version>1.15.4</version>
</dependency>
```

# [REST API](#tab/rest)

No SDK installation required. Use [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) to obtain an access token:

```bash
az login
```

---

## Create an agent

An agent is a persisted orchestration definition that combines AI models, instructions, code, tools, parameters, and optional safety or governance controls.

Store agents as named, versioned assets in Microsoft Foundry. During response generation, the agent definition works with interaction history (conversation or previous response) to process and respond to user input.

The following example creates a prompt agent with a name, model, and instructions. Use the project client for agent creation and versioning.

# [Python](#tab/python)

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

# Format: "https://resource_name.services.ai.azure.com/api/projects/project_name"
PROJECT_ENDPOINT = "your_project_endpoint"

# Create project client to call Foundry API
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

# Create a prompt agent
agent = project.agents.create_version(
    agent_name="my-agent",
    definition=PromptAgentDefinition(
        model="gpt-5-mini",
        instructions="You are a helpful assistant.",
    ),
)
print(f"Agent: {agent.name}, Version: {agent.version}")
```

# [C#](#tab/csharp)

```csharp
using Azure.Identity;
using Azure.AI.Projects;

// Format: "https://resource_name.services.ai.azure.com/api/projects/project_name"
var projectEndpoint = "your_project_endpoint";

// Create project client to call Foundry API
AIProjectClient projectClient = new(
    endpoint: new Uri(projectEndpoint),
    tokenProvider: new DefaultAzureCredential());

// Create a prompt agent
var agent = await projectClient.Agents
    .CreateAgentVersionAsync(
        agentName: "my-agent",
        options: new(
            new PromptAgentDefinition("gpt-5-mini")
            {
                Instructions = "You are a helpful assistant.",
            }));
Console.WriteLine($"Agent: {agent.Value.Name}, Version: {agent.Value.Version}");
```

# [JavaScript](#tab/javascript)

```javascript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";

// Format: "https://resource_name.services.ai.azure.com/api/projects/project_name"
const PROJECT_ENDPOINT = "your_project_endpoint";

// Create project client to call Foundry API
const project = new AIProjectClient(PROJECT_ENDPOINT, new DefaultAzureCredential());

// Create a prompt agent
const agent = await project.agents.createVersion(
  "my-agent",
  {
    kind: "prompt",
    model: "gpt-5-mini",
    instructions: "You are a helpful assistant.",
  },
);
console.log(`Agent: ${agent.name}, Version: ${agent.version}`);
```

# [Java](#tab/java)

```java
import com.azure.ai.agents.AgentsClientBuilder;
import com.azure.ai.agents.AgentsClient;
import com.azure.ai.agents.models.PromptAgentDefinition;
import com.azure.identity.DefaultAzureCredentialBuilder;

// Format: "https://resource_name.services.ai.azure.com/api/projects/project_name"
String projectEndpoint = "your_project_endpoint";

// Create agents client to call Foundry API
AgentsClient agentsClient = new AgentsClientBuilder()
    .credential(new DefaultAzureCredentialBuilder().build())
    .endpoint(projectEndpoint)
    .buildAgentsClient();

// Create a prompt agent
PromptAgentDefinition definition = new PromptAgentDefinition("gpt-5-mini");
definition.setInstructions("You are a helpful assistant.");

var agent = agentsClient.createAgentVersion("my-agent", definition);
System.out.println("Agent: " + agent.getName() + ", Version: " + agent.getVersion());
```

# [REST API](#tab/rest)

```bash
# Configuration
ENDPOINT="https://{resource_name}.services.ai.azure.com/api/projects/{project_name}"
ACCESS_TOKEN="$(az account get-access-token --resource https://ai.azure.com/ --query accessToken -o tsv)"

# Create a prompt agent
curl -X POST "${ENDPOINT}/agents?api-version=v1" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-agent",
    "definition": {
      "kind": "prompt",
      "model": "gpt-5-mini",
      "instructions": "You are a helpful assistant."
    }
  }'
```

---

For additional agent types (workflow, hosted), see [Agent development lifecycle](./development-lifecycle.md).

## Generate responses

Response generation invokes the agent. The agent uses its configuration and any provided history (conversation or previous response) to perform tasks by calling models and tools. As part of response generation, the agent appends items to the conversation.

You can also generate a response without defining an agent. In this case, you provide all configurations directly in the request and use them only for that response. This approach is useful for simple scenarios with minimal tools.

### Generate a response with an agent

The following example generates a response using an agent reference and a conversation. The agent processes the conversation history and produces output.

# [Python](#tab/python)

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Format: "https://resource_name.services.ai.azure.com/api/projects/project_name"
PROJECT_ENDPOINT = "your_project_endpoint"
AGENT_NAME = "your_agent_name"

# Create clients to call Foundry API
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()

# Create a conversation for multi-turn chat
conversation = openai.conversations.create()

# Generate a response using the agent
response = openai.responses.create(
    conversation=conversation.id,
    extra_body={
        "agent_reference": {
            "name": AGENT_NAME,
            "type": "agent_reference",
        }
    },
    input="What is the largest city in France?",
)
print(response.output_text)
```

# [C#](#tab/csharp)

```csharp
using Azure.Identity;
using Azure.AI.Projects;
using Azure.AI.Projects.OpenAI;

// Format: "https://resource_name.services.ai.azure.com/api/projects/project_name"
var projectEndpoint = "your_project_endpoint";
var agentName = "your_agent_name";

// Create project client to call Foundry API
AIProjectClient projectClient = new(
    endpoint: new Uri(projectEndpoint),
    tokenProvider: new DefaultAzureCredential());

// Create a conversation for multi-turn chat
ProjectConversation conversation
    = await projectClient.OpenAI.Conversations.CreateProjectConversationAsync();

// Generate a response using the agent
ResponsesClient responsesClient
    = projectClient.OpenAI.GetProjectResponsesClientForAgent(
        new AgentReference { Name = agentName },
        conversation.Id);
ResponseResult response = await responsesClient.CreateResponseAsync(
    "What is the largest city in France?");
Console.WriteLine(response.GetOutputText());
```

# [JavaScript](#tab/javascript)

```javascript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";

// Format: "https://resource_name.services.ai.azure.com/api/projects/project_name"
const PROJECT_ENDPOINT = "your_project_endpoint";
const AGENT_NAME = "your_agent_name";

// Create clients to call Foundry API
const project = new AIProjectClient(PROJECT_ENDPOINT, new DefaultAzureCredential());
const openai = await project.getOpenAIClient();

// Create a conversation for multi-turn chat
const conversation = await openai.conversations.create();

// Generate a response using the agent
const response = await openai.responses.create({
  conversation: conversation.id,
  input: "What is the largest city in France?",
  agent_reference: {
    name: AGENT_NAME,
    type: "agent_reference",
  },
});
console.log(response.output_text);
```

# [Java](#tab/java)

```java
import com.azure.ai.agents.*;
import com.azure.ai.agents.models.AgentReference;
import com.azure.identity.DefaultAzureCredentialBuilder;

// Format: "https://resource_name.services.ai.azure.com/api/projects/project_name"
String projectEndpoint = "your_project_endpoint";
String agentName = "your_agent_name";

// Create clients to call Foundry API
AgentsClientBuilder builder = new AgentsClientBuilder()
    .credential(new DefaultAzureCredentialBuilder().build())
    .endpoint(projectEndpoint);
ResponsesClient responsesClient = builder.buildResponsesClient();

// Generate a response using the agent
AgentReference agentRef = new AgentReference(agentName);

Response response = responsesClient.createWithAgent(
    agentRef,
    ResponseCreateParams.builder()
        .input("What is the largest city in France?"));
System.out.println(response.output());
```

# [REST API](#tab/rest)

```bash
# Configuration
ENDPOINT="https://{resource_name}.services.ai.azure.com/api/projects/{project_name}"
ACCESS_TOKEN="$(az account get-access-token --resource https://ai.azure.com/ --query accessToken -o tsv)"
AGENT_NAME="your_agent_name"
CONVERSATION_ID="conv_abc123"

# Generate a response using an agent
curl -X POST "${ENDPOINT}/openai/v1/responses" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "What is the largest city in France?",
    "conversation": "'"${CONVERSATION_ID}"'",
    "agent_reference": {
      "name": "'"${AGENT_NAME}"'",
      "type": "agent_reference"
    }
  }'
```

---

### Generate a response without an agent

For simple scenarios, you can generate a response directly with a model, without creating an agent first.

# [Python](#tab/python)

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Format: "https://resource_name.services.ai.azure.com/api/projects/project_name"
PROJECT_ENDPOINT = "your_project_endpoint"

# Create clients to call Foundry API
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()

# Generate a response directly with a model
response = openai.responses.create(
    model="gpt-5-mini",
    input="What is the largest city in France?",
)
print(response.output_text)
```

# [C#](#tab/csharp)

```csharp
using Azure.Identity;
using Azure.AI.Projects;
using Azure.AI.Projects.OpenAI;

// Format: "https://resource_name.services.ai.azure.com/api/projects/project_name"
var projectEndpoint = "your_project_endpoint";

// Create project client to call Foundry API
AIProjectClient projectClient = new(
    endpoint: new Uri(projectEndpoint),
    tokenProvider: new DefaultAzureCredential());

// Generate a response directly with a model
ProjectResponsesClient responsesClient
    = projectClient.OpenAI.GetProjectResponsesClientForModel("gpt-5-mini");
ResponseResult response = await responsesClient.CreateResponseAsync(
    "What is the largest city in France?");
Console.WriteLine(response.GetOutputText());
```

# [JavaScript](#tab/javascript)

```javascript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";

// Format: "https://resource_name.services.ai.azure.com/api/projects/project_name"
const PROJECT_ENDPOINT = "your_project_endpoint";

// Create clients to call Foundry API
const project = new AIProjectClient(PROJECT_ENDPOINT, new DefaultAzureCredential());
const openai = await project.getOpenAIClient();

// Generate a response directly with a model
const response = await openai.responses.create({
  model: "gpt-5-mini",
  input: "What is the largest city in France?",
});
console.log(response.output_text);
```

# [Java](#tab/java)

```java
import com.azure.ai.agents.AgentsClientBuilder;
import com.azure.ai.agents.ResponsesClient;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.models.responses.ResponseCreateParams;

// Format: "https://resource_name.services.ai.azure.com/api/projects/project_name"
String projectEndpoint = "your_project_endpoint";

// Create responses client to call Foundry API
ResponsesClient responsesClient = new AgentsClientBuilder()
    .credential(new DefaultAzureCredentialBuilder().build())
    .endpoint(projectEndpoint)
    .buildResponsesClient();

// Generate a response directly with a model
ResponseCreateParams request = new ResponseCreateParams.Builder()
    .model("gpt-5-mini")
    .input("What is the largest city in France?")
    .build();
var response = responsesClient.getResponseService().create(request);
System.out.println(response.output());
```

# [REST API](#tab/rest)

```bash
# Configuration
ENDPOINT="https://{resource_name}.services.ai.azure.com/api/projects/{project_name}"
ACCESS_TOKEN="$(az account get-access-token --resource https://ai.azure.com/ --query accessToken -o tsv)"

# Generate a response directly with a model
curl -X POST "${ENDPOINT}/openai/v1/responses" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-5-mini",
    "input": "What is the largest city in France?"
  }'
```

---

## Conversations and conversation items

A conversation manages state automatically, so you don't need to pass inputs manually for each turn.

Conversations are durable objects with unique identifiers. After creation, you can reuse them across sessions.

Conversations store items, which can include messages, tool calls, tool outputs, and other data.

### Create a conversation

The following example creates a conversation with an initial user message. Use the OpenAI client (obtained from the project client) for conversations and responses.

# [Python](#tab/python)

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Format: "https://resource_name.services.ai.azure.com/api/projects/project_name"
PROJECT_ENDPOINT = "your_project_endpoint"

# Create clients to call Foundry API
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()

# Create a conversation with an initial user message
conversation = openai.conversations.create(
    items=[
        {
            "type": "message",
            "role": "user",
            "content": "What is the largest city in France?",
        }
    ],
)
print(f"Conversation ID: {conversation.id}")
```

# [C#](#tab/csharp)

```csharp
using Azure.Identity;
using Azure.AI.Projects;
using Azure.AI.Projects.OpenAI;

// Format: "https://resource_name.services.ai.azure.com/api/projects/project_name"
var projectEndpoint = "your_project_endpoint";

// Create project client to call Foundry API
AIProjectClient projectClient = new(
    endpoint: new Uri(projectEndpoint),
    tokenProvider: new DefaultAzureCredential());

// Create a conversation
ProjectConversation conversation
    = await projectClient.OpenAI.Conversations.CreateProjectConversationAsync();
Console.WriteLine($"Conversation ID: {conversation.Id}");
```

# [JavaScript](#tab/javascript)

```javascript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";

// Format: "https://resource_name.services.ai.azure.com/api/projects/project_name"
const PROJECT_ENDPOINT = "your_project_endpoint";

// Create clients to call Foundry API
const project = new AIProjectClient(PROJECT_ENDPOINT, new DefaultAzureCredential());
const openai = await project.getOpenAIClient();

// Create a conversation with an initial user message
const conversation = await openai.conversations.create({
  items: [
    {
      type: "message",
      role: "user",
      content: "What is the largest city in France?",
    },
  ],
});
console.log(`Conversation ID: ${conversation.id}`);
```

# [Java](#tab/java)

```java
import com.azure.ai.agents.AgentsClientBuilder;
import com.azure.ai.agents.ConversationsClient;
import com.azure.identity.DefaultAzureCredentialBuilder;

// Format: "https://resource_name.services.ai.azure.com/api/projects/project_name"
String projectEndpoint = "your_project_endpoint";

// Create conversations client to call Foundry API
ConversationsClient conversationsClient = new AgentsClientBuilder()
    .credential(new DefaultAzureCredentialBuilder().build())
    .endpoint(projectEndpoint)
    .buildConversationsClient();

// Create a conversation
var conversation = conversationsClient.getConversationService().create();
System.out.println("Conversation ID: " + conversation.id());
```

# [REST API](#tab/rest)

```bash
# Configuration
ENDPOINT="https://{resource_name}.services.ai.azure.com/api/projects/{project_name}"
ACCESS_TOKEN="$(az account get-access-token --resource https://ai.azure.com/ --query accessToken -o tsv)"

# Create a conversation with an initial user message
curl -X POST "${ENDPOINT}/openai/v1/conversations" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "type": "message",
        "role": "user",
        "content": "What is the largest city in France?"
      }
    ]
  }'
```

---

### When to use a conversation

Use a conversation when you want:

- **Multi-turn continuity**: Keep a stable history across turns without rebuilding context yourself.
- **Cross-session continuity**: Reuse the same conversation for a user who returns later.
- **Easier debugging**: Inspect what happened over time (for example, tool calls and outputs).

If you don't create a conversation, you can still build multi-turn flows by using the output from a previous response as the starting point for the next request. This approach gives you more flexibility than the older thread-based pattern, where state was tightly coupled to thread objects. For migration guidance, see [Migrate to the Agents SDK](../how-to/migrate.md).

### Conversation item types

Conversations store **items** rather than only chat messages. Items capture what happened during response generation so the next turn can reuse that context.

Common item types include:

- **Message items**: User or assistant messages.
- **Tool call items**: Records of tool invocations the agent attempted.
- **Tool output items**: Outputs returned by tools (for example, retrieval results).
- **Output items**: The response content you display back to the user.

### Add items to a conversation

After you create a conversation, use `conversations.items.create()` to add subsequent user messages or other items.

# [Python](#tab/python)

```python
# Add a follow-up message to an existing conversation
openai.conversations.items.create(
    conversation_id=conversation.id,
    items=[
        {
            "type": "message",
            "role": "user",
            "content": "What about Germany?",
        }
    ],
)
```

# [C#](#tab/csharp)

```csharp
// In C#, send follow-up input directly
// through the responses client
var followUp = await responsesClient.CreateResponseAsync(
    "What about Germany?");
Console.WriteLine(followUp.GetOutputText());
```

# [JavaScript](#tab/javascript)

```javascript
// Add a follow-up message to an existing conversation
await openai.conversations.items.create(
  conversation.id,
  {
    items: [
      {
        type: "message",
        role: "user",
        content: "What about Germany?",
      },
    ],
  },
);
```

# [Java](#tab/java)

```java
// In Java, send follow-up input directly
// through the responses client
AgentReference agentRef = new AgentReference("my-agent");

Response followUp = responsesClient.createWithAgent(
    agentRef,
    ResponseCreateParams.builder()
        .input("What about Germany?"));
System.out.println(followUp.output());
```

# [REST API](#tab/rest)

```bash
# Add items to an existing conversation
CONVERSATION_ID="conv_abc123"

curl -X POST "${ENDPOINT}/openai/v1/conversations/${CONVERSATION_ID}/items" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "type": "message",
        "role": "user",
        "content": "What about Germany?"
      }
    ]
  }'
```

---

For examples that show how conversations and responses work together in code, see [Create and use memory in Foundry Agent Service](../how-to/memory-usage.md).

## Streaming and background responses

Some response generation modes return results incrementally (streaming) or complete asynchronously (background). In these cases, you typically monitor the response until it finishes and then consume the final output items.

### Stream a response

Streaming returns partial results as they're generated. This approach is useful for showing output to users in real time.

# [Python](#tab/python)

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Format: "https://resource_name.services.ai.azure.com/api/projects/project_name"
PROJECT_ENDPOINT = "your_project_endpoint"

# Create clients to call Foundry API
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()

# Stream a response
stream = openai.responses.create(
    model="gpt-5-mini",
    input="Explain how agents work in one paragraph.",
    stream=True,
)
for event in stream:
    if hasattr(event, "delta") and event.delta:
        print(event.delta, end="", flush=True)
```

# [C#](#tab/csharp)

```csharp
using Azure.Identity;
using Azure.AI.Projects;
using Azure.AI.Projects.OpenAI;

// Format: "https://resource_name.services.ai.azure.com/api/projects/project_name"
var projectEndpoint = "your_project_endpoint";

// Create project client to call Foundry API
AIProjectClient projectClient = new(
    endpoint: new Uri(projectEndpoint),
    tokenProvider: new DefaultAzureCredential());

// Stream a response
ProjectResponsesClient responsesClient
    = projectClient.OpenAI.GetProjectResponsesClientForModel("gpt-5-mini");
await foreach (var update in responsesClient.CreateResponseStreamingAsync(
    "Explain how agents work in one paragraph."))
{
    Console.Write(update.Text);
}
```

# [JavaScript](#tab/javascript)

```javascript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";

// Format: "https://resource_name.services.ai.azure.com/api/projects/project_name"
const PROJECT_ENDPOINT = "your_project_endpoint";

// Create clients to call Foundry API
const project = new AIProjectClient(PROJECT_ENDPOINT, new DefaultAzureCredential());
const openai = await project.getOpenAIClient();

// Stream a response
const stream = await openai.responses.create({
  model: "gpt-5-mini",
  input: "Explain how agents work in one paragraph.",
  stream: true,
});
for await (const event of stream) {
  if (event.type === "response.output_text.delta") {
    process.stdout.write(event.delta);
  }
}
```

# [Java](#tab/java)

> [!NOTE]
> Streaming isn't yet supported in the Java SDK. Check the [azure-ai-agents release notes](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/ai/azure-ai-agents/CHANGELOG.md) for updates.

```java
// Streaming is not yet supported in the Java SDK.
// Use a synchronous response call instead.
import com.azure.ai.agents.AgentsClientBuilder;
import com.azure.ai.agents.ResponsesClient;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.models.responses.ResponseCreateParams;

String projectEndpoint = "your_project_endpoint";

ResponsesClient responsesClient = new AgentsClientBuilder()
    .credential(new DefaultAzureCredentialBuilder().build())
    .endpoint(projectEndpoint)
    .buildResponsesClient();

ResponseCreateParams request = new ResponseCreateParams.Builder()
    .model("gpt-5-mini")
    .input("Explain how agents work in one paragraph.")
    .build();
var response = responsesClient.getResponseService().create(request);
System.out.println(response.output());
```

# [REST API](#tab/rest)

```bash
# Configuration
ENDPOINT="https://{resource_name}.services.ai.azure.com/api/projects/{project_name}"
ACCESS_TOKEN="$(az account get-access-token --resource https://ai.azure.com/ --query accessToken -o tsv)"

# Stream a response (returns server-sent events)
curl -N -X POST "${ENDPOINT}/openai/v1/responses" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-5-mini",
    "input": "Explain how agents work in one paragraph.",
    "stream": true
  }'
```

---

For details about response modes and how to consume outputs, see [Responses API](../../openai/how-to/responses.md).

## Add tools to an agent

Tools extend what an agent can do beyond generating text. When you attach tools to an agent, the agent can call external services, run code, search files, and access data sources during response generation—using tools such as code interpreter or function calling.

You can attach one or more tools when you create an agent. During response generation, the agent decides whether to call a tool based on the user input and its instructions. The following example creates an agent with a code interpreter tool attached.

# [Python](#tab/python)

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, CodeInterpreterTool

PROJECT_ENDPOINT = "your_project_endpoint"

project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

# Create an agent with a code interpreter tool
agent = project.agents.create_version(
    agent_name="my-tool-agent",
    definition=PromptAgentDefinition(
        model="gpt-5-mini",
        instructions="You are a helpful assistant that can run code.",
        tools=[CodeInterpreterTool()],
    ),
)
print(f"Agent: {agent.name}, Version: {agent.version}")
```

# [C#](#tab/csharp)

```csharp
using Azure.Identity;
using Azure.AI.Projects;

var projectEndpoint = "your_project_endpoint";

AIProjectClient projectClient = new(
    endpoint: new Uri(projectEndpoint),
    tokenProvider: new DefaultAzureCredential());

// Create an agent with a code interpreter tool
var agent = await projectClient.Agents
    .CreateAgentVersionAsync(
        agentName: "my-tool-agent",
        options: new(
            new PromptAgentDefinition("gpt-5-mini")
            {
                Instructions = "You are a helpful assistant that can run code.",
                Tools = { new CodeInterpreterToolDefinition() },
            }));
Console.WriteLine($"Agent: {agent.Value.Name}, Version: {agent.Value.Version}");
```

# [JavaScript](#tab/javascript)

```javascript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";

const PROJECT_ENDPOINT = "your_project_endpoint";
const project = new AIProjectClient(PROJECT_ENDPOINT, new DefaultAzureCredential());

// Create an agent with a code interpreter tool
const agent = await project.agents.createVersion(
  "my-tool-agent",
  {
    kind: "prompt",
    model: "gpt-5-mini",
    instructions: "You are a helpful assistant that can run code.",
    tools: [{ type: "code_interpreter" }],
  },
);
console.log(`Agent: ${agent.name}, Version: ${agent.version}`);
```

# [Java](#tab/java)

```java
import com.azure.ai.agents.AgentsClientBuilder;
import com.azure.ai.agents.AgentsClient;
import com.azure.ai.agents.models.PromptAgentDefinition;
import com.azure.ai.agents.models.CodeInterpreterTool;
import com.azure.identity.DefaultAzureCredentialBuilder;

String projectEndpoint = "your_project_endpoint";

AgentsClient agentsClient = new AgentsClientBuilder()
    .credential(new DefaultAzureCredentialBuilder().build())
    .endpoint(projectEndpoint)
    .buildAgentsClient();

// Create an agent with a code interpreter tool
PromptAgentDefinition definition = new PromptAgentDefinition("gpt-5-mini");
definition.setInstructions("You are a helpful assistant that can run code.");
definition.setTools(Arrays.asList(new CodeInterpreterTool()));

var agent = agentsClient.createAgentVersion("my-tool-agent", definition);
System.out.println("Agent: " + agent.getName() + ", Version: " + agent.getVersion());
```

# [REST API](#tab/rest)

```bash
ENDPOINT="https://{resource_name}.services.ai.azure.com/api/projects/{project_name}"
ACCESS_TOKEN="$(az account get-access-token --resource https://ai.azure.com/ --query accessToken -o tsv)"

# Create an agent with a code interpreter tool
curl -X POST "${ENDPOINT}/agents?api-version=v1" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-tool-agent",
    "definition": {
      "kind": "prompt",
      "model": "gpt-5-mini",
      "instructions": "You are a helpful assistant that can run code.",
      "tools": [{ "type": "code_interpreter" }]
    }
  }'
```

---

For the full list of available tools, see the [tools overview](./tool-catalog.md). For best practices, see [Best practices for using tools](./tool-best-practice.md).

## Attach memory to an agent

Memory gives agents the ability to retain information across sessions, so they can personalize responses and recall user preferences over time. Without memory, each conversation starts from scratch.

Foundry Agent Service provides a managed memory solution (preview) that you configure through **memory stores**. A memory store defines which types of information the agent should retain. Attach a memory store to your agent, and the agent uses stored memories as additional context during response generation.

The following example creates a memory store and attaches it to an agent.

# [Python](#tab/python)

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    MemoryStoreDefaultDefinition,
    MemoryStoreDefaultOptions,
)

PROJECT_ENDPOINT = "your_project_endpoint"

project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

# Create a memory store
options = MemoryStoreDefaultOptions(
    chat_summary_enabled=True,
    user_profile_enabled=True,
)
definition = MemoryStoreDefaultDefinition(
    chat_model="gpt-5.2",
    embedding_model="text-embedding-3-small",
    options=options,
)
memory_store = project.beta.memory_stores.create(
    name="my_memory_store",
    definition=definition,
    description="Memory store for my agent",
)
print(f"Memory store: {memory_store.name}")
```

# [C#](#tab/csharp)

```csharp
using Azure.Identity;
using Azure.AI.Projects;

#pragma warning disable AAIP001

var projectEndpoint = "your_project_endpoint";

AIProjectClient projectClient = new(
    new Uri(projectEndpoint),
    new DefaultAzureCredential());

// Create a memory store
MemoryStoreDefaultDefinition memoryStoreDefinition = new(
    chatModel: "gpt-5.2",
    embeddingModel: "text-embedding-3-small");
memoryStoreDefinition.Options = new(
    userProfileEnabled: true,
    chatSummaryEnabled: true);

MemoryStore memoryStore = await projectClient.MemoryStores
    .CreateMemoryStoreAsync(
        name: "my_memory_store",
        definition: memoryStoreDefinition,
        description: "Memory store for my agent");
Console.WriteLine($"Memory store: {memoryStore.Name}");
```

# [JavaScript](#tab/javascript)

```javascript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";

const PROJECT_ENDPOINT = "your_project_endpoint";
const project = new AIProjectClient(PROJECT_ENDPOINT, new DefaultAzureCredential());

// Create a memory store
const memoryStore = await project.beta.memoryStores.create(
  "my_memory_store",
  {
    kind: "default",
    chat_model: "gpt-5.2",
    embedding_model: "text-embedding-3-small",
    options: {
      user_profile_enabled: true,
      chat_summary_enabled: true,
    },
  },
  { description: "Memory store for my agent" },
);
console.log(`Memory store: ${memoryStore.name}`);
```

# [Java](#tab/java)

```java
import com.azure.ai.agents.AgentsClientBuilder;
import com.azure.ai.agents.MemoryStoresClient;
import com.azure.ai.agents.models.MemoryStoreDefaultDefinition;
import com.azure.ai.agents.models.MemoryStoreDetails;
import com.azure.identity.DefaultAzureCredentialBuilder;

String projectEndpoint = "your_project_endpoint";

// Create memory stores client
MemoryStoresClient memoryStoresClient = new AgentsClientBuilder()
    .credential(new DefaultAzureCredentialBuilder().build())
    .endpoint(projectEndpoint)
    .buildMemoryStoresClient();

// Create a memory store
MemoryStoreDefaultDefinition definition =
    new MemoryStoreDefaultDefinition("gpt-5.2", "text-embedding-3-small");
MemoryStoreDetails memoryStore = memoryStoresClient
    .createMemoryStore("my_memory_store", definition,
        "Memory store for my agent", null);
System.out.println("Memory store: " + memoryStore.getName());
```

# [REST API](#tab/rest)

```bash
ENDPOINT="https://{resource_name}.services.ai.azure.com/api/projects/{project_name}"
API_VERSION="2025-11-15-preview"
ACCESS_TOKEN="$(az account get-access-token --resource https://ai.azure.com/ --query accessToken -o tsv)"

# Create a memory store
curl -X POST "${ENDPOINT}/memory_stores?api-version=${API_VERSION}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my_memory_store",
    "description": "Memory store for my agent",
    "definition": {
      "kind": "default",
      "chat_model": "gpt-5.2",
      "embedding_model": "text-embedding-3-small",
      "options": {
        "chat_summary_enabled": true,
        "user_profile_enabled": true
      }
    }
  }'
```

---

For conceptual details, see [Memory in Foundry Agent Service](./what-is-memory.md). For full implementation guidance, see [Create and use memory](../how-to/memory-usage.md).

## Security and data handling

Because conversations and responses can persist user-provided content and tool outputs, treat runtime data like application data:

- **Avoid storing secrets in prompts or conversation history**. Use connections and managed secret stores instead (for example, [Set up a Key Vault connection](../../how-to/set-up-key-vault-connection.md)).
- **Use least privilege for tool access**. When a tool accesses external systems, the agent can potentially read or send data through that tool.
- **Be careful with non-Microsoft services**. If your agent calls tools backed by non-Microsoft services, some data might flow to those services. For related considerations, see [Discover tools in the Foundry Tools](./tool-catalog.md).

## Limits and constraints

Limits can depend on the model, region, and the tools you attach (for example, streaming availability and tool support). For current availability and constraints for responses, see [Responses API](../../openai/how-to/responses.md).

## Related content

- [Agent development lifecycle](./development-lifecycle.md)
- [Discover tools in the Foundry Tools](./tool-catalog.md)
- [Best practices for using tools in Microsoft Foundry Agent Service](./tool-best-practice.md)
- [Publish and share agents in Microsoft Foundry](../how-to/publish-agent.md)
- [Agent tracing overview](../../observability/concepts/trace-agent-concept.md)
- [Migrate to the new agents developer experience](../how-to/migrate.md)
- [Create and use memory in Foundry Agent Service](../how-to/memory-usage.md)
