---
title: Include file
description: Include file
author: msakande
ms.reviewer: seramasu
ms.author: mopeakande
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

Priority processing provides low-latency performance with the flexibility of pay-as-you-go. In this article, you enable priority processing on a model deployment, verify which service tier processed your requests, and monitor associated costs.

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Microsoft Foundry project with a model of the deployment type `GlobalStandard` or `DataZoneStandard` deployed.
- API version `2025-12-01` or later.

## Key use cases

- **Consistent, low latency** for responsive user experiences.
- **Pay-as-you-go simplicity** with no long-term commitments. 
- **Business-hour or bursty traffic** that benefits from scalable, cost-efficient performance. Optionally, you can combine priority processing with Provisioned Throughput Units (PTU) for steady-state capacity and cost optimization.

## Latency target

| Model | Latency target value<sup>2</sup> | 
| --- | --- |
| gpt-5.4, 2026-03-05<sup>1</sup> | 99% > 50 Tokens Per Second |
| gpt-5.2, 2025-12-11 | 99% > 50 Tokens Per Second |
| gpt-5.1, 2025-11-13 | 99% > 50 Tokens Per Second |
| gpt-4.1, 2025-04-14<sup>1</sup> | 99% > 80 Tokens Per Second |

<sup>1</sup> Long context requests (that is, requests estimated at larger than 128k prompt tokens) will be downgraded to standard processing and you'll be charged at the standard tier rate.

<sup>2</sup> Calculated as p50 request latency on a per 5 minute basis.
