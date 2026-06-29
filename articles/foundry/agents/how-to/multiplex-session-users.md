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

This article shows you how to pool sessions across users from your middle tier, and how to keep each user's data isolated inside a shared session. You own two things: the user-to-session mapping in your middle tier, and per-user data partitioning inside your container. The platform doesn't fence delegated users from each other in a shared session, so isolation depends on your code: pass each user's `x-ms-user-identity` and key your stored data by it.

## Prerequisites

- A hosted agent that uses container protocol version 2.0.0. To upgrade, see [Migrate hosted agents to the refreshed public preview](migrate-hosted-agent-preview.md).
- The `Microsoft.CognitiveServices/accounts/AIServices/agents/endpoints/UserIdentityImpersonation/action` permission assigned to your middle-tier service's identity. Without it, the `x-ms-user-identity` header is rejected with a `403`.
- The Azure AI Projects client library for the middle tier, and the Azure AI AgentServer SDK for the container ([`azure-ai-agentserver-core`](https://pypi.org/project/azure-ai-agentserver-core/) 2.0.0b7+ for Python, or [`Azure.AI.AgentServer.Core`](https://www.nuget.org/packages/Azure.AI.AgentServer.Core) 1.0.0-beta.26+ for .NET).
- A deployed agent to test against. Isolation isn't enforced for local runs.

## Why multiplex sessions

Each session counts against the [regional concurrent-session limits](../concepts/limits-quotas-regions.md) while it actively processes a turn. If you create one session per user, a large user base can require more concurrent sessions than a region allows.

Multiplexing decouples the number of users you serve from the number of sessions you run. Because users read, think, and type between turns, your peak concurrent requests are typically a small fraction of your total user count. You serve all your users through a bounded pool of sessions sized to that peak, and you identify each user on every request so their data stays isolated.

You own two responsibilities:

- **In your middle tier:** map each user to a session in the pool, and pass that user's identity on every call.
- **In your container:** partition any data you store by the user, so users who share a session can't see each other's data.

When delegation is in effect, the platform doesn't enforce single-user ownership of a session, so your middle tier is free to place multiple users on one session.

## Choose a routing strategy

Decide how to map users to sessions. Common strategies include:

- **Sticky, least-loaded.** A returning user reuses their session; new users go to the least-loaded session. This strategy spreads load evenly and keeps a user's turns together. Grow the pool when sessions reach a per-user cap.
- **Hash-based.** Assign a session with `hash(user_id) % pool_size`. This strategy is simple and stateless, but load can be uneven and resizing the pool reshuffles users.
- **Round-robin.** Distribute requests evenly across the pool. This strategy is simple, but a user's turns can land on different sessions.
- **Group-based.** Route by tenant, team, or region so related users share sessions. This strategy is useful when users in a group share context.

Pick the strategy that fits your latency, statefulness, and scaling needs. The example in this article uses a sticky, least-loaded approach.

## Example: route users through a session pool

The following shows one way to route users and identify them on each call. It's an illustration of the pattern, not the only approach - use the routing strategy that fits your application.

```python
# Route the user to a session with your own pool policy, then identify the
# user on the call. Here, get_session_for_user applies a sticky, least-loaded
# policy and grows the pool when sessions reach a per-user cap.
session_id = pool.get_session_for_user(user_id)
response = agent.create_response(
    input=user_message,
    session_id=session_id,
    headers={"x-ms-user-identity": user_id},   # requires delegation
)
```

The `x-ms-user-identity` header keeps each user individually identified while sharing a session, so the platform scopes their data and telemetry to them.

## Partition per-user data inside your container

Pooling keeps users individually identified, but your container still stores data inside one shared session. Partition any user-owned data by both the session ID and the user ID so two users in the same session can't see each other's data:

```text
partition = (agent_session_id, user_id)
```

> [!WARNING]
> When users share a session, the platform doesn't isolate their data for you. If your container keys data by session ID alone, every user in the pool sees the same data. Always include the user ID in the partition key.

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

Confirm that two users in the same session can't see each other's data:

1. Invoke the agent in one session as user A, and have the agent store a fact.
1. Invoke the agent in the same session as user B, and have the agent store a different fact.
1. Read the stored fact back as each user, and confirm each user sees only their own fact.

Sending a legacy isolation header on a protocol 2.0.0 path returns an error, because that model is replaced by the platform user context.

## Related content

- [Isolate hosted agent sessions per user](isolate-sessions-per-user.md) for the default, per-caller isolation model.
- [Note-taking agent sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/responses/notetaking-agent) for a container that persists user-owned data per session (Python and C#).
- [Quotas and limits for Foundry Agent Service](../concepts/limits-quotas-regions.md) for regional concurrent-session limits.
- [Migrate hosted agents to the refreshed public preview](migrate-hosted-agent-preview.md) to move a container to protocol 2.0.0.
- [Hosted agent runtime contract](../concepts/hosted-agent-contract.md) for the platform headers and environment variables a container receives.
