---
title: "Disable preview features with role-based access control (classic)"
description: "Learn how to disable preview features in Microsoft Foundry using role-based access control (RBAC). Create custom roles to manage feature access effectively. (classic)"
#customer intent: As an IT admin, I want to disable preview features in Microsoft Foundry through role-based access control so that my organization complies with enterprise policies.
author: jonburchel
ms.author: jburchel
ms.reviewer: meerakurup
ms.date: 02/23/2026
ms.topic: concept-article
ms.service: azure-ai-foundry
ms.custom:
  - classic-and-new
  - dev-focus
ai-usage: ai-assisted
ROBOTS: NOINDEX, NOFOLLOW
---

# Disable preview features in Microsoft Foundry by using role-based access control (classic)

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

Some features in Microsoft Foundry are in preview. You can block access to specific preview features by creating a custom Azure role that excludes the corresponding permissions, and then assigning that role to users.

This article lists the permissions for each preview feature so you can block features individually. Because you can't modify built-in roles, you create a [custom role](/azure/role-based-access-control/custom-roles) that uses `notDataActions` (or `notActions` for control plane features like Tracing) to exclude the permissions you want to block.

The following table summarizes the preview features you can block and the type of permissions to exclude.

| Preview feature | Resource provider path | Permission type | Exclusion field |
| --- | --- | --- | --- |
| [Agent Service](#agent-service) | `Microsoft.CognitiveServices/accounts/AIServices/agents/*` | Data action | `notDataActions` |
| [Content Understanding](#content-understanding) | `Microsoft.CognitiveServices/accounts/MultiModalIntelligence/*` | Data action | `notDataActions` |
| [Fine-tuning](#fine-tuning) | `Microsoft.CognitiveServices/accounts/OpenAI/fine-tunes/*` and related paths | Data action | `notDataActions` |
| [Evaluations](#evaluations) | `Microsoft.CognitiveServices/accounts/AIServices/evaluations/*` | Data action | `notDataActions` |
| [Content Safety](#content-safety) | `Microsoft.CognitiveServices/accounts/ContentSafety/*` | Data action | `notDataActions` |
| [Tracing](#tracing) | `Microsoft.Insights/*` | Control plane action | `notActions` |

## Prerequisites

- A Microsoft Foundry project.
- An Azure subscription with permissions to create custom roles at the scope where you want the role to be assignable (for example, the Owner role or the User Access Administrator role).
- Permissions to assign roles at the scope where you assign access (for example, the Role Based Access Control Administrator role or the User Access Administrator role).
- Azure CLI installed and signed in, if you create the role from the command line. For more information, see [Install the Azure CLI](/cli/azure/install-azure-cli).

## Create a custom role that blocks a preview feature

This section walks through creating a custom role definition and assigning it to a user. The example blocks Agent Service, but you can substitute any data actions from the [feature sections](#preview-feature-data-actions) in this article.

### Step 1: Define the role JSON

Create a JSON file named `custom-role.json` with the following content. Replace `<subscription-id>` with your Azure subscription ID and add the data actions you want to block to `notDataActions`.

```json
{
  "properties": {
    "roleName": "Foundry custom role (preview features blocked)",
    "description": "Custom role that excludes specific Foundry preview features.",
    "assignableScopes": [
      "/subscriptions/<subscription-id>"
    ],
    "permissions": [
      {
        "actions": [
          "Microsoft.CognitiveServices/*/read",
          "Microsoft.Authorization/*/read"
        ],
        "notActions": [],
        "dataActions": [
          "Microsoft.CognitiveServices/accounts/AIServices/*"
        ],
        "notDataActions": [
          "Microsoft.CognitiveServices/accounts/AIServices/agents/write",
          "Microsoft.CognitiveServices/accounts/AIServices/agents/read",
          "Microsoft.CognitiveServices/accounts/AIServices/agents/delete"
        ]
      }
    ]
  }
}
```

> [!TIP]
> If you clone an existing role or use wildcard permissions in `dataActions`, add the preview feature data actions to `notDataActions` so the role excludes them. For Tracing, use `notActions` instead because Tracing uses control plane actions.

### Step 2: Create the role

# [Azure CLI](#tab/cli)

```azurecli
az role definition create --role-definition custom-role.json
```

# [Azure portal](#tab/portal)

1. In the [Azure portal](https://portal.azure.com), go to the subscription or resource group where you want the custom role.
1. Select **Access control (IAM)** > **Add** > **Add custom role**.
1. On the **Basics** tab, enter a role name and description.
1. On the **JSON** tab, select **Edit**, and paste the JSON content from step 1.
1. Select **Review + create**.

---

### Step 3: Assign the role

# [Azure CLI](#tab/cli)

```azurecli
az role assignment create \
    --role "Foundry custom role (preview features blocked)" \
    --assignee "<user-email-or-object-id>" \
    --scope "/subscriptions/<subscription-id>"
```

# [Azure portal](#tab/portal)

1. In the [Azure portal](https://portal.azure.com), go to the scope where you want to assign the role.
1. Select **Access control (IAM)** > **Add** > **Add role assignment**.
1. Under **Role**, search for and select the custom role you created.
1. Under **Members**, select **User, group, or service principal**, search for the user, and select **Select**.
1. Select **Review + assign**.

---

### Step 4: Verify the role assignment

Confirm that the custom role excludes the expected permissions.

# [Azure CLI](#tab/cli)

List the role assignments for the user and verify the custom role appears:

```azurecli
az role assignment list --assignee "<user-email-or-object-id>" --output table
```

View the custom role definition to confirm `notDataActions` contains the expected data actions:

```azurecli
az role definition list --name "Foundry custom role (preview features blocked)" --output json
```

# [Azure portal](#tab/portal)

1. In the [Azure portal](https://portal.azure.com), go to the resource where you assigned the role.
1. Select **Access control (IAM)** > **Check access**.
1. Search for the user and review their effective permissions.
1. Verify that the blocked data actions don't appear in the user's effective permissions.

---

## Preview feature data actions

Each of the following sections lists the permissions for a preview feature. Add the data actions you want to block to `notDataActions` in your custom role definition, except for [Tracing](#tracing), which uses control plane actions in `notActions`.

### Agent Service

Add these data actions to `notDataActions` in your custom role definition:

- `Microsoft.CognitiveServices/accounts/AIServices/agents/write`
- `Microsoft.CognitiveServices/accounts/AIServices/agents/read`
- `Microsoft.CognitiveServices/accounts/AIServices/agents/delete`

To block all Agent Service operations with a single entry, use the wildcard `Microsoft.CognitiveServices/accounts/AIServices/agents/*`.

### Content Understanding

Add these data actions to `notDataActions` in your custom role definition:

- `Microsoft.CognitiveServices/accounts/MultiModalIntelligence/analyzers/read`
- `Microsoft.CognitiveServices/accounts/MultiModalIntelligence/analyzers/write`
- `Microsoft.CognitiveServices/accounts/MultiModalIntelligence/analyzers/delete`
- `Microsoft.CognitiveServices/accounts/MultiModalIntelligence/classifiers/read`
- `Microsoft.CognitiveServices/accounts/MultiModalIntelligence/classifiers/write`
- `Microsoft.CognitiveServices/accounts/MultiModalIntelligence/classifiers/delete`
- `Microsoft.CognitiveServices/accounts/MultiModalIntelligence/batchAnalysisJobs/*`

If your team labels documents in Foundry, also block the labeling data actions. In the Azure portal custom role editor, search for `labelingProjects` under the **Microsoft.CognitiveServices** resource provider to find the available operations, such as:

- `Microsoft.CognitiveServices/accounts/MultiModalIntelligence/labelingProjects/read`
- `Microsoft.CognitiveServices/accounts/MultiModalIntelligence/labelingProjects/write`
- `Microsoft.CognitiveServices/accounts/MultiModalIntelligence/labelingProjects/delete`

> [!NOTE]
> Verify the exact `labelingProjects` data actions in the Azure portal, because the available operations might change as the feature evolves.

### Fine-tuning

Fine-tuning uses several data action paths under `Microsoft.CognitiveServices/accounts/OpenAI/`. Add each path you want to block to `notDataActions` in your custom role definition:

- `Microsoft.CognitiveServices/accounts/OpenAI/fine-tunes/*`
- `Microsoft.CognitiveServices/accounts/OpenAI/files/*`
- `Microsoft.CognitiveServices/accounts/OpenAI/uploads/*`
- `Microsoft.CognitiveServices/accounts/OpenAI/stored-completions/*`
- `Microsoft.CognitiveServices/accounts/OpenAI/evals/*`
- `Microsoft.CognitiveServices/accounts/OpenAI/models/*`

Optionally, if your team runs RLHF jobs, also add:

- `Microsoft.CognitiveServices/accounts/OpenAI/1p-jobs/*`

> [!IMPORTANT]
> Each path listed is a separate data action scope. The `fine-tunes/*` wildcard matches only operations under `fine-tunes/`. To fully block fine-tuning, include all the paths listed.

### Tracing

> [!IMPORTANT]
> Tracing uses Azure Monitor, which is a control plane service. The permissions listed in this section are **actions, not data actions**. Add them to `notActions` (not `notDataActions`) in your custom role definition.

Add these actions to `notActions` in your custom role definition:

- `Microsoft.Insights/alertRules/read`
- `Microsoft.Insights/diagnosticSettings/read`
- `Microsoft.Insights/logDefinitions/read`
- `Microsoft.Insights/metricdefinitions/read`
- `Microsoft.Insights/metrics/read`

Blocking these read actions prevents users from viewing the Tracing pane in the Foundry portal. Users who need Tracing access require a separate role that includes the `Microsoft.Insights` read actions, such as a Reader role on the connected Application Insights resource.

### Evaluations

Add these data actions to `notDataActions` in your custom role definition:

- `Microsoft.CognitiveServices/accounts/AIServices/evaluations/write`
- `Microsoft.CognitiveServices/accounts/AIServices/evaluations/read`
- `Microsoft.CognitiveServices/accounts/AIServices/evaluations/delete`

### Content Safety

Add these data actions to `notDataActions` in your custom role definition:

- `Microsoft.CognitiveServices/accounts/ContentSafety/*`

To block only specific Content Safety operations instead of all operations, search for `ContentSafety` in the Azure portal custom role editor and select the individual data actions you want to exclude.

## Troubleshooting

| Symptom | Cause | Resolution |
| --- | --- | --- |
| User can still access a blocked feature. | The role assignment might not have propagated yet, or the user has another role that grants the blocked permission. | Wait a few minutes for propagation. Check all role assignments for the user with `az role assignment list --assignee "<user>"`. Remove any conflicting roles that grant the blocked data actions. |
| Custom role creation fails with "invalid data action." | The data action path might be misspelled or the resource provider might not be registered. | Verify the data action path in the Azure portal custom role editor. Ensure the `Microsoft.CognitiveServices` resource provider is registered in your subscription. |
| Tracing permissions aren't blocked after adding to `notDataActions`. | Tracing uses control plane actions (`Microsoft.Insights`), not data actions. | Move the `Microsoft.Insights` entries from `notDataActions` to `notActions` in the role definition. |

## Related content

- [Role-based access control for Microsoft Foundry](rbac-foundry.md)
- [Authentication and authorization in Microsoft Foundry](authentication-authorization-foundry.md)
- [Role-based access control for Microsoft Foundry (hubs and projects)](hub-rbac-foundry.md)
- [Create or update Azure custom roles using the Azure portal](/azure/role-based-access-control/custom-roles-portal)
- [Create or update Azure custom roles using Azure CLI](/azure/role-based-access-control/custom-roles-cli)
- [Assign Azure roles using the Azure portal](/azure/role-based-access-control/role-assignments-portal)
