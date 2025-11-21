---
title: Role-based access control for Microsoft Foundry
titleSuffix: Microsoft Foundry
description: This article introduces role-based access control in Microsoft Foundry portal.
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: concept-article
ms.date: 11/18/2025
ms.reviewer: deeikele
ms.author: jburchel 
author: jonburchel 
monikerRange: 'foundry-classic || foundry'
ai.usage: ai-assisted
---

# Role-based access control for Microsoft Foundry

[!INCLUDE [version-banner](../includes/version-banner.md)]

::: moniker range="foundry-classic"
> [!TIP]
> An alternate hub-focused RBAC article is available: [Role-based access control for Microsoft Foundry (Hubs and Projects)](hub-rbac-azure-ai-foundry.md).

In this article, you learn how to manage access to your [Foundry](https://ai.azure.com/?cid=learnDocs) resources. Use Azure role-based access control (Azure RBAC) to manage access to Azure resources, like creating new resources or using existing ones. In Microsoft Entra ID, assign users roles that grant access to resources. Azure provides built-in roles and lets you create custom roles.

::: moniker-end

::: moniker range="foundry"

In this article, you learn how to manage access to your [!INCLUDE [foundry-link](../default/includes/foundry-link.md)] resources. Use Azure role-based access control (Azure RBAC) to manage access to Azure resources, like creating new resources or using existing ones. In Microsoft Entra ID, assign users roles that grant access to resources. Azure provides built-in roles and lets you create custom roles.

::: moniker-end

If the built-in Azure AI User role doesn't meet your needs, you can create a [custom role](#create-custom-roles-for-projects).

> [!WARNING]
> Applying some roles might limit UI functionality in the Foundry portal for other users. For example, if a user's role doesn't have permission to create a compute instance, the option to create one isn't available in the portal. This behavior is expected and prevents the user from starting actions that return an access denied error.

## Foundry project roles

In the Foundry portal, there are two levels of access:

- **Account**: The account is home to the infrastructure (including virtual network setup, customer-managed keys, managed identities, and policies) for your Foundry resource.
- **Project**: The project is where the developer begins to build with Foundry, such as build Agents, run evaluations, and more. 
The Foundry resource has built-in roles that are available by default for both the account and project. Here's a table of the built-in roles and their permissions.

| Role                     | Description                                                                                                                                                                                                 |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Azure AI User**            | Grants reader access to AI projects, reader access to AI accounts, and data actions for an AI project. If you can assign roles, this role is assigned to you automatically. Otherwise, your subscription Owner or a user with role assignment permissions grants it. |
| **Azure AI Project Manager** | Lets you perform management actions on Foundry projects, build and develop with projects, and conditionally assign the Azure AI User role to other user principals.          |
| **Azure AI Account Owner**   | Grants full access to manage AI projects and accounts, and lets you conditionally assign the Azure AI User role to other user principals. |
| **Azure AI Owner**    | Grants full access to managed AI projects and accounts and build and develop with projects. |

>[!NOTE]
> The Azure AI Owner role is not currently available to assign but will be available to assign in the Azure and Foundry portal soon. 

:::image type="content" source="../media/how-to/network/detailed-rbac-diagram.png" alt-text="Diagram of the built-in roles in Foundry." lightbox="../media/how-to/network/detailed-rbac-diagram.png":::

>[!NOTE]
>To view and purge deleted Foundry accounts, you must have Contributor role assigned at the subscription scope.

In addition to these built-in role assignments, there are Azure privileged administrator roles like Owner, Contributor, and Reader. These roles aren't specific to Foundry resource permissions, so use the previously described built-in roles for least privilege access.
 
Use the following table to see the privileges for each built-in role, including the Azure privileged administrator roles:

| Built-in role                         | Create Foundry projects | Create Foundry accounts | Build and develop in a project (data actions) | Complete role assignments                          | Reader access to projects and accounts | Manage models |
|--------------------------|-------------------------|--------------------------|-----------------------------------------------|---------------------------------------------------|-----------------------------------------|-----------------------------------------|
| **Azure AI User**        |                         |                          | ✔                                             |                                                 | ✔                                       |                                                 |
| **Azure AI Project Manager** | ✔                     |                          | ✔                                             | ✔ (only assign Azure AI User role)               | ✔                                       |                                                 |
| **Azure AI Account Owner**   | ✔                     | ✔                        |                                               | ✔ (only assign Azure AI User role)               | ✔                                       | ✔                                               |
| **Azure AI  Owner**   | ✔                     | ✔                        | ✔                                               | ✔                                               | ✔                                       | ✔                                               |
| **Owner**                | ✔                     | ✔                        |                                               | ✔ (assign any role to any user)                  | ✔                                       | ✔                                               |
| **Contributor**          | ✔                     | ✔                        |                                               |                                                 | ✔                                       | ✔                                               |
| **Reader**               |                         |                          |                                               |                                                 | ✔                                       |                                                 |

## Built-in roles for the project

### Azure AI User

The Azure AI User role is the least-privilege access role in Foundry, granting only the required control plane access. Here are the permissions for the **Azure AI User** role:

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
> If you have permissions to role assign in Azure (ex. Owner role assigned on the account scope) to your user principle, and you deploy a Foundry resource from the Azure portal or Foundry portal UI, then the Azure AI User role gets automatically assigned to your user principle. This is not applicable when deploying Foundry from SDK or CLI. Additionally, in the Foundry portal, the only role assignment you can give to other team members is a combination of the Azure AI User role and the Azure AI Account Owner role. For suggestions on what to role assign depending on your access isolation requirements, see below on Access Isolation. 

### Azure AI Project Manager

The Azure AI Project Manager role uses conditional Azure role assignment delegation.
With conditional delegation, the role can assign only the Azure AI User role to user principals in the resource group.
Conditional delegation lets your admin delegate role assignments so teams can start building Foundry projects.
To learn more, see [Delegate Azure role assignment management to others with conditions](/azure/role-based-access-control/delegate-role-assignments-portal). 

Here are the permissions for the **Azure AI Project Manager** role:

```json
{
    "id": "/providers/Microsoft.Authorization/roleDefinitions/eadc314b-1a2d-4efa-be10-5d325db5065e",
    "properties": {
        "roleName": "Azure AI Project Manager",
        "description": "Lets you perform developer actions and management actions on Foundry Projects. Allows for making role assignments, but limited to Cognitive Service User role.",
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

The Azure AI Account Owner role utilizes delegated Azure role assignment management to others with conditions. Because of the conditional delegation, the Azure AI Account Owner role can assign only the Azure AI User role to other user principals in the resource group. Conditional delegation allows the admin of your enterprise to delegate the work of role assignments to get started building and developing with Foundry projects. For more information on role assignments with conditions, see [Delegate Azure role assignment management to others with conditions](/azure/role-based-access-control/delegate-role-assignments-portal).

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
## Azure AI Owner

The Azure AI  Owner role is for enterprises looking for a self-serve built-in role that allows for all actions from creating a Foundry resource and deploying models to building Agents and running evaluations in Foundry. This role will be available to assign soon. 

The full set of permissions for the new Azure AI Owner role is:

```json
{ 
    "id": "/providers/Microsoft.Authorization/roleDefinitions/", 
    "properties": { 
        "roleName": "Azure AI Owner", 
        "description": " Grants full to manage AI project and accounts. Grants reader access to AI projects, reader access to AI accounts, and data actions for an AI project.", 
        "assignableScopes": [ 
            "/" 
        ], 
        "permissions": [ 
            { 
                "actions": [ 
                    "Microsoft.Authorization/*/read", 
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
                "dataActions": [
                     "Microsoft.CognitiveServices/*" 
                ], 
                "notDataActions": [] 
            } 
        ] 
    } 
}
```

## Sample enterprise RBAC setup for projects

This table shows an example of role-based access control (RBAC) for an enterprise Foundry resource.

| Persona                  | Role                                      | Purpose                                                                                                                                                                                                                     |
|--------------------------|------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| IT admin                 | Subscription Owner                       | The IT admin ensures the Foundry resource meets enterprise standards. Assign managers the **Azure AI Account Owner** role on the resource to let them create new Foundry accounts. Assign managers the **Azure AI Project Manager** role on the resource to let them create projects within an account. |
| Managers                 | Azure AI Account Owner on Foundry resource | Managers manage the Foundry resource, deploy models, audit compute resources, audit connections, and create shared connections. They can't build in projects, but they can assign the **Azure AI User** role to themselves and others to start building. |
| Team lead or lead developer | Azure AI Project Manager on Foundry resource | Lead developers create projects for their team and start building in those projects. After you create a project, project owners invite other members and assign the **Azure AI User** role.                                   |
| Team members or developers  | Azure AI User on Foundry project        | Developers build agents in a project.                             |

> [!IMPORTANT]
> Users with the Contributor role can deploy models in Foundry.

### Access Isolation Examples

Each organization may have different access isolation requirements depending on the user personas in their enterprise. Access isolation refers to which users in your enterprise are given what role assignments for either a separation of permissions using our built-in roles or a unified, highly permissive role. There are three access isolation options for Foundry that you can select for your organization depending on your access isolation requirements. These role assignments may be assigned on different scopes, either the Foundry account or the Foundry project. 

1) No access isolation. This means in your enterprise you do not have any requirements separating permissions between a developer, project manager, or an admin. The permissions for these roles can be assigned across teams. 

Therefore, you should...
* Grant all users in your enterprise the **Contributor** and **Azure AI User** role on the account level  

2) Partial access isolation. This means the project manager in your enterprise should be able to develop within projects as well as create projects. But your admins should not be able to develop within Foundry, only create Foundry projects and accounts. 

Therefore, you should...
* Grant your admin with** Azure AI Account Owner** on the account level
* Grant your developer and project managers with **Azure AI Project Manager** role and **Reader** role on the account level

3) Full access isolation. This means your admins, project managers, and developers have clear permissions assigned that do not overlap for their different functions within an enterprise. 

Therefore you should...
* Grant your admin the **Azure AI Account Owner** on account level
* Grant your developer the **Reader** role on Account and **Azure AI User** on project level
* Grant your project manager the **Azure AI Project Manager** role on account level


## Access resources created outside Foundry

When you create a Foundry resource, built-in role-based access control (RBAC) permissions give you access to the resource. To use resources created outside Foundry, make sure both of the following are true:

- The resource has permissions that let you access it.
For example, to use a new Azure Blob Storage account, add the Foundry account resource's managed identity to the Storage Blob Data Reader role on that storage account. To use a new Azure AI Search source, add Foundry to the Azure AI Search role assignments.

## Manage access with roles for projects

If you're an owner of a Foundry account resource, add or remove roles.

::: moniker range="foundry-classic"
In the Azure Foundry AI portal, you can manage permissions by:

1. On the **Home** page in [Foundry](https://ai.azure.com/?cid=learnDocs), select your Foundry resource.
1. Select **Users** to add or remove users for the resource.
::: moniker-end

You can manage permissions in the [Azure portal](https://portal.azure.com) under **Access Control (IAM)** or by using Azure CLI.

For example, the following command assigns the Azure AI User role to `joe@contoso.com` for the resource group `this-rg` in the subscription with ID `00000000-0000-0000-0000-000000000000`:

```azurecli
az role assignment create --role "Azure AI User" --assignee "joe@contoso.com" --scope /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/this-rg 
```

## Create custom roles for projects

If the built-in roles aren't enough, create a custom role. Custom roles can include read, write, and delete permissions for Foundry resources. Make the role available at the project, resource group, or subscription scope.

> [!NOTE]
> You need the Owner role at that scope to create custom roles in that resource.
 
In order to create a custom role, it is important to know what permissions in Foundry will block certain scenarios or features in Foundry. Below are the collection of permissions per scenario or feature which can be added to either the notActions or notDataActions of a custom role created for more scoped user role.

### Resource Provisioning Permissions

The following permissions are related to resource provisioning. The permissions are mostly control plane, or actions. 

#### Permissions to create Foundry resource
A user provisions a new Foundry resource or project. They might set up a workspace for a new team or define resource group and subscription settings.
  
Actions
- _*/write (granted by Contributor role)_
- _Microsoft.CognitiveServices/accounts/*_
- _Microsoft.Resources/subscriptions/resourceGroups/write*_


#### Permissions to create a Foundry project 
A user provisions a new Foundry project. 
Actions
- _Microsoft.CognitiveServices/accounts/projects/read_
- _Microsoft.CognitiveServices/accounts/projects/write_
- _Microsoft.CognitiveServices/accounts/projects/delete_


#### Permissions to view cost management
A user reviews spend and usage reports. They might check cost breakdown for model training vs inference, analyze consumption trends for budgeting, or export cost data for finance teams.

Actions
- _Microsoft.CostManagement/*/read_
- _Microsoft.Consumption/*/read_

#### Permissions to deploy an Agent to a web app
A user publishes an Agent as a web application. They might deploy to Azure App Service for customer-facing use, configure authentication and scaling settings, or integrate with enterprise identity (Entra ID).

Actions
- _Microsoft.Web/sites/*_ (for App Service) 
- _Microsoft.Resources/deployments/*_ 
- _Microsoft.Authorization/*/read_ 


#### Permissions to deploy a model (Model catalog)
A user takes a trained or fine-tuned model and makes it available for inference. They might deploy as a real-time endpoint, set up autoscaling and networking rules, or apply governance policies for production use.

Actions
- _Microsoft.CognitiveServices/accounts/deployments/read_
- _Microsoft.CognitiveServices/accounts/deployments/write_
- _Microsoft.CognitiveServices/accounts/deployments/delete_

DataActions
- _Microsoft.CognitiveServices/accounts/AIServices/deployments/read_

#### Permissions to create and read connections 
A user integrates Foundry with external or internal resources using connections in Foundry. 

DataActions
- _Microsoft.CognitiveServices/accounts/AIServices/connections/read_
- _Microsoft.CognitiveServices/accounts/AIServices/connections/listSecrets/action_
Actions
- _Microsoft.CognitiveServices/accounts/connections/*_
- _Microsoft.CognitiveServices/accounts/projects/connections/*_

### Consumption Permissions
The following permissions are related to consuming Foundry. The permissions are mostly data plane, or dataActions. 

> [!NOTE]
> Across the board, for any of these scenarios, a basic read permission on the Foundry account/project is required. Hence consider the required Action across all scenarios is having this permission, in addition to the required dataActions: “Microsoft.CognitiveServices/accounts/*/read”

#### Permissions to view telemetry / tracing
A user wants to monitor system health and performance for Foundry resources. They might check logs for troubleshooting model deployments, view metrics like latency, error rates, or throughput, query diagnostic data in Application Insights. 

DataActions 
- _Microsoft.OperationalInsights/workspaces/search/action_
- _Microsoft.Support/*_
- _Microsoft.Insights/alertRules/read_
- _Microsoft.Insights/diagnosticSettings/read_
- _Microsoft.Insights/logDefinitions/read_
- _Microsoft.Insights/metricdefinitions/read_
- _Microsoft.Insights/metrics/read_

Actions
- _Microsoft.Insights/*/read_ (for control-plane access to monitoring resources)

Other Built-in roles assignment for App Insights resource: 
- _Monitoring Reader_
- _Monitoring Contributor_

For more on the built-in roles for Monitoring, see [Azure built-in roles for Monitor](/azure/role-based-access-control/built-in-roles/monitor#monitoring-reader). 

#### Permissions to fine-tune model
A user customizes a base model for their domain-specific data. They might upload training datasets, start a fine-tuning run on an LLM, or monitor progress and retrieve the tuned model for deployment.

DataActions
- _Microsoft.CognitiveServices/accounts/AIServices/fine_tuning/read_
- _Microsoft.CognitiveServices/accounts/AIServices/fine_tuning/write_
- _Microsoft.CognitiveServices/accounts/AIServices/fine_tuning/delete_

#### Permissions to build Agents
A user creates Agents in Foundry. They might deploy an Agent with a model, add tools or connectors (e.g., Azure AI Search, Logic Apps), or configure orchestration logic for multi-step tasks.

DataActions
- _Microsoft.CognitiveServices/accounts/AIServices/agents/read_
- _Microsoft.CognitiveServices/accounts/AIServices/agents/write_
- _Microsoft.CognitiveServices/accounts/AIServices/agents/delete_

#### Permissions for batch inferencing in Foundry
A user sends requests to a deployed model for predictions. They might call REST APIs for scoring, run batch inference on large datasets, validate outputs for accuracy and compliance.

DataActions: 
- _Microsoft.CognitiveServices/accounts/OpenAI/batch-jobs/read_
- _Microsoft.CognitiveServices/accounts/OpenAI/batches/read_
- _Microsoft.CognitiveServices/accounts/OpenAI/batches/delete_
- _Microsoft.CognitiveServices/accounts/OpenAI/batches/cancel/action_

Actions: 
- _Microsoft.CognitiveServices/accounts/deployments/read_
- _Microsoft.CognitiveServices/accounts/deployments/write_
- _Microsoft.CognitiveServices/accounts/deployments/completions/action_

#### Permissions using Azure AI Search
A user enables search-based retrieval for Foundry Agents or apps. They might create and manage indexes, or query documents for RAG (Retrieval-Augmented Generation) scenarios.

DataActions
- _Microsoft.Search/searchServices/indexes/*_
- _Microsoft.Search/searchServices/query/action_
  
Actions
- _Microsoft.Search/searchServices/*/read_
- _Microsoft.Search/searchServices/*/write_

Other Built-in roles assignment on the Search resource: 
- _Search Service Contributor_ (manage indexes and settings)
- _Search Index Data Contributor_ (read/write index data) 
- _Search Index Data Reader_ (least privilege read-only access for queries)

For more on the Azure AI Search built-in roles, see [Connect using Azure roles - Azure AI Search.](/azure/search/search-security-rbac?tabs=roles-portal-admin%2Croles-portal%2Croles-portal-query%2Ctest-portal%2Ccustom-role-portal)

#### Permissions to call Logic Apps in Foundry
A user integrates workflow automation into Foundry. They might, trigger a Logic App when an Agent completes a task, call external APIs via Logic App connector, or automate notifications or data movement. 

DataActions
- _Microsoft.Logic/workflows/run/action_
- _Microsoft.Logic/workflows/read_

Actions
- _Microsoft.Logic/workflows/*/read_
- _Microsoft.Logic/workflows/*/write_
- _Microsoft.Logic/workflows/*/action_
  
Built-in roles assignment on the Logic Apps resource:
- _Logic App Contributor_
- _Logic App Operator_
  
For more details on creating a custom role, see one of the following articles:

- [Azure portal](/azure/role-based-access-control/custom-roles-portal)
- [Azure CLI](/azure/role-based-access-control/custom-roles-cli)
- [Azure PowerShell](/azure/role-based-access-control/custom-roles-powershell)

## Use Microsoft Entra groups with Foundry

Microsoft Entra ID provides several ways to manage access to resources, applications, and tasks. With Microsoft Entra groups, you can grant access and permissions to a group of users instead of to each individual user. Microsoft Entra groups can be created in the Azure portal for enterprise IT admins to simplify the role assignment process for developers. When you create a Microsoft Entra group, you can minimize the number of role assignments required for new developers working on Foundry projects by assigning the group the required role assignment on the necessary resource.

Complete the following steps to use Entra ID groups with Foundry:

1. Navigate to **Groups** in the Azure portal.
1. Create a new **Security** group in the Groups portal.
1. Assign the Owner of the Microsoft Entra group and add individual user
   principles in your organization to the group as Members. Save the
   group.
1. Navigate to the resource that requires a role assignment.
   
   1. **Example:** To build Agents, run traces, and more in Foundry, the minimum privilege ‘Azure AI User’ role must be assigned to your user principle. Assign the ‘Azure AI User’ role to your new Microsoft Entra group so all users in your enterprise can build in Foundry.
   1. **Example:** To use Tracing and Monitoring features in Azure AI Foundry, a ‘Reader’ role assignment on the connected Application Insights resource is required. Assign the ‘Reader’ role to your new Microsoft Entra group so all users in your enterprise can use the Tracing and Monitoring feature.


1. Navigate to Access Control (IAM).
1. Select the role to assign.
1. Assign access to “User, group, or service principle” and select the new Security group.
1. Review and assign. Role assignment now applies to all user principles assigned to the group.

To learn more about Entra ID groups, prerequisites, and limitations, refer to:

- [Learn about groups, group membership, and access in Microsoft Entra](/entra/fundamentals/concept-learn-about-groups).
- [How to manage groups in Microsoft Entra](/entra/fundamentals/how-to-manage-groups).

## Related content

::: moniker range="foundry-classic"

- [Create a project](../how-to/create-projects.md).
- [Add a connection in Foundry portal](../how-to/connections-add.md).

::: moniker-end

::: moniker range="foundry"

[Create a project](../how-to/create-projects.md).

::: moniker-end
