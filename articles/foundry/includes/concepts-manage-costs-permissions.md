---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: aashishb
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/23/2026
ms.custom: include
---

### Configure permissions to view costs

To view Foundry costs, assign roles based on the task and scope. For cost reporting, assign the [Cost Management Reader role](/azure/role-based-access-control/built-in-roles/management-and-governance#cost-management-reader) at the required scope. Assign the [Azure AI User role](../concepts/rbac-foundry.md#built-in-roles) when users also need to inspect Foundry resources and usage context.

If built-in roles don't meet your needs, you can create a custom role with least-privilege permissions. Validate role actions in your environment because available actions can evolve over time.

Example read permissions:

* `Microsoft.Consumption/*/read`
* `Microsoft.CostManagement/*/read`
* `Microsoft.Resources/subscriptions/read`
* `Microsoft.CognitiveServices/accounts/AIServices/usage/read`

> [!NOTE]
> You need the **Owner** role at the subscription or resource group scope to create custom roles in that scope.
> 

To create a custom role, use one of the following articles:

* [Azure portal](/azure/role-based-access-control/custom-roles-portal)
* [Azure CLI](/azure/role-based-access-control/custom-roles-cli)
* [Azure PowerShell](/azure/role-based-access-control/custom-roles-powershell)

For more information about custom roles, see [Azure custom roles](/azure/role-based-access-control/custom-roles).

To create a custom role, construct a role definition JSON file that specifies permissions and scope for the role. The following example is an illustrative starting point for a custom Foundry Cost Reader role:

```json
{
    "Name": "Foundry Cost Reader",
    "IsCustom": true,
    "Description": "Can see cost metrics in Foundry",
    "Actions": [
        "Microsoft.Consumption/*/read",
        "Microsoft.CostManagement/*/read",
        "Microsoft.Resources/subscriptions/read",
        "Microsoft.CognitiveServices/accounts/AIServices/usage/read"
    ],
    "NotActions": [],
    "DataActions": [],
    "NotDataActions": [],
    "AssignableScopes": [
        "/subscriptions/<subscriptionId>/resourceGroups/<resourceGroupName>/providers/Microsoft.CognitiveServices/accounts/<foundryResourceName>"
    ]
}
```

Replace `<subscriptionId>`, `<resourceGroupName>`, and `<foundryResourceName>` with your actual values.

> [!NOTE]
> Validate custom role definitions in a nonproduction environment before broad rollout, and verify each action against your tenant's supported resource provider operations.

> [!NOTE]
> This custom role example doesn't grant access to Foundry resources by itself. Assign an additional role such as [Azure AI User](../concepts/rbac-foundry.md#built-in-roles) if users also need Foundry resource visibility.
