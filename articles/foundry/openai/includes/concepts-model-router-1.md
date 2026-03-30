---
title: Include file
description: Include file
author: PatrickFarley
ms.reviewer: sgilley
ms.author: pafarley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
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

The latest version, `2025-11-18` includes several capabilities:
1. Support Global Standard and Data Zone Standard deployments.
1. Adds support for new models: `grok-4`, `grok-4-fast-reasoning`, `DeepSeek-V3.1`, `DeepSeek-V3.2`, `gpt-oss-120b`, `Llama-4-Maverick-17B-128E-Instruct-FP8`, `gpt-4o`, `gpt-4o-mini`, `gpt-5.2`, `gpt-5.2-chat`, `claude-haiku-4-5`, `claude-sonnet-4-5`, `claude-opus-4-1`, and `claude-opus-4-6`.
1. Quick deploy or Custom deploy with **routing mode** and **model subset** options.
1. **Routing mode**: Optimize the routing logic for your needs. Supported options: `Quality`, `Cost`, `Balanced` (default).
1. **Model subset**: Select your preferred models to create your model subset for routing.
1. Support for agentic scenarios including tools so you can now use it in the Foundry Agent Service.

## Versioning

Each version of model router is associated with a specific set of underlying models and their versions. This set is fixed&mdash;only newer versions of model router can expose new underlying models.

If you select **Auto-update** at the deployment step (see [Model updates](../how-to/working-with-models.md#model-updates)), then your model router model automatically updates when new versions become available. When that happens, the set of underlying models also changes, which could affect the overall performance of the model and costs.

[!INCLUDE [model-router-supported](model-router-supported.md)]
