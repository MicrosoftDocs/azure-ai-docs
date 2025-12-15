---
title: Disable Preview Features with Role-Based Access
description: Learn how to disable preview features in Microsoft Foundry using role-based access control (RBAC). Create custom roles to manage feature access effectively.
#customer intent: As an IT admin, I want to disable preview features in Microsoft Foundry through role-based access control so that my organization complies with enterprise policies.
author: jonburchel
ms.author: jburchel
ms.reviewer: meerakurup
ms.date: 09/25/2025
ms.topic: concept-article
ms.service: azure-ai-foundry
ai.usage: ai-assisted
---

# Disable preview features in Microsoft Foundry with role-based access control

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

In Microsoft Foundry projects, some features are in preview. Administrators can bock access to them by denying specific data actions to a custom role, and granting their users role memberships to enable/disable specific features as required. This article lists the data actions for each preview feature so you can disable them on an individual basis. However, since you can't modify built-in roles in Foundry projects, you need to create a custom role. For steps to create a custom role, see [Create or update Azure custom roles using the Azure portal - Azure RBAC](/azure/role-based-access-control/custom-roles-portal).

## Agents service data actions

Use these data actions in a custom role definition:

- `Microsoft.CognitiveServices/accounts/AIServices/agents/write`
- `Microsoft.CognitiveServices/accounts/AIServices/agents/read`
- `Microsoft.CognitiveServices/accounts/AIServices/agents/delete`

## Content understanding (multimodal intelligence)

The associated data actions to allow or disallow in your custom role
definition are the following:

- `Microsoft.CognitiveServices/accounts/MultiModalIntelligence/analyzers/read`
- `Microsoft.CognitiveServices/accounts/MultiModalIntelligence/analyzers/write`
- `Microsoft.CognitiveServices/accounts/MultiModalIntelligence/analyzers/delete`
- `Microsoft.CognitiveServices/accounts/MultiModalIntelligence/classifiers/read`
- `Microsoft.CognitiveServices/accounts/MultiModalIntelligence/classifiers/write`
- `Microsoft.CognitiveServices/accounts/MultiModalIntelligence/classifiers/delete`
- `Microsoft.CognitiveServices/accounts/MultiModalIntelligence/batchAnalysisJobs/\*`
- Optional: include the /labelingProjects data actions if your team labels documents in Foundry.

## Fine-tuning

The associated data actions to allow or disallow in your custom role
definition are the following:

- `Microsoft.CognitiveServices/accounts/OpenAI/fine-tunes/*`, includes `/files/*`, `/uploads/*`, `/stored-completions/*`, `/evals/*`, `/models/*`
- (optional, if you run RLHF jobs) `Microsoft.CognitiveServices/accounts/OpenAI/1p-jobs/*`

## Tracing

Allow or deny the following data actions in the custom role definition.

Foundry’s Tracing pane uses Azure Monitor. In the custom role wizard, set the provider to Microsoft.Insights, then add or remove only the read actions you need:

- `Microsoft.Insights/alertRules/read`
- `Microsoft.Insights/diagnosticSettings/read`
- `Microsoft.Insights/logDefinitions/read`
- `Microsoft.Insights/metricdefinitions/read`
- `Microsoft.Insights/metrics/read`

## Evaluation data actions

The associated data actions to allow or disallow in your custom role
definition are the following:

- `Microsoft.CognitiveServices/accounts/AIServices/evaluations/write`
- `Microsoft.CognitiveServices/accounts/AIServices/evaluations/read`
- `Microsoft.CognitiveServices/accounts/AIServices/evaluations/delete`

## Content safety risks and alerts

The associated data actions to allow or disallow in your custom role
definition are the following

- `Microsoft.CognitiveServices/accounts/ContentSafety/\*`
  - …/`Analyze Text`
  - …/`Analyze Image`
  - …/`Analyze Protected Material`
  - …/`Unified Analyze`

## Related content

[Role-based access control for Foundry](rbac-azure-ai-foundry.md)
