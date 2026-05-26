---
title: Include file
description: Include file
author: msakande
ms.reviewer: seramasu
ms.author: mopeakande
ms.service: microsoft-foundry
ms.topic: include
ms.date: 05/25/2026
ms.custom: include
---

Spillover manages traffic fluctuations on provisioned deployments by automatically routing overage requests to a corresponding standard deployment. When your provisioned deployment is fully utilized and returns non-200 responses (such as a `429` when PTUs are exhausted), spillover redirects those requests to the standard deployment, helping you reduce disruptions during traffic bursts. This optional capability can be configured for all requests on a deployment or managed on a per-request basis.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learncognitive-services).
- A provisioned managed deployment and a standard deployment in the same Foundry resource.
- Azure CLI installed for REST API examples, or access to the Foundry portal.
- The `AZURE_OPENAI_ENDPOINT` environment variable set to your Azure OpenAI endpoint URL.
- **Cognitive Services Contributor** role or higher on the Foundry resource to create or modify deployments.

