---
title: What's new in Azure AI Translator?
titleSuffix: Azure AI services
description: Learn about the latest changes to the Azure AI Translator Service API.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: overview
ms.date: 06/03/2025
ms.author: lajanuar
---
<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD036 -->
<!-- markdownlint-disable MD001 -->

# What's new in Azure AI Translator?

Bookmark this page to stay up to date with release notes, feature enhancements, and our newest documentation.

Azure AI Translator is a language service that enables users to translate text and documents, helps entities expand their global outreach, and supports preservation of at-risk and endangered languages. 

Azure AI Translator service supports language translation for more than 100 languages. If your language community is interested in partnering with Microsoft to add your language to Translator, contact us via the [Translator community partner onboarding form](https://forms.office.com/pages/responsepage.aspx?id=v4j5cvGGr0GRqy180BHbR-riVR3Xj0tOnIRdZOALbM9UOU1aMlNaWFJOOE5YODhRR1FWVzY0QzU1OS4u).

## June 2025

### Document Translation new feature update

Azure AI Translator [Document translation feature](document-translation/overview.md#batch-key-features) now supports [translating text embedded in images](document-translation/how-to-guides/use-rest-api-programmatically.md#translate-text-embedded-in-images-within-documents-) within documents.

* This feature is optional and must be enabled for each translation request.
* Currently, the feature is available only with the [batch document translation](document-translation/how-to-guides/use-rest-api-programmatically.md#translate-text-embedded-within-images-in-a-document-) API for `.docx` file format.
* An [Azure AI Foundry resource](https://portal.azure.com/?Microsoft_Azure_PIMCommon=true#create/Microsoft.CognitiveServicesAIFoundry) (not the standalone Translator resource) is required to use this feature.

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

A [single API](document-translation/reference/rest-api-guide.md) is now available for both [asynchronous batch](document-translation/overview.md#asynchronous-batch-translation) and [synchronous single document](document-translation/overview.md#synchronous-translation) translation operations.

## February 2024

The Document translation API now supports two translation operations:

* [Asynchronous Batch](document-translation/overview.md#asynchronous-batch-translation) document translation supports asynchronous processing of multiple documents and files. The batch translation process requires an Azure Blob storage account with containers for your source and translated documents.

* [Synchronous](document-translation/overview.md#synchronous-translation) document translation supports synchronous processing of single file translations. The file translation process doesn't require an Azure Blob storage account. The final response contains the translated document and is returned directly to the calling client.

## Related content

[Azure AI Translator release history](release-history.md)

