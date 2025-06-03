---
title: Azure AI Foundry custom translation key terms
titleSuffix: Azure AI services
description: List of key terms used in Azure AI Foundry custom translation articles.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.date: 05/19/2025
ms.author: lajanuar
ms.topic: reference
---

# Azure AI Foundry custom translation key terms

The following table presents a list of key terms that you may find as you work with custom translation in the [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs).

| Word or Phrase|Definition|
|------------------|-----------|
| **Source language** | The source language is the starting language that you want to convert to another language (the "target").|
| **Target language**| The target language is the language that you want the machine translation to provide after it receives the source language. |
| **Monolingual file** | A monolingual file has a single language not paired with another file of a different language. |
| **Parallel files** | A parallel file is combination of two files with corresponding text. One file has the source language. The other has the target language.|
| **Sentence alignment**| Parallel dataset must align sentences to sentences that represent the same text in both languages. For instance, in a source parallel file the first sentence should, in theory, map to the first sentence in the target parallel file.|
| **Aligned text** | One of the most important steps of file validation is to align the sentences in the parallel documents. Things are expressed differently in different languages. Also different languages have different word orders. This step does the job of aligning the sentences with the same content so that they can be used for training. A low sentence alignment indicates there might be something wrong with one or both of the files. |
| **Word breaking/ Unbreaking** | Word breaking is the function of marking the boundaries between words. Many writing systems use a space to denote the boundary between words. Word unbreaking refers to the removal of any visible marker that may be inserted between words in a preceding step. |
| **Delimiters**   | Delimiters are the ways that a sentence is divided up into segments or delimit the margin between sentences. For instance, in English spaces delimit words, colons, and semi-colons delimit clauses and periods delimit sentences. |
| **Training files** | A training file is used to teach the machine translation system how to map from one language (the source) to a target language (the target). The more data you provide, the better the system performs. |
| **Tuning files** | These files are often randomly derived from the training set (if you don't select a tuning set). The sentences are autoselected and used to tune the system and ensure that it's functioning properly. If you wish to create a general-purpose translation model and create your own tuning files, make sure they're a random set of sentences across domains |
| **Testing files**| These files are often derived files, randomly selected from the training set (if you don't select any test set). The purpose of these sentences is to evaluate the translation model's accuracy. To make sure the system accurately translates these sentences, you may wish to create a testing set and upload it to the translator. Doing so ensures that the sentences are used in the system's evaluation (the generation of a `BLEU` score).   |
| **Combo file**   | A type of file in which the source and translated sentences are contained in the same file. Supported file formats (`TMX`, `XLIFF`, `XLF`, `ICI`, and `XLSX`). |
| **Archive file** | A file that contains other files. Supported file formats (zip, gz, tgz).  |
| **`BLEU` Score**   | [`BLEU`](concepts/bleu-score.md) is the industry standard method for evaluating the "precision" or accuracy of the translation model. Though other methods of evaluation exist, Microsoft Translator relies `BLEU`  method to report accuracy to Project Owners.|
