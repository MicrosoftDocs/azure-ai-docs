---
title: Rate limits, region support, and enterprise features for evaluation
titleSuffix: Microsoft Foundry
description: Learn about region availability, rate limits, virtual network support, and using your own storage account for evaluation in Microsoft Foundry.
author: lgayhardt
ms.author: lagayhar
ms.reviewer: skohlmeier
ms.date: 02/10/2026
ms.topic: how-to
ms.service: azure-ai-foundry
monikerRange: 'foundry-classic || foundry'
ms.custom: references_regions
---

# Rate limits, region support, and enterprise features for evaluation

[!INCLUDE [version-banner](../includes/version-banner.md)]  

This article provides an overview of which regions support AI-assisted evaluators, the rate limits that apply to evaluation runs, how to configure virtual network support for network isolation, and using your own storage account to run evaluations.

## Region support

### Risk and safety evaluators and AI red teaming region support

Certain AI-assisted evaluators and AI red teaming are available only in the following regions:

| Region | Hate and unfairness, Sexual, Violent, Self-harm, Indirect attack, Code vulnerabilities, Ungrounded attributes,  AI red teaming | Groundedness Pro | Protected material |
|--|--|--|--|
| East US 2 | Supported | Supported | Supported |
| Sweden Central | Supported | Supported | N/A |
| US North Central | Supported | N/A | N/A |
| France Central | Supported | N/A | N/A |
| Switzerland West | Supported | N/A | N/A |

### Agent playground evaluation region support

The Foundry portal supports agent playground evaluation in the following regions:

- East US 2
- West US
- West US 2
- West US 3
- France Central
- Norway East
- Sweden Central

### Unsupported regions for batch evaluation

Batch evaluations aren't supported in the following regions:

- Canada Central
- Qatar Central
- South Central US
- Southeast Asia
- Spain Central

### Unsupported regions for Azure OpenAI graders

The following regions don't support Azure OpenAI graders or custom code evaluator:

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

For network isolation, you can bring your own virtual network for evaluation. To learn more, see [How to configure a private link](../how-to/configure-private-link.md).

> [!NOTE]
> If you connect Application Insights, evaluation data is sent to it. Virtual network support for Application Insights and tracing isn't available. Inline datasource isn't supported.

> [!IMPORTANT]
> To prevent evaluation and red teaming run failures, assign the Azure AI User role to the project's Managed Identity during initial project setup.

### Virtual network region support

Bringing your own virtual network for evaluation is supported in all regions except:

- Central India
- East Asia
- North Europe
- Qatar Central

## Bring your own storage

You can  use your own storage account to run evaluations.

::: moniker range="foundry-classic"
You can either use a Bicep template or [manually create and provision access](../how-to/evaluations-storage-account.md) to your storage account in the Azure portal. To use a Bicep template, follow these steps.
::: moniker-end

1. Create and connect your storage account to your Foundry project at the resource level. You can [use a Bicep template](https://github.com/azure-ai-foundry/foundry-samples/blob/main/infrastructure/infrastructure-setup-bicep/01-connections/connection-storage-account.bicep), which provisions and connects a storage account to your Foundry project with key authentication.
1. Make sure the connected storage account has access to all projects.
1. If you connected your storage account by using Microsoft Entra ID, make sure to give managed identity **Storage Blob Data Owner** permissions to both your account and the Foundry project resource in the Azure portal.

## Related content

- [How to configure a private link](../how-to/configure-private-link.md)
- [Observability for generative AI applications](observability.md)
