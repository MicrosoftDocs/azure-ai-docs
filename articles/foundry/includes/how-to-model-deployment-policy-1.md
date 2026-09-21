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
> To deploy and use [model router](/azure/ai-foundry/openai/concepts/model-router) while the approved-models policy is assigned, model router and every model included in the deployment must satisfy the policy through either an allowed publisher or an allowed asset ID. If you use publisher-based approval, include `Microsoft` for model router and each publisher represented in the selected routing set, such as `Anthropic` for Claude models. Publisher names are listed on each model's card in the [model catalog](/azure/ai-foundry/how-to/model-catalog-overview). With ARM or CLI, any noncompliant model in the requested set causes the entire deployment to fail. In the Foundry portal, noncompliant models can be excluded and a compliant subset deployed.

## Prerequisites

- An Azure account with an active subscription. If you don't have one, create a [free Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn). Your
  Azure account lets you access the Foundry portal.

- Permissions to create and assign policies. To create and assign policies, you must be an [Owner](/azure/role-based-access-control/built-in-roles#owner) or [Resource Policy Contributor](/azure/role-based-access-control/built-in-roles#resource-policy-contributor) at the Azure subscription or resource group level.

- Familiarity with Azure Policy. To learn more, see [What is Azure Policy?](/azure/governance/policy/overview).
