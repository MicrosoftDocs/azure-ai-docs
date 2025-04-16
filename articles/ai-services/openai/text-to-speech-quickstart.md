---
title: 'Text to speech with Azure OpenAI Service'
titleSuffix: Azure OpenAI
description: Use the Azure OpenAI Service for text to speech with OpenAI voices.
manager: nitinme
ms.service: azure-ai-openai
ms.topic: quickstart
ms.date: 3/10/2025
ms.reviewer: eur
ms.author: eur
author: eric-urban
recommendations: false
zone_pivot_groups: programming-languages-rest-js-cs
---

# Quickstart: Text to speech with the Azure OpenAI Service

In this quickstart, you use the Azure OpenAI Service for text to speech with OpenAI voices.  

The available voices are: `alloy`, `echo`, `fable`, `onyx`, `nova`, and `shimmer`. For more information, see [Azure OpenAI Service reference documentation for text to speech](./reference.md#text-to-speech-preview).

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

- [Azure portal](../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

* Learn more about how to work with text to speech with Azure OpenAI Service in the [Azure OpenAI Service reference documentation](./reference.md#text-to-speech-preview).
* For more examples, check out the [Azure OpenAI Samples GitHub repository](https://github.com/Azure-Samples/openai)
