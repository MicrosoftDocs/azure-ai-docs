---
title: Azure Translator in Foundry Tools custom translation for beginners
titleSuffix: Foundry Tools
description: User guide for understanding the end-to-end customized machine translation process using Microsoft Foundry.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.author: lajanuar
ms.date: 11/18/2025
ms.topic: overview
---

# Foundry Tools custom translation for beginners

 [Custom translation](overview.md) enables you to a build translation system that reflects your business, industry, and domain-specific terminology and style. Training and deploying a custom system is easy and doesn't require any programming skills. The customized translation system seamlessly integrates into your existing applications, workflows, and websites and is available on Azure through the same cloud-based [Microsoft Text Translation API](../../text-translation/reference/v3/translate.md) service that powers billions of translations every day.

[Custom translation](overview.md) empowers you to build a translation system that truly captures your business's unique language, industry terminology, and domain-specific style. With an intuitive interface, training, testing, and deploying your custom model is simple and requires no programming expertise. Seamlessly integrate your tailored translation system into your existing applications, workflows, and websites—all backed by the cloud-based [Azure Translator Text Translation API](../../text-translation/reference/v3/translate.md?tabs=curl) service that powers billions of translations each day.

The platform enables users to build and publish custom translation systems to and from English. The Custom Translator supports more than 100 languages that map directly to the languages available for Neural machine translation (NMT). For a complete list, *see* [Translator language support](../../../language-support.md).

## Is a custom translation model the right choice for you?

A well-trained custom translation model excels at delivering accurate, domain-specific translations by learning from your previously translated in-domain documents. This approach ensures that your specialized terms and phrases are used in context, producing fluent, natural translations that respect the target language's grammatical nuances.

Keep in mind that developing a full custom translation model requires a substantial amount of training data—typically at least 10,000 parallel sentences. If you don't have enough data to train a comprehensive model, you might consider building a dictionary-only model to capture essential terminology, or you can rely on the high-quality, out-of-the-box translations offered by the Text Translation API.

Ultimately, if you need translations that reflect your industry's specific language and you have ample training resources, a custom translation model can be the ideal choice for your organization.

:::image type="content" source="../media/how-to/for-beginners.png" alt-text="Screenshot illustrating the difference between custom and general models.":::

## What does training a custom translation model involve?

Building a custom translation model requires:

* Understanding your use-case.

* Obtaining in-domain translated data (preferably human translated).

* Assessing translation quality or target language translations.

## How do I evaluate my use-case?

Having clarity on your use-case and what success looks like is the first step towards sourcing proficient training data. Here are a few considerations:

* Is your desired outcome specified and how is it measured?

* Is your business domain identified?

* Do you have in-domain sentences of similar terminology and style?

* Does your use-case involve multiple domains? If yes, should you build one translation system or multiple systems?

* Do you have requirements impacting regional data residency at-rest and in-transit?

* Are the target users in one or multiple regions?

## How should I source my data?

Finding in-domain quality data is often a challenging task that varies based on user classification. Here are some questions you can ask yourself as you evaluate what data is available to you:

* Does your company have previous translation data available that you can use? Enterprises often have a wealth of translation data accumulated over many years of using human translation.

* Do you have a vast amount of monolingual data? Monolingual data is data in only one language. If so, can you get translations for this data?

* Can you crawl online portals to collect source sentences and synthesize target sentences?

## What should I use for training material?

| Source | What it does | Rules to follow |
|---|---|---|
| Bilingual training documents | Teaches the system your terminology and style. | **Be liberal**. Any in-domain human translation is better than machine translation. Add and remove documents as you go and try to improve the [BLEU score](concepts/bleu-score.md?WT.mc_id=aiml-43548-heboelma). |
| Tuning documents | Trains the Neural Machine Translation parameters. | **Be strict**. Compose them to be optimally representative of what you are going to translate in the future. |
| Test documents | Calculate the [BLEU score](concepts/bleu-score.md?WT.mc_id=aiml-43548-heboelma).| **Be strict**. Compose test documents to be optimally representative of what you plan to translate in the future. |
| Phrase dictionary | Forces the given translation 100% of the time. | **Be restrictive**. A phrase dictionary is case-sensitive and any word or phrase listed is translated in the way you specify. In many cases, it's better to not use a phrase dictionary and let the system learn. |
| Sentence dictionary | Forces the given translation 100% of the time. | **Be strict**. A sentence dictionary is case-insensitive and good for common in domain short sentences. For a sentence dictionary match to occur, the entire submitted sentence must match the source dictionary entry. If only a portion of the sentence matches, the entry doesn't match. |

## What is a BLEU score?

BLEU (Bilingual Evaluation Understudy) is an algorithm for evaluating the precision or accuracy of text that's machine translated from one language to another. Custom translation uses the BLEU metric as one way of conveying translation accuracy.

A BLEU score is a number between zero and 100. A score of zero indicates a low quality translation where nothing in the translation matched the reference. A score of 100 indicates a perfect translation that's identical to the reference. It's not necessary to attain a score of 100 - a BLEU score between 40 and 60 indicates a high-quality translation.

[Read more](concepts/bleu-score.md?WT.mc_id=aiml-43548-heboelma)

## What happens if I don't submit tuning or testing data?

Tuning and test sentences are optimally representative of what you plan to translate in the future. If you don't submit any tuning or testing data, custom translation automatically excludes sentences from your training documents to use as tuning and test data.

| System-generated | Manual-selection |
|---|---|
| Convenient. | Enables fine-tuning for your future needs.|
| Good, if you know that your training data is representative of what you are planning to translate. | Provides more freedom to compose your training data.|
| Easy to redo when you grow or shrink the domain. | Allows for more data and better domain coverage.|
|Changes each training run.| Remains static over repeated training runs|

## How is training material processed by custom translation?

To prepare for training, documents undergo a series of processing and filtering steps. Knowledge of the filtering process can help with understanding the sentence count displayed as well as the steps you can take to prepare training documents for training with custom translation. The filtering steps are as follows:

* ### Sentence alignment

  If your document isn't in `XLIFF`, `XLSX`, `TMX`, or `ALIGN` format, custom translation aligns the sentences of your source and target documents to each other, sentence-by-sentence. Translator doesn't perform document alignment—it follows your naming convention for the documents to find a matching document in the other language. Within the source text, custom translation tries to find the corresponding sentence in the target language. It uses document markup like embedded HTML tags to help with the alignment.

  If you see a large discrepancy between the number of sentences in the source and target documents, your source document can't be parallel, or couldn't be aligned. The document pairs with a large difference (>10%) of sentences on each side warrant a second look to make sure they're indeed parallel.

* ### Tuning and testing data extraction

  Tuning and testing data is optional. If you don't provide it, the system removes an appropriate percentage from your training documents to use for tuning and testing. The removal happens dynamically as part of the training process. Since this step occurs as part of training, your uploaded documents aren't affected. You can see the final used sentence counts for each category of data—training, tuning, testing, and dictionary—on the Model details page after training succeeds.

* ### Length filter

  * Removes sentences with only one word on either side.
  * Removes sentences with more than 100 words on either side. Chinese, Japanese, Korean are exempt.
  * Removes sentences with fewer than three characters. Chinese, Japanese, Korean are exempt.
  * Removes sentences with more than 2,000 characters for Chinese, Japanese, Korean.
  * Removes sentences with less than 1% alphanumeric characters.
  * Removes dictionary entries containing more than 50 words.

* ### White space

  * Replaces any sequence of white-space characters including tabs and CR/LF sequences with a single space character.
  * Removes leading or trailing space in the sentence.

* ### Sentence end punctuation

  * Replaces multiple sentence-end punctuation characters with a single instance. Japanese character normalization.

  * Converts full width letters and digits to half-width characters.

* ### Unescaped XML tags

   Transforms unescaped tags into escaped tags:

  | Tag | Becomes |
  |---|---|
  | \&lt; | \&amp;lt;  |
  | \&gt; | \&amp;gt;  |
  | \&amp; | \&amp;amp; |

* ### Invalid characters

  Custom translation removes sentences that contain Unicode character U+FFFD. The character U+FFFD indicates a failed encoding conversion.

* ### Invalid HTML tags

  Custom translation removes valid tags during training. Invalid tags cause unpredictable results and should be manually removed. 

## What steps should I take before uploading data?

* Remove sentences with invalid encoding.
* Remove Unicode control characters.
* Align sentences (source-to-target), if feasible.
* Remove source and target sentences that don't match the source and target languages.
* When source and target sentences have mixed languages, ensure that untranslated words are intentional, for example, names of organizations and products.
* Avoid teaching errors to your model by making certain that grammar and typography are correct.
* Have one source sentence mapped to one target sentence. Although our training process handles source and target lines containing multiple sentences, one-to-one mapping is a best practice.
* Remove invalid HTML tags before uploading training data.

## How do I evaluate the results?

After your model is successfully trained, you can view the model's BLEU score and baseline model BLEU score on the model details page. We use the same set of test data to generate both the model's BLEU score and the baseline BLEU score. This data helps you make an informed decision regarding which model would be better for your use-case.

## Next steps

> [!div class="nextstepaction"]
> [Try create project](../azure-ai-foundry/how-to/create-project.md)
