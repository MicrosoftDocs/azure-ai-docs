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

In this quickstart, you create a provisioned throughput deployment in Microsoft Foundry, make an inference call to confirm it works, and view its utilization metric.

A provisioned throughput deployment gives your application dedicated model processing throughput with predictable latency. Billing is done per provisioned throughput unit (PTU) per hour. For long-term workloads, Azure Reservations offer financial discounts compared to hourly billing. For a full conceptual introduction, see [What is provisioned throughput for Foundry Models?](../concepts/provisioned-throughput.md).


## Prerequisites

- An Azure subscription with a valid payment method. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.
- **Azure Contributor** or **Cognitive Services Contributor** role on the subscription or resource group where you plan to create the deployment.
- A [Microsoft Foundry project](../../how-to/create-projects.md) in the region where you have PTU quota. A Foundry project is managed under a Foundry resource.
- Optionally, for deployment using Azure CLI, have [Azure CLI installed](/cli/azure/install-azure-cli).

## Check model and region availability

Before creating a deployment, confirm that your model supports provisioned throughput in your target region.

1. Go to the [model and region availability table](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=provisioned) to see if your model supports provisioned throughput deployment in your target region.
1. Filter by your region and verify that the model appears in a **Provisioned** deployment type.

Also note the model's minimum PTU count, as you need this information when you configure the deployment. Minimums vary by model and are listed in [Deployment parameters and throughput values by model](../how-to/provisioned-throughput-sizing.md#deployment-parameters-and-throughput-values-by-model).
