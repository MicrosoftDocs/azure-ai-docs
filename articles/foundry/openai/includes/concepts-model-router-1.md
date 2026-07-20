---
title: Include file
description: Include file
author: PatrickFarley
ms.reviewer: sgilley
ms.author: pafarley
ms.service: microsoft-foundry
ms.topic: include
ms.date: 05/20/2026
ms.custom: include
---

## How model router works

As a trained language model, model router analyzes your prompts in real time based on complexity, reasoning, task type, and other attributes. It does not store your prompts. It routes only to eligible models based on your access and deployment types, honoring data zone boundaries.

> [!IMPORTANT]
> The effective context window is limited by the smallest underlying model. For larger contexts, use [model subset](#model-subset) to select models that support your requirements.

- In Balanced mode (default), it considers all underlying models within a small quality range (for example, 1% to 2% compared with the highest-quality model for that prompt) and picks the most cost-effective model.
- In Cost mode, it considers a larger quality band (for example, 5% to 6% compared with the highest-quality model for that prompt) and chooses the most cost-effective model.
- In Quality mode, it picks the highest quality rated model for the prompt, ignoring the cost.

## Why use model router?

Model router optimizes costs and latencies while maintaining comparable quality. Smaller and cheaper models are used when they're sufficient for the task, but larger and more expensive models are available for more complex tasks. Also, reasoning models are available for tasks that require complex reasoning, and non-reasoning models are used otherwise. Model router provides a single deployment and chat experience that combines the best features from all of the underlying chat models.

The current version, `2025-11-18` (latest), includes the following capabilities:
1. Support Global Standard and Data Zone Standard deployments.
1. Adds support for new models: `grok-4`, `grok-4-fast-reasoning`, `DeepSeek-V3.1`, `DeepSeek-V3.2`, `gpt-oss-120b`, `Llama-4-Maverick-17B-128E-Instruct-FP8`, `gpt-4o`, `gpt-4o-mini`, `gpt-5.2`, `gpt-5.2-chat`, `claude-haiku-4-5`, `claude-sonnet-4-5`, `claude-opus-4-1`, and `claude-opus-4-6`.
1. Quick deploy or Custom deploy with **routing mode** and **model subset** options.
1. **Routing mode**: Optimize the routing logic for your needs. Supported options: `Quality`, `Cost`, `Balanced` (default).
1. **Model subset**: Select your preferred models to create your model subset for routing.
1. Support for agentic scenarios including tools so you can now use it in the Foundry Agent Service.

## Versioning

Model router uses date-stamped versions. The current version is `2025-11-18` (latest), which is actively maintained — new underlying models and features are added to this version over time without changing the version identifier.

Older versions (`2025-08-07`, `2025-05-19`) are frozen and don't receive new model additions.

| Version | Status | Description |
|:--------|:-------|:------------|
| `2025-11-18` | **Active (latest)** | Receives ongoing model and feature updates |
| `2025-08-07` | Frozen | Fixed set of models; no new additions |
| `2025-05-19` | Frozen | Fixed set of models; no new additions |

> [!TIP]
> You don't need to wait for a new version number to access newly supported models. The `2025-11-18` version is updated in place as new models become available.

If you select **Auto-update** at the deployment step (see [Model updates](../how-to/working-with-models.md#model-updates)), your model router deployment automatically updates when new versions become available. When that happens, the set of underlying models also changes, which could affect the overall performance of the model and costs.

[!INCLUDE [model-router-supported](model-router-supported.md)]
