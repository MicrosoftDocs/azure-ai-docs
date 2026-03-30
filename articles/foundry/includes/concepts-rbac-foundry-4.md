---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: meerakurup
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Appendix

### Access Isolation Examples

Each organization may have different access isolation requirements depending on the user personas in their enterprise. Access isolation refers to which users in your enterprise are given what role assignments for either a separation of permissions using our built-in roles or a unified, highly permissive role. There are three access isolation options for Foundry that you can select for your organization depending on your access isolation requirements. 

**No access isolation.** This means in your enterprise, you don't have any requirements separating permissions between a developer, project manager, or an admin. The permissions for these roles can be assigned across teams. 

Therefore, you should...
* Grant all users in your enterprise the **Azure AI Owner** role on the resource scope 

**Partial access isolation.** This means the project manager in your enterprise should be able to develop within projects as well as create projects. But your admins shouldn't be able to develop within Foundry, only create Foundry projects and accounts. 

Therefore, you should...
* Grant your admin with **Azure AI Account Owner** on the resource scope
* Grant your developer and project managers with **Azure AI Project Manager** role on the resource 

**Full access isolation.** This means your admins, project managers, and developers have clear permissions assigned that don't overlap for their different functions within an enterprise. 

Therefore you should...
* Grant your admin the **Azure AI Account Owner** on resource scope
* Grant your developer the **Reader** role on Foundry resource scope and **Azure AI User** on project scope
* Grant your project manager the **Azure AI Project Manager** role on resource scope

### Use Microsoft Entra groups with Foundry

Microsoft Entra ID provides several ways to manage access to resources, applications, and tasks. By using Microsoft Entra groups, you can grant access and permissions to a group of users instead of to each individual user. Enterprise IT admins can create Microsoft Entra groups in the Azure portal to simplify the role assignment process for developers. When you create a Microsoft Entra group, you can minimize the number of role assignments required for new developers working on Foundry projects by assigning the group the required role assignment on the necessary resource.

Complete the following steps to use Microsoft Entra ID groups with Foundry:

1. Create a **Security** group in **Groups** in the Azure portal.
1. Add an owner and the user principals in your organization who need shared access.
1. Open the target resource and go to **Access control (IAM)**.
1. Assign the required role to **User, group, or service principal**, and select the new security group.
1. Select **Review + assign** so the role assignment applies to all members of the group.

Common examples:

* To build agents, run traces, and use core Foundry capabilities, assign **Azure AI User** to the Microsoft Entra group.
* To use Tracing and Monitoring features, assign **Reader** on the connected Application Insights resource to the same group.

To learn more about Microsoft Entra ID groups, prerequisites, and limitations, refer to:

- [Learn about groups, group membership, and access in Microsoft Entra](/entra/fundamentals/concept-learn-about-groups).
- [How to manage groups in Microsoft Entra](/entra/fundamentals/how-to-manage-groups).
