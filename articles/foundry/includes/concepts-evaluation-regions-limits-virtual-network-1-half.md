---
title: Include file
description: Include file
author: lgayhardt
ms.author: lagayhar
ms.service: microsoft-foundry
ms.topic: include
ms.date: 10/01/2026
ms.custom: include, references_regions
ai-usage: ai-assisted
---

### Supported regions for data generation

The following regions support synthetic data generation and trace-to-dataset generation:

| Americas | Europe | Asia Pacific | Middle East & Africa |
|--|--|--|--|
| Brazil South | France Central | Australia East | South Africa North |
| Canada Central | Germany West Central | Japan East | UAE North |
| Canada East | Italy North | Japan West |  |
| Central US | Norway East | Korea Central |  |
| East US | Poland Central | South India |  |
| East US 2 | Spain Central | Southeast Asia |  |
| North Central US | Sweden Central |  |  |
| South Central US | Switzerland North |  |  |
| West Central US | Switzerland West |  |  |
| West US | UK South |  |  |
| West US 3 | UK West |  |  |
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
