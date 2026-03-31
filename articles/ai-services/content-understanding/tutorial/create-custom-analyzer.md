---
title: Create a custom analyzer with Azure Content Understanding in Foundry Tools
titleSuffix: Foundry Tools
description: Learn to create a custom analyzer with Azure Content Understanding in Foundry Tools
author: PatrickFarley 
ms.author: paulhsu
manager: nitinme
ms.date: 03/16/2026
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.custom:
  - build-2025
zone_pivot_groups: programming-languages-content-understanding
ai-usage: ai-assisted
---

# Create a custom analyzer

Content Understanding analyzers define how to process and extract insights from your content. They ensure uniform processing and output structure across all your content, so you get reliable and predictable results. For common use cases, you can use the [prebuilt analyzers](../concepts/prebuilt-analyzers.md). This guide shows how you can customize these analyzers to better fit your needs.

::: zone pivot="programming-language-rest"

[!INCLUDE [REST API custom analyzer](./includes/rest-custom-analyzer.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python SDK custom analyzer](./includes/python-custom-analyzer.md)]

::: zone-end

::: zone pivot="programming-language-csharp"

[!INCLUDE [.NET SDK custom analyzer](./includes/csharp-custom-analyzer.md)]

::: zone-end

::: zone pivot="programming-language-java"

[!INCLUDE [Java SDK custom analyzer](./includes/java-custom-analyzer.md)]

::: zone-end

::: zone pivot="programming-language-javascript"

[!INCLUDE [JavaScript SDK custom analyzer](./includes/javascript-custom-analyzer.md)]

::: zone-end

::: zone pivot="programming-language-typescript"

[!INCLUDE [TypeScript SDK custom analyzer](./includes/typescript-custom-analyzer.md)]

::: zone-end

## Related content

* Review code samples: [**visual document search**](https://github.com/Azure-Samples/azure-ai-search-with-content-understanding-python/blob/main/notebooks/search_with_visual_document.ipynb).
* Review code sample: [**analyzer templates**](https://github.com/Azure-Samples/azure-ai-content-understanding-python/tree/main/analyzer_templates).
* Explore more [Python SDK samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples)
* Explore more [.NET SDK samples](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/contentunderstanding/Azure.AI.ContentUnderstanding/samples)
* Explore more [Java SDK samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding)
* Explore more [JavaScript SDK samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/javascript)
* Explore more [TypeScript SDK samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/typescript)
* Try processing your document content using Content Understanding in [Foundry](https://aka.ms/cu-landing).