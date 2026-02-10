---
title: Enforce Token Limits for Models
titleSuffix: Microsoft Foundry
description: Use Foundry Control Plane integration with an AI gateway to apply limits for model inference, including token limits.
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

Microsoft Foundry Control Plane enforces tokens-per-minute (TPM) rate limits and total token quotas for model deployments at the project scope. This enforcement prevents runaway token consumption and aligns usage with organizational guardrails. Foundry Control Plane integrates with AI gateways to provide advanced policy enforcement for models.

This article explains how to configure token rate limiting and token quotas.

## Prerequisites

- [!INCLUDE [azure-subscription](../../includes/azure-subscription.md)]

- A Foundry resource with an AI gateway configured. [Learn more about how to enable an AI gateway for a Foundry resource](../configuration/enable-ai-api-management-gateway-portal.md).

- A Foundry project added to the configured AI gateway. To enable an AI gateway for a project, you need the API Management Service Contributor or API Management Service Owner role on the Azure API Management resource.

## Understand AI gateways

When you use an AI gateway with Foundry Control Plane to provide advanced policy enforcement for models, the AI gateway sits between clients and model deployments. It makes all requests flow through the API Management instance that's associated with it.

Limits apply at the project level. That is, each project can have its own TPM and quota settings.

:::image type="content" source="..\media\enable-ai-api-management-gateway-portal\gateway-architecture-diagram.png" alt-text="Diagram of the logical flow of client requests passing through Azure API Management as an AI gateway before reaching model deployments within a project.":::

Use an AI gateway for:

> [!div class="checklist"]
>
> - Multiple-team token containment (prevent one project from monopolizing capacity).
> - Cost control by capping aggregate usage.
> - Compliance boundaries for regulated workloads (enforce predictable usage ceilings).

## Configure token limits

You can configure token limits for specific model deployments within your projects:

1. In the **AI Gateway** list, select the gateway that you want to use.

1. On the gateway details pane that appears, select **Token management**.

1. Select **+ Add limit** to create a new limit for a model deployment.

1. Select the project and deployment that you want to restrict, and enter a value for **Limit (Token-per-minute)**.

1. Select **Create** to save your changes.

:::image type="content" source="..\media\enable-ai-api-management-gateway-portal\set-token-limits.png" alt-text="Screenshot of the project settings pane that shows input boxes for tokens per minute and total token quota limits." lightbox="..\media\enable-ai-api-management-gateway-portal\set-token-limits.png":::

## Understand quota windows

Token limits have two complementary enforcement dimensions:

- **TPM rate limit**: Limits token consumption to a configured maximum per minute. When requests exceed the TPM limit, the caller receives a `429 Too Many Requests` response status code.

- **Total token quota**: Limits token consumption to a configured maximum per quota period (for example, hourly, daily, weekly, monthly, or yearly). When requests exceed the quota, the caller receives a `403 Forbidden` response status code.

If you send many requests concurrently, token consumption can temporarily exceed the configured limits until responses are processed.

Adjusting a quota or TPM value affects subsequent enforcement decisions.

For more information, see [AI gateway in Azure API Management](/azure/api-management/genai-gateway-capabilities) and [Limit large language model API token usage](/azure/api-management/llm-token-limit-policy).

## Verify enforcement

1. Send test requests to a model deployment endpoint by using the project's gateway URL and key.

1. Gradually increase request frequency until the TPM limit triggers.

1. Track cumulative tokens until the quota triggers.

1. Validate that:

   - `429 Too Many Requests` (rate-limited response) is returned when requests exceed the TPM limit.
   - `403 Forbidden` (quota error) is returned when requests exhaust the quota.

## Adjust limits

1. Return to the project's **AI Gateway** settings.

1. Modify TPM or quota values.

1. Save the changes. New limits apply immediately to subsequent requests.

## Troubleshoot

| Problem | Possible cause | Action |
| --- | --- | --- |
| API Management instance doesn't appear | Provisioning delay | Refresh after a few minutes. |
| Limits aren't enforced | Misconfiguration or project not linked | Reopen settings and confirm that the enforcement toggle is on. Confirm that the AI gateway is enabled for the project and that correct limits are configured. |
| Latency is high after enablement | API Management cold start or region mismatch | Check API Management region versus resource region. Call the model directly and compare the result with the call proxied through the AI gateway to identify if performance problems are related to the gateway. |

If the admin console is slow, retry after a brief interval.

## Related content

- [AI gateway in Azure API Management](/azure/api-management/genai-gateway-capabilities)
- [What is Azure API Management?](/azure/api-management/api-management-key-concepts)
- [Limit large language model API token usage](/azure/api-management/llm-token-limit-policy)
- [How to use role-based access control in Azure API Management](/azure/api-management/api-management-role-based-access-control)
- [Role-based access control for Microsoft Foundry](../../concepts/rbac-foundry.md)
