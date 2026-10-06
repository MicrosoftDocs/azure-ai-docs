---
title: "Cancel a hosted agent turn (preview)"
description: "Cancel an in-flight turn on a long-running hosted agent, understand how cancellation differs between the Responses and Invocations protocols, and how it differs from stopping a session."
author: aahill
ms.author: aahi
ms.manager: mcleans
ms.date: 09/02/2026
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# Cancel a hosted agent turn (preview)

Cancel is a route on the agent itself - `/responses/{response_id}/cancel` or `/invocations/{invocation_id}/cancel` - scoped to one specific in-flight turn. It's different from [steering](steer-hosted-agent.md), which redirects a turn by queuing a replacement, and different from [stopping a session](manage-hosted-sessions.md#stop-a-session), which is a session-management API, not a per-turn one - see [How stopping a session affects an in-flight turn](manage-hosted-sessions.md#how-stopping-a-session-affects-an-in-flight-turn) for the side effect stopping a session has on any work in flight.

> [!NOTE]
> Long-running agents are in preview. APIs and package versions can change.

## Cancel in the Responses protocol

The framework exposes a built-in cancel endpoint - you don't implement it yourself:

```bash
POST {endpoint}/responses/{response_id}/cancel
```

Calling it only works on a response created with `background=true`; calling it on a synchronous response returns an error. It sets the same cooperative cancel signal your handler already observes as its third positional parameter, and stamps `context.client_cancelled = True` so the handler can tell a genuine cancel apart from steering pressure:

```python
@app.response_handler
async def handler(request, context, cancellation_signal):
    while not cancellation_signal.is_set():
        ...
    if context.client_cancelled:
        # Explicit /cancel call. Distinguish from steering pressure, which
        # sets cancellation_signal without this flag.
        return
    # A newer turn is queued (steering) - wind down and return partial
    # output instead, per the steering pattern.
```

For a multi-turn conversation, canceling a turn doesn't end the conversation - the underlying chain stays alive and resumable for the next turn (see [What happens at the task-store level](#what-happens-at-the-task-store-level)).

## Cancel in the Invocations protocol

The Invocations protocol registers the `/invocations/{invocation_id}/cancel` route for you, but doesn't wire it to anything automatically - the framework has no built-in disconnect monitoring or automatic cancellation for this protocol. Without a registered handler, calling it returns `404 not_found`.

If you're using the task primitives (`@task` / `@multi_turn_task`) directly, the way to actually end an in-flight or suspended multi-turn chain is `delete()`, called on the decorated function itself:

```python
@multi_turn_task(name="conv", steerable=True)
async def conv(ctx: TaskContext[dict]) -> dict:
    ...

@app.cancel_invocation_handler
async def cancel_invocation(request):
    invocation_id = request.path_params["invocation_id"]
    await conv.delete(invocation_id)
    return Response(status_code=202)
```

> [!IMPORTANT]
> `delete()` always removes the chain's persisted record, for a running turn or a suspended one waiting on its next turn. This behavior is a real difference from the Responses protocol's `/cancel`: Responses cancels the current turn but keeps the conversation resumable; `delete()` ends the conversation - there's no next turn to resume. There's no built-in "cancel this turn only, keep the chain alive" primitive for direct task-primitive use; if you need that, build it as an app-level convention (for example, a flag in your own task state that the handler checks and reacts to by returning normally, leaving the chain in its usual `suspended` state).
>
> One-shot tasks (`@task`) have no equivalent method - they're always deleted automatically on their own completion, failure, or cancellation, so there's nothing separate to call.

## What happens at the task-store level

The outcome depends on which mechanism ends the turn. The two protocols don't always produce the same result:

| Task shape | Effect |
| --- | --- |
| One-shot (`@task`) | The system deletes the persisted record. This outcome matches any other terminal result for a one-shot task. |
| Multi-turn (`@multi_turn_task`) via the Responses protocol's built-in `/cancel` | The chain transitions to `suspended`, exactly like a normal `return` from the handler ends a turn. The chain stays alive; a turn that was queued behind the canceled one is promoted and runs next. |
| Multi-turn (`@multi_turn_task`) via `delete()` | The system removes the persisted record outright. The chain isn't resumable afterward. |

## How this process differs from stopping a session

Cancel is an agent-level route scoped to one turn. [Stopping a session](manage-hosted-sessions.md#stop-a-session) is a session-management API that tears down the whole container. It has no `response_id` or `invocation_id` and isn't part of the cancellation contract described on this page. Because it ends the container rather than targeting a turn, it still affects any turn that happens to be running. To learn more, see [How stopping a session affects an in-flight turn](manage-hosted-sessions.md#how-stopping-a-session-affects-an-in-flight-turn).

## Related content

- [Steer an in-flight agent turn](steer-hosted-agent.md)
- [Recover long-running work after a crash](recover-long-running-work.md)
- [Manage hosted agent sessions](manage-hosted-sessions.md)
- [Resilience for long-running hosted agents](../concepts/long-running-agent-resilience.md)
