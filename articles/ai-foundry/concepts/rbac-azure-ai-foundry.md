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
ms.date: 08/27/2025
ms.reviewer: deeikele
ms.author: jburchel 
author: jonburchel 
zone_pivot_groups: project-type
ai.usage: ai-assisted
---
# Role-based access control for Azure AI Foundry

In this article, you learn how to manage access to your [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs) resources. Use Azure role-based access control (Azure RBAC) to manage access to Azure resources, like creating new resources or using existing ones. In Microsoft Entra ID, assign users roles that grant access to resources. Azure provides built-in roles and lets you create custom roles.

Azure AI Foundry supports two project types: a **[!INCLUDE [fdp](../includes/fdp-project-name.md)]** and a **[!INCLUDE [hub](../includes/hub-project-name.md)]**. To learn about the differences between these types, see [Types of projects](../what-is-azure-ai-foundry.md#project-types). Use the project type selector on this page to switch between project types.

> [!WARNING]
> Applying some roles might limit UI functionality in the Azure AI Foundry portal for other users. For example, if a user's role doesn't have permission to create a compute instance, the option to create one isn't available in the portal. This behavior is expected and prevents the user from starting actions that return an access denied error.

::: zone pivot="fdp-project"

## Azure AI Foundry project roles

In the Azure AI Foundry portal, there are two levels of access:

- **Account**: The account is home to the infrastructure (including virtual network setup, customer-managed keys, managed identities, and policies) for your Azure AI Foundry resource.
The Azure AI Foundry resource has built-in roles that are available by default for both the account and project. Here's a table of the built-in roles and their permissions.

| Role                     | Description                                                                                                                                                                                                 |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Azure AI User**            | Grants reader access to AI projects, reader access to AI accounts, and data actions for an AI project. If you can assign roles, this role is assigned to you automatically. Otherwise, your subscription Owner or a user with role assignment permissions grants it. |
| **Azure AI Project Manager** | Lets you perform management actions on Azure AI Foundry projects, build and develop with projects, and conditionally assign the Azure AI User role to other user principals.          |
| **Azure AI Account Owner**   | Grants full access to manage AI projects and accounts, and lets you conditionally assign the Azure AI User role to other user principals.                                                       |

The key differences between **Azure AI Project Manager** and **Azure AI Account Owner** are the abilities to:

- Create new Azure AI Foundry account resources. Only the **Azure AI Account Owner** can do this.
The second difference appears in the role definitions: the data action `Microsoft.CognitiveServices/*`. This data action lets the user complete any read, write, or delete data actions within a project. The **Azure AI Project Manager** can perform this action, but the **Azure AI Account Owner** can't. Only **Azure AI User** and **Azure AI Project Manager** get data actions for an AI project. Think of **Azure AI Project Manager** as an elevated **Azure AI User**.
 
In addition to these built-in role assignments, there are Azure privileged administrator roles like Owner, Contributor, and Reader. These roles aren't specific to Azure AI Foundry resource permissions, so use the built-in roles above for least privilege access.
 
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
> If only the Azure AI User role is assigned to your user principal and no other Azure built-in roles are assigned, also assign the Reader role on the Azure AI Foundry resource to meet least privilege requirements.

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
| Team lead or lead developer | Azure AI Project Manager on Azure AI Foundry resource | Lead developers create projects for their team and start building in those projects. After creating a project, project owners invite other members and assign the **Azure AI User** role.                                   |
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

## Next steps for projects

- [Create a project](../how-to/create-projects.md)
- [Add a connection in Azure AI Foundry portal](../how-to/connections-add.md)

::: zone-end

::: zone pivot="hub-project"


## Azure AI Foundry hub vs project

In the Azure AI Foundry portal, access has two levels: the hub and the project. The hub hosts infrastructure (including virtual network setup, customer-managed keys, managed identities, and policies). It’s where you configure Azure AI services. Hub access lets you modify infrastructure, create hubs, and create projects. Projects are a subset of the hub and act as workspaces to build and deploy AI systems. In a project, develop flows, deploy models, and manage project assets. Project access lets you build and deploy AI end to end while using the hub infrastructure.

:::image type="content" source="../media/concepts/resource-provider-connected-resources.svg" alt-text="Diagram that shows the relationship between Azure AI Foundry resources.":::

A key benefit of the hub and project relationship is that developers can create projects that inherit hub security settings. Some developers are contributors to a project and can't create new projects.

## Default roles for the hub 

The Azure AI Foundry hub has built-in roles that are available by default. 

Here's a table of the built-in roles and their permissions for the hub:

| Role | Description | 
| --- | --- |
| Owner | Full access to the hub, including the ability to manage hubs, create new hubs, and assign permissions. This role is automatically assigned to the hub creator.|
| Contributor | User has full access to the hub, including the ability to create new hubs, but isn't able to manage hub permissions on the existing resource. |
| Azure AI Administrator | Automatically assigned to the hub's system-assigned managed identity. Grants the minimum permissions the managed identity needs to perform tasks. For more information, see [Azure AI Administrator role](#azure-ai-administrator-role). |
| Azure AI Developer |     Perform all actions except creating new hubs or managing hub permissions. For example, users can create projects, compute, and connections. Users can assign permissions within their project. Users can interact with existing Azure AI resources such as Azure OpenAI, Azure AI Search, and Azure AI services. |
| Azure AI Inference Deployment Operator | Do all actions required to create a resource deployment within a resource group. |
| Reader |     Read-only access to the hub. This role is automatically assigned to all project members within the hub. |

The key difference between Contributor and Azure AI Developer is the ability to create new hubs. If you don't want users to create new hubs (because of quota, cost, or managing how many hubs you have), assign the Azure AI Developer role.

Only the Owner and Contributor roles let you create a hub. At this time, custom roles can't grant you permission to create hubs.

### Azure AI Administrator role

Before 11/19/2024, the system-assigned managed identity created for the hub was automatically assigned the __Contributor__ role for the resource group that contains the hub and projects. Hubs created after this date have the system-assigned managed identity assigned to the __Azure AI Administrator__ role. This role is more narrowly scoped to the minimum permissions needed for the managed identity to perform its tasks.

The __Azure AI Administrator__ role has the following permissions:

```json
{
    "permissions": [
        {
            "actions": [
                "Microsoft.Authorization/*/read",
                "Microsoft.CognitiveServices/*",
                "Microsoft.ContainerRegistry/registries/*",
                "Microsoft.DocumentDb/databaseAccounts/*",
                "Microsoft.Features/features/read",
                "Microsoft.Features/providers/features/read",
                "Microsoft.Features/providers/features/register/action",
                "Microsoft.Insights/alertRules/*",
                "Microsoft.Insights/components/*",
                "Microsoft.Insights/diagnosticSettings/*",
                "Microsoft.Insights/generateLiveToken/read",
                "Microsoft.Insights/logDefinitions/read",
                "Microsoft.Insights/metricAlerts/*",
                "Microsoft.Insights/metricdefinitions/read",
                "Microsoft.Insights/metrics/read",
                "Microsoft.Insights/scheduledqueryrules/*",
                "Microsoft.Insights/topology/read",
                "Microsoft.Insights/transactions/read",
                "Microsoft.Insights/webtests/*",
                "Microsoft.KeyVault/*",
                "Microsoft.MachineLearningServices/workspaces/*",
                "Microsoft.Network/virtualNetworks/subnets/joinViaServiceEndpoint/action",
                "Microsoft.ResourceHealth/availabilityStatuses/read",
                "Microsoft.Resources/deployments/*",
                "Microsoft.Resources/deployments/operations/read",
                "Microsoft.Resources/subscriptions/operationresults/read",
                "Microsoft.Resources/subscriptions/read",
                "Microsoft.Resources/subscriptions/resourcegroups/deployments/*",
                "Microsoft.Resources/subscriptions/resourceGroups/read",
                "Microsoft.Resources/subscriptions/resourceGroups/write",
                "Microsoft.Storage/storageAccounts/*",
                "Microsoft.Support/*",
                "Microsoft.Search/searchServices/write",
                "Microsoft.Search/searchServices/read",
                "Microsoft.Search/searchServices/delete",
                "Microsoft.Search/searchServices/indexes/*",
                "Microsoft.DataFactory/factories/*"
            ],
            "notActions": [],
            "dataActions": [],
            "notDataActions": []
        }
    ]
}
```

> [!TIP]
> We recommend that you convert hubs created before 11/19/2024 to use the Azure AI Administrator role. The Azure AI Administrator role is more narrowly scoped than the previously used Contributor role and follows the principle of least privilege.


- Azure REST API: Use a `PATCH` request to the Azure REST API for the workspace. The body of the request sets `{"properties":{"allowRoleAssignmentOnRG":true}}`. The following example shows a `PATCH` request using `curl`. Replace `{subscription-id}`, `{resource-group-name}`, `{workspace-name}`, and `{access-token}` with the values for your scenario. For more information on using REST APIs, visit the [Azure REST API documentation](/rest/api/azure/).

```bash
curl -X PATCH "https://management.azure.com/subscriptions/{subscription-id}/resourcegroups/{resource-group-name}/providers/Microsoft.MachineLearningServices/workspaces/{workspace-name}?api-version=2024-04-01-preview" -H "Authorization: Bearer {access-token}" -H "Content-Type: application/json" --data '{"properties":{"allowRoleAssignmentOnRG":true}}'
```

- Azure CLI: Use the `az ml workspace update` command with the `--allow-roleassignment-on-rg true` parameter. The following example updates a workspace named `myworkspace`. This command requires the Azure Machine Learning CLI extension version 2.27.0 or later.

```azurecli
az ml workspace update --name myworkspace --allow-roleassignment-on-rg true
```

- Azure Python SDK: Set the `allow_roleassignment_on_rg` property of the Workspace object to `True` and then perform an update operation. The following example updates a workspace named `myworkspace`. This operation requires the Azure Machine Learning SDK version 1.17.0 or later.

```python
ws = ml_client.workspaces.get(name="myworkspace")
ws.allow_roleassignment_on_rg = True
ws = ml_client.workspaces.begin_update(workspace=ws).result()
```

If you encounter problems with the Azure AI Administrator role, you can revert to the Contributor role as a troubleshooting step. For more information, see [Revert to the Contributor role](#revert-to-the-contributor-role).

### Azure AI Developer role

The full set of permissions for the Azure AI Developer role is as follows:

```json
{
    "permissions": [
        {
            "actions": [
                "Microsoft.MachineLearningServices/workspaces/*/read",
                "Microsoft.MachineLearningServices/workspaces/*/action",
                "Microsoft.MachineLearningServices/workspaces/*/delete",
                "Microsoft.MachineLearningServices/workspaces/*/write",
                "Microsoft.MachineLearningServices/locations/*/read",
                "Microsoft.Authorization/*/read",
                "Microsoft.Resources/deployments/*"
            ],
            "notActions": [
                "Microsoft.MachineLearningServices/workspaces/delete",
                "Microsoft.MachineLearningServices/workspaces/write",
                "Microsoft.MachineLearningServices/workspaces/listKeys/action",
                "Microsoft.MachineLearningServices/workspaces/hubs/write",
                "Microsoft.MachineLearningServices/workspaces/hubs/delete",
                "Microsoft.MachineLearningServices/workspaces/featurestores/write",
                "Microsoft.MachineLearningServices/workspaces/featurestores/delete"
            ],
            "dataActions": [
                "Microsoft.CognitiveServices/accounts/OpenAI/*",
                "Microsoft.CognitiveServices/accounts/SpeechServices/*",
                "Microsoft.CognitiveServices/accounts/ContentSafety/*"
            ],
            "notDataActions": []
        }
    ]
}
```

If the built-in Azure AI Developer role doesn't meet your needs, you can create a [custom role](#create-custom-roles-for-hubs).

## Default roles for projects 

Projects in Azure AI Foundry portal have built-in roles that are available by default. 

The following table lists the built-in project roles and descriptions:

| Role | Description | 
| --- | --- |
| Owner | Full access to the project, including assigning permissions to project users. |
| Contributor | Full access to the project, but can't assign permissions to project users. |
| Azure AI Administrator | This role is automatically assigned to the system-assigned managed identity for the hub. The Azure AI Administrator role has the minimum permissions needed for the managed identity to perform its tasks. For more information, see [Azure AI Administrator role](#azure-ai-administrator-role). |
| Azure AI Developer | Performs most actions, including creating deployments, but can't assign permissions to project users. |
| Azure AI Inference Deployment Operator | Perform all actions required to create a resource deployment within a resource group. |
| Reader | Read-only access to the project. |

When you grant a user access to a project (for example, through permission management in the Azure AI Foundry portal), the system also assigns two roles. The first role is the Reader role on the hub. The second role is the Inference Deployment Operator role, which lets the user create deployments in the project's resource group. This role includes these permissions: `Microsoft.Authorization/*/read` and `Microsoft.Resources/deployments/*`.

To complete end-to-end AI development and deployment, users need these two automatically assigned roles and either the Contributor or Azure AI Developer role on the project.

To create a project, you need a role that includes the allowed action `Microsoft.MachineLearningServices/workspaces/hubs/join` on the hub. The Azure AI Developer built-in role includes this permission.

## Dependency service Azure RBAC permissions

The hub has dependencies on other Azure services. The following table lists the permissions required for these services when you create a hub. The person that creates the hub needs these permissions. The person who creates a project from the hub doesn't need them.

| Permission | Purpose |
|------------|-------------|
| `Microsoft.Storage/storageAccounts/write` | Create a storage account with the specified parameters or update the properties or tags or adds custom domain for the specified storage account. |
| `Microsoft.KeyVault/vaults/write` | Create a new key vault or updates the properties of an existing key vault. Certain properties might require more permissions. |
| `Microsoft.CognitiveServices/accounts/write` | Write API Accounts. |
| `Microsoft.MachineLearningServices/workspaces/write` | Create a new workspace or updates the properties of an existing workspace. |

## Sample enterprise RBAC setup for hubs
The following table is an example of how to set up role-based access control for your Azure AI Foundry for an enterprise.

| Persona | Role | Purpose |
| --- | --- | ---|
| IT admin | Owner of the hub | The IT admin can ensure the hub is set up to their enterprise standards. They can assign managers the Contributor role on the resource if they want to enable managers to make new hubs. Or they can assign managers the Azure AI Developer role on the resource to not allow for new hub creation. |
| Managers | Contributor or Azure AI Developer on the hub | Managers can manage the hub, audit compute resources, audit connections, and create shared connections. |
| Team lead/Lead developer | Azure AI Developer on the hub | Lead developers can create projects for their team and create shared resources (such as compute and connections) at the hub level. After project creation, project owners can invite other members. |
| Team members/developers | Contributor or Azure AI Developer on the project | Developers can build and deploy AI models within a project and create assets that enable development such as computes and connections. |

## Access to resources created outside of the hub

- Your hub is allowed to access it. 

For example, if you're trying to consume a new Blob storage, you need to ensure that hub's managed identity is added to the Blob Storage Reader role for the Blob. If you're trying to use a new Azure AI Search source, you might need to add the hub to the Azure AI Search's role assignments. 

## Manage access with roles for hubs 

If you're an owner of a hub, you can add and remove roles for Azure AI Foundry. Go to the **Home** page in [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs) and select your hub. Then select **Users** to add and remove users for the hub. You can also manage permissions from the Azure portal under **Access Control (IAM)** or through the Azure CLI. For example, to assign the Azure AI Developer role to "joe@contoso.com" for resource group "this-rg" in the subscription with an ID of `00000000-0000-0000-0000-000000000000`, you can use the following Azure CLI command: 
 
```azurecli-interactive
az role assignment create --role "Azure AI Developer" --assignee "joe@contoso.com" --scope /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/this-rg 
```

## Create custom roles for hubs

If the built-in roles are insufficient, you can create custom roles. Custom roles might have the read, write, delete, and compute resource permissions in that Azure AI Foundry. You can make the role available at a specific project level, a specific resource group level, or a specific subscription level. 

> [!NOTE]
> You must be an owner of the resource at that level to create custom roles within that resource.

The following JSON example defines a custom Azure AI Foundry developer role at the subscription level:

```json
{
    "properties": {
        "roleName": "Azure AI Foundry Developer",
        "description": "Custom role for Azure AI Foundry. At subscription level",
        "assignableScopes": [
            "/subscriptions/<your-subscription-id>"
        ],
        "permissions": [
            {
                "actions": [
                    "Microsoft.MachineLearningServices/workspaces/write",
                    "Microsoft.MachineLearningServices/workspaces/endpoints/write",
                    "Microsoft.Storage/storageAccounts/write",
                    "Microsoft.Resources/deployments/validate/action",
                    "Microsoft.KeyVault/vaults/write",
                    "Microsoft.Authorization/roleAssignments/read",
                    "Microsoft.Authorization/roleDefinitions/read",
                    "Microsoft.CognitiveServices/*/read"
                ],
                "notActions": [
                    "Microsoft.MachineLearningServices/workspaces/delete",
                    "Microsoft.MachineLearningServices/workspaces/write",
                    "Microsoft.MachineLearningServices/workspaces/listKeys/action",
                    "Microsoft.MachineLearningServices/workspaces/hubs/write",
                    "Microsoft.MachineLearningServices/workspaces/hubs/delete",
                    "Microsoft.MachineLearningServices/workspaces/featurestores/write",
                    "Microsoft.MachineLearningServices/workspaces/featurestores/delete"
                ],
                "dataActions": [
                    "Microsoft.CognitiveServices/accounts/OpenAI/*/read",
                    "Microsoft.CognitiveServices/accounts/OpenAI/engines/completions/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/engines/search/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/engines/generate/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/deployments/search/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/deployments/completions/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/deployments/chat/completions/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/deployments/extensions/chat/completions/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/deployments/embeddings/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/images/generations/action"
                ],
                "notDataActions": []
            }
        ]
    }
}
```

- [Azure PowerShell](/azure/role-based-access-control/custom-roles-powershell)

For more information on creating custom roles in general, visit the [Azure custom roles](/azure/role-based-access-control/custom-roles) article.

## Assigning roles in Azure AI Foundry portal

You can add users and assign roles directly from Azure AI Foundry at either the hub or project level. In the [management center](management-center.md), select **Users** in either the hub or project section, then select **New user** to add a user. 

> [!NOTE]
> You're limited to selecting built-in roles. If you need to assign custom roles, you must use the [Azure portal](/azure/role-based-access-control/role-assignments-portal), [Azure CLI](/azure/role-based-access-control/role-assignments-cli), or [Azure PowerShell](/azure/role-based-access-control/role-assignments-powershell).

:::image type="content" source="../media/concepts/hub-overview-add-user.png" lightbox="../media/concepts/hub-overview-add-user.png" alt-text="Screenshot of the Azure AI Foundry hub overview with the new user button highlighted.":::

You're then prompted to enter the user information and select a built-in role.

:::image type="content" source="../media/concepts/add-resource-users.png" lightbox="../media/concepts/add-resource-users.png" alt-text="Screenshot of the add users prompt with the role set to Azure AI Developer.":::

## Scenario: Use a customer-managed key

When configuring a hub to use a customer-managed key (CMK), an Azure Key Vault is used to store the key. The user or service principal used to create the workspace must have owner or contributor access to the key vault.

If your Azure AI Foundry hub is configured with a **user-assigned managed identity**, the identity must be granted the following roles. These roles allow the managed identity to create the Azure Storage, Azure Cosmos DB, and Azure Search resources used when using a customer-managed key:
- `Microsoft.DocumentDB/databaseAccounts/write`

Within the key vault, the user or service principal must have the create, get, delete, and purge access to the key through a key vault access policy. For more information, see [Azure Key Vault security](/azure/key-vault/general/security-features#controlling-access-to-key-vault-data).

## Scenario: Connections using Microsoft Entra ID authentication

When you create a connection that uses Microsoft Entra ID authentication, you must assign roles to your developers so they can access the resource.

| Resource connection | Role | Description |
|----------|------|-------------|
| Azure AI Search | Contributor | List API-Keys to list indexes from Azure AI Foundry. |
| Azure AI Search | Search Index Data Contributor | Required for indexing scenarios |
| Azure AI services / Azure OpenAI | Cognitive Services OpenAI Contributor | Call public ingestion API from Azure AI Foundry. |
| Azure AI services / Azure OpenAI | Cognitive Services User | List API-Keys from Azure AI Foundry. |
| Azure AI services / Azure OpenAI | Cognitive Services Contributor | Allows for calls to the control plane. |
| Azure Blob Storage | Storage Blob Data Contributor | Required for reading and writing data to the blob storage. |
| Azure Data Lake Storage Gen 2 | Storage Blob Data Contributor | Required for reading and writing data to the data lake. |
| Microsoft OneLake | Contributor | To give someone access to Microsoft OneLake, you must [give them access to your Microsoft Fabric workspace](/fabric/get-started/give-access-workspaces). |

> [!IMPORTANT]
> If you're using Promptflow with Azure Storage (including Azure Data Lake Storage Gen 2), you must also assign the __Storage File Data Privileged Contributor__ role.

When using Microsoft Entra ID authenticated connections in the chat playground, the services need to authorize each other to access the required resources. The admin performing the configuration needs to have the __Owner__ role on these resources to add role assignments. The following table lists the required role assignments for each resource. The __Assignee__ column refers to the system-assigned managed identity of the listed resource. The __Resource__ column refers to the resource that the assignee needs to access. For example, Azure OpenAI has a system-assigned managed identity that needs to be assigned the __Search Index Data Reader__ role for the Azure AI Search resource.

| Role | Assignee | Resource | Description |
|------|----------|----------|-------------|
| Search Index Data Reader | Azure AI services / Azure OpenAI | Azure AI Search | Inference service queries the data from the index. Only used for inference scenarios. |
| Search Index Data Contributor | Azure AI services / Azure OpenAI | Azure AI Search | Read-write access to content in indexes. Import, refresh, or query the documents collection of an index. Only used for ingestion and inference scenarios. |
| Search Service Contributor | Azure AI services / Azure OpenAI | Azure AI Search | Read-write access to object definitions (indexes, aliases, synonym maps, indexers, data sources, and skillsets). Inference service queries the index schema for auto fields mapping. Data ingestion service creates index, data sources, skill set, indexer, and queries the indexer status. |
| Cognitive Services OpenAI Contributor | Azure AI Search | Azure AI services / Azure OpenAI | Custom skill |
| Cognitive Services OpenAI User | Azure OpenAI Resource for chat model | Azure OpenAI resource for embedding model | Required only if using two Azure OpenAI resources to communicate. |
| Storage Blob Data Contributor | Azure AI Search | Azure Storage Account | Reads blob and writes knowledge store. |
| Storage Blob Data Contributor | Azure AI services / Azure OpenAI | Azure Storage Account | Reads from the input container and writes the preprocess results to the output container. |

> [!NOTE]
> The __Cognitive Services OpenAI User__ role is only required if you're using two Azure OpenAI resources: one for your chat model and one for your embedding model. If this applies, enable Trusted Services AND ensure the connection for your embedding model Azure OpenAI resource has Microsoft Entra ID enabled.  

## Scenario: Use an existing Azure OpenAI resource

When you create a connection to an existing Azure OpenAI resource, you must also assign roles to your users so they can access the resource. You should assign either the **Cognitive Services OpenAI User** or **Cognitive Services OpenAI Contributor** role, depending on the tasks they need to perform. For information on these roles and the tasks they enable, see [Azure OpenAI roles](/azure/ai-foundry/openai/how-to/role-based-access-control#azure-openai-roles).

## Scenario: Use Azure Container Registry

An Azure Container Registry instance is an optional dependency for Azure AI Foundry hub. The following table lists the support matrix when authenticating a hub to Azure Container Registry, depending on the authentication method and the __Azure Container Registry's__ [public network access configuration](/azure/container-registry/container-registry-access-selected-networks). 

| Authentication method | Public network access </br>disabled | Azure Container Registry</br>Public network access enabled |
| ---- | :----: | :----: |
| Admin user | ✓ | ✓ |
| Azure AI Foundry hub system-assigned managed identity | ✓ | ✓ |
| Azure AI Foundry hub user-assigned managed identity </br>with the **ACRPull** role assigned to the identity |  | ✓ |

A system-assigned managed identity is automatically assigned to the correct roles when the hub is created. If you're using a user-assigned managed identity, you must assign the **ACRPull** role to the identity.

## Scenario: Use Azure Application Insights for logging

Azure Application Insights is an optional dependency for Azure AI Foundry hub. The following table lists the permissions required if you want to use Application Insights when you create a hub. The person that creates the hub needs these permissions. The person who creates a project from the hub doesn't need these permissions.

| Permission | Purpose |
|------------|-------------|
| `Microsoft.Insights/Components/Write` | Write to an application insights component configuration. |
| `Microsoft.OperationalInsights/workspaces/write` | Create a new workspace or links to an existing workspace by providing the customer ID from the existing workspace. |

## Scenario: Provisioned throughput unit procurer

The following example defines a custom role that can procure [provisioned throughput units (PTU)](/azure/ai-foundry/openai/concepts/provisioned-throughput).

```json
{
    "properties": {
        "roleName": "PTU procurer",
        "description": "Custom role to purchase PTU",
        "assignableScopes": [
            "/subscriptions/<your-subscription-id>"
        ],
        "permissions": [
            {
                "actions": [
                    "Microsoft.CognitiveServices/accounts/commitmentplans/read",
                    "Microsoft.CognitiveServices/accounts/commitmentplans/write",
                    "Microsoft.CognitiveServices/accounts/commitmentplans/delete",
                    "Microsoft.CognitiveServices/locations/commitmentTiers/read",
                    "Microsoft.CognitiveServices/accounts/commitmentplans/read",
                    "Microsoft.CognitiveServices/accounts/commitmentplans/write",
                    "Microsoft.CognitiveServices/accounts/commitmentplans/delete",
                    "Microsoft.Features/features/read",
                    "Microsoft.Features/providers/features/read",
                    "Microsoft.Features/providers/features/register/action",
                    "Microsoft.Insights/logDefinitions/read",
                    "Microsoft.Insights/metricdefinitions/read",
                    "Microsoft.Insights/metrics/read",
                    "Microsoft.ResourceHealth/availabilityStatuses/read",
                    "Microsoft.Resources/deployments/operations/read",
                    "Microsoft.Resources/subscriptions/operationresults/read",
                    "Microsoft.Resources/subscriptions/read",
                    "Microsoft.Resources/subscriptions/resourcegroups/deployments/*",
                    "Microsoft.Resources/subscriptions/resourceGroups/read"
                ],
                "notActions": [],
                "dataActions": [],
                "notDataActions": []
            }
        ]
    }
}
```

## Scenario: Azure OpenAI Assistants API

The following example defines a role for a developer using [Azure OpenAI Assistants](/azure/ai-foundry/openai/how-to/assistant).

```json
{
    "id": "",
    "properties": {
        "roleName": "Azure OpenAI Assistants API Developer",
        "description": "Custom role to work with Azure OpenAI Assistants API",
        "assignableScopes": [
            "<your-scope>"
        ],
        "permissions": [
            {
                "actions": [
                    "Microsoft.CognitiveServices/*/read",
                    "Microsoft.Authorization/roleAssignments/read",
                    "Microsoft.Authorization/roleDefinitions/read"
                ],
                "notActions": [],
                "dataActions": [
                    "Microsoft.CognitiveServices/accounts/OpenAI/*/read",
                    "Microsoft.CognitiveServices/accounts/OpenAI/engines/completions/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/engines/search/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/engines/generate/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/deployments/search/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/deployments/completions/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/deployments/chat/completions/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/deployments/extensions/chat/completions/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/deployments/embeddings/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/images/generations/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/write",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/read",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/delete",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/files/write",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/files/read",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/files/delete",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/threads/write",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/threads/read",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/threads/delete",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/threads/messages/write",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/threads/messages/read",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/threads/messages/files/read",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/threads/runs/write",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/threads/runs/read",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/threads/runs/steps/read"
                ],
                "notDataActions": []
            }
        ]
    }
}
```

## Troubleshooting

### Error: Principal doesn't have access to API/Operation

#### Symptoms

When using the Azure AI Foundry portal chat playground, you receive an error message stating "Principal doesn't have access to API/Operation". The error might also include an "Apim-request-id".

#### Cause

The user or service principal used to authenticate requests to Azure OpenAI or Azure AI Search doesn't have the required permissions to access the resource.

#### Solution

Assign the following roles to the user or service principal. The role you assign depends on the services you're using and the level of access the user or service principal requires:

| Service being accessed | Role | Description |
| --- | --- | --- |
| Azure OpenAI | Cognitive Services OpenAI Contributor | Call public ingestion API from Azure AI Foundry. |
| Azure OpenAI | Cognitive Services User | List API-Keys from Azure AI Foundry. |
| Azure AI Search | Search Index Data Contributor | Required for indexing scenarios. |
| Azure AI Search| Search Index Data Reader | Inference service queries the data from the index. Only used for inference scenarios. |

### Revert to the Contributor role

If you create a new hub and encounter errors with the new default role assignment of Azure AI Administrator for the managed identity, use the following steps to change the hub to the Contributor role:

> [!IMPORTANT]
> We don't recommend reverting a hub to the Contributor role unless you encounter problems. If reverting does solve the problems that you're encountering, open a support incident with information on the problems that reverting solved so that we can invesitage further.
>
> If you would like to revert to the Contributor role as the _default_ for new hubs, open a [support request](https://ms.portal.azure.com/#view/Microsoft_Azure_Support/NewSupportRequestV3Blade) with your Azure subscription details and request that your subscription be changed to use the Contributor role as the default for the system-assigned managed identity of new hubs.

1. Delete the role assignment for the hub's managed-identity. The scope for this role assignment is the __resource group__ that contains the hub, so the role must be deleted from the resource group. 

    > [!TIP]
    > The system-assigned managed identity for the hub is the same as the hub name.

    From the Azure portal, navigate to the __resource group__ that contains the hub. Select __Access control (IAM)__, and then select __Role assignments__. In the list of role assignments, find the role assignment for the managed identity. Select it, and then select __Delete__.

    For information on deleting a role assignment, see [Remove role assignments](/azure/role-based-access-control/role-assignments-remove).

1. Create a new role assignment on the __resource group__ for the __Contributor__ role. When adding this role assignment, select the managed-identity for the hub as the assignee. The name of the system-assigned managed identity is same as the hub name.

    1. From the Azure portal, navigate to the __resource group__ that contains the hub. Select __Access control (IAM)__, and then select __Add role assignment__. 
    1. From the __Role__ tab, select __Contributor__. 
    1. From the __Members__ tab, select __Managed identity__, __+ Select members__, and set the __Managed identity__ dropdown to __Azure AI hub__. In the __Select__ field, enter the name of the hub. Select the hub from the list, and then select __Select__.
    1. From the __Review + assign__ tab, select __Review + assign__.

## Next steps for hubs

- [How to create an Azure AI Foundry hub](../how-to/create-azure-ai-resource.md)
- [How to create an Azure AI Foundry project](../how-to/create-projects.md)
- [How to create a connection in Azure AI Foundry portal](../how-to/connections-add.md)

::: zone-end
