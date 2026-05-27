---
title: Copy custom analyzers
titleSuffix: Foundry Tools
description: Copy custom analyzers within a resource and across Azure resources.
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 01/29/2026
ai-usage: ai-assisted
ms.service: azure-ai-content-understanding
ms.topic: how-to
ms.custom:
  - ignite-2024-understanding-release
  - references_regions
  - build-2025
zone_pivot_groups: programming-languages-content-understanding
---

# Copy custom analyzers

Every Content Understanding resource provides access to all prebuilt analyzers by default. For a complete list, see [prebuilt analyzers](../concepts/prebuilt-analyzers.md). Custom analyzers are analyzers you define to process specific content where you can define the content type, schema, and any other processing logic. For more information on defining a custom analyzer, see [defining a custom analyzer](./customize-analyzer-content-understanding-studio.md).

The copy operation on analyzers supports a few different scenarios:
* **Copy within a resource** to create a copy of an existing analyzer in the same resource as a backup or a version you can iterate on.
* **Copy across resources** to copy an analyzer from one Foundry resource to another. This supports failover scenarios and sharing analyzers across teams.

> [!IMPORTANT]
>
> The copy operation for copying across resources supports copying analyzers across subscriptions and even Azure tenants.

::: zone pivot="programming-language-rest"

[!INCLUDE [REST API copy analyzers](./includes/rest-copy-analyzers.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python SDK copy analyzers](./includes/python-copy-analyzers.md)]

::: zone-end

::: zone pivot="programming-language-csharp"

[!INCLUDE [.NET SDK copy analyzers](./includes/csharp-copy-analyzers.md)]

::: zone-end

::: zone pivot="programming-language-java"

[!INCLUDE [Java SDK copy analyzers](./includes/java-copy-analyzers.md)]

::: zone-end

::: zone pivot="programming-language-javascript"

[!INCLUDE [JavaScript SDK copy analyzers](./includes/javascript-copy-analyzers.md)]

::: zone-end

::: zone pivot="programming-language-typescript"

[!INCLUDE [TypeScript SDK copy analyzers](./includes/typescript-copy-analyzers.md)]

::: zone-end

## Related content

* Explore more [Python SDK samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples)
* Explore more [.NET SDK samples](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/contentunderstanding/Azure.AI.ContentUnderstanding/samples)
* Explore more [Java SDK samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding)
* Explore more [JavaScript SDK samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/javascript)
* Explore more [TypeScript SDK samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/typescript)
