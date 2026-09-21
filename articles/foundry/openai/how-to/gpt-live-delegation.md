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


When a GPT-Live conversation needs search, deeper reasoning, or another action that the live model can't complete on its own, it delegates that work while the live interaction continues. GPT-Live supports two delegation modes, configured in the `delegation` field of [session configuration](gpt-live.md#session-configuration).

| Mode | Description |
|---|---|
| **Client delegation** | GPT-Live hands work to your application. Your client or backend performs the work and returns the result as context. This option is the most flexible, but it requires more upfront integration. |
| **Responses delegation** | GPT-Live routes the request to a configured [Responses API](responses.md) deployment. Hosted tools run server-side (this incurs normal charges for Responses API usage). Client-actionable function calls are returned to your application for completion. |

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

With client delegation, `session.delegation.created` identifies a unit of work with `target: "client"` and a delegation `id`. The delegation object carries metadata, not the task text, so use transcript events and your application state to work out what the user wants. Save the `id` to correlate your result.

```json
{
  "type": "session.delegation.created",
  "event_id": "event_delegation",
  "offset_ms": 1000,
  "delegation": {
    "id": "item_delegation_123",
    "type": "delegation",
    "target": "client"
  }
}
```

Return the result with `session.commentary.append` for content the model should say aloud, or `session.thinking.append` for quiet context. Set `delegation_id` to the delegation `id`. Each event takes a plain-string `content` of up to 500 tokens.

```json
{
  "type": "session.commentary.append",
  "event_id": "event_result_1",
  "delegation_id": "item_delegation_123",
  "content": "It is 62 degrees and raining in Seattle."
}
```

```json
{
  "type": "session.commentary.appended",
  "client_event_id": "event_result_1",
  "start_ms": 1200,
  "end_ms": 1600
}
```

Repeated appends can continue the same client delegation. The acknowledgment arrives after estimated context injection; it doesn't prove that the model consumed or spoke the result, or that an external action succeeded.

## Handle Responses delegation

By using Responses delegation, `session.delegation.created` identifies the delegation with `target: "responses"` and a `response_id` that binds it to the Responses lifecycle. GPT-Live manages the backend call; don't send a standalone Responses request into the GPT-Live event stream.

```json
{
  "type": "session.delegation.created",
  "event_id": "event_delegation",
  "offset_ms": 1000,
  "delegation": {
    "id": "item_delegation_456",
    "type": "delegation",
    "target": "responses",
    "response_id": "resp_123"
  }
}
```

Subsequent Responses events arrive inside a `response.event` envelope. Dispatch on the nested `event.type` and preserve the outer `delegation_id`. Don't treat top-level `response.*` values as unwrapped Responses events.

```json
{
  "type": "response.event",
  "event_id": "event_response_1",
  "delegation_id": "item_delegation_456",
  "event": {
    "type": "response.output_text.delta",
    "item_id": "msg_123",
    "delta": "The forecast is"
  }
}
```

Delegated output text is also injected into the live session, so it can surface as normal transcript and audio output. Live speech and delegated work continue independently: a completed backend response doesn't mean the user heard the answer.

### Complete a client-actionable function call

Read completed function calls from the nested `response.output_item.done` event inside a `response.event` envelope. The finished item contains `call_id`, `name`, and `arguments`.

```json
{
  "type": "response.event",
  "delegation_id": "item_delegation_456",
  "event": {
    "type": "response.output_item.done",
    "item": {
      "type": "function_call",
      "call_id": "call_123",
      "name": "get_weather",
      "arguments": "{\"location\":\"Seattle\"}"
    }
  }
}
```

Run your authorized handler, then submit the result as a Responses item with `response.item.create`.

```json
{
  "type": "response.item.create",
  "event_id": "event_function_output_1",
  "item": {
    "type": "function_call_output",
    "call_id": "call_123",
    "output": "{\"temperature\":62,\"conditions\":\"rain\"}"
  }
}
```

Submit every required result for the pending tool calls, then explicitly continue the backend response with `response.create`. Parallel calls require one result per call.

```json
{
  "type": "response.create",
  "event_id": "event_continue_1"
}
```

Appending a function result doesn't automatically continue the response, and it has no standalone success acknowledgment. Keep reading `response.event` envelopes until the nested lifecycle reaches a terminal event such as `response.completed`, or an error.

## Related content

- [Use GPT-Live for real-time voice](gpt-live.md)
- [GPT-Live event API reference](../gpt-live-reference.md)
