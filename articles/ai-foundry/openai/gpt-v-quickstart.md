---
title: 'Quickstart: Use vision-enabled chats with the Azure OpenAI in Microsoft Foundry Models'
titleSuffix: Azure OpenAI
description: Use this article to get started using Azure OpenAI to deploy and use the GPT-4 Turbo with Vision model or other vision-enabled models. 
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.custom: devx-track-python, devx-track-js, devx-track-ts, dev-focus
ms.topic: quickstart
author: PatrickFarley
ms.author: pafarley
ms.date: 01/29/2026
zone_pivot_groups: openai-quickstart-gpt-v
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted

---

# Quickstart: Use images in your AI chats

Get started using images in your chats with Azure OpenAI in Microsoft Foundry Models.

[!INCLUDE [version-banner](../includes/version-banner.md)]

> [!IMPORTANT]
> - Extra usage fees might apply when using chat completion models with vision functionality.
> - When uploading images, there's a limit of **10 images per chat request**.
> - Always set `max_tokens` in your API requests, or responses might be truncated.


::: zone pivot="ai-foundry-portal"

[!INCLUDE [Foundry portal quickstart](includes/gpt-v-studio.md)]

::: zone-end

::: zone pivot="rest-api"

[!INCLUDE [REST API quickstart](includes/gpt-v-rest.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python quickstart](includes/gpt-v-python.md)]

::: zone-end

::: zone pivot="programming-language-javascript"

[!INCLUDE [JavaScript quickstart](includes/gpt-v-javascript.md)]

::: zone-end

::: zone pivot="programming-language-typescript"

[!INCLUDE [TypeScript quickstart](includes/gpt-v-typescript.md)]

::: zone-end

::: zone pivot="programming-language-dotnet"

[!INCLUDE [.NET quickstart](includes/gpt-v-dotnet.md)]

::: zone-end

## Related content

* [Get started with multimodal vision chat apps using Azure OpenAI AI App template](/azure/developer/ai/get-started-app-chat-vision?tabs=github-codespaces)
* Learn more about these APIs in the [Vision-enabled models how-to guide](./how-to/gpt-with-vision.md)
* [GPT-4 Turbo with Vision frequently asked questions](./faq.yml#gpt-4-turbo-with-vision)
* [GPT-4 Turbo with Vision API reference](https://aka.ms/gpt-v-api-ref)
