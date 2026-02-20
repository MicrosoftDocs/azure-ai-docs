---
title: 'Text to speech with Azure OpenAI in Microsoft Foundry Models'
titleSuffix: Azure OpenAI
description: Convert text to speech using Azure OpenAI voices.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: quickstart
ms.date: 01/30/2026
ms.author: pafarley
author: PatrickFarley
recommendations: false
zone_pivot_groups: programming-languages-rest-js-cs

---

# Quickstart: Convert text to speech with Azure OpenAI in Microsoft Foundry Models

This quickstart shows you how to convert text to speech using Azure OpenAI voices.  

The available voices are: `alloy`, `echo`, `fable`, `onyx`, `nova`, and `shimmer`. For more information, see [Azure OpenAI reference documentation for text to speech](./reference.md#text-to-speech-preview).

::: zone pivot="rest-api"

[!INCLUDE [REST API quickstart](includes/text-to-speech-rest.md)]

::: zone-end

::: zone pivot="programming-language-javascript"

[!INCLUDE [JavaScript quickstart](includes/text-to-speech-javascript.md)]

::: zone-end

::: zone pivot="programming-language-typescript"

[!INCLUDE [TypeScript quickstart](includes/text-to-speech-typescript.md)]

::: zone-end

::: zone pivot="programming-language-dotnet"

[!INCLUDE [.NET quickstart](includes/text-to-speech-dotnet.md)]

::: zone-end

## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource. Before deleting the resource, you must first delete any deployed models.

- [Azure portal](../../ai-services/multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../ai-services/multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

* Learn more about how to work with text to speech with Azure OpenAI in the [Azure OpenAI reference documentation](./reference.md#text-to-speech-preview).
* For more examples, check out the [Azure OpenAI Samples GitHub repository](https://github.com/Azure-Samples/openai)
