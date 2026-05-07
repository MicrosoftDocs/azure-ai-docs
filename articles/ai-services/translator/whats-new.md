---
title: What's new in Azure Translator in Foundry Tools?
titleSuffix: Foundry Tools
description: Learn about the latest changes to the Azure Translator API.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: overview
ms.date: 05/05/2026
ms.author: lajanuar
---
<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD036 -->
<!-- markdownlint-disable MD001 -->
<!-- markdownlint-disable MD025 -->

# What's new in Azure Translator?

Bookmark this page to stay up to date with release notes, feature enhancements, and our newest documentation.

Azure Translator in Foundry Tools is a language service that enables users to translate text and documents, helps entities expand their global outreach, and supports preservation of at-risk and endangered languages. 

Azure Translator supports language translation for more than 100 languages. If your language community is interested in partnering with Microsoft to add your language to Translator, contact us via the [Translator community partner onboarding form](https://forms.office.com/pages/responsepage.aspx?id=v4j5cvGGr0GRqy180BHbR-riVR3Xj0tOnIRdZOALbM9UOU1aMlNaWFJOOE5YODhRR1FWVzY0QzU1OS4u).

## June 2026

### Azure Translator 2026-06-06 (GA) release

Translator **2026-06-06** is our latest cloud-based multilingual translation service. You can choose between neural machine translation (NMT) or generative AI language models (LLMs) for each request. Both approaches are available at production scale. To learn more about migrating to Translator 2026-06-06, *see* [Migrate from Azure Translator Text API v3 to Azure Translator Text API 2026-06-06](text-translation/how-to/migrate-to-2026-06-06.md).

### Microsoft Foundry (new)

**Microsoft Foundry portal**: Provides unified access to translation models, agents, and tools in a single interface. Enables you to manage projects and experiments, build end-to-end translation workflows, and test configurations in real time before deployment.

**Text translation**: Lets you choose from multiple models and tailor translations by gender or tone. Allows you to refine output using domain-specific data and terminology, with access to a playground for testing translation quality.

**Document translation**: Enables you to upload or paste content, select a target language, and preview translated output directly in an integrated playground.

**Adaptive custom translation (AdaptCT)**: Available in Foundry under **Build** → **Models** → **AI Services** → **Azure Translator** — **Text Translation** → **Adaptive LLM**. Allows you to upload bilingual documents, create language-pair dataset indexes, and validate translation results.

  :::image type="content" source="media/adaptive-custom-translation.png" alt-text="Screenshot of the adaptive custom translation pane in Foundry." lightbox="media/adaptive-custom-translation.png":::

## December 2025

### Translate image files (2025-12-01-preview)

**Asynchronous document translation image file formats support**

* The batch API now enables you to [submit image files for translation](document-translation/reference/start-batch-translation.md#translate-image-files).
* This update eliminates the requirement to preprocess images by converting them to PDF format or using scanned PDF translation pipelines
* For pricing details, *see* [Azure Translator pricing ](https://azure.microsoft.com/pricing/details/cognitive-services/translator/)

## November 2025

### Microsoft Foundry (new)

**Microsoft Foundry portal**: Streamlines access to models, agents, and tools for Foundry projects.

**Text translation**: Choose from three model options: Azure-MT (neural machine translation), GPT-4o, and GPT-4o mini. Tailor translations to specific gender or tone preferences, and refine results with your domain-specific data and terminology.

**Document translation**: Available through a built-in playground where you can upload or paste content, select a target language, and preview translated output.

### Azure Translator in Foundry Tools 2025-10-01-preview

Translator `2025-10-01-preview` is our newest cloud-based multilingual translation solution. It offers flexibility to use either standard neural machine translation (NMT) or select from various generative AI large language models (LLMs) for each translation request. This service provides powerful and scalable translation functionality, making it ideal for a wide range of needs and applications.

For more information, *see* [Text translation overview](text-translation/overview.md).

## July 2025

### Microsoft Translator Pro expanded on-device language support

[**Microsoft Translator Pro**](translator-pro/overview.md) is a mobile app that delivers accurate real-time speech-to-speech translations. It now offers expanded multilingual support on-device (doesn't require internet connectivity). For more information, *see* our [Translator Pro Language support](solutions/translator-pro/language-support.md).

## June 2025

### Document Translation new feature update

Azure Translator [Document translation feature](document-translation/overview.md#key-features) now supports [translating text embedded in images detected in Word documents](document-translation/how-to-guides/use-rest-api-programmatically.md#translate-images-in-word-documents-docx-and-powerpoint-files-pptx) within documents.

* This feature is optional and must be enabled for each translation request.
* Currently, the feature is available only with the [batch document translation](document-translation/how-to-guides/use-rest-api-programmatically.md#translate-images-in-word-documents-docx-and-powerpoint-files-pptx) API for `.docx` file format.
* A [Foundry resource](https://portal.azure.com/?Microsoft_Azure_PIMCommon=true#create/Microsoft.CognitiveServicesAIFoundry) (not the standalone Translator resource) is required to use this feature.

## May 2025

### Microsoft Translator Pro new feature update

[**Microsoft Translator Pro**](translator-pro/overview.md), a mobile application that provides precise real-time speech-to-speech translations, now includes **same-language transcription**. This functionality accurately converts spoken words into written text while maintaining the original language of the speech.

## March 2025

### Microsoft Translator Pro new features and updates

[**Microsoft Translator Pro**](translator-pro/overview.md) is a mobile application designed specifically for enterprises, providing precise real-time speech-to-speech translations. The latest updates include:

  * A new text-to-speech experience in full-screen mode that lets you decide which translated sentences to skip and which to play.

  * An audio noise cancellation feature that ensures seamless conversations by suppressing background noise. This feature can be enabled/disabled in settings.

  * On-device translation that now supports non-English source languages.


## February 2025

### Microsoft Translator Pro features and updates

[**Microsoft Translator Pro**](translator-pro/overview.md) is a mobile application, designed specifically for enterprises, that enables seamless real-time speech-to-speech translation. The following new and updated capabilities are now available:

* **Enhanced administrator experience**. The history section now includes options for recording transcript and audio, exporting sessions/audio, sharing sessions, and toggling transcript/audio history without exporting to cloud storage. Additionally, administrators can now enable or disable the use of a custom phrasebook and easily browse the current phrasebook.
* **Added content filtering**. Administrators can now enable or disable content filtering and censoring, providing greater control over content visibility.
* **Enabled full screen mode**. A full screen viewing option is now available, enabling translations to be viewed on a single screen rather than a split-screen view.
* **Expanded source language support**. Translation source language support is broadened to include all languages.

## January 2025

[**Microsoft Translator Pro**](translator-pro/overview.md), a speech-to-speech translation mobile app, is now generally available (GA).

## May 2024

A [single API](document-translation/reference/rest-api-guide.md) is now available for both [asynchronous batch](document-translation/overview.md#key-features) and [synchronous single document](document-translation/overview.md#key-features) translation operations.

## February 2024

The Document translation API now supports two translation operations:

* [Asynchronous Batch](document-translation/overview.md#key-features) document translation supports asynchronous processing of multiple documents and files. The batch translation process requires an Azure Blob storage account with containers for your source and translated documents.

* [Synchronous](document-translation/overview.md#key-features) document translation supports synchronous processing of single file translations. The file translation process doesn't require an Azure Blob storage account. The final response contains the translated document and is returned directly to the calling client.

## Related content

[Azure Translator release history](release-history.md)



