---
title: Role-based access control for Azure AI Foundry
titleSuffix: Azure AI Foundry
description: This article introduces role-based access control in Azure AI Foundry portal.
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: concept-article
ms.date: 09/25/2025
ms.reviewer: deeikele
ms.author: jburchel 
author: jonburchel 
ai.usage: ai-assisted
---

# Role-based access control for Azure AI Foundry

> [!NOTE]
> An alternate hub-focused RBAC article is available: [Role-based access control for Azure AI Foundry (Hubs and Projects)](hub-rbac-azure-ai-foundry.md).

In this article, you learn how to manage access to your [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs) resources. Use Azure role-based access control (Azure RBAC) to manage access to Azure resources, like creating new resources or using existing ones. In Microsoft Entra ID, assign users roles that grant access to resources. Azure provides built-in roles and lets you create custom roles.

If the built-in Azure AI Developer role doesn't meet your needs, you can create a [custom role](#create-custom-roles-for-projects).

> [!WARNING]
> Applying some roles might limit UI functionality in the Azure AI Foundry portal for other users. For example, if a user's role doesn't have permission to create a compute instance, the option to create one isn't available in the portal. This behavior is expected and prevents the user from starting actions that return an access denied error.

## Azure AI Foundry project roles

In the Azure AI Foundry portal, there are two levels of access:

- **Account**: The account is home to the infrastructure (including virtual network setup, customer-managed keys, managed identities, and policies) for your Azure AI Foundry resource.
The Azure AI Foundry resource has built-in roles that are available by default for both the account and project. Here's a table of the built-in roles and their permissions.

| Role                     | Description                                                                                                                                                                                                 |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Azure AI User**            | Grants reader access to AI projects, reader access to AI accounts, and data actions for an AI project. If you can assign roles, this role is assigned to you automatically. Otherwise, your subscription Owner or a user with role assignment permissions grants it. |
| **Azure AI Project Manager** | Lets you perform management actions on Azure AI Foundry projects, build and develop with projects, and conditionally assign the Azure AI User role to other user principals.          |
| **Azure AI Account Owner**   | Grants full access to manage AI projects and accounts, and lets you conditionally assign the Azure AI User role to other user principals.      

>[!NOTE]
>To view and purge deleted AI Foundry accounts, you must have Contributor role assigned at the subscription scope.

The key differences between **Azure AI Project Manager** and **Azure AI Account Owner** are the abilities to:

- Create new Azure AI Foundry account resources. Only the **Azure AI Account Owner** can do this.
The second difference appears in the role definitions: the data action `Microsoft.CognitiveServices/*`. This data action lets the user complete any read, write, or delete data actions within a project. The **Azure AI Project Manager** can perform this action, but the **Azure AI Account Owner** can't. Only **Azure AI User** and **Azure AI Project Manager** get data actions for an AI project. Think of **Azure AI Project Manager** as an elevated **Azure AI User**.
 
In addition to these built-in role assignments, there are Azure privileged administrator roles like Owner, Contributor, and Reader. These roles aren't specific to Azure AI Foundry resource permissions, so use the previously described built-in roles for least privilege access.
 
Use the following table to see the privileges for each built-in role, including the Azure privileged administrator roles:

| Built-in role                         | Create Foundry projects | Create Foundry accounts | Build and develop in a project (data actions) | Complete role assignments                          | Reader access to projects and accounts | Manage models |
|--------------------------|-------------------------|--------------------------|-----------------------------------------------|---------------------------------------------------|-----------------------------------------|-----------------------------------------|
| **Azure AI User**        |                         |                          | ✔                                             |                                                 | ✔                                       |                                                 |
| **Azure AI Project Manager** | ✔                     |                          | ✔                                             | ✔ (only assign Azure AI User role)               | ✔                                       |                                                 |
| **Azure AI Account Owner**   | ✔                     | ✔                        |                                               | ✔ (only assign Azure AI User role)               | ✔                                       | ✔                                               |
| **Owner**                | ✔                     | ✔                        |                                               | ✔ (assign any role to any user)                  | ✔                                       | ✔                                               |
| **Contributor**          | ✔                     | ✔                        |                                               |                                                 | ✔                                       | ✔                                               |
| **Reader**               |                         |                          |                                               |                                                 | ✔                                       |                                                 |

## Default roles for the project

### Azure AI User

Here are the permissions for the **Azure AI User** role:

```json
{
    "id": "/providers/Microsoft.Authorization/roleDefinitions/53ca6127-db72-4b80-b1b0-d745d6d5456d",
    "properties": {
        "roleName": "Azure AI User",
        "description": "Grants reader access to AI projects, reader access to AI accounts, and data actions for an AI project.",
        "assignableScopes": ["/"],
        "permissions": [
            {
                "actions": [
                    "Microsoft.CognitiveServices/*/read",
                    "Microsoft.CognitiveServices/accounts/listkeys/action",
                    "Microsoft.Insights/alertRules/read",
                    "Microsoft.Insights/diagnosticSettings/read",
                    "Microsoft.Insights/logDefinitions/read",
                    "Microsoft.Insights/metricdefinitions/read",
                    "Microsoft.Insights/metrics/read",
                    "Microsoft.ResourceHealth/availabilityStatuses/read",
                    "Microsoft.Resources/deployments/*",
                    "Microsoft.Resources/subscriptions/operationresults/read",
                    "Microsoft.Resources/subscriptions/read",
                    "Microsoft.Resources/subscriptions/resourceGroups/read",
                    "Microsoft.Support/*"
                ],
                "notActions": [],
                "dataActions": ["Microsoft.CognitiveServices/*"],
                "notDataActions": []
            }
        ]
    }
}
```

> [!NOTE]
> If only the Azure AI User role is assigned to your user principal and no other Azure built-in roles are assigned, also assign the Reader role on the Azure AI Foundry resource to view your Foundry resource in the Foundry portal. This only applies to the Foundry Portal UX experience.

### Azure AI Project Manager

The Azure AI Account Owner role uses conditional Azure role assignment delegation.
With conditional delegation, the role can assign only the Azure AI User role to user principals in the resource group.
Conditional delegation lets your admin delegate role assignments so teams can start building AI Foundry projects.
To learn more, see [Delegate Azure role assignment management to others with conditions](/azure/role-based-access-control/delegate-role-assignments-portal). 

Here are the permissions for the **Azure AI Project Manager** role:

```json
{
    "id": "/providers/Microsoft.Authorization/roleDefinitions/eadc314b-1a2d-4efa-be10-5d325db5065e",
    "properties": {
        "roleName": "Azure AI Project Manager",
        "description": "Lets you perform developer actions and management actions on Azure AI Foundry Projects. Allows for making role assignments, but limited to Cognitive Service User role.",
        "assignableScopes": [
            "/"
        ],
        "permissions": [
            {
                "actions": [
                    "Microsoft.Authorization/roleAssignments/write",
                    "Microsoft.Authorization/roleAssignments/delete",
                    "Microsoft.CognitiveServices/accounts/*/read",
                    "Microsoft.CognitiveServices/accounts/projects/*",
                    "Microsoft.CognitiveServices/locations/*/read",
                    "Microsoft.Authorization/*/read",
                    "Microsoft.Insights/alertRules/*",
                    "Microsoft.Resources/deployments/*",
                    "Microsoft.Resources/subscriptions/resourceGroups/read"
                ],
                "notActions": [],
                "dataActions": [
                    "Microsoft.CognitiveServices/*"
                ],
                "notDataActions": [],
                "conditionVersion": "2.0",
                "condition": "((!(ActionMatches{'Microsoft.Authorization/roleAssignments/write'})) OR (@Request[Microsoft.Authorization/roleAssignments:RoleDefinitionId] ForAnyOfAnyValues:GuidEquals{53ca6127-db72-4b80-b1b0-d745d6d5456d})) AND ((!(ActionMatches{'Microsoft.Authorization/roleAssignments/delete'})) OR (@Resource[Microsoft.Authorization/roleAssignments:RoleDefinitionId] ForAnyOfAnyValues:GuidEquals{53ca6127-db72-4b80-b1b0-d745d6d5456d}))"
            }
        ]
    }
}
```

## Azure AI Account Owner

The Azure AI Account Owner role utilizes delegated Azure role assignment management to others with conditions. Because of the conditional delegation, the Azure AI Account Owner role can assign only the Azure AI User role to other user principals in the resource group. Conditional delegation allows the admin of your enterprise to delegate the work of role assignments to get started building and developing with AI Foundry projects. For more information on role assignments with conditions, see [Delegate Azure role assignment management to others with conditions](/azure/role-based-access-control/delegate-role-assignments-portal).

The full set of permissions for the new Azure AI Account Owner role is:

```json
{
    "id": "/providers/Microsoft.Authorization/roleDefinitions/e47c6f54-e4a2-4754-9501-8e0985b135e1",
    "properties": {
        "roleName": "Azure AI Account Owner",
        "description": "Grants full access to manage AI projects and accounts. Grants conditional assignment of the Azure AI User role to other user principals.",
        "assignableScopes": [
            "/"
        ],
        "permissions": [
            {
                "actions": [
                    "Microsoft.Authorization/*/read",
                    "Microsoft.Authorization/roleAssignments/write",
                    "Microsoft.Authorization/roleAssignments/delete",
                    "Microsoft.CognitiveServices/*",
                    "Microsoft.Features/features/read",
                    "Microsoft.Features/providers/features/read",
                    "Microsoft.Features/providers/features/register/action",
                    "Microsoft.Insights/alertRules/*",
                    "Microsoft.Insights/diagnosticSettings/*",
                    "Microsoft.Insights/logDefinitions/read",
                    "Microsoft.Insights/metricdefinitions/read",
                    "Microsoft.Insights/metrics/read",
                    "Microsoft.ResourceHealth/availabilityStatuses/read",
                    "Microsoft.Resources/deployments/*",
                    "Microsoft.Resources/deployments/operations/read",
                    "Microsoft.Resources/subscriptions/operationresults/read",
                    "Microsoft.Resources/subscriptions/read",
                    "Microsoft.Resources/subscriptions/resourcegroups/deployments/*",
                    "Microsoft.Resources/subscriptions/resourceGroups/read",
                    "Microsoft.Support/*"
                ],
                "notActions": [],
                "dataActions": [],
                "notDataActions": [],
                "conditionVersion": "2.0",
                "condition": "((!(ActionMatches{'Microsoft.Authorization/roleAssignments/write'})) OR (@Request[Microsoft.Authorization/roleAssignments:RoleDefinitionId] ForAnyOfAnyValues:GuidEquals{53ca6127-db72-4b80-b1b0-d745d6d5456d})) AND ((!(ActionMatches{'Microsoft.Authorization/roleAssignments/delete'})) OR (@Resource[Microsoft.Authorization/roleAssignments:RoleDefinitionId] ForAnyOfAnyValues:GuidEquals{53ca6127-db72-4b80-b1b0-d745d6d5456d}))"
            }
        ]
    }
}
```

## Sample enterprise RBAC setup for projects

This table shows an example of role-based access control (RBAC) for an enterprise Azure AI Foundry resource.

| Persona                  | Role                                      | Purpose                                                                                                                                                                                                                     |
|--------------------------|------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| IT admin                 | Subscription Owner                       | The IT admin ensures the Azure AI Foundry resource meets enterprise standards. Assign managers the **Azure AI Account Owner** role on the resource to let them create new Azure AI Foundry accounts. Assign managers the **Azure AI Project Manager** role on the resource to let them create projects within an account. |
| Managers                 | Azure AI Account Owner on Azure AI Foundry resource | Managers manage the Azure AI Foundry resource, deploy models, audit compute resources, audit connections, and create shared connections. They can't build in projects, but they can assign the **Azure AI User** role to themselves and others to start building. |
| Team lead or lead developer | Azure AI Project Manager on Azure AI Foundry resource | Lead developers create projects for their team and start building in those projects. After you create a project, project owners invite other members and assign the **Azure AI User** role.                                   |
| Team members or developers  | Azure AI User on Azure AI Foundry resource         | Developers build agents in a project.                             |

> [!IMPORTANT]
> Users with the Contributor role can deploy models in Azure AI Foundry.

## Access resources created outside AI Foundry

When you create an AI Foundry resource, built-in role-based access control (RBAC) permissions give you access to the resource. To use resources created outside AI Foundry, make sure both of the following are true:

- The resource has permissions that let you access it.
For example, to use a new Azure Blob Storage account, add the AI Foundry account resource's managed identity to the Storage Blob Data Reader role on that storage account. To use a new Azure AI Search source, add AI Foundry to the Azure AI Search role assignments.


## Manage access with roles for projects

If you're an owner of an Azure AI Foundry account resource, add or remove roles. 1. On the **Home** page in [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs), select your Azure AI Foundry resource.
1. Select **Users** to add or remove users for the resource. Also manage permissions in the [Azure portal](https://portal.azure.com) under **Access Control (IAM)** or by using Azure CLI.

For example, the following command assigns the Azure AI User role to `joe@contoso.com` for the resource group `this-rg` in the subscription with ID `00000000-0000-0000-0000-000000000000`:

```azurecli
az role assignment create --role "Azure AI User" --assignee "joe@contoso.com" --scope /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/this-rg 
```

## Create custom roles for projects

If the built-in roles aren't enough, create a custom role. Custom roles can include read, write, delete, and compute permissions for Azure AI Foundry resources. Make the role available at the project, resource group, or subscription scope.

> [!NOTE]
> You need the Owner role at that scope to create custom roles in that resource.

To create a custom role, use one of the following articles:

- [Azure portal](/azure/role-based-access-control/custom-roles-portal)
- [Azure CLI](/azure/role-based-access-control/custom-roles-cli)
- [Azure PowerShell](/azure/role-based-access-control/custom-roles-powershell)


For more information about custom roles, see the [Azure custom roles](/azure/role-based-access-control/custom-roles) article.

## Use Microsoft Entra groups with Azure AI Foundry

Microsoft Entra ID provides several ways to manage access to resources, applications, and tasks. With Microsoft Entra groups, you can grant access and permissions to a group of users instead of to each individual user. Microsoft Entra groups can be created in the Azure portal for enterprise IT admins to simplify the role assignment process for developers. When you create an Microsoft Entra group, you can minimize the number of role assignments required for new developers working on Foundry projects by assigning the group the required role assignment on the necessary resource.

Complete the following steps to use Entra ID groups with Azure AI Foundry:

1. Navigate to **Groups** in the Azure portal.
1. Create a new **Security** group in the Groups portal.
1. Assign the Owner of the Microsoft Entra group and add individual user
   principles in your organization to the group as Members. Save the
   group.
1. Navigate to the resource that requires a role assignment.
   
   1. **Example:** To build Agents, run traces, and more in Foundry, the minimum privilege ‘Azure AI User’ role must be assigned to your user principle. Assing the ‘Azure AI User’ role to your new Microsoft Entra group so all users in your enterprise can build in Foundry.
   1. **Example:** To use Tracing and Monitoring features in Azure AI Foundry, a ‘Reader’ role assignment on the connected Application Insights resource is required. Assign the ‘Reader’ role to your new Microsoft Entra group so all users in your enterprise can use the Tracing and Monitoring feature.

1. Navigate to Access Control (IAM).
1. Select the role to assign.
1. Assign access to “User, group, or service principle” and select the new Security group.
1. Review and assign. Role assignment now applies to all user principles assigned to the group.

To learn more about Entra ID groups, prerequisites, and limitations, refer to:

- [Learn about groups, group membership, and access in Microsoft Entra](/entra/fundamentals/concept-learn-about-groups).
- [How to manage groups in Microsoft Entra](/entra/fundamentals/how-to-manage-groups).

## Related content

- [Create a project](../how-to/create-projects.md).
- [Add a connection in Azure AI Foundry portal](../how-to/connections-add.md).
