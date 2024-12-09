---
title: Conversational Language Understanding None Intent
titleSuffix: Azure AI services
description: Learn about the default None intent in conversational language understanding.
#services: cognitive-services
author: jboback
manager: nitinme
ms.service: azure-ai-language
ms.topic: conceptual
ms.date: 11/21/2024
ms.author: jboback
ms.custom: language-service-clu
ms.reviewer: haelhamm
---

# None intent

Every project in conversational language understanding includes a default None intent. The None intent is a required intent and can't be deleted or renamed. The intent is meant to categorize utterances that don't belong to any of your other custom intents.

An utterance can be predicted as the None intent if the top scoring intent's score is *lower* than the None score threshold. It can also be predicted if the utterance is similar to examples added to the None intent.

## None score threshold

You can go to the **project settings** of any project and set the **None score threshold**. The threshold is a decimal score from **0.0** to **1.0**. 

For any query and utterance, the highest scoring intent ends up *lower* than the threshold score, so the top intent is automatically replaced with the None intent. The scores of all the other intents remain unchanged.

The score should be set according to your own observations of prediction scores because they might vary by project. A higher threshold score forces the utterances to be more similar to the examples you have in your training data.

When you export a project's JSON file, the None score threshold is defined in the `settings` parameter of the JSON as the `confidenceThreshold`. The threshold accepts a decimal value between 0.0 and 1.0.

> [!NOTE]
> During model evaluation of your test set, the None score threshold isn't applied.

## Add examples to the None intent

The None intent is also treated like any other intent in your project. If there are utterances that you want predicted as None, consider adding similar examples to them in your training data. If you want to categorize utterances that aren't important to your project as None, add those utterances to your intent. Examples might include greetings, yes-and-no answers, and responses to questions such as providing a number.

You should also consider adding false positive examples to the None intent. For example, in a flight booking project it's likely that the utterance "I want to buy a book" could be confused with a Book Flight intent. You can add "I want to buy a book" or "I love reading books" as None training utterances. They help to alter the predictions of those types of utterances toward the None intent instead of Book Flight.

## Related content

- [Conversational language understanding overview](../overview.md)
