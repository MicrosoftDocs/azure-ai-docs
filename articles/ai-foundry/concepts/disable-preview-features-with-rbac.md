---
title: Disable Preview Features with Role-Based Access
description: Learn how to disable preview features in Azure AI Foundry using role-based access control (RBAC). Create custom roles to manage feature access effectively.
#customer intent: As an IT admin, I want to disable preview features in Azure AI Foundry through role-based access control so that my organization complies with enterprise policies.
author: jonburchel
ms.author: jburchel
ms.reviewer: meerakurup
ms.date: 09/25/2025
ms.topic: concept-article
ms.service: azure-ai-foundry
ai.usage: ai-assisted
---

# Disable preview features in Azure AI Foundry with role-based access control

In Azure AI Foundry projects, some features are in preview. Administrators can bock access to them by denying specific data actions to a custom role, and granting their users role memberships to enable/disable specific features as required. This article lists the data actions for each preview feature so you can disable them on an individual basis. However, since you can't modify built-in roles in Azure AI Foundry projects, you need to create a custom role. For steps to create a custom role, see [Create or update Azure custom roles using the Azure portal - Azure RBAC](/azure/role-based-access-control/custom-roles-portal).

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

- `Microsoft.CognitiveServices/accounts/OpenAI/assistants/\*` (include
  _read_, _write_, and _delete_ and all child resources)
- `Microsoft.CognitiveServices/accounts/OpenAI/assistants/files/\*`
- `Microsoft.CognitiveServices/accounts/OpenAI/assistants/threads/\*`
- `Microsoft.CognitiveServices/accounts/OpenAI/assistants/threads/messages/\*`
- `Microsoft.CognitiveServices/accounts/OpenAI/assistants/vector_stores/\*`

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

## Preview feature RBAC action matrix

Use this matrix to determine which data actions to include (enable) or exclude (disable) in a custom role for each preview feature. To disable a feature for a principal, ensure none of the listed enable actions are granted by any assigned role (or put them in NotActions).

| Feature | To ENABLE (include all these dataActions) | To DISABLE (ensure none of these are granted) |
|---------|-------------------------------------------|-----------------------------------------------|
| Agents (Foundry agent service) | `Microsoft.CognitiveServices/accounts/AIServices/agents/read`<br>`Microsoft.CognitiveServices/accounts/AIServices/agents/write`<br>`Microsoft.CognitiveServices/accounts/AIServices/agents/delete` | Exclude all three agent actions (or add the wildcard `Microsoft.CognitiveServices/accounts/AIServices/agents/*` to NotActions). |
| Content Understanding (Multi-Modal Intelligence) | `Microsoft.CognitiveServices/accounts/MultiModalIntelligence/analyzers/read`<br>&nbsp;&nbsp;&nbsp;`.../analyzers/write`<br>&nbsp;&nbsp;&nbsp;`.../analyzers/delete`<br>`Microsoft.CognitiveServices/accounts/MultiModalIntelligence/classifiers/read`<br>&nbsp;&nbsp;&nbsp;`.../classifiers/write`<br>&nbsp;&nbsp;&nbsp;`.../classifiers/delete`<br>`Microsoft.CognitiveServices/accounts/MultiModalIntelligence/batchAnalysisJobs/*`<br>Optional: any `/labelingProjects` trees your teams use* | Exclude every action beginning `Microsoft.CognitiveServices/accounts/MultiModalIntelligence/` |
| Assistants (Azure OpenAI Assistants API) | `Microsoft.CognitiveServices/accounts/OpenAI/assistants/*` (read, write, delete + children)<br>`Microsoft.CognitiveServices/accounts/OpenAI/assistants/files/*`<br>`Microsoft.CognitiveServices/accounts/OpenAI/assistants/threads/*`<br>`Microsoft.CognitiveServices/accounts/OpenAI/assistants/threads/messages/*`<br>`Microsoft.CognitiveServices/accounts/OpenAI/assistants/vector_stores/*` | Remove every action starting `Microsoft.CognitiveServices/accounts/OpenAI/assistants/` |
| Fine-tuning | `Microsoft.CognitiveServices/accounts/OpenAI/fine-tunes/read`<br>&nbsp;&nbsp;&nbsp;`.../fine-tunes/write`<br>&nbsp;&nbsp;&nbsp;`.../fine-tunes/delete`<br>Optional (RLHF): `Microsoft.CognitiveServices/accounts/OpenAI/1p-jobs/*`<br>`Microsoft.CognitiveServices/accounts/OpenAI/fine-tunes/files/*`<br>`.../fine-tunes/uploads/*`<br>&nbsp;&nbsp;&nbsp;`.../fine-tunes/stored-completions/*`<br>&nbsp;&nbsp;&nbsp;`.../fine-tunes/evals/*`<br>&nbsp;&nbsp;&nbsp;`.../fine-tunes/models/*` | Remove all `Microsoft.CognitiveServices/accounts/OpenAI/fine-tunes/*` (and any `.../1p-jobs/*` if present). |
| Tracing / Telemetry (Azure Monitor reads) | `Microsoft.Insights/alertRules/read`<br>`Microsoft.Insights/diagnosticSettings/read`<br>`Microsoft.Insights/logDefinitions/read`<br>`Microsoft.Insights/metricdefinitions/read`<br>`Microsoft.Insights/metrics/read` | Omit the Azure Monitor read actions (or list them in NotActions). |
| Risk + Alerts (Content Safety) | `Microsoft.CognitiveServices/accounts/ContentSafety/*` - at minimum:<br>&nbsp;&nbsp;&nbsp;`.../Analyze Text`<br>&nbsp;&nbsp;&nbsp;`.../Analyze Image`<br>&nbsp;&nbsp;&nbsp;`.../Analyze Protected Material`<br>&nbsp;&nbsp;&nbsp;`.../Unified Analyze` | Exclude every action starting `Microsoft.CognitiveServices/accounts/ContentSafety/` and avoid assigning any role on the Content Safety resource. |
| Governance (Foundry management center) | `Microsoft.CognitiveServices/accounts/write`<br>`Microsoft.CognitiveServices/accounts/delete`<br>Plus any required VNet / Private Endpoint / Key Vault reference writes you govern. | Grant only `Microsoft.CognitiveServices/accounts/read` and remove any write/delete actions on the account resource. |

*Optional labeling projects: include only if teams label documents inside Foundry.

> [!NOTE]
> When disabling a feature, verify no other assigned role grants a broader wildcard (for example `Microsoft.CognitiveServices/accounts/*`) that would implicitly re-enable it.

## Related content

- [Role-based access control for Azure AI Foundry](rbac-azure-ai-foundry.md)

