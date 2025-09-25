---
title: Authentication and authorization options in Azure AI Foundry
description: Learn the authentication and authorization options for Azure AI Foundry including API keys, Microsoft Entra ID, managed identities, and common RBAC scenarios.
ms.author: jburchel
author: jonburchel
ms.reviewer: meerakurup
ms.date: 09/25/2025
ms.topic: concept-article
ms.service: azure-ai-foundry
ai.usage: ai-assisted
#customer intent: As a platform admin, I want to choose and implement the right authentication approach for Azure AI Foundry so my teams are secure and productive.
---

# Authentication and authorization options in Azure AI Foundry

Azure AI Foundry supports multiple authentication approaches so you can balance security, operational simplicity, and velocity. This article explains the control plane vs. data plane model, compares API key and Microsoft Entra ID (formerly Azure AD) authentication, shows how identities map to roles, and walks through common least‑privilege scenarios. Use it together with:

- [Role-based access control for Azure AI Foundry](rbac-azure-ai-foundry.md)
- [Configure key-less authentication with Microsoft Entra ID](../foundry-models/how-to/configure-entra-id.md)
- [Rotate API access keys](../../ai-services/rotate-keys.md?context=/azure/ai-foundry/context/context)
- [Azure built-in roles (AI + machine learning)](/azure/role-based-access-control/built-in-roles#ai-+-machine-learning)

> [!IMPORTANT]
> Favor Microsoft Entra ID for production workloads to enable conditional access, managed identities, and least‑privilege RBAC. API keys are convenient for quick evaluation and legacy tooling but lack user-level traceability.

## Control plane vs. data plane

Azure services separate the management (_control plane_) from runtime operations (_data plane_):

| Plane | Scope in Azure AI Foundry | Typical operations | Example tools | Authorization surface |
|-------|---------------------------|--------------------|---------------|-----------------------|
| Control plane | Provisioning and configuration of hubs, projects, network, encryption, connections | Create/delete resources, assign roles, rotate keys, configure private link | Azure portal, Azure CLI, ARM/Bicep, Terraform | Azure RBAC (management actions + dataActions) |
| Data plane | Execution and consumption of model inference, agent interactions, evaluation jobs, content safety calls | Chat completions, embedding generation, fine-tune job start, agent message send, analyzer/classifier operations | SDKs, REST APIs, Foundry portal playground | API key header OR OAuth 2.0 (Microsoft Entra ID token) + dataActions |

### Diagram: control vs. data plane

![Conceptual diagram showing the control plane (configuration, role assignments, networking/keys) influencing data plane operations (model inference, agent service, evaluations, content safety).](../media/authentication-options-ai-foundry/control-data-plane.png)

_Diagram source file: control-data-plane.mmd (stored with the image for maintenance; not published)._ 

> [!NOTE]
> Diagram is conceptual. Validate latest supported resources and operations against current service documentation. [**TO VERIFY**]

## Authentication methods

### API keys

API keys are static secrets scoped to an Azure AI Foundry (formerly Azure AI Services) resource.

**Recommended for:**
- Rapid prototyping, isolated test environments
- Systems where rotating a single secret across multiple callers is operationally acceptable

**Advantages:** Simple, language-agnostic, no token acquisition flow.

**Limitations:** Cannot express user identity, difficult to scope granularly, harder to audit; should be disabled when Entra ID adoption is complete.

### Microsoft Entra ID (token-based / keyless)

Microsoft Entra ID uses OAuth 2.0 bearer tokens; principals obtain tokens for the resource scope (`https://cognitiveservices.azure.com/.default`).

**Recommended for:**
- Production workloads
- Conditional access / MFA / Just‑in‑Time access
- Least‑privilege RBAC and managed identity integration

**Advantages:** Fine-grained role assignments, per‑principal audit, token lifetimes, automatic secret hygiene, managed identities for services.

**Limitations:** Slightly higher initial setup complexity; requires custom subdomain endpoints for some services. See [Configure key-less authentication with Microsoft Entra ID](../foundry-models/how-to/configure-entra-id.md).

## Feature support matrix: API key vs. Microsoft Entra ID

> [!IMPORTANT]
> Validate features marked [**TO VERIFY**] against current release notes if you rely on them for compliance-critical scenarios.

| Capability / Feature | API Key | Microsoft Entra ID | Notes |
|---------------------|---------|--------------------|-------|
| Basic model inference (chat, embeddings) | Yes | Yes | Both fully supported. |
| Fine-tuning operations | Yes | Yes | Entra ID provides per-principal audit. [**TO VERIFY**] |
| Agents service interactions | Yes | Yes | Prefer Entra ID for managed identity tool access. |
| Content safety analyze calls | Yes | Yes | Use RBAC to limit high-risk operations. |
| Batch analysis jobs (Multimodal Intelligence) | Yes | Yes | Entra ID recommended for large-scale labeling. [**TO VERIFY**] |
| Portal playground usage | Yes | Yes | Playground uses project connection authentication mode. |
| Network isolation with Private Link | Yes | Yes | Entra ID adds conditional access benefits. |
| Conditional Access / MFA enforcement | No | Yes | Key-based bypasses user identity. |
| Least-privilege via built-in + custom roles | Limited | Yes | Keys are all-or-nothing per resource. |
| Managed identity (system/user-assigned) | No | Yes | Enables secretless server-to-service auth. |
| Per-request user attribution | No | Yes | Token includes tenant & object IDs. |
| Revocation (immediate) | Rotate key | Remove role / disable principal | Token lifetime still applies (short). |
| Support in automation pipelines | Yes (secret) | Yes (service principal / managed identity) | Entra ID avoids secret rotation overhead. |

## Identity types

| Identity type | Description | Typical use in Foundry | Advantages | Considerations |
|---------------|-------------|------------------------|------------|----------------|
| User principal | Individual human user in Entra ID | Portal, exploratory dev, model evaluation | Fine-grained audit; Conditional Access policies | Not ideal for unattended jobs |
| Service principal (app registration) | Application identity with client secret or certificate | CI/CD pipelines, batch orchestration, external systems | Automatable; supports certificate auth | Secrets/certs must be rotated; avoid over-scoping roles |
| Managed identity (system-assigned) | Azure resource-bound identity auto managed by platform | Deployed services calling Foundry (Functions, Web Apps, Container Apps) | No secret management; lifecycle tied to resource | Exists only in Azure; cannot be used outside cloud |
| Managed identity (user-assigned) | Standalone identity attachable to multiple resources | Shared workload identity across apps, rotation boundary | Reusable across hosts; granular role scoping | Lifecycle decoupled - must manage separately |

## Built-in roles (overview)

Refer to the authoritative list: [Azure built-in roles (AI + machine learning)](/azure/role-based-access-control/built-in-roles#ai-+-machine-learning). Common examples:

| Scenario | Typical built-in role(s) | Notes |
|----------|--------------------------|-------|
| Consume inference only | Cognitive Services User / Cognitive Services OpenAI User | Grants data plane usage; no management-plane writes |
| Manage deployments / fine-tune | Cognitive Services OpenAI Contributor | Includes create/update model deployment permissions |
| Rotate keys / manage resource | Cognitive Services Contributor | Broad - consider custom role for least privilege |
| Observability / metric reads | (Varies) Cognitive Services User + monitoring roles | Combine with Azure Monitor Reader if needed [**TO VERIFY**] |

> [!TIP]
> Use custom roles when built-in roles bundle more permissions than required.

## How to set up Microsoft Entra ID

High-level steps (see detailed guide: [Configure key-less authentication](../foundry-models/how-to/configure-entra-id.md)):

1. Ensure your Azure AI Foundry resource has a custom subdomain configured. (See [Custom subdomains](/azure/ai-services/cognitive-services-custom-subdomains)).
1. Assign the appropriate built-in or custom roles (e.g., Cognitive Services User) to each principal (user, service principal, managed identity) at the resource or project scope.
1. For service principals: create app registration, add client secret or certificate, capture tenant ID, client ID, and secret/cert.
1. For managed identities: enable system-assigned on the calling service or attach a user-assigned identity, then role-assign it to the Foundry resource.
1. Update project connections in Azure AI Foundry to use Microsoft Entra ID (Management center > Connected resources > Access details > Authentication: Microsoft Entra ID).
1. Remove (or plan removal of) key-based authentication after all callers use token auth; optionally disable local auth via deployment templates. [**TO VERIFY**]

### Example: Contoso mixed workload scenario

![Diagram showing developers (user principals), a CI/CD service principal, and a managed identity enabled Azure Function all interacting with an Azure AI Foundry resource; security admin applies RBAC and Azure Monitor/Tracing receives logs.](../media/authentication-options-ai-foundry/contoso-mixed-scenario.png)

_Diagram source file: contoso-mixed-scenario.mmd (stored with the image for maintenance; not published)._ 

- Developers get `Cognitive Services User` for inference.
- Service principal gets a custom role allowing deployment + evaluation actions.
- Managed identity for the Azure Function gets only inference dataActions.
- Security admin periodically reviews role assignments.

## Common setup scenarios

### Scenario: Restrict users to model inference but not agents
1. Create a custom role excluding agent dataActions (see: [Disable preview features with RBAC](disable-preview-features-with-rbac.md)).
2. Assign users the custom role + `Cognitive Services User` if needed for baseline inference.
3. Validate by attempting an agent action (should be denied).

### Scenario: Separate admins (configuration) from developers (build)
1. Assign a minimal management-plane custom role to admins (resource write/delete + networking, no dataActions).
2. Assign developers data plane roles (e.g., Cognitive Services OpenAI User or custom) without management-plane delete rights.
3. Periodically review using Azure Access Reviews. [**TO VERIFY**]

### Scenario: Least-privileged project access
1. Inventory required operations (inference, fine-tune, evaluation, content safety, etc.).
2. Start from the narrowest built-in role that covers the majority; clone into a custom role.
3. Add only the needed dataActions (avoid wildcards) for additional features.
4. Test with a non-privileged principal; expand incrementally.
5. Automate assignment via IaC (Bicep/ARM) for consistency.

## Service authentication patterns

| Pattern | Description | Example | Recommended identity |
|---------|-------------|---------|----------------------|
| Server-to-service (headless) | Backend performs inference on behalf of users | API layer enriching chat responses | Managed identity (preferred) or service principal |
| Client app direct call | Front-end calls inference (avoid exposing secrets) | Native/mobile app | Secure backend token broker; avoid embedding keys |
| Data pipeline batch | Nightly batch fine-tunes or evaluations | Scheduled job | Service principal with limited custom role |
| Agent tool access to Azure resources | Agent invokes other Azure services via tools | Retrieval augmentation | Managed identity with least privilege |

## Auto-role assignments

Some creation workflows may auto-assign broad roles (for example, resource creator gets Owner or Contributor). Review and downgrade to least privilege immediately after provisioning. Document any automation that depends on elevated roles. [**TO VERIFY**]

## Auditing and monitoring

- Use Azure Monitor logs + activity logs to correlate RBAC changes with data plane usage.
- Enable diagnostic settings exporting to Log Analytics / SIEM.
- Periodically scan for principals still using API keys and migrate them to Entra ID.

## Related content

- [Authenticate requests to Azure AI services](/azure/ai-services/authentication)
- [Configure key-less authentication with Microsoft Entra ID](../foundry-models/how-to/configure-entra-id.md)
- [Azure built-in roles (AI + machine learning)](/azure/role-based-access-control/built-in-roles#ai-+-machine-learning)
- [Disable preview features with RBAC](disable-preview-features-with-rbac.md)
- [Managed identities for Azure resources](/entra/identity/managed-identities-azure-resources/overview)