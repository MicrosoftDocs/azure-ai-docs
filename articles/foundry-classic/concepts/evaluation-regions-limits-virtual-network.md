---
title: "Rate limits, region support, and enterprise features for evaluation (classic)"
description: "Learn about region availability, rate limits, virtual network support, and using your own storage account for evaluation in Microsoft Foundry. (classic)"
author: lgayhardt
ms.author: lagayhar
ms.reviewer: skohlmeier
ms.date: 02/10/2026
ms.topic: how-to
ms.service: azure-ai-foundry
ms.custom:
  - references_regions
  - classic-and-new
ROBOTS: NOINDEX, NOFOLLOW
---

# Rate limits, region support, and enterprise features for evaluation (classic)

**Currently viewing:** :::image type="icon" source="../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../foundry/concepts/evaluation-regions-limits-virtual-network.md)

[!INCLUDE [evaluation-regions-limits-virtual-network 1](../../foundry/includes/concepts-evaluation-regions-limits-virtual-network-1.md)]

## Bring your own storage

You can  use your own storage account to run evaluations.

You can either use a Bicep template or [manually create and provision access](../how-to/evaluations-storage-account.md) to your storage account in the Azure portal. To use a Bicep template, follow these steps.
1. Create and connect your storage account to your Foundry project at the resource level. You can [use a Bicep template](https://github.com/microsoft-foundry/foundry-samples/blob/main/infrastructure/infrastructure-setup-bicep/01-connections/connection-storage-account.bicep), which provisions and connects a storage account to your Foundry project with key authentication.
1. Make sure the connected storage account has access to all projects.
1. If you connected your storage account by using Microsoft Entra ID, make sure to give managed identity **Storage Blob Data Owner** permissions to both your account and the Foundry project resource in the Azure portal.

[!INCLUDE [evaluation-regions-limits-virtual-network 2](../../foundry/includes/concepts-evaluation-regions-limits-virtual-network-2.md)]
