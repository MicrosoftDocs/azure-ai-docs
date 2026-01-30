---
title: Migrate to V3 - Azure Translator in Foundry Tools
titleSuffix: Foundry Tools
description: This article provides the steps to help you migrate from V2 to V3 of the Azure Translator.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: concept-article
ms.date: 11/18/2025
ms.author: lajanuar
---

# Azure Translator in Foundry Tools V3 Migration

> [!NOTE]
> Microsoft Translator V2 was deprecated on April 30, 2018. Migrate your applications to V3 and experience new functionality available exclusively in V3. V2 was retired on May 24, 2021.

Azure Translator Version 3 (V3) is generally available. The release includes new features, deprecated methods and a new format for sending to, and receiving data from the Microsoft Translator. This document provides information for changing applications to use V3.

The end of this document contains helpful links for you to learn more.

## Summary of features

* No Trace - In V3 No-Trace applies to all pricing tiers in the Azure portal. This feature means that the service doesn't save text submitted to the V3 API.
* JSON - XML replaces JSON. All data sent to the service and received from the service is in JSON format.
* Multiple target languages in a single request - The Translate method accepts multiple `to` languages for translation in a single request. For example, a single request can be `from` English and `to` German, Spanish and Japanese, or any other group of languages.
* Bilingual dictionary - A bilingual dictionary method is added to the API. This method includes `lookup` and `examples`.
* Transliteration - A transliterate method is added to the API. This method converts words and sentences in one script into another script. For example, Arabic to Latin.
* Languages - A new `languages` method delivers language information, in JSON format, for use with the `translate`, `dictionary`, and `transliterate` methods.
* New to Translate - New capabilities are added to the `translate` method to support some of the features that were in the V2 API as separate methods. An example is TranslateArray.
* Speech method - Text to speech functionality is no longer supported in the Microsoft Translator. Text to speech functionality is available in [Microsoft Speech Service](../../../speech-service/text-to-speech.md).

The following list of V2 and V3 methods identifies the V3 methods and APIs that provide the functionality that came with V2.

| V2 API Method   | V3 API Compatibility |
|:----------- |:-------------|
| `Translate`     | [Translate](../reference/v3/translate.md)          |
| `TranslateArray`      | [Translate](../reference/v3/translate.md)        |
| `GetLanguageNames`      | [Languages](../reference/v3/languages.md)         |
| `GetLanguagesForTranslate`     | [Languages](../reference/v3/languages.md)       |
| `GetLanguagesForSpeak`      | [Microsoft Speech Service](../../../speech-service/language-support.md)         |
| `Speak`     | [Microsoft Speech Service](../../../speech-service/text-to-speech.md)          |
| `Detect`     | [Detect](../reference/v3/detect.md)         |
| `DetectArray`     | [Detect](../reference/v3/detect.md)         |
| `AddTranslation`     | Feature is no longer supported       |
| `AddTranslationArray`    | Feature is no longer supported          |
| `BreakSentences`      | [BreakSentence](../reference/v3/break-sentence.md)       |
| `GetTranslations`      | Feature is no longer supported         |
| `GetTranslationsArray`      | Feature is no longer supported         |

## Move to JSON format

Microsoft Translator Translation V2 accepted and returned data in XML format. In V3, all data sent and received using the API is in JSON format. XML is no longer accepted or returned in V3.

This change affects several aspects of an application written for the V2 Text translation API. As an example: The Languages API returns language information for text translation, transliteration, and the two dictionary methods. You can request all language information for all methods in one call or request them individually.

## Authentication Key

The authentication key used for V2 is accepted for V3. You don't need to get a new subscription. You can mix V2 and V3 in your apps during the yearlong migration period, making it easier for you to release new versions while you migrate from V2-XML to V3-JSON.

## Pricing Model

Microsoft Translator V3 is priced in the same way V2 was priced; per character, including spaces. The new features in V3 make some changes in what characters are counted for billing.

| V3 Method   | Characters Counted for Billing |
|:----------- |:-------------|
| `Languages`     | No characters submitted, none counted, no charge.          |
 | `Translate`     | Count is based on how many characters are submitted for translation, and how many languages the characters are translated into. 50 characters submitted, and 5 counted as 50x5.           |
| `Transliterate`     | Number of characters submitted for transliteration are counted.         |
| `Dictionary lookup & example`     | Number of characters submitted for Dictionary lookup and examples are counted.         |
| `BreakSentence`     | No Charge.       |
| `Detect`     | No Charge.      |

## V3 End Points

Global

* api.cognitive.microsofttranslator.com

## V3 API text translations methods

[`Languages`](../reference/v3/languages.md)

[`Translate`](../reference/v3/translate.md)

[`Transliterate`](../reference/v3/transliterate.md)

[`BreakSentence`](../reference/v3/break-sentence.md)

[`Detect`](../reference/v3/detect.md)

[`Dictionary/lookup`](../reference/v3/dictionary-lookup.md)

[`Dictionary/example`](../reference/v3/dictionary-examples.md)

## Compatibility and customization

> [!NOTE]
>
> The Microsoft Translator Hub will be retired on May 17, 2019. [View important migration information and dates](https://www.microsoft.com/translator/business/hub/).

Azure Translator V3 uses neural machine translation by default. As such, it can't be used with the Microsoft Translator Hub. The Translator Hub only supports legacy statistical machine translation. Customization for neural translation is now available using the Custom Translator. [Learn more about customizing neural machine translation](../../custom-translator/overview.md)

Neural translation with the V3 text API doesn't support the use of standard categories (`SMT`, `speech`, `tech`, `generalnn`).

| Version | Endpoint | Translator Hub support? | Custom Translator support? |
| :------ | :------- |:----------------- | :------------------------------ |
|Translator Version 2|  api.microsofttranslator.com|Yes  |No|
|Translator Version 3|  api.cognitive.microsofttranslator.com| No| Yes|

**Translator Version 3**

* It's generally available and fully supported.
* It allows you to invoke the neural network translation systems you customized with Custom Translator (Preview), the new Translator neural machine translation (NMT) customization feature.
* It doesn't provide access to custom translation systems created using the Microsoft Translator Hub.

You're using Version 3 of the Translator if you're using the api.cognitive.microsofttranslator.com endpoint.

**Translator Version 2**

* Doesn't satisfy all ISO 20001,20018 and SOC 3 certification requirements.
* Doesn't allow you to invoke the neural network translation systems you customized with the Translator customization feature.
* Does provide access to custom translation systems created using the Microsoft Translator Hub.
* Uses the api.microsofttranslator.com endpoint.

No version of the Azure Translator creates a record of your translations. Your translations are never shared with anyone. More information on the [Translator No-Trace](https://www.aka.ms/NoTrace) webpage.

## Links

* [Microsoft Privacy Policy](https://privacy.microsoft.com/privacystatement)
* [Microsoft Azure Legal Information](https://azure.microsoft.com/support/legal)
* [Online Services Terms](https://www.microsoftvolumelicensing.com/DocumentSearch.aspx?Mode=3&DocumentTypeId=31)

## Next steps

> [!div class="nextstepaction"]
> [View Azure Translator V3.0 Documentation](../reference/v3/reference.md)
