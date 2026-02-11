---
title: Region support, rate limits, and virtual network support for evaluation
titleSuffix: Microsoft Foundry
description: Learn about region availability, rate limits, and virtual network support for evaluation in Microsoft Foundry.
author: lgayhardt
ms.author: lagayhar
ms.reviewer: skohlmeier
ms.date: 02/10/2026
ms.topic: how-to
ms.service: azure-ai-foundry
monikerRange: 'foundry-classic || foundry'
---

# Region support, rate limits, and virtual network support for evaluation

[!INCLUDE [version-banner](../includes/version-banner.md)]  

This article provides an overview of which regions support AI-assisted evaluators, the rate limits that apply to evaluation runs, and how to configure virtual network support for network isolation.

## Region support

Currently, certain AI-assisted evaluators are available only in the following regions:

| Region | Hate and unfairness, Sexual, Violent, Self-harm, Indirect attack, Code vulnerabilities, Ungrounded attributes | Groundedness Pro | Protected material |
|--|--|--|--|
| East US 2 | Supported | Supported | Supported |
| Sweden Central | Supported | Supported | N/A |
| US North Central | Supported | N/A | N/A |
| France Central | Supported | N/A | N/A |
| Switzerland West | Supported | N/A | N/A |

> [!NOTE]
> Red teaming agent is available only in regions that support risk and safety evaluators.

### Agent playground evaluation region support

| Region | Status |
|--|--|
| East US | Supported |
| East US 2 | Supported |
| West US | Supported |
| West US 2 | Supported |
| West US 3 | Supported |
| France Central | Supported |
| Norway East | Supported |
| Sweden Central | Supported |

### Batch evaluation excluded regions

Batch evaluations aren't supported in the following regions:

- Canada Central
- Qatar Central
- South Central US
- Southeast Asia
- Spain Central

### OpenAI grader excluded regions

The following regions don't support OpenAI grader or custom code evaluator:

- Canada East
- Central India
- East Asia
- East US
- North Europe
- South India

## Rate limits

The following rate limits apply to evaluation runs:

| Limit | Value |
|--|--|
| Maximum size per row | 2 MB |
| Maximum rows per batch evaluation | 100,000 |

Evaluation run creations are rate-limited at the tenant, subscription, and project levels. If you exceed the limit:

- The response includes a `retry-after` header with the wait time.
- The response body contains rate limit details.

Use exponential backoff when retrying failed requests.

## Virtual network support for evaluation

For network isolation purposes, you can bring your own virtual network for evaluation. To learn more, see [How to configure a private link](../how-to/configure-private-link.md).

> [!NOTE]
> If you connect Application Insights, evaluation data is sent to it. Virtual network support for Application Insights and tracing isn't available. Inline datasource isn't supported.

> [!IMPORTANT]
> To prevent evaluation and red teaming run failures, assign the Azure AI User role to the project's Managed Identity during initial project setup.

### Virtual network region support

Bring your own virtual network for evaluation is supported in all regions except for Central India, East Asia, North Europe, and Qatar Central.

## Related content

- [How to configure a private link](../how-to/configure-private-link.md)
- [Observability for generative AI applications](observability.md)
