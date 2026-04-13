---
title: "Connect to your own storage (classic)"
ms.reviewer: andyaviles
description: "Learn how to bring your own storage to Microsoft Foundry for agents, evaluations, datasets, and other capabilities. (classic)"
# customer intent: As a developer, I want to set up capability hosts for agents so that I can use my own storage instead of Microsoft-managed storage.
author: jonburchel
ms.author: jburchel
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2024, build-2025
  - classic-and-new
ms.topic: how-to
ms.date: 02/24/2026
ai-usage: ai-assisted
ROBOTS: NOINDEX, NOFOLLOW
---

# Connect to your own storage (classic)

**Currently viewing:** :::image type="icon" source="../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../foundry/how-to/bring-your-own-azure-storage-foundry.md)

[!INCLUDE [bring-your-own-azure-storage-foundry 1](../../foundry/includes/how-to-bring-your-own-azure-storage-foundry-1.md)]

## Create a storage connection

1. [!INCLUDE [version-sign-in](../includes/version-sign-in.md)]
1. Select your project.
1. In the left pane, select **Connections** (or **Connected resources**).

   > [!NOTE]
   > The **Connections** or **Connected resources** option might not be available in all versions of the classic Foundry portal. If you don't see this option, use the [current Foundry portal](../../foundry/how-to/bring-your-own-azure-storage-foundry.md) for the latest storage connection experience.

1. Select **+ New connection**.
1. Choose **Azure Blob Storage**.
1. Provide:
   - Name
   - Subscription
   - Storage account
   - Authentication method (system-assigned managed identity recommended)
1. Select **Create**.

The connection is now available to Agents (when not overridden), Evaluations, Datasets, Content Understanding, Speech, and Language.

> [!NOTE]
> Azure portal (portal.azure.com) steps are version-agnostic and intentionally not wrapped in moniker blocks.

[!INCLUDE [bring-your-own-azure-storage-foundry 2](../../foundry/includes/how-to-bring-your-own-azure-storage-foundry-2.md)]

## Configure Content Understanding

1. [!INCLUDE [version-sign-in](../includes/version-sign-in.md)]
1. Open the resource.
1. In the left pane, select **Content Understanding**.
1. Choose the existing storage connection.

> [!NOTE]
> Programmatic configuration options for Content Understanding are under evaluation.

[!INCLUDE [bring-your-own-azure-storage-foundry 3](../../foundry/includes/how-to-bring-your-own-azure-storage-foundry-3.md)]
