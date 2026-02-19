---
title: "Quickstart: Detect personally identifiable information (PII) in text"
titleSuffix: Foundry Tools
description: Use Azure Language in Foundry Tools to detect and redact personally identifiable information (PII) in text with client libraries, the REST API, or the Microsoft Foundry portal.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: quickstart
ms.date: 02/06/2026
ms.author: lajanuar
ms.devlang: csharp
# ms.devlang: csharp, java, javascript, python
ms.custom:
- language-service-pii
- mode-other
- devx-track-extended-java
- devx-track-js
- devx-track-python
- pilot-ai-workflow-jan-2026
keywords: pii, personally identifiable information, redaction, text analytics
zone_pivot_groups: programming-languages-text-analytics
ai-usage: ai-assisted
---

# Quickstart: Detect personally identifiable information (PII)
<!-- markdownlint-disable MD025 -->

In this quickstart, you use the Azure Language in Foundry Tools PII detection feature to identify and redact personally identifiable information in text. You can get started using your preferred client library, the REST API, or the Microsoft Foundry portal.

If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.

> [!NOTE]
> This quickstart covers PII detection in documents. To detect PII in conversations, see [How to detect and redact PII in conversations](how-to/redact-conversation-pii.md). To detect PII in text, see [How to detect and redact PII in text](how-to/redact-text-pii.md).

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
| --- | --- |
| You get a `401` or `403` error when calling the API. | Confirm your key and endpoint are correct for the same Azure AI resource. If you recently changed role assignments, wait a few minutes and try again. |
| You get an error about missing environment variables. | Confirm `LANGUAGE_KEY` and `LANGUAGE_ENDPOINT` are set in your environment before you run the sample. |
| The Foundry experience doesn't match the steps. | In the Foundry portal, use the version toggle to switch between Foundry (classic) and Foundry (new), then follow the matching tab in the Foundry section. |
| No entities are detected in your text. | Verify that the input text contains recognizable PII patterns (names, addresses, phone numbers). Check that the **Types** filter includes the entity categories you expect. |
| The API returns an `InvalidLanguage` error. | Confirm the language code in the request matches one of the [supported languages](language-support.md). |

## Clean up resources

If you no longer need the resources you created in this quickstart, delete the individual resource or the entire resource group. Deleting the resource group also deletes all other resources associated with it.

* [Azure portal](../../multi-service-resource.md?pivots=azportal#clean-up-resources)
* [Azure CLI](../../multi-service-resource.md?pivots=azcli#clean-up-resources)

## Related content

* [PII overview](overview.md)
* [How to detect and redact PII in text](how-to/redact-text-pii.md)
* [How to detect and redact PII in conversations](how-to/redact-conversation-pii.md)
* [Supported entity categories for text](concepts/entity-categories.md)
