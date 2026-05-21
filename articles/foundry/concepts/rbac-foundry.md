---
title: "Role-based access control for Microsoft Foundry"
description: "This article introduces role-based access control in Microsoft Foundry portal."
ms.service: microsoft-foundry
ms.subservice: foundry-platform
ms.custom:
  - classic-and-new
  - ignite-2023
  - build-2024
  - ignite-2024
  - doc-kit-assisted
ms.topic: concept-article
ms.date: 04/13/2026
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


### Permissions for each built-in role

Use the following table to see the permissions allowed for each built-in role in Microsoft Foundry. 

|Built-in role|Create Foundry projects|Create Foundry accounts|Build and develop in a project (data actions)|Complete role assignments|Reader access to projects and accounts|Manage models|Publish agents|
|---|---|---|---|---|---|---|---|
|**Foundry User**|||✔||✔|||
|**Foundry Project Manager**|||✔|✔ (only assign Foundry User role)|✔||✔|
|**Foundry Account Owner**|✔|✔||✔ (assign Foundry User, ACR, and monitoring roles)|✔|✔||
|**Foundry Owner**|✔|✔|✔|✔ (assign Foundry User, ACR, and monitoring roles)|✔|✔|✔|

[!INCLUDE [role-rename-note](../includes/role-rename-note.md)]

Use the following table to see the permissions allowed for each key Azure built-in roles (Owner, Contributor, Reader). 

|Built-in role|Create Foundry projects|Create Foundry accounts|Build and develop in a project (data actions)|Complete role assignments|Reader access to projects and accounts|Manage models|Publish agents|
|---|---|---|---|---|---|---|---|
|**Owner**|✔|✔||✔ (assign any role to any user)|✔|✔|✔|
|**Contributor**|✔|✔|||✔|✔||
|**Reader**|||||✔|||

To publish agents, you need the **Foundry Project Manager** role (minimum) on the Foundry resource scope. For more information, see [Agent applications in Microsoft Foundry](../agents/how-to/agent-applications.md).



[!INCLUDE [rbac-foundry 2](../includes/concepts-rbac-foundry-2.md)]

## Manage role assignments

To manage roles in Foundry, you must have permission to assign and remove roles in Azure. The Azure built-in **Owner** role includes that permission. You can assign roles through the Foundry portal (Admin page), Azure portal IAM, or Azure CLI. You can remove roles by using Azure portal IAM or Azure CLI.

In the Foundry portal, manage permissions by:

1. Open the **Admin** page in [Foundry](https://ai.azure.com), then select **Operate** > **Admin**.
1. Select your project name.
1. Select **Add user** to manage project access. This action is available only if you have role-assignment permissions.
1. Apply the same flow for Foundry resource-level access.

You can manage permissions in the [Azure portal](https://portal.azure.com) under **Access Control (IAM)** or by using Azure CLI.

For example, the following command assigns the Foundry User role to `joe@contoso.com` for resource group `this-rg` in subscription `00000000-0000-0000-0000-000000000000`:

```azurecli
az role assignment create --role "53ca6127-db72-4b80-b1b0-d745d6d5456d" --assignee "joe@contoso.com" --scope /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/this-rg 
```

[!INCLUDE [role-rename-note-code](../includes/role-rename-note-code.md)]

[!INCLUDE [rbac-foundry 3](../includes/concepts-rbac-foundry-3.md)]

## Related content

- [Create a project](../how-to/create-projects.md).
- [Check access for a user to a single Azure resource](/azure/role-based-access-control/check-access?tabs=default).
- [Authentication and Authorization in Foundry](../concepts/authentication-authorization-foundry.md).
- [Disable preview features in Microsoft Foundry](../how-to/disable-preview-features.md).
- [Hosted agent permissions reference](../agents/concepts/hosted-agent-permissions.md).

[!INCLUDE [rbac-foundry 4](../includes/concepts-rbac-foundry-4.md)]
