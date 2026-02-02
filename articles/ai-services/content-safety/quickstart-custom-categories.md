---
title: "Quickstart: Custom categories (preview)"
titleSuffix: Azure AI services
description: Use the custom categories API to create your own content categories and train the Content Safety model for your use case.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.topic: quickstart
ms.date: 09/02/2025
ms.author: pafarley
zone_pivot_groups: programming-languages-content-safety-foundry-rest
#customer intent: As a developer, I want to create custom content categories so that I can train the Content Safety model for specific use cases.
---


# Quickstart: Custom categories (standard mode) (preview)

Follow this guide to use Azure AI Content Safety Custom categories (standard) REST API to create your own content categories for your use case and train Azure AI Content Safety to detect them in new text content. 

For more information on Custom categories, see the [Custom categories concept page](./concepts/custom-categories.md). For API input limits, see the [Input requirements](./overview.md#input-requirements) section of the Overview. 

> [!IMPORTANT]
> This feature is only available in certain Azure regions. See [Region availability](./overview.md#region-availability).

> [!IMPORTANT]
> **Allow enough time for model training**
>
> The end-to-end execution of custom category training can take from around five hours to ten hours. Plan your moderation pipeline accordingly.



::: zone pivot="programming-language-foundry-portal"

[!INCLUDE [Foundry portal quickstart](./includes/quickstarts/foundry-quickstart-custom-categories.md)]

::: zone-end

::: zone pivot="programming-language-rest"

[!INCLUDE [REST API quickstart](./includes/quickstarts/rest-quickstart-custom-categories.md)]

::: zone-end


## Related content

* [Custom categories concepts](./concepts/custom-categories.md)
* [Moderate content with Content Safety](./quickstart-text.md)
