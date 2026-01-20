---
title: Add and configure models to Microsoft Foundry using code
titleSuffix: Microsoft Foundry
description: Learn how to add and configure Microsoft Foundry Models in your Foundry resource for use in inferencing applications.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 01/20/2026
ms.custom: ignite-2024, github-universe-2024
author: msakande   
ms.author: mopeakande
recommendations: false
zone_pivot_groups: azure-ai-create-deployment
monikerRange: 'foundry-classic || foundry'
ai.usage: ai-assisted

#CustomerIntent: As a developer or AI practitioner, I want to deploy Microsoft Foundry Models using code, so that I can integrate these AI models into my applications and perform inference tasks for my business needs.
---

# Deploy Microsoft Foundry Models using code

[!INCLUDE [version-banner](../../includes/version-banner.md)]

[!INCLUDE [migrate-model-inference-to-v1-openai](../../includes/migrate-model-inference-to-v1-openai.md)]

::: zone pivot="programming-language-cli"
[!INCLUDE [cli](../../foundry-models/includes/create-model-deployments/cli.md)]
::: zone-end

::: zone pivot="programming-language-bicep"
[!INCLUDE [bicep](../../foundry-models/includes/create-model-deployments/bicep.md)]
::: zone-end

## Next step

- [How to generate text responses with Microsoft Foundry Models](generate-responses.md)