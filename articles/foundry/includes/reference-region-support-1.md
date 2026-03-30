---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: deeikele
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## How to verify region support for your workload

Use this process before you create resources:

1. Select a candidate project region from the **Foundry projects** list in this article.
1. Verify model and quota availability in [Azure OpenAI quotas and limits](/azure/ai-foundry/openai/quotas-limits#regional-quota-capacity-limits).
1. Verify feature-specific support in the **Foundry features** list links.
1. Confirm the final service list in [Azure global infrastructure products by region](https://azure.microsoft.com/global-infrastructure/services/).

## Quick decision checklist

Before you choose a production region, confirm all answers are **Yes**:

- Is your required model available in the target region?
- Do you have enough quota in that region for your expected traffic?
- Are all dependent services (for example, Speech, Content Safety, Agent Service tools) available in that region?
- Do your compliance requirements require a sovereign cloud region?
- Have you validated availability in both docs and your portal experience for the same subscription and tenant?

When you validate availability, keep these constraints in mind:

- Azure OpenAI quotas are allocated per region, per subscription, and per model or deployment type.
- Azure Speech keys are region-specific and only work for the region where the Speech resource is created.
- The region list in this article is a documentation snapshot. Always verify against the linked service-specific and infrastructure pages before production rollout.

## Troubleshoot region mismatch issues

If a feature isn't available in your selected region:

- Use the feature-specific regional availability article linked in **Foundry features**.
- Create the required dependent resource in a supported region.
- Re-check model availability and quota limits for that region.
- For Speech workloads, confirm that your app configuration uses the same region as your Speech resource.
- If your organization requires a sovereign cloud, review **Foundry in sovereign clouds** in this article.
