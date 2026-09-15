---
ms.service: azure-ai-search
ms.topic: include
ms.date: 08/14/2026
ai-usage: ai-assisted
---

1. Complete the [private network prerequisites](#prerequisites).

1. Set `networkAccessMode` to `private` in the knowledge source creation request. You can only set this property during creation. To change it later, delete and recreate the knowledge source.

   Creation can fail if the service tier or runtime doesn't support private execution or if a required shared private link doesn't exist.

1. Confirm that the generated indexer's `executionEnvironment` is `private`.

1. Confirm that each required shared private link is approved and targets the correct dependency. Successful creation alone doesn't confirm link approval or targeting.

1. Poll the knowledge source status until `lastSynchronizationState.endTime` has a value. Confirm that `itemsUpdatesFailed` is `0`, and then verify the connector-specific source content. Synchronization fails if a dependency isn't reachable.
