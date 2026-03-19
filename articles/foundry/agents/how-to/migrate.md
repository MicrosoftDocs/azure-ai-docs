---
title: "Migrate to the new Foundry Agent Service"
description: "Learn how to migrate from the Assistants API and classic agents to the new Foundry Agent Service, including threads to conversations, runs to responses, and updated SDK patterns."
author: aahill
ms.author: aahi
manager: nitinme
ms.date: 03/18/2026
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
#Customer Intent: As a developer, I want to migrate my existing agents or assistants to the new Foundry Agent Service so that I can use the latest API and features.
---

# Migrate to the new agents developer experience
> [!TIP]
> A [migration tool](https://aka.ms/agent/migrate/tool) is available to help automate migration from the Assistants API to Agents.

Foundry Agent Service provides an upgraded developer experience for building intelligent agents that are easy to build, version, operate, and observe. The new agents API introduces a modernized SDK, new enterprise-grade capabilities, and preserves the identity, governance, and observability features you rely on today.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?icid=azurefreeaccount).
- A [Microsoft Foundry project](../../how-to/create-projects.md).
- The Foundry Agent Service SDK for your language, and corresponding identity package for authentication. Install the packages for your language and sign in with `az login` or use `DefaultAzureCredential`:

# [Python](#tab/python)

```bash
pip install "azure-ai-projects>=2.0.0"
```

# [C#](#tab/csharp)

```bash
dotnet add package Azure.AI.Projects --prerelease
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

---

- Existing agents or assistants code that you want to migrate.

The following code initializes the clients used throughout this guide:

# [Python](#tab/python)

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Format: "https://resource_name.services.ai.azure.com/api/projects/project_name"
PROJECT_ENDPOINT = "your_project_endpoint"

project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()
```

# [C#](#tab/csharp)

```csharp
using Azure.AI.Projects;
using Azure.AI.Extensions.OpenAI;
using Azure.Identity;

AIProjectClient projectClient = new(
    new Uri(Environment.GetEnvironmentVariable(
        "PROJECT_ENDPOINT")!),
    new DefaultAzureCredential());
```

# [JavaScript](#tab/javascript)

```javascript
import { AIProjectClient } from "@azure/ai-projects";
import { DefaultAzureCredential }
    from "@azure/identity";

const projectClient = new AIProjectClient(
    process.env["PROJECT_ENDPOINT"],
    new DefaultAzureCredential()
);
const openAIClient = await projectClient
    .getOpenAIClient();
```

# [Java](#tab/java)

```java
import com.azure.ai.agents.AgentsClient;
import com.azure.ai.agents.AgentsClientBuilder;
import com.azure.identity.DefaultAzureCredentialBuilder;

AgentsClient agentsClient =
    new AgentsClientBuilder()
        .credential(
            new DefaultAzureCredentialBuilder()
                .build())
        .endpoint(System.getenv(
            "PROJECT_ENDPOINT"))
        .buildAgentsClient();
```

---

Use `project` for agent creation and versioning. Use `openai` (or the equivalent in your language) for conversations and responses.

### Key benefits

The new agents provide the following benefits:

**Developer productivity**

- ⭐ **More models.** Generate responses by using any Foundry model either in your agent or directly as a response generation call.
- **More features.** Web Search, File Search, Code Interpreter, MCP tool calling, image generation, and reasoning summaries.
- **Modern API primitive.** Built on the Responses API instead of the older Assistants API.
- **Background mode**. Support for long-running tools (like image-generation), and durable streams (supports disconnect/reconnect scenarios)
- **Future-proof.** New features and model support are only added to the new agents.
- **New agent types.** Create prompt-based, workflow-based agents, workflow-based agents (preview), and hosted agents (preview).

**Enterprise readiness**

- ⭐ **Single-tenant storage.** Use single-tenant storage, with the option to bring your own Azure Cosmos DB to store state and keep your data secure.
- **Enhanced security.** Control who can run or modify agent definitions.
- **Separation of duties.** Define agents once and execute them with various inputs.
- **Deployable agents.** Agents can be exposed as individual endpoints.

**API modernization**

- **Improved state management.** Uses conversations instead of threads and messages.
- **Stateful context.** Automatically retains context across calls.
- **Superset of Responses API.** Builds on the Responses API and adds more capabilities.
- **Single or multi-agent workflows.** Easily chain agents for complex workflows.

## Key changes

The following table summarizes the main API changes between the previous and current agent experience.

| Before | After | Details |
| -------- | ------- | ------ |
| Threads | Conversations | Supports streams of items, not just messages. |
| Runs | Responses | Responses send input items or use a conversation object and receive output items. Tool call loops are explicitly managed. |
| Assistants / agents | Agents (new) | Support for enterprise-ready prompt, workflow, and hosted agents with stateful context by default for any Foundry model. |

## Agent tool availability

The following table compares agent tools available in classic agents and the new Foundry Agent Service. Use it to identify which tools carry over directly, which have changed, and which are exclusive to the new experience.

| Tool | Foundry (classic) | Foundry (new) |
| --- | --- | --- |
| Agent to Agent (A2A) | No | Yes (Public Preview) |
| Azure AI Search | Yes (GA) | Yes (GA) |
| Azure Functions | Yes (GA) | No |
| Browser Automation | Yes (Public Preview) | Yes (Public Preview) |
| Code Interpreter | Yes (GA) | Yes (GA) |
| Computer Use | Yes (Public Preview) | Yes (Public Preview) |
| Connected Agents | Yes (Public Preview) | No (Recommendation: Workflow and A2A tool) |
| Deep Research | Yes (Public Preview) | No (Recommendation: Deep Research model with Web Search tool) |
| Fabric Data Agent | Yes (Public Preview) | Yes (Public Preview) |
| File Search | Yes (GA) | Yes (GA) |
| Function | Yes (GA) | Yes (GA) |
| Grounding with Bing Search | Yes (GA) | Yes (GA) |
| Grounding with Bing Custom Search | Yes (Public Preview) | Yes (Public Preview) |
| Image Generation | No | Yes (Public Preview) |
| MCP | Yes (Public Preview) | Yes (GA) |
| OpenAPI | Yes (GA) | Yes (GA) |
| SharePoint Grounding | Yes (Public Preview) | Yes (Public Preview) |
| Web Search | No | Yes (Public Preview) |

> [!IMPORTANT]
> In the new API, the conversations and responses APIs use the **OpenAI client** (or its language equivalent). In Python, call `project.get_openai_client()`. In C#, use `projectClient.OpenAI.GetProjectResponsesClientForAgent()`. In JavaScript, call `projectClient.getOpenAIClient()`. In Java, use `AgentsClientBuilder` to build a `ResponsesClient`. Agent creation and versioning remain on the **project client**. The examples in each section show which client to use.

## Migrate threads to conversations

Threads stored messages on the server side. A conversation can store items, including messages, tool calls, tool outputs, and other data.

### Requests

The following examples compare thread creation (previous) with conversation creation (current). The current approach uses the OpenAI client obtained from `project.get_openai_client()`.

**Previous - threads**

# [Python](#tab/python)

```python
thread = client.agents.threads.create( 
     messages=[{"role": "user", "content": "Tell me a one line funny story about unicorns"}], 
     metadata={"agent": "my-awesome-agent"}, 
) 
```

# [C#](#tab/csharp)

```csharp
AgentThread thread =
    await agentsClient.CreateThreadAsync(
        messages: new[]
        {
            new ThreadMessageOptions(
                MessageRole.User,
                "Tell me a one line funny "
                + "story about unicorns")
        },
        metadata:
            new Dictionary<string, string>
        {
            ["agent"] = "my-awesome-agent"
        });
```

# [JavaScript](#tab/javascript)

```javascript
const thread =
    await client.agents.createThread({
        messages: [
            {
                role: "user",
                content:
                    "Tell me a one line funny "
                    + "story about unicorns",
            },
        ],
        metadata: {
            agent: "my-awesome-agent",
        },
    });
```

# [Java](#tab/java)

```java
AgentThread thread =
    agentsClient.createThread(
        new CreateThreadOptions()
            .setMessages(Arrays.asList(
                new ThreadMessageOptions(
                    MessageRole.USER,
                    "Tell me a one line "
                    + "funny story about "
                    + "unicorns")))
            .setMetadata(Map.of(
                "agent",
                "my-awesome-agent")));
```

---

**Current - conversations**

# [Python](#tab/python)

```python
conversation = openai.conversations.create(
    items=[
        {
            "type": "message",
            "role": "user",
            "content": "Tell me a one line funny "
                       "story about unicorns",
        }
    ],
    metadata={"agent": "my-awesome-agent"},
)
```

# [C#](#tab/csharp)

```csharp
ProjectResponsesClient responsesClient =
    projectClient.OpenAI
        .GetProjectResponsesClientForAgent(
            "my-awesome-agent");

var result = responsesClient.CreateResponse(
    "Tell me a one line funny story "
    + "about unicorns");
```

# [JavaScript](#tab/javascript)

```javascript
const conversation =
    await openAIClient.conversations.create({
        items: [
            {
                type: "message",
                role: "user",
                content:
                    "Tell me a one line funny "
                    + "story about unicorns",
            },
        ],
        metadata: { agent: "my-awesome-agent" },
    });
```

# [Java](#tab/java)

```java
ResponsesClient responsesClient =
    new AgentsClientBuilder()
        .credential(
            new DefaultAzureCredentialBuilder()
                .build())
        .endpoint(System.getenv(
            "PROJECT_ENDPOINT"))
        .buildResponsesClient();

AgentReference agentRef = new AgentReference("my-agent");

Response result = responsesClient.createWithAgent(
    agentRef,
    ResponseCreateParams.builder()
        .input("Tell me a one line funny story about unicorns"));
```

---

### Responses

The JSON responses show the structural differences between thread objects and conversation objects.

**Previous - threads**

```json
{ 
  "id": "thread_1234abcd",  
  "object": "thread",  
  "created_at": 1762217858,  
  "metadata": {"agent": "my-awesome-agent"},  
  "tool_resources": {} 
} 
```

**Current - conversations**

```json
{ 
  "id":"conv_1234abcd", 
  "created_at":1762217961, 
  "metadata":{"agent":"my-awesome-agent"}, 
  "object":"conversation" 
} 
```

### Add items to an existing conversation

After you create a conversation, use `conversations.items.create()` to add subsequent messages. This pattern replaces adding messages to threads with `client.agents.messages.create()`.

**Previous - add a message to a thread**

# [Python](#tab/python)

```python
message = client.agents.messages.create(
    thread_id=thread.id,
    role="user",
    content="Follow-up question about the same topic",
)
```

# [C#](#tab/csharp)

```csharp
ThreadMessage message =
    await agentsClient.CreateMessageAsync(
        thread.Id,
        MessageRole.User,
        "Follow-up question about "
        + "the same topic");
```

# [JavaScript](#tab/javascript)

```javascript
const message =
    await client.agents.createMessage(
        thread.id,
        {
            role: "user",
            content:
                "Follow-up question about "
                + "the same topic",
        }
    );
```

# [Java](#tab/java)

```java
ThreadMessage message =
    agentsClient.createMessage(
        thread.getId(),
        new CreateMessageOptions(
            MessageRole.USER,
            "Follow-up question about "
            + "the same topic"));
```

---

**Current - add items to a conversation**

# [Python](#tab/python)

```python
openai.conversations.items.create(
    conversation_id=conversation.id,
    items=[
        {
            "type": "message",
            "role": "user",
            "content": "Follow-up question "
                       "about the same topic",
        }
    ],
)
```

# [C#](#tab/csharp)

```csharp
// In C#, send follow-up input directly
// through the responses client.
var followUp = responsesClient.CreateResponse(
    "Follow-up question about the same topic");
```

# [JavaScript](#tab/javascript)

```javascript
await openAIClient.conversations.items.create(
    conversation.id,
    {
        items: [
            {
                type: "message",
                role: "user",
                content:
                    "Follow-up question "
                    + "about the same topic",
            },
        ],
    }
);
```

# [Java](#tab/java)

```java
// In Java, send follow-up input directly
AgentReference agentRef = new AgentReference("my-agent");

Response result = responsesClient.createWithAgent(
    agentRef,
    ResponseCreateParams.builder()
        .input("Follow-up question "
        + "about the same topic"));
```

---

## Migrate runs to responses

Runs were asynchronous processes that executed against threads. Responses are simpler: provide a set of input items to execute and get a list of output items back. Responses can be used alone, or with conversation objects for storing context. The responses API uses the OpenAI client.

### Requests

The following examples compare how you invoke agent logic. The previous approach used asynchronous runs with polling. The current approach calls `responses.create()` on the OpenAI client.

**Previous - runs**

# [Python](#tab/python)

```python
thread_id = "thread_abcd1234" 
assistant_id = "asst_efgh5678" 
run = project_client.agents.runs.create( 
  thread_id=thread_id,  
  agent_id=assistant_id, 
  additional_instructions="Please address the user as Jane Doe. The user has a premium account" 
) 
while run.status in ("queued", "in_progress"): 
  time.sleep(1) 
  run = project_client.agents.runs.get(thread_id=thread_id, run_id=run.id) 
```

# [C#](#tab/csharp)

```csharp
string threadId = "thread_abcd1234";
string assistantId = "asst_efgh5678";

ThreadRun run =
    await agentsClient.CreateRunAsync(
        threadId,
        assistantId,
        additionalInstructions:
            "Please address the user as "
            + "Jane Doe. The user has a "
            + "premium account");

while (run.Status == RunStatus.Queued
    || run.Status ==
        RunStatus.InProgress)
{
    await Task.Delay(1000);
    run = await agentsClient.GetRunAsync(
        threadId, run.Id);
}
```

# [JavaScript](#tab/javascript)

```javascript
const threadId = "thread_abcd1234";
const assistantId = "asst_efgh5678";

let run = await client.agents.createRun(
    threadId,
    assistantId,
    {
        additionalInstructions:
            "Please address the user as "
            + "Jane Doe. The user has a "
            + "premium account",
    });

while (run.status === "queued"
    || run.status === "in_progress") {
    await new Promise(
        (r) => setTimeout(r, 1000));
    run = await client.agents.getRun(
        threadId, run.id);
}
```

# [Java](#tab/java)

```java
String threadId = "thread_abcd1234";
String assistantId = "asst_efgh5678";

ThreadRun run =
    agentsClient.createRun(
        threadId,
        assistantId,
        new CreateRunOptions()
            .setAdditionalInstructions(
                "Please address the user "
                + "as Jane Doe. The user "
                + "has a premium account"));

while (RunStatus.QUEUED
        .equals(run.getStatus())
    || RunStatus.IN_PROGRESS
        .equals(run.getStatus())) {
    Thread.sleep(1000);
    run = agentsClient.getRun(
        threadId, run.getId());
}
```

---

**Current - responses**

# [Python](#tab/python)

```python
conversation_id = "conv_11112222AAAABBBB"

response = openai.responses.create(
    input="Hi, Agent! Draw a graph for a line "
          "with a slope of 4 and "
          "y-intercept of 9.",
    conversation=conversation_id,
    extra_body={
        "agent_reference": {
            "name": "my-agent",
            "type": "agent_reference",
        }
    },
)
```

# [C#](#tab/csharp)

```csharp
ProjectResponsesClient responsesClient =
    projectClient.OpenAI
        .GetProjectResponsesClientForAgent(
            "my-agent");

var result = responsesClient.CreateResponse(
    "Hi, Agent! Draw a graph for a line "
    + "with a slope of 4 and "
    + "y-intercept of 9.");
```

# [JavaScript](#tab/javascript)

```javascript
const conversationId =
    "conv_11112222AAAABBBB";

const response =
    await openAIClient.responses.create({
        input:
            "Hi, Agent! Draw a graph for a "
            + "line with a slope of 4 and "
            + "y-intercept of 9.",
        conversation: conversationId,
        agent_reference: {
            name: "my-agent",
            type: "agent_reference",
        },
    });
```

# [Java](#tab/java)

```java
AgentReference agentRef = new AgentReference("my-agent");

Response result = responsesClient.createWithAgent(
    agentRef,
    ResponseCreateParams.builder()
        .input("Hi, Agent! Draw a graph for a line "
        + "with a slope of 4 and "
        + "y-intercept of 9."));
```

---

### Responses

**Previous - runs**

```json
{
  "id": "run_xyz",
  "object": "thread.run",
  "created_at": 1762218810,
  "assistant_id": "asst_efgh5678",
  "thread_id": "thread_abcd1234",
  "status": "completed",
  "started_at": 1762218810,
  "expires_at": null,
  "cancelled_at": null,
  "failed_at": null,
  "completed_at": 1762218812,
  "required_action": null,
  "last_error": null,
  "model": "gpt-4.1",
  "instructions": "You politely help with math questions. Use the Code Interpreter tool when asked to visualize numbers. Please address the user as Jane Doe. The user has a premium account",
  "tools": [
    {
      "type": "code_interpreter"
    }
  ],
  "tool_resources": {},
  "metadata": {},
  "temperature": 1.0,
  "top_p": 1.0,
  "max_completion_tokens": null,
  "max_prompt_tokens": null,
  "truncation_strategy": {
    "type": "auto",
    "last_messages": null
  },
  "incomplete_details": null,
  "usage": {
    "prompt_tokens": 1216,
    "completion_tokens": 76,
    "total_tokens": 1292,
    "prompt_token_details": {
      "cached_tokens": 0
    }
  },
  "response_format": "auto",
  "tool_choice": "auto",
  "parallel_tool_calls": true
}
```

**Current - responses**

```json
{
  "id": "resp_3483e9c8dda4f165006909550333588190afc76a645a0e877a",
  "created_at": 1762219267.0,
  "error": null,
  "incomplete_details": null,
  "instructions": null,
  "metadata": {
    "x-ms-telemetry-agent-kind": "",
    "x-ms-telemetry-user-agent": "OpenAI/Python 2.4.0",
    "x-ms-telemetry-response-start-time": "2025-11-04T01:21:06.5346780+00:00"
  },
  "model": "gpt-4.1",
  "object": "response",
  "output": [
    {
      "id": "msg_3483e9c8dda4f1650069095503abf881909917865574cddf2c",
      "content": [
        {
          "annotations": [],
          "text": "Of course! Here's a simple plot for the line with a rate of change of 4 and a y-intercept of 9.\\n\\nThe equation of the line is:\\n\\n\\\\[ y = 4x + 9 \\\\]\\n\\nLet's draw a graph for it:\\n\\n---\\n\\n```plaintext\\n  |\\n20|                     *\\n  |                  *\\n  |               *\\n  |            *\\n10|         *\\n  |      *\\n  |   *\\n  |*\\n  +---------------------------\\n   -2 -1  0  1  2  3\\n```\\n\\n**Key points:**\\n- The y-intercept is **9**, so at \\\\(x = 0\\\\), \\\\(y = 9\\\\) (point: (0,9))\\n- For each step right (increase in x), y goes up 4 units (rate of change \\\\(m = 4\\\\))\\n  - For \\\\(x = 1\\\\): \\\\(y = 4(1) + 9 = 13\\\\) (point: (1,13))\\n  - For \\\\(x = -1\\\\): \\\\(y = 4(-1) + 9 = 5\\\\) (point: (-1,5))\\n\\nIf you'd like a precise graph or want to visualize it interactively, let me know!",

          "type": "output_text",
          "logprobs": []
        }
      ],
      "role": "assistant",
      "status": "completed",
      "type": "message"
    }
  ],
  "parallel_tool_calls": true,
  "temperature": 1.0,
  "tool_choice": "auto",
  "tools": [],
  "top_p": 1.0,
  "background": false,
  "conversation": {
    "id": "conv_3483e9c8dda4f16500GwcAgtdWlSmbMPzYLjWvDjiSe6LSFcC6"
  },
  "max_output_tokens": null,
  "max_tool_calls": null,
  "previous_response_id": null,
  "prompt": null,
  "prompt_cache_key": null,
  "reasoning": {
    "effort": null,
    "generate_summary": null,
    "summary": null
  },
  "safety_identifier": null,
  "service_tier": "default",
  "status": "completed",
  "text": {
    "format": {
      "type": "text"
    },
    "verbosity": "medium"
  },
  "top_logprobs": 0,
  "truncation": "disabled",
  "usage": {
    "input_tokens": 45,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 264,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 309
  },
  "user": null,
  "content_filters": null,
  "store": true
}
```

## Migrate classic agents to new agents

If you use the `client.agents.create_agent()` method from earlier SDK versions, migrate to `client.agents.create_version()`. The new method introduces structured agent definitions with explicit `kind`, `model`, and `instructions` fields.

### Requests

**Previous**

# [Python](#tab/python)

```python
agent = client.agents.create_agent( 
    model="gpt-4.1", 
    name="my-agent",  # Name of the agent 
    instructions="You politely help with math questions. Use the Code Interpreter tool when asked to visualize numbers.",  # Instructions for the agent 
    tools=code_interpreter.definitions,  # Attach the tool 
) 
```

# [C#](#tab/csharp)

```csharp
Agent agent =
    await agentsClient.CreateAgentAsync(
        model: "gpt-4.1",
        name: "my-agent",
        instructions:
            "You politely help with "
            + "math questions. Use the "
            + "Code Interpreter tool "
            + "when asked to visualize "
            + "numbers.",
        tools: new List<ToolDefinition>
        {
            new CodeInterpreterToolDefinition()
        });
```

# [JavaScript](#tab/javascript)

```javascript
const agent =
    await client.agents.createAgent(
        "gpt-4.1",
        {
            name: "my-agent",
            instructions:
                "You politely help with "
                + "math questions. Use "
                + "the Code Interpreter "
                + "tool when asked to "
                + "visualize numbers.",
            tools: [
                { type: "code_interpreter" },
            ],
        }
    );
```

# [Java](#tab/java)

```java
Agent agent =
    agentsClient.createAgent("gpt-4.1",
        new CreateAgentOptions()
            .setName("my-agent")
            .setInstructions(
                "You politely help with "
                + "math questions. Use the "
                + "Code Interpreter tool "
                + "when asked to visualize "
                + "numbers.")
            .setTools(Arrays.asList(
                new CodeInterpreterToolDefinition())));
```

---

**Current**

# [Python](#tab/python)

```python
from azure.ai.projects.models import (
    CodeInterpreterTool,
    PromptAgentDefinition,
)

agent = project.agents.create_version(
    agent_name="my-agent",
    definition=PromptAgentDefinition(
        model="gpt-4.1",
        instructions=(
            "You politely help with math "
            "questions. Use the Code "
            "Interpreter tool when asked to "
            "visualize numbers."
        ),
        tools=[CodeInterpreterTool()],
    ),
)
```

# [C#](#tab/csharp)

```csharp
var agent = await projectClient.Agents
    .CreateAgentVersionAsync(
        agentName: "my-agent",
        options: new(
            new PromptAgentDefinition("gpt-4.1")
            {
                Instructions =
                    "You politely help with math "
                    + "questions. Use the Code "
                    + "Interpreter tool when asked "
                    + "to visualize numbers.",
                Tools =
                {
                    new CodeInterpreterToolDefinition()
                },
            }));
```

# [JavaScript](#tab/javascript)

```javascript
const agent =
    await projectClient.agents.createVersion(
        "my-agent",
        {
            kind: "prompt",
            model: "gpt-4.1",
            instructions:
                "You politely help with math "
                + "questions. Use the Code "
                + "Interpreter tool when asked "
                + "to visualize numbers.",
            tools: [
                { type: "code_interpreter" },
            ],
        }
    );
```

# [Java](#tab/java)

```java
import com.azure.ai.agents.models.PromptAgentDefinition;
import com.azure.ai.agents.models.CodeInterpreterTool;

PromptAgentDefinition definition =
    new PromptAgentDefinition("gpt-4.1");
definition.setInstructions(
    "You politely help with math questions. "
    + "Use the Code Interpreter tool when "
    + "asked to visualize numbers.");
definition.setTools(Arrays.asList(
    new CodeInterpreterTool()));

var agent = agentsClient.createAgentVersion(
    "my-agent", definition);
```

---

### Responses

The following JSON examples compare the response objects returned by the previous and current agent creation methods.

**Previous**

```python
{ 
  'id': 'asst_AVKrdr2KJthDnZiJ51nca1jy', 
  'object': 'assistant', 
  'created_at': 1762218496, 
  'name': 'my-agent', 
  'description': None, 
  'model': 'gpt-4.1', 
  'instructions': 'You politely help with math questions. Use the Code Interpreter tool when asked to visualize numbers.', 
  'tools': [ 
    { 
      'type': 'code_interpreter' 
    } 
  ], 
  'top_p': 1.0, 
  'temperature': 1.0, 
  'tool_resources': { 
    'code_interpreter': { 
      'file_ids': [      
      ] 
    } 
  }, 
  'metadata': { 
  }, 
  'response_format': 'auto' 
} 
```
**Current**

```json
{
  "metadata": {},
  "object": "agent.version",
  "id": "code-agent:1",
  "name": "code-agent",
  "version": "1",
  "description": "Agent with code interpreter",
  "created_at": 1772045947,
  "definition": {
    "kind": "prompt",
    "model": "gpt-4.1",
    "instructions": "You politely help with math questions. Use the Code Interpreter tool when asked to visualize numbers.",
    "tools": [
      {
        "type": "code_interpreter"
      }
    ]
  }
}
```

## Migrate assistants to new agents

If your code uses the OpenAI Assistants API (`client.beta.assistants.create()`), migrate to the Foundry Agent Service by using `client.agents.create_version()`. The following examples show the structural differences.

**Previous - assistants**

# [Python](#tab/python)

```python
assistant = client.beta.assistants.create( 
    model="gpt-4.1", 
    name="my-assistant", 
    instructions="You politely help with math questions. Use the Code Interpreter tool when asked to visualize numbers.",  # Instructions for the agent 
    tools=[{"type": "code_interpreter"}], 
) 
```

# [C#](#tab/csharp)

```csharp
// Using the OpenAI Assistants API
AzureOpenAIClient azureClient = new(
    new Uri(Environment.GetEnvironmentVariable(
        "AZURE_OPENAI_ENDPOINT")!),
    new DefaultAzureCredential());
AssistantClient assistantClient =
    azureClient.GetAssistantClient();

Assistant assistant =
    await assistantClient
        .CreateAssistantAsync(
            "gpt-4.1",
            new AssistantCreationOptions
            {
                Name = "my-assistant",
                Instructions =
                    "You politely help "
                    + "with math questions. "
                    + "Use the Code "
                    + "Interpreter tool "
                    + "when asked to "
                    + "visualize numbers.",
                Tools =
                {
                    new CodeInterpreterToolDefinition()
                },
            });
```

# [JavaScript](#tab/javascript)

```javascript
// Using the OpenAI Assistants API
const assistant =
    await client.beta.assistants.create({
        model: "gpt-4.1",
        name: "my-assistant",
        instructions:
            "You politely help with math "
            + "questions. Use the Code "
            + "Interpreter tool when "
            + "asked to visualize numbers.",
        tools: [{ type: "code_interpreter" }],
    });
```

# [Java](#tab/java)

```java
// Using the OpenAI Assistants API
AssistantCreationOptions options =
    new AssistantCreationOptions("gpt-4.1")
        .setName("my-assistant")
        .setInstructions(
            "You politely help with math "
            + "questions. Use the Code "
            + "Interpreter tool when "
            + "asked to visualize numbers.")
        .setTools(Arrays.asList(
            new CodeInterpreterToolDefinition()));

Assistant assistant =
    agentsClient.createAssistant(options);
```

---

**Current - new agents**

# [Python](#tab/python)

```python
from azure.ai.projects.models import (
    CodeInterpreterTool,
    PromptAgentDefinition,
)

agent = project.agents.create_version(
    agent_name="my-agent",
    definition=PromptAgentDefinition(
        model="gpt-4.1",
        instructions=(
            "You politely help with math "
            "questions. Use the Code "
            "Interpreter tool when asked to "
            "visualize numbers."
        ),
        tools=[CodeInterpreterTool()],
    ),
)
```

# [C#](#tab/csharp)

```csharp
var agent = await projectClient.Agents
    .CreateAgentVersionAsync(
        agentName: "my-agent",
        options: new(
            new PromptAgentDefinition("gpt-4.1")
            {
                Instructions =
                    "You politely help with math "
                    + "questions. Use the Code "
                    + "Interpreter tool when asked "
                    + "to visualize numbers.",
                Tools =
                {
                    new CodeInterpreterToolDefinition()
                },
            }));
```

# [JavaScript](#tab/javascript)

```javascript
const agent =
    await projectClient.agents.createVersion(
        "my-agent",
        {
            kind: "prompt",
            model: "gpt-4.1",
            instructions:
                "You politely help with math "
                + "questions. Use the Code "
                + "Interpreter tool when asked "
                + "to visualize numbers.",
            tools: [
                { type: "code_interpreter" },
            ],
        }
    );
```

# [Java](#tab/java)

```java
import com.azure.ai.agents.models.PromptAgentDefinition;
import com.azure.ai.agents.models.CodeInterpreterTool;

PromptAgentDefinition definition =
    new PromptAgentDefinition("gpt-4.1");
definition.setInstructions(
    "You politely help with math questions. "
    + "Use the Code Interpreter tool when "
    + "asked to visualize numbers.");
definition.setTools(Arrays.asList(
    new CodeInterpreterTool()));

var agent = agentsClient.createAgentVersion(
    "my-agent", definition);
```

---

## Run the migration tool

A [migration tool](https://aka.ms/agent/migrate/tool) is available on GitHub to help automate the migration of your agents and assistants. The tool migrates code constructs such as agent definitions, thread creation, message creation, and run creation. It doesn't migrate state data like past runs, threads, or messages. After migration, you can run the new code, and any new state data is created in the updated format.

The following example shows a complete before-and-after comparison. Notice that the current code uses both `project` for agent creation and `openai` for conversations and responses. 

**Previous**

# [Python](#tab/python)

```python
agent = project_client.agents.create_agent( 
    model="gpt-4.1", 
    name="my-agent", 
    instructions="You politely help with math questions. Use the Code Interpreter tool when asked to visualize numbers.",  # Instructions for the agent 
    tools=[{"type": "code_interpreter"}] 
) 
thread = project_client.agents.threads.create() 
message = project_client.agents.messages.create( 
    thread_id=thread.id, 
    role="user",  # Role of the message sender 
    content="Hi, Agent! Draw a graph for a line with a rate of change of 4 and y-intercept of 9.",  # Message content 
) 
run = project_client.agents.runs.create_and_process( 
    thread_id=thread.id, 
    agent_id=agent.id, 
    additional_instructions="Please address the user as Jane Doe. The user has a premium account", 
) 
messages = project_client.agents.messages.list(thread_id=thread.id) 
for message in messages: 
    print(f"Role: {message.role}, Content: {message.content}") 
```

# [C#](#tab/csharp)

```csharp
// Create agent
Agent agent =
    await agentsClient.CreateAgentAsync(
        model: "gpt-4.1",
        name: "my-agent",
        instructions:
            "You politely help with "
            + "math questions. Use the "
            + "Code Interpreter tool "
            + "when asked to visualize "
            + "numbers.",
        tools: new List<ToolDefinition>
        {
            new CodeInterpreterToolDefinition()
        });

// Create thread
AgentThread thread =
    await agentsClient.CreateThreadAsync();

// Create message
await agentsClient.CreateMessageAsync(
    thread.Id,
    MessageRole.User,
    "Hi, Agent! Draw a graph for a "
    + "line with a rate of change "
    + "of 4 and y-intercept of 9.");

// Create run and poll
ThreadRun run =
    await agentsClient.CreateRunAsync(
        thread.Id,
        agent.Id,
        additionalInstructions:
            "Please address the user as "
            + "Jane Doe. The user has a "
            + "premium account");

while (run.Status ==
        RunStatus.Queued
    || run.Status ==
        RunStatus.InProgress)
{
    await Task.Delay(1000);
    run = await agentsClient.GetRunAsync(
        thread.Id,
        run.Id);
}

// Get messages
var messages = agentsClient.GetMessages(
    thread.Id);
foreach (var msg in messages)
{
    Console.WriteLine(
        $"Role: {msg.Role}, "
        + $"Content: {msg.Content}");
}
```

# [JavaScript](#tab/javascript)

```javascript
// Create agent
const agent =
    await client.agents.createAgent(
        "gpt-4.1",
        {
            name: "my-agent",
            instructions:
                "You politely help with "
                + "math questions. Use "
                + "the Code Interpreter "
                + "tool when asked to "
                + "visualize numbers.",
            tools: [
                { type: "code_interpreter" },
            ],
        }
    );

// Create thread
const thread =
    await client.agents.createThread();

// Create message
await client.agents.createMessage(
    thread.id,
    {
        role: "user",
        content:
            "Hi, Agent! Draw a graph "
            + "for a line with a rate "
            + "of change of 4 and "
            + "y-intercept of 9.",
    }
);

// Create run and poll
let run = await client.agents.createRun(
    thread.id,
    agent.id,
    {
        additionalInstructions:
            "Please address the user as "
            + "Jane Doe. The user has a "
            + "premium account",
    });

while (run.status === "queued"
    || run.status === "in_progress") {
    await new Promise(
        (r) => setTimeout(r, 1000));
    run = await client.agents.getRun(
        thread.id, run.id);
}

// Get messages
const messages =
    await client.agents.listMessages(
        thread.id);
for (const msg of messages.data) {
    console.log(
        `Role: ${msg.role}, `
        + `Content: ${msg.content}`);
}
```

# [Java](#tab/java)

```java
// Create agent
Agent agent =
    agentsClient.createAgent("gpt-4.1",
        new CreateAgentOptions()
            .setName("my-agent")
            .setInstructions(
                "You politely help with "
                + "math questions. Use the "
                + "Code Interpreter tool "
                + "when asked to visualize "
                + "numbers.")
            .setTools(Arrays.asList(
                new CodeInterpreterToolDefinition())));

// Create thread
AgentThread thread =
    agentsClient.createThread();

// Create message
agentsClient.createMessage(
    thread.getId(),
    new CreateMessageOptions(
        MessageRole.USER,
        "Hi, Agent! Draw a graph for "
        + "a line with a rate of change "
        + "of 4 and y-intercept of 9."));

// Create run and poll
ThreadRun run =
    agentsClient.createRun(
        thread.getId(),
        agent.getId(),
        new CreateRunOptions()
            .setAdditionalInstructions(
                "Please address the user "
                + "as Jane Doe. The user "
                + "has a premium account"));

while (RunStatus.QUEUED
        .equals(run.getStatus())
    || RunStatus.IN_PROGRESS
        .equals(run.getStatus())) {
    Thread.sleep(1000);
    run = agentsClient.getRun(
        thread.getId(),
        run.getId());
}

// Get messages
PageableList<ThreadMessage> messages =
    agentsClient.listMessages(
        thread.getId());
for (ThreadMessage msg : messages) {
    System.out.printf(
        "Role: %s, Content: %s%n",
        msg.getRole(),
        msg.getContent());
}
```

---

**Current**

# [Python](#tab/python)

```python
from azure.ai.projects.models import (
    CodeInterpreterTool,
    PromptAgentDefinition,
)

# Create the agent
agent = project.agents.create_version(
    agent_name="my-agent",
    definition=PromptAgentDefinition(
        model="gpt-4.1",
        instructions=(
            "You politely help with math "
            "questions. Use the Code "
            "Interpreter tool when asked "
            "to visualize numbers."
        ),
        tools=[CodeInterpreterTool()],
    ),
)

# Create a conversation with initial message
conversation = openai.conversations.create(
    items=[
        {
            "type": "message",
            "role": "user",
            "content": (
                "Hi, Agent! Draw a graph "
                "for a line with a rate "
                "of change of 4 and "
                "y-intercept of 9."
            ),
        }
    ],
)

# Send a response with the agent
response = openai.responses.create(
    conversation=conversation.id,
    extra_body={
        "agent_reference": {
            "name": agent.name,
            "type": "agent_reference",
        }
    },
    input=(
        "Please address the user as "
        "Jane Doe. The user has a "
        "premium account"
    ),
)

# Print the response output
for item in response.output:
    if item.type == "message":
        for block in item.content:
            print(block.text)
```

# [C#](#tab/csharp)

```csharp
var agent = await projectClient.Agents
    .CreateAgentVersionAsync(
        agentName: "my-agent",
        options: new(
            new PromptAgentDefinition("gpt-4.1")
            {
                Instructions =
                    "You politely help with math "
                    + "questions. Use the Code "
                    + "Interpreter tool when asked "
                    + "to visualize numbers.",
                Tools =
                {
                    new CodeInterpreterToolDefinition()
                },
            }));

ProjectResponsesClient responsesClient =
    projectClient.OpenAI
        .GetProjectResponsesClientForAgent(
            "my-agent");

var result = responsesClient.CreateResponse(
    "Hi, Agent! Draw a graph for a line "
    + "with a rate of change of 4 and "
    + "y-intercept of 9. Please address the "
    + "user as Jane Doe. The user has a "
    + "premium account");

// Print the response output
foreach (var item in result.OutputItems)
{
    if (item is ResponseMessageItem msg)
    {
        foreach (var block in msg.Content)
        {
            Console.WriteLine(block.Text);
        }
    }
}
```

# [JavaScript](#tab/javascript)

```javascript
const agent =
    await projectClient.agents.createVersion(
        "my-agent",
        {
            kind: "prompt",
            model: "gpt-4.1",
            instructions:
                "You politely help with math "
                + "questions. Use the Code "
                + "Interpreter tool when asked "
                + "to visualize numbers.",
            tools: [
                { type: "code_interpreter" },
            ],
        }
    );

const openAIClient =
    await projectClient.getOpenAIClient();

const conversation =
    await openAIClient.conversations.create({
        items: [
            {
                type: "message",
                role: "user",
                content:
                    "Hi, Agent! Draw a graph "
                    + "for a line with a rate "
                    + "of change of 4 and "
                    + "y-intercept of 9.",
            },
        ],
    });

const response =
    await openAIClient.responses.create({
        input:
            "Please address the user as "
            + "Jane Doe. The user has a "
            + "premium account",
        conversation: conversation.id,
        agent_reference: {
            name: agent.name,
            type: "agent_reference",
        },
    });

// Print the response output
for (const item of response.output) {
    if (item.type === "message") {
        for (const block of item.content) {
            console.log(block.text);
        }
    }
}
```

# [Java](#tab/java)

```java
import com.azure.ai.agents.models.PromptAgentDefinition;
import com.azure.ai.agents.models.CodeInterpreterTool;

PromptAgentDefinition definition =
    new PromptAgentDefinition("gpt-4.1");
definition.setInstructions(
    "You politely help with math questions. "
    + "Use the Code Interpreter tool when "
    + "asked to visualize numbers.");
definition.setTools(Arrays.asList(
    new CodeInterpreterTool()));

var agent = agentsClient.createAgentVersion(
    "my-agent", definition);

ResponsesClient responsesClient =
    new AgentsClientBuilder()
        .credential(
            new DefaultAzureCredentialBuilder()
                .build())
        .endpoint(System.getenv(
            "PROJECT_ENDPOINT"))
        .buildResponsesClient();

AgentReference agentRef = new AgentReference("my-agent");

Response result = responsesClient.createWithAgent(
    agentRef,
    ResponseCreateParams.builder()
        .input("Hi, Agent! Draw a graph for a line "
        + "with a rate of change of 4 and "
        + "y-intercept of 9. Please address "
        + "the user as Jane Doe. The user "
        + "has a premium account"));

// Print the response output
for (ResponseItem item : result.getOutput()) {
    if (item instanceof ResponseMessageItem) {
        ResponseMessageItem msg =
            (ResponseMessageItem) item;
        for (ContentBlock block
                : msg.getContent()) {
            System.out.println(
                block.getText());
        }
    }
}
```

---
## Verify your migration

After you migrate your code, confirm that everything works correctly:

1. **Run the updated code** and verify that it executes without errors.
1. **Check agent creation** by confirming that `create_version()` returns an object with an `id` and `version` field.
1. **Test a conversation** by creating a conversation, sending a response, and verifying that output items are returned.
1. **Confirm context retention** by sending multiple responses to the same conversation and checking that the agent remembers earlier messages.

## Troubleshoot common issues

| Symptom | Cause | Resolution |
| --------- | ------- | ------------ |
| **Python**: `AttributeError: 'AIProjectClient' has no attribute 'conversations'` | You called `conversations.create()` on the project client instead of the OpenAI client. | Use `project.get_openai_client()` to obtain the OpenAI client, then call `openai.conversations.create()`. |
| **C#**: `Azure.AI.Extensions.OpenAI` namespace not found | The `Azure.AI.Extensions.OpenAI` NuGet package is missing. | Install `Azure.AI.Projects` (which brings in `Azure.AI.Extensions.OpenAI` and `Azure.AI.Projects.Agents` as dependencies). |
| **JavaScript**: `getOpenAIClient is not a function` | You're using an older version of `@azure/ai-projects`. | Update to `@azure/ai-projects@2.0.0-beta.5` or later: `npm install @azure/ai-projects@2.0.0-beta.5`. |
| **Java**: `AgentsClientBuilder` can't resolve | The `azure-ai-agents` Maven dependency is missing or outdated. | Add `com.azure:azure-ai-agents:2.0.0-beta.2` to your `pom.xml` dependencies. |
| `create_agent()` is removed | Earlier SDK versions used `create_agent()`, which was removed in v2.0.0. | Replace with `create_version()` (Python/JS) or `CreateAgentVersionAsync()` (C#) or `createAgentVersion()` (Java) and pass a `PromptAgentDefinition` object. |
| Old thread data isn't available | The migration tool doesn't migrate state data (past runs, threads, or messages). | Start new conversations after migration. Historical data remains accessible through the previous API until it's deprecated. |
| `responses.create()` raises a model error | The model name might be incorrect or unavailable in your region. | Verify the model name in your Foundry project and check [model region availability](../concepts/limits-quotas-regions.md). |

## Related content

- [Agent runtime components](../concepts/runtime-components.md)
- [Quickstart: Create a hosted agent](../quickstarts/quickstart-hosted-agent.md)
- [Deploy a hosted agent](deploy-hosted-agent.md)
