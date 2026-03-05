---
title: Find features in the Foundry portal
description: Learn where to find model deployments, playgrounds, and admin settings in the Microsoft Foundry portal if you're familiar with the classic experience.
author: sdgilley
ms.author: sgilley
ms.reviewer: sgilley
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 03/05/2026
ms.custom:
  - classic-and-new
  - build-2025
ai-usage: ai-assisted
#customer intent: As a developer familiar with the classic Foundry portal, I want to find my model deployments, playgrounds, and admin settings in the current Foundry portal.
---

# Find features in the Foundry portal

If you're accustomed to Microsoft Foundry (classic), the current Foundry portal reorganizes navigation from a single left pane into five top-level sections: **Home**, **Discover**, **Build**, **Operate**, and **Docs**. Each section has its own left-pane navigation. This article maps common classic-portal locations to their current equivalents so you can find what you need quickly.

The classic portal uses a single customizable left pane for all navigation, with **Management center** at the bottom. The current portal splits features across five top-level sections, each with its own left pane. **Home**, **Discover**, and **Build** are scoped to your selected project. **Operate** shows information for all your projects.

| Section | Scope | What you find there |
| --- | --- | --- |
| **Home** | Selected project | Project overview and quick actions |
| **Discover** | Selected project | Model catalog and model benchmarks |
| **Build** | Selected project | Agents, models, playgrounds, evaluations, fine-tuning |
| **Operate** | All projects | Admin, quota, compliance, fleet health, tracing |
| **Docs** | N/A | Documentation links |

The following table maps frequently used locations in the classic portal to their current equivalents.

| Task | Classic portal location | Current portal location |
| --- | --- | --- |
| View model deployments | **Models + endpoints** in the left pane | **Build** > **Models** |
| Open a playground | **Playgrounds** in the left pane | **Build** > **Models** > select a model |
| Build agents | **Agents** in the left pane | **Build** > **Agents** |
| Browse the model catalog | **Model catalog** in the left pane | **Discover** > **Model catalog** |
| View evaluations | **Evaluation** in the left pane | **Build** > **Evaluations** |
| Fine-tune a model | **Fine-tuning** in the left pane | **Build** > **Fine-tuning** |
| Tracing and monitoring | **Tracing** in the left pane | **Operate** > **Tracing** |
| Manage quotas | **Management center** > **Quota** | **Operate** > **Quota** |
| Manage users and permissions | **Management center** > **Users** | **Operate** > **Admin** |
| View all projects and resources | **Management center** > **All resources** | **Operate** > **Admin** |
| Connected resources | **Management center** > **Connected resources** | **Operate** > **Admin** > select a project |
| Guardrails and content filters | **Guardrails + controls** in the left pane | **Operate** > **Compliance** |

## Prerequisites

- An Azure account with an active subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A [Foundry project](create-projects.md).

## Find model deployments

In the classic portal, select **Models + endpoints** from the left pane to see all deployed models. In the current portal, model deployments are under **Build**.

1. Select **Build** from the top navigation bar.
1. Select **Models** from the left pane.

The page lists all model deployments for your selected project.

## Find model playgrounds

In the classic portal, **Playgrounds** is a standalone item in the left pane. In the current portal, model playgrounds are accessed through the models list.

1. Select **Build** from the top navigation bar.
1. Select **Models** from the left pane.
1. Select a deployed model to open its details and interact with it in the playground.

## Find agent playgrounds

In the classic portal, you access the agent playground from the **Agents** item in the left pane. In the current portal, agent playgrounds are also under **Build**.

1. Select **Build** from the top navigation bar.
1. Select **Agents** from the left pane.
1. Select an agent to open its playground, or create a new agent to start a playground session.

## Find management center features

In the classic portal, the **Management center** appears at the bottom of the left pane for quotas, user management, and resource configuration. In the current portal, these capabilities move to the **Operate** section, which shows information for all your projects.

1. Select **Operate** from the top navigation bar.
1. Select **Admin** from the left pane to manage projects, users, and connected resources.
1. Select **Quota** from the left pane to manage model quotas and usage.

## Switch between portal experiences

You can switch between the classic and current portal experiences at any time. The toggle preserves your current context, such as the project you're working in.

> [!TIP]
> The current portal shows only Foundry projects. If you need to access hub-based projects or other resource types, switch back to the classic portal.

1. Look for the **New Foundry** toggle in the top banner.
1. Select the toggle to switch between the classic and current experiences.
1. The page reloads with the selected portal interface.


## Related content

- [What is Microsoft Foundry?](../what-is-foundry.md)
- [Use a screen reader with Microsoft Foundry](../tutorials/screen-reader.md)
