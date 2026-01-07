---
title: Enforce token limits for models
titleSuffix: Microsoft Foundry
description: Use Control Plane integration with AI Gateway to apply limits for model inference, including token limits.
author: santiagxf
ms.author: scottpolly
ms.reviewer: fasantia
ms.service: azure-ai-foundry
ms.topic: how-to
ms.custom: dev-focus
ms.date: 01/06/2026
ai-usage: ai-assisted
---

# Enforce token limits for models

Microsoft Foundry Control Plane enforces tokens-per-minute (TPM) rate limits and total token quotas for model deployments at the project scope to prevent runaway token consumption and align usage with organizational guardrails. Control Planes integrates with AI Gateway to provide advance policy enforcement for models.

This article explains how to configure token rate limiting and token quotas.

## Prerequisites

Before getting started, make sure you have:

- [!INCLUDE [azure-subscription](../../includes/azure-subscription.md)]

- A Foundry resource with AI Gateway configured. Learn more about [how to enable AI Gateway for a Foundry resource](../configuration/enable-ai-api-management-gateway-portal.md).

- A Foundry project added to the configured AI Gateway. 

  > [!TIP]
  > You need **API Management Service Contributor** (or **Owner**) on the Azure API Management resource to enable AI Gateway at a given project.

## Understand AI Gateway

Control Planes integrates with AI Gateway to provide advanced policy enforcement for models. AI Gateway sits between clients and model deployments, making all requests flow through the API Management instance associated with it. Limits apply at the project level (each project can have its own TPM and quota settings).

:::image type="content" source="..\media\enable-ai-api-management-gateway-portal\gateway-architecture-diagram.png" alt-text="Logical flow showing client requests passing through AI Gateway (APIM) before reaching model deployments within a project.":::

Use AI Gateway for:

> [!div class="checklist"]
> * Multi-team token containment (prevent one project from monopolizing capacity).
> * Cost control by capping aggregate usage.
> * Compliance boundaries for regulated workloads (enforce predictable usage ceilings).

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

For more information, see [AI Gateway capabilities in Azure API Management](/azure/api-management/genai-gateway-capabilities) and [Limit large language model API token usage](/azure/api-management/llm-token-limit-policy).

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


## Troubleshooting

| Issue | Possible cause | Action |
| --- | --- | --- |
| APIM instance doesn't appear | Provisioning delay | Refresh after a few minutes. |
| Limits aren't enforced | Misconfiguration or project not linked | Reopen settings; confirm enforcement toggle is on. Confirm that the AI Gateway is enabled for the project and if correct limits are configured. |
| High latency after enablement | APIM cold start or region mismatch | Check APIM region vs resource region. Call the model directly and compare the result with the call proxied through the AI Gateway to identify if performance issues are related to the gateway. |

If the Admin console is slow, retry after a brief interval.


## Related content

- [AI Gateway capabilities in Azure API Management](/azure/api-management/genai-gateway-capabilities)
- [Azure API Management overview](/azure/api-management/api-management-key-concepts)
- [Limit large language model API token usage](/azure/api-management/llm-token-limit-policy)
- [How to use role-based access control in Azure API Management](/azure/api-management/api-management-role-based-access-control)
- [Role-based access control for Microsoft Foundry](../../concepts/rbac-foundry.md)