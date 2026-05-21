---
title: "Role-based access control for Microsoft Foundry (classic)"
description: "This article introduces role-based access control in Microsoft Foundry portal. (classic)"
ms.service: microsoft-foundry
ms.subservice: foundry-platform
ms.custom:
  - classic-and-new
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: concept-article
ms.date: 04/13/2026
ms.reviewer: meerakurup
ms.author: sgilley 
author: sdgilley 
ai-usage: ai-assisted
ROBOTS: NOINDEX, NOFOLLOW
---

# Role-based access control for Microsoft Foundry (classic)

**Currently viewing:** :::image type="icon" source="../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../foundry/concepts/rbac-foundry.md)

> [!TIP]
> This article is for a Foundry project type. An alternate RBAC article for hub-based projects is available: [Role-based access control for Microsoft Foundry (Hubs and Projects)](hub-rbac-foundry.md).

In this article, you learn about role-based access control (RBAC) in your Microsoft Foundry resource and how to assign roles that control access to resources.  

> [!TIP]
> RBAC roles apply when you authenticate using Microsoft Entra ID. If you use key-based authentication instead, the key grants full access without role restrictions. Microsoft recommends using Entra ID authentication for improved security and granular access control.

[!INCLUDE [rbac-foundry 1](../../foundry/includes/concepts-rbac-foundry-1.md)]


### Permissions for each built-in role

Use the following table and diagram to see the permissions allowed for each built-in role in Foundry, including the key Azure built-in roles. 

|Built-in role|Create Foundry projects|Create Foundry accounts|Build and develop in a project (data actions)|Complete role assignments|Reader access to projects and accounts|Manage models|
|---|---|---|---|---|---|---|
|**Foundry User**|||✔||✔||
|**Foundry Project Manager**|✔||✔|✔ (only assign Foundry User role)|✔||
|**Foundry Account Owner**|✔|✔||✔ (only assign Foundry User role)|✔|✔|
|**Foundry Owner**|✔|✔|✔|✔|✔|✔|
|**Owner**|✔|✔||✔ (assign any role to any user)|✔|✔|
|**Contributor**|✔|✔|||✔|✔|
|**Reader**|||||✔||

[!INCLUDE [role-rename-note](../../foundry/includes/role-rename-note.md)]


[!INCLUDE [rbac-foundry 2](../../foundry/includes/concepts-rbac-foundry-2.md)]

## Manage role assignments

To manage roles in Foundry, you must have permission to assign and remove roles in Azure. The Azure built-in **Owner** role includes that permission. You can assign roles through the Foundry portal (Admin page), Azure portal IAM, or Azure CLI. You can remove roles by using Azure portal IAM or Azure CLI.

In the Foundry portal, manage permissions by:

1. On the **Home** page in [Foundry](https://ai.azure.com/?cid=learnDocs), select your Foundry resource.
1. Select **Users** to add or remove users for the resource.

You can manage permissions in the [Azure portal](https://portal.azure.com) under **Access Control (IAM)** or by using Azure CLI.

For example, the following command assigns the Foundry User role to `joe@contoso.com` for resource group `this-rg` in subscription `00000000-0000-0000-0000-000000000000`:

```azurecli
az role assignment create --role "53ca6127-db72-4b80-b1b0-d745d6d5456d" --assignee "joe@contoso.com" --scope /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/this-rg 
```

[!INCLUDE [role-rename-note-code](../../foundry/includes/role-rename-note-code.md)]

[!INCLUDE [rbac-foundry 3](../../foundry/includes/concepts-rbac-foundry-3.md)]

## Related content

- [Create a project](../how-to/create-projects.md).
- [Add a connection in Foundry portal](../how-to/connections-add.md).
- [Authentication and Authorization in Foundry](../concepts/authentication-authorization-foundry.md).
- [Disable preview features in Microsoft Foundry](../../foundry/how-to/disable-preview-features.md).

[!INCLUDE [rbac-foundry 4](../../foundry/includes/concepts-rbac-foundry-4.md)]
