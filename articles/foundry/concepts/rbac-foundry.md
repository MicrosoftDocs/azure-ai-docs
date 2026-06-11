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
ms.date: 06/02/2026
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
|**Foundry User**|✘|✘|✔|✘|✔|✘|✘|
|**Foundry Project Manager**|✘|✘|✔|✔ (only assign Foundry User role)|✔|✘|✔|
|**Foundry Account Owner**|✔|✔|✘|✔ (assign Foundry User, ACR, and monitoring roles)|✔|✔|✘|
|**Foundry Owner**|✔|✔|✔|✔ (assign Foundry User, ACR, and monitoring roles)|✔|✔|✔|

[!INCLUDE [role-rename-note](../includes/role-rename-note.md)]

Use the following table to see the permissions allowed for each key Azure built-in roles (Owner, Contributor, Reader). 

|Built-in role|Create Foundry projects|Create Foundry accounts|Build and develop in a project (data actions)|Complete role assignments|Reader access to projects and accounts|Manage models|Publish agents|
|---|---|---|---|---|---|---|---|
|**Owner**|✔|✔|✘|✔ (assign any role to any user)|✔|✔|✔|
|**Contributor**|✔|✔|✘|✘|✔|✔|✘|
|**Reader**|✘|✘|✘|✘|✔|✘|✘|

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

## Deployment type–specific permissions

The following sections cover the permission surface for specific deployment types. Use them alongside the built-in role tables in [Permissions for each built-in role](#permissions-for-each-built-in-role) when planning role assignments for a particular workload.

### Managed compute control-plane operations

[Managed compute deployments (Preview)](managed-compute-overview.md) are governed by their own set of Azure resource provider operations under the `Microsoft.CognitiveServices` provider. These operations control who can create, read, update, and delete a managed compute deployment, and who can read the available accelerator capacity and quota usage for a Foundry account.

This section lists the five required control-plane operations, the built-in roles that grant them, and how the role-to-permission mapping differs from standard (pay-per-token and PTU) deployments.

> [!NOTE]
> The operations in this section govern the **control plane** — creating, configuring, and deleting deployments. To call a deployment at inference time, assign the **Foundry User** role on the Foundry account scope (or use the account API key). See [Authentication and Authorization in Foundry](authentication-authorization-foundry.md).

#### Required operations

Five operations are required to fully manage managed compute deployments on a Foundry account:

| Operation | Description |
|---|---|
| `Microsoft.CognitiveServices/accounts/managedComputeDeployments/read` | Read or list managed compute deployments on a Foundry account. |
| `Microsoft.CognitiveServices/accounts/managedComputeDeployments/write` | Create or update a managed compute deployment. |
| `Microsoft.CognitiveServices/accounts/managedComputeDeployments/delete` | Delete a managed compute deployment. |
| `Microsoft.CognitiveServices/locations/managedComputeCapacities/read` | List available accelerator capacity by region. |
| `Microsoft.CognitiveServices/locations/usages/read` | Read accelerator usage and quota consumption. |

> [!IMPORTANT]
> A root-level operation `Microsoft.CognitiveServices/capacities/read` does **not** exist. Custom roles that grant capacity reads must use the location-scoped `locations/managedComputeCapacities/read` operation (or `managedComputeCapacities/read` if scoped at the root of the provider). A wildcard such as `Microsoft.CognitiveServices/locations/*/read` matches `locations/usages/read` but does **not** match `locations/managedComputeCapacities/read`. List the operation explicitly when authoring a custom role.

#### Role-to-permission mapping

The following table shows which built-in roles grant each of the five managed compute control-plane operations.

| Role | `managedComputeDeployments/read` | `managedComputeDeployments/write` | `managedComputeDeployments/delete` | `managedComputeCapacities/read` | `usages/read` |
|---|:---:|:---:|:---:|:---:|:---:|
| **Cognitive Services Contributor** | ✔ | ✔ | ✔ | ✔ | ✔ |
| **Cognitive Services User** | ✔ | ✘ | ✘ | ✔ | ✔ |
| **Foundry Owner** | ✔ | ✔ | ✔ | ✔ | ✔ |
| **Foundry Account Owner** | ✔ | ✔ | ✔ | ✔ | ✔ |
| **Foundry Project Manager** | ✔ | ✘ | ✘ | ✔ | ✔ |
| **Foundry User** | ✔ | ✘ | ✘ | ✔ | ✔ |

The Azure built-in **Owner** and **Contributor** roles grant all five operations through their wildcard action grant on the subscription or resource group.

#### Comparison: standard deployments vs managed compute deployments

The control-plane permission surface for managed compute deployments mirrors the surface for standard (pay-per-token and PTU) deployments; the operation names differ only by the resource type segment (`deployments` vs `managedComputeDeployments`, and `modelCapacities` vs `managedComputeCapacities`).

The following table summarizes how each role's CRUD coverage compares across the two deployment families:

| Role | Standard deployments CRUD | Managed compute deployments CRUD | Difference |
|---|---|---|---|
| Cognitive Services Contributor | Full | Full | Same |
| Cognitive Services User | Read-only | Read-only | Same |
| Foundry Owner | Full | Full | Same |
| Foundry Account Owner | Full | Full | Same |
| Foundry Project Manager | Read + capacities + usages | Read + capacities + usages | Same |
| Foundry User | Read + capacities + usages | Read + capacities + usages | Same |

> [!NOTE]
> If you author a custom role that uses a `locations/*/read` wildcard to grant capacity reads for standard deployments, that wildcard does not cover `managedComputeCapacities/read`. Add `Microsoft.CognitiveServices/locations/managedComputeCapacities/read` to the custom role explicitly to grant capacity reads on the managed compute control plane.

#### Recommended role assignments

Use the following starting points when assigning access for these operations with managed compute:

- **Deploy and operate managed compute deployments**: assign **Cognitive Services Contributor** on the Foundry account scope.
- **Read-only viewer for deployments and quota**: assign **Cognitive Services User** or **Foundry User** on the Foundry account scope.
- **Manage a Foundry project but not deploy models**: assign **Foundry Project Manager** on the Foundry account scope. Project Managers can read deployments and quota but cannot create or delete them.
- **Call a managed compute deployment with Microsoft Entra ID at inference time**: assign **Foundry User** on the Foundry account scope, in addition to whatever control-plane role the user holds (or with no control-plane role at all for inference-only users).

For the end-to-end deployment workflow, see [Deploy open-source models with managed compute](../how-to/deploy-models-managed.md).

## Related content

- [Create a project](../how-to/create-projects.md).
- [Check access for a user to a single Azure resource](/azure/role-based-access-control/check-access?tabs=default).
- [Authentication and Authorization in Foundry](../concepts/authentication-authorization-foundry.md).
- [Disable preview features in Microsoft Foundry](../how-to/disable-preview-features.md).
- [Hosted agent permissions reference](../agents/concepts/hosted-agent-permissions.md).

[!INCLUDE [rbac-foundry 4](../includes/concepts-rbac-foundry-4.md)]
