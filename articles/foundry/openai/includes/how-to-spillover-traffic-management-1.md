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

This article describes how to manage traffic with spillover for provisioned deployments in Azure OpenAI. Spillover manages traffic fluctuations by routing overage traffic to a corresponding standard deployment. This optional capability can be set for all requests on a deployment or managed on a per-request basis, helping you reduce disruptions during traffic bursts.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learncognitive-services).

- A provisioned managed deployment and a standard deployment in the same Azure OpenAI resource

- Azure CLI installed for REST API examples, or access to the Foundry portal

- The `AZURE_OPENAI_ENDPOINT` environment variable set to your Azure OpenAI endpoint URL

- **Cognitive Services Contributor** role or higher on the Azure OpenAI resource to create or modify deployments
