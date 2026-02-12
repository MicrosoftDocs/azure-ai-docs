---
title: "How to migrate to the new agent service"
titleSuffix: Microsoft Foundry
description: Learn how to migrate to the latest agents API in the Microsoft Foundry.
author: aahill
ms.author: aahi
manager: nitinme
ms.date: 12/09/2025
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
---


# Upgrading to the new agents developer experience 

> [!TIP]
> You can use the [available migration tool](https://aka.ms/agent/migrate/tool) to migrate from the Assistants API to Agents.

The new agents offer an upgraded experience which enables developers and enterprises to design intelligent agents that are easy to build, version, operate, and observe. It introduces a modernized API and SDK, new enterprise-grade capabilities, and preserves the identity, governance, and observability features customers rely on today. 

Key benefits 

The new agents provide the following benefits:

- **New Agent Types**: Create prompt-based, workflow-based, or container-based agents.
- **More models**: Generate responses using any Azure Foundry model either in your agent or directly as a response generation call.
- **Enterprise Readiness**: Use single tenant storage, with the added option to bring your own Cosmos DB to store state and keep your data secure.
- **Single or Multi-Agent Workflows**: Easily chain agents for complex workflows.
- **More features**: Web Search, File Search, Code Interpreter, MCP tool calling, image generation, and reasoning summaries.
- **Stateful Context**: Automatically retains context across calls unless opted out using store: false.
- **Deployable Agents**: agents can be exposed as individual endpoints.
- **Enhanced Security**: Control who can run or modify agent definitions.
- **Separation of Duties**: Define agents once; execute with various inputs.
- **Superset of Responses API**: builds on Responses API and adds more capabilities.
- **Improved State Management**: Uses conversations instead of threads/messages.
- **Modern API Primitive**: built on Responses API instead of the older Assistants API.
- **Future proof**: New features and model support will only be added to the new agents.
- **Lower Costs**: Improved cache utilization reduces costs.
- **Encrypted Reasoning**: Opt-out of statefulness while retaining advanced reasoning. 


## Key changes

| Before | After | Details |
|--------|-------|------|
| Threads | Conversations | Supports streams of items and not just messages. |
| Runs | Responses | Responses send input items or use a conversation object and receive output items. Tool call loops are explicitly managed. |
| Assistants / agents | agents (new) | Support for enterprise ready prompt workflow and hosted agents, stateful context by default to use with any Azure Foundry Model | 

## Threads to conversations 

Threads stored messages on the server-side. A conversation can store items – including messages, tool calls, tool outputs, and other data.

### Requests

**Previous - threads**

```python
thread = client.agents.threads.create( 
     messages=[{"role": "user", "content": "Tell me a one line funny story about unicorns"}], 
     metadata={"agent": "my-awesome-agent"}, 
) 
```

**Current - conversations**

```python
conversation = client.conversations.create( 
    items=[{"type": "message", "role": "user", "content": "Tell me a one line funny story about unicorns"}], 
    metadata={"agent": "my-awesome-agent"} 
) 
```

### Responses

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

## Runs to responses 

Runs are asynchronous processes that executed against threads. See the example below. Responses are simpler: provide a set of input items to execute and get a list of output items back. Responses can be used alone, or also with conversation objects for storing context. 

### Requests

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
    conversation=conversation_id
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

## Classic agents to new agents 

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
agent = client.agents.create_version( 
    agent_name="my-agent", 
    definition={ 
        "kind": "prompt", 
        "model": "gpt-4.1",  
        "instructions": "You politely help with math questions. Use the Code Interpreter tool when asked to visualize numbers." 
    }
) 
```

### Response

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

## Assistants to new agents

**Previous - assistants**

```python
assistant = client.beta.assistants.create( 
    model="gpt-4.1", 
    name="my-assistant", 
    instructions="You politely help with math questions. Use the Code Interpreter tool when asked to visualize numbers.",  # Instructions for the agent 
    tools=[{"type": "code_interpreter"}], 
) 
```

**Current - new agents**

```python
agent = client.agents.create_version( 
    agent_name="my-agent", 
    definition={ 
        "kind": "prompt", 
        "model": "gpt-4.1",  
        "instructions": "You politely help with math questions. Use the Code Interpreter tool when asked to visualize numbers." 
    } 
) 
```

## Migrating to new agents 

You can use the provided tool [available on GitHub](https://aka.ms/agent/migrate/tool) to migrate your agents and assistants to the new agents. It will only migrate code such as: agent definitions, thread creation, message creation, and run creation. It will not migrate state data like past runs, threads, or messages. After migration, you can run the new code, and any new state data will be created in the updated format. 

The following is an example of the previous and current format. 

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
with project_client.get_openai_client() as openai_client:
    agent = project_client.agents.create_version( 
        agent_name="my-agent", 
        definition={ 
            "kind": "prompt", 
            "model": "gpt-4.1",  
            "instructions": "You politely help with math questions. Use the Code Interpreter tool when asked to visualize numbers.", 
            "tools": [{"type": "code_interpreter", "container": {"type": "auto"}}] 
        } 
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
