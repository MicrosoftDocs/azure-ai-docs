---
title: 'Quickstart: Generate images with Azure OpenAI in Microsoft Foundry Models'
titleSuffix: Azure OpenAI
description: Learn how to get started generating images with Azure OpenAI by using the Python SDK, the REST APIs, or Microsoft Foundry portal.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.custom: devx-track-python, devx-track-dotnet, devx-track-extended-java, devx-track-go, devx-track-js, devx-track-ts, dev-focus
ms.topic: quickstart
author: PatrickFarley
ms.author: pafarley
ms.date: 01/29/2026
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
zone_pivot_groups: openai-quickstart-dall-e
---

# Quickstart: Generate images with Azure OpenAI in Microsoft Foundry Models

[!INCLUDE [version-banner](../includes/version-banner.md)]

Azure OpenAI provides multiple image generation models. This quickstart covers both model families:

| Model | Availability | Key capabilities |
|-------|--------------|------------------|
| **DALL-E 3** | Generally available | High-quality image generation with `quality` and `style` parameters. Best for production workloads. |
| **GPT-image-1 series** | Limited access preview | Image generation plus editing and variations. Best for advanced image manipulation workflows. Requires [limited access registration](https://aka.ms/oai/access). |

> [!TIP]
> Image generation typically takes 10-30 seconds depending on the model, size, and quality settings.

Use the tabs to select your preferred API approach and model.

::: zone pivot="rest-api"

[!INCLUDE [REST API quickstart](includes/dall-e-rest.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python SDK quickstart](includes/dall-e-python.md)]

::: zone-end

::: zone pivot="programming-language-csharp"

[!INCLUDE [C# SDK quickstart](includes/dall-e-dotnet.md)]

::: zone-end

::: zone pivot="programming-language-java"

[!INCLUDE [Java SDK quickstart](includes/dall-e-java.md)]

::: zone-end

::: zone pivot="programming-language-javascript"

[!INCLUDE [JavaScript SDK quickstart](includes/dall-e-javascript.md)]

::: zone-end

::: zone pivot="programming-language-typescript"

[!INCLUDE [TypeScript SDK quickstart](includes/dall-e-typescript.md)]

::: zone-end

::: zone pivot="programming-language-go"

[!INCLUDE [Go SDK quickstart](includes/dall-e-go.md)]

::: zone-end


::: zone pivot="programming-language-powershell"

[!INCLUDE [PowerShell quickstart](includes/dall-e-powershell.md)]

::: zone-end

::: zone pivot="programming-language-studio"

[!INCLUDE [Portal quickstart](includes/dall-e-studio.md)]

::: zone-end


