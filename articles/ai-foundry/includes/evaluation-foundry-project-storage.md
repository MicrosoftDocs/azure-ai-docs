---
title: Include file
description: Include file
author: lgayhardt
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 7/23/2025
ms.author: lagayhar
ms.custom: include file
---

If this is your first time running evaluations and logging it to your Microsoft Foundry project, you might need to do a few additional steps:

1. Create and connect your storage account to your Foundry project at the resource level. There are two ways you can do this. You can [use a Bicep template](https://github.com/azure-ai-foundry/foundry-samples/blob/main/infrastructure/infrastructure-setup-bicep/01-connections/connection-storage-account.bicep), which provisions and connects a storage account to your Foundry project with key authentication.
    ::: moniker range="foundry-classic"
    You can also [manually create and provision access](../how-to/evaluations-storage-account.md) to your storage account in the Azure portal.
    ::: moniker-end
1. Make sure the connected storage account has access to all projects.
1. If you connected your storage account with Microsoft Entra ID, make sure to give managed identity **Storage Blob Data Owner** permissions to both your account and the Foundry project resource in the Azure portal.