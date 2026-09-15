---
title: Include file
description: Include file
author: lgayhardt
ms.author: lagayhar
ms.service: microsoft-foundry
ms.topic: include
ms.date: 08/13/2026
ms.custom: include, references_regions
---

### Supported regions for data generation

The following regions support synthetic data generation and trace-to-dataset generation:

| Americas | Europe | Asia Pacific | Middle East & Africa |
|--|--|--|--|
| East US | France Central | Australia East | South Africa North |
| East US 2 | Germany West Central | Japan East | UAE North |
| North Central US | Italy North | South India |  |
| South Central US | Norway East |  |  |
| West US | Poland Central |  |  |
| West US 3 | Sweden Central |  |  |
|  | Switzerland North |  |  |
|  | UK South |  |  |
|  | West Europe |  |  |

### Azure OpenAI graders regional availability

For the Azure OpenAI graders regional list, see [Regional availability](../../foundry-classic/openai/how-to/evaluations.md#regional-availability).

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

Virtual network support for evaluation requires network injection (subnet delegation), but if you **only need evaluation capabilities** and don't require full agent support (Cosmos DB, AI Search, or project capability host), consider using the simplified [evaluation-only setup template (15a)](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/15a-private-network-evaluation-only-setup) instead. It deploys a minimal network-secured environment tailored for evaluation scenarios with fewer resources and reduced complexity.

> [!NOTE]
> If you connect Application Insights, evaluation data is sent to it.

> [!IMPORTANT]
> To prevent evaluation and red teaming run failures, assign the Foundry User role to the project's Managed Identity during initial project setup.

[!INCLUDE [role-rename-note](./role-rename-note.md)]

### Virtual network region support

You can bring your own virtual network for evaluation in the following regions:

| Americas | Europe | Asia Pacific | Middle East & Africa |
|--|--|--|--|
| Brazil South | France Central | Australia East | South Africa North |
| Canada Central | Germany West Central | Japan East | UAE North |
| Canada East | Italy North | Korea Central |  |
| East US | Norway East | South India |  |
| East US 2 | Poland Central | Southeast Asia |  |
| North Central US | Spain Central |  |  |
| South Central US | Sweden Central |  |  |
| West US | Switzerland North |  |  |
| West US 2 | UK South |  |  |
| West US 3 | West Europe |  |  |

## Virtual network support for data generation

Data generation (synthetic data generation and trace-to-dataset generation) uses the same network injection (subnet delegation) and [evaluation-only setup template (15a)](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/15a-private-network-evaluation-only-setup) as evaluation. To learn more, see [How to configure a private link](../how-to/configure-private-link.md). Supported regions match [supported regions for data generation](#supported-regions-for-data-generation).
