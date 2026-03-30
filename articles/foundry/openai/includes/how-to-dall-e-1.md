---
title: Include file
description: Include file
author: PatrickFarley
ms.reviewer: sgilley
ms.author: pafarley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

[!INCLUDE [DALL-E retirement notice](dall-e-retirement.md)]

OpenAI's image generation models create images from user-provided text prompts and optional images. This article explains how to use these models, configure options, and benefit from advanced image generation capabilities in Azure.

You can do image generation via [image generation API](/azure/ai-foundry/openai/dall-e-quickstart) or [responses API](/azure/ai-foundry/openai/how-to/responses?tabs=python-key). Or you can experiment with image generation in the [Foundry portal](https://ai.azure.com)

Use the tabs at the start of this page to select your preferred API approach and model.

## Models and capabilities

Use this table to learn the differences between the different image generation models, and to help you choose the best model for your image generation needs.

| Aspect | GPT-Image-1.5 | GPT-Image-1 | GPT-Image-1-Mini |
|--------|---------------|--------------|------------------|
|**Availability** | Limited access preview ([Apply for GPT-image-1.5 access](https://aka.ms/oai/gptimage1.5access)) | Limited access preview ([Apply for GPT-image-1 access](https://aka.ms/oai/gptimage1access)) | Limited access preview ([Apply for GPT-image-1 access](https://aka.ms/oai/gptimage1access)) |
| **Strengths** | Best for realism, instruction following, multimodal context, and improved speed/cost | Best for realism, instruction following, and multimodal context | Best for fast prototyping, bulk generation, or cost-sensitive use cases |
| **Input / Output Modalities & Format** | Accepts **text + image** inputs; outputs images only in **base64** (no URL option). | Accepts **text + image** inputs; outputs images only in **base64** (no URL option). | Accepts **text + image** inputs; outputs images only in **base64** (no URL option). |
| **Image Sizes / Resolutions** | 1024×1024, 1024×1536, 1536×1024 | 1024×1024, 1024×1536, 1536×1024 | 1024×1024, 1024×1536, 1536×1024 |
| **Quality Options** | `low`, `medium`, `high` (default = high) | `low`, `medium`, `high` (default = high) | `low`, `medium`, `high` (default = medium) |
| **Number of Images per Request** | 1–10 images per request (`n` parameter) | 1–10 images per request (`n` parameter) | 1–10 images per request (`n` parameter) |
| **Editing (inpainting / variations)** | ✅ Supports inpainting and variations with mask + prompt | ✅ Supports inpainting and variations with mask + prompt | ✅ Supports inpainting and variations with mask + prompt |
| **Face Preservation** | ✅ Advanced **face preservation** for realistic, consistent results | ✅ Advanced **face preservation** for realistic, consistent results | ❌ No dedicated face preservation; better for **non-portrait/general creative** imagery |
| **Performance & Cost** | High-fidelity, **realism-optimized** model; improved efficiency and latency over GPT-Image-1 | High-fidelity, **realism-optimized** model; higher latency and cost | **Cost-efficient** and **faster** for large-scale or iterative generation |

## Quickstart

::: zone pivot="rest-api"

[!INCLUDE [REST API quickstart](dall-e-rest.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python SDK quickstart](dall-e-python.md)]

::: zone-end

::: zone pivot="programming-language-csharp"

[!INCLUDE [C# SDK quickstart](dall-e-dotnet.md)]

::: zone-end

::: zone pivot="programming-language-java"

[!INCLUDE [Java SDK quickstart](dall-e-java.md)]

::: zone-end

::: zone pivot="programming-language-javascript"

[!INCLUDE [JavaScript SDK quickstart](dall-e-javascript.md)]

::: zone-end

::: zone pivot="programming-language-typescript"

[!INCLUDE [TypeScript SDK quickstart](dall-e-typescript.md)]

::: zone-end

::: zone pivot="programming-language-go"

[!INCLUDE [Go SDK quickstart](dall-e-go.md)]

::: zone-end

::: zone pivot="programming-language-powershell"

[!INCLUDE [PowerShell quickstart](dall-e-powershell.md)]

::: zone-end

::: zone pivot="programming-language-studio"

[!INCLUDE [Portal quickstart](dall-e-studio.md)]

::: zone-end

## Quotas and limits

Image generation has default rate limits per deployment:

| Model | Default quota (images/min) |
|-------|---------------------------|
| GPT-image-1 series | 5 |

To view your current quota or request an increase, see [Manage Azure OpenAI quotas](/azure/ai-foundry/openai/how-to/quota).
