---
title: "Role-based access control for Microsoft Foundry"
description: "This article introduces role-based access control in Microsoft Foundry portal."
ms.service: azure-ai-foundry
ms.custom:
  - classic-and-new
  - ignite-2023
  - build-2024
  - ignite-2024
  - doc-kit-assisted
ms.topic: concept-article
ms.date: 12/31/2025
ms.reviewer: meerakurup
ms.author: sgilley 
author: sdgilley 
ai-usage: ai-assisted
---

# Role-based access control for Microsoft Foundry

In this article, you learn core role-based access control (RBAC) concepts for Microsoft Foundry, including scopes, built-in roles, and common enterprise assignment patterns.  

> [!TIP]
> RBAC roles apply when you authenticate using Microsoft Entra ID. If you use key-based authentication instead, the key grants full access without role restrictions. Microsoft recommends using Entra ID authentication for improved security and granular access control.

For more information about authentication and authorization in Microsoft Foundry, see [Authentication and Authorization](../concepts/authentication-authorization-foundry.md).

[!INCLUDE [rbac-foundry 1](../includes/concepts-rbac-foundry-1.md)]

## Built-in roles

A **built-in role** in Foundry is a role created by Microsoft that covers common access scenarios that you can assign to your team members. Key built-in roles used across Azure include Owner, Contributor, and Reader. These roles aren't specific to Foundry resource permissions. 

For Foundry resources, use additional built-in roles to follow least-privilege access principles. The following table lists key built-in roles for Foundry and links to the exact role definitions in [AI + Machine Learning built-in roles](/azure/role-based-access-control/built-in-roles/ai-machine-learning).

|Role|Description|
|---|---|
|**Azure AI User**|Grants reader access to Foundry project, Foundry resource, and data actions for your Foundry project. If you can assign roles, this role is assigned to you automatically. Otherwise, your subscription Owner or a user with role assignment permissions grants it. Least privilege access role in Foundry.|
|**Azure AI Project Manager**|Lets you perform management actions on Foundry projects, build and develop with projects, and conditionally assign the Azure AI User role to other user principals.|
|**Azure AI Account Owner**|Grants full access to manage projects and resources, and lets you conditionally assign the Azure AI User role to other user principals.|
|**Azure AI Owner**|Grants full access to managed projects and resources and build and develop with projects. Highly privileged self-serve role designed for digital natives.|

### Permissions for each built-in role

Use the following table to see the permissions allowed for each built-in role in Microsoft Foundry. 

|Built-in role|Create Foundry projects|Create Foundry accounts|Build and develop in a project (data actions)|Complete role assignments|Reader access to projects and accounts|Manage models|
|---|---|---|---|---|---|---|
|**Azure AI User**|||✔||✔||
|**Azure AI Project Manager**|||✔|✔ (only assign Azure AI User role)|✔||
|**Azure AI Account Owner**|✔|✔||✔ (only assign Azure AI User role)|✔|✔|
|**Azure AI Owner**|✔|✔|✔|✔|✔|✔|

Use the following table to see the permissions allowed for each key Azure built-in roles (Owner, Contributor, Reader). 

|Built-in role|Create Foundry projects|Create Foundry accounts|Build and develop in a project (data actions)|Complete role assignments|Reader access to projects and accounts|Manage models|
|---|---|---|---|---|---|---|
|**Owner**|✔|✔||✔ (assign any role to any user)|✔|✔|
|**Contributor**|✔|✔|||✔|✔|
|**Reader**|||||✔||

:::image type="content" source="../media/how-to/network/detailed-rbac-diagram.png" alt-text="Diagram of the built-in roles in Foundry." lightbox="../media/how-to/network/detailed-rbac-diagram.png":::
 
For more on built-in roles in Azure and Foundry, see [Azure built-in roles](/azure/role-based-access-control/built-in-roles). To learn more about conditional delegation used in the Azure AI Account Owner and Azure AI Project Manager role, see [Delegate Azure role assignment management to others with conditions](/azure/role-based-access-control/delegate-role-assignments-portal).

[!INCLUDE [rbac-foundry 2](../includes/concepts-rbac-foundry-2.md)]

## Manage role assignments

To manage roles in Foundry, you must have permission to assign and remove roles in Azure. The Azure built-in **Owner** role includes that permission. You can assign roles through the Foundry portal (Admin page), Azure portal IAM, or Azure CLI. You can remove roles by using Azure portal IAM or Azure CLI.

In the Foundry portal, manage permissions by:

1. Open the **Admin** page in [Foundry](https://ai.azure.com/nextgen), then select **Operate** > **Admin**.
1. Select your project name.
1. Select **Add user** to manage project access. This action is available only if you have role-assignment permissions.
1. Apply the same flow for Foundry resource-level access.

You can manage permissions in the [Azure portal](https://portal.azure.com) under **Access Control (IAM)** or by using Azure CLI.

For example, the following command assigns the Azure AI User role to `joe@contoso.com` for resource group `this-rg` in subscription `00000000-0000-0000-0000-000000000000`:

```azurecli
az role assignment create --role "Azure AI User" --assignee "joe@contoso.com" --scope /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/this-rg 
```

[!INCLUDE [rbac-foundry 3](../includes/concepts-rbac-foundry-3.md)]

## Related content

- [Create a project](../how-to/create-projects.md).
- [Check access for a user to a single Azure resource](/azure/role-based-access-control/check-access?tabs=default).
- [Authentication and Authorization in Foundry](../concepts/authentication-authorization-foundry.md).
- [Disable preview features in Microsoft Foundry](../how-to/disable-preview-features.md).

[!INCLUDE [rbac-foundry 4](../includes/concepts-rbac-foundry-4.md)]
