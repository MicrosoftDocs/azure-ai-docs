---
title: "Durable state store for Microsoft Foundry hosted agents (preview)"
description: "Learn how the Microsoft Foundry durable state store preserves hosted agent data with user isolation, tags, expiration, and service limits."
author: aahill
ms.author: aahi
ms.manager: mcleans
ms.reviewer: glennc
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: concept-article
ms.date: 08/24/2026
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# Durable state store for Microsoft Foundry hosted agents (preview)

The **durable state store** for Microsoft Foundry hosted agents provides server-backed key-value storage for JSON data that must persist when an agent container crashes, restarts, or is evicted after an idle period. Use it to store framework checkpoints, application-managed conversation history, intermediate artifacts, and user preferences.

Your agent explicitly writes and updates state-store items. Unlike [sessions and conversations](hosted-agents.md#sessions-conversations-and-the-state-store), the platform doesn't populate the store automatically. The store supports per-user isolation, tags, optimistic concurrency, and configurable expiration.

This article explains how to partition data, manage caller identity, create and access stores and items, and work within service limits. During preview, the state store is available only to hosted agents.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

## What to keep in the state store

A hosted agent's compute is ephemeral. When the container restarts or the platform evicts it after an idle period, your agent loses anything it writes to local disk outside a [session](hosted-agents.md#sessions-conversations-and-the-state-store). The state store holds the state that must outlive the container.

Typical contents include:

- Framework checkpoints, so a bring-your-own agent framework such as LangGraph or Microsoft Agent Framework can resume its own graph or workflow state.
- Conversation history that your agent manages itself, which is the Invocations-protocol case where the platform doesn't store history for you.
- Generated artifacts and intermediate work that a later turn needs.
- Per-user profiles, preferences, and other long-lived application data.

The state store isn't the only option. A database, blob storage, or another application-owned store works the same way. The state store removes the need to provision and secure that storage yourself, and it applies the agent's identity model automatically.

Keep values small enough to fetch on demand. An item is capped at 1 MB, so large binaries belong in blob storage, with the store holding a reference to them.

> [!TIP]
> Long-running agents can keep progress markers and bulk checkpoints in separate items in the same state store. For a recovery pattern, see [Manage state for long-running agents](../how-to/manage-task-state.md).

## Stores

A `FoundryStateStore` client binds to one store name that you choose. That name serves as both the store's identity and its outermost partition. A store holds keyed JSON items that you can read, write, delete, and list.

- **Store name is the identity**: You can't change a store name after creation, so choose a stable naming scheme upfront.
- **Get-or-create is the store-level operation**: A single get-or-create call fetches the store or creates it when it's absent. Creation options apply only on first creation, so the service ignores them when the store already exists. An item write doesn't create a missing store.
- **Item lifetime**: A store-level idle window removes items. The default is 30 days, and you can configure a store so that items never expire. Writes renew the window, and reads don't. You set this option at creation.

## Partition data

The store gives you two independent ways to partition data, and most agents need only one of them.

- **By store name**: Every store name is its own partition. Names can contain `/`, so you can use it as a hierarchy separator, as in `checkpoints/thread-abc` or `workflow-state/run-42`. Choose this partition when the code that reads an item always has the partition identifier available to rebuild the name.
- **By end user**: A store created with user isolation partitions its items per end user, so a single store name is safe to share across the users of a multitenant agent. Choose this partition when the same store name serves more than one user. You set this option at creation, and the store resolves the user from the request rather than from anything your code passes. For details, see [Caller identity](#caller-identity).

Prefer the narrowest partition that your lookup path can reconstruct. A store name that encodes an identifier is only useful if every caller that reads the item still has that identifier. When a lookup carries an item key alone, as a framework checkpoint loader typically does, keep the store name flat and let user isolation do the partitioning instead.

The two axes compose, but keep them separate in kind: a store name should carry only non-user scope, such as a thread, run, or workflow identifier.

> [!IMPORTANT]
> Don't encode an end-user identifier in a store name. Store names appear in operational surfaces such as logs and error messages, and a name your own code builds isn't a verified identity. Use user isolation for per-user partitioning, so the platform enforces the boundary from the caller it established rather than from a value your agent supplies.

## Caller identity

The state store applies the hosted agent identity model. On [container protocol 2.0.0](hosted-agent-contract.md#platform-request-headers-container-protocol-200), each request the platform routes to your agent carries an `x-agent-foundry-call-id` header that identifies the caller, and the store resolves the acting end user from it. The Foundry SDKs forward the header on store calls for you, so most agents never handle it directly.

Two consequences matter when you design with it:

- **User isolation derives from the call ID**: In a user-isolated store, the partition comes from the caller the platform identified, not from anything your agent passes. A hosted agent doesn't supply an end-user identifier of its own. If your runtime issues its own HTTP requests instead of using an SDK client, forward the header unchanged, and treat the value as opaque.
- **Local runs don't support user isolation**: The platform doesn't provide the call ID off-platform. Neither the Python nor .NET SDK can enforce user isolation when you run the container locally. Test user-isolation boundaries with a deployed hosted agent.

### Carry the call ID into deferred work

Item operations act on behalf of a caller, and store operations don't.

| Operation | Scope | Acting user |
| --- | --- | --- |
| `create_item`, `set_item`, `get_item`, `delete_item`, `list_keys` | The items in the bound store | Resolved from the call ID when the store uses user isolation |
| Get-or-create for the store | The store itself | Not resolved; the operation is store-scoped |

By default an item operation uses the call ID of the request it runs inside, which is what you want for work that finishes during that request.

Work that outlives the request has no ambient call ID to inherit, such as background processing or a step that resumes in a later process lifetime. Every item operation accepts an explicit call ID for this case. Capture it while you still have the request, carry it alongside the work, and pass it back on each item operation, so those operations keep acting for the original caller.

The call ID identifies the caller of the current request, and it only partitions the items inside a user-isolated store. It doesn't partition anything else your container stores. For files, database rows, or caches that your own code owns, key them by the session ID and the user ID, as described in [Multiplex users in a shared session](../how-to/multiplex-session-users.md#partition-per-user-data-your-container-stores).

## Items

An item is a key and a JSON value, with optional string tags.

- **Values are your application JSON**: The store doesn't interpret an item value. Serialize your framework or domain models explicitly.
- **Tags are for filtering**: Tags are simple string labels, matched with AND when you list keys. Promote only the fields you need to filter on.
- **Listing returns keys only**: A page of keys is cheap even when the values are large, so listing and fetching are separate steps.
- **Optimistic concurrency**: Every item carries an ETag. Use an `If-Match` precondition for read-modify-write operations on mutable items, such as counters, where a lost update would corrupt state. A failed precondition reports the current ETag.
- **Append-only checkpoints don't need preconditions**: When each save writes a fresh key, there's no write contention, so the checkpoint path never needs `If-Match`.

## Create a store and items

The following example gets or creates a user-isolated store, writes an item, reads it back, and lists keys by tag. Get-or-create is the only store-level call an agent needs: it fetches the store, or creates it with the options you pass when the store is absent.

# [Python](#tab/python)

```python
from azure.ai.agentserver.core.storage import FoundryStateStore

# Fetch the store, or create it on first use
store = await FoundryStateStore.get_or_create(
    "checkpoints/thread-abc",
    user_isolation=True,
)

# Write an item; the value is your own application JSON
await store.set_item(
    "step-1",
    {"done": False, "attempt": 1},
    tags={"kind": "checkpoint"},
)

# Read it back
item = await store.get_item("step-1")
if item is not None:
    print(item.key, item.value["done"], item.etag)

# List keys by tag, then fetch only the values you need
page = await store.list_keys(tags={"kind": "checkpoint"}, limit=50, order="asc")
for key in page.keys:
    print(key.key, key.etag)
```

# [C#](#tab/csharp)

```csharp
using Azure.AI.AgentServer.Core.Storage;
using Azure.Identity;

// Fetch the store, or create it on first use
FoundryStateStore store = await FoundryStateStore.GetOrCreateAsync(
    "checkpoints/thread-abc",
    new DefaultAzureCredential(),
    userIsolation: true);

// Write an item; the value is your own application JSON
await store.SetItemAsync(
    "step-1",
    new Dictionary<string, BinaryData>
    {
        ["done"] = BinaryData.FromObjectAsJson(false),
        ["attempt"] = BinaryData.FromObjectAsJson(1),
    },
    tags: new Dictionary<string, string> { ["kind"] = "checkpoint" });

// Read it back
StateStoreItem? item = await store.GetItemAsync("step-1");
if (item is not null)
{
    bool done = item.Value["done"].ToObjectFromJson<bool>();
    Console.WriteLine($"{item.Key}: done={done}, etag={item.Etag}");
}

// List keys by tag, then fetch only the values you need
StateStoreItemKeyPage page = await store.ListKeysAsync(
    tags: new Dictionary<string, string> { ["kind"] = "checkpoint" },
    limit: 50,
    order: ListRequestOrder.Asc);

foreach (StateStoreItemKey key in page.Keys)
{
    Console.WriteLine($"{key.Key} {key.Etag}");
}
```

---

When you don't pass an endpoint, the client resolves the project endpoint from the environment, which the platform sets for a hosted agent.

## Service limits

The service enforces these limits. If you violate a limit, the service returns `400 Bad Request` and names the invalid field in the error message.

| Field | Limit |
| --- | --- |
| Store name | 1-128 characters, unique within the project and agent. |
| Item key | 1-128 characters, unique within the store. |
| Item value | Up to 1 MB of serialized JSON. |
| Store or item tags | Up to 16 entries. A key is 1-64 characters, and a value is up to 256 characters. |
| Description | Up to 1,024 characters. |
| Keys per list page | 1-100, with a default of 20. |

## Related content

- [Hosted agents in Foundry Agent Service](hosted-agents.md#sessions-conversations-and-the-state-store)
- [Hosted agent runtime contract](hosted-agent-contract.md#platform-request-headers-container-protocol-200)
- [Resilience for long-running hosted agents](long-running-agent-resilience.md)
- [Manage state for long-running agents](../how-to/manage-task-state.md)
- [Long-running agent API reference](long-running-agent-reference.md)
