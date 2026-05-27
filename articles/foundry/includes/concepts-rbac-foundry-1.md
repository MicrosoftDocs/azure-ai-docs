---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: meerakurup
ms.author: sgilley
ms.service: microsoft-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Minimum role assignments to get started

For new users to Azure and Microsoft Foundry, start with these minimum assignments so both your user principal and project managed identity can access Foundry features.

You can verify current assignments by using [Check access for a user to a single Azure resource](/azure/role-based-access-control/check-access?tabs=default).

* Assign the **Foundry User** role on your Foundry resource to your **user principal**.

  [!INCLUDE [role-rename-note](./role-rename-note.md)]
* Assign the **Foundry User** role on your Foundry resource to your **project's managed identity**.

If the user who created the project can assign roles (for example, by having the Azure **Owner** role at subscription or resource group scope), both assignments are added automatically.

To assign these roles manually, use the following quick steps.

### Assign a role to your user principal

In the Azure portal, open your Foundry resource and go to **Access control (IAM)**. Create a role assignment for **Foundry User**, set **Members** to **User, group, or service principal**, select your user principal, and then select **Review + assign**.

### Assign a role to your project's managed identity 

In the Azure portal, open your Foundry project and go to **Access control (IAM)**. Create a role assignment for **Foundry User**, set **Members** to **Managed identity**, select your project's managed identity, and then select **Review + assign**.

## Terminology for role-based access control in Foundry

To understand role-based access control in Microsoft Foundry, consider two questions for your enterprise. 

* What permissions do I want my team to have when building in Microsoft Foundry?
* At what scope do I want to assign permissions to my team?

To help answer these questions, here are descriptions of some terminology used throughout this article. 

* **Permissions**: Allowed or denied actions that an identity can perform on a resource, such as reading, writing, deleting, or managing both control plane and data plane operations.
* **Scope**: The set of Azure resources to which a role assignment applies. Typical scopes include subscription, resource group, Foundry resource, or Foundry project.
* **Role**: A named collection of permissions that defines which actions can be performed on Azure resources at a given scope.

An identity gets a *role* with specific *permissions* at a selected *scope* based on your enterprise requirements.

In Microsoft Foundry, consider two scopes when completing role assignments. 

* **Foundry resource**: The top-level scope that defines the administrative, security, and monitoring boundary for a Microsoft Foundry environment.
* **Foundry project**: A sub-scope within a Foundry resource used to organize work and enforce access control for Foundry APIs, tools, and developer workflows.

## Built-in roles

A **built-in role** in Foundry is a role created by Microsoft that covers common access scenarios that you can assign to your team members. Key built-in roles used across Azure include Owner, Contributor, and Reader. These roles aren't specific to Foundry resource permissions. 

For Foundry resources, use additional built-in roles to follow least-privilege access principles. The following table lists key built-in roles for Foundry and links to the exact role definitions in [AI + Machine Learning built-in roles](/azure/role-based-access-control/built-in-roles/ai-machine-learning).

|Role|Description|
|---|---|
|**Foundry User**|Grants reader access to Foundry project, Foundry resource, and data actions for your Foundry project. If you can assign roles, this role is assigned to you automatically. Otherwise, your subscription Owner or a user with role assignment permissions grants it. Least privilege access role in Foundry.|
|**Foundry Project Manager**|Lets you perform management actions on Foundry projects, build and develop with projects, and conditionally assign the Foundry User role to other user principals.|
|**Foundry Account Owner**|Grants full access to manage projects and resources, and lets you conditionally assign the Foundry User, ACR, and monitoring roles to other user principals.|
|**Foundry Owner**|Grants full access to manage projects and resources and build and develop with projects. Lets you conditionally assign the Foundry User, ACR, and monitoring roles. Highly privileged self-serve role designed for digital natives.|

> [!NOTE]
> Don't assign built-in roles that start with **Cognitive Services**. These roles are designed for accessing AI Services resources directly and don't apply to Foundry scenarios.
> Similarly, don't use the **Azure AI Developer** role for Foundry work. Despite the name, this role is scoped to Azure Machine Learning workspaces and Foundry hubs, not to Foundry projects or Foundry hosted agents. For Foundry project access, use **Foundry User** or **Foundry Owner** instead.