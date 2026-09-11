---
title: "Delegate work in GPT-Live"
titleSuffix: Microsoft Foundry
description: Learn how GPT-Live delegates work to your application or to a Responses API model, and how to complete client-actionable function calls.
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: how-to
ms.date: 09/04/2026
author: PatrickFarley
ms.author: pafarley
recommendations: false
ai-usage: ai-assisted
---

# Delegate work in GPT-Live

[!INCLUDE [preview-feature](../includes/preview-feature.md)]

When a GPT-Live conversation needs search, deeper reasoning, or another action that the live model can't complete on its own, it delegates that work while the live interaction continues. GPT-Live supports two delegation modes, configured in the `delegation` field of [session configuration](gpt-live.md#session-configuration).

| Mode | Description |
|---|---|
| **Client delegation** | GPT-Live hands work to your application. Your client or backend performs the work and returns the result as context. This option is the most flexible, but it requires more upfront integration. |
| **Responses delegation** | GPT-Live routes the request to a configured [Responses API](responses.md) model. Hosted tools run server-side; client-actionable function calls are returned to your application for completion. |

Omitted or `null` delegation defaults to client delegation.

## Choose a delegation mode

Start with Responses delegation when its managed workflow fits your task. Choose client delegation when you need more control over the backend's context, execution, or the results that reach GPT-Live.

| Consideration | Favor Responses delegation when: | Favor client delegation when: |
|---|---|---|
| Implementation effort | You want GPT-Live to prepare backend requests, manage the connection, and return results to the conversation. | You want to build and operate those pieces yourself. |
| Reviewing backend results | Backend output can return directly to GPT-Live. | Your application must validate, redact, combine, or discard results before they reach GPT-Live. |
| Backend capabilities | Your workflow fits the Responses model and tools that GPT-Live supports. | You need another backend, multiple models, or capabilities beyond the managed configuration. |
| Context ownership | The conversation context that GPT-Live supplies fits your application. | You need to choose exactly which history, memory, and application state each backend request receives. |
| Execution policy | A configured model and tool loop fits the task. | You need custom routing, fallbacks, checkpoints, or budgets across backend steps. |

You choose the mode when you create the session. To change modes, start a new session. In both modes, your application enforces permissions and required confirmations before it runs a tool, and it keeps the authoritative task state.

## Configure a delegation mode

Set `delegation` in the session object. Client delegation:

```json
{
  "delegation": { "type": "client" }
}
```

Responses delegation, with tools:

```json
{
  "delegation": {
    "type": "responses",
    "responses": {
      "model": "gpt-5.5",
      "instructions": "Use tools when current information is required.",
      "tools": [
        { "type": "web_search" },
        {
          "type": "function",
          "name": "get_weather",
          "description": "Get current weather for a location.",
          "parameters": {
            "type": "object",
            "properties": { "location": { "type": "string" } },
            "required": ["location"],
            "additionalProperties": false
          }
        }
      ],
      "tool_choice": "auto",
      "parallel_tool_calls": true
    }
  }
}
```

`delegation.responses.service_tier` accepts `auto`, `default`, `flex`, or `priority`. Replacing `delegation` in a later `session.update` requires a complete delegation object—nested fields aren't patched independently. Set `delegation` to `null` to reset to client delegation.

## Handle client delegation

With client delegation, `delegation.created` contains the unit of work and a client-targeted item ID. Use that ID as `delegation_item_id` when you return the result as context.

```json
{
  "type": "delegation.created",
  "offset_ms": 1000,
  "item": {
    "id": "item_delegation_123",
    "type": "delegation",
    "target": "client",
    "content": [{ "type": "input_text", "text": "What is the weather?" }]
  }
}
```

```json
{
  "type": "delegation.context.append",
  "event_id": "event_delegation_context_1",
  "delegation_item_id": "item_delegation_123",
  "content": [{ "type": "input_text", "text": "It is 62 degrees and raining in Seattle." }]
}
```

```json
{
  "type": "delegation.context.appended",
  "delegation_item_id": "item_delegation_123",
  "start_ms": 1200,
  "end_ms": 1600
}
```

Each `delegation.context.append` event contains exactly one `input_text` part and is limited to 500 tokens. Repeated appends continue the same delegation stream—they don't create independently addressable context items. `delegation.context.appended` intentionally has no separate context-item ID; the delegation item ID is the stable correlation handle.

## Handle Responses delegation

With Responses delegation, `delegation.created` identifies the delegation item, sets `target: "responses"`, and includes a `response_id` that binds it to the Responses lifecycle. GPT-Live emits `delegation.created` immediately before the matching top-level `response.created` event. Don't send `response.create` into the GPT-Live event stream.

```json
{
  "type": "delegation.created",
  "offset_ms": 1000,
  "item": {
    "id": "item_delegation_456",
    "type": "delegation",
    "target": "responses",
    "response_id": "resp_123",
    "content": [{ "type": "input_text", "text": "What is the weather?" }]
  }
}
```

```json
{
  "type": "response.created",
  "response": { "id": "resp_123", "status": "in_progress", "model": "gpt-5.5" }
}
```

Responses events are passed through at the top level, without a wrapper. Dispatch on the full event type string, and tolerate new `response.*` lifecycle events. Delegated output text is also injected into the live session, so it can surface as normal transcript, turn, and audio output.

### Complete a client-actionable function call

When `response.function_call_arguments.done` identifies an actionable call, send one `delegation.function_call_output.create` event for that `call_id`. Unknown or already-resolved IDs are rejected, and parallel calls require one result event per call.

```json
{
  "type": "response.function_call_arguments.done",
  "response_id": "resp_123",
  "item_id": "fc_123",
  "output_index": 0,
  "call_id": "call_123",
  "name": "get_weather",
  "arguments": "{\"location\":\"Seattle\"}"
}
```

```json
{
  "type": "delegation.function_call_output.create",
  "event_id": "event_function_output_1",
  "item": {
    "type": "function_call_output",
    "call_id": "call_123",
    "output": "{\"temperature\":62,\"conditions\":\"rain\"}"
  }
}
```

```json
{
  "type": "delegation.function_call_output.created",
  "item": {
    "id": "item_function_output_123",
    "type": "function_call_output",
    "call_id": "call_123",
    "output": "{\"temperature\":62,\"conditions\":\"rain\"}"
  }
}
```

The `delegation.function_call_output.created` acknowledgment means the result was accepted, not that the Responses delegation has finished. Keep reading `response.*` events until the lifecycle reaches a terminal event such as `response.completed`, or an error.

## Related content

- [Use GPT-Live for real-time voice](gpt-live.md)
- [GPT-Live event API reference](../gpt-live-reference.md)
