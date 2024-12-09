---
title: Multilingual projects
titleSuffix: Azure AI services
description: Learn about how to make use of multilingual projects in conversational language understanding.
#services: cognitive-services
author: jboback
manager: nitinme
ms.service: azure-ai-language
ms.topic: conceptual
ms.date: 11/21/2024
ms.author: jboback
---

# Multilingual projects

Conversational language understanding makes it easy for you to extend your project to several languages at once. When you enable multiple languages in projects, you can add language-specific utterances and synonyms to your project. You can get multilingual predictions for your intents and entities.

## Multilingual intent and learned entity components

When you enable multiple languages in a project, you can train the project primarily in one language and immediately get predictions in other languages.

For example, you can train your project entirely with English utterances and query it in French, German, Mandarin, Japanese, Korean, and others. Conversational language understanding makes it easy for you to scale your projects to multiple languages by using multilingual technology to train your models.

Whenever you identify that a particular language isn't performing as well as other languages, you can add utterances for that language in your project. In the [tag utterances](../how-to/tag-utterances.md) page in Language Studio, you can select the language of the utterance you're adding. When you introduce examples for that language to the model, it's introduced to more of the syntax of that language and learns to predict it better.

You aren't expected to add the same number of utterances for every language. You should build most of your project in one language and only add a few utterances in languages that you observe aren't performing well. If you create a project that's primarily in English and start testing it in French, German, and Spanish, you might observe that German doesn't perform as well as the other two languages. In that case, consider adding 5% of your original English examples in German, train a new model, and test in German again. You should see better results for German queries. The more utterances you add, the more likely the results are going to get better.

When you add data in another language, you shouldn't expect it to negatively affect other languages.

## List and prebuilt components in multiple languages

Projects with multiple languages enabled allow you to specify synonyms *per language* for every list key. Depending on the language you query your project with, you only get matches for the list component with synonyms of that language. When you query your project, you can specify the language in the request body:

```json
"query": "{query}"
"language": "{language code}"
```

If you don't provide a language, it falls back to the default language of your project. For a list of different language codes, see [Language support](../language-support.md).

Prebuilt components are similar, where you should expect to get predictions for prebuilt components that are available in specific languages. The request's language again determines which components are attempting to be predicted. For information on the language support of each prebuilt component, see the [Supported prebuilt entity components](../prebuilt-component-reference.md).

## Related content

* [Tag utterances](../how-to/tag-utterances.md) 
* [Train a model](../how-to/train-model.md)
