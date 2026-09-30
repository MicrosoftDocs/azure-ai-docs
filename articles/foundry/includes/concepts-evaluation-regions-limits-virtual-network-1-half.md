---
title: Include file
description: Include file
author: lgayhardt
ms.author: lagayhar
ms.service: microsoft-foundry
ms.topic: include
ms.date: 08/13/2026
ms.custom: include, references_regions
ai-usage: ai-assisted
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
