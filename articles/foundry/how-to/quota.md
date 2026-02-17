---
title: "Manage and increase quotas for resources (temp)"
description: "This article provides instructions on how to manage and increase quotas for resources with Microsoft Foundry. (temp)"
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.custom:
  - classic-and-new
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: how-to
ms.date: 10/30/2025
ms.reviewer: haakar
reviewer: haakar
ms.author: mopeakande
author: msakande 
manager: nitinme
ai-usage: ai-assisted
# Customer intent: As a Microsoft Foundry user, I want to know how to manage and increase quotas for resources with Microsoft Foundry.
---

# Manage and increase quotas for resources with Microsoft Foundry (Foundry projects) (temp)

Quota provides the flexibility to actively manage the allocation of rate limits across the deployments within your subscription. This article walks through the process of managing quota for your Foundry Models (Foundry projects).

Azure uses limits and quotas to prevent budget overruns due to fraud and to honor Azure capacity constraints. It's also a good way for admins to control costs. Consider these limits as you scale for production workloads. 

In this article, you learn about: 

- Viewing your quotas and limits 
- Requesting quota and limit increases 

## Foundry shared quota 

Foundry provides a pool of shared quota that different users across various regions can use concurrently. Depending on availability, users can temporarily access quota from the shared pool and use the quota to perform testing for a limited amount of time. The specific time duration depends on the use case. By temporarily using quota from the quota pool, you no longer need to file a support ticket for a short-term quota increase or wait for your quota request to be approved before you can proceed with your workload. 

You can use the shared quota pool for testing inferencing for Foundry Models from the model catalog. Use the shared quota only for creating temporary test endpoints, not production endpoints. For endpoints in production, you should [request dedicated quota](#view-and-request-quotas-in-foundry-portal). Billing for shared quota is usage-based. 

## View and request quotas in Foundry portal

Use quotas to manage model quota allocation between multiple [!INCLUDE [fdp](../includes/fdp-project-name.md)]s in the same subscription.

1. [!INCLUDE [version-sign-in](../includes/version-sign-in.md)]
 
1. Projects help organize your work. The project you're working on appears in the upper-left corner. If you want to create a new project, select the project name, then **Create new project**.

1. Select **Operate** from the upper-right navigation.

1. Select **Quota** from the left pane to land on the **Quota** pane. Here, you can view your quota on the **Token per minute** tab and view provisioned models on the **Provisioned throughput unit** tab. 

1. Select any of the deployments in the list to open its details pane on the right side. 

1. On the deployment's details pane, go to the **Affiliated deployments using shared quota** section. Select the pencil icon in the **Actions** column of the table to edit quota allocation for the deployment and free up unused quota or increase allocation as needed.

1. Select the **Request quota** button in the upper-right corner to request increases in quota for the standard deployment type.

## Related content

- [Create a project](../how-to/create-projects.md)
