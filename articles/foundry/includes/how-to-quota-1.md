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

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/free/).
- A [Foundry project](../how-to/create-projects.md).
- **Cognitive Services Usages Reader** role at the subscription level, to view quota allocations.
- **Owner** or **Contributor** role on the subscription, to request quota increases.
- **Cognitive Services Contributor** role combined with **Cognitive Services Usages Reader**, to edit quota allocations in the Foundry portal.

## Foundry shared quota

Foundry provides a pool of shared quota that different users across various regions can use concurrently. Depending on availability, users can temporarily access quota from the shared pool and use the quota to perform testing for a limited amount of time. The specific time duration depends on the use case. By temporarily using quota from the quota pool, you no longer need to file a support ticket for a short-term quota increase or wait for your quota request to be approved before you can proceed with your workload. 

You can use the shared quota pool for testing inferencing for Foundry Models from the model catalog. Use the shared quota only for creating temporary test endpoints, not production endpoints. For endpoints in production, you should [request dedicated quota](#view-and-request-quotas-in-foundry-portal). Billing for shared quota is usage-based.
