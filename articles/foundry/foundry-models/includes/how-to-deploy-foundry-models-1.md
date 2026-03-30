---
title: Include file
description: Include file
author: msakande
ms.reviewer: sgilley
ms.author: mopeakande
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

In this article, you learn how to use the Foundry portal to deploy a Foundry Model in a Foundry resource for inference. Foundry Models include models such as Azure OpenAI models, Meta Llama models, and more. After you deploy a Foundry Model, you can interact with it in the Foundry Playground and use it from code.

This article uses a Foundry Model from partners and community `Llama-3.2-90B-Vision-Instruct` for illustration. Models from partners and community require that you subscribe to Azure Marketplace before deployment. On the other hand, Foundry Models sold directly by Azure, such as Azure OpenAI in Foundry Models, don't have this requirement. For more information about Foundry Models, including the regions where they're available for deployment, see [Foundry Models sold directly by Azure](../concepts/models-sold-directly-by-azure.md) and [Foundry Models from partners and community](../concepts/models-from-partners.md).

## Prerequisites

To complete this article, you need:

- An Azure subscription with a valid payment method. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin. If you're using GitHub Models, you can [upgrade to Foundry Models](../how-to/quickstart-github-models.md) and create an Azure subscription in the process.

- The **Cognitive Services Contributor** role or equivalent permissions on the Foundry resource to create and manage deployments. For more information, see [Azure RBAC roles](/azure/role-based-access-control/built-in-roles).

- A [Microsoft Foundry project](../../how-to/create-projects.md). This kind of project is managed under a Foundry resource.

- [Foundry Models from partners and community](../concepts/models-from-partners.md) require access to **Azure Marketplace** to create subscriptions. Ensure you have the [permissions required to subscribe to model offerings](../how-to/configure-marketplace.md). [Foundry Models sold directly by Azure](../concepts/models-sold-directly-by-azure.md) don't have this requirement.
