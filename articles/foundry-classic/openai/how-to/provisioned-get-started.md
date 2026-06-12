---
title: "Operate provisioned throughput deployments in production (classic)"
description: "Manage PTU quota, create and scale deployments, purchase reservations, benchmark, monitor utilization, and handle high load for provisioned throughput in production. (classic)"
ai-usage: ai-assisted
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-models
ms.custom:
  - openai, pilot-ai-workflow-jan-2026
  - classic-and-new
  - doc-kit-assisted
ms.topic: how-to
author: msakande
ms.author: mopeakande
ms.reviewer: seramasu
reviewer: rsethur
ms.date: 05/25/2026
recommendations: false
#customerIntent: As a developer with a provisioned throughput deployment, I want to benchmark, monitor, and scale it so I can run it reliably in production.
ROBOTS: NOINDEX, NOFOLLOW
---

# Operate provisioned deployments in production (classic)

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../../foundry/openai/how-to/provisioned-get-started.md)

[!INCLUDE [how-to-provisioned-get-started-1](../../../foundry/openai/includes/how-to-provisioned-get-started-1.md)]


## Check and request PTU quota

PTU quota is granted per subscription, per region, and limits the total PTUs you can deploy in that region across all models. For details on how quota and capacity relate, see [PTU quota vs. capacity](../concepts/provisioned-throughput.md#quota-and-capacity).

To check current usage or request additional quota:

1. Go to **Management center** > **Quota** > **Provisioned throughput** in the Foundry portal.
1. Select the desired subscription and region to view current usage.
1. Select **Request Quota** next to any of the listed **Quota names**. 
1. Complete the form.

> [!TIP]
> You can also follow this [direct link to the quota request form](https://aka.ms/oai/stuquotarequest).

## Create a provisioned deployment

To create a provisioned deployment, see [Quickstart: Create a provisioned throughput deployment](../provisioned-quickstart.md).

PTU quota is shared across all provisioned deployments of the same deployment type within a region. If you have remaining quota after your initial deployment, you can use it to deploy other supported models without requesting more quota. Check your quota usage by going to **Management center** > **Quota** > **Provisioned throughput** in the Foundry portal.

You can manage your quota by [requesting additional quota](https://aka.ms/oai/stuquotarequest), or by deleting existing deployments to free up PTUs for new deployments.


[!INCLUDE [how-to-provisioned-get-started-2](../../../foundry/openai/includes/how-to-provisioned-get-started-2.md)]

