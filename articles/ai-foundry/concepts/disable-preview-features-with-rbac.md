---
title: Disable preview features with role-based access control
description: Learn how to disable preview features in Microsoft Foundry using role-based access control (RBAC). Create custom roles to manage feature access effectively.
#customer intent: As an IT admin, I want to disable preview features in Microsoft Foundry through role-based access control so that my organization complies with enterprise policies.
author: jonburchel
ms.author: jburchel
ms.reviewer: meerakurup
ms.date: 01/05/2026
ms.topic: concept-article
ms.service: azure-ai-foundry
ms.custom:
  - dev-focus
ai-usage: ai-assisted
monikerRange: foundry-classic || foundry
---

# Disable preview features in Microsoft Foundry by using role-based access control

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

In Microsoft Foundry projects, some features are in preview. You can block access to these features by excluding specific data actions from a custom role, and then assigning that role to users.

This article lists the data actions for each preview feature so you can block features individually. Because you can't modify built-in roles in Foundry projects, you need to create a custom role.

## Prerequisites

- A Microsoft Foundry project.
- Permissions to create custom roles at the scope where you want the role to be assignable (for example, Owner or User Access Administrator).
- Permissions to assign roles at the scope where you assign access (for example, Role Based Access Control Administrator or User Access Administrator).

## Example: Create a custom role that blocks a preview feature

This example shows the JSON shape for a custom role definition and where to put the preview feature data actions.

If you clone an existing role or use wildcard permissions, add the preview feature data actions to `notDataActions` so the role excludes them.

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
        "actions": [],
        "notActions": [],
        "dataActions": [],
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

Reference: [Create or update Azure custom roles using the Azure portal](/azure/role-based-access-control/custom-roles-portal)

Reference: [Assign Azure roles using the Azure portal](/azure/role-based-access-control/role-assignments-portal)

## Agent Service data actions

Use these data actions in a custom role definition:

- `Microsoft.CognitiveServices/accounts/AIServices/agents/write`
- `Microsoft.CognitiveServices/accounts/AIServices/agents/read`
- `Microsoft.CognitiveServices/accounts/AIServices/agents/delete`

## Content understanding (multimodal intelligence)

Add these data actions to your custom role definition:

- `Microsoft.CognitiveServices/accounts/MultiModalIntelligence/analyzers/read`
- `Microsoft.CognitiveServices/accounts/MultiModalIntelligence/analyzers/write`
- `Microsoft.CognitiveServices/accounts/MultiModalIntelligence/analyzers/delete`
- `Microsoft.CognitiveServices/accounts/MultiModalIntelligence/classifiers/read`
- `Microsoft.CognitiveServices/accounts/MultiModalIntelligence/classifiers/write`
- `Microsoft.CognitiveServices/accounts/MultiModalIntelligence/classifiers/delete`
- `Microsoft.CognitiveServices/accounts/MultiModalIntelligence/batchAnalysisJobs/*`

If your team labels documents in Foundry, search for `labelingProjects` under the **Microsoft.CognitiveServices** resource provider and include the matching data actions.

## Fine-tuning

Add these data actions to your custom role definition:

- `Microsoft.CognitiveServices/accounts/OpenAI/fine-tunes/*`, includes `/files/*`, `/uploads/*`, `/stored-completions/*`, `/evals/*`, `/models/*`
- (optional, if you run RLHF jobs) `Microsoft.CognitiveServices/accounts/OpenAI/1p-jobs/*`

## Tracing

Allow or deny the following data actions in the custom role definition.

Foundry's Tracing pane uses Azure Monitor. In the custom role wizard, set the provider to `Microsoft.Insights`, then add or remove only the read actions you need:

- `Microsoft.Insights/alertRules/read`
- `Microsoft.Insights/diagnosticSettings/read`
- `Microsoft.Insights/logDefinitions/read`
- `Microsoft.Insights/metricdefinitions/read`
- `Microsoft.Insights/metrics/read`

## Evaluation data actions

Add these data actions to your custom role definition:

- `Microsoft.CognitiveServices/accounts/AIServices/evaluations/write`
- `Microsoft.CognitiveServices/accounts/AIServices/evaluations/read`
- `Microsoft.CognitiveServices/accounts/AIServices/evaluations/delete`

## Content safety risks and alerts

Add these data actions to your custom role definition:

- `Microsoft.CognitiveServices/accounts/ContentSafety/*`

To allow only specific Content Safety operations, search for `ContentSafety` in the Azure portal custom role editor and select the specific data actions you need.

## Related content

[Role-based access control for Foundry](rbac-foundry.md)
