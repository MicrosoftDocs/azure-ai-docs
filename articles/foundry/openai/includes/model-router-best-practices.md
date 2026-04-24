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

## Best practices

Follow these recommendations to get the most from model router.

**Start with Balanced mode, then tune.** Let traffic flow through Balanced mode, observe the routing distribution in Azure Monitor for a few weeks, and then adjust. Switch latency-insensitive batch pipelines to Cost mode and promote critical-path reasoning tasks to Quality mode.

**Use model subset as your compliance gate.** Get model approval from your security team, encode it in the subset, and know that new models won't appear without explicit opt-in.

**Monitor routing distribution.** In the Azure portal, go to **Monitoring** > **Metrics** for your resource, filter by your model router deployment, and split by underlying model. This view shows exactly where your tokens go.

**Design for the smallest context window — or raise the floor.** If your prompts consistently exceed the context window of the smallest model in the pool, use model subset to include only models that support your required context length.

**Use prompt caching.** Consistent prompt prefixes combined with stable routing to the same model yield caching benefits. Use the `cached_tokens` field in the response to verify.

**Select at least two models for failover.** A single-model subset defeats the purpose of routing and disables automatic failover.

**Handle rate limits client-side.** Model router's built-in failover handles transient model issues, but quota exhaustion requires retry logic with exponential backoff in your application code.

### Practices to avoid

**Don't deploy model router and individual deployments of the same underlying models.** Doing so doubles cost and creates confusion about which endpoint handles traffic. Use model router as your unified entry point.

**Don't use single-model subsets.** You lose routing optimization, cost savings, and failover — effectively using model router as an expensive passthrough.

**Don't expect deterministic model selection.** The router optimizes globally across your traffic, not for per-request repeatability. If you need the same model every time, use a direct deployment.

**Don't set content filters or rate limits on underlying models.** These controls belong on the model router deployment itself. The router applies them uniformly across all underlying models.

**Don't ignore the `model` field in responses.** This field is your primary observability signal. Log it, build dashboards, and alert on unexpected distribution shifts.
