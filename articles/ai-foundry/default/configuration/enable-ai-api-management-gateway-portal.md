---
title: Enforce token limits with AI Gateway
titleSuffix: Microsoft Foundry
description: Enable AI Gateway with Azure API Management to apply tokens-per-minute limits and token quotas to model deployments in Microsoft Foundry.
#customer intent: As an IT admin, I want to enforce token limits on AI model deployments so that I can prevent excessive usage and align with organizational policies.
author: jonburchel
ms.author: jburchel
ms.reviewer: ankamene
ms.service: azure-ai-foundry
ms.topic: how-to
ms.custom: dev-focus
ms.date: 01/05/2026
ai-usage: ai-assisted
---

# Enforce token limits with AI Gateway

Use AI Gateway in Microsoft Foundry to enforce tokens-per-minute (TPM) rate limits and total token quotas for model deployments at the project scope. This integration uses Azure API Management behind the scenes and applies limits per project to prevent runaway token consumption and align usage with organizational guardrails. This article covers token rate limiting and token quotas. You configure all settings in the Foundry portal.

## Prerequisites

- Azure subscription ([create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)).
- Permissions to create or reuse an Azure API Management (APIM) instance:
  - To create an APIM instance: **Contributor** or **Owner** on the target resource group (or subscription).
  - To manage an existing APIM instance: **API Management Service Contributor** (or **Owner**) on the APIM instance. For more information, see [How to use role-based access control in Azure API Management](/azure/api-management/api-management-role-based-access-control).
- Access to the Foundry portal (**Admin console**) for the target Foundry resource.
  - For example: **Azure AI Account Owner** or **Azure AI Owner** on the Foundry resource. For more information, see [Role-based access control for Microsoft Foundry](../../concepts/rbac-foundry.md).
- Decision on whether to create a dedicated APIM instance or reuse an existing one.

## Understand AI Gateway scope

An AI Gateway sits between clients and model deployments. All requests flow through the APIM instance once associated. Limits apply at the project level (each project can have its own TPM and quota settings). This article covers TPM rate limits and token quotas.

:::image type="content" source="..\media\enable-ai-api-management-gateway-portal\gateway-architecture-diagram.png" alt-text="Logical flow showing client requests passing through AI Gateway (APIM) before reaching model deployments within a project.":::

## Choose API Management usage model

When you create a new AI Gateway, decide whether to:

- Create a new APIM instance.
- Use an existing APIM instance.

If you use an existing APIM instance, choose one that meets your organization's governance and networking requirements.

When you create a new instance from the Foundry portal flow, the SKU defaults to Basic v2. For more information about costs and pricing for the API Management service, see [API Management Pricing](https://azure.microsoft.com/pricing/details/api-management/).

## Create an AI Gateway

Follow these steps in the Foundry portal to enable AI Gateway for a resource.

1. [!INCLUDE [foundry-sign-in](../../default/includes/foundry-sign-in.md)]
1. Select **Operate** > **Admin console**.
1. Open the **AI Gateway** tab.
1. Select **Add AI Gateway**.
1. Select the Foundry resource you want to connect with the gateway.
1. Select **Create new** or **Use existing** APIM.
1. If you create a new APIM instance, review [API Management Pricing](https://azure.microsoft.com/pricing/details/api-management/).
1. Name the gateway, and select **Add** to create or associate the APIM instance.
1. Validate that the Gateway status shows **Enabled** once provisioning completes.

:::image type="content" source="..\media\enable-ai-api-management-gateway-portal\create-ai-gateway-portal.png" alt-text="AI Gateway tab in the Admin console showing options to create or select an API Management instance." lightbox="..\media\enable-ai-api-management-gateway-portal\create-ai-gateway-portal.png":::

## Configure token limits

You can configure token limits for specific model deployments within your projects. 

1. Select the gateway you want to use from the **AI Gateway** gateway list.
1. Select **Token management** in the gateway details pane that appears.
1. Select **+ Add limit** to create a new limit for a model deployment.
1. Select the project and deployment you want to restrict, and enter a value for **Limit (Token-per-minute)**.
1. Select **Create** to save your changes.

Subsequent requests that exceed the TPM threshold receive rate-limit responses. Requests that exceed the quota produce quota-exceeded responses indicating `429 Too Many Requests` if the rate limit is exceeded, or `403 Forbidden` if the total token quota is exhausted.

:::image type="content" source="..\media\enable-ai-api-management-gateway-portal\set-token-limits.png" alt-text="Project settings panel showing input fields for tokens-per-minute and total token quota limits." lightbox="..\media\enable-ai-api-management-gateway-portal\set-token-limits.png":::

## Understand quota windows

Token limits have two complementary enforcement dimensions:

- Tokens per minute (TPM) rate limit: Limits token consumption to a configured maximum per minute. When the TPM limit is exceeded, the caller receives a `429 Too Many Requests` response status code.

- Total token quota: Limits token consumption to a configured maximum per quota period (for example, hourly, daily, weekly, monthly, or yearly). When the quota is exceeded, the caller receives a `403 Forbidden` response status code.

If you send many requests concurrently, token consumption can temporarily exceed the configured limits until responses are processed.

Adjusting a quota or TPM value affects subsequent enforcement decisions.

For more details, see [AI Gateway capabilities in Azure API Management](/azure/api-management/genai-gateway-capabilities) and [Limit large language model API token usage](/azure/api-management/llm-token-limit-policy).

## Verify enforcement

1. Send test requests to a model deployment endpoint by using the project's gateway URL and key.
1. Gradually increase request frequency until the TPM limit triggers.
1. Track cumulative tokens until the quota triggers.
1. Validate that `429 Too Many Requests` is returned once the TPM limit is exceeded, and `403 Forbidden` is returned once the quota is exhausted.


Success criteria:
- Rate-limited responses appear once TPM exceeded.
- Quota error appears once total token allocation exhausted.

## Adjust limits

1. Return to project **AI Gateway** settings.
1. Modify TPM or quota values.
1. Save; new limits apply immediately to subsequent requests.

## Governance scenarios

Use AI Gateway for:
- Multi-team token containment (prevent one project from monopolizing capacity).
- Cost control by capping aggregate usage.
- Compliance boundaries for regulated workloads (enforce predictable usage ceilings).

## Troubleshooting

| Issue | Possible cause | Action |
| --- | --- | --- |
| APIM instance doesn't appear | Provisioning delay | Refresh after a few minutes. |
| Limits aren't enforced | Misconfiguration or project not linked | Reopen settings; confirm enforcement toggle is on. Confirm that the AI Gateway is enabled for the project and if correct limits are configured. |
| High latency after enablement | APIM cold start or region mismatch | Check APIM region vs resource region. Call the model directly and compare the result with the call proxied through the AI Gateway to identify if performance issues are related to the gateway. |

If the Admin console is slow, retry after a brief interval.

## Limitations

- You can configure settings only through the Foundry portal; no support yet for CLI, ARM, or API.
- Token limits configured in the Foundry portal apply at the project scope.

## Clean up resources

If you created a dedicated APIM instance for this purpose:

1. Confirm that no other workloads depend on it.
1. Disable the AI Gateway for all projects in the Foundry resource it's associated with.
1. Remove linked resources in Azure portal.
1. Delete the APIM instance with the same name as the AI gateway in Azure portal (if it's not used for any other purpose).

## Related content

- [AI Gateway capabilities in Azure API Management](/azure/api-management/genai-gateway-capabilities)
- [Azure API Management overview](/azure/api-management/api-management-key-concepts)
- [Limit large language model API token usage](/azure/api-management/llm-token-limit-policy)
- [How to use role-based access control in Azure API Management](/azure/api-management/api-management-role-based-access-control)
- [Role-based access control for Microsoft Foundry](../../concepts/rbac-foundry.md)
