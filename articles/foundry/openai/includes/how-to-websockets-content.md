---
title: include file
description: include file
author: alvinashcraft
ms.author: aashcraft
ms.service: microsoft-foundry
ms.topic: include
ms.date: 04/29/2026
ms.custom: include
ai-usage: ai-assisted
---

The Responses API supports a WebSocket mode for long-running, tool-heavy workflows. In WebSocket mode, you keep a persistent connection to `/v1/responses` and continue each turn by sending only new input items together with a `previous_response_id`. This approach reduces per-turn overhead and improves end-to-end latency across long chains.

WebSocket mode works with both Zero Data Retention (ZDR) and `store=false`.

## Prerequisites

- An Azure OpenAI model deployed.
- An authentication method:
  - API key, or
  - Microsoft Entra ID.
- For Python examples:
  - Install the `websocket-client` package.
  - Install `azure-identity` for Microsoft Entra ID authentication.

## When to use WebSocket mode

Use WebSocket mode when a workflow involves many model-tool round trips, such as agentic coding or orchestration loops with repeated tool calls. Because the connection stays open and each turn sends only incremental input, continuation latency is lower than with repeated HTTP requests.

For single-shot requests or short conversations, keep using the standard HTTP Responses API.

## How it works

You open one WebSocket connection to `/v1/responses` and drive it with `response.create` events:

- The first `response.create` starts a new turn. The payload mirrors the HTTP create body, except that transport-specific fields like `stream` and `background` don't apply.
- Follow-up `response.create` messages chain from the prior response using `previous_response_id` and include only new input items.

Server events and ordering match the existing Responses streaming event model.

### Start a turn

Send a `response.create` event on the open socket. The following example connects by using an API key and asks the model a question.

```python
from websocket import create_connection
import json

ws = create_connection(
    f"wss://{YOUR_RESOURCE_NAME}.openai.azure.com/openai/v1/responses",
    header=[f"Authorization: Bearer {YOUR_AOAI_API_KEY}"], # Or your Entra ID token
)

ws.send(json.dumps({
    "type": "response.create",
    "model": "gpt-4.1", # Replace with your model deployment name
    "store": False,
    "input": [
        {
            "type": "message",
            "role": "user",
            "content": [{"type": "input_text", "text": "Find fizz_buzz()"}],
        }
    ],
    "tools": [],
}))
```

> [!TIP]
> You can optionally warm up request state by sending `response.create` with `generate: false`. Use this option when you already know the tools, instructions, or messages you plan to send with an upcoming turn. A warmup doesn't return model output but prepares request state so the next generated turn can start faster. The warmup request returns a response ID that you can chain from by using `previous_response_id`.

### Stream the response

Read events from the WebSocket, print text as it streams in, and stop when the response is done.

```python
while True:
    event = json.loads(ws.recv())

    if event["type"] == "response.output_text.delta":
        print(event["delta"], end="", flush=True)

    elif event["type"] == "response.completed":
        response_id = event.get("response", {}).get("id")
        print(f"\nResponse ID: {response_id}")
        break

# Close the socket only when you are done with all turns.
# ws.close()
```

### Continue with incremental inputs

To continue the same chain, send another `response.create` on the same socket with:

- `previous_response_id` set to the prior response ID.
- `input` containing only new items, such as tool outputs and the next user message.

```python
ws.send(json.dumps({
    "type": "response.create",
    "model": "gpt-4.1",
    "store": False,
    "previous_response_id": f"{response_id}",
    "input": [
        {
            "type": "message",
            "role": "user",
            "content": [{"type": "input_text", "text": "Now optimize it."}],
        },
    ],
    "tools": [],
}))
```

## Continuation semantics

WebSocket mode uses the same `previous_response_id` chaining as HTTP mode, but adds a lower-latency continuation path on the active socket.

On an active WebSocket connection, the service keeps one previous-response state in a connection-local in-memory cache (the most recent response). Continuing from that response is fast because the service reuses connection-local state. Because this state is retained only in memory and isn't written to disk, WebSocket mode is compatible with `store=false` and Zero Data Retention (ZDR).

If a `previous_response_id` isn't in the in-memory cache, behavior depends on whether you store responses:

- With `store=true`, the service might hydrate older response IDs from persisted state. Continuation still works but usually loses the in-memory latency benefit.
- With `store=false` (including ZDR), there's no persisted fallback. If the ID is uncached, the request returns `previous_response_not_found`.

If a turn fails (`4xx` or `5xx`), the service evicts the referenced `previous_response_id` from the connection-local cache. This prevents reusing stale cached state for that failed continuation.

## Compaction

If you use context compaction, there are two different continuation patterns.

### Server-side compaction

When you enable [server-side compaction](../how-to/responses.md?tabs=python-key#server-side-compaction) (`context_management` with `compact_threshold`), compaction happens during normal `/responses` generation. In WebSocket mode, you continue the same way you normally do: send the next `response.create` with the latest `previous_response_id` and only new input items.

### Standalone `/responses/compact`

The standalone [`/responses/compact`](../how-to/responses.md?tabs=python-key#compact-using-items-returned) endpoint returns a new compacted input window, not a response ID. After compaction, start a new response on your WebSocket connection by omitting `previous_response_id` (or setting it to `null`) and passing the compacted output as input, plus the next user or tool items. Pass the compacted output as-is; don't prune the returned window.

```python
# Compact your current window (HTTP call)
compacted = client.responses.compact(
    model="gpt-4.1",
    input=long_input_items_array,
)

# Start a new response on the WebSocket using the compacted window
ws.send(json.dumps({
    "type": "response.create",
    "model": "gpt-4.1",
    "store": False,
    "input": [
        *compacted.output,
        {
            "type": "message",
            "role": "user",
            "content": [{"type": "input_text", "text": "Continue from here."}],
        },
    ],
    "tools": [],
}))
```

## Connection behavior and limits

- A single WebSocket connection can receive multiple `response.create` messages, but it runs them sequentially (one in-flight response at a time).
- The connection doesn't support multiplexing. Use multiple connections if you need parallel runs.
- Connection duration is limited to 60 minutes. Reconnect when you reach the limit.

## Reconnect and recover

When a connection closes or hits the 60-minute limit, open a new WebSocket connection and continue with one of these patterns:

- If your prior response is persisted (`store=true`) and you have a valid response ID, continue with `previous_response_id` and new input items.
- If you can't continue the chain (for example, `store=false`/ZDR or `previous_response_not_found`), start a new response by omitting `previous_response_id` (or setting it to `null`) and send the full input context for the next turn.
- If you compacted context with `/responses/compact`, use the returned compacted window as the base `input` for the new response, then append the latest user or tool items.

## Troubleshooting

- **`previous_response_not_found`**: The referenced response ID isn't in the connection-local cache and there's no persisted state to hydrate from. Start a new chain, or enable `store=true` if your scenario allows it.

    ```json
    {
      "type": "error",
      "status": 400,
      "error": {
        "code": "previous_response_not_found",
        "message": "Previous response with id 'resp_abc' not found.",
        "param": "previous_response_id"
      }
    }
    ```

- **`websocket_connection_limit_reached`**: The connection is open for 60 minutes. Open a new WebSocket connection and continue using one of the [Reconnect and recover](#reconnect-and-recover) patterns.

    ```json
    {
      "type": "error",
      "status": 400,
      "error": {
        "type": "invalid_request_error",
        "code": "websocket_connection_limit_reached",
        "message": "Responses websocket connection limit reached (60 minutes). Create a new websocket connection to continue."
      }
    }
    ```

## Next step

> [!div class="nextstepaction"]
> [Use the Azure OpenAI Responses API](../how-to/responses.md)
