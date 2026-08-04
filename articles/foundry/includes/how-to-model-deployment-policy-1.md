---
title: Include file
description: Include file
author: s-polly
ms.reviewer: aashishb
ms.author: scottpolly
ms.service: microsoft-foundry
ms.topic: include
ms.date: 05/12/2026
ms.custom: include
---

Azure Policy provides built-in policy definitions that help you govern the deployment of AI models in Microsoft Foundry portal. You can use
these policies to control what models your developers can deploy in the Foundry portal.

> [!NOTE]
> To deploy and use [model router](/azure/ai-foundry/openai/concepts/model-router) while this policy is assigned, include `Microsoft` in the list of allowed publishers, because Microsoft is the publisher of model router. Also include the publisher name of each supported model that you deploy for routing, as listed on the model's card in the [model catalog](/azure/ai-foundry/how-to/model-catalog-overview). For example, to route to Claude models, which you deploy separately, also include `Anthropic`. If the list of allowed publishers doesn't include these names, the policy blocks the model router deployment.

## Prerequisites

- An Azure account with an active subscription. If you don't have one, create a [free Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn). Your
  Azure account lets you access the Foundry portal.

- Permissions to create and assign policies. To create and assign policies, you must be an [Owner](/azure/role-based-access-control/built-in-roles#owner) or [Resource Policy Contributor](/azure/role-based-access-control/built-in-roles#resource-policy-contributor) at the Azure subscription or resource group level.

- Familiarity with Azure Policy. To learn more, see [What is Azure Policy?](/azure/governance/policy/overview).
