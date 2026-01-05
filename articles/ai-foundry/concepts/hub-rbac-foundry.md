---
title: Role-based access control for Microsoft Foundry (Hubs and Projects)
titleSuffix: Microsoft Foundry
description: This article introduces role-based access control in Microsoft Foundry portal (hub-focused version).
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
  - hub-only
ms.topic: concept-article
ms.date: 12/31/2025
ms.reviewer: deeikele
ms.author: sgilley 
author: sdgilley 
ai-usage: ai-assisted
# Hub-focused copy of RBAC article. Project-only content remains in rbac-foundry.md
---
# Role-based access control for Microsoft Foundry (hub-focused)

[!INCLUDE [uses-hub-only](../includes/uses-hub-only.md)]

> [!TIP]
> An alternate Foundry project-focused RBAC article is available: [Role-based access control for Microsoft Foundry](rbac-foundry.md).

In this article, you learn how to manage access at the hub and project levels of Foundry. Use Azure role-based access control (Azure RBAC) to manage access to Azure resources. Azure provides built-in roles and lets you create custom roles.

## Foundry hub vs project

In the Foundry portal, access has two levels: the hub and the project. The hub hosts infrastructure (including virtual network setup, customer-managed keys, managed identities, and policies). It’s where you configure Foundry Tools. Hub access lets you modify infrastructure, create hubs, and create projects. Projects are a subset of the hub and act as workspaces to build and deploy AI systems. In a project, develop flows, deploy models, and manage project assets. Project access lets you build and deploy AI end to end while using the hub infrastructure.

:::image type="content" source="../media/concepts/resource-provider-connected-resources.svg" alt-text="Diagram that shows the relationship between Foundry resources.":::

A key benefit of the hub and project relationship is that developers can create projects that inherit hub security settings. Some developers are contributors to a project and can't create new projects.

## Default roles for the hub 

The Foundry hub has built-in roles that are available by default. 

| Role | Description | 
| --- | --- |
| Owner | Full access to the hub, including the ability to manage hubs, create new hubs, and assign permissions. This role is automatically assigned to the hub creator.|
| Contributor | User has full access to the hub, including the ability to create new hubs, but isn't able to manage hub permissions on the existing resource. |
| Azure AI Administrator | Automatically assigned to the hub's system-assigned managed identity. Grants the minimum permissions the managed identity needs to perform tasks. |
| Azure AI Developer | Perform all actions except creating new hubs or managing hub permissions. Users can assign permissions within their project. |
| Azure AI Inference Deployment Operator | Do all actions required to create a resource deployment within a resource group. |
| Reader | Read-only access to the hub. This role is automatically assigned to all project members within the hub. |

The key difference between Contributor and Azure AI Developer is the ability to create new hubs. Only the Owner and Contributor roles let you create a hub. Custom roles can't grant hub creation.

### Azure AI Administrator role

Hubs created after 11/19/2024 have the system-assigned managed identity assigned to the __Azure AI Administrator__ role instead of __Contributor__.

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

### Azure AI Developer role

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

## Default roles for projects 

When you grant a user access to a project, the system also assigns the Reader role on the hub and the Inference Deployment Operator role to allow deployments in the resource group.

| Role | Description | 
| --- | --- |
| Owner | Full access to the project, including assigning permissions to project users. |
| Contributor | Full access but can't assign permissions. |
| Azure AI Administrator | Automatically assigned to the hub managed identity. |
| Azure AI Developer | Create deployments; can't assign permissions. |
| Azure AI Inference Deployment Operator | Actions required to create resource deployments. |
| Reader | Read-only access. |

To create a project, a role must include `Microsoft.MachineLearningServices/workspaces/hubs/join` on the hub (included in Azure AI Developer).

## Dependency service permissions

| Permission | Purpose |
|------------|---------|
| `Microsoft.Storage/storageAccounts/write` | Create/update storage account. |
| `Microsoft.KeyVault/vaults/write` | Create/update key vault. |
| `Microsoft.CognitiveServices/accounts/write` | Write API accounts. |
| `Microsoft.MachineLearningServices/workspaces/write` | Create/update workspace. |

## Sample enterprise RBAC setup for hubs

| Persona | Role | Purpose |
| --- | --- | ---|
| IT admin | Owner | Ensures hub standards. Assigns manager roles. |
| Managers | Contributor or Azure AI Developer | Manage hub, audit shared resources. |
| Team lead | Azure AI Developer | Create projects and shared resources. |
| Developers | Contributor or Azure AI Developer (project) | Build and deploy models. |

## Access to external resources

Ensure the hub managed identity is granted required roles on external services (for example, storage, search) before use.

## Manage access

Use the Foundry portal (Users blade) or Azure portal IAM / CLI to assign roles.

Example CLI:

```azurecli-interactive
az role assignment create --role "Azure AI Developer" --assignee "user@contoso.com" --scope /subscriptions/<sub-id>/resourceGroups/<rg-name>
```

## Custom roles

Define custom roles when built-in roles don't meet needs. Example subscription-level custom role excerpt:

```json
{
  "properties": {
    "roleName": "Foundry Developer",
    "description": "Custom role for Foundry. At subscription level",
    "assignableScopes": ["/subscriptions/<your-subscription-id>"],
    "permissions": [ { "actions": ["Microsoft.MachineLearningServices/workspaces/write", "Microsoft.MachineLearningServices/workspaces/endpoints/write"], "notActions": [], "dataActions": ["Microsoft.CognitiveServices/accounts/OpenAI/*/read"], "notDataActions": [] } ]
  }
}
```

## Assigning roles in the portal

In the management center, select **Users** at hub or project level, then **New user**.

## Scenario highlights

- Customer-managed key: Grant workspace creator access to Key Vault; if using user-assigned identity, grant needed data-plane permissions.
- Connections with Microsoft Entra ID: Assign required Azure RBAC roles (for example, Storage Blob Data Contributor, Search Index Data Contributor).
- Azure Container Registry: Use system-assigned managed identity or assign `ACRPull` to user-assigned identity.
- Application Insights: Requires `Microsoft.Insights/Components/Write` and `Microsoft.OperationalInsights/workspaces/write` during hub creation.

## Troubleshooting

If new hubs using Azure AI Administrator identity role encounter issues, you can temporarily revert to Contributor (see original article for detailed steps).

## Next steps

- [Create a Foundry hub](../how-to/create-azure-ai-resource.md)
- [Create a project](../how-to/create-projects.md)
- [Add a connection](../how-to/connections-add.md)
