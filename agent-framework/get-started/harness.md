---
title: "Step 6: Agent Harness"
description: "Create a harness agent that plans, tracks todos, and runs multi-step tasks."
zone_pivot_groups: programming-languages
author: westey-m
ms.topic: tutorial
ms.author: westey
ms.date: 10/07/2026
ms.service: agent-framework
ai-usage: ai-assisted
---

# Step 6: Agent Harness

A *harness* wraps a chat client with the scaffolding an agent needs to work through long, multi-step tasks — planning / execution modes, a todo list to plan against, context compaction, file memory, file access, and don't-ask-again tool approval. Instead of assembling those pieces yourself, you create a harness agent and get them out of the box.

:::zone pivot="programming-language-csharp"

Create a harness agent from any `IChatClient` with the `AsHarnessAgent` extension method. Because a harness works through tasks interactively over many steps, you typically drive it from a conversation loop: keep an `AgentSession` so the harness state (plan, todos, and history) persists across turns, read the user's next instruction, and stream the agent's output as it's produced.

```csharp
using System;
using Microsoft.Agents.AI;
using Microsoft.Extensions.AI;

// chatClient is any IChatClient implementation (Foundry, Azure OpenAI, OpenAI, Anthropic, ...).
AIAgent agent = chatClient.AsHarnessAgent();

// A session carries the harness state (plan, todos, history) across turns.
AgentSession session = await agent.CreateSessionAsync();

Console.WriteLine("Harness agent ready. Type 'exit' to quit.");
while (true)
{
    Console.Write("> ");
    string? input = Console.ReadLine();
    if (string.IsNullOrWhiteSpace(input) || input.Equals("exit", StringComparison.OrdinalIgnoreCase))
    {
        break;
    }

    // Stream this turn's output as the harness plans and works through the request.
    await foreach (var update in agent.RunStreamingAsync(input, session))
    {
        Console.Write(update);
    }

    Console.WriteLine();
}
```

The harness handles planning, todo tracking, and history persistence for you across the whole conversation. For a full-featured console — with tool-approval prompts, todo/mode rendering, and slash commands — see the [sample terminal UX](../concepts/harness.md#sample-terminal-ux).

> [!TIP]
> See the [.NET harness samples](https://github.com/microsoft/agent-framework/tree/main/dotnet/samples/02-agents/Harness) for full runnable applications.

:::zone-end

:::zone pivot="programming-language-python"

The complete sample creates a Microsoft Foundry chat client, wraps it with `create_harness_agent`, and reuses one session across two turns. The harness adds planning, todo tracking, and compaction while the sample disables file memory and web search to stay focused.

:::code language="python" source="~/../agent-framework-code/python/samples/01-get-started/06_agent_harness.py" range="9-34" highlight="9-18":::

From the Agent Framework repository root, run the sample:

```bash
python python/samples/01-get-started/06_agent_harness.py
```

The shared session preserves the harness state across both calls. For a full-featured console — with tool-approval prompts, todo/mode rendering, and slash commands — see the [sample terminal UX](../concepts/harness.md#sample-terminal-ux).

> [!TIP]
> See the [full get-started sample](https://github.com/microsoft/agent-framework/blob/main/python/samples/01-get-started/06_agent_harness.py).
> For more patterns, see the [Python harness samples](https://github.com/microsoft/agent-framework/tree/main/python/samples/02-agents/harness).

:::zone-end

:::zone pivot="programming-language-go"

> [!NOTE]
> Go support for agent harnesses is coming soon. See the [Agent Framework Go repository](https://github.com/microsoft/agent-framework-go) for the latest status.

:::zone-end

## Next steps

> [!div class="nextstepaction"]
> [Step 7: Host Your Agent](./hosting.md)

**Go deeper:**

- [Agent Harnesses](../concepts/harness.md) — compaction, looping, shell, and the sample terminal UX
- [Agent Skills](../agents/skills.md) — progressively load skills from the file system
