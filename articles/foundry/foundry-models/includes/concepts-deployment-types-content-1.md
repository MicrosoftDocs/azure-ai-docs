---
title: include file
description: include file
ai-usage: ai-assisted
author: alvinashcraft
ms.author: aashcraft
ms.service: microsoft-foundry
ms.topic: include
ms.date: 08/06/2026
ms.custom: include, classic-and-new
---

When you deploy a model in Microsoft Foundry, you choose a deployment type that determines:

- **Where your data is processed** (global, data zone, or single region)
- **How you pay** (pay-per-token or reserved capacity)
- **Performance characteristics** (latency variance, throughput limits)

These deployment types apply to the **Serverless API** deployment option. Open-source and custom models that use **managed compute** don't use these types. For how the options differ, see [Deployment overview for Microsoft Foundry Models](../../concepts/deployments-overview.md).

The service offers three main categories: *standard* (pay-per-token), *provisioned* (reserved capacity), and *batch* (discounted asynchronous processing). A *Developer* type is also available for fine-tuned model evaluation. Within the standard and provisioned categories, you can choose global, data zone, or regional processing based on your compliance requirements.
