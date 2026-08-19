---
title: "Resilience for long-running Microsoft Foundry hosted agents (preview)"
description: "Understand how Microsoft Foundry hosted agents preserve long-running work, recover after process interruptions, and replay streamed results."
author: aahill
ms.author: aahi
ms.manager: mcleans
ms.reviewer: glennc
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: concept-article
ms.date: 07/30/2026
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# Resilience for long-running Microsoft Foundry hosted agents (preview)

Long-running hosted agents can keep working after the request that started them disconnects. They can also recover after their hosting process stops unexpectedly. Foundry Agent Service and the AgentServer SDKs provide durable work identity, persisted inputs, lease-based recovery, and stream replay. Your agent is still responsible for preserving meaningful progress and preventing duplicate side effects.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

## Background execution and resilience

Background execution and resilience solve different problems. Background execution lets work continue without keeping the original HTTP connection open. Resilience lets a later process lifetime recover work after a restart, crash, out-of-memory termination, or redeployment.

| Capability | What it provides | What it doesn't provide |
| --- | --- | --- |
| Background execution | Asynchronous work that clients can poll or reconnect to. | Recovery after the process that owns the work stops. |
| Resilient execution | Durable work identity, persisted input, process-loss detection, and handler reentry. | Automatic preservation of every intermediate application state or side effect. |
| Stream replay | Retained events that reconnecting clients can receive from a cursor. | A checkpoint of the agent's internal workflow state. |

For the Responses protocol, full crash recovery applies only to stored background responses when the server opts in to resilient background execution. Foreground responses remain tied to the client connection and aren't reinvoked after a process interruption.

For the Invocations protocol, your application defines the request, response, and status contract. Use the AgentServer resilient task primitive to preserve execution, and expose the polling or streaming behavior that your clients need.

## Resilient work model

A resilient unit of work has two identities:

- A **work identity** names the logical job or multi-turn conversation.
- An **input identity** names one input or turn within that work.

Before a handler starts, the runtime persists its input and acquires a lease on the work record. While the handler runs, the runtime renews the lease. If the process stops and abandons the lease, a later process can reclaim the record and invoke the registered handler with the same identities and input.

:::image type="content" source="../media/long-running-agent-resilience/resilient-work-recovery.png" alt-text="Diagram that shows a handler acquiring a lease on a work record, the hosting process stopping, and a later process reclaiming the lease and reentering the handler with the same work and input identities." lightbox="../media/long-running-agent-resilience/resilient-work-recovery.png":::

Recovery reenters the handler from its beginning. It isn't deterministic replay, and it doesn't restore local variables or an in-memory call stack. The handler uses durable checkpoints or watermarks to determine which work is already complete.

Recovery also differs from retry. A retry handles a failure reported by the running handler and can consume retry budget. Recovery continues the same durable attempt after its process disappears.

## Work shapes

Choose a work shape based on the lifetime and concurrency of the operation.

| Shape | Use when | Lifecycle |
| --- | --- | --- |
| One-shot resilient work | One operation must survive a process interruption. | One input produces one result, and the work can be removed after it reaches a terminal state. |
| Multi-turn chain | A conversation or agent session accepts multiple inputs over time. | One work identity remains active across turns until the application deletes it or its retention period expires. |

Calls that use the same one-shot work identity converge on the same logical operation instead of executing duplicate work. A multi-turn chain accepts turns sequentially. *Steering* is an optional mode that lets a newer turn queue behind the active turn and signal the current handler to finish early, so a conversation can redirect without starting a second concurrent handler.

## Platform and application responsibilities

The runtime preserves execution metadata. Your application preserves domain progress.

| Foundry and the AgentServer SDK provide | Your agent provides |
| --- | --- |
| Durable work and input identities. | Stable identifiers that map to your job or conversation model. |
| Input persistence before handler execution. | Inputs that fit the task payload limit, with large data stored externally. |
| Lease-based process-loss detection and handler reentry. | A safe rerun path or a recovery branch that resumes from durable progress. |
| Small durable metadata values. | Checkpoint references, idempotency keys, and side-effect watermarks. |
| Conversation locking and optional steering queues. | User-visible behavior for queued, rejected, interrupted, and canceled turns. |
| Event retention and cursor-based replay. | Per-turn stream identities and reconnect-aware clients. |
| Cleanup of terminal or expired runtime records. | Cleanup of external checkpoints, sessions, and application data. |

## Preserve agent progress

Keep task metadata small. Use it as a checkpoint index, not as a checkpoint store.

Good metadata values include:

- An upstream framework session or checkpoint ID.
- The last completed workflow phase.
- An idempotency key for an external operation.
- A pointer to state in a database or blob store.

Keep conversation history, model output, tool results, and large intermediate artifacts in an agent framework checkpointer or application-owned storage.

Choose one of these recovery strategies based on where progress lives:

| Strategy | Where progress lives | Recovery behavior |
| --- | --- | --- |
| Safe rerun | The operation is inexpensive and repeatable. | Run the handler again from the beginning. |
| Response checkpoints | Persisted response snapshots mark completed phases. | Restore the latest snapshot and continue after its completed output items. |
| Upstream-owned resume | An agent framework or application store owns checkpoints. | Resume the upstream session or workflow from its latest durable state. |

Any strategy can use a side-effect watermark. Persist the watermark before an operation that can't be safely repeated, and clear it after the operation commits. A recovered handler checks the watermark before it issues the operation again.

## Replay streamed output

Use a separate stream identity for each request or turn. Don't reuse a multi-turn work identity as the stream identity because a completed stream closes while the conversation can continue with later turns.

Replayable streams retain events and assign cursors that clients use when they reconnect. A persistent replay backing also lets a recovered producer find its last emitted cursor and continue with the next event.

For a recovered Responses stream, a later `response.in_progress` event is a snapshot reset. A client replaces its locally accumulated output with the snapshot in that event, discards partial output that isn't in the snapshot, and then applies subsequent events. Output indexes identify slots in the current snapshot; they aren't guaranteed to increase across recovery attempts.

## Handle cancellation and shutdown

Cancellation and shutdown are cooperative. The runtime signals the handler, and the handler decides whether to return a partial result, finish normally, cancel, or defer unfinished work for recovery.

Treat graceful shutdown differently from failure. If the handler can't finish during the shutdown window, defer the work without writing a terminal state. A later process can then reclaim and reenter it.

When steering is enabled, queued input can also signal the current turn to wind down. The conversation remains sequential: steering doesn't create a fork or let two turns modify the same conversation concurrently.

## Design boundaries

Resilient tasks don't provide deterministic replay, workflow orchestration, or bulk storage. They compose with these systems instead.

- Use an agent framework checkpointer for graph state and human-in-the-loop suspension.
- Use a workflow engine for fan-out, fan-in, durable timers, or child workflows.
- Use application storage for large inputs, generated artifacts, and external state.
- Use idempotency support from downstream services whenever it's available.

Design each handler so that process loss at any point leads to one of two outcomes: the operation safely runs again, or durable state identifies the exact boundary from which it resumes.

## Related content

- [Hosted agents in Foundry Agent Service](hosted-agents.md)
- [Hosted agent runtime contract](hosted-agent-contract.md)
- [Add a protocol adapter to your hosted agent](../how-to/add-protocol-adapter.md)
- [Bring-your-own hosted agent samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples)