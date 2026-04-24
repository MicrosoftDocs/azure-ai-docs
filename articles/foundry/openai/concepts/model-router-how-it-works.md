---
title: "How model router works in Microsoft Foundry"
description: "Learn how model router analyzes prompts, scores candidate models, and routes requests to optimize cost, quality, and latency in Microsoft Foundry."
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.date: 04/22/2026
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: concept-article
ms.custom:
  - classic-and-new
  - doc-kit-assisted
ai-usage: ai-assisted

#CustomerIntent: As a developer evaluating or already using model router, I want to understand how routing decisions are made so that I can configure model router effectively and set realistic expectations for cost, quality, and latency.
---

# How model router works in Microsoft Foundry

Model router is a purpose-built, trained machine-learning model that analyzes each prompt in real time and routes it to the most suitable large language model (LLM). It's a lightweight ML model designed to predict which model performs best for a given prompt at minimal latency.

This article explains the capabilities, routing modes, and best practices that power model router. For supported models and version information, see the [model router overview](model-router.md). For deployment and usage steps, see [Use model router](../how-to/model-router.md).

## Prerequisites

- Familiarity with LLMs and the [Chat Completions API](/azure/ai-foundry/openai/how-to/chatgpt)
- Understanding of the [model router overview](model-router.md)

## Why Model router

Choosing the right model for every prompt is hard to do manually. Model router is a purpose-built ML model trained on hundreds of thousands of examples across diverse scenarios — from simple Q&A to complex agentic workflows. It automatically matches each prompt to the best-suited model, optimizing for quality, cost, and latency.

Rather than relying on static rules or manual selection, model router learns from data and adapts as models evolve.

## How requests are routed

When a prompt arrives, model router processes it through three steps:

1. Understand the prompt. The router analyzes the full request — including system message, user message, tool definitions, and conversation history — to determine what the prompt is asking for and how challenging it is.

2. Select the best model. Based on the analysis, the router estimates which model in the pool will deliver the best result for this specific prompt, factoring in the routing mode you have configured (Balanced, Cost, or Quality).

3. Route and respond. The prompt is forwarded to the selected model. The entire routing decision adds minimal overhead — a negligible fraction of the LLM inference time.

## Key design deliverables

- **Efficiency.** The router is optimized for fast inference, keeping overhead minimal regardless of prompt complexity.
- **Adaptability.** The router adjusts automatically as the set of supported models evolves, without requiring changes to your application.
- **Transparency.** The selected model is always disclosed in the API response via the model field, so you can see exactly which model handled each request.

Model router analyzes prompts to make routing decisions but does not store them. It honors data-zone boundaries, routing only to models approved within your deployment’s geographic and compliance constraints.

## Model overview

Model router is a purpose-built ML model optimized for fast inference. It is not an LLM itself — it is designed to make routing decisions with minimal latency overhead.

The router is trained on a large, diverse dataset spanning hundreds of thousands of examples across many domains, including question answering, code generation, mathematical reasoning, summarization, conversational AI, and agentic workflows. Training data is continuously expanded as new models and capabilities are added.

The router is specifically trained to handle production-level complexity, including agentic and tool-calling workloads that require structured invocations and multi-step workflows.

## Intelligent prompt routing

One of model router’s key capabilities is understanding prompt difficulty. Not all coding questions are equally hard; not all summaries require the same reasoning depth.

The router distinguishes between prompts that any capable model can handle well — ideal for fast, cost-efficient models — and prompts that demand deeper reasoning, nuanced judgment, or sophisticated tool orchestration, where frontier models justify their higher cost.

This difficulty-aware routing is what allows model router to save costs without sacrificing quality. It only pays for frontier-level capability when the prompt genuinely needs it.

### Handling real-world complexity

Production prompts are rarely tidy single-sentence questions. The router handles:
- Long contexts spanning thousands of tokens, where the routing signal might be distributed across the entire input.
- Multi-turn conversations, where earlier turns provide context but the latest user message carries the most routing-relevant signal.
- Agentic and tool-calling scenarios, where the model must produce structured tool invocations, a capability the router is specifically optimized for.

### Adapting to model subsets

When you customize the model pool using model subsets, the router automatically recalibrates its routing decisions to optimize across the available models.

## Routing modes in depth

Model router exposes three routing modes that control the cost-quality tradeoff. For the mode descriptions and configuration steps, see the [model router overview](model-router.md#routing-mode) and the [how-to guide](../how-to/model-router.md#select-a-routing-mode).

Balanced (default): Optimizes for the best combination of quality and cost. Most workloads should start here.
Cost: Aggressively favors cheaper models, accepting slightly lower quality on complex prompts.
Quality: Always selects the highest-quality model for each prompt, regardless of cost.

## Observe routing behavior

Each routing mode produces a different distribution of traffic across underlying models. You can observe your routing distribution using Azure Monitor:

• In **Balanced mode**, traffic is distributed more broadly across the model pool based on prompt complexity.
• In **Cost mode**, the majority of traffic routes to smaller, cheaper models, escalating to larger models only when the prompt requires it.
• In **Quality mode**, frontier and high-capability models handle the majority of traffic.

## Illustrative example

The [ModelRouter-Distribution repository](https://github.com/guygregory/ModelRouter-Distribution) lets you run routing experiments against your own prompt corpus to preview how each mode distributes your workload before choosing.

:::image type="content" source="../media/model-router-how-it-works/routing-distribution-colors.png" alt-text="Bar chart that shows routing distribution across model tiers for Cost, Balanced, and Quality modes, with Cost mode heavily favoring nano-class models and Quality mode favoring frontier models.":::

<div align="center">

| Color | Mode | Description |
|---|---|---|
| 🟥 | **Cost mode** | First bar — routes to cheapest models by default |
| 🟦 | **Balanced mode** | Second bar — spreads across cheap and mid-tier |
| 🟠 | **Quality mode** | Third bar — favors frontier and reasoning models |

*Based on a point-in-time experiment; actual models and distribution will vary. Source: [ModelRouter-Distribution](https://github.com/guygregory/ModelRouter-Distribution).*

</div>

[!INCLUDE [model-router-when-to-use](../includes/model-router-when-to-use.md)]

[!INCLUDE [model-router-best-practices](../includes/model-router-best-practices.md)]

## Related content

- [Model router overview](model-router.md)
- [Use model router](../how-to/model-router.md)
- [What's new in model router](/azure/ai-foundry/foundry-models/whats-new-model-router)
