---
title: "High availability and resiliency for Microsoft Foundry projects and Agent Services (classic)"
description: "Learn how to plan for high availability and resiliency for Microsoft Foundry projects and Agent Service. (classic)"
ms.service: azure-ai-foundry
ms.topic: how-to
ms.author: jburchel 
author: jonburchel 
ms.reviewer: andyaviles
ms.date: 02/24/2026
ms.custom:
  - dev-focus
  - classic-and-new
ai-usage: ai-assisted
ROBOTS: NOINDEX, NOFOLLOW
---

# High availability and resiliency for Microsoft Foundry projects and Agent Services (classic)

**Currently viewing:** :::image type="icon" source="../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../foundry/how-to/high-availability-resiliency.md)

[!INCLUDE [feature-preview](../../foundry/includes/feature-preview.md)]

Plan ahead to maintain business continuity and prepare for disaster recovery with [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs).

Microsoft strives to ensure that Azure services are always available. However, unplanned service outages might occur. Create a disaster recovery plan to handle regional service outages. In this article, you learn how to:

* Plan a multi-region deployment of Foundry and associated resources.
* Maximize your chances to recover logs, notebooks, Docker images, and other metadata.
* Design your solution for high availability.
* Fail over to another region.

> [!IMPORTANT]
> Foundry itself doesn't provide automatic failover or disaster recovery.

> [!NOTE]
> The information in this article applies only to **[!INCLUDE [fdp](../../foundry/includes/fdp-project-name.md)]**. For disaster recovery for **[!INCLUDE [hub](../includes/hub-project-name.md)]**, see [Disaster recovery for Foundry hubs](hub-disaster-recovery.md).

[!INCLUDE [high-availability-resiliency 1](../../foundry/includes/how-to-high-availability-resiliency-1.md)]
