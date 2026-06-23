---
title: "Connect to your own storage"
ms.reviewer: andyaviles
description: "Learn how to bring your own storage to Microsoft Foundry for agents, evaluations, datasets, and other capabilities."
# customer intent: As a developer, I want to set up capability hosts for agents so that I can use my own storage instead of Microsoft-managed storage.
author: s-polly
ms.author: scottpolly
ms.service: microsoft-foundry
ms.subservice: foundry-platform
ms.custom:
  - ignite-2024, build-2025
  - classic-and-new
  - doc-kit-assisted
ms.topic: how-to
ms.date: 05/12/2026
ai-usage: ai-assisted
---

# Connect to your own storage

[!INCLUDE [bring-your-own-azure-storage-foundry 1](../includes/how-to-bring-your-own-azure-storage-foundry-1.md)]

## Create a storage connection

1. [!INCLUDE [version-sign-in](../includes/version-sign-in.md)]
1. Select **Operate** in the upper-right navigation.
1. Select **Admin** in the left pane.
1. Select your project name in the **Manage all projects** list.
1. Select **Add connection** in the upper-right corner.
1. In the list of available services, select **Azure Storage**.
1. Browse for and select your Azure Storage account, choose an **Authentication** type, and then select **Add connection**.

> [!NOTE]
> Azure portal (portal.azure.com) steps are version-agnostic and intentionally not wrapped in moniker blocks.

[!INCLUDE [bring-your-own-azure-storage-foundry 2](../includes/how-to-bring-your-own-azure-storage-foundry-2.md)]

[!INCLUDE [bring-your-own-azure-storage-foundry 3](../includes/how-to-bring-your-own-azure-storage-foundry-3.md)]
