---
title: Native computer use
titleSuffix: Microsoft Agent Framework
description: Handle native computer calls from Python Responses clients in Microsoft Agent Framework.
author: eavanvalkenburg
ms.topic: article
ms.author: edvan
ms.date: 09/29/2026
ms.service: agent-framework
ai-usage: ai-assisted
---

# Native computer use

Native computer use lets a Responses model request ordered desktop or browser
actions. Your application owns the execution environment, presents safety
checks for approval, performs the actions, captures a screenshot, and returns
the result to the model.

The following Python clients expose the native tool:

| Client | Factory | Notes |
|---|---|---|
| `OpenAIChatClient` | `get_computer_tool()` | Uses the OpenAI Responses API. |
| `FoundryChatClient` | `get_computer_tool()` | Requires `azure-ai-projects` 2.3.0 or later. |

`FoundryChatClient.get_computer_use_tool(...)` is a separate preview API. For
its configuration options, see the
[Microsoft Foundry model provider](../../integrations/by-component/model-providers/microsoft-foundry.md#computer-use).

## Add the tool to an agent

Create the provider tool and pass it to the agent:

```python
from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient

client = OpenAIChatClient()
agent = Agent(
    client=client,
    tools=[client.get_computer_tool()],
)
```

The model returns a `Content` item with
`type="computer_tool_call"`. The item includes:

- An item `id` and a distinct `call_id`.
- An ordered `actions` list.
- Optional `pending_safety_checks`.

Unanswered calls appear in `AgentResponse.user_input_requests`. Display the
actions and warnings to the user before your application executes anything.
The framework never acknowledges safety checks automatically.

## Return the result

After your application executes the approved actions, return a screenshot in a
tool message. The following fragment assumes `request` is the computer request,
`screenshot_bytes` is a PNG captured by your execution environment, and
`confirmed_checks` contains only checks that the user explicitly approved:

```python
from agent_framework import Content, Message

result = Content.from_computer_tool_result(
    call_id=request.call_id,
    screenshot=Content.from_data(screenshot_bytes, "image/png"),
    acknowledged_safety_checks=confirmed_checks,
)

tool_message = Message(role="tool", contents=[result])
response = await agent.run(tool_message, session=session)
```

Reuse the same `AgentSession` when you send the result. You can also provide the
screenshot with `Content.from_uri(...)` or
`Content.from_hosted_file(...)`. OpenAI and Foundry Responses require a
screenshot even though the shared result type allows providers to omit one.

The `ComputerSafetyCheck` type and
`Content.from_computer_tool_call(...)` and
`Content.from_computer_tool_result(...)` constructors are experimental Agent
Framework APIs. Calls and results can be persisted with `Content.to_dict()` and
restored with `Content.from_dict()`.

## Workflow behavior

When a workflow pauses for native computer input, Agent Framework preserves the
call ID, action order, and pending safety checks across checkpoints. If local
function calls complete in the same batch, their results are returned with the
computer result in the original call order.

If one computer request in an agent's pending batch is canceled, the remaining
requests in that batch are also canceled. Already completed results remain in
the terminal output, and the next turn starts with a fresh agent session.
