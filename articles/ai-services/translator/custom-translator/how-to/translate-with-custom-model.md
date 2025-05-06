---
title: Translate text with an Azure AI Custom Translator model
titleSuffix: Azure AI services
description: How to make translation requests using custom models published with the Azure AI Custom Translator.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.date: 05/19/2025
ms.author: lajanuar
ms.topic: how-to
---
# Translate text with an Azure AI Custom Translator model

After you publish your custom model, you can access it with the Azure AI Translator API by using the `Category ID` parameter.

## How to translate

1. Use the `Category ID` when making a custom translation request via Microsoft Translator [Text API V3](../../text-translation/reference/v3/translate.md?tabs=curl). The `Category ID` is created by concatenating the WorkspaceID, project label, and category code. Use the `CategoryID` with the Text translation API to get custom translations.

   ```http
   https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=de&category=a2eb72f9-43a8-46bd-82fa-4693c8b64c3c-TECH

   ```

   More information about the Translator Text API can be found on the [Translator API Reference](../../text-translation/reference/v3/translate.md) page.

1. You can also download and install our free [DocumentTranslator app for Windows](https://github.com/MicrosoftTranslator/DocumentTranslation/releases).

## Next steps

> [!div class="nextstepaction"]
> [Learn more about building and publishing  Azure AI Custom Translator models](../beginners-guide.md)
