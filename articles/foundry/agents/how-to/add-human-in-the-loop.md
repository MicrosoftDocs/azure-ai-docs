---
title: "Add a human-in-the-loop approval step (preview)"
description: "Pause a long-running hosted agent for human approval or input, then resume the conversation from durable state."
author: aahill
ms.author: aahi
ms.manager: mcleans
ms.date: 09/21/2026
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# Add a human-in-the-loop approval step (preview)

Some agent workflows must stop and wait for a person - to approve an action,
answer a question, or provide missing input - and then continue. A
[long-running hosted agent](../concepts/long-running-agent-resilience.md) can
pause without holding a request open. A multi-turn chain and application state
preserve its place within their configured retention windows.

> [!NOTE]
> Long-running agents are in preview. APIs and package versions are subject to change.

## Prerequisites

- A hosted AgentServer application with `azure-ai-agentserver-core` 2.1.0 or
  later.
- Resilient tasks enabled before host startup.
- An application retention policy for pending approvals. Task chains expire
  after 30 days without a new turn. Foundry State Store items also default to
  30 days, and reads don't renew their retention window.

## How pause-and-resume works

A `@multi_turn_task` chain doesn't end when a turn returns - it moves to the `suspended` state and stays alive under one `task_id`. The next input on the same `task_id` reenters the same handler with `ctx.entry_mode == "resumed"`. That is the natural shape for a human-in-the-loop pause:

1. The agent does work until it needs a human decision.
2. It returns a turn that asks for the decision (the chain suspends).
3. A person replies; your app starts a new turn on the same `task_id`.
4. The handler resumes and continues with the human's answer.

The wait can survive container restarts. It remains bounded by the task,
session, and application-state retention settings that apply to your agent.

## Implement the approval turn

```python
from azure.ai.agentserver.core.storage import FoundryStateStore
from azure.ai.agentserver.core.tasks import (
    TaskContext,
    multi_turn_task,
    set_resilient_tasks_enabled,
)

APPROVAL_TTL_SECONDS = 30 * 24 * 60 * 60
set_resilient_tasks_enabled(True)


async def open_approval_store(task_id: str) -> FoundryStateStore:
    return await FoundryStateStore.get_or_create(
        f"expense-approval/{task_id}",
        item_ttl_seconds=APPROVAL_TTL_SECONDS,
    )


async def save_expense(task_id: str, expense_id: str, summary: str) -> None:
    store = await open_approval_store(task_id)
    async with store:
        await store.set_item(
            "expense",
            {"expense_id": expense_id, "summary": summary},
        )


async def load_expense(task_id: str) -> dict | None:
    store = await open_approval_store(task_id)
    async with store:
        item = await store.get_item("expense")
    return None if item is None else dict(item.value)


async def delete_approval_state(task_id: str) -> None:
    store = await open_approval_store(task_id)
    async with store:
        await store.delete()


@multi_turn_task(name="expense-approval")
async def approve(ctx: TaskContext[dict]) -> dict:
    kind = ctx.input.get("kind")

    if kind == "decision":
        saved = await load_expense(ctx.task_id)
        if saved is None:
            raise RuntimeError("The approval state expired or is missing.")

        decision = ctx.input.get("decision")
        if decision == "approved":
            operation_id = f"{ctx.task_id}:{ctx.input_id}:submit"
            await submit_expense(
                saved["expense_id"],
                idempotency_key=operation_id,
            )
            return {"status": "submitted"}
        if decision == "rejected":
            return {"status": "rejected"}
        raise ValueError("decision must be 'approved' or 'rejected'.")

    if kind != "request":
        raise ValueError("kind must be 'request' or 'decision'.")

    saved = await load_expense(ctx.task_id)
    if saved is None:
        expense = await build_expense(ctx.input)
        saved = {"expense_id": expense.id, "summary": expense.summary}
        await save_expense(ctx.task_id, expense.id, expense.summary)

    return {"status": "awaiting_approval", "summary": saved["summary"]}
```

The input's `kind` selects the business operation. Don't use
`ctx.entry_mode` for that decision: either the request turn or the approval
turn can be reentered with `entry_mode == "recovered"`. The sample reuses saved
preparation state and gives submission a stable idempotency key for the same
input attempt.

Drive it from your application:

```python
# Turn 1 - agent produces an approval request, then the chain suspends.
r1 = await approve.run(
    task_id="exp-42",
    input={"kind": "request", "amount": 1200, "category": "travel"},
)
# ... show r1["summary"] to a human and wait for their reply (could be much later) ...

# Turn 2 - same task_id resumes the suspended chain.
r2 = await approve.run(
    task_id="exp-42",
    input={"kind": "decision", "decision": "approved"},
)
```

> [!TIP]
> Store pause-and-resume state in Foundry State Store, your database, or a
> framework checkpoint. Don't rely on local variables from the previous turn.
> See [Manage state for long-running agents](manage-task-state.md).

## Use a framework interrupt with Responses

If you build on an agent framework (for example, LangGraph or Microsoft Agent Framework) over a background response, use the framework's own interrupt and approval mechanism. Keep the response resilient so the pause survives a restart. Set `resilient_background=True` and persist the framework's checkpoint at the interrupt point. On resume, rebuild from that checkpoint. See [Recover long-running work after a crash](recover-long-running-work.md).

## Clean up a finished chain

Delete both the task chain and its application-owned state when the approval
finishes or expires. Deleting the chain doesn't delete the separate State Store.

```python
await approve.delete("exp-42")
await delete_approval_state("exp-42")
```

## Related content

- [Resilience for long-running hosted agents](../concepts/long-running-agent-resilience.md)
- [Long-running agent API reference](../concepts/long-running-agent-reference.md)
- [Steer an in-flight agent turn](steer-hosted-agent.md)
- [Manage state for long-running agents](manage-task-state.md)
- [Recover long-running work after a crash](recover-long-running-work.md)
