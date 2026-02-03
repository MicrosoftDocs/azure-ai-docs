---
title: "Quickstart: Use the Azure Language Detection client library"
titleSuffix: Foundry Tools
description: Detect the language of text with Azure Language Detection using SDKs, the REST API, or the Foundry portal.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: quickstart
ms.date: 11/18/2025
ms.author: lajanuar
ms.devlang: csharp
# ms.devlang: csharp, java, javascript, python
ms.custom: language-service-language-detection, mode-api, devx-track-extended-java, devx-track-js, devx-track-python
keywords: text mining, language detection
zone_pivot_groups: programming-languages-text-analytics
ai-usage: ai-assisted
---
# Quickstart: Use the Azure Language Detection client library and REST API

::: zone pivot="programming-language-csharp"

[!INCLUDE [C# quickstart](includes/quickstarts/csharp-sdk.md)]

::: zone-end

::: zone pivot="programming-language-java"

[!INCLUDE [Java quickstart](includes/quickstarts/java-sdk.md)]

::: zone-end

::: zone pivot="programming-language-javascript"

[!INCLUDE [Node.js quickstart](includes/quickstarts/nodejs-sdk.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python quickstart](includes/quickstarts/python-sdk.md)]

::: zone-end

::: zone pivot="rest-api"

[!INCLUDE [REST API quickstart](includes/quickstarts/rest-api.md)]

::: zone-end

::: zone pivot="ai-foundry-portal"

[!INCLUDE [Microsoft Foundry quickstart](includes/quickstarts/azure-ai-foundry.md)]

::: zone-end

## Troubleshooting

| Issue | Resolution |
|---|---|
| You get a `401` or `403` error when calling the API. | Confirm your key and endpoint are correct for the same Azure AI resource. If you recently changed role assignments, wait a few minutes and try again. |
| You get an error about missing environment variables. | Confirm `LANGUAGE_KEY` and `LANGUAGE_ENDPOINT` are set in your environment before you run the sample. |
| The Foundry experience doesn't match the steps. | In the Foundry portal, use the version toggle to switch between Foundry (classic) and Foundry (new), then follow the matching tab in the Foundry section. |

## Clean up resources

To clean up and remove an Azure AI resource, you can delete either the individual resource or the entire resource group. If you delete the resource group, all resources contained within are also deleted.

* [Azure portal](../../multi-service-resource.md?pivots=azportal#clean-up-resources)
* [Azure CLI](../../multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

* [Language detection overview](overview.md)
* [Call the Language Detection API](how-to/call-api.md)
* [Language support](language-support.md)
* [Use containers](how-to/use-containers.md)
