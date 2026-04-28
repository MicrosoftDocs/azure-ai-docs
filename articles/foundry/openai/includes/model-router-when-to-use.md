---
title: Include file
description: Include file
author: PatrickFarley
ms.reviewer: sgilley
ms.author: pafarley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 04/22/2026
ms.custom: include
---

## When to use model router vs. direct deployment

Choosing between model router and a direct model deployment depends on your workload characteristics, compliance requirements, and operational preferences.

### When to use model router

- **Your workload is diverse.** A mix of simple and complex prompts benefits most from intelligent routing. The router matches each prompt to the best-suited model, delivering quality comparable to — or exceeding — a single general-purpose model.
- **Cost optimization matters.** Smaller, cheaper models handle simple prompts while frontier models are reserved for complex tasks. The savings are validated on both in-domain and out-of-domain benchmarks.
- **Latency and responsiveness are critical.** For high-traffic, user-facing scenarios like chatbots and customer support, model router routes simpler prompts to faster models. The result is lower average latency across your traffic mix compared to always calling a frontier model.
- **You want a single endpoint.** One deployment, one API call, one rate limit — simpler operations.
- **You're building agents.** Model router supports tools and can select fast models for classification subtasks and reasoning models for analysis — dynamically, per step.
- **You want automatic failover.** Built-in resilience with no extra configuration.
- **You want to simplify model lifecycle management.** Each router version maintains a curated set of underlying models. Deprecated models are replaced transparently. With auto-update enabled, your endpoint and application code don't change as models evolve.

### When to use direct deployment

- **You need the same model on every request.** Model router always reveals which model handled a request (via the model response field), but it might select different models for different prompts. If your workflow requires same model across all— pin to a specific model.

### The hybrid pattern

The most effective architecture uses both:
- **Model router** as the default path for general API traffic, capturing cost savings across the majority of requests.
- **Direct deployments** for specialized, compliance-mandated, or parameter-sensitive workloads.

This approach gives you broad optimization and precise control where you need it.
