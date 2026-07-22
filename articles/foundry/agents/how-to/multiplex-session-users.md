---
title: "Multiplex multiple users in one hosted agent session"
description: "Serve many users through a Microsoft Foundry hosted agent by pooling them onto shared sessions while keeping each user's data isolated."
author: aahill
ms.author: aahi
ms.reviewer: asultania
ms.manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 06/27/2026
ms.custom: dev-focus
ai-usage: ai-assisted

#CustomerIntent: As a middle-tier developer, I want to serve many users through a bounded pool of hosted agent sessions so that I can scale without one session per user while keeping each user's data isolated.
---

# Multiplex multiple users in one hosted agent session

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

By default, each caller gets their own hosted agent session, as described in [Isolate hosted agent sessions per user](isolate-sessions-per-user.md). Applications that serve many users - a Teams bot, an ISV gateway, or a customer-support platform - don't need one session per user. Instead, a middle-tier service maps many users onto a bounded pool of shared sessions and identifies each user on every call.

This article shows you how to pool sessions across users from your middle tier while keeping each user's data isolated inside a shared session.

The platform isolates conversation state for you, even when users share a session: a response chain that one user creates can't be continued by another user through `previous_response_id`, and `context.get_history()` returns only the history the current request's user is authorized to see. You own two things: the user-to-session mapping in your middle tier, and the partitioning of any data your container stores *itself* (files, rows, or cache) beyond that platform-managed conversation state.

A complete, runnable [session multiplexing sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/responses/session-multiplexing) demonstrates both sides - the middle-tier session pool and the container handler - and this article links its files as you go.

## Prerequisites

- A hosted agent that uses container protocol version 2.0.0. To upgrade, see [Migrate hosted agents](migrate-hosted-agent-preview.md).
- The `Microsoft.CognitiveServices/accounts/AIServices/agents/endpoints/UserIdentityImpersonation/action` permission assigned to your middle-tier service's identity. This permission isn't included in built-in roles; grant it through a custom role — see [Delegate the end-user identity](../concepts/hosted-agent-permissions.md#delegate-the-end-user-identity). Without it, the `x-ms-user-identity` header is rejected with a `403`.
- The Azure AI Projects client library for the middle tier, and the Azure AI AgentServer SDK for the container ([`azure-ai-agentserver-core`](https://pypi.org/project/azure-ai-agentserver-core/) 2.0.0b7+ for Python, or [`Azure.AI.AgentServer.Core`](https://www.nuget.org/packages/Azure.AI.AgentServer.Core) 1.0.0-beta.26+ for .NET).
- A deployed agent to test against. Isolation isn't enforced for local runs.

## Isolate two users in a shared session

Start with the core behavior: two users - call them Alice and Bob, the acted-for users in the sample - can share one `agent_session_id`, and the platform still keeps each user's conversation private. Your middle tier identifies the acted-for user on every call with the `x-ms-user-identity` header (delegation). To continue a user's own conversation, it passes that user's previous response as `previous_response_id`.

The minimal [`invoke_previous_response_isolation.py`](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/bring-your-own/responses/session-multiplexing/scripts/invoke_previous_response_isolation.py) caller in the sample sends exactly that, using the SDK's agent-bound Responses client:

```python
# Agent-bound Responses client from the Foundry SDK.
responses_client = project_client.get_openai_client(agent_name=agent_name).responses

# Target the shared session with agent_session_id, and identify the acted-for
# user with x-ms-user-identity (delegation). Pass previous_response_id to
# continue this user's own chain. Don't send x-agent-user-id; Foundry sets the
# container-side request context after it resolves the user.
kwargs = {
    "input": user_message,
    "stream": False,
    "store": True,
    "extra_body": {"agent_session_id": session_id},
    "extra_headers": {"x-ms-user-identity": user_id},
}
if previous_response_id:
    kwargs["previous_response_id"] = previous_response_id

response = responses_client.create(**kwargs)
```

The platform ties each response chain to the user who created it. If Bob sends Alice's `previous_response_id` while sitting in the same session, the call fails - Bob can't continue Alice's conversation. That guarantee holds without any extra isolation code in your container.

## Scale to many users with a session pool

Isolating two users in one session is the building block. To serve many users, pool them across a bounded set of sessions instead of opening one session per user.

Each session counts against the [regional concurrent-session limits](../concepts/limits-quotas-regions.md) while it actively processes a turn, so one session per user doesn't scale. Because users read, think, and type between turns, your peak concurrent requests are typically a small fraction of your total user count. Size a pool to that peak, then map each user to a session in it and pass that user's identity on every call, exactly as in the previous section.

Decide how to map users to sessions. Common strategies include:

- **Sticky, least-loaded.** A returning user reuses their session; new users go to the least-loaded session. This strategy spreads load evenly and keeps a user's turns together. Grow the pool when sessions reach a per-user cap.
- **Hash-based.** Assign a session with `hash(user_id) % pool_size`. This strategy is simple and stateless, but load can be uneven and resizing the pool reshuffles users.
- **Round-robin.** Distribute requests evenly across the pool. This strategy is simple, but a user's turns can land on different sessions.
- **Group-based.** Route by tenant, team, or region so related users share sessions. This strategy is useful when users in a group share context.

The [`invoke_session_pool.py`](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/bring-your-own/responses/session-multiplexing/scripts/invoke_session_pool.py) caller in the sample implements caller-owned assignment with two strategies, `sticky-fill` and `round-robin`. A returning user always keeps their session; a new user is placed by the selected strategy. The sticky-fill path fills the least-loaded session and opens a new one only when every session is at capacity:

```python
def get_session_for_user(self, user_id: str) -> str:
    if user_id in self.user_to_session:
        return self.user_to_session[user_id]      # returning user is sticky
    session_id = self._next_fill_session()        # new user: place by strategy
    self.user_to_session[user_id] = session_id
    self.session_user_counts[session_id] += 1
    return session_id

def _next_fill_session(self) -> str:
    # Reuse a session with capacity; open a new one only when all are full.
    session_id = next(
        (s for s, count in self.session_user_counts.items()
         if count < self.max_users_per_session),
        None,
    )
    if session_id is None:
        session_id = self._session_name(len(self.session_user_counts))
        self.session_user_counts[session_id] = 0
    return session_id
```

Feed the returned session ID into the same delegated call shown earlier: it becomes `agent_session_id` in `extra_body`, and `x-ms-user-identity` stays the per-user identifier.

## Handle the request in your container

On protocol 2.0.0, the platform resolves the acted-for user and exposes it to your handler through `get_request_context()`. Validate that context (fail closed when it's missing, such as on local runs), then let the platform return the per-user history with `context.get_history()`. The [`main.py`](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/bring-your-own/responses/session-multiplexing/main.py) handler in the sample keeps no conversation state of its own:

```python
from azure.ai.agentserver.core import get_request_context

@app.response_handler
async def handler(request, context, _cancellation_signal):
    ctx = get_request_context()
    if not (ctx.user_id and ctx.call_id):
        # Hosted protocol 2.0.0 populates this context; off-platform it's absent.
        raise ValueError("A user context is required on protocol 2.0.0.")

    user_input = await context.get_input_text() or "Hello!"
    history = await context.get_history()       # platform-authorized for this user
    input_items = _build_input(user_input, history)

    response = _responses_client.create(model=_model, input=input_items, store=False)
    return TextResponse(context, request, text=response.output_text)
```

Because the platform authorizes `context.get_history()` per request, a user in a shared session never receives another user's conversation history.

## Partition per-user data your container stores

The platform isolates conversation history for you. If your container *also* stores its own data - files, database rows, or a cache - that data isn't partitioned automatically. Key it by both the session ID and the user ID so two users in the same session can't see each other's data:

```text
partition = (agent_session_id, user_id)
```

> [!WARNING]
> When users share a session, the platform doesn't partition the data your container stores itself. If your container keys that data by session ID alone, every user in the pool sees the same data. Always include the user ID in the partition key.

Read the user ID from the per-request platform context:

# [Python](#tab/python)

```python
from azure.ai.agentserver.core import get_request_context

def partition_key() -> tuple[str, str]:
    ctx = get_request_context()
    if not ctx or not ctx.user_id:
        raise PermissionError("A user context is required on protocol 2.0.0.")
    return (ctx.session_id, ctx.user_id)   # key all user-owned data by this
```

The platform also injects the user as the `x-agent-user-id` request header. If your runtime doesn't use the SDK context, read this header directly.

The platform populates `get_request_context().user_id` on protocol 2.0.0. Never use the session ID alone for user-owned data when more than one user can enter the session.

# [C#](#tab/csharp)

```csharp
using Azure.AI.AgentServer.Core;

static (string SessionId, string UserId) PartitionKey()
{
    var ctx = FoundryAgentRequestContext.Current;
    if (string.IsNullOrEmpty(ctx.UserId))
    {
        throw new UnauthorizedAccessException(
            "A user context is required on protocol 2.0.0.");
    }
    return (ctx.SessionId!, ctx.UserId!);   // key all user-owned data by this
}
```

The platform populates `FoundryAgentRequestContext.Current.UserId` on protocol 2.0.0. Never use the session ID alone for user-owned data when more than one user can enter the session.

---

For a worked example of per-session storage to build on, see the [note-taking agent sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/responses/notetaking-agent). It keys one file per session under `$HOME`. For a shared session, extend that key with the user ID from the request context so each user gets their own partition.

## Verify isolation

Confirm the guarantee with the sample's A-A-B test, [`invoke_previous_response_isolation.py`](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/bring-your-own/responses/session-multiplexing/scripts/invoke_previous_response_isolation.py). Run it against your deployed agent with two distinct users (the sample defaults to Alice and Bob):

1. As Alice, create a response in a shared session and capture its `id`.
1. As Alice, create a second response in the same session with `previous_response_id` set to the first response's `id`, and capture its `id`.
1. As Bob, in the same session, send a request with `previous_response_id` set to Alice's second response. The call fails - Bob can't continue Alice's chain.

Use two different Entra users or object IDs. Two labels that resolve to the same identity aren't a valid cross-user test.

Sending a legacy isolation header on a protocol 2.0.0 path returns an error, because that model is replaced by the platform user context.

## Related content

- [Isolate hosted agent sessions per user](isolate-sessions-per-user.md) for the default, per-caller isolation model.
- [Session multiplexing sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/responses/session-multiplexing) for the complete middle-tier session pool, container handler, and isolation test.
- [Note-taking agent sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/responses/notetaking-agent) for a container that persists user-owned data per session (Python and C#).
- [Quotas and limits for Foundry Agent Service](../concepts/limits-quotas-regions.md) for regional concurrent-session limits.
- [Migrate hosted agents](migrate-hosted-agent-preview.md) to move a container to protocol 2.0.0.
- [Hosted agent runtime contract](../concepts/hosted-agent-contract.md) for the platform headers and environment variables a container receives.
