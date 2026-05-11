---
title: "Region availability for Foundry Models sold directly by Azure"
description: "Find region availability, capabilities, and deployments types available for Microsoft Foundry Models sold directly by Azure, to inform their use in AI applications."
author: msakande
ms.author: mopeakande
manager: nitinme
ms.date: 05/08/2026
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: product-comparison
ms.custom:
  - classic-and-new
ai-usage: ai-assisted
zone_pivot_groups: adm-region-availability

#CustomerIntent: As a developer, I want to browse the list of Microsoft Foundry Models sold directly by Azure based on the supported deployment types, availability in Azure regions, and model capabilities,, so that I can select the right model for my application.
---

# Region availability for Foundry Models sold directly by Azure

[!INCLUDE [models-sold-directly-by-azure-region-availability-content](../includes/models-sold-directly-by-azure-region-availability-content.md)]

<!-- Microsoft Foundry provides customers with choices on the hosting structure that fits their business and usage patterns. The service offers two main deployment categories, *standard* (pay-per-token) and *provisioned* (reserved capacity), along with other categories like *batch* (for asynchronous requests). Within these categories, you can choose global, data zone, or regional processing based on your compliance requirements.

For all deployment types, data stored at rest remains in the designated Azure geography (Americas, Europe, Asia Pacific, Middle East & Africa). However, inferencing data is processed as follows:
- **Global** types: May be processed in any Azure region where the Foundry Model is deployed
- **DataZone** types: Processed anywhere within the Microsoft-specified data zone (US or EU)
- **Standard/Regional** types: Processed in the region associated with your deployment (not available for batch deployments)

All deployments can perform the exact same inference operations, but the billing, scale, and performance are substantially different. To learn more about Microsoft Foundry deployment types, including *Batch* deployment types, see [Deployment types for Microsoft Foundry Models](deployment-types.md).


::: zone pivot="standard"

[!INCLUDE [deployments-standard](../includes/model-matrix/deployments-standard.md)]

::: zone-end


::: zone pivot="provisioned"

[!INCLUDE [deployments-provisioned](../includes/model-matrix/deployments-provisioned.md)]

::: zone-end


::: zone pivot="batch"

[!INCLUDE [deployments-batch](../includes/model-matrix/deployments-batch.md)]

::: zone-end -->