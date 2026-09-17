---
title: Claude Model Quotas and Rate Limits Reference
description: Explore Claude model quotas and rate limits in Microsoft Foundry, including subscription defaults, prompt caching, and quota increase steps.
author: msakande
ms.author: mopeakande
ms.reviewer: ambadal
ms.service: microsoft-foundry
ms.topic: include
ms.date: 09/11/2026
ms.custom: include, classic-and-new
ai-usage: ai-assisted
---

Claude model quotas and rate limits in Microsoft Foundry determine how much traffic each model can process. This reference explains how deployments share quota, how prompt caching affects token accounting, and which default limits apply to each Azure subscription type.

## Claude quota scope

Microsoft Foundry manages Claude model quota at the subscription level. Resources and regions share quota instead of receiving separate allocations.

- All Global Standard deployments of the same model and version in a subscription draw from one shared quota pool across all regions.
- All Data Zone Standard deployments of the same model and version in a subscription draw from a shared quota pool within each data zone, such as the US data zone.

For general quota management guidance, see [Microsoft Foundry Models quotas and limits](../quotas-limits.md).

## Rate-limit measurements

Claude models use the following rate-limit measurements for each model:

- **Requests per minute (RPM)** measures the number of requests.
- **Uncached input tokens per minute (ITPM)** measures input tokens that aren't read from a prompt cache.
- **Output tokens per minute (OTPM)** measures tokens that the model generates.

### Cache-aware ITPM

For most Claude models, only uncached input tokens count toward ITPM limits. These tokens include:

- **Input tokens**: Tokens in the request after the last cache breakpoint (uncached input).
- **Cache creation input tokens**: Tokens written to either the 5-minute or 1-hour prompt cache.

> [!TIP]
> The _total input tokens_ is the sum of **Input tokens**, **Cache creation input tokens**, and **Cache read input tokens** (the tokens read from cache). However, the _Cache read input tokens_ don't count towards ITPM. **OTPM** also doesn't count towards ITPM.

For more information about rate limits and prompt caching, see [Rate limits in the Claude API documentation](https://platform.claude.com/docs/en/api/rate-limits#rate-limits).

## Default rate limits by subscription type

Your Azure subscription type determines your default rate limits. The **Version 2: Hosted on Azure** and **Version 1: Hosted on Anthropic infrastructure** columns indicate whether each model and deployment type combination supports quota allocation. **Yes** means the combination supports quota allocation, but its default numeric limit might be zero. **N/A** means the combination doesn't support quota allocation for that deployment type. The RPM, ITPM, and OTPM columns show the default capacity.

# [Pay-as-you-go](#tab/pay-go)

#### Pay-as-you-go

| Model             | Deployment type         | Version 2: Hosted on Azure | Version 1: Hosted on Anthropic infrastructure | RPM       | ITPM      | OTPM     |
|:------------------|:------------------------|:--------------------------:|:---------------------------------------------:|----------:|----------:|---------:|
| claude-fable-5-1  | Global Standard         | N/A                        | Yes                                           | 0         | 0         | 0        |
| claude-fable-5    | Global Standard         | N/A                        | Yes                                           | 0         | 0         | 0        |
| claude-opus-5     | Global Standard         | Yes                        | Yes                                           | 40        | 40,000    | 8,000    |
| claude-opus-5     | Data Zone Standard (US) | Yes                        | N/A                                           | 40        | 40,000    | 8,000    |
| claude-opus-4-8   | Global Standard         | Yes                        | Yes                                           | 40        | 40,000    | 8,000    |
| claude-opus-4-8   | Data Zone Standard (US) | Yes                        | N/A                                           | 40        | 40,000    | 8,000    |
| claude-opus-4-7   | Global Standard         | N/A                        | Yes                                           | 40        | 40,000    | 8,000    |
| claude-opus-4-6   | Global Standard         | N/A                        | Yes                                           | 40        | 40,000    | 8,000    |
| claude-opus-4-5   | Global Standard         | N/A                        | Yes                                           | 40        | 40,000    | 8,000    |
| claude-sonnet-5   | Global Standard         | Yes                        | Yes                                           | 40        | 40,000    | 8,000    |
| claude-sonnet-5   | Data Zone Standard (US) | Yes                        | N/A                                           | 40        | 40,000    | 8,000    |
| claude-sonnet-4-6 | Global Standard         | N/A                        | Yes                                           | 80        | 80,000    | 16,000   |
| claude-sonnet-4-5 | Global Standard         | N/A                        | Yes                                           | 80        | 80,000    | 16,000   |
| claude-haiku-4-5  | Global Standard         | Yes                        | Yes                                           | 80        | 80,000    | 16,000   |

# [Enterprise and MCA-E](#tab/enterprise)

#### Enterprise and MCA-E

| Model             | Deployment type         | Version 2: Hosted on Azure | Version 1: Hosted on Anthropic infrastructure | RPM       | ITPM       | OTPM      |
|:------------------|:------------------------|:--------------------------:|:---------------------------------------------:|----------:|-----------:|----------:|
| claude-fable-5-1  | Global Standard         | N/A                        | Yes                                           | 4,000     | 4,000,000  | 800,000   |
| claude-fable-5    | Global Standard         | N/A                        | Yes                                           | 4,000     | 4,000,000  | 800,000   |
| claude-opus-5     | Global Standard         | Yes                        | Yes                                           | 10,000    | 10,000,000 | 2,000,000 |
| claude-opus-5     | Data Zone Standard (US) | Yes                        | N/A                                           | 10,000    | 10,000,000 | 2,000,000 |
| claude-opus-4-8   | Global Standard         | Yes                        | Yes                                           | 10,000    | 10,000,000 | 2,000,000 |
| claude-opus-4-8   | Data Zone Standard (US) | Yes                        | N/A                                           | 10,000    | 10,000,000 | 2,000,000 |
| claude-opus-4-7   | Global Standard         | N/A                        | Yes                                           | 10,000    | 10,000,000 | 2,000,000 |
| claude-opus-4-6   | Global Standard         | N/A                        | Yes                                           | 10,000    | 10,000,000 | 2,000,000 |
| claude-opus-4-5   | Global Standard         | N/A                        | Yes                                           | 10,000    | 10,000,000 | 2,000,000 |
| claude-sonnet-5   | Global Standard         | Yes                        | Yes                                           | 10,000    | 10,000,000 | 2,000,000 |
| claude-sonnet-5   | Data Zone Standard (US) | Yes                        | N/A                                           | 10,000    | 10,000,000 | 2,000,000 |
| claude-sonnet-4-6 | Global Standard         | N/A                        | Yes                                           | 10,000    | 10,000,000 | 2,000,000 |
| claude-sonnet-4-5 | Global Standard         | N/A                        | Yes                                           | 10,000    | 10,000,000 | 2,000,000 |
| claude-haiku-4-5  | Global Standard         | Yes                        | Yes                                           | 10,000    | 10,000,000 | 2,000,000 |

# [Free Trial](#tab/free)

#### Free Trial

| Model             | Deployment type         | Version 2: Hosted on Azure | Version 1: Hosted on Anthropic infrastructure | RPM       | ITPM      | OTPM     |
|:------------------|:------------------------|:--------------------------:|:---------------------------------------------:|----------:|----------:|---------:|
| claude-fable-5-1  | Global Standard         | N/A                        | Yes                                           | 0         | 0         | 0        |
| claude-fable-5    | Global Standard         | N/A                        | Yes                                           | 0         | 0         | 0        |
| claude-opus-5     | Global Standard         | Yes                        | Yes                                           | 0         | 0         | 0        |
| claude-opus-5     | Data Zone Standard (US) | Yes                        | N/A                                           | 0         | 0         | 0        |
| claude-opus-4-8   | Global Standard         | Yes                        | Yes                                           | 0         | 0         | 0        |
| claude-opus-4-8   | Data Zone Standard (US) | Yes                        | N/A                                           | 0         | 0         | 0        |
| claude-opus-4-7   | Global Standard         | N/A                        | Yes                                           | 0         | 0         | 0        |
| claude-opus-4-6   | Global Standard         | N/A                        | Yes                                           | 0         | 0         | 0        |
| claude-opus-4-5   | Global Standard         | N/A                        | Yes                                           | 0         | 0         | 0        |
| claude-sonnet-5   | Global Standard         | Yes                        | Yes                                           | 0         | 0         | 0        |
| claude-sonnet-5   | Data Zone Standard (US) | Yes                        | N/A                                           | 0         | 0         | 0        |
| claude-sonnet-4-6 | Global Standard         | N/A                        | Yes                                           | 0         | 0         | 0        |
| claude-sonnet-4-5 | Global Standard         | N/A                        | Yes                                           | 0         | 0         | 0        |
| claude-haiku-4-5  | Global Standard         | Yes                        | Yes                                           | 0         | 0         | 0        |

---

## Quota checks and requests for increase

The  **Quota** page in the Foundry portal shows the quota available to your subscription. 

To request quota beyond the default limits, submit the [quota increase request form](https://aka.ms/oai/stuquotarequest). Quota increase requests are evaluated individually and aren't guaranteed to be approved.

## Rate-limit error handling

When an application exceeds a rate limit, the API returns an HTTP 429 response. Implement exponential backoff, reduce request frequency or token usage, and request more quota when the default limits don't meet your workload requirements.

For other errors you might encounter when you deploy or call Claude models, see [Troubleshoot Claude model deployments](../how-to/use-foundry-models-claude.md#troubleshooting).

## Related content

- [Overview: Claude models in Microsoft Foundry](../concepts/claude-models.md)
- [Deploy and use Claude models in Microsoft Foundry](../how-to/use-foundry-models-claude.md)
- [Claude Consumption Units billing in Microsoft Foundry](../concepts/claude-models-billing.md)
- [Microsoft Foundry Models quotas and limits](../quotas-limits.md)