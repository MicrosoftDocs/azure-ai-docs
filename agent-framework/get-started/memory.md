---
title: "Step 4: Memory & Persistence"
description: "Add context providers and persistent memory to your agent."
zone_pivot_groups: programming-languages
author: eavanvalkenburg
ms.topic: tutorial
ms.author: edvan
ms.date: 10/07/2026
ms.service: agent-framework
ai-usage: ai-assisted
ms.custom: update-code1
---

# Step 4: Memory & Persistence

Add context to your agent so it can remember user preferences, past interactions, or external knowledge.

:::zone pivot="programming-language-csharp"

By default, agents will store chat history in an `InMemoryChatHistoryProvider` or in the underlying AI service,
depending on what the underlying service requires.

The following agent uses OpenAI Chat Completion, which neither supports nor requires in-service chat history storage
so therefore automatically creates and uses an `InMemoryChatHistoryProvider`.

```csharp
using System;
using Azure.AI.Projects;
using Azure.Identity;
using Microsoft.Agents.AI;

var endpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT")
    ?? throw new InvalidOperationException("Set AZURE_OPENAI_ENDPOINT");
var deploymentName = Environment.GetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT_NAME") ?? "gpt-4o-mini";

AIAgent agent = new AIProjectClient(new Uri(endpoint), new DefaultAzureCredential())
    .AsAIAgent(
        model: deploymentName,
        instructions: "You are a friendly assistant. Keep your answers brief.",
        name: "MemoryAgent");
```

> [!WARNING]
> `DefaultAzureCredential` is convenient for development but requires careful consideration in production. In production, consider using a specific credential (e.g., `ManagedIdentityCredential`) to avoid latency issues, unintended credential probing, and potential security risks from fallback mechanisms.

To use a custom `ChatHistoryProvider` you can pass one to the agent options:

```csharp
using System;
using Azure.AI.Projects;
using Azure.Identity;
using Microsoft.Agents.AI;

var endpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT")
    ?? throw new InvalidOperationException("Set AZURE_OPENAI_ENDPOINT");
var deploymentName = Environment.GetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT_NAME") ?? "gpt-4o-mini";

AIAgent agent = new AIProjectClient(new Uri(endpoint), new DefaultAzureCredential())
    .AsAIAgent(model: deploymentName, options: new ChatClientAgentOptions()
    {
        ChatOptions = new() { Instructions = "You are a helpful assistant." },
        ChatHistoryProvider = new CustomChatHistoryProvider()
    });
```

Use a session to share context across runs:

```csharp
AgentSession session = await agent.CreateSessionAsync();

Console.WriteLine(await agent.RunAsync("Hello! What's the square root of 9?", session));
Console.WriteLine(await agent.RunAsync("My name is Alice", session));
Console.WriteLine(await agent.RunAsync("What is my name?", session));
```

> [!TIP]
> See [here](https://github.com/microsoft/agent-framework/tree/main/dotnet/samples/02-agents/Agents/Agent_Step04_3rdPartyChatHistoryStorage) for a full runnable sample application.

:::zone-end

:::zone pivot="programming-language-python"

The complete sample defines a context provider, adds it to an agent, and uses one session to preserve personalization state:

:::code language="python" source="~/../agent-framework-code/python/samples/01-get-started/04_memory.py" range="8-69" highlight="9,11,21-25,35-41,44-58":::

> [!TIP]
> See the [full sample](https://github.com/microsoft/agent-framework/blob/main/python/samples/01-get-started/04_memory.py) for the complete runnable file.

> [!NOTE]
> In Python, persistence/memory is handled by `ContextProvider` and `HistoryProvider` implementations. `InMemoryHistoryProvider` is the built-in local, in-memory history provider.
> `RawAgent` may auto-add `InMemoryHistoryProvider()` in specific cases (for example, when using a session with no configured context providers and no service-side storage indicators), but this is not guaranteed in all scenarios.
> If you always want local persistence, add an `InMemoryHistoryProvider` explicitly. Also make sure only one history provider has `load_messages=True`, so you don't replay multiple stores into the same invocation.
>
> Create a project client and memory store by following [Microsoft Foundry managed semantic memory](../integrations/by-component/context-providers/microsoft-foundry.md#add-managed-semantic-memory).
> Then combine local transcript history, managed memory, and an audit store:
>
> ```python
> from agent_framework import InMemoryHistoryProvider
> from agent_framework.foundry import FoundryMemoryProvider
>
> history = InMemoryHistoryProvider(load_messages=True)
> memory = FoundryMemoryProvider(
>     project_client=project_client,
>     memory_store_name="user-memory",
>     scope="user-123",
> )
> audit_store = InMemoryHistoryProvider(
>     "audit",
>     load_messages=False,
>     store_context_messages=True,  # include context added by other providers
> )
>
> agent = client.as_agent(
>     name="MemoryAgent",
>     instructions="You are a friendly assistant.",
>     context_providers=[history, memory, audit_store],  # audit store last
> )
> ```

:::zone-end

:::zone pivot="programming-language-go"

By default, agents use either local in-memory history or service-managed history depending on the provider and session.

The following Foundry agent uses a project-backed model deployment. Add a context provider when you want application-specific memory or personalization state beyond the conversation history.

```go
a := foundryprovider.NewAgent(
    endpoint,
    token,
    foundryprovider.ModelDeployment(model),
    foundryprovider.AgentConfig{
        Instructions: "You are a friendly assistant. Keep your answers brief.",
        Config: agent.Config{
            Name: "MemoryAgent",
        },
    },
)
```

Define a context provider that stores user info in session state and injects personalization instructions:

```go
import (
    "context"
    "fmt"
    "strings"

    "github.com/microsoft/agent-framework-go/agent"
    "github.com/microsoft/agent-framework-go/message"
)

const userMemorySourceID = "user_memory"

type providerState struct {
    UserName string `json:"user_name,omitempty"`
}

func newUserMemoryProvider() agent.ContextProvider {
    return agent.NewContextProvider(agent.ContextProviderConfig{
        SourceID: userMemorySourceID,
        Provide:  provideUserMemory,
        Store:    storeUserMemory,
    })
}

func provideUserMemory(ctx context.Context, invoking agent.InvokingContext) ([]*message.Message, []agent.Option, error) {
    session, _ := agent.GetOption(invoking.Options, agent.WithSession)
    var state providerState
    _, _ = session.Get(userMemorySourceID, &state)

    instructions := "You don't know the user's name yet. Ask for it politely."
    if state.UserName != "" {
        instructions = fmt.Sprintf("The user's name is %s. Always address them by name.", state.UserName)
    }
    return nil, []agent.Option{agent.WithInstructions(instructions)}, nil
}

func storeUserMemory(ctx context.Context, invoked agent.InvokedContext) error {
    session, _ := agent.GetOption(invoked.Options, agent.WithSession)
    var state providerState
    _, _ = session.Get(userMemorySourceID, &state)
    for _, msg := range invoked.RequestMessages {
        text := strings.TrimSpace(msg.Contents.Text())
        lower := strings.ToLower(text)
        if idx := strings.Index(lower, "my name is"); idx >= 0 {
            parts := strings.Fields(text[idx+len("my name is"):])
            if len(parts) == 0 {
                continue
            }
            state.UserName = strings.Trim(parts[0], ".,!?")
            session.Set(userMemorySourceID, state)
            break
        }
    }
    return nil
}
```

Create an agent with the context provider:

```go
a := foundryprovider.NewAgent(
    endpoint,
    token,
    foundryprovider.ModelDeployment(model),
    foundryprovider.AgentConfig{
        Instructions: "You are a friendly assistant.",
        Config: agent.Config{
            Name:             "MemoryAgent",
            ContextProviders: []agent.ContextProvider{newUserMemoryProvider()},
        },
    },
)
```

Run it — the agent now has access to the context:

```go
ctx := context.Background()
session, err := a.CreateSession(ctx)
if err != nil {
    panic(err)
}

// The provider doesn't know the user yet.
resp, err := a.RunText(ctx, "Hello, what is the square root of 9?", agent.WithSession(session)).Collect()
fmt.Println(resp, err)

// Teach the provider the user's name.
resp, err = a.RunText(ctx, "My name is Alice", agent.WithSession(session)).Collect()
fmt.Println(resp, err)

// Subsequent calls are personalized using session state.
resp, err = a.RunText(ctx, "What is 2 + 2?", agent.WithSession(session)).Collect()
fmt.Println(resp, err)
```

> [!TIP]
> See the [full sample](https://github.com/microsoft/agent-framework-go/blob/main/examples/01-get-started/04_memory/main.go) for the complete runnable file.

:::zone-end

## Next steps

> [!div class="nextstepaction"]
> [Step 5: Workflows](./workflows.md)

**Go deeper:**

- [Persistent storage](../concepts/agents/conversations/storage.md) — store conversations in databases
- [Chat history](../concepts/agents/conversations/context-providers.md) — manage chat history and memory
