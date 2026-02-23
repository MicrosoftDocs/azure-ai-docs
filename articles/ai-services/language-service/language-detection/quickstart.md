---
title: "Quickstart: Detect the language of text"
titleSuffix: Foundry Tools
description: Use Azure Language in Foundry Tools to detect the language of text with client libraries, the REST API, or the Microsoft Foundry portal.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: quickstart
ms.date: 02/06/2026
ms.author: lajanuar
ms.devlang: csharp
# ms.devlang: csharp, java, javascript, python
ms.custom: language-service-language-detection, mode-api, devx-track-extended-java, devx-track-js, devx-track-python
keywords: text mining, language detection
zone_pivot_groups: programming-languages-text-analytics
ai-usage: ai-assisted
---
# Quickstart: Detect the language of text

In this quickstart, you use the Azure Language in Foundry Tools language detection feature to identify the language of input text. You can get started using your preferred client library, the REST API, or the Microsoft Foundry portal.

If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.

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
| The API returns `unknown` as the detected language. | The input text might be too short or ambiguous. Provide a longer text sample or set the **Country/region hint** to improve accuracy. |
| The API returns an `InvalidCountryHint` error. | Confirm the country/region hint code is a valid ISO 3166-1 alpha-2 code (for example, `US`, `FR`, `JP`). |

## Clean up resources

If you no longer need the resources you created in this quickstart, delete the individual resource or the entire resource group. Deleting the resource group also deletes all other resources associated with it.

* [Azure portal](../../multi-service-resource.md?pivots=azportal#clean-up-resources)
* [Azure CLI](../../multi-service-resource.md?pivots=azcli#clean-up-resources)

## Related content

* [Language detection overview](overview.md)
* [Call the Language Detection API](how-to/call-api.md)
* [Language support](language-support.md)
* [Use containers](how-to/use-containers.md)
