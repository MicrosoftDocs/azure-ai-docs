---
title: Authentication and authorization in Microsoft Foundry
ms.service: azure-ai-foundry
ms.date: 11/05/2025
ms.reviewer: meerakurup
ms.author: jburchel
author: jonburchel
description: Learn how to authenticate and authorize access in Microsoft Foundry using Microsoft Entra ID and API keys. Explore RBAC, identity types, and best practices.
#customer intent: As an IT admin, I want to understand how to configure authentication and authorization in Microsoft Foundry so that I can secure access to resources and operations.
ms.topic: concept-article
ai-usage: ai-assisted
---

# Authentication and authorization in Microsoft Foundry

Authentication and authorization in Microsoft Foundry define how principals prove identity and gain permission to perform control plane and data plane operations. Foundry supports API key and Microsoft Entra ID token-based authentication. Microsoft Entra ID enables conditional access, managed identities, granular role-based access control (RBAC) actions, and least privilege scenarios. API keys remain available for rapid prototyping and legacy integration but lack per-user traceability.

> [!IMPORTANT]
> Use Microsoft Entra ID for production workloads to enable conditional access, managed identities, and least privilege RBAC. API keys are convenient for quick evaluation but provide coarse-grained access.

## Control plane and data plane

Azure separates resource management (control plane) from operational runtime (data plane). In Foundry, the control plane covers resource configuration and management tasks. The data plane covers execution tasks like model inference, agent interactions, and evaluations.

| Plane | Scope in Foundry | Typical operations | Example tools | Authorization surface |
| --- | --- | --- | --- | --- |
| Control plane | Resource, projects, networking, encryption, connections | Create or delete resources, assign roles, rotate keys, set up Private Link | Azure portal, Azure CLI, ARM templates, Bicep, Terraform | Azure RBAC actions |
| Data plane | Model inference, agent interactions, evaluation jobs, content safety calls | Chat completions, embeddings, fine-tune jobs, agent messages, analyzer and classifier operations | SDKs, REST APIs, Foundry portal playground | Azure RBAC dataActions |

Control plane actions include resource and project creation, capability host setup, model deployment, and connection creation. Data plane actions include building agents, running evaluations, tracing, monitoring, and fine-tuning workloads.

:::image type="content" source="media/authentication-authorization-ai-foundry/azure-ai-control-data-plane-diagram.png" alt-text="Diagram illustrating separation of control plane and data plane operations with associated RBAC surfaces." lightbox="media/authentication-authorization-ai-foundry/azure-ai-control-data-plane-diagram.png":::

## Authentication methods

Foundry supports Microsoft Entra ID (token-based, keyless) and API keys.

### Microsoft Entra ID

Microsoft Entra ID uses OAuth 2.0 bearer tokens scoped to `https://cognitiveservices.azure.com/.default`.

Use Microsoft Entra ID for:
- Production workloads.
- Conditional access, multifactor authentication (MFA), and just-in-time access.
- Least privilege RBAC and managed identity integration.

Advantages: Fine-grained role assignments, per-principal auditing, controllable token lifetimes, automatic secret hygiene, and managed identities for services.

Limitations: Higher initial setup complexity. [TO VERIFY: link to Foundry RBAC doc]

### API keys

API keys are static secrets scoped to a Foundry resource.

Use Microsoft Entra ID for:
- Rapid prototyping.
- Isolated test environments where single-secret rotation is acceptable.

Advantages: Simple, language agnostic, and doesn't require token acquisition.

Limitations: No user-level identity, coarse scope, harder audit posture. Disable API keys after Microsoft Entra ID adoption.

For more information on enabling keyless authentication, see Configure key-less authentication with Microsoft Entra ID (link in Related content).

## Feature support matrix

| Capability or feature | API key | Microsoft Entra ID | Notes |
| --- | --- | --- | --- |
| Basic model inference (chat, embeddings) | Yes | Yes | Fully supported. |
| Fine-tuning operations | Yes | Yes | Entra ID adds per-principal audit. |
| Agents service | No | Yes | Use Entra ID for managed identity tool access. |
| Evaluations | No | Yes | Use Entra ID. |
| Content safety analyze calls | Yes | Yes | Use RBAC to limit high-risk operations. |
| Batch analysis jobs (Content Understanding) | Yes | Yes | Entra ID recommended for scale. |
| Portal playground usage | Yes | Yes | Playground uses project connection mode. |
| Network isolation with Private Link | Yes | Yes | Entra ID adds conditional access. |
| Least privilege with built-in and custom roles | No | Yes | Keys are all-or-nothing per resource. |
| Managed identity (system or user-assigned) | No | Yes | Enables secret-less auth. |
| Per-request user attribution | No | Yes | Token contains tenant and object IDs. |
| Revocation (immediate) | Rotate key | Remove role or disable principal | Short token lifetime applies. |
| Support in automation pipelines | Yes (secret) | Yes (service principal or managed identity) | Entra ID reduces secret rotation. |
| Assistants API | Yes | Yes |  |
| Batch inferencing | Yes | Yes |  |

## Identity types

Identity types determine usage patterns and life cycle management.

| Identity type | Description | Typical use in Foundry |
| --- | --- | --- |
| User principal | Individual user in Microsoft Entra ID | Portal usage, exploratory development, playground evaluation. |
| Service principal (app registration) | Application identity using client secret or certificate | CI/CD pipelines, batch orchestration, external systems. |
| Managed identity (system-assigned) | Identity tied to a single Azure resource | Functions, Web Apps, Container Apps calling Foundry. |
| Managed identity (user-assigned) | Reusable identity attachable to multiple resources | Shared workload identity, boundary for rotation, BCDR setup. |

Reference: [TO VERIFY: link to Entra ID identity types]

## Built-in roles overview

Foundry provides built-in roles that separate control and data plane permissions. Enterprises can choose narrow or combined roles based on operational models.

| Scenario | Typical built-in roles | Notes |
| --- | --- | --- |
| Build agents with pre-deployed models | Azure AI User role | Data plane usage only; no management writes. |
| Manage deployments or fine-tune models | Azure AI Project Manager | Includes model deployment creation and update. |
| Rotate keys or manage resource | Azure AI Account Owner | High privilege; consider custom role for least privilege. |
| Manage resource, manage deployments, build agents | Azure AI Full Access | Combine with Azure Monitor Reader if observability required. |
| Observability, tracing, monitoring | Azure AI User (minimum) | Add Azure Monitor Reader on Application Insights. |

:::image type="content" source="media/authentication-authorization-ai-foundry/azure-ai-role-mapping-diagram.png" alt-text="Diagram mapping built-in roles to control plane actions and data plane actions in Foundry." lightbox="media/authentication-authorization-ai-foundry/azure-ai-role-mapping-diagram.png":::

> [!TIP]
> Create a custom role if a built-in role grants excess permissions. [TO VERIFY: link to custom roles section]

## Example custom role (restrict agent writes)

The following example shows a custom role definition that restricts agent-related write operations but allows inference. Before use, validate all action and dataAction lists against current service definitions. [TO VERIFY: confirm action list currency]

```json
{
  "id": "/providers/Microsoft.Authorization/roleDefinitions/{role_id}",
  "properties": {
    "roleName": "Custom AI User Role",
    "description": "Restricts users to inference models. Grants permissions to read project and build Agents.",
    "assignableScopes": [ "/" ],
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
        "dataActions": [
          "Microsoft.CognitiveServices/*"
        ],
        "notDataActions": [
          "Microsoft.CognitiveServices/accounts/OpenAI/batch-jobs/write",
          "Microsoft.CognitiveServices/accounts/OpenAI/batch-jobs/delete"
        ]
      }
    ]
  }
}
```

## Microsoft Entra ID setup overview

Key setup elements include configuring a custom subdomain, assigning roles to user, service principal, or managed identity, and removing key-based authentication after migration. Service principals use client secrets or certificates; managed identities avoid credential management.

:::image type="content" source="media/authentication-authorization-ai-foundry/microsoft-entra-rbac-diagram.png" alt-text="Diagram showing mixed workload using user principals, service principals, and managed identities with RBAC applied." lightbox="media/authentication-authorization-ai-foundry/microsoft-entra-rbac-diagram.png":::

Core considerations:
- Assign only required built-in or custom roles at resource or project scope.
- Use managed identities for Azure-hosted workloads where possible.
- Remove API keys after all callers adopt token acquisition.

## Common identity scenarios

Scenario: Restrict users to model inference but not agents.
- Apply a custom role excluding agent dataActions and batch job writes (example in the preceding section).
- Combine with Azure AI User role if minimal data plane access is still required.
- Test denial path for agent creation.

Scenario: Separate administrators from developers.
- Administrators: Azure AI Account Owner (control plane).
- Developers: Azure AI User (data plane).
- Periodically review assignments with access reviews.

Scenario: Configure authentication for external app components.
- Update project connections: Management center > Connected resources > Access details > Authentication > Microsoft Entra ID. [TO VERIFY: UI labels]

## Service authentication patterns

| Pattern | Description | Example | Recommended identity |
| --- | --- | --- | --- |
| Server-to-service (headless) | Backend invokes inference for users | API layer enriching responses | Managed identity or service principal |
| Client app direct call | Front end invokes inference (avoid secret exposure) | Mobile or native app | Backend token broker (no embedded keys) |
| Data pipeline batch | Scheduled evaluations or fine-tunes | Nightly job | Service principal with limited custom role |
| Agent tool access to Azure resources | Agent retrieves external data via tools | Retrieval augmentation | Managed identity with least privilege |

## Auto role assignments

When you create your first Foundry resource and project in the Foundry portal or Azure portal (not via Bicep or CLI), the Azure AI User role can be auto-assigned to the creating user principal if the principal has role assignment permission (exact action [TO VERIFY]). This process streamlines initial data plane access.

## Related content

- Role-based access control for Foundry (link in same directory) [TO VERIFY]
- [Configure key-less authentication with Microsoft Entra ID](../../foundry-models/how-to/configure-entra-id.md)
- [Rotate API access keys](../../../ai-services/rotate-keys.md?context=/azure/ai-foundry/context/context)
- [Azure built-in roles (AI + machine learning)](/azure/role-based-access-control/built-in-roles#ai-+-machine-learning)
- [Authentication vs. authorization (Microsoft Entra ID)](/entra/identity-platform/authentication-vs-authorization)
- [Identity fundamentals](/entra/fundamentals/identity-fundamental-concepts)
