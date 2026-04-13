---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: aashishb
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/23/2026
ms.custom: include
---

## Troubleshoot common cost analysis issues

- **Costs don't match your estimate:** Confirm that all dependent resources (for example, storage, networking, and Marketplace resources) are included in your Cost Management scope.
- **Can't see cost data:** Confirm you have both cost visibility permissions and Foundry access permissions at the correct scope.
- **Unexpected meter charges:** Group by **Meter** and **Resource** to identify which service generated the charge, then compare with deployment and traffic patterns.
- **Region rollout cost variance:** Validate region/model availability before deployment and recheck assumptions if you deploy in different regions.
- **Tag filters return incomplete results:** Verify required tags are applied to all participating resources and inherited consistently from your deployment process.
- **Budget alerts are noisy or delayed:** Recalibrate alert thresholds after observing normal usage for a full trend window, then separate warning and critical thresholds.
- **Policy or scope drift changes cost visibility:** Confirm your selected scope and policy assignments still include all resources used by the workload.
- **Data appears delayed after test runs:** Wait for ingestion latency, then recheck the same time window before concluding there is a billing discrepancy.
