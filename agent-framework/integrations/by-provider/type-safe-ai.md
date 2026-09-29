---
title: TypeSafe AI
titleSuffix: Microsoft Agent Framework
description: Use TypeSafe AI System One models for typed decisions with Agent Framework Python.
author: eavanvalkenburg
ms.topic: article
ms.author: edvan
ms.date: 09/29/2026
ms.service: agent-framework
ai-usage: ai-assisted
---

# TypeSafe AI

The alpha TypeSafe AI integration adapts System One models, including Jev, to
Agent Framework Python. These models evaluate application state against typed
questions and return probabilities and scores. They don't generate ordinary
free-form chat responses.

## Install the package

```bash
pip install agent-framework-typesafe --pre
```

## Configuration

Set the API key before creating the client:

```bash
TYPESAFE_API_KEY="<api-key>"
# Optional:
TYPESAFE_DEFAULT_MODEL="jev-latest"
TYPESAFE_BASE_URL="<api-root>"
```

Constructor values take precedence over environment variables. You can also
inject a configured TypeSafe `AsyncTypeSafeClient`. Injected clients remain
caller-owned; close clients created by `TypeSafeChatClient` with `close()` or
an asynchronous context manager.

## Create a typed decision agent

Pass a TypeSafe `Questions` mapping through the Agent Framework
`response_format` option:

```python
import asyncio

from agent_framework import Agent
from agent_framework_typesafe import TypeSafeChatClient
from typesafe_sdk import Choice, Noul


async def main() -> None:
    client = TypeSafeChatClient()
    try:
        agent = Agent(
            client=client,
            name="TicketEvaluator",
            instructions="Evaluate the support request.",
        )
        response = await agent.run(
            "Our checkout has failed for three days and we are losing sales.",
            options={
                "response_format": {
                    "department": Choice(
                        instructions="Which team should handle this request?",
                        criteria={
                            "billing": None,
                            "technical": None,
                            "sales": None,
                        },
                    ),
                    "urgent": Noul(
                        instructions="Does this request need urgent attention?"
                    ),
                },
            },
        )
        print(response.value)
    finally:
        await client.close()


asyncio.run(main())
```

For this connector, `response_format` is a nonempty TypeSafe `Questions`
mapping containing `Noul`, `Choice`, or `Score` questions. You can access the
complete typed `SystemOneResponse` through `response.value`.

Use `default_questions` on the client when an integration has one fixed
contract. For example, a TypeSafe client with default questions can act as the
quarantine client for `SecureAgentConfig`.

## Function and MCP tools

`TypeSafeChatClient` supports the standard Agent Framework function-invocation
loop for closed-set schemas. Supported argument shapes include:

- Fixed constants.
- Enums or Python `Literal` values.
- Boolean values.
- Arrays of enum or `Literal` values without additional array constraints.
- Optional versions of those shapes.

The client doesn't support required free-form strings or numbers, nested
objects, general arrays, required nullable arguments, or schema constraints
that the connector can't preserve. If you specify an unsupported argument, the
client excludes the entire tool in automatic mode or rejects the tool when you
require it.

MCP tools work through `Agent`, which discovers MCP functions and expands them
into function tools before TypeSafe routing. Only functions whose schemas fit
the supported subset are routable. A request supports at most 32 routable
tools, 64 properties per tool, 64 enum members per argument, and 128 generated
internal questions.

The client defaults to one tool call per run. Configure
`function_invocation_configuration={"max_function_calls": N}` to allow
sequential tool round trips.

## Capabilities and limits

| Capability | Support |
|---|---|
| Typed classification, scoring, and routing | TypeSafe `Questions` and `SystemOneResponse` |
| Agent Framework middleware and telemetry | Supported |
| Local function tools | Supported for the constrained schema subset |
| MCP functions | Supported for the constrained schema subset |
| Streaming | Not supported |
| Free-form text generation | Not supported |
| Non-text message content | Not supported |
| Generative options such as `temperature` | Rejected |

Use `TypeSafeChatClient` for the standard framework layers. Use
`RawTypeSafeChatClient` only when you intentionally want to compose a custom
layer stack or opt out of function execution, middleware, and telemetry.

## Next steps

> [!div class="nextstepaction"]
> [Use structured outputs](../../agents/structured-outputs.md)
