---
title: Include file
description: Include file
author: msakande
ms.reviewer: ambadal
ms.author: mopeakande
ms.service: microsoft-foundry
ms.topic: include
ms.date: 06/23/2026
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
- A [Microsoft Foundry project](../../how-to/create-projects.md) created in a supported deployment location. All Claude models (Hosted on Azure and Hosted on Anthropic infrastructure) support Global Standard deployments in **East US2** or **Sweden Central**. The `claude-opus-4-8` model (Hosted on Azure) is also available for Data Zone Standard (US) deployment.
- [Foundry Models from partners and community](../concepts/models-from-partners.md) require access to **Azure Marketplace** to create subscriptions. Ensure that you have the [permissions required to subscribe to model offerings](../how-to/configure-marketplace.md).
- **Contributor** or **Owner** role on the resource group to deploy models. For more information, see [Azure RBAC roles](/azure/role-based-access-control/built-in-roles).

## Subscription type and region support

[!INCLUDE [claude-usage-restriction](claude-usage-restriction.md)]

## Use the Claude on Foundry starter kit

To get started with Claude on Foundry quickly, use the [Claude on Foundry starter kit](https://github.com/Azure-Samples/claude#readme). The starter kit uses a single `azd up` command to provision a Foundry account, project, and your chosen Claude model deployments by using either Bicep or Terraform. It then wires the Anthropic SDK and the Claude Code CLI to call your deployment over Microsoft Entra ID, with no API keys to manage.
