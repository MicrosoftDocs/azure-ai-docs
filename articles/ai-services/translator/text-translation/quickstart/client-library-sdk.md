---
title: "Quickstart: Azure Translator client libraries (SDKs)"
titleSuffix: Foundry Tools
description: "Learn to translate text with the Translator service SDks in a programming language of your choice: C#, Java, JavaScript, or Python."
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: quickstart
ms.date: 11/18/2025
ms.author: lajanuar
ms.devlang: csharp
# ms.devlang: csharp, java, javascript, python
ms.custom: mode-other, devx-track-dotnet, devx-track-extended-java, devx-track-js, devx-track-python
zone_pivot_groups:  programming-languages-set-translator-sdk
---

<!-- markdownlint-disable MD033 -->
<!-- markdownlint-disable MD001 -->
<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD036 -->
<!-- markdownlint-disable MD049 -->

# Quickstart: Azure Translator SDKs (text translation)

In this quickstart, get started using the Translator to [translate text](../reference/v3/translate.md) using a programming language of your choice. For this project, we recommend using the free pricing tier (F0), while you're learning the technology, and later upgrading to a paid tier for production.

## Prerequisites

You need an active Azure subscription. If you don't have an Azure subscription, you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)

* Once you have your Azure subscription, create a [Translator resource](../../create-translator-resource.md) in the [Azure portal](https://portal.azure.com/#create/Microsoft.CognitiveServicesTextTranslation).

* After your resource deploys, select **Go to resource** and retrieve your key and endpoint.

  * Get the key, endpoint, and region from the resource and connect your application to the Translator. Paste these values into the code later in the quickstart. You can find them on the Azure portal **Keys and Endpoint** page:

    :::image type="content" source="../../media/quickstarts/keys-and-endpoint-portal.png" alt-text="Screenshot: Azure portal keys and endpoint page.":::

::: zone pivot="programming-language-csharp"

[!INCLUDE [C# programming](includes/client-libraries-sdk/csharp.md)]
::: zone-end

::: zone pivot="programming-language-java"

[!INCLUDE [Java programming](includes/client-libraries-sdk/java.md)]
::: zone-end

::: zone pivot="programming-language-javascript"

[!INCLUDE [Node.js programming](includes/client-libraries-sdk/javascript.md)]
::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python programming](includes/client-libraries-sdk/python.md)]
::: zone-end

That's it, congratulations! In this quickstart, you used a Text translation SDK to translate text.

## Next steps

Learn more about Text translation development options:

> [!div class="nextstepaction"]
>[Text translation SDK overview](../sdk-overview.md) </br></br>[Text translation V3 reference](../reference/v3/reference.md)
