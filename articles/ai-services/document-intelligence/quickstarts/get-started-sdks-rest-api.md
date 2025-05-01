---
title: "Quickstart: Document Intelligence client libraries | REST API "
titleSuffix: Azure AI services
description: Use a Document Intelligence SDK or the REST API to create a forms processing app that extracts key data and structure elements from your documents.
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.custom:
  - devx-track-dotnet
  - devx-track-extended-java
  - devx-track-js
  - devx-track-python
ms.topic: quickstart
ms.date: 04/11/2025
ms.author: lajanuar
zone_pivot_groups: programming-languages-set-formre
---


# Get started with Document Intelligence

> [!IMPORTANT]
>
> * Azure Cognitive Services Form Recognizer is now Azure AI Document Intelligence.
> * Some platforms are still awaiting the renaming update.
> * All mention of Form Recognizer or Document Intelligence in our documentation refers to the same Azure service.

:::moniker range="doc-intel-4.0.0"

**This content applies to:** ![checkmark](../media/yes-icon.png) **v4.0 (GA)** **Earlier versions:** ![blue-checkmark](../media/blue-yes-icon.png) [v3.1 (GA)](?view=doc-intel-3.1.0&preserve-view=true) ![blue-checkmark](../media/blue-yes-icon.png) [v3.0 (GA)](?view=doc-intel-3.0.0&preserve-view=true)

* Get started with Azure AI Document Intelligence latest stable version v4.0 `2024-11-30` (GA).

:::moniker-end

::: moniker range="doc-intel-3.1.0"

**This content applies to:** ![checkmark](../media/yes-icon.png) **v3.1 (GA)** **Earlier versions:** ![blue-checkmark](../media/blue-yes-icon.png) [v3.0](?view=doc-intel-3.0.0&preserve-view=true) ![blue-checkmark](../media/blue-yes-icon.png) [v2.1](?view=doc-intel-2.1.0&preserve-view=true)

* Get started with Azure Form Recognizer latest GA version (`2023-07-31`).

::: moniker-end

::: moniker range="doc-intel-3.0.0"

**This content applies to:** ![checkmark](../media/yes-icon.png) **v3.0 (GA)** **Newer version:** ![blue-checkmark](../media/blue-yes-icon.png) [v3.1](?view=doc-intel-3.1.0&preserve-view=true)   ![blue-checkmark](../media/blue-yes-icon.png) [v2.1](?view=doc-intel-2.1.0&preserve-view=true)

* Get started with Azure Form Recognizer legacy GA version (`2022-08-31`).

::: moniker-end

* Azure AI Document Intelligence / Form Recognizer is a cloud-based Azure AI service that uses machine learning to extract key-value pairs, text, tables, and key data from your documents.

* You can easily integrate document processing models into your workflows and applications by using a programming language SDK or calling the REST API.

* We recommend that you use the free service while you're learning the technology for this quickstart. Remember that the number of free pages is limited to 500 per month.

To learn more about the API features and development options, visit our [Overview](../overview.md) page.

::: zone pivot="programming-language-csharp"

::: moniker range="doc-intel-4.0.0 || doc-intel-3.1.0 || doc-intel-3.0.0"
[!INCLUDE [C# SDK](includes/csharp-sdk.md)]
::: moniker-end

::: zone-end

::: zone pivot="programming-language-java"

::: moniker range="doc-intel-4.0.0 || doc-intel-3.1.0 || doc-intel-3.0.0"
[!INCLUDE [Java SDK](includes/java-sdk.md)]
::: moniker-end

::: zone-end

::: zone pivot="programming-language-javascript"

::: moniker range="doc-intel-4.0.0 || doc-intel-3.1.0 || doc-intel-3.0.0"
[!INCLUDE [Node.js SDK](includes/javascript-sdk.md)]
::: moniker-end

::: zone-end

::: zone pivot="programming-language-python"

::: moniker range="doc-intel-4.0.0 || doc-intel-3.1.0 || doc-intel-3.0.0"
[!INCLUDE [Python SDK](includes/python-sdk.md)]
::: moniker-end

::: zone-end

::: zone pivot="programming-language-rest-api"

::: moniker range="doc-intel-4.0.0 || doc-intel-3.1.0 || doc-intel-3.0.0"
[!INCLUDE [REST API](includes/rest-api.md)]
::: moniker-end

::: zone-end

::: moniker range="doc-intel-4.0.0 || doc-intel-3.1.0 || doc-intel-3.0.0"

That's it, congratulations!

In this quickstart, you used a document Intelligence model to analyze various forms and documents. Next, explore the Document Intelligence Studio and reference documentation to learn about Document Intelligence API in depth.

## Next steps

* For an enhanced experience and advanced model quality, try [**Document Intelligence Studio**](https://formrecognizer.appliedai.azure.com/studio)

* For v3.1 to v4.0 migration, see [**Changelog Migration guides**](../changelog-release-history.md#march-2024-preview-release).

::: moniker-end

::: moniker range="doc-intel-4.0.0" 
* [**Find more samples on GitHub**](https://github.com/Azure-Samples/document-intelligence-code-samples/tree/main).
::: moniker-end

::: moniker range="doc-intel-3.1.0" 
* [**Find more samples on GitHub**](https://github.com/Azure-Samples/document-intelligence-code-samples/tree/v3.1(2023-07-31-GA)).
::: moniker-end

::: moniker range="doc-intel-2.1.0"
[!INCLUDE [applies to v2.1](../includes/applies-to-v21.md)]
::: moniker-end

::: moniker range="doc-intel-2.1.0"

Get started with Azure AI Document Intelligence using the programming language of your choice or the REST API. Document Intelligence is a cloud-based Azure AI service that uses machine learning to extract key-value pairs, text, and tables from your documents. We recommend that you use the free service when you're learning the technology. Remember that the number of free pages is limited to 500 per month.

To learn more about Document Intelligence features and development options, visit our [Overview](../overview.md) page.

::: moniker-end

::: zone pivot="programming-language-csharp"

::: moniker range="doc-intel-2.1.0"
[!INCLUDE [C# SDK](includes/v2-1/csharp.md)]
::: moniker-end

::: zone-end

::: zone pivot="programming-language-java"

::: moniker range="doc-intel-2.1.0"
[!INCLUDE [Java SDK](includes/v2-1/java.md)]
::: moniker-end

::: zone-end

::: zone pivot="programming-language-javascript"

::: moniker range="doc-intel-2.1.0"
[!INCLUDE [Node.js SDK](includes/v2-1/javascript.md)]
::: moniker-end

::: zone-end

::: zone pivot="programming-language-python"

::: moniker range="doc-intel-2.1.0"
[!INCLUDE [Python SDK](includes/v2-1/python.md)]
::: moniker-end

::: zone-end

::: zone pivot="programming-language-rest-api"

::: moniker range="doc-intel-2.1.0"
[!INCLUDE [REST API](includes/v2-1/rest-api.md)]
::: moniker-end

::: zone-end

::: moniker range="doc-intel-2.1.0"

That's it, well done!

## Next steps

* For an enhanced experience and advanced model quality, try the [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio).

  * The Studio supports any model trained with v2.1 labeled data.
  
  * The changelogs provide detailed information about migrating from v3.1 to v4.0. 

::: moniker-end
