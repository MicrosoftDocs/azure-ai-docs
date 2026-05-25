---
title: "Manage traffic with spillover for provisioned deployments (classic)"
description: "Learn how to configure spillover for provisioned deployments of Azure OpenAI models to automatically route overflow requests to a standard deployment and reduce disruptions during traffic bursts. (classic)"
#customer intent: As a developer, I want to enable spillover for my provisioned deployments so that I can manage traffic bursts effectively.
author: msakande
ms.author: mopeakande
ms.service: microsoft-foundry
ms.subservice: foundry-models
ms.reviewer: seramasu
reviewer: rsethur
ms.topic: how-to
ms.date: 05/25/2026
ms.custom:
  - dev-focus
  - classic-and-new
  - doc-kit-assisted
ai-usage: ai-assisted
#CustomerIntent: As a developer, I want to manage traffic bursts on my provisioned deployments by routing overage traffic to standard deployments using spillover.
ROBOTS: NOINDEX, NOFOLLOW
---


# Manage traffic with spillover for provisioned deployments (classic)

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../../foundry/openai/how-to/spillover-traffic-management.md)

[!INCLUDE [how-to-spillover-traffic-management-1](../../../foundry/openai/includes/how-to-spillover-traffic-management-1.md)]

## Enable spillover for all requests on a provisioned deployment

# [Foundry portal](#tab/portal)

First, create a provisioned throughput deployment. See [Use the Foundry portal for deployment](../provisioned-quickstart.md#use-the-foundry-portal-for-deployment).

Once you have a provisioned deployment, update it to enable traffic spillover as follows: 

1. [!INCLUDE [classic-sign-in](../../../foundry/includes/classic-sign-in.md)]
1. Select the subscription and the Foundry resource in the region where you deployed your model.
1. In the Foundry portal, on the left navigation menu, select **Models + endpoints** > **Model deployments**.
1. Select the deployment.
1. Select **Edit** on the deployment page.
1. Update the deployment to enable **Traffic spillover**.

    > [!NOTE]
    > To enable spillover, your account must have at least one active pay-as-you-go deployment that matches the model and version of your current provisioned deployment.

1. Submit changes.


[!INCLUDE [how-to-spillover-traffic-management-2](../../../foundry/openai/includes/how-to-spillover-traffic-management-2.md)]
