---
title: Frequently asked questions - Azure Translator in Foundry Tools
titleSuffix: Foundry Tools
description: Get answers to frequently asked questions about the Azure Translator API in Foundry Tools.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: faq
ms.date: 11/18/2025
ms.author: lajanuar
---

# Azure Translator in Foundry Tools frequently asked questions

Welcome to Azure Translator frequently asked questions (FAQ). This resource provides targeted, technically focused answers to key questions regarding Azure Translator, Microsoft's advanced cloud-based machine translation service. Whether you are a developer seeking integration guidance or an IT professional evaluating multilingual support capabilities, these FAQs are designed to clarify Azure Translator's architecture, supported features, implementation strategies, and operational best practices.

## How does Azure Translator count characters?

Azure Translator counts every code point defined in Unicode as a character. Each translation counts as a separate translation, even if the request was made in a single API call translating to multiple languages. The length of the response doesn't matter and the number of requests, words, bytes, or sentences isn't relevant to character count.

Azure Translator counts the following input:

* Text passed to Azure Translator in the body of a request.
  * `Text` when using the [Translate](text-translation/reference/v3/translate.md), [Transliterate](text-translation/reference/v3/transliterate.md), and [Dictionary Lookup](text-translation/reference/v3/dictionary-lookup.md) methods
  * `Text` and `Translation` when using the [Dictionary Examples](text-translation/reference/v3/dictionary-examples.md) method.

* All markup: HTML, XML tags, etc. within the request body text field. JSON notation used to build the request (for instance the key "Text:") is **not** counted.
* An individual letter.
* Punctuation.
* A space, tab, markup, or any white-space character.
* A repeated translation, even if you previously translated the same text. Every character submitted to the translate function is counted even when the content is unchanged or the source and target language are the same.

For scripts based on graphic symbols, such as written Chinese and Japanese Kanji, the Azure Translator counts the number of Unicode code points. One character per symbol. Exception: Unicode surrogate pairs count as two characters.

Calls to the **Detect** and **BreakSentence** methods aren't counted in the character consumption. However, we do expect calls to the Detect and BreakSentence methods to be reasonably proportionate to the use of other counted functions. If the number of Detect or BreakSentence calls exceeds the number of other counted methods by 100 times, Microsoft reserves the right to restrict your use of the Detect and BreakSentence methods.

For detailed information regarding Azure Translator request limits, *see* [**Text translation request limits**](service-limits.md#text-translation).

## Where can I see my monthly usage?

The [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/) can be used to estimate your costs. You can also monitor, view, and add Azure alerts for your Azure services in your user account in the Azure portal:

1. Sign in to the [Azure portal](https://portal.azure.com).
1. Navigate to your Azure Translator resource Overview page.
1. Select the **subscription** for your Azure Translator resource.

    :::image type="content" source="media/azure-portal-overview.png" alt-text="Screenshot of the subscription link on overview page in the Azure portal.":::

1. In the left rail, make your selection under **Cost Management**:

    :::image type="content" source="media/azure-portal-cost-management.png" alt-text="Screenshot of the cost management resources links in the Azure portal.":::

## Is attribution required when using Azure Translator?

Attribution isn't required when using Azure Translator for text and speech translation. We recommended that you inform users that the content they're viewing is machine translated.

If attribution is present, it must conform to the [Azure Translator attribution guidelines](https://www.microsoft.com/translator/business/attribution/).

## Is Azure Translator a replacement for human translator?

No, both have their place as essential tools for communication. Use machine translation where the quantity of content, speed of creation, and budget constraints make it impossible to use human translation.

Machine translation is used as a first pass, before using human translation, by several of our [language service provider (LSP)](https://www.microsoft.com/translator/business/partners/) partners and can improve productivity by up to 50 percent. For a list of LSP partners, visit the Azure Translator partner page.

## Does Azure Translator retain any user data?

No. Customer data submitted for translation to Azure Translator isn't stored permanently and not data is stored at rest. There's no record of the submitted text or document in any Microsoft data center. All organizational data remains within your organization's Azure subscription, ensuring that no data is shared with Microsoft. You maintain full control over your data, which remains your exclusive business. Microsoft further strengthens this control by adhering to extensive privacy laws, such as GDPR, and privacy standards, including the ISO/IEC 27018—the world's first international code of practice for cloud privacy. For more information, *see* [Azure Translator data, privacy, and security](/azure/ai-foundry/responsible-ai/translator/data-privacy-security) and [Microsoft Translator Confidentiality](https://www.microsoft.com/translator/business/notrace/#compliance).

---
> [!TIP]

> If you can't find answers to your questions in this FAQ, try asking the Azure Translator API community on [StackOverflow](https://stackoverflow.com/search?q=%5Bmicrosoft-cognitive%5D+or+%5Bmicrosoft-cognitive%5D+translator&s=34bf0ce2-b6b3-4355-86a6-d45a1121fe27).

