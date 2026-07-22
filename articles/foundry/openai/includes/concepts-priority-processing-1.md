---
title: Include file
description: Include file
author: msakande
ms.reviewer: seramasu
ms.author: mopeakande
ms.service: microsoft-foundry
ms.topic: include
ms.date: 07/13/2026
ms.custom: include
---

Priority processing provides low-latency performance with the flexibility of pay-as-you-go. In this article, you enable priority processing on a model deployment, verify which service tier processed your requests, and monitor associated costs.

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Microsoft Foundry project with a model of the deployment type `GlobalStandard` or `DataZoneStandard` deployed.
- Model versions `2025-12-01` or later.

## Key use cases

- **Consistent, low latency** for responsive user experiences.
- **Pay-as-you-go simplicity** with no long-term commitments. 
- **Business-hour or bursty traffic** that benefits from scalable, cost-efficient performance. Optionally, you can combine priority processing with Provisioned Throughput Units (PTU) for steady-state capacity and cost optimization.

## Latency target

The following table lists the *latency target value* for each model that supports priority processing. The latency target value is calculated as p50 request latency on a per 5 minute basis and expressed as a percentile threshold. For example, "99% > 50 Tokens per Second (TPS)" means 99% of requests are processed at more than 50 tokens per second.

| Model | Latency target value | 
| --- | --- |
| gpt-5.6-terra, 2026-07-09<sup>1</sup> | 99% > 70 TPS |
| gpt-5.6-sol, 2026-07-09<sup>1</sup> | 99% > 50 TPS |
| gpt-5.5, 2026-04-24 | 99% > 50 TPS |
| gpt-5.4-mini, 2026-03-17 | 99% > 100 TPS |
| gpt-5.4, 2026-03-05<sup>2</sup> | 99% > 50 TPS |
| gpt-5.2, 2025-12-11 | 99% > 50 TPS |
| gpt-5.1, 2025-11-13 | 99% > 50 TPS |
| gpt-4.1, 2025-04-14<sup>2</sup> | 99% > 80 TPS |

<sup>1</sup> *Long context* for this model, that is, requests estimated to exceed **272k prompt tokens** are downgraded to standard processing and charged at the standard tier rate.

<sup>2</sup> *Long context* for this model, that is, requests estimated to exceed **128k prompt tokens** are downgraded to standard processing and charged at the standard tier rate.


