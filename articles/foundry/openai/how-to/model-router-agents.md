---
title: "Use model router with Foundry agents"
description: "Learn how model router selects the optimal model per request for your Foundry agents, reducing costs while maintaining quality across tool-calling, RAG, and multi-turn scenarios."
author: sanjeev3
ms.author: sajagtap
ms.date: 05/22/2026
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: how-to
ms.custom:
  - build-2025
  - doc-kit-assisted
ai-usage: ai-assisted
---

# Use model router with Foundry agents

Model router selects the optimal large language model (LLM) for each request your agent makes — per turn, not per session. A simple greeting routes to a fast, inexpensive model. A complex tool-calling chain routes to a frontier model. You deploy one endpoint, write zero routing logic, and get automatic cost optimization across all agent interactions.

This article explains how model router behaves with Foundry Agent Service agents, which tool types it supports, the routing patterns you can expect, and how to get started.

For general model router concepts, see the [model router overview](../concepts/model-router.md). For deployment steps, see [Use model router](model-router.md).

## Prerequisites

- A Microsoft Foundry project with a model router deployment. See [Deploy a model router model](model-router.md#deploy-a-model-router-model).
- Familiarity with [Foundry Agent Service](/azure/ai-foundry/agents/overview).
- Azure CLI installed and authenticated (`az login`).

## Why use model router for agents

Building agents requires choosing a model — but agents handle diverse tasks within the same session. A single conversation might include:

- A simple factual lookup (inexpensive model is sufficient)
- A multi-step tool-calling chain (mid-tier model handles orchestration)
- Complex reasoning or synthesis (frontier model needed)

Without model router, you either over-provision (use an expensive model for everything) or under-provision (use a cheap model that degrades on complex tasks). Model router eliminates this tradeoff by selecting the right model for each individual request.

Key benefits for agent workloads:

- **Zero model selection overhead.** One deployment serves all agent scenarios — no per-agent model decisions.
- **Per-request optimization.** Different turns in the same conversation use different models based on complexity.
- **Automatic cost efficiency.** Simple queries use inexpensive models; expensive models only activate when the prompt genuinely needs them.
- **Tool-aware routing.** The router understands tool-calling patterns and selects models capable of structured invocations.
- **Future-proof.** As new models become available, the router incorporates them without code changes.

## Supported tool types

Model router works with all Foundry Agent Service tool types:

| Tool type | Description | Routing behavior |
| --- | --- | --- |
| FunctionTool | Client-side function calling with custom APIs | Mid-tier models handle structured tool calls efficiently |
| WebSearchTool | Built-in server-side web search | Routes based on query complexity — simple lookups vs. research synthesis |
| CodeInterpreterTool | Sandboxed code execution | Higher-capability models for code generation; mid-tier for simple computations |
| FileSearchTool | Document retrieval with vector stores (RAG) | Full-capability models for synthesis across retrieved documents |
| MCPTool | External tools via Model Context Protocol | Routes based on orchestration complexity |

> [!IMPORTANT]
> If you use Agent service tools in your flows, only OpenAI models are used for routing.

## How routing works with agents

Model router analyzes the full request context — system message, user message, tool definitions, conversation history — to determine complexity and select a model. For agents, this means:

### Per-request, not per-session

Each turn in a conversation is routed independently. A conversation might use three different models across five turns based on what each turn requires. You can observe which model handled each request through the `model` field in the API response.

### Complexity-aware selection

The router distinguishes between:

- **Low complexity** — Factual recall, simple greetings, or basic follow-up questions route to fast, inexpensive models.
- **Medium complexity** — Tool orchestration (calling a function, passing arguments, formatting results) routes to capable mid-tier models that generate valid tool calls at lower cost.
- **High complexity** — Research synthesis, multi-step reasoning, and complex code generation route to frontier models.

### Tool-aware routing

When tools are attached to an agent, the router factors tool definitions into its routing decision. Mechanistic tool calls (structured JSON generation with `strict=True`) don't require expensive models — the router selects cost-efficient models that reliably produce valid tool invocations.

## Routing patterns for agent scenarios

The following patterns describe typical model router behavior with agents. Specific model selections vary over time as new models become available and routing logic evolves.

### Simple conversations

Factual questions, greetings, and basic follow-ups route to fast, inexpensive models. This applies regardless of whether the agent has tools attached — if the current turn doesn't need them, the router optimizes for speed and cost.

### Tool orchestration

When an agent invokes tools (function calls, web search, code execution), the router selects models capable of structured output generation. For straightforward tool calls, mid-tier models handle orchestration at a fraction of frontier model cost.

### RAG and document synthesis

Retrieval-augmented generation — where the agent searches a vector store and synthesizes information across multiple documents — consistently routes to higher-capability models. The reasoning and synthesis demands justify the cost.

### Summarization

Summarization tasks (for example, "summarize our conversation") route to models specialized for that task type. The router recognizes summarization as a distinct category regardless of the agent scenario.

### Multi-step orchestration

Complex agentic workflows that chain multiple tool calls, require multi-step reasoning, or involve external service orchestration (MCP servers, Toolbox) route to frontier models.

## Cost implications

Model router delivers cost savings by matching model capability to task demands:

- **Simple agent interactions** (typically 50–60% of traffic) route to models that cost significantly less than frontier models while maintaining equivalent quality for those tasks.
- **Complex interactions** still use frontier models — quality is preserved where it matters.
- **Net effect** — You pay frontier-model prices only for requests that genuinely require frontier-model capability.

The exact savings depend on your workload mix. Workloads with a higher proportion of simple interactions (classification, lookup, basic Q&A) see larger savings.

## Get started

### Configure your agent to use model router

Set model router as the model for your agent. No additional routing configuration is needed.

In the [Foundry portal](https://ai.azure.com/?cid=learnDocs), select your model router deployment from the **model** dropdown when creating or editing an agent in the agent playground.

For programmatic agent creation, specify your model router deployment name:

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

project = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

agent = project.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT"],  # "model-router"
    name="my-agent",
    instructions="You are a helpful assistant.",
)
```

### Observe routing decisions

Each response includes the `model` field showing which underlying model was selected. Log this field to track routing distribution across your agent's interactions:

```python
response = project.agents.runs.create_and_process(
    thread_id=thread.id,
    agent_id=agent.id,
)

# The model field shows which model handled this request
for message in project.agents.messages.list(thread_id=thread.id):
    print(f"[model: {message.model}] {message.content}")
```

### Tune routing behavior

After observing your agent's routing distribution:

- **Switch routing mode** — Use Quality mode for critical agents (legal, medical) or Cost mode for high-volume agents (classification, triage). See [Change the routing mode](model-router.md#optional-change-the-routing-mode).
- **Constrain the model pool** — Use model subset to limit which models the router can select. See [Route to a model subset](model-router.md#optional-route-to-a-model-subset).

## Explore with hands-on demos

The [Foundry Agent Lab](https://github.com/microsoft-foundry/Foundry-Agent-Lab) provides a progressive series of agent demos — all using model router — that demonstrate routing behavior across scenarios including function tools, web search, code interpretation, RAG, MCP, and Toolbox. Each demo includes session logs showing which models the router selected and why.

## Related content

- [Model router overview](../concepts/model-router.md)
- [How model router works](../concepts/model-router-how-it-works.md)
- [Use model router](model-router.md)
- [Foundry Agent Service overview](/azure/ai-foundry/agents/overview)
