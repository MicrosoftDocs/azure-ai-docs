---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 12/27/2024
ms.custom: include
---

The general pattern for assigning role-based access control (RBAC) for any resource is:

1. Navigate to the Azure portal for the given resource. 
1. From the left page in the Azure portal, select **Access control (IAM)**. 
1. Select **+ Add** > **Add role assignment**.
1. Search for the role you need to assign and select it. Then select **Next**.
1. When assigning a role to yourself: 
    1. Select **User, group, or service principal**. 
    1. Select **Select members**.
    1. Search for your name and select it.
1. When assigning a role to another resource: 
    1. Select **Managed identity**. 
    1. Select **Select members**.
    1. Use the dropdown to find the type of resource you want to assign. For example, **Foundry Tools** or **Search service**.
    1. Select the resource from the list that appears. There might only be one, but you still need to select it.
1. Continue through the wizard and select **Review + assign** to add the role assignment.