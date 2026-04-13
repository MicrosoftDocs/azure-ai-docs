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

## When to enable spillover

To maximize the utilization of your provisioned deployment, enable spillover for all global and data zone provisioned deployments. With spillover, bursts or fluctuations in traffic can be automatically managed by the service. This capability reduces the risk of experiencing disruptions when a provisioned deployment is fully utilized. Alternatively, spillover is configurable per-request to provide flexibility across different scenarios and workloads. Spillover also works with the [Foundry Agent Service](../../agents/overview.md).

## When spillover comes into effect

When you enable spillover for a deployment or configure it for a given inference request, spillover initiates when a specific non-`200` response code is received as a result of one of these scenarios:

- Provisioned throughput units (PTU) are completely used, which results in a `429` response code.

- You send a long context token request, which results in a `400` error code. For example, when you use `gpt 4.1` series models, PTU supports only context lengths less than 128K and returns HTTP 400.

- Server errors occur when processing your request, which results in error code `500` or `503`.

When a request results in one of these non-`200` response codes, Azure OpenAI automatically sends the request from your provisioned deployment to your standard deployment to be processed.

> [!NOTE]
> Even if a subset of requests is routed to the standard deployment, the service prioritizes sending requests to the provisioned deployment before sending any overage requests to the standard deployment. This prioritization might incur additional latency.
