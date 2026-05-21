---
title: Include file
description: Include file for custom code training prerequisites
author: soumyapatro
ms.author: soumyapatro
ms.service: microsoft-foundry
ms.topic: include
ms.date: 05/19/2026
ms.custom: include
---

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Foundry project. For more information, see [Create a project](../how-to/create-projects.md).
- A minimum role of **Foundry User** on the Foundry resource. This role is sufficient for submitting jobs, uploading datasets, and registering model assets. Elevated permissions are required for creating compute clusters, model deployments, and project connections. For more information, see [RBAC in Foundry](../concepts/rbac-foundry.md).

  [!INCLUDE [role-rename-note](role-rename-note.md)]

- A GPU compute cluster attached to your project. For more information, see [Set up compute for training](../training/setup-compute.md).
- (Optional) If you use data from your own Azure Blob Storage account, add a storage connection to your project. For more information, see [Connect to your own storage](../how-to/bring-your-own-azure-storage-foundry.md).
- (Optional) If you use a custom Docker image from Azure Container Registry (ACR), configure a user-assigned managed identity (UAMI) on your Foundry project. The UAMI must have appropriate permissions on the Foundry project and all connected resources, including any bring-your-own-storage accounts. At minimum, assign the **AcrPull** role on your ACR resource. For more information, see [Grant your project access to ACR](../training/setup-training-environment.md#grant-your-project-access-to-acr).
