---
title: "Long-running agent API reference (preview)"
description: "API surface for building long-running, crash-resilient hosted agents with the AgentServer SDKs: task decorators, TaskContext, retry policy, resilient response options, and the streaming registry, in Python and C#."
author: aahill
ms.author: aahi
ms.manager: mcleans
ms.date: 08/10/2026
ms.topic: reference
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# Long-running agent API reference (preview)

This reference lists the AgentServer SDK surface for building [long-running, resilient hosted agents](long-running-agent-resilience.md): the resilient task primitives, the resilient Responses options, and the streaming registry. For the concepts behind these APIs, see [Resilience for long-running hosted agents](long-running-agent-resilience.md). For task-oriented walkthroughs, see the [how-to guides](../how-to/recover-long-running-work.md).

> [!NOTE]
> Long-running agents are in preview. The APIs on this page are from the `azure-ai-agentserver` packages and are subject to change.

## Packages

The APIs on this page require at least the following package versions. The Python packages are generally available; the .NET packages are in preview—install them with `--prerelease`.

| Protocol | Python (minimum version) | .NET (minimum version) |
| --- | --- | --- |
| Core (tasks, streaming, storage) | `azure-ai-agentserver-core` &ge; 2.0.0 | `Azure.AI.AgentServer.Core` &ge; 1.0.0-beta.28 |
| Responses | `azure-ai-agentserver-responses` &ge; 2.0.0 | `Azure.AI.AgentServer.Responses` &ge; 1.0.0-beta.8 |
| Invocations | `azure-ai-agentserver-invocations` &ge; 1.0.0 | `Azure.AI.AgentServer.Invocations` &ge; 1.0.0-beta.6 |

> [!NOTE]
> Use the latest available version. The versions listed are the minimums that include the resilient task, resilient Responses, and streaming-registry APIs described here.

## Resilient tasks

The task primitives make a unit of work crash-resilient. Declaring a task automatically enables the startup recovery scan.

### Declare a task

# [Python](#tab/python)

```python
from datetime import timedelta
from azure.ai.agentserver.core.tasks import task, multi_turn_task, TaskContext, RetryPolicy

@task(name="summarize", timeout=timedelta(minutes=10), retry=RetryPolicy())
async def summarize(ctx: TaskContext[str]) -> str:
    ...

@multi_turn_task(name="chat", steerable=True)
async def chat(ctx: TaskContext[dict]) -> dict:
    ...
```

| Decorator | Purpose |
| --- | --- |
| `@task(*, name, title=None, timeout=None, retry=None)` | One-shot resilient work. One input produces one result. |
| `@multi_turn_task(*, name, title=None, timeout=None, retry=None, steerable=False)` | A conversation chain that stays `suspended` between turns. Set `steerable=True` to queue a new turn behind the active one. |

# [C#](#tab/csharp)

```csharp
using Azure.AI.AgentServer.Core.Tasks;

// Register the task engine, then declare tasks.
builder.Services.AddResilientTasks(credential);

builder.Services.AddResilientTaskBuilder(tasks =>
{
    tasks.AddTask<string, string>("summarize", async (TaskContext<string> ctx, CancellationToken ct) =>
    {
        // ...
        return result;
    });

    tasks.AddMultiTurnTask<ChatInput, ChatOutput>("chat", async (ctx, ct) =>
    {
        // ...
        return output;
    }, steerable: true);
});
```

| Method | Purpose |
| --- | --- |
| `services.AddResilientTasks(TokenCredential)` | Registers the resilient task engine and recovery scanner. |
| `ResilientTaskBuilder.AddTask<TIn,TOut>(name, handler, configure?)` | Declares one-shot resilient work. |
| `ResilientTaskBuilder.AddMultiTurnTask<TIn,TOut>(name, handler, steerable, configure?)` | Declares a multi-turn chain. |

---

### Run a task

# [Python](#tab/python)

```python
# One-shot: run returns the output directly.
result = await summarize.run(input="...")

# Multi-turn: same task_id resumes the chain; if_last_input_id enforces ordering.
r = await chat.run(task_id="conv-7", input={"msg": "hi"}, if_last_input_id=prev_id)

# Fire-and-track: start returns a TaskRun handle.
run = await chat.start(task_id="conv-7", input={"msg": "hi"})
```

| Call | Returns | Notes |
| --- | --- | --- |
| `await task.run(*, input, task_id=None, if_last_input_id=None)` | `Output` | Runs to completion and returns the result. |
| `task.start(*, input, task_id=None, if_last_input_id=None)` | `TaskRun[Output]` | Returns a handle you can await or cancel. |

# [C#](#tab/csharp)

```csharp
// Resolve the task and run it.
var run = await task.StartAsync(input, new RunOptions
{
    TaskId = "conv-7",
    IfLastInputId = prevId,
});
var output = await run.GetResultAsync();
```

`RunOptions` carries `TaskId`, `InputId`, and `IfLastInputId` (the ordering precondition).

---

### `TaskContext`

The handler receives a `TaskContext` describing the current attempt.

| Python (`TaskContext[Input]`) | C# (`TaskContext<T>`) | Description |
| --- | --- | --- |
| `input` | `Input` | The value the caller passed. Persisted before the handler runs. |
| `task_id` | `TaskId` | The durable work identity. |
| `input_id` | `InputId` | The per-turn/per-input identity. |
| `entry_mode` | `EntryMode` | `fresh`, `resumed`, or `recovered`. |
| `metadata` | `Metadata` | Small durable key-value state (`TaskMetadata`). |
| `retry_attempt` | `RetryAttempt` | 0 on the first try. |
| — | `RecoveryCount` | Number of crash recoveries for this attempt. |
| `is_steered_turn` | `IsSteeredTurn` | `True` if this turn was promoted from the steering queue. |
| `pending_input_count` | `PendingInputCount` | How many newer turns are queued. |
| `cancel` | `Cancellation` | Cooperative cancel signal (any cause). |
| `cancel_requested` | `CancelRequested` | Cause: an explicit cancel was requested. |
| `timeout_exceeded` | `TimeoutExceeded` | Cause: the per-task timeout fired. |
| `shutdown` | `Shutdown` | The container is shutting down. |
| `await ctx.exit_for_recovery()` | `await ctx.ExitForRecoveryAsync()` | Defer unfinished work; leaves the record in progress for a later lifetime. |

`entry_mode` / `EntryMode` values:

| Value | Meaning |
| --- | --- |
| `fresh` / `Fresh` | First execution for this `(task_id, input_id)`. |
| `resumed` / `Resumed` | A subsequent turn of an existing chain. |
| `recovered` / `Recovered` | A previous lifetime ran this attempt and didn't finish; re-invoked with the persisted input. |

### `TaskRun`

The handle returned by `start` / `StartAsync`.

| Python (`TaskRun[Output]`) | C# (`TaskRun<T>`) | Description |
| --- | --- | --- |
| `task_id` | `TaskId` | The work identity. |
| `input_id` | `InputId` | The input identity. |
| `metadata` | `Metadata` | Live metadata reference while in flight. |
| `is_queued` | `IsQueued` | `True` if this input was queued behind an active steerable turn. |
| `await run.result()` | `await run.GetResultAsync()` | Await the output. |
| `await run.cancel()` | `await run.CancelAsync()` | Cooperatively cancel. |
| `await run` | `run.GetAwaiter()` | Awaitable directly. |

### Retry policy

Retries apply to handler failures, not to crash recovery. Crash recovery re-enters the same attempt and doesn't consume retry budget.

# [Python](#tab/python)

```python
from azure.ai.agentserver.core.tasks import RetryPolicy

RetryPolicy(
    initial_delay=timedelta(seconds=1),   # base delay
    backoff_coefficient=2.0,              # multiplier per attempt (>= 1.0)
    max_delay=timedelta(seconds=60),      # cap
    max_attempts=3,                       # total tries, including the first
)
RetryPolicy.no_retry()                    # single attempt
```

Delay formula: `min(initial_delay * backoff_coefficient ** attempt, max_delay)`.

# [C#](#tab/csharp)

```csharp
TaskRetryPolicy.ExponentialBackoff(maxAttempts: 3, initialDelay: TimeSpan.FromSeconds(1),
    backoffCoefficient: 2.0, maxDelay: TimeSpan.FromSeconds(60), jitter: true);
TaskRetryPolicy.FixedDelay(maxAttempts, delay, jitter);
TaskRetryPolicy.LinearBackoff(maxAttempts, initialDelay, increment, maxDelay, jitter);
TaskRetryPolicy.NoRetry;
```

Properties: `InitialDelay`, `BackoffCoefficient`, `MaxDelay`, `MaxAttempts`, `Jitter`, `RetryOn`.

---

### Task status and exceptions

`TaskStatus` (C#) / status values: `Pending`, `InProgress`, `Suspended`, `Completed`.

| Python exception | C# exception | Raised when |
| --- | --- | --- |
| `TaskConflictError` | `TaskConflictException` | A concurrent non-steerable `start` hit an in-flight task. |
| `TaskCancelled` | `TaskCancelledException` | The run was cancelled. |
| `TaskFailed` | `TaskFailedException` | The handler failed terminally. |
| `TaskDeferred` | `TaskDeferredException` | Work was deferred for recovery. |
| `SteeringQueueFull` | `SteeringQueueFullException` | The steering queue is at capacity. |
| `LastInputIdPreconditionFailed` | `LastInputIdPreconditionFailedException` | `if_last_input_id` / `IfLastInputId` didn't match. |
| `InputTooLarge` | `InputTooLargeException` | The input exceeded the task payload limit (~10 MiB). |

### Force-enable recovery

Declaring a task auto-enables the recovery scan. Force-enable it when tasks are registered lazily after host startup.

# [Python](#tab/python)

```python
from azure.ai.agentserver.core.tasks import set_resilient_tasks_enabled
set_resilient_tasks_enabled(True)   # call at import time, before host startup
```

# [C#](#tab/csharp)

`AddResilientTasks(credential)` registers the recovery scanner during host startup; no separate switch is required.

---

## Resilient Responses options

Set on `ResponsesServerOptions` when constructing the host. Both flags default to off.

# [Python](#tab/python)

```python
from azure.ai.agentserver.responses import ResponsesAgentServerHost, ResponsesServerOptions

app = ResponsesAgentServerHost(
    options=ResponsesServerOptions(
        resilient_background=True,       # re-invoke stored background responses after a crash
        steerable_conversations=True,    # queue a new turn instead of 409 conversation_locked
        default_fetch_history_count=100,
        sse_keep_alive_interval_seconds=None,
        shutdown_grace_period_seconds=10,
    ),
)
```

# [C#](#tab/csharp)

```csharp
var options = new ResponsesServerOptions
{
    ResilientBackground = true,
    SteerableConversations = true,
    DefaultFetchHistoryCount = 100,
};
```

---

| Python | C# | Default | Description |
| --- | --- | --- | --- |
| `resilient_background` | `ResilientBackground` | `False` | Re-invoke the handler on restart. Applies only to `store=true`, `background=true` responses. |
| `steerable_conversations` | `SteerableConversations` | `False` | Queue a concurrent turn instead of rejecting it. |
| `default_fetch_history_count` | `DefaultFetchHistoryCount` | `100` | Max history items hydrated per turn. |
| `sse_keep_alive_interval_seconds` | — | `None` | SSE keep-alive interval. |
| `shutdown_grace_period_seconds` | — | `10` | Seconds to wait for in-flight work on shutdown. |

### Recovery-aware `ResponseContext`

Available on the response handler's `context` when resilience is enabled.

| Python | C# | Description |
| --- | --- | --- |
| `context.is_recovery` | `IsRecovery` | `True` when the handler was re-invoked after a crash. |
| `context.persisted_response` | `PersistedResponse` | The last durably checkpointed response snapshot. |
| `context.conversation_chain_metadata` | `ConversationChainMetadata` | Small cross-turn references and watermarks. |
| — | `ConversationChainId` | Stable identity of the conversation chain. |
| `context.is_steered_turn` | `IsSteeredTurn` | `True` if this turn was promoted from the steering queue. |
| `context.pending_input_count` | `PendingInputCount` | Newer turns waiting in the queue. |
| `await context.exit_for_recovery()` | `await ExitForRecoveryAsync()` | Defer for recovery on shutdown; leaves the response `in_progress`. |

## Streaming registry

Pick one backing at startup, then look streams up by a per-turn id.

# [Python](#tab/python)

```python
from azure.ai.agentserver.core.streaming import streams

streams.use_in_memory_live()                                        # no replay, no restart survival
streams.use_in_memory_replay(cursor_fn=lambda e: e["n"], ttl_seconds=600)
streams.use_file_backed_replay(storage_dir=Path("/streams"),
                               cursor_fn=lambda e: e["n"])

stream = await streams.get_or_create(invocation_id)
await stream.emit({"n": 0, "delta": "..."})
async for event in stream.subscribe(after=last_cursor):
    ...
await stream.close()
```

| Configurator | Replay | Survives restart |
| --- | --- | --- |
| `use_in_memory_live()` | No | No |
| `use_in_memory_replay(*, cursor_fn=None, ttl_seconds=None)` | Yes, within TTL | No |
| `use_file_backed_replay(*, storage_dir=None, cursor_fn=None, ttl_seconds=None, serializer=None, deserializer=None)` | Yes | Yes |

Registry operations: `await streams.get_or_create(id)`, `await streams.delete(id)`. Pass `cursor_fn` to enable `subscribe(after=...)` and `last_cursor()`.

# [C#](#tab/csharp)

```csharp
using Azure.AI.AgentServer.Core.Streaming;

builder.Services.AddEventStreams(options =>
{
    // Configure the backing (live / replay / file-backed) via EventStreamOptions.
});

// Resolve the registry and obtain a per-turn stream.
EventStream stream = await registry.GetOrCreateAsync(invocationId);
```

Backings: `BroadcastEventStream` (live), `ReplayEventStream` (in-memory replay), `FileBackedReplayEventStream` (persistent). Registry: `EventStreamRegistry` / `InMemoryEventStreamRegistry`.

---

Streaming exceptions: `EventStreamClosedError`/`EventStreamClosedException`, `EventStreamNotFoundError`/`EventStreamNotFoundException`, and the base `EventStreamError`/`EventStreamException`.

## Related content

- [Resilience for long-running hosted agents](long-running-agent-resilience.md)
- [Recover long-running work after a crash](../how-to/recover-long-running-work.md)
- [Steer an in-flight agent turn](../how-to/steer-hosted-agent.md)
- [Stream long-running agent output with reconnect](../how-to/stream-with-reconnect.md)
- [Manage state for long-running agents](../how-to/manage-task-state.md)
