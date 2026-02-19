---
title: Characteristics and limitations for LUIS
titleSuffix: Foundry Tools
description: Characteristics and limitations for Language Understanding
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.subservice: azure-ai-luis
ms.date: 02/08/2024
---

# Characteristics and limitations for using Language Understanding

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

Performance with Language Understanding (LUIS) will vary based on the scenario, input data, and enabled features. The following sections are designed to help the reader understand key concepts about performance as they apply to LUIS.

## Understand and measure performance

The performance of LUIS is measured by examining the predicted intents and entities for a user's utterances and how well the system recognizes the custom natural language processing (NLP) concepts (at a threshold value in comparison with a human judge). Comparing the human judge's performance with the custom recognized intents and entities allows the developer to classify the events into two kinds of correct (or "true") events and two kinds of incorrect (or "false") events. The following table shows the options by using a "Make call" intent as an example.

| Term | Correct/Incorrect | Definition | Example |
|----|----|----|----|
| True positive | Correct | The system returns the same results that would be expected from a human judge. | For the utterance "Make a phone call to Sarah," the system correctly predicts the intent as "Make call." |
| True negative | Correct | The system doesn't return a result, which aligns with what would be expected from a human judge. | For the utterance "Turn off the lights," the system doesn't predict this utterance as a "Make call" intent and predicts it as a "None" intent. |
| False positive | Incorrect | The system returns an incorrect result where a human judge wouldn't. | For the utterance "Turn off the lights," the system incorrectly predicts the intent as "Make call." |
| False negative | Incorrect | The system doesn't return a result when a human judge would return a correct result. | For the utterance "I need to call Sarah to tell her that I am late," the system incorrectly predicts this utterance as a "None" intent. |

Errors that happen with LUIS are mostly dependent on the utterances provided as training data for each intent during the authoring phase. Any application of LUIS will experience both false negative and false positive errors. Developers need to consider how each type of error will affect the overall system and carefully think through scenarios where true events won't be recognized and incorrect events will be recognized. Customers should assess the downstream effects that will be in the implementation and understand the consequences of both types of errors on their client application. Developers should create ways to identify, report, and respond to each type of error.

Given that a LUIS prediction response triggers the client application to perform a specific action, if the prediction is incorrect, the client application will perform an action different than the intended one. For example, suppose the user utterance was "I need to make a phone call to Sarah" and the predicted intent from LUIS was a "None" intent. In this case, the client application won't go through the "making a call" logic and will be unable to perform the expected action properly. Handling this error from the client application side is the short-term solution. The system would expect another clear input from the user similar to the utterances given to the system during authoring like "Make call."

The more reliable solution is to review the user's traffic in LUIS and add the incorrectly predicted utterances to the correct intent to be retrained and republished. Developers may want to give the end-users a way to report errors like these, so that they can improve the LUIS model over time. Developers need to periodically plan to review the performance of the deployed system to ensure errors are being handled appropriately.

## System limitations and best practices for enhancing system performance

* **Understand service limitations:** There are some service limitations such as number of intents per application and number of example utterances per intent. [Learn more on system limitations](/azure/ai-services/luis/luis-limits).
* **Plan application schema:** Think about end-user utterances and the main actions that the client application will perform based on these utterances. Developers need to plan the LUIS application schema accordingly with the intents, example utterances, and entities to be extracted. This step is essential, and we advise all LUIS users to do it. [Learn more](/azure/ai-services/luis/concepts/application-design).
* **Quality of training data:** The quality of example utterances provided during training impacts the end results. Carefully choose realistic example utterances for training the model. Capture a variety of different example utterances expected to be sent from the end-users with varied terminologies and contextual differences. Beware of using sensitive information in example utterances that are added during authoring. For example, don't add a real credit card number in an example utterance. Example utterances are saved in LUIS storage accounts to train models. [Learn more](/azure/ai-services/luis/data-collection#data-used-in-luis).
* **Build models by using real world data:** Avoid using automatically generated data because then the model learns a fixed grammar, which diminishes the model’s ability to generalize across different ways of speaking. A good practice is to deploy a simple model and start collecting data that's used in training the final model. This practice helps give an understanding of how users are shifting and how they might express different things over time.
* **Regularly review endpoint utterances:** Enable [active learning feature](/azure/ai-services/luis/how-to/improve-application#log-user-queries-to-enable-active-learning) to review endpoint utterances. This feature gives the customer insight on how the model is performing. Based on performance, developers can modify example utterances, retrain, and republish the application to improve the model's prediction accuracy. If the customer decides to enable this feature, it is advised to inform the end-users that their utterances are being saved during processing. [Learn more](/azure/ai-services/luis/data-collection#data-review-after-luis-app-is-in-production).
* **Provide secondary paths:** LUIS may not perform well when used with speech to text in situations with a lot of background noise or for people with speaking difficulties and speech impairments. Ensure there's always a secondary path for users to enact commands when LUIS does not perform as expected.

## General guidelines to understand and improve performance

The following guidelines helps understand and improve performance in LUIS.

### Understand confidence scores

Depending on system configuration, LUIS might return a confidence score for the detected intent and entity models as part of the system's prediction response. In the latest [V3 prediction endpoint](https://westus.dev.cognitive.microsoft.com/docs/services/luis-endpoint-api-v3-0/operations/5cb0a91e54c9db63d589f433), if the user enables the "show-all-intent" flag in the prediction endpoint, LUIS returns all intents that were created along with the confidence score for each intent. If the flag is disabled, only the top scoring intent returns along with its score.

The top two intents can have a very small score difference between them. LUIS doesn't indicate this proximity. It only returns the scores for each intent or the score of the top intent depending on whether the flag is enabled or not. For entities, the "verbose" flag must be enabled to return the scores of the detected entities along with an array of detailed information per entity. If the flag is disabled, only the detected entities return.

These scores serve as an indicator of how confident the service is with the system's response. A higher value indicates that the service is more confident that the result is accurate.

A confidence score is between zero (0) and one (1). A highly confident LUIS score is 0.99. A low confidence score is 0.01. The returned score is directly affected by the data provided during the authoring of the application.

If the user's input is similar to the trained utterances, a higher score intent is returned and more accurate entities are extracted. If user input is different than the utterances provided during the authoring phase, scores are lower.

To obtain an accurate prediction and a high confidence score, provide multiple variations of an utterance with the same meaning.

### Set confidence score thresholds

Developers may choose to make decisions in the system based on the intent confidence score the system returns. The confidence score threshold the system uses can be adjusted to meet the required needs. If it's more important to identify all potential intents of the text, use a lower threshold. This means that you might get more false positives but fewer false negatives.

If it's more important for the system to recognize only true intents of the text being analyzed, use a higher threshold. When using a higher threshold, you might get fewer false positives but more false negatives.

Different intent scenarios call for different approaches. For example, if there is an intent for greetings or starting the bot, a developer may accept a lower threshold (0.40, for example) as they would want to accept multiple variations of the incoming text. But if there is an intent for a specific action like making a phone call, the developer would probably want to set a higher threshold (0.95, for example) to ensure accuracy of the predicted text.

Returning and reviewing all intent scores is a good way to verify that the correct intent is identified, and also that the next identified intent's score is significantly and consistently lower.

If multiple intents have close prediction scores, the developer might want to review and add to more example utterances for each intent. Define a threshold for the delta score between the top two intents. If the difference is lower than the threshold defined, make programmatic choices about handling such cases.

It's critical to test the system with any thresholds being added by using real data that the system will process in production to determine the effects of various threshold values. At any point, you can always continue to add example utterances with a wider variety of contextual differences and republish the application.

### Different training sessions can result in different predictions

When training an intent model in a LUIS application, the system chooses a set of random example utterances from all the other intents created as negative examples. With each training iteration, the random set of negative examples changes. This turnover affects the scores returned from the system on the same example utterance being predicted.

This difference occurs because there's non-deterministic training. In other words, there's an element of randomness. This randomness can also cause an overlap of an utterance to more than one intent. This means that the top intent for the same utterance can change based on training. For example, the top score could become the second top score, and the second top score could become the first top score.

 To prevent this situation, add example utterances to each of the top two intents for that utterance with word choice and context that differentiates the two intents. The two intents should have about the same number of example utterances. A rule of thumb for separation to prevent inversion because of training is a 15 percent difference in scores.

Customers can choose to turn off the non-deterministic training. The system will then train an intent with all the data provided to the other intents as negative examples instead of training by using a small random percentage of the other intent's data.

### Improve accuracy by using patterns when several utterances are similar

A [Pattern](/azure/ai-services/luis/concepts/patterns-features) in LUIS is a template utterance assigned to an intent. It contains syntax to identify entities and ignorable text.

Patterns are another feature that can be used to increase the confidence scores for intent and entity prediction without providing many more utterances. Use patterns when an intent score is low or if the correct intent's score is close to the top scoring intent.

Be aware that setting an intent for a template utterance in a pattern isn't a guarantee of the intent prediction, but it's a strong signal. Understand how [to can use patterns in LUIS application](/azure/ai-services/luis/luis-how-to-model-intent-pattern).

### Review incorrect predictions to improve performance

LUIS customers can improve the application's prediction accuracy if the active learning feature is enabled. If the "log" flag is enabled in the prediction API, LUIS logs the user queries and selects those that need validation to be added to a review list. The utterances are added to the review list when the top firing intent has a low confidence score or the top two intents' confidence scores are too close.

The app owner or contributor reviews and validates the selected utterances, which include the correct intent and any entities within the intent. If an utterance wasn't correctly predicted, the user has the option to add this utterance as an example utterance of the correct intent and extract the correct entities from it. If scores of the same top two intents are close for a number of endpoint utterances, add more example utterances to each intent with a wider variety of contextual differences, train and publish the app again.

Reviewing suggested utterances should be part of the regular maintenance for the LUIS application to ensure that it keeps returning correct predictions of a high score. Learn about [fixing unsure predictions by reviewing endpoint utterances](/azure/ai-services/luis/how-to/improve-application).

### Quality of the incoming text to the system will affect results

LUIS only processes text. The fidelity and formatting of the incoming text will affect the performance of the system. Make sure to consider the following:

* Speech transcription quality might affect the quality of the results. If the source data is voice, make sure to use the highest quality combination of automatic and human transcription to ensure the best performance. Consider using custom speech models to obtain better quality results.
* Lack of standard punctuation or casing might affect the quality of the results. If using a speech system, like Azure Speech in Foundry Tools to Text, be sure to select the option to include punctuation.
* Frequent misspellings in the training data might affect the confidence of the response. Consider using a spell-checking service to correct misspelled words. You can easily integrate with [Bing Spell Check](/azure/ai-services/luis/luis-tutorial-bing-spellcheck).
* Spell-checking could be introduced, but it might not always be the best solution to include. In all cases, the use of actual data, including spelling mistakes, would be best.
* The training data for LUIS models is provided by the application owner. Data that most closely resembles the training data yields the best performance.

### Performance varies across features and languages

LUIS has a variety of features within the service. Not all features are at the same language parity. For example, language support varies for prebuilt entities and prebuilt domains. You might find that performance for a particular feature isn't consistent with another feature. Also, you might find that for a particular feature that performance isn't consistent across various languages. Understand [language support across all LUIS features](/azure/ai-services/luis/luis-language-support#languages-supported).

## Next steps

* [Introduction to Language Understanding](/azure/ai-services/luis/what-is-luis)
* [Language Understanding transparency note](luis-transparency-note.md)
* [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai?rtc=1&activetab=pivot1%3aprimaryr6)
* [Building responsible bots](https://www.microsoft.com/research/uploads/prod/2018/11/Bot_Guidelines_Nov_2018.pdf)
