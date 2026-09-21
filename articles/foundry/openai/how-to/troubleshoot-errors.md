---
title: Troubleshoot common HTTP errors - Azure OpenAI in Microsoft Foundry
description: Learn how to diagnose and resolve common HTTP errors when using Azure OpenAI in Microsoft Foundry Models, including 400, 401, 403, 404, 429, and 500 errors.
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: troubleshooting
ms.date: 09/20/2026
author: alvinashcraft
ms.author: aashcraft
ai-usage: ai-assisted
---

# Troubleshoot common HTTP errors for Azure OpenAI

This article helps you diagnose and resolve common HTTP errors returned by Azure OpenAI in Microsoft Foundry Models inference endpoints.

## Error reference

| HTTP Status | Error | Common Causes | Resolution |
|------------|-------|---------------|------------|
| **400** | Bad Request | Invalid request payload, context length exceeded, unsupported parameters, content filtering blocked a prompt or response | Check the error message for the validation failure. Content filtering returns HTTP 400 with the `content_filter` code. See [Content filtering](../concepts/content-filter-severity-levels.md). |
| **401** | Unauthorized | Invalid API key, expired or misconfigured Microsoft Entra token, wrong token scope or audience, missing RBAC role assignment | Verify your API key or token. For Microsoft Entra ID authentication, use the `https://ai.azure.com/.default` scope for Azure OpenAI endpoints. See [Configure keyless authentication with Microsoft Entra ID](../../foundry-models/how-to/configure-entra-id.md#troubleshooting). |
| **403** | Forbidden | See [HTTP 403 causes](#http-403-forbidden) below | Depends on the specific cause |
| **404** | Not Found | Incorrect endpoint URL, deployment name doesn't exist, unsupported API version | Verify your endpoint URL, deployment name, and API version in the [REST API reference](../reference.md). |
| **429** | Too Many Requests | Rate limit exceeded, system capacity throttling, or a temporary rate limit adjustment | Follow the `retry-after-ms` header when present. Review [quotas and limits](../quotas-limits.md) and [429 throttling guidance](quota.md#understanding-429-throttling-errors-and-what-to-do). |
| **500 / 503** | Server Error | Transient service issue, backend overload | Retry with exponential backoff. If errors persist for more than a few minutes, check [Azure Service Health](https://portal.azure.com/#blade/Microsoft_Azure_Health/AzureHealthBrowseBlade) or file a support request. |

## HTTP 403 Forbidden

A 403 response means the server understood your request but refuses to authorize it. Unlike 401, a 403 indicates that your credentials might be valid but access is denied.

### Network access denied

The resource's network access controls blocked your request.

**Symptoms:**

- Error message references network access, IP restriction, or private endpoint.
- You recently changed virtual network, firewall, or private endpoint settings.

**Resolution:**

1. In the Azure portal, go to your resource and select **Networking**.
1. Verify your client IP is in the allowed list if you use IP firewall rules.
1. If you use a private endpoint, verify DNS resolves to the private IP. See [Troubleshoot private endpoint connectivity](/troubleshoot/azure/private-link/troubleshoot-private-endpoint-connectivity).
1. Check that network security group (NSG) rules on the subnet aren't blocking traffic.

To set up a Foundry private endpoint, see [Configure private link](../../how-to/configure-private-link.md). For virtual network, firewall, and IP rules, see [Configure Azure AI services virtual networks](/azure/ai-services/cognitive-services-virtual-networks).

### Resource suspended (abuse policy)

Automated abuse detection systems suspended your resource because it violated the [Microsoft Online Services Acceptable Use Policy](https://www.microsoft.com/licensing/terms/product/ForOnlineServices/all).

**Symptoms:**

- Error message contains "resource has been temporarily blocked".
- All requests to the resource return 403.

**Resolution:**
Create a [support request](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade) and include:

- Your subscription ID and resource name.
- A description of your use case.
- Corrective actions you already took.

For more information, see [Abuse monitoring](../concepts/abuse-monitoring.md).

## Related content

- [Azure OpenAI REST API reference](../reference.md)
- [Quotas and limits](../quotas-limits.md)
- [429 throttling guidance](quota.md#understanding-429-throttling-errors-and-what-to-do)
- [Content filtering](../concepts/content-filter-severity-levels.md)
- [Abuse monitoring](../concepts/abuse-monitoring.md)
- [Azure Service Health](https://portal.azure.com/#blade/Microsoft_Azure_Health/AzureHealthBrowseBlade)
