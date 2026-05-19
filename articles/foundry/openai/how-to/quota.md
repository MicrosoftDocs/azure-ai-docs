---
title: "Manage Azure OpenAI in Microsoft Foundry Models quota"
description: "Learn how to use Azure OpenAI to control your deployments rate limits."
author: alvinashcraft
ms.reviewer: shiyingfu
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: how-to
ms.date: 05/04/2026
ms.author: aashcraft
ms.custom: classic-and-new

#CustomerIntent: As a developer or AI practitioner, I want to understand how to manage Azure OpenAI deployment quotas in Microsoft Foundry so that I can control rate limits for my models.
---

# Manage Azure OpenAI in Microsoft Foundry Models quota

[!INCLUDE [quota 1](../includes/quota-1.md)]

## View and request quotas in Foundry portal

Use quotas to manage model quota allocation between multiple [!INCLUDE [fdp](../../includes/fdp-project-name.md)]s in the same subscription.

1. [!INCLUDE [version-sign-in](../../includes/version-sign-in.md)]
 
1. Projects help organize your work. The project you're working on appears in the upper-left corner. If you want to create a new project, select the project name, then **Create new project**.

1. Select **Operate** from the upper-right navigation.

1. Select **Quota** from the left pane to land on the **Quota** pane. The quota view has two tabs:

    - **Token per minute** — View and manage token-per-minute (TPM) quota allocations for standard deployments.
    - **Provisioned throughput unit** — View and manage provisioned throughput unit (PTU) allocations for provisioned deployments, including capacity estimation tools.

1. Select any of the deployments in the list to open its details pane on the right side. The details pane shows the deployment's current quota allocation, usage, and affiliated deployments.

1. On the deployment's details pane, go to the **Affiliated deployments using shared quota** section. Select the pencil icon in the **Actions** column of the table to edit quota allocation for the deployment and free up unused quota or increase allocation as needed.

1. Select the **Request quota** button in the upper-right corner to request increases in quota for the standard deployment type.

> [!NOTE]
> After you edit a quota allocation or submit a request, allow up to 15 minutes for changes to propagate. Refresh the **Quota** page to verify the updated allocation.

[!INCLUDE [quota 2](../includes/quota-2.md)]
