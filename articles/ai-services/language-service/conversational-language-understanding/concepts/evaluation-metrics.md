---
title: Conversational language understanding model concepts
titleSuffix: Foundry Tools
description: "Learn core concepts for conversational language understanding models: evaluation metrics, the None intent, and accepted data formats."
author: laujan
manager: mcleans
ms.service: azure-language-foundry-tools
ms.topic: concept-article
ms.date: 06/30/2026
ms.author: lajanuar
ms.custom: language-service-clu
---
<!-- markdownlint-disable MD025 -->
# Conversational language understanding model concepts

This article covers core concepts for building and evaluating conversational language understanding (CLU) models, including how to measure model performance, the default None intent, and the data formats that CLU accepts.

## Evaluation metrics

Your [dataset is split](../how-to/build-train-deploy-model.md#data-splitting) into two parts: a set for training and a set for testing. The training set is used to train the model, while the testing set is used as a test for model after training to calculate the model performance and evaluation. The testing set isn't introduced to the model through the training process to make sure that the model is tested on new data.

Model evaluation is triggered automatically after training is completed successfully. The evaluation process starts by using the trained model to predict user-defined intents and entities for utterances in the test set. Then the process compares them with the provided tags to establish a baseline of truth. The results are returned so that you can review the model's performance. For evaluation, conversational language understanding uses the following metrics:

* **Precision**: Measures how precise or accurate your model is. It's the ratio between the correctly identified positives (true positives) and all identified positives. The precision metric reveals how many of the predicted classes are correctly labeled.

    `Precision = #True_Positive / (#True_Positive + #False_Positive)`

* **Recall**: Measures the model's ability to predict actual positive classes. It's the ratio between the predicted true positives and what was tagged. The recall metric reveals how many of the predicted classes are correct.

    `Recall = #True_Positive / (#True_Positive + #False_Negatives)`

* **F1 score**: The F1 score is a function of precision and recall. It's needed when you seek a balance between precision and recall.

    `F1 Score = 2 * Precision * Recall / (Precision + Recall)`

Precision, recall, and the F1 score are calculated for:

* Each entity separately (entity-level evaluation).
* Each intent separately (intent-level evaluation).
* For the model collectively (model-level evaluation).

The definitions of precision, recall, and evaluation are the same for entity-level, intent-level, and model-level evaluations. However, the counts for *true positives*, *false positives*, and *false negatives* can differ. For example, consider the following text.

### Example

* Make a response with "thank you very much."
* Reply with saying "yes."
* Check my email please.
* Email to Cynthia that dinner last week was splendid.
* Send an email to Mike.

The intents used are `Reply`, `sendEmail`, and `readEmail`. The entities are `contactName` and `message`.

The model could make the following predictions:

| Utterance | Predicted intent | Actual intent |Predicted entity| Actual entity|
|--|--|--|--|--|
|Make a response with "thank you very much"|Reply|Reply|`thank you very much` as `message` |`thank you very much` as `message` |
|Reply with saying "yes"| sendEmail|Reply|--|`yes` as `message`|
|Check my email please|readEmail|readEmail|--|--|
|Email to Cynthia that dinner last week was splendid|Reply|sendEmail|`dinner last week was splendid` as `message`| `cynthia` as `contactName`, `dinner last week was splendid` as `message`|
|Send an email to Mike|sendEmail|sendEmail|`mike` as `message`|`mike` as `contactName`|

### Intent-level evaluation for Reply intent

| Key | Count | Explanation |
|--|--|--|
| True positive | 1 | Utterance 1 was correctly predicted as `Reply`. |
| False positive | 1 |Utterance 4 was mistakenly predicted as `Reply`. |
| False negative | 1 | Utterance 2 was mistakenly predicted as `sendEmail`. |

**Precision** = `#True_Positive / (#True_Positive + #False_Positive) = 1 / (1 + 1) = 0.5`

**Recall** = `#True_Positive / (#True_Positive + #False_Negatives) = 1 / (1 + 1) = 0.5`

**F1 score** = `2 * Precision * Recall / (Precision + Recall) =  (2 * 0.5 * 0.5) / (0.5 + 0.5) = 0.5 `

### Intent-level evaluation for sendEmail intent

| Key | Count | Explanation |
|--|--|--|
| True positive | 1 | Utterance 5 was correctly predicted as `sendEmail`. |
| False positive | 1 |Utterance 2 was mistakenly predicted as `sendEmail`. |
| False negative | 1 | Utterance 4 was mistakenly predicted as `Reply`. |

**Precision** = `#True_Positive / (#True_Positive + #False_Positive) = 1 / (1 + 1) = 0.5`

**Recall** = `#True_Positive / (#True_Positive + #False_Negatives) = 1 / (1 + 1) = 0.5`

**F1 score** = `2 * Precision * Recall / (Precision + Recall) =  (2 * 0.5 * 0.5) / (0.5 + 0.5) = 0.5 `

### Intent-level evaluation for readEmail intent

| Key | Count | Explanation |
|--|--|--|
| True positive | 1 | Utterance 3 was correctly predicted as `readEmail`. |
| False positive | 0 |--|
| False negative | 0 |--|

**Precision** = `#True_Positive / (#True_Positive + #False_Positive) = 1 / (1 + 0) = 1`

**Recall** = `#True_Positive / (#True_Positive + #False_Negatives) = 1 / (1 + 0) = 1`

**F1 score** = `2 * Precision * Recall / (Precision + Recall) =  (2 * 1 * 1) / (1 + 1) = 1`

### Entity-level evaluation for contactName entity

| Key | Count | Explanation |
|--|--|--|
| True positive | 1 |  `cynthia` was correctly predicted as `contactName` in utterance 4.|
| False positive | 0 |--|
| False negative | 1 | `mike` was mistakenly predicted as `message` in utterance 5. |

**Precision** = `#True_Positive / (#True_Positive + #False_Positive) = 1 / (1 + 0) = 1`

**Recall** = `#True_Positive / (#True_Positive + #False_Negatives) = 1 / (1 + 1) = 0.5`

**F1 score** = `2 * Precision * Recall / (Precision + Recall) =  (2 * 1 * 0.5) / (1 + 0.5) = 0.67`

### Entity-level evaluation for message entity

| Key | Count | Explanation |
|--|--|--|
| True positive | 2 |`thank you very much` was correctly predicted as `message` in utterance 1 and `dinner last week was splendid` was correctly predicted as `message` in utterance 4. |
| False positive | 1 |`mike` was mistakenly predicted as `message` in utterance 5.  |
| False negative | 1 | ` yes` wasn't predicted as `message` in utterance 2. |

**Precision** = `#True_Positive / (#True_Positive + #False_Positive) = 2 / (2 + 1) = 0.67`

**Recall** = `#True_Positive / (#True_Positive + #False_Negatives) = 2 / (2 + 1) = 0.67`

**F1 Score** = `2 * Precision * Recall / (Precision + Recall) =  (2 * 0.67 * 0.67) / (0.67 + 0.67) = 0.67`

### Model-level evaluation for the collective model

| Key | Count | Explanation |
|--|--|--|
| True positive | 6 | Sum of true positives for all intents and entities. |
| False positive | 3| Sum of false positives for all intents and entities.  |
| False negative | 4 | Sum of false negatives for all intents and entities.  |

**Precision** = `#True_Positive / (#True_Positive + #False_Positive) = 6 / (6 + 3) = 0.67`

**Recall** = `#True_Positive / (#True_Positive + #False_Negatives) = 6 / (6 + 4) = 0.60`

**F1 score** = `2 * Precision * Recall / (Precision + Recall) =  (2 * 0.67 * 0.60) / (0.67 + 0.60) = 0.63`

### Confusion matrix

A confusion matrix is an N x N matrix used for model performance evaluation, where N is the number of entities or intents. The matrix compares the expected labels with the ones predicted by the model. The matrix gives a holistic view of how well the model is performing and what kinds of errors it's making.

You can use the confusion matrix to identify intents or entities that are too close to each other and often get mistaken (ambiguity). In this case, consider merging these intents or entities together. If merging isn't possible, consider adding more tagged examples of both intents or entities to help the model differentiate between them.

The highlighted diagonal in the following image shows the correctly predicted entities, where the predicted tag is the same as the actual tag.

:::image type="content" source="../media/confusion-matrix-example.png" alt-text="Screenshot that shows an example Confusion matrix." lightbox="../media/confusion-matrix-example.png":::

You can calculate the intent-level or entity-level and model-level evaluation metrics from the confusion matrix:

* The values in the diagonal are the true positive values of each intent or entity.
* The sum of the values in the intent or entities rows (excluding the diagonal) is the false positive of the model.
* The sum of the values in the intent or entities columns (excluding the diagonal) is the false negative of the model.

Similarly:

* The true positive of the model is the sum of true positives for all intents or entities.
* The false positive of the model is the sum of false positives for all intents or entities.
* The false negative of the model is the sum of false negatives for all intents or entities.

### Guidance

After you train your model, you see some guidance and recommendations on how to improve the model. We recommend that you have a model covering every point in the guidance section.

* **Training set has enough data:** When an intent or entity has fewer than 15 labeled instances in the training data, it can lead to lower accuracy because the model isn't adequately trained on that intent. In this case, consider adding more labeled data in the training set. You should only consider adding more labeled data to your entity if your entity has a learned component. If your entity is defined only by list, prebuilt, and regex components, this recommendation doesn't apply.
* **All intents or entities are present in test set:** When the testing data lacks labeled instances for an intent or entity, the model evaluation is less comprehensive because of untested scenarios. Consider having test data for every intent and entity in your model to ensure that everything is being tested.
* **Unclear distinction between intents or entities:** When data is similar for different intents or entities, it can lead to lower accuracy because they might be frequently misclassified as each other. Review the following intents and entities and consider merging them if they're similar. Otherwise, add more examples to better distinguish them from each other. You can check the **Confusion matrix** tab for more guidance. If you're seeing two entities constantly being predicted for the same spans because they share the same list, prebuilt, or regex components, make sure to add a *learned* component for each entity and make it *required*. Learn more about [entity components](./entity-components.md).

## None intent

Every project in conversational language understanding includes a default None intent. The None intent is a required intent and you can't delete or rename it. Use this intent to categorize utterances that don't belong to any of your other custom intents.

An utterance can be predicted as the None intent if the top scoring intent's score is *lower* than the None score threshold. The model can also predict the None intent if the utterance is similar to examples you add to the None intent.

### None score threshold

Go to the **project settings** of any project and set the **None score threshold**. The threshold is a decimal score from **0.0** to **1.0**. 

For any query and utterance, if the highest scoring intent ends up *lower* than the threshold score, the top intent is automatically replaced with the None intent. The scores of all the other intents remain unchanged.

Set the score according to your own observations of prediction scores because they might vary by project. A higher threshold score forces the utterances to be more similar to the examples you have in your training data.

When you export a project's JSON file, the None score threshold is defined in the `settings` parameter of the JSON as the `confidenceThreshold`. The threshold accepts a decimal value between 0.0 and 1.0.

> [!NOTE]
> During model evaluation of your test set, the None score threshold isn't applied.

### Add examples to the None intent

The None intent is also treated like any other intent in your project. If there are utterances that you want predicted as None, consider adding similar examples to them in your training data. If you want to categorize utterances that aren't important to your project as None, add those utterances to your intent. Examples might include greetings, yes-and-no answers, and responses to questions such as providing a number.

Consider adding false positive examples to the None intent. For example, in a flight booking project it's likely that the utterance "I want to buy a book" could be confused with a Book Flight intent. You can add "I want to buy a book" or "I love reading books" as None training utterances. They help to alter the predictions of those types of utterances toward the None intent instead of Book Flight.

## Data formats

If you're uploading your data into conversational language understanding, it must follow a specific format. Use this section to learn more about accepted data formats.

### Import project file format

If you're [importing a project](../how-to/create-project.md#import-an-existing-foundry-project) into conversational language understanding, upload the file in the following format:

```json
{
  "projectFileVersion": "2022-10-01-preview",
  "stringIndexType": "Utf16CodeUnit",
  "metadata": {
    "projectKind": "Conversation",
    "projectName": "{PROJECT-NAME}",
    "multilingual": true,
    "description": "DESCRIPTION",
    "language": "{LANGUAGE-CODE}",
    "settings": {
            "confidenceThreshold": 0
        }
  },
  "assets": {
    "projectKind": "Conversation",
    "intents": [
      {
        "category": "intent1"
      }
    ],
    "entities": [
      {
        "category": "entity1",
        "compositionSetting": "{COMPOSITION-SETTING}",
        "list": {
          "sublists": [
            {
              "listKey": "list1",
              "synonyms": [
                {
                  "language": "{LANGUAGE-CODE}",
                  "values": [
                    "{VALUES-FOR-LIST}"
                  ]
                }
              ]
            }            
          ]
        },
        "prebuilts": [
          {
            "category": "{PREBUILT-COMPONENTS}"
          }
        ],
        "regex": {
          "expressions": [
              {
                  "regexKey": "regex1",
                  "language": "{LANGUAGE-CODE}",
                  "regexPattern": "{REGEX-PATTERN}"
              }
          ]
        },
        "requiredComponents": [
            "{REQUIRED-COMPONENTS}"
        ]
      }
    ],
    "utterances": [
      {
        "text": "utterance1",
        "intent": "intent1",
        "language": "{LANGUAGE-CODE}",
        "dataset": "{DATASET}",
        "entities": [
          {
            "category": "ENTITY1",
            "offset": 6,
            "length": 4
          }
        ]
      }
    ]
  }
}

```

|Key  |Placeholder  |Value  | Example |
|---------|---------|----------|--|
|`{API-VERSION}`     | The [version](../../concepts/model-lifecycle.md#api-versions) of the API you're calling. | `2023-04-01` |
|`confidenceThreshold`|`{CONFIDENCE-THRESHOLD}`|The threshold score for which the intent is predicted as [None intent](#none-intent). Values are from `0` to `1`.|`0.7`|
| `projectName` | `{PROJECT-NAME}` | The name of your project. This value is case sensitive. | `EmailApp` |
| `multilingual` | `true`| A Boolean value that enables you to have utterances in multiple languages in your dataset. When your model is deployed, you can query the model in any supported language (not necessarily included in your training documents). For more information about supported language codes, see [Language support](../language-support.md#multi-lingual-option). | `true`|
|`sublists`|`[]`|Array that contains sublists. Each sublist is a key and its associated values.|`[]`|
|`compositionSetting`|`{COMPOSITION-SETTING}`|Rule that defines how to manage multiple components in your entity. Options are `combineComponents` or `separateComponents`. |`combineComponents`|
|`synonyms`|`[]`|Array that contains all the synonyms.|synonym|
| `language` | `{LANGUAGE-CODE}` |  A string specifying the language code for the utterances, synonyms, and regular expressions used in your project. If your project is a multilingual project, choose the [language code](../language-support.md) of most the utterances. |`en-us`|
| `intents` | `[]` | Array that contains all the intents you have in the project. These intents are classified from your utterances.| `[]` |
| `entities` | `[]` | Array that contains all the entities in your project. These entities are extracted from your utterances. Every entity can have other optional components defined with them: list, prebuilt, or regex. | `[]` |
| `dataset` | `{DATASET}` |  The test set that this utterance is assigned to when the data is split before training. To learn more about data splitting, see [Train your conversational language understanding model](../how-to/build-train-deploy-model.md#data-splitting). Possible values for this field are `Train` and `Test`.      |`Train`|
| `category` | ` ` |  The type of entity associated with the span of text specified. | `Entity1`|
| `offset` | ` ` |  The inclusive character position of the start of the entity.      |`5`|
| `length` | ` ` |  The character length of the entity.      |`5`|
| `listKey`| ` ` | A normalized value for the list of synonyms to map back to in prediction. | `Microsoft` |
| `values`| `{VALUES-FOR-LIST}` | A list of comma-separated strings that are matched exactly for extraction and map to the list key. | `"msft", "microsoft", "MS"` |
| `regexKey`| `{REGEX-PATTERN}` | A normalized value for the regular expression to map back to in prediction. | `ProductPattern1` |
| `regexPattern`| `{REGEX-PATTERN}` | A regular expression. | `^pre` |
| `prebuilts`| `{PREBUILT-COMPONENTS}` | The prebuilt components that can extract common types. For the list of prebuilts you can add, see [Supported prebuilt entity components](../prebuilt-component-reference.md). | `Quantity.Number` |
| `requiredComponents` | `{REQUIRED-COMPONENTS}` |  A setting that specifies a requirement that a specific component must be present to return the entity. To learn more, see [Entity components](./entity-components.md#required-components). The possible values are `learned`, `regex`, `list`, or `prebuilts`.   |`"learned", "prebuilt"`|

### Utterance file format

Conversational language understanding offers the option to upload your utterances directly to the project rather than typing them in one by one. You can find this option on the [data labeling](../how-to/build-train-deploy-model.md#label-your-utterances) page for your project.

```json
[
    {
        "text": "{Utterance-Text}",
        "language": "{LANGUAGE-CODE}",
        "dataset": "{DATASET}",
        "intent": "{intent}",
        "entities": [
            {
                "category": "{entity}",
                "offset": 19,
                "length": 10
            }
        ]
    },
    {
        "text": "{Utterance-Text}",
        "language": "{LANGUAGE-CODE}",
        "dataset": "{DATASET}",
        "intent": "{intent}",
        "entities": [
            {
                "category": "{entity}",
                "offset": 20,
                "length": 10
            },
            {
                "category": "{entity}",
                "offset": 31,
                "length": 5
            }
        ]
    }
]

```

|Key  |Placeholder  |Value  | Example |
|---------|---------|----------|--|
|`text`|`{Utterance-Text}`|Your utterance text.|Testing|
| `language` | `{LANGUAGE-CODE}` |  A string that specifies the language code for the utterances used in your project. If your project is a multilingual project, choose the language code of most of the utterances. For more information about supported language codes, see [Language support](../language-support.md). |`en-us`|
| `dataset` | `{DATASET}` |  The test set that this utterance is assigned to when the data is split before training. To learn more about data splitting, see [Train your conversational language understanding model](../how-to/build-train-deploy-model.md#data-splitting). Possible values for this field are `Train` and `Test`.      |`Train`|
|`intent`|`{intent}`|The assigned intent.| intent1|
|`entity`|`{entity}`|The entity to be extracted.| entity1|
| `category` | ` ` |  The type of entity associated with the span of text specified. | `Entity1`|
| `offset` | ` ` |  The inclusive character position of the start of the text.      |`0`|
| `length` | ` ` |  The length of the bounding box in terms of UTF16 characters. Training only considers the data in this region.      |`500`|

## Related content

* [Train a model](../how-to/build-train-deploy-model.md#train-your-model)
* [Entity components](./entity-components.md)
* [Label your utterances](../how-to/build-train-deploy-model.md#label-your-utterances)
* [Import project](../how-to/create-project.md#import-an-existing-foundry-project)
* [Conversational language understanding overview](../overview.md)
