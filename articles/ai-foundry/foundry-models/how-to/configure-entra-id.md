---
title: Configure key-less authentication with Microsoft Entra ID
titleSuffix: Microsoft Foundry
description: Learn how to configure key-less authorization to use Microsoft Foundry Models with Microsoft Entra ID and enhance security.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 09/26/2025
ms.custom: ignite-2024, github-universe-2024, dev-focus
author: msakande
ms.author: mopeakande
recommendations: false
zone_pivot_groups: azure-ai-models-deployment
ms.reviewer: fasantia
reviewer: santiagxf
ai-usage: ai-assisted

#CustomerIntent: As a developer, I want to configure keyless authentication with Microsoft Entra ID for Microsoft Foundry Models so that I can secure my AI model deployments without relying on API keys and leverage role-based access control for better security and compliance.
---

# Configure key-less authentication with Microsoft Entra ID

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

[!INCLUDE [migrate-model-inference-to-v1-openai](../../includes/migrate-model-inference-to-v1-openai.md)]

::: zone pivot="ai-foundry-portal"
[!INCLUDE [portal](../../foundry-models/includes/configure-entra-id/portal.md)]
::: zone-end

::: zone pivot="programming-language-cli"
[!INCLUDE [cli](../../foundry-models/includes/configure-entra-id/cli.md)]
::: zone-end

::: zone pivot="programming-language-bicep"
[!INCLUDE [bicep](../../foundry-models/includes/configure-entra-id/bicep.md)]
::: zone-end

## Next step

* [Develop applications using Microsoft Foundry Models](../../model-inference/supported-languages.md)
