---
title: "Quickstart: Use a text blocklist"
titleSuffix: Azure AI services
description: Get started using a text blocklist to detect harmful content in text.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.custom: devx-track-python, devx-track-dotnet
ms.topic: quickstart
ms.date: 02/22/2025
ms.author: pafarley
zone_pivot_groups: programming-languages-content-safety-abridged
---

# QuickStart: Use a text blocklist

Get started using Azure AI Content Safety to create a custom text blocklist and use it to detect harmful content in text.

> [!CAUTION]
> 
> The sample data and code may contain offensive content. User discretion is advised.

::: zone pivot="programming-language-foundry-portal"

[!INCLUDE [Foundry portal quickstart](./includes/quickstarts/foundry-quickstart-blocklist.md)]

::: zone-end

::: zone pivot="programming-language-rest"

[!INCLUDE [REST API quickstart](./includes/quickstarts/rest-quickstart-blocklist.md)]

::: zone-end

::: zone pivot="programming-language-csharp"

[!INCLUDE [.NET SDK quickstart](./includes/quickstarts/csharp-quickstart-blocklist.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python SDK quickstart](./includes/quickstarts/python-quickstart-blocklist.md)]

::: zone-end


## Clean up resources

If you want to clean up and remove an Azure AI services subscription, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

- [Azure portal](../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../multi-service-resource.md?pivots=azcli#clean-up-resources)


## Next step

Follow the Blocklist how-to guide for more in-depth guidance on how you can use the blocklist APIs.

> [!div class="nextstepaction"]
> [How to use a blocklist](./how-to/use-blocklist.md)