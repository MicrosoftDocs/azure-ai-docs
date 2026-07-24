---
title: Include file
description: Include file
author: msakande
ms.reviewer: ambadal
ms.author: mopeakande
ms.service: microsoft-foundry
ms.topic: include
ms.date: 07/24/2026
ms.custom: include, classic-and-new
ai-usage: ai-assisted
---

Anthropic's Claude models bring advanced conversational AI capabilities to Microsoft Foundry, enabling you to build intelligent applications with state-of-the-art language understanding and generation. Claude models excel at complex reasoning, code generation, and multimodal tasks including image analysis.

In this article, you learn how to:

- Deploy Claude models in Microsoft Foundry
- Authenticate by using Microsoft Entra ID or API keys
- Call the Claude Messages API from Python, JavaScript, or REST

For the full list of available Claude models, model versions, capabilities, quotas, and billing, see [Claude models in Microsoft Foundry](../concepts/claude-models.md).

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

## Prerequisites

- An Azure subscription with a valid payment method. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn). See [subscription type and region support](#subscription-type-and-region-support) for more details.
- Access to Microsoft Foundry with appropriate permissions to create and manage resources.
- A [Microsoft Foundry project](../../how-to/create-projects.md) created in a supported deployment location. All Claude models (Hosted on Azure and Hosted on Anthropic infrastructure) support Global Standard deployments. The Hosted on Azure versions of some Claude models are also available for Data Zone Standard (US) deployment. For the exact Azure regions where Claude models are available for deployment, see [Region availability by deployment type](../concepts/models-from-partners.md#region-availability-by-deployment-type).
- [Foundry Models from partners and community](../concepts/models-from-partners.md) require access to **Azure Marketplace** to create subscriptions. Ensure that you have the [permissions required to subscribe to model offerings](../how-to/configure-marketplace.md).
- **Contributor** or **Owner** role on the resource group to deploy models. For more information, see [Azure RBAC roles](/azure/role-based-access-control/built-in-roles).

## Subscription type and region support

[!INCLUDE [claude-usage-restriction](claude-usage-restriction.md)]

## Use the Claude on Foundry starter kit

To deploy Claude models in Microsoft Foundry using infrastructure-as-code tools, see [Deploy Claude models in Microsoft Foundry using Bicep or Terraform](/azure/developer/ai/how-to/deploy-claude-foundry?context=/azure/foundry/context/context). The article is based on the [Claude on Foundry starter kit](https://github.com/Azure-Samples/claude#readme), and it covers how to provision a Foundry account and project, deploy your chosen Claude model, and configure authentication with Microsoft Entra ID or API keys using Bicep or Terraform automation.
