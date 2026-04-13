---
title: Include file
description: Include file
author: msakande
ms.reviewer: haakar
ms.author: mopeakande
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Troubleshooting

If you encounter issues when viewing or requesting quotas, try these solutions:

| Issue | Solution |
| ----- | -------- |
| Quota page is empty or shows no allocations | Verify that you have **Cognitive Services Usages Reader** role at the subscription level. Check that you're viewing the correct subscription in the portal. |
| **Request quota** button is disabled | Verify that you have **Owner** or **Contributor** role on the subscription. Some model and region combinations might not support quota increases. |
| Quota change not reflected after approval | Quota changes can take up to 15 minutes to propagate. Refresh the **Quota** page. If the issue persists after 24 hours, contact [Azure support](https://azure.microsoft.com/support/options/). |
| Can't find quota for a specific model | Check regional availability. Not all models are available in all regions. See [Region support](../reference/region-support.md). |
