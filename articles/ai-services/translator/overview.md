---
title: What is Azure Translator in Foundry Tools?
titlesuffix: Foundry Tools
description: Learn more about Azure Translator, a cloud-based neural machine translation solution that translates text across multiple languages and dialects.
manager: nitinme
ms.service: azure-ai-translator
ms.topic: overview
ms.date: 01/12/2026
ms.author: lajanuar
---

# What is Azure Translator in Foundry Tools?

Azure Translator in Foundry Tools is a cloud-based neural machine translation service that's part of the [Foundry Tools](../what-are-ai-services.md) family and can be used with any operating system. Translator powers many Microsoft products and services used by thousands of businesses worldwide for language translation and other language-related operations. In this overview, learn how Translator can enable you to build intelligent, multi-language solutions for your applications across all [supported languages](./language-support.md).

## Azure Translator in Foundry Tools features and development options

Translator supports the following features. Use the links in this table to learn more about each feature and browse the API references.

| Feature | Description | Development options |
| -- | -- | -- |
| [**Text translation 2025-10-01-preview (latest)**](text-translation/preview/overview.md) | &bullet; Azure Translator in Foundry Tools text translation `2025-10-01-preview` introduces our newest cloud-based, multilingual, neural machine translation service.</br>&bullet; Key enhancements include the option to select specified large language models (LLM), adaptive custom translation, and expanded parameters for translation requests.</br>&bullet; For more information, *see* the [preview migration guide](text-translation/how-to/migrate-to-preview.md). | [**REST API**](text-translation/preview/rest-api-guide.md) |
| [**Text translation v3 (GA)**](text-translation/overview.md) | Execute text translation between supported source and target languages in real time. Create a [dynamic dictionary](dynamic-dictionary.md) and learn how to [prevent translations](prevent-translation.md) using the Translator API. | &bull; [**REST API**](text-translation/reference/rest-api-guide.md)</br></br>&bull; [**Text translation SDK**](text-sdk-overview.md)</br></br>&bullet; [**Foundry (classic) portal**](https://ai.azure.com/) </br></br>&bull; [**Translator container**](containers/translator-how-to-install-container.md) |
| [**Document translation (Asynchronous)**](document-translation/overview.md) | &bullet; **Batch translation**: Translate batch and complex files while preserving the structure and format of the original documents. The batch translation process requires an Azure Blob storage account with containers for your source and translated documents.| &bull; [**REST API**](document-translation/reference/rest-api-guide.md)</br></br>&bullet; [**Document Translation SDK**](document-translation/document-sdk-overview.md)</br></br>&bullet; [**Translator container**](containers/translator-how-to-install-container.md) |
| [**Document translation (Synchronous)**](document-translation/overview.md) | &bullet; **Single file translation**: Translate a single document file alone or with a glossary file while preserving the structure and format of the original document. The file translation process doesn't require an Azure Blob storage account. The final response contains the translated document and is returned directly to the calling client. | &bull; [**REST API**](document-translation/reference/rest-api-guide.md)</br></br>&bullet; [**Foundry (classic) portal**](https://ai.azure.com/)</br></br>&bull; [**Translator container**](containers/translator-how-to-install-container.md) |
| [**Custom Translator**](custom-translator/overview.md) | Build customized models to translate domain- and industry-specific language, terminology, and style. [Create a dictionary (phrase or sentence)](custom-translator/concepts/dictionaries.md) for custom translations. | &bull; [**Custom Translator portal**](https://portal.customtranslator.azure.ai/) |

For detailed information regarding Azure Translator request limits, *see* [**Service and request limits**](service-limits.md#text-translation).

> [!TIP]
> Use  [**Microsoft Foundry**](https://ai.azure.com/) for text and synchronous document translation operations via a no-code interface.

## Try the Translator service for free

First, you need a Microsoft account; if you don't have one, you can sign up for free at the [**Microsoft account portal**](https://account.microsoft.com/account). Select **Create a Microsoft account** and follow the steps to create and verify your new account.

Next, you need to  have an Azure account—navigate to the [**Azure sign-up page**](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn), select the **Start free** button, and create a new Azure account using your Microsoft account credentials.

Now, you're ready to get started! [**Create a Translator**](how-to/create-translator-resource.md "Go to the Azure portal."), [**get your access keys and API endpoint**](how-to/create-translator-resource.md#authentication-keys-and-endpoint-url "An endpoint URL and read-only key are required for authentication."), and try our [**quickstart**](text-translation/quickstart/rest-api.md "Learn to use Translator via REST.").

## Next steps

* Learn more about the following features:

  * [**Text translation**](text-translation/overview.md)
  * [**Document translation**](document-translation/overview.md)
  * [**Custom Translator**](custom-translator/overview.md)

* Review [**Translator pricing**](https://azure.microsoft.com/pricing/details/cognitive-services/translator-text-api/)
