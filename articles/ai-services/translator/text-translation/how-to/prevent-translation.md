---
title: Prevent content translation - Azure Translator in Foundry Tools
titleSuffix: Foundry Tools
description: Prevent translation of content with the Azure Translator. Azure Translator allows you to tag content so that it isn't translated.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: how-to
ms.date: 11/18/2025
ms.author: lajanuar
---

# Prevent content translation with Azure Translator

Azure Translator in Foundry Tools allows you to tag content so that it isn't translated. For example, you might want to tag code, a brand name, or a word/phrase that doesn't make sense when localized.

## Methods for preventing translation

1. Tag your content with `notranslate`. It's by design that this works only when the input textType is set as HTML

   Example:

   ```html
   <span class="notranslate">This will not be translated.</span>
   <span>This will be translated. </span>
   ```

   ```html
   <div class="notranslate">This will not be translated.</div>
   <div>This will be translated. </div>
   ```

2. Tag your content with `translate="no"`. This tag only works when the input textType is set as HTML

   Example:

   ```html
   <span translate="no">This will not be translated.</span>
   <span>This will be translated. </span>
   ```

   ```html
   <div translate="no">This will not be translated.</div>
   <div>This will be translated. </div>
   ```

3. Use the [dynamic dictionary](../../dynamic-dictionary.md) to prescribe a specific translation.

4. Don't pass the string to the Translator for translation.

5. Custom Translator: Use a [dictionary in Custom Translator](../../custom-translator/concepts/dictionaries.md) to prescribe the translation of a phrase with 100% probability.

## Next steps

> [!div class="nextstepaction"]
> [Translate text reference](../reference/v3/translate.md)
