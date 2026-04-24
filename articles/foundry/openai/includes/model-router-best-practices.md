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

- **Start with Balanced mode, then tune.** Let traffic flow through Balanced mode, observe the routing distribution in Azure Monitor for a few weeks, and then adjust. Switch latency-insensitive batch pipelines to Cost mode and promote critical-path reasoning tasks to Quality mode.
- **Use model subset as your compliance gate.** Get model approval from your security team, encode it in the subset, and know that new models won't appear without explicit opt-in.
- **Monitor routing distribution.** In the Azure portal, go to **Monitoring > Metrics** for your resource, filter by your model router deployment, and split by underlying model. This view shows exactly where your tokens go.
- **Design for the smallest context window — or raise the floor.** If your prompts consistently exceed the context window of the smallest model in the pool, use model subset to include only models that support your required context length.
- **Select at least two models for failover.** A single-model subset defeats the purpose of routing and disables automatic failover.

### Practices to avoid
- **Don't use single-model subsets.** You lose routing optimization, cost savings, and failover — effectively using model router as an expensive passthrough.
- **Don't ignore the model field in responses.** This field is your primary observability signal. Log it, build dashboards, and track which models are handling your traffic.
