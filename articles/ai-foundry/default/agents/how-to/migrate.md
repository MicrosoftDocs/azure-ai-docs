---
title: Migrate to the new Foundry Agent Service
titleSuffix: Microsoft Foundry
description: Learn how to migrate from the Assistants API and classic agents to the new Foundry Agent Service, including threads to conversations, runs to responses, and updated SDK patterns.
author: aahill
ms.author: aahi
manager: nitinme
ms.date: 02/17/2026
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
- A [Microsoft Foundry project](../../../how-to/create-projects.md).
- The `azure-ai-projects` Python SDK (version 2.0.0b1 or later). Install with `pip install "azure-ai-projects>=2.0.0b1" --pre`.
- The `azure-identity` package for authentication. Install with `pip install azure-identity` and sign in with `az login` or use `DefaultAzureCredential`.
- Existing agents or assistants code that you want to migrate.

The following code initializes the clients used throughout this guide:

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

project_client = AIProjectClient(
    endpoint="<your-project-endpoint>",
    credential=DefaultAzureCredential(),
)
openai_client = project_client.get_openai_client()
```

Use `project_client` for agent creation and versioning. Use `openai_client` for conversations and responses.

### Key benefits

The new agents provide the following benefits:

**Developer productivity**

- ⭐ **More models.** Generate responses by using any Foundry model either in your agent or directly as a response generation call.
- **More features.** Web Search, File Search, Code Interpreter, MCP tool calling, image generation, and reasoning summaries.
- **Modern API primitive.** Built on the Responses API instead of the older Assistants API.
- **Future-proof.** New features and model support are only added to the new agents.
- **New agent types.** Create prompt-based or workflow-based agents.

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

> [!IMPORTANT]
> In the new API, the conversations and responses APIs use the **OpenAI client**, which you obtain by calling `project_client.get_openai_client()`. Agent creation and versioning remain on the **project client** (`AIProjectClient`). The examples in each section reflect which client to use.

## Migrate threads to conversations

Threads stored messages on the server side. A conversation can store items, including messages, tool calls, tool outputs, and other data.

### Requests

The following examples compare thread creation (previous) with conversation creation (current). The current approach uses the OpenAI client obtained from `project_client.get_openai_client()`.

**Previous - threads**

```python
thread = client.agents.threads.create( 
     messages=[{"role": "user", "content": "Tell me a one line funny story about unicorns"}], 
     metadata={"agent": "my-awesome-agent"}, 
) 
```

**Current - conversations**

```python
conversation = openai_client.conversations.create( 
    items=[{"type": "message", "role": "user", "content": "Tell me a one line funny story about unicorns"}], 
    metadata={"agent": "my-awesome-agent"} 
) 
```

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

```python
message = client.agents.messages.create(
    thread_id=thread.id,
    role="user",
    content="Follow-up question about the same topic",
)
```

**Current - add items to a conversation**

```python
openai_client.conversations.items.create(
    conversation_id=conversation.id,
    items=[{"type": "message", "role": "user", "content": "Follow-up question about the same topic"}],
)
```

## Migrate runs to responses

Runs were asynchronous processes that executed against threads. Responses are simpler: provide a set of input items to execute and get a list of output items back. Responses can be used alone, or with conversation objects for storing context. The responses API uses the OpenAI client.

### Requests

The following examples compare how you invoke agent logic. The previous approach used asynchronous runs with polling. The current approach calls `responses.create()` on the OpenAI client.

**Previous - runs**

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

**Current - responses**

```python
conversation_id = "conv_11112222AAAABBBB"

response = openai_client.responses.create(
    model="gpt-4.1",
    input=[{"role": "user", "content": "Hi, Agent! Draw a graph for a line with a slope of 4 and y-intercept of 9."}],
    conversation=conversation_id,
    extra_body={"agent_reference": {"type": "agent_reference", "name": "my-agent", "version": "1"}}
)
```


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

```python
agent = client.agents.create_agent( 
    model="gpt-4.1", 
    name="my-agent",  # Name of the agent 
    instructions="You politely help with math questions. Use the Code Interpreter tool when asked to visualize numbers.",  # Instructions for the agent 
    tools=code_interpreter.definitions,  # Attach the tool 
) 
```


**Current**

```python
from azure.ai.projects.models import PromptAgentDefinition

agent = project_client.agents.create_version( 
    agent_name="my-agent", 
    definition=PromptAgentDefinition(
        model="gpt-4.1",  
        instructions="You politely help with math questions. Use the Code Interpreter tool when asked to visualize numbers."
    )
) 
```

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

```python
{ 
  'metadata': {  
  }, 
  'object': 'agent.version', 
  'id': 'my-agent:1', 
  'name': 'my-agent', 
  'version': '1', 
  'description': '', 
  'created_at': 1762219751, 
  'definition': { 
    'kind': 'prompt', 
    'model': 'gpt-4.1', 
    'instructions': 'You politely help with math questions. Use the Code Interpreter tool when asked to visualize numbers.' 
  } 
} 
```

## Migrate assistants to new agents

If your code uses the OpenAI Assistants API (`client.beta.assistants.create()`), migrate to the Foundry Agent Service by using `client.agents.create_version()`. The following examples show the structural differences.

**Previous - assistants**

```python
assistant = client.beta.assistants.create( 
    model="gpt-4.1", 
    name="my-assistant", 
    instructions="You politely help with math questions. Use the Code Interpreter tool when asked to visualize numbers.",  # Instructions for the agent 
    tools=[{"type": "code_interpreter"}], 
) 
```

**Current - new agents**

```python
from azure.ai.projects.models import PromptAgentDefinition

agent = project_client.agents.create_version( 
    agent_name="my-agent", 
    definition=PromptAgentDefinition(
        model="gpt-4.1",  
        instructions="You politely help with math questions. Use the Code Interpreter tool when asked to visualize numbers."
    )
) 
```

## Run the migration tool

A [migration tool](https://aka.ms/agent/migrate/tool) is available on GitHub to help automate the migration of your agents and assistants. The tool migrates code constructs such as agent definitions, thread creation, message creation, and run creation. It doesn't migrate state data like past runs, threads, or messages. After migration, you can run the new code, and any new state data is created in the updated format.

The following example shows a complete before-and-after comparison. Notice that the current code uses both `project_client` for agent creation and `openai_client` for conversations and responses. 

**Previous**

```python
agent = project_client.agents.create_agent( 
    model="gpt-4.1", 
    name="my-agent", 
    instructions="You politely help with math questions. Use the Code Interpreter tool when asked to visualize numbers.",  # Instructions for the agent 
    tools=[{"type": "code_interpreter"}] 
) 
thread = project_client.agents.threads.create() 
message = project_client.agents.messages.create( 
    thread_id=thread.id, 
    role="user",  # Role of the message sender 
    content="Hi, Agent! Draw a graph for a line with a rate of change of 4 and y-intercept of 9.",  # Message content 
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

**Current**

```python
from azure.ai.projects.models import CodeInterpreterTool, PromptAgentDefinition

with project_client.get_openai_client() as openai_client:
    agent = project_client.agents.create_version( 
        agent_name="my-agent", 
        definition=PromptAgentDefinition(
            model="gpt-4.1",
            instructions="You politely help with math questions. Use the Code Interpreter tool when asked to visualize numbers.",
            tools=[CodeInterpreterTool()]
        ) 
    )
    conversation = openai_client.conversations.create( 
        items=[{"type": "message", "role": "user", "content": "Hi, Agent! Draw a graph for a line with a rate of change of 4 and y-intercept of 9."}], 
    ) 
    response = openai_client.responses.create( 
        conversation=conversation.id,
        extra_body={"agent": {"type": "agent_reference", "name": agent.name, "version": agent.version}},
        input="Please address the user as Jane Doe. The user has a premium account"
    ) 
```
## Verify your migration

After you migrate your code, confirm that everything works correctly:

1. **Run the updated code** and verify that it executes without errors.
1. **Check agent creation** by confirming that `create_version()` returns an object with an `id` and `version` field.
1. **Test a conversation** by creating a conversation, sending a response, and verifying that output items are returned.
1. **Confirm context retention** by sending multiple responses to the same conversation and checking that the agent remembers earlier messages.

## Troubleshoot common issues

| Symptom | Cause | Resolution |
| --------- | ------- | ------------ |
| `AttributeError: 'AIProjectClient' has no attribute 'conversations'` | You called `conversations.create()` on the project client instead of the OpenAI client. | Use `project_client.get_openai_client()` to obtain the OpenAI client, then call `openai_client.conversations.create()`. |
| `create_agent()` is deprecated | Earlier SDK versions used `create_agent()`. | Replace with `create_version()` and pass a `PromptAgentDefinition` object as the `definition` parameter. |
| Old thread data isn't available | The migration tool doesn't migrate state data (past runs, threads, or messages). | Start new conversations after migration. Historical data remains accessible through the previous API until it's deprecated. |
| `responses.create()` raises a model error | The model name might be incorrect or unavailable in your region. | Verify the model name in your Foundry project and check [model region availability](../../../how-to/deploy-models-serverless-availability.md). |

## Related content

- [Agent runtime components](../concepts/runtime-components.md)
- [Quickstart: Create a hosted agent](../quickstarts/quickstart-hosted-agent.md)
- [Deploy a hosted agent](deploy-hosted-agent.md)
