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
ms.date: 09/20/2026
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# Resilience for long-running Microsoft Foundry hosted agents (preview)

Long-running hosted agents can keep working after the request that started them disconnects. They can also recover after their hosting process stops unexpectedly. Foundry Agent Service and the AgentServer SDKs provide durable work identity, persisted inputs, lease-based recovery, and stream replay. Your agent is still responsible for preserving meaningful progress and preventing duplicate side effects.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

## Start with the recovery guarantee

For a stored background response with resilience enabled, Foundry preserves the
logical work and invokes your handler again when the process that owned the work
disappears. The recovered handler receives the persisted input and the same
logical work identity.

The guarantee is **at-least-once handler execution with recovery from a durable
boundary**. The runtime doesn't restore process memory, the call stack, local
variables, or an external operation that completed without a durable record.

| Event | What Foundry guarantees | What your application must handle |
| --- | --- | --- |
| The initiating client disconnects. | Stored background work continues, and the client can poll or reconnect by using the response ID. | Retain the response ID or stream cursor. |
| The hosting process stops. | After the lease expires, another process can reclaim the same work and reenter the handler with the persisted input. | Restore application progress from a checkpoint or safely rerun the unfinished step. |
| The process stops inside a step. | The last durable response and task metadata remain available. | Expect the unconfirmed step to run again. |
| An external operation commits before the next checkpoint. | Foundry recovers the agent work, but it doesn't roll back or deduplicate the external operation. | Use a stable idempotency key or reconcile the operation before retrying it. |

For the Responses protocol, this guarantee applies when all three conditions are
true:

- The request sets `store=true`.
- The request sets `background=true`.
- The server sets `resilient_background=True`.

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

```mermaid
sequenceDiagram
    participant Client
    participant Runtime as Foundry and AgentServer
    participant P1 as Agent process 1
    participant State as Durable application state
    participant P2 as Agent process 2

    Client->>Runtime: Start stored background response
    Runtime->>Runtime: Persist work identity and input
    Runtime->>P1: Acquire lease and invoke handler
    P1->>State: Save completed-step checkpoint
    P1->>Runtime: Checkpoint response snapshot
    Note over P1: Process stops unexpectedly
    Runtime->>Runtime: Detect expired lease
    Runtime->>P2: Reclaim work and reenter handler
    P2->>State: Load application checkpoint
    P2->>Runtime: Continue response
    Client->>Runtime: Poll or reconnect with response ID
    Runtime-->>Client: Replay stored output and continue
```

Recovery reenters the handler from its beginning. It isn't deterministic replay, and it doesn't restore local variables or an in-memory call stack. The handler uses durable checkpoints or watermarks to determine which work is already complete.

Recovery also differs from retry. A retry handles a failure reported by the running handler and can consume retry budget. Recovery continues the same durable attempt after its process disappears.

## Understand what state survives

Resilience uses several durable records. They have different owners and
lifetimes.

| State | What it contains | What happens after process loss |
| --- | --- | --- |
| Runtime task record | Work ID, input ID, serialized input, execution status, lease and recovery bookkeeping, and small task metadata. | AgentServer uses it to detect unfinished work and reenter the handler. The record isn't an application checkpoint. |
| Stored response | Response ID and status, the last checkpointed response snapshot, conversation-chain metadata, and retained stream events and cursors. | A recovered Responses handler can restore the snapshot. A reconnecting client can replay retained output. |
| Session filesystem | Files under `$HOME` and files uploaded through `/files`, scoped to one agent session. | Foundry restores the files when the same session resumes, including on newly provisioned compute. Other sessions can't access them. |
| Application or framework checkpoint | Workflow state, completed-step results, tool state, or a reference to larger data in Foundry State Store or another durable store. | Your handler or framework loads the checkpoint and selects the next step. Foundry doesn't create this checkpoint automatically. |
| Process-local state | Memory, local variables, call stack, open handles, unflushed buffers, and files outside the session-persisted filesystem. | The state is lost. Reconstruct it when the handler is reentered. |

`$HOME` is persistent **per session**, not per agent. Processes running in the
same session sandbox can access the same files. A different session receives a
different filesystem. Foundry deletes a session after 30 days of inactivity.
Use [session storage](hosted-agents.md#session-storage) for session-scoped files
and [Foundry State Store](agent-state-store.md) for JSON state that must persist
independently of session compute or support explicit user isolation.

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

Task metadata is a small recovery index. Updating it doesn't save the handler's
local variables or commit the external work that the metadata describes. Write
the application checkpoint or external result first, then advance the metadata
that points to it.

Choose one of these recovery strategies based on where progress lives:

| Strategy | Where progress lives | Recovery behavior |
| --- | --- | --- |
| Safe rerun | The operation is inexpensive and repeatable. | Run the handler again from the beginning. |
| Response checkpoints | Persisted response snapshots mark completed phases. | Restore the latest snapshot and continue after its completed output items. |
| Upstream-owned resume | An agent framework or application store owns checkpoints. | Resume the upstream session or workflow from its latest durable state. |

Any strategy can carry a stable operation ID for an external side effect. A
recovered handler uses that ID to retry through a downstream idempotency API or
to query whether the operation already committed.

## Walk through a crash at a side-effect boundary

The following example shows why checkpointing and idempotency are separate
requirements.

| Phase | Durable evidence | Recovery behavior |
| --- | --- | --- |
| The handler starts a `publish-report` step. | It derives an operation ID from the work ID and step name, then stores that ID with the checkpoint. | A recovered handler derives the same operation ID. |
| The publishing service accepts the report. | The downstream service records the operation ID with its result. | Repeating the request with the same operation ID returns the stored result. |
| The agent process stops before advancing its checkpoint. | The runtime task remains unfinished, and the application checkpoint still points to `publish-report`. | Foundry reenters the handler, which might issue the step again. |
| The recovered handler retries the operation. | The downstream service recognizes the operation ID. | The report is published once, and the handler records the returned result before advancing the checkpoint. |

A metadata flag by itself doesn't close the crash window. If the process stops
after an external system commits but before the agent records completion, the
flag can't prove whether the operation completed. Use downstream idempotency or
a reconciliation API for this boundary.

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
- [Durable state store for hosted agents](agent-state-store.md)
- [Hosted agent runtime contract](hosted-agent-contract.md)
- [Add a protocol adapter to your hosted agent](../how-to/add-protocol-adapter.md)
- [Bring-your-own hosted agent samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples)