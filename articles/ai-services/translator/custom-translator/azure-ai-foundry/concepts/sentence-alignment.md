---
title: Foundry Tools custom translation sentence pairing and alignment
titleSuffix: Foundry Tools
description: During the training execution, sentences present in parallel documents are paired or aligned. Custom translation learns translations one sentence at a time, by reading a sentence and translating it. Then it aligns words and phrases in these two sentences to each other.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.date: 11/18/2025
ms.author: lajanuar
ms.topic: concept-article
ms.custom: cogserv-non-critical-translator
#Customer intent: As a custom translation user, I want to know how sentence alignment works, so that I can have better understanding of underlying process of sentence extraction, pairing, filtering, aligning.
---

# Foundry Tools custom translation sentence pairing and alignment

After documents are uploaded, sentences present in parallel documents are paired or aligned. Custom translation reports the number of sentences it was able to pair as the Aligned Sentences in each of the data sets.

## Pairing and alignment process

Custom translation learns translations of sentences one sentence at a time. It reads a sentence from the source text, and then the translation of this sentence from the target text. Then it aligns words and phrases in these two sentences to each other. This process enables it to create a map of the words and phrases in one sentence to the equivalent words and phrases in the translation of the sentence. Alignment tries to ensure that the system trains on sentences that are translations of each other.

## Prealigned documents

If you know you have parallel documents, you can override the sentence alignment by supplying prealigned text files. You can extract all sentences from both documents into text file, organized one sentence per line, and upload with an `.align` extension. The `.align` extension signals Custom Translation that it should skip sentence alignment.

For best results, try to make sure that you have one sentence per line in your files. Don't have newline characters within a sentence—it causes poor alignments.

## Suggested minimum number of sentences

For a training to succeed, the following table shows the minimum number of sentences required in each document type. This limitation is a safety net to ensure your parallel sentences contain enough unique vocabulary to successfully train a translation model. The general guideline is having more in-domain parallel sentences of human translation quality should produce higher-quality models.

| Document type   | Suggested minimum sentence count | Maximum sentence count |
|------------|--------------------------------------------|--------------------------------|
| Training   | 10,000                                     | No upper limit                 |
| Tuning     | 500                                      | 2,500       |
| Testing    | 500                                      | 2,500  |
| Dictionary | 0                                          | 250,000                 |

> [!NOTE]
>
> - Training doesn't start and fails if the 10,000 minimum sentence count for training isn't met.
> - Tuning and testing are optional. If you don't provide them, the system removes an appropriate percentage from training to use for validation and testing.
> - You can train a model using dictionary data only. For more information, *see* [What is a dictionary](dictionaries.md).
> - The Document Translation feature is recommended for training with dictionaries that contain more than 250,000 sentences. For more information, *see* [Document Translation](../../../document-translation/overview.md).
> - Free (F0) subscription training has a maximum limit of 2,000,000 characters.

## Next steps

> [!div class="nextstepaction"]
> [Learn how to use a dictionary](dictionaries.md)
