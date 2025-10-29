---
title: Enforce token limits with AI Gateway
titleSuffix: Azure AI Foundry
description: Enable AI Gateway with Azure API Management to apply tokens-per-minute limits and token quotas to model deployments in Azure AI Foundry.
#customer intent: As an IT admin, I want to enforce token limits on AI model deployments so that I can prevent excessive usage and align with organizational policies.
author: jonburchel
ms.author: jburchel
ms.reviewer: ankamene
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 10/29/2025
ai-usage: ai-assisted
---

# Enforce token limits with AI Gateway

Use AI Gateway in Azure AI Foundry to apply governance controls, such as tokens-per-minute (TPM) rate limits and total token quotas, on model deployments. This integration uses Azure API Management behind the scenes and applies limits at the project scope so you prevent runaway token consumption and align usage with organizational guardrails. Only token rate limiting and quota enforcement are in scope for this release. You configure all settings in the UI; no CLI or API support exists yet. [TO VERIFY: Confirm scope]

## Prerequisites

- Azure subscription with permission to create or reuse an Azure API Management (APIM) instance.
- Access to the **Admin console** for the target Azure AI Foundry resource.
- Ability to configure a project in the resource.
- Reference material for [AI Gateway capabilities in APIM](/azure/api-management/genai-gateway-capabilities).
- Decision on whether to create a dedicated APIM instance or reuse an existing one.

## Understand AI Gateway scope

AI Gateway sits between clients and model deployments. All requests flow through the APIM instance once associated. Limits apply at the project level (each project can have its own TPM and quota settings). Supported features for this release are TPM rate limits and token quotas only. No other policy types are enforced.

:::image type="content" source="..\media\enable-ai-api-management-gateway-portal\gateway-architecture-diagram.png" alt-text="Logical flow showing client requests passing through AI Gateway (APIM) before reaching model deployments within a project.":::

## Choose API Management usage model

Decide whether to:
1. Create a new APIM instance (isolated governance, predictable usage boundary).
1. Reuse an existing APIM instance (centralized management, shared cost).
[TO VERIFY: Any constraints on shared instances]

When you create a new instance from the AI Foundry UI flow, the SKU defaults to Basic v2 (free for the first 30 days). [TO VERIFY: Pricing confirmation and legal wording]

## Enable AI Gateway

Follow these steps in the Azure AI Foundry UI to enable AI Gateway for a resource.

1. Sign in to <https://ai.azure.com>.
1. Go to your Azure AI Foundry resource.
1. Select **Operate** > **Admin console**.
1. Open the **AI Gateway** tab.
1. Select **Create new** or **Use existing** APIM.
1. If creating new, review the [Basic v2 SKU limitation and trial cost details](#limitations).
1. Confirm the APIM instance selection.
1. Finish setup; provisioning or association completes in the UI.

:::image type="content" source="..\media\enable-ai-api-management-gateway-portal\create-ai-gateway-portal.png" alt-text="AI Gateway tab in the Admin console showing options to create or select an API Management instance.":::

## Associate API Management with resource

After selection or creation:
1. Ensure the APIM instance displays as linked in the **AI Gateway** tab.
1. Proceed to configure token limits.

If association fails, see Troubleshooting.

## Configure token limits

You can configure token limits for specific model deployments within your projects. 

1. Select the gateway you want to use from the **AI Gateway** gateway list.
1. Select **Token management** in the gateway details pane that appears.
1. Select *+ Add limit** to create a new limit for a model deployment.
1. Select the project and deployment you want to restrict then, and enter a value for **Limit (Token-per-minute)**.
1. Select **Create** to save your changes, then.

Expected result: Subsequent requests that exceed the TPM threshold receive rate-limit responses. Requests that exceed the quota produce quota-exceeded responses. [TO VERIFY: Response codes or messages]

:::image type="content" source="..\media\enable-ai-api-management-gateway-portal\set-token-limits.png" alt-text="Project settings panel showing input fields for tokens-per-minute and total token quota limits.":::

## Verify enforcement

1. Send test requests to a model deployment endpoint by using the project’s gateway URL and key. [TO VERIFY: Gateway URL format]
1. Gradually increase request frequency until the TPM limit triggers.
1. Track cumulative tokens until the quota triggers.
1. Review logs or metrics surface (if available in UI). [TO VERIFY: Location of logs]

Success criteria:
- Rate-limited responses appear once TPM exceeded.
- Quota error appears once total token allocation exhausted.

## Adjust limits

1. Return to project **AI Gateway** settings.
1. Modify TPM or quota values.
1. Save; new limits apply immediately to subsequent requests. [TO VERIFY: Propagation time]

## Governance scenarios

Use AI Gateway for:
- Multi-team token containment (prevent one project from monopolizing capacity).
- Cost control by capping aggregate usage.
- Compliance boundaries for regulated workloads (enforce predictable usage ceilings).
[TO VERIFY: Any additional approved scenarios]

## Troubleshooting

| Issue | Possible cause | Action |
|-------|----------------|--------|
| APIM instance doesn't appear | Provisioning delay | Refresh after a few minutes. [TO VERIFY: Typical delay] |
| Limits aren't enforced | Misconfiguration or project not linked | Reopen settings; confirm enforcement toggle is on. |
| Unexpected quota resets | Misaligned time window definition | Verify quota window configuration. [TO VERIFY] |
| High latency after enablement | APIM cold start or region mismatch | Check APIM region vs resource region. [TO VERIFY] |

If the Admin console is slow, retry after a brief interval. [TO VERIFY: Official status page link]

## Limitations

- The current release supports only TPM rate limits and token quotas.
- You can configure settings only through the UI; no support yet for CLI, ARM, or API.
- Basic v2 APIM SKU is free for the first 30 days (confirm official pricing and legal text). [TO VERIFY]
- Dedicated APIM isolates governance, while shared APIM centralizes operations.
- Enforcement is project-scoped; resource-level global limits aren't in scope. [TO VERIFY]

## Clean up resources

If you created a dedicated APIM instance for this purpose:
1. Confirm that no other workloads depend on it.
1. Delete the APIM instance from the Azure portal. [TO VERIFY: Required role]
1. Remove AI Gateway association in Admin console (if supported). [TO VERIFY]

## Related content

- [AI Gateway capabilities in Azure API Management](/azure/api-management/genai-gateway-capabilities)
- [Azure API Management overview](/azure/api-management/api-management-key-concepts)

## TODO placeholders

- Replace [TO VERIFY] items with confirmed links, labels, and wording.
- Confirm response behaviors for rate-limit and quota exceed events.
