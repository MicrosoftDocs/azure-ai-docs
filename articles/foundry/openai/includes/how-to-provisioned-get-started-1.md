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

This article covers the end-to-end tasks for operating provisioned throughput deployments in production: managing provisioned throughput unit (PTU) quota, creating deployments, purchasing Azure Reservations, making inference calls, benchmarking, monitoring utilization, handling high load, scaling, and cleaning up resources.

This article assumes familiarity with the concepts in [What is provisioned throughput?](../concepts/provisioned-throughput.md) and the billing details in [PTU billing and cost management](../concepts/provisioned-throughput-billing.md).

## Prerequisites

- An Azure subscription with a valid payment method. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.
- **Azure Contributor** or **Cognitive Services Contributor** role on the subscription or resource group where you plan to create the deployment.
- A [Microsoft Foundry project](../../how-to/create-projects.md) in the region where you have PTU quota. A Foundry project is managed under a Foundry resource.

## Estimate PTU requirements

Before creating a provisioned deployment, you should estimate how many PTUs your workload needs. For the estimation formulas, a worked example, and walkthrough of the capacity calculator, see [Determine PTU sizing for a workload](../how-to/provisioned-throughput-sizing.md).