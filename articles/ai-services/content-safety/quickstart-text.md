---
title: "Quickstart: Analyze text content"
titleSuffix: Azure AI services
description: Get started using Azure AI Content Safety to analyze text content for objectionable material.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.custom: build-2023, devx-track-python, devx-track-dotnet, devx-track-extended-java, devx-track-js, dev-focus
ms.topic: quickstart
ms.date: 11/21/2025
ms.author: pafarley
ai-usage: ai-assisted
zone_pivot_groups: programming-languages-content-safety-2
---

# QuickStart: Analyze text content

In this quickstart, you analyze text content for harmful material using Azure AI Content Safety. The Azure AI Content Safety service provides you with AI algorithms for flagging objectionable content.

For more information on text moderation, see the [Harm categories concept page](./concepts/harm-categories.md). For API input limits, see the [Input requirements](./overview.md#input-requirements) section of the Overview.

Choose your preferred language below for detailed steps:

> [!CAUTION]
> 
> The sample data and code may contain offensive content. User discretion is advised.

::: zone pivot="programming-language-foundry-portal"

[!INCLUDE [Foundry portal quickstart](./includes/quickstarts/foundry-quickstart-text.md)]

::: zone-end

::: zone pivot="programming-language-rest"

[!INCLUDE [REST API quickstart](./includes/quickstarts/rest-quickstart-text.md)]

::: zone-end

::: zone pivot="programming-language-csharp"

[!INCLUDE [.NET SDK quickstart](./includes/quickstarts/csharp-quickstart-text.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python SDK quickstart](./includes/quickstarts/python-quickstart-text.md)]

::: zone-end

::: zone pivot="programming-language-java"

[!INCLUDE [Python SDK quickstart](./includes/quickstarts/java-quickstart-text.md)]

::: zone-end

::: zone pivot="programming-language-javascript"

[!INCLUDE [Python SDK quickstart](./includes/quickstarts/javascript-quickstart-text.md)]

::: zone-end
::: zone pivot="programming-language-typescript"

[!INCLUDE [TypeScript SDK quickstart](./includes/quickstarts/typescript-quickstart-text.md)]

::: zone-end


## Clean up resources

If you want to clean up and remove an Azure AI services subscription, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

- [Azure portal](../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../multi-service-resource.md?pivots=azcli#clean-up-resources)


## Related content

* [Harm categories](./concepts/harm-categories.md)
* Configure filters for each category and test on datasets using [Content Safety Studio](studio-quickstart.md), export the code and deploy.
