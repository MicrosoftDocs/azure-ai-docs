---
title: "Frequently asked questions - Foundry Tools custom translation"
titleSuffix: Foundry Tools
description: This article contains answers to Microsoft Foundry custom translation frequently asked questions.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.date: 11/18/2025
ms.author: lajanuar
ms.topic: faq
---

# Foundry Tools custom translation frequently asked questions

This article contains answers to frequently asked questions about custom translation in [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs).

## What are the current restrictions in custom translation?

There are restrictions and limits with respect to file size, model training, and model deployment. Keep these restrictions in mind when setting up your training to build a model in custom translation.

- Files for translation must be less than 100 MB in size.
- Monolingual data isn't supported. A monolingual file has a single language not paired with another file of a different language.

## When should I request deployment for a trained translation system?

It may take several trainings to create the optimal translation system for your language pair. You might want to try using more training data or more carefully filtered data, if the **BLEU** score and/ or the test results aren't satisfactory. You should be strict and careful in designing your tuning set and your test set. Make certain your sets fully represent the terminology and style of material you want to translate. You can be more liberal in composing your training data, and experiment with different options. Request a system deployment when the translations in your system test results are satisfactory and you don't have more data to add to improve your trained system.

## How many trained systems can be deployed in a language pair?

Only one trained system can be deployed per a language pair. It may take several trainings to create a suitable translation system for your language pair and we encourage you to request deployment of a training that gives you the best result. You can determine the quality of the training by the **BLEU** score (higher is better), and by consulting with reviewers before deciding that the quality of translations is suitable for deployment.

## When can I expect my trained model to be deployed and ready to use?

The deployment generally takes less than an hour.

## How do you access a deployed system?

Deployed systems can be accessed via the Azure Translator Text API V3 by specifying the Category ID. More information about the Translator Text API can be found in the [API Reference](../../text-translation/reference/v3/translate.md) webpage.

## How do I skip alignment and sentence breaking if my data is already sentence aligned?

Custom translation skips sentence alignment and sentence breaking for **TMX** files and for text files with **align** extension. The **align** files give users an option to skip custom translation's sentence breaking and alignment process for the files that are perfectly aligned, and need no further processing. We recommend using **align** extension only for files that are perfectly aligned.

If the number of extracted sentences doesn't match the two files with the same base name, custom translation runs the sentence aligner on **align** files.

## I tried uploading my Translation Memory Exchange (TMX) file, but it says "document processing failed"

Ensure that the TMX conforms to the [TMX 1.4b Specification](https://www.ttt.org/oscarStandards/tmx/tmx14b.html).

## Next steps

> [!div class="nextstepaction"]
> [Learn more about custom translation](../azure-ai-foundry/beginners-guide.md)
