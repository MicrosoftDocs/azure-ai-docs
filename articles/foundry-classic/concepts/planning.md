---
title: "Microsoft Foundry Rollout Across My Organization (classic)"
description: "Learn how to plan the rollout of Microsoft Foundry across your organization, including environment setup, data isolation, and governance. (classic)"
ms.service: azure-ai-foundry
author: sdgilley
ms.topic: concept-article
ms.date: 04/06/2026
ms.author: sgilley
ms.reviewer: deeikele
ms.custom:
  - classic-and-new
  - dev-focus
ai-usage: ai-assisted
ROBOTS: NOINDEX, NOFOLLOW
---

# Microsoft Foundry rollout across my organization (classic)

**Currently viewing:** :::image type="icon" source="../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../foundry/concepts/planning.md)

[!INCLUDE [planning 1](../../foundry/includes/concepts-planning-1.md)]

## Access extended functionality with Azure AI Hub

While a Foundry resource alone gives you access to most Foundry functionality, select capabilities are currently only available in combination with an Azure AI hub resource powered by Azure Machine Learning. These capabilities are lower in the AI development stack and focus on model customization.

Hub resources require their own project types that you can also access by using the Azure Machine Learning Studio, SDK, or CLI. To help plan your deployment, see [this table](../what-is-foundry.md#which-type-of-project-do-i-need) and [choose a resource type](../concepts/resource-types.md) for an overview of supported capabilities.

You deploy a hub resource side-by-side with your Foundry resource. The hub resource takes a dependency on your Foundry resource to provide access to select tools and models.

## Learn more

- Identity and managed identity: [Configure managed identity](../openai/how-to/managed-identity.md)

[!INCLUDE [planning 2](../../foundry/includes/concepts-planning-2.md)]
