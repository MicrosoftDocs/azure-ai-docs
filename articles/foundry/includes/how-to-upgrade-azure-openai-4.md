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

## How to check if a resource was upgraded

You can check the following Azure resource property to see if a resource was previously upgraded to Foundry.

```bicep
{
  {
    // Read only properties if your resource was upgraded:
    previouskind: "OpenAI"
  }
}
```

If you're not sure who upgraded your resource to Foundry, you can [view the activity log in the Azure portal](/azure/azure-monitor/platform/activity-log-insights#view-the-activity-log) to find out when the upgrade operation took place and which user performed it:

1. Use Azure Activity Logs (under "Monitoring") to see if an upgrade operation was performed.
1. Filter by "Write" operations on the storage account.
1. Look for operations listed as `Microsoft.CognitiveServices/accounts/write`.
