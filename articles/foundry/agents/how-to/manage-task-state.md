---
title: "Manage state for long-running agents (preview)"
description: "Keep durable progress for a hosted agent using small task metadata as a checkpoint index and the Foundry state store for bulk checkpoints and framework recovery."
author: aahill
ms.author: aahi
ms.manager: mcleans
ms.date: 08/05/2026
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# Manage state for long-running agents (preview)

A [long-running hosted agent](../concepts/long-running-agent-resilience.md) recovers from crashes only if its progress is durable. This article shows the two layers of durable state - small task metadata as a checkpoint *index*, and the Foundry state store as a checkpoint *store* - and how to back a framework checkpointer so framework-level recovery survives restarts.

> [!NOTE]
> Long-running agents are in preview. APIs and package versions are subject to change.

## Two layers of state

| Layer | What it holds | Where |
| --- | --- | --- |
| Task metadata | Small references and watermarks: an upstream session ID, a last-processed input ID, a step number, an idempotency key. | `ctx.metadata` / `context.conversation_chain_metadata` |
| Durable state store | Bulk state: framework checkpoints, conversation history, generated artifacts, intermediate work. | `FoundryStateStore` (or your own database / blob storage) |

The rule: **metadata is a checkpoint index, not a checkpoint store.** Small writes are cheap and fast; bulk writes hit task-store payload limits and slow recovery.

## Use task metadata for watermarks

`ctx.metadata` is a small key-value namespace that survives crashes and is visible across turns of a chain. Values must be JSON-serializable.

```python
@multi_turn_task(name="workflow")
async def run(ctx: TaskContext[dict]) -> dict:
    step = int(ctx.metadata.get("workflow_step", 0))
    for i in range(step, total_steps):
        await upstream_store.write_step_result(i, result)   # bulk data goes to your store
        ctx.metadata["workflow_step"] = i + 1
        await ctx.metadata.flush()                          # explicit fence before the next side effect
    return {"done": True}
```

Persistence isn't implicit. Call `flush()` when the metadata write must land *before* a side effect that can't be deduplicated. Names beginning with `_` are reserved for the framework and raise `ValueError`.

Three useful scopes:

| Scope | Purpose |
| --- | --- |
| Conversation-chain metadata | Cross-turn references and watermarks later turns need. |
| Per-turn / internal metadata | State needed only to reconstruct the current response after a crash. |
| Client-visible response metadata | Metadata that is part of the public response contract. |

## Store bulk state in the Foundry state store

`FoundryStateStore` is a durable, server-backed key-value store for state that must survive crashes and idle-eviction. A store is bound to one caller-chosen name; encode your scope (session, thread, or run) into that name.

```python
from azure.ai.agentserver.core.storage import FoundryStateStore

store = await FoundryStateStore.get_or_create(
    "checkpoints/thread-abc",   # store name == scope
    user_isolation=True,        # partition items per end user when the name is shared
    item_ttl_seconds=3600,      # idle items age out (store-level; renewed on write)
    description="Checkpoints for thread abc",
)
async with store:
    await store.set_item("step-1", {"done": False})
    item = await store.get_item("step-1")
```

Key behaviors:

- **`get_or_create()`** fetches or creates the store in one call; it applies `user_isolation` / `item_ttl_seconds` only on first creation.
- **Store name = scope.** Names can contain `/`; use it as a hierarchy separator and choose a stable scheme up front.
- **Optimistic concurrency.** Use `if_match=item.etag` for mutable items like counters; skip it on append-only checkpoints. A failed precondition raises `FoundryStoragePreconditionError`.
- **Limits.** Item value ≤ 1 MB serialized; store name 1–128 chars; up to 16 tags per item.

## Back a framework checkpointer

Point a LangGraph or Microsoft Agent Framework (MAF) checkpointer at `FoundryStateStore` and the framework's own recovery becomes durable across crashes - no custom recovery code.

| Framework concept | FoundryStateStore |
| --- | --- |
| Thread / scope | Store name (encode the ID into it) |
| Checkpoint ID | Item key |
| Serialized checkpoint | Item value (JSON `dict`) |
| "latest" / history / filtering | Tags + `list_keys(order="desc")` |
| Per-user safety | `user_isolation=True` |

Checkpoints are append-only - each save uses a fresh ID, so there's no write contention and you never need `if_match` on the checkpoint path.

```python
# LangGraph: one thread = one store
async def _store(thread_id: str) -> FoundryStateStore:
    return await FoundryStateStore.get_or_create(
        f"langGraphCheckpoints/{thread_id}", user_isolation=True
    )
```

> [!WARNING]
> For the MAF adapter, always set `user_isolation=True`. MAF's only grouping is `workflow_name` - a definition name shared across users - so without user isolation, `get_latest` / `list_checkpoints` would return other callers' checkpoints.

## Keep inputs small

Task inputs are persisted before the handler runs (that's what recovery rests on), so keep them small - the per-input limit is about 10 MiB after JSON serialization, and larger inputs raise `InputTooLarge` before any network call. Externalize big payloads to blob storage and pass a reference.

## Related content

- [Resilience for long-running hosted agents](../concepts/long-running-agent-resilience.md#preserve-agent-progress)
- [Long-running agent API reference](../concepts/long-running-agent-reference.md)
- [Recover long-running work after a crash](recover-long-running-work.md)
- [Add a human-in-the-loop approval step](add-human-in-the-loop.md)
