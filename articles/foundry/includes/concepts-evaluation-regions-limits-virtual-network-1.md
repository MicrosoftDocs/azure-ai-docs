---
title: Include file
description: Include file
author: lgayhardt
ms.reviewer: skohlmeier
ms.author: lagayhar
ms.service: microsoft-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include, references_regions
---

This article provides an overview of which regions support AI-assisted evaluators, the rate limits that apply to evaluation runs, how to configure virtual network support for network isolation, and using your own storage account to run evaluations.

## Regional availability

### Supported regions for Agent playground evaluations

The agent playground evaluations are supported in the following regions:

| Americas | Europe |
|--|--|
| East US 2 | France Central |
| West US | Norway East |
| West US 2 | Sweden Central |
| West US 3 | Germany West Central |
| Central US | Italy North |
| East US | Poland Central |
| North Central US | Spain Central |
| South Central US |  |

### Supported regions for batch evaluations

The batch evaluations are supported in the following regions:

| Americas | Europe | Asia Pacific | Middle East & Africa |
|--|--|--|--|
| Brazil South | France Central | Australia East | South Africa North |
| Canada Central | Germany West Central | Central India | UAE North |
| Canada East | Italy North | East Asia |  |
| Central US | North Europe | Japan East |  |
| East US | Norway East | Japan West |  |
| East US 2 | Poland Central | Korea Central |  |
| North Central US | Spain Central | South India |  |
| South Central US | Sweden Central | Southeast Asia |  |
| West Central US | Switzerland North |  |  |
| West US | UK South |  |  |
| West US 2 | West Europe |  |  |
| West US 3 |  |  |  |

### Risk and safety evaluators and AI red teaming region support

The following safety evaluators and AI red teaming are supported in these regions: Hate and unfairness, Sexual, Violent, Self-harm, Indirect attack, Code vulnerabilities, Ungrounded attributes, and AI red teaming.

| Americas | Europe | Asia Pacific |
|--|--|--|
| East US 2 | France Central | Australia East |
| North Central US | Sweden Central |  |
|  | Switzerland West |  |

Supported regions for Groundedness Pro:

- East US 2
- Sweden Central

Supported regions for Protected material:

- East US 2

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

Virtual network support for evaluation requires network injection (subnet delegation), but if you **only need evaluation capabilities** and do not require full agent support (Cosmos DB, AI Search, or project capability host), consider using the simplified [evaluation-only setup template (15a)](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/15a-private-network-evaluation-only-setup) instead. It deploys a minimal network-secured environment tailored for evaluation scenarios with fewer resources and reduced complexity.

> [!NOTE]
> If you connect Application Insights, evaluation data is sent to it.

> [!IMPORTANT]
> To prevent evaluation and red teaming run failures, assign the Foundry User role to the project's Managed Identity during initial project setup.

[!INCLUDE [role-rename-note](./role-rename-note.md)]

### Virtual network region support

Bringing your own virtual network for evaluation is supported in the following regions:

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
