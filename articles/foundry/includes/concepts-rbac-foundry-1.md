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

## Minimum role assignments to get started

For new users to Azure and Microsoft Foundry, start with these minimum assignments so both your user principal and project managed identity can access Foundry features.

You can verify current assignments by using [Check access for a user to a single Azure resource](/azure/role-based-access-control/check-access?tabs=default).

* Assign the **Azure AI User** role on your Foundry resource to your **user principal**.
* Assign the **Azure AI User** role on your Foundry resource to your **project's managed identity**.

If the user who created the project can assign roles (for example, by having the Azure **Owner** role at subscription or resource group scope), both assignments are added automatically.

To assign these roles manually, use the following quick steps.

### Assign a role to your user principal

In the Azure portal, open your Foundry resource and go to **Access control (IAM)**. Create a role assignment for **Azure AI User**, set **Members** to **User, group, or service principal**, select your user principal, and then select **Review + assign**.

### Assign a role to your project's managed identity 

In the Azure portal, open your Foundry project and go to **Access control (IAM)**. Create a role assignment for **Azure AI User**, set **Members** to **Managed identity**, select your project's managed identity, and then select **Review + assign**.

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
