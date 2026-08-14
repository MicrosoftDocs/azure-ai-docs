---
title: include file
description: include file
ai-usage: ai-assisted
author: alvinashcraft
ms.author: aashcraft
ms.service: microsoft-foundry
ms.topic: include
ms.date: 08/06/2026
ms.custom: include, classic-and-new
---

:::image type="content" source="../media/add-model-deployments/models-deploy-deployment-type.png" alt-text="Screenshot of the Foundry portal deployment dialog showing the deployment type selection box with Global Standard selected." lightbox="../media/add-model-deployments/models-deploy-deployment-type.png":::

> [!IMPORTANT]
> **Data residency for all deployment types**: Data stored at rest remains in the designated Azure geography. However, inferencing data is processed as follows:
> - **Global** types: May be processed in any Azure region
> - **Data Zone** types: The service processes data only within the Microsoft-specified data zone (US, EU, or Asia Pacific (APAC)).
> - **Standard (single region)** types: The service processes data in the deployment region.
>
> [Learn more about data residency](https://azure.microsoft.com/explore/global-infrastructure/data-residency/).

## Start with Global Standard

For most workloads, start with **Global Standard**. It launches first when a new model releases, has the lowest price, and offers the broadest region coverage. Move to another deployment type only when you have a specific reason, such as data residency, reserved throughput, or asynchronous batch processing.

New deployment types become available in a set order: Global, then Data Zone, then single region. Single-region deployment types arrive last, have no guaranteed availability date, and depend on capacity that frees up as older models retire. For the authoritative launch order, see [Model launch and availability](../../openai/concepts/model-retirements.md#model-launch-and-availability).

## Deployment type comparison
