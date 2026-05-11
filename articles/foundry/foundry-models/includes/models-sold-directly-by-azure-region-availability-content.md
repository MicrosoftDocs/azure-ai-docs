---
title: Content - Region availability for Foundry Models sold directly by Azure
author: msakande
ms.author: mopeakande
manager: nitinme
ms.date: 05/11/2026
ms.service: microsoft-foundry
ms.topic: include
ms.custom: pilot-ai-workflow-jan-2026, classic-and-new
zone_pivot_groups: adm-region-availability
---

Microsoft Foundry provides customers with choices on the hosting structure that fits their business and usage patterns. The service offers two main deployment categories, *standard* (pay-per-token) and *provisioned* (reserved capacity), along with other categories like *batch* (for asynchronous requests). Within these categories, you can choose global, data zone, or regional processing based on your compliance requirements.

For all deployment types, data stored at rest remains in the designated Azure geography (Americas, Europe, Asia Pacific, Middle East & Africa). However, inferencing data is processed as follows:
- **Global** types: May be processed in any Azure region where the Foundry Model is deployed
- **DataZone** types: Processed anywhere within the Microsoft-specified data zone (US or EU)
- **Standard/Regional** types: Processed in the region associated with your deployment (not available for batch deployments)

All deployments can perform the exact same inference operations, but the billing, scale, and performance are substantially different. To learn more about Microsoft Foundry deployment types, including *Batch* deployment types, see [Deployment types for Microsoft Foundry Models](../concepts/deployment-types.md).


::: zone pivot="standard"

[!INCLUDE [deployments-standard](../includes/model-matrix/deployments-standard.md)]

::: zone-end


::: zone pivot="provisioned"

[!INCLUDE [deployments-provisioned](../includes/model-matrix/deployments-provisioned.md)]

::: zone-end


::: zone pivot="batch"

[!INCLUDE [deployments-batch](../includes/model-matrix/deployments-batch.md)]

::: zone-end