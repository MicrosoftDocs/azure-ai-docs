---
title: Characteristics and limitations for CLU
titleSuffix: Foundry Tools
description: Characteristics and limitations for using conversational language understanding.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 09/15/2021
---

# Characteristics and limitations for using conversational language understanding

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

Performance with conversational language understanding (CLU) varies based on the scenario, input data, and enabled features. The following sections are designed to help the reader understand key concepts about performance as they apply to CLU.

## Understand and measure performance

The performance of CLU is measured by examining the predicted intents and entities for a given utterance and how well the system recognizes the custom natural language processing (NLP) concepts (at a threshold value in comparison with a human judge). In the process of building a model, training and testing sets are either defined by developers during tagging or chosen at random during training. The training set is used to train the custom model, while the testing set is used as a blind set to evaluate the model's performance.

The model evaluation process is triggered after training is completed successfully. The evaluation process takes place by using the trained model to predict user-defined entities from the testing set and compare them with the provided data tags (ground truth). The results are returned to the developer to review the model's performance.

The first step in calculating the model's evaluation is categorizing the extracted entities in one of the following categories: true positives, false positives, or false negatives. The following table shows the options by using a "Make call" intent as an example.

| Term | Correct/Incorrect | Definition | Example |
|----|----|----|----|
| True positive | Correct | The system returns the same results that would be expected from a human judge. | For the utterance "Make a phone call to Sarah," the system correctly predicts the intent as "Make call." |
| False positive | Incorrect | The system returns an incorrect result where a human judge wouldn't. | For the utterance "Turn off the lights," the system incorrectly predicts the intent as "Make call." |
| False negative | Incorrect | The system doesn't return a result when a human judge would return a correct result. | For the utterance "I need to call Sarah to tell her that I am late," the system incorrectly predicts this utterance as a "Schedule meeting" intent. |

The preceding categories are then used to calculate *precision*, *recall* and *F1 score*. These metrics are provided to developers as part of the service's model evaluation. Here are the metric definitions and how they're calculated:

- **Precision**: The ratio between the true positives and all the positives. Out of predicted positive classes, precision reveals how many of them are actual positives (belong to the right entity type as predicted).
- **Recall**: The measure of the model's ability to extract actual positive entities. It's the ratio between the predicted true positives and the actually tagged positives. Out of actual tagged entities, recall reveals how many of them are predicted correctly.
- **F1 score**: A function of precision and recall. You need it when you seek a balance between precision and recall.

Errors that happen with CLU are mostly dependent on the utterances provided as training data. Any CLU model experiences both false negative and false positive errors. Developers need to consider how each type of error affects the overall system and carefully think through scenarios where true events won't be recognized and incorrect events are recognized. Customers should assess the downstream effects that occur in the implementation and understand the consequences of both types of errors on their client application. Developers should create ways to identify, report, and respond to each type of error.

Given that a CLU prediction response triggers the client application to perform a specific action, if the prediction is incorrect, the client application performs an action different to the intended one. Depending on the scenario, *precision* or *recall* could be a more suitable metric for evaluating your model's performance.

For example, suppose the user utterance was "I need to make a phone call to Sarah" and the predicted intent from CLU was a "Schedule meeting" intent. In this case, the client application won't go through the "making a call" logic and will be unable to perform the expected action properly. The system should then be more sensitive to false positives, and precision would be a more relevant metric for evaluation in this scenario. Handling this error from the client application side is the short-term solution. The system would expect another clear input from the user similar to the example utterances given to the system before training like "Make call."

## System limitations and best practices for enhancing system performance

* **Understand service limitations:** Be aware of service limitations such as number of intents per project and number of example utterances per intent. [Learn more on service limits](/azure/ai-services/language-service/conversational-language-understanding/service-limits)
* **Plan schema:** Think about user utterances and the main actions that the client application will perform based on these utterances. Developers need to plan the CLU project schema accordingly with the intents, example utterances, and entities to be extracted. This step is essential, and we advise all CLU users to do it. [Learn more](/azure/ai-services/language-service/conversational-language-understanding/how-to/build-schema)
* **Use good training data:** The quality of example utterances provided during training affects the end results. Carefully choose realistic example utterances for training the model. Capture a variety of different example utterances expected to be sent from the users with varied terminologies and contextual differences. Beware of using sensitive information in example utterances that are added during tagging. For example, don't add a real credit card number in an example utterance. Example utterances are saved in CLU storage accounts to train models.
* **Build models by using real-world data:** Avoid using automatically generated data because then the model learns a fixed grammar, which diminishes the model's ability to generalize across different ways of speaking. A good practice is to deploy a simple model and start collecting data that's used in training the final model. This practice helps give an understanding of how users are shifting and how they might express different things over time.
* **Review evaluation and improve model:** After the model was trained successfully, check the model evaluation and [confusion matrix](/azure/ai-services/language-service/conversational-language-understanding/concepts/evaluation-metrics#confusion-matrix). This review helps you understand where your model went wrong and learn about entities/intents that aren't performing well. It's also considered as a best practice to [review the testing set](/azure/ai-services/language-service/conversational-language-understanding/how-to/train-model#evaluate-model) and view the predicted and tagged entities side by side. It helps you to gauge the model's performance and decide if any changes in the schema or the tags are necessary.
* **Provide secondary paths:** CLU might not perform well when used with speech to text in situations with a lot of background noise or for people with speaking difficulties and speech impairments. Ensure there's always a secondary path for users to enact commands when the cloud doesn't perform as expected.

## General guidelines to understand and improve performance

The following guidelines help you understand and improve performance in CLU.

### Understand confidence scores

If you're content with the model's performance after training, the model should then be deployed to be consumed in a production environment. Deploying a model means making it available for use via the [analyze-conversation API](https://westus2.dev.cognitive.microsoft.com/docs/services/Language-2021-11-01-preview/operations/ConversationAnalysis_AnalyzeConversations) to detect the intent and extract entities from a given text. The API returns a JSON object containing a list of all intents that were created along with their confidence scores and the extracted entities each with its start index, length, and confidence score.

These scores serve as an indicator of how confident the service is with the system's response. A higher value indicates the service is more confident that the result is accurate. A confidence score is between zero (0) and one (1), zero being no confidence and 1 being high confidence. The returned score is directly affected by the data provided during tagging data.

The top two intents can have a very small score difference between them. CLU doesn't indicate proximity. It only returns the scores for each created intent, which is calculated independently.

If the user's input is similar to utterances in the training data, an intent with a higher score will be returned, and more accurate entities are extracted. If user input is different from the utterances in the training data, scores are lower. To obtain an accurate prediction and a high confidence score, provide multiple variations of an utterance with the same meaning.

### Set confidence score thresholds

You might choose to make decisions in the system based on the intent confidence score the system returns. The confidence score threshold the system uses can be adjusted to meet the needs in your scenario. If it's more important to identify all potential intents of the text, use a lower threshold. As a result, you might get more false positives but fewer false negatives. If it's more important for the system to recognize only true intents of the text being analyzed, use a higher threshold.

Different intent scenarios call for different approaches. For example, if there's an intent for greetings or starting the bot, you might accept a lower threshold (0.40, for example) because you want to accept multiple variations of the incoming text. But if there's an intent for a specific action like making a phone call, you might want to set a higher threshold (0.95, for example) to ensure accuracy of the predicted text. Returning and reviewing all intent scores is a good way to verify that the correct intent is identified. The difference between the confidence scores of the top returned intent and the next best returned intent should be significant.

If multiple intents have close prediction scores, you might want to review and add more example utterances for each intent. Define a threshold for the difference between the top two intents. If the difference is lower than the threshold defined, make programmatic choices about handling such cases.

It's critical to test the system with any thresholds being added by using real data that the system will process in production to determine the effects of various threshold values. At any point, you can always continue to add example utterances with a wider variety of contextual differences and retrain and redeploy your model.

### Different training sessions and changes in evaluation

Retraining the same model without any changes in tagged data results in the same model output, and as a result, the same evaluation scores. If you add or remove tags, the model performance changes accordingly. The evaluation scores can then be compared with the previous version of the model because both have the same files in the training and testing sets, provided that no new files were added during tagging.

Adding new files or training a different model with random set splits leads to different files in training and testing sets. Although changes in evaluation scores might be noticed, they can't be directly compared to other models because performance is calculated on different splits for testing sets.

### Quality of the incoming text to the system affects results

CLU only processes text. The fidelity and formatting of the incoming text affects the performance of the system. Make sure to consider the following:

* Speech transcription quality might affect the quality of the results. If the source data is voice, use the highest quality combination of automatic and human transcription to ensure the best performance. Consider using custom speech models to obtain better-quality results.
* Lack of standard punctuation or casing might affect the quality of the results. If you're using a speech system, like Azure Speech in Foundry Tools to Text, select the option to include punctuation.
* Frequent misspellings in the training data might affect the confidence of the response. Consider using a spell-checking service to correct misspelled words. However, introducing spell-checking may not be the best solution. In all cases, the use of actual data, including spelling mistakes, provides the best results.
* The training data for CLU models is provided by the developer. Data used in production that most closely resembles the training data yields the best performance.

### Performance varies across features and languages

CLU gives users the option to use data in multiple languages. Developers can have multiple files in a dataset with different languages. A model that's trained with one language can be used to query text in other languages. Enable the multilingual option during project creation. If low scores in a certain language are noticed, consider adding more data in this language to your training set.

Not all features are at the same language parity. For example, language support in CLU varies for prebuilt entities. You might find that performance for a particular feature isn't consistent with another feature. Also, you might find that for a particular feature that performance isn't consistent across various languages. Understand [language support across CLU](/azure/ai-services/language-service/conversational-language-understanding/language-support).

## Next steps

* [Introduction to conversational language understanding](/azure/ai-services/language-service/conversational-language-understanding/overview)
* [Language Understanding transparency note](/azure/ai-foundry/responsible-ai/luis/luis-transparency-note)

* [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai?rtc=1&activetab=pivot1%3aprimaryr6)
* [Building responsible bots](https://www.microsoft.com/research/uploads/prod/2018/11/Bot_Guidelines_Nov_2018.pdf)
