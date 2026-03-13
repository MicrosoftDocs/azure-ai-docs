---
title: "Role-based access control for Microsoft Foundry"
description: "This article introduces role-based access control in Microsoft Foundry portal."
ms.service: azure-ai-foundry
ms.custom:
  - classic-and-new
  - ignite-2023
  - build-2024
  - ignite-2024
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

Use the following table and diagram to see the permissions allowed for each built-in role in Foundry, including the key Azure built-in roles. 

|Built-in role|Create Foundry projects|Create Foundry accounts|Build and develop in a project (data actions)|Complete role assignments|Reader access to projects and accounts|Manage models|
|---|---|---|---|---|---|---|
|**Azure AI User**|||✔||✔||
|**Azure AI Project Manager**|✔||✔|✔ (only assign Azure AI User role)|✔||
|**Azure AI Account Owner**|✔|✔||✔ (only assign Azure AI User role)|✔|✔|
|**Azure AI Owner**|✔|✔|✔|✔|✔|✔|
|**Owner**|✔|✔||✔ (assign any role to any user)|✔|✔|
|**Contributor**|✔|✔|||✔|✔|
|**Reader**|||||✔||

:::image type="content" source="../media/how-to/network/detailed-rbac-diagram.png" alt-text="Diagram of the built-in roles in Foundry." lightbox="../media/how-to/network/detailed-rbac-diagram.png":::
 
For more on built-in roles in Azure and Foundry, see [Azure built-in roles](/azure/role-based-access-control/built-in-roles). To learn more about conditional delegation used in the Azure AI Account Owner and Azure AI Project Manager role, see [Delegate Azure role assignment management to others with conditions](/azure/role-based-access-control/delegate-role-assignments-portal).

## Sample enterprise RBAC mappings for projects

Here's an example of how to implement role-based access control (RBAC) for an enterprise Foundry resource. 

|Persona|Role and Scope|Purpose|
|---|---|---|
|IT admin|Owner on subscription scope|The IT admin ensures the Foundry resource meets enterprise standards. Assign managers the **Azure AI Account Owner** role on the resource to let them create new Foundry accounts. Assign managers the **Azure AI Project Manager** role on the resource to let them create projects within an account.|
|Managers|Azure AI Account Owner on Foundry resource scope|Managers manage the Foundry resource, deploy models, audit compute resources, audit connections, and create shared connections. They can't build in projects, but they can assign the **Azure AI User** role to themselves and others to start building.|
|Team lead or lead developer|Azure AI Project Manager on Foundry resource scope|Lead developers create projects for their team and start building in those projects. After you create a project, project owners invite other members and assign the **Azure AI User** role.|
|Team members or developers|Azure AI User on Foundry project scope and Reader on the Foundry resource scope|Developers build agents in a project with pre-deployed Foundry models and pre-built connections.|

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

## Create custom roles for projects

If the built-in roles don't meet your enterprise requirements, create a custom role that allows for precise control over allowed actions and scopes. Here's an example subscription-level custom role definition:

```json
{
  "properties": {
    "roleName": "My Enterprise Foundry User",
    "description": "Custom role for Foundry at my enterprise to only allow building Agents. Assign at subscription level.",
    "assignableScopes": ["/subscriptions/<your-subscription-id>"],
    "permissions": [ { 
        "actions": ["Microsoft.CognitiveServices/*/read", "Microsoft.Authorization/*/read", "Microsoft.CognitiveServices/accounts/listkeys/action","Microsoft.Resources/deployments/*"], 
        "notActions": [], 
        "dataActions": ["Microsoft.CognitiveServices/accounts/AIServices/agents/*"], 
        "notDataActions": []     
    } ]
  }
}
```

For more information on creating a custom role, see the following articles. 

- [Azure portal](/azure/role-based-access-control/custom-roles-portal)
- [Azure CLI](/azure/role-based-access-control/custom-roles-cli)
- [Azure PowerShell](/azure/role-based-access-control/custom-roles-powershell)
- [Disable preview features in Microsoft Foundry](../how-to/disable-preview-features.md). This article provides more details on specific permissions in Foundry across control and data plane which you can utilize when building custom roles.

## Notes and limitations

* To view and purge deleted Foundry accounts, you must have the Contributor role assigned at the subscription scope.
* Users with the Contributor role can deploy models in Foundry.
* You need the Owner role on a resource's scope to create custom roles in the resource.
* If you have permissions to role assign in Azure (for example, the Owner role assigned on the account scope) to your user principal, and you deploy a Foundry resource from the Azure portal or Foundry portal UI, then the Azure AI User role gets automatically assigned to your user principal. This assignment doesn't apply when deploying Foundry from SDK or CLI. 
* When you create a Foundry resource, the built-in role-based access control (RBAC) permissions give you access to the resource. To use resources created outside Foundry, ensure the resource has permissions that let you access it. Here are some examples: 
    * To use a new Azure Blob Storage account, add the Foundry account resource's managed identity to the Storage Blob Data Reader role on that storage account. 
    * To use a new Azure AI Search source, add Foundry to the Azure AI Search role assignments.
* To fine-tune a model in Foundry, you need both data plane and control plane permissions. Deploying a fine-tuned model is a control plane permission. Therefore, the only built-in role with both data plane and control plane permissions is the **Azure AI Owner** role. Or, if you prefer, you can also assign the **Azure AI User** role for data plane permissions and the **Azure AI Account Owner** role for control plane permissions. 

## Related content

- [Create a project](../how-to/create-projects.md).
- [Check access for a user to a single Azure resource](/azure/role-based-access-control/check-access?tabs=default).
- [Authentication and Authorization in Foundry](../concepts/authentication-authorization-foundry.md).
- [Disable preview features in Microsoft Foundry](../how-to/disable-preview-features.md).

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
