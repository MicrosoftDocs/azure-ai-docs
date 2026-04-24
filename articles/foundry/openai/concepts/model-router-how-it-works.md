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

Model router is a purpose-built, trained machine-learning model that analyzes each prompt in real time and routes it to the most suitable large language model (LLM). It isn't a set of rules, a keyword matcher, or an LLM itself. It's a compact classifier designed to predict which model performs best for a given prompt at minimal latency.

This article explains the architecture, routing logic, and decision factors that power model router. For supported models and version information, see the [model router overview](model-router.md). For deployment and usage steps, see [Use model router](../how-to/model-router.md).

## Prerequisites

- Familiarity with LLMs and the [Chat Completions API](/azure/ai-foundry/openai/how-to/chatgpt)
- Understanding of the [model router overview](model-router.md)

## Why a learned router

There are several possible approaches to automated LLM routing. Each makes a different tradeoff.

- **Rule-based routing** maps keywords or query traits to models. It's simple and fast, but brittle, doesn't generalize, and never improves on its own.
- **LLM-based routing** uses a smaller LLM to pick the best model per query. It's flexible, but adds hundreds of milliseconds of latency, produces inconsistent decisions, and exposes every prompt to the router LLM.
- **Cascading and fallback** tries an inexpensive model first and escalates if the answer isn't good enough. It's pragmatic, but hard queries pay double latency and "good enough" is difficult to define automatically.
- **Third-party routing frameworks** offer SDK integration. They're fast to adopt, but bring vendor lock-in, external dependencies, and security review overhead.
- **Mixture-of-Experts (MoE)** embeds routing inside the model via learned gating. It's efficient, but models can't be swapped without retraining, and cost or latency budgets can't be encoded at runtime.
- **ML classifier-based routing** uses a lightweight model to predict the best LLM per query. It's adaptive and fast, but historically requires expensive training data, produces opaque decisions, and carries misrouting risk.

Model router in Microsoft Foundry takes the ML classifier approach and addresses its known weaknesses:

| Concern | Traditional approaches | Model router |
|---|---|---|
| **Latency** | Rules: none; LLM routers: hundreds of ms; cascades: variable | Milliseconds — orders of magnitude faster than LLM-based routing |
| **Learning** | Rules and cascades don't learn | Hundreds of thousands of training examples across hundreds of datasets |
| **Cost-quality control** | Manual rules or crude thresholds | Three routing modes with tuned quality-cost tradeoffs |
| **Transparency** | ML classifiers are traditionally opaque | Selected model exposed in every response; auditable routing modes and subsets |
| **Prompt privacy** | LLM routers expose prompts; cascades expose to multiple models | Prompts are never stored; data-zone boundaries are honored |
| **Failover** | Cascades have escalation; most approaches have none | Automatic failover across the model subset |
| **Misrouting risk** | All approaches carry risk | Quality thresholds guarantee near-parity with always picking the best model |

## The routing pipeline

When a prompt arrives, model router processes it through four stages:

1. **Prompt analysis.** The router encodes the incoming prompt — including system message, user message, tool definitions, and conversation history — and builds an internal representation of what the prompt asks for and how challenging it is.

1. **Per-model quality estimation.** The router estimates how well each candidate model would handle this specific prompt. These estimates are informed by training on hundreds of thousands of labeled examples spanning diverse domains and difficulty levels.

1. **Cost-aware selection.** The router applies the chosen routing mode (Balanced, Quality, or Cost) to select the optimal model, balancing predicted quality against cost according to the mode's policy.

1. **Dispatch.** The prompt is forwarded to the selected model. The entire routing decision adds only milliseconds of overhead — a negligible fraction of the LLM inference time.

:::image type="content" source="../media/model-router-how-it-works/routing-pipeline.png" alt-text="Diagram that shows the four-stage model router pipeline: prompt analysis, per-model quality estimation, cost-aware selection, and dispatch to the chosen model.":::

This design delivers three key properties:

- **Efficiency.** The router is a lightweight ML model, not an LLM, keeping overhead to milliseconds regardless of prompt complexity.
- **Adaptability.** The router adjusts automatically for any set of supported LLMs without retraining.
- **Robustness.** Quality estimates are backed by statistically rigorous evaluation data, ensuring reliable routing even for less common prompt types.

The selected model is always disclosed in the API response via the `model` field, providing full transparency into routing decisions.

> [!IMPORTANT]
> Model router analyzes prompts to make routing decisions but does not store them. It honors data-zone boundaries, routing only to models approved within the deployment's geographic and compliance constraints.

## Training and architecture

### Training data

The router is trained on a large, diverse dataset spanning hundreds of thousands of examples across hundreds of datasets and dozens of domains. Domains include question answering, mathematical reasoning, code generation, summarization, conversational chat, tool calling, and adversarial inputs. This breadth ensures the router generalizes across real-world prompt diversity rather than overfitting to narrow benchmarks.

Training data comes from two sources:

- **Supervised data** from established academic and industry benchmarks where ground-truth answers exist, providing quality reference points.
- **Semi-supervised data** labeled using an LLM-as-Judge approach, where a capable model evaluates outputs and assigns quality labels. Synthetic data generation fills coverage gaps in underrepresented domains.

Agentic and tool-calling workloads receive dedicated training data that covers structured tool invocations, multi-step agent workflows, and function-calling patterns.

### Compact architecture

Model router is a lightweight classification model, not a large language model. This is a deliberate design choice that keeps inference overhead latency to milliseconds. Standard ML techniques, including transfer learning and parameter-efficient fine-tuning, ensure accuracy and robustness without requiring the parameter count of a generative model. The training process accounts for class imbalance, ensuring the router performs well even on less common prompt types.

## Prompt complexity and difficulty awareness

One of the router's key capabilities is assessing prompt difficulty. Not all coding questions are equally hard; not all summaries require the same reasoning depth. The router learns to distinguish:

- **Simple, factual queries** that any capable model can answer correctly — ideal candidates for fast, cost-efficient models.
- **Moderate tasks** requiring multi-step reasoning or domain expertise — where mid-tier models excel.
- **High-complexity requests** demanding deep reasoning, nuanced judgment, or sophisticated tool orchestration — where frontier models justify their higher cost.

This difficulty-aware routing is what allows model router to save costs without sacrificing quality. It only pays for frontier-level capability when the prompt needs it.

### Handling real-world complexity

Production prompts are rarely tidy single-sentence questions. The router handles:

- **Long contexts** spanning thousands of tokens, where the routing signal might be distributed across the entire input.
- **Multi-turn conversations**, where earlier turns provide context but the latest user message carries the most routing-relevant signal.
- **Agentic and tool-calling scenarios**, where the model must produce structured tool invocations — a domain with distinct quality characteristics that the router recognizes and handles differently from standard text generation.

### Adapting to model subsets

When the available model pool changes because you restrict which models participate in routing, quality-cost tradeoffs need to be recalibrated. The number of possible subsets grows combinatorially with each new model. Model router handles this recalibration automatically, ensuring optimal model selection regardless of which models are included or excluded. For more on configuring model subsets, see [Model subset](model-router.md#model-subset).

## Routing modes in depth

Model router exposes three routing modes that control the cost-quality tradeoff. For the mode descriptions and configuration steps, see the [model router overview](model-router.md#routing-mode) and the [how-to guide](../how-to/model-router.md#select-a-routing-mode).

The modes work by adjusting the quality band — the tolerance for routing to a cheaper model:

- **Balanced** (default) considers all eligible models within a narrow quality band (for example, within 1% to 2% of the highest-quality model for that prompt) and picks the most cost-effective model.
- **Cost** considers a wider quality band (for example, within 5% to 6%) and aggressively favors cheaper models.
- **Quality** picks the highest-scoring model for the prompt, ignoring cost.

### Traffic distribution patterns

The quality-band mechanics translate into measurably different routing distributions. An [open-source experiment](https://github.com/guygregory/ModelRouter-Distribution) ran 1,000 diverse prompts through each mode and charted which underlying models were selected. The specific models evolve over time, but the pattern illustrates how the modes differ:

- **Cost mode** concentrated the vast majority of traffic on the cheapest nano-class models, escalating to larger models only when the router determined a prompt genuinely needed it.
- **Balanced mode** spread traffic more broadly — the cheapest model still handled about half, but mid-tier models picked up significant share for harder prompts.
- **Quality mode** flipped the distribution — the full frontier model handled roughly half of traffic, with reasoning and high-capability models appearing for prompts that needed them.

:::image type="content" source="../media/model-router-how-it-works/routing-distribution-colors.png" alt-text="Bar chart that shows routing distribution across model tiers for Cost, Balanced, and Quality modes, with Cost mode heavily favoring nano-class models and Quality mode favoring frontier models.":::

<div align="center">

| Color | Mode | Description |
|---|---|---|
| 🟥 | **Cost mode** | First bar — routes to cheapest models by default |
| 🟦 | **Balanced mode** | Second bar — spreads across cheap and mid-tier |
| 🟠 | **Quality mode** | Third bar — favors frontier and reasoning models |

*Based on a point-in-time experiment; actual models and distribution will vary. Source: [ModelRouter-Distribution](https://github.com/guygregory/ModelRouter-Distribution).*

</div>

The key insight: even in Quality mode, the router doesn't automatically send everything to the most expensive model. Simple prompts still route to cheaper models because the router knows they produce equivalent results. And even in Cost mode, the router escalates when it matters. This is what distinguishes a learned router from a static rule-based router.

> [!TIP]
> The [ModelRouter-Distribution repository](https://github.com/guygregory/ModelRouter-Distribution) includes a batch runner, plotting scripts, and full methodology. Run it against your own prompt corpus to build a baseline distribution for your workload before choosing a mode.

[!INCLUDE [model-router-when-to-use](../includes/model-router-when-to-use.md)]

[!INCLUDE [model-router-best-practices](../includes/model-router-best-practices.md)]

## Related content

- [Model router overview](model-router.md)
- [Use model router](../how-to/model-router.md)
- [What's new in model router](/azure/ai-foundry/foundry-models/whats-new-model-router)
