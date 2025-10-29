---
title: Utterances
description: Utterances concepts
ms.service: azure-ai-language
ms.author: lajanuar
author: laujan
ms.manager: nitinme
ms.subservice: azure-ai-luis
ms.topic: conceptual
ms.date: 06/12/2025
---
# Utterances

[!INCLUDE [deprecation notice](../includes/deprecation-notice.md)]


Utterances are inputs from users that your app needs to interpret. To train LUIS to extract intents and entities from these inputs, it's important to capture various different example utterances for each intent. Active learning, or the process of continuing to train on new utterances, is essential to the machine-learning intelligence that LUIS provides.

Collect utterances that you think users will enter. Include utterances, which mean the same thing but are constructed in various ways:

* Utterance length - short, medium, and long for your client-application
* Word and phrase length
* Word placement - entity at beginning, middle, and end of utterance
* Grammar
* Pluralization
* Stemming
* Noun and verb choice
* [Punctuation](../luis-reference-application-settings.md#punctuation-normalization) - using both correct and incorrect grammar

## Choose varied utterances

When you start  [adding example utterances](../how-to/entities.md) to your LUIS model, there are several principles to keep in mind:

## Utterances aren't always well formed

Your app might need to process sentences, like "Book a ticket to Paris for me," or a fragment of a sentence, like "Booking" or "Paris flight" Users also often make spelling mistakes. When planning your app, consider whether or not you want to use [Bing Spell Check](../luis-tutorial-bing-spellcheck.md) to correct user input before passing it to LUIS.

If you don't spell check user utterances, you should train LUIS on utterances that include typos and misspellings.

### Use the representative language of the user

When choosing utterances, be aware that what you think are common terms or phrases might not be common for the typical user of your client application. They might not have domain experience or use different terminology. Be careful when using terms or phrases that a user would only say if they were an expert.

### Choose varied terminology and phrasing

You'll find that even if you make efforts to create varied sentence patterns, you'll still repeat some vocabulary. For example, the following utterances have similar meaning, but different terminology and phrasing:

* "*How do I get a computer?*"
* "*Where do I get a computer?*" 
* "*I want to get a computer, how do I go about it?*"
* "*When can I have a computer?*"

The core term here, _computer_, isn't varied. Use alternatives such as desktop computer, laptop, workstation, or even just machine. LUIS can intelligently infer synonyms from context, but when you create utterances for training, it's always better to vary them.

## Example utterances in each intent

Each intent needs to have example utterances - at least 15. If you have an intent that doesn't have any example utterances, you will not be able to train LUIS. If you have an intent with one or few example utterances, LUIS might not accurately predict the intent.

## Add small groups of utterances

Each time you iterate on your model to improve it, don't add large quantities of utterances. Consider adding utterances in quantities of 15. Then [Train](../how-to/train-test.md), [publish](../how-to/publish.md), and [test](../how-to/train-test.md) again.

LUIS builds effective models with utterances that are carefully selected by the LUIS model author. Adding too many utterances isn't valuable because it introduces confusion.

It's better to start with a few utterances, then [review the endpoint utterances](../how-to/improve-application.md) for correct intent prediction and entity extraction.

## Utterance normalization

Utterance normalization is the process of ignoring the effects of types of text, such as punctuation and diacritics, during training and prediction.

Utterance normalization settings are turned off by default. These settings include:

* Word forms
* Diacritics
* Punctuation

If you turn on a normalization setting, scores in the  **Test**  pane, batch tests, and endpoint queries will change for all utterances for that normalization setting.

When you clone a version in the LUIS portal, the version settings are kept in the new cloned version.

Set your app's version settings using the LUIS portal by selecting **Manage**  from the top navigation menu, in the  **Application Settings**  page. You can also use the [Update Version Settings API](/rest/api/luis/settings/update). See the  [Reference](../luis-reference-application-settings.md) documentation for more information.

## Word forms

Normalizing  **word forms**  ignores the differences in words that expand beyond the root.

## Diacritics

Diacritics are marks or signs within the text, such as:

`İ ı Ş Ğ ş ğ ö ü`

## Punctuation marks

Normalizing  **punctuation**  means that before your models get trained and before your endpoint queries get predicted, punctuation will be removed from the utterances.

Punctuation is a separate token in LUIS. An utterance that contains a period at the end is a separate utterance than one that doesn't contain a period at the end, and might get two different predictions.

If punctuation isn't normalized, LUIS doesn't ignore punctuation marks by default because some client applications might place significance on these marks. Make sure to include example utterances that use punctuation, and ones that don't, for both styles to return the same relative scores.

Make sure the model handles punctuation either in the example utterances (both having and not having punctuation) or in [patterns](../concepts/patterns-features.md) where it is easier to ignore punctuation. For example: I am applying for the {Job} position[.]

If punctuation has no specific meaning in your client application, consider [ignoring punctuation](../concepts/utterances.md#utterance-normalization) by normalizing punctuation.

## Ignoring words and punctuation

If you want to ignore specific words or punctuation in patterns, use a [pattern](../concepts/patterns-features.md) with the _ignore_ syntax of square brackets, `[]`.

## Training with all utterances

Training is nondeterministic: utterance prediction can vary slightly across versions or apps. You can remove nondeterministic training by updating the [version settings](/rest/api/luis/settings/update) API with the UseAllTrainingData name/value pair to use all training data.

## Testing utterances

Developers should start testing their LUIS application with real data by sending utterances to the [prediction endpoint](../luis-how-to-azure-subscription.md) URL. These utterances are used to improve the performance of the intents and entities with [Review utterances](../how-to/improve-application.md). Tests submitted using the testing pane in the LUIS portal aren't sent through the endpoint, and don't contribute to active learning.

## Review utterances

After your model is trained, published, and receiving [endpoint](../luis-glossary.md#endpoint) queries, [review the utterances](../how-to/improve-application.md) suggested by LUIS. LUIS selects endpoint utterances that have low scores for either the intent or entity.

## Best practices

### Label for word meaning

If the word choice or word arrangement is the same, but doesn't mean the same thing, don't label it with the entity.

In the following utterances, the word fair is a homograph, which means it's spelled the same but has a different meaning:
* "*What kinds of county fairs are happening in the Seattle area this summer?*" 
* "*Is the current 2-star rating for the restaurant fair?*

If you want an event entity to find all event data, label the word fair in the first utterance, but not in the second.

### Don't ignore possible utterance variations

LUIS expects variations in an intent's utterances. The utterances can vary while having the same overall meaning. Variations can include utterance length, word choice, and word placement.


| Don't use the same format | Do use varying formats |
|--|--|
| Buy a ticket to Seattle|Buy 1 ticket to Seattle|
|Buy a ticket to Paris|Reserve two tickets on the red eye to Paris next Monday|
|Buy a ticket to Orlando |I would like to book 3 tickets to Orlando for spring break |


The second column uses different verbs (buy, reserve, book), different quantities (1, &"two", 3), and different arrangements of words but all have the same intention of purchasing airline tickets for travel.

### Don't add too many example utterances to intents

After the app is published, only add utterances from active learning in the development lifecycle process. If utterances are too similar, add a pattern.

## Next steps

* [Intents](intents.md)
* [Patterns and features concepts](patterns-features.md)
