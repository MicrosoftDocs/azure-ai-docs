---
title: Dynamic Dictionary - Azure Translator in Foundry Tools
titleSuffix: Foundry Tools
description: Learn how to use the dynamic dictionary feature of the Azure Translator.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: how-to
ms.date: 11/18/2025
ms.author: lajanuar
---

# Azure Translator in Foundry Tools dynamic dictionary

The Azure Translator dynamic dictionary feature allows you to customize translations for specific terms or phrases. You define custom translations for your unique context, language, or specific needs. If you already know the translation you want to apply to a word or a phrase, you can supply it as markup within the request. The dynamic dictionary is safe only for compound nouns like proper names and product names.

**Syntax:**

<mstrans:dictionary translation="translation of phrase">phrase</mstrans:dictionary>

**Requirements:**

* The `From` and `To` languages must include English and another supported language. 
* You must include the `From` parameter in your API translation request instead of using the autodetect feature. 

**Example: en-de:**

Source input: `The word <mstrans:dictionary translation=\"wordomatic\">wordomatic</mstrans:dictionary> is a dictionary entry.`

Target output: `Das Wort "wordomatic" ist ein Wörterbucheintrag.`

This feature works the same way with and without HTML mode.

Using the dynamic dictionary feature is considered one of the simplest methods to customize translation output. While it's highly effective, the process of creating and maintaining dynamic dictionaries for a large number of terms can be challenging and time-intensive. In such cases, a custom translation using Custom Translator can be a more viable choice. Custom Translator makes full use of context and statistical probabilities. If you have or can create training data that shows your work or phrase in context, you get better results. You can find more information about Custom Translator at [https://aka.ms/CustomTranslator](https://aka.ms/CustomTranslator).
