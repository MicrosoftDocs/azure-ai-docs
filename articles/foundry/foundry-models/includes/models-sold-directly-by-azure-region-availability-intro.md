---
title: Region availability for Foundry Models sold by Azure (intro)
author: msakande
ms.author: mopeakande
manager: mcleans
ms.date: 07/08/2026
manager: mcleans
ms.date: 07/08/2026
ms.service: microsoft-foundry
ms.topic: include
ms.custom: pilot-ai-workflow-jan-2026, classic-and-new
---

Microsoft Foundry provides customers with choices on the hosting structure that fits their business and usage patterns. In Foundry Models sold by Azure, model offerings include both Azure OpenAI models and models from other providers. This article introduces regional availability across both collections. 

Serverless API deployment in Microsoft Foundry includes three deployment categories: *standard* (pay-per-token), *provisioned* (reserved capacity), and *batch* (for asynchronous requests). Within these categories, you can choose global, data zone, or regional deployment types based on your compliance requirements.
For all deployment types, data stored at rest remains in the designated Azure geography (Americas, Europe, Asia Pacific, and Middle East and Africa). However, inferencing data is processed as follows:
- **Global** types: Might be processed in any Azure region where the model is deployed
- **Data Zone** types: Processed anywhere within the Microsoft-specified data zone (US, EU, or Asia Pacific (APAC))
- **Standard/Regional** types: Processed in the region associated with your deployment (not available for batch deployments)

All deployments can perform the exact same inference operations, but the billing, scale, and performance are substantially different. To learn more about Microsoft Foundry deployment types, including *batch* deployment types, see [Deployment types for Microsoft Foundry Models](../concepts/deployment-types.md).

> [!TIP]
> Use the tabs at the top of this page to switch deployment categories: [Standard deployment options](../concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard), [Provisioned deployment options](../concepts/models-sold-directly-by-azure-region-availability.md?pivots=provisioned), and [Batch deployment options](../concepts/models-sold-directly-by-azure-region-availability.md?pivots=batch).
